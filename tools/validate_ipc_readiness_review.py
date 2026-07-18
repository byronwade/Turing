#!/usr/bin/env python3
"""Validate checked no-claim IPC readiness-review templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
DEFAULT_REVIEW = (
    MACHINE / "ipc-readiness-reviews" / "no-claim-ipc-readiness-template.json"
)

REVIEW_ID = re.compile(r"^IPC\.READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_REVIEW_FILES = [
    "docs/blueprint-v1/machine/ipc-readiness-review.schema.json",
    "docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json",
    "tools/validate_ipc_readiness_review.py",
]

REQUIRED_SOURCE_RECORDS = {
    "crates/turing-ipc/src/lib.rs",
    "crates/turing-kernel/src/lib.rs",
    "crates/turing-types/src/lib.rs",
    "docs/research/ipc-capability-boundary-inventory-2026-07.md",
    "docs/research/pre-build-readiness-gap-audit-2026-07.md",
    "docs/api-design/02-async-streaming-and-cancellation.md",
    "docs/api-design/03-schemas-errors-versioning-and-compatibility.md",
    "docs/security-engine/10-capability-provenance-attenuation-and-revocation.md",
    "docs/blueprint-v1/04-system-architecture.md",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/blueprint-v1/machine/process-capabilities.json",
    "docs/blueprint-v1/machine/ipc-capability-boundary.schema.json",
    "docs/blueprint-v1/machine/ipc-capability-boundary.json",
    "docs/blueprint-v1/machine/ipc-schema-source.schema.json",
    "docs/blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json",
    "docs/blueprint-v1/machine/ipc-readiness-review.schema.json",
    "docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "tools/validate_ipc_capability_boundaries.py",
    "tools/validate_ipc_readiness_review.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no security review",
    "no architecture review",
    "no API review",
    "no performance review",
    "no implemented schema generator",
    "no approved generator source",
    "no wire encoding decision",
    "no generated types",
    "no generated validators",
    "no generated fixtures",
    "no connection authentication review",
    "no bounded queues review",
    "no backpressure review",
    "no timeout semantics review",
    "no cancellation semantics review",
    "no stale-epoch receiver proof",
    "no negative-test review",
    "no fuzz or model-test review",
    "no process-capability generation review",
    "no PB-011 readiness promotion",
    "no renderer-security claim",
    "no agent-security claim",
    "no process-isolation readiness claim",
    "no site-isolation claim",
    "no production IPC claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "security_reviewed",
    "architecture_reviewed",
    "api_reviewed",
    "performance_reviewed",
    "boundary_inventory_reviewed",
    "schema_source_template_reviewed",
    "schema_generator_implemented",
    "schema_generator_reviewed",
    "wire_encoding_reviewed",
    "generated_types_reviewed",
    "generated_validators_reviewed",
    "generated_fixtures_reviewed",
    "connection_authentication_reviewed",
    "bounded_queues_reviewed",
    "backpressure_reviewed",
    "timeout_semantics_reviewed",
    "cancellation_semantics_reviewed",
    "stale_epoch_reviewed",
    "negative_tests_reviewed",
    "fuzz_model_tests_reviewed",
    "process_capability_generation_reviewed",
    "pb011_ready",
    "renderer_security_supported",
    "agent_security_supported",
    "process_isolation_supported",
    "site_isolation_supported",
    "production_ipc_supported",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "boundary_inventory",
    "schema_source_template",
    "schema_generator",
    "wire_encoding_decision",
    "owner_reviewer",
    "security_reviewer",
    "architecture_reviewer",
    "api_reviewer",
    "performance_reviewer",
]

REQUIRED_AXIS_TERMS = [
    "schema generator",
    "approved generator source",
    "generated Rust types",
    "generated validators",
    "protocol documentation",
    "compatibility fixtures",
    "negative fixtures",
    "fuzz corpus seeds",
    "schema diff policy",
    "wire encoding decision",
    "bounded decode",
    "unknown variant policy",
    "connection authentication",
    "bounded queues",
    "backpressure",
    "timeout semantics",
    "cancellation semantics",
    "stale document epoch rejection",
    "browser_kernel",
    "renderer",
    "network",
    "storage",
    "gpu",
    "media_utility",
    "extension_host",
    "devtools",
    "agent_host",
    "updater",
    "crash_handler",
    "process capability generation",
    "malformed",
    "oversized",
    "stale",
    "duplicate",
    "reordered",
    "unauthorized",
    "wrong-principal",
    "timeout",
    "cancellation",
    "fuzz and model tests",
    "owner review",
    "security review",
    "architecture review",
    "API compatibility review",
    "performance review",
    "privacy review",
    "promotion boundary",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "schema generator",
    "wire encoding",
    "generated validators",
    "negative tests",
    "authority",
    "connection authentication",
    "unbounded queues",
    "timeout",
    "cancellation",
    "stale epoch",
    "process capability",
    "validation",
    "claim boundary",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_ipc_capability_boundaries.py",
    "python3 -B tools/validate_ipc_readiness_review.py",
    "python3 -B tools/validate_blueprint.py",
    ".\\tools\\check.ps1",
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


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(f"{key} must be an object")
    return value


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("schema source", "schema-source"),
        ("wire encoding", "wire-encoding"),
        ("generated type", "generated-type"),
        ("generated validator", "generated-validator"),
        ("generated fixture", "generated-fixture"),
        ("connection authentication", "connection-authentication"),
        ("bounded queue", "bounded-queue"),
        ("process capability", "process-capability"),
        ("stale epoch", "stale-epoch"),
        ("stale document epoch", "stale-document-epoch"),
        ("renderer security", "renderer-security"),
        ("agent security", "agent-security"),
        ("process isolation", "process-isolation"),
        ("site isolation", "site-isolation"),
        ("production ipc", "production-ipc"),
        ("claim boundary", "claim-boundary"),
        ("pb 011", "pb-011"),
        ("pb011", "pb-011"),
        ("api", "api"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def validate_review(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: review must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    review_id = text(data.get("review_id"))
    if not REVIEW_ID.fullmatch(review_id):
        fail(f"{path}: invalid review_id {review_id!r}")
    if data.get("status") != "no_claim_ipc_readiness_template":
        fail(f"{path}: status must be no_claim_ipc_readiness_template")

    boundary_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[text(value) for value in require_list(data, "unsupported_boundaries")],
            ]
        )
    )
    for phrase in REQUIRED_CLAIM_PHRASES:
        if normalize(phrase) not in boundary_text:
            fail(f"{path}: missing claim boundary phrase: {phrase}")

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in source_records:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    scope = require_object(data, "review_scope")
    if scope.get("review_status") != "template_only_no_review":
        fail(f"{path}: review_scope.review_status must be template_only_no_review")
    for field in NULL_SCOPE_FIELDS:
        if scope.get(field) is not None:
            fail(f"{path}: review_scope.{field} must be null in the no-claim template")
    policy = normalize(text(scope.get("prohibited_placeholder_policy")))
    for phrase in ["placeholder", "self-approval", "pb-011", "null"]:
        if phrase not in policy:
            fail(f"{path}: prohibited_placeholder_policy must mention {phrase}")

    readiness = require_object(data, "readiness_status")
    missing_flags = sorted(set(READINESS_STATUS_FLAGS) - set(readiness))
    if missing_flags:
        fail(f"{path}: readiness_status missing flags: {', '.join(missing_flags)}")
    for flag in READINESS_STATUS_FLAGS:
        if readiness.get(flag) is not False:
            fail(f"{path}: readiness_status.{flag} must be false in the no-claim template")

    axis_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for key in [
                "schema_generator_axes",
                "wire_transport_axes",
                "authority_identity_axes",
                "negative_test_axes",
                "owner_review_axes",
            ]
            for item in require_list(data, key)
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing IPC readiness axis term: {phrase}")
    if "beyond the checked no-claim ipc readiness-review template" not in axis_text:
        fail(f"{path}: axes must require evidence beyond the checked no-claim template")

    rejection_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for item in require_list(data, "rejection_rules")
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_REJECTION_TERMS:
        if normalize(phrase) not in rejection_text:
            fail(f"{path}: rejection rules must mention {phrase}")

    commands = [text(value) for value in require_list(data, "validation_commands")]
    for command in REQUIRED_VALIDATION_COMMANDS:
        if command not in commands:
            fail(f"{path}: validation_commands missing {command}")


def validate_readiness_registry() -> None:
    payload = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        fail("pre-build-readiness.json must contain items")
    item = next(
        (
            entry
            for entry in payload["items"]
            if isinstance(entry, dict) and entry.get("id") == "PB-011"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-011")
    if item.get("status") != "partial":
        fail("PB-011 must remain partial while the IPC review is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-011 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-011 evidence is missing IPC readiness review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim IPC readiness-review template",
        "owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template",
        "accepted TASK-000011 schema generator and M0 reference evidence bundle beyond the checked no-claim schema-source template",
        "wire encoding decision",
        "connection authentication",
        "bounded queues",
        "backpressure",
        "stale-epoch receiver rejection",
        "timeout",
        "cancellation",
        "PB-011 readiness promotion",
        "renderer-security",
        "production IPC",
    ]:
        if normalize(phrase) not in required_text:
            fail(f"PB-011 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000003"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000003 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000003 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000003 allowed_paths missing IPC review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim IPC readiness-review template",
        "owner-reviewed IPC readiness review",
        "cannot be cited",
        "PB-011 readiness",
        "renderer-security",
        "agent-security",
        "process-isolation",
        "site-isolation",
        "production IPC",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000003 must mention IPC review boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-kernel-process-authority-ipc"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing IPC lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("IPC lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("IPC lane evidence_start missing IPC review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template",
        "no PB-011 readiness promotion",
        "no production IPC claim from the checked no-claim IPC readiness-review template",
        "no renderer-security claim",
        "no process-isolation readiness claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"IPC lane must mention {phrase}")


def validate_docs() -> None:
    docs_to_check = {
        ROOT / "README.md": ["IPC readiness-review template", "owner-reviewed IPC readiness"],
        DOCS / "start-here.md": ["IPC readiness-review template", "no owner-reviewed IPC readiness"],
        DOCS / "README.md": ["IPC readiness-review template", "owner-reviewed IPC readiness"],
        DOCS / "repository-map.md": ["IPC readiness-review template", "ipc-readiness-review.schema.json"],
        DOCS / "research" / "README.md": ["IPC readiness-review template", "owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template"],
        DOCS / "research" / "ipc-capability-boundary-inventory-2026-07.md": ["IPC readiness-review template", "owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template"],
        DOCS / "api-design" / "03-schemas-errors-versioning-and-compatibility.md": ["IPC readiness-review template", "no owner-reviewed IPC readiness"],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": ["IPC readiness-review template", "owner-reviewed IPC readiness"],
        DOCS / "project-buildout" / "17-build-readiness-task-queue.md": ["IPC readiness-review template", "owner-reviewed IPC readiness"],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": ["IPC readiness-review template", "owner-reviewed IPC readiness"],
    }
    for doc_path, phrases in docs_to_check.items():
        content = doc_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in content]
        if missing:
            fail(f"{doc_path}: missing IPC readiness-review documentation: {', '.join(missing)}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    validate_docs()
    print(f"IPC readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
