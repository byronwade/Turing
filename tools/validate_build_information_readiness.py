#!/usr/bin/env python3
"""Validate the checked no-claim build-information readiness ledger."""

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
DEFAULT_LEDGER = PROJECT_MACHINE / "build-information-readiness-ledger.json"
BACKLOG_PATH = MACHINE / "backlog.json"
TRACEABILITY_PATH = MACHINE / "professional-traceability.json"
VERIFICATION_MATRIX_PATH = MACHINE / "requirement-verification-matrix.json"

LEDGER_ID = re.compile(r"^PB020\.BUILD_INFORMATION_READINESS_LEDGER\.[A-Z0-9._-]+$")
PROPOSED_TASKS = {f"TASK-{number:06d}" for number in range(1, 11)}
REVIEW_PENDING_TASKS = {"TASK-000011"}

EXPECTED_STATE = {
    "contained_m0_information_ready": True,
    "broad_build_information_ready": False,
    "all_information_ready_for_building": False,
    "chrome_class_information_ready": False,
    "production_information_ready": False,
    "proposed_task_information_ready": False,
    "owner_review_required_for_promotion": True,
}

EXPECTED_CLASSES = {
    "INFO-ENTRYPOINTS": {"gates": {"PB-001", "PB-020"}, "tasks": set()},
    "INFO-TOOLCHAIN": {"gates": {"PB-008", "PB-009"}, "tasks": {"TASK-000002"}},
    "INFO-TASK-AUTHORITY": {"gates": {"PB-020"}, "tasks": PROPOSED_TASKS | REVIEW_PENDING_TASKS},
    "INFO-SOURCE-STRATEGY": {"gates": {"PB-002"}, "tasks": {"TASK-000001"}},
    "INFO-FRESH-HOST": {"gates": {"PB-009", "PB-020"}, "tasks": {"TASK-000002"}},
    "INFO-IPC": {"gates": {"PB-011"}, "tasks": {"TASK-000003", "TASK-000011"}},
    "INFO-SANDBOX": {"gates": {"PB-012"}, "tasks": {"TASK-000004"}},
    "INFO-BENCHMARK": {"gates": {"PB-013"}, "tasks": {"TASK-000005"}},
    "INFO-NATIVE-SHELL": {
        "gates": {"PB-003", "PB-004", "PB-005", "PB-014", "PB-015"},
        "tasks": {"TASK-000006"},
    },
    "INFO-REFERENCE-PLATFORM": {
        "gates": {"PB-006", "PB-020"},
        "tasks": {"TASK-000002", "TASK-000004", "TASK-000005", "TASK-000006", "TASK-000009", "TASK-000010"},
    },
    "INFO-PROFILE-SESSION": {"gates": {"PB-016"}, "tasks": {"TASK-000007"}},
    "INFO-PACKAGE-UPDATE": {"gates": {"PB-017"}, "tasks": {"TASK-000009"}},
    "INFO-INCIDENT-RESPONSE": {"gates": {"PB-018"}, "tasks": {"TASK-000010"}},
    "INFO-BACKUP-OWNERSHIP": {"gates": {"PB-019", "PB-020"}, "tasks": {"TASK-000008"}},
    "INFO-CHROME-CLASS-PRODUCT": {"gates": {"PB-020"}, "tasks": set()},
}

REQUIRED_SOURCE_RECORDS = {
    "README.md",
    "docs/start-here.md",
    "docs/README.md",
    "docs/documentation-policy.md",
    "docs/repository-map.md",
    "docs/security.md",
    "docs/project-buildout/README.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/project-buildout/23-owner-decision-closure-board.md",
    "docs/project-buildout/implementation-plan/README.md",
    "docs/project-buildout/machine/implementation-kickoff-review.json",
    "docs/project-buildout/machine/build-readiness-dependency-graph.json",
    "docs/project-buildout/machine/documentation-readiness-completion-audit.json",
    "docs/project-buildout/machine/contained-m0-start-state.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/agent-execution/README.md",
    "docs/production-readiness/README.md",
    "docs/research/README.md",
    "docs/research/chrome-class-capability-traceability-map-2026-07.md",
    "docs/research/reference-platform-support-scorecard-2026-07.md",
    "docs/platform/machine/reference-platform-scorecard.json",
    "docs/platform/machine/reference-platform-scorecard.schema.json",
    "tools/validate_reference_platform_scorecard.py",
}

REQUIRED_CLAIM_PHRASES = [
    "no complete documentation",
    "no all-information-ready-for-building",
    "no proposed task approval",
    "no task-000011 acceptance",
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
]

REQUIRED_PB020_EVIDENCE = [
    "docs/research/build-information-readiness-ledger-2026-07.md",
    "docs/project-buildout/machine/build-information-readiness-ledger.schema.json",
    "docs/project-buildout/machine/build-information-readiness-ledger.json",
    "tools/validate_build_information_readiness.py",
]

REQUIRED_PB020_TERMS = [
    "build-information readiness ledger",
    "all-information-ready-for-building",
    "source strategy",
    "fresh-host",
    "ipc",
    "sandbox",
    "benchmark",
    "native-shell",
    "reference platform",
    "profile/session",
    "package/update",
    "incident response",
    "backup ownership",
    "owner review",
    "chrome-class",
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
    replacements = [
        ("chrome class", "chrome-class"),
        ("task 000011", "task-000011"),
        ("all information ready for building", "all-information-ready-for-building"),
        ("all-information ready for building", "all-information-ready-for-building"),
        ("release-readiness", "release readiness"),
    ]
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    return normalized


def ensure_existing_repo_path(path: Path, value: str, label: str) -> None:
    ref_path = value.split("#", 1)[0]
    if not ref_path:
        fail(f"{label}: empty path reference")
    if not (ROOT / ref_path).exists():
        fail(f"{label}: referenced path does not exist: {ref_path}")


def validate_ledger(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: ledger must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    ledger_id = text(data.get("ledger_id"))
    if not LEDGER_ID.fullmatch(ledger_id):
        fail(f"{path}: invalid ledger_id {ledger_id!r}")
    if data.get("status") != "no_claim_information_readiness_gap_ledger":
        fail(f"{path}: status must be no_claim_information_readiness_gap_ledger")

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
        ensure_existing_repo_path(path, source, "source_records")

    current_state = require_object(data, "current_state")
    for flag, expected in EXPECTED_STATE.items():
        if current_state.get(flag) is not expected:
            fail(f"{path}: current_state.{flag} must be {expected}")

    task_state = require_object(data, "task_queue_state")
    proposed = set(text(value) for value in require_list(task_state, "proposed_tasks"))
    review_pending = set(text(value) for value in require_list(task_state, "review_pending_tasks"))
    accepted = task_state.get("accepted_tasks")
    release_gated = task_state.get("release_gated_tasks")
    if proposed != PROPOSED_TASKS:
        fail(f"{path}: proposed_tasks must be TASK-000001 through TASK-000010")
    if review_pending != REVIEW_PENDING_TASKS:
        fail(f"{path}: review_pending_tasks must contain only TASK-000011")
    if accepted != []:
        fail(f"{path}: accepted_tasks must remain empty")
    if release_gated != []:
        fail(f"{path}: release_gated_tasks must remain empty")

    classes: dict[str, dict[str, Any]] = {}
    for info_class in require_list(data, "information_classes"):
        if not isinstance(info_class, dict):
            fail(f"{path}: information_classes entries must be objects")
        class_id = text(info_class.get("id"))
        if class_id in classes:
            fail(f"{path}: duplicate information class {class_id}")
        if class_id not in EXPECTED_CLASSES:
            fail(f"{path}: unexpected information class {class_id}")
        classes[class_id] = info_class
        expected = EXPECTED_CLASSES[class_id]
        gates = set(text(value) for value in require_list(info_class, "gate_refs"))
        tasks = set(text(value) for value in info_class.get("task_refs", []))
        if gates != expected["gates"]:
            fail(f"{path}: {class_id} gate_refs mismatch")
        if tasks != expected["tasks"]:
            fail(f"{path}: {class_id} task_refs mismatch")
        if info_class.get("ready_for_broad_build") is not False:
            fail(f"{path}: {class_id} ready_for_broad_build must remain false")
        if info_class.get("owner_review_required") is not True:
            fail(f"{path}: {class_id} owner_review_required must remain true")
        for field in [
            "required_information",
            "current_evidence",
            "missing_information",
            "owner_only_decisions",
            "prohibited_claims",
        ]:
            require_list(info_class, field)
        if not text(info_class.get("next_research_or_review")):
            fail(f"{path}: {class_id} next_research_or_review must be non-empty")
        for evidence in require_list(info_class, "current_evidence"):
            ensure_existing_repo_path(path, text(evidence), f"{class_id}.current_evidence")
        missing_text = normalize(
            " ".join(text(value) for value in require_list(info_class, "missing_information"))
        )
        owner_text = normalize(
            " ".join(text(value) for value in require_list(info_class, "owner_only_decisions"))
        )
        prohibited_text = normalize(
            " ".join(text(value) for value in require_list(info_class, "prohibited_claims"))
        )
        if "owner" not in owner_text:
            fail(f"{path}: {class_id} owner_only_decisions must mention owner")
        if not any(
            term in missing_text
            for term in [
                "missing",
                "owner-reviewed",
                "owner-approved",
                "independent",
                "executable",
                "beyond",
            ]
        ):
            fail(f"{path}: {class_id} missing_information must describe missing evidence")
        if "no " not in prohibited_text:
            fail(f"{path}: {class_id} prohibited_claims must preserve no-claim language")

    missing_classes = sorted(set(EXPECTED_CLASSES) - set(classes))
    if missing_classes:
        fail(f"{path}: missing information classes: {', '.join(missing_classes)}")

    validation_commands = set(text(value) for value in require_list(data, "validation_commands"))
    for command in [
        "python3 -B tools/validate_build_information_readiness.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in validation_commands:
            fail(f"{path}: missing validation command {command}")

    check_companion_records(path)


def check_companion_records(path: Path) -> None:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    if readiness.get("status") != "not_ready_for_broad_implementation":
        fail("pre-build-readiness.json must remain not_ready_for_broad_implementation")
    if readiness.get("contained_m0_authorization") != "ready":
        fail("pre-build-readiness.json must keep contained_m0_authorization ready")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    pb020 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-020"), None)
    if not isinstance(pb020, dict):
        fail("pre-build-readiness.json is missing PB-020")
    if pb020.get("status") != "partial":
        fail("PB-020 must remain partial while the information ledger is no-claim")
    evidence = pb020.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-020 evidence must be an array")
    missing_evidence = sorted(set(REQUIRED_PB020_EVIDENCE) - set(text(value) for value in evidence))
    if missing_evidence:
        fail("PB-020 evidence is missing build-information readiness files: " + ", ".join(missing_evidence))
    required_text = normalize(" ".join(text(value) for value in pb020.get("evidence_required", [])))
    for term in REQUIRED_PB020_TERMS:
        if normalize(term) not in required_text:
            fail(f"PB-020 evidence_required must include {term}")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(task_queue, dict):
        fail("build-readiness-task-queue.json must be an object")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task_status = {text(task.get("id")): text(task.get("status")) for task in tasks if isinstance(task, dict)}
    missing_tasks = sorted(PROPOSED_TASKS - set(task_status))
    if missing_tasks:
        fail("build-readiness-task-queue.json is missing proposed tasks: " + ", ".join(missing_tasks))
    for task_id in sorted(PROPOSED_TASKS):
        if task_status.get(task_id) != "proposed":
            fail(f"{task_id} must remain proposed")

    task_schema = load_json(DOCS / "agent-execution" / "machine" / "execution-task.schema.json")
    task_000011 = load_json(DOCS / "agent-execution" / "machine" / "tasks" / "TASK-000011.json")
    if not isinstance(task_000011, dict):
        fail("TASK-000011 must be an object")
    required_task_fields = set(task_schema.get("required", []))
    missing_task_fields = sorted(required_task_fields - set(task_000011))
    if missing_task_fields:
        fail("TASK-000011 is missing execution-task schema fields: " + ", ".join(missing_task_fields))
    allowed_task_fields = set(task_schema.get("properties", {}))
    unknown_task_fields = sorted(set(task_000011) - allowed_task_fields)
    if unknown_task_fields:
        fail("TASK-000011 has fields outside execution-task schema: " + ", ".join(unknown_task_fields))
    if task_000011.get("schema_version") != 1 or task_000011.get("id") != "TASK-000011":
        fail("TASK-000011 schema version or task ID is incorrect")
    if task_000011.get("status") != "review_pending":
        fail("TASK-000011 must remain review_pending")
    if task_000011.get("work_packages") != ["WP-002"]:
        fail("TASK-000011 must bind exactly to WP-002")
    backlog = load_json(BACKLOG_PATH)
    work_packages = backlog.get("items") if isinstance(backlog, dict) else None
    if not isinstance(work_packages, list) or not any(
        isinstance(item, dict) and item.get("id") == "WP-002"
        for item in work_packages
    ):
        fail("TASK-000011 binds to WP-002, but WP-002 is missing from the canonical backlog")
    traceability = load_json(TRACEABILITY_PATH)
    requirement_records = {
        item.get("id"): item
        for item in traceability.get("requirements", [])
        if isinstance(item, dict)
    }
    wp_evidence_path = "docs/research/wp-002-kernel-ipc-2026-07.md"
    for requirement_id in ("REQ-SEC-003", "REQ-PERF-004"):
        record = requirement_records.get(requirement_id)
        if not isinstance(record, dict) or wp_evidence_path not in record.get("evidence", []):
            fail(f"{requirement_id} must point to the WP-002 evidence report")
    verification_matrix = load_json(VERIFICATION_MATRIX_PATH)
    verification_lanes = verification_matrix.get("lanes", [])
    for requirement_id in ("REQ-SEC-003", "REQ-PERF-004"):
        if not any(
            isinstance(lane, dict)
            and requirement_id in lane.get("requirement_ids", [])
            and "WP-002" in lane.get("work_packages", [])
            for lane in verification_lanes
        ):
            fail(f"requirement-verification matrix must route {requirement_id} through WP-002")

    report = DOCS / "research" / "build-information-readiness-ledger-2026-07.md"
    report_text = report.read_text(encoding="utf-8")
    for phrase in [
        "Build Information Readiness Ledger",
        "no-claim gap ledger",
        "all-information-ready-for-building",
        "INFO-SOURCE-STRATEGY",
        "INFO-BENCHMARK",
        "INFO-CHROME-CLASS-PRODUCT",
        "does not support complete documentation",
    ]:
        if phrase not in report_text:
            fail(f"{report}: missing required phrase {phrase!r}")

    for evidence_path in REQUIRED_PB020_EVIDENCE:
        if not (ROOT / evidence_path).exists():
            fail(f"{path}: PB-020 evidence path does not exist: {evidence_path}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "ledger",
        nargs="?",
        type=Path,
        default=DEFAULT_LEDGER,
        help="Path to build-information-readiness-ledger.json",
    )
    args = parser.parse_args(argv)
    validate_ledger(args.ledger)
    print("build-information readiness validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
