#!/usr/bin/env python3
"""Validate specified, non-executable manifests for proposed build tasks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "docs" / "blueprint-v1" / "machine" / "build-readiness-task-queue.json"
MANIFEST_DIR = ROOT / "docs" / "agent-execution" / "machine" / "tasks"
TASK_IDS = [f"TASK-{index:06d}" for index in range(1, 11)]

REQUIRED_KEYS = {
    "schema_version",
    "id",
    "status",
    "readiness_items",
    "owner",
    "independent_reviewer",
    "requirements",
    "risks",
    "allowed_paths",
    "prohibited_paths",
    "preconditions",
    "acceptance_criteria",
    "negative_tests",
    "resource_budget",
    "rollback",
    "dependencies",
}

# These fields define the queue-owned execution boundary and may not drift in a
# specified manifest. Human wording and approval-state fields are checked below.
IMMUTABLE_QUEUE_FIELDS = (
    "requirements",
    "risks",
    "adrs",
    "allowed_paths",
    "prohibited_paths",
    "resource_budget",
    "rollback",
    "dependencies",
    "expires_at",
    "readiness_items",
)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path}: cannot load JSON: {error}")
    if not isinstance(value, dict):
        fail(f"{path}: top-level value must be an object")
    return value


def fail(message: str) -> None:
    print(f"specified task manifest validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    queue = load(QUEUE_PATH)
    queue_digest = hashlib.sha256(
        json.dumps(queue, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest().upper()
    rows = queue.get("tasks")
    if not isinstance(rows, list):
        fail(f"{QUEUE_PATH}: tasks must be an array")
    by_id = {row.get("id"): row for row in rows if isinstance(row, dict)}
    if set(TASK_IDS) - set(by_id):
        fail(f"queue is missing task rows: {sorted(set(TASK_IDS) - set(by_id))}")

    for task_id in TASK_IDS:
        row = by_id[task_id]
        if row.get("status") != "proposed":
            fail(f"{task_id}: queue status must remain proposed")
        path = MANIFEST_DIR / f"{task_id}.json"
        if not path.exists():
            fail(f"{task_id}: specified manifest is missing at {path}")
        manifest = load(path)
        missing = sorted(REQUIRED_KEYS - set(manifest))
        if missing:
            fail(f"{task_id}: missing required fields: {', '.join(missing)}")
        if manifest.get("schema_version") != 1 or manifest.get("id") != task_id:
            fail(f"{task_id}: schema version or task ID is incorrect")
        if manifest.get("status") != "specified":
            fail(f"{task_id}: manifest status must remain specified")
        readiness_items = manifest.get("readiness_items")
        if not isinstance(readiness_items, list) or not readiness_items:
            fail(f"{task_id}: readiness_items must be a non-empty array")
        if any(not isinstance(item, str) or not re.fullmatch(r"PB-[0-9]{3}", item) for item in readiness_items):
            fail(f"{task_id}: readiness_items must contain PB-* IDs")
        for field in IMMUTABLE_QUEUE_FIELDS:
            if manifest.get(field) != row.get(field):
                fail(f"{task_id}: immutable queue field drifted: {field}")
        owner = str(manifest.get("owner", ""))
        reviewer = str(manifest.get("independent_reviewer", ""))
        if "name required before ready" not in owner or "name required before ready" not in reviewer:
            fail(f"{task_id}: owner and independent reviewer must remain named-identity placeholders")
        preconditions = manifest.get("preconditions")
        if not isinstance(preconditions, list):
            fail(f"{task_id}: preconditions must be an array")
        joined = " ".join(str(value) for value in preconditions)
        if "queue status remains proposed" not in joined:
            fail(f"{task_id}: missing proposed-status non-execution boundary")
        if queue_digest not in joined:
            fail(f"{task_id}: missing source queue digest {queue_digest}")
        if "specified manifest" not in joined or "non-executable" not in joined:
            fail(f"{task_id}: missing specified/non-executable boundary")
        if manifest.get("status") in {"reviewed", "ready", "running", "accepted"}:
            fail(f"{task_id}: manifest cannot authorize execution from this validator")

    print(f"specified task manifest validation passed: {len(TASK_IDS)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
