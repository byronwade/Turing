#!/usr/bin/env python3
"""Validate benchmark manifest fixtures without third-party packages."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARDWARE_MANIFEST_DIR = ROOT / "docs" / "blueprint-v1" / "machine" / "benchmark-hardware"
OS_CONTROL_MANIFEST_DIR = ROOT / "docs" / "blueprint-v1" / "machine" / "benchmark-os-controls"
RESOURCE_ATTRIBUTION_MANIFEST_DIR = (
    ROOT / "docs" / "blueprint-v1" / "machine" / "benchmark-resource-attribution"
)
DEFAULT_MANIFESTS = [
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "benchmark-manifests"
    / "no-claim-runner-smoke.sample.json"
]

BENCHMARK_ID = re.compile(r"^[A-Z0-9][A-Z0-9._-]+$")
HARDWARE_ID = re.compile(r"^TURING\.BENCHMARK\.HARDWARE\.[A-Z0-9._-]+$")
OS_CONTROL_ID = re.compile(r"^TURING\.BENCHMARK\.OS_CONTROL\.[A-Z0-9._-]+$")
RESOURCE_ATTRIBUTION_ID = re.compile(
    r"^TURING\.BENCHMARK\.RESOURCE_ATTRIBUTION\.[A-Z0-9._-]+$"
)
SHA256 = re.compile(r"^[a-f0-9]{64}$")
STATES = [
    "active",
    "background",
    "throttled",
    "frozen",
    "serialized",
    "discarded",
    "crashed",
]


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


def require_string(
    path: Path, obj: dict[str, object], key: str, label: str, *, non_empty: bool = True
) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or (non_empty and not value):
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_bool(path: Path, obj: dict[str, object], key: str, label: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        fail(path, f"{label}.{key} must be a boolean")
    return value


def require_int(
    path: Path, obj: dict[str, object], key: str, label: str, *, minimum: int = 0
) -> int:
    value = obj.get(key)
    if type(value) is not int or value < minimum:
        fail(path, f"{label}.{key} must be an integer >= {minimum}")
    return value


def require_number(
    path: Path, obj: dict[str, object], key: str, label: str, *, minimum: float = 0
) -> float:
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= minimum:
        fail(path, f"{label}.{key} must be a number > {minimum}")
    return float(value)


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(path, f"{label}.{key} must be an array of strings")
    return value


def load_hardware_registry() -> dict[str, dict[str, object]]:
    registry: dict[str, dict[str, object]] = {}
    for hardware_path in sorted(HARDWARE_MANIFEST_DIR.glob("*.json")):
        payload = require_object(
            hardware_path, load_json(hardware_path), "hardware manifest"
        )
        hardware_id = require_string(
            hardware_path, payload, "hardware_id", "hardware manifest"
        )
        if not HARDWARE_ID.fullmatch(hardware_id):
            fail(hardware_path, "hardware_id has invalid format")
        if hardware_id in registry:
            fail(hardware_path, f"duplicate hardware_id: {hardware_id}")
        registry[hardware_id] = payload
    return registry


def load_os_control_registry() -> dict[str, dict[str, object]]:
    registry: dict[str, dict[str, object]] = {}
    for control_path in sorted(OS_CONTROL_MANIFEST_DIR.glob("*.json")):
        payload = require_object(control_path, load_json(control_path), "OS-control manifest")
        control_id = require_string(control_path, payload, "os_control_id", "OS-control manifest")
        if not OS_CONTROL_ID.fullmatch(control_id):
            fail(control_path, "os_control_id has invalid format")
        if control_id in registry:
            fail(control_path, f"duplicate os_control_id: {control_id}")
        registry[control_id] = payload
    return registry


def load_resource_attribution_registry() -> dict[str, dict[str, object]]:
    registry: dict[str, dict[str, object]] = {}
    for resource_path in sorted(RESOURCE_ATTRIBUTION_MANIFEST_DIR.glob("*.json")):
        payload = require_object(
            resource_path, load_json(resource_path), "resource attribution manifest"
        )
        resource_id = require_string(
            resource_path, payload, "resource_attribution_id", "resource attribution manifest"
        )
        if not RESOURCE_ATTRIBUTION_ID.fullmatch(resource_id):
            fail(resource_path, "resource_attribution_id has invalid format")
        if resource_id in registry:
            fail(resource_path, f"duplicate resource_attribution_id: {resource_id}")
        registry[resource_id] = payload
    return registry


def validate_browser(path: Path, value: object) -> None:
    obj = require_object(path, value, "browser")
    required = {
        "name",
        "version",
        "commit",
        "channel",
        "build_profile",
        "arguments",
        "features",
    }
    reject_extra(path, obj, required, "browser")
    require_keys(path, obj, required, "browser")
    for key in ["name", "version", "commit", "channel", "build_profile"]:
        require_string(path, obj, key, "browser")
    require_string_array(path, obj, "arguments", "browser")
    features = require_object(path, obj.get("features"), "browser.features")
    for key, item in features.items():
        if not isinstance(key, str) or isinstance(item, (list, dict)):
            fail(path, "browser.features values must be string, number, boolean, or null")


def validate_environment_matches_hardware(
    path: Path,
    environment: dict[str, object],
    hardware: dict[str, object],
) -> None:
    cpu = require_object(path, hardware.get("cpu"), "hardware registry cpu")
    memory = require_object(path, hardware.get("memory"), "hardware registry memory")
    os_image = require_object(path, hardware.get("os_image"), "hardware registry os_image")
    power = require_object(
        path, hardware.get("power_thermal"), "hardware registry power_thermal"
    )
    gpus_value = hardware.get("gpus")
    if not isinstance(gpus_value, list) or not gpus_value:
        fail(path, "hardware registry gpus must be a non-empty array")

    if environment["cpu"] != require_string(path, cpu, "name", "hardware registry cpu"):
        fail(path, "environment.cpu does not match the hardware registry")
    if environment["logical_cores"] != require_int(
        path, cpu, "logical_processors", "hardware registry cpu", minimum=1
    ):
        fail(path, "environment.logical_cores does not match the hardware registry")
    if environment["memory_bytes"] != require_int(
        path, memory, "total_physical_bytes", "hardware registry memory", minimum=1
    ):
        fail(path, "environment.memory_bytes does not match the hardware registry")
    if environment["os"] != require_string(
        path, os_image, "caption", "hardware registry os_image"
    ):
        fail(path, "environment.os does not match the hardware registry")
    if environment["os_version"] != require_string(
        path, os_image, "version", "hardware registry os_image"
    ):
        fail(path, "environment.os_version does not match the hardware registry")
    if environment["power_mode"] != require_string(
        path, power, "active_power_scheme", "hardware registry power_thermal"
    ):
        fail(path, "environment.power_mode does not match the hardware registry")
    if environment["thermal_state"] != require_string(
        path, power, "thermal_state", "hardware registry power_thermal"
    ):
        fail(path, "environment.thermal_state does not match the hardware registry")

    matching_gpu = None
    for index, item in enumerate(gpus_value, start=1):
        gpu = require_object(path, item, f"hardware registry gpus[{index}]")
        if environment["gpu"] == require_string(
            path, gpu, "name", f"hardware registry gpus[{index}]"
        ):
            matching_gpu = gpu
            break
    if matching_gpu is None:
        fail(path, "environment.gpu does not match any hardware registry GPU")
    if "display_hz" in environment:
        refresh = require_int(
            path, matching_gpu, "current_refresh_hz", "hardware registry gpu", minimum=1
        )
        if float(environment["display_hz"]) != float(refresh):
            fail(path, "environment.display_hz does not match the hardware registry")


def validate_environment(
    path: Path,
    value: object,
    hardware_registry: dict[str, dict[str, object]],
    os_control_registry: dict[str, dict[str, object]],
) -> dict[str, object]:
    obj = require_object(path, value, "environment")
    required = {
        "hardware_id",
        "os_control_id",
        "cpu",
        "logical_cores",
        "memory_bytes",
        "gpu",
        "os",
        "os_version",
        "power_mode",
        "thermal_state",
    }
    optional = {"display_hz", "scale_factor"}
    reject_extra(path, obj, required | optional, "environment")
    require_keys(path, obj, required, "environment")
    for key in [
        "hardware_id",
        "os_control_id",
        "cpu",
        "gpu",
        "os",
        "os_version",
        "power_mode",
        "thermal_state",
    ]:
        require_string(path, obj, key, "environment")
    require_int(path, obj, "logical_cores", "environment", minimum=1)
    require_int(path, obj, "memory_bytes", "environment", minimum=1)
    for key in optional & set(obj):
        require_number(path, obj, key, "environment", minimum=0)
    hardware_id = str(obj["hardware_id"])
    if not HARDWARE_ID.fullmatch(hardware_id):
        fail(path, "environment.hardware_id has invalid format")
    hardware = hardware_registry.get(hardware_id)
    if hardware is None:
        fail(path, f"environment.hardware_id is not registered: {hardware_id}")
    validate_environment_matches_hardware(path, obj, hardware)
    os_control_id = str(obj["os_control_id"])
    if not OS_CONTROL_ID.fullmatch(os_control_id):
        fail(path, "environment.os_control_id has invalid format")
    os_control = os_control_registry.get(os_control_id)
    if os_control is None:
        fail(path, f"environment.os_control_id is not registered: {os_control_id}")
    if os_control.get("hardware_id") != hardware_id:
        fail(path, "environment.os_control_id does not belong to environment.hardware_id")
    return obj


def validate_tabs(path: Path, value: object) -> dict[str, int]:
    if not isinstance(value, list) or not value:
        fail(path, "workload.tabs must be a non-empty array")
    counts = {state: 0 for state in STATES}
    seen: set[str] = set()
    allowed = {
        "tab_id",
        "corpus_case",
        "top_level_site",
        "state",
        "site_instances",
        "renderer_process",
        "protected",
        "protection_reason",
        "revival_ms",
        "lost_state",
    }
    required = {
        "tab_id",
        "corpus_case",
        "top_level_site",
        "state",
        "site_instances",
        "renderer_process",
        "protected",
    }
    for index, item in enumerate(value, start=1):
        tab = require_object(path, item, f"workload.tabs[{index}]")
        reject_extra(path, tab, allowed, f"workload.tabs[{index}]")
        require_keys(path, tab, required, f"workload.tabs[{index}]")
        tab_id = require_string(path, tab, "tab_id", f"workload.tabs[{index}]")
        if tab_id in seen:
            fail(path, f"duplicate tab_id: {tab_id}")
        seen.add(tab_id)
        for key in ["corpus_case", "top_level_site"]:
            require_string(path, tab, key, f"workload.tabs[{index}]")
        state = require_string(path, tab, "state", f"workload.tabs[{index}]")
        if state not in counts:
            fail(path, f"workload.tabs[{index}].state is not a known lifecycle state")
        counts[state] += 1
        require_int(path, tab, "site_instances", f"workload.tabs[{index}]", minimum=0)
        renderer_process = tab.get("renderer_process")
        if renderer_process is not None and not isinstance(renderer_process, str):
            fail(path, f"workload.tabs[{index}].renderer_process must be string or null")
        protected = require_bool(path, tab, "protected", f"workload.tabs[{index}]")
        protection_reason = tab.get("protection_reason")
        if protection_reason is not None and not isinstance(protection_reason, str):
            fail(path, f"workload.tabs[{index}].protection_reason must be string or null")
        if protected and not protection_reason:
            fail(path, f"workload.tabs[{index}] protected tab needs a protection_reason")
        revival_ms = tab.get("revival_ms")
        if revival_ms is not None and (
            isinstance(revival_ms, bool)
            or not isinstance(revival_ms, (int, float))
            or revival_ms < 0
        ):
            fail(path, f"workload.tabs[{index}].revival_ms must be non-negative or null")
        lost_state = tab.get("lost_state", [])
        if not isinstance(lost_state, list) or any(
            not isinstance(item, str) for item in lost_state
        ):
            fail(path, f"workload.tabs[{index}].lost_state must be an array of strings")
    return counts


def validate_workload(path: Path, value: object) -> dict[str, int]:
    obj = require_object(path, value, "workload")
    required = {"corpus_version", "scenario", "cache_state", "network_profile", "tabs"}
    optional = {"extensions", "agent_mode"}
    reject_extra(path, obj, required | optional, "workload")
    require_keys(path, obj, required, "workload")
    for key in ["corpus_version", "scenario", "network_profile"]:
        require_string(path, obj, key, "workload")
    if obj.get("cache_state") not in {"cold", "warm", "mixed"}:
        fail(path, "workload.cache_state must be cold, warm, or mixed")
    if "extensions" in obj:
        require_string_array(path, obj, "extensions", "workload")
    if "agent_mode" in obj and obj["agent_mode"] not in {"disabled", "idle", "local", "remote"}:
        fail(path, "workload.agent_mode must be disabled, idle, local, or remote")
    return validate_tabs(path, obj.get("tabs"))


def validate_security(path: Path, value: object) -> None:
    obj = require_object(path, value, "security")
    required = {"sandbox", "site_isolation", "jit", "mitigations"}
    optional = {"exceptions"}
    reject_extra(path, obj, required | optional, "security")
    require_keys(path, obj, required, "security")
    require_bool(path, obj, "sandbox", "security")
    require_bool(path, obj, "site_isolation", "security")
    require_string(path, obj, "jit", "security")
    require_string_array(path, obj, "mitigations", "security")
    if "exceptions" in obj:
        require_string_array(path, obj, "exceptions", "security")


def validate_lifecycle(
    path: Path, value: object, tab_state_counts: dict[str, int]
) -> None:
    obj = require_object(path, value, "lifecycle")
    required = {"process_count", "renderer_count", "state_counts"}
    optional = {"protected_tabs"}
    reject_extra(path, obj, required | optional, "lifecycle")
    require_keys(path, obj, required, "lifecycle")
    require_int(path, obj, "process_count", "lifecycle", minimum=1)
    require_int(path, obj, "renderer_count", "lifecycle", minimum=0)
    state_counts = require_object(path, obj.get("state_counts"), "lifecycle.state_counts")
    reject_extra(path, state_counts, set(STATES), "lifecycle.state_counts")
    require_keys(path, state_counts, set(STATES), "lifecycle.state_counts")
    for state in STATES:
        value = require_int(path, state_counts, state, "lifecycle.state_counts", minimum=0)
        if value != tab_state_counts[state]:
            fail(path, f"lifecycle.state_counts.{state} does not match workload.tabs")
    protected_tabs = obj.get("protected_tabs", [])
    if not isinstance(protected_tabs, list):
        fail(path, "lifecycle.protected_tabs must be an array")
    for index, item in enumerate(protected_tabs, start=1):
        protected = require_object(path, item, f"lifecycle.protected_tabs[{index}]")
        require_keys(path, protected, {"tab_id", "reason"}, f"lifecycle.protected_tabs[{index}]")
        require_string(path, protected, "tab_id", f"lifecycle.protected_tabs[{index}]")
        require_string(path, protected, "reason", f"lifecycle.protected_tabs[{index}]")


def validate_samples(path: Path, value: object) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(path, "samples must be a non-empty array")
    notes: list[str] = []
    for index, item in enumerate(value, start=1):
        sample = require_object(path, item, f"samples[{index}]")
        reject_extra(path, sample, {"iteration", "metrics", "notes"}, f"samples[{index}]")
        require_keys(path, sample, {"iteration", "metrics"}, f"samples[{index}]")
        require_int(path, sample, "iteration", f"samples[{index}]", minimum=1)
        metrics = require_object(path, sample.get("metrics"), f"samples[{index}].metrics")
        if not metrics:
            fail(path, f"samples[{index}].metrics must not be empty")
        for key, item in metrics.items():
            if not isinstance(key, str) or isinstance(item, bool) or not isinstance(item, (int, float)):
                fail(path, f"samples[{index}].metrics values must be numbers")
        if "notes" in sample:
            notes.extend(require_string_array(path, sample, "notes", f"samples[{index}]"))
    return notes


def validate_failures(path: Path, value: object) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        fail(path, "failures must be an array")
    for index, item in enumerate(value, start=1):
        failure = require_object(path, item, f"failures[{index}]")
        reject_extra(path, failure, {"target", "classification", "detail"}, f"failures[{index}]")
        require_keys(path, failure, {"target", "classification"}, f"failures[{index}]")
        require_string(path, failure, "target", f"failures[{index}]")
        require_string(path, failure, "classification", f"failures[{index}]")
        if "detail" in failure:
            require_string(path, failure, "detail", f"failures[{index}]")


def validate_raw_artifacts(path: Path, value: object, *, require_local_hashes: bool) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        fail(path, "raw_artifacts must be an array")
    for index, item in enumerate(value, start=1):
        artifact = require_object(path, item, f"raw_artifacts[{index}]")
        reject_extra(path, artifact, {"kind", "sha256", "path"}, f"raw_artifacts[{index}]")
        require_keys(path, artifact, {"kind", "sha256"}, f"raw_artifacts[{index}]")
        require_string(path, artifact, "kind", f"raw_artifacts[{index}]")
        digest = require_string(path, artifact, "sha256", f"raw_artifacts[{index}]")
        if not SHA256.fullmatch(digest):
            fail(path, f"raw_artifacts[{index}].sha256 must be lowercase SHA-256")
        artifact_path = artifact.get("path")
        if artifact_path is not None and not isinstance(artifact_path, str):
            fail(path, f"raw_artifacts[{index}].path must be a string")
        if require_local_hashes:
            if not artifact_path:
                fail(path, f"raw_artifacts[{index}] needs a local path")
            resolved = (ROOT / artifact_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(path, f"raw_artifacts[{index}].path points outside repository")
            if not resolved.is_file():
                fail(path, f"raw_artifacts[{index}].path does not exist")
            actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
            if actual != digest:
                fail(path, f"raw_artifacts[{index}].sha256 does not match {artifact_path}")


def validate_claim(path: Path, value: object) -> dict[str, object] | None:
    if value is None:
        return None
    claim = require_object(path, value, "claim")
    required = {
        "status",
        "text",
        "owner",
        "reviewer",
        "supported_scope",
        "unsupported_behavior",
        "expires_at",
        "rerun_triggers",
    }
    reject_extra(path, claim, required, "claim")
    require_keys(path, claim, required, "claim")
    status = require_string(path, claim, "status", "claim")
    if status not in {"no_claim", "draft", "public_candidate", "approved", "expired"}:
        fail(path, "claim.status must be no_claim, draft, public_candidate, approved, or expired")
    for key in ["text", "owner", "reviewer"]:
        require_string(path, claim, key, "claim")
    for key in ["supported_scope", "unsupported_behavior", "rerun_triggers"]:
        items = require_string_array(path, claim, key, "claim")
        if not items:
            fail(path, f"claim.{key} must not be empty")
    expires_at = claim.get("expires_at")
    if expires_at is not None and not isinstance(expires_at, str):
        fail(path, "claim.expires_at must be a string or null")
    if status != "no_claim" and not expires_at:
        fail(path, "claim.expires_at is required unless claim.status is no_claim")
    return claim


def validate_manifest(
    path: Path,
    payload: object,
    *,
    require_local_hashes: bool,
    hardware_registry: dict[str, dict[str, object]],
    os_control_registry: dict[str, dict[str, object]],
    resource_attribution_registry: dict[str, dict[str, object]],
) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "benchmark_id",
        "resource_attribution_id",
        "browser",
        "environment",
        "workload",
        "security",
        "lifecycle",
        "samples",
    }
    optional = {"recorded_at", "failures", "raw_artifacts", "claim"}
    reject_extra(path, manifest, required | optional, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    benchmark_id = require_string(path, manifest, "benchmark_id", "manifest")
    if not BENCHMARK_ID.fullmatch(benchmark_id):
        fail(path, "benchmark_id has invalid characters")
    resource_attribution_id = require_string(
        path, manifest, "resource_attribution_id", "manifest"
    )
    if not RESOURCE_ATTRIBUTION_ID.fullmatch(resource_attribution_id):
        fail(path, "resource_attribution_id has invalid format")
    if resource_attribution_id not in resource_attribution_registry:
        fail(path, f"resource_attribution_id is not registered: {resource_attribution_id}")
    if "recorded_at" in manifest:
        require_string(path, manifest, "recorded_at", "manifest")
    validate_browser(path, manifest.get("browser"))
    environment = validate_environment(
        path, manifest.get("environment"), hardware_registry, os_control_registry
    )
    tab_state_counts = validate_workload(path, manifest.get("workload"))
    validate_security(path, manifest.get("security"))
    validate_lifecycle(path, manifest.get("lifecycle"), tab_state_counts)
    notes = validate_samples(path, manifest.get("samples"))
    validate_failures(path, manifest.get("failures"))
    validate_raw_artifacts(
        path, manifest.get("raw_artifacts"), require_local_hashes=require_local_hashes
    )
    claim = validate_claim(path, manifest.get("claim"))

    if require_local_hashes:
        if not benchmark_id.startswith("NOCLAIM."):
            fail(path, "default sample benchmark_id must start with NOCLAIM.")
        hardware_id = str(environment.get("hardware_id", ""))
        if not HARDWARE_ID.fullmatch(hardware_id):
            fail(path, "default sample environment.hardware_id must use the hardware registry")
        os_control_id = str(environment.get("os_control_id", ""))
        if not OS_CONTROL_ID.fullmatch(os_control_id):
            fail(path, "default sample environment.os_control_id must use the OS-control registry")
        if not RESOURCE_ATTRIBUTION_ID.fullmatch(resource_attribution_id):
            fail(path, "default sample resource_attribution_id must use the resource-attribution registry")
        if "harness smoke evidence only" not in " ".join(notes):
            fail(path, "default sample must include the no-claim evidence note")
        if not manifest.get("failures"):
            fail(path, "default sample must keep unsupported behavior visible")
        if not manifest.get("raw_artifacts"):
            fail(path, "default sample must include a checked raw_artifacts hash")
        if claim is None or claim.get("status") != "no_claim":
            fail(path, "default sample must include claim.status no_claim")
        claim_text = str(claim.get("text", "")).lower()
        if "no" not in claim_text or "claim" not in claim_text:
            fail(path, "default sample claim text must be explicit that no claim is made")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else DEFAULT_MANIFESTS
    try:
        hardware_registry = load_hardware_registry()
        os_control_registry = load_os_control_registry()
        resource_attribution_registry = load_resource_attribution_registry()
        for path in paths:
            validate_manifest(
                path,
                load_json(path),
                require_local_hashes=path.resolve() in {p.resolve() for p in DEFAULT_MANIFESTS},
                hardware_registry=hardware_registry,
                os_control_registry=os_control_registry,
                resource_attribution_registry=resource_attribution_registry,
            )
    except ValidationError as error:
        print(f"benchmark manifest validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark manifest validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
