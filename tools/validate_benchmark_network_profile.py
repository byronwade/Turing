#!/usr/bin/env python3
"""Validate benchmark network-profile fixtures without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = (
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "benchmark-network-profiles"
    / "no-claim-local-static.profile.json"
)
DEFAULT_CORPUS = (
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "benchmark-corpora"
    / "no-claim-smoke.corpus.json"
)
DEFAULT_MANIFEST = (
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "benchmark-manifests"
    / "no-claim-runner-smoke.sample.json"
)

PROFILE_ID = re.compile(r"^[A-Z0-9][A-Z0-9._-]+$")
ALLOWED_STATUS = {
    "sample_only_no_server",
    "self_test_only_no_benchmark_result",
    "draft",
    "reviewed",
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


def reject_extra(
    path: Path, obj: dict[str, object], allowed: set[str], label: str
) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(
    path: Path, obj: dict[str, object], required: set[str], label: str
) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_bool(path: Path, obj: dict[str, object], key: str, label: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        fail(path, f"{label}.{key} must be a boolean")
    return value


def require_number(
    path: Path, obj: dict[str, object], key: str, label: str, *, minimum: float = 0
) -> float:
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < minimum:
        fail(path, f"{label}.{key} must be a number >= {minimum}")
    return float(value)


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(path, f"{label}.{key} must be an array of strings")
    return value


def corpus_cases(path: Path) -> tuple[str, dict[str, dict[str, object]]]:
    corpus = require_object(path, load_json(path), "corpus")
    corpus_id = require_string(path, corpus, "corpus_id", "corpus")
    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        fail(path, "corpus.cases must be a non-empty array")
    by_id: dict[str, dict[str, object]] = {}
    for case in cases:
        item = require_object(path, case, "corpus.case")
        case_id = require_string(path, item, "case_id", "corpus.case")
        by_id[case_id] = item
    return corpus_id, by_id


def validate_sample_manifest_reference(path: Path, profile_id: str) -> None:
    manifest = require_object(DEFAULT_MANIFEST, load_json(DEFAULT_MANIFEST), "manifest")
    workload = require_object(DEFAULT_MANIFEST, manifest.get("workload"), "manifest.workload")
    network_profile = require_string(
        DEFAULT_MANIFEST, workload, "network_profile", "manifest.workload"
    )
    if network_profile != profile_id:
        fail(path, "default benchmark sample does not reference this network profile")


def validate_server(path: Path, value: object) -> None:
    server = require_object(path, value, "server")
    required = {"mode", "bind_host", "port_policy", "document_root", "external_network_allowed"}
    reject_extra(path, server, required, "server")
    require_keys(path, server, required, "server")
    require_string(path, server, "mode", "server")
    bind_host = require_string(path, server, "bind_host", "server")
    if bind_host not in {"127.0.0.1", "::1"}:
        fail(path, "server.bind_host must be loopback")
    require_string(path, server, "port_policy", "server")
    document_root = require_string(path, server, "document_root", "server")
    root = (ROOT / document_root).resolve()
    try:
        root.relative_to(ROOT / "benchmarks" / "corpus")
    except ValueError:
        fail(path, "server.document_root must live under benchmarks/corpus")
    if not root.is_dir():
        fail(path, "server.document_root does not exist")
    if require_bool(path, server, "external_network_allowed", "server"):
        fail(path, "server.external_network_allowed must be false for no-claim profile")


def validate_origin(path: Path, value: object) -> None:
    origin = require_object(path, value, "origin")
    required = {"scheme", "host", "port", "base_url_template"}
    reject_extra(path, origin, required, "origin")
    require_keys(path, origin, required, "origin")
    if require_string(path, origin, "scheme", "origin") != "http":
        fail(path, "no-claim seed profile must use plain http until TLS profile exists")
    if require_string(path, origin, "host", "origin") != "turing.invalid":
        fail(path, "origin.host must be turing.invalid")
    require_string(path, origin, "port", "origin")
    base = require_string(path, origin, "base_url_template", "origin")
    if not base.startswith("http://turing.invalid:{port}/"):
        fail(path, "origin.base_url_template must use the turing.invalid loopback template")


def validate_dns(path: Path, value: object) -> None:
    dns = require_object(path, value, "dns")
    required = {"mode", "host", "address", "external_dns_allowed"}
    reject_extra(path, dns, required, "dns")
    require_keys(path, dns, required, "dns")
    require_string(path, dns, "mode", "dns")
    if require_string(path, dns, "host", "dns") != "turing.invalid":
        fail(path, "dns.host must be turing.invalid")
    if require_string(path, dns, "address", "dns") not in {"127.0.0.1", "::1"}:
        fail(path, "dns.address must be loopback")
    if require_bool(path, dns, "external_dns_allowed", "dns"):
        fail(path, "dns.external_dns_allowed must be false")


def validate_protocols(path: Path, value: object) -> None:
    protocols = require_object(path, value, "protocols")
    required = {"http1", "http2", "http3", "tls"}
    reject_extra(path, protocols, required, "protocols")
    require_keys(path, protocols, required, "protocols")
    if not require_bool(path, protocols, "http1", "protocols"):
        fail(path, "no-claim seed profile must enable HTTP/1.1")
    for key in ["http2", "http3", "tls"]:
        if require_bool(path, protocols, key, "protocols"):
            fail(path, f"no-claim seed profile must keep {key} disabled")


def validate_cache(path: Path, value: object) -> None:
    cache = require_object(path, value, "cache")
    required = {"default_state", "reset_required", "response_headers"}
    reject_extra(path, cache, required, "cache")
    require_keys(path, cache, required, "cache")
    if require_string(path, cache, "default_state", "cache") != "cold":
        fail(path, "cache.default_state must be cold for the seed profile")
    if not require_bool(path, cache, "reset_required", "cache"):
        fail(path, "cache.reset_required must be true")
    headers = require_object(path, cache.get("response_headers"), "cache.response_headers")
    for key, value in headers.items():
        if not isinstance(key, str) or not isinstance(value, str):
            fail(path, "cache.response_headers values must be strings")
    if headers.get("Cache-Control") != "no-store":
        fail(path, "cache.response_headers must include Cache-Control: no-store")


def validate_network_conditions(path: Path, value: object) -> None:
    conditions = require_object(path, value, "network_conditions")
    required = {"transport", "latency_ms", "loss_percent", "bandwidth", "shaping"}
    reject_extra(path, conditions, required, "network_conditions")
    require_keys(path, conditions, required, "network_conditions")
    if require_string(path, conditions, "transport", "network_conditions") != "loopback":
        fail(path, "network_conditions.transport must be loopback")
    require_number(path, conditions, "latency_ms", "network_conditions", minimum=0)
    require_number(path, conditions, "loss_percent", "network_conditions", minimum=0)
    require_string(path, conditions, "bandwidth", "network_conditions")
    require_string(path, conditions, "shaping", "network_conditions")


def validate_authentication(path: Path, value: object) -> None:
    auth = require_object(path, value, "authentication")
    required = {"mode", "credentials"}
    reject_extra(path, auth, required, "authentication")
    require_keys(path, auth, required, "authentication")
    if require_string(path, auth, "mode", "authentication") != "disabled":
        fail(path, "authentication.mode must be disabled for seed profile")
    if require_string_array(path, auth, "credentials", "authentication"):
        fail(path, "authentication.credentials must be empty")


def validate_routes(
    path: Path, value: object, cases: dict[str, dict[str, object]]
) -> None:
    if not isinstance(value, list) or len(value) < 2:
        fail(path, "routes must contain at least two entries")
    seen: set[str] = set()
    for index, route_value in enumerate(value, start=1):
        route = require_object(path, route_value, f"routes[{index}]")
        required = {"case_id", "origin_path", "entry_path", "expected_status", "content_type"}
        reject_extra(path, route, required, f"routes[{index}]")
        require_keys(path, route, required, f"routes[{index}]")
        case_id = require_string(path, route, "case_id", f"routes[{index}]")
        if case_id in seen:
            fail(path, f"duplicate route case_id: {case_id}")
        seen.add(case_id)
        if case_id not in cases:
            fail(path, f"route case_id is not in corpus manifest: {case_id}")
        origin_path = require_string(path, route, "origin_path", f"routes[{index}]")
        if not origin_path.startswith("/corpus/no-claim-smoke/"):
            fail(path, "route.origin_path must stay under /corpus/no-claim-smoke/")
        entry_path = require_string(path, route, "entry_path", f"routes[{index}]")
        case_entry = cases[case_id].get("entry_path")
        if entry_path != case_entry:
            fail(path, f"route.entry_path does not match corpus case {case_id}")
        resolved = (ROOT / entry_path).resolve()
        try:
            resolved.relative_to(ROOT / "benchmarks" / "corpus")
        except ValueError:
            fail(path, f"route.entry_path must live under benchmarks/corpus: {entry_path}")
        if not resolved.is_file():
            fail(path, f"route.entry_path does not exist: {entry_path}")
        expected_status = route.get("expected_status")
        if type(expected_status) is not int or expected_status != 200:
            fail(path, "route.expected_status must be integer 200")
        if require_string(path, route, "content_type", f"routes[{index}]") != "text/html; charset=utf-8":
            fail(path, "route.content_type must be text/html; charset=utf-8")
    missing = set(cases) - seen
    if missing:
        fail(path, "network profile routes do not cover corpus cases: " + ", ".join(sorted(missing)))


def validate_profile(path: Path, payload: object) -> None:
    profile = require_object(path, payload, "profile")
    required = {
        "schema_version",
        "profile_id",
        "status",
        "created_at",
        "claim_status",
        "corpus_id",
        "server",
        "origin",
        "dns",
        "protocols",
        "cache",
        "network_conditions",
        "authentication",
        "routes",
        "unsupported",
    }
    reject_extra(path, profile, required, "profile")
    require_keys(path, profile, required, "profile")
    if profile.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    profile_id = require_string(path, profile, "profile_id", "profile")
    if not PROFILE_ID.fullmatch(profile_id):
        fail(path, "profile_id has invalid characters")
    if path.resolve() == DEFAULT_PROFILE.resolve():
        validate_sample_manifest_reference(path, profile_id)
    status = require_string(path, profile, "status", "profile")
    if status not in ALLOWED_STATUS:
        fail(path, f"status is not allowed: {status}")
    claim_status = require_string(path, profile, "claim_status", "profile")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    require_string(path, profile, "created_at", "profile")

    corpus_id, cases = corpus_cases(DEFAULT_CORPUS)
    if require_string(path, profile, "corpus_id", "profile") != corpus_id:
        fail(path, "profile.corpus_id must match the no-claim corpus manifest")

    validate_server(path, profile.get("server"))
    validate_origin(path, profile.get("origin"))
    validate_dns(path, profile.get("dns"))
    validate_protocols(path, profile.get("protocols"))
    validate_cache(path, profile.get("cache"))
    validate_network_conditions(path, profile.get("network_conditions"))
    validate_authentication(path, profile.get("authentication"))
    validate_routes(path, profile.get("routes"), cases)
    unsupported = require_string_array(path, profile, "unsupported", "profile")
    for phrase in [
        "no browser-run server evidence",
        "checked runner-managed lifecycle self-test",
        "no HTTP/2",
        "no HTTP/3",
        "no TLS",
        "no browser run",
    ]:
        if not any(phrase in item for item in unsupported):
            fail(path, f"profile.unsupported must mention: {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_PROFILE]
    try:
        for path in paths:
            validate_profile(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark network profile validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark network profile validation passed: {len(paths)} profile(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
