#!/usr/bin/env python3
"""Validate checked no-claim task approval templates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AGENT_MACHINE = DOCS / "agent-execution" / "machine"
BLUEPRINT_MACHINE = DOCS / "blueprint-v1" / "machine"
DEFAULT_TEMPLATE_DIR = AGENT_MACHINE / "task-approval-templates"

TEMPLATE_ID = re.compile(r"^AGENT\.TASK_APPROVAL_TEMPLATE\.[A-Z0-9._-]+$")
TASK_ID = re.compile(r"^TASK-[0-9]{6}$")

REQUIRED_REFERENCE_PATHS = {
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/templates/agent-task.md",
    "docs/agent-execution/machine/execution-task.schema.json",
    "docs/agent-execution/machine/agent-run-manifest.schema.json",
    "docs/agent-execution/machine/evidence-bundle.schema.json",
}

REQUIRED_CLAIM_PHRASES = [
    "no task is approved",
    "running",
    "accepted",
    "release-gated",
    "production-authorized",
    "readiness-promoted",
    "Chrome-class",
    "performance",
    "compatibility",
    "security",
    "accessibility",
    "production claim",
]

REQUIRED_INPUT_TERMS = [
    "queue task ID",
    "owner",
    "independent reviewer",
    "requirements",
    "risks",
    "ADRs",
    "allowed paths",
    "prohibited paths",
    "network allowlist",
    "credential",
    "resource budget",
    "evidence bundle",
    "rollback",
    "claim boundary",
]

REQUIRED_MANIFEST_TERMS = [
    "execution-task.schema.json",
    "reviewed or ready",
    "source queue digest",
    "approval timestamp",
    "owner",
    "independent reviewer",
    "allowed path",
    "network destination",
    "evidence bundle",
    "agent run manifest",
    "preconditions",
    "acceptance criteria",
    "negative tests",
    "rollback",
    "dependencies",
    "expiry",
]

REQUIRED_AUTHORITY_TERMS = [
    "deny all paths",
    "deny all network",
    "production signing keys",
    "offline roots",
    "real user profiles",
    "self-approval",
    "wall time",
    "CPU",
    "memory",
    "disk",
    "network",
    "command",
    "tool call",
    "source-tree cleanliness",
    "escalate authority outside the manifest",
]

REQUIRED_EVIDENCE_TERMS = [
    "agent run manifest",
    "evidence bundle",
    "source commit",
    "instruction digest",
    "toolchain digest",
    "raw command output",
    "exit codes",
    "validation output",
    "SHA-256",
    "negative-test",
    "rollback",
    "independent reviewer",
    "unsupported behavior",
    "residual risk",
]

REQUIRED_REJECTION_TERMS = [
    "proposed queue row",
    "named owner",
    "named independent reviewer",
    "same person",
    "allowed path",
    "network",
    "credential",
    "budget",
    "evidence bundle",
    "rollback",
    "expiry",
    "authority expansion",
    "raw artifacts",
    "hashes",
    "exit codes",
    "validation output",
    "source-tree status",
    "weakens sandbox",
    "source-strategy adoption",
    "production signing",
    "independent review",
    "stale manifests",
]

REQUIRED_UNSUPPORTED = [
    "No task approval claim.",
    "No running task claim.",
    "No accepted task claim.",
    "No readiness promotion claim.",
    "No source-strategy approval claim.",
    "No broad M1 implementation claim.",
    "No Chrome-class claim.",
    "No performance claim.",
    "No compatibility claim.",
    "No security claim.",
    "No accessibility claim.",
    "No beta claim.",
    "No stable claim.",
    "No release claim.",
    "No production claim.",
    "No daily-driver claim.",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_task_approval_templates.py",
    "python3 -B tools/validate_blueprint.py",
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


def as_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(path: Path, data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        fail(path, f"{key} must be a non-empty array")
    return value


def text_block(values: list[Any]) -> str:
    return " ".join(value for value in values if isinstance(value, str))


def require_terms(path: Path, label: str, text: str, terms: list[str]) -> None:
    missing = [term for term in terms if term not in text]
    if missing:
        fail(path, f"{label} is missing required terms: {', '.join(missing)}")


def expected_task_ids() -> list[str]:
    queue = load_json(BLUEPRINT_MACHINE / "build-readiness-task-queue.json")
    tasks = queue.get("tasks") if isinstance(queue, dict) else None
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json", "tasks must be an array")
    ids = [task.get("id") for task in tasks if isinstance(task, dict)]
    expected = [f"TASK-{index:06d}" for index in range(1, 11)]
    if ids != expected:
        fail("build-readiness-task-queue.json", f"expected TASK-000001 through TASK-000010, found {ids}")
    return expected


def validate_template(path: Path, task_ids: list[str]) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(path, "template must be an object")
    if data.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    template_id = as_text(data.get("template_id"))
    if not TEMPLATE_ID.fullmatch(template_id):
        fail(path, f"invalid template_id {template_id!r}")
    if data.get("status") != "template_no_approval":
        fail(path, "status must remain template_no_approval")

    for key, expected_path in [
        ("source_queue", "docs/blueprint-v1/machine/build-readiness-task-queue.json"),
        ("source_template", "docs/templates/agent-task.md"),
        ("task_schema", "docs/agent-execution/machine/execution-task.schema.json"),
        ("run_manifest_schema", "docs/agent-execution/machine/agent-run-manifest.schema.json"),
        ("evidence_bundle_schema", "docs/agent-execution/machine/evidence-bundle.schema.json"),
    ]:
        if data.get(key) != expected_path:
            fail(path, f"{key} must be {expected_path}")
        if not (ROOT / expected_path).exists():
            fail(path, f"{key} path does not exist: {expected_path}")

    claim_status = as_text(data.get("claim_status"))
    require_terms(path, "claim_status", claim_status, REQUIRED_CLAIM_PHRASES)

    applies_to_tasks = require_list(path, data, "applies_to_tasks")
    if applies_to_tasks != task_ids:
        fail(path, "applies_to_tasks must match TASK-000001 through TASK-000010")
    for task_id in applies_to_tasks:
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            fail(path, f"invalid task id in applies_to_tasks: {task_id!r}")

    require_terms(
        path,
        "required_approval_inputs",
        text_block(require_list(path, data, "required_approval_inputs")),
        REQUIRED_INPUT_TERMS,
    )
    require_terms(
        path,
        "immutable_manifest_requirements",
        text_block(require_list(path, data, "immutable_manifest_requirements")),
        REQUIRED_MANIFEST_TERMS,
    )
    require_terms(
        path,
        "authority_controls",
        text_block(require_list(path, data, "authority_controls")),
        REQUIRED_AUTHORITY_TERMS,
    )
    require_terms(
        path,
        "evidence_bundle_requirements",
        text_block(require_list(path, data, "evidence_bundle_requirements")),
        REQUIRED_EVIDENCE_TERMS,
    )
    require_terms(
        path,
        "rejection_rules",
        text_block(require_list(path, data, "rejection_rules")),
        REQUIRED_REJECTION_TERMS,
    )

    unsupported = require_list(path, data, "unsupported_boundaries")
    missing_unsupported = [phrase for phrase in REQUIRED_UNSUPPORTED if phrase not in unsupported]
    if missing_unsupported:
        fail(path, "unsupported_boundaries is missing: " + ", ".join(missing_unsupported))

    commands = require_list(path, data, "validation_commands")
    missing_commands = [command for command in REQUIRED_VALIDATION_COMMANDS if command not in commands]
    if missing_commands:
        fail(path, "validation_commands is missing: " + ", ".join(missing_commands))


def validate_docs() -> None:
    required_doc_phrases = {
        DOCS / "agent-execution" / "README.md": [
            "Task approval template",
            "task-approval-template.schema.json",
            "no-claim-task-approval-template.json",
        ],
        DOCS / "project-buildout" / "17-build-readiness-task-queue.md": [
            "Task approval template",
            "no-claim-task-approval-template.json",
            "validate_task_approval_templates.py",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "task approval template",
            "validate_task_approval_templates.py",
        ],
        DOCS / "repository-map.md": [
            "Task approval template",
            "validate_task_approval_templates.py",
        ],
        DOCS / "start-here.md": [
            "task approval template",
            "no-claim-task-approval-template.json",
        ],
    }
    for path, phrases in required_doc_phrases.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(path, "missing task approval template coverage: " + ", ".join(missing))


def template_paths(args: argparse.Namespace) -> list[Path]:
    if args.paths:
        return [Path(path) for path in args.paths]
    return sorted(DEFAULT_TEMPLATE_DIR.glob("*.json"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="task approval template JSON files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = template_paths(args)
    if not paths:
        fail(DEFAULT_TEMPLATE_DIR, "no task approval template files found")
    task_ids = expected_task_ids()
    for required_path in REQUIRED_REFERENCE_PATHS:
        if not (ROOT / required_path).exists():
            fail(required_path, "required reference path does not exist")
    for path in paths:
        validate_template(path, task_ids)
    validate_docs()
    print(f"task approval template validation passed: {len(paths)} template(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
