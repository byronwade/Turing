#!/usr/bin/env python3
"""Validate no-claim fresh-host reproduction inventories."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
DEFAULT_INVENTORY = DOCS / "project-buildout" / "machine" / "fresh-host-reproduction.json"

INVENTORY_ID = re.compile(r"^BUILD\.FRESH_HOST\.[A-Z0-9._-]+$")
AXIS_ID = re.compile(r"^FRESH-HOST-AXIS-[A-Z0-9_]+$")

REQUIRED_EVIDENCE_FILES = [
    "docs/research/fresh-host-reproduction-inventory-2026-07.md",
    "docs/project-buildout/machine/fresh-host-reproduction.schema.json",
    "docs/project-buildout/machine/fresh-host-reproduction.json",
    "docs/project-buildout/machine/fresh-host-run-record.schema.json",
    "docs/project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json",
    "docs/project-buildout/machine/fresh-host-readiness-review.schema.json",
    "docs/project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json",
    "tools/validate_fresh_host_reproduction.py",
    "tools/validate_fresh_host_run_records.py",
    "tools/validate_fresh_host_readiness_review.py",
]

REQUIRED_SOURCE_RECORDS = {
    "docs/research/m0-build-foundation-2026-07.md",
    "docs/project-buildout/05-repository-build-toolchain-and-coding-standards.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    ".github/workflows/repository-validation.yml",
    "tools/bootstrap.sh",
    "tools/bootstrap.ps1",
    "tools/doctor.sh",
    "tools/doctor.ps1",
    "tools/check.sh",
    "tools/check.ps1",
    "tools/xtask/src/main.rs",
    "docs/project-buildout/machine/fresh-host-run-record.schema.json",
    "docs/project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json",
    "docs/project-buildout/machine/fresh-host-readiness-review.schema.json",
    "docs/project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json",
    "tools/validate_fresh_host_run_records.py",
    "tools/validate_fresh_host_readiness_review.py",
}

REQUIRED_AXES = {
    "FRESH-HOST-AXIS-HOST_IDENTITY",
    "FRESH-HOST-AXIS-SOURCE_IDENTITY",
    "FRESH-HOST-AXIS-COMMAND_OUTPUT",
    "FRESH-HOST-AXIS-CACHE_TARGET",
    "FRESH-HOST-AXIS-FAILURE_ROLLBACK",
    "FRESH-HOST-AXIS-REPRODUCIBILITY_LEVELS",
}

REQUIRED_CLAIM_PHRASES = [
    "no independent fresh-host reproduction",
    "no owner-approved clean-VM equivalent",
    "no PB-009 readiness promotion",
    "no broad implementation readiness",
    "no preview readiness",
    "no beta readiness",
    "no stable readiness",
    "no production readiness",
    "no Chrome-class claim",
]

SCOPE_TERMS = [
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
    "no repository build outputs",
    "cargo target directory",
    "rustup toolchain cache",
    "package cache",
    "clean repository checkout",
    "git commit",
    "remote url",
    "dirty-state",
    "source-tree cleanliness",
    "line-ending",
    "tools/bootstrap",
    "tools/doctor",
    "tools/check",
    "xtask",
    "exit code",
    "rust version",
    "cargo version",
    "git version",
    "cargo_target_dir",
    "cache root",
    "temp directory",
    "hashes",
    "failure logs",
    "rollback notes",
]

REJECTION_TERMS = [
    "same-host reruns",
    "prior Turing target directories",
    "generated output",
    "downloaded installers",
    "command failures",
    "exit codes",
    "source-tree status",
    "build artifacts inside durable source",
    "PB-009 is ready",
]

PB009_REQUIRED_TERMS = [
    "independent fresh-host reproduction beyond the checked no-claim inventory",
    "owner-approved clean-VM equivalent",
    "bootstrap",
    "doctor",
    "check",
    "xtask",
    "exact OS",
    "shell",
    "Rust",
    "Cargo",
    "Git",
    "cache",
    "target directory",
    "source-tree cleanliness",
    "same-host reruns",
    "owner review",
]

TASK_REQUIRED_TERMS = [
    "fresh-host reproduction inventory",
    "owner-approved clean VM",
    "exact OS",
    "shell",
    "Rust",
    "Cargo",
    "Git",
    "cache",
    "target directory",
    "source-tree cleanliness",
    "bootstrap",
    "doctor",
    "check",
    "xtask",
    "same-host reruns",
    "PB-009",
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
        ("clean vm", "clean-vm"),
        ("fresh host", "fresh-host"),
        ("source tree", "source-tree"),
        ("target directory", "target-directory"),
        ("cargo target dir", "cargo-target-dir"),
        ("cargo-target-dir", "cargo-target-dir"),
        ("pb 009", "pb-009"),
        ("pb009", "pb-009"),
        ("owner approved", "owner-approved"),
        ("same host", "same-host"),
        ("line ending", "line-ending"),
        ("remote url", "remote-url"),
        ("rustup toolchain", "rustup-toolchain"),
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
    if data.get("status") != "no_claim_fresh_host_reproduction_inventory":
        fail(f"{path}: status must be no_claim_fresh_host_reproduction_inventory")

    boundary_text = " ".join(
        [text(data.get("claim_status")), *[text(value) for value in require_list(data, "unsupported_boundaries")]]
    ).lower()
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase.lower() not in boundary_text:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    sources = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - sources)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in REQUIRED_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    baseline_text = normalize(" ".join(text(value) for value in require_list(data, "current_local_baseline")))
    for phrase in ["bootstrap", "doctor", "check", "xtask", "cargo-target-dir", "outside the repository", "same-host"]:
        if normalize(phrase) not in baseline_text:
            fail(f"{path}: current_local_baseline must mention {phrase}")

    scope = data.get("required_reproduction_scope")
    if not isinstance(scope, dict):
        fail(f"{path}: required_reproduction_scope must be an object")
    scope_text = normalize(
        " ".join(text(value) for values in scope.values() if isinstance(values, list) for value in values)
    )
    for phrase in SCOPE_TERMS:
        if normalize(phrase) not in scope_text:
            fail(f"{path}: required_reproduction_scope must include {phrase}")

    axis_ids: list[str] = []
    for item in require_list(data, "evidence_axes"):
        if not isinstance(item, dict):
            fail(f"{path}: evidence_axes entries must be objects")
        axis_id = text(item.get("axis_id"))
        if not AXIS_ID.fullmatch(axis_id):
            fail(f"{path}: invalid axis_id {axis_id!r}")
        axis_ids.append(axis_id)
        axis_text = " ".join(text(item.get(key)) for key in ("name", "required_output", "missing_status"))
        if len(axis_text) < 80:
            fail(f"{path}: {axis_id} must be descriptive")
    check_no_duplicates(axis_ids, "axis ids")
    if set(axis_ids) != REQUIRED_AXES:
        fail(f"{path}: evidence axes must be exactly: {', '.join(sorted(REQUIRED_AXES))}")

    rejection_text = normalize(" ".join(text(value) for value in require_list(data, "rejection_rules")))
    for phrase in REJECTION_TERMS:
        if normalize(phrase) not in rejection_text:
            fail(f"{path}: rejection_rules must mention {phrase}")


def validate_pb009() -> None:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    pb009 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-009"), None)
    if not isinstance(pb009, dict):
        fail("pre-build-readiness.json is missing PB-009")
    if pb009.get("status") != "partial":
        fail("PB-009 must remain partial while only no-claim fresh-host inventory exists")
    evidence = pb009.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-009 must list no-claim fresh-host evidence")
    missing = [path for path in REQUIRED_EVIDENCE_FILES if path not in evidence]
    if missing:
        fail("PB-009 evidence is missing fresh-host records: " + ", ".join(missing))
    required_text = normalize(" ".join(value for value in pb009.get("evidence_required", []) if isinstance(value, str)))
    for phrase in PB009_REQUIRED_TERMS:
        if normalize(phrase) not in required_text:
            fail(f"PB-009 evidence_required must include {phrase}")


def validate_task000002() -> None:
    queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = queue.get("tasks") if isinstance(queue, dict) else None
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next((item for item in tasks if isinstance(item, dict) and item.get("id") == "TASK-000002"), None)
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000002")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000002 must list allowed_paths")
    missing = [path for path in REQUIRED_EVIDENCE_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000002 allowed_paths is missing fresh-host records: " + ", ".join(missing))
    combined = normalize(
        " ".join(
            value
            for key in ("preconditions", "acceptance_criteria", "negative_tests")
            for value in task.get(key, [])
            if isinstance(value, str)
        )
    )
    for phrase in TASK_REQUIRED_TERMS:
        if normalize(phrase) not in combined:
            fail(f"TASK-000002 scope must include {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg) for arg in argv] if argv else [DEFAULT_INVENTORY]
    for path in paths:
        validate_inventory(path if path.is_absolute() else ROOT / path)
    validate_pb009()
    validate_task000002()
    print(f"fresh-host reproduction validation passed: {len(paths)} inventory file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
