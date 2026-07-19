#!/usr/bin/env python3
"""Validate the no-claim benchmark-source manifest for PB-013."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "blueprint-v1" / "machine" / "benchmark-source-manifest.json"
SCHEMA = ROOT / "docs" / "blueprint-v1" / "machine" / "benchmark-source-manifest.schema.json"

REQUIRED_AXES = {
    "suite_identity_version",
    "workload_integrity",
    "harness_controls",
    "warmup_and_statistics",
    "hardware_os_controls",
    "browser_pin",
    "trace_artifact",
    "failure_denominator",
    "equal_security_lifecycle",
    "claim_review_and_expiry",
}
REQUIRED_SOURCES = {
    "BENCH-SOURCE-SPEEDOMETER-METHODOLOGY",
    "BENCH-SOURCE-SPEEDOMETER-INSTRUCTIONS",
    "BENCH-SOURCE-JETSTREAM-METHODOLOGY",
    "BENCH-SOURCE-MOTIONMARK-METHODOLOGY",
    "BENCH-SOURCE-CHROMIUM-REGRESSION-POLICY",
    "BENCH-SOURCE-CHROMIUM-TELEMETRY",
    "BENCH-SOURCE-WPT-DOCUMENTATION",
    "BENCH-SOURCE-CHROME-PERFORMANCE-REPORT",
    "BENCH-SOURCE-MICROSOFT-WPR",
    "BENCH-SOURCE-MICROSOFT-ETW",
    "BENCH-SOURCE-PERFETTO-TRACE-CONFIG",
}
REQUIRED_UNSUPPORTED = {
    "No Turing browser benchmark has been run.",
    "No owner-reviewed benchmark readiness or statistics analysis exists.",
}


def fail(message: str) -> None:
    print(f"benchmark source validation failed: {message}", file=sys.stderr)
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
    if manifest.get("status") != "no_claim_benchmark_source_manifest":
        fail("status must remain no_claim_benchmark_source_manifest")
    if manifest.get("related_gate") != "PB-013":
        fail("related_gate must be PB-013")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "not", "result", "comparison", "claim"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete benchmark evidence set")

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    ids: set[str] = set()
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            fail(f"sources[{index}] must be an object")
        required = {"source_id", "title", "publisher", "url", "retrieved", "observation", "run_consequence"}
        if set(source) != required:
            fail(f"sources[{index}] fields do not match the manifest schema")
        source_id = require_string(source["source_id"], f"sources[{index}].source_id")
        if source_id in ids:
            fail(f"duplicate source_id: {source_id}")
        ids.add(source_id)
        url = require_string(source["url"], f"sources[{index}].url")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"sources[{index}].url must be an HTTPS URL")
        for key in ("title", "publisher", "retrieved", "observation", "run_consequence"):
            require_string(source[key], f"sources[{index}].{key}")

    if ids != REQUIRED_SOURCES:
        fail("source IDs do not match the required benchmark source set")

    documents = manifest.get("source_documents")
    if not isinstance(documents, list) or not documents:
        fail("source_documents must be a non-empty array")
    for document in documents:
        path = ROOT / require_string(document, "source_documents entry")
        if not path.is_file():
            fail(f"source document is missing: {document}")

    unsupported = manifest.get("unsupported")
    if not isinstance(unsupported, list) or not REQUIRED_UNSUPPORTED <= set(unsupported):
        fail("unsupported must preserve the benchmark no-claim boundary")

    print(
        "benchmark source validation passed: "
        f"{len(sources)} sources, {len(axes)} evidence axes, PB-013 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
