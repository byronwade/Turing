#!/usr/bin/env python3
"""Validate no-claim benchmark launch-runner contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
DEFAULT_MANIFEST = (
    MACHINE
    / "benchmark-launch-runners"
    / "no-claim-browser-launch.plan.json"
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
ARTIFACT_PACKAGE = (
    MACHINE / "benchmark-artifact-packages" / "no-claim-trace-package.plan.json"
)
BROWSER_PIN_CAPTURE = (
    MACHINE / "benchmark-browser-pin-captures" / "current-windows-high-end.no-claim.plan.json"
)
BROWSER_PIN_DIAGNOSTIC = (
    MACHINE
    / "benchmark-browser-pin-diagnostics"
    / "current-windows-high-end.chrome-edge.no-claim.2026-07.json"
)
COMPETITOR_VERSIONS = (
    MACHINE
    / "benchmark-competitor-versions"
    / "current-desktop-release-candidates.2026-07.json"
)
COMPETITOR_LOCAL_INSTALLS = (
    MACHINE
    / "benchmark-competitor-local-installs"
    / "current-windows-high-end.candidate.json"
)

LAUNCH_RUNNER_ID = re.compile(r"^TURING\.BENCHMARK\.LAUNCH_RUNNER\.[A-Z0-9._-]+$")
STAGE_ID = re.compile(r"^PB13-LAUNCH-STAGE-[A-Z0-9._-]+$")
STATUS_VALUES = {"contract_only_no_browser_benchmark", "draft", "reviewed"}
REQUIRED_STAGES = {
    "PB13-LAUNCH-STAGE-PREFLIGHT-REGISTRIES",
    "PB13-LAUNCH-STAGE-SERVER-START",
    "PB13-LAUNCH-STAGE-BROWSER-PIN-RESOLVE",
    "PB13-LAUNCH-STAGE-TEMP-PROFILE-CREATE",
    "PB13-LAUNCH-STAGE-CACHE-RESET",
    "PB13-LAUNCH-STAGE-TRACE-START",
    "PB13-LAUNCH-STAGE-BROWSER-LAUNCH",
    "PB13-LAUNCH-STAGE-WARMUP",
    "PB13-LAUNCH-STAGE-MEASURED-SAMPLE",
    "PB13-LAUNCH-STAGE-ARTIFACT-FINALIZE",
    "PB13-LAUNCH-STAGE-CLEANUP",
    "PB13-LAUNCH-STAGE-CLAIM-BLOCK",
}
REQUIRED_ARGUMENTS = {
    "--hardware-id",
    "--os-control-id",
    "--corpus-id",
    "--network-profile-id",
    "--browser-pin-id",
    "--tab-scenario-set-id",
    "--artifact-root",
    "--claim-mode",
}
FORBIDDEN_ARGUMENTS = {
    "--use-default-profile",
    "--allow-real-profile",
    "--skip-failures",
    "--ignore-timeouts",
    "--disable-sandbox-for-benchmark",
    "--allow-network-downloads",
    "--claim",
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


def require_int(path: Path, obj: dict[str, object], key: str, label: str) -> int:
    value = obj.get(key)
    if type(value) is not int or value < 1:
        fail(path, f"{label}.{key} must be a positive integer")
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
        "artifact_package_id": (ARTIFACT_PACKAGE, "package_id"),
        "browser_pin_capture_plan_id": (BROWSER_PIN_CAPTURE, "capture_plan_id"),
        "browser_pin_diagnostic_id": (BROWSER_PIN_DIAGNOSTIC, "diagnostic_id"),
        "competitor_version_manifest_id": (
            COMPETITOR_VERSIONS,
            "competitor_version_manifest_id",
        ),
        "competitor_local_install_manifest_id": (
            COMPETITOR_LOCAL_INSTALLS,
            "local_install_manifest_id",
        ),
    }
    loaded: dict[str, str] = {}
    for output_key, (path, source_key) in references.items():
        payload = require_object(path, load_json(path), output_key)
        loaded[output_key] = require_string(path, payload, source_key, output_key)
    return loaded


def validate_command_contract(path: Path, value: object) -> None:
    contract = require_object(path, value, "command_contract")
    required = {
        "planned_runner_path",
        "planned_modes",
        "required_arguments",
        "forbidden_arguments",
        "self_test_status",
    }
    reject_extra(path, contract, required, "command_contract")
    require_keys(path, contract, required, "command_contract")
    planned_path = require_string(
        path, contract, "planned_runner_path", "command_contract"
    )
    if planned_path != "tools/run_benchmark_browser_launch.py":
        fail(path, "planned_runner_path must name the future browser-launch runner")
    modes = set(require_string_array(path, contract, "planned_modes", "command_contract"))
    for mode in {"validate-contract", "future-local-browser-pipeline"}:
        if mode not in modes:
            fail(path, f"planned_modes must include {mode}")

    args = contract.get("required_arguments")
    if not isinstance(args, list):
        fail(path, "command_contract.required_arguments must be an array")
    seen_args: set[str] = set()
    for index, item in enumerate(args, start=1):
        arg = require_object(path, item, f"required_arguments[{index}]")
        allowed = {"name", "required_for_real_run", "purpose"}
        reject_extra(path, arg, allowed, f"required_arguments[{index}]")
        require_keys(path, arg, allowed, f"required_arguments[{index}]")
        name = require_string(path, arg, "name", f"required_arguments[{index}]")
        seen_args.add(name)
        if not require_bool(
            path, arg, "required_for_real_run", f"required_arguments[{index}]"
        ):
            fail(path, f"{name} must be required_for_real_run")
        require_string(path, arg, "purpose", f"required_arguments[{index}]")
    missing_args = sorted(REQUIRED_ARGUMENTS - seen_args)
    if missing_args:
        fail(path, "command_contract.required_arguments is missing: " + ", ".join(missing_args))

    forbidden = set(
        require_string_array(path, contract, "forbidden_arguments", "command_contract")
    )
    missing_forbidden = sorted(FORBIDDEN_ARGUMENTS - forbidden)
    if missing_forbidden:
        fail(path, "command_contract.forbidden_arguments is missing: " + ", ".join(missing_forbidden))
    self_test = require_string(path, contract, "self_test_status", "command_contract")
    for phrase in [
        "tools/run_benchmark_browser_launch.py --self-test",
        "command parsing",
        "forbidden arguments",
        "checked registry references",
        "artifact-root handling",
        "no-claim finalization",
        "launching no browser",
        "producing no benchmark result",
    ]:
        if phrase not in self_test:
            fail(path, f"self_test_status must mention: {phrase}")


def validate_registry_references(path: Path, value: object) -> None:
    references = load_reference_ids()
    registry = require_object(path, value, "registry_references")
    reject_extra(path, registry, set(references), "registry_references")
    require_keys(path, registry, set(references), "registry_references")
    for key, expected in references.items():
        if require_string(path, registry, key, "registry_references") != expected:
            fail(path, f"registry_references.{key} must match checked no-claim registry")


def validate_target_policy(path: Path, value: object) -> None:
    policy = require_object(path, value, "target_policy")
    required = {
        "browser_launch_allowed_in_this_record",
        "target_resolution",
        "profile_boundary",
        "network_boundary",
        "comparison_boundary",
    }
    reject_extra(path, policy, required, "target_policy")
    require_keys(path, policy, required, "target_policy")
    if require_bool(path, policy, "browser_launch_allowed_in_this_record", "target_policy"):
        fail(path, "target_policy.browser_launch_allowed_in_this_record must be false")
    for key in (
        "target_resolution",
        "profile_boundary",
        "network_boundary",
        "comparison_boundary",
    ):
        require_string(path, policy, key, "target_policy")
    if "must not read or write real user profiles" not in policy["profile_boundary"]:
        fail(path, "target_policy.profile_boundary must prohibit real profile access")


def validate_stage_contract(path: Path, value: object) -> None:
    if not isinstance(value, list):
        fail(path, "stage_contract must be an array")
    seen: set[str] = set()
    for index, item in enumerate(value, start=1):
        stage = require_object(path, item, f"stage_contract[{index}]")
        required = {
            "stage_id",
            "name",
            "status",
            "required_for_real_run",
            "inputs",
            "outputs",
            "failure_policy",
        }
        reject_extra(path, stage, required, f"stage_contract[{index}]")
        require_keys(path, stage, required, f"stage_contract[{index}]")
        stage_id = require_string(path, stage, "stage_id", f"stage_contract[{index}]")
        if not STAGE_ID.fullmatch(stage_id):
            fail(path, f"invalid stage_id: {stage_id}")
        if stage_id in seen:
            fail(path, f"duplicate stage_id: {stage_id}")
        seen.add(stage_id)
        if require_string(path, stage, "status", f"stage_contract[{index}]") != (
            "contract_only_not_implemented"
        ):
            fail(path, "current launch stages must remain contract-only")
        if not require_bool(
            path, stage, "required_for_real_run", f"stage_contract[{index}]"
        ):
            fail(path, f"{stage_id} must be required_for_real_run")
        require_string(path, stage, "name", f"stage_contract[{index}]")
        require_string_array(path, stage, "inputs", f"stage_contract[{index}]")
        require_string_array(path, stage, "outputs", f"stage_contract[{index}]")
        require_string(path, stage, "failure_policy", f"stage_contract[{index}]")
    missing = sorted(REQUIRED_STAGES - seen)
    if missing:
        fail(path, "stage_contract is missing: " + ", ".join(missing))


def validate_sample_control(path: Path, value: object) -> None:
    control = require_object(path, value, "sample_control")
    required = {
        "minimum_repetitions_for_real_run",
        "warmup_policy",
        "randomization_policy",
        "denominator_policy",
        "result_label",
        "measurement_claim_allowed",
    }
    reject_extra(path, control, required, "sample_control")
    require_keys(path, control, required, "sample_control")
    if require_int(path, control, "minimum_repetitions_for_real_run", "sample_control") < 5:
        fail(path, "minimum_repetitions_for_real_run must be at least 5")
    if require_bool(path, control, "measurement_claim_allowed", "sample_control"):
        fail(path, "sample_control.measurement_claim_allowed must be false")
    denominator = require_string(path, control, "denominator_policy", "sample_control")
    for phrase in ["failed", "unsupported", "timed-out", "cancelled", "crashed"]:
        if phrase not in denominator:
            fail(path, f"denominator_policy must mention {phrase}")
    for key in ("warmup_policy", "randomization_policy", "result_label"):
        require_string(path, control, key, "sample_control")


def validate_bool_policy(path: Path, value: object, label: str, required: set[str]) -> dict[str, object]:
    policy = require_object(path, value, label)
    reject_extra(path, policy, required, label)
    require_keys(path, policy, required, label)
    return policy


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "launch_runner_id",
        "status",
        "created_at",
        "claim_status",
        "command_contract",
        "registry_references",
        "target_policy",
        "stage_contract",
        "sample_control",
        "cache_profile_policy",
        "timeout_cancellation_policy",
        "failure_finalization_policy",
        "trace_artifact_policy",
        "resource_attribution_policy",
        "unsupported_behavior",
        "evidence_required",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    launch_runner_id = require_string(path, manifest, "launch_runner_id", "manifest")
    if not LAUNCH_RUNNER_ID.fullmatch(launch_runner_id):
        fail(path, f"launch_runner_id has invalid format: {launch_runner_id}")
    status = require_string(path, manifest, "status", "manifest")
    if status not in STATUS_VALUES:
        fail(path, f"status is not allowed: {status}")
    if status != "contract_only_no_browser_benchmark":
        fail(path, "current launch runner contract must remain contract-only")
    require_string(path, manifest, "created_at", "manifest")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in [
        "no browser benchmark run",
        "no benchmark result",
        "no trace captured",
        "no raw sample",
        "no Chrome-class claim",
        "no performance claim",
    ]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")

    validate_command_contract(path, manifest.get("command_contract"))
    validate_registry_references(path, manifest.get("registry_references"))
    validate_target_policy(path, manifest.get("target_policy"))
    validate_stage_contract(path, manifest.get("stage_contract"))
    validate_sample_control(path, manifest.get("sample_control"))

    cache_policy = validate_bool_policy(
        path,
        manifest.get("cache_profile_policy"),
        "cache_profile_policy",
        {
            "temporary_profile_required",
            "real_profile_access_allowed",
            "cache_reset_required",
            "cookie_storage_policy",
            "extension_policy",
            "account_sync_policy",
            "cleanup_required",
        },
    )
    for key in ("temporary_profile_required", "cache_reset_required", "cleanup_required"):
        if not require_bool(path, cache_policy, key, "cache_profile_policy"):
            fail(path, f"cache_profile_policy.{key} must be true")
    if require_bool(path, cache_policy, "real_profile_access_allowed", "cache_profile_policy"):
        fail(path, "cache_profile_policy.real_profile_access_allowed must be false")
    for key in ("cookie_storage_policy", "extension_policy", "account_sync_policy"):
        require_string(path, cache_policy, key, "cache_profile_policy")

    timeout_policy = validate_bool_policy(
        path,
        manifest.get("timeout_cancellation_policy"),
        "timeout_cancellation_policy",
        {
            "global_timeout_seconds",
            "per_stage_timeout_seconds",
            "cancellation_records_required",
            "cleanup_on_timeout_required",
        },
    )
    require_int(path, timeout_policy, "global_timeout_seconds", "timeout_cancellation_policy")
    require_int(path, timeout_policy, "per_stage_timeout_seconds", "timeout_cancellation_policy")
    for key in ("cancellation_records_required", "cleanup_on_timeout_required"):
        if not require_bool(path, timeout_policy, key, "timeout_cancellation_policy"):
            fail(path, f"timeout_cancellation_policy.{key} must be true")

    failure_policy = validate_bool_policy(
        path,
        manifest.get("failure_finalization_policy"),
        "failure_finalization_policy",
        {
            "failures_in_denominator",
            "unsupported_in_denominator",
            "crash_records_required",
            "partial_artifact_required",
            "result_finalization_required",
        },
    )
    for key in failure_policy:
        if not require_bool(path, failure_policy, key, "failure_finalization_policy"):
            fail(path, f"failure_finalization_policy.{key} must be true")

    trace_policy = validate_bool_policy(
        path,
        manifest.get("trace_artifact_policy"),
        "trace_artifact_policy",
        {
            "artifact_package_required",
            "trace_capture_required",
            "sha256_manifest_required",
            "redaction_review_required",
            "retention_decision_required",
        },
    )
    for key in trace_policy:
        if not require_bool(path, trace_policy, key, "trace_artifact_policy"):
            fail(path, f"trace_artifact_policy.{key} must be true")

    attribution_policy = validate_bool_policy(
        path,
        manifest.get("resource_attribution_policy"),
        "resource_attribution_policy",
        {
            "semantic_owner_required",
            "unknown_bucket_policy",
            "shared_resource_policy",
            "gpu_accounting_required",
        },
    )
    for key in ("semantic_owner_required", "gpu_accounting_required"):
        if not require_bool(path, attribution_policy, key, "resource_attribution_policy"):
            fail(path, f"resource_attribution_policy.{key} must be true")
    for key in ("unknown_bucket_policy", "shared_resource_policy"):
        require_string(path, attribution_policy, key, "resource_attribution_policy")

    unsupported = require_string_array(path, manifest, "unsupported_behavior", "manifest")
    for phrase in [
        "no browser benchmark launch implementation exists beyond the checked no-browser self-test",
        "no browser benchmark run was executed",
        "no browser was launched",
        "no trace",
        "no competitor comparison",
    ]:
        if not any(phrase in item for item in unsupported):
            fail(path, f"unsupported_behavior must mention: {phrase}")
    evidence_required = require_string_array(path, manifest, "evidence_required", "manifest")
    for phrase in [
        "implemented browser benchmark launch runner beyond the checked no-browser self-test",
        "runner-managed local server artifact",
        "owner-reviewed benchmark-ready browser pins",
        "trace and artifact package generated by a real run",
        "raw result manifest",
        "negative tests",
    ]:
        if not any(phrase in item for item in evidence_required):
            fail(path, f"evidence_required must mention: {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_MANIFEST]
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark launch runner validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark launch runner validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
