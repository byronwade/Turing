#!/usr/bin/env python3
"""Validate no-claim IPC capability boundary inventories."""

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
DEFAULT_INVENTORY = MACHINE / "ipc-capability-boundary.json"
DEFAULT_SCHEMA_SOURCE = (
    MACHINE / "ipc-schema-sources" / "no-claim-control-envelope-template.json"
)

INVENTORY_ID = re.compile(r"^IPC\.CAPABILITY\.[A-Z0-9._-]+$")
SCHEMA_SOURCE_ID = re.compile(r"^IPC\.SCHEMA_SOURCE\.[A-Z0-9._-]+$")
M0_ID = re.compile(r"^IPC-M0-[A-Z0-9_]+$")
BLOCKER_ID = re.compile(r"^IPC-BLOCKER-[A-Z0-9_]+$")
NEGATIVE_ID = re.compile(r"^IPC-NEG-[A-Z0-9_]+$")
ROLE_ID = re.compile(r"^IPC-ROLE-[A-Z0-9_]+$")

REQUIRED_SOURCE_RECORDS = {
    "crates/turing-ipc/src/lib.rs",
    "crates/turing-kernel/src/lib.rs",
    "crates/turing-types/src/lib.rs",
    "docs/blueprint-v1/04-system-architecture.md",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/blueprint-v1/machine/process-capabilities.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/machine/ipc-readiness-review.schema.json",
    "docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json",
    "docs/api-design/02-async-streaming-and-cancellation.md",
    "docs/api-design/03-schemas-errors-versioning-and-compatibility.md",
    "docs/security-engine/10-capability-provenance-attenuation-and-revocation.md",
    "tools/validate_ipc_readiness_review.py",
}

REQUIRED_SCHEMA_SOURCE_RECORDS = {
    "crates/turing-ipc/src/lib.rs",
    "crates/turing-kernel/src/lib.rs",
    "crates/turing-types/src/lib.rs",
    "docs/blueprint-v1/04-system-architecture.md",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/blueprint-v1/machine/process-capabilities.json",
    "docs/blueprint-v1/machine/ipc-capability-boundary.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/machine/ipc-readiness-review.schema.json",
    "docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json",
    "docs/api-design/02-async-streaming-and-cancellation.md",
    "docs/api-design/03-schemas-errors-versioning-and-compatibility.md",
    "docs/security-engine/10-capability-provenance-attenuation-and-revocation.md",
    "tools/validate_ipc_readiness_review.py",
}

REQUIRED_M0_EVIDENCE = {
    "bounded envelope",
    "oversize test",
    "role capabilities",
    "typed identities",
    "process capability record",
}

REQUIRED_BLOCKERS = {
    "schema generator",
    "wire encoding decision",
    "connection authentication",
    "bounded queues and backpressure",
    "timeout semantics",
    "cancellation semantics",
    "stale document epoch rejection",
    "fuzz and model tests",
}

REQUIRED_NEGATIVE_CASES = {
    "malformed",
    "oversized",
    "stale",
    "duplicate",
    "reordered",
    "unauthorized",
    "wrong-principal",
    "timeout",
    "cancellation",
}

REQUIRED_CLAIM_PHRASES = [
    "no renderer-security claim",
    "no agent-security claim",
    "no process-isolation readiness claim",
    "no site-isolation claim",
    "no production IPC claim",
    "no wire encoding decision claim",
    "no schema generator claim",
    "no timeout or cancellation implementation claim",
    "no implementation readiness claim",
]

REQUIRED_SCHEMA_SOURCE_CLAIM_PHRASES = [
    "no schema generator claim",
    "no approved generator source claim",
    "no wire encoding decision claim",
    "no generated type claim",
    "no generated validator claim",
    "no generated fixture claim",
    "no renderer-security claim",
    "no agent-security claim",
    "no process-isolation readiness claim",
    "no site-isolation claim",
    "no timeout or cancellation implementation claim",
    "no production IPC claim",
    "no implementation readiness claim",
]

REQUIRED_MESSAGE_METADATA = {
    "schema family",
    "major version",
    "minor version",
    "sender role",
    "receiver role",
    "required capability",
    "maximum encoded size",
    "timeout semantics",
    "cancellation semantics",
    "document epoch policy",
    "profile or storage partition scope",
    "origin or top-level site scope",
    "resource owner",
    "sensitivity and redaction class",
    "audit event class",
    "unknown variant policy",
    "bounded allocation policy",
    "error code mapping",
    "compatibility fixture path",
}

REQUIRED_GENERATOR_OUTPUTS = {
    "Rust request, response, event, error, and handle types",
    "decode-time size and range validators",
    "sender role and receiver role validators",
    "capability and principal validators",
    "protocol documentation",
    "redaction and sensitivity metadata",
    "trace and audit metadata",
    "compatibility fixtures",
    "negative fixtures",
    "fuzz corpus seeds",
    "schema-diff classification output",
}

REQUIRED_SCHEMA_COMMANDS = {
    "python3 -B tools/validate_ipc_capability_boundaries.py",
    "python3 -B tools/validate_blueprint.py",
}

SAFE_FAILURE_TERMS = {
    "abort",
    "block",
    "fail",
    "hold",
    "reject",
    "return",
    "stop",
}


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
    if not isinstance(value, list):
        fail(f"{key} must be an array")
    return value


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def normalize(value: str) -> str:
    return value.lower().replace("_", " ").replace("-", "-").strip()


def require_safe_failure(path: Path, item_id: str, value: str) -> None:
    lowered = value.lower()
    if not any(term in lowered for term in SAFE_FAILURE_TERMS):
        fail(f"{path}: {item_id} safe_failure must describe blocking, rejection, return, or abort behavior")


def validate_inventory(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    inventory_id = text(data.get("inventory_id"))
    if not INVENTORY_ID.match(inventory_id):
        fail(f"{path}: invalid inventory_id {inventory_id!r}")
    if data.get("status") != "no_claim_boundary_inventory":
        fail(f"{path}: status must be no_claim_boundary_inventory")

    boundaries = [text(value).lower() for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")).lower(), *boundaries])
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

    m0_items = require_list(data, "m0_evidence")
    m0_ids: list[str] = []
    m0_text = ""
    for item in m0_items:
        if not isinstance(item, dict):
            fail(f"{path}: m0_evidence entries must be objects")
        item_id = text(item.get("id"))
        if not M0_ID.match(item_id):
            fail(f"{path}: invalid M0 evidence id {item_id!r}")
        m0_ids.append(item_id)
        for field in ("artifact", "evidence", "limit"):
            value = text(item.get(field))
            if len(value) < 3:
                fail(f"{path}: {item_id} {field} must be descriptive")
            m0_text += " " + value.lower()
    check_no_duplicates(m0_ids, "M0 evidence IDs")
    for phrase in REQUIRED_M0_EVIDENCE:
        if phrase not in m0_text:
            fail(f"{path}: M0 evidence must mention {phrase}")

    blockers = require_list(data, "schema_and_transport_blockers")
    blocker_ids: list[str] = []
    blocker_names: list[str] = []
    for item in blockers:
        if not isinstance(item, dict):
            fail(f"{path}: schema_and_transport_blockers entries must be objects")
        item_id = text(item.get("id"))
        if not BLOCKER_ID.match(item_id):
            fail(f"{path}: invalid blocker id {item_id!r}")
        blocker_ids.append(item_id)
        blocker_names.append(text(item.get("blocker")).lower())
        if item.get("status") not in {"missing", "partially_covered", "proposed"}:
            fail(f"{path}: {item_id} has invalid blocker status")
        for field in ("required_evidence", "safe_failure"):
            value = text(item.get(field))
            if len(value) < 30:
                fail(f"{path}: {item_id} {field} must be descriptive")
        require_safe_failure(path, item_id, text(item.get("safe_failure")))
    check_no_duplicates(blocker_ids, "blocker IDs")
    missing_blockers = sorted(REQUIRED_BLOCKERS - set(blocker_names))
    if missing_blockers:
        fail(f"{path}: missing blockers: {', '.join(missing_blockers)}")

    negative_items = require_list(data, "negative_coverage_requirements")
    negative_ids: list[str] = []
    negative_cases: list[str] = []
    for item in negative_items:
        if not isinstance(item, dict):
            fail(f"{path}: negative_coverage_requirements entries must be objects")
        item_id = text(item.get("id"))
        if not NEGATIVE_ID.match(item_id):
            fail(f"{path}: invalid negative coverage id {item_id!r}")
        negative_ids.append(item_id)
        case = text(item.get("case")).lower()
        negative_cases.append(case)
        if item.get("current_status") not in {"implemented_m0_test", "missing", "not_executable_without_schema"}:
            fail(f"{path}: {item_id} has invalid current_status")
        for field in ("current_evidence", "required_evidence", "safe_failure"):
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: {item_id} {field} must be descriptive")
        require_safe_failure(path, item_id, text(item.get("safe_failure")))
    check_no_duplicates(negative_ids, "negative coverage IDs")
    if set(negative_cases) != REQUIRED_NEGATIVE_CASES:
        fail(
            f"{path}: negative cases must be exactly: "
            + ", ".join(sorted(REQUIRED_NEGATIVE_CASES))
        )
    oversized = next((item for item in negative_items if item.get("case") == "oversized"), None)
    if not isinstance(oversized, dict) or oversized.get("current_status") != "implemented_m0_test":
        fail(f"{path}: oversized negative case must identify implemented M0 test")
    for item in negative_items:
        if item.get("case") != "oversized" and item.get("current_status") == "implemented_m0_test":
            fail(f"{path}: only oversized can be implemented_m0_test in current inventory")

    process_capabilities = load_json(MACHINE / "process-capabilities.json")
    roles = process_capabilities.get("roles") if isinstance(process_capabilities, dict) else None
    if not isinstance(roles, dict):
        fail("process-capabilities.json must contain a roles object")

    role_items = require_list(data, "role_capability_boundaries")
    role_ids: list[str] = []
    boundary_roles: list[str] = []
    for item in role_items:
        if not isinstance(item, dict):
            fail(f"{path}: role_capability_boundaries entries must be objects")
        item_id = text(item.get("id"))
        if not ROLE_ID.match(item_id):
            fail(f"{path}: invalid role boundary id {item_id!r}")
        role_ids.append(item_id)
        role = text(item.get("process_capability_role"))
        boundary_roles.append(role)
        if role not in roles:
            fail(f"{path}: role {role!r} is not in process-capabilities.json")
        for field in ("boundary", "current_evidence", "missing_evidence"):
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: {item_id} {field} must be descriptive")
    check_no_duplicates(role_ids, "role boundary IDs")
    if set(boundary_roles) != set(roles):
        fail(
            f"{path}: role boundaries must match process-capabilities roles; found: "
            + ", ".join(sorted(boundary_roles))
        )

    ipc_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "crates" / "turing-ipc" / "src").glob("*.rs"))
    )
    for phrase in [
        "MAX_REGISTERED_PROCESSES",
        "rejects_message_larger_than_generated_kind_limit",
        "enforces_generated_document_scope",
        "applies_byte_backpressure_without_dropping_item",
        "tools/generate_ipc.py",
    ]:
        if phrase not in ipc_source:
            fail(f"turing-ipc source is missing expected current-evidence phrase: {phrase}")
    kernel_source = (ROOT / "crates" / "turing-kernel" / "src" / "lib.rs").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "renderer_cannot_launch_processes",
        "generated_route_and_capability_are_enforced",
        "attenuated_process_cannot_use_removed_capability",
        "renderer_cannot_register_a_channel",
    ]:
        if phrase not in kernel_source:
            fail(f"turing-kernel source is missing expected current-evidence phrase: {phrase}")

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    readiness_items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(readiness_items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb011 = next((item for item in readiness_items if item.get("id") == "PB-011"), None)
    if not isinstance(pb011, dict):
        fail("pre-build-readiness.json is missing PB-011")
    if pb011.get("status") != "partial":
        fail("PB-011 must remain partial while only no-claim boundary inventory, schema-source template, and readiness-review template exist")
    required_evidence = {
        "docs/research/ipc-capability-boundary-inventory-2026-07.md",
        "docs/blueprint-v1/machine/ipc-capability-boundary.schema.json",
        "docs/blueprint-v1/machine/ipc-capability-boundary.json",
        "docs/blueprint-v1/machine/ipc-schema-source.schema.json",
        "docs/blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json",
        "docs/blueprint-v1/machine/ipc-readiness-review.schema.json",
        "docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json",
        "tools/validate_ipc_capability_boundaries.py",
        "tools/validate_ipc_readiness_review.py",
    }
    pb011_evidence = pb011.get("evidence")
    if not isinstance(pb011_evidence, list):
        fail("PB-011 must list no-claim boundary inventory evidence")
    missing_evidence = sorted(required_evidence - set(pb011_evidence))
    if missing_evidence:
        fail("PB-011 evidence is missing IPC capability boundary records: " + ", ".join(missing_evidence))

    required_text = " ".join(
        value for value in pb011.get("evidence_required", []) if isinstance(value, str)
    ).lower()
    for phrase in [
        "schema generator",
        "checked no-claim schema-source template",
        "checked no-claim ipc readiness-review template",
        "wire encoding decision",
        "connection authentication",
        "bounded queues",
        "backpressure",
        "malformed",
        "oversized",
        "stale",
        "duplicate",
        "reordered",
        "unauthorized",
        "wrong-principal",
        "timeout",
        "cancellation",
        "owner-reviewed ipc readiness review",
    ]:
        if phrase not in required_text:
            fail(f"PB-011 evidence_required must include {phrase}")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks") if isinstance(task_queue, dict) else None
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain a tasks array")
    task = next((item for item in tasks if item.get("id") == "TASK-000003"), None)
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000003")
    if task.get("status") != "proposed":
        fail("TASK-000003 must remain proposed until owner review converts it to an executable task")


def validate_schema_source(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: schema source must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    schema_source_id = text(data.get("schema_source_id"))
    if not SCHEMA_SOURCE_ID.match(schema_source_id):
        fail(f"{path}: invalid schema_source_id {schema_source_id!r}")
    if data.get("status") != "no_claim_schema_source_template":
        fail(f"{path}: status must be no_claim_schema_source_template")

    boundaries = [text(value).lower() for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")).lower(), *boundaries])
    for phrase in REQUIRED_SCHEMA_SOURCE_CLAIM_PHRASES:
        if phrase.lower() not in boundary_text:
            fail(f"{path}: missing schema-source unsupported boundary phrase: {phrase}")

    sources = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SCHEMA_SOURCE_RECORDS - sources)
    if missing_sources:
        fail(f"{path}: missing schema-source records: {', '.join(missing_sources)}")
    for source in REQUIRED_SCHEMA_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: schema-source record does not exist: {source}")

    generator_status = data.get("generator_status")
    if not isinstance(generator_status, dict):
        fail(f"{path}: generator_status must be an object")
    if generator_status.get("implemented") is not False:
        fail(f"{path}: generator_status.implemented must remain false")
    if generator_status.get("approved_generator_source") is not False:
        fail(f"{path}: approved_generator_source must remain false")
    if not text(generator_status.get("regeneration_command")).startswith("none "):
        fail(f"{path}: regeneration_command must state none")

    wire_status = data.get("wire_encoding_status")
    if not isinstance(wire_status, dict):
        fail(f"{path}: wire_encoding_status must be an object")
    if wire_status.get("decision") != "not_decided":
        fail(f"{path}: wire_encoding_status.decision must remain not_decided")
    if wire_status.get("approved") is not False:
        fail(f"{path}: wire_encoding_status.approved must remain false")
    if wire_status.get("bounded_decode_evidence") != "missing":
        fail(f"{path}: bounded_decode_evidence must remain missing")
    if "fail closed" not in text(wire_status.get("unknown_variant_policy")).lower():
        fail(f"{path}: unknown_variant_policy must require fail-closed behavior")

    schema_scope = data.get("schema_scope")
    if not isinstance(schema_scope, dict):
        fail(f"{path}: schema_scope must be an object")
    if schema_scope.get("maturity") != "template_only":
        fail(f"{path}: schema_scope.maturity must be template_only")
    if (
        schema_scope.get("linked_process_capabilities")
        != "docs/blueprint-v1/machine/process-capabilities.json"
    ):
        fail(f"{path}: schema_scope must link process-capabilities.json")
    for key in ("message_definition_status", "persistent_format_status"):
        value = text(schema_scope.get(key)).lower()
        if "not" not in value and "no " not in value:
            fail(f"{path}: schema_scope.{key} must keep unsupported status explicit")

    metadata = {text(value) for value in require_list(data, "required_message_metadata")}
    missing_metadata = sorted(REQUIRED_MESSAGE_METADATA - metadata)
    if missing_metadata:
        fail(f"{path}: missing required message metadata: {', '.join(missing_metadata)}")

    process_capabilities = load_json(MACHINE / "process-capabilities.json")
    roles = process_capabilities.get("roles") if isinstance(process_capabilities, dict) else None
    if not isinstance(roles, dict):
        fail("process-capabilities.json must contain a roles object")
    links = require_list(data, "role_authority_links")
    linked_roles: list[str] = []
    for item in links:
        if not isinstance(item, dict):
            fail(f"{path}: role_authority_links entries must be objects")
        role = text(item.get("process_capability_role"))
        linked_roles.append(role)
        if role not in roles:
            fail(f"{path}: role {role!r} is not in process-capabilities.json")
        if item.get("capabilities_checked") is not True:
            fail(f"{path}: {role} capabilities_checked must be true")
        if item.get("forbidden_authority_checked") is not True:
            fail(f"{path}: {role} forbidden_authority_checked must be true")
        if len(text(item.get("schema_source_status"))) < 30:
            fail(f"{path}: {role} schema_source_status must be descriptive")
    check_no_duplicates(linked_roles, "schema-source role links")
    if set(linked_roles) != set(roles):
        fail(
            f"{path}: role_authority_links must match process-capabilities roles; found: "
            + ", ".join(sorted(linked_roles))
        )

    outputs = {text(value) for value in require_list(data, "generator_output_plan")}
    missing_outputs = sorted(REQUIRED_GENERATOR_OUTPUTS - outputs)
    if missing_outputs:
        fail(f"{path}: missing generator output plan entries: {', '.join(missing_outputs)}")

    negative_items = require_list(data, "negative_fixture_plan")
    cases: list[str] = []
    for item in negative_items:
        if not isinstance(item, dict):
            fail(f"{path}: negative_fixture_plan entries must be objects")
        case = text(item.get("case")).lower()
        cases.append(case)
        if item.get("current_status") not in {"missing", "not_executable_without_generator"}:
            fail(f"{path}: {case} has invalid current_status")
        for field in ("required_fixture", "safe_failure"):
            value = text(item.get(field))
            if len(value) < 30:
                fail(f"{path}: {case} {field} must be descriptive")
        require_safe_failure(path, case, text(item.get("safe_failure")))
    check_no_duplicates(cases, "schema-source negative fixture cases")
    if set(cases) != REQUIRED_NEGATIVE_CASES:
        fail(
            f"{path}: negative fixture cases must be exactly: "
            + ", ".join(sorted(REQUIRED_NEGATIVE_CASES))
        )
    if "architecture owner review" not in " ".join(text(value) for value in require_list(data, "review_gates")).lower():
        fail(f"{path}: review_gates must require architecture owner review")
    commands = set(text(value) for value in require_list(data, "validation_commands"))
    missing_commands = sorted(REQUIRED_SCHEMA_COMMANDS - commands)
    if missing_commands:
        fail(f"{path}: missing validation commands: {', '.join(missing_commands)}")

    docs_to_check = {
        ROOT / "README.md": ["IPC schema-source template", "`TASK-000011` acceptance"],
        DOCS / "start-here.md": ["IPC schema-source template", "no accepted `TASK-000011`"],
        DOCS / "README.md": ["IPC schema-source template", "`TASK-000011` acceptance"],
        DOCS / "repository-map.md": ["IPC schema-source template", "`TASK-000011` review handoff"],
        DOCS / "research" / "README.md": ["IPC schema-source template", "Independent review and evidence bundle for `TASK-000011`"],
        DOCS / "research" / "ipc-capability-boundary-inventory-2026-07.md": ["IPC schema-source template", "accepted `TASK-000011` evidence bundle"],
        DOCS / "api-design" / "03-schemas-errors-versioning-and-compatibility.md": ["IPC schema-source template", "review-pending M0 generator/reference"],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": ["IPC schema-source template", "no accepted `TASK-000011`"],
        DOCS / "project-buildout" / "17-build-readiness-task-queue.md": ["IPC schema-source template", "no schema-generator approval"],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": ["TASK-000011 WP-002 review handoff", "evidence-bundle instance"],
    }
    for doc_path, phrases in docs_to_check.items():
        content = doc_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in content]
        if missing:
            fail(f"{doc_path}: missing IPC schema-source documentation: {', '.join(missing)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inventories",
        nargs="*",
        type=Path,
        default=[DEFAULT_INVENTORY],
        help="IPC capability boundary inventory JSON files to validate.",
    )
    args = parser.parse_args()
    for path in args.inventories:
        validate_inventory(path)
    validate_schema_source(DEFAULT_SCHEMA_SOURCE)
    print(
        f"IPC capability boundary validation passed: {len(args.inventories)} inventory file(s), "
        "1 schema-source template"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
