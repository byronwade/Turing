#!/usr/bin/env python3
"""Validate benchmark OS and update-control manifests without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
MANIFEST_DIR = MACHINE / "benchmark-os-controls"
HARDWARE_MANIFEST_DIR = MACHINE / "benchmark-hardware"
DEFAULT_MANIFESTS = [MANIFEST_DIR / "current-windows-high-end.candidate.json"]

OS_CONTROL_ID = re.compile(r"^TURING\.BENCHMARK\.OS_CONTROL\.[A-Z0-9._-]+$")
HARDWARE_ID = re.compile(r"^TURING\.BENCHMARK\.HARDWARE\.[A-Z0-9._-]+$")
FORBIDDEN_SECRET_MARKERS = ["ProductId", "DigitalProductId", "S-1-5-21-"]


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


def reject_extra(path: Path, obj: dict[str, object], allowed: set[str], label: str) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(path: Path, obj: dict[str, object], required: set[str], label: str) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_int(path: Path, obj: dict[str, object], key: str, label: str, *, minimum: int = 0) -> int:
    value = obj.get(key)
    if type(value) is not int or value < minimum:
        fail(path, f"{label}.{key} must be an integer >= {minimum}")
    return value


def require_bool(path: Path, obj: dict[str, object], key: str, label: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        fail(path, f"{label}.{key} must be a boolean")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str, *, min_items: int = 0
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        fail(path, f"{label}.{key} must be an array of non-empty strings")
    if len(value) < min_items:
        fail(path, f"{label}.{key} must contain at least {min_items} item(s)")
    return value


def load_hardware_ids(path: Path) -> set[str]:
    hardware_ids: set[str] = set()
    for hardware_path in sorted(HARDWARE_MANIFEST_DIR.glob("*.json")):
        payload = require_object(hardware_path, load_json(hardware_path), "hardware manifest")
        hardware_id = require_string(hardware_path, payload, "hardware_id", "hardware manifest")
        if not HARDWARE_ID.fullmatch(hardware_id):
            fail(hardware_path, "hardware_id has invalid format")
        hardware_ids.add(hardware_id)
    if not hardware_ids:
        fail(path, "no benchmark hardware manifests are registered")
    return hardware_ids


def check_no_secret_markers(path: Path, value: object, label: str = "manifest") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if any(marker in key for marker in FORBIDDEN_SECRET_MARKERS):
                fail(path, f"{label} contains forbidden sensitive key marker: {key}")
            check_no_secret_markers(path, item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value, start=1):
            check_no_secret_markers(path, item, f"{label}[{index}]")
    elif isinstance(value, str) and any(marker in value for marker in FORBIDDEN_SECRET_MARKERS):
        fail(path, f"{label} contains forbidden sensitive value marker")


def validate_os_identity(path: Path, value: object) -> None:
    obj = require_object(path, value, "os_identity")
    required = {
        "caption",
        "version",
        "build_number",
        "display_version",
        "ubr",
        "edition_id",
        "installation_type",
        "build_branch",
        "lcu_version",
        "pending_install",
        "install_date",
        "last_boot_time",
        "insider_preview",
        "insider_channel",
        "insider_ring",
        "insider_content_type",
        "clean_image_status",
    }
    reject_extra(path, obj, required, "os_identity")
    require_keys(path, obj, required, "os_identity")
    for key in sorted(required - {"ubr", "pending_install", "insider_preview"}):
        require_string(path, obj, key, "os_identity")
    require_int(path, obj, "ubr", "os_identity", minimum=0)
    require_int(path, obj, "pending_install", "os_identity", minimum=0)
    require_bool(path, obj, "insider_preview", "os_identity")


def validate_update_control(path: Path, value: object) -> None:
    obj = require_object(path, value, "update_control")
    required = {
        "windows_update_access_policy",
        "os_upgrade_policy",
        "automatic_update_policy",
        "feature_update_policy",
        "quality_update_policy",
        "driver_update_policy",
        "preview_build_policy",
        "active_hours",
        "metered_download_policy",
        "policy_status",
    }
    reject_extra(path, obj, required, "update_control")
    require_keys(path, obj, required, "update_control")
    for key in sorted(required):
        require_string(path, obj, key, "update_control")


def validate_driver_firmware(path: Path, value: object) -> None:
    obj = require_object(path, value, "driver_firmware_control")
    required = {
        "gpu_name",
        "gpu_driver_version",
        "bios_vendor",
        "bios_version",
        "bios_release_date",
        "baseboard",
        "driver_inventory_status",
        "firmware_freeze_status",
    }
    reject_extra(path, obj, required, "driver_firmware_control")
    require_keys(path, obj, required, "driver_firmware_control")
    for key in sorted(required):
        require_string(path, obj, key, "driver_firmware_control")


def validate_power_display_thermal(path: Path, value: object) -> None:
    obj = require_object(path, value, "power_display_thermal_control")
    required = {
        "active_power_scheme",
        "processor_minimum_ac_percent",
        "processor_maximum_ac_percent",
        "display_resolution",
        "display_refresh_hz",
        "display_refresh_status",
        "thermal_state",
        "thermal_capture_status",
    }
    reject_extra(path, obj, required, "power_display_thermal_control")
    require_keys(path, obj, required, "power_display_thermal_control")
    for key in sorted(required - {"processor_minimum_ac_percent", "processor_maximum_ac_percent", "display_refresh_hz"}):
        require_string(path, obj, key, "power_display_thermal_control")
    require_int(path, obj, "processor_minimum_ac_percent", "power_display_thermal_control", minimum=0)
    require_int(path, obj, "processor_maximum_ac_percent", "power_display_thermal_control", minimum=0)
    require_int(path, obj, "display_refresh_hz", "power_display_thermal_control", minimum=1)


def validate_clock_network(path: Path, value: object) -> None:
    obj = require_object(path, value, "clock_network_control")
    required = {
        "timezone_id",
        "timezone_display",
        "supports_daylight_saving_time",
        "w32time_status",
        "network_isolation_status",
        "artifact_storage_status",
    }
    reject_extra(path, obj, required, "clock_network_control")
    require_keys(path, obj, required, "clock_network_control")
    for key in sorted(required - {"supports_daylight_saving_time"}):
        require_string(path, obj, key, "clock_network_control")
    require_bool(path, obj, "supports_daylight_saving_time", "clock_network_control")


def validate_services(path: Path, value: object) -> None:
    if not isinstance(value, list) or not value:
        fail(path, "background_services must be a non-empty array")
    required = {"name", "status", "start_type"}
    optional = {"query_note"}
    seen: set[str] = set()
    for index, item in enumerate(value, start=1):
        service = require_object(path, item, f"background_services[{index}]")
        reject_extra(path, service, required | optional, f"background_services[{index}]")
        require_keys(path, service, required, f"background_services[{index}]")
        name = require_string(path, service, "name", f"background_services[{index}]")
        if name in seen:
            fail(path, f"duplicate service record: {name}")
        seen.add(name)
        require_string(path, service, "status", f"background_services[{index}]")
        require_string(path, service, "start_type", f"background_services[{index}]")
        if "query_note" in service:
            require_string(path, service, "query_note", f"background_services[{index}]")


def validate_manifest(path: Path, payload: object, hardware_ids: set[str]) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "os_control_id",
        "hardware_id",
        "status",
        "claim_status",
        "observed_at",
        "os_identity",
        "update_control",
        "driver_firmware_control",
        "power_display_thermal_control",
        "clock_network_control",
        "background_services",
        "unsupported_behavior",
        "evidence_required",
        "sources",
        "external_sources",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")
    check_no_secret_markers(path, manifest)
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    os_control_id = require_string(path, manifest, "os_control_id", "manifest")
    if not OS_CONTROL_ID.fullmatch(os_control_id):
        fail(path, "os_control_id has invalid format")
    hardware_id = require_string(path, manifest, "hardware_id", "manifest")
    if not HARDWARE_ID.fullmatch(hardware_id):
        fail(path, "hardware_id has invalid format")
    if hardware_id not in hardware_ids:
        fail(path, f"hardware_id is not registered: {hardware_id}")
    status = require_string(path, manifest, "status", "manifest")
    if status not in {"candidate_current_host_uncontrolled", "draft", "reviewed", "retired"}:
        fail(path, "status must be candidate_current_host_uncontrolled, draft, reviewed, or retired")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in ["no clean image", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    require_string(path, manifest, "observed_at", "manifest")
    validate_os_identity(path, manifest.get("os_identity"))
    validate_update_control(path, manifest.get("update_control"))
    validate_driver_firmware(path, manifest.get("driver_firmware_control"))
    validate_power_display_thermal(path, manifest.get("power_display_thermal_control"))
    validate_clock_network(path, manifest.get("clock_network_control"))
    validate_services(path, manifest.get("background_services"))
    unsupported = require_string_array(path, manifest, "unsupported_behavior", "manifest", min_items=1)
    evidence = require_string_array(path, manifest, "evidence_required", "manifest", min_items=1)
    require_string_array(path, manifest, "sources", "manifest", min_items=1)
    external = require_string_array(path, manifest, "external_sources", "manifest", min_items=1)
    if status != "reviewed" and not evidence:
        fail(path, "non-reviewed manifests must keep evidence_required visible")
    for phrase in ["not a clean OS image", "display refresh rate is not normalized"]:
        if phrase not in unsupported:
            fail(path, f"unsupported_behavior must mention: {phrase}")
    if not any(source.startswith("https://learn.microsoft.com/") for source in external):
        fail(path, "external_sources must include Microsoft documentation")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else DEFAULT_MANIFESTS
    try:
        hardware_ids = load_hardware_ids(paths[0] if paths else MANIFEST_DIR)
        for path in paths:
            validate_manifest(path, load_json(path), hardware_ids)
    except ValidationError as error:
        print(f"benchmark OS-control validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark OS-control validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
