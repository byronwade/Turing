#!/usr/bin/env python3
"""Validate no-claim benchmark statistics-analysis contracts."""

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
DEFAULT_PLAN = (
    MACHINE
    / "benchmark-statistics-analyses"
    / "no-claim-statistics-analysis-plan.json"
)

ANALYSIS_ID = re.compile(r"^TURING\.BENCHMARK\.STATISTICS_ANALYSIS\.[A-Z0-9._-]+$")

REFERENCE_FILES = {
    "benchmark_manifest_id": (
        MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.sample.json",
        "benchmark_id",
    ),
    "raw_artifact_index_id": (
        MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.raw-artifacts.json",
        "artifact_id",
    ),
    "artifact_package_id": (
        MACHINE / "benchmark-artifact-packages" / "no-claim-trace-package.plan.json",
        "package_id",
    ),
    "claim_bundle_id": (
        MACHINE / "benchmark-claim-bundles" / "no-claim-public-claim-template.json",
        "claim_bundle_id",
    ),
    "benchmark_readiness_review_id": (
        MACHINE
        / "benchmark-readiness-reviews"
        / "no-claim-benchmark-readiness-template.json",
        "review_id",
    ),
}

REQUIRED_SOURCE_RECORDS = {
    "docs/research/benchmark-statistics-analysis-contract-2026-07.md",
    "docs/research/performance-benchmark-readiness-packet-2026-07.md",
    "docs/research/chrome-class-performance-runbook-2026-07.md",
    "docs/benchmark-lab/07-statistics-artifacts-regressions-and-claims.md",
    "docs/performance/05-benchmarks-statistics-and-regression-governance.md",
    "docs/blueprint-v1/09-performance-memory.md",
    "docs/blueprint-v1/machine/benchmark-statistics-analysis.schema.json",
    "docs/blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json",
    "tools/validate_benchmark_statistics_analysis.py",
    "tools/validate_blueprint.py",
}

REQUIRED_CLAIM_PHRASES = [
    "no browser benchmark run",
    "no runner-generated raw sample",
    "no statistical summary from real samples",
    "no confidence interval from measured browser data",
    "no benchmark result",
    "no competitor result",
    "no memory result",
    "no energy result",
    "no Chrome-class claim",
    "no faster claim",
    "no lower-memory claim",
    "no lower-energy claim",
    "no public performance claim",
    "no production claim",
    "no daily-driver claim",
]

REQUIRED_INPUTS = {
    "runner-generated raw samples",
    "trace and artifact package hashes",
    "noise study",
    "failure denominator",
    "owner-reviewed analysis",
}

REQUIRED_METHOD_IDS = {
    "noise-study",
    "sample-count",
    "confidence-interval",
    "effect-size",
    "outlier-policy",
    "multiple-comparison",
}

REQUIRED_METRIC_IDS = {
    "latency",
    "memory",
    "energy",
    "thirty-tab",
    "compatibility-failure",
}

TERM_REQUIREMENTS = {
    "sample_design_controls": [
        "sample count",
        "warmup",
        "randomization",
        "paired",
        "cache",
        "thermal",
        "denominator",
        "30-tab",
        "all-live",
    ],
    "denominator_controls": [
        "denominator size",
        "unsupported behavior",
        "failed cases",
        "security settings",
        "lifecycle settings",
        "raw artifacts",
        "no-claim templates",
    ],
    "unsupported_behavior": [
        "no browser benchmark run exists",
        "no runner-generated raw sample exists",
        "no real statistical summary exists",
        "no benchmark result exists",
        "no competitor result exists",
        "no Chrome-class claim is supported",
        "no public performance, production, release, stable, beta, daily-driver, or implementation claim is supported",
    ],
}

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_benchmark_statistics_analysis.py",
    "python3 -B tools/validate_blueprint.py",
    ".\\tools\\check.ps1",
]


class ValidationError(ValueError):
    pass


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(path: Path | str, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(relative(path), f"invalid JSON: {error}")


def require_object(path: Path, value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(relative(path), f"{label} must be an object")
    return value


def require_string(path: Path, obj: dict[str, Any], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(relative(path), f"{label}.{key} must be a non-empty string")
    return value


def require_bool(path: Path, obj: dict[str, Any], key: str, label: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        fail(relative(path), f"{label}.{key} must be a boolean")
    return value


def require_list(path: Path, obj: dict[str, Any], key: str, label: str) -> list[Any]:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        fail(relative(path), f"{label}.{key} must be a non-empty array")
    return value


def string_block(values: list[Any]) -> str:
    parts: list[str] = []
    for value in values:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            parts.extend(str(item) for item in value.values())
    return " ".join(parts)


def load_reference_ids() -> dict[str, str]:
    refs: dict[str, str] = {}
    for key, (path, source_key) in REFERENCE_FILES.items():
        payload = require_object(path, load_json(path), key)
        refs[key] = require_string(path, payload, source_key, key)
    return refs


def validate_source_records(path: Path, records: list[Any]) -> None:
    if any(not isinstance(record, str) or not record for record in records):
        fail(relative(path), "source_records entries must be non-empty strings")
    present = set(records)
    missing = sorted(REQUIRED_SOURCE_RECORDS - present)
    if missing:
        fail(relative(path), "source_records is missing: " + ", ".join(missing))
    for record in records:
        if not (ROOT / record).exists():
            fail(relative(path), f"source record does not exist: {record}")


def validate_required_inputs(path: Path, inputs: list[Any]) -> None:
    names: set[str] = set()
    for item in inputs:
        obj = require_object(path, item, "required_inputs[]")
        name = require_string(path, obj, "input", "required_inputs[]")
        names.add(name)
        if not require_bool(path, obj, "required_for_real_analysis", "required_inputs[]"):
            fail(relative(path), f"{name}: required_for_real_analysis must be true")
        status = require_string(path, obj, "current_status", "required_inputs[]")
        if status not in {"not_generated", "contract_only", "not_reviewed"}:
            fail(relative(path), f"{name}: unsupported current_status {status!r}")
        missing_proof = require_string(path, obj, "missing_proof", "required_inputs[]")
        if "No " not in missing_proof and "no " not in missing_proof:
            fail(relative(path), f"{name}: missing_proof must describe absent evidence")
    missing = sorted(REQUIRED_INPUTS - names)
    if missing:
        fail(relative(path), "required_inputs is missing: " + ", ".join(missing))


def validate_methods(path: Path, methods: list[Any]) -> None:
    ids: set[str] = set()
    for item in methods:
        obj = require_object(path, item, "statistical_methods[]")
        method_id = require_string(path, obj, "id", "statistical_methods[]")
        if method_id in ids:
            fail(relative(path), f"duplicate statistical method id: {method_id}")
        ids.add(method_id)
        require_string(path, obj, "method", "statistical_methods[]")
        if not require_bool(path, obj, "required_for_claim", "statistical_methods[]"):
            fail(relative(path), f"{method_id}: required_for_claim must be true")
        if require_string(path, obj, "current_status", "statistical_methods[]") != "not_generated":
            fail(relative(path), f"{method_id}: current_status must be not_generated")
        missing_proof = require_string(path, obj, "missing_proof", "statistical_methods[]")
        if "No " not in missing_proof and "no " not in missing_proof:
            fail(relative(path), f"{method_id}: missing_proof must describe absent evidence")
    missing = sorted(REQUIRED_METHOD_IDS - ids)
    if missing:
        fail(relative(path), "statistical_methods is missing: " + ", ".join(missing))


def validate_metric_families(path: Path, metrics: list[Any]) -> None:
    ids: set[str] = set()
    for item in metrics:
        obj = require_object(path, item, "metric_families[]")
        metric_id = require_string(path, obj, "id", "metric_families[]")
        if metric_id in ids:
            fail(relative(path), f"duplicate metric family id: {metric_id}")
        ids.add(metric_id)
        summaries = require_list(path, obj, "required_summaries", "metric_families[]")
        if any(not isinstance(summary, str) or not summary for summary in summaries):
            fail(relative(path), f"{metric_id}: required_summaries entries must be strings")
        units = require_list(path, obj, "units", "metric_families[]")
        if any(not isinstance(unit, str) or not unit for unit in units):
            fail(relative(path), f"{metric_id}: units entries must be strings")
        policy = require_string(path, obj, "failure_policy", "metric_families[]")
        for term in ("failure", "denominator"):
            if term not in policy.lower():
                fail(relative(path), f"{metric_id}: failure_policy must mention {term}")
    missing = sorted(REQUIRED_METRIC_IDS - ids)
    if missing:
        fail(relative(path), "metric_families is missing: " + ", ".join(missing))


def validate_rejection_rules(path: Path, rules: list[Any]) -> None:
    ids: set[str] = set()
    block = string_block(rules)
    for item in rules:
        obj = require_object(path, item, "rejection_rules[]")
        rule_id = require_string(path, obj, "id", "rejection_rules[]")
        if rule_id in ids:
            fail(relative(path), f"duplicate rejection rule id: {rule_id}")
        ids.add(rule_id)
        require_string(path, obj, "condition", "rejection_rules[]")
        outcome = require_string(path, obj, "outcome", "rejection_rules[]")
        if "Reject" not in outcome:
            fail(relative(path), f"{rule_id}: outcome must reject unsupported claims")
    for term in [
        "raw samples",
        "confidence interval",
        "denominator",
        "security setting",
        "validation",
        "Chrome-class",
    ]:
        if term not in block:
            fail(relative(path), f"rejection_rules must mention {term}")


def validate_terms(path: Path, key: str, values: list[Any]) -> None:
    block = string_block(values)
    missing = [term for term in TERM_REQUIREMENTS[key] if term not in block]
    if missing:
        fail(relative(path), f"{key} is missing terms: {', '.join(missing)}")


def validate_plan(path: Path) -> None:
    schema = load_json(MACHINE / "benchmark-statistics-analysis.schema.json")
    if not isinstance(schema, dict) or schema.get("title") != (
        "Turing benchmark statistics-analysis contract"
    ):
        fail(relative(MACHINE / "benchmark-statistics-analysis.schema.json"), "unexpected schema title")

    data = require_object(path, load_json(path), "statistics-analysis plan")
    if data.get("schema_version") != 1:
        fail(relative(path), "schema_version must be 1")
    analysis_id = require_string(path, data, "analysis_id", "statistics-analysis plan")
    if not ANALYSIS_ID.fullmatch(analysis_id):
        fail(relative(path), f"invalid analysis_id: {analysis_id!r}")
    if data.get("status") != "no_claim_statistics_analysis_contract":
        fail(relative(path), "status must be no_claim_statistics_analysis_contract")
    if data.get("evidence_id") != "PB13-EV-006":
        fail(relative(path), "evidence_id must be PB13-EV-006")
    if data.get("task") != "TASK-000005":
        fail(relative(path), "task must be TASK-000005")

    claim_status = require_string(path, data, "claim_status", "statistics-analysis plan")
    missing_claims = [
        phrase for phrase in REQUIRED_CLAIM_PHRASES if phrase not in claim_status
    ]
    if missing_claims:
        fail(relative(path), "claim_status is missing: " + ", ".join(missing_claims))

    refs = load_reference_ids()
    registry = require_object(path, data.get("registry_references"), "registry_references")
    for key, expected in refs.items():
        if registry.get(key) != expected:
            fail(relative(path), f"registry_references.{key} must be {expected}")

    scope = require_object(path, data.get("analysis_scope"), "analysis_scope")
    if require_string(path, scope, "level", "analysis_scope") != "contract_only_no_result":
        fail(relative(path), "analysis_scope.level must be contract_only_no_result")
    for key, expected in {
        "actual_samples_present": False,
        "statistical_summary_present": False,
        "claim_supported": False,
        "future_runner_required": True,
        "owner_review_required": True,
    }.items():
        if require_bool(path, scope, key, "analysis_scope") is not expected:
            fail(relative(path), f"analysis_scope.{key} must be {expected}")

    validate_source_records(path, require_list(path, data, "source_records", "statistics-analysis plan"))
    validate_required_inputs(path, require_list(path, data, "required_inputs", "statistics-analysis plan"))
    sample_controls = require_list(path, data, "sample_design_controls", "statistics-analysis plan")
    validate_terms(path, "sample_design_controls", sample_controls)
    validate_methods(path, require_list(path, data, "statistical_methods", "statistics-analysis plan"))
    validate_metric_families(path, require_list(path, data, "metric_families", "statistics-analysis plan"))
    denominator_controls = require_list(path, data, "denominator_controls", "statistics-analysis plan")
    validate_terms(path, "denominator_controls", denominator_controls)
    validate_rejection_rules(path, require_list(path, data, "rejection_rules", "statistics-analysis plan"))
    unsupported = require_list(path, data, "unsupported_behavior", "statistics-analysis plan")
    validate_terms(path, "unsupported_behavior", unsupported)

    commands = require_list(path, data, "validation_commands", "statistics-analysis plan")
    missing_commands = [command for command in REQUIRED_VALIDATION_COMMANDS if command not in commands]
    if missing_commands:
        fail(relative(path), "validation_commands is missing: " + ", ".join(missing_commands))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, default=[DEFAULT_PLAN])
    args = parser.parse_args(argv)

    try:
        for path in args.paths:
            validate_plan(path)
    except ValidationError as error:
        print(f"benchmark statistics-analysis validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "benchmark statistics-analysis validation passed: "
        f"{len(args.paths)} no-claim contract(s), {len(REQUIRED_METHOD_IDS)} method controls, "
        f"{len(REQUIRED_METRIC_IDS)} metric families"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
