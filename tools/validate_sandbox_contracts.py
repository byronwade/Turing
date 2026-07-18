#!/usr/bin/env python3
"""Validate the no-claim WP-003 sandbox operation and evidence contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "schemas" / "sandbox" / "probe-catalog.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas" / "sandbox" / "probe-evidence.schema.json"
REPORT_PATH = ROOT / "docs" / "research" / "wp-003-sandbox-probe-plan-2026-07.md"
TASK_QUEUE_PATH = ROOT / "docs" / "blueprint-v1" / "machine" / "build-readiness-task-queue.json"
PREBUILD_PATH = ROOT / "docs" / "blueprint-v1" / "machine" / "pre-build-readiness.json"
RESEARCH_INDEX_PATH = ROOT / "docs" / "research" / "README.md"

EXPECTED_RESULTS = [
    "allowed",
    "denied",
    "killed",
    "brokered",
    "unsupported",
    "not_attempted",
    "error",
]
EXPECTED_PLATFORMS = {"linux", "macos", "windows"}
EXPECTED_REDACTIONS = {
    "user_profile_path",
    "username",
    "hostname",
    "credential",
    "token",
    "cookie",
    "page_content",
    "clipboard_content",
    "device_serial",
    "stable_machine_identifier",
    "external_ip_address",
}
EXPECTED_CATEGORIES = {
    "control",
    "file",
    "dynamic-code",
    "socket",
    "process",
    "debug",
    "credential",
    "device",
    "ipc",
    "registry",
    "profile",
}
REQUIRED_PB012_EVIDENCE = [
    "docs/research/wp-003-sandbox-probe-plan-2026-07.md",
    "schemas/sandbox/probe-catalog.json",
    "schemas/sandbox/probe-evidence.schema.json",
    "tools/validate_sandbox_contracts.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"sandbox contract validation failed: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as error:
        fail(f"{path.relative_to(ROOT)} is invalid JSON: {error}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def find_task(task_queue: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = task_queue.get("tasks")
    require(isinstance(tasks, list), "build-readiness task queue must contain tasks[]")
    for task in tasks:
        if isinstance(task, dict) and task.get("id") == task_id:
            return task
    fail(f"build-readiness task queue is missing {task_id}")


def find_readiness(readiness: dict[str, Any], item_id: str) -> dict[str, Any]:
    items = readiness.get("items")
    require(isinstance(items, list), "pre-build readiness must contain items[]")
    for item in items:
        if isinstance(item, dict) and item.get("id") == item_id:
            return item
    fail(f"pre-build readiness is missing {item_id}")


def validate_catalog(catalog: dict[str, Any]) -> None:
    require(catalog.get("schema_version") == 1, "catalog schema_version must be 1")
    require(catalog.get("catalog_id") == "SANDBOX.PROBE.CATALOG.2026_07", "catalog_id drifted")
    require(catalog.get("status") == "no_claim_contract", "catalog status must stay no_claim_contract")
    require(catalog.get("related_readiness") == "PB-012", "catalog must map to PB-012")
    require(catalog.get("related_task") == "TASK-000004", "catalog must map to TASK-000004")
    require(catalog.get("default_policy") == "deny", "catalog default policy must be deny")
    claim_status = catalog.get("claim_status", "")
    for phrase in [
        "No-claim sandbox probe contract only",
        "no effective platform policy",
        "no owner-reviewed sandbox readiness",
        "no renderer-security",
        "no site-isolation",
        "no SEC-GATE evidence",
        "no production-safety",
        "no implementation claim",
    ]:
        require(phrase in claim_status, f"catalog claim_status is missing {phrase}")
    require(catalog.get("result_values") == EXPECTED_RESULTS, "catalog result enum drifted")

    rules = catalog.get("rules")
    require(isinstance(rules, dict), "catalog must define rules")
    for key in [
        "unsandboxed_control_required",
        "unexpected_allow_is_blocking",
        "unexpected_deny_requires_review",
        "destructive_external_targets_forbidden",
    ]:
        require(rules.get(key) is True, f"catalog rule {key} must be true")
    for key in ["unsupported_is_pass", "application_stub_denial_is_pass"]:
        require(rules.get(key) is False, f"catalog rule {key} must be false")

    operations = catalog.get("operations")
    require(isinstance(operations, list), "catalog operations must be a list")
    require(len(operations) == 21, "catalog must define exactly 21 operations")
    seen_ids: set[str] = set()
    seen_categories: set[str] = set()
    seen_platforms: set[str] = set()
    controls = 0
    for index, operation in enumerate(operations, start=1):
        require(isinstance(operation, dict), "catalog operations must be objects")
        expected_id = f"SBX-PROBE-{index:03d}"
        probe_id = operation.get("id")
        require(probe_id == expected_id, f"expected {expected_id}, got {probe_id}")
        require(probe_id not in seen_ids, f"duplicate probe id {probe_id}")
        seen_ids.add(probe_id)
        require(operation.get("destructive") is False, f"{probe_id} must be non-destructive")
        require(isinstance(operation.get("name"), str) and operation["name"], f"{probe_id} must have a name")
        require(
            isinstance(operation.get("safe_target"), str) and len(operation["safe_target"]) >= 12,
            f"{probe_id} must describe a safe target",
        )
        require(
            isinstance(operation.get("enforcement_required"), str)
            and len(operation["enforcement_required"]) >= 12,
            f"{probe_id} must describe required enforcement",
        )
        category = operation.get("category")
        require(isinstance(category, str), f"{probe_id} category must be a string")
        seen_categories.add(category)
        expected = operation.get("expected_on_supported_sandbox")
        require(expected in EXPECTED_RESULTS, f"{probe_id} uses unknown expected result {expected}")
        platforms = operation.get("platforms")
        require(isinstance(platforms, list) and platforms, f"{probe_id} must list platforms")
        require(set(platforms).issubset(EXPECTED_PLATFORMS), f"{probe_id} has an unknown platform")
        seen_platforms.update(str(platform) for platform in platforms)
        if operation.get("control") is True:
            controls += 1
            require(expected == "allowed", f"{probe_id} control probes must be expected allowed")
        else:
            require(expected != "allowed", f"{probe_id} expected-deny probe cannot expect allowed")

    require(controls == 3, "catalog must contain exactly three control probes")
    require(EXPECTED_PLATFORMS <= seen_platforms, "catalog must cover linux, macos, and windows")
    missing_categories = EXPECTED_CATEGORIES - seen_categories
    require(not missing_categories, "catalog missing categories: " + ", ".join(sorted(missing_categories)))


def validate_evidence_schema(schema: dict[str, Any]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft drifted")
    require(schema.get("type") == "object", "evidence schema must describe an object")
    require(schema.get("additionalProperties") is False, "evidence schema must reject additional properties")
    required = schema.get("required")
    for field in [
        "schema_version",
        "probe_catalog_version",
        "run_id",
        "build_identity",
        "platform",
        "sandbox_policy",
        "launcher",
        "probe_process",
        "redaction",
        "results",
        "summary",
    ]:
        require(isinstance(required, list) and field in required, f"evidence schema missing required {field}")

    properties = schema.get("properties")
    require(isinstance(properties, dict), "evidence schema properties must be an object")
    result_enum = (
        properties.get("results", {})
        .get("items", {})
        .get("properties", {})
        .get("actual", {})
        .get("enum")
    )
    require(result_enum == EXPECTED_RESULTS, "evidence result enum must match catalog")
    release_claim = properties.get("summary", {}).get("properties", {}).get("release_claim", {}).get("const")
    require(release_claim == "research_evidence_only", "evidence release_claim must remain research_evidence_only")
    stable_machine_identifier = (
        properties.get("redaction", {})
        .get("properties", {})
        .get("stable_machine_identifier_included", {})
        .get("const")
    )
    require(stable_machine_identifier is False, "redaction must exclude stable machine identifiers")
    forbidden_classes = (
        properties.get("redaction", {})
        .get("properties", {})
        .get("forbidden_data_classes", {})
        .get("items", {})
        .get("enum")
    )
    require(set(forbidden_classes or []) == EXPECTED_REDACTIONS, "redaction forbidden data classes drifted")
    role_enum = properties.get("sandbox_policy", {}).get("properties", {}).get("role", {}).get("enum")
    for role in ["renderer", "network", "storage", "gpu", "decoder", "extension", "devtools", "agent", "updater"]:
        require(role in (role_enum or []), f"evidence schema missing role {role}")


def validate_task_and_readiness(task_queue: dict[str, Any], readiness: dict[str, Any]) -> None:
    task = find_task(task_queue, "TASK-000004")
    require(task.get("status") == "proposed", "TASK-000004 must remain proposed")
    require(task.get("dependencies") == ["TASK-000003"], "TASK-000004 dependency must remain TASK-000003")
    allowed_paths = task.get("allowed_paths")
    require(isinstance(allowed_paths, list), "TASK-000004 allowed_paths must be a list")
    for path in [
        "schemas/sandbox/",
        "tools/validate_sandbox_contracts.py",
        "docs/research/wp-003-sandbox-probe-plan-2026-07.md",
    ]:
        require(path in allowed_paths, f"TASK-000004 allowed_paths missing {path}")
    task_text = " ".join(
        value
        for field in ("preconditions", "acceptance_criteria", "negative_tests")
        for value in task.get(field, [])
        if isinstance(value, str)
    )
    for phrase in [
        "operation catalog",
        "evidence schema",
        "unsandboxed control",
        "unsupported",
        "application-level stub",
        "owner-reviewed sandbox readiness",
    ]:
        require(phrase in task_text, f"TASK-000004 scope missing {phrase}")

    pb012 = find_readiness(readiness, "PB-012")
    require(pb012.get("status") == "partial", "PB-012 must remain partial")
    evidence = pb012.get("evidence")
    require(isinstance(evidence, list), "PB-012 evidence must be a list")
    for path in REQUIRED_PB012_EVIDENCE:
        require(path in evidence, f"PB-012 evidence missing {path}")
    evidence_required = " ".join(value for value in pb012.get("evidence_required", []) if isinstance(value, str))
    for phrase in [
        "stable operation catalog",
        "evidence schema",
        "unsandboxed control",
        "application-level stub",
        "unsupported platform primitives",
    ]:
        require(phrase in evidence_required, f"PB-012 evidence_required missing {phrase}")


def validate_report_and_index() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    for phrase in [
        "Status: no-claim implementation-planning contract",
        "Related task: `TASK-000004`",
        "An unsandboxed control run is mandatory",
        "Unsupported platform primitives are recorded as `unsupported` and never counted as a pass",
        "Application-level stub denial is not enough",
        "No strategy is approved by this plan",
        "`TASK-000004` remains proposed",
        "This contract does not support",
    ]:
        require(phrase in report, f"WP-003 report missing {phrase}")

    research_index = RESEARCH_INDEX_PATH.read_text(encoding="utf-8")
    for phrase in [
        "WP-003 Sandbox Probe Contract",
        "probe-catalog.json",
        "probe-evidence.schema.json",
        "validate_sandbox_contracts.py",
    ]:
        require(phrase in research_index, f"research index missing {phrase}")


def main() -> None:
    validate_catalog(load_json(CATALOG_PATH))
    validate_evidence_schema(load_json(EVIDENCE_SCHEMA_PATH))
    validate_task_and_readiness(load_json(TASK_QUEUE_PATH), load_json(PREBUILD_PATH))
    validate_report_and_index()
    print("sandbox contract validation passed: WP-003 no-claim contract stays tied to PB-012/TASK-000004")


if __name__ == "__main__":
    main()
