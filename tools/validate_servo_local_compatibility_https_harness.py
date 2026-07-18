#!/usr/bin/env python3
"""Validate ADR-0009 no-claim HTTPS host-alias harness plans."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import validate_servo_local_compatibility_corpus as corpus_validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = (
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "servo-local-compatibility-harnesses"
    / "no-claim-https-host-alias.plan.json"
)

HARNESS_ID = re.compile(r"^ADR9-EV-013\.HTTPS_HOST_ALIAS\.[A-Z0-9._-]+$")
LOCAL_ORIGIN = re.compile(r"^https://[a-z0-9.-]+\.turing\.invalid/$")
LOCAL_HOST = re.compile(r"^[a-z0-9.-]+\.turing\.invalid$")
REQUIRED_CLAIM_PHRASES = {
    "no browser run",
    "no Servo adoption",
    "no Turing compatibility claim",
    "no Chrome-class claim",
    "no WPT/Test262 pass-rate claim",
    "no HTTPS execution evidence",
    "no release-code authorization",
}
REQUIRED_BROWSER_RECORD_PHRASES = {
    "source baseline",
    "Servo binary path",
    "operating system",
    "HTTPS server command",
    "certificate fingerprint",
    "host-alias state",
    "per-origin route result",
    "per-case pass",
    "failure-denominator accounting",
}
REQUIRED_CERT_ARTIFACT_PHRASES = {
    "fingerprint",
    "private-key non-commitment",
    "trust-store",
    "TLS protocol",
    "cleanup proof",
}
REQUIRED_HOST_ARTIFACT_PHRASES = {
    "host-to-loopback",
    "before/after",
    "browser-visible origin",
    "cleanup proof",
    "failure record",
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


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
    ):
        fail(path, f"{label}.{key} must be a non-empty array of strings")
    return value


def require_bool(path: Path, obj: dict[str, object], key: str, label: str, expected: bool) -> None:
    if obj.get(key) is not expected:
        fail(path, f"{label}.{key} must be {str(expected).lower()}")


def reject_extra(path: Path, obj: dict[str, object], allowed: set[str], label: str) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(path: Path, obj: dict[str, object], required: set[str], label: str) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def host_for_origin(origin: str) -> str:
    host = urlsplit(origin).hostname
    if not host:
        raise ValidationError(f"origin has no host: {origin}")
    return host


def corpus_origins(path: Path, manifest_path: Path) -> dict[str, dict[str, object]]:
    payload = corpus_validator.load_json(manifest_path)
    corpus_validator.validate_manifest(manifest_path, payload)
    manifest = require_object(path, payload, "corpus_manifest")
    origins: dict[str, dict[str, object]] = {}
    cases = manifest.get("cases")
    if not isinstance(cases, list):
        fail(path, "corpus manifest cases must be an array")
    for case_value in cases:
        case = require_object(path, case_value, "case")
        fixtures = case.get("fixtures")
        if not isinstance(fixtures, list):
            fail(path, "corpus case fixtures must be an array")
        for fixture_value in fixtures:
            fixture = require_object(path, fixture_value, "fixture")
            origin = require_string(path, fixture, "origin", "fixture")
            route_path = require_string(path, fixture, "route_path", "fixture")
            record = origins.setdefault(
                origin,
                {
                    "host": host_for_origin(origin),
                    "fixture_count": 0,
                    "route_paths": set(),
                },
            )
            record["fixture_count"] = int(record["fixture_count"]) + 1
            route_paths = record["route_paths"]
            if not isinstance(route_paths, set):
                fail(path, "internal route path accumulator error")
            route_paths.add(route_path)
    return origins


def require_phrase_set(path: Path, label: str, values: list[str], phrases: set[str]) -> None:
    missing = [phrase for phrase in phrases if not any(phrase in value for value in values)]
    if missing:
        fail(path, f"{label} is missing required phrase(s): {', '.join(sorted(missing))}")


def validate_tls(path: Path, plan: dict[str, object], expected_hosts: set[str]) -> None:
    tls = require_object(path, plan.get("tls_plan"), "tls_plan")
    required = {
        "certificate_strategy",
        "certificate_private_key_committed",
        "tls_version_min",
        "sni_required",
        "san_hosts",
        "trust_store_modification_policy",
        "certificate_artifacts_required",
    }
    reject_extra(path, tls, required, "tls_plan")
    require_keys(path, tls, required, "tls_plan")
    require_string(path, tls, "certificate_strategy", "tls_plan")
    require_bool(path, tls, "certificate_private_key_committed", "tls_plan", False)
    require_string(path, tls, "tls_version_min", "tls_plan")
    require_bool(path, tls, "sni_required", "tls_plan", True)
    san_hosts = require_string_array(path, tls, "san_hosts", "tls_plan")
    invalid_hosts = [host for host in san_hosts if not LOCAL_HOST.fullmatch(host)]
    if invalid_hosts:
        fail(path, f"tls_plan.san_hosts contains invalid hosts: {', '.join(invalid_hosts)}")
    if set(san_hosts) != expected_hosts:
        fail(path, "tls_plan.san_hosts must exactly match corpus fixture hosts")
    trust_policy = require_string(path, tls, "trust_store_modification_policy", "tls_plan")
    for phrase in ["isolated profile", "cleanup", "persistent"]:
        if phrase not in trust_policy:
            fail(path, f"tls_plan.trust_store_modification_policy must mention {phrase}")
    require_phrase_set(
        path,
        "tls_plan.certificate_artifacts_required",
        require_string_array(path, tls, "certificate_artifacts_required", "tls_plan"),
        REQUIRED_CERT_ARTIFACT_PHRASES,
    )


def validate_host_alias(path: Path, plan: dict[str, object]) -> None:
    host_alias = require_object(path, plan.get("host_alias_plan"), "host_alias_plan")
    required = {
        "mode",
        "external_dns_allowed",
        "persistent_hosts_file_allowed",
        "host_header_substitute_for_browser_allowed",
        "cleanup_required",
        "required_artifacts",
    }
    reject_extra(path, host_alias, required, "host_alias_plan")
    require_keys(path, host_alias, required, "host_alias_plan")
    mode = require_string(path, host_alias, "mode", "host_alias_plan")
    for phrase in ["transient host alias", "browser execution", "Host headers"]:
        if phrase not in mode:
            fail(path, f"host_alias_plan.mode must mention {phrase}")
    require_bool(path, host_alias, "external_dns_allowed", "host_alias_plan", False)
    require_bool(path, host_alias, "persistent_hosts_file_allowed", "host_alias_plan", False)
    require_bool(path, host_alias, "host_header_substitute_for_browser_allowed", "host_alias_plan", False)
    require_bool(path, host_alias, "cleanup_required", "host_alias_plan", True)
    require_phrase_set(
        path,
        "host_alias_plan.required_artifacts",
        require_string_array(path, host_alias, "required_artifacts", "host_alias_plan"),
        REQUIRED_HOST_ARTIFACT_PHRASES,
    )


def validate_origin_bindings(
    path: Path,
    plan: dict[str, object],
    expected_origins: dict[str, dict[str, object]],
) -> None:
    bindings = plan.get("origin_bindings")
    if not isinstance(bindings, list) or not bindings:
        fail(path, "origin_bindings must be a non-empty array")
    seen: dict[str, dict[str, object]] = {}
    required = {"origin", "host", "fixture_count", "route_paths"}
    for binding_value in bindings:
        binding = require_object(path, binding_value, "origin_binding")
        reject_extra(path, binding, required, "origin_binding")
        require_keys(path, binding, required, "origin_binding")
        origin = require_string(path, binding, "origin", "origin_binding")
        if not LOCAL_ORIGIN.fullmatch(origin):
            fail(path, f"origin_binding.origin is invalid: {origin}")
        host = require_string(path, binding, "host", "origin_binding")
        if host != host_for_origin(origin):
            fail(path, f"{origin}: host must match origin host")
        fixture_count = binding.get("fixture_count")
        if type(fixture_count) is not int or fixture_count < 1:
            fail(path, f"{origin}: fixture_count must be an integer >= 1")
        route_paths = require_string_array(path, binding, "route_paths", "origin_binding")
        seen[origin] = {
            "host": host,
            "fixture_count": fixture_count,
            "route_paths": set(route_paths),
        }
    if set(seen) != set(expected_origins):
        fail(path, "origin_bindings must exactly match corpus fixture origins")
    for origin, expected in expected_origins.items():
        actual = seen[origin]
        if actual["host"] != expected["host"]:
            fail(path, f"{origin}: host differs from corpus fixture host")
        if actual["fixture_count"] != expected["fixture_count"]:
            fail(path, f"{origin}: fixture_count differs from corpus fixtures")
        if actual["route_paths"] != expected["route_paths"]:
            fail(path, f"{origin}: route_paths differ from corpus fixtures")


def validate_plan(path: Path, payload: object) -> None:
    plan = require_object(path, payload, "plan")
    required = {
        "schema_version",
        "harness_id",
        "status",
        "created_at",
        "related_gate",
        "evidence_id",
        "source_strategy_status",
        "claim_status",
        "corpus_manifest",
        "route_self_test_tool",
        "execution_status",
        "tls_plan",
        "host_alias_plan",
        "origin_bindings",
        "required_browser_run_record",
        "prohibited_claims",
        "unsupported",
    }
    reject_extra(path, plan, required, "plan")
    require_keys(path, plan, required, "plan")
    if plan.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    harness_id = require_string(path, plan, "harness_id", "plan")
    if not HARNESS_ID.fullmatch(harness_id):
        fail(path, f"plan.harness_id has invalid format: {harness_id}")
    if require_string(path, plan, "status", "plan") != "plan_only_no_browser_run":
        fail(path, "plan.status must be plan_only_no_browser_run")
    if require_string(path, plan, "related_gate", "plan") != "PB-002":
        fail(path, "plan.related_gate must be PB-002")
    if require_string(path, plan, "evidence_id", "plan") != "ADR9-EV-013":
        fail(path, "plan.evidence_id must be ADR9-EV-013")
    if require_string(path, plan, "source_strategy_status", "plan") != "no_source_strategy_decision":
        fail(path, "plan.source_strategy_status must remain no_source_strategy_decision")
    if require_string(path, plan, "execution_status", "plan") != "not_executed":
        fail(path, "plan.execution_status must remain not_executed")
    claim_status = require_string(path, plan, "claim_status", "plan")
    missing_claims = [phrase for phrase in REQUIRED_CLAIM_PHRASES if phrase not in claim_status]
    if missing_claims:
        fail(path, "plan.claim_status is missing: " + ", ".join(sorted(missing_claims)))

    corpus_manifest = require_string(path, plan, "corpus_manifest", "plan")
    corpus_path = (ROOT / corpus_manifest).resolve()
    try:
        corpus_path.relative_to(ROOT)
    except ValueError:
        fail(path, f"plan.corpus_manifest points outside repository: {corpus_manifest}")
    if corpus_path != corpus_validator.DEFAULT_MANIFEST:
        fail(path, "plan.corpus_manifest must point to the checked ADR-0009 corpus manifest")
    route_tool = require_string(path, plan, "route_self_test_tool", "plan")
    if route_tool != "tools/serve_servo_local_compatibility_corpus.py":
        fail(path, "plan.route_self_test_tool must point to the checked route self-test")
    if not (ROOT / route_tool).is_file():
        fail(path, f"plan.route_self_test_tool does not exist: {route_tool}")

    expected_origins = corpus_origins(path, corpus_path)
    expected_hosts = {str(record["host"]) for record in expected_origins.values()}
    validate_tls(path, plan, expected_hosts)
    validate_host_alias(path, plan)
    validate_origin_bindings(path, plan, expected_origins)
    require_phrase_set(
        path,
        "required_browser_run_record",
        require_string_array(path, plan, "required_browser_run_record", "plan"),
        REQUIRED_BROWSER_RECORD_PHRASES,
    )
    prohibited = require_string_array(path, plan, "prohibited_claims", "plan")
    for phrase in ["Servo adoption", "Turing compatibility", "Chrome-class compatibility"]:
        if phrase not in prohibited:
            fail(path, f"prohibited_claims must include {phrase}")
    unsupported = " ".join(require_string_array(path, plan, "unsupported", "plan"))
    for phrase in ["no HTTPS server", "no certificate", "no Servo", "no WPT", "no compatibility"]:
        if phrase not in unsupported:
            fail(path, f"unsupported must mention {phrase}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_PLAN]
    try:
        for path in paths:
            validate_plan(path, load_json(path))
    except (ValidationError, corpus_validator.ValidationError) as error:
        print(f"Servo local compatibility HTTPS harness validation failed: {error}", file=sys.stderr)
        return 1
    print(f"Servo local compatibility HTTPS harness validation passed: {len(paths)} plan(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
