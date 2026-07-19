#!/usr/bin/env python3
"""Validate the checked no-claim implementation kickoff review inventory."""

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
    DOCS / "project-buildout" / "machine" / "implementation-kickoff-review.json"
)

INVENTORY_ID = re.compile(r"^PB020\.KICKOFF\.[A-Z0-9._-]+$")
GATE_ID = re.compile(r"^KICKOFF-GATE-[A-Z0-9_]+$")

REQUIRED_ITEMS = {
    "PB-002": "blocked",
    "PB-003": "partial",
    "PB-004": "partial",
    "PB-005": "partial",
    "PB-008": "partial",
    "PB-009": "partial",
    "PB-011": "partial",
    "PB-012": "partial",
    "PB-013": "documented_no_runner",
    "PB-014": "partial",
    "PB-015": "partial",
    "PB-016": "partial",
    "PB-017": "partial",
    "PB-018": "partial",
    "PB-019": "blocked",
}

REQUIRED_SOURCE_RECORDS = {
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/project-buildout/23-owner-decision-closure-board.md",
    "docs/research/pre-build-readiness-gap-audit-2026-07.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/agent-execution/README.md",
    "docs/production-readiness/README.md",
    "docs/blueprint-v1/20-definition-of-done.md",
}

REQUIRED_GATES = {
    "source-strategy",
    "fresh-host-reproduction",
    "ipc-boundary",
    "sandbox-probes",
    "benchmark-claims",
    "native-shell",
    "profile-session",
    "package-update",
    "incident-response",
    "backup-ownership",
    "owner-review-release-authority",
}

REQUIRED_BEFORE_M1_TERMS = {
    "adr-0009",
    "fresh-host",
    "toolchain",
    "ipc",
    "sandbox",
    "benchmark",
    "adr-0013",
    "adr-0014",
    "ui-gate-7",
    "adr-0016",
    "profile",
    "research-package",
    "incident",
    "backup",
}

REQUIRED_CLAIM_PHRASES = [
    "no broad m1 implementation claim",
    "no developer preview claim",
    "no beta claim",
    "no stable claim",
    "no production claim",
    "no chrome-class claim",
    "no faster/lower-memory/lower-energy claim",
    "no compatibility claim",
    "no security claim",
    "no accessibility claim",
    "no daily-driver claim",
    "no release readiness claim",
    "no task approval claim",
    "no readiness promotion claim",
]

REQUIRED_PB020_EVIDENCE = [
    "docs/research/implementation-kickoff-review-inventory-2026-07.md",
    "docs/project-buildout/machine/implementation-kickoff-review.schema.json",
    "docs/project-buildout/machine/implementation-kickoff-review.json",
    "tools/validate_implementation_kickoff_review.py",
]

REQUIRED_PB020_REQUIRED_TERMS = [
    "implementation kickoff review inventory",
    "remaining p0 items",
    "owner review",
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
    "release authority",
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


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("fresh host", "fresh-host"),
        ("m1", "m1"),
        ("chrome class", "chrome-class"),
        ("profile session", "profile/session"),
        ("profile-session", "profile/session"),
        ("package update", "package/update"),
        ("package-update", "package/update"),
        ("incident-response", "incident response"),
        ("backup-ownership", "backup ownership"),
        ("source-strategy", "source strategy"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def validate_inventory(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    inventory_id = text(data.get("inventory_id"))
    if not INVENTORY_ID.fullmatch(inventory_id):
        fail(f"{path}: invalid inventory_id {inventory_id!r}")
    if data.get("status") != "no_claim_kickoff_inventory":
        fail(f"{path}: status must be no_claim_kickoff_inventory")

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
    for source in REQUIRED_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced source record does not exist: {source}")

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    readiness_items = readiness.get("items")
    if not isinstance(readiness_items, list):
        fail("pre-build-readiness.json must contain an items array")
    readiness_by_id = {
        item.get("id"): item for item in readiness_items if isinstance(item, dict)
    }

    inventory_items = require_list(data, "readiness_items")
    seen_item_ids: list[str] = []
    required_before_text_parts: list[str] = []
    prohibited_text_parts: list[str] = []
    for item in inventory_items:
        if not isinstance(item, dict):
            fail(f"{path}: readiness_items entries must be objects")
        item_id = text(item.get("id"))
        seen_item_ids.append(item_id)
        if item_id not in REQUIRED_ITEMS:
            fail(f"{path}: unexpected readiness item {item_id}")
        expected_status = REQUIRED_ITEMS[item_id]
        actual_status = text(item.get("status"))
        if actual_status != expected_status:
            fail(f"{path}: {item_id} status must be {expected_status}")
        registry_item = readiness_by_id.get(item_id)
        if not isinstance(registry_item, dict):
            fail(f"pre-build-readiness.json is missing {item_id}")
        if registry_item.get("status") != actual_status:
            fail(
                f"{path}: {item_id} status {actual_status} does not match "
                "pre-build-readiness.json"
            )
        if registry_item.get("status") == "ready":
            fail(f"{path}: {item_id} must not be ready in kickoff inventory")
        if text(item.get("owner_scope")) != text(registry_item.get("owner_scope")):
            fail(f"{path}: {item_id} owner_scope does not match pre-build readiness")
        for field in [
            "current_evidence",
            "required_before_m1",
            "first_next_actions",
            "owner_only_decisions",
            "prohibited_claims",
            "validation_or_evidence_refs",
        ]:
            require_list(item, field)
        required_before_text_parts.extend(
            text(value) for value in require_list(item, "required_before_m1")
        )
        prohibited_text_parts.extend(
            text(value) for value in require_list(item, "prohibited_claims")
        )
        for ref in require_list(item, "validation_or_evidence_refs"):
            ref_path = text(ref).split("#", 1)[0]
            if not ref_path:
                fail(f"{path}: {item_id} has empty reference")
            if not (ROOT / ref_path).exists():
                fail(f"{path}: {item_id} reference does not exist: {ref_path}")

    check_no_duplicates(seen_item_ids, "readiness item ids")
    if set(seen_item_ids) != set(REQUIRED_ITEMS):
        missing = sorted(set(REQUIRED_ITEMS) - set(seen_item_ids))
        extra = sorted(set(seen_item_ids) - set(REQUIRED_ITEMS))
        fail(f"{path}: readiness item set mismatch; missing={missing}; extra={extra}")

    required_before_text = normalize(" ".join(required_before_text_parts))
    for term in REQUIRED_BEFORE_M1_TERMS:
        if term not in required_before_text:
            fail(f"{path}: required_before_m1 is missing term {term}")

    prohibited_text = normalize(" ".join([*prohibited_text_parts, boundary_text]))
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in prohibited_text:
            fail(f"{path}: prohibited_claims are missing phrase {phrase}")

    gates = require_list(data, "kickoff_gates")
    gate_names: list[str] = []
    gate_ids: list[str] = []
    gate_item_refs: set[str] = set()
    for gate in gates:
        if not isinstance(gate, dict):
            fail(f"{path}: kickoff_gates entries must be objects")
        gate_id = text(gate.get("id"))
        if not GATE_ID.fullmatch(gate_id):
            fail(f"{path}: invalid kickoff gate id {gate_id!r}")
        gate_ids.append(gate_id)
        gate_name = text(gate.get("gate"))
        gate_names.append(gate_name)
        if gate_name not in REQUIRED_GATES:
            fail(f"{path}: unexpected kickoff gate {gate_name}")
        related = require_list(gate, "related_readiness_items")
        for item_id in related:
            item_id_text = text(item_id)
            if item_id_text not in REQUIRED_ITEMS:
                fail(f"{path}: gate {gate_name} references unknown item {item_id_text}")
            gate_item_refs.add(item_id_text)
        for field in ["blocked_until", "owner_only_decision", "no_claim_boundary"]:
            value = text(gate.get(field))
            if len(value) < 20:
                fail(f"{path}: gate {gate_name} field {field} is too short")
    check_no_duplicates(gate_ids, "kickoff gate ids")
    check_no_duplicates(gate_names, "kickoff gate names")
    if set(gate_names) != REQUIRED_GATES:
        missing = sorted(REQUIRED_GATES - set(gate_names))
        extra = sorted(set(gate_names) - REQUIRED_GATES)
        fail(f"{path}: kickoff gate set mismatch; missing={missing}; extra={extra}")
    missing_item_gate_refs = sorted(set(REQUIRED_ITEMS) - gate_item_refs)
    if missing_item_gate_refs:
        fail(
            f"{path}: kickoff gates do not cover readiness items: "
            + ", ".join(missing_item_gate_refs)
        )

    check_readiness_records()


def check_readiness_records() -> None:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    by_id = {item.get("id"): item for item in items if isinstance(item, dict)}
    pb020 = by_id.get("PB-020")
    if not isinstance(pb020, dict):
        fail("pre-build-readiness.json is missing PB-020")
    if pb020.get("status") != "partial":
        fail("PB-020 must remain partial")
    evidence = pb020.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-020 evidence must be an array")
    missing_evidence = [
        value for value in REQUIRED_PB020_EVIDENCE if value not in evidence
    ]
    if missing_evidence:
        fail(
            "PB-020 evidence is missing implementation kickoff records: "
            + ", ".join(missing_evidence)
        )
    evidence_required_text = normalize(
        " ".join(
            value
            for value in pb020.get("evidence_required", [])
            if isinstance(value, str)
        )
    )
    for term in REQUIRED_PB020_REQUIRED_TERMS:
        if term not in evidence_required_text:
            fail(f"PB-020 evidence_required must mention {term}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "inventory",
        nargs="?",
        type=Path,
        default=DEFAULT_INVENTORY,
        help="Path to implementation-kickoff-review.json",
    )
    args = parser.parse_args(argv)
    validate_inventory(args.inventory)
    print("implementation kickoff review inventory validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
