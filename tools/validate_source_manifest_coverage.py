#!/usr/bin/env python3
"""Require every checked source manifest to remain bound to its owning controls."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "docs/blueprint-v1/machine/research-readiness-crosswalk.json"
LEDGER = ROOT / "docs/project-buildout/machine/build-information-readiness-ledger.json"
AUDIT = ROOT / "docs/project-buildout/machine/documentation-readiness-completion-audit.json"
CLOSURE = ROOT / "docs/project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json"

CONTROL = {
    "docs/accessibility/machine/accessibility-source-manifest.json": "research-lane-native-shell-page-surface",
    "docs/blueprint-v1/machine/benchmark-source-manifest.json": "research-lane-benchmark-extreme-performance-lab",
    "docs/blueprint-v1/machine/ipc-wire-source-manifest.json": "research-lane-kernel-process-authority-ipc",
    "docs/blueprint-v1/machine/technology-dependency-source-manifest.json": "research-lane-source-strategy-adr-0009",
    "docs/research/machine/browser-engine-landscape-source-manifest.json": "research-lane-source-strategy-adr-0009",
    "docs/project-buildout/machine/fresh-host-toolchain-source-manifest.json": "research-lane-fresh-host-build-confidence",
    "docs/project-buildout/machine/ownership-control-source-manifest.json": "research-lane-ownership-review-capacity",
    "docs/release-operations/machine/package-update-source-manifest.json": "research-lane-research-package-updater-lab",
    "docs/security-engine/machine/incident-response-source-manifest.json": "research-lane-security-incident-patch-rehearsal",
    "docs/security-engine/machine/sandbox-platform-source-manifest.json": "research-lane-sandbox-probes",
    "docs/storage/machine/profile-session-source-manifest.json": "research-lane-profile-space-session-snapshot-migration",
    "docs/ui-runtime/machine/design-source-manifest.json": "research-lane-native-shell-page-surface",
    "docs/web-platform/machine/web-platform-source-manifest.json": "research-lane-source-strategy-adr-0009",
}

VALIDATOR = {
    "docs/accessibility/machine/accessibility-source-manifest.json": "tools/validate_accessibility_sources.py",
    "docs/blueprint-v1/machine/benchmark-source-manifest.json": "tools/validate_benchmark_sources.py",
    "docs/blueprint-v1/machine/ipc-wire-source-manifest.json": "tools/validate_ipc_wire_sources.py",
    "docs/blueprint-v1/machine/technology-dependency-source-manifest.json": "tools/validate_technology_dependency_sources.py",
    "docs/research/machine/browser-engine-landscape-source-manifest.json": "tools/validate_browser_engine_landscape_sources.py",
    "docs/project-buildout/machine/fresh-host-toolchain-source-manifest.json": "tools/validate_fresh_host_toolchain_sources.py",
    "docs/project-buildout/machine/ownership-control-source-manifest.json": "tools/validate_ownership_control_sources.py",
    "docs/release-operations/machine/package-update-source-manifest.json": "tools/validate_package_update_sources.py",
    "docs/security-engine/machine/incident-response-source-manifest.json": "tools/validate_incident_response_sources.py",
    "docs/security-engine/machine/sandbox-platform-source-manifest.json": "tools/validate_sandbox_platform_sources.py",
    "docs/storage/machine/profile-session-source-manifest.json": "tools/validate_profile_session_sources.py",
    "docs/ui-runtime/machine/design-source-manifest.json": "tools/validate_design_source.py",
    "docs/web-platform/machine/web-platform-source-manifest.json": "tools/validate_web_platform_sources.py",
}


def fail(message: str) -> None:
    print(f"source-manifest coverage validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def validate_source_document_links(manifest_path: str, manifest: dict) -> int:
    documents = manifest.get("source_documents")
    if documents is None:
        return 0
    if not isinstance(documents, list) or not documents:
        fail(f"{manifest_path} source_documents must be a non-empty array")
    checked = 0
    manifest_name = Path(manifest_path).name
    for document in documents:
        if not isinstance(document, str) or not document:
            fail(f"{manifest_path} source_documents entries must be non-empty strings")
        document_path = (ROOT / document).resolve()
        try:
            document_path.relative_to(ROOT)
        except ValueError:
            fail(f"{manifest_path} source document escapes repository: {document}")
        if not document_path.is_file():
            fail(f"{manifest_path} source document does not exist: {document}")
        content = document_path.read_text(encoding="utf-8", errors="ignore")
        if manifest_name not in content and manifest_path not in content:
            fail(f"{manifest_path} is not referenced by source document: {document}")
        checked += 1
    return checked


def main() -> int:
    if set(CONTROL) != set(VALIDATOR):
        fail("manifest and validator maps must cover the same paths")
    crosswalk = load(CROSSWALK)
    ledger = load(LEDGER)
    audit = load(AUDIT)
    closure = load(CLOSURE)
    crosswalk_entries = {
        entry
        for lane in crosswalk.get("lanes", [])
        for entry in lane.get("evidence_start", [])
    }
    lane_entries = {
        lane.get("id"): set(lane.get("evidence_start", []))
        for lane in crosswalk.get("lanes", [])
    }
    ledger_entries = set(ledger.get("source_records", []))
    audit_entries = set(audit.get("source_records", []))
    closure_entries = set(closure.get("source_records", []))
    missing: list[str] = []
    source_document_count = 0
    for manifest, lane_id in CONTROL.items():
        manifest_data = load(ROOT / manifest)
        source_document_count += validate_source_document_links(manifest, manifest_data)
        schema = manifest.removesuffix(".json") + ".schema.json"
        required = [manifest, schema]
        required.append(VALIDATOR[manifest])
        for path in required:
            if not (ROOT / path).is_file():
                missing.append(f"filesystem:{path}")
            if path not in crosswalk_entries:
                missing.append(f"crosswalk:{path}")
            if path not in ledger_entries:
                missing.append(f"ledger:{path}")
            if path not in audit_entries:
                missing.append(f"audit:{path}")
            if path not in closure_entries:
                missing.append(f"closure:{path}")
        if manifest not in lane_entries.get(lane_id, set()):
            missing.append(f"lane:{lane_id}:{manifest}")
    if missing:
        fail("missing bindings: " + ", ".join(sorted(missing)))
    print(
        f"source-manifest coverage validation passed: {len(CONTROL)} manifests, "
        f"{source_document_count} repository source-document links, 4 control surfaces"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
