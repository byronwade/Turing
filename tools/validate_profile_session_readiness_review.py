#!/usr/bin/env python3
"""Validate checked no-claim profile/session readiness-review templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
STORAGE_MACHINE = DOCS / "storage" / "machine"
DEFAULT_REVIEW = (
    STORAGE_MACHINE
    / "profile-session-readiness-reviews"
    / "no-claim-profile-session-readiness-template.json"
)

REVIEW_ID = re.compile(r"^PROFILE_SESSION\.READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/research/profile-session-format-inventory-2026-07.md",
    "docs/storage/machine/profile-session-format-inventory.schema.json",
    "docs/storage/machine/profile-session-format-inventory.json",
    "docs/storage/machine/profile-session-schema-package.schema.json",
    "docs/storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json",
    "docs/storage/machine/profile-session-readiness-review.schema.json",
    "docs/storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/07-network-storage-media.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/storage/README.md",
    "docs/storage/06-profile-history-bookmarks-settings-and-journals.md",
    "docs/storage/07-migrations-corruption-disk-full-and-power-loss.md",
    "docs/storage/08-encryption-credentials-clearing-and-export.md",
    "docs/storage/09-observability-repair-and-testing.md",
    "docs/product-experience/README.md",
    "docs/product-experience/02-onboarding-migration-profiles-and-private-sessions.md",
    "docs/product-experience/04-resource-manager-lifecycle-and-recovery.md",
    "docs/production-readiness/08-data-loss-migration-and-recovery-gates.md",
    "tools/validate_profile_session_formats.py",
    "tools/validate_profile_session_readiness_review.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no independent review",
    "no privacy review",
    "no executable profile schema",
    "no Space schema",
    "no session schema",
    "no snapshot schema",
    "no migration schema",
    "no migration test claim",
    "no fault test claim",
    "no real-profile fixture approval",
    "no private-session readiness claim",
    "no protected-work readiness claim",
    "no data-loss safety claim",
    "no user-data handling readiness claim",
    "no production profile-format claim",
    "no sync claim",
    "no credential-storage claim",
    "no release-path approval",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "independent_reviewed",
    "privacy_reviewed",
    "executable_profile_schema_reviewed",
    "executable_space_schema_reviewed",
    "executable_session_schema_reviewed",
    "executable_snapshot_schema_reviewed",
    "executable_migration_schema_reviewed",
    "migration_tests_passed",
    "fault_tests_passed",
    "real_profile_fixture_approved",
    "private_session_behavior_supported",
    "protected_work_behavior_supported",
    "data_loss_safety_supported",
    "user_data_handling_ready",
    "production_profile_format_approved",
    "sync_supported",
    "credential_storage_supported",
    "release_path_approved",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "schema_package",
    "reference_platform",
    "fixture_policy",
    "owner_reviewer",
    "independent_reviewer",
    "privacy_reviewer",
]

REQUIRED_REVIEW_FILES = [
    "docs/storage/machine/profile-session-readiness-review.schema.json",
    "docs/storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json",
    "tools/validate_profile_session_readiness_review.py",
]

REQUIRED_AXIS_TERMS = [
    "profile schema",
    "space schema",
    "session schema",
    "snapshot schema",
    "migration schema",
    "disk-full",
    "power-loss",
    "corruption",
    "downgrade",
    "export",
    "deletion",
    "private-session",
    "crash-recovery",
    "protected-work",
    "privacy",
    "data-loss",
    "classify-source",
    "validate-input",
    "plan-migration",
    "write-temporary-snapshot",
    "commit-or-rollback",
    "repair-or-quarantine",
    "verify-privacy-and-cleanup",
    "real user profile data",
    "fake profile",
    "fake credentials",
    "bounded temporary roots",
    "cleanup",
    "credential exclusion",
    "diagnostic redaction",
    "retention expiry",
    "sync boundary",
    "storage owner review",
    "privacy-data review",
    "product review",
    "security review",
    "quality review",
    "release-operations review",
    "production-readiness review",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "executable schema",
    "migration",
    "success paths",
    "protected work",
    "private-session",
    "corrupt",
    "real user data",
    "sync",
    "credential",
    "privacy review",
    "validation",
    "claim boundary",
]

CLOSURE_WORKSHEET = (
    DOCS / "research" / "profile-session-execution-and-data-safety-closure-preparation-2026-07.md"
)

REQUIRED_CLOSURE_TERMS = [
    "profile/session closure worksheet",
    "scope and data-class identity",
    "schema and format authority",
    "profile/session/space isolation",
    "fault and recovery matrix",
    "migration and rollback identity",
    "privacy and credential boundary",
    "loss and restoration accounting",
    "review and promotion record",
    "resumability control",
    "does not turn the no-claim templates into executable schemas",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_profile_session_readiness_review.py",
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
        ("space schema", "space schema"),
        ("profile/session", "profile/session"),
        ("disk full", "disk-full"),
        ("power loss", "power-loss"),
        ("private session", "private-session"),
        ("crash recovery", "crash-recovery"),
        ("protected work", "protected-work"),
        ("data loss", "data-loss"),
        ("classify_source", "classify-source"),
        ("validate_input", "validate-input"),
        ("plan_migration", "plan-migration"),
        ("write_temporary_snapshot", "write-temporary-snapshot"),
        ("commit_or_rollback", "commit-or-rollback"),
        ("repair_or_quarantine", "repair-or-quarantine"),
        ("verify_privacy_and_cleanup", "verify-privacy-and-cleanup"),
        ("real-profile", "real profile"),
        ("real user profile", "real user profile"),
        ("temporary root", "temporary roots"),
        ("credential-storage", "credential-storage"),
        ("owner-reviewed", "owner review"),
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
    if data.get("status") != "no_claim_profile_session_readiness_template":
        fail(f"{path}: status must be no_claim_profile_session_readiness_template")

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

    axis_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for key in [
                "format_axes",
                "behavior_axes",
                "migration_axes",
                "fixture_policy_axes",
                "privacy_axes",
                "owner_review_axes",
            ]
            for item in require_list(data, key)
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing profile/session axis term: {phrase}")
    if "beyond the checked no-claim profile/session readiness-review template" not in axis_text:
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


def validate_closure_worksheet() -> None:
    if not CLOSURE_WORKSHEET.is_file():
        fail(f"missing profile/session closure worksheet: {CLOSURE_WORKSHEET}")
    content = normalize(CLOSURE_WORKSHEET.read_text(encoding="utf-8"))
    for phrase in REQUIRED_CLOSURE_TERMS:
        if normalize(phrase) not in content:
            fail(f"profile/session closure worksheet missing term: {phrase}")


def validate_readiness_registry() -> None:
    payload = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        fail("pre-build-readiness.json must contain items")
    item = next(
        (
            entry
            for entry in payload["items"]
            if isinstance(entry, dict) and entry.get("id") == "PB-016"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-016")
    if item.get("status") != "partial":
        fail("PB-016 must remain partial while the profile/session review is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-016 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-016 evidence is missing profile/session readiness review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim profile/session readiness-review template",
        "beyond the checked no-claim profile/session readiness-review template",
        "owner review",
        "privacy",
        "data-loss",
    ]:
        if phrase not in required_text:
            fail(f"PB-016 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000007"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000007 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000007 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000007 allowed_paths missing profile/session review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim profile/session readiness-review template",
        "data-loss safety",
        "user-data handling readiness",
        "production profile-format",
        "cannot be cited",
    ]:
        if phrase not in task_text:
            fail(f"TASK-000007 must mention profile/session template boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-profile-space-session-snapshot-migration"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing profile/session lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("profile/session lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("profile/session lane evidence_start missing profile/session review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed profile/session readiness review beyond the checked no-claim profile/session readiness-review template",
        "no owner review",
        "no data-loss safety claim",
        "no production profile-format claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"profile/session lane must mention {phrase}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_closure_worksheet()
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    print(f"profile/session readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
