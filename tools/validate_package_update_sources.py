#!/usr/bin/env python3
"""Validate the no-claim package/update source manifest for PB-017."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "release-operations" / "machine" / "package-update-source-manifest.json"
SCHEMA = ROOT / "docs" / "release-operations" / "machine" / "package-update-source-manifest.schema.json"

REQUIRED_AXES = {
    "metadata_roles_thresholds_and_freshness",
    "target_binding_and_rollback",
    "build_provenance_identity",
    "authorized_supply_chain_steps",
    "artifact_signing_and_transparency",
    "installation_transaction_and_recovery",
    "profile_transition_and_downgrade",
    "privacy_retention_and_claim_review",
}
REQUIRED_SOURCES = {
    "REL-UPDATE-SOURCE-TUF-METADATA",
    "REL-UPDATE-SOURCE-TUF-SECURITY",
    "REL-UPDATE-SOURCE-SLSA-PROVENANCE",
    "REL-UPDATE-SOURCE-SLSA-VERIFY",
    "REL-UPDATE-SOURCE-IN-TOTO-LAYOUT",
    "REL-UPDATE-SOURCE-SIGSTORE-SIGNING",
    "REL-UPDATE-SOURCE-SIGSTORE-BUNDLE",
    "REL-UPDATE-SOURCE-WINDOWS-SIGNTOOL",
    "REL-UPDATE-SOURCE-WINDOWS-CODE-SIGNING",
}
REQUIRED_UNSUPPORTED = {
    "No Turing package, updater, installer, metadata parser, signing hierarchy, or stable channel has been implemented or selected.",
    "No fake-key update lab, installation fault rehearsal, rollback result, profile migration result, or owner-reviewed PB-017 readiness decision exists.",
}


def fail(message: str) -> None:
    print(f"package/update source validation failed: {message}", file=sys.stderr)
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
    if manifest.get("status") != "no_claim_package_update_source_manifest":
        fail("status must remain no_claim_package_update_source_manifest")
    if manifest.get("related_gate") != "PB-017":
        fail("related_gate must be PB-017")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "not", "release", "production"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete package/update evidence set")

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    ids: set[str] = set()
    required_fields = {"source_id", "title", "publisher", "url", "retrieved", "observation", "decision_consequence"}
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            fail(f"sources[{index}] must be an object")
        if set(source) != required_fields:
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
        fail("source IDs do not match the required package/update source set")

    documents = manifest.get("source_documents")
    if not isinstance(documents, list) or not documents:
        fail("source_documents must be a non-empty array")
    for document in documents:
        path = ROOT / require_string(document, "source_documents entry")
        if not path.is_file():
            fail(f"source document is missing: {document}")

    unsupported = manifest.get("unsupported")
    if not isinstance(unsupported, list) or not REQUIRED_UNSUPPORTED <= set(unsupported):
        fail("unsupported must preserve the package/update no-claim boundary")

    print(
        "package/update source validation passed: "
        f"{len(sources)} sources, {len(axes)} evidence axes, PB-017 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
