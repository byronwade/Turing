#!/usr/bin/env python3
"""Validate checked no-claim fresh-host readiness-review templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
PROJECT_MACHINE = DOCS / "project-buildout" / "machine"
DEFAULT_REVIEW = (
    PROJECT_MACHINE
    / "fresh-host-readiness-reviews"
    / "no-claim-fresh-host-readiness-template.json"
)

REVIEW_ID = re.compile(r"^BUILD\.FRESH_HOST\.READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_REVIEW_FILES = [
    "docs/project-buildout/machine/fresh-host-readiness-review.schema.json",
    "docs/project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json",
    "tools/validate_fresh_host_readiness_review.py",
]

REQUIRED_SOURCE_RECORDS = {
    "docs/research/m0-build-foundation-2026-07.md",
    "docs/research/fresh-host-reproduction-inventory-2026-07.md",
    "docs/research/pre-build-readiness-gap-audit-2026-07.md",
    "docs/project-buildout/05-repository-build-toolchain-and-coding-standards.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/project-buildout/machine/fresh-host-reproduction.schema.json",
    "docs/project-buildout/machine/fresh-host-reproduction.json",
    "docs/project-buildout/machine/fresh-host-run-record.schema.json",
    "docs/project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json",
    "docs/project-buildout/machine/fresh-host-readiness-review.schema.json",
    "docs/project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/13-build-release-operations.md",
    "docs/blueprint-v1/14-roadmap-work-breakdown.md",
    "docs/blueprint-v1/22-research-program.md",
    "tools/bootstrap.sh",
    "tools/bootstrap.ps1",
    "tools/doctor.sh",
    "tools/doctor.ps1",
    "tools/check.sh",
    "tools/check.ps1",
    "tools/xtask/src/main.rs",
    "tools/validate_fresh_host_reproduction.py",
    "tools/validate_fresh_host_run_records.py",
    "tools/validate_fresh_host_readiness_review.py",
    "tools/validate_blueprint.py",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no independent review",
    "no release-operations review",
    "no quality review",
    "no independent fresh-host reproduction",
    "no owner-approved clean-VM equivalent",
    "no command execution review",
    "no retained bootstrap/doctor/check/xtask logs",
    "no exact host-fact review",
    "no source identity review",
    "no cache or target-directory review",
    "no source-tree cleanliness review",
    "no failure-denominator review",
    "no rollback or cleanup review",
    "no environmental-waiver review",
    "no PB-009 readiness promotion",
    "no broad M1 readiness",
    "no preview readiness",
    "no beta readiness",
    "no stable readiness",
    "no production readiness",
    "no release confidence",
    "no Chrome-class claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "independent_reviewed",
    "release_operations_reviewed",
    "quality_reviewed",
    "independent_fresh_host_reviewed",
    "owner_approved_clean_vm_reviewed",
    "bootstrap_log_reviewed",
    "doctor_log_reviewed",
    "check_log_reviewed",
    "xtask_log_reviewed",
    "exact_host_facts_reviewed",
    "source_identity_reviewed",
    "cache_target_reviewed",
    "source_tree_cleanliness_reviewed",
    "failure_denominator_reviewed",
    "retained_hashes_reviewed",
    "rollback_cleanup_reviewed",
    "environmental_waivers_reviewed",
    "same_host_reruns_rejected",
    "pb009_ready",
    "broad_m1_ready",
    "preview_ready",
    "beta_ready",
    "stable_ready",
    "production_ready",
    "release_confidence_supported",
    "chrome_class_supported",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "run_record",
    "reference_host",
    "clean_vm_waiver",
    "owner_reviewer",
    "independent_reviewer",
    "release_operations_reviewer",
    "quality_reviewer",
]

REQUIRED_AXIS_TERMS = [
    "independent fresh reference host",
    "owner-approved clean VM equivalent",
    "operating system",
    "shell",
    "Rust",
    "Cargo",
    "Git",
    "bootstrap",
    "doctor",
    "check",
    "xtask",
    "exit code",
    "retained log",
    "SHA-256",
    "cache",
    "target directory",
    "temp directory",
    "source-tree cleanliness",
    "source identity",
    "failure classification",
    "failure denominator",
    "rollback",
    "cleanup",
    "environmental waiver",
    "same-host reruns",
    "owner review",
    "release-operations review",
    "quality review",
    "release confidence",
    "Chrome-class",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "same-host",
    "command output",
    "host identity",
    "source identity",
    "source-tree",
    "cache",
    "failure",
    "waiver",
    "validation",
    "claim boundary",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_fresh_host_reproduction.py",
    "python3 -B tools/validate_fresh_host_run_records.py",
    "python3 -B tools/validate_fresh_host_readiness_review.py",
    "python3 -B tools/validate_blueprint.py",
    ".\\tools\\check.ps1",
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
        ("clean vm", "clean-vm"),
        ("fresh host", "fresh-host"),
        ("source tree", "source-tree"),
        ("target directory", "target-directory"),
        ("target dir", "target-directory"),
        ("temp directory", "temp-directory"),
        ("pb 009", "pb-009"),
        ("pb009", "pb-009"),
        ("owner approved", "owner-approved"),
        ("same host", "same-host"),
        ("release operations", "release-operations"),
        ("line ending", "line-ending"),
        ("host fact", "host-fact"),
        ("failure denominator", "failure-denominator"),
        ("environmental waiver", "environmental-waiver"),
        ("release confidence", "release-confidence"),
        ("sha-256", "sha-256"),
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
    if data.get("status") != "no_claim_fresh_host_readiness_template":
        fail(f"{path}: status must be no_claim_fresh_host_readiness_template")

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
    for phrase in ["placeholder", "self-approval", "same-host", "pb-009", "null"]:
        if phrase not in policy:
            fail(f"{path}: prohibited_placeholder_policy must mention {phrase}")

    readiness = require_object(data, "readiness_status")
    missing_flags = sorted(set(READINESS_STATUS_FLAGS) - set(readiness))
    if missing_flags:
        fail(f"{path}: readiness_status missing flags: {', '.join(missing_flags)}")
    for flag in READINESS_STATUS_FLAGS:
        if readiness.get(flag) is not False:
            fail(f"{path}: readiness_status.{flag} must be false in the no-claim template")

    axis_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for key in [
                "host_identity_axes",
                "source_checkout_axes",
                "command_execution_axes",
                "cache_artifact_axes",
                "failure_review_axes",
                "owner_review_axes",
            ]
            for item in require_list(data, key)
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing fresh-host readiness axis term: {phrase}")
    if (
        "beyond the checked no-claim fresh-host readiness-review template"
        not in axis_text
    ):
        fail(f"{path}: axes must require evidence beyond the checked no-claim template")

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


def validate_readiness_registry() -> None:
    payload = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        fail("pre-build-readiness.json must contain items")
    item = next(
        (
            entry
            for entry in payload["items"]
            if isinstance(entry, dict) and entry.get("id") == "PB-009"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-009")
    if item.get("status") != "partial":
        fail("PB-009 must remain partial while the fresh-host review is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-009 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-009 evidence is missing fresh-host readiness review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim fresh-host readiness-review template",
        "owner-reviewed fresh-host readiness review beyond the checked no-claim fresh-host readiness-review template",
        "independent fresh-host reproduction",
        "PB-009 readiness promotion",
        "same-host reruns",
    ]:
        if normalize(phrase) not in required_text:
            fail(f"PB-009 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000002"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000002 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000002 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000002 allowed_paths missing fresh-host review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim fresh-host readiness-review template",
        "owner-reviewed fresh-host readiness review",
        "cannot be cited",
        "same-host reruns",
        "PB-009 readiness",
        "Chrome-class",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000002 must mention fresh-host review boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-fresh-host-build-confidence"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing fresh-host lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("fresh-host lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("fresh-host lane evidence_start missing fresh-host review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed fresh-host readiness review beyond the checked no-claim fresh-host readiness-review template",
        "no PB-009 readiness promotion",
        "no independent reproducibility claim from same-host reruns",
        "no Chrome-class claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"fresh-host lane must mention {phrase}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    print(f"fresh-host readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
