#!/usr/bin/env python3
"""Validate the no-claim profile/session source manifest for PB-016."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "storage" / "machine" / "profile-session-source-manifest.json"
SCHEMA = ROOT / "docs" / "storage" / "machine" / "profile-session-source-manifest.schema.json"

REQUIRED_AXES = {
    "origin_and_partition_identity",
    "storage_bucket_and_state_class",
    "transaction_commit_and_durability",
    "storage_backend_and_process_model",
    "abort_failure_and_quota",
    "origin_scoped_clearing",
    "browser_owned_state_separation",
    "migration_journal_and_recovery",
    "privacy_export_and_secret_exclusion",
    "unsupported_cases_and_claim_review",
}
REQUIRED_SOURCES = {
    "STORAGE-PROFILE-SOURCE-WHATWG-STORAGE",
    "STORAGE-PROFILE-SOURCE-W3C-INDEXEDDB",
    "STORAGE-PROFILE-SOURCE-W3C-CLEAR-SITE-DATA",
    "STORAGE-PROFILE-SOURCE-W3C-SECURITY-PRIVACY",
    "STORAGE-PROFILE-SOURCE-SQLITE-ATOMIC-COMMIT",
    "STORAGE-PROFILE-SOURCE-SQLITE-CORRUPTION",
    "STORAGE-PROFILE-SOURCE-LMDB-TRANSACTIONS",
    "STORAGE-PROFILE-SOURCE-ROCKSDB-TRANSACTIONS",
    "STORAGE-PROFILE-SOURCE-ROCKSDB-WAL",
    "STORAGE-PROFILE-SOURCE-WINDOWS-FLUSH",
    "STORAGE-PROFILE-SOURCE-WINDOWS-CREDENTIAL-MANAGER",
    "STORAGE-PROFILE-SOURCE-MACOS-KEYCHAIN",
    "STORAGE-PROFILE-SOURCE-LINUX-SECRET-SERVICE",
}
REQUIRED_UNSUPPORTED = {
    "No executable profile, Space, session, snapshot, or migration schema is approved by this manifest.",
    "No migration, rollback, crash, power-loss, quota, corruption, deletion, export, private-session, credential, or real-profile execution evidence exists.",
}


def fail(message: str) -> None:
    print(f"profile/session source validation failed: {message}", file=sys.stderr)
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
    if manifest.get("status") != "no_claim_profile_session_source_manifest":
        fail("status must remain no_claim_profile_session_source_manifest")
    if manifest.get("related_gate") != "PB-016":
        fail("related_gate must be PB-016")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "not", "production", "implementation"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete profile/session evidence set")

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
        fail("source IDs do not match the required profile/session source set")

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
        fail("unsupported must preserve the profile/session no-claim boundary")

    print(
        "profile/session source validation passed: "
        f"{len(sources)} sources, {len(axes)} evidence axes, PB-016 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
