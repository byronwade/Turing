#!/usr/bin/env python3
"""Validate checked no-claim incident/patch readiness-review templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
SECURITY_MACHINE = DOCS / "security-engine" / "machine"
DEFAULT_REVIEW = (
    SECURITY_MACHINE
    / "incident-patch-readiness-reviews"
    / "no-claim-incident-patch-readiness-template.json"
)

REVIEW_ID = re.compile(r"^SEC\.INCIDENT_READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/research/incident-patch-rehearsal-inventory-2026-07.md",
    "docs/security-engine/machine/incident-patch-rehearsal.schema.json",
    "docs/security-engine/machine/incident-patch-rehearsal.json",
    "docs/security-engine/machine/incident-patch-rehearsal-record.schema.json",
    "docs/security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json",
    "docs/security-engine/machine/incident-patch-readiness-review.schema.json",
    "docs/security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/security.md",
    "docs/security-engine/README.md",
    "docs/security-engine/05-update-supply-chain-and-vulnerability-response.md",
    "docs/security-engine/06-security-verification-and-release-gates.md",
    "docs/release-operations/README.md",
    "docs/release-operations/08-vulnerability-response-and-supported-lifecycle.md",
    "docs/production-readiness/README.md",
    "docs/production-readiness/06-security-and-vulnerability-response-gates.md",
    "docs/production-readiness/14-legal-signing-and-human-release-authority.md",
    "tools/validate_incident_patch_rehearsal.py",
    "tools/validate_incident_patch_readiness_review.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no independent review",
    "no security review",
    "no release-operations review",
    "no legal review",
    "no support review",
    "no executed private-intake tabletop",
    "no emergency patch dry run",
    "no regression or backport evidence",
    "no signing or update dry-run evidence",
    "no coordinated disclosure rehearsal",
    "no postmortem evidence",
    "no role matrix review",
    "no backup-owner coverage",
    "no incident-response readiness claim",
    "no emergency patch capacity claim",
    "no supported security versions claim",
    "no production-safe browsing claim",
    "no disclosure authority claim",
    "no stable promotion authority claim",
    "no signing authority claim",
    "no incident closure authority claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "independent_reviewed",
    "security_reviewed",
    "release_operations_reviewed",
    "legal_reviewed",
    "support_reviewed",
    "private_intake_tabletop_reviewed",
    "emergency_patch_dry_run_reviewed",
    "regression_backport_reviewed",
    "signing_update_dry_run_reviewed",
    "disclosure_rehearsal_reviewed",
    "postmortem_reviewed",
    "role_matrix_reviewed",
    "backup_owner_coverage_reviewed",
    "incident_response_readiness_approved",
    "emergency_patch_capacity_approved",
    "supported_security_versions_approved",
    "production_safe_browsing_approved",
    "disclosure_authority_approved",
    "stable_promotion_approved",
    "signing_authority_approved",
    "incident_closure_authority_approved",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "rehearsal_record",
    "reference_platform",
    "private_channel",
    "owner_reviewer",
    "independent_reviewer",
    "security_reviewer",
    "release_operations_reviewer",
    "legal_reviewer",
    "support_reviewer",
]

REQUIRED_REVIEW_FILES = [
    "docs/security-engine/machine/incident-patch-readiness-review.schema.json",
    "docs/security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json",
    "tools/validate_incident_patch_readiness_review.py",
]

REQUIRED_AXIS_TERMS = [
    "report access control",
    "acknowledgement",
    "reproduction",
    "severity",
    "asset analysis",
    "affected-version statement",
    "embargo handling",
    "sanitized evidence preservation",
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
    "active exploitation",
    "update or signing compromise",
    "dependency vulnerability",
    "data loss",
    "privacy leak",
    "sandbox regression",
    "malicious extension or provider",
    "service outage",
    "owner",
    "reviewer",
    "release",
    "security",
    "legal",
    "support",
    "on-call",
    "private channel",
    "redaction",
    "retention",
    "fake vulnerability",
    "fake signing keys",
    "backup-owner coverage",
    "secret rotation",
    "support targets",
    "incident-response review",
    "security review",
    "release-operations review",
    "legal review",
    "support review",
    "quality review",
    "production-readiness review",
    "documentation and registry update",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "public issue",
    "exploit",
    "agent",
    "severity",
    "disclosure",
    "incident closure",
    "stable promotion",
    "signing authority",
    "private intake",
    "emergency patch",
    "production signing keys",
    "offline root",
    "role matrix",
    "backup-owner coverage",
    "supported security",
    "production-safe browsing",
    "validation",
    "claim boundary",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_incident_patch_readiness_review.py",
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
        ("private intake", "private-intake"),
        ("emergency patch", "emergency patch"),
        ("dry run", "dry-run"),
        ("supported-security", "supported security"),
        ("supported security versions", "supported security versions"),
        ("production safe", "production-safe"),
        ("stable-promotion", "stable promotion"),
        ("incident-response", "incident-response"),
        ("incident response", "incident-response"),
        ("release operations", "release-operations"),
        ("production readiness", "production-readiness"),
        ("backup owner", "backup-owner"),
        ("owner-reviewed", "owner review"),
        ("cve", "cve"),
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
    if data.get("status") != "no_claim_incident_patch_readiness_template":
        fail(f"{path}: status must be no_claim_incident_patch_readiness_template")

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
                "private_intake_axes",
                "emergency_patch_axes",
                "incident_class_axes",
                "role_authority_axes",
                "evidence_control_axes",
                "owner_review_axes",
            ]
            for item in require_list(data, key)
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing incident/patch axis term: {phrase}")
    if "beyond the checked no-claim incident/patch readiness-review template" not in axis_text:
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
            if isinstance(entry, dict) and entry.get("id") == "PB-018"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-018")
    if item.get("status") != "partial":
        fail("PB-018 must remain partial while the incident/patch review is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-018 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-018 evidence is missing incident/patch readiness review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim incident/patch readiness-review template",
        "beyond the checked no-claim incident/patch readiness-review template",
        "incident-response readiness",
        "emergency patch capacity",
        "supported security versions",
        "production-safe browsing",
    ]:
        if normalize(phrase) not in required_text:
            fail(f"PB-018 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000010"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000010 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000010 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000010 allowed_paths missing incident/patch review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim incident/patch readiness-review template",
        "incident-response readiness",
        "emergency patch capacity",
        "supported security",
        "production-safe browsing",
        "cannot be cited",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000010 must mention incident/patch template boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-security-incident-patch-rehearsal"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing incident/patch lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("incident/patch lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("incident/patch lane evidence_start missing incident/patch review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed incident/patch readiness review beyond the checked no-claim incident/patch readiness-review template",
        "no owner review",
        "no incident-response readiness claim",
        "no emergency patch capacity claim",
        "no supported security versions claim",
        "no production-safe browsing claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"incident/patch lane must mention {phrase}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    print(f"incident/patch readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
