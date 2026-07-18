#!/usr/bin/env python3
"""Validate ADR-0009 source-strategy evidence tracking."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
REGISTRY = MACHINE / "adr-0009-evidence.json"
DECISION_REVIEW = (
    MACHINE
    / "adr-0009-decision-reviews"
    / "no-claim-decision-review-template.json"
)
MATRIX = ROOT / "docs" / "project-buildout" / "15-adr-0009-evidence-traceability-matrix.md"
OWNERS = MACHINE / "professional-owners.json"
READINESS = MACHINE / "pre-build-readiness.json"
CLEAN_GENERATED_OUTPUT_REPORT = (
    "docs/research/servo-clean-generated-output-reproduction-2026-07.md"
)
GENERATED_OUTPUT_GENERATOR_MANIFEST = (
    "docs/research/servo-generated-output-generator-manifest-2026-07.md"
)

EVIDENCE_ID = re.compile(r"^ADR9-EV-\d{3}$")
DECISION_REVIEW_ID = re.compile(r"^ADR0009\.DECISION_REVIEW\.[A-Z0-9._-]+$")
MATRIX_ROW = re.compile(r"^\| `(?P<id>ADR9-EV-\d{3})` \|")

REQUIRED_DECISION_REVIEW_SOURCES = {
    "docs/project-buildout/09-servo-adoption-decision-framework.md",
    "docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md",
    "docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md",
    "docs/project-buildout/16-adr-0009-decision-draft.md",
    "docs/blueprint-v1/machine/adr-0009-evidence.schema.json",
    "docs/blueprint-v1/machine/adr-0009-evidence.json",
    "docs/blueprint-v1/machine/adr-0009-decision-review.schema.json",
    "docs/blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/17-architecture-decisions.md",
    "docs/blueprint-v1/20-definition-of-done.md",
    CLEAN_GENERATED_OUTPUT_REPORT,
    GENERATED_OUTPUT_GENERATOR_MANIFEST,
    "tools/validate_adr_0009_evidence.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_DECISION_CLAIM_PHRASES = [
    "no Servo source strategy",
    "no source baseline",
    "no feature profile",
    "no owner-selected option",
    "no dependency approval",
    "no component approval",
    "no JavaScript-runtime change",
    "no source import",
    "no source adoption",
    "no compatibility claim",
    "no performance claim",
    "no security claim",
    "no support commitment",
    "no release-code authorization",
    "no PB-002 readiness promotion",
    "no implementation claim",
]

REQUIRED_DECISION_STATUS_FLAGS = [
    "owner_selected_option",
    "source_baseline_selected",
    "feature_profile_selected",
    "evidence_items_closed",
    "exceptions_approved",
    "public_claim_diff_applied",
    "support_language_updated",
    "pb002_unblocked",
    "source_import_authorized",
    "servo_source_strategy_accepted",
    "component_approval_granted",
    "release_code_authorized",
]

REQUIRED_DECISION_AXIS_TERMS = [
    *[f"adr9-ev-{index:03d}" for index in range(1, 19)],
    "option a",
    "option b",
    "option c",
    "option d",
    "option e",
    "owner-selected option",
    "source baseline",
    "feature profile",
    "component boundaries",
    "javascript-runtime",
    "compatibility",
    "performance",
    "security",
    "maintenance",
    "public claim",
    "support language",
]

REQUIRED_DECISION_REJECTION_TERMS = [
    "template",
    "placeholder",
    "unclosed evidence",
    "source baseline",
    "dependency",
    "legal",
    "build replay",
    "component",
    "javascript-runtime",
    "compatibility",
    "performance",
    "security",
    "maintenance",
    "document",
    "exception",
    "release-code authorization",
]


class ValidationError(ValueError):
    pass


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(message: str) -> None:
    raise ValidationError(message)


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{relative(path)}: invalid JSON: {error}")


def require_object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def require_string(obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(f"{label}.{key} must be a non-empty string")
    return value


def require_string_array(
    obj: dict[str, object], key: str, label: str, *, allow_empty: bool = False
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        fail(f"{label}.{key} must be an array of non-empty strings")
    if not allow_empty and not value:
        fail(f"{label}.{key} must not be empty")
    return value


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("source-strategy", "source strategy"),
        ("java-script", "javascript"),
        ("release code", "release-code"),
        ("pb002", "pb-002"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def owner_scopes() -> set[str]:
    payload = require_object(load_json(OWNERS), "owners")
    owners = payload.get("owners")
    if not isinstance(owners, list):
        fail("professional-owners.json must contain an owners array")
    scopes = {item.get("scope") for item in owners if isinstance(item, dict)}
    return {scope for scope in scopes if isinstance(scope, str)}


def validate_registry(payload: dict[str, object], scopes: set[str]) -> list[dict[str, object]]:
    if payload.get("schema_version") != 1:
        fail("adr-0009-evidence.json must use schema_version 1")
    if payload.get("adr_id") != "ADR-0009":
        fail("adr-0009-evidence.json must track ADR-0009")
    if payload.get("readiness_gate") != "PB-002":
        fail("adr-0009-evidence.json must track PB-002")
    if payload.get("decision_status") != "no_source_strategy_decision":
        fail("ADR-0009 must remain no_source_strategy_decision until owner review")
    claim_status = require_string(payload, "claim_status", "registry")
    for phrase in [
        "no Servo source strategy",
        "no source baseline",
        "no dependency approval",
        "no component approval",
        "no compatibility claim",
        "no performance claim",
        "no release-code authorization",
    ]:
        if phrase not in claim_status:
            fail(f"ADR-0009 claim_status must mention: {phrase}")

    items_value = payload.get("items")
    if not isinstance(items_value, list):
        fail("registry.items must be an array")
    items: list[dict[str, object]] = []
    for index, value in enumerate(items_value, start=1):
        item = require_object(value, f"items[{index}]")
        items.append(item)
    expected_ids = [f"ADR9-EV-{index:03d}" for index in range(1, 19)]
    ids = [item.get("id") for item in items]
    if ids != expected_ids:
        fail(f"ADR-0009 evidence IDs must be ADR9-EV-001 through ADR9-EV-018; found {ids}")

    allowed_status = {
        "partial",
        "missing",
        "captured",
        "owner_review_required",
        "owner_reviewed",
        "blocked",
    }
    required_fields = {
        "id",
        "decision_area",
        "status",
        "owner_scopes",
        "existing_evidence",
        "missing_outputs",
        "next_action",
    }
    for item in items:
        item_id = require_string(item, "id", "item")
        if not EVIDENCE_ID.fullmatch(item_id):
            fail(f"{item_id}: invalid evidence ID")
        missing = required_fields - set(item)
        if missing:
            fail(f"{item_id}: missing fields: {', '.join(sorted(missing))}")
        status = require_string(item, "status", item_id)
        if status not in allowed_status:
            fail(f"{item_id}: unknown status: {status}")
        require_string(item, "decision_area", item_id)
        require_string(item, "next_action", item_id)
        item_scopes = require_string_array(item, "owner_scopes", item_id)
        unknown = sorted(set(item_scopes) - scopes)
        if unknown:
            fail(f"{item_id}: unknown owner scopes: {', '.join(unknown)}")
        evidence_paths = require_string_array(
            item, "existing_evidence", item_id, allow_empty=status == "missing"
        )
        missing_outputs = require_string_array(
            item, "missing_outputs", item_id, allow_empty=status == "owner_reviewed"
        )
        if status in {"partial", "captured", "owner_review_required"} and not evidence_paths:
            fail(f"{item_id}: {status} items require existing evidence")
        if status != "owner_reviewed" and not missing_outputs:
            fail(f"{item_id}: unresolved items require missing outputs")
        for evidence_path in evidence_paths:
            resolved = (ROOT / evidence_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"{item_id}: existing_evidence points outside repository: {evidence_path}")
            if not resolved.exists():
                fail(f"{item_id}: existing evidence path does not exist: {evidence_path}")
        if status == "blocked":
            blockers = require_string_array(item, "blocked_by", item_id)
            unknown_blockers = sorted(set(blockers) - set(expected_ids))
            if unknown_blockers:
                fail(f"{item_id}: unknown blocked_by IDs: {', '.join(unknown_blockers)}")
        elif "blocked_by" in item:
            fail(f"{item_id}: only blocked items may declare blocked_by")
    by_id = {str(item["id"]): item for item in items}
    ev007 = by_id["ADR9-EV-007"]
    ev007_evidence = require_string_array(ev007, "existing_evidence", "ADR9-EV-007")
    for required in [
        CLEAN_GENERATED_OUTPUT_REPORT,
        GENERATED_OUTPUT_GENERATOR_MANIFEST,
    ]:
        if required not in ev007_evidence:
            fail(f"ADR9-EV-007 existing_evidence must include {required}")
    ev007_missing = "\n".join(
        require_string_array(ev007, "missing_outputs", "ADR9-EV-007")
    )
    for phrase in [
        "feature-correct full clean-target",
        "independent-host comparison",
        "owner-reviewed generator manifest",
        "source-to-output",
    ]:
        if phrase not in ev007_missing:
            fail(f"ADR9-EV-007 missing_outputs must mention {phrase}")
    ev007_next_action = require_string(ev007, "next_action", "ADR9-EV-007")
    for phrase in [
        "owner-review the generator manifest",
        "feature-correct full clean target",
        "independent host",
    ]:
        if phrase not in ev007_next_action:
            fail(f"ADR9-EV-007 next_action must mention {phrase}")
    return items


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def normalize_status(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def validate_matrix(items: list[dict[str, object]]) -> None:
    text = MATRIX.read_text(encoding="utf-8")
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = MATRIX_ROW.match(line)
        if not match:
            continue
        row = split_markdown_row(line)
        if len(row) != 6:
            fail(f"{relative(MATRIX)}: malformed matrix row for {match.group('id')}")
        rows[match.group("id")] = row
    expected_ids = [str(item["id"]) for item in items]
    if list(rows) != expected_ids:
        fail(f"{relative(MATRIX)}: matrix IDs do not match registry IDs")
    for item in items:
        item_id = str(item["id"])
        row = rows[item_id]
        decision_area = row[1]
        status = normalize_status(row[2])
        owner_scope = [scope.strip() for scope in row[5].split(",")]
        if decision_area != item["decision_area"]:
            fail(f"{item_id}: matrix decision area differs from registry")
        if status != item["status"]:
            fail(f"{item_id}: matrix status differs from registry")
        if owner_scope != item["owner_scopes"]:
            fail(f"{item_id}: matrix owner scope differs from registry")
    if "The same status move must update [`adr-0009-evidence.json`]" not in text:
        fail(f"{relative(MATRIX)}: handoff rule must mention adr-0009-evidence.json")
    for phrase in [
        "clean generated-output reproduction probe",
        "generated-output generator manifest",
        "feature-correct full clean-target regeneration diff",
        "owner-reviewed generator manifest",
    ]:
        if phrase not in text:
            fail(f"{relative(MATRIX)}: matrix must mention {phrase}")


def validate_readiness() -> None:
    readiness = require_object(load_json(READINESS), "readiness")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    pb002 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-002"), None)
    if not isinstance(pb002, dict):
        fail("pre-build-readiness.json is missing PB-002")
    if pb002.get("status") != "blocked":
        fail("PB-002 must remain blocked while ADR-0009 is unresolved")
    evidence = pb002.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-002 evidence must be an array")
    for required in [
        "docs/blueprint-v1/machine/adr-0009-evidence.schema.json",
        "docs/blueprint-v1/machine/adr-0009-evidence.json",
        "docs/blueprint-v1/machine/adr-0009-decision-review.schema.json",
        "docs/blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json",
        CLEAN_GENERATED_OUTPUT_REPORT,
        GENERATED_OUTPUT_GENERATOR_MANIFEST,
    ]:
        if required not in evidence:
            fail(f"PB-002 evidence must include {required}")
    evidence_required = require_string_array(pb002, "evidence_required", "PB-002")
    if not any("feature-correct full clean generated-output regeneration" in item for item in evidence_required):
        fail("PB-002 evidence_required must retain the feature-correct clean generated-output blocker")
    if not any("owner-reviewed generated-output generator manifest" in item for item in evidence_required):
        fail("PB-002 evidence_required must retain the owner-reviewed generated-output generator manifest blocker")


def validate_decision_review() -> None:
    payload = require_object(load_json(DECISION_REVIEW), "decision review")
    if payload.get("schema_version") != 1:
        fail("ADR-0009 decision review template must use schema_version 1")
    review_id = require_string(payload, "review_id", "decision review")
    if not DECISION_REVIEW_ID.fullmatch(review_id):
        fail(f"ADR-0009 decision review has invalid review_id: {review_id}")
    if payload.get("status") != "no_claim_decision_review_template":
        fail("ADR-0009 decision review status must be no_claim_decision_review_template")

    boundary_text = "\n".join(
        [
            require_string(payload, "claim_status", "decision review"),
            *require_string_array(payload, "unsupported_boundaries", "decision review"),
        ]
    )
    for phrase in REQUIRED_DECISION_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"ADR-0009 decision review claim boundary must mention: {phrase}")

    source_records = set(require_string_array(payload, "source_records", "decision review"))
    missing_sources = sorted(REQUIRED_DECISION_REVIEW_SOURCES - source_records)
    if missing_sources:
        fail(
            "ADR-0009 decision review is missing source records: "
            + ", ".join(missing_sources)
        )
    for source in source_records:
        resolved = (ROOT / source).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f"ADR-0009 decision review source is outside repository: {source}")
        if not resolved.exists():
            fail(f"ADR-0009 decision review source does not exist: {source}")

    review_scope = require_object(payload.get("review_scope"), "decision review.review_scope")
    for key in [
        "selected_option",
        "source_baseline",
        "feature_profile",
        "owner_reviewer",
        "independent_reviewer",
    ]:
        if review_scope.get(key) is not None:
            fail(f"ADR-0009 decision review {key} must remain null in template")
    if review_scope.get("review_status") != "template_only_no_decision":
        fail("ADR-0009 decision review must remain template_only_no_decision")
    policy = normalize(require_string(review_scope, "prohibited_placeholder_policy", "review_scope"))
    for term in ["placeholder", "self-approval", "source adoption", "owner-reviewed"]:
        if term not in policy:
            fail(f"ADR-0009 decision review placeholder policy must mention {term}")

    decision_status = require_object(payload.get("decision_status"), "decision review.decision_status")
    for flag in REQUIRED_DECISION_STATUS_FLAGS:
        if decision_status.get(flag) is not False:
            fail(f"ADR-0009 decision review decision_status.{flag} must be false")

    axis_text_parts: list[str] = []
    for key in [
        "evidence_axes",
        "option_axes",
        "owner_review_axes",
        "required_document_updates",
    ]:
        entries = payload.get(key)
        if not isinstance(entries, list) or not entries:
            fail(f"ADR-0009 decision review {key} must be a non-empty array")
        for index, entry_value in enumerate(entries, start=1):
            entry = require_object(entry_value, f"decision review.{key}[{index}]")
            for field in ["axis", "required_evidence", "template_status"]:
                value = require_string(entry, field, f"decision review.{key}[{index}]")
                axis_text_parts.append(value)
    axis_text = normalize("\n".join(axis_text_parts))
    for term in REQUIRED_DECISION_AXIS_TERMS:
        if term not in axis_text:
            fail(f"ADR-0009 decision review axes must mention: {term}")

    rejection_text_parts: list[str] = []
    rejection_rules = payload.get("rejection_rules")
    if not isinstance(rejection_rules, list) or not rejection_rules:
        fail("ADR-0009 decision review rejection_rules must be a non-empty array")
    for index, rule_value in enumerate(rejection_rules, start=1):
        rule = require_object(rule_value, f"decision review.rejection_rules[{index}]")
        rule_id = require_string(rule, "id", f"decision review.rejection_rules[{index}]")
        if not rule_id.startswith("reject_"):
            fail(f"ADR-0009 decision review rejection rule id must start with reject_: {rule_id}")
        rejection_text_parts.append(require_string(rule, "condition", rule_id))
        rejection_text_parts.append(require_string(rule, "outcome", rule_id))
    rejection_text = normalize("\n".join(rejection_text_parts))
    for term in REQUIRED_DECISION_REJECTION_TERMS:
        if term not in rejection_text:
            fail(f"ADR-0009 decision review rejection rules must mention: {term}")

    commands = set(require_string_array(payload, "validation_commands", "decision review"))
    for command in [
        "python3 -B tools/validate_adr_0009_evidence.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in commands:
            fail(f"ADR-0009 decision review missing validation command: {command}")


def main() -> int:
    try:
        scopes = owner_scopes()
        items = validate_registry(require_object(load_json(REGISTRY), "registry"), scopes)
        validate_decision_review()
        validate_matrix(items)
        validate_readiness()
    except ValidationError as error:
        print(f"ADR-0009 evidence validation failed: {error}", file=sys.stderr)
        return 1
    print(f"ADR-0009 evidence validation passed: {len(items)} evidence item(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
