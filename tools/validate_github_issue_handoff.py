#!/usr/bin/env python3
"""Validate the offline GitHub issue handoff snapshot."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PROJECT_BUILDOUT = DOCS / "project-buildout"
MACHINE = PROJECT_BUILDOUT / "machine"
HANDOFF = PROJECT_BUILDOUT / "19-github-issue-handoff.md"
SNAPSHOT = MACHINE / "github-issue-handoff.json"
SCHEMA = MACHINE / "github-issue-handoff.schema.json"

EXPECTED_ISSUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]
EXPECTED_OPEN = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]
EXPECTED_CLOSED = [1]
EXPECTED_PRS = [42, 43]
REQUIRED_CLAIMS = [
    "Chrome-class",
    "production",
    "release",
    "compatibility",
    "performance",
    "security",
    "accessibility",
]


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}")
    if not isinstance(payload, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return payload


def require_string(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{context} must be a non-empty string")
    return value


def require_string_list(value: object, context: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{context} must be a non-empty string array")
    return list(value)


def check_schema_marker() -> None:
    schema = load_json(SCHEMA)
    if schema.get("schema_version") != 1:
        fail("github issue handoff schema must be schema_version 1")
    if schema.get("title") != "GitHub issue handoff snapshot schema":
        fail("github issue handoff schema title changed unexpectedly")


def check_snapshot() -> dict[str, object]:
    payload = load_json(SNAPSHOT)
    if payload.get("schema_version") != 1:
        fail("github issue handoff snapshot must be schema_version 1")

    snapshot = payload.get("snapshot")
    if not isinstance(snapshot, dict):
        fail("snapshot must be an object")
    if snapshot.get("repository") != "byronwade/Turing":
        fail("snapshot repository must be byronwade/Turing")
    observed_date = require_string(snapshot.get("observed_date"), "snapshot.observed_date")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", observed_date):
        fail("snapshot observed_date must be an explicit ISO date")
    baseline = require_string(snapshot.get("baseline_commit"), "snapshot.baseline_commit")
    if not re.fullmatch(r"[0-9a-f]{40}", baseline):
        fail("snapshot baseline_commit must be a full Git SHA")

    commands = require_string_list(snapshot.get("commands"), "snapshot.commands")
    for required in ("gh issue list", "gh pr list", "git rev-parse HEAD"):
        if not any(required in command for command in commands):
            fail(f"snapshot commands must include {required}")

    issue_numbers = snapshot.get("canonical_issue_numbers")
    if issue_numbers != EXPECTED_ISSUES:
        fail(f"canonical issue numbers must be {EXPECTED_ISSUES}; found {issue_numbers}")
    notes = snapshot.get("shared_numbering_notes")
    if not isinstance(notes, list) or not any(isinstance(note, dict) and note.get("number") == 13 for note in notes):
        fail("snapshot must explain why issue number 13 is absent")

    boundary = require_string(payload.get("claim_boundary"), "claim_boundary")
    for phrase in REQUIRED_CLAIMS:
        if phrase not in boundary:
            fail(f"claim_boundary must mention {phrase}")
    if "does not approve tasks" not in boundary:
        fail("claim_boundary must reject task approval")

    return payload


def check_issue_records(payload: dict[str, object]) -> None:
    issues = payload.get("issues")
    if not isinstance(issues, list) or not all(isinstance(item, dict) for item in issues):
        fail("issues must be an array of objects")
    numbers = [item.get("number") for item in issues]
    if numbers != EXPECTED_ISSUES:
        fail(f"issues must be ordered as {EXPECTED_ISSUES}; found {numbers}")

    for item in issues:
        number = item["number"]
        expected_state = "closed" if number in EXPECTED_CLOSED else "open"
        if item.get("state") != expected_state:
            fail(f"issue #{number} must be {expected_state}")
        require_string(item.get("title"), f"issue #{number} title")
        url = require_string(item.get("url"), f"issue #{number} url")
        if url != f"https://github.com/byronwade/Turing/issues/{number}":
            fail(f"issue #{number} URL is not canonical")
        records = require_string_list(item.get("canonical_records"), f"issue #{number} canonical_records")
        if not any(record.startswith(("WP-", "PB-", "TASK-", "RQ-", "M")) for record in records):
            fail(f"issue #{number} must map to canonical project records")
        require_string(item.get("disposition"), f"issue #{number} disposition")
        require_string_list(item.get("next_proof"), f"issue #{number} next_proof")
        blocked_claims = require_string_list(item.get("must_not_claim"), f"issue #{number} must_not_claim")
        unsupported_markers = (
            "claim",
            "readiness",
            "support",
            "safety",
            "compatibility",
            "production",
        )
        if number in EXPECTED_OPEN and not any(marker in claim for claim in blocked_claims for marker in unsupported_markers):
            fail(f"issue #{number} must retain unsupported-claim language")


def check_pr_cleanup(payload: dict[str, object]) -> None:
    records = payload.get("pull_request_cleanup")
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        fail("pull_request_cleanup must be an array of objects")
    numbers = [item.get("number") for item in records]
    if numbers != EXPECTED_PRS:
        fail(f"pull_request_cleanup must be ordered as {EXPECTED_PRS}; found {numbers}")
    for item in records:
        number = item["number"]
        if item.get("state") != "closed" or item.get("merged") is not False:
            fail(f"PR #{number} must be recorded as closed and not merged")
        if item.get("remote_branch_deleted") is not True:
            fail(f"PR #{number} must record remote branch deletion")
        commits = item.get("superseding_commits")
        if not isinstance(commits, list) or not commits or not all(isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit) for commit in commits):
            fail(f"PR #{number} must list full superseding commit SHAs")
        reason = require_string(item.get("reason"), f"PR #{number} reason")
        if "stale" not in reason or "main" not in reason:
            fail(f"PR #{number} reason must explain stale branch replacement on main")


def check_prose(payload: dict[str, object]) -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    snapshot = payload["snapshot"]
    assert isinstance(snapshot, dict)
    baseline = require_string(snapshot.get("baseline_commit"), "snapshot.baseline_commit")
    required = [
        "# GitHub Issue Handoff",
        "Status: coordination snapshot; no task approval",
        f"Baseline commit at observation: `{baseline}`.",
        "github-issue-handoff.json",
        "validate_github_issue_handoff.py",
        "Issue number `#13` is not a missing backlog issue",
        "A passing issue-handoff validation proves only that the offline snapshot is internally consistent",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"handoff prose missing required phrase: {phrase}")
    for number in EXPECTED_ISSUES:
        if f"[#{number}](https://github.com/byronwade/Turing/issues/{number})" not in text:
            fail(f"handoff prose must link issue #{number}")
    for item in payload["pull_request_cleanup"]:
        number = item["number"]
        if f"[#{number}](https://github.com/byronwade/Turing/pull/{number})" not in text:
            fail(f"handoff prose must link PR #{number}")


def main() -> int:
    try:
        check_schema_marker()
        payload = check_snapshot()
        check_issue_records(payload)
        check_pr_cleanup(payload)
        check_prose(payload)
    except ValueError as error:
        print(f"github issue handoff validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "github issue handoff validation passed: "
        "13 canonical issues, 1 closed baseline issue, 12 open backlog issues, "
        "2 closed stale PR branches"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
