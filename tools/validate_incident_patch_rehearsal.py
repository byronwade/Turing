#!/usr/bin/env python3
"""Validate no-claim security incident and patch rehearsal inventories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = (
    ROOT / "docs" / "security-engine" / "machine" / "incident-patch-rehearsal.json"
)
DEFAULT_REHEARSAL_RECORD = (
    ROOT
    / "docs"
    / "security-engine"
    / "machine"
    / "incident-patch-rehearsal-records"
    / "no-claim-incident-patch-rehearsal-template.json"
)

EXERCISE_ID = re.compile(r"^SEC\.INCIDENT\.[A-Z0-9._-]+$")
REHEARSAL_ID = re.compile(r"^SEC\.INCIDENT_REHEARSAL\.[A-Z0-9._-]+$")
INTAKE_ID = re.compile(r"^SEC-INTAKE-[A-Z0-9._-]+$")
PATCH_ID = re.compile(r"^SEC-PATCH-[A-Z0-9._-]+$")
INCIDENT_ID = re.compile(r"^SEC-INCIDENT-[A-Z0-9._-]+$")
ROLE_ID = re.compile(r"^SEC-ROLE-[A-Z0-9._-]+$")

REQUIRED_INTAKE_STEPS = {
    "report access control",
    "acknowledgement",
    "reproduction",
    "severity",
    "asset analysis",
    "affected-version statement",
    "embargo handling",
    "sanitized evidence preservation",
}

REQUIRED_PATCH_STEPS = {
    "protected patch branch",
    "embargoed CI",
    "regression test",
    "backport decision",
    "signing and update dry run",
    "staged rollout",
    "minimum secure version",
    "revocation",
    "release notes",
    "user and admin communication",
    "CVE and credit handling",
    "coordinated disclosure",
    "postmortem remediation",
}

REQUIRED_INCIDENT_CLASSES = {
    "active exploitation",
    "update or signing compromise",
    "dependency vulnerability",
    "data loss",
    "privacy leak",
    "sandbox regression",
    "malicious extension or provider",
    "service outage",
}

REQUIRED_ROLES = {
    "owner",
    "reviewer",
    "release",
    "security",
    "legal",
    "support",
    "on-call",
}

REQUIRED_CLAIM_PHRASES = [
    "no production-safe browsing claim",
    "no supported security versions claim",
    "no incident-response readiness claim",
    "no emergency patch capacity claim",
    "no disclosure authority claim",
    "no stable promotion authority claim",
    "no signing authority claim",
    "no incident closure authority claim",
    "no implementation claim",
]

REQUIRED_REHEARSAL_RECORD_SOURCES = {
    "docs/research/incident-patch-rehearsal-inventory-2026-07.md",
    "docs/security-engine/machine/incident-patch-rehearsal.schema.json",
    "docs/security-engine/machine/incident-patch-rehearsal.json",
    "docs/security-engine/machine/incident-patch-rehearsal-record.schema.json",
    "docs/security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/security.md",
    "docs/security-engine/06-security-verification-and-release-gates.md",
    "docs/release-operations/08-vulnerability-response-and-supported-lifecycle.md",
    "docs/production-readiness/README.md",
}

REQUIRED_REHEARSAL_RECORD_CLAIM_PHRASES = [
    "no executed private-intake tabletop",
    "no emergency patch dry run",
    "no regression or backport evidence",
    "no signing or update dry-run evidence",
    "no coordinated disclosure rehearsal",
    "no postmortem evidence",
    "no role matrix review",
    "no backup-owner coverage",
    "no owner review",
    *REQUIRED_CLAIM_PHRASES,
]

REQUIRED_REHEARSAL_LIFECYCLE = {
    "restrict_private_channel",
    "acknowledge_report",
    "reproduce_privately",
    "triage_severity",
    "analyze_assets_versions",
    "set_embargo",
    "open_protected_patch_branch",
    "run_embargoed_ci",
    "verify_regression_backport",
    "dry_run_signing_update",
    "rehearse_rollout_revocation",
    "draft_communications_disclosure",
    "complete_postmortem",
    "review_roles_backups_close_or_hold",
}

REQUIRED_REJECTION_TERMS = [
    "public",
    "agent",
    "access control",
    "reproduction",
    "patch",
    "production signing",
    "regression",
    "communication",
    "role",
    "backup",
    "incident closure",
    "supported security",
    "redact",
]

SAFE_FAILURE_TERMS = [
    "abort",
    "block",
    "discard",
    "escalate",
    "hold",
    "keep",
    "preserve",
    "quarantine",
    "redact",
    "reject",
    "restrict",
    "stop",
]

AUTHORITY_TERMS = [
    "agent",
    "disclosure",
    "signing",
    "stable",
    "closure",
]


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing inventory: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        fail(f"{key} must be an array")
    return value


def require_string_list(data: dict[str, Any], key: str) -> list[str]:
    values = require_list(data, key)
    strings: list[str] = []
    for value in values:
        if not isinstance(value, str) or len(value) < 3:
            fail(f"{key} entries must be descriptive strings")
        strings.append(value)
    return strings


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def validate_step_collection(
    path: Path,
    items: list[Any],
    *,
    id_pattern: re.Pattern[str],
    id_label: str,
    key: str,
    required_values: set[str],
) -> None:
    ids: list[str] = []
    values: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            fail(f"{path}: {key} entries must be objects")
        item_id = text(item.get("id"))
        if not id_pattern.match(item_id):
            fail(f"{path}: invalid {id_label} id {item_id!r}")
        ids.append(item_id)
        step_value = text(item.get(key))
        values.append(step_value)
        for field in ["required_evidence", "authority_boundary", "safe_failure"]:
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: {item_id} {field} must be descriptive")
        authority = text(item.get("authority_boundary")).lower()
        if not any(term in authority for term in AUTHORITY_TERMS):
            fail(f"{path}: {item_id} authority_boundary must mention agent, disclosure, signing, stable, or closure authority")
        safe_failure = text(item.get("safe_failure")).lower()
        if not any(term in safe_failure for term in SAFE_FAILURE_TERMS):
            fail(f"{path}: {item_id} safe_failure must describe blocking, escalation, preservation, or rejection")
    check_no_duplicates(ids, id_label)
    missing = sorted(required_values - set(values))
    if missing:
        fail(f"{path}: missing {key} values: {', '.join(missing)}")


def validate_inventory(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    exercise_id = text(data.get("exercise_id"))
    if not EXERCISE_ID.match(exercise_id):
        fail(f"{path}: invalid exercise_id {exercise_id!r}")
    if data.get("status") != "no_claim_rehearsal_inventory":
        fail(f"{path}: status must be no_claim_rehearsal_inventory")

    claim_status = text(data.get("claim_status")).lower()
    boundaries = [text(item).lower() for item in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([claim_status, *boundaries])
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    validate_step_collection(
        path,
        require_list(data, "private_intake_steps"),
        id_pattern=INTAKE_ID,
        id_label="private intake step",
        key="step",
        required_values=REQUIRED_INTAKE_STEPS,
    )
    validate_step_collection(
        path,
        require_list(data, "emergency_patch_steps"),
        id_pattern=PATCH_ID,
        id_label="emergency patch step",
        key="step",
        required_values=REQUIRED_PATCH_STEPS,
    )

    incident_items = require_list(data, "incident_classes")
    incident_ids: list[str] = []
    incident_classes: list[str] = []
    for item in incident_items:
        if not isinstance(item, dict):
            fail(f"{path}: incident_classes entries must be objects")
        item_id = text(item.get("id"))
        if not INCIDENT_ID.match(item_id):
            fail(f"{path}: invalid incident class id {item_id!r}")
        incident_ids.append(item_id)
        incident_classes.append(text(item.get("incident_class")))
        for field in ["tabletop_scope", "blocking_gap", "safe_failure"]:
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: {item_id} {field} must be descriptive")
        safe_failure = text(item.get("safe_failure")).lower()
        if not any(term in safe_failure for term in SAFE_FAILURE_TERMS):
            fail(f"{path}: {item_id} safe_failure must describe blocking, escalation, preservation, or rejection")
    check_no_duplicates(incident_ids, "incident class IDs")
    missing_incidents = sorted(REQUIRED_INCIDENT_CLASSES - set(incident_classes))
    if missing_incidents:
        fail(f"{path}: missing incident classes: {', '.join(missing_incidents)}")

    role_items = require_list(data, "role_matrix")
    role_ids: list[str] = []
    roles: list[str] = []
    role_text = ""
    for item in role_items:
        if not isinstance(item, dict):
            fail(f"{path}: role_matrix entries must be objects")
        item_id = text(item.get("id"))
        if not ROLE_ID.match(item_id):
            fail(f"{path}: invalid role id {item_id!r}")
        role_ids.append(item_id)
        roles.append(text(item.get("role")))
        for field in ["responsibility", "authority_boundary", "missing_evidence"]:
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: {item_id} {field} must be descriptive")
            role_text += " " + value.lower()
    check_no_duplicates(role_ids, "role IDs")
    missing_roles = sorted(REQUIRED_ROLES - set(roles))
    if missing_roles:
        fail(f"{path}: missing roles: {', '.join(missing_roles)}")
    for term in ["timing", "escalation", "secret", "backup", "signing", "stable", "disclosure", "closure"]:
        if term not in role_text:
            fail(f"{path}: role matrix coverage missing term: {term}")


def validate_rehearsal_record(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: rehearsal record must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    rehearsal_id = text(data.get("rehearsal_id"))
    if not REHEARSAL_ID.match(rehearsal_id):
        fail(f"{path}: invalid rehearsal_id {rehearsal_id!r}")
    if data.get("status") != "no_claim_incident_patch_rehearsal_template":
        fail(f"{path}: status must be no_claim_incident_patch_rehearsal_template")

    claim_status = text(data.get("claim_status")).lower()
    boundaries = [
        text(item).lower() for item in require_list(data, "unsupported_boundaries")
    ]
    boundary_text = " ".join([claim_status, *boundaries])
    for phrase in REQUIRED_REHEARSAL_RECORD_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing rehearsal template boundary phrase: {phrase}")

    source_records = set(require_string_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_REHEARSAL_RECORD_SOURCES - source_records)
    if missing_sources:
        fail(f"{path}: missing source_records: {', '.join(missing_sources)}")

    rehearsal_status = data.get("rehearsal_status")
    if not isinstance(rehearsal_status, dict):
        fail(f"{path}: rehearsal_status must be an object")
    false_fields = [
        "private_intake_tabletop",
        "emergency_patch_dry_run",
        "regression_backport_evidence",
        "signing_update_dry_run",
        "disclosure_rehearsal",
        "role_matrix_review",
        "backup_owner_coverage",
        "owner_reviewed",
    ]
    for field in false_fields:
        if rehearsal_status.get(field) is not False:
            fail(f"{path}: rehearsal_status.{field} must be false for the no-claim template")
    if len(text(rehearsal_status.get("current_scope"))) < 60:
        fail(f"{path}: rehearsal_status.current_scope must be descriptive")

    for key, required_values in [
        ("private_intake_axes", REQUIRED_INTAKE_STEPS),
        ("emergency_patch_axes", REQUIRED_PATCH_STEPS),
        ("incident_class_axes", REQUIRED_INCIDENT_CLASSES),
        ("authority_role_axes", REQUIRED_ROLES),
    ]:
        values = set(require_string_list(data, key))
        missing_values = sorted(required_values - values)
        if missing_values:
            fail(f"{path}: {key} missing values: {', '.join(missing_values)}")

    lifecycle = require_list(data, "rehearsal_lifecycle")
    lifecycle_stages: list[str] = []
    lifecycle_text = ""
    for item in lifecycle:
        if not isinstance(item, dict):
            fail(f"{path}: rehearsal_lifecycle entries must be objects")
        stage = text(item.get("stage"))
        required_record = text(item.get("required_record"))
        lifecycle_stages.append(stage)
        lifecycle_text += " " + required_record.lower()
        if len(required_record) < 30:
            fail(f"{path}: lifecycle stage {stage!r} required_record is too short")
    check_no_duplicates(lifecycle_stages, "rehearsal lifecycle stages")
    missing_lifecycle = sorted(REQUIRED_REHEARSAL_LIFECYCLE - set(lifecycle_stages))
    if missing_lifecycle:
        fail(f"{path}: missing rehearsal lifecycle stages: {', '.join(missing_lifecycle)}")
    for term in [
        "private",
        "exploit",
        "severity",
        "embargo",
        "protected",
        "ci",
        "regression",
        "backport",
        "signing",
        "update",
        "rollout",
        "revocation",
        "disclosure",
        "postmortem",
        "backup",
    ]:
        if term not in lifecycle_text:
            fail(f"{path}: rehearsal lifecycle coverage missing term: {term}")

    fixture_policy = data.get("fixture_policy")
    if not isinstance(fixture_policy, dict):
        fail(f"{path}: fixture_policy must be an object")
    for field in [
        "private_channel_required",
        "exploit_details_public_prohibited",
        "production_signing_keys_prohibited",
        "stable_promotion_prohibited",
        "fake_vulnerability_required",
        "fake_update_dry_run_only",
        "sanitized_evidence_required",
        "backup_owner_review_required",
    ]:
        if fixture_policy.get(field) is not True:
            fail(f"{path}: fixture_policy.{field} must be true")

    rejection_rules = require_list(data, "rejection_rules")
    rejection_text = ""
    rule_ids: list[str] = []
    for item in rejection_rules:
        if not isinstance(item, dict):
            fail(f"{path}: rejection_rules entries must be objects")
        rule = text(item.get("rule"))
        condition = text(item.get("condition"))
        if len(rule) < 3 or len(condition) < 30:
            fail(f"{path}: rejection rule entries must be descriptive")
        rule_ids.append(rule)
        rejection_text += " " + condition.lower()
    check_no_duplicates(rule_ids, "rejection rules")
    for term in REQUIRED_REJECTION_TERMS:
        if term not in rejection_text:
            fail(f"{path}: rejection rules missing term: {term}")

    validation_commands = require_string_list(data, "validation_commands")
    for command in [
        "python3 -B tools/validate_incident_patch_rehearsal.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in validation_commands:
            fail(f"{path}: validation_commands missing {command}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "records",
        nargs="*",
        type=Path,
        default=[DEFAULT_INVENTORY, DEFAULT_REHEARSAL_RECORD],
        help="Incident patch rehearsal inventory or rehearsal-record JSON files to validate.",
    )
    args = parser.parse_args()
    inventory_count = 0
    rehearsal_record_count = 0
    for path in args.records:
        data = load_json(path)
        if not isinstance(data, dict):
            fail(f"{path}: record must be an object")
        if "exercise_id" in data:
            validate_inventory(path)
            inventory_count += 1
        elif "rehearsal_id" in data:
            validate_rehearsal_record(path)
            rehearsal_record_count += 1
        else:
            fail(f"{path}: record must contain exercise_id or rehearsal_id")
    print(
        "incident patch rehearsal validation passed: "
        f"{inventory_count} inventory file(s), "
        f"{rehearsal_record_count} rehearsal-record template(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
