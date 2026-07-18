#!/usr/bin/env python3
"""Validate benchmark corpus fixtures without third-party packages."""

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
    / "benchmark-corpora"
    / "no-claim-smoke.corpus.json"
)

CORPUS_ID = re.compile(r"^[A-Z0-9][A-Z0-9._-]+$")
CASE_ID = re.compile(r"^PB13-CORPUS-[A-Z0-9._-]+$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
ALLOWED_STATUS = {"sample_only_no_benchmark_result", "draft", "reviewed"}
REQUIRED_CATEGORIES = {
    "static_document",
    "app_like",
    "accessibility",
    "international_text",
    "hostile_markup",
    "media_document",
    "service_worker_contract",
}
ALLOWED_CATEGORY = REQUIRED_CATEGORIES


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


def require_int(path: Path, obj: dict[str, object], key: str, label: str) -> int:
    value = obj.get(key)
    if type(value) is not int or value < 1:
        fail(path, f"{label}.{key} must be an integer >= 1")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(path, f"{label}.{key} must be an array of strings")
    return value


def validate_case(path: Path, case: object, seen: set[str]) -> None:
    item = require_object(path, case, "case")
    required = {
        "case_id",
        "name",
        "category",
        "entry_path",
        "top_level_site",
        "sha256",
        "bytes",
        "generated",
        "license",
        "expected_m0_status",
        "external_network_allowed",
        "measurement_claim_allowed",
    }
    optional = {"features"}
    reject_extra(path, item, required | optional, "case")
    require_keys(path, item, required, "case")

    case_id = require_string(path, item, "case_id", "case")
    if not CASE_ID.fullmatch(case_id):
        fail(path, f"case.case_id has invalid format: {case_id}")
    if case_id in seen:
        fail(path, f"duplicate case_id: {case_id}")
    seen.add(case_id)

    require_string(path, item, "name", "case")
    category = require_string(path, item, "category", "case")
    if category not in ALLOWED_CATEGORY:
        fail(path, f"case.category is not allowed: {category}")

    top_level_site = require_string(path, item, "top_level_site", "case")
    if not top_level_site.startswith("https://turing.invalid/"):
        fail(path, "case.top_level_site must use the turing.invalid test origin")

    digest = require_string(path, item, "sha256", "case")
    if not SHA256.fullmatch(digest):
        fail(path, "case.sha256 must be lowercase SHA-256")
    expected_bytes = require_int(path, item, "bytes", "case")
    if not require_bool(path, item, "generated", "case"):
        fail(path, "seed corpus cases must be generated content")
    require_string(path, item, "license", "case")
    require_string(path, item, "expected_m0_status", "case")
    if require_bool(path, item, "external_network_allowed", "case"):
        fail(path, "seed corpus cases must not allow external network access")
    if require_bool(path, item, "measurement_claim_allowed", "case"):
        fail(path, "seed corpus cases must not allow measurement claims")
    if "features" in item:
        require_string_array(path, item, "features", "case")

    entry = require_string(path, item, "entry_path", "case")
    resolved = (ROOT / entry).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        fail(path, f"case.entry_path points outside repository: {entry}")
    if not resolved.is_file():
        fail(path, f"case.entry_path does not exist: {entry}")
    if not resolved.is_relative_to(ROOT / "benchmarks" / "corpus"):
        fail(path, f"case.entry_path must live under benchmarks/corpus: {entry}")
    data = resolved.read_bytes()
    if len(data) != expected_bytes:
        fail(path, f"case.bytes does not match file length for {entry}")
    actual = hashlib.sha256(data).hexdigest()
    if actual != digest:
        fail(path, f"case.sha256 does not match file bytes for {entry}")
    text = data.decode("utf-8")
    if "\r" in text:
        fail(path, f"case file contains CR line endings: {entry}")
    lowered = text.lower()
    for forbidden in ("http://", "https://", "src=\"//", "href=\"//"):
        if forbidden in lowered:
            fail(path, f"case file may not contain external network reference: {entry}")


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {"schema_version", "corpus_id", "status", "created_at", "license", "cases"}
    optional = {"purpose"}
    reject_extra(path, manifest, required | optional, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    corpus_id = require_string(path, manifest, "corpus_id", "manifest")
    if not CORPUS_ID.fullmatch(corpus_id):
        fail(path, "corpus_id has invalid characters")
    status = require_string(path, manifest, "status", "manifest")
    if status not in ALLOWED_STATUS:
        fail(path, f"status is not allowed: {status}")
    require_string(path, manifest, "created_at", "manifest")
    require_string(path, manifest, "license", "manifest")
    if "purpose" in manifest:
        require_string(path, manifest, "purpose", "manifest")

    cases = manifest.get("cases")
    if not isinstance(cases, list) or len(cases) < 2:
        fail(path, "cases must contain at least two corpus cases")
    seen: set[str] = set()
    categories: set[str] = set()
    for case in cases:
        case_obj = require_object(path, case, "case")
        categories.add(str(case_obj.get("category")))
        validate_case(path, case, seen)
    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        fail(
            path,
            "seed corpus is missing required categories: "
            + ", ".join(sorted(missing_categories)),
        )


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_MANIFEST]
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark corpus validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark corpus validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
