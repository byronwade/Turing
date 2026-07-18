#!/usr/bin/env python3
"""Validate ADR-0009 no-claim local compatibility corpus contracts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
    ROOT
    / "docs"
    / "blueprint-v1"
    / "machine"
    / "servo-local-compatibility-corpora"
    / "no-claim-tiny-adr0009.corpus.json"
)

CORPUS_ID = re.compile(r"^ADR9-EV-013\.[A-Z0-9._-]+$")
CASE_ID = re.compile(r"^ADR9-COMPAT-[A-Z0-9-]+$")
LOCAL_ORIGIN = re.compile(r"^https://[a-z0-9.-]+\.turing\.invalid/$")
LOCAL_URL = re.compile(r"^https://[a-z0-9.-]+\.turing\.invalid(?:/|$)")
URL = re.compile(r"https?://[^\s\"'<>]+")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
FIXTURE_ROOT = ROOT / "benchmarks" / "compatibility" / "adr0009" / "no-claim-tiny"
REQUIRED_CATEGORIES = {
    "static_document",
    "dynamic_dom_events",
    "origin_storage",
    "fetch_cors_csp",
    "webidl_js_binding",
    "form_editing_accessibility",
    "webdriver_headless_smoke",
    "crash_timeout_resource",
}
ALLOWED_STATUS = {"contract_only_no_browser_run", "draft_no_claim"}
REQUIRED_RUN_RECORD_PHRASES = {
    "source baseline",
    "binary hash",
    "operating system",
    "local server root",
    "per-case pass",
    "raw logs",
    "disabled-test",
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


def require_false(path: Path, obj: dict[str, object], key: str, label: str) -> None:
    if obj.get(key) is not False:
        fail(path, f"{label}.{key} must be false")


def require_true(path: Path, obj: dict[str, object], key: str, label: str) -> None:
    if obj.get(key) is not True:
        fail(path, f"{label}.{key} must be true")


def require_int(path: Path, obj: dict[str, object], key: str, label: str) -> int:
    value = obj.get(key)
    if type(value) is not int or value < 1:
        fail(path, f"{label}.{key} must be an integer >= 1")
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


def validate_fixture(
    path: Path,
    fixture: object,
    case_id: str,
    allowed_origins: set[str],
    seen_paths: set[str],
) -> str:
    item = require_object(path, fixture, "fixture")
    required = {
        "origin",
        "route_path",
        "fixture_path",
        "sha256",
        "bytes",
        "generated",
        "license",
    }
    reject_extra(path, item, required, "fixture")
    require_keys(path, item, required, "fixture")

    origin = require_string(path, item, "origin", "fixture")
    if origin not in allowed_origins:
        fail(path, f"{case_id}: fixture.origin must be listed in case.local_origins: {origin}")
    if not LOCAL_ORIGIN.fullmatch(origin):
        fail(path, f"{case_id}: fixture.origin must use a turing.invalid HTTPS origin: {origin}")

    route_path = require_string(path, item, "route_path", "fixture")
    if not route_path.startswith("/") or "\\" in route_path:
        fail(path, f"{case_id}: fixture.route_path must be an absolute URL path")

    fixture_path = require_string(path, item, "fixture_path", "fixture")
    if fixture_path in seen_paths:
        fail(path, f"duplicate fixture_path: {fixture_path}")
    seen_paths.add(fixture_path)
    resolved = (ROOT / fixture_path).resolve()
    try:
        resolved.relative_to(ROOT)
        resolved.relative_to(FIXTURE_ROOT)
    except ValueError:
        fail(path, f"{case_id}: fixture_path must stay under {relative(FIXTURE_ROOT)}: {fixture_path}")
    if not resolved.is_file():
        fail(path, f"{case_id}: fixture_path does not exist: {fixture_path}")
    if resolved.suffix != ".html":
        fail(path, f"{case_id}: fixture_path must be an HTML fixture: {fixture_path}")

    digest = require_string(path, item, "sha256", "fixture")
    if not SHA256.fullmatch(digest):
        fail(path, f"{case_id}: fixture.sha256 must be lowercase SHA-256")
    expected_bytes = require_int(path, item, "bytes", "fixture")
    require_true(path, item, "generated", "fixture")
    require_string(path, item, "license", "fixture")

    data = resolved.read_bytes()
    if len(data) != expected_bytes:
        fail(path, f"{case_id}: fixture.bytes does not match file length for {fixture_path}")
    actual = hashlib.sha256(data).hexdigest()
    if actual != digest:
        fail(path, f"{case_id}: fixture.sha256 does not match file bytes for {fixture_path}")
    text = data.decode("utf-8")
    if "\r" in text:
        fail(path, f"{case_id}: fixture file contains CR line endings: {fixture_path}")
    for url in URL.findall(text):
        if not LOCAL_URL.match(url):
            fail(path, f"{case_id}: fixture file contains non-local URL {url}: {fixture_path}")

    return origin


def validate_case(path: Path, case: object, seen: set[str], seen_paths: set[str]) -> str:
    item = require_object(path, case, "case")
    required = {
        "case_id",
        "category",
        "name",
        "purpose",
        "primary_risk",
        "local_origins",
        "required_assertion_groups",
        "required_artifacts",
        "failure_denominator",
        "wpt_focus_areas",
        "test262_relevance",
        "fixtures",
        "execution_status",
        "external_network_allowed",
        "compatibility_claim_allowed",
    }
    reject_extra(path, item, required, "case")
    require_keys(path, item, required, "case")

    case_id = require_string(path, item, "case_id", "case")
    if not CASE_ID.fullmatch(case_id):
        fail(path, f"case.case_id has invalid format: {case_id}")
    if case_id in seen:
        fail(path, f"duplicate case_id: {case_id}")
    seen.add(case_id)

    category = require_string(path, item, "category", "case")
    if category not in REQUIRED_CATEGORIES:
        fail(path, f"case.category is not allowed: {category}")
    for key in ("name", "purpose", "primary_risk", "test262_relevance"):
        require_string(path, item, key, "case")
    if require_string(path, item, "execution_status", "case") != "not_executed":
        fail(path, "case.execution_status must be not_executed")
    require_false(path, item, "external_network_allowed", "case")
    require_false(path, item, "compatibility_claim_allowed", "case")

    origins = require_string_array(path, item, "local_origins", "case")
    for origin in origins:
        if not LOCAL_ORIGIN.fullmatch(origin):
            fail(path, f"case.local_origins must use turing.invalid HTTPS origins: {origin}")
    require_string_array(path, item, "required_assertion_groups", "case")
    artifacts = require_string_array(path, item, "required_artifacts", "case")
    if "result-json" not in artifacts:
        fail(path, f"{case_id}: required_artifacts must include result-json")
    denominator = require_string_array(path, item, "failure_denominator", "case")
    if not any(value in denominator for value in ("timeout", "crash")):
        fail(path, f"{case_id}: failure_denominator must include timeout or crash")
    require_string_array(path, item, "wpt_focus_areas", "case")
    fixtures = item.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        fail(path, f"{case_id}: fixtures must be a non-empty array")
    fixture_origins = {
        validate_fixture(path, fixture, case_id, set(origins), seen_paths)
        for fixture in fixtures
    }
    missing_origins = set(origins) - fixture_origins
    if missing_origins:
        fail(path, f"{case_id}: fixtures are missing origins: {', '.join(sorted(missing_origins))}")
    return category


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "corpus_id",
        "status",
        "created_at",
        "related_gate",
        "evidence_id",
        "claim_status",
        "source_strategy_status",
        "run_status",
        "fixture_status",
        "fixture_root",
        "required_run_record",
        "cases",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")

    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    corpus_id = require_string(path, manifest, "corpus_id", "manifest")
    if not CORPUS_ID.fullmatch(corpus_id):
        fail(path, f"manifest.corpus_id has invalid format: {corpus_id}")
    status = require_string(path, manifest, "status", "manifest")
    if status not in ALLOWED_STATUS:
        fail(path, f"manifest.status is not allowed: {status}")
    if require_string(path, manifest, "related_gate", "manifest") != "PB-002":
        fail(path, "manifest.related_gate must be PB-002")
    if require_string(path, manifest, "evidence_id", "manifest") != "ADR9-EV-013":
        fail(path, "manifest.evidence_id must be ADR9-EV-013")
    if (
        require_string(path, manifest, "source_strategy_status", "manifest")
        != "no_source_strategy_decision"
    ):
        fail(path, "manifest.source_strategy_status must remain no_source_strategy_decision")
    if require_string(path, manifest, "run_status", "manifest") != "not_executed":
        fail(path, "manifest.run_status must remain not_executed")
    if (
        require_string(path, manifest, "fixture_status", "manifest")
        != "materialized_no_browser_run"
    ):
        fail(path, "manifest.fixture_status must be materialized_no_browser_run")
    if (
        require_string(path, manifest, "fixture_root", "manifest")
        != "benchmarks/compatibility/adr0009/no-claim-tiny"
    ):
        fail(path, "manifest.fixture_root must point to the checked ADR-0009 fixture root")
    if status == "contract_only_no_browser_run":
        fail(path, "manifest.status cannot remain contract_only_no_browser_run after fixtures exist")

    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in [
        "no browser run",
        "no Servo adoption",
        "no Turing compatibility claim",
        "no Chrome-class claim",
        "no WPT/Test262 pass-rate claim",
        "no release-code authorization",
    ]:
        if phrase not in claim_status:
            fail(path, f"manifest.claim_status must mention: {phrase}")

    run_record = require_string_array(path, manifest, "required_run_record", "manifest")
    missing_record = [
        phrase
        for phrase in REQUIRED_RUN_RECORD_PHRASES
        if not any(phrase in item for item in run_record)
    ]
    if missing_record:
        fail(path, "manifest.required_run_record is missing: " + ", ".join(missing_record))

    cases = manifest.get("cases")
    if not isinstance(cases, list):
        fail(path, "manifest.cases must be an array")
    seen: set[str] = set()
    seen_paths: set[str] = set()
    categories = {validate_case(path, case, seen, seen_paths) for case in cases}
    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        fail(
            path,
            "manifest.cases is missing required categories: "
            + ", ".join(sorted(missing_categories)),
        )
    extra_categories = categories - REQUIRED_CATEGORIES
    if extra_categories:
        fail(
            path,
            "manifest.cases contains unsupported categories: "
            + ", ".join(sorted(extra_categories)),
        )


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_MANIFEST]
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"Servo local compatibility corpus validation failed: {error}", file=sys.stderr)
        return 1
    print(f"Servo local compatibility corpus validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
