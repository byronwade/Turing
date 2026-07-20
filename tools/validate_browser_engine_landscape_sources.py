#!/usr/bin/env python3
"""Validate the no-claim browser-engine landscape source manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/research/machine/browser-engine-landscape-source-manifest.json"
SCHEMA = ROOT / "docs/research/machine/browser-engine-landscape-source-manifest.schema.json"

REQUIRED_AXES = {
    "engine_architecture_and_process_model",
    "rendering_pipeline_and_compositor",
    "javascript_runtime_and_wasm",
    "developer_protocol_and_observability",
    "standards_and_compatibility",
    "security_privilege_and_site_isolation",
    "platform_integration_and_embedding",
    "project_governance_and_maintenance",
    "performance_methodology_and_claim_limits",
}
REQUIRED_SOURCES = {
    "ENGINE-SOURCE-CHROMIUM-RENDERING", "ENGINE-SOURCE-CHROMIUM-PROCESS", "ENGINE-SOURCE-CDP",
    "ENGINE-SOURCE-V8-SPARKPLUG", "ENGINE-SOURCE-V8-MAGLEV", "ENGINE-SOURCE-WEBKIT-DOCS",
    "ENGINE-SOURCE-WEBKIT2", "ENGINE-SOURCE-WEBKIT-SITE-ISOLATION", "ENGINE-SOURCE-JSC",
    "ENGINE-SOURCE-FIREFOX-PROCESS", "ENGINE-SOURCE-SPIDERMONKEY", "ENGINE-SOURCE-FIREFOX-PERFORMANCE",
    "ENGINE-SOURCE-SERVO", "ENGINE-SOURCE-LADYBIRD", "ENGINE-SOURCE-WPT", "ENGINE-SOURCE-WEBDRIVER-BIDI",
    "ENGINE-SOURCE-INTEROP", "ENGINE-SOURCE-BROWSERBENCH",
}


def fail(message: str) -> None:
    print(f"browser-engine landscape source validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
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
    if manifest.get("schema_version") != 1 or manifest.get("status") != "no_claim_engine_landscape_source_manifest":
        fail("manifest status or schema_version is invalid")
    if not {"RQ-16", "RQ-25"} <= set(manifest.get("related_questions", [])):
        fail("related_questions must include RQ-16 and RQ-25")
    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "no", "select", "approve"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")
    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete engine-landscape evidence set")
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    ids: set[str] = set()
    required = {"source_id", "title", "publisher", "url", "retrieved", "observation", "decision_consequence"}
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict) or set(source) != required:
            fail(f"sources[{index}] fields do not match the manifest schema")
        source_id = require_string(source["source_id"], f"sources[{index}].source_id")
        if source_id in ids:
            fail(f"duplicate source_id: {source_id}")
        ids.add(source_id)
        parsed = urlparse(require_string(source["url"], f"sources[{index}].url"))
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"sources[{index}].url must be an HTTPS URL")
        for key in ("title", "publisher", "retrieved", "observation", "decision_consequence"):
            require_string(source[key], f"sources[{index}].{key}")
    if ids != REQUIRED_SOURCES:
        fail("source IDs do not match the required engine-landscape source set")
    documents = manifest.get("source_documents")
    if not isinstance(documents, list) or not documents or len(documents) != len(set(documents)):
        fail("source_documents must be a non-empty unique array")
    for document in documents:
        if not (ROOT / require_string(document, "source_documents entry")).is_file():
            fail(f"source document is missing: {document}")
    unsupported = manifest.get("unsupported")
    if not isinstance(unsupported, list) or len(unsupported) < 4:
        fail("unsupported must preserve the engine-landscape no-claim boundary")
    print(f"browser-engine landscape source validation passed: {len(sources)} sources, {len(axes)} evidence axes, no-claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
