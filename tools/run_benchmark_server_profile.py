#!/usr/bin/env python3
"""Run the no-claim benchmark server lifecycle self-test."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import socket
import sys
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import serve_benchmark_profile as profile_server

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = profile_server.DEFAULT_PROFILE
ARTIFACT_ID = "NOCLAIM.NETWORK_PROFILE_SERVER_RUN.2026_07"
CLAIM_STATUS = (
    "runner-managed server lifecycle self-test only; no browser run, "
    "no benchmark result, no latency result, no cache result, no TLS result, "
    "no DNS result, and no performance claim"
)


class ServerRunError(RuntimeError):
    pass


def require_object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ServerRunError(f"{label} must be an object")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def prepare_output_dir(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.exists() and any(resolved.iterdir()):
        raise ServerRunError(f"output directory must be empty: {resolved}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def confirm_port_closed(port: int) -> dict[str, object]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
    try:
        connection.request("GET", "/")
        response = connection.getresponse()
        response.read()
    except (ConnectionRefusedError, ConnectionResetError, TimeoutError, OSError, socket.timeout) as error:
        return {
            "status": "closed",
            "connection_attempt_rejected": True,
            "error_type": type(error).__name__,
        }
    finally:
        connection.close()
    raise ServerRunError("server still accepted a connection after shutdown")


def validate_summary(output_dir: Path, summary: dict[str, Any]) -> None:
    if summary.get("artifact_id") != ARTIFACT_ID:
        raise ServerRunError("summary has the wrong artifact_id")
    claim_status = summary.get("claim_status")
    if not isinstance(claim_status, str):
        raise ServerRunError("summary is missing claim_status")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            raise ServerRunError(f"summary claim_status must mention: {phrase}")
    if summary.get("server_started") is not True:
        raise ServerRunError("summary must state server_started=true")
    if summary.get("server_shutdown") is not True:
        raise ServerRunError("summary must state server_shutdown=true")
    if summary.get("browser_launched") is not False:
        raise ServerRunError("summary must state browser_launched=false")
    if summary.get("benchmark_result_generated") is not False:
        raise ServerRunError("summary must state benchmark_result_generated=false")
    if summary.get("external_network_used") is not False:
        raise ServerRunError("summary must state external_network_used=false")
    files = summary.get("artifact_files")
    if not isinstance(files, list) or len(files) != 5:
        raise ServerRunError("summary must include five artifact file records")
    resolved_root = output_dir.resolve()
    for file_value in files:
        item = require_object(file_value, "artifact_file")
        relative_path = item.get("path")
        expected_sha = item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_sha, str):
            raise ServerRunError("artifact file records need path and sha256")
        actual_path = (output_dir / relative_path).resolve()
        try:
            actual_path.relative_to(resolved_root)
        except ValueError as error:
            raise ServerRunError(f"artifact path escapes root: {relative_path}") from error
        if not actual_path.is_file():
            raise ServerRunError(f"artifact file is missing: {relative_path}")
        if sha256_file(actual_path) != expected_sha:
            raise ServerRunError(f"artifact file hash mismatch: {relative_path}")


def run_server_lifecycle(
    output_dir: Path,
    *,
    profile_path: Path,
    persisted: bool,
) -> dict[str, Any]:
    output_dir = prepare_output_dir(output_dir)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    profile = profile_server.load_profile(profile_path.resolve())
    host = profile_server.require_string(
        profile_server.require_object(profile.get("server"), "server"),
        "bind_host",
        "server",
    )
    origin = profile_server.require_object(profile.get("origin"), "origin")
    origin_host = profile_server.require_string(origin, "host", "origin")
    dns = profile_server.require_object(profile.get("dns"), "dns")
    dns_address = profile_server.require_string(dns, "address", "dns")

    server = profile_server.start_server(profile, host, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = profile_server.require_int(server.server_address[1], "server.port")
    try:
        startup = {
            "schema_version": 1,
            "artifact_id": f"{ARTIFACT_ID}.STARTUP",
            "generated_at": generated_at,
            "profile_id": profile["profile_id"],
            "claim_status": CLAIM_STATUS,
            "bind_host": host,
            "bound_port": port,
            "dns_override": (
                f"{origin_host} -> {dns_address}; self-test uses the Host header only "
                "and does not modify the OS resolver"
            ),
            "protocol": "HTTP/1.1 over loopback",
            "routes": profile_server.route_summaries(server),
            "server_started": True,
            "external_network_used": False,
            "dns_os_modified": False,
        }
        routes_checked = []
        for summary in profile_server.route_summaries(server):
            route = server.routes[str(summary["origin_path"])]
            routes_checked.append(profile_server.request_route(port, origin_host, route))
        route_checks = {
            "schema_version": 1,
            "artifact_id": f"{ARTIFACT_ID}.ROUTES",
            "generated_at": generated_at,
            "profile_id": profile["profile_id"],
            "claim_status": CLAIM_STATUS,
            "host_header": f"{origin_host}:{port}",
            "routes_checked": routes_checked,
            "external_network_used": False,
            "browser_launched": False,
            "benchmark_result_generated": False,
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    if thread.is_alive():
        raise ServerRunError("server thread did not stop after shutdown")

    shutdown = {
        "schema_version": 1,
        "artifact_id": f"{ARTIFACT_ID}.SHUTDOWN",
        "generated_at": generated_at,
        "profile_id": profile["profile_id"],
        "claim_status": CLAIM_STATUS,
        "server_shutdown": True,
        "thread_joined": True,
        "port_closed_check": confirm_port_closed(port),
        "temporary_profile_used": False,
        "browser_launched": False,
        "benchmark_result_generated": False,
    }
    runner_summary = {
        "schema_version": 1,
        "artifact_id": ARTIFACT_ID,
        "generated_at": generated_at,
        "status": "server_lifecycle_self_test_only_no_browser",
        "claim_status": CLAIM_STATUS,
        "profile_id": profile["profile_id"],
        "profile_path": str(profile_path.relative_to(ROOT)).replace("\\", "/"),
        "bind_host": host,
        "bound_port": port,
        "server_started": True,
        "server_shutdown": True,
        "routes_checked": routes_checked,
        "external_network_used": False,
        "dns_os_modified": False,
        "browser_launched": False,
        "benchmark_result_generated": False,
        "commands": [
            "python3 -B tools/validate_benchmark_network_profile.py",
            "python3 -B tools/run_benchmark_server_profile.py --self-test",
        ],
        "unsupported": [
            "no browser process is launched",
            "no page is loaded by Turing or any competitor browser",
            "no DNS resolver state is modified",
            "no TLS, HTTP/2, HTTP/3, proxy, authentication, cache-revalidation, or network-shaping profile is exercised",
            "no timing, memory, CPU, GPU, energy, accessibility, compatibility, comparison, regression, release, or performance claim is allowed",
        ],
    }

    startup_path = output_dir / "server-startup.json"
    routes_path = output_dir / "route-checks.json"
    shutdown_path = output_dir / "server-shutdown.json"
    summary_path = output_dir / "runner-summary.json"
    index_path = output_dir / "artifact-index.json"
    write_json(startup_path, startup)
    write_json(routes_path, route_checks)
    write_json(shutdown_path, shutdown)
    write_json(summary_path, runner_summary)
    files = [
        file_record(startup_path, output_dir, "server-startup"),
        file_record(routes_path, output_dir, "route-checks"),
        file_record(shutdown_path, output_dir, "server-shutdown"),
        file_record(summary_path, output_dir, "runner-summary"),
    ]
    artifact_index = {
        "schema_version": 1,
        "artifact_id": f"{ARTIFACT_ID}.INDEX",
        "generated_at": generated_at,
        "claim_status": CLAIM_STATUS,
        "profile_id": profile["profile_id"],
        "files": files,
        "server_started": True,
        "server_shutdown": True,
        "browser_launched": False,
        "benchmark_result_generated": False,
    }
    write_json(index_path, artifact_index)
    index_record = file_record(index_path, output_dir, "artifact-index")
    summary = {
        **runner_summary,
        "output_dir": str(output_dir),
        "output_dir_persisted": persisted,
        "artifact_files": [*files, index_record],
    }
    validate_summary(output_dir, summary)
    return summary


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.output_dir is not None:
            summary = run_server_lifecycle(
                args.output_dir,
                profile_path=args.profile,
                persisted=True,
            )
        elif args.self_test:
            with tempfile.TemporaryDirectory(prefix="turing-network-server-run-") as tmp:
                summary = run_server_lifecycle(
                    Path(tmp),
                    profile_path=args.profile,
                    persisted=False,
                )
        else:
            raise ServerRunError("pass --self-test or --output-dir")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except (
        OSError,
        ServerRunError,
        profile_server.ServerError,
        profile_server.profile_validator.ValidationError,
    ) as error:
        print(f"benchmark server profile runner failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
