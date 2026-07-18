#!/usr/bin/env python3
"""Validate the no-claim browser launch-runner envelope without launching browsers."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
CONTRACT = (
    MACHINE
    / "benchmark-launch-runners"
    / "no-claim-browser-launch.plan.json"
)
CONTRACT_VALIDATOR = ROOT / "tools" / "validate_benchmark_launch_runners.py"

ARTIFACT_ID = "NOCLAIM.BENCHMARK_BROWSER_LAUNCH_SELF_TEST.2026_07"
LAUNCH_RUNNER_ID = "TURING.BENCHMARK.LAUNCH_RUNNER.NOCLAIM_BROWSER_LAUNCH.2026_07"
DEFAULT_HARDWARE_ID = "TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07"
DEFAULT_OS_CONTROL_ID = "TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07"
DEFAULT_CORPUS_ID = "TURING.CORPUS.NOCLAIM_SMOKE.2026_07"
DEFAULT_NETWORK_PROFILE_ID = "TURING.NETWORK.NOCLAIM_LOCAL_STATIC.2026_07"
DEFAULT_BROWSER_PIN_ID = (
    "TURING.BENCHMARK.BROWSER_PIN_DIAGNOSTIC.CURRENT_WINDOWS_HIGH_END.CHROME_EDGE.2026_07"
)
DEFAULT_TAB_SCENARIO_SET_ID = (
    "TURING.BENCHMARK.TAB_SCENARIOS.NOCLAIM_30_TAB_SMOKE.2026_07"
)

FORBIDDEN_ARGUMENTS = [
    "--use-default-profile",
    "--allow-real-profile",
    "--skip-failures",
    "--ignore-timeouts",
    "--disable-sandbox-for-benchmark",
    "--allow-network-downloads",
    "--claim",
]
REQUIRED_ARGUMENTS = [
    "--hardware-id",
    "--os-control-id",
    "--corpus-id",
    "--network-profile-id",
    "--browser-pin-id",
    "--tab-scenario-set-id",
    "--artifact-root",
    "--claim-mode",
]
CLAIM_STATUS = (
    "browser launch-runner self-test only; no browser run, no browser launched, "
    "no benchmark result, no trace captured, no raw sample, no memory result, "
    "no energy result, no competitor result, no Chrome-class claim, and no performance claim"
)


class LaunchRunnerError(RuntimeError):
    pass


class ParserError(LaunchRunnerError):
    pass


class NoExitArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ParserError(message)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LaunchRunnerError(f"cannot read JSON from {path}: {error}") from error


def require_object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise LaunchRunnerError(f"{label} must be an object")
    return value


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


def find_forbidden_arguments(argv: list[str]) -> list[str]:
    found: list[str] = []
    for token in argv:
        for forbidden in FORBIDDEN_ARGUMENTS:
            if token == forbidden or token.startswith(f"{forbidden}="):
                found.append(forbidden)
    return found


def parser() -> NoExitArgumentParser:
    cli = NoExitArgumentParser(description=__doc__)
    cli.add_argument("--self-test", action="store_true")
    cli.add_argument("--validate-contract", action="store_true")
    cli.add_argument("--hardware-id", default=DEFAULT_HARDWARE_ID)
    cli.add_argument("--os-control-id", default=DEFAULT_OS_CONTROL_ID)
    cli.add_argument("--corpus-id", default=DEFAULT_CORPUS_ID)
    cli.add_argument("--network-profile-id", default=DEFAULT_NETWORK_PROFILE_ID)
    cli.add_argument("--browser-pin-id", default=DEFAULT_BROWSER_PIN_ID)
    cli.add_argument("--tab-scenario-set-id", default=DEFAULT_TAB_SCENARIO_SET_ID)
    cli.add_argument("--artifact-root", type=Path)
    cli.add_argument("--claim-mode", default="no-claim", choices=["no-claim"])
    return cli


def parse_args(argv: list[str]) -> argparse.Namespace:
    forbidden = find_forbidden_arguments(argv)
    if forbidden:
        raise ParserError(
            "forbidden browser launch-runner argument is not allowed: "
            + ", ".join(sorted(set(forbidden)))
        )
    args = parser().parse_args(argv)
    if args.self_test and args.validate_contract:
        raise ParserError("choose either --self-test or --validate-contract")
    if not args.self_test and not args.validate_contract:
        raise ParserError("pass --self-test or --validate-contract")
    return args


def prepare_artifact_root(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.exists() and any(resolved.iterdir()):
        raise LaunchRunnerError(f"artifact root must be empty: {resolved}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def run_contract_validator() -> str:
    result = subprocess.run(
        [sys.executable, "-B", str(CONTRACT_VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        raise LaunchRunnerError(detail or "benchmark launch-runner contract validation failed")
    return result.stdout.strip()


def contract_references() -> dict[str, str]:
    payload = require_object(load_json(CONTRACT), "contract")
    if payload.get("launch_runner_id") != LAUNCH_RUNNER_ID:
        raise LaunchRunnerError("contract launch_runner_id does not match the self-test")
    references = require_object(payload.get("registry_references"), "registry_references")
    expected = {
        "hardware_id": DEFAULT_HARDWARE_ID,
        "os_control_id": DEFAULT_OS_CONTROL_ID,
        "corpus_id": DEFAULT_CORPUS_ID,
        "network_profile_id": DEFAULT_NETWORK_PROFILE_ID,
        "browser_pin_diagnostic_id": DEFAULT_BROWSER_PIN_ID,
        "tab_scenario_set_id": DEFAULT_TAB_SCENARIO_SET_ID,
    }
    for key, value in expected.items():
        if references.get(key) != value:
            raise LaunchRunnerError(f"contract registry_references.{key} does not match")
    return {key: str(value) for key, value in references.items() if isinstance(value, str)}


def argument_validation_case(output_dir: Path) -> dict[str, Any]:
    explicit_valid_argv = [
        "--validate-contract",
        "--hardware-id",
        DEFAULT_HARDWARE_ID,
        "--os-control-id",
        DEFAULT_OS_CONTROL_ID,
        "--corpus-id",
        DEFAULT_CORPUS_ID,
        "--network-profile-id",
        DEFAULT_NETWORK_PROFILE_ID,
        "--browser-pin-id",
        DEFAULT_BROWSER_PIN_ID,
        "--tab-scenario-set-id",
        DEFAULT_TAB_SCENARIO_SET_ID,
        "--artifact-root",
        str(output_dir),
        "--claim-mode",
        "no-claim",
    ]
    parsed = parse_args(explicit_valid_argv)
    parsed_arguments = {
        "hardware_id": parsed.hardware_id,
        "os_control_id": parsed.os_control_id,
        "corpus_id": parsed.corpus_id,
        "network_profile_id": parsed.network_profile_id,
        "browser_pin_id": parsed.browser_pin_id,
        "tab_scenario_set_id": parsed.tab_scenario_set_id,
        "artifact_root": str(parsed.artifact_root),
        "claim_mode": parsed.claim_mode,
    }
    forbidden_checks: list[dict[str, object]] = []
    for forbidden in FORBIDDEN_ARGUMENTS:
        token = forbidden if forbidden == "--claim" else f"{forbidden}=1"
        try:
            parse_args(["--self-test", token])
        except ParserError as error:
            forbidden_checks.append(
                {
                    "argument": forbidden,
                    "status": "rejected",
                    "message": str(error),
                }
            )
        else:
            raise LaunchRunnerError(f"forbidden argument was accepted: {forbidden}")
    try:
        parse_args(["--self-test", "--claim-mode", "performance"])
    except ParserError as error:
        invalid_claim_mode = {"status": "rejected", "message": str(error)}
    else:
        raise LaunchRunnerError("--claim-mode accepted a claiming value")
    parsed_no_claim = parse_args(["--self-test", "--claim-mode", "no-claim"])
    if parsed_no_claim.claim_mode != "no-claim":
        raise LaunchRunnerError("--claim-mode no-claim did not parse correctly")
    return {
        "schema_version": 1,
        "status": "passed",
        "required_arguments_checked": REQUIRED_ARGUMENTS,
        "parsed_arguments": parsed_arguments,
        "forbidden_arguments_checked": forbidden_checks,
        "invalid_claim_mode_check": invalid_claim_mode,
        "claim_mode_no_claim_check": "accepted",
        "browser_launched": False,
    }


def artifact_root_validation_case() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="turing-launch-artifact-root-check-") as tmp:
        candidate = Path(tmp) / "candidate"
        prepared = prepare_artifact_root(candidate)
        marker = prepared / "existing.json"
        write_json(marker, {"status": "non_empty_root_marker"})
        try:
            prepare_artifact_root(prepared)
        except LaunchRunnerError as error:
            rejected_non_empty = {"status": "rejected", "message": str(error)}
        else:
            raise LaunchRunnerError("non-empty artifact root was accepted")
    return {
        "schema_version": 1,
        "status": "passed",
        "empty_root_created": True,
        "non_empty_root_check": rejected_non_empty,
        "real_profile_accessed": False,
        "browser_launched": False,
    }


def validate_summary(output_dir: Path, summary: dict[str, Any]) -> None:
    if summary.get("artifact_id") != ARTIFACT_ID:
        raise LaunchRunnerError("summary has the wrong artifact_id")
    claim_status = summary.get("claim_status")
    if not isinstance(claim_status, str):
        raise LaunchRunnerError("summary is missing claim_status")
    for phrase in [
        "no browser run",
        "no browser launched",
        "no benchmark result",
        "no performance claim",
    ]:
        if phrase not in claim_status:
            raise LaunchRunnerError(f"summary claim_status must mention: {phrase}")
    if summary.get("browser_launched") is not False:
        raise LaunchRunnerError("summary must state browser_launched=false")
    if summary.get("benchmark_result_generated") is not False:
        raise LaunchRunnerError("summary must state benchmark_result_generated=false")
    if summary.get("claim_mode") != "no-claim":
        raise LaunchRunnerError("summary must keep claim_mode=no-claim")
    files = summary.get("artifact_files")
    if not isinstance(files, list) or len(files) != 5:
        raise LaunchRunnerError("summary must include five artifact files")
    resolved_root = output_dir.resolve()
    for item in files:
        file_item = require_object(item, "artifact_file")
        relative_path = file_item.get("path")
        expected_sha = file_item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_sha, str):
            raise LaunchRunnerError("artifact file records need path and sha256")
        actual_path = (output_dir / relative_path).resolve()
        try:
            actual_path.relative_to(resolved_root)
        except ValueError as error:
            raise LaunchRunnerError(f"artifact path escapes root: {relative_path}") from error
        if not actual_path.is_file():
            raise LaunchRunnerError(f"artifact file is missing: {relative_path}")
        if sha256_file(actual_path) != expected_sha:
            raise LaunchRunnerError(f"artifact file hash mismatch: {relative_path}")


def run_launch_self_test(
    artifact_root: Path,
    *,
    persisted: bool,
    args: argparse.Namespace,
) -> dict[str, Any]:
    output_dir = prepare_artifact_root(artifact_root)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    references = contract_references()
    contract_validator_output = run_contract_validator()

    contract_validation = {
        "schema_version": 1,
        "status": "passed",
        "validator": "tools/validate_benchmark_launch_runners.py",
        "validator_output": contract_validator_output,
        "contract_path": "docs/blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json",
        "launch_runner_id": LAUNCH_RUNNER_ID,
        "registry_references_checked": references,
        "browser_launched": False,
        "benchmark_result_generated": False,
    }
    argument_validation = argument_validation_case(output_dir)
    artifact_root_validation = artifact_root_validation_case()
    no_claim_finalization = {
        "schema_version": 1,
        "status": "passed",
        "claim_mode": args.claim_mode,
        "claim_status": CLAIM_STATUS,
        "browser_launched": False,
        "benchmark_result_generated": False,
        "trace_captured": False,
        "raw_sample_generated": False,
        "unsupported": [
            "no browser process is launched",
            "no page is loaded by Turing or any competitor browser",
            "no trace, raw sample, memory snapshot, power sample, or artifact package is generated",
            "no comparison, Chrome-class, daily-driver, beta, stable, security, compatibility, accessibility, or performance claim is allowed",
        ],
    }

    contract_path = output_dir / "contract-validation.json"
    argument_path = output_dir / "argument-validation.json"
    artifact_root_path = output_dir / "artifact-root-validation.json"
    finalization_path = output_dir / "no-claim-finalization.json"
    index_path = output_dir / "artifact-index.json"

    write_json(contract_path, contract_validation)
    write_json(argument_path, argument_validation)
    write_json(artifact_root_path, artifact_root_validation)
    write_json(finalization_path, no_claim_finalization)

    files = [
        file_record(contract_path, output_dir, "contract-validation"),
        file_record(argument_path, output_dir, "argument-validation"),
        file_record(artifact_root_path, output_dir, "artifact-root-validation"),
        file_record(finalization_path, output_dir, "no-claim-finalization"),
    ]
    artifact_index = {
        "schema_version": 1,
        "artifact_id": f"{ARTIFACT_ID}.INDEX",
        "generated_at": generated_at,
        "claim_status": CLAIM_STATUS,
        "launch_runner_id": LAUNCH_RUNNER_ID,
        "files": files,
        "browser_launched": False,
        "benchmark_result_generated": False,
    }
    write_json(index_path, artifact_index)
    index_record = file_record(index_path, output_dir, "artifact-index")

    summary = {
        "schema_version": 1,
        "artifact_id": ARTIFACT_ID,
        "generated_at": generated_at,
        "status": "self_test_only_no_browser",
        "claim_status": CLAIM_STATUS,
        "launch_runner_id": LAUNCH_RUNNER_ID,
        "hardware_id": args.hardware_id,
        "os_control_id": args.os_control_id,
        "corpus_id": args.corpus_id,
        "network_profile_id": args.network_profile_id,
        "browser_pin_id": args.browser_pin_id,
        "tab_scenario_set_id": args.tab_scenario_set_id,
        "artifact_package_id": references.get("artifact_package_id"),
        "claim_mode": args.claim_mode,
        "artifact_root": str(output_dir),
        "artifact_root_persisted": persisted,
        "artifact_files": [*files, index_record],
        "required_arguments_checked": REQUIRED_ARGUMENTS,
        "forbidden_arguments_checked": FORBIDDEN_ARGUMENTS,
        "registry_references_checked": True,
        "artifact_root_behavior_checked": True,
        "browser_launched": False,
        "benchmark_result_generated": False,
        "commands": [
            "python3 -B tools/validate_benchmark_launch_runners.py",
            "python3 -B tools/run_benchmark_browser_launch.py --self-test",
        ],
        "unsupported": no_claim_finalization["unsupported"],
    }
    validate_summary(output_dir, summary)
    return summary


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        if args.artifact_root is not None:
            summary = run_launch_self_test(
                args.artifact_root,
                persisted=True,
                args=args,
            )
        else:
            with tempfile.TemporaryDirectory(prefix="turing-browser-launch-self-test-") as tmp:
                summary = run_launch_self_test(Path(tmp), persisted=False, args=args)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except (OSError, LaunchRunnerError) as error:
        print(f"benchmark browser launch runner failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
