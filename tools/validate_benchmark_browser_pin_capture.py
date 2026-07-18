#!/usr/bin/env python3
"""Validate benchmark browser-pin capture plan manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
MANIFEST_DIR = MACHINE / "benchmark-browser-pin-captures"
DEFAULT_MANIFESTS = [MANIFEST_DIR / "current-windows-high-end.no-claim.plan.json"]

PLAN_ID = re.compile(r"^TURING\.BENCHMARK\.BROWSER_PIN_CAPTURE\.[A-Z0-9._-]+$")
EXPECTED_TARGETS = [
    "chrome-current-host-pin-capture",
    "edge-current-host-pin-capture",
    "firefox-current-host-pin-capture",
    "safari-stable-pin-capture",
    "safari-technology-preview-pin-capture",
]
HARDWARE_ID = "TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07"
OS_CONTROL_ID = "TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07"
RELEASE_CATALOG_ID = "TURING.BENCHMARK.COMPETITOR_VERSIONS.CURRENT_DESKTOP.2026_07"
LOCAL_INSTALL_ID = "TURING.BENCHMARK.COMPETITOR_LOCAL_INSTALLS.CURRENT_WINDOWS_HIGH_END.2026_07"


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


def require_keys(path: Path, obj: dict[str, object], keys: set[str], label: str) -> None:
    missing = sorted(keys - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")
    extra = sorted(set(obj) - keys)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_string_list(
    path: Path, obj: dict[str, object], key: str, label: str, *, min_items: int = 1
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        fail(path, f"{label}.{key} must be an array of non-empty strings")
    if len(value) < min_items:
        fail(path, f"{label}.{key} must have at least {min_items} item(s)")
    return value


def validate_privacy(path: Path, value: object) -> None:
    privacy = require_object(path, value, "privacy_boundary")
    keys = {
        "allowed_reads",
        "prohibited_reads",
        "allowed_writes",
        "prohibited_writes",
        "retention_policy",
    }
    require_keys(path, privacy, keys, "privacy_boundary")
    prohibited = " ".join(
        require_string_list(path, privacy, "prohibited_reads", "privacy_boundary", min_items=2)
    ).lower()
    for phrase in ["real", "profile", "cookies", "credentials"]:
        if phrase not in prohibited:
            fail(path, f"privacy_boundary.prohibited_reads must mention {phrase}")
    writes = " ".join(
        require_string_list(path, privacy, "allowed_writes", "privacy_boundary", min_items=1)
    ).lower()
    if "%temp%" not in writes:
        fail(path, "privacy_boundary.allowed_writes must restrict writes to a temp root")
    require_string_list(path, privacy, "prohibited_writes", "privacy_boundary", min_items=2)
    require_string(path, privacy, "retention_policy", "privacy_boundary")


def validate_isolation(path: Path, value: object) -> None:
    isolation = require_object(path, value, "isolation_policy")
    keys = {
        "profile_root_policy",
        "profile_lifecycle",
        "network_policy",
        "account_policy",
        "extension_policy",
        "update_policy",
        "benchmark_argument_policy",
    }
    require_keys(path, isolation, keys, "isolation_policy")
    profile_policy = require_string(path, isolation, "profile_root_policy", "isolation_policy").lower()
    if "%temp%" not in profile_policy or "rejects existing user profile" not in profile_policy:
        fail(path, "isolation_policy.profile_root_policy must require temp profiles and reject user profiles")
    network_policy = require_string(path, isolation, "network_policy", "isolation_policy").lower()
    if "offline by default" not in network_policy:
        fail(path, "isolation_policy.network_policy must be offline by default")
    account_policy = require_string(path, isolation, "account_policy", "isolation_policy").lower()
    if "no account" not in account_policy or "sync" not in account_policy:
        fail(path, "isolation_policy.account_policy must prohibit accounts and sync")
    for key in ["profile_lifecycle", "extension_policy", "update_policy", "benchmark_argument_policy"]:
        require_string(path, isolation, key, "isolation_policy")


def validate_target(path: Path, value: object, index: int) -> str:
    label = f"browser_targets[{index}]"
    target = require_object(path, value, label)
    keys = {
        "target_id",
        "product_name",
        "platform",
        "release_catalog_browser_id",
        "local_install_browser_id",
        "status",
        "planned_profile_mode",
        "planned_version_capture",
        "planned_capture_arguments",
        "expected_artifacts",
        "blocked_until",
    }
    require_keys(path, target, keys, label)
    target_id = require_string(path, target, "target_id", label)
    status = require_string(path, target, "status", label)
    if status not in {
        "planned_from_local_executable",
        "blocked_missing_local_install",
        "blocked_requires_platform_host",
    }:
        fail(path, f"{label}.status is invalid")
    local_install = target.get("local_install_browser_id")
    if status == "planned_from_local_executable":
        if not isinstance(local_install, str) or not local_install:
            fail(path, f"{label}.local_install_browser_id is required for planned local captures")
    else:
        if local_install is not None:
            fail(path, f"{label}.local_install_browser_id must be null when blocked")
    profile_mode = require_string(path, target, "planned_profile_mode", label).lower()
    if "temporary" not in profile_mode:
        fail(path, f"{label}.planned_profile_mode must require a temporary profile")
    version_capture = " ".join(
        require_string_list(path, target, "planned_version_capture", label, min_items=2)
    ).lower()
    if "browser-reported version" not in version_capture:
        fail(path, f"{label}.planned_version_capture must include browser-reported version")
    artifacts = " ".join(
        require_string_list(path, target, "expected_artifacts", label, min_items=3)
    ).lower()
    for phrase in ["artifact index", "version"]:
        if phrase not in artifacts:
            fail(path, f"{label}.expected_artifacts must mention {phrase}")
    args = target.get("planned_capture_arguments")
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        fail(path, f"{label}.planned_capture_arguments must be an array of strings")
    if status == "planned_from_local_executable":
        joined_args = " ".join(args).lower()
        if "--user-data-dir=%temp%" not in joined_args:
            fail(path, f"{label}.planned_capture_arguments must use a temp user-data-dir")
        if "disable-sync" not in joined_args:
            fail(path, f"{label}.planned_capture_arguments must disable sync for capture")
    require_string_list(path, target, "blocked_until", label, min_items=1)
    return target_id


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    keys = {
        "schema_version",
        "capture_plan_id",
        "status",
        "claim_status",
        "created_at",
        "host_references",
        "privacy_boundary",
        "isolation_policy",
        "browser_targets",
        "artifact_contract",
        "validation_contract",
        "unsupported_behavior",
        "evidence_required",
    }
    require_keys(path, manifest, keys, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    plan_id = require_string(path, manifest, "capture_plan_id", "manifest")
    if not PLAN_ID.fullmatch(plan_id):
        fail(path, "capture_plan_id has invalid format")
    if manifest.get("status") != "plan_no_browser_run":
        fail(path, "status must remain plan_no_browser_run")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in ["no browser was launched", "no browser-reported version", "no benchmark ran", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    require_string(path, manifest, "created_at", "manifest")
    refs = require_object(path, manifest.get("host_references"), "host_references")
    require_keys(
        path,
        refs,
        {"hardware_id", "os_control_id", "release_catalog_manifest_id", "local_install_manifest_id"},
        "host_references",
    )
    expected_refs = {
        "hardware_id": HARDWARE_ID,
        "os_control_id": OS_CONTROL_ID,
        "release_catalog_manifest_id": RELEASE_CATALOG_ID,
        "local_install_manifest_id": LOCAL_INSTALL_ID,
    }
    for key, expected in expected_refs.items():
        if refs[key] != expected:
            fail(path, f"host_references.{key} does not match expected current-host evidence")
    validate_privacy(path, manifest.get("privacy_boundary"))
    validate_isolation(path, manifest.get("isolation_policy"))
    targets = manifest.get("browser_targets")
    if not isinstance(targets, list):
        fail(path, "browser_targets must be an array")
    target_ids = [validate_target(path, item, index) for index, item in enumerate(targets, start=1)]
    if target_ids != EXPECTED_TARGETS:
        fail(path, "browser_targets must list Chrome, Edge, Firefox, Safari, and Safari TP in order")
    artifact_contract = " ".join(
        require_string_list(path, manifest, "artifact_contract", "manifest", min_items=3)
    ).lower()
    if "prohibited path" not in artifact_contract:
        fail(path, "artifact_contract must record prohibited-path checks")
    validation_contract = " ".join(
        require_string_list(path, manifest, "validation_contract", "manifest", min_items=3)
    ).lower()
    for phrase in ["reject any capture", "profile path", "no-claim"]:
        if phrase not in validation_contract:
            fail(path, f"validation_contract must mention: {phrase}")
    unsupported = " ".join(
        require_string_list(path, manifest, "unsupported_behavior", "manifest", min_items=4)
    ).lower()
    for phrase in ["no browser was launched", "no browser-reported version", "no benchmark ran"]:
        if phrase not in unsupported:
            fail(path, f"unsupported_behavior must mention: {phrase}")
    evidence = " ".join(
        require_string_list(path, manifest, "evidence_required", "manifest", min_items=5)
    ).lower()
    for phrase in ["browser-launch capture runner", "browser-reported version", "safari", "owner review"]:
        if phrase not in evidence:
            fail(path, f"evidence_required must mention: {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(argument) for argument in argv] if argv else DEFAULT_MANIFESTS
    try:
        for path in paths:
            if not path.is_absolute():
                path = ROOT / path
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark browser-pin capture validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark browser-pin capture validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
