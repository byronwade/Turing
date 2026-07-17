#!/usr/bin/env python3
"""Validate the WP-003 sandbox planning contracts without third-party packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "schemas/sandbox/probe-catalog.json"
EVIDENCE_PATH = ROOT / "schemas/sandbox/probe-evidence.schema.json"
TASK_PATH = ROOT / "docs/agent-execution/machine/tasks/TASK-000002.json"
REPORT_PATH = ROOT / "docs/research/wp-003-sandbox-probe-plan-2026-07.md"

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


class ContractError(ValueError):
    """Raised when a sandbox planning contract violates an invariant."""


def load_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"{path.relative_to(ROOT)}: invalid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise ContractError(f"{path.relative_to(ROOT)}: root must be an object")
    return payload


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def validate_catalog(catalog: dict[str, object]) -> None:
    require(catalog.get("schema_version") == 1, "probe catalog must use schema_version 1")
    require(catalog.get("status") == "proposed_contract", "probe catalog must remain proposed_contract")
    require(catalog.get("default_policy") == "deny", "probe catalog default policy must be deny")
    require(catalog.get("result_values") == EXPECTED_RESULTS, "probe catalog result values drifted")

    rules = catalog.get("rules")
    require(isinstance(rules, dict), "probe catalog rules must be an object")
    assert isinstance(rules, dict)
    require(rules.get("unsupported_is_pass") is False, "unsupported operations must never pass")
    require(
        rules.get("application_stub_denial_is_pass") is False,
        "application-level stub denials must never pass",
    )
    require(rules.get("unexpected_allow_is_blocking") is True, "unexpected allows must block")

    operations = catalog.get("operations")
    require(isinstance(operations, list), "probe catalog operations must be an array")
    assert isinstance(operations, list)
    expected_ids = [f"SBX-PROBE-{index:03d}" for index in range(1, 22)]
    ids: list[object] = []
    names: list[object] = []
    control_count = 0
    for operation in operations:
        require(isinstance(operation, dict), "each probe operation must be an object")
        assert isinstance(operation, dict)
        ids.append(operation.get("id"))
        names.append(operation.get("name"))
        platforms = operation.get("platforms")
        require(isinstance(platforms, list) and platforms, f"{operation.get('id')}: platforms must be non-empty")
        assert isinstance(platforms, list)
        require(set(platforms).issubset(EXPECTED_PLATFORMS), f"{operation.get('id')}: unknown platform")
        require(operation.get("destructive") is False, f"{operation.get('id')}: destructive probe forbidden")
        require(
            isinstance(operation.get("sandbox_expectation"), str)
            and bool(operation.get("sandbox_expectation")),
            f"{operation.get('id')}: sandbox expectation required",
        )
        require(
            isinstance(operation.get("unsandboxed_control_expectation"), str)
            and bool(operation.get("unsandboxed_control_expectation")),
            f"{operation.get('id')}: control expectation required",
        )
        require(
            isinstance(operation.get("target"), str) and bool(operation.get("target")),
            f"{operation.get('id')}: safe target description required",
        )
        if operation.get("category") == "control":
            control_count += 1
            require(operation.get("sandbox_expectation") == "allowed", f"{operation.get('id')}: control must be allowed")
    require(ids == expected_ids, f"probe IDs must be contiguous SBX-PROBE-001..021; found {ids}")
    require(len(names) == len(set(names)), "probe operation names must be unique")
    require(control_count >= 3, "catalog must contain at least three positive controls")


def validate_evidence_schema(schema: dict[str, object]) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "evidence schema draft drifted")
    require(schema.get("additionalProperties") is False, "evidence root must reject additional properties")
    required = schema.get("required")
    require(isinstance(required, list), "evidence schema required list missing")
    assert isinstance(required, list)
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
        require(field in required, f"evidence schema must require {field}")

    properties = schema.get("properties")
    require(isinstance(properties, dict), "evidence schema properties missing")
    assert isinstance(properties, dict)
    require(properties.get("schema_version") == {"const": 1}, "evidence schema version must be 1")

    results = properties.get("results")
    require(isinstance(results, dict), "results schema missing")
    assert isinstance(results, dict)
    item = results.get("items")
    require(isinstance(item, dict), "results item schema missing")
    assert isinstance(item, dict)
    item_properties = item.get("properties")
    require(isinstance(item_properties, dict), "results item properties missing")
    assert isinstance(item_properties, dict)
    actual = item_properties.get("actual")
    require(isinstance(actual, dict), "result actual enum missing")
    assert isinstance(actual, dict)
    require(actual.get("enum") == EXPECTED_RESULTS, "evidence actual values must match catalog result values")

    summary = properties.get("summary")
    require(isinstance(summary, dict), "summary schema missing")
    assert isinstance(summary, dict)
    summary_properties = summary.get("properties")
    require(isinstance(summary_properties, dict), "summary properties missing")
    assert isinstance(summary_properties, dict)
    release_claim = summary_properties.get("release_claim")
    require(
        release_claim == {"const": "research_evidence_only"},
        "sandbox evidence must remain research_evidence_only",
    )

    redaction = properties.get("redaction")
    require(isinstance(redaction, dict), "redaction schema missing")
    assert isinstance(redaction, dict)
    redaction_properties = redaction.get("properties")
    require(isinstance(redaction_properties, dict), "redaction properties missing")
    assert isinstance(redaction_properties, dict)
    stable = redaction_properties.get("stable_machine_identifier_included")
    require(stable == {"const": False}, "stable machine identifiers must be forbidden")
    forbidden = redaction_properties.get("forbidden_data_classes")
    require(isinstance(forbidden, dict), "forbidden data classes schema missing")
    assert isinstance(forbidden, dict)
    items = forbidden.get("items")
    require(isinstance(items, dict), "forbidden data classes items missing")
    assert isinstance(items, dict)
    require(set(items.get("enum", [])) == EXPECTED_REDACTIONS, "redaction data-class set drifted")


def validate_task(task: dict[str, object]) -> None:
    require(task.get("schema_version") == 1, "TASK-000002 must use schema_version 1")
    require(task.get("id") == "TASK-000002", "sandbox task ID must be TASK-000002")
    require(task.get("status") == "specified", "TASK-000002 must remain specified")
    require(task.get("dependencies") == ["TASK-000001"], "TASK-000002 must depend on TASK-000001")
    require(task.get("requirements") == ["REQ-SEC-001"], "TASK-000002 must map only to REQ-SEC-001")
    preconditions = task.get("preconditions")
    require(isinstance(preconditions, list), "TASK-000002 preconditions missing")
    assert isinstance(preconditions, list)
    require(any("independently accepted" in item for item in preconditions), "WP-002 independent acceptance gate missing")
    acceptance = task.get("acceptance_criteria")
    require(isinstance(acceptance, list) and len(acceptance) >= 10, "TASK-000002 acceptance criteria incomplete")
    negatives = task.get("negative_tests")
    require(isinstance(negatives, list) and len(negatives) >= 15, "TASK-000002 negative tests incomplete")


def validate_report(report: str) -> None:
    required_phrases = [
        "An unsandboxed control run is mandatory",
        "unsupported",
        "application-level stub",
        "research laboratory rather than a product-support promise",
        "No strategy is approved by this plan",
        "After PR #40 is independently approved and merged",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in report]
    require(not missing, "sandbox report missing policy markers: " + ", ".join(missing))


def main() -> int:
    try:
        for path in [CATALOG_PATH, EVIDENCE_PATH, TASK_PATH, REPORT_PATH]:
            require(path.is_file(), f"missing sandbox planning file: {path.relative_to(ROOT)}")
        validate_catalog(load_json(CATALOG_PATH))
        validate_evidence_schema(load_json(EVIDENCE_PATH))
        validate_task(load_json(TASK_PATH))
        validate_report(REPORT_PATH.read_text(encoding="utf-8"))
    except ContractError as error:
        print(f"sandbox contract validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "sandbox contract validation passed: 21 probes, 3 platforms, "
        "research-only evidence, TASK-000002 blocked on TASK-000001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
