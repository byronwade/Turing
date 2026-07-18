#!/usr/bin/env python3
"""Validate checked no-claim native UI readiness-review templates."""

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
DEFAULT_REVIEW = (
    UI_MACHINE
    / "native-ui-readiness-reviews"
    / "no-claim-native-ui-readiness-template.json"
)

REVIEW_ID = re.compile(r"^UI\.READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md",
    "docs/research/native-ui-framework-bakeoff-inventory-2026-07.md",
    "docs/research/native-ui-component-fixture-inventory-2026-07.md",
    "docs/research/page-surface-composition-inventory-2026-07.md",
    "docs/research/window-input-accessibility-spike-inventory-2026-07.md",
    "docs/ui-runtime/README.md",
    "docs/ui-runtime/02-framework-landscape-and-selection-method.md",
    "docs/ui-runtime/03-rust-state-command-and-adapter-architecture.md",
    "docs/ui-runtime/04-page-surface-compositor-and-process-integration.md",
    "docs/ui-runtime/07-windowing-input-ime-accessibility-and-platform.md",
    "docs/ui-runtime/09-testing-observability-recovery-and-release-gates.md",
    "docs/ui-runtime/10-prototype-plan-decision-record-and-migration.md",
    "docs/accessibility/README.md",
    "docs/platform/README.md",
    "docs/product-experience/README.md",
    "docs/blueprint-v1/11-product-ui-devtools.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/ui-runtime/machine/adapter-contract-inventory.schema.json",
    "docs/ui-runtime/machine/adapter-contract-inventory.json",
    "docs/ui-runtime/machine/framework-bakeoff-inventory.schema.json",
    "docs/ui-runtime/machine/framework-bakeoff-inventory.json",
    "docs/ui-runtime/machine/component-fixture-inventory.schema.json",
    "docs/ui-runtime/machine/component-fixture-inventory.json",
    "docs/ui-runtime/machine/page-surface-composition.schema.json",
    "docs/ui-runtime/machine/page-surface-composition.json",
    "docs/accessibility/machine/window-input-accessibility-spike.schema.json",
    "docs/accessibility/machine/window-input-accessibility-spike.json",
    "docs/ui-runtime/machine/native-ui-readiness-review.schema.json",
    "docs/ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json",
    "tools/validate_ui_adapter_contract.py",
    "tools/validate_framework_bakeoff.py",
    "tools/validate_ui_component_fixtures.py",
    "tools/validate_page_surface_composition.py",
    "tools/validate_window_input_accessibility_spike.py",
    "tools/validate_native_ui_readiness_review.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no independent review",
    "no ADR-0013 approval",
    "no ADR-0014 approval",
    "no ADR-0016 approval",
    "no UI-GATE-7 claim",
    "no UI-GATE-10 claim",
    "no native adapter prototype claim",
    "no UI toolkit selection",
    "no trusted-chrome readiness claim",
    "no accessibility readiness claim",
    "no screen-reader coverage claim",
    "no page-tree composition proof",
    "no page-surface approval",
    "no compositor ownership decision",
    "no release-path UI approval",
    "no production claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "independent_reviewed",
    "adr_0013_accepted",
    "adr_0014_accepted",
    "adr_0016_accepted",
    "ui_gate_7_passed",
    "ui_gate_10_passed",
    "native_adapter_prototype_reviewed",
    "toolkit_selected",
    "trusted_chrome_ready",
    "accessibility_ready",
    "screen_reader_coverage_supported",
    "page_tree_proof_supported",
    "page_surface_approved",
    "compositor_ownership_decided",
    "release_path_ui_approved",
    "production_claim_supported",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "selected_toolkit",
    "selected_adapter_strategy",
    "reference_platform",
    "owner_reviewer",
    "independent_reviewer",
]

REQUIRED_GATE_IDS = {"PB-003", "PB-004", "PB-005", "PB-014", "PB-015"}

REQUIRED_AXIS_TERMS = [
    "pb-003",
    "pb-004",
    "pb-005",
    "pb-014",
    "pb-015",
    "adr-0013",
    "adr-0014",
    "adr-0016",
    "ui-gate-7",
    "ui-gate-10",
    "toolkit-neutral",
    "state",
    "command",
    "surface",
    "accessibility",
    "diagnostic",
    "adapter",
    "native adapter prototype",
    "toolkit-owned authority",
    "equivalent",
    "slint",
    "vizia",
    "floem",
    "gpui",
    "license",
    "dependency",
    "provenance",
    "page-surface",
    "typed page-surface handles",
    "brokered surface handle",
    "document",
    "device generations",
    "resize",
    "scale",
    "damage",
    "input",
    "ime",
    "occlusion",
    "capture",
    "renderer crash",
    "gpu-loss",
    "software fallback",
    "latency",
    "frame-pacing",
    "design-token",
    "component-fixture",
    "browser chrome",
    "tabs",
    "spaces",
    "command field",
    "permission prompts",
    "agent confirmations",
    "resource manager",
    "settings",
    "recovery ui",
    "keyboard",
    "focus",
    "screen-reader",
    "forced-color",
    "high contrast",
    "reduced motion",
    "density",
    "localization",
    "error-state",
    "reference-platform",
    "windowing",
    "page-tree composition",
    "clipboard",
    "drag-drop",
    "manual assistive-technology",
    "voiceover",
    "narrator",
    "nvda",
    "orca",
    "electron",
    "tauri",
    "system webview",
    "node",
    "runtime react",
    "runtime dom",
    "runtime css parser",
    "owner review",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "adapter",
    "framework",
    "page-surface",
    "fixture",
    "accessibility",
    "runtime",
    "webview",
    "owner review",
    "adr",
    "ui-gate",
    "validation",
    "claim boundary",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_native_ui_readiness_review.py",
    "python3 -B tools/validate_blueprint.py",
    ".\\tools\\check.ps1",
]

REQUIRED_REVIEW_FILES = [
    "docs/ui-runtime/machine/native-ui-readiness-review.schema.json",
    "docs/ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json",
    "tools/validate_native_ui_readiness_review.py",
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


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(f"{key} must be an object")
    return value


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("ui gate", "ui-gate"),
        ("page surface", "page-surface"),
        ("page tree", "page-tree"),
        ("screen reader", "screen-reader"),
        ("assistive technology", "assistive-technology"),
        ("gpu device loss", "gpu-loss"),
        ("gpu loss", "gpu-loss"),
        ("frame pacing", "frame-pacing"),
        ("design token", "design-token"),
        ("component fixture", "component-fixture"),
        ("forced color", "forced-color"),
        ("error state", "error-state"),
        ("reference platform", "reference-platform"),
        ("drag/drop", "drag-drop"),
        ("drag drop", "drag-drop"),
        ("system web view", "system webview"),
        ("runtime css", "runtime css"),
        ("runtime dom", "runtime dom"),
        ("runtime react", "runtime react"),
        ("owner-reviewed", "owner review"),
        ("owner-review", "owner review"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def validate_review(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: review must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    review_id = text(data.get("review_id"))
    if not REVIEW_ID.fullmatch(review_id):
        fail(f"{path}: invalid review_id {review_id!r}")
    if data.get("status") != "no_claim_native_ui_readiness_template":
        fail(f"{path}: status must be no_claim_native_ui_readiness_template")

    boundary_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[text(value) for value in require_list(data, "unsupported_boundaries")],
            ]
        )
    )
    for phrase in REQUIRED_CLAIM_PHRASES:
        if normalize(phrase) not in boundary_text:
            fail(f"{path}: missing claim boundary phrase: {phrase}")

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in source_records:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    scope = require_object(data, "review_scope")
    if scope.get("review_status") != "template_only_no_review":
        fail(f"{path}: review_scope.review_status must be template_only_no_review")
    for field in NULL_SCOPE_FIELDS:
        if scope.get(field) is not None:
            fail(f"{path}: review_scope.{field} must be null in the no-claim template")
    policy = normalize(text(scope.get("prohibited_placeholder_policy")))
    for phrase in ["placeholder", "self-approval", "owner", "null"]:
        if phrase not in policy:
            fail(f"{path}: prohibited_placeholder_policy must mention {phrase}")

    status = require_object(data, "readiness_status")
    missing_status = sorted(set(READINESS_STATUS_FLAGS) - set(status))
    if missing_status:
        fail(f"{path}: readiness_status missing flags: {', '.join(missing_status)}")
    for flag in READINESS_STATUS_FLAGS:
        if status.get(flag) is not False:
            fail(f"{path}: readiness_status.{flag} must be false in the no-claim template")

    gate_axes = require_list(data, "gate_axes")
    gate_ids = [item.get("gate_id") for item in gate_axes if isinstance(item, dict)]
    if set(gate_ids) != REQUIRED_GATE_IDS:
        fail(f"{path}: gate_axes must cover exactly {', '.join(sorted(REQUIRED_GATE_IDS))}")
    if len(gate_ids) != len(set(gate_ids)):
        fail(f"{path}: gate_axes must not contain duplicate gate IDs")
    for item in gate_axes:
        if not isinstance(item, dict):
            fail(f"{path}: gate_axes entries must be objects")
        evidence = normalize(text(item.get("required_evidence")))
        if "beyond the checked no-claim native ui readiness-review template" not in evidence:
            fail(f"{path}: {item.get('gate_id')} must require evidence beyond the template")
        if "missing" not in normalize(text(item.get("template_status"))):
            fail(f"{path}: {item.get('gate_id')} template_status must remain missing")

    axis_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[
                    " ".join(text(value) for value in item.values())
                    for key in [
                        "gate_axes",
                        "adapter_axes",
                        "framework_axes",
                        "page_surface_axes",
                        "fixture_axes",
                        "accessibility_axes",
                        "release_exclusion_axes",
                        "owner_review_axes",
                    ]
                    for item in require_list(data, key)
                    if isinstance(item, dict)
                ],
            ]
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing native UI axis term: {phrase}")

    rejection_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for item in require_list(data, "rejection_rules")
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_REJECTION_TERMS:
        if normalize(phrase) not in rejection_text:
            fail(f"{path}: rejection rules must mention {phrase}")

    commands = [text(value) for value in require_list(data, "validation_commands")]
    for command in REQUIRED_VALIDATION_COMMANDS:
        if command not in commands:
            fail(f"{path}: validation_commands missing {command}")


def readiness_items() -> list[dict[str, Any]]:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    return [item for item in items if isinstance(item, dict)]


def validate_readiness_registry() -> None:
    items = readiness_items()
    for gate_id in sorted(REQUIRED_GATE_IDS):
        item = next((entry for entry in items if entry.get("id") == gate_id), None)
        if not isinstance(item, dict):
            fail(f"pre-build-readiness.json is missing {gate_id}")
        if item.get("status") != "partial":
            fail(f"{gate_id} must remain partial while the native UI review is a no-claim template")
        evidence = item.get("evidence")
        if not isinstance(evidence, list):
            fail(f"{gate_id} evidence must be an array")
        missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
        if missing:
            fail(f"{gate_id} evidence is missing native UI readiness review files: {', '.join(missing)}")
        required_text = normalize(
            " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
        )
        for phrase in [
            "checked no-claim native ui readiness-review template",
            "beyond the checked no-claim native ui readiness-review template",
            "owner review",
        ]:
            if phrase not in required_text:
                fail(f"{gate_id} evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (item for item in payload["tasks"] if isinstance(item, dict) and item.get("id") == "TASK-000006"),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000006 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000006 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000006 allowed_paths missing native UI review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim native ui readiness-review template",
        "toolkit selection",
        "accessibility readiness",
        "page-surface approval",
        "release-path ui approval",
        "cannot be cited",
    ]:
        if phrase not in task_text:
            fail(f"TASK-000006 must mention native UI template boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-native-shell-page-surface"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing native shell lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("native shell lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("native shell lane evidence_start missing native UI review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner review native ui readiness review beyond the checked no-claim native ui readiness-review template",
        "no owner review",
        "no release-path ui approval",
    ]:
        if phrase not in lane_text:
            fail(f"native shell lane must mention {phrase}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    print(f"native UI readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
