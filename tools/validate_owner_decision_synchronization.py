#!/usr/bin/env python3
"""Validate the no-claim owner-decision synchronization matrix."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/project-buildout/machine/owner-decision-synchronization.json"
SCHEMA = ROOT / "docs/project-buildout/machine/owner-decision-synchronization.schema.json"
BOARD = ROOT / "docs/project-buildout/23-owner-decision-closure-board.md"

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

TASK_QUEUE_PATH = "docs/blueprint-v1/machine/build-readiness-task-queue.json"
TASK_MANIFESTS_BY_SCOPE = {
    frozenset({"PB-002", "ADR-0009"}): ("TASK-000001",),
    frozenset({"PB-003", "PB-004", "PB-005", "PB-014", "PB-015"}): ("TASK-000006",),
    frozenset({"PB-008", "PB-009"}): ("TASK-000002",),
    frozenset({"PB-011"}): ("TASK-000003", "TASK-000011"),
    frozenset({"PB-012"}): ("TASK-000004",),
    frozenset({"PB-013"}): ("TASK-000005",),
    frozenset({"PB-016"}): ("TASK-000007",),
    frozenset({"PB-017"}): ("TASK-000009",),
    frozenset({"PB-018"}): ("TASK-000010",),
    frozenset({"PB-019"}): ("TASK-000008",),
    frozenset({"PB-020"}): tuple(f"TASK-{index:06d}" for index in range(1, 12)),
}


def fail(message: str) -> None:
    print(f"owner-decision synchronization validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def require_strings(value: object, label: str, minimum: int) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{label} must contain at least {minimum} non-empty strings")
    return value


def main() -> int:
    try:
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read matrix or schema: {exc}")

    if schema.get("properties", {}).get("schema_version", {}).get("const") != 1:
        fail("schema must declare schema_version 1")
    if matrix.get("schema_version") != 1:
        fail("schema_version must be 1")
    if matrix.get("status") != "no_claim_owner_decision_synchronization_matrix":
        fail("status must remain no_claim_owner_decision_synchronization_matrix")
    claim = require_string(matrix.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "does not", "approve", "authority", "production"):
        if phrase not in claim:
            fail(f"claim_status must preserve {phrase!r} boundary")

    for record in require_strings(matrix.get("related_records"), "related_records", 8):
        if not (ROOT / record).is_file():
            fail(f"related record is missing: {record}")
    require_strings(matrix.get("validation_commands"), "validation_commands", 3)
    unsupported = require_strings(matrix.get("unsupported"), "unsupported", 8)
    if not any("passing validator" in value.lower() for value in unsupported):
        fail("unsupported must state that validation is not owner review")

    scopes = matrix.get("decision_scopes")
    if not isinstance(scopes, list) or len(scopes) != len(EXPECTED_SCOPES):
        fail("decision_scopes must contain exactly 11 canonical scopes")
    seen: set[frozenset[str]] = set()
    ids: set[str] = set()
    for index, record in enumerate(scopes):
        if not isinstance(record, dict):
            fail(f"decision_scopes[{index}] must be an object")
        scope_id = require_string(record.get("scope_id"), f"decision_scopes[{index}].scope_id")
        if scope_id in ids:
            fail(f"duplicate scope_id: {scope_id}")
        ids.add(scope_id)
        gate_scope = frozenset(require_strings(record.get("gate_scope"), f"decision_scopes[{index}].gate_scope", 1))
        if gate_scope not in EXPECTED_SCOPES:
            fail(f"decision_scopes[{index}] has a non-canonical gate scope")
        if gate_scope in seen:
            fail(f"decision_scopes[{index}] duplicates a gate scope")
        seen.add(gate_scope)
        for key in ("owner_role", "independent_reviewer_role"):
            require_string(record.get(key), f"decision_scopes[{index}].{key}")
        for key in ("required_evidence", "required_synchronization", "exception_policy", "prohibited_until"):
            values = require_strings(record.get(key), f"decision_scopes[{index}].{key}", 3)
            if key == "required_synchronization":
                for path in values:
                    if not path.startswith("docs/") and not path.startswith("tools/"):
                        fail(f"decision_scopes[{index}].required_synchronization has non-repository path: {path}")
                    if path.endswith("/"):
                        if not (ROOT / path).is_dir():
                            fail(f"required synchronization directory is missing: {path}")
                    elif not (ROOT / path).is_file():
                        fail(f"required synchronization file is missing: {path}")
                if TASK_QUEUE_PATH not in values:
                    fail(f"{scope_id}.required_synchronization must include the canonical task queue")
                expected_manifests = {
                    f"docs/agent-execution/machine/tasks/{task_id}.json"
                    for task_id in TASK_MANIFESTS_BY_SCOPE[gate_scope]
                }
                missing_manifests = sorted(expected_manifests - set(values))
                if missing_manifests:
                    fail(
                        f"{scope_id}.required_synchronization is missing task manifests: "
                        + ", ".join(missing_manifests)
                    )
    if seen != EXPECTED_SCOPES:
        fail("decision_scopes do not cover all canonical PB-020 scopes")

    try:
        board = BOARD.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read owner-decision closure board: {exc}")
    start_marker = "## Decision lanes"
    end_marker = "## Required decision record"
    if start_marker not in board or end_marker not in board:
        fail("owner-decision closure board is missing the decision-lanes section")
    lane_section = board.split(start_marker, 1)[1].split(end_marker, 1)[0]
    lane_rows = [
        line for line in lane_section.splitlines()
        if line.startswith("|") and line.count("|") >= 5 and not line.startswith("|---")
    ]
    if len(lane_rows) != len(EXPECTED_SCOPES) + 1:
        fail(f"owner-decision closure board must contain exactly 11 decision-lane rows; found {max(len(lane_rows) - 1, 0)}")
    board_scopes: set[frozenset[str]] = set()
    for row in lane_rows[1:]:
        gate_cell = row.split("|", 2)[1]
        scope = frozenset(re.findall(r"(?:PB|ADR)-\d+", gate_cell))
        if scope not in EXPECTED_SCOPES:
            fail(f"owner-decision closure board has a non-canonical decision-lane scope: {gate_cell.strip()}")
        if scope in board_scopes:
            fail(f"owner-decision closure board duplicates a decision-lane scope: {gate_cell.strip()}")
        board_scopes.add(scope)
    if board_scopes != EXPECTED_SCOPES:
        fail("owner-decision closure board does not cover the machine matrix gate scopes")

    print("owner-decision synchronization validation passed: 11 canonical scopes, no-claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
