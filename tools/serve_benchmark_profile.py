#!/usr/bin/env python3
"""Serve and self-test the no-claim benchmark network profile."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import validate_benchmark_network_profile as profile_validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = (
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "benchmark-network-profiles"
    / "no-claim-local-static.profile.json"
)
ARTIFACT_ID = "NOCLAIM.NETWORK_PROFILE_SELF_TEST.2026_07"
SERVER_ARTIFACT_ID = "NOCLAIM.NETWORK_PROFILE_SERVER.2026_07"
CLAIM_STATUS = (
    "static server self-test only; no browser run, no benchmark result, "
    "no latency result, no cache result, no TLS result, no DNS result, "
    "and no performance claim"
)


class ServerError(RuntimeError):
    pass


def require_object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ServerError(f"{label} must be an object")
    return value


def require_string(obj: dict[str, Any], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise ServerError(f"{label}.{key} must be a non-empty string")
    return value


def require_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise ServerError(f"{label} must be an integer")
    return value


def load_profile(path: Path) -> dict[str, Any]:
    payload = profile_validator.load_json(path)
    profile_validator.validate_profile(path, payload)
    return require_object(payload, "profile")


def build_routes(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    routes_value = profile.get("routes")
    if not isinstance(routes_value, list):
        raise ServerError("profile.routes must be an array")
    routes: dict[str, dict[str, Any]] = {}
    for route_value in routes_value:
        route = require_object(route_value, "route")
        origin_path = require_string(route, "origin_path", "route")
        entry_path = require_string(route, "entry_path", "route")
        resolved = (ROOT / entry_path).resolve()
        body = resolved.read_bytes()
        record = {
            "case_id": require_string(route, "case_id", "route"),
            "origin_path": origin_path,
            "entry_path": entry_path,
            "expected_status": require_int(route.get("expected_status"), "route.expected_status"),
            "content_type": require_string(route, "content_type", "route"),
            "body": body,
            "sha256": hashlib.sha256(body).hexdigest(),
            "bytes": len(body),
        }
        routes[origin_path] = record
        if origin_path.endswith("/"):
            routes[f"{origin_path}index.html"] = record
    return routes


class ProfileHTTPServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler_class: type[BaseHTTPRequestHandler],
        profile: dict[str, Any],
    ) -> None:
        self.profile = profile
        self.routes = build_routes(profile)
        super().__init__(server_address, handler_class)


class ProfileHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        server = require_profile_server(self.server)
        host = self.headers.get("Host", "")
        expected_host = require_string(
            require_object(server.profile.get("origin"), "origin"), "host", "origin"
        )
        port = require_int(server.server_address[1], "server.port")
        if host not in {expected_host, f"{expected_host}:{port}"}:
            self.send_error(421, "profile host header required")
            return

        path = urlsplit(self.path).path
        route = server.routes.get(path)
        if route is None:
            self.send_error(404, "profile route not found")
            return

        headers = require_object(
            require_object(server.profile.get("cache"), "cache").get("response_headers"),
            "cache.response_headers",
        )
        body = route["body"]
        self.send_response(route["expected_status"])
        for name, value in headers.items():
            self.send_header(str(name), str(value))
        self.send_header("Content-Type", route["content_type"])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def require_profile_server(value: object) -> ProfileHTTPServer:
    if not isinstance(value, ProfileHTTPServer):
        raise ServerError("handler is not attached to a profile server")
    return value


def start_server(profile: dict[str, Any], host: str, port: int) -> ProfileHTTPServer:
    server_config = require_object(profile.get("server"), "server")
    expected_host = require_string(server_config, "bind_host", "server")
    if host != expected_host:
        raise ServerError(f"server must bind to profile host {expected_host}")
    return ProfileHTTPServer((host, port), ProfileHandler, profile)


def route_summaries(server: ProfileHTTPServer) -> list[dict[str, object]]:
    seen: set[str] = set()
    summaries: list[dict[str, object]] = []
    for route in server.routes.values():
        case_id = str(route["case_id"])
        if case_id in seen:
            continue
        seen.add(case_id)
        summaries.append(
            {
                "case_id": case_id,
                "origin_path": route["origin_path"],
                "entry_path": route["entry_path"],
                "bytes": route["bytes"],
                "sha256": route["sha256"],
            }
        )
    return summaries


def request_route(port: int, origin_host: str, route: dict[str, Any]) -> dict[str, object]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        connection.request(
            "GET",
            str(route["origin_path"]),
            headers={"Host": f"{origin_host}:{port}"},
        )
        response = connection.getresponse()
        body = response.read()
    finally:
        connection.close()

    if response.status != route["expected_status"]:
        raise ServerError(
            f"{route['case_id']} returned {response.status}, expected {route['expected_status']}"
        )
    if body != route["body"]:
        raise ServerError(f"{route['case_id']} body did not match fixture bytes")
    if response.getheader("Cache-Control") != "no-store":
        raise ServerError(f"{route['case_id']} did not return Cache-Control: no-store")
    if response.getheader("Content-Type") != route["content_type"]:
        raise ServerError(f"{route['case_id']} returned the wrong Content-Type")

    return {
        "case_id": route["case_id"],
        "origin_path": route["origin_path"],
        "status": response.status,
        "content_type": response.getheader("Content-Type"),
        "cache_control": response.getheader("Cache-Control"),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
    }


def run_self_test(profile: dict[str, Any]) -> dict[str, object]:
    host = require_string(require_object(profile.get("server"), "server"), "bind_host", "server")
    origin_host = require_string(
        require_object(profile.get("origin"), "origin"), "host", "origin"
    )
    dns_address = require_string(require_object(profile.get("dns"), "dns"), "address", "dns")
    server = start_server(profile, host, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = require_int(server.server_address[1], "server.port")
        routes_checked: list[dict[str, object]] = []
        for summary in route_summaries(server):
            route = server.routes[str(summary["origin_path"])]
            routes_checked.append(request_route(port, origin_host, route))
        return {
            "schema_version": 1,
            "artifact_id": ARTIFACT_ID,
            "profile_id": profile["profile_id"],
            "claim_status": CLAIM_STATUS,
            "bind_host": host,
            "bound_port": port,
            "dns_override": (
                f"{origin_host} -> {dns_address}; self-test uses the Host header only "
                "and does not modify the OS resolver"
            ),
            "protocol": "HTTP/1.1 over loopback",
            "routes_checked": routes_checked,
            "unsupported": profile["unsupported"],
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def run_forever(profile: dict[str, Any], port: int) -> int:
    host = require_string(require_object(profile.get("server"), "server"), "bind_host", "server")
    origin_host = require_string(
        require_object(profile.get("origin"), "origin"), "host", "origin"
    )
    dns_address = require_string(require_object(profile.get("dns"), "dns"), "address", "dns")
    server = start_server(profile, host, port)
    bound_port = require_int(server.server_address[1], "server.port")
    startup = {
        "schema_version": 1,
        "artifact_id": SERVER_ARTIFACT_ID,
        "profile_id": profile["profile_id"],
        "claim_status": CLAIM_STATUS,
        "bind_host": host,
        "bound_port": bound_port,
        "dns_override": (
            f"{origin_host} -> {dns_address}; caller must provide a host mapping "
            "or equivalent Host header"
        ),
        "routes": route_summaries(server),
        "unsupported": profile["unsupported"],
    }
    print(json.dumps(startup, indent=2, sort_keys=True), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=0)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        profile = load_profile(args.profile.resolve())
        if args.self_test:
            print(json.dumps(run_self_test(profile), indent=2, sort_keys=True))
            return 0
        if args.port < 0:
            raise ServerError("--port must be >= 0")
        return run_forever(profile, args.port)
    except (OSError, ServerError, profile_validator.ValidationError) as error:
        print(f"benchmark profile server failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
