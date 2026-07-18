#!/usr/bin/env python3
"""Validate no-claim window/input/accessibility spike inventories."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
ACCESSIBILITY_MACHINE = DOCS / "accessibility" / "machine"
DEFAULT_INVENTORY = ACCESSIBILITY_MACHINE / "window-input-accessibility-spike.json"

INVENTORY_ID = re.compile(r"^WIN\.INPUT\.A11Y\.[A-Z0-9._-]+$")
AXIS_ID = re.compile(r"^WIN-A11Y-AXIS-[A-Z0-9_-]+$")
WORKFLOW_ID = re.compile(r"^WIN-A11Y-WORKFLOW-[A-Z0-9_-]+$")
BLOCKER_ID = re.compile(r"^WIN-A11Y-BLOCKER-[A-Z0-9_-]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/blueprint-v1/11-product-ui-devtools.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/accessibility/README.md",
    "docs/accessibility/04-platform-accessibility-bridges.md",
    "docs/accessibility/05-browser-ui-devtools-automation-and-agents.md",
    "docs/accessibility/07-testing-assistive-technology-matrices-and-release-gates.md",
    "docs/platform/README.md",
    "docs/platform/02-windows-surfaces-displays-and-lifecycle.md",
    "docs/platform/03-input-ime-clipboard-and-drag-drop.md",
    "docs/ui-runtime/README.md",
    "docs/ui-runtime/04-page-surface-compositor-and-process-integration.md",
    "docs/ui-runtime/07-windowing-input-ime-accessibility-and-platform.md",
    "docs/ui-runtime/09-testing-observability-recovery-and-release-gates.md",
    "docs/ui-runtime/10-prototype-plan-decision-record-and-migration.md",
    "docs/ui-runtime/machine/component-fixture-inventory.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
}

REQUIRED_AXES = {
    "WIN-A11Y-AXIS-WINDOWING": "windowing",
    "WIN-A11Y-AXIS-INPUT": "input",
    "WIN-A11Y-AXIS-IME": "ime",
    "WIN-A11Y-AXIS-ACCESSIBILITY-TREE": "accessibility",
    "WIN-A11Y-AXIS-PAGE-TREE-COMPOSITION": "page-tree",
    "WIN-A11Y-AXIS-CLIPBOARD": "clipboard",
    "WIN-A11Y-AXIS-DRAG-DROP": "drag",
    "WIN-A11Y-AXIS-LOCALIZATION": "localization",
    "WIN-A11Y-AXIS-ZOOM": "zoom",
    "WIN-A11Y-AXIS-HIGH-CONTRAST": "high contrast",
    "WIN-A11Y-AXIS-FORCED-COLORS": "forced",
    "WIN-A11Y-AXIS-REDUCED-MOTION": "reduced motion",
    "WIN-A11Y-AXIS-CRASH-RECOVERY": "crash",
    "WIN-A11Y-AXIS-RENDERER-HANG": "renderer hang",
    "WIN-A11Y-AXIS-GPU-LOSS": "gpu",
}

REQUIRED_WORKFLOWS = {
    "browser_window_lifecycle",
    "tab_strip_and_groups",
    "spaces_side_panel",
    "address_command_field",
    "permission_agent_confirmation",
    "page_surface_composition",
    "devtools_docking",
    "resource_manager",
    "settings_recovery",
}

REQUIRED_PLATFORM_AT = {
    "macos": ("AX", {"VoiceOver"}),
    "windows": ("UI Automation", {"Narrator", "NVDA"}),
    "linux": ("AT-SPI", {"Orca"}),
}

REQUIRED_BLOCKERS = {
    "reference platform selected",
    "isolated adapter runner",
    "rendered reference shell",
    "page-surface stub",
    "accessibility tree snapshot schema",
    "manual assistive technology matrix",
    "input and IME fixture harness",
    "clipboard drag-drop security fixtures",
    "localization zoom appearance fixtures",
    "crash hang GPU-loss fault fixtures",
    "latency and resource capture",
    "owner review",
}

REQUIRED_CLAIM_PHRASES = [
    "no native UI implementation claim",
    "no UI toolkit selection",
    "no accessibility readiness claim",
    "no screen-reader coverage claim",
    "no manual assistive-technology coverage claim",
    "no page-tree composition proof",
    "no IME correctness claim",
    "no keyboard completeness claim",
    "no clipboard or drag-drop safety claim",
    "no localization readiness claim",
    "no zoom high-contrast reduced-motion readiness claim",
    "no crash-recovery renderer-hang or GPU-loss readiness claim",
    "no UI-GATE-7 claim",
    "no UI-GATE-10 claim",
    "no release-path UI approval",
    "no production claim",
]

REQUIRED_EVIDENCE_FILES = [
    "docs/research/window-input-accessibility-spike-inventory-2026-07.md",
    "docs/accessibility/machine/window-input-accessibility-spike.schema.json",
    "docs/accessibility/machine/window-input-accessibility-spike.json",
    "tools/validate_window_input_accessibility_spike.py",
]

PB015_REQUIRED_TERMS = [
    "reference-platform",
    "workflow matrix",
    "windowing",
    "input",
    "ime",
    "accessibility",
    "page-tree composition",
    "clipboard",
    "drag-drop",
    "localization",
    "zoom",
    "high contrast",
    "reduced motion",
    "crash recovery",
    "renderer hang",
    "gpu-loss",
    "manual assistive-technology",
    "screen readers",
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
        ("gpu loss", "gpu-loss"),
        ("gpu device loss", "gpu-loss"),
        ("drag/drop", "drag-drop"),
        ("drag drop", "drag-drop"),
        ("page tree", "page-tree"),
        ("assistive technology", "assistive-technology"),
        ("ui gate", "ui-gate"),
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
    if data.get("status") != "no_claim_workflow_inventory":
        fail(f"{path}: status must be no_claim_workflow_inventory")

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

    axis_ids: list[str] = []
    for item in require_list(data, "workflow_axes"):
        if not isinstance(item, dict):
            fail(f"{path}: workflow_axes entries must be objects")
        axis_id = text(item.get("axis_id"))
        if not AXIS_ID.fullmatch(axis_id):
            fail(f"{path}: invalid axis_id {axis_id!r}")
        axis_ids.append(axis_id)
        for field in ("name", "purpose", "current_status"):
            if len(text(item.get(field))) < 5:
                fail(f"{path}: {axis_id}.{field} must be descriptive")
        required_evidence = [text(value) for value in item.get("required_evidence", [])]
        if len(required_evidence) < 3:
            fail(f"{path}: {axis_id}.required_evidence must contain at least three entries")
        axis_term = REQUIRED_AXES.get(axis_id)
        if axis_term is None:
            fail(f"{path}: unexpected axis {axis_id}")
        axis_text = normalize(" ".join([text(item.get("name")), text(item.get("purpose")), *required_evidence]))
        if normalize(axis_term) not in axis_text:
            fail(f"{path}: {axis_id} must describe {axis_term}")
    check_no_duplicates(axis_ids, "workflow axes")
    if set(axis_ids) != set(REQUIRED_AXES):
        fail(f"{path}: workflow axes must be exactly: {', '.join(sorted(REQUIRED_AXES))}")

    workflows: list[str] = []
    covered_axes: set[str] = set()
    for item in require_list(data, "core_workflows"):
        if not isinstance(item, dict):
            fail(f"{path}: core_workflows entries must be objects")
        workflow_id = text(item.get("workflow_id"))
        if not WORKFLOW_ID.fullmatch(workflow_id):
            fail(f"{path}: invalid workflow_id {workflow_id!r}")
        workflow = text(item.get("workflow"))
        workflows.append(workflow)
        axes = [text(value) for value in item.get("covers_axes", [])]
        if not axes:
            fail(f"{path}: {workflow_id}.covers_axes must not be empty")
        unknown_axes = sorted(set(axes) - set(REQUIRED_AXES))
        if unknown_axes:
            fail(f"{path}: {workflow_id} references unknown axes: {', '.join(unknown_axes)}")
        covered_axes.update(axes)
        contract = normalize(text(item.get("page_tree_contract")))
        if "page-tree" not in contract or not any(term in contract for term in ("authority", "origin", "profile", "epoch", "stale")):
            fail(f"{path}: {workflow_id}.page_tree_contract must discuss page-tree identity or authority")
        if len(text(item.get("missing_evidence"))) < 40:
            fail(f"{path}: {workflow_id}.missing_evidence must be descriptive")
    check_no_duplicates(workflows, "core workflows")
    if set(workflows) != REQUIRED_WORKFLOWS:
        fail(f"{path}: core workflows must be exactly: {', '.join(sorted(REQUIRED_WORKFLOWS))}")
    if covered_axes != set(REQUIRED_AXES):
        fail(f"{path}: core workflows must cover every required axis")

    platforms: list[str] = []
    for item in require_list(data, "platform_assistive_technology_matrix"):
        if not isinstance(item, dict):
            fail(f"{path}: platform matrix entries must be objects")
        platform = text(item.get("platform"))
        platforms.append(platform)
        api, required_at = REQUIRED_PLATFORM_AT.get(platform, ("", set()))
        if not api:
            fail(f"{path}: unexpected platform {platform!r}")
        if api.lower() not in text(item.get("accessibility_api")).lower():
            fail(f"{path}: {platform} must list accessibility API {api}")
        ats = set(text(value) for value in item.get("assistive_technologies", []))
        missing_at = sorted(required_at - ats)
        if missing_at:
            fail(f"{path}: {platform} missing assistive technologies: {', '.join(missing_at)}")
        coverage_text = normalize(
            " ".join(
                [
                    *[text(value) for value in item.get("input_coverage", [])],
                    *[text(value) for value in item.get("required_artifacts", [])],
                    text(item.get("missing_evidence")),
                ]
            )
        )
        for phrase in ["keyboard", "ime", "clipboard", "drag-drop", "contrast", "reduced motion", "latency"]:
            if normalize(phrase) not in coverage_text:
                fail(f"{path}: {platform} matrix must mention {phrase}")
        if len(text(item.get("missing_evidence"))) < 40:
            fail(f"{path}: {platform}.missing_evidence must be descriptive")
    check_no_duplicates(platforms, "platform matrix entries")
    if set(platforms) != set(REQUIRED_PLATFORM_AT):
        fail(f"{path}: platform matrix must cover macos, windows, and linux")

    blocker_names: list[str] = []
    for item in require_list(data, "evidence_blockers"):
        if not isinstance(item, dict):
            fail(f"{path}: evidence_blockers entries must be objects")
        blocker_id = text(item.get("blocker_id"))
        if not BLOCKER_ID.fullmatch(blocker_id):
            fail(f"{path}: invalid blocker_id {blocker_id!r}")
        blocker = text(item.get("blocker"))
        blocker_names.append(blocker)
        if not isinstance(item.get("needed_for"), list) or not item["needed_for"]:
            fail(f"{path}: {blocker_id}.needed_for must be a non-empty array")
        if len(text(item.get("missing_evidence"))) < 35:
            fail(f"{path}: {blocker_id}.missing_evidence must be descriptive")
    check_no_duplicates(blocker_names, "evidence blockers")
    missing_blockers = sorted(REQUIRED_BLOCKERS - set(blocker_names))
    if missing_blockers:
        fail(f"{path}: missing evidence blockers: {', '.join(missing_blockers)}")


def validate_readiness_records() -> None:
    prebuild = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(prebuild, dict) or not isinstance(prebuild.get("items"), list):
        fail("pre-build-readiness.json must contain an items array")
    pb015 = next((item for item in prebuild["items"] if item.get("id") == "PB-015"), None)
    if not isinstance(pb015, dict):
        fail("pre-build-readiness.json is missing PB-015")
    if pb015.get("status") != "partial":
        fail("PB-015 must remain partial while only no-claim workflow inventory evidence exists")
    evidence = pb015.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-015 must list no-claim workflow inventory evidence")
    missing_evidence = [path for path in REQUIRED_EVIDENCE_FILES if path not in evidence]
    if missing_evidence:
        fail("PB-015 evidence is missing records: " + ", ".join(missing_evidence))
    required_text = normalize(" ".join(text(value) for value in pb015.get("evidence_required", [])))
    for phrase in PB015_REQUIRED_TERMS:
        if normalize(phrase) not in required_text:
            fail(f"PB-015 evidence_required must include {phrase}")

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
        "docs/accessibility/",
        "docs/research/window-input-accessibility-spike-inventory-2026-07.md",
        "tools/validate_window_input_accessibility_spike.py",
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
        "checked no-claim window/input/accessibility workflow inventory",
        "manual assistive-technology",
        "page-tree",
        "reference-platform",
        "screen-reader",
        "ui-gate-10",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000006 must mention {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_INVENTORY]
    for path in paths:
        validate_inventory(path)
    validate_readiness_records()
    print(f"window/input/accessibility spike validation passed: {len(paths)} inventory file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
