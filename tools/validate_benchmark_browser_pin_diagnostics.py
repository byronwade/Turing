#!/usr/bin/env python3
"""Validate benchmark browser-pin diagnostic capture manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
MANIFEST_DIR = MACHINE / "benchmark-browser-pin-diagnostics"
DEFAULT_MANIFESTS = [
    MANIFEST_DIR / "current-windows-high-end.chrome-edge.no-claim.2026-07.json"
]

DIAGNOSTIC_ID = re.compile(
    r"^TURING\.BENCHMARK\.BROWSER_PIN_DIAGNOSTIC\.[A-Z0-9._-]+$"
)
SHA256 = re.compile(r"^[a-f0-9]{64}$")
EXPECTED_TARGETS = [
    "chrome-current-host-pin-capture",
    "edge-current-host-pin-capture",
]
EXPECTED_REFS = {
    "hardware_id": "TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07",
    "os_control_id": "TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07",
    "release_catalog_manifest_id": "TURING.BENCHMARK.COMPETITOR_VERSIONS.CURRENT_DESKTOP.2026_07",
    "local_install_manifest_id": "TURING.BENCHMARK.COMPETITOR_LOCAL_INSTALLS.CURRENT_WINDOWS_HIGH_END.2026_07",
    "capture_plan_id": "TURING.BENCHMARK.BROWSER_PIN_CAPTURE.CURRENT_WINDOWS_HIGH_END.2026_07",
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


def require_string_list(path: Path, obj: dict[str, object], key: str, label: str) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        fail(path, f"{label}.{key} must be an array of non-empty strings")
    return value


def validate_artifact_files(path: Path, value: object) -> None:
    files = value
    if not isinstance(files, list) or len(files) < 6:
        fail(path, "artifact_package.artifact_files must include target artifact records")
    seen_kinds: dict[str, set[str]] = {target: set() for target in EXPECTED_TARGETS}
    for index, item in enumerate(files, start=1):
        artifact = require_object(path, item, f"artifact_files[{index}]")
        require_keys(
            path,
            artifact,
            {"target_id", "kind", "path", "bytes", "sha256"},
            f"artifact_files[{index}]",
        )
        target_id = require_string(path, artifact, "target_id", f"artifact_files[{index}]")
        if target_id not in seen_kinds:
            fail(path, f"artifact_files[{index}].target_id is unexpected")
        kind = require_string(path, artifact, "kind", f"artifact_files[{index}]")
        seen_kinds[target_id].add(kind)
        digest = require_string(path, artifact, "sha256", f"artifact_files[{index}]")
        if not SHA256.fullmatch(digest):
            fail(path, f"artifact_files[{index}].sha256 must be lowercase SHA-256")
        bytes_value = artifact.get("bytes")
        if type(bytes_value) is not int or bytes_value < 0:
            fail(path, f"artifact_files[{index}].bytes must be a non-negative integer")
        require_string(path, artifact, "path", f"artifact_files[{index}]")
    for target_id, kinds in seen_kinds.items():
        for required_kind in {"browser-version", "temporary-profile-manifest", "target-summary"}:
            if required_kind not in kinds:
                fail(path, f"{target_id} is missing {required_kind} artifact")


def validate_target(path: Path, value: object, expected_id: str) -> None:
    target = require_object(path, value, expected_id)
    required = {
        "target_id",
        "product_name",
        "local_install_browser_id",
        "release_catalog_browser_id",
        "status",
        "browser_launched",
        "browser_reported_version",
        "local_executable_sha256",
        "profile_source",
        "temporary_profile_cleanup",
        "prohibited_access_detected",
        "profile_hash_status",
        "capture_arguments",
        "observations",
    }
    require_keys(path, target, required, expected_id)
    if target.get("target_id") != expected_id:
        fail(path, f"{expected_id}.target_id is out of order")
    if target.get("status") != "diagnostic_capture_unreviewed":
        fail(path, f"{expected_id}.status must be diagnostic_capture_unreviewed")
    if target.get("browser_launched") is not True:
        fail(path, f"{expected_id}.browser_launched must be true")
    if target.get("temporary_profile_cleanup") != "deleted":
        fail(path, f"{expected_id}.temporary_profile_cleanup must be deleted")
    if target.get("prohibited_access_detected") is not False:
        fail(path, f"{expected_id}.prohibited_access_detected must be false")
    if target.get("profile_hash_status") != "complete":
        fail(path, f"{expected_id}.profile_hash_status must be complete")
    version = require_string(path, target, "browser_reported_version", expected_id)
    if expected_id.startswith("chrome") and not version.startswith("Chrome/"):
        fail(path, "Chrome target must record a Chrome/ browser-reported version")
    if expected_id.startswith("edge") and not version.startswith("Edg/"):
        fail(path, "Edge target must record an Edg/ browser-reported version")
    digest = require_string(path, target, "local_executable_sha256", expected_id)
    if not SHA256.fullmatch(digest):
        fail(path, f"{expected_id}.local_executable_sha256 must be lowercase SHA-256")
    args = require_string_list(path, target, "capture_arguments", expected_id)
    joined = " ".join(args).lower()
    for phrase in ["--user-data-dir=%temp%", "--disable-sync", "--headless=new"]:
        if phrase not in joined:
            fail(path, f"{expected_id}.capture_arguments must include {phrase}")
    observations = " ".join(require_string_list(path, target, "observations", expected_id)).lower()
    if "benchmark" in observations and "not" not in observations:
        fail(path, f"{expected_id}.observations must not imply benchmark evidence")


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "diagnostic_id",
        "status",
        "claim_status",
        "captured_at",
        "tool",
        "host_references",
        "artifact_package",
        "browser_targets",
        "unsupported_behavior",
        "evidence_required",
    }
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    diagnostic_id = require_string(path, manifest, "diagnostic_id", "manifest")
    if not DIAGNOSTIC_ID.fullmatch(diagnostic_id):
        fail(path, "diagnostic_id has invalid format")
    if manifest.get("status") != "no_claim_diagnostic_unreviewed":
        fail(path, "status must be no_claim_diagnostic_unreviewed")
    claim_status = require_string(path, manifest, "claim_status", "manifest").lower()
    for phrase in ["no benchmark run", "no competitor result", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    tool = require_object(path, manifest.get("tool"), "tool")
    require_keys(path, tool, {"path", "command", "artifact_id", "mode", "runner_status"}, "tool")
    if tool.get("path") != "tools/capture_benchmark_browser_pins.py":
        fail(path, "tool.path must point at the browser-pin capture runner")
    if tool.get("mode") != "local_capture":
        fail(path, "tool.mode must be local_capture")
    refs = require_object(path, manifest.get("host_references"), "host_references")
    require_keys(path, refs, set(EXPECTED_REFS), "host_references")
    for key, expected in EXPECTED_REFS.items():
        if refs.get(key) != expected:
            fail(path, f"host_references.{key} does not match current evidence")
    package = require_object(path, manifest.get("artifact_package"), "artifact_package")
    require_keys(
        path,
        package,
        {
            "run_id",
            "storage",
            "raw_artifacts_committed",
            "raw_artifacts_not_committed_reason",
            "capture_summary_sha256",
            "artifact_index_sha256",
            "artifact_files",
        },
        "artifact_package",
    )
    if package.get("raw_artifacts_committed") is not False:
        fail(path, "artifact_package.raw_artifacts_committed must be false")
    for key in ["capture_summary_sha256", "artifact_index_sha256"]:
        digest = require_string(path, package, key, "artifact_package")
        if not SHA256.fullmatch(digest):
            fail(path, f"artifact_package.{key} must be lowercase SHA-256")
    validate_artifact_files(path, package.get("artifact_files"))
    targets = manifest.get("browser_targets")
    if not isinstance(targets, list) or len(targets) != len(EXPECTED_TARGETS):
        fail(path, "browser_targets must contain Chrome and Edge diagnostics")
    for target, expected_id in zip(targets, EXPECTED_TARGETS):
        validate_target(path, target, expected_id)
    unsupported = " ".join(
        require_string_list(path, manifest, "unsupported_behavior", "manifest")
    ).lower()
    for phrase in ["no benchmark", "no competitor comparison", "no timing"]:
        if phrase not in unsupported:
            fail(path, f"unsupported_behavior must mention: {phrase}")
    evidence = " ".join(
        require_string_list(path, manifest, "evidence_required", "manifest")
    ).lower()
    for phrase in ["owner review", "channel", "firefox", "safari"]:
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
        print(f"benchmark browser-pin diagnostic validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark browser-pin diagnostic validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
