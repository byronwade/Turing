#!/usr/bin/env python3
"""Capture no-claim browser-pin artifacts with isolated temporary profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
PLAN_PATH = (
    MACHINE
    / "benchmark-browser-pin-captures"
    / "current-windows-high-end.no-claim.plan.json"
)
LOCAL_INSTALL_PATH = (
    MACHINE
    / "benchmark-competitor-local-installs"
    / "current-windows-high-end.candidate.json"
)

ARTIFACT_ID = "NOCLAIM.BROWSER_PIN_CAPTURE.2026_07"
DEFAULT_HARDWARE_ID = "TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07"
DEFAULT_OS_CONTROL_ID = "TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07"
DEFAULT_RELEASE_CATALOG_ID = (
    "TURING.BENCHMARK.COMPETITOR_VERSIONS.CURRENT_DESKTOP.2026_07"
)
DEFAULT_LOCAL_INSTALL_ID = (
    "TURING.BENCHMARK.COMPETITOR_LOCAL_INSTALLS.CURRENT_WINDOWS_HIGH_END.2026_07"
)
DEFAULT_CAPTURE_PLAN_ID = (
    "TURING.BENCHMARK.BROWSER_PIN_CAPTURE.CURRENT_WINDOWS_HIGH_END.2026_07"
)
CLAIM_STATUS = (
    "browser-pin capture artifact only; no benchmark run, no competitor result, "
    "no latency result, no memory result, no energy result, no compatibility result, "
    "and no performance claim"
)
SELF_TEST_CLAIM_STATUS = (
    "browser-pin capture self-test only; no browser was launched, "
    "no browser-reported version was captured, no benchmark run occurred, "
    "and no performance claim is supported"
)
TEMP_ROOT_NAME = "turing-browser-pin-capture"
DEVTOOLS_VERSION_TIMEOUT_SECONDS = 20
BROWSER_EXIT_TIMEOUT_SECONDS = 8


class CaptureError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CaptureError(f"cannot read {path}: {error}") from error
    if not isinstance(payload, dict):
        raise CaptureError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, root: Path, kind: str) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": str(path.relative_to(root)).replace("\\", "/"),
        "kind": kind,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def profile_file_record(path: Path, root: Path) -> dict[str, object]:
    relative_path = str(path.relative_to(root)).replace("\\", "/")
    try:
        data = path.read_bytes()
    except OSError as error:
        return {
            "path": relative_path,
            "kind": "temporary-profile-file",
            "readable": False,
            "bytes": None,
            "sha256": None,
            "error": str(error),
        }
    return {
        "path": relative_path,
        "kind": "temporary-profile-file",
        "readable": True,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def known_profile_roots() -> list[Path]:
    roots: list[Path] = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    app_data = os.environ.get("APPDATA")
    home = Path.home()
    if local_app_data:
        roots.extend(
            [
                Path(local_app_data) / "Google" / "Chrome" / "User Data",
                Path(local_app_data) / "Microsoft" / "Edge" / "User Data",
                Path(local_app_data) / "Mozilla" / "Firefox" / "Profiles",
            ]
        )
    if app_data:
        roots.append(Path(app_data) / "Mozilla" / "Firefox" / "Profiles")
    roots.extend(
        [
            home / "Library" / "Safari",
            home / "Library" / "Application Support" / "Google" / "Chrome",
            home / "Library" / "Application Support" / "Microsoft Edge",
            home / ".config" / "google-chrome",
            home / ".config" / "microsoft-edge",
            home / ".mozilla" / "firefox",
        ]
    )
    return roots


def prepare_output_dir(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.exists() and any(resolved.iterdir()):
        raise CaptureError(f"output directory must be empty: {resolved}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def temp_profile_root(run_id: str) -> Path:
    return Path(tempfile.gettempdir()) / TEMP_ROOT_NAME / run_id


def ensure_temporary_profile_path(path: Path, run_root: Path) -> dict[str, Any]:
    resolved = path.resolve()
    run_root_resolved = run_root.resolve()
    if not path_is_relative_to(resolved, run_root_resolved):
        raise CaptureError(f"profile path is outside runner temp root: {resolved}")
    prohibited_roots = [root.resolve() for root in known_profile_roots()]
    for root in prohibited_roots:
        if path_is_relative_to(resolved, root):
            raise CaptureError(f"profile path points under a real browser profile root: {resolved}")
    return {
        "status": "passed_configured_paths_only",
        "profile_path": str(resolved),
        "runner_temp_root": str(run_root_resolved),
        "prohibited_roots_checked": [str(root) for root in prohibited_roots],
        "prohibited_access_detected": False,
        "limitations": [
            "The runner rejects configured profile paths under known real browser profile roots.",
            "This check is not an OS-level filesystem access monitor.",
        ],
    }


def load_plan_targets() -> list[dict[str, Any]]:
    plan = load_json(PLAN_PATH)
    targets = plan.get("browser_targets")
    if not isinstance(targets, list):
        raise CaptureError("browser pin capture plan has no browser_targets array")
    normalized: list[dict[str, Any]] = []
    for item in targets:
        if not isinstance(item, dict):
            raise CaptureError("browser pin capture plan target must be an object")
        normalized.append(item)
    return normalized


def load_local_installs() -> dict[str, dict[str, Any]]:
    manifest = load_json(LOCAL_INSTALL_PATH)
    observed = manifest.get("observed_browsers")
    if not isinstance(observed, list):
        raise CaptureError("local install manifest has no observed_browsers array")
    installs: dict[str, dict[str, Any]] = {}
    for item in observed:
        if not isinstance(item, dict):
            raise CaptureError("local install browser item must be an object")
        browser_id = item.get("browser_id")
        if isinstance(browser_id, str):
            installs[browser_id] = item
    return installs


def select_targets(
    plan_targets: list[dict[str, Any]], requested: list[str] | None
) -> list[dict[str, Any]]:
    if not requested:
        return [
            target
            for target in plan_targets
            if target.get("status") == "planned_from_local_executable"
        ]
    aliases: dict[str, dict[str, Any]] = {}
    for target in plan_targets:
        target_id = str(target.get("target_id", ""))
        aliases[target_id] = target
        product_name = str(target.get("product_name", "")).lower()
        if "chrome" in product_name:
            aliases["chrome"] = target
        if "edge" in product_name:
            aliases["edge"] = target
        if "firefox" in product_name:
            aliases["firefox"] = target
    selected: list[dict[str, Any]] = []
    for name in requested:
        target = aliases.get(name.lower())
        if target is None:
            raise CaptureError(f"unknown browser target: {name}")
        selected.append(target)
    return selected


def replaced_capture_args(target: dict[str, Any], profile_dir: Path) -> list[str]:
    raw_args = target.get("planned_capture_arguments")
    if not isinstance(raw_args, list) or any(not isinstance(arg, str) for arg in raw_args):
        raise CaptureError("planned_capture_arguments must be an array of strings")
    replaced: list[str] = []
    for arg in raw_args:
        if arg.startswith("--user-data-dir="):
            replaced.append(f"--user-data-dir={profile_dir}")
        else:
            replaced.append(
                arg.replace(
                    "%TEMP%\\turing-browser-pin-capture\\${run_id}",
                    str(profile_dir.parent),
                )
            )
    if not any(arg.startswith("--user-data-dir=") for arg in replaced):
        replaced.append(f"--user-data-dir={profile_dir}")
    added = [
        "--headless=new",
        "--remote-debugging-port=0",
        "--host-resolver-rules=MAP * 127.0.0.1, EXCLUDE localhost",
        "about:blank",
    ]
    return replaced + [arg for arg in added if arg not in replaced]


def wait_for_devtools_version(profile_dir: Path) -> tuple[dict[str, Any], str]:
    active_port = profile_dir / "DevToolsActivePort"
    deadline = time.monotonic() + DEVTOOLS_VERSION_TIMEOUT_SECONDS
    last_error = ""
    while time.monotonic() < deadline:
        if active_port.exists():
            lines = active_port.read_text(encoding="utf-8", errors="replace").splitlines()
            if lines:
                port = lines[0].strip()
                if port.isdigit():
                    url = f"http://127.0.0.1:{port}/json/version"
                    try:
                        with urllib.request.urlopen(url, timeout=2) as response:
                            payload = json.loads(response.read().decode("utf-8"))
                        if isinstance(payload, dict):
                            return payload, url
                        last_error = "DevTools version endpoint did not return an object"
                    except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
                        last_error = str(error)
        time.sleep(0.25)
    raise CaptureError(last_error or "timed out waiting for DevTools version endpoint")


def kill_windows_process_tree(pid: int) -> dict[str, Any] | None:
    if os.name != "nt":
        return None
    result = subprocess.run(
        ["taskkill", "/PID", str(pid), "/T", "/F"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "command": ["taskkill", "/PID", str(pid), "/T", "/F"],
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def stop_windows_processes_for_path(path: Path) -> dict[str, Any] | None:
    if os.name != "nt":
        return None
    needle = str(path)
    escaped = needle.replace("'", "''")
    script = (
        f"$needle = '{escaped}'; "
        "$matches = Get-CimInstance Win32_Process "
        "-Filter \"name='chrome.exe' or name='msedge.exe' or name='firefox.exe'\" | "
        "Where-Object { $_.CommandLine -like \"*$needle*\" }; "
        "$records = @(); "
        "foreach ($process in $matches) { "
        "$records += [pscustomobject]@{ProcessId=$process.ProcessId;Name=$process.Name}; "
        "Stop-Process -Id $process.ProcessId -Force -ErrorAction SilentlyContinue "
        "}; "
        "$records | ConvertTo-Json -Compress"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "command": "Stop browser processes whose command line contains the temp profile path",
        "path": needle,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def terminate_process(process: subprocess.Popen[str]) -> dict[str, Any]:
    taskkill_record = None
    if process.poll() is None:
        taskkill_record = kill_windows_process_tree(process.pid)
        if taskkill_record is None:
            process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=BROWSER_EXIT_TIMEOUT_SECONDS)
        killed = False
    except subprocess.TimeoutExpired:
        if taskkill_record is None:
            taskkill_record = kill_windows_process_tree(process.pid)
        if taskkill_record is None:
            process.kill()
        stdout, stderr = process.communicate(timeout=BROWSER_EXIT_TIMEOUT_SECONDS)
        killed = True
    return {
        "exit_code": process.returncode,
        "terminated_by_runner": True,
        "force_killed": killed,
        "process_tree_kill": taskkill_record,
        "stdout": stdout,
        "stderr": stderr,
    }


def hash_profile(profile_dir: Path) -> dict[str, Any]:
    files: list[dict[str, object]] = []
    if profile_dir.exists():
        for path in sorted(profile_dir.rglob("*")):
            if path.is_file():
                files.append(profile_file_record(path, profile_dir))
    unreadable = [item for item in files if item.get("readable") is False]
    return {
        "schema_version": 1,
        "profile_path": str(profile_dir),
        "file_count": len(files),
        "readable_file_count": len(files) - len(unreadable),
        "unreadable_file_count": len(unreadable),
        "files": files,
    }


def cleanup_profile(profile_dir: Path, *, keep_profile: bool) -> dict[str, Any]:
    if keep_profile:
        return {"status": "kept_by_operator", "path": str(profile_dir)}
    if not profile_dir.exists():
        return {"status": "not_present", "path": str(profile_dir)}
    for attempt in range(1, 6):
        try:
            shutil.rmtree(profile_dir)
            return {"status": "deleted", "path": str(profile_dir), "attempts": attempt}
        except OSError as error:
            if attempt == 5:
                return {
                    "status": "delete_failed",
                    "path": str(profile_dir),
                    "attempts": attempt,
                    "error": str(error),
                }
            time.sleep(0.75)
    return {"status": "delete_failed", "path": str(profile_dir), "attempts": 5}


def target_slug(target_id: str) -> str:
    return "".join(char if char.isalnum() or char in "-_" else "-" for char in target_id)


def write_target_artifacts(
    output_dir: Path,
    target_id: str,
    target_summary: dict[str, Any],
    version_payload: dict[str, Any] | None,
    profile_manifest: dict[str, Any] | None,
    stdout: str,
    stderr: str,
) -> list[dict[str, object]]:
    target_dir = output_dir / "targets" / target_slug(target_id)
    files: list[dict[str, object]] = []
    if version_payload is not None:
        version_path = target_dir / "version.json"
        write_json(version_path, version_payload)
        files.append(file_record(version_path, output_dir, "browser-version"))
    if profile_manifest is not None:
        profile_path = target_dir / "temporary-profile-manifest.json"
        write_json(profile_path, profile_manifest)
        files.append(file_record(profile_path, output_dir, "temporary-profile-manifest"))
    stdout_path = target_dir / "stdout.txt"
    stderr_path = target_dir / "stderr.txt"
    write_text(stdout_path, stdout)
    write_text(stderr_path, stderr)
    files.append(file_record(stdout_path, output_dir, "stdout"))
    files.append(file_record(stderr_path, output_dir, "stderr"))
    summary_path = target_dir / "target-summary.json"
    target_summary["artifact_files"] = files.copy()
    write_json(summary_path, target_summary)
    files.append(file_record(summary_path, output_dir, "target-summary"))
    return files


def blocked_target_summary(target: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target_id": target.get("target_id"),
        "product_name": target.get("product_name"),
        "status": "blocked",
        "blocked_reason": reason,
        "browser_launched": False,
        "temporary_profile_created": False,
        "browser_reported_version": None,
        "unsupported": [
            "no browser was launched for this target",
            "no browser-reported version was captured",
            "no benchmark ran and no comparison claim is supported",
        ],
    }


def capture_target(
    target: dict[str, Any],
    local_installs: dict[str, dict[str, Any]],
    output_dir: Path,
    run_root: Path,
    *,
    keep_profiles: bool,
) -> tuple[dict[str, Any], list[dict[str, object]]]:
    target_id = str(target.get("target_id"))
    status = target.get("status")
    if status != "planned_from_local_executable":
        summary = blocked_target_summary(target, f"target status is {status}")
        files = write_target_artifacts(output_dir, target_id, summary, None, None, "", "")
        return summary, files

    local_id = target.get("local_install_browser_id")
    if not isinstance(local_id, str) or local_id not in local_installs:
        summary = blocked_target_summary(target, "local install evidence is missing")
        files = write_target_artifacts(output_dir, target_id, summary, None, None, "", "")
        return summary, files
    local = local_installs[local_id]
    executable = local.get("executable_path")
    if not isinstance(executable, str) or not Path(executable).is_file():
        summary = blocked_target_summary(target, f"executable is missing: {executable}")
        files = write_target_artifacts(output_dir, target_id, summary, None, None, "", "")
        return summary, files

    profile_dir = run_root / target_slug(target_id)
    profile_dir.mkdir(parents=True, exist_ok=True)
    prohibited_check = ensure_temporary_profile_path(profile_dir, run_root)
    args = replaced_capture_args(target, profile_dir)
    command = [executable, *args]
    version_payload: dict[str, Any] | None = None
    version_url = None
    lingering_process_cleanup = None
    process_record: dict[str, Any] = {
        "exit_code": None,
        "terminated_by_runner": False,
        "force_killed": False,
        "stdout": "",
        "stderr": "",
    }
    capture_status = "failed"
    failure = None
    started_at = utc_now()

    try:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        try:
            version_payload, version_url = wait_for_devtools_version(profile_dir)
            capture_status = "diagnostic_capture_unreviewed"
        finally:
            process_record = terminate_process(process)
            lingering_process_cleanup = stop_windows_processes_for_path(profile_dir)
            time.sleep(0.5)
    except (OSError, CaptureError) as error:
        failure = str(error)
        lingering_process_cleanup = stop_windows_processes_for_path(profile_dir)
        time.sleep(0.5)
    profile_manifest = hash_profile(profile_dir)
    cleanup = cleanup_profile(profile_dir, keep_profile=keep_profiles)
    browser_reported_version = None
    if version_payload is not None:
        browser_value = version_payload.get("Browser")
        if isinstance(browser_value, str):
            browser_reported_version = browser_value

    target_summary: dict[str, Any] = {
        "schema_version": 1,
        "target_id": target_id,
        "product_name": target.get("product_name"),
        "status": capture_status,
        "started_at": started_at,
        "completed_at": utc_now(),
        "browser_launched": capture_status == "diagnostic_capture_unreviewed",
        "browser_reported_version": browser_reported_version,
        "browser_version_endpoint": version_url,
        "local_install_browser_id": local_id,
        "local_executable_path": executable,
        "local_executable_sha256": local.get("sha256"),
        "requested_command_line": command,
        "effective_command_line_status": (
            "runner-requested command line recorded; process-tree command line "
            "not independently audited"
        ),
        "temporary_profile_created": True,
        "temporary_profile_path": str(profile_dir),
        "temporary_profile_cleanup": cleanup,
        "prohibited_path_check": prohibited_check,
        "process": {
            "exit_code": process_record.get("exit_code"),
            "terminated_by_runner": process_record.get("terminated_by_runner"),
            "force_killed": process_record.get("force_killed"),
            "process_tree_kill": process_record.get("process_tree_kill"),
            "lingering_process_cleanup": lingering_process_cleanup,
        },
        "settings_state": {
            "profile_source": "runner-owned temporary profile",
            "network_policy": "capture requested about:blank and host resolver mapping to loopback",
            "update_state": "not triggered by runner; local-install metadata remains the only update evidence",
            "extension_state": "new temporary profile; extension enumeration not implemented",
            "cache_state": "new temporary profile; profile file hashes captured before cleanup",
            "sync_account_state": "capture arguments request sync disabled; account state not attached by runner",
            "sandbox_site_isolation_state": "not independently proven by this diagnostic capture",
            "workload_argument_status": (
                "capture-only arguments are not approved benchmark workload arguments"
            ),
        },
        "unsupported": [
            "no benchmark suite or corpus page was loaded",
            "no timing, memory, CPU, GPU, energy, accessibility, or compatibility sample was collected",
            "no competitor comparison, ranking, regression, or performance claim is supported",
            "diagnostic capture arguments are not benchmark workload arguments",
        ],
    }
    if failure is not None:
        target_summary["failure"] = failure
        target_summary["browser_launched"] = False
        target_summary["unsupported"].append("browser-reported version capture failed")
    if profile_manifest.get("unreadable_file_count", 0):
        target_summary["status"] = f"{target_summary['status']}_profile_hash_incomplete"
        target_summary["unsupported"].append(
            "one or more temporary profile files were not readable for hashing"
        )
    if cleanup.get("status") != "deleted" and not keep_profiles:
        target_summary["unsupported"].append("temporary profile cleanup did not complete")
    files = write_target_artifacts(
        output_dir,
        target_id,
        target_summary,
        version_payload,
        profile_manifest,
        str(process_record.get("stdout", "")),
        str(process_record.get("stderr", "")),
    )
    return target_summary, files


def self_test_target(
    output_dir: Path, run_root: Path, *, keep_profiles: bool
) -> tuple[dict[str, Any], list[dict[str, object]]]:
    target_id = "self-test-no-browser-pin-capture"
    profile_dir = run_root / target_id
    profile_dir.mkdir(parents=True, exist_ok=True)
    marker = profile_dir / "SELF_TEST_PROFILE_MARKER.txt"
    marker.write_text("runner-owned temporary profile self-test\n", encoding="utf-8")
    prohibited_check = ensure_temporary_profile_path(profile_dir, run_root)
    profile_manifest = hash_profile(profile_dir)
    cleanup = cleanup_profile(profile_dir, keep_profile=keep_profiles)
    target_summary: dict[str, Any] = {
        "schema_version": 1,
        "target_id": target_id,
        "product_name": "Browser pin capture self-test",
        "status": "self_test_no_browser",
        "browser_launched": False,
        "browser_reported_version": None,
        "requested_command_line": [],
        "effective_command_line_status": "not captured because no browser was launched",
        "temporary_profile_created": True,
        "temporary_profile_path": str(profile_dir),
        "temporary_profile_cleanup": cleanup,
        "prohibited_path_check": prohibited_check,
        "unsupported": [
            "no browser was launched",
            "no browser-reported version was captured",
            "no benchmark ran and no comparison claim is supported",
        ],
    }
    files = write_target_artifacts(
        output_dir,
        target_id,
        target_summary,
        None,
        profile_manifest,
        "",
        "",
    )
    return target_summary, files


def write_run_artifacts(
    output_dir: Path,
    *,
    run_id: str,
    mode: str,
    persisted: bool,
    target_summaries: list[dict[str, Any]],
    target_files: list[dict[str, object]],
) -> dict[str, Any]:
    generated_at = utc_now()
    run_summary: dict[str, Any] = {
        "schema_version": 1,
        "artifact_id": ARTIFACT_ID,
        "run_id": run_id,
        "generated_at": generated_at,
        "mode": mode,
        "status": "no_claim_artifact_package",
        "claim_status": SELF_TEST_CLAIM_STATUS if mode == "self_test" else CLAIM_STATUS,
        "hardware_id": DEFAULT_HARDWARE_ID,
        "os_control_id": DEFAULT_OS_CONTROL_ID,
        "release_catalog_manifest_id": DEFAULT_RELEASE_CATALOG_ID,
        "local_install_manifest_id": DEFAULT_LOCAL_INSTALL_ID,
        "capture_plan_id": DEFAULT_CAPTURE_PLAN_ID,
        "output_dir": str(output_dir),
        "output_dir_persisted": persisted,
        "target_summaries": target_summaries,
        "unsupported": [
            "no benchmark result is present",
            "no comparison, ranking, regression, release, or performance claim is allowed",
            "capture-only arguments must be separately reviewed before benchmark use",
        ],
    }
    summary_path = output_dir / "capture-summary.json"
    write_json(summary_path, run_summary)
    summary_record = file_record(summary_path, output_dir, "capture-summary")
    index_payload: dict[str, Any] = {
        "schema_version": 1,
        "artifact_id": f"{ARTIFACT_ID}.INDEX",
        "generated_at": generated_at,
        "run_id": run_id,
        "claim_status": run_summary["claim_status"],
        "files": [*target_files, summary_record],
    }
    index_path = output_dir / "artifact-index.json"
    write_json(index_path, index_payload)
    index_record = file_record(index_path, output_dir, "artifact-index")
    run_summary["artifact_files"] = [*target_files, summary_record, index_record]
    validate_summary(output_dir, run_summary)
    return run_summary


def validate_summary(output_dir: Path, summary: dict[str, Any]) -> None:
    if summary.get("artifact_id") != ARTIFACT_ID:
        raise CaptureError("summary has the wrong artifact_id")
    claim_status = summary.get("claim_status")
    if not isinstance(claim_status, str):
        raise CaptureError("summary is missing claim_status")
    for phrase in ["no benchmark", "no performance claim"]:
        if phrase not in claim_status:
            raise CaptureError(f"summary claim_status must mention: {phrase}")
    for key, expected in {
        "hardware_id": DEFAULT_HARDWARE_ID,
        "os_control_id": DEFAULT_OS_CONTROL_ID,
        "release_catalog_manifest_id": DEFAULT_RELEASE_CATALOG_ID,
        "local_install_manifest_id": DEFAULT_LOCAL_INSTALL_ID,
        "capture_plan_id": DEFAULT_CAPTURE_PLAN_ID,
    }.items():
        if summary.get(key) != expected:
            raise CaptureError(f"summary {key} does not match current registry evidence")
    files = summary.get("artifact_files")
    if not isinstance(files, list) or not files:
        raise CaptureError("summary must include artifact_files")
    output_root = output_dir.resolve()
    for file_value in files:
        if not isinstance(file_value, dict):
            raise CaptureError("artifact file records must be objects")
        relative_path = file_value.get("path")
        expected_sha = file_value.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_sha, str):
            raise CaptureError("artifact file records need path and sha256")
        actual_path = (output_root / relative_path).resolve()
        if not path_is_relative_to(actual_path, output_root):
            raise CaptureError(f"artifact file points outside package: {relative_path}")
        if not actual_path.is_file():
            raise CaptureError(f"artifact file is missing: {relative_path}")
        if sha256_file(actual_path) != expected_sha:
            raise CaptureError(f"artifact file hash mismatch: {relative_path}")
    targets = summary.get("target_summaries")
    if not isinstance(targets, list) or not targets:
        raise CaptureError("summary must include target_summaries")
    for target in targets:
        if not isinstance(target, dict):
            raise CaptureError("target_summaries entries must be objects")
        check = target.get("prohibited_path_check")
        if isinstance(check, dict) and check.get("prohibited_access_detected") is not False:
            raise CaptureError("prohibited_path_check must not report prohibited access")


def run_self_test(output_dir: Path, *, persisted: bool, keep_profiles: bool) -> dict[str, Any]:
    run_id = f"self-test-{uuid.uuid4().hex[:12]}"
    output_dir = prepare_output_dir(output_dir)
    run_root = temp_profile_root(run_id)
    run_root.mkdir(parents=True, exist_ok=True)
    target_summary, target_files = self_test_target(
        output_dir, run_root, keep_profiles=keep_profiles
    )
    return write_run_artifacts(
        output_dir,
        run_id=run_id,
        mode="self_test",
        persisted=persisted,
        target_summaries=[target_summary],
        target_files=target_files,
    )


def run_local_capture(
    output_dir: Path,
    *,
    persisted: bool,
    keep_profiles: bool,
    requested_targets: list[str] | None,
) -> dict[str, Any]:
    run_id = f"local-{uuid.uuid4().hex[:12]}"
    output_dir = prepare_output_dir(output_dir)
    run_root = temp_profile_root(run_id)
    run_root.mkdir(parents=True, exist_ok=True)
    plan_targets = load_plan_targets()
    targets = select_targets(plan_targets, requested_targets)
    local_installs = load_local_installs()
    summaries: list[dict[str, Any]] = []
    files: list[dict[str, object]] = []
    for target in targets:
        summary, target_files = capture_target(
            target,
            local_installs,
            output_dir,
            run_root,
            keep_profiles=keep_profiles,
        )
        summaries.append(summary)
        files.extend(target_files)
    return write_run_artifacts(
        output_dir,
        run_id=run_id,
        mode="local_capture",
        persisted=persisted,
        target_summaries=summaries,
        target_files=files,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--capture-local", action="store_true")
    parser.add_argument("--target", action="append", help="target id or chrome/edge/firefox")
    parser.add_argument("--keep-profiles", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.output_dir is not None:
            output_dir = args.output_dir
            persisted = True
            if args.self_test:
                summary = run_self_test(
                    output_dir, persisted=persisted, keep_profiles=args.keep_profiles
                )
            else:
                summary = run_local_capture(
                    output_dir,
                    persisted=persisted,
                    keep_profiles=args.keep_profiles,
                    requested_targets=args.target,
                )
        else:
            prefix = "turing-browser-pin-self-test-" if args.self_test else "turing-browser-pin-"
            with tempfile.TemporaryDirectory(prefix=prefix) as tmp:
                output_dir = Path(tmp)
                if args.self_test:
                    summary = run_self_test(
                        output_dir, persisted=False, keep_profiles=args.keep_profiles
                    )
                else:
                    summary = run_local_capture(
                        output_dir,
                        persisted=False,
                        keep_profiles=args.keep_profiles,
                        requested_targets=args.target,
                    )
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except CaptureError as error:
        print(f"browser pin capture failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
