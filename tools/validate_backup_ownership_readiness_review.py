#!/usr/bin/env python3
"""Validate checked no-claim backup ownership readiness-review templates."""

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
    / "backup-ownership-readiness-reviews"
    / "no-claim-backup-ownership-readiness-template.json"
)

REVIEW_ID = re.compile(r"^OWN\.BACKUP_READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_SOURCE_RECORDS = {
    ".github/CODEOWNERS",
    "docs/research/backup-ownership-gap-inventory-2026-07.md",
    "docs/project-buildout/machine/backup-ownership-gap.schema.json",
    "docs/project-buildout/machine/backup-ownership-gap.json",
    "docs/project-buildout/machine/backup-owner-qualification-record.schema.json",
    "docs/project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json",
    "docs/project-buildout/machine/backup-ownership-readiness-review.schema.json",
    "docs/project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json",
    "docs/blueprint-v1/machine/professional-owners.json",
    "docs/blueprint-v1/machine/professional-review-rules.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/project-buildout/README.md",
    "docs/project-buildout/02-ownership-codeowners-and-maintainer-ladder.md",
    "docs/project-buildout/08-release-incident-legal-data-and-support.md",
    "docs/agent-execution/README.md",
    "docs/production-readiness/README.md",
    "tools/validate_backup_ownership_gap.py",
    "tools/validate_backup_ownership_readiness_review.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_REVIEW_FILES = [
    "docs/project-buildout/machine/backup-ownership-readiness-review.schema.json",
    "docs/project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json",
    "tools/validate_backup_ownership_readiness_review.py",
]

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no independent review",
    "no security review",
    "no release-operations review",
    "no legal review",
    "no support review",
    "no all-critical-scope review",
    "no named qualified backups",
    "no owner identity verification",
    "no role level review",
    "no subsystem competence review",
    "no representative path coverage",
    "no recent review record",
    "no availability record",
    "no succession evidence",
    "no recusal review",
    "no inactive owner replacement",
    "no CODEOWNERS reconciliation",
    "no review-rule reconciliation",
    "no escalation-policy reconciliation",
    "no repository-access review",
    "no stale privileged access review",
    "no ownerless protected-path review",
    "no primary-only path review",
    "no two-person control",
    "no owner coverage claim",
    "no release authority claim",
    "no release promotion claim",
    "no stable signing authority claim",
    "no update trust claim",
    "no supported-version changes claim",
    "no security-disclosure authority claim",
    "no irreversible migration approval claim",
    "no legal approval claim",
    "no incident closure authority claim",
    "no production authority claim",
    "no broad readiness claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "independent_reviewed",
    "security_reviewed",
    "release_operations_reviewed",
    "legal_reviewed",
    "support_reviewed",
    "all_critical_scopes_reviewed",
    "named_backups_reviewed",
    "owner_identity_reviewed",
    "role_level_reviewed",
    "subsystem_competence_reviewed",
    "representative_path_coverage_reviewed",
    "recent_review_records_verified",
    "availability_reviewed",
    "succession_reviewed",
    "recusal_reviewed",
    "inactivity_reviewed",
    "removal_reviewed",
    "emergency_replacement_reviewed",
    "codeowners_reconciled",
    "review_rules_reconciled",
    "escalation_policy_reconciled",
    "repository_access_reviewed",
    "stale_access_reviewed",
    "ownerless_paths_reviewed",
    "primary_only_paths_reviewed",
    "two_person_control_reviewed",
    "owner_coverage_approved",
    "release_authority_approved",
    "release_promotion_approved",
    "stable_signing_approved",
    "update_trust_approved",
    "supported_version_changes_approved",
    "security_disclosure_approved",
    "irreversible_migration_approved",
    "legal_approval_supported",
    "incident_closure_approved",
    "production_authority_approved",
    "broad_readiness_approved",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "ownership_inventory",
    "qualification_record_set",
    "owner_reviewer",
    "independent_reviewer",
    "security_reviewer",
    "release_operations_reviewer",
    "legal_reviewer",
    "support_reviewer",
]

REQUIRED_SCOPE_TERMS = [
    "program",
    "architecture",
    "security",
    "release-operations",
    "human-release-authority",
    "incident-response",
    "legal-community",
    "support",
    "quality",
    "supply-chain",
    "documentation-research",
    "product",
    "platform",
    "engine",
    "javascript",
    "networking",
    "storage",
    "performance",
    "accessibility",
    "ui-runtime",
    "agent-operations",
    "privacy-data",
]

REQUIRED_QUALIFICATION_TERMS = [
    "role level",
    "subsystem competence",
    "representative path coverage",
    "recent review record",
    "availability",
    "succession",
    "recusal",
    "inactivity",
    "removal",
    "emergency replacement",
]

REQUIRED_RECONCILIATION_TERMS = [
    "CODEOWNERS",
    "review-rule",
    "escalation-policy",
    "support",
    "signing",
    "disclosure",
    "package",
    "CI",
    "service",
    "repository-access",
    "no stale privileged access",
    "ownerless protected-path",
    "primary-only path",
    "blocked-status",
    "single-owner residual-risk",
]

REQUIRED_TWO_PERSON_TERMS = [
    "stable signing",
    "update trust",
    "supported-version changes",
    "security-disclosure",
    "irreversible profile migration",
    "release promotion",
    "legal approval",
    "incident closure",
]

REQUIRED_AUTHORITY_TERMS = [
    "owner coverage",
    "release authority",
    "release promotion",
    "stable signing authority",
    "update trust",
    "supported-version changes",
    "security-disclosure authority",
    "irreversible profile migration",
    "legal approval",
    "incident closure",
    "production authority",
    "broad readiness",
    "implementation",
]

REQUIRED_OWNER_REVIEW_TERMS = [
    "owner review",
    "independent review",
    "security review",
    "release-operations review",
    "legal review",
    "support review",
    "evidence retention",
    "blocked",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "self-nomination",
    "owner identity",
    "role level",
    "subsystem competence",
    "path coverage",
    "recent review",
    "availability",
    "succession",
    "recusal",
    "inactivity",
    "removal",
    "emergency replacement",
    "CODEOWNERS",
    "review-rule",
    "escalation-policy",
    "repository access",
    "stale privileged access",
    "ownerless protected-path",
    "primary-only path",
    "two-person control",
    "release authority",
    "signing authority",
    "disclosure authority",
    "legal approval",
    "incident closure",
    "production authority",
    "broad readiness",
    "implementation",
    "claim boundary",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_backup_ownership_readiness_review.py",
    "python3 -B tools/validate_backup_ownership_gap.py",
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
    replacements = [
        ("codeowners", "codeowners"),
        ("release operations", "release-operations"),
        ("backup owner", "backup-owner"),
        ("backup ownership", "backup-ownership"),
        ("two person", "two-person"),
        ("owner reviewed", "owner review"),
        ("owner-reviewed", "owner review"),
        ("path-coverage", "path coverage"),
        ("repository-access", "repository-access"),
        ("repository access", "repository access"),
        ("stale privileged-access", "stale privileged access"),
        ("ownerless protected path", "ownerless protected-path"),
        ("primary only path", "primary-only path"),
        ("supported version", "supported-version"),
        ("security disclosure", "security-disclosure"),
        ("irreversible migration", "irreversible profile migration"),
        ("stable-signing", "stable signing"),
    ]
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    return normalized


def axis_blob(data: dict[str, Any], keys: list[str]) -> str:
    chunks: list[str] = []
    for key in keys:
        for item in require_list(data, key):
            if isinstance(item, dict):
                chunks.append(" ".join(text(value) for value in item.values()))
    return normalize(" ".join(chunks))


def validate_review(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: review must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    review_id = text(data.get("review_id"))
    if not REVIEW_ID.fullmatch(review_id):
        fail(f"{path}: invalid review_id {review_id!r}")
    if data.get("status") != "no_claim_backup_ownership_readiness_template":
        fail(f"{path}: status must be no_claim_backup_ownership_readiness_template")

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
    for phrase in ["placeholder", "private contact", "null", "beyond the checked no-claim backup-ownership readiness-review template"]:
        if normalize(phrase) not in policy:
            fail(f"{path}: prohibited_placeholder_policy must mention {phrase}")

    status = require_object(data, "readiness_status")
    missing_status = sorted(set(READINESS_STATUS_FLAGS) - set(status))
    if missing_status:
        fail(f"{path}: readiness_status missing flags: {', '.join(missing_status)}")
    for flag in READINESS_STATUS_FLAGS:
        if status.get(flag) is not False:
            fail(f"{path}: readiness_status.{flag} must be false in the no-claim template")

    coverage_text = axis_blob(data, ["coverage_axes"])
    for phrase in REQUIRED_SCOPE_TERMS:
        if normalize(phrase) not in coverage_text:
            fail(f"{path}: coverage_axes must mention {phrase}")
    if "beyond the checked no-claim backup-ownership readiness-review template" not in coverage_text:
        fail(f"{path}: coverage axes must require evidence beyond the checked no-claim template")

    qualification_text = axis_blob(data, ["qualification_axes"])
    for phrase in REQUIRED_QUALIFICATION_TERMS:
        if normalize(phrase) not in qualification_text:
            fail(f"{path}: qualification_axes must mention {phrase}")

    reconciliation_text = axis_blob(data, ["reconciliation_axes"])
    for phrase in REQUIRED_RECONCILIATION_TERMS:
        if normalize(phrase) not in reconciliation_text:
            fail(f"{path}: reconciliation_axes must mention {phrase}")

    two_person_text = axis_blob(data, ["two_person_control_axes"])
    for phrase in REQUIRED_TWO_PERSON_TERMS:
        if normalize(phrase) not in two_person_text:
            fail(f"{path}: two_person_control_axes must mention {phrase}")

    authority_text = axis_blob(data, ["authority_boundary_axes"])
    for phrase in REQUIRED_AUTHORITY_TERMS:
        if normalize(phrase) not in authority_text:
            fail(f"{path}: authority_boundary_axes must mention {phrase}")

    owner_review_text = axis_blob(data, ["owner_review_axes"])
    for phrase in REQUIRED_OWNER_REVIEW_TERMS:
        if normalize(phrase) not in owner_review_text:
            fail(f"{path}: owner_review_axes must mention {phrase}")

    rejection_text = axis_blob(data, ["rejection_rules"])
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
            if isinstance(entry, dict) and entry.get("id") == "PB-019"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-019")
    if item.get("status") != "blocked":
        fail("PB-019 must remain blocked while backup ownership readiness is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-019 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-019 evidence is missing backup ownership readiness-review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim backup-ownership readiness-review template",
        "beyond the checked no-claim backup-ownership readiness-review template",
        "owner coverage",
        "two-person control",
        "release authority",
        "production authority",
        "implementation claim",
    ]:
        if normalize(phrase) not in required_text:
            fail(f"PB-019 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000008"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000008 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000008 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000008 allowed_paths missing backup ownership readiness-review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim backup-ownership readiness-review template",
        "owner coverage",
        "two-person control",
        "release authority",
        "production authority",
        "cannot be cited",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000008 must mention backup ownership review boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-ownership-review-capacity"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing ownership lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("ownership lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("ownership lane evidence_start missing backup ownership readiness-review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed backup ownership readiness review beyond the checked no-claim backup-ownership readiness-review template",
        "no owner-reviewed backup ownership readiness claim",
        "no owner coverage claim",
        "no two-person control claim",
        "no production authority claim",
        "no release authority claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"ownership lane must mention {phrase}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    print(f"backup ownership readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
