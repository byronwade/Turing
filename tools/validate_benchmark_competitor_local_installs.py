#!/usr/bin/env python3
"""Validate benchmark competitor local-install inventory manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
MANIFEST_DIR = MACHINE / "benchmark-competitor-local-installs"
DEFAULT_MANIFESTS = [MANIFEST_DIR / "current-windows-high-end.candidate.json"]

MANIFEST_ID = re.compile(r"^TURING\.BENCHMARK\.COMPETITOR_LOCAL_INSTALLS\.[A-Z0-9._-]+$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_OBSERVED = ["chrome-local-desktop", "edge-local-desktop"]
EXPECTED_ABSENT = [
    "firefox-stable-desktop",
    "safari-stable-desktop",
    "safari-technology-preview",
]

HARDWARE_ID = "TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07"
OS_CONTROL_ID = "TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07"
RELEASE_CATALOG_ID = "TURING.BENCHMARK.COMPETITOR_VERSIONS.CURRENT_DESKTOP.2026_07"


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


def validate_signature(path: Path, value: object, label: str) -> None:
    signature = require_object(path, value, label)
    keys = {"status", "signer_subject", "signer_thumbprint"}
    require_keys(path, signature, keys, label)
    if require_string(path, signature, "status", label) != "Valid":
        fail(path, f"{label}.status must be Valid")
    require_string(path, signature, "signer_subject", label)
    thumbprint = require_string(path, signature, "signer_thumbprint", label)
    if not re.fullmatch(r"[0-9A-F]{40}", thumbprint):
        fail(path, f"{label}.signer_thumbprint must be 40 uppercase hex characters")


def validate_browser(path: Path, value: object, index: int) -> str:
    label = f"observed_browsers[{index}]"
    browser = require_object(path, value, label)
    keys = {
        "browser_id",
        "release_catalog_browser_id",
        "product_name",
        "channel_claim",
        "engine_family",
        "platform",
        "executable_path",
        "file_version",
        "product_version",
        "browser_reported_version",
        "file_size_bytes",
        "last_write_time_utc",
        "sha256",
        "signature",
        "registry_observations",
        "version_state",
        "release_catalog_relation",
        "local_pin_status",
        "benchmark_eligible",
        "missing_pin_evidence",
    }
    require_keys(path, browser, keys, label)
    browser_id = require_string(path, browser, "browser_id", label)
    require_string(path, browser, "release_catalog_browser_id", label)
    require_string(path, browser, "product_name", label)
    require_string(path, browser, "channel_claim", label)
    require_string(path, browser, "engine_family", label)
    require_string(path, browser, "platform", label)
    executable_path = require_string(path, browser, "executable_path", label)
    if "\\Users\\" in executable_path:
        fail(path, f"{label}.executable_path must not point at a user profile")
    require_string(path, browser, "file_version", label)
    require_string(path, browser, "product_version", label)
    if browser.get("browser_reported_version") is not None:
        fail(path, f"{label}.browser_reported_version must remain null until isolated capture")
    file_size = browser.get("file_size_bytes")
    if not isinstance(file_size, int) or file_size <= 0:
        fail(path, f"{label}.file_size_bytes must be a positive integer")
    require_string(path, browser, "last_write_time_utc", label)
    sha256 = require_string(path, browser, "sha256", label)
    if not HEX64.fullmatch(sha256):
        fail(path, f"{label}.sha256 must be lowercase SHA-256 hex")
    validate_signature(path, browser.get("signature"), f"{label}.signature")
    require_string_list(path, browser, "registry_observations", label, min_items=2)
    version_state = require_object(path, browser.get("version_state"), f"{label}.version_state")
    require_keys(path, version_state, {"status", "details"}, f"{label}.version_state")
    if require_string(path, version_state, "status", f"{label}.version_state") != "inconsistent_local_metadata":
        fail(path, f"{label}.version_state.status must record inconsistent_local_metadata")
    require_string(path, version_state, "details", f"{label}.version_state")
    relation = require_string(path, browser, "release_catalog_relation", label).lower()
    if "not benchmark eligible" not in relation and "must be resolved" not in relation:
        fail(path, f"{label}.release_catalog_relation must block benchmark eligibility")
    if require_string(path, browser, "local_pin_status", label) != "executable_hash_captured_profile_missing":
        fail(path, f"{label}.local_pin_status must remain executable_hash_captured_profile_missing")
    if browser.get("benchmark_eligible") is not False:
        fail(path, f"{label}.benchmark_eligible must be false")
    missing = " ".join(
        require_string_list(path, browser, "missing_pin_evidence", label, min_items=4)
    ).lower()
    for phrase in ["profile", "command-line", "runner-generated benchmark manifest"]:
        if phrase not in missing:
            fail(path, f"{label}.missing_pin_evidence must mention {phrase}")
    return browser_id


def validate_absent(path: Path, value: object, index: int) -> str:
    label = f"absent_or_unsupported_browsers[{index}]"
    entry = require_object(path, value, label)
    require_keys(path, entry, {"browser_id", "status", "checked_evidence"}, label)
    browser_id = require_string(path, entry, "browser_id", label)
    require_string(path, entry, "status", label)
    require_string_list(path, entry, "checked_evidence", label, min_items=1)
    return browser_id


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    keys = {
        "schema_version",
        "local_install_manifest_id",
        "status",
        "claim_status",
        "captured_at",
        "host_references",
        "capture_scope",
        "observed_browsers",
        "absent_or_unsupported_browsers",
        "unsupported_behavior",
        "evidence_required",
    }
    require_keys(path, manifest, keys, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    manifest_id = require_string(path, manifest, "local_install_manifest_id", "manifest")
    if not MANIFEST_ID.fullmatch(manifest_id):
        fail(path, "local_install_manifest_id has invalid format")
    if manifest.get("status") != "candidate_current_host_unreviewed":
        fail(path, "status must remain candidate_current_host_unreviewed")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in [
        "no browser-reported version proof",
        "no profile",
        "no command line",
        "no benchmark run",
        "no performance claim",
    ]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    require_string(path, manifest, "captured_at", "manifest")
    refs = require_object(path, manifest.get("host_references"), "host_references")
    require_keys(
        path,
        refs,
        {"hardware_id", "os_control_id", "release_catalog_manifest_id"},
        "host_references",
    )
    if refs["hardware_id"] != HARDWARE_ID:
        fail(path, "host_references.hardware_id does not match current benchmark hardware")
    if refs["os_control_id"] != OS_CONTROL_ID:
        fail(path, "host_references.os_control_id does not match current OS-control manifest")
    if refs["release_catalog_manifest_id"] != RELEASE_CATALOG_ID:
        fail(path, "host_references.release_catalog_manifest_id does not match competitor catalog")
    require_string_list(path, manifest, "capture_scope", "manifest", min_items=3)
    observed = manifest.get("observed_browsers")
    if not isinstance(observed, list):
        fail(path, "observed_browsers must be an array")
    observed_ids = [validate_browser(path, item, index) for index, item in enumerate(observed, start=1)]
    if observed_ids != EXPECTED_OBSERVED:
        fail(path, "observed_browsers must list Chrome and Edge local candidates in order")
    absent = manifest.get("absent_or_unsupported_browsers")
    if not isinstance(absent, list):
        fail(path, "absent_or_unsupported_browsers must be an array")
    absent_ids = [validate_absent(path, item, index) for index, item in enumerate(absent, start=1)]
    if absent_ids != EXPECTED_ABSENT:
        fail(path, "absent_or_unsupported_browsers must list Firefox, Safari, and Safari TP in order")
    unsupported = " ".join(
        require_string_list(path, manifest, "unsupported_behavior", "manifest", min_items=4)
    ).lower()
    for phrase in ["no isolated browser-reported version", "no benchmark suite", "no competitor result"]:
        if phrase not in unsupported:
            fail(path, f"unsupported_behavior must mention: {phrase}")
    evidence = " ".join(
        require_string_list(path, manifest, "evidence_required", "manifest", min_items=5)
    ).lower()
    for phrase in ["browser-reported version", "profile", "firefox", "runner-generated benchmark manifest"]:
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
        print(f"benchmark competitor local-install validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark competitor local-install validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
