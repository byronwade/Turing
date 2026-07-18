#!/usr/bin/env python3
"""Validate no-claim toolkit-neutral UI adapter contract inventories."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
UI_MACHINE = DOCS / "ui-runtime" / "machine"
DEFAULT_INVENTORY = UI_MACHINE / "adapter-contract-inventory.json"

INVENTORY_ID = re.compile(r"^UI\.ADAPTER\.[A-Z0-9._-]+$")
AREA_ID = re.compile(r"^UI-ADAPTER-AREA-[A-Z0-9_-]+$")
INVARIANT_ID = re.compile(r"^UI-ADAPTER-INVARIANT-[A-Z0-9_-]+$")
DENIAL_ID = re.compile(r"^UI-ADAPTER-DENIAL-[A-Z0-9_-]+$")
EVIDENCE_ID = re.compile(r"^UI-ADAPTER-EV-[A-Z0-9_-]+$")

REQUIRED_SOURCE_RECORDS = {
    "crates/turing-ui-model/src/lib.rs",
    "docs/ui-runtime/README.md",
    "docs/ui-runtime/03-rust-state-command-and-adapter-architecture.md",
    "docs/ui-runtime/04-page-surface-compositor-and-process-integration.md",
    "docs/ui-runtime/07-windowing-input-ime-accessibility-and-platform.md",
    "docs/ui-runtime/09-testing-observability-recovery-and-release-gates.md",
    "docs/blueprint-v1/11-product-ui-devtools.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/ui-runtime/machine/framework-bakeoff-inventory.json",
    "docs/ui-runtime/machine/component-fixture-inventory.json",
    "docs/ui-runtime/machine/page-surface-composition.json",
    "docs/accessibility/machine/window-input-accessibility-spike.json",
}

REQUIRED_AREAS = {
    "state",
    "command",
    "surface",
    "accessibility",
    "diagnostic",
    "adapter",
}

REQUIRED_INVARIANTS = {
    "immutable versioned ShellSnapshot",
    "typed window profile Space tab and view identities",
    "explicit tab lifecycle",
    "typed shell commands",
    "snapshot validation",
    "no toolkit platform GPU page credential Plug-in or agent types",
}

REQUIRED_DENIALS = {
    "navigation",
    "profile",
    "permission",
    "credential",
    "agent",
    "Plug-in",
    "persistence",
    "update",
}

REQUIRED_EVIDENCE_NAMES = {
    "ADR-0013",
    "state contract",
    "command contract",
    "surface contract",
    "accessibility contract",
    "diagnostic contract",
    "adapter trait contract",
    "native adapter prototype",
    "no toolkit-owned authority negative tests",
    "owner review",
}

REQUIRED_CLAIM_PHRASES = [
    "no ADR-0013",
    "no native adapter prototype",
    "no UI toolkit selection",
    "no trusted-chrome readiness",
    "no accessibility readiness",
    "no page-surface approval",
    "no release-path UI approval",
    "no production claim",
    "no implementation claim",
]

REQUIRED_EVIDENCE_FILES = [
    "docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md",
    "docs/ui-runtime/machine/adapter-contract-inventory.schema.json",
    "docs/ui-runtime/machine/adapter-contract-inventory.json",
    "tools/validate_ui_adapter_contract.py",
]

PB003_REQUIRED_TERMS = [
    "ADR-0013",
    "toolkit-neutral state",
    "command",
    "surface",
    "accessibility",
    "diagnostic",
    "adapter contract",
    "native adapter prototype",
    "navigation",
    "profile",
    "permission",
    "credential",
    "agent",
    "Plug-in",
    "persistence",
    "update authority",
    "owner review",
]


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        fail(f"{key} must be an array")
    return value


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def normalize(value: str) -> str:
    normalized = value.lower()
    for old, new in [
        ("ui toolkit", "ui-toolkit"),
        ("trusted chrome", "trusted-chrome"),
        ("page surface", "page-surface"),
        ("release path ui", "release-path ui"),
        ("toolkit neutral", "toolkit-neutral"),
        ("adapter contract", "adapter-contract"),
        ("native adapter", "native-adapter"),
        ("plug-in", "plug-in"),
        ("update authority", "update-authority"),
        ("owner review", "owner-review"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def validate_inventory(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    inventory_id = text(data.get("inventory_id"))
    if not INVENTORY_ID.fullmatch(inventory_id):
        fail(f"{path}: invalid inventory_id {inventory_id!r}")
    if data.get("status") != "no_claim_contract_inventory":
        fail(f"{path}: status must be no_claim_contract_inventory")

    boundary_text = " ".join(
        [text(data.get("claim_status")), *[text(value) for value in require_list(data, "unsupported_boundaries")]]
    )
    boundary_lower = boundary_text.lower()
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase.lower() not in boundary_lower:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    sources = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - sources)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in REQUIRED_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    areas: list[str] = []
    for item in require_list(data, "contract_areas"):
        if not isinstance(item, dict):
            fail(f"{path}: contract_areas entries must be objects")
        area_id = text(item.get("area_id"))
        if not AREA_ID.fullmatch(area_id):
            fail(f"{path}: invalid area_id {area_id!r}")
        area = text(item.get("area"))
        areas.append(area)
        if not text(item.get("owner_scope")):
            fail(f"{path}: {area_id}.owner_scope must be set")
        for key in ("current_evidence", "required_contract", "missing_evidence"):
            if len(text(item.get(key))) < 35:
                fail(f"{path}: {area_id}.{key} must be descriptive")
    check_no_duplicates(areas, "contract areas")
    if set(areas) != REQUIRED_AREAS:
        fail(f"{path}: contract areas must be exactly: {', '.join(sorted(REQUIRED_AREAS))}")

    invariants: list[str] = []
    for item in require_list(data, "current_model_invariants"):
        if not isinstance(item, dict):
            fail(f"{path}: current_model_invariants entries must be objects")
        invariant_id = text(item.get("invariant_id"))
        if not INVARIANT_ID.fullmatch(invariant_id):
            fail(f"{path}: invalid invariant_id {invariant_id!r}")
        invariant = text(item.get("invariant"))
        invariants.append(invariant)
        for key in ("source", "still_missing"):
            if len(text(item.get(key))) < 25:
                fail(f"{path}: {invariant_id}.{key} must be descriptive")
    check_no_duplicates(invariants, "current model invariants")
    if set(invariants) != REQUIRED_INVARIANTS:
        fail(
            f"{path}: current model invariants must be exactly: "
            + ", ".join(sorted(REQUIRED_INVARIANTS))
        )

    denials: list[str] = []
    for item in require_list(data, "adapter_authority_denials"):
        if not isinstance(item, dict):
            fail(f"{path}: adapter_authority_denials entries must be objects")
        denial_id = text(item.get("denial_id"))
        if not DENIAL_ID.fullmatch(denial_id):
            fail(f"{path}: invalid denial_id {denial_id!r}")
        authority = text(item.get("authority"))
        denials.append(authority)
        if len(text(item.get("denial_rule"))) < 45:
            fail(f"{path}: {denial_id}.denial_rule must be descriptive")
        negative = item.get("required_negative_evidence")
        if not isinstance(negative, list) or len(negative) < 3:
            fail(f"{path}: {denial_id}.required_negative_evidence must contain at least three entries")
        if any(not isinstance(value, str) or not value for value in negative):
            fail(f"{path}: {denial_id}.required_negative_evidence must contain non-empty strings")
        if len(text(item.get("missing_evidence"))) < 25:
            fail(f"{path}: {denial_id}.missing_evidence must be descriptive")
    check_no_duplicates(denials, "adapter authority denials")
    if set(denials) != REQUIRED_DENIALS:
        fail(f"{path}: authority denials must be exactly: {', '.join(sorted(REQUIRED_DENIALS))}")

    evidence_names: list[str] = []
    for item in require_list(data, "required_evidence"):
        if not isinstance(item, dict):
            fail(f"{path}: required_evidence entries must be objects")
        evidence_id = text(item.get("evidence_id"))
        if not EVIDENCE_ID.fullmatch(evidence_id):
            fail(f"{path}: invalid evidence_id {evidence_id!r}")
        name = text(item.get("name"))
        evidence_names.append(name)
        needed_for = item.get("needed_for")
        if not isinstance(needed_for, list) or len(needed_for) < 2:
            fail(f"{path}: {evidence_id}.needed_for must contain at least two entries")
        if len(text(item.get("current_status"))) < 5:
            fail(f"{path}: {evidence_id}.current_status must be set")
        if len(text(item.get("missing_evidence"))) < 35:
            fail(f"{path}: {evidence_id}.missing_evidence must be descriptive")
    check_no_duplicates(evidence_names, "required evidence names")
    if set(evidence_names) != REQUIRED_EVIDENCE_NAMES:
        fail(f"{path}: required evidence names must be exactly: {', '.join(sorted(REQUIRED_EVIDENCE_NAMES))}")


def validate_readiness_records() -> None:
    prebuild = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(prebuild, dict) or not isinstance(prebuild.get("items"), list):
        fail("pre-build-readiness.json must contain an items array")
    pb003 = next((item for item in prebuild["items"] if item.get("id") == "PB-003"), None)
    if not isinstance(pb003, dict):
        fail("pre-build-readiness.json is missing PB-003")
    if pb003.get("status") != "partial":
        fail("PB-003 must remain partial while only no-claim adapter contract evidence exists")
    evidence = pb003.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-003 must list no-claim adapter contract evidence")
    missing_evidence = [path for path in REQUIRED_EVIDENCE_FILES if path not in evidence]
    if missing_evidence:
        fail("PB-003 evidence is missing records: " + ", ".join(missing_evidence))
    required_text = normalize(" ".join(text(value) for value in pb003.get("evidence_required", [])))
    for phrase in PB003_REQUIRED_TERMS:
        if normalize(phrase) not in required_text:
            fail(f"PB-003 evidence_required must include {phrase}")

    tasks = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(tasks, dict) or not isinstance(tasks.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain a tasks array")
    task = next((item for item in tasks["tasks"] if item.get("id") == "TASK-000006"), None)
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000006")
    if task.get("status") != "proposed":
        fail("TASK-000006 must remain proposed")
    allowed_paths = set(text(value) for value in task.get("allowed_paths", []))
    for required in [
        "docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md",
        "tools/validate_ui_adapter_contract.py",
    ]:
        if required not in allowed_paths:
            fail(f"TASK-000006 allowed_paths must include {required}")
    task_text = normalize(
        " ".join(
            text(value)
            for field in ("preconditions", "acceptance_criteria", "negative_tests")
            for value in task.get(field, [])
        )
    )
    for phrase in [
        "checked no-claim adapter contract inventory",
        "ADR-0013",
        "toolkit-neutral state",
        "command",
        "surface",
        "accessibility",
        "diagnostic",
        "adapter contract",
        "native adapter prototype",
        "no toolkit-owned authority negative tests",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000006 must mention {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_INVENTORY]
    for path in paths:
        validate_inventory(path)
    validate_readiness_records()
    print(f"UI adapter contract validation passed: {len(paths)} inventory file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
