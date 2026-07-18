#!/usr/bin/env python3
"""Validate no-claim native UI framework bake-off inventories."""

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
DEFAULT_INVENTORY = UI_MACHINE / "framework-bakeoff-inventory.json"

INVENTORY_ID = re.compile(r"^UI\.FRAMEWORK\.[A-Z0-9._-]+$")
SOURCE_ID = re.compile(r"^UI-FRAMEWORK-SOURCE-[A-Z0-9_-]+$")
AXIS_ID = re.compile(r"^UI-FRAMEWORK-AXIS-[A-Z0-9_-]+$")
DISQUALIFIER_ID = re.compile(r"^UI-FRAMEWORK-DISQUALIFIER-[A-Z0-9_-]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/blueprint-v1/03-language-and-dependency-strategy.md",
    "docs/blueprint-v1/11-product-ui-devtools.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/security.md",
    "docs/security-engine/README.md",
    "docs/ui-runtime/README.md",
    "docs/ui-runtime/02-framework-landscape-and-selection-method.md",
    "docs/ui-runtime/03-rust-state-command-and-adapter-architecture.md",
    "docs/ui-runtime/04-page-surface-compositor-and-process-integration.md",
    "docs/ui-runtime/07-windowing-input-ime-accessibility-and-platform.md",
    "docs/ui-runtime/08-performance-memory-binary-and-energy-budgets.md",
    "docs/ui-runtime/09-testing-observability-recovery-and-release-gates.md",
    "docs/ui-runtime/10-prototype-plan-decision-record-and-migration.md",
    "docs/ui-runtime/machine/framework-candidates.json",
    "docs/ui-runtime/machine/ui-performance-budgets.json",
    "docs/research/native-ui-framework-evaluation-2026-07.md",
    "docs/research/native-ui-component-fixture-inventory-2026-07.md",
    "docs/research/page-surface-composition-inventory-2026-07.md",
    "docs/research/window-input-accessibility-spike-inventory-2026-07.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
}

REQUIRED_EXTERNAL_SOURCES = {
    "UI-FRAMEWORK-SOURCE-SLINT_DOCS",
    "UI-FRAMEWORK-SOURCE-SLINT_LICENSE",
    "UI-FRAMEWORK-SOURCE-VIZIA_DOCS",
    "UI-FRAMEWORK-SOURCE-FLOEM_DOCS",
    "UI-FRAMEWORK-SOURCE-GPUI_DOCS",
    "UI-FRAMEWORK-SOURCE-TAURI_ARCHITECTURE",
}

REQUIRED_AXES = {
    "UI-FRAMEWORK-AXIS-EQUIVALENT_ADAPTERS",
    "UI-FRAMEWORK-AXIS-ACCESSIBILITY",
    "UI-FRAMEWORK-AXIS-IME_KEYBOARD_TEXT",
    "UI-FRAMEWORK-AXIS-PAGE_SURFACE",
    "UI-FRAMEWORK-AXIS-CRASH_GPU_RECOVERY",
    "UI-FRAMEWORK-AXIS-PERFORMANCE_MEMORY_BINARY_ENERGY",
    "UI-FRAMEWORK-AXIS-LICENSE_DEPENDENCY_PROVENANCE",
    "UI-FRAMEWORK-AXIS-REPLACEMENT_MAINTENANCE",
    "UI-FRAMEWORK-AXIS-BUILD_ITERATION_PACKAGING",
}

REQUIRED_DISQUALIFIERS = {
    "UI-FRAMEWORK-DISQUALIFIER-WEBVIEW_RUNTIME",
    "UI-FRAMEWORK-DISQUALIFIER-TOOLKIT_AUTHORITY",
    "UI-FRAMEWORK-DISQUALIFIER-NO_ACCESSIBILITY_PATH",
    "UI-FRAMEWORK-DISQUALIFIER-NO_PAGE_SURFACE_PATH",
    "UI-FRAMEWORK-DISQUALIFIER-LICENSE_OR_PROVENANCE_BLOCKER",
}

REQUIRED_CLAIM_PHRASES = [
    "no UI toolkit selection",
    "no ADR-0014 approval",
    "no equivalent adapter evidence",
    "no accessibility readiness",
    "no IME or keyboard proof",
    "no page-surface approval",
    "no trusted-chrome readiness",
    "no release-path UI approval",
    "no performance memory or energy claim",
    "no license or provenance approval",
    "no production claim",
]

REQUIRED_EVIDENCE_FILES = [
    "docs/research/native-ui-framework-bakeoff-inventory-2026-07.md",
    "docs/ui-runtime/machine/framework-bakeoff-inventory.schema.json",
    "docs/ui-runtime/machine/framework-bakeoff-inventory.json",
    "tools/validate_framework_bakeoff.py",
]

PB004_REQUIRED_TERMS = [
    "three-adapter",
    "owner-approved reduced reference-shell bake-off",
    "equivalent shell tasks",
    "ADR-0014",
    "accessibility",
    "IME",
    "keyboard",
    "crash",
    "GPU-loss",
    "startup",
    "memory",
    "binary",
    "latency",
    "frame-pacing",
    "energy",
    "license",
    "dependency",
    "provenance",
    "Electron",
    "Tauri",
    "system webview",
    "Node",
    "runtime React",
    "runtime DOM",
    "runtime CSS parser",
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
    if not isinstance(value, list) or not value:
        fail(f"{key} must be a non-empty array")
    return value


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("page surface", "page-surface"),
        ("ui toolkit", "ui-toolkit"),
        ("adr 0014", "adr-0014"),
        ("gpu device loss", "gpu-loss"),
        ("gpu loss", "gpu-loss"),
        ("frame pacing", "frame-pacing"),
        ("runtime css", "runtime-css"),
        ("runtime dom", "runtime-dom"),
        ("runtime react", "runtime-react"),
        ("system web view", "system-webview"),
        ("system webview", "system-webview"),
        ("owner approved", "owner-approved"),
        ("reference shell", "reference-shell"),
        ("three adapter", "three-adapter"),
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
    if data.get("status") != "no_claim_framework_bakeoff_inventory":
        fail(f"{path}: status must be no_claim_framework_bakeoff_inventory")

    boundary_text = " ".join(
        [text(data.get("claim_status")), *[text(value) for value in require_list(data, "unsupported_boundaries")]]
    )
    boundary_text_lower = boundary_text.lower()
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase.lower() not in boundary_text_lower:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    sources = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - sources)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in REQUIRED_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    external_ids: list[str] = []
    for item in require_list(data, "external_observations"):
        if not isinstance(item, dict):
            fail(f"{path}: external_observations entries must be objects")
        source_id = text(item.get("source_id"))
        if not SOURCE_ID.fullmatch(source_id):
            fail(f"{path}: invalid source_id {source_id!r}")
        external_ids.append(source_id)
        for key in ("source", "observation", "claim_boundary"):
            if len(text(item.get(key))) < 20:
                fail(f"{path}: {source_id}.{key} must be descriptive")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text(item.get("retrieved"))):
            fail(f"{path}: {source_id}.retrieved must be an ISO date")
    check_no_duplicates(external_ids, "external source ids")
    missing_external = sorted(REQUIRED_EXTERNAL_SOURCES - set(external_ids))
    if missing_external:
        fail(f"{path}: missing external observations: {', '.join(missing_external)}")

    candidate_registry = load_json(UI_MACHINE / "framework-candidates.json")
    registry_candidates = candidate_registry.get("candidates") if isinstance(candidate_registry, dict) else None
    if not isinstance(registry_candidates, list):
        fail("framework-candidates.json must contain candidates")
    expected_candidates = [item.get("id") for item in registry_candidates]
    if expected_candidates != [f"UIF-{index:03d}" for index in range(1, 10)]:
        fail("framework-candidates.json must contain UIF-001 through UIF-009")

    candidate_ids: list[str] = []
    for item in require_list(data, "candidate_summaries"):
        if not isinstance(item, dict):
            fail(f"{path}: candidate_summaries entries must be objects")
        candidate_id = text(item.get("candidate_id"))
        candidate_ids.append(candidate_id)
        if candidate_id not in expected_candidates:
            fail(f"{path}: unknown candidate_id {candidate_id}")
        source_ids = [text(value) for value in item.get("source_ids", []) if isinstance(value, str)]
        unknown_sources = sorted(set(source_ids) - set(external_ids))
        if unknown_sources:
            fail(f"{path}: {candidate_id} references unknown sources: {', '.join(unknown_sources)}")
        if len(text(item.get("name"))) < 2:
            fail(f"{path}: {candidate_id}.name must be present")
        if len(text(item.get("current_disposition"))) < 8:
            fail(f"{path}: {candidate_id}.current_disposition must be descriptive")
        for key in ("required_bakeoff_evidence", "blockers"):
            values = item.get(key)
            if not isinstance(values, list) or not values or any(len(text(value)) < 15 for value in values):
                fail(f"{path}: {candidate_id}.{key} must contain descriptive strings")
        disposition = normalize(text(item.get("current_disposition")))
        if "not selected" not in disposition and "not primary trusted chrome" not in disposition and "future escape path" not in disposition:
            fail(f"{path}: {candidate_id} disposition must preserve no-selection status")
    check_no_duplicates(candidate_ids, "candidate ids")
    if candidate_ids != expected_candidates:
        fail(f"{path}: candidate summaries must match framework-candidates order")

    scope = data.get("required_bakeoff_scope")
    if not isinstance(scope, dict):
        fail(f"{path}: required_bakeoff_scope must be an object")
    scope_text = normalize(" ".join(text(value) for values in scope.values() if isinstance(values, list) for value in values))
    for phrase in [
        "slint adapter",
        "vizia adapter",
        "floem or gpui adapter",
        "owner-approved reduced scope",
        "100 synthetic tabs",
        "spaces",
        "address",
        "page-surface",
        "permission prompt",
        "agent confirmation",
        "resource manager",
        "keyboard",
        "ime",
        "accessibility",
        "high contrast",
        "reduced motion",
        "renderer hang",
        "gpu-loss",
        "same turing ui model",
        "same command contract",
    ]:
        if normalize(phrase) not in scope_text:
            fail(f"{path}: required_bakeoff_scope must include {phrase}")

    axis_ids: list[str] = []
    for item in require_list(data, "evidence_axes"):
        if not isinstance(item, dict):
            fail(f"{path}: evidence_axes entries must be objects")
        axis_id = text(item.get("axis_id"))
        if not AXIS_ID.fullmatch(axis_id):
            fail(f"{path}: invalid axis_id {axis_id!r}")
        axis_ids.append(axis_id)
        axis_text = " ".join(text(item.get(key)) for key in ("name", "required_output", "missing_status"))
        if len(axis_text) < 80:
            fail(f"{path}: {axis_id} must be descriptive")
    check_no_duplicates(axis_ids, "axis ids")
    if set(axis_ids) != REQUIRED_AXES:
        fail(f"{path}: evidence axes must be exactly: {', '.join(sorted(REQUIRED_AXES))}")

    disqualifier_ids: list[str] = []
    disqualifier_texts: list[str] = []
    for item in require_list(data, "disqualifiers"):
        if not isinstance(item, dict):
            fail(f"{path}: disqualifiers entries must be objects")
        disqualifier_id = text(item.get("disqualifier_id"))
        if not DISQUALIFIER_ID.fullmatch(disqualifier_id):
            fail(f"{path}: invalid disqualifier_id {disqualifier_id!r}")
        disqualifier_ids.append(disqualifier_id)
        combined = " ".join(text(item.get(key)) for key in ("condition", "reason"))
        disqualifier_texts.append(normalize(combined))
        if len(combined) < 80:
            fail(f"{path}: {disqualifier_id} must be descriptive")
    check_no_duplicates(disqualifier_ids, "disqualifier ids")
    if set(disqualifier_ids) != REQUIRED_DISQUALIFIERS:
        fail(f"{path}: disqualifiers must be exactly: {', '.join(sorted(REQUIRED_DISQUALIFIERS))}")
    disqualifier_text = " ".join(disqualifier_texts)
    for phrase in [
        "electron",
        "tauri",
        "system-webview",
        "node",
        "runtime-react",
        "runtime javascript",
        "runtime-dom",
        "runtime-css parser",
        "authority",
        "accessibility",
        "page-surface",
        "license",
        "provenance",
    ]:
        if normalize(phrase) not in disqualifier_text:
            fail(f"{path}: disqualifiers must mention {phrase}")


def validate_pb004() -> None:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    pb004 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-004"), None)
    if not isinstance(pb004, dict):
        fail("pre-build-readiness.json is missing PB-004")
    if pb004.get("status") != "partial":
        fail("PB-004 must remain partial while only no-claim framework bake-off inventory exists")
    evidence = pb004.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-004 must list no-claim framework bake-off evidence")
    missing = [path for path in REQUIRED_EVIDENCE_FILES if path not in evidence]
    if missing:
        fail("PB-004 evidence is missing framework bake-off records: " + ", ".join(missing))
    required_text = " ".join(value for value in pb004.get("evidence_required", []) if isinstance(value, str))
    normalized_required = normalize(required_text)
    for phrase in PB004_REQUIRED_TERMS:
        if normalize(phrase) not in normalized_required:
            fail(f"PB-004 evidence_required must include {phrase}")


def validate_task_queue() -> None:
    queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = queue.get("tasks") if isinstance(queue, dict) else None
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next((item for item in tasks if isinstance(item, dict) and item.get("id") == "TASK-000006"), None)
    if not isinstance(task, dict):
        fail("TASK-000006 is missing")
    allowed = task.get("allowed_paths")
    if not isinstance(allowed, list):
        fail("TASK-000006.allowed_paths must be an array")
    missing_allowed = [path for path in REQUIRED_EVIDENCE_FILES if path not in allowed]
    if missing_allowed:
        fail("TASK-000006 allowed_paths is missing framework bake-off records: " + ", ".join(missing_allowed))
    task_text = " ".join(
        value
        for key in ("preconditions", "acceptance_criteria", "negative_tests")
        for value in task.get(key, [])
        if isinstance(value, str)
    )
    normalized_task = normalize(task_text)
    for phrase in [
        "framework bake-off inventory",
        "three-adapter",
        "owner-approved reduced",
        "equivalent shell tasks",
        "adr-0014",
        "accessibility",
        "ime",
        "keyboard",
        "page-surface",
        "gpu-loss",
        "startup",
        "memory",
        "binary",
        "latency",
        "frame-pacing",
        "energy",
        "license",
        "dependency",
        "provenance",
        "electron",
        "tauri",
        "system-webview",
        "runtime-react",
        "runtime javascript",
        "runtime-dom",
        "runtime-css parser",
    ]:
        if normalize(phrase) not in normalized_task:
            fail(f"TASK-000006 must include {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg) for arg in argv[1:]] or [DEFAULT_INVENTORY]
    for path in paths:
        validate_inventory(path)
    validate_pb004()
    validate_task_queue()
    print(f"framework bake-off validation passed: {len(paths)} inventory file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
