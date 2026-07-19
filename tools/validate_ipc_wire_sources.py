#!/usr/bin/env python3
"""Validate the no-claim IPC wire-source manifest for PB-011."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "blueprint-v1" / "machine" / "ipc-wire-source-manifest.json"
SCHEMA = ROOT / "docs" / "blueprint-v1" / "machine" / "ipc-wire-source-manifest.schema.json"

REQUIRED_AXES = {
    "deterministic_encoding",
    "bounds_and_allocation",
    "schema_evolution",
    "unknown_values",
    "generated_provenance",
    "fuzzability",
    "platform_authentication",
    "resource_cost",
    "cross_language_maintenance",
}
REQUIRED_SOURCES = {
    "IPC-SOURCE-IETF-RFC8949",
    "IPC-SOURCE-PROTOBUF-ENCODING",
    "IPC-SOURCE-PROTOBUF-SPEC",
    "IPC-SOURCE-FLATBUFFERS-SCHEMA",
    "IPC-SOURCE-FLATBUFFERS-EVOLUTION",
}
REQUIRED_UNSUPPORTED = {
    "No IPC encoding has been selected.",
    "No schema generator or serialization dependency has been approved.",
}


def fail(message: str) -> None:
    print(f"IPC wire-source validation failed: {message}", file=sys.stderr)
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
    if manifest.get("status") != "no_claim_wire_source_manifest":
        fail("status must remain no_claim_wire_source_manifest")
    if manifest.get("related_gate") != "PB-011":
        fail("related_gate must be PB-011")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "not", "selected", "approval", "production"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete IPC wire evidence set")

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    ids: set[str] = set()
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            fail(f"sources[{index}] must be an object")
        required = {"source_id", "title", "publisher", "url", "retrieved", "observation", "decision_consequence"}
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
        for key in ("title", "publisher", "retrieved", "observation", "decision_consequence"):
            require_string(source[key], f"sources[{index}].{key}")

    if ids != REQUIRED_SOURCES:
        fail("source IDs do not match the required CBOR/Protocol Buffers/FlatBuffers source set")

    documents = manifest.get("source_documents")
    if not isinstance(documents, list) or not documents:
        fail("source_documents must be a non-empty array")
    for document in documents:
        path = ROOT / require_string(document, "source_documents entry")
        if not path.is_file():
            fail(f"source document is missing: {document}")

    unsupported = manifest.get("unsupported")
    if not isinstance(unsupported, list) or not REQUIRED_UNSUPPORTED <= set(unsupported):
        fail("unsupported must preserve the IPC no-claim boundary")

    print(
        "IPC wire-source validation passed: "
        f"{len(sources)} sources, {len(axes)} evidence axes, PB-011 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
