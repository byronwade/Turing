#!/usr/bin/env python3
"""Validate the checked no-claim contained M0 start-state inventory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
PROJECT_MACHINE = DOCS / "project-buildout" / "machine"
DEFAULT_STATE = PROJECT_MACHINE / "contained-m0-start-state.json"

STATE_ID = re.compile(r"^PB020\.CONTAINED_M0_START_STATE\.[A-Z0-9._-]+$")
PROPOSED_TASKS = {f"TASK-{number:06d}" for number in range(1, 11)}
REVIEW_PENDING_TASKS = {"TASK-000011"}
START_CLASSES = {
    "START-NO_CLAIM_DOC_RESEARCH": ("allowed_now", True),
    "START-TASK_000011_REVIEW_HANDOFF": ("review_pending_only", True),
    "START-PROPOSED_TASKS_000001_000010": ("owner_approval_required", False),
    "START-BROAD_M1_OR_PRODUCT": ("blocked", False),
}

REQUIRED_SOURCE_RECORDS = {
    "README.md",
    "docs/start-here.md",
    "docs/README.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/project-buildout/machine/implementation-kickoff-review.json",
    "docs/project-buildout/machine/build-readiness-dependency-graph.json",
    "docs/project-buildout/machine/documentation-readiness-completion-audit.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/agent-execution/README.md",
    "docs/agent-execution/machine/tasks/TASK-000011.json",
    "docs/research/task-000011-wp002-review-handoff-2026-07.md",
    "docs/agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json",
}

REQUIRED_FLAGS = {
    "contained_m0_continuation_allowed": True,
    "proposed_task_execution_authorized": False,
    "task_000011_acceptance_authorized": False,
    "broad_m1_authorized": False,
    "production_authorized": False,
    "chrome_class_claim_supported": False,
    "all_information_ready_for_building": False,
}

REQUIRED_CLAIM_PHRASES = [
    "no proposed task approval",
    "no task-000011 acceptance",
    "no accepted independent evidence-bundle",
    "no readiness promotion",
    "no broad m1 implementation",
    "no developer preview",
    "no beta",
    "no stable",
    "no production",
    "no chrome-class",
    "no performance",
    "no compatibility",
    "no security",
    "no accessibility",
    "no release readiness",
    "no daily-driver",
    "no all-information-ready-for-building",
]

REQUIRED_PB020_EVIDENCE = [
    "docs/research/contained-m0-start-state-inventory-2026-07.md",
    "docs/project-buildout/machine/contained-m0-start-state.schema.json",
    "docs/project-buildout/machine/contained-m0-start-state.json",
    "tools/validate_contained_m0_start_state.py",
]

REQUIRED_PB020_TERMS = [
    "contained m0 start-state",
    "task approval",
    "task-000011",
    "proposed tasks",
    "owner review",
    "broad m1",
    "all-information-ready-for-building",
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
        ("m1", "m1"),
        ("chrome class", "chrome-class"),
        ("task 000011", "task-000011"),
        ("task-000011", "task-000011"),
        ("all information ready for building", "all-information-ready-for-building"),
        ("all-information ready for building", "all-information-ready-for-building"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def validate_state(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: start state must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    state_id = text(data.get("state_id"))
    if not STATE_ID.fullmatch(state_id):
        fail(f"{path}: invalid state_id {state_id!r}")
    if data.get("status") != "no_claim_contained_m0_start_state":
        fail(f"{path}: status must be no_claim_contained_m0_start_state")

    boundary_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[text(value) for value in require_list(data, "unsupported_boundaries")],
            ]
        )
    )
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing claim boundary phrase: {phrase}")

    source_records = {text(value) for value in require_list(data, "source_records")}
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in source_records:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced source record does not exist: {source}")

    current_state = require_object(data, "current_state")
    for flag, expected in REQUIRED_FLAGS.items():
        if current_state.get(flag) is not expected:
            fail(f"{path}: current_state.{flag} must be {expected}")

    task_status_requirements = require_object(data, "task_status_requirements")
    proposed = set(text(value) for value in require_list(task_status_requirements, "proposed_queue_tasks"))
    review_pending = set(text(value) for value in require_list(task_status_requirements, "review_pending_tasks"))
    if proposed != PROPOSED_TASKS:
        fail(f"{path}: proposed_queue_tasks must be TASK-000001 through TASK-000010")
    if review_pending != REVIEW_PENDING_TASKS:
        fail(f"{path}: review_pending_tasks must contain only TASK-000011")

    class_by_id: dict[str, dict[str, Any]] = {}
    for start_class in require_list(data, "start_classes"):
        if not isinstance(start_class, dict):
            fail(f"{path}: start_classes entries must be objects")
        class_id = text(start_class.get("id"))
        if class_id in class_by_id:
            fail(f"{path}: duplicate start class {class_id}")
        class_by_id[class_id] = start_class
        if class_id not in START_CLASSES:
            fail(f"{path}: unexpected start class {class_id}")
        expected_state, expected_may_start = START_CLASSES[class_id]
        if start_class.get("state") != expected_state:
            fail(f"{path}: {class_id} state must be {expected_state}")
        if start_class.get("may_start_execution") is not expected_may_start:
            fail(f"{path}: {class_id} may_start_execution must be {expected_may_start}")
        for field in [
            "allowed_actions",
            "required_before_start",
            "must_stop_before",
            "evidence_refs",
            "prohibited_claims",
        ]:
            require_list(start_class, field)
        stop_text = normalize(" ".join(text(value) for value in require_list(start_class, "must_stop_before")))
        if "stop" not in stop_text or "claim" not in stop_text:
            fail(f"{path}: {class_id} must_stop_before must mention stop and claim")
        prohibited_text = normalize(" ".join(text(value) for value in require_list(start_class, "prohibited_claims")))
        if "no " not in prohibited_text:
            fail(f"{path}: {class_id} prohibited_claims must preserve no-claim language")
        for ref in require_list(start_class, "evidence_refs"):
            ref_path = text(ref).split("#", 1)[0]
            if not (ROOT / ref_path).exists():
                fail(f"{path}: {class_id} evidence ref does not exist: {ref_path}")

    missing_classes = sorted(set(START_CLASSES) - set(class_by_id))
    if missing_classes:
        fail(f"{path}: missing start classes: {', '.join(missing_classes)}")

    validation_commands = set(text(value) for value in require_list(data, "validation_commands"))
    for command in [
        "python3 -B tools/validate_contained_m0_start_state.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in validation_commands:
            fail(f"{path}: missing validation command {command}")

    check_readiness_and_tasks(path)


def check_readiness_and_tasks(path: Path) -> None:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    if readiness.get("status") != "not_ready_for_broad_implementation":
        fail("pre-build-readiness.json must remain not_ready_for_broad_implementation")
    if readiness.get("contained_m0_authorization") != "ready":
        fail("pre-build-readiness.json must keep contained_m0_authorization ready")
    allowed_now = readiness.get("allowed_now")
    if not isinstance(allowed_now, list):
        fail("pre-build-readiness.json allowed_now must be an array")
    for required in ["documentation", "research", "contained M0 source tasks in the root Cargo workspace"]:
        if required not in allowed_now:
            fail(f"pre-build-readiness.json allowed_now is missing {required}")

    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    pb020 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-020"), None)
    if not isinstance(pb020, dict):
        fail("pre-build-readiness.json is missing PB-020")
    if pb020.get("status") != "partial":
        fail("PB-020 must remain partial while start state is no-claim")
    evidence = pb020.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-020 evidence must be an array")
    missing_evidence = [item for item in REQUIRED_PB020_EVIDENCE if item not in evidence]
    if missing_evidence:
        fail("PB-020 evidence is missing contained M0 start-state files: " + ", ".join(missing_evidence))
    required_text = normalize(
        " ".join(value for value in pb020.get("evidence_required", []) if isinstance(value, str))
    )
    for term in REQUIRED_PB020_TERMS:
        if term not in required_text:
            fail(f"PB-020 evidence_required must include {term}")

    queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task_by_id = {task.get("id"): task for task in tasks if isinstance(task, dict)}
    for task_id in sorted(PROPOSED_TASKS):
        task = task_by_id.get(task_id)
        if not isinstance(task, dict):
            fail(f"build-readiness-task-queue.json is missing {task_id}")
        if task.get("status") != "proposed":
            fail(f"{task_id} must remain proposed in build-readiness-task-queue.json")

    task_000011 = load_json(DOCS / "agent-execution" / "machine" / "tasks" / "TASK-000011.json")
    if not isinstance(task_000011, dict):
        fail("TASK-000011 must be an object")
    if task_000011.get("status") != "review_pending":
        fail("TASK-000011 must remain review_pending")

    for evidence_path in REQUIRED_PB020_EVIDENCE:
        if not (ROOT / evidence_path).exists():
            fail(f"{path}: PB-020 evidence path does not exist: {evidence_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "state",
        nargs="?",
        type=Path,
        default=DEFAULT_STATE,
        help="Path to contained-m0-start-state.json",
    )
    args = parser.parse_args(argv)
    validate_state(args.state)
    print("contained M0 start-state validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
