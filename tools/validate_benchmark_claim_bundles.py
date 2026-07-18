#!/usr/bin/env python3
"""Validate no-claim benchmark public-claim bundle templates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
DEFAULT_BUNDLE_DIR = MACHINE / "benchmark-claim-bundles"

REFERENCE_FILES = {
    "benchmark_manifest_id": (MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.sample.json", "benchmark_id"),
    "hardware_id": (MACHINE / "benchmark-hardware" / "current-windows-high-end.candidate.json", "hardware_id"),
    "os_control_id": (MACHINE / "benchmark-os-controls" / "current-windows-high-end.candidate.json", "os_control_id"),
    "corpus_id": (MACHINE / "benchmark-corpora" / "no-claim-smoke.corpus.json", "corpus_id"),
    "network_profile_id": (MACHINE / "benchmark-network-profiles" / "no-claim-local-static.profile.json", "profile_id"),
    "resource_attribution_id": (MACHINE / "benchmark-resource-attribution" / "semantic-owners.v1.json", "resource_attribution_id"),
    "tab_scenario_set_id": (MACHINE / "benchmark-tab-scenarios" / "no-claim-30-tab-smoke.scenarios.json", "scenario_set_id"),
    "artifact_package_id": (MACHINE / "benchmark-artifact-packages" / "no-claim-trace-package.plan.json", "package_id"),
    "launch_runner_id": (MACHINE / "benchmark-launch-runners" / "no-claim-browser-launch.plan.json", "launch_runner_id"),
    "browser_pin_capture_plan_id": (MACHINE / "benchmark-browser-pin-captures" / "current-windows-high-end.no-claim.plan.json", "capture_plan_id"),
    "browser_pin_diagnostic_id": (MACHINE / "benchmark-browser-pin-diagnostics" / "current-windows-high-end.chrome-edge.no-claim.2026-07.json", "diagnostic_id"),
    "competitor_version_manifest_id": (MACHINE / "benchmark-competitor-versions" / "current-desktop-release-candidates.2026-07.json", "competitor_version_manifest_id"),
    "competitor_local_install_manifest_id": (MACHINE / "benchmark-competitor-local-installs" / "current-windows-high-end.candidate.json", "local_install_manifest_id"),
}

CLAIM_BUNDLE_ID = re.compile(r"^TURING\.BENCHMARK\.CLAIM_BUNDLE\.[A-Z0-9._-]+$")

REQUIRED_CLAIM_PHRASES = [
    "no browser benchmark run",
    "no benchmark result",
    "no competitor result",
    "no trace captured",
    "no raw sample",
    "no memory result",
    "no energy result",
    "no Chrome-class claim",
    "no faster claim",
    "no lower-memory claim",
    "no lower-energy claim",
    "no public performance claim",
    "no compatibility claim",
    "no security claim",
    "no accessibility claim",
    "no production claim",
    "no daily-driver claim",
]

REQUIRED_EVIDENCE_INPUTS = {
    "approved hardware tiers",
    "approved clean OS and update controls",
    "reviewed representative corpus",
    "implemented browser launch runner",
    "owner-reviewed browser pins",
    "runner-generated trace and artifact package",
    "runner-generated 30-tab artifacts",
    "raw samples and statistics",
    "equal-workload and equal-security review",
    "publication review",
}

TERM_REQUIREMENTS = {
    "statistical_controls": [
        "raw sample count",
        "warmup policy",
        "repetitions",
        "confidence intervals",
        "outlier policy",
        "denominator",
        "effect size",
        "hardware",
    ],
    "equivalence_controls": [
        "workload versions",
        "browser channel",
        "sandbox",
        "unsupported",
        "CrUX",
        "process topology",
        "Turing",
        "competitor versions",
    ],
    "denominator_controls": [
        "failed",
        "unsupported",
        "browser launch failures",
        "trace",
        "tab discard",
        "security mitigation",
        "accessibility",
        "denominator size",
    ],
    "overhead_controls": [
        "accessibility tree",
        "crash recovery",
        "DevTools",
        "extension",
        "profile",
        "updater",
    ],
    "expiry_policy": [
        "30 days",
        "14 days",
        "competitor stable channel",
        "benchmark suite versions",
        "hardware",
        "omitted failure",
        "remove expired claims",
    ],
    "publication_controls": [
        "owner-approved claim text",
        "supported hardware",
        "raw artifact bundle hash",
        "unsupported behavior",
        "rerun triggers",
        "block fastest",
    ],
    "rejection_rules": [
        "raw samples",
        "trace and artifact package hashes",
        "browser pins",
        "denominator records",
        "security",
        "different benchmark suite versions",
        "sample count",
        "public text",
        "owner",
        "expired",
    ],
    "unsupported_behavior": [
        "no browser benchmark run exists",
        "no benchmark result exists",
        "no competitor result exists",
        "no raw sample exists",
        "no trace package exists",
        "no memory result exists",
        "no energy result exists",
        "no Chrome-class claim is supported",
        "no faster claim is supported",
        "no lower-memory claim is supported",
        "no lower-energy claim is supported",
        "no compatibility claim is supported",
        "no security claim is supported",
        "no accessibility claim is supported",
        "no production, beta, stable, release, or daily-driver claim is supported",
    ],
    "missing_proof": [
        "Tier L",
        "clean OS image",
        "representative offline corpus",
        "browser launch runner",
        "browser pins",
        "raw samples",
        "30-tab",
        "statistics",
        "equal-workload",
        "public claim text",
    ],
}

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_benchmark_claim_bundles.py",
    "python3 -B tools/validate_blueprint.py",
]


class ValidationError(ValueError):
    pass


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(path: Path | str, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(relative(path), f"invalid JSON: {error}")


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(path: Path, data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        fail(relative(path), f"{key} must be a non-empty array")
    return value


def string_block(values: list[Any]) -> str:
    return " ".join(value for value in values if isinstance(value, str))


def require_terms(path: Path, key: str, values: list[Any], terms: list[str]) -> None:
    block = string_block(values)
    missing = [term for term in terms if term not in block]
    if missing:
        fail(relative(path), f"{key} is missing required terms: {', '.join(missing)}")


def reference_ids() -> dict[str, str]:
    ids: dict[str, str] = {}
    for key, (path, source_key) in REFERENCE_FILES.items():
        payload = load_json(path)
        if not isinstance(payload, dict):
            fail(relative(path), "reference payload must be an object")
        value = payload.get(source_key)
        if not isinstance(value, str) or not value:
            fail(relative(path), f"missing reference id {source_key}")
        ids[key] = value
    return ids


def validate_bundle(path: Path, refs: dict[str, str]) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(relative(path), "claim bundle must be an object")
    if data.get("schema_version") != 1:
        fail(relative(path), "schema_version must be 1")
    claim_bundle_id = text(data.get("claim_bundle_id"))
    if not CLAIM_BUNDLE_ID.fullmatch(claim_bundle_id):
        fail(relative(path), f"invalid claim_bundle_id: {claim_bundle_id!r}")
    if data.get("status") != "template_only_no_public_claim":
        fail(relative(path), "status must remain template_only_no_public_claim")
    if data.get("claim_text") != "No public claim is approved by this template.":
        fail(relative(path), "claim_text must not approve public claim language")
    if data.get("claim_owner_scope") == data.get("independent_reviewer_scope"):
        fail(relative(path), "claim_owner_scope and independent_reviewer_scope must differ")

    claim_status = text(data.get("claim_status"))
    missing_claims = [phrase for phrase in REQUIRED_CLAIM_PHRASES if phrase not in claim_status]
    if missing_claims:
        fail(relative(path), "claim_status is missing: " + ", ".join(missing_claims))

    registry = data.get("registry_references")
    if not isinstance(registry, dict):
        fail(relative(path), "registry_references must be an object")
    for key, expected in refs.items():
        if registry.get(key) != expected:
            fail(relative(path), f"registry_references.{key} must be {expected}")

    evidence_inputs = require_list(path, data, "evidence_inputs")
    seen_inputs: set[str] = set()
    for item in evidence_inputs:
        if not isinstance(item, dict):
            fail(relative(path), "evidence_inputs entries must be objects")
        input_name = text(item.get("input"))
        seen_inputs.add(input_name)
        if item.get("required_for_public_claim") is not True:
            fail(relative(path), f"{input_name}: required_for_public_claim must be true")
        current_status = text(item.get("current_status"))
        missing_proof = text(item.get("missing_proof"))
        if not current_status or "approved" in current_status and "not_approved" not in current_status:
            fail(relative(path), f"{input_name}: current_status must not imply approval")
        if "No " not in missing_proof and "no " not in missing_proof:
            fail(relative(path), f"{input_name}: missing_proof must describe absent evidence")
    missing_inputs = sorted(REQUIRED_EVIDENCE_INPUTS - seen_inputs)
    if missing_inputs:
        fail(relative(path), "evidence_inputs is missing: " + ", ".join(missing_inputs))

    for key, terms in TERM_REQUIREMENTS.items():
        require_terms(path, key, require_list(path, data, key), terms)

    commands = require_list(path, data, "validation_commands")
    missing_commands = [command for command in REQUIRED_VALIDATION_COMMANDS if command not in commands]
    if missing_commands:
        fail(relative(path), "validation_commands is missing: " + ", ".join(missing_commands))


def validate_docs() -> None:
    requirements = {
        ROOT / "README.md": ["owner-reviewed claim bundles", "claim-bundle template"],
        DOCS / "start-here.md": ["claim-bundle template", "owner-reviewed claim bundle"],
        DOCS / "README.md": ["claim-bundle template", "owner-reviewed claim bundles"],
        DOCS / "project-buildout" / "README.md": ["claim-bundle template", "owner-reviewed claim bundles"],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": ["claim-bundle template", "validate_benchmark_claim_bundles.py"],
        DOCS / "repository-map.md": ["Benchmark claim bundles", "validate_benchmark_claim_bundles.py"],
        DOCS / "research" / "chrome-class-performance-runbook-2026-07.md": ["claim-bundle template", "validate_benchmark_claim_bundles.py"],
    }
    for path, phrases in requirements.items():
        content = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in content]
        if missing:
            fail(relative(path), "missing benchmark claim-bundle coverage: " + ", ".join(missing))


def bundle_paths(args: argparse.Namespace) -> list[Path]:
    if args.paths:
        return [Path(path) for path in args.paths]
    return sorted(DEFAULT_BUNDLE_DIR.glob("*.json"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="benchmark claim bundle JSON files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = bundle_paths(args)
    if not paths:
        fail(relative(DEFAULT_BUNDLE_DIR), "no benchmark claim bundle files found")
    refs = reference_ids()
    for path in paths:
        validate_bundle(path, refs)
    validate_docs()
    print(f"benchmark claim-bundle validation passed: {len(paths)} bundle(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as error:
        print(f"benchmark claim-bundle validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
