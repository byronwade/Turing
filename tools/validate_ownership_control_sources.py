#!/usr/bin/env python3
"""Validate the no-claim ownership/control source manifest for PB-019/PB-020."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "project-buildout" / "machine" / "ownership-control-source-manifest.json"
SCHEMA = ROOT / "docs" / "project-buildout" / "machine" / "ownership-control-source-manifest.schema.json"

REQUIRED_AXES = {
    "roles_responsibilities_and_authorities",
    "separation_of_duties_and_dual_control",
    "named_qualification_and_path_coverage",
    "codeowners_routing_and_team_access",
    "effective_branch_rules_and_bypass",
    "least_privilege_and_access_reconciliation",
    "succession_availability_and_emergency_replacement",
    "independent_review_expiry_and_claim_boundary",
}
REQUIRED_SOURCES = {
    "GOV-OWNERSHIP-SOURCE-NIST-CSF-GOVERN",
    "GOV-OWNERSHIP-SOURCE-NIST-AC5",
    "GOV-OWNERSHIP-SOURCE-GITHUB-CODEOWNERS",
    "GOV-OWNERSHIP-SOURCE-GITHUB-PROTECTED-BRANCHES",
    "GOV-OWNERSHIP-SOURCE-GITHUB-BRANCH-API",
}
REQUIRED_UNSUPPORTED = {
    "No qualified backup owner is named or verified by this manifest; current PB-019 primary-only/null-backup status remains unchanged.",
    "No authenticated repository access capture, effective branch-rule capture, CODEOWNERS exercise, two-person-control exercise, succession drill, or independent owner review exists.",
}


def fail(message: str) -> None:
    print(f"ownership/control source validation failed: {message}", file=sys.stderr)
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
    if manifest.get("status") != "no_claim_ownership_control_source_manifest":
        fail("status must remain no_claim_ownership_control_source_manifest")
    if manifest.get("related_gates") != ["PB-019", "PB-020"]:
        fail("related_gates must remain PB-019 and PB-020")

    claim_status = require_string(manifest.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "not", "authority", "production"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    axes = manifest.get("evidence_axes")
    if not isinstance(axes, list) or not REQUIRED_AXES <= set(axes):
        fail("evidence_axes must include the complete ownership/control evidence set")

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    ids: set[str] = set()
    required_fields = {"source_id", "title", "publisher", "url", "retrieved", "observation", "control_consequence"}
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
        for key in ("title", "publisher", "retrieved", "observation", "control_consequence"):
            require_string(source[key], f"sources[{index}].{key}")

    if ids != REQUIRED_SOURCES:
        fail("source IDs do not match the required ownership/control source set")

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
        fail("unsupported must preserve the ownership/control no-claim boundary")

    print(
        "ownership/control source validation passed: "
        f"{len(sources)} sources, {len(axes)} evidence axes, PB-019/PB-020 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
