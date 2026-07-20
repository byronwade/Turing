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

# These are the narrow closure records that must be editable together with the
# task. Broad directory entries are accepted when the queue intentionally owns
# an entire lane; exact entries protect against omissions in explicit lists.
REQUIRED_SCOPE_PATHS = {
    "TASK-000003": (
        "docs/research/ipc-transport-and-authority-closure-preparation-2026-07.md",
        "docs/research/ipc-wire-encoding-decision-prep-2026-07.md",
        "docs/research/ipc-transport-packet-examples-2026-07.md",
        "docs/research/task-000011-wp002-review-handoff-2026-07.md",
        "docs/research-log.md",
        "docs/blueprint-v1/machine/ipc-wire-source-manifest.json",
        "docs/blueprint-v1/machine/ipc-wire-source-manifest.schema.json",
        "tools/validate_ipc_wire_sources.py",
    ),
    "TASK-000004": (
        "docs/research/sandbox-probe-execution-and-containment-closure-preparation-2026-07.md",
        "docs/research/sandbox-platform-evidence-decision-prep-2026-07.md",
        "docs/research/sandbox-probe-result-packet-examples-2026-07.md",
        "docs/research-log.md",
    ),
    "TASK-000005": (
        "docs/research/benchmark-evidence-and-claim-closure-preparation-2026-07.md",
    ),
    "TASK-000006": (
        "docs/research/native-ui-and-accessibility-closure-preparation-2026-07.md",
    ),
    "TASK-000007": (
        "docs/research/profile-session-execution-and-data-safety-closure-preparation-2026-07.md",
    ),
    "TASK-000008": (
        "docs/research/backup-ownership-execution-and-two-person-control-closure-preparation-2026-07.md",
    ),
    "TASK-000009": (
        "docs/research/package-update-execution-and-release-safety-closure-preparation-2026-07.md",
    ),
    "TASK-000010": (
        "docs/research/incident-response-execution-and-disclosure-closure-preparation-2026-07.md",
    ),
}


def scope_path_is_allowed(path: str, allowed_paths: list[str]) -> bool:
    """Return whether an exact path is covered by an exact or directory entry."""
    normalized = path.rstrip("/")
    for allowed in allowed_paths:
        if allowed.endswith("/"):
            if normalized.startswith(allowed.rstrip("/") + "/"):
                return True
        elif normalized == allowed:
            return True
    return False


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
        required_scope_paths = REQUIRED_SCOPE_PATHS.get(task_id, ())
        allowed_paths = manifest.get("allowed_paths")
        missing_scope_paths = [
            path
            for path in required_scope_paths
            if not scope_path_is_allowed(path, allowed_paths)
        ]
        if missing_scope_paths:
            fail(
                f"{task_id}: allowed_paths omit required closure-route files: "
                + ", ".join(missing_scope_paths)
            )
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
