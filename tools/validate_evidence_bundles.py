#!/usr/bin/env python3
"""Validate checked agent evidence-bundle records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AGENT_MACHINE = DOCS / "agent-execution" / "machine"
DEFAULT_BUNDLE_DIR = AGENT_MACHINE / "evidence-bundles"

BUNDLE_ID = re.compile(r"^EVID-[0-9]{8}-[A-Z0-9-]+$")
TASK_ID = re.compile(r"^TASK-[0-9]{6}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_DECISIONS = {
    "accepted",
    "rejected",
    "needs_changes",
    "needs_independent_review",
    "rolled_back",
}

REQUIRED_NO_CLAIM_LIMITATIONS = [
    "No TASK-000011 acceptance.",
    "No independent reviewer decision.",
    "No accepted evidence-bundle instance.",
    "No PB-011 readiness promotion.",
    "No owner-reviewed IPC readiness.",
    "No production IPC claim.",
    "No Chrome-class claim.",
]


def fail(path: Path | str, message: str) -> None:
    raise SystemExit(f"{path}: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(path, "missing JSON file")
    except json.JSONDecodeError as exc:
        fail(path, f"invalid JSON: {exc}")


def require_string(path: Path, data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{key} must be a non-empty string")
    return value


def require_bool(path: Path, data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        fail(path, f"{key} must be a boolean")
    return value


def require_array(path: Path, data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        fail(path, f"{key} must be an array")
    return value


def git_blob(commit: str, artifact_path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{artifact_path}"],
            cwd=ROOT,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"{artifact_path}: cannot read from {commit}: {message}")


def validate_source_artifact(path: Path, commit: str, artifact: dict[str, Any]) -> None:
    artifact_path = require_string(path, artifact, "path")
    if Path(artifact_path).is_absolute() or ".." in Path(artifact_path).parts:
        fail(path, f"source_file artifact path must be repository-relative: {artifact_path}")
    expected_hash = require_string(path, artifact, "sha256")
    data = git_blob(commit, artifact_path)
    actual_hash = hashlib.sha256(data).hexdigest()
    if actual_hash != expected_hash:
        fail(path, f"{artifact_path} sha256 mismatch for source_commit")


def validate_artifact(path: Path, commit: str, artifact: Any) -> None:
    if not isinstance(artifact, dict):
        fail(path, "artifact entries must be objects")
    artifact_type = require_string(path, artifact, "type")
    artifact_path = require_string(path, artifact, "path")
    artifact_hash = require_string(path, artifact, "sha256")
    result = require_string(path, artifact, "result")
    if not SHA256.fullmatch(artifact_hash):
        fail(path, f"artifact has invalid sha256: {artifact_hash!r}")
    if result == "accepted":
        fail(path, "artifact result must not use accepted as a shortcut for review")
    if artifact_type == "source_file":
        validate_source_artifact(path, commit, artifact)
    elif artifact_type == "github_actions_run":
        if not artifact_path.startswith("https://github.com/byronwade/Turing/actions/runs/"):
            fail(path, "github_actions_run artifact must use the repository Actions run URL")
    else:
        fail(path, f"unsupported artifact type {artifact_type!r}")


def validate_bundle(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(path, "bundle must be an object")
    if data.get("schema_version") != 1:
        fail(path, "schema_version must be 1")

    bundle_id = require_string(path, data, "bundle_id")
    if not BUNDLE_ID.fullmatch(bundle_id):
        fail(path, f"invalid bundle_id {bundle_id!r}")

    task_id = require_string(path, data, "task_id")
    if not TASK_ID.fullmatch(task_id):
        fail(path, f"invalid task_id {task_id!r}")
    task_path = AGENT_MACHINE / "tasks" / f"{task_id}.json"
    task = load_json(task_path)
    if not isinstance(task, dict):
        fail(task_path, "task manifest must be an object")

    source_commit = require_string(path, data, "source_commit")
    if not COMMIT.fullmatch(source_commit):
        fail(path, "source_commit must be a 40-character lowercase git commit")

    environment = data.get("environment")
    if not isinstance(environment, dict) or not environment:
        fail(path, "environment must be a non-empty object")
    for key in ["captured_at", "host_os", "shell", "python", "rustc", "cargo", "git"]:
        require_string(path, environment, key)

    artifacts = require_array(path, data, "artifacts")
    if not artifacts:
        fail(path, "artifacts must not be empty")
    for artifact in artifacts:
        validate_artifact(path, source_commit, artifact)

    failures = require_array(path, data, "failures")
    for failure in failures:
        if not isinstance(failure, dict):
            fail(path, "failure entries must be objects")

    limitations = require_array(path, data, "limitations")
    if not all(isinstance(value, str) and value for value in limitations):
        fail(path, "limitations must contain non-empty strings")

    review = data.get("review")
    if not isinstance(review, dict):
        fail(path, "review must be an object")
    reviewer = require_string(path, review, "reviewer")
    independent = require_bool(path, review, "independent")
    decision = require_string(path, review, "decision")
    if decision not in ALLOWED_DECISIONS:
        fail(path, f"unsupported review decision {decision!r}")

    task_owner = task.get("owner")
    task_status = task.get("status")
    if independent and reviewer == task_owner:
        fail(path, "independent reviewer must not be the task owner")
    if decision == "accepted" and not independent:
        fail(path, "accepted evidence bundles require independent review")
    if decision == "accepted" and task_status != "accepted":
        fail(path, "accepted evidence bundle cannot point at a non-accepted task")
    if decision == "needs_independent_review":
        if task_status != "review_pending":
            fail(path, "needs_independent_review bundles require a review_pending task")
        missing = [
            phrase for phrase in REQUIRED_NO_CLAIM_LIMITATIONS if phrase not in limitations
        ]
        if missing:
            fail(path, "no-claim limitations are missing: " + ", ".join(missing))


def validate_docs() -> None:
    required_doc_phrases = {
        DOCS / "agent-execution" / "README.md": [
            "Evidence bundle records",
            "TASK-000011.no-claim.2026-07-18.json",
            "validate_evidence_bundles.py",
        ],
        DOCS / "research" / "task-000011-wp002-review-handoff-2026-07.md": [
            "TASK-000011.no-claim.2026-07-18.json",
            "non-accepting evidence capture",
            "validate_evidence_bundles.py",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "TASK-000011.no-claim.2026-07-18.json",
            "validate_evidence_bundles.py",
        ],
        DOCS / "repository-map.md": [
            "evidence-bundles",
            "validate_evidence_bundles.py",
        ],
    }
    for doc_path, phrases in required_doc_phrases.items():
        text = doc_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(doc_path, "missing evidence-bundle coverage: " + ", ".join(missing))


def bundle_paths(args: argparse.Namespace) -> list[Path]:
    if args.paths:
        return [Path(path) for path in args.paths]
    return sorted(DEFAULT_BUNDLE_DIR.glob("*.json"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="evidence-bundle JSON files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = bundle_paths(args)
    if not paths:
        fail(DEFAULT_BUNDLE_DIR, "no evidence-bundle records found")
    for path in paths:
        validate_bundle(path)
    validate_docs()
    print(f"evidence bundle validation passed: {len(paths)} bundle(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
