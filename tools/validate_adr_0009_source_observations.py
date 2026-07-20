#!/usr/bin/env python3
"""Validate the no-claim upstream source observations for ADR-0009/PB-002."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "blueprint-v1" / "machine" / "adr-0009-source-observation-manifest.json"
SCHEMA = ROOT / "docs" / "blueprint-v1" / "machine" / "adr-0009-source-observation-manifest.schema.json"

REQUIRED_AXES = {
    "source_identity",
    "archive_equivalence",
    "dependency_pinning",
    "offline_reproducibility",
    "platform_bootstrap",
    "binary_artifact_provenance",
    "support_boundary",
}
REQUIRED_SOURCES = {
    "ADR9-SOURCE-SERVO-REPOSITORY",
    "ADR9-SOURCE-SERVO-LIVE-METADATA",
    "ADR9-SOURCE-MOZJS-LIVE-METADATA",
    "ADR9-SOURCE-SERVO-GETTING-CODE",
    "ADR9-SOURCE-SERVO-OFFLINE-BUILD",
    "ADR9-SOURCE-SERVO-CRATE-DEPENDENCIES",
    "ADR9-SOURCE-SERVO-PINNED-GIT-DEPENDENCIES",
}
REQUIRED_UNSUPPORTED = {
    "No owner-selected ADR-0009 source baseline exists.",
    "No independent clean-host reproduction or owner-reviewed replay acceptance exists.",
}


def fail(message: str) -> None:
    print(f"ADR-0009 source-observation validation failed: {message}", file=sys.stderr)
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
    if manifest.get("status") != "no_claim_source_observation_manifest":
        fail("status must remain no_claim_source_observation_manifest")
    if set(manifest.get("related_gates", [])) != {"PB-002", "ADR-0009"}:
        fail("related_gates must contain PB-002 and ADR-0009")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "not", "baseline", "approval", "authorization"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("observation_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("observation_axes must include the complete source-strategy evidence set")

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
        fail("source IDs do not match the required upstream source set")

    documents = manifest.get("source_documents")
    if not isinstance(documents, list) or not documents:
        fail("source_documents must be a non-empty array")
    if len(documents) != len(set(documents)):
        fail("source_documents must not contain duplicate paths")
    for document in documents:
        path = ROOT / require_string(document, "source_documents entry")
        if not path.is_file():
            fail(f"source document is missing: {document}")

    unsupported = manifest.get("unsupported")
    if not isinstance(unsupported, list) or not REQUIRED_UNSUPPORTED <= set(unsupported):
        fail("unsupported must preserve the source-strategy no-claim boundary")

    print(
        "ADR-0009 source-observation validation passed: "
        f"{len(sources)} sources, {len(axes)} observation axes, PB-002 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
