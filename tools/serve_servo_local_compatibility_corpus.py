#!/usr/bin/env python3
"""Serve and self-test ADR-0009 no-claim local compatibility fixtures."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import validate_servo_local_compatibility_corpus as corpus_validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = corpus_validator.DEFAULT_MANIFEST
ARTIFACT_ID = "ADR9.EV013.NOCLAIM_ROUTE_SELF_TEST.2026_07"
CLAIM_STATUS = (
    "local fixture route self-test only; no HTTPS, no browser run, no WPT result, "
    "no Test262 result, no Servo adoption, no Turing compatibility claim, "
    "no Chrome-class claim, and no release-code authorization"
)


class RouteServerError(RuntimeError):
    pass


def require_object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RouteServerError(f"{label} must be an object")
    return value


def require_string(obj: dict[str, Any], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise RouteServerError(f"{label}.{key} must be a non-empty string")
    return value


def require_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise RouteServerError(f"{label} must be an integer")
    return value


def origin_host(origin: str) -> str:
    host = urlsplit(origin).hostname
    if not host:
        raise RouteServerError(f"origin has no host: {origin}")
    return host


def load_manifest(path: Path) -> dict[str, Any]:
    payload = corpus_validator.load_json(path)
    corpus_validator.validate_manifest(path, payload)
    return require_object(payload, "manifest")


def fixture_record(case: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    fixture_path = require_string(fixture, "fixture_path", "fixture")
    resolved = (ROOT / fixture_path).resolve()
    body = resolved.read_bytes()
    expected_sha = require_string(fixture, "sha256", "fixture")
    actual_sha = hashlib.sha256(body).hexdigest()
    if actual_sha != expected_sha:
        raise RouteServerError(f"fixture hash mismatch: {fixture_path}")
    expected_bytes = require_int(fixture.get("bytes"), "fixture.bytes")
    if len(body) != expected_bytes:
        raise RouteServerError(f"fixture byte count mismatch: {fixture_path}")
    return {
        "case_id": require_string(case, "case_id", "case"),
        "category": require_string(case, "category", "case"),
        "origin": require_string(fixture, "origin", "fixture"),
        "host": origin_host(require_string(fixture, "origin", "fixture")),
        "route_path": require_string(fixture, "route_path", "fixture"),
        "fixture_path": fixture_path,
        "body": body,
        "bytes": len(body),
        "sha256": actual_sha,
        "content_type": "text/html; charset=utf-8",
    }


def build_routes(manifest: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    cases = manifest.get("cases")
    if not isinstance(cases, list):
        raise RouteServerError("manifest.cases must be an array")
    routes: dict[tuple[str, str], dict[str, Any]] = {}
    for case_value in cases:
        case = require_object(case_value, "case")
        fixtures = case.get("fixtures")
        if not isinstance(fixtures, list):
            raise RouteServerError("case.fixtures must be an array")
        for fixture_value in fixtures:
            fixture = require_object(fixture_value, "fixture")
            record = fixture_record(case, fixture)
            host = str(record["host"])
            path = str(record["route_path"])
            for route_path in {path, f"{path.rstrip('/')}/index.html"}:
                key = (host, route_path)
                if key in routes:
                    raise RouteServerError(f"duplicate route: {host}{route_path}")
                routes[key] = record
    return routes


class CompatibilityHTTPServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler_class: type[BaseHTTPRequestHandler],
        manifest: dict[str, Any],
    ) -> None:
        self.manifest = manifest
        self.routes = build_routes(manifest)
        super().__init__(server_address, handler_class)


class CompatibilityHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        server = require_server(self.server)
        raw_host = self.headers.get("Host", "")
        host = raw_host.split(":", 1)[0].lower()
        path = urlsplit(self.path).path
        route = server.routes.get((host, path))
        if route is None:
            if any(host == route_host for route_host, _ in server.routes):
                self.send_error(404, "compatibility fixture route not found")
            else:
                self.send_error(421, "compatibility fixture host header required")
            return
        body = route["body"]
        self.send_response(200)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Type", str(route["content_type"]))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def require_server(value: object) -> CompatibilityHTTPServer:
    if not isinstance(value, CompatibilityHTTPServer):
        raise RouteServerError("handler is not attached to a compatibility server")
    return value


def start_server(manifest: dict[str, Any], host: str, port: int) -> CompatibilityHTTPServer:
    return CompatibilityHTTPServer((host, port), CompatibilityHandler, manifest)


def route_summaries(server: CompatibilityHTTPServer) -> list[dict[str, object]]:
    seen: set[tuple[str, str]] = set()
    summaries: list[dict[str, object]] = []
    for (host, route_path), route in sorted(server.routes.items()):
        case_key = (str(route["fixture_path"]), str(route["origin"]))
        if case_key in seen:
            continue
        seen.add(case_key)
        summaries.append(
            {
                "case_id": route["case_id"],
                "category": route["category"],
                "origin": route["origin"],
                "host": host,
                "route_path": route_path,
                "fixture_path": route["fixture_path"],
                "bytes": route["bytes"],
                "sha256": route["sha256"],
            }
        )
    return summaries


def request_route(port: int, route: dict[str, Any]) -> dict[str, object]:
    host = str(route["host"])
    route_path = str(route["route_path"])
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        connection.request("GET", route_path, headers={"Host": f"{host}:{port}"})
        response = connection.getresponse()
        body = response.read()
    finally:
        connection.close()

    if response.status != 200:
        raise RouteServerError(f"{host}{route_path} returned {response.status}")
    if body != route["body"]:
        raise RouteServerError(f"{host}{route_path} body did not match fixture bytes")
    if response.getheader("Cache-Control") != "no-store":
        raise RouteServerError(f"{host}{route_path} did not return Cache-Control: no-store")
    if response.getheader("Content-Type") != route["content_type"]:
        raise RouteServerError(f"{host}{route_path} returned the wrong Content-Type")
    return {
        "case_id": route["case_id"],
        "origin": route["origin"],
        "route_path": route_path,
        "status": response.status,
        "content_type": response.getheader("Content-Type"),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
    }


def unique_fixture_routes(server: CompatibilityHTTPServer) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    routes: list[dict[str, Any]] = []
    for route in sorted(
        server.routes.values(),
        key=lambda item: (str(item["host"]), str(item["route_path"]), str(item["fixture_path"])),
    ):
        key = (str(route["fixture_path"]), str(route["origin"]))
        if key in seen:
            continue
        seen.add(key)
        routes.append(route)
    return routes


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
    raise RouteServerError("server still accepted a connection after shutdown")


def run_self_test(manifest_path: Path) -> dict[str, object]:
    manifest = load_manifest(manifest_path.resolve())
    server = start_server(manifest, "127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = require_int(server.server_address[1], "server.port")
    try:
        route_checks = [request_route(port, route) for route in unique_fixture_routes(server)]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    if thread.is_alive():
        raise RouteServerError("server thread did not stop after shutdown")

    expected_fixture_count = sum(
        len(require_object(case, "case").get("fixtures", []))
        for case in manifest.get("cases", [])
        if isinstance(case, dict)
    )
    if len(route_checks) != expected_fixture_count:
        raise RouteServerError("route self-test did not check every fixture route")
    return {
        "schema_version": 1,
        "artifact_id": ARTIFACT_ID,
        "corpus_id": manifest["corpus_id"],
        "claim_status": CLAIM_STATUS,
        "manifest_path": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "bind_host": "127.0.0.1",
        "bound_port": port,
        "protocol": "HTTP/1.1 over loopback",
        "host_header_mapping": "self-test uses Host headers only and does not modify DNS or OS resolver state",
        "server_started": True,
        "server_shutdown": True,
        "port_closed_check": confirm_port_closed(port),
        "routes_available": route_summaries(server),
        "routes_checked": route_checks,
        "external_network_used": False,
        "dns_os_modified": False,
        "https_used": False,
        "tls_certificate_provided": False,
        "browser_launched": False,
        "compatibility_result_generated": False,
        "wpt_result_generated": False,
        "test262_result_generated": False,
        "unsupported": [
            "no HTTPS certificate or trust-store state is created",
            "no OS DNS or hosts-file state is modified",
            "no Servo, Turing, or competitor browser process is launched",
            "no WPT or Test262 command is run",
            "no compatibility, security, performance, memory, accessibility, Chrome-class, release, or production claim is allowed",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=0)
    return parser.parse_args(argv)


def run_forever(manifest_path: Path, port: int) -> int:
    manifest = load_manifest(manifest_path.resolve())
    server = start_server(manifest, "127.0.0.1", port)
    bound_port = require_int(server.server_address[1], "server.port")
    print(
        json.dumps(
            {
                "schema_version": 1,
                "artifact_id": f"{ARTIFACT_ID}.SERVER",
                "corpus_id": manifest["corpus_id"],
                "claim_status": CLAIM_STATUS,
                "bind_host": "127.0.0.1",
                "bound_port": bound_port,
                "protocol": "HTTP/1.1 over loopback",
                "routes_available": route_summaries(server),
                "unsupported": [
                    "caller must provide Host headers or reviewed host mapping",
                    "no HTTPS, browser run, WPT result, Test262 result, or compatibility claim is produced by serving fixtures",
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.self_test == args.serve:
            raise RouteServerError("pass exactly one of --self-test or --serve")
        if args.port < 0:
            raise RouteServerError("--port must be >= 0")
        if args.self_test:
            print(json.dumps(run_self_test(args.manifest), indent=2, sort_keys=True))
            return 0
        return run_forever(args.manifest, args.port)
    except (
        OSError,
        RouteServerError,
        corpus_validator.ValidationError,
    ) as error:
        print(f"ADR-0009 compatibility fixture server failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
