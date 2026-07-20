#!/usr/bin/env python3
"""Validate the no-claim template and future real PB-020 closure packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW = (
    ROOT
    / "docs/project-buildout/machine/build-readiness-closure-reviews/"
    / "no-claim-build-readiness-closure-template.json"
)
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PLACEHOLDER_RE = re.compile(r"example|placeholder|no-claim|not a real|000000", re.I)

EXPECTED_SCOPES = {
    frozenset({"PB-002", "ADR-0009"}),
    frozenset({"PB-003", "PB-004", "PB-005", "PB-014", "PB-015"}),
    frozenset({"PB-008", "PB-009"}),
    frozenset({"PB-011"}),
    frozenset({"PB-012"}),
    frozenset({"PB-013"}),
    frozenset({"PB-016"}),
    frozenset({"PB-017"}),
    frozenset({"PB-018"}),
    frozenset({"PB-019"}),
    frozenset({"PB-020"}),
}

CLOSURE_PREPARATION = (
    ROOT / "docs/research/build-readiness-closure-and-owner-decision-preparation-2026-07.md"
)

REQUIRED_CLOSURE_WORKSHEET_TERMS = [
    "pb-020 closure worksheet",
    "review identity and snapshot",
    "gate reconciliation",
    "task and authority boundary",
    "evidence and failure accounting",
    "decision and exception",
    "claim and authority scope",
    "synchronization result",
    "final promotion decision",
    "does not replace their evidence",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"validation failed: missing closure review: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"validation failed: invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"validation failed: closure review must be an object: {path}")
    return value


def strings(value: Any) -> list[str]:
    return value if isinstance(value, list) and all(isinstance(item, str) for item in value) else []


def check_digest(errors: list[str], label: str, value: Any) -> None:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail(errors, f"{label} must be a lowercase sha256 digest")


def check_links(errors: list[str], source_records: list[str]) -> None:
    for record in source_records:
        if record.startswith(("http://", "https://", "mailto:")):
            continue
        target = (ROOT / record).resolve()
        if not target.is_file():
            fail(errors, f"source record does not resolve: {record}")


def validate_template(data: dict[str, Any], errors: list[str]) -> None:
    if data.get("status") != "no_claim_build_readiness_closure_template":
        fail(errors, "template validation requires the no-claim template status")
    scope = data.get("review_scope")
    if not isinstance(scope, dict) or scope.get("review_status") != "template_only_no_review":
        fail(errors, "template must have template_only_no_review review status")
    closure = data.get("closure_status")
    if not isinstance(closure, dict):
        fail(errors, "template is missing closure_status")
    else:
        for key, value in closure.items():
            if value is not False:
                fail(errors, f"template closure_status.{key} must remain false")
    records = data.get("decision_records")
    if not isinstance(records, list):
        fail(errors, "template decision_records must be an array")
    else:
        for index, record in enumerate(records):
            if not isinstance(record, dict) or record.get("status") != "unresolved_template":
                fail(errors, f"template decision_records[{index}] must remain unresolved_template")
    claim_status = str(data.get("claim_status", "")).lower()
    for phrase in ("no owner review", "no independent review", "no task approval", "no production claim"):
        if phrase not in claim_status:
            fail(errors, f"template claim_status is missing: {phrase}")


def validate_closure_preparation(errors: list[str]) -> None:
    if not CLOSURE_PREPARATION.is_file():
        fail(errors, f"missing PB-020 closure preparation: {CLOSURE_PREPARATION}")
        return
    content = CLOSURE_PREPARATION.read_text(encoding="utf-8").lower()
    for phrase in REQUIRED_CLOSURE_WORKSHEET_TERMS:
        if phrase not in content:
            fail(errors, f"PB-020 closure preparation is missing worksheet term: {phrase}")


def validate_real(data: dict[str, Any], errors: list[str]) -> None:
    if data.get("status") not in {"draft", "reviewed", "superseded"}:
        fail(errors, "real closure packet status must be draft, reviewed, or superseded")
    identity = data.get("packet_identity")
    if not isinstance(identity, dict):
        fail(errors, "real closure packet requires packet_identity")
    else:
        for key in ("source_commit", "platform", "toolchain", "configuration"):
            value = identity.get(key)
            if not isinstance(value, str) or not value.strip() or PLACEHOLDER_RE.search(value):
                fail(errors, f"packet_identity.{key} is missing or placeholder")
        for key in ("source_tree_digest", "registry_digest", "task_manifest_digest"):
            check_digest(errors, f"packet_identity.{key}", identity.get(key))
        if not isinstance(identity.get("collected_at"), str) or "T" not in identity["collected_at"]:
            fail(errors, "packet_identity.collected_at must be an ISO date-time")

    scope = data.get("review_scope")
    if not isinstance(scope, dict):
        fail(errors, "real closure packet requires review_scope")
    else:
        for key in ("scope", "owner_reviewer", "independent_reviewer"):
            value = scope.get(key)
            if not isinstance(value, str) or not value.strip() or PLACEHOLDER_RE.search(value):
                fail(errors, f"review_scope.{key} is missing or placeholder")
        if data.get("status") == "reviewed" and scope.get("review_status") != "owner_reviewed":
            fail(errors, "reviewed closure packet requires owner_reviewed review_status")

    records = data.get("decision_records")
    if not isinstance(records, list) or len(records) != len(EXPECTED_SCOPES):
        fail(errors, "real closure packet must contain exactly 11 decision records")
        records = []
    seen: set[frozenset[str]] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            fail(errors, f"decision_records[{index}] must be an object")
            continue
        scope_ids = frozenset(item for item in strings(record.get("gate_scope")) if re.fullmatch(r"PB-\d{3}", item) or item == "ADR-0009")
        if scope_ids not in EXPECTED_SCOPES:
            fail(errors, f"decision_records[{index}] has a non-canonical gate scope")
        if scope_ids in seen:
            fail(errors, f"decision_records[{index}] duplicates a gate scope")
        seen.add(scope_ids)
        status = record.get("status")
        if status not in {"selected", "rejected", "held"}:
            fail(errors, f"decision_records[{index}] cannot remain unresolved in a real packet")
        for key in ("decision", "rationale", "owner", "independent_reviewer"):
            value = record.get(key)
            if not isinstance(value, str) or not value.strip() or PLACEHOLDER_RE.search(value):
                fail(errors, f"decision_records[{index}].{key} is missing or placeholder")
        evidence_refs = strings(record.get("evidence_refs"))
        if not evidence_refs:
            fail(errors, f"decision_records[{index}] requires direct evidence_refs")
        digests = strings(record.get("evidence_digests"))
        if not digests:
            fail(errors, f"decision_records[{index}] requires evidence_digests")
        for digest in digests:
            check_digest(errors, f"decision_records[{index}].evidence_digests entry", digest)
        if not strings(record.get("validator_results")):
            fail(errors, f"decision_records[{index}] requires validator_results")
        if not strings(record.get("prohibited_claims")):
            fail(errors, f"decision_records[{index}] requires prohibited_claims")
        if record.get("authority_granted") is not False:
            fail(errors, f"decision_records[{index}] must set authority_granted to false")
        limitations = strings(record.get("unresolved_limitations"))
        if not limitations:
            fail(errors, f"decision_records[{index}] requires unresolved_limitations")
        registry_updates = strings(record.get("registry_updates"))
        if not registry_updates:
            fail(errors, f"decision_records[{index}] requires registry_updates")
        exception = record.get("exception")
        if status == "held":
            if not isinstance(exception, dict) or exception.get("status") in {None, "none_in_template"}:
                fail(errors, f"decision_records[{index}] held status requires an explicit exception")
            elif any(not exception.get(key) for key in ("owner", "risk_refs", "expires_at", "rollback", "support_boundary_change")):
                fail(errors, f"decision_records[{index}] exception is missing owner, risk, expiry, rollback, or support boundary")

    if seen != EXPECTED_SCOPES:
        fail(errors, "real closure packet does not cover the canonical PB-020 decision scopes")

    closure = data.get("closure_status")
    if not isinstance(closure, dict):
        fail(errors, "real closure packet requires closure_status")
    else:
        if any(value is True for key, value in closure.items() if key.endswith("_claim_supported")):
            if data.get("status") != "reviewed" or closure.get("owner_reviewed") is not True or closure.get("independent_reviewed") is not True:
                fail(errors, "supported claims require reviewed status and both owner and independent review")
        if closure.get("all_information_ready_for_building") is True and (
            closure.get("all_pb_gates_closed") is not True or closure.get("all_tasks_approved") is not True
        ):
            fail(errors, "all-information-ready-for-building requires all PB gates closed and all tasks approved")
        if closure.get("broad_m1_authorized") is True and closure.get("all_information_ready_for_building") is not True:
            fail(errors, "broad M1 authorization requires all-information-ready-for-building")
        if closure.get("release_authority_granted") is True and closure.get("production_authority_granted") is not True:
            fail(errors, "release authority requires production authority")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--closure-review", type=Path, default=DEFAULT_REVIEW)
    args = parser.parse_args()
    path = args.closure_review if args.closure_review.is_absolute() else ROOT / args.closure_review
    data = load(path)
    errors: list[str] = []
    required = {"schema_version", "closure_review_id", "status", "claim_status", "source_records", "review_scope", "decision_records", "closure_status", "validation_commands"}
    missing = sorted(required - data.keys())
    if missing:
        fail(errors, f"missing required top-level fields: {', '.join(missing)}")
    if data.get("schema_version") != 1:
        fail(errors, "schema_version must be 1")
    if not isinstance(data.get("source_records"), list) or len(data["source_records"]) < 14:
        fail(errors, "source_records must contain at least 14 paths")
    else:
        check_links(errors, data["source_records"])
    if path == DEFAULT_REVIEW or data.get("status") == "no_claim_build_readiness_closure_template":
        validate_template(data, errors)
    else:
        validate_real(data, errors)
    validate_closure_preparation(errors)
    if errors:
        for error in errors:
            print(f"validation failed: {error}", file=sys.stderr)
        return 1
    label = "template" if path == DEFAULT_REVIEW else "real closure packet"
    print(f"build-readiness closure review validation passed: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
