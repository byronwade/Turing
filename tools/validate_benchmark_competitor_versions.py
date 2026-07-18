#!/usr/bin/env python3
"""Validate benchmark competitor-version catalog manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
MANIFEST_DIR = MACHINE / "benchmark-competitor-versions"
DEFAULT_MANIFESTS = [MANIFEST_DIR / "current-desktop-release-candidates.2026-07.json"]

MANIFEST_ID = re.compile(r"^TURING\.BENCHMARK\.COMPETITOR_VERSIONS\.[A-Z0-9._-]+$")
BROWSER_ID = re.compile(r"^[a-z0-9][a-z0-9-]+$")

EXPECTED_BROWSER_IDS = [
    "chrome-stable-desktop",
    "edge-stable-desktop",
    "firefox-stable-desktop",
    "safari-stable-desktop",
    "safari-technology-preview",
]

REQUIRED_LOCAL_PIN_FIELDS = {
    "product_name",
    "channel",
    "exact_version_reported_by_browser",
    "platform",
    "architecture",
    "executable_path",
    "executable_sha256",
    "release_source_url",
    "command_line",
    "profile_source",
    "extension_state",
    "sync_account_state",
    "update_state_before_run",
    "update_state_after_run",
    "sandbox_and_site_isolation_settings",
    "memory_or_energy_saver_settings",
    "cache_state",
    "user_agent_policy",
    "failure_denominator_policy",
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


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str, *, min_items: int = 1
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        fail(path, f"{label}.{key} must be an array of non-empty strings")
    if len(value) < min_items:
        fail(path, f"{label}.{key} must contain at least {min_items} item(s)")
    return value


def validate_browser(path: Path, value: object, index: int) -> str:
    label = f"browsers[{index}]"
    browser = require_object(path, value, label)
    allowed = {
        "id",
        "product_name",
        "channel",
        "engine_family",
        "platform_scope",
        "version",
        "release_date",
        "source_url",
        "source_observation",
        "local_pin_status",
        "benchmark_eligible",
        "missing_pin_evidence",
    }
    reject_extra(path, browser, allowed, label)
    require_keys(path, browser, allowed, label)
    browser_id = require_string(path, browser, "id", label)
    if not BROWSER_ID.fullmatch(browser_id):
        fail(path, f"{label}.id has invalid format")
    for key in [
        "product_name",
        "channel",
        "engine_family",
        "platform_scope",
        "version",
        "source_url",
        "source_observation",
        "local_pin_status",
    ]:
        require_string(path, browser, key, label)
    release_date = browser.get("release_date")
    if release_date is not None and (
        not isinstance(release_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", release_date)
    ):
        fail(path, f"{label}.release_date must be null or YYYY-MM-DD")
    if browser["local_pin_status"] != "not_installed_or_observed_by_manifest":
        fail(path, f"{label}.local_pin_status must remain not_installed_or_observed_by_manifest")
    if browser.get("benchmark_eligible") is not False:
        fail(path, f"{label}.benchmark_eligible must remain false without local pins")
    missing = require_string_array(path, browser, "missing_pin_evidence", label, min_items=2)
    if "local executable path" not in " ".join(missing).lower() and "application path" not in " ".join(missing).lower():
        fail(path, f"{label}.missing_pin_evidence must mention local executable or application path")
    if not browser["source_url"].startswith("https://"):
        fail(path, f"{label}.source_url must use https")
    return browser_id


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    allowed = {
        "schema_version",
        "competitor_version_manifest_id",
        "status",
        "claim_status",
        "retrieved_at",
        "source_policy",
        "required_local_pin_fields",
        "browsers",
        "benchmark_suite_notes",
        "unsupported_behavior",
        "evidence_required",
    }
    reject_extra(path, manifest, allowed, "manifest")
    require_keys(path, manifest, allowed, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    manifest_id = require_string(path, manifest, "competitor_version_manifest_id", "manifest")
    if not MANIFEST_ID.fullmatch(manifest_id):
        fail(path, "competitor_version_manifest_id has invalid format")
    if manifest.get("status") != "release_catalog_no_local_install_pins":
        fail(path, "status must remain release_catalog_no_local_install_pins")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in [
        "no installed browser path",
        "no executable hash",
        "no benchmark run",
        "no competitor result",
        "no performance claim",
    ]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    retrieved_at = require_string(path, manifest, "retrieved_at", "manifest")
    if "T" not in retrieved_at:
        fail(path, "retrieved_at must be a date-time string")
    source_policy = require_string_array(path, manifest, "source_policy", "manifest", min_items=2)
    if not any("official" in item.lower() for item in source_policy):
        fail(path, "source_policy must require official sources")
    local_pin_fields = set(
        require_string_array(path, manifest, "required_local_pin_fields", "manifest", min_items=10)
    )
    missing_pin_fields = sorted(REQUIRED_LOCAL_PIN_FIELDS - local_pin_fields)
    if missing_pin_fields:
        fail(path, "required_local_pin_fields is missing: " + ", ".join(missing_pin_fields))
    browsers = manifest.get("browsers")
    if not isinstance(browsers, list) or not browsers:
        fail(path, "browsers must be a non-empty array")
    browser_ids = [validate_browser(path, item, index) for index, item in enumerate(browsers, start=1)]
    if browser_ids != EXPECTED_BROWSER_IDS:
        fail(path, "browsers must match the required competitor order")
    suite_notes = require_string_array(path, manifest, "benchmark_suite_notes", "manifest", min_items=3)
    for suite in ["Speedometer 3.1", "JetStream 3.0", "MotionMark"]:
        if not any(suite in note for note in suite_notes):
            fail(path, f"benchmark_suite_notes must mention {suite}")
    unsupported = " ".join(
        require_string_array(path, manifest, "unsupported_behavior", "manifest", min_items=3)
    ).lower()
    for phrase in ["no local browser executable", "no benchmark suite", "no competitor result"]:
        if phrase not in unsupported:
            fail(path, f"unsupported_behavior must mention: {phrase}")
    evidence_required = " ".join(
        require_string_array(path, manifest, "evidence_required", "manifest", min_items=3)
    ).lower()
    for phrase in ["executable", "profile", "runner-generated benchmark manifest", "raw artifacts"]:
        if phrase not in evidence_required:
            fail(path, f"evidence_required must mention: {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(argument) for argument in argv] if argv else DEFAULT_MANIFESTS
    try:
        for path in paths:
            if not path.is_absolute():
                path = ROOT / path
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark competitor-version validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark competitor-version validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
