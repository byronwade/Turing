#!/usr/bin/env python3
"""Validate benchmark hardware and OS manifests without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "docs" / "blueprint-v1" / "machine" / "benchmark-hardware"
DEFAULT_MANIFESTS = [MANIFEST_DIR / "current-windows-high-end.candidate.json"]

HARDWARE_ID = re.compile(r"^TURING\.BENCHMARK\.HARDWARE\.[A-Z0-9._-]+$")


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


def require_string_array(path: Path, obj: dict[str, object], key: str, label: str, *, min_items: int = 0) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        fail(path, f"{label}.{key} must be an array of non-empty strings")
    if len(value) < min_items:
        fail(path, f"{label}.{key} must contain at least {min_items} item(s)")
    return value


def validate_host(path: Path, value: object) -> None:
    host = require_object(path, value, "host")
    required = {"hostname", "manufacturer", "model", "system_type", "role", "owner"}
    reject_extra(path, host, required, "host")
    require_keys(path, host, required, "host")
    for key in sorted(required):
        require_string(path, host, key, "host")


def validate_cpu(path: Path, value: object) -> None:
    cpu = require_object(path, value, "cpu")
    required = {"name", "physical_cores", "logical_processors"}
    reject_extra(path, cpu, required, "cpu")
    require_keys(path, cpu, required, "cpu")
    require_string(path, cpu, "name", "cpu")
    cores = require_int(path, cpu, "physical_cores", "cpu", minimum=1)
    logical = require_int(path, cpu, "logical_processors", "cpu", minimum=1)
    if logical < cores:
        fail(path, "cpu.logical_processors must be >= cpu.physical_cores")


def validate_memory(path: Path, value: object) -> None:
    memory = require_object(path, value, "memory")
    required = {"total_physical_bytes", "installed_capacity_bytes", "module_count"}
    reject_extra(path, memory, required, "memory")
    require_keys(path, memory, required, "memory")
    total = require_int(path, memory, "total_physical_bytes", "memory", minimum=1)
    installed = require_int(path, memory, "installed_capacity_bytes", "memory", minimum=1)
    require_int(path, memory, "module_count", "memory", minimum=1)
    if total > installed:
        fail(path, "memory.total_physical_bytes must be <= installed_capacity_bytes")


def validate_gpus(path: Path, value: object) -> None:
    if not isinstance(value, list) or not value:
        fail(path, "gpus must be a non-empty array")
    required = {"name", "driver_version", "current_refresh_hz"}
    for index, item in enumerate(value, start=1):
        gpu = require_object(path, item, f"gpus[{index}]")
        reject_extra(path, gpu, required, f"gpus[{index}]")
        require_keys(path, gpu, required, f"gpus[{index}]")
        require_string(path, gpu, "name", f"gpus[{index}]")
        require_string(path, gpu, "driver_version", f"gpus[{index}]")
        require_int(path, gpu, "current_refresh_hz", f"gpus[{index}]", minimum=1)


def validate_storage(path: Path, value: object) -> None:
    if not isinstance(value, list) or not value:
        fail(path, "storage must be a non-empty array")
    required = {"model", "media_type", "size_bytes", "role"}
    for index, item in enumerate(value, start=1):
        disk = require_object(path, item, f"storage[{index}]")
        reject_extra(path, disk, required, f"storage[{index}]")
        require_keys(path, disk, required, f"storage[{index}]")
        for key in ["model", "media_type", "role"]:
            require_string(path, disk, key, f"storage[{index}]")
        require_int(path, disk, "size_bytes", f"storage[{index}]", minimum=1)


def validate_os_image(path: Path, value: object) -> None:
    os_image = require_object(path, value, "os_image")
    required = {
        "caption",
        "version",
        "build_number",
        "display_version",
        "ubr",
        "edition_id",
        "installation_type",
        "install_date",
        "last_boot_time",
        "update_control_status",
    }
    reject_extra(path, os_image, required, "os_image")
    require_keys(path, os_image, required, "os_image")
    for key in required - {"ubr"}:
        require_string(path, os_image, key, "os_image")
    require_int(path, os_image, "ubr", "os_image", minimum=0)


def validate_power_thermal(path: Path, value: object) -> None:
    power = require_object(path, value, "power_thermal")
    required = {"active_power_scheme", "thermal_state", "display_refresh_control"}
    reject_extra(path, power, required, "power_thermal")
    require_keys(path, power, required, "power_thermal")
    for key in sorted(required):
        require_string(path, power, key, "power_thermal")


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "hardware_id",
        "status",
        "claim_status",
        "observed_at",
        "hardware_tier",
        "host",
        "cpu",
        "memory",
        "gpus",
        "storage",
        "os_image",
        "power_thermal",
        "stability_controls",
        "unsupported_behavior",
        "evidence_required",
        "sources",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    hardware_id = require_string(path, manifest, "hardware_id", "manifest")
    if not HARDWARE_ID.fullmatch(hardware_id):
        fail(path, "hardware_id has invalid format")
    status = require_string(path, manifest, "status", "manifest")
    if status not in {"candidate_current_host", "draft", "reviewed", "retired"}:
        fail(path, "status must be candidate_current_host, draft, reviewed, or retired")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    require_string(path, manifest, "observed_at", "manifest")
    if require_string(path, manifest, "hardware_tier", "manifest") not in {"Tier L", "Tier M", "Tier H"}:
        fail(path, "hardware_tier must be Tier L, Tier M, or Tier H")
    validate_host(path, manifest.get("host"))
    validate_cpu(path, manifest.get("cpu"))
    validate_memory(path, manifest.get("memory"))
    validate_gpus(path, manifest.get("gpus"))
    validate_storage(path, manifest.get("storage"))
    validate_os_image(path, manifest.get("os_image"))
    validate_power_thermal(path, manifest.get("power_thermal"))
    require_string_array(path, manifest, "stability_controls", "manifest")
    require_string_array(path, manifest, "unsupported_behavior", "manifest", min_items=1)
    require_string_array(path, manifest, "evidence_required", "manifest", min_items=1)
    require_string_array(path, manifest, "sources", "manifest", min_items=1)
    if status != "reviewed" and not manifest["evidence_required"]:
        fail(path, "non-reviewed manifests must keep evidence_required visible")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else DEFAULT_MANIFESTS
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark hardware validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark hardware validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
