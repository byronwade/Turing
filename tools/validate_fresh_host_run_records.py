#!/usr/bin/env python3
"""Validate checked no-claim fresh-host run-record templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DEFAULT_RECORDS = [
    DOCS / "project-buildout" / "machine" / "fresh-host-runs" / "no-claim-run-record-template.json"
]

RECORD_ID = re.compile(r"^BUILD\.FRESH_HOST\.RUN_RECORD\.[A-Z0-9._-]+$")
COMMAND_ID = re.compile(r"^FRESH-HOST-CMD-[A-Z0-9_]+$")
EXPECTED_COMMANDS = {
    "FRESH-HOST-CMD-BOOTSTRAP": "bootstrap",
    "FRESH-HOST-CMD-DOCTOR": "doctor",
    "FRESH-HOST-CMD-CHECK": "check",
    "FRESH-HOST-CMD-XTASK_BOOTSTRAP": "xtask-bootstrap",
    "FRESH-HOST-CMD-XTASK_DOCTOR": "xtask-doctor",
    "FRESH-HOST-CMD-XTASK_CHECK": "xtask-check",
}
CLAIM_PHRASES = [
    "no independent fresh-host reproduction",
    "no owner-approved clean-VM equivalent",
    "no command execution evidence",
    "no retained bootstrap/doctor/check/xtask logs",
    "no PB-009 readiness promotion",
    "no broad implementation readiness",
    "no preview readiness",
    "no beta readiness",
    "no stable readiness",
    "no production readiness",
    "no Chrome-class claim",
]
HOST_TERMS = [
    "independent fresh reference host",
    "owner-approved clean VM equivalent",
    "operating system",
    "shell",
    "locale",
    "timezone",
    "cpu",
    "memory",
    "disk",
    "network posture",
    "privilege",
    "waiver",
    "cleanup evidence",
]
SOURCE_TERMS = [
    "remote URL",
    "branch",
    "commit hash",
    "Git version",
    "line-ending",
    "source-tree status",
    "generated build output",
    "untracked installers",
    "credentials",
    "local profiles",
]
COMMAND_FIELD_TERMS = [
    "command line",
    "shell",
    "exit code",
    "stdout/stderr retention path",
    "SHA-256",
]
CACHE_TERMS = [
    "CARGO_TARGET_DIR",
    "Cargo cache root",
    "Rustup toolchain cache",
    "temp directory",
    "durable source",
    "cleanup evidence",
]
PROHIBITED_TERMS = [
    "same-host reruns",
    "current-host diagnostics",
    "PB-009",
    "exit codes",
    "source-tree status",
    "retained logs",
    "target directory",
    "failure classification",
    "credentials",
]


class ValidationError(Exception):
    pass


def fail(path: Path, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def require_string(path: Path, data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{key} must be a non-empty string")
    return value


def require_string_array(path: Path, data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
    ):
        fail(path, f"{key} must be a non-empty array of strings")
    return value


def require_object(path: Path, data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(path, f"{key} must be an object")
    return value


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("clean vm", "clean-vm"),
        ("fresh host", "fresh-host"),
        ("source tree", "source-tree"),
        ("source-controlled", "source-controlled"),
        ("current host", "current-host"),
        ("same host", "same-host"),
        ("line ending", "line-ending"),
        ("target dir", "target-directory"),
        ("target directory", "target-directory"),
        ("cargo target dir", "cargo-target-dir"),
        ("cargo_target_dir", "cargo-target-dir"),
        ("sha-256", "sha-256"),
        ("stdout/stderr", "stdout-stderr"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def require_terms(path: Path, label: str, values: list[str], terms: list[str]) -> None:
    haystack = normalize(" ".join(values))
    for term in terms:
        if normalize(term) not in haystack:
            fail(path, f"{label} must mention {term}")


def validate_requirement_group(path: Path, group: dict[str, Any], label: str, terms: list[str]) -> None:
    fields = require_string_array(path, group, "required_fields")
    artifacts = require_string_array(path, group, "evidence_artifacts")
    require_terms(path, label, [*fields, *artifacts], terms)


def validate_commands(path: Path, commands: Any) -> None:
    if not isinstance(commands, list) or not commands:
        fail(path, "commands must be a non-empty array")
    ids: list[str] = []
    for command in commands:
        if not isinstance(command, dict):
            fail(path, "commands entries must be objects")
        command_id = require_string(path, command, "command_id")
        if not COMMAND_ID.fullmatch(command_id):
            fail(path, f"invalid command_id {command_id!r}")
        ids.append(command_id)
        expected_family = EXPECTED_COMMANDS.get(command_id)
        if expected_family is None:
            fail(path, f"unexpected command_id {command_id!r}")
        if command.get("command_family") != expected_family:
            fail(path, f"{command_id} command_family must be {expected_family}")
        required_commands = require_string_array(path, command, "required_commands")
        required_fields = require_string_array(path, command, "required_fields")
        success = require_string_array(path, command, "success_evidence")
        failure = require_string_array(path, command, "failure_evidence")
        require_terms(path, command_id, [*required_commands, *required_fields], COMMAND_FIELD_TERMS)
        require_terms(path, f"{command_id} failure_evidence", failure, ["exit code", "retained log", "classification", "cleanup"])
        if not success:
            fail(path, f"{command_id} success_evidence must not be empty")
    duplicates = sorted({command_id for command_id in ids if ids.count(command_id) > 1})
    if duplicates:
        fail(path, "duplicate command ids: " + ", ".join(duplicates))
    if set(ids) != set(EXPECTED_COMMANDS):
        fail(path, "commands must cover: " + ", ".join(sorted(EXPECTED_COMMANDS)))


def validate_record(path: Path, record: Any) -> None:
    if not isinstance(record, dict):
        fail(path, "run record must be an object")
    if record.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    record_id = require_string(path, record, "record_id")
    if not RECORD_ID.fullmatch(record_id):
        fail(path, f"invalid record_id {record_id!r}")
    if record.get("related_gate") != "PB-009":
        fail(path, "related_gate must be PB-009")
    if record.get("related_task") != "TASK-000002":
        fail(path, "related_task must be TASK-000002")
    if record.get("source_inventory") != "docs/project-buildout/machine/fresh-host-reproduction.json":
        fail(path, "source_inventory must point at fresh-host-reproduction.json")
    if record.get("status") == "template_no_execution":
        if record.get("run_class") != "template_only":
            fail(path, "template_no_execution records must use run_class template_only")
        if record.get("execution_status") != "not_executed":
            fail(path, "template_no_execution records must use execution_status not_executed")
    boundary_text = [
        require_string(path, record, "claim_status"),
        *require_string_array(path, record, "unsupported_boundaries"),
    ]
    require_terms(path, "claim_status and unsupported_boundaries", boundary_text, CLAIM_PHRASES)
    validate_requirement_group(path, require_object(path, record, "host_identity"), "host_identity", HOST_TERMS)
    validate_requirement_group(path, require_object(path, record, "source_checkout"), "source_checkout", SOURCE_TERMS)
    validate_commands(path, record.get("commands"))
    require_terms(
        path,
        "cache_and_artifact_controls",
        require_string_array(path, record, "cache_and_artifact_controls"),
        CACHE_TERMS,
    )
    require_terms(
        path,
        "source_tree_cleanliness",
        require_string_array(path, record, "source_tree_cleanliness"),
        ["source-tree status", "changed", "untracked", "ignored", "generated", "reject"],
    )
    require_terms(
        path,
        "failure_denominator",
        require_string_array(path, record, "failure_denominator"),
        ["all attempted commands", "environmental", "source-controlled", "network-dependent", "nondeterministic", "timeout", "cancellation", "disk-full", "owner accepts"],
    )
    require_terms(
        path,
        "prohibited_evidence",
        require_string_array(path, record, "prohibited_evidence"),
        PROHIBITED_TERMS,
    )


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else DEFAULT_RECORDS
    try:
        for path in paths:
            validate_record(path, load_json(path))
    except ValidationError as error:
        print(f"fresh-host run-record validation failed: {error}", file=sys.stderr)
        return 1
    print(f"fresh-host run-record validation passed: {len(paths)} record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
