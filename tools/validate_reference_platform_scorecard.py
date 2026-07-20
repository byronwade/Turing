#!/usr/bin/env python3
"""Validate the no-claim PB-006 reference-platform scorecard."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCORECARD = ROOT / "docs" / "platform" / "machine" / "reference-platform-scorecard.json"
SCHEMA = ROOT / "docs" / "platform" / "machine" / "reference-platform-scorecard.schema.json"

REQUIRED_GATES = {"PB-006", "PB-003", "PB-004", "PB-005", "PB-008", "PB-009", "PB-012", "PB-013", "PB-015", "PB-017", "PB-018"}
REQUIRED_PLATFORMS = {"windows", "macos", "linux"}
REQUIRED_CANDIDATES = {"reference-windows-x64", "reference-macos-arm64", "reference-linux-wayland-x64"}
REQUIRED_SOURCES = {
    "PLAT-SOURCE-RUST-PLATFORM-SUPPORT",
    "PLAT-SOURCE-GITHUB-RUNNERS",
    "PLAT-SOURCE-WINDOWS-DESKTOP",
    "PLAT-SOURCE-WINDOWS-UIAUTOMATION",
    "PLAT-SOURCE-WINDOWS-NARRATOR",
    "PLAT-SOURCE-MACOS-APPKIT",
    "PLAT-SOURCE-MACOS-ACCESSIBILITY",
    "PLAT-SOURCE-MACOS-VOICEOVER",
    "PLAT-SOURCE-LINUX-WAYLAND",
    "PLAT-SOURCE-LINUX-DESKTOP-PORTALS",
    "PLAT-SOURCE-LINUX-ORCA",
}
REQUIRED_DIMENSIONS = {
    "window_display_and_lifecycle",
    "input_ime_clipboard_and_drag_drop",
    "accessibility_and_assistive_technology",
    "graphics_compositor_and_software_fallback",
    "sandbox_permissions_and_broker_surfaces",
    "toolchain_ci_and_reproducibility",
    "packaging_startup_update_and_recovery",
    "power_thermal_sleep_and_resume",
    "benchmark_hardware_and_resource_attribution",
    "support_scope_ownership_and_incident_capacity",
    "unsupported_cases_and_claim_review",
}
REQUIRED_UNSUPPORTED = {
    "No reference desktop platform is selected.",
    "No platform scorecard row has been executed on hardware or a clean host.",
    "No platform is supported, compatible, accessible, secure, performant, or production-ready from this scorecard.",
}


def fail(message: str) -> None:
    print(f"reference-platform scorecard validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty string")
    return value


def main() -> int:
    try:
        scorecard = json.loads(SCORECARD.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read scorecard or schema: {exc}")

    if schema.get("properties", {}).get("schema_version", {}).get("const") != 1:
        fail("schema must declare schema_version 1")
    if scorecard.get("schema_version") != 1:
        fail("schema_version must be 1")
    if scorecard.get("status") != "no_claim_reference_platform_scorecard":
        fail("status must remain no_claim_reference_platform_scorecard")
    if not REQUIRED_GATES <= set(scorecard.get("related_gates", [])):
        fail("related_gates must include PB-006 and all dependent platform lanes")

    claim_status = require_string(scorecard.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "no platform", "selected", "supported", "production-ready"):
        if phrase not in claim_status:
            fail(f"claim_status must preserve {phrase!r} boundary")

    dimensions = scorecard.get("evidence_dimensions")
    if not isinstance(dimensions, list) or not REQUIRED_DIMENSIONS <= set(dimensions):
        fail("evidence_dimensions must include the complete reference-platform set")

    sources = scorecard.get("sources")
    if not isinstance(sources, list):
        fail("sources must be an array")
    source_ids: set[str] = set()
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            fail(f"sources[{index}] must be an object")
        required = {"source_id", "platform", "title", "publisher", "url", "retrieved", "observation", "evidence_consequence"}
        if set(source) != required:
            fail(f"sources[{index}] fields do not match the scorecard schema")
        source_id = require_string(source["source_id"], f"sources[{index}].source_id")
        if source_id in source_ids:
            fail(f"duplicate source_id: {source_id}")
        source_ids.add(source_id)
        url = require_string(source["url"], f"sources[{index}].url")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"sources[{index}].url must be an HTTPS URL")
        for key in ("title", "publisher", "retrieved", "observation", "evidence_consequence"):
            require_string(source[key], f"sources[{index}].{key}")
    if source_ids != REQUIRED_SOURCES:
        fail("source IDs do not match the required cross-platform and desktop-platform source set")

    candidates = scorecard.get("candidates")
    if not isinstance(candidates, list):
        fail("candidates must be an array")
    candidate_ids = set()
    candidate_platforms = set()
    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            fail(f"candidates[{index}] must be an object")
        required = {"candidate_id", "platform", "architecture", "selection_status", "source_ids", "required_evidence", "open_questions"}
        if set(candidate) != required:
            fail(f"candidates[{index}] fields do not match the scorecard schema")
        candidate_id = require_string(candidate["candidate_id"], f"candidates[{index}].candidate_id")
        candidate_ids.add(candidate_id)
        candidate_platforms.add(require_string(candidate["platform"], f"candidates[{index}].platform"))
        if candidate["selection_status"] != "not_selected":
            fail(f"candidates[{index}] must remain not_selected")
        if not set(candidate["source_ids"]) <= source_ids:
            fail(f"candidates[{index}] references an unknown source")
        if not candidate["required_evidence"] or not candidate["open_questions"]:
            fail(f"candidates[{index}] must preserve evidence and open-question rows")
    if candidate_ids != REQUIRED_CANDIDATES or candidate_platforms != REQUIRED_PLATFORMS:
        fail("candidates must cover the three not-selected reference candidates")

    documents = scorecard.get("source_documents")
    if not isinstance(documents, list) or not documents:
        fail("source_documents must be a non-empty array")
    if len(documents) != len(set(documents)):
        fail("source_documents must not contain duplicate paths")
    for document in documents:
        path = ROOT / require_string(document, "source_documents entry")
        if not path.is_file():
            fail(f"source document is missing: {document}")

    unsupported = scorecard.get("unsupported")
    if not isinstance(unsupported, list) or not REQUIRED_UNSUPPORTED <= set(unsupported):
        fail("unsupported must preserve the reference-platform no-claim boundary")

    print(
        "reference-platform scorecard validation passed: "
        f"{len(candidates)} candidates, {len(sources)} sources, {len(dimensions)} evidence dimensions, PB-006 no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
