#!/usr/bin/env python3
"""Validate no-claim sandbox probe inventories."""

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
SECURITY_MACHINE = DOCS / "security-engine" / "machine"
DEFAULT_INVENTORY = SECURITY_MACHINE / "sandbox-probe-inventory.json"
DEFAULT_PROBE_PACKAGE = (
    SECURITY_MACHINE
    / "sandbox-probe-packages"
    / "no-claim-expected-deny-template.json"
)

INVENTORY_ID = re.compile(r"^SANDBOX\.PROBE\.[A-Z0-9._-]+$")
PROBE_PACKAGE_ID = re.compile(r"^SANDBOX\.PROBE_PACKAGE\.[A-Z0-9._-]+$")
BLOCKER_ID = re.compile(r"^SBX-BLOCKER-[A-Z0-9_]+$")

REQUIRED_SOURCE_RECORDS = {
    "docs/blueprint-v1/04-system-architecture.md",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/blueprint-v1/12-testing-compatibility.md",
    "docs/security-engine/01-threat-model-and-process-isolation.md",
    "docs/security-engine/02-sandbox-brokers-and-platform-containment.md",
    "docs/security-engine/06-security-verification-and-release-gates.md",
    "docs/platform/README.md",
    "docs/blueprint-v1/machine/process-capabilities.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/security-engine/machine/sandbox-readiness-review.schema.json",
    "docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json",
    "tools/validate_sandbox_readiness_review.py",
}

REQUIRED_PROBE_PACKAGE_SOURCE_RECORDS = {
    "docs/security-engine/machine/sandbox-probe-inventory.json",
    "docs/security-engine/machine/sandbox-probe-inventory.schema.json",
    "docs/security-engine/machine/sandbox-probe-package.schema.json",
    "docs/security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json",
    "docs/security-engine/machine/sandbox-readiness-review.schema.json",
    "docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json",
    "docs/blueprint-v1/machine/process-capabilities.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "docs/security-engine/02-sandbox-brokers-and-platform-containment.md",
    "docs/security-engine/06-security-verification-and-release-gates.md",
    "docs/research/sandbox-probe-inventory-2026-07.md",
    "tools/validate_sandbox_readiness_review.py",
}

REQUIRED_SURFACES = {
    "file",
    "socket",
    "process",
    "registry",
    "device",
    "shared-memory",
    "credential",
    "debug",
    "profile",
    "ipc",
}

REQUIRED_TARGETS = {
    "renderer": "renderer",
    "network": "network",
    "storage": "storage",
    "gpu": "gpu",
    "decoder": "media_utility",
    "extension": "extension_host",
    "devtools": "devtools",
    "agent": "agent_host",
    "updater": "updater",
}

REQUIRED_PLATFORMS = {"macos", "windows", "linux"}

REQUIRED_BLOCKERS = {
    "packaged role runner",
    "effective policy capture",
    "probe result schema",
    "safe host execution",
    "broker fixtures",
    "compromised client harnesses",
    "platform matrix",
    "owner review",
}

REQUIRED_CLAIM_PHRASES = [
    "no sandbox-readiness claim",
    "no renderer-security claim",
    "no site-isolation claim",
    "no hostile-browsing safety claim",
    "no platform containment claim",
    "no packaged-build probe claim",
    "no effective-policy claim",
    "no SEC-GATE-1 claim",
    "no SEC-GATE-6 claim",
    "no production-safety claim",
]

REQUIRED_PACKAGE_STATUS_FALSE = {
    "packaged_probe_harness",
    "effective_policy_captured",
    "platform_matrix_executed",
    "owner_reviewed",
}

REQUIRED_PLATFORM_PACKAGE_TERMS = {
    "windows": {
        "appcontainer",
        "token",
        "integrity",
        "job",
        "mitigation",
        "handle",
        "dynamic-code",
    },
    "macos": {
        "seatbelt",
        "app sandbox",
        "entitlement",
        "hardened runtime",
        "jit",
        "code signing",
    },
    "linux": {
        "namespace",
        "seccomp",
        "landlock",
        "mount",
        "capabilities",
        "broker",
    },
}

REQUIRED_PACKAGE_LIFECYCLE_STAGES = {
    "build_package",
    "launch_isolated_role",
    "attempt_expected_deny",
    "capture_effective_policy",
    "record_broker_exception",
    "cleanup_and_classify",
}

REQUIRED_RESULT_FIELDS = {
    "role",
    "platform",
    "artifact build id",
    "command line",
    "process identity",
    "surface",
    "expected denied operation",
    "actual result",
    "exit code",
    "policy artifact hash",
    "stdout",
    "stderr",
    "cleanup",
    "owner review",
    "failure denominator",
}

REQUIRED_REJECTION_TERMS = {
    "host-safe",
    "effective policy",
    "success paths only",
    "hidden failures",
    "real secrets",
    "production profile",
    "unbounded",
    "owner review",
    "sandbox-readiness",
    "sec-gate",
}

REQUIRED_VALIDATION_COMMANDS = {
    "python3 -B tools/validate_sandbox_probe_inventory.py",
    "python3 -B tools/validate_sandbox_readiness_review.py",
    "python3 -B tools/validate_blueprint.py",
    ".\\tools\\check.ps1",
}

SAFE_FAILURE_TERMS = {
    "abort",
    "block",
    "deny",
    "fail",
    "hold",
    "reject",
    "return",
}


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
    if not isinstance(value, list):
        fail(f"{key} must be an array")
    return value


def require_dict(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(f"{key} must be an object")
    return value


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def normalize_surface(value: str) -> str:
    lowered = value.lower().replace("_", "-").strip()
    if lowered == "shared memory":
        return "shared-memory"
    return lowered


def require_safe_failure(path: Path, item_id: str, value: str) -> None:
    lowered = value.lower()
    if not any(term in lowered for term in SAFE_FAILURE_TERMS):
        fail(f"{path}: {item_id} safe_failure must describe denial, rejection, return, abort, or blocking behavior")


def validate_inventory(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    inventory_id = text(data.get("inventory_id"))
    if not INVENTORY_ID.match(inventory_id):
        fail(f"{path}: invalid inventory_id {inventory_id!r}")
    if data.get("status") != "no_claim_probe_inventory":
        fail(f"{path}: status must be no_claim_probe_inventory")

    boundaries = [text(value) for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")), *boundaries])
    boundary_text_lower = boundary_text.lower()
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase.lower() not in boundary_text_lower:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    sources = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - sources)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in REQUIRED_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    surfaces = require_list(data, "required_probe_surfaces")
    surface_names: list[str] = []
    for item in surfaces:
        if not isinstance(item, dict):
            fail(f"{path}: required_probe_surfaces entries must be objects")
        surface = normalize_surface(text(item.get("surface")))
        surface_names.append(surface)
        for field in ("hostile_attempt", "expected_safe_result", "missing_evidence"):
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: surface {surface} {field} must be descriptive")
        expected = text(item.get("expected_safe_result")).lower()
        if not any(term in expected for term in ("deny", "return", "reject", "abort")):
            fail(f"{path}: surface {surface} expected_safe_result must describe denial or bounded return behavior")
    check_no_duplicates(surface_names, "probe surfaces")
    if set(surface_names) != REQUIRED_SURFACES:
        fail(
            f"{path}: probe surfaces must be exactly: "
            + ", ".join(sorted(REQUIRED_SURFACES))
        )

    process_capabilities = load_json(MACHINE / "process-capabilities.json")
    roles = process_capabilities.get("roles") if isinstance(process_capabilities, dict) else None
    if not isinstance(roles, dict):
        fail("process-capabilities.json must contain a roles object")

    targets = require_list(data, "probe_targets")
    target_names: list[str] = []
    for item in targets:
        if not isinstance(item, dict):
            fail(f"{path}: probe_targets entries must be objects")
        target = text(item.get("target")).lower()
        target_names.append(target)
        expected_role = REQUIRED_TARGETS.get(target)
        if expected_role is None:
            fail(f"{path}: unexpected probe target {target!r}")
        role = text(item.get("process_capability_role"))
        if role != expected_role:
            fail(f"{path}: target {target} must map to process capability role {expected_role}")
        if role not in roles:
            fail(f"{path}: process capability role {role!r} is not in process-capabilities.json")
        for field in ("purpose", "current_evidence", "missing_evidence"):
            value = text(item.get(field))
            if len(value) < 20:
                fail(f"{path}: target {target} {field} must be descriptive")
        matrix = item.get("probe_matrix")
        if not isinstance(matrix, list):
            fail(f"{path}: target {target} probe_matrix must be an array")
        matrix_surfaces: list[str] = []
        for probe in matrix:
            if not isinstance(probe, dict):
                fail(f"{path}: target {target} probe_matrix entries must be objects")
            surface = normalize_surface(text(probe.get("surface")))
            matrix_surfaces.append(surface)
            if surface not in REQUIRED_SURFACES:
                fail(f"{path}: target {target} has unknown surface {surface}")
            expected = text(probe.get("expected_result")).lower()
            if len(expected) < 20:
                fail(f"{path}: target {target} surface {surface} expected_result must be descriptive")
            if not any(term in expected for term in ("deny", "allow only", "approved", "authorized")):
                fail(f"{path}: target {target} surface {surface} expected_result must describe denial or narrow authorization")
            if probe.get("current_status") not in {
                "missing_no_harness",
                "policy_record_only",
                "unsupported_until_platform_selected",
            }:
                fail(f"{path}: target {target} surface {surface} has invalid current_status")
        check_no_duplicates(matrix_surfaces, f"{target} probe surfaces")
        if set(matrix_surfaces) != REQUIRED_SURFACES:
            fail(f"{path}: target {target} must cover every required probe surface")
        if not any(probe.get("current_status") == "missing_no_harness" for probe in matrix if isinstance(probe, dict)):
            fail(f"{path}: target {target} must remain missing executable harness evidence")
    check_no_duplicates(target_names, "probe targets")
    if set(target_names) != set(REQUIRED_TARGETS):
        fail(
            f"{path}: probe targets must be exactly: "
            + ", ".join(sorted(REQUIRED_TARGETS))
        )

    platforms = require_list(data, "platform_evidence_requirements")
    platform_names: list[str] = []
    platform_text = ""
    for item in platforms:
        if not isinstance(item, dict):
            fail(f"{path}: platform_evidence_requirements entries must be objects")
        platform = text(item.get("platform"))
        platform_names.append(platform)
        artifacts = item.get("required_artifacts")
        if not isinstance(artifacts, list) or len(artifacts) < 3:
            fail(f"{path}: platform {platform} required_artifacts must list evidence")
        platform_text += " " + " ".join(text(value).lower() for value in artifacts)
        if len(text(item.get("missing_evidence"))) < 30:
            fail(f"{path}: platform {platform} missing_evidence must be descriptive")
    check_no_duplicates(platform_names, "platform evidence records")
    if set(platform_names) != REQUIRED_PLATFORMS:
        fail(f"{path}: platform evidence must cover macos, windows, and linux")
    for phrase in [
        "seatbelt",
        "app sandbox",
        "appcontainer",
        "job",
        "namespace",
        "seccomp",
        "landlock",
    ]:
        if phrase not in platform_text:
            fail(f"{path}: platform evidence must mention {phrase}")

    blockers = require_list(data, "harness_blockers")
    blocker_ids: list[str] = []
    blocker_names: list[str] = []
    for item in blockers:
        if not isinstance(item, dict):
            fail(f"{path}: harness_blockers entries must be objects")
        item_id = text(item.get("id"))
        if not BLOCKER_ID.match(item_id):
            fail(f"{path}: invalid harness blocker id {item_id!r}")
        blocker_ids.append(item_id)
        blocker_names.append(text(item.get("blocker")).lower())
        if item.get("status") not in {"missing", "partially_covered", "proposed"}:
            fail(f"{path}: {item_id} has invalid blocker status")
        for field in ("required_evidence", "safe_failure"):
            value = text(item.get(field))
            if len(value) < 30:
                fail(f"{path}: {item_id} {field} must be descriptive")
        require_safe_failure(path, item_id, text(item.get("safe_failure")))
    check_no_duplicates(blocker_ids, "harness blocker IDs")
    missing_blockers = sorted(REQUIRED_BLOCKERS - set(blocker_names))
    if missing_blockers:
        fail(f"{path}: missing harness blockers: {', '.join(missing_blockers)}")

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    readiness_items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(readiness_items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb012 = next((item for item in readiness_items if item.get("id") == "PB-012"), None)
    if not isinstance(pb012, dict):
        fail("pre-build-readiness.json is missing PB-012")
    if pb012.get("status") != "partial":
        fail("PB-012 must remain partial while only no-claim sandbox probe inventory, probe-package template, and readiness-review template exist")
    required_evidence = {
        "docs/research/sandbox-probe-inventory-2026-07.md",
        "docs/security-engine/machine/sandbox-probe-inventory.schema.json",
        "docs/security-engine/machine/sandbox-probe-inventory.json",
        "docs/security-engine/machine/sandbox-probe-package.schema.json",
        "docs/security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json",
        "docs/security-engine/machine/sandbox-readiness-review.schema.json",
        "docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json",
        "tools/validate_sandbox_probe_inventory.py",
        "tools/validate_sandbox_readiness_review.py",
    }
    pb012_evidence = pb012.get("evidence")
    if not isinstance(pb012_evidence, list):
        fail("PB-012 must list no-claim sandbox probe inventory evidence")
    missing_evidence = sorted(required_evidence - set(pb012_evidence))
    if missing_evidence:
        fail("PB-012 evidence is missing sandbox probe inventory records: " + ", ".join(missing_evidence))

    required_text = " ".join(
        value for value in pb012.get("evidence_required", []) if isinstance(value, str)
    ).lower()
    for phrase in [
        "packaged expected-deny probes",
        "checked no-claim probe-package template",
        "checked no-claim sandbox readiness-review template",
        "renderer",
        "network",
        "storage",
        "gpu",
        "decoder",
        "extension",
        "devtools",
        "agent",
        "updater",
        "file",
        "socket",
        "process",
        "registry",
        "device",
        "shared-memory",
        "credential",
        "debug",
        "profile",
        "ipc",
        "effective platform policy",
        "host-safe",
        "owner review",
        "owner-reviewed sandbox readiness review",
    ]:
        if phrase not in required_text:
            fail(f"PB-012 evidence_required must include {phrase}")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks") if isinstance(task_queue, dict) else None
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain a tasks array")
    task = next((item for item in tasks if item.get("id") == "TASK-000004"), None)
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000004")
    if task.get("status") != "proposed":
        fail("TASK-000004 must remain proposed until owner review converts it to an executable task")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000004 allowed_paths must be an array")
    missing_allowed = sorted(required_evidence - set(allowed_paths))
    if missing_allowed:
        fail("TASK-000004 allowed_paths is missing sandbox inventory records: " + ", ".join(missing_allowed))


def validate_probe_package(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: probe package must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    package_id = text(data.get("package_id"))
    if not PROBE_PACKAGE_ID.match(package_id):
        fail(f"{path}: invalid package_id {package_id!r}")
    if data.get("status") != "no_claim_probe_package_template":
        fail(f"{path}: status must be no_claim_probe_package_template")

    boundaries = [text(value) for value in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([text(data.get("claim_status")), *boundaries])
    boundary_text_lower = boundary_text.lower()
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase.lower() not in boundary_text_lower:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    sources = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_PROBE_PACKAGE_SOURCE_RECORDS - sources)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in REQUIRED_PROBE_PACKAGE_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: source record does not exist: {source}")

    package_status = require_dict(data, "package_status")
    for field in REQUIRED_PACKAGE_STATUS_FALSE:
        if package_status.get(field) is not False:
            fail(f"{path}: package_status.{field} must be false for the no-claim template")
    if len(text(package_status.get("current_scope"))) < 40:
        fail(f"{path}: package_status.current_scope must be descriptive")

    process_capabilities = load_json(MACHINE / "process-capabilities.json")
    roles = process_capabilities.get("roles") if isinstance(process_capabilities, dict) else None
    if not isinstance(roles, dict):
        fail("process-capabilities.json must contain a roles object")

    targets = require_list(data, "role_targets")
    target_names: list[str] = []
    for item in targets:
        if not isinstance(item, dict):
            fail(f"{path}: role_targets entries must be objects")
        target = text(item.get("target")).lower()
        target_names.append(target)
        expected_role = REQUIRED_TARGETS.get(target)
        if expected_role is None:
            fail(f"{path}: unexpected role target {target!r}")
        role = text(item.get("process_capability_role"))
        if role != expected_role:
            fail(f"{path}: target {target} must map to process capability role {expected_role}")
        if role not in roles:
            fail(f"{path}: process capability role {role!r} is not in process-capabilities.json")
        if item.get("probe_target_status") != "template_only":
            fail(f"{path}: target {target} must remain template_only")
        for field in (
            "host_safe_fixture_required",
            "broker_fixture_required",
            "compromised_client_harness_required",
            "effective_policy_capture_required",
        ):
            if item.get(field) is not True:
                fail(f"{path}: target {target} {field} must be true")
        platforms = item.get("platform_matrix_required")
        if not isinstance(platforms, list) or set(platforms) != REQUIRED_PLATFORMS:
            fail(f"{path}: target {target} platform_matrix_required must cover macos, windows, and linux")
    check_no_duplicates(target_names, "probe package role targets")
    if set(target_names) != set(REQUIRED_TARGETS):
        fail(
            f"{path}: probe package role targets must be exactly: "
            + ", ".join(sorted(REQUIRED_TARGETS))
        )

    access_surfaces = [normalize_surface(text(value)) for value in require_list(data, "access_surfaces")]
    check_no_duplicates(access_surfaces, "probe package access surfaces")
    if set(access_surfaces) != REQUIRED_SURFACES:
        fail(
            f"{path}: probe package access surfaces must be exactly: "
            + ", ".join(sorted(REQUIRED_SURFACES))
        )

    platform_records = require_list(data, "platform_evidence_requirements")
    platform_names: list[str] = []
    for item in platform_records:
        if not isinstance(item, dict):
            fail(f"{path}: platform_evidence_requirements entries must be objects")
        platform = text(item.get("platform")).lower()
        platform_names.append(platform)
        artifacts = item.get("required_artifacts")
        if not isinstance(artifacts, list) or len(artifacts) < 4:
            fail(f"{path}: platform {platform} required_artifacts must list evidence")
        artifact_text = " ".join(text(value).lower() for value in artifacts)
        for phrase in REQUIRED_PLATFORM_PACKAGE_TERMS.get(platform, set()):
            if phrase not in artifact_text:
                fail(f"{path}: platform {platform} evidence must mention {phrase}")
        if len(text(item.get("missing_evidence"))) < 30:
            fail(f"{path}: platform {platform} missing_evidence must be descriptive")
    check_no_duplicates(platform_names, "probe package platform evidence records")
    if set(platform_names) != REQUIRED_PLATFORMS:
        fail(f"{path}: probe package platform evidence must cover macos, windows, and linux")

    lifecycle = require_list(data, "probe_lifecycle")
    stages: list[str] = []
    lifecycle_text = ""
    for item in lifecycle:
        if not isinstance(item, dict):
            fail(f"{path}: probe_lifecycle entries must be objects")
        stage = text(item.get("stage"))
        stages.append(stage)
        required_record = text(item.get("required_record"))
        if len(required_record) < 30:
            fail(f"{path}: lifecycle stage {stage} required_record must be descriptive")
        lifecycle_text += " " + required_record.lower()
    check_no_duplicates(stages, "probe package lifecycle stages")
    if set(stages) != REQUIRED_PACKAGE_LIFECYCLE_STAGES:
        fail(
            f"{path}: probe package lifecycle stages must be exactly: "
            + ", ".join(sorted(REQUIRED_PACKAGE_LIFECYCLE_STAGES))
        )
    for phrase in ("artifact build id", "effective platform policy", "expected-deny", "cleanup"):
        if phrase not in lifecycle_text:
            fail(f"{path}: probe_lifecycle must mention {phrase}")

    result_text = " ".join(text(value).lower() for value in require_list(data, "result_record_requirements"))
    for phrase in REQUIRED_RESULT_FIELDS:
        if phrase not in result_text:
            fail(f"{path}: result_record_requirements must include {phrase}")

    rejection_rules = require_list(data, "rejection_rules")
    rejection_text = ""
    rule_names: list[str] = []
    for item in rejection_rules:
        if not isinstance(item, dict):
            fail(f"{path}: rejection_rules entries must be objects")
        rule = text(item.get("rule"))
        rule_names.append(rule)
        condition = text(item.get("condition"))
        if len(condition) < 30:
            fail(f"{path}: rejection rule {rule} condition must be descriptive")
        rejection_text += " " + condition.lower()
    check_no_duplicates(rule_names, "probe package rejection rules")
    for phrase in REQUIRED_REJECTION_TERMS:
        if phrase not in rejection_text:
            fail(f"{path}: rejection_rules must mention {phrase}")

    commands = set(text(value) for value in require_list(data, "validation_commands"))
    missing_commands = sorted(REQUIRED_VALIDATION_COMMANDS - commands)
    if missing_commands:
        fail(f"{path}: missing validation commands: {', '.join(missing_commands)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inventories",
        nargs="*",
        type=Path,
        default=[DEFAULT_INVENTORY],
        help="Sandbox probe inventory JSON files to validate.",
    )
    parser.add_argument(
        "--probe-package",
        type=Path,
        default=DEFAULT_PROBE_PACKAGE,
        help="No-claim sandbox probe package template to validate.",
    )
    args = parser.parse_args()
    for path in args.inventories:
        validate_inventory(path)
    validate_probe_package(args.probe_package)
    print(
        "sandbox probe inventory validation passed: "
        f"{len(args.inventories)} inventory file(s), 1 probe-package template"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
