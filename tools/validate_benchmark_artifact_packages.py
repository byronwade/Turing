#!/usr/bin/env python3
"""Validate no-claim benchmark artifact-package contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
DEFAULT_MANIFEST = (
    MACHINE
    / "benchmark-artifact-packages"
    / "no-claim-trace-package.plan.json"
)
HARDWARE = MACHINE / "benchmark-hardware" / "current-windows-high-end.candidate.json"
OS_CONTROL = (
    MACHINE / "benchmark-os-controls" / "current-windows-high-end.candidate.json"
)
CORPUS = MACHINE / "benchmark-corpora" / "no-claim-smoke.corpus.json"
NETWORK_PROFILE = (
    MACHINE / "benchmark-network-profiles" / "no-claim-local-static.profile.json"
)
RESOURCE_ATTRIBUTION = (
    MACHINE / "benchmark-resource-attribution" / "semantic-owners.v1.json"
)
TAB_SCENARIOS = (
    MACHINE / "benchmark-tab-scenarios" / "no-claim-30-tab-smoke.scenarios.json"
)
SMOKE_MANIFEST = MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.sample.json"
RAW_ARTIFACT_INDEX = (
    MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.raw-artifacts.json"
)

PACKAGE_ID = re.compile(r"^TURING\.BENCHMARK\.ARTIFACT_PACKAGE\.[A-Z0-9._-]+$")
TRACE_ID = re.compile(r"^PB13-TRACE-[A-Z0-9._-]+$")
STATUS_VALUES = {"sample_only_no_benchmark_result", "draft", "reviewed"}
TRACE_KINDS = {
    "trace-etw",
    "trace-perfetto",
    "trace-semantic-resource",
    "trace-tab-lifecycle",
}
ARTIFACT_KINDS = {
    "environment-manifest",
    "benchmark-manifest",
    "trace-etw",
    "trace-perfetto",
    "runner-log",
    "browser-stdout-stderr",
    "screenshot",
    "video",
    "raw-samples",
    "memory-snapshot",
    "power-energy-sample",
    "cpu-gpu-counter",
    "failure-record",
    "artifact-index",
    "hashes",
    "profile-self-test",
    "server-run-evidence",
    "tab-lifecycle-log",
}
ARTIFACT_STATUSES = {"not_generated", "sample_placeholder", "generated"}
REQUIRED_ARTIFACT_KINDS = {
    "environment-manifest",
    "benchmark-manifest",
    "trace-etw",
    "trace-perfetto",
    "runner-log",
    "browser-stdout-stderr",
    "screenshot",
    "raw-samples",
    "memory-snapshot",
    "power-energy-sample",
    "failure-record",
    "artifact-index",
    "tab-lifecycle-log",
}


class ValidationError(ValueError):
    pass


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(path: Path, message: str) -> None:
    raise ValidationError(f"{relative(path)}: {message}")


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(path, f"invalid JSON: {error}")


def require_object(path: Path, value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(path, f"{label} must be an object")
    return value


def reject_extra(
    path: Path, obj: dict[str, object], allowed: set[str], label: str
) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(
    path: Path, obj: dict[str, object], required: set[str], label: str
) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_bool(path: Path, obj: dict[str, object], key: str, label: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        fail(path, f"{label}.{key} must be a boolean")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        fail(path, f"{label}.{key} must be a non-empty array")
    if any(not isinstance(item, str) or not item for item in value):
        fail(path, f"{label}.{key} entries must be non-empty strings")
    return value


def load_reference_ids() -> dict[str, str]:
    references = {
        "hardware_id": (HARDWARE, "hardware_id"),
        "os_control_id": (OS_CONTROL, "os_control_id"),
        "corpus_id": (CORPUS, "corpus_id"),
        "network_profile_id": (NETWORK_PROFILE, "profile_id"),
        "resource_attribution_id": (RESOURCE_ATTRIBUTION, "resource_attribution_id"),
        "tab_scenario_set_id": (TAB_SCENARIOS, "scenario_set_id"),
        "benchmark_manifest_id": (SMOKE_MANIFEST, "benchmark_id"),
        "raw_artifact_index_id": (RAW_ARTIFACT_INDEX, "artifact_id"),
    }
    loaded: dict[str, str] = {}
    for output_key, (path, source_key) in references.items():
        payload = require_object(path, load_json(path), output_key)
        loaded[output_key] = require_string(path, payload, source_key, output_key)
    return loaded


def validate_package_root(path: Path, value: object) -> None:
    policy = require_object(path, value, "package_root_policy")
    required = {
        "root_kind",
        "source_tree_policy",
        "cleanup_required",
        "prohibit_real_profiles",
        "path_redaction",
    }
    reject_extra(path, policy, required, "package_root_policy")
    require_keys(path, policy, required, "package_root_policy")
    if require_string(path, policy, "root_kind", "package_root_policy") != (
        "runner_managed_temporary_or_external_artifact_root"
    ):
        fail(path, "package_root_policy.root_kind must use a runner-owned root")
    for key in ("source_tree_policy", "path_redaction"):
        require_string(path, policy, key, "package_root_policy")
    if not require_bool(path, policy, "cleanup_required", "package_root_policy"):
        fail(path, "package_root_policy.cleanup_required must be true")
    if not require_bool(path, policy, "prohibit_real_profiles", "package_root_policy"):
        fail(path, "package_root_policy.prohibit_real_profiles must be true")


def validate_trace(path: Path, value: object, seen: set[str]) -> str:
    trace = require_object(path, value, "trace_capture[]")
    required = {
        "trace_id",
        "trace_kind",
        "platform",
        "status",
        "tool",
        "output_extensions",
        "required_for_real_run",
        "redaction_boundary",
        "missing_proof",
    }
    reject_extra(path, trace, required, "trace_capture[]")
    require_keys(path, trace, required, "trace_capture[]")
    trace_id = require_string(path, trace, "trace_id", "trace_capture[]")
    if not TRACE_ID.fullmatch(trace_id):
        fail(path, f"trace_id has invalid format: {trace_id}")
    if trace_id in seen:
        fail(path, f"duplicate trace_id: {trace_id}")
    seen.add(trace_id)
    kind = require_string(path, trace, "trace_kind", "trace_capture[]")
    if kind not in TRACE_KINDS:
        fail(path, f"trace_kind is not allowed: {kind}")
    if require_string(path, trace, "status", "trace_capture[]") != "not_generated":
        fail(path, "current trace_capture entries must remain not_generated")
    require_string(path, trace, "platform", "trace_capture[]")
    require_string(path, trace, "tool", "trace_capture[]")
    require_string_array(path, trace, "output_extensions", "trace_capture[]")
    if not require_bool(path, trace, "required_for_real_run", "trace_capture[]"):
        fail(path, "trace_capture[].required_for_real_run must be true")
    require_string(path, trace, "redaction_boundary", "trace_capture[]")
    missing = require_string(path, trace, "missing_proof", "trace_capture[]")
    if "No " not in missing and "no " not in missing:
        fail(path, "trace_capture[].missing_proof must describe absent evidence")
    return kind


def validate_artifact_class(path: Path, value: object) -> str:
    artifact = require_object(path, value, "artifact_classes[]")
    required = {
        "kind",
        "status",
        "required_for_real_run",
        "producer",
        "path_policy",
        "hash_required",
        "redaction",
        "retention",
        "missing_proof",
    }
    reject_extra(path, artifact, required, "artifact_classes[]")
    require_keys(path, artifact, required, "artifact_classes[]")
    kind = require_string(path, artifact, "kind", "artifact_classes[]")
    if kind not in ARTIFACT_KINDS:
        fail(path, f"artifact kind is not allowed: {kind}")
    status = require_string(path, artifact, "status", "artifact_classes[]")
    if status not in ARTIFACT_STATUSES:
        fail(path, f"artifact status is not allowed: {status}")
    if status == "generated":
        fail(path, "current artifact package contract must not mark artifacts generated")
    if not require_bool(path, artifact, "required_for_real_run", "artifact_classes[]"):
        fail(path, "artifact_classes[].required_for_real_run must be true")
    if not require_bool(path, artifact, "hash_required", "artifact_classes[]"):
        fail(path, "artifact_classes[].hash_required must be true")
    for key in ("producer", "path_policy", "redaction", "retention", "missing_proof"):
        require_string(path, artifact, key, "artifact_classes[]")
    return kind


def validate_manifest(path: Path, payload: object) -> None:
    references = load_reference_ids()
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "package_id",
        "status",
        "created_at",
        "claim_status",
        "benchmark_manifest_id",
        "raw_artifact_index_id",
        "hardware_id",
        "os_control_id",
        "corpus_id",
        "network_profile_id",
        "resource_attribution_id",
        "tab_scenario_set_id",
        "package_root_policy",
        "trace_capture",
        "artifact_classes",
        "required_manifest_records",
        "prohibited_content",
        "unsupported_behavior",
        "missing_proof",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    package_id = require_string(path, manifest, "package_id", "manifest")
    if not PACKAGE_ID.fullmatch(package_id):
        fail(path, f"package_id has invalid format: {package_id}")
    if require_string(path, manifest, "status", "manifest") not in STATUS_VALUES:
        fail(path, "status is not allowed")
    if manifest.get("status") != "sample_only_no_benchmark_result":
        fail(path, "current artifact package contract must remain sample-only")
    require_string(path, manifest, "created_at", "manifest")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in [
        "no browser run",
        "no benchmark result",
        "no trace captured",
        "no Chrome-class claim",
        "no performance claim",
    ]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    for key, expected in references.items():
        if require_string(path, manifest, key, "manifest") != expected:
            fail(path, f"manifest.{key} must match checked no-claim registry")

    validate_package_root(path, manifest.get("package_root_policy"))

    traces = manifest.get("trace_capture")
    if not isinstance(traces, list):
        fail(path, "trace_capture must be an array")
    seen_traces: set[str] = set()
    trace_kinds = {
        validate_trace(path, item, seen_traces)
        for item in traces
    }
    for required_kind in {"trace-etw", "trace-perfetto", "trace-tab-lifecycle"}:
        if required_kind not in trace_kinds:
            fail(path, f"trace_capture must include {required_kind}")

    artifacts = manifest.get("artifact_classes")
    if not isinstance(artifacts, list):
        fail(path, "artifact_classes must be an array")
    artifact_kinds = [validate_artifact_class(path, item) for item in artifacts]
    duplicates = sorted({kind for kind in artifact_kinds if artifact_kinds.count(kind) > 1})
    if duplicates:
        fail(path, "duplicate artifact class kinds: " + ", ".join(duplicates))
    missing_kinds = sorted(REQUIRED_ARTIFACT_KINDS - set(artifact_kinds))
    if missing_kinds:
        fail(path, "artifact_classes is missing: " + ", ".join(missing_kinds))

    records = require_string_array(
        path, manifest, "required_manifest_records", "manifest"
    )
    for phrase in ["SHA-256", "failure", "unsupported", "tab_scenario_set_id"]:
        if not any(phrase in item for item in records):
            fail(path, f"required_manifest_records must mention: {phrase}")
    prohibited = require_string_array(path, manifest, "prohibited_content", "manifest")
    for phrase in ["secrets", "real user profile", "private page content"]:
        if not any(phrase in item for item in prohibited):
            fail(path, f"prohibited_content must mention: {phrase}")
    unsupported = require_string_array(
        path, manifest, "unsupported_behavior", "manifest"
    )
    for phrase in [
        "no browser was launched",
        "no benchmark result exists",
        "no ETW",
        "no raw sample file",
        "no Chrome-class",
    ]:
        if not any(phrase in item for item in unsupported):
            fail(path, f"unsupported_behavior must mention: {phrase}")
    missing_proof = require_string_array(path, manifest, "missing_proof", "manifest")
    for phrase in [
        "runner-generated trace and artifact package root",
        "ETW or equivalent Windows trace",
        "raw samples",
        "30-tab lifecycle log",
        "owner-reviewed",
    ]:
        if not any(phrase in item for item in missing_proof):
            fail(path, f"missing_proof must mention: {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_MANIFEST]
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark artifact package validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark artifact package validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
