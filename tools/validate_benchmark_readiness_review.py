#!/usr/bin/env python3
"""Validate checked no-claim benchmark readiness-review templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
DEFAULT_REVIEW = (
    MACHINE
    / "benchmark-readiness-reviews"
    / "no-claim-benchmark-readiness-template.json"
)

REVIEW_ID = re.compile(r"^TURING\.BENCHMARK\.READINESS_REVIEW\.[A-Z0-9._-]+$")

REQUIRED_REVIEW_FILES = [
    "docs/blueprint-v1/machine/benchmark-readiness-review.schema.json",
    "docs/blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json",
    "tools/validate_benchmark_readiness_review.py",
]

REQUIRED_SOURCE_RECORDS = {
    "docs/research/performance-benchmark-readiness-packet-2026-07.md",
    "docs/research/benchmark-corpus-expansion-2026-07.md",
    "docs/research/chrome-class-performance-runbook-2026-07.md",
    "docs/research/benchmark-hardware-os-manifest-2026-07.md",
    "docs/research/benchmark-os-update-control-manifest-2026-07.md",
    "docs/research/semantic-resource-attribution-taxonomy-2026-07.md",
    "docs/research/benchmark-competitor-version-manifest-2026-07.md",
    "docs/research/benchmark-competitor-local-install-inventory-2026-07.md",
    "docs/research/benchmark-browser-pin-capture-contract-2026-07.md",
    "docs/research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md",
    "docs/research/benchmark-server-lifecycle-self-test-2026-07.md",
    "docs/research/benchmark-30-tab-scenario-contract-2026-07.md",
    "docs/research/benchmark-trace-artifact-package-contract-2026-07.md",
    "docs/research/benchmark-browser-launch-runner-contract-2026-07.md",
    "docs/research/benchmark-statistics-analysis-contract-2026-07.md",
    "docs/benchmark-lab/README.md",
    "docs/performance/README.md",
    "docs/blueprint-v1/09-performance-memory.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/blueprint-v1/22-research-program.md",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/machine/benchmark-manifest.schema.json",
    "docs/blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json",
    "docs/blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json",
    "docs/blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json",
    "docs/blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json",
    "docs/blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json",
    "docs/blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json",
    "docs/blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json",
    "docs/blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json",
    "docs/blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json",
    "docs/blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json",
    "docs/blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json",
    "docs/blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json",
    "docs/blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json",
    "docs/blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json",
    "docs/blueprint-v1/machine/benchmark-readiness-review.schema.json",
    "docs/blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json",
    "docs/blueprint-v1/machine/benchmark-statistics-analysis.schema.json",
    "docs/blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json",
    "tools/validate_benchmark_claim_bundles.py",
    "tools/validate_benchmark_readiness_review.py",
    "tools/validate_benchmark_statistics_analysis.py",
    "tools/validate_blueprint.py",
    "tools/check.ps1",
}

REQUIRED_CLAIM_PHRASES = [
    "no owner review",
    "no performance review",
    "no benchmark operations review",
    "no quality review",
    "no security review",
    "no accessibility review",
    "no release-operations review",
    "no approved hardware tiers",
    "no clean OS-control review",
    "no representative corpus review",
    "no browser-run server evidence review",
    "no implemented browser launch runner review",
    "no benchmark-ready browser pin review",
    "no trace-artifact review",
    "no raw result review",
    "no 30-tab artifact review",
    "no statistics review",
    "no denominator review",
    "no equal-workload review",
    "no claim-bundle review",
    "no benchmark-ready status",
    "no public performance claim",
    "no faster claim",
    "no lower-memory claim",
    "no lower-energy claim",
    "no Chrome-class claim",
    "no competitor-result claim",
    "no daily-driver claim",
    "no production claim",
    "no implementation claim",
]

READINESS_STATUS_FLAGS = [
    "owner_reviewed",
    "performance_reviewed",
    "benchmark_operations_reviewed",
    "quality_reviewed",
    "security_reviewed",
    "accessibility_reviewed",
    "release_operations_reviewed",
    "hardware_tiers_reviewed",
    "os_controls_reviewed",
    "corpus_reviewed",
    "network_profiles_reviewed",
    "server_evidence_reviewed",
    "launch_runner_reviewed",
    "browser_pins_reviewed",
    "trace_artifacts_reviewed",
    "raw_results_reviewed",
    "thirty_tab_artifacts_reviewed",
    "statistics_reviewed",
    "denominator_reviewed",
    "resource_attribution_reviewed",
    "equal_workload_reviewed",
    "claim_bundle_reviewed",
    "benchmark_ready_supported",
    "public_performance_claim_supported",
    "faster_claim_supported",
    "lower_memory_claim_supported",
    "lower_energy_claim_supported",
    "chrome_class_claim_supported",
    "competitor_result_supported",
    "daily_driver_claim_supported",
    "production_claim_supported",
    "implementation_claim_supported",
]

NULL_SCOPE_FIELDS = [
    "benchmark_manifest",
    "hardware_tiers",
    "os_controls",
    "corpus",
    "network_profile",
    "launch_runner",
    "artifact_package",
    "browser_pins",
    "claim_bundle",
    "owner_reviewer",
    "performance_reviewer",
    "benchmark_operations_reviewer",
    "quality_reviewer",
    "security_reviewer",
    "accessibility_reviewer",
    "release_operations_reviewer",
]

REQUIRED_AXIS_TERMS = [
    "Tier L",
    "Tier M",
    "Tier H",
    "clean OS image",
    "update freeze",
    "driver freeze",
    "firmware freeze",
    "display",
    "thermal",
    "network isolation",
    "artifact storage",
    "representative offline corpus",
    "page",
    "app",
    "accessibility",
    "media",
    "hostile",
    "service-worker",
    "international",
    "browser-run server evidence",
    "DNS",
    "HTTP/2",
    "HTTP/3",
    "TLS",
    "proxy",
    "authentication",
    "cache-revalidation",
    "network shaping",
    "implemented browser launch runner",
    "timeout",
    "cancellation",
    "cache reset",
    "temporary-profile",
    "prohibited-path",
    "trace package",
    "raw samples",
    "artifact hashes",
    "cleanup",
    "30-tab",
    "mixed-state",
    "all-live",
    "resource-attribution",
    "GPU",
    "energy",
    "Chrome",
    "Edge",
    "Firefox",
    "Safari",
    "browser pins",
    "channel proof",
    "settings",
    "command lines",
    "equal-workload",
    "equal-security",
    "sample count",
    "confidence",
    "outlier",
    "failure denominator",
    "owner review",
    "performance",
    "benchmark operations",
    "quality",
    "security",
    "release-operations",
    "claim bundle",
    "expiry",
    "public copy",
    "promotion boundary",
]

REQUIRED_REJECTION_TERMS = [
    "template",
    "placeholder",
    "hardware",
    "clean OS",
    "corpus",
    "browser-run server",
    "launch runner",
    "raw samples",
    "trace",
    "browser pins",
    "unequal workload",
    "security",
    "hidden failures",
    "real user profiles",
    "claim bundle",
    "expired",
    "validation",
]

REQUIRED_VALIDATION_COMMANDS = [
    "python3 -B tools/validate_benchmark_statistics_analysis.py",
    "python3 -B tools/validate_benchmark_claim_bundles.py",
    "python3 -B tools/validate_benchmark_readiness_review.py",
    "python3 -B tools/validate_blueprint.py",
    ".\\tools\\check.ps1",
]


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        fail(f"{key} must be a non-empty array")
    return value


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(f"{key} must be an object")
    return value


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("benchmark readiness", "benchmark-readiness"),
        ("benchmark ready", "benchmark-ready"),
        ("public performance", "public-performance"),
        ("lower memory", "lower-memory"),
        ("lower energy", "lower-energy"),
        ("chrome class", "chrome-class"),
        ("competitor result", "competitor-result"),
        ("daily driver", "daily-driver"),
        ("browser run", "browser-run"),
        ("browser pin", "browser-pin"),
        ("trace artifact", "trace-artifact"),
        ("raw result", "raw-result"),
        ("raw sample", "raw-sample"),
        ("claim bundle", "claim-bundle"),
        ("equal workload", "equal-workload"),
        ("equal security", "equal-security"),
        ("failure denominator", "failure-denominator"),
        ("temporary profile", "temporary-profile"),
        ("prohibited path", "prohibited-path"),
        ("cache reset", "cache-reset"),
        ("30 tab", "30-tab"),
        ("pb 013", "pb-013"),
        ("pb013", "pb-013"),
        ("clean os", "clean-os"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def validate_review(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: review must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    review_id = text(data.get("review_id"))
    if not REVIEW_ID.fullmatch(review_id):
        fail(f"{path}: invalid review_id {review_id!r}")
    if data.get("status") != "no_claim_benchmark_readiness_template":
        fail(f"{path}: status must be no_claim_benchmark_readiness_template")

    boundary_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[text(value) for value in require_list(data, "unsupported_boundaries")],
            ]
        )
    )
    for phrase in REQUIRED_CLAIM_PHRASES:
        if normalize(phrase) not in boundary_text:
            fail(f"{path}: missing claim boundary phrase: {phrase}")

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in source_records:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    scope = require_object(data, "review_scope")
    if scope.get("review_status") != "template_only_no_review":
        fail(f"{path}: review_scope.review_status must be template_only_no_review")
    for field in NULL_SCOPE_FIELDS:
        if scope.get(field) is not None:
            fail(f"{path}: review_scope.{field} must be null in the no-claim template")
    policy = normalize(text(scope.get("prohibited_placeholder_policy")))
    for phrase in ["placeholder", "self-approval", "pb-013", "null", "benchmark-readiness"]:
        if phrase not in policy:
            fail(f"{path}: prohibited_placeholder_policy must mention {phrase}")

    readiness = require_object(data, "readiness_status")
    missing_flags = sorted(set(READINESS_STATUS_FLAGS) - set(readiness))
    if missing_flags:
        fail(f"{path}: readiness_status missing flags: {', '.join(missing_flags)}")
    for flag in READINESS_STATUS_FLAGS:
        if readiness.get(flag) is not False:
            fail(f"{path}: readiness_status.{flag} must be false in the no-claim template")

    axis_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for key in [
                "hardware_os_axes",
                "corpus_network_axes",
                "runner_artifact_axes",
                "browser_pin_comparison_axes",
                "statistics_denominator_axes",
                "claim_review_axes",
            ]
            for item in require_list(data, key)
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_AXIS_TERMS:
        if normalize(phrase) not in axis_text:
            fail(f"{path}: missing benchmark readiness axis term: {phrase}")
    if "beyond the checked no-claim benchmark-readiness-review template" not in axis_text:
        fail(f"{path}: axes must require evidence beyond the checked no-claim template")

    rejection_text = normalize(
        " ".join(
            " ".join(text(value) for value in item.values())
            for item in require_list(data, "rejection_rules")
            if isinstance(item, dict)
        )
    )
    for phrase in REQUIRED_REJECTION_TERMS:
        if normalize(phrase) not in rejection_text:
            fail(f"{path}: rejection rules must mention {phrase}")

    commands = [text(value) for value in require_list(data, "validation_commands")]
    for command in REQUIRED_VALIDATION_COMMANDS:
        if command not in commands:
            fail(f"{path}: validation_commands missing {command}")


def validate_readiness_registry() -> None:
    payload = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        fail("pre-build-readiness.json must contain items")
    item = next(
        (
            entry
            for entry in payload["items"]
            if isinstance(entry, dict) and entry.get("id") == "PB-013"
        ),
        None,
    )
    if not isinstance(item, dict):
        fail("pre-build-readiness.json is missing PB-013")
    if item.get("status") != "documented_no_runner":
        fail("PB-013 must remain documented_no_runner while the benchmark review is a no-claim template")
    evidence = item.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence]
    if missing:
        fail("PB-013 evidence is missing benchmark readiness review files: " + ", ".join(missing))
    required_text = normalize(
        " ".join(value for value in item.get("evidence_required", []) if isinstance(value, str))
    )
    for phrase in [
        "checked no-claim benchmark readiness-review template",
        "owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template",
        "fixed hardware",
        "clean OS image",
        "reviewed representative offline corpus",
        "implemented browser benchmark launch runner",
        "runner-generated raw result",
        "trace and artifact package",
        "30-tab",
        "benchmark-ready browser pins",
        "owner-reviewed claim bundle",
        "Chrome-class",
        "public performance",
    ]:
        if normalize(phrase) not in required_text:
            fail(f"PB-013 evidence_required must mention {phrase}")


def validate_task_queue() -> None:
    payload = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            entry
            for entry in payload["tasks"]
            if isinstance(entry, dict) and entry.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("TASK-000005 is missing from build-readiness-task-queue.json")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in allowed_paths]
    if missing:
        fail("TASK-000005 allowed_paths missing benchmark review files: " + ", ".join(missing))
    task_text = normalize(
        " ".join(
            value
            for field in ["preconditions", "acceptance_criteria", "negative_tests"]
            for value in task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "checked no-claim benchmark readiness-review template",
        "owner-reviewed benchmark readiness review",
        "cannot be cited",
        "benchmark-ready",
        "public performance",
        "Chrome-class",
        "faster",
        "lower-memory",
        "lower-energy",
    ]:
        if normalize(phrase) not in task_text:
            fail(f"TASK-000005 must mention benchmark review boundary for {phrase}")


def validate_crosswalk() -> None:
    payload = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(payload, dict) or not isinstance(payload.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain lanes")
    lane = next(
        (
            item
            for item in payload["lanes"]
            if isinstance(item, dict)
            and item.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    evidence_start = lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("benchmark lane evidence_start must be an array")
    missing = [path for path in REQUIRED_REVIEW_FILES if path not in evidence_start]
    if missing:
        fail("benchmark lane evidence_start missing benchmark review files: " + ", ".join(missing))
    lane_text = normalize(
        " ".join(
            value
            for field in ["next_proof", "claim_boundary"]
            for value in lane.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [
        "owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template",
        "no benchmark-ready claim from the checked no-claim benchmark readiness-review template",
        "no public performance claim",
        "no Chrome-class claim",
        "no competitor-result claim",
    ]:
        if normalize(phrase) not in lane_text:
            fail(f"benchmark lane must mention {phrase}")


def validate_docs() -> None:
    docs_to_check = {
        ROOT / "README.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "start-here.md": ["benchmark readiness-review template", "no owner-reviewed benchmark readiness"],
        DOCS / "README.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "repository-map.md": ["benchmark readiness-review template", "benchmark-readiness-review.schema.json"],
        DOCS / "research" / "README.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template"],
        DOCS / "research" / "performance-benchmark-readiness-packet-2026-07.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template"],
        DOCS / "benchmark-lab" / "README.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "performance" / "README.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "blueprint-v1" / "09-performance-memory.md": ["benchmark readiness-review template", "no owner-reviewed benchmark readiness"],
        DOCS / "blueprint-v1" / "22-research-program.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "project-buildout" / "17-build-readiness-task-queue.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": ["benchmark readiness-review template", "owner-reviewed benchmark readiness"],
    }
    for doc_path, phrases in docs_to_check.items():
        content = doc_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in content]
        if missing:
            fail(f"{doc_path}: missing benchmark readiness-review documentation: {', '.join(missing)}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REVIEW
    validate_review(path)
    validate_readiness_registry()
    validate_task_queue()
    validate_crosswalk()
    validate_docs()
    print(f"benchmark readiness review validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
