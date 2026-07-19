#!/usr/bin/env python3
"""Validate the no-claim web-platform source manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "web-platform" / "machine" / "web-platform-source-manifest.json"
SCHEMA = ROOT / "docs" / "web-platform" / "machine" / "web-platform-source-manifest.schema.json"

REQUIRED_GATES = {"PB-002", "PB-020"}
REQUIRED_AXES = {
    "normative_spec_identity_and_revision",
    "test_suite_commit_manifest_and_harness",
    "dependency_graph_and_denominator",
    "interop_and_multi_implementer_context",
    "security_privacy_accessibility_and_abuse_review",
    "feature_lifecycle_experiment_and_deprecation",
    "differential_testing_and_failure_accounting",
    "unsupported_behavior_and_claim_review",
}
REQUIRED_SOURCES = {
    "WEB-SOURCE-WHATWG-HTML",
    "WEB-SOURCE-WHATWG-DOM",
    "WEB-SOURCE-WHATWG-FETCH",
    "WEB-SOURCE-CSSWG-DRAFTS",
    "WEB-SOURCE-ECMA-262",
    "WEB-SOURCE-TEST262",
    "WEB-SOURCE-WPT",
    "WEB-SOURCE-INTEROP",
    "WEB-SOURCE-WEBDRIVER-BIDI",
    "WEB-SOURCE-DESIGN-PRINCIPLES",
}
REQUIRED_UNSUPPORTED = {
    "No HTML, DOM, CSS, Fetch, ECMAScript, WPT, Test262, Interop, or WebDriver BiDi execution has been established by this manifest.",
    "No exact standards snapshot, WPT/Test262 denominator, browser-run artifact package, or differential result is accepted as current compatibility evidence here.",
    "No feature is selected for implementation, no web-platform API is supported, and no compatibility exception or user-agent intervention is approved.",
}


def fail(message: str) -> None:
    print(f"web-platform source validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty string")
    return value


def main() -> int:
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read manifest or schema: {exc}")

    if schema.get("properties", {}).get("schema_version", {}).get("const") != 1:
        fail("schema must declare schema_version 1")
    if manifest.get("schema_version") != 1:
        fail("schema_version must be 1")
    if manifest.get("status") != "no_claim_web_platform_source_manifest":
        fail("status must remain no_claim_web_platform_source_manifest")
    if set(manifest.get("related_gates", [])) != REQUIRED_GATES:
        fail("related_gates must contain PB-002 and PB-020")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "standards", "compatibility", "security", "accessibility", "performance", "production"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete web-platform evidence set")

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    source_ids: set[str] = set()
    categories: set[str] = set()
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            fail(f"sources[{index}] must be an object")
        required = {"source_id", "category", "title", "publisher", "url", "retrieved", "observation", "evidence_consequence"}
        if set(source) != required:
            fail(f"sources[{index}] fields do not match the manifest schema")
        source_id = require_string(source["source_id"], f"sources[{index}].source_id")
        if source_id in source_ids:
            fail(f"duplicate source_id: {source_id}")
        source_ids.add(source_id)
        categories.add(require_string(source["category"], f"sources[{index}].category"))
        url = require_string(source["url"], f"sources[{index}].url")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"sources[{index}].url must be an HTTPS URL")
        for key in ("title", "publisher", "retrieved", "observation", "evidence_consequence"):
            require_string(source[key], f"sources[{index}].{key}")
    if source_ids != REQUIRED_SOURCES:
        fail("source IDs do not match the required standards and conformance source set")
    if not {"standard", "test-suite", "interop", "language", "protocol", "governance"} <= categories:
        fail("sources must cover standards, language, test-suite, interop, protocol, and governance categories")

    documents = manifest.get("source_documents")
    if not isinstance(documents, list) or not documents:
        fail("source_documents must be a non-empty array")
    for document in documents:
        path = ROOT / require_string(document, "source_documents entry")
        if not path.is_file():
            fail(f"source document is missing: {document}")

    unsupported = manifest.get("unsupported")
    if not isinstance(unsupported, list) or not REQUIRED_UNSUPPORTED <= set(unsupported):
        fail("unsupported must preserve the web-platform no-claim boundary")

    print(
        "web-platform source validation passed: "
        f"{len(sources)} sources, {len(axes)} evidence axes, PB-002/PB-020 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
