#!/usr/bin/env python3
"""Run the no-claim benchmark smoke artifact pipeline."""

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
PROFILE_SERVER = ROOT / "tools" / "serve_benchmark_profile.py"
ARTIFACT_ID = "NOCLAIM.BENCHMARK_SMOKE_RUNNER.2026_07"
PROFILE_SELF_TEST_ARTIFACT_ID = "NOCLAIM.NETWORK_PROFILE_SELF_TEST.2026_07"
DEFAULT_HARDWARE_ID = "TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07"
DEFAULT_OS_CONTROL_ID = "TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07"
DEFAULT_RESOURCE_ATTRIBUTION_ID = (
    "TURING.BENCHMARK.RESOURCE_ATTRIBUTION.SEMANTIC_OWNERS.2026_07"
)
CLAIM_STATUS = (
    "runner smoke self-test only; no browser run, no benchmark result, "
    "no latency result, no memory result, no energy result, no compatibility result, "
    "and no performance claim"
)


class SmokeError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SmokeError(f"{label} must be an object")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_profile_self_test() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-B", str(PROFILE_SERVER), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        raise SmokeError(detail or "profile self-test failed")
    try:
        artifact = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SmokeError(f"profile self-test emitted invalid JSON: {error}") from error
    artifact = require_object(artifact, "profile_self_test")
    if artifact.get("artifact_id") != PROFILE_SELF_TEST_ARTIFACT_ID:
        raise SmokeError("profile self-test emitted the wrong artifact_id")
    routes = artifact.get("routes_checked")
    if not isinstance(routes, list) or len(routes) < 2:
        raise SmokeError("profile self-test must check at least two routes")
    return artifact


def prepare_output_dir(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.exists() and any(resolved.iterdir()):
        raise SmokeError(f"output directory must be empty: {resolved}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def file_record(path: Path, root: Path, kind: str) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": str(path.relative_to(root)).replace("\\", "/"),
        "kind": kind,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def run_smoke(
    output_dir: Path,
    *,
    persisted: bool,
    hardware_id: str,
    os_control_id: str,
    resource_attribution_id: str,
) -> dict[str, Any]:
    output_dir = prepare_output_dir(output_dir)
    profile_self_test = run_profile_self_test()
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    profile_path = output_dir / "profile-self-test.json"
    runner_path = output_dir / "runner-summary.json"
    index_path = output_dir / "artifact-index.json"

    write_json(profile_path, profile_self_test)
    runner_summary: dict[str, Any] = {
        "schema_version": 1,
        "artifact_id": ARTIFACT_ID,
        "generated_at": generated_at,
        "status": "self_test_only_no_browser",
        "claim_status": CLAIM_STATUS,
        "hardware_id": hardware_id,
        "os_control_id": os_control_id,
        "resource_attribution_id": resource_attribution_id,
        "profile_self_test_artifact_id": PROFILE_SELF_TEST_ARTIFACT_ID,
        "profile_id": profile_self_test.get("profile_id"),
        "routes_checked": profile_self_test.get("routes_checked"),
        "commands": [
            "python3 -B tools/serve_benchmark_profile.py --self-test",
            "python3 -B tools/run_benchmark_smoke.py --self-test",
        ],
        "unsupported": [
            "no browser process is launched",
            "no page is loaded by Turing or any competitor browser",
            "no timing samples are collected",
            "no memory, CPU, GPU, energy, accessibility, or compatibility measurements are collected",
            "no comparison, regression, release, or performance claim is allowed",
        ],
    }
    write_json(runner_path, runner_summary)
    files = [
        file_record(profile_path, output_dir, "profile-self-test"),
        file_record(runner_path, output_dir, "runner-summary"),
    ]
    artifact_index: dict[str, Any] = {
        "schema_version": 1,
        "artifact_id": f"{ARTIFACT_ID}.INDEX",
        "generated_at": generated_at,
        "claim_status": CLAIM_STATUS,
        "hardware_id": hardware_id,
        "os_control_id": os_control_id,
        "resource_attribution_id": resource_attribution_id,
        "files": files,
    }
    write_json(index_path, artifact_index)
    index_record = file_record(index_path, output_dir, "artifact-index")
    summary: dict[str, Any] = {
        "schema_version": 1,
        "artifact_id": ARTIFACT_ID,
        "generated_at": generated_at,
        "status": "self_test_only_no_browser",
        "claim_status": CLAIM_STATUS,
        "hardware_id": hardware_id,
        "os_control_id": os_control_id,
        "resource_attribution_id": resource_attribution_id,
        "output_dir": str(output_dir),
        "output_dir_persisted": persisted,
        "profile_self_test_artifact_id": PROFILE_SELF_TEST_ARTIFACT_ID,
        "artifact_files": [*files, index_record],
        "routes_checked": profile_self_test.get("routes_checked"),
        "unsupported": runner_summary["unsupported"],
    }
    validate_summary(output_dir, summary)
    return summary


def validate_summary(output_dir: Path, summary: dict[str, Any]) -> None:
    if summary.get("artifact_id") != ARTIFACT_ID:
        raise SmokeError("runner summary has the wrong artifact_id")
    claim_status = summary.get("claim_status")
    if not isinstance(claim_status, str):
        raise SmokeError("runner summary is missing claim_status")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            raise SmokeError(f"runner claim_status must mention: {phrase}")
    hardware_id = summary.get("hardware_id")
    if not isinstance(hardware_id, str) or not hardware_id.startswith(
        "TURING.BENCHMARK.HARDWARE."
    ):
        raise SmokeError("runner summary needs a benchmark hardware registry id")
    os_control_id = summary.get("os_control_id")
    if not isinstance(os_control_id, str) or not os_control_id.startswith(
        "TURING.BENCHMARK.OS_CONTROL."
    ):
        raise SmokeError("runner summary needs a benchmark OS-control registry id")
    resource_attribution_id = summary.get("resource_attribution_id")
    if not isinstance(resource_attribution_id, str) or not resource_attribution_id.startswith(
        "TURING.BENCHMARK.RESOURCE_ATTRIBUTION."
    ):
        raise SmokeError("runner summary needs a benchmark resource-attribution registry id")
    files = summary.get("artifact_files")
    if not isinstance(files, list) or len(files) != 3:
        raise SmokeError("runner summary must include three artifact files")
    for file_value in files:
        file_item = require_object(file_value, "artifact_file")
        relative_path = file_item.get("path")
        expected_sha = file_item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_sha, str):
            raise SmokeError("artifact file records need path and sha256")
        actual_path = (output_dir / relative_path).resolve()
        try:
            actual_path.relative_to(output_dir.resolve())
        except ValueError as error:
            raise SmokeError(f"artifact file points outside package: {relative_path}") from error
        if not actual_path.is_file():
            raise SmokeError(f"artifact file is missing: {relative_path}")
        if sha256_file(actual_path) != expected_sha:
            raise SmokeError(f"artifact file hash mismatch: {relative_path}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--hardware-id", default=DEFAULT_HARDWARE_ID)
    parser.add_argument("--os-control-id", default=DEFAULT_OS_CONTROL_ID)
    parser.add_argument(
        "--resource-attribution-id", default=DEFAULT_RESOURCE_ATTRIBUTION_ID
    )
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.output_dir is not None:
            summary = run_smoke(
                args.output_dir,
                persisted=True,
                hardware_id=args.hardware_id,
                os_control_id=args.os_control_id,
                resource_attribution_id=args.resource_attribution_id,
            )
        elif args.self_test:
            with tempfile.TemporaryDirectory(prefix="turing-benchmark-smoke-") as tmp:
                summary = run_smoke(
                    Path(tmp),
                    persisted=False,
                    hardware_id=args.hardware_id,
                    os_control_id=args.os_control_id,
                    resource_attribution_id=args.resource_attribution_id,
                )
        else:
            raise SmokeError("pass --self-test or --output-dir")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except (OSError, SmokeError) as error:
        print(f"benchmark smoke runner failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
