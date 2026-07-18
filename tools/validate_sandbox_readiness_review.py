#!/usr/bin/env python3
"""Validate checked no-claim sandbox readiness-review templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
SECURITY_MACHINE = DOCS / "security-engine" / "machine"
DEFAULT_REVIEW = (
    SECURITY_MACHINE
    / "sandbox-readiness-reviews"
    / "no-claim-sandbox-readiness-template.json"
)

REVIEW_ID = re.compile(r"^SANDBOX\.READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_REVIEW_FILES = [
    "docs/security-engine/machine/sandbox-readiness-review.schema.json",
    "docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json",
    "tools/validate_sandbox_readiness_review.py",
]

REQUIRED_SOURCE_RECORDS = {
    "docs/research/sandbox-probe-inventory-2026-07.md",
    "docs/security-engine/machine/sandbox-probe-inventory.schema.json",
    "docs/security-engine/machine/sandbox-probe-inventory.json",
    "docs/security-engine/machine/sandbox-probe-package.schema.json",
    "docs/security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json",
    "docs/security-engine/machine/sandbox-readiness-review.schema.json",
    "docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json",
    "docs/blueprint-v1/machine/process-capabilities.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/04-system-architecture.md",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/security-engine/01-threat-model-and-process-isolation.md",
    "docs/security-engine/02-sandbox-brokers-and-platform-containment.md",
    "docs/security-engine/06-security-verification-and-release-gates.md",
    "docs/platform/README.md",
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "tools/validate_sandbox_probe_inventory.py",
    "tools/validate_sandbox_readiness_review.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no security review",
    "no platform review",
    "no quality review",
    "no release-operations review",
    "no packaged expected-deny probes",
    "no effective platform policy review",
    "no host-safe fixture review",
    "no broker fixture review",
    "no compromised-client harness review",
    "no platform matrix review",
    "no result-record review",
    "no failure-denominator review",
    "no cleanup review",
    "no sandbox-readiness claim",
    "no renderer-security claim",
    "no site-isolation claim",
    "no hostile-browsing safety claim",
    "no platform containment claim",
    "no SEC-GATE-1 claim",
    "no SEC-GATE-6 claim",
    "no production-safety claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "security_reviewed",
    "platform_reviewed",
    "quality_reviewed",
    "release_operations_reviewed",
    "probe_inventory_reviewed",
    "probe_package_reviewed",
    "packaged_expected_deny_probes_reviewed",
    "effective_policy_reviewed",
    "host_safe_fixtures_reviewed",
    "broker_fixtures_reviewed",
    "compromised_client_harnesses_reviewed",
    "platform_matrix_reviewed",
    "result_records_reviewed",
    "failure_denominator_reviewed",
    "cleanup_reviewed",
    "sandbox_readiness_supported",
    "renderer_security_supported",
    "site_isolation_supported",
    "hostile_browsing_safety_supported",
    "platform_containment_supported",
    "sec_gate_1_supported",
    "sec_gate_6_supported",
    "production_safety_supported",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "probe_inventory",
    "probe_package",
    "owner_reviewer",
    "security_reviewer",
    "platform_reviewer",
    "quality_reviewer",
    "release_operations_reviewer",
]

REQUIRED_AXIS_TERMS = [
    "packaged role runner",
    "artifact build ID",
    "role launch path",
    "handle set",
    "process identity",
    "result record schema",
    "failure denominator",
    "windows effective policy",
    "macos effective policy",
    "linux effective policy",
    "effective platform policy capture",
    "platform matrix",
    "unsupported and degraded modes",
    "renderer",
    "network",
    "storage",
    "gpu",
    "decoder",
    "extension",
    "devtools",
    "agent",
    "updater",
    "file",
    "socket",
    "process",
    "registry",
    "device",
    "shared-memory",
    "credential",
    "debug",
    "profile",
    "IPC",
    "host-safe fixtures",
    "bounded temporary roots",
    "fake credentials",
    "fake profiles",
    "loopback fixtures",
    "cleanup checks",
    "broker fixtures",
    "compromised-client harnesses",
    "forged IDs",
    "stale epochs",
    "oversized paths and sizes",
    "ordering and retries",
    "broker exceptions",
    "audit and redaction",
    "owner review",
    "security review",
    "platform review",
    "quality review",
    "release-operations review",
    "SEC-GATE-1",
    "SEC-GATE-6",
    "promotion boundary",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "packaged expected-deny probes",
    "effective platform policy",
    "platform matrix",
    "host-safe",
    "broker fixtures",
    "compromised-client",
    "hidden failures",
    "real secrets",
    "production profile",
    "unbounded",
    "validation",
    "claim boundary",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_sandbox_probe_inventory.py",
    "python3 -B tools/validate_sandbox_readiness_review.py",
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
        ("sandbox readiness", "sandbox-readiness"),
        ("renderer security", "renderer-security"),
        ("site isolation", "site-isolation"),
        ("hostile browsing", "hostile-browsing"),
        ("platform containment", "platform-containment"),
        ("production safety", "production-safety"),
        ("effective platform policy", "effective-platform-policy"),
        ("host safe", "host-safe"),
        ("compromised client", "compromised-client"),
        ("expected deny", "expected-deny"),
        ("sec gate", "sec-gate"),
        ("sec-gate-1", "sec-gate-1"),
        ("sec-gate-6", "sec-gate-6"),
        ("claim boundary", "claim-boundary"),
        ("pb 012", "pb-012"),
        ("pb012", "pb-012"),
        ("result record", "result-record"),
        ("failure denominator", "failure-denominator"),
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
    if data.get("status") != "no_claim_sandbox_readiness_template":
        fail(f"{path}: status must be no_claim_sandbox_readiness_template")

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
    for phrase in ["placeholder", "self-approval", "pb-012", "null"]:
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
                "probe_package_axes",
                "platform_policy_axes",
                "role_surface_axes",
                "host_safety_axes",
                "broker_compromised_axes",
                "owner_review_axes",
            ]
            for item in require_list(data, key)
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing sandbox readiness axis term: {phrase}")
    if "beyond the checked no-claim sandbox-readiness-review template" not in axis_text:
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
            if isinstance(entry, dict) and entry.get("id") == "PB-012"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-012")
    if item.get("status") != "partial":
        fail("PB-012 must remain partial while the sandbox review is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-012 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-012 evidence is missing sandbox readiness review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim sandbox readiness-review template",
        "owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template",
        "packaged expected-deny probes",
        "effective platform policy",
        "host-safe fixtures",
        "broker fixtures",
        "compromised-client harnesses",
        "platform matrix evidence",
        "sandbox-readiness",
        "renderer-security",
        "site-isolation",
        "SEC-GATE-1",
        "SEC-GATE-6",
        "production-safety",
    ]:
        if normalize(phrase) not in required_text:
            fail(f"PB-012 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000004"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000004 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000004 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000004 allowed_paths missing sandbox review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim sandbox readiness-review template",
        "owner-reviewed sandbox readiness review",
        "cannot be cited",
        "PB-012 readiness",
        "sandbox-readiness",
        "renderer-security",
        "site-isolation",
        "SEC-GATE",
        "production-safety",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000004 must mention sandbox review boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict) and item.get("id") == "research-lane-sandbox-probes"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing sandbox lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("sandbox lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("sandbox lane evidence_start missing sandbox review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template",
        "no PB-012 readiness promotion",
        "no sandbox-readiness claim from the checked no-claim sandbox readiness-review template",
        "no renderer-security claim",
        "no site-isolation claim",
        "no production-safety claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"sandbox lane must mention {phrase}")


def validate_docs() -> None:
    docs_to_check = {
        ROOT / "README.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness"],
        DOCS / "start-here.md": ["sandbox readiness-review template", "no owner-reviewed sandbox readiness"],
        DOCS / "README.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness"],
        DOCS / "repository-map.md": ["sandbox readiness-review template", "sandbox-readiness-review.schema.json"],
        DOCS / "research" / "README.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template"],
        DOCS / "research" / "sandbox-probe-inventory-2026-07.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template"],
        DOCS / "security-engine" / "02-sandbox-brokers-and-platform-containment.md": ["sandbox readiness-review template", "no owner-reviewed sandbox readiness"],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness"],
        DOCS / "project-buildout" / "17-build-readiness-task-queue.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness"],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": ["sandbox readiness-review template", "owner-reviewed sandbox readiness"],
    }
    for doc_path, phrases in docs_to_check.items():
        content = doc_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in content]
        if missing:
            fail(f"{doc_path}: missing sandbox readiness-review documentation: {', '.join(missing)}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    validate_docs()
    print(f"sandbox readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
