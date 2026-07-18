#!/usr/bin/env python3
"""Validate the checked blocked backup ownership gap inventory."""

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
DEFAULT_INVENTORY = (
    DOCS / "project-buildout" / "machine" / "backup-ownership-gap.json"
)
DEFAULT_QUALIFICATION_RECORD = (
    DOCS
    / "project-buildout"
    / "machine"
    / "backup-owner-qualification-records"
    / "no-claim-backup-owner-qualification-template.json"
)

INVENTORY_ID = re.compile(r"^OWN\.BACKUP\.[A-Z0-9._-]+$")
QUALIFICATION_RECORD_ID = re.compile(r"^OWN\.BACKUP_QUALIFICATION\.[A-Z0-9._-]+$")
SCOPE_ID = re.compile(r"^OWN-SCOPE-[A-Z0-9_]+$")

REQUIRED_SCOPES = [
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

REQUIRED_SOURCE_REGISTRIES = {
    ".github/CODEOWNERS",
    "docs/blueprint-v1/machine/professional-owners.json",
    "docs/blueprint-v1/machine/professional-review-rules.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
}

REQUIRED_QUALIFICATION_RECORD_SOURCES = {
    ".github/CODEOWNERS",
    "docs/research/backup-ownership-gap-inventory-2026-07.md",
    "docs/project-buildout/machine/backup-ownership-gap.schema.json",
    "docs/project-buildout/machine/backup-ownership-gap.json",
    "docs/project-buildout/machine/backup-owner-qualification-record.schema.json",
    "docs/project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json",
    "docs/blueprint-v1/machine/professional-owners.json",
    "docs/blueprint-v1/machine/professional-review-rules.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
}

QUALIFICATION_TERMS = {
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
}

RECONCILIATION_TERMS = {
    "codeowners",
    "review-rule",
    "escalation-policy",
    "support",
    "signing",
    "disclosure",
    "package",
    "ci",
    "service",
    "repository-access",
    "no stale privileged access",
    "ownerless protected-path",
    "primary-only path",
    "blocked-status",
    "single-owner residual-risk",
}

TWO_PERSON_TERMS = {
    "stable signing",
    "update trust",
    "supported-version changes",
    "security-disclosure",
    "irreversible profile migration",
    "release promotion",
    "legal approval",
    "incident closure",
}

REQUIRED_CLAIM_PHRASES = [
    "no broad readiness claim",
    "no production authority claim",
    "no release authority claim",
    "no release promotion claim",
    "no stable signing authority claim",
    "no update trust claim",
    "no supported-version changes claim",
    "no security-disclosure authority claim",
    "no irreversible migration approval claim",
    "no incident closure authority claim",
    "no legal approval claim",
    "no owner coverage claim",
    "no implementation claim",
]

REQUIRED_QUALIFICATION_RECORD_CLAIM_PHRASES = [
    "no named qualified backup",
    "no owner identity verification",
    "no role level review",
    "no subsystem competence review",
    "no representative path coverage",
    "no recent review record",
    "no availability record",
    "no codeowners reconciliation",
    "no review-rule reconciliation",
    "no stale privileged access review",
    "no two-person control",
    *REQUIRED_CLAIM_PHRASES,
]

REQUIRED_QUALIFICATION_LIFECYCLE = {
    "select_build_critical_scope",
    "name_candidate_backup",
    "verify_identity",
    "verify_role_level",
    "verify_subsystem_competence",
    "review_representative_paths",
    "verify_recent_review_record",
    "review_availability",
    "review_succession",
    "review_recusal",
    "review_inactivity_removal_emergency_replacement",
    "reconcile_codeowners",
    "reconcile_review_rules",
    "reconcile_escalation_policy",
    "review_repository_access",
    "review_ownerless_and_primary_only_paths",
    "review_two_person_control",
    "owner_review_close_or_hold",
}

REQUIRED_QUALIFICATION_REJECTION_TERMS = {
    "placeholder",
    "self-nomination",
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
    "codeowners",
    "review-rule",
    "escalation-policy",
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
}

QUALIFICATION_STATUS_FLAGS = [
    "named_backup_owner",
    "owner_identity_verified",
    "role_level_reviewed",
    "subsystem_competence_reviewed",
    "representative_path_coverage_reviewed",
    "recent_review_record_verified",
    "availability_reviewed",
    "succession_reviewed",
    "recusal_reviewed",
    "inactivity_reviewed",
    "removal_reviewed",
    "emergency_replacement_reviewed",
    "codeowners_reconciled",
    "review_rules_reconciled",
    "escalation_policy_reconciled",
    "stale_access_reviewed",
    "two_person_control_reviewed",
    "owner_reviewed",
]

SAFE_FAILURE_TERMS = {
    "block",
    "blocked",
    "keep",
    "reject",
    "stop",
    "hold",
    "escalate",
    "unavailable",
}


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


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(f"{key} must be an object")
    return value


def require_axis_list(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    values = require_list(data, key)
    axes: list[dict[str, Any]] = []
    for value in values:
        if not isinstance(value, dict):
            fail(f"{key} entries must be objects")
        for required in ("axis", "required_evidence", "template_status"):
            if not text(value.get(required)):
                fail(f"{key} entries must include {required}")
        axes.append(value)
    return axes


def axis_text(values: list[dict[str, Any]]) -> str:
    return " ".join(
        " ".join(text(value.get(key)).lower() for key in ("axis", "required_evidence", "template_status"))
        for value in values
    )


def normalized_terms(values: list[Any]) -> set[str]:
    return {text(value).strip().lower() for value in values}


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def validate_inventory(path: Path, data: dict[str, Any] | None = None) -> None:
    data = data if data is not None else load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    inventory_id = text(data.get("inventory_id"))
    if not INVENTORY_ID.match(inventory_id):
        fail(f"{path}: invalid inventory_id {inventory_id!r}")
    if data.get("status") != "blocked_gap_inventory":
        fail(f"{path}: status must be blocked_gap_inventory")

    boundaries = [text(value).lower() for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")).lower(), *boundaries])
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    source_registries = set(text(value) for value in require_list(data, "source_registries"))
    missing_sources = sorted(REQUIRED_SOURCE_REGISTRIES - source_registries)
    if missing_sources:
        fail(f"{path}: missing source registry references: {', '.join(missing_sources)}")
    for source in REQUIRED_SOURCE_REGISTRIES:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced source registry does not exist: {source}")

    missing_qualification = sorted(
        QUALIFICATION_TERMS - normalized_terms(require_list(data, "qualification_evidence_required"))
    )
    if missing_qualification:
        fail(f"{path}: missing qualification evidence terms: {', '.join(missing_qualification)}")
    missing_reconciliation = sorted(
        RECONCILIATION_TERMS - normalized_terms(require_list(data, "reconciliation_evidence_required"))
    )
    if missing_reconciliation:
        fail(f"{path}: missing reconciliation evidence terms: {', '.join(missing_reconciliation)}")
    missing_two_person = sorted(
        TWO_PERSON_TERMS - normalized_terms(require_list(data, "two_person_control_required"))
    )
    if missing_two_person:
        fail(f"{path}: missing two-person-control terms: {', '.join(missing_two_person)}")

    owners = load_json(MACHINE / "professional-owners.json")
    if not isinstance(owners, dict):
        fail("professional-owners.json must be an object")
    owner_records = owners.get("owners")
    if not isinstance(owner_records, list):
        fail("professional-owners.json must contain an owners array")
    owner_by_scope = {
        item.get("scope"): item for item in owner_records if isinstance(item, dict)
    }

    scopes = require_list(data, "critical_scopes")
    seen_ids: list[str] = []
    seen_scopes: list[str] = []
    for item in scopes:
        if not isinstance(item, dict):
            fail(f"{path}: critical_scopes entries must be objects")
        item_id = text(item.get("id"))
        if not SCOPE_ID.match(item_id):
            fail(f"{path}: invalid scope id {item_id!r}")
        seen_ids.append(item_id)
        scope = text(item.get("scope"))
        seen_scopes.append(scope)
        owner = owner_by_scope.get(scope)
        if not isinstance(owner, dict):
            fail(f"{path}: critical scope lacks professional owner record: {scope}")
        if item.get("owner_record_status") != owner.get("status"):
            fail(f"{path}: {scope} owner_record_status does not match professional owner registry")
        if item.get("current_primary") != owner.get("primary"):
            fail(f"{path}: {scope} current_primary does not match professional owner registry")
        if item.get("current_backup") != owner.get("backup"):
            fail(f"{path}: {scope} current_backup does not match professional owner registry")
        if item.get("next_review") != owner.get("next_review"):
            fail(f"{path}: {scope} next_review does not match professional owner registry")
        if owner.get("backup") is None and item.get("gap_status") != "blocked_missing_backup":
            fail(f"{path}: {scope} must remain blocked_missing_backup while professional backup is null")
        if len(text(item.get("blocking_gap"))) < 40:
            fail(f"{path}: {scope} blocking_gap must be descriptive")
        required_evidence = text(item.get("required_evidence")).lower()
        for term in ("named qualified backup", "role level", "two-person-control"):
            if term not in required_evidence:
                fail(f"{path}: {scope} required_evidence must mention {term}")
        safe_failure = text(item.get("safe_failure")).lower()
        if not any(term in safe_failure for term in SAFE_FAILURE_TERMS):
            fail(f"{path}: {scope} safe_failure must keep claims blocked or unavailable")

    check_no_duplicates(seen_ids, "scope IDs")
    check_no_duplicates(seen_scopes, "critical scopes")
    if seen_scopes != REQUIRED_SCOPES:
        fail(
            f"{path}: critical scopes must match required order; found: "
            + ", ".join(seen_scopes)
        )

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    readiness_items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(readiness_items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb019 = next((item for item in readiness_items if item.get("id") == "PB-019"), None)
    if not isinstance(pb019, dict):
        fail("pre-build-readiness.json is missing PB-019")
    if pb019.get("status") != "blocked":
        fail("PB-019 must remain blocked while checked backup gap inventory has null backups")
    required_evidence = {
        "docs/research/backup-ownership-gap-inventory-2026-07.md",
        "docs/project-buildout/machine/backup-ownership-gap.schema.json",
        "docs/project-buildout/machine/backup-ownership-gap.json",
        "tools/validate_backup_ownership_gap.py",
    }
    pb019_evidence = pb019.get("evidence")
    if not isinstance(pb019_evidence, list):
        fail("PB-019 must list checked blocked gap inventory evidence")
    missing_pb019 = sorted(required_evidence - set(pb019_evidence))
    if missing_pb019:
        fail("PB-019 evidence is missing backup ownership records: " + ", ".join(missing_pb019))

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks") if isinstance(task_queue, dict) else None
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain a tasks array")
    task = next((item for item in tasks if item.get("id") == "TASK-000008"), None)
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000008")
    if task.get("status") != "proposed":
        fail("TASK-000008 must remain proposed until owner review converts it to an executable task")

    review_rules = load_json(MACHINE / "professional-review-rules.json")
    rules = review_rules.get("rules") if isinstance(review_rules, dict) else None
    if not isinstance(rules, list):
        fail("professional-review-rules.json must contain a rules array")
    rule_ids = {item.get("id") for item in rules if isinstance(item, dict)}
    for rule_id in ("REV-RELEASE", "REV-PRODUCTION-READINESS"):
        if rule_id not in rule_ids:
            fail(f"professional-review-rules.json is missing {rule_id}")
    owner_scopes = set(owner_by_scope)
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        reviewers = rule.get("reviewers")
        if not isinstance(reviewers, list):
            fail(f"{rule.get('id')}: reviewers must be an array")
        for reviewer in reviewers:
            if reviewer != "owner" and reviewer not in owner_scopes:
                fail(f"{rule.get('id')}: reviewer {reviewer!r} has no professional owner scope")

    codeowners = (ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    if "Qualified backups are required before preview" not in codeowners:
        fail("CODEOWNERS must keep the qualified-backups-required warning")
    if "@byronwade" not in codeowners:
        fail("CODEOWNERS must still expose the current provisional primary owner")


def validate_qualification_record(path: Path, data: dict[str, Any] | None = None) -> None:
    data = data if data is not None else load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: qualification record must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    record_id = text(data.get("qualification_record_id"))
    if not QUALIFICATION_RECORD_ID.match(record_id):
        fail(f"{path}: invalid qualification_record_id {record_id!r}")
    if data.get("status") != "no_claim_backup_owner_qualification_template":
        fail(f"{path}: status must be no_claim_backup_owner_qualification_template")

    boundaries = [text(value).lower() for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")).lower(), *boundaries])
    for phrase in REQUIRED_QUALIFICATION_RECORD_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing unsupported qualification boundary phrase: {phrase}")

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_QUALIFICATION_RECORD_SOURCES - source_records)
    if missing_sources:
        fail(f"{path}: missing qualification source records: {', '.join(missing_sources)}")
    for source in REQUIRED_QUALIFICATION_RECORD_SOURCES:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced qualification source record does not exist: {source}")

    candidate_scope = require_object(data, "candidate_scope")
    if candidate_scope.get("scope") is not None:
        fail(f"{path}: no-claim template scope must be null")
    if candidate_scope.get("candidate_backup") is not None:
        fail(f"{path}: no-claim template candidate_backup must be null")
    if candidate_scope.get("candidate_status") != "template_only_no_candidate":
        fail(f"{path}: candidate_status must be template_only_no_candidate")
    policy = text(candidate_scope.get("prohibited_placeholder_policy")).lower()
    for phrase in ("placeholder", "private contact", "owner-reviewed evidence"):
        if phrase not in policy:
            fail(f"{path}: prohibited placeholder policy must mention {phrase}")

    status = require_object(data, "qualification_status")
    for flag in QUALIFICATION_STATUS_FLAGS:
        if status.get(flag) is not False:
            fail(f"{path}: no-claim template flag {flag} must be false")

    qualification_text = axis_text(require_axis_list(data, "qualification_axes"))
    for phrase in QUALIFICATION_TERMS:
        if phrase not in qualification_text:
            fail(f"{path}: qualification_axes must include {phrase}")
    reconciliation_text = axis_text(require_axis_list(data, "reconciliation_axes"))
    for phrase in RECONCILIATION_TERMS:
        if phrase not in reconciliation_text:
            fail(f"{path}: reconciliation_axes must include {phrase}")
    two_person_text = axis_text(require_axis_list(data, "two_person_control_axes"))
    for phrase in TWO_PERSON_TERMS:
        if phrase not in two_person_text:
            fail(f"{path}: two_person_control_axes must include {phrase}")

    lifecycle_axes = {
        text(value.get("axis")) for value in require_axis_list(data, "qualification_lifecycle")
    }
    missing_lifecycle = sorted(REQUIRED_QUALIFICATION_LIFECYCLE - lifecycle_axes)
    if missing_lifecycle:
        fail(f"{path}: qualification_lifecycle is missing: {', '.join(missing_lifecycle)}")

    fixture_policy = require_object(data, "fixture_policy")
    for key, value in fixture_policy.items():
        if value is not True:
            fail(f"{path}: fixture_policy {key} must be true")

    rejection_text = " ".join(
        " ".join(text(rule.get(key)).lower() for key in ("id", "condition", "outcome"))
        for rule in require_list(data, "rejection_rules")
        if isinstance(rule, dict)
    )
    for phrase in REQUIRED_QUALIFICATION_REJECTION_TERMS:
        if phrase not in rejection_text:
            fail(f"{path}: rejection_rules must mention {phrase}")

    commands = normalized_terms(require_list(data, "validation_commands"))
    for command in (
        "python3 -b tools/validate_backup_ownership_gap.py",
        "python3 -b tools/validate_blueprint.py",
    ):
        if command not in commands:
            fail(f"{path}: validation_commands must include {command}")

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    readiness_items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(readiness_items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb019 = next((item for item in readiness_items if item.get("id") == "PB-019"), None)
    if not isinstance(pb019, dict):
        fail("pre-build-readiness.json is missing PB-019")
    pb019_evidence = pb019.get("evidence")
    required_evidence = {
        "docs/project-buildout/machine/backup-owner-qualification-record.schema.json",
        "docs/project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json",
    }
    if not isinstance(pb019_evidence, list):
        fail("PB-019 must list backup owner qualification template evidence")
    missing_pb019 = sorted(required_evidence - set(pb019_evidence))
    if missing_pb019:
        fail("PB-019 evidence is missing qualification template records: " + ", ".join(missing_pb019))
    evidence_required = " ".join(
        text(value).lower() for value in pb019.get("evidence_required", [])
    )
    for phrase in (
        "checked no-claim backup-owner qualification template",
        "beyond the checked no-claim backup-owner qualification template",
    ):
        if phrase not in evidence_required:
            fail(f"PB-019 evidence_required must mention {phrase}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inventories",
        nargs="*",
        type=Path,
        default=[DEFAULT_INVENTORY, DEFAULT_QUALIFICATION_RECORD],
        help="Backup ownership gap inventory or qualification-record JSON files to validate.",
    )
    args = parser.parse_args()
    inventory_count = 0
    qualification_count = 0
    for path in args.inventories:
        data = load_json(path)
        if not isinstance(data, dict):
            fail(f"{path}: JSON root must be an object")
        if "inventory_id" in data:
            validate_inventory(path, data)
            inventory_count += 1
        elif "qualification_record_id" in data:
            validate_qualification_record(path, data)
            qualification_count += 1
        else:
            fail(f"{path}: unrecognized backup ownership record shape")
    print(
        "backup ownership gap validation passed: "
        f"{inventory_count} inventory file(s), "
        f"{qualification_count} qualification-record template(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
