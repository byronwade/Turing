#!/usr/bin/env python3
"""Validate no-claim page-surface composition inventories."""

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
DEFAULT_INVENTORY = UI_MACHINE / "page-surface-composition.json"

INVENTORY_ID = re.compile(r"^UI\.SURFACE\.[A-Z0-9._-]+$")
ALT_ID = re.compile(r"^UI-SURFACE-ALT-[A-Z0-9_-]+$")
TEST_ID = re.compile(r"^UI-SURFACE-TEST-[A-Z0-9_-]+$")
FAILURE_ID = re.compile(r"^UI-SURFACE-FAILURE-[A-Z0-9_-]+$")
BOUNDARY_ID = re.compile(r"^UI-SURFACE-BOUNDARY-[A-Z0-9_-]+$")
BLOCKER_ID = re.compile(r"^UI-SURFACE-BLOCKER-[A-Z0-9_-]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/blueprint-v1/04-system-architecture.md",
    "docs/blueprint-v1/05-web-engine.md",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/blueprint-v1/11-product-ui-devtools.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/engine/05-paint-compositor-and-gpu.md",
    "docs/ui-runtime/README.md",
    "docs/ui-runtime/04-page-surface-compositor-and-process-integration.md",
    "docs/ui-runtime/07-windowing-input-ime-accessibility-and-platform.md",
    "docs/ui-runtime/09-testing-observability-recovery-and-release-gates.md",
    "docs/ui-runtime/10-prototype-plan-decision-record-and-migration.md",
    "docs/accessibility/README.md",
    "docs/accessibility/machine/window-input-accessibility-spike.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
}

REQUIRED_CONTRACT_FIELDS = {
    "view_id",
    "document_epoch",
    "device_generation",
    "logical_size",
    "physical_size",
    "scale_factor",
    "color_space",
    "alpha_mode",
    "damage_region",
    "synchronization_primitive",
    "frame_sequence",
    "presentation_deadline",
    "release_acknowledgement",
    "brokered_surface_handle",
}

REQUIRED_ALTERNATIVES = {
    "UI-SURFACE-ALT-OWN_SWAPCHAIN",
    "UI-SURFACE-ALT-TOOLKIT_EXTERNAL_TEXTURE",
    "UI-SURFACE-ALT-PLATFORM_CHILD_SURFACE",
    "UI-SURFACE-ALT-DETERMINISTIC_SOFTWARE_FALLBACK",
}

REQUIRED_WORKFLOWS = {
    "resize",
    "scale",
    "damage",
    "input-routing",
    "ime-routing",
    "accessibility-composition",
    "occlusion",
    "capture",
    "renderer-crash",
    "gpu-device-loss",
    "latency-frame-pacing",
}

REQUIRED_FAILURE_CASES = {
    "stale-document-epoch",
    "stale-view-id",
    "stale-device-generation",
    "renderer-crash-recovery-ui",
    "gpu-device-loss-rebuild",
    "toolkit-failure-no-profile-corruption",
    "release-ack-timeout",
    "cross-origin-surface-isolation",
    "capture-policy-denial",
}

REQUIRED_BOUNDARIES = {
    "profile",
    "view",
    "document epoch",
    "process",
    "origin site frame",
    "device generation",
    "surface handle",
    "resource owner",
}

REQUIRED_BLOCKERS = {
    "page-surface protocol",
    "brokered handle model",
    "reference shell adapter",
    "simulated renderer frames",
    "hit-test input IME accessibility routing",
    "resize scale damage occlusion capture fixtures",
    "renderer crash and GPU-loss faults",
    "latency and frame-pacing traces",
    "owner review and ADR-0016",
}

REQUIRED_CLAIM_PHRASES = [
    "no UI-GATE-7 claim",
    "no page-surface approval",
    "no compositor ownership decision",
    "no UI toolkit selection",
    "no renderer-texture composition proof",
    "no typed page-surface handle implementation",
    "no brokered surface handle proof",
    "no resize scale or damage proof",
    "no input IME or accessibility routing proof",
    "no occlusion or capture proof",
    "no renderer-crash or GPU device-loss proof",
    "no software-fallback proof",
    "no latency or frame-pacing proof",
    "no release-path UI approval",
    "no production claim",
]

REQUIRED_EVIDENCE_FILES = [
    "docs/research/page-surface-composition-inventory-2026-07.md",
    "docs/ui-runtime/machine/page-surface-composition.schema.json",
    "docs/ui-runtime/machine/page-surface-composition.json",
    "tools/validate_page_surface_composition.py",
]

PB005_REQUIRED_TERMS = [
    "UI-GATE-7",
    "ADR-0016",
    "renderer-produced page textures",
    "resize",
    "scale",
    "damage",
    "input",
    "IME",
    "accessibility",
    "occlusion",
    "capture",
    "renderer crash",
    "GPU device loss",
    "typed page-surface handles",
    "document",
    "device generations",
    "brokered surface handle",
    "software fallback",
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
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("gpu device loss", "gpu-device-loss"),
        ("gpu loss", "gpu-device-loss"),
        ("device loss", "device-loss"),
        ("renderer crash", "renderer-crash"),
        ("page surface", "page-surface"),
        ("surface handle", "surface-handle"),
        ("brokered surface", "brokered-surface"),
        ("ui gate", "ui-gate"),
        ("frame pacing", "frame-pacing"),
        ("software fallback", "software-fallback"),
        ("release path ui", "release-path ui"),
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
    if data.get("status") != "no_claim_surface_inventory":
        fail(f"{path}: status must be no_claim_surface_inventory")

    boundaries = [text(value) for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")), *boundaries])
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

    fields: list[str] = []
    for item in require_list(data, "surface_contract_fields"):
        if not isinstance(item, dict):
            fail(f"{path}: surface_contract_fields entries must be objects")
        field = text(item.get("field"))
        fields.append(field)
        for key in ("purpose", "missing_evidence"):
            if len(text(item.get(key))) < 35:
                fail(f"{path}: field {field}.{key} must be descriptive")
    check_no_duplicates(fields, "surface contract fields")
    if set(fields) != REQUIRED_CONTRACT_FIELDS:
        fail(f"{path}: surface contract fields must be exactly: {', '.join(sorted(REQUIRED_CONTRACT_FIELDS))}")

    alternatives: list[str] = []
    for item in require_list(data, "composition_alternatives"):
        if not isinstance(item, dict):
            fail(f"{path}: composition_alternatives entries must be objects")
        alternative_id = text(item.get("alternative_id"))
        if not ALT_ID.fullmatch(alternative_id):
            fail(f"{path}: invalid alternative_id {alternative_id!r}")
        alternatives.append(alternative_id)
        evidence = [text(value) for value in item.get("required_evidence", [])]
        if len(evidence) < 3:
            fail(f"{path}: {alternative_id}.required_evidence must contain at least three entries")
        for key in ("ownership_model", "missing_evidence"):
            if len(text(item.get(key))) < 35:
                fail(f"{path}: {alternative_id}.{key} must be descriptive")
    check_no_duplicates(alternatives, "composition alternatives")
    if set(alternatives) != REQUIRED_ALTERNATIVES:
        fail(f"{path}: composition alternatives must be exactly: {', '.join(sorted(REQUIRED_ALTERNATIVES))}")

    workflows: list[str] = []
    workflow_text = ""
    for item in require_list(data, "workflow_test_matrix"):
        if not isinstance(item, dict):
            fail(f"{path}: workflow_test_matrix entries must be objects")
        test_id = text(item.get("test_id"))
        if not TEST_ID.fullmatch(test_id):
            fail(f"{path}: invalid test_id {test_id!r}")
        workflow = text(item.get("workflow"))
        workflows.append(workflow)
        artifacts = [text(value) for value in item.get("required_artifacts", [])]
        if len(artifacts) < 3:
            fail(f"{path}: {test_id}.required_artifacts must contain at least three entries")
        observation = text(item.get("required_observation"))
        if len(observation) < 45:
            fail(f"{path}: {test_id}.required_observation must be descriptive")
        workflow_text += " " + normalize(" ".join([workflow, observation, *artifacts]))
    check_no_duplicates(workflows, "workflow tests")
    if set(workflows) != REQUIRED_WORKFLOWS:
        fail(f"{path}: workflow tests must be exactly: {', '.join(sorted(REQUIRED_WORKFLOWS))}")
    for phrase in [
        "resize",
        "scale",
        "damage",
        "input",
        "ime",
        "accessibility",
        "occlusion",
        "capture",
        "renderer-crash",
        "gpu-device-loss",
        "latency",
        "frame-pacing",
    ]:
        if normalize(phrase) not in workflow_text:
            fail(f"{path}: workflow matrix must mention {phrase}")

    failures: list[str] = []
    for item in require_list(data, "failure_recovery_cases"):
        if not isinstance(item, dict):
            fail(f"{path}: failure_recovery_cases entries must be objects")
        case_id = text(item.get("case_id"))
        if not FAILURE_ID.fullmatch(case_id):
            fail(f"{path}: invalid case_id {case_id!r}")
        case = text(item.get("case"))
        failures.append(case)
        safe_result = text(item.get("safe_result")).lower()
        if not any(term in safe_result for term in ("reject", "replace", "rebuild", "deny", "cancel", "reclaim", "stop")):
            fail(f"{path}: {case_id}.safe_result must describe bounded safe behavior")
        if len(text(item.get("missing_evidence"))) < 25:
            fail(f"{path}: {case_id}.missing_evidence must be descriptive")
    check_no_duplicates(failures, "failure cases")
    if set(failures) != REQUIRED_FAILURE_CASES:
        fail(f"{path}: failure cases must be exactly: {', '.join(sorted(REQUIRED_FAILURE_CASES))}")

    boundaries_seen: list[str] = []
    for item in require_list(data, "security_identity_boundaries"):
        if not isinstance(item, dict):
            fail(f"{path}: security_identity_boundaries entries must be objects")
        boundary_id = text(item.get("boundary_id"))
        if not BOUNDARY_ID.fullmatch(boundary_id):
            fail(f"{path}: invalid boundary_id {boundary_id!r}")
        boundary = text(item.get("boundary"))
        boundaries_seen.append(boundary)
        for key in ("enforced_identity", "unsafe_if_missing", "missing_evidence"):
            if len(text(item.get(key))) < 25:
                fail(f"{path}: {boundary_id}.{key} must be descriptive")
    check_no_duplicates(boundaries_seen, "security identity boundaries")
    if set(boundaries_seen) != REQUIRED_BOUNDARIES:
        fail(f"{path}: security identity boundaries must be exactly: {', '.join(sorted(REQUIRED_BOUNDARIES))}")

    blockers: list[str] = []
    for item in require_list(data, "evidence_blockers"):
        if not isinstance(item, dict):
            fail(f"{path}: evidence_blockers entries must be objects")
        blocker_id = text(item.get("blocker_id"))
        if not BLOCKER_ID.fullmatch(blocker_id):
            fail(f"{path}: invalid blocker_id {blocker_id!r}")
        blocker = text(item.get("blocker"))
        blockers.append(blocker)
        if not isinstance(item.get("needed_for"), list) or len(item["needed_for"]) < 2:
            fail(f"{path}: {blocker_id}.needed_for must contain at least two entries")
        if len(text(item.get("missing_evidence"))) < 35:
            fail(f"{path}: {blocker_id}.missing_evidence must be descriptive")
    check_no_duplicates(blockers, "evidence blockers")
    if set(blockers) != REQUIRED_BLOCKERS:
        fail(f"{path}: evidence blockers must be exactly: {', '.join(sorted(REQUIRED_BLOCKERS))}")


def validate_readiness_records() -> None:
    prebuild = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(prebuild, dict) or not isinstance(prebuild.get("items"), list):
        fail("pre-build-readiness.json must contain an items array")
    pb005 = next((item for item in prebuild["items"] if item.get("id") == "PB-005"), None)
    if not isinstance(pb005, dict):
        fail("pre-build-readiness.json is missing PB-005")
    if pb005.get("status") != "partial":
        fail("PB-005 must remain partial while only no-claim page-surface composition evidence exists")
    evidence = pb005.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-005 must list no-claim page-surface composition evidence")
    missing_evidence = [path for path in REQUIRED_EVIDENCE_FILES if path not in evidence]
    if missing_evidence:
        fail("PB-005 evidence is missing records: " + ", ".join(missing_evidence))
    required_text = normalize(" ".join(text(value) for value in pb005.get("evidence_required", [])))
    for phrase in PB005_REQUIRED_TERMS:
        if normalize(phrase) not in required_text:
            fail(f"PB-005 evidence_required must include {phrase}")

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
        "docs/research/page-surface-composition-inventory-2026-07.md",
        "tools/validate_page_surface_composition.py",
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
        "checked no-claim page-surface composition inventory",
        "UI-GATE-7",
        "ADR-0016",
        "typed page-surface handles",
        "brokered surface handle",
        "document and device generations",
        "resize",
        "scale",
        "damage",
        "occlusion",
        "capture",
        "software fallback",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000006 must mention {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_INVENTORY]
    for path in paths:
        validate_inventory(path)
    validate_readiness_records()
    print(f"page-surface composition validation passed: {len(paths)} inventory file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
