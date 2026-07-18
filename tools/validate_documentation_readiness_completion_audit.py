#!/usr/bin/env python3
"""Validate the checked no-claim documentation-readiness completion audit."""

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
DEFAULT_AUDIT = (
    DOCS
    / "project-buildout"
    / "machine"
    / "documentation-readiness-completion-audit.json"
)
DEFAULT_CLOSURE_REVIEW = (
    DOCS
    / "project-buildout"
    / "machine"
    / "build-readiness-closure-reviews"
    / "no-claim-build-readiness-closure-template.json"
)

AUDIT_ID = re.compile(r"^PB020\.DOCUMENTATION_READINESS_COMPLETION_AUDIT\.[A-Z0-9._-]+$")
CLOSURE_REVIEW_ID = re.compile(
    r"^PB020\.BUILD_READINESS_CLOSURE\.[A-Z0-9._-]+$"
)

REQUIRED_SOURCE_RECORDS = {
    "README.md",
    "docs/start-here.md",
    "docs/README.md",
    "docs/documentation-policy.md",
    "docs/repository-map.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/project-buildout/machine/implementation-kickoff-review.json",
    "docs/project-buildout/machine/build-readiness-dependency-graph.json",
    "docs/research/README.md",
    "docs/research/pre-build-readiness-gap-audit-2026-07.md",
    "docs/blueprint-v1/20-definition-of-done.md",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CRITERIA = {
    "DOC-READY-ENTRYPOINTS",
    "DOC-READY-STOP_RESUME",
    "DOC-READY-MACHINE_REGISTRIES",
    "DOC-READY-RESEARCH_LANES",
    "DOC-READY-TASK_HANDOFF",
    "DOC-READY-SEQUENCING",
    "DOC-READY-CLAIM_BOUNDARIES",
    "DOC-READY-VALIDATION",
    "DOC-READY-OWNER_DECISIONS",
    "DOC-READY-REMAINING_BLOCKERS",
}

REQUIRED_MISSING_TERMS = [
    "broad m1",
    "chrome-class",
    "performance",
    "security",
    "compatibility",
    "accessibility",
    "source strategy",
    "fresh-host",
    "ipc",
    "sandbox",
    "benchmark",
    "native-shell",
    "profile/session",
    "package/update",
    "incident response",
    "backup ownership",
]

REQUIRED_CLAIM_PHRASES = [
    "no complete documentation",
    "no all-information-ready-for-building",
    "no broad m1 implementation",
    "no task approval",
    "no readiness promotion",
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
    "docs/research/documentation-readiness-completion-audit-2026-07.md",
    "docs/project-buildout/machine/documentation-readiness-completion-audit.schema.json",
    "docs/project-buildout/machine/documentation-readiness-completion-audit.json",
    "docs/project-buildout/machine/build-readiness-closure-review.schema.json",
    "docs/project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json",
    "tools/validate_documentation_readiness_completion_audit.py",
]

REQUIRED_PB020_REQUIRED_TERMS = [
    "documentation-readiness completion audit",
    "completion audit",
    "remaining p0 items",
    "all-information-ready-for-building",
    "m1 expansion",
    "source strategy",
    "fresh-host",
    "ipc",
    "sandbox",
    "benchmark",
    "native-shell",
    "profile/session",
    "package/update",
    "incident response",
    "backup ownership",
    "owner review",
    "release authority",
    "build-readiness closure-review template",
    "closure-review",
]

REQUIRED_CLOSURE_SOURCE_RECORDS = {
    "README.md",
    "docs/start-here.md",
    "docs/README.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/research/pre-build-readiness-gap-audit-2026-07.md",
    "docs/research/implementation-kickoff-review-inventory-2026-07.md",
    "docs/project-buildout/machine/implementation-kickoff-review.json",
    "docs/research/build-readiness-dependency-graph-inventory-2026-07.md",
    "docs/project-buildout/machine/build-readiness-dependency-graph.json",
    "docs/research/documentation-readiness-completion-audit-2026-07.md",
    "docs/project-buildout/machine/documentation-readiness-completion-audit.json",
    "docs/project-buildout/machine/build-readiness-closure-review.schema.json",
    "docs/project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json",
    "docs/agent-execution/README.md",
    "docs/production-readiness/README.md",
    "docs/blueprint-v1/20-definition-of-done.md",
    "tools/validate_documentation_readiness_completion_audit.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLOSURE_CLAIM_PHRASES = [
    "no owner review",
    "no independent review",
    "no all-information-ready-for-building",
    "no broad m1 implementation",
    "no task approval",
    "no readiness promotion",
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
    "no release authority",
    "no production authority",
    "no daily-driver",
]

REQUIRED_CLOSURE_GATE_TERMS = [
    "pb-002",
    "pb-009",
    "pb-011",
    "pb-012",
    "pb-013",
    "pb-003",
    "pb-004",
    "pb-005",
    "pb-014",
    "pb-015",
    "pb-016",
    "pb-017",
    "pb-018",
    "pb-019",
    "pb-020",
    "source strategy",
    "fresh-host",
    "ipc",
    "sandbox",
    "benchmark",
    "native-shell",
    "page-surface",
    "profile/session",
    "package/update",
    "incident response",
    "backup ownership",
    "owner review",
    "release authority",
    "all-information-ready-for-building",
]

REQUIRED_CLOSURE_REJECTION_TERMS = [
    "template",
    "placeholder",
    "unresolved",
    "source strategy",
    "fresh-host",
    "ipc",
    "sandbox",
    "benchmark",
    "native",
    "accessibility",
    "profile/session",
    "package/update",
    "incident response",
    "backup ownership",
    "task approval",
    "validation",
    "exception",
    "release authority",
    "all-information-ready-for-building",
    "claim boundary",
]

CLOSURE_STATUS_FLAGS = [
    "owner_reviewed",
    "independent_reviewed",
    "all_pb_gates_closed",
    "all_tasks_approved",
    "all_information_ready_for_building",
    "broad_m1_authorized",
    "release_authority_granted",
    "production_authority_granted",
    "security_claim_supported",
    "performance_claim_supported",
    "compatibility_claim_supported",
    "accessibility_claim_supported",
    "daily_driver_claim_supported",
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
        ("source-strategy", "source strategy"),
        ("fresh host", "fresh-host"),
        ("native shell", "native-shell"),
        ("profile session", "profile/session"),
        ("profile-session", "profile/session"),
        ("package update", "package/update"),
        ("package-update", "package/update"),
        ("incident-response", "incident response"),
        ("backup-ownership", "backup ownership"),
        ("all information ready for building", "all-information-ready-for-building"),
        ("all-information ready for building", "all-information-ready-for-building"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def validate_audit(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: audit must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    audit_id = text(data.get("audit_id"))
    if not AUDIT_ID.fullmatch(audit_id):
        fail(f"{path}: invalid audit_id {audit_id!r}")
    if data.get("status") != "no_claim_completion_audit":
        fail(f"{path}: status must be no_claim_completion_audit")
    overall_status = normalize(text(data.get("overall_status")))
    if not overall_status or overall_status in {"complete", "completed", "ready"}:
        fail(f"{path}: overall_status must not claim completion")
    if "contained-m0" not in overall_status.replace("_", "-"):
        fail(f"{path}: overall_status must mention contained M0 scope")

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

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in source_records:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced source record does not exist: {source}")

    criteria = require_list(data, "criteria")
    criteria_by_id: dict[str, dict[str, Any]] = {}
    blocker_status_seen = False
    missing_text_parts: list[str] = []
    for criterion in criteria:
        if not isinstance(criterion, dict):
            fail(f"{path}: criteria entries must be objects")
        criterion_id = text(criterion.get("id"))
        if criterion_id in criteria_by_id:
            fail(f"{path}: duplicate criterion {criterion_id}")
        criteria_by_id[criterion_id] = criterion
        status = text(criterion.get("status"))
        if status not in {"ready_for_contained_m0", "partial", "blocked_for_full_goal"}:
            fail(f"{path}: {criterion_id} has invalid status {status!r}")
        if status in {"partial", "blocked_for_full_goal"}:
            blocker_status_seen = True
        for field in ["current_evidence", "missing_for_full_goal", "evidence_refs"]:
            require_list(criterion, field)
        if len(text(criterion.get("next_audit_action"))) < 20:
            fail(f"{path}: {criterion_id} has a short next_audit_action")
        claim_boundary = normalize(text(criterion.get("claim_boundary")))
        if "claim" not in claim_boundary or "no " not in claim_boundary:
            fail(f"{path}: {criterion_id} claim_boundary must preserve no-claim language")
        missing_text_parts.extend(
            text(value) for value in require_list(criterion, "missing_for_full_goal")
        )
        for ref in require_list(criterion, "evidence_refs"):
            ref_path = text(ref).split("#", 1)[0]
            if not (ROOT / ref_path).exists():
                fail(f"{path}: {criterion_id} evidence ref does not exist: {ref_path}")

    missing_criteria = sorted(REQUIRED_CRITERIA - set(criteria_by_id))
    if missing_criteria:
        fail(f"{path}: missing required criteria: {', '.join(missing_criteria)}")
    unexpected_criteria = sorted(set(criteria_by_id) - REQUIRED_CRITERIA)
    if unexpected_criteria:
        fail(f"{path}: unexpected criteria: {', '.join(unexpected_criteria)}")
    if not blocker_status_seen:
        fail(f"{path}: at least one criterion must remain partial or blocked")

    unresolved_groups = require_list(data, "unresolved_blocker_groups")
    for group in unresolved_groups:
        if not isinstance(group, dict):
            fail(f"{path}: unresolved_blocker_groups entries must be objects")
        require_list(group, "blockers")
        require_list(group, "source_refs")
        if len(text(group.get("missing_before_full_goal"))) < 30:
            fail(f"{path}: unresolved blocker group has short missing_before_full_goal")
        missing_text_parts.append(text(group.get("missing_before_full_goal")))
        for ref in require_list(group, "source_refs"):
            ref_path = text(ref).split("#", 1)[0]
            if not (ROOT / ref_path).exists():
                fail(f"{path}: unresolved blocker source ref does not exist: {ref_path}")

    missing_text = normalize(" ".join(missing_text_parts))
    for term in REQUIRED_MISSING_TERMS:
        if term not in missing_text:
            fail(f"{path}: missing full-goal blocker term: {term}")

    for proof in require_list(data, "next_required_proofs"):
        if len(text(proof)) < 20:
            fail(f"{path}: short next_required_proofs entry")

    validate_pb020_readiness(path)


def validate_closure_review(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: closure review must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    closure_review_id = text(data.get("closure_review_id"))
    if not CLOSURE_REVIEW_ID.fullmatch(closure_review_id):
        fail(f"{path}: invalid closure_review_id {closure_review_id!r}")
    if data.get("status") != "no_claim_build_readiness_closure_template":
        fail(f"{path}: status must be no_claim_build_readiness_closure_template")

    boundary_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[text(value) for value in require_list(data, "unsupported_boundaries")],
            ]
        )
    )
    for phrase in REQUIRED_CLOSURE_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing closure claim boundary phrase: {phrase}")

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_CLOSURE_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing closure source records: {', '.join(missing_sources)}")
    for source in source_records:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced closure source record does not exist: {source}")

    review_scope = require_object(data, "review_scope")
    for null_field in ["scope", "owner_reviewer", "independent_reviewer"]:
        if review_scope.get(null_field) is not None:
            fail(f"{path}: review_scope.{null_field} must remain null in template")
    if review_scope.get("review_status") != "template_only_no_review":
        fail(f"{path}: review_status must be template_only_no_review")
    placeholder_policy = normalize(text(review_scope.get("prohibited_placeholder_policy")))
    for term in ["placeholder", "self-approval", "private contact", "owner-reviewed"]:
        if term not in placeholder_policy:
            fail(f"{path}: prohibited placeholder policy must mention {term}")

    closure_status = require_object(data, "closure_status")
    for flag in CLOSURE_STATUS_FLAGS:
        if closure_status.get(flag) is not False:
            fail(f"{path}: closure_status.{flag} must be false in template")

    axis_text_parts: list[str] = []
    for key in [
        "gate_axes",
        "owner_review_axes",
        "release_authority_axes",
        "readiness_lifecycle",
    ]:
        for axis in require_list(data, key):
            if not isinstance(axis, dict):
                fail(f"{path}: {key} entries must be objects")
            for field in ["axis", "required_evidence", "template_status"]:
                if len(text(axis.get(field))) < 10:
                    fail(f"{path}: {key} entry has short {field}")
                axis_text_parts.append(text(axis.get(field)))

    axis_text = normalize(" ".join(axis_text_parts))
    for term in REQUIRED_CLOSURE_GATE_TERMS:
        if term not in axis_text:
            fail(f"{path}: closure review is missing gate term: {term}")

    rejection_text_parts: list[str] = []
    rejection_rules = require_list(data, "rejection_rules")
    for rule in rejection_rules:
        if not isinstance(rule, dict):
            fail(f"{path}: rejection_rules entries must be objects")
        rule_id = text(rule.get("id"))
        if not rule_id.startswith("reject_"):
            fail(f"{path}: rejection rule id must start with reject_: {rule_id}")
        for field in ["condition", "outcome"]:
            if len(text(rule.get(field))) < 20:
                fail(f"{path}: rejection rule {rule_id} has short {field}")
            rejection_text_parts.append(text(rule.get(field)))

    rejection_text = normalize(" ".join(rejection_text_parts))
    for term in REQUIRED_CLOSURE_REJECTION_TERMS:
        if term not in rejection_text:
            fail(f"{path}: closure rejection rules are missing term: {term}")

    validation_commands = set(text(value) for value in require_list(data, "validation_commands"))
    for command in [
        "python3 -B tools/validate_documentation_readiness_completion_audit.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in validation_commands:
            fail(f"{path}: missing validation command {command}")


def validate_pb020_readiness(path: Path) -> None:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb020 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-020"), None)
    if not isinstance(pb020, dict):
        fail("pre-build-readiness.json is missing PB-020")
    if pb020.get("status") != "partial":
        fail("PB-020 must remain partial after documentation-readiness completion audit")
    evidence = pb020.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-020 evidence must be an array")
    missing_evidence = [item for item in REQUIRED_PB020_EVIDENCE if item not in evidence]
    if missing_evidence:
        fail(
            "PB-020 evidence is missing documentation-readiness completion audit records: "
            + ", ".join(missing_evidence)
        )
    required_text = normalize(
        " ".join(value for value in pb020.get("evidence_required", []) if isinstance(value, str))
    )
    for term in REQUIRED_PB020_REQUIRED_TERMS:
        if term not in required_text:
            fail(f"PB-020 evidence_required must include {term}")
    for evidence_path in REQUIRED_PB020_EVIDENCE:
        if not (ROOT / evidence_path).exists():
            fail(f"PB-020 evidence path does not exist: {evidence_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_AUDIT),
        help="documentation readiness completion audit JSON path",
    )
    parser.add_argument(
        "--closure-review",
        default=str(DEFAULT_CLOSURE_REVIEW),
        help="build-readiness closure review template JSON path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validate_audit(Path(args.path))
    validate_closure_review(Path(args.closure_review))
    print("documentation-readiness completion audit validation passed: audit and closure-review template")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
