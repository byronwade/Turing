#!/usr/bin/env python3
"""Validate no-claim research package/update lab inventories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = (
    ROOT
    / "docs"
    / "release-operations"
    / "machine"
    / "research-package-update-lab.json"
)
DEFAULT_LAB_PACKAGE = (
    ROOT
    / "docs"
    / "release-operations"
    / "machine"
    / "research-package-update-lab-packages"
    / "no-claim-update-lab-template.json"
)

LAB_ID = re.compile(r"^REL\.UPDATE\.[A-Z0-9._-]+$")
LAB_PACKAGE_ID = re.compile(r"^REL\.UPDATE_LAB_PACKAGE\.[A-Z0-9._-]+$")
PACKAGE_ID = re.compile(r"^REL-PKG-[A-Z0-9._-]+$")
UPDATE_ID = re.compile(r"^REL-UPD-[A-Z0-9._-]+$")

REQUIRED_PACKAGE_FIELDS = {
    "source commit",
    "build ID",
    "channel",
    "platform",
    "architecture",
    "toolchain",
    "feature set",
    "SBOM",
    "provenance",
    "symbols",
    "notices",
    "artifact hashes",
    "artifact sizes",
    "no-stable-support label",
}

REQUIRED_UPDATE_BEHAVIORS = {
    "role separation",
    "signature threshold",
    "expiry",
    "minimum secure version",
    "rollout",
    "mirrors",
    "staged install",
    "tamper",
    "replay",
    "wrong-target",
    "partial-write",
    "disk-full",
    "power-loss",
    "rollback",
    "vulnerable version refusal",
    "migration",
    "downgrade",
    "crash-loop",
    "privacy-preserving local event",
}

REQUIRED_CLAIM_PHRASES = [
    "no production signing keys",
    "no offline root keys",
    "no stable channel",
    "no real updater",
    "no public binary distribution",
    "no real user profile migration",
    "no rollback safety claim",
    "no migration safety claim",
    "no release readiness claim",
    "no supported security claim",
    "no production updater claim",
]

SAFE_FAILURE_TERMS = [
    "abort",
    "block",
    "discard",
    "hold",
    "preserve",
    "quarantine",
    "recover",
    "redact",
    "reject",
    "stop",
]

PACKAGE_REQUIRED_TERMS = {
    "source commit",
    "build",
    "channel",
    "platform",
    "architecture",
    "toolchain",
    "feature",
    "sbom",
    "provenance",
    "symbols",
    "notices",
    "hash",
    "size",
    "no-stable-support",
}
REQUIRED_LAB_PACKAGE_SOURCES = {
    "docs/research/research-package-update-lab-inventory-2026-07.md",
    "docs/release-operations/machine/research-package-update-lab.schema.json",
    "docs/release-operations/machine/research-package-update-lab.json",
    "docs/release-operations/machine/research-package-update-lab-package.schema.json",
    "docs/release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/13-build-release-operations.md",
    "docs/release-operations/README.md",
    "docs/security-engine/05-update-supply-chain-and-vulnerability-response.md",
}
REQUIRED_LAB_PACKAGE_CLAIM_PHRASES = [
    "no executable package manifest",
    "no update metadata parser",
    "no signature threshold tests",
    "no staged install tests",
    "no rollback migration tests",
    *REQUIRED_CLAIM_PHRASES,
]
REQUIRED_LAB_LIFECYCLE = [
    "collect_source_identity",
    "generate_research_manifest",
    "sign_with_fake_keys",
    "publish_local_metadata",
    "stage_install",
    "verify_or_reject",
    "rollback_or_hold",
    "record_privacy_event",
    "cleanup",
]
REQUIRED_LAB_REJECTION_TERMS = [
    "production signing keys",
    "offline root",
    "stable channel",
    "real updater",
    "public distribution",
    "real user profile",
    "executable package manifest",
    "metadata parser",
    "tamper",
    "replay",
    "wrong-target",
    "expiry",
    "partial-write",
    "disk-full",
    "power-loss",
    "rollback safety",
    "migration safety",
    "supported security",
    "privacy",
    "owner review",
]


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing inventory: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        fail(f"{key} must be an array")
    return value


def require_string_list(data: dict[str, Any], key: str, label: str) -> list[str]:
    value = require_list(data, key)
    if any(not isinstance(item, str) or not item for item in value):
        fail(f"{label}.{key} must contain non-empty strings")
    return value


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def validate_inventory(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: inventory must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    lab_id = text(data.get("lab_id"))
    if not LAB_ID.match(lab_id):
        fail(f"{path}: invalid lab_id {lab_id!r}")
    if data.get("status") != "no_claim_lab_inventory":
        fail(f"{path}: status must be no_claim_lab_inventory")

    claim_status = text(data.get("claim_status")).lower()
    boundaries = [text(item).lower() for item in require_list(data, "unsupported_boundaries")]
    boundary_text = " ".join([claim_status, *boundaries])
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing unsupported boundary phrase: {phrase}")

    package_items = require_list(data, "package_identity_fields")
    package_ids: list[str] = []
    package_fields: list[str] = []
    package_text = ""
    for item in package_items:
        if not isinstance(item, dict):
            fail(f"{path}: package_identity_fields entries must be objects")
        item_id = text(item.get("id"))
        if not PACKAGE_ID.match(item_id):
            fail(f"{path}: invalid package field id {item_id!r}")
        package_ids.append(item_id)
        field = text(item.get("field"))
        package_fields.append(field)
        for required in ["requirement", "evidence_gap", "boundary"]:
            value = text(item.get(required))
            if len(value) < 20:
                fail(f"{path}: {item_id} {required} must be descriptive")
            package_text += " " + value.lower()
        package_text += " " + field.lower()
    check_no_duplicates(package_ids, "package field IDs")
    missing_package_fields = sorted(REQUIRED_PACKAGE_FIELDS - set(package_fields))
    if missing_package_fields:
        fail(f"{path}: missing package fields: {', '.join(missing_package_fields)}")
    normalized_package_text = package_text.replace("stable support", "stable-support")
    for term in PACKAGE_REQUIRED_TERMS:
        if term not in normalized_package_text:
            fail(f"{path}: package field coverage missing term: {term}")

    behavior_items = require_list(data, "update_behavior_matrix")
    behavior_ids: list[str] = []
    behaviors: list[str] = []
    for item in behavior_items:
        if not isinstance(item, dict):
            fail(f"{path}: update_behavior_matrix entries must be objects")
        item_id = text(item.get("id"))
        if not UPDATE_ID.match(item_id):
            fail(f"{path}: invalid update behavior id {item_id!r}")
        behavior_ids.append(item_id)
        behavior = text(item.get("behavior"))
        behaviors.append(behavior)
        for required in ["required_evidence", "negative_case", "safe_failure"]:
            value = text(item.get(required))
            if len(value) < 20:
                fail(f"{path}: {item_id} {required} must be descriptive")
        safe_failure = text(item.get("safe_failure")).lower()
        if not any(term in safe_failure for term in SAFE_FAILURE_TERMS):
            fail(f"{path}: {item_id} safe_failure must describe rejection, blocking, recovery, or preservation")
    check_no_duplicates(behavior_ids, "update behavior IDs")
    missing_behaviors = sorted(REQUIRED_UPDATE_BEHAVIORS - set(behaviors))
    if missing_behaviors:
        fail(f"{path}: missing update behaviors: {', '.join(missing_behaviors)}")


def validate_lab_package(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: lab package must be an object")
    allowed = {
        "$schema",
        "schema_version",
        "package_id",
        "status",
        "updated",
        "claim_status",
        "source_records",
        "package_status",
        "manifest_fields",
        "metadata_behavior_axes",
        "lab_lifecycle",
        "fixture_policy",
        "rejection_rules",
        "unsupported_boundaries",
        "validation_commands",
    }
    extra = sorted(set(data) - allowed)
    if extra:
        fail(f"{path}: unsupported lab package fields: {', '.join(extra)}")
    missing = sorted(allowed - set(data))
    if missing:
        fail(f"{path}: missing lab package fields: {', '.join(missing)}")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    package_id = text(data.get("package_id"))
    if not LAB_PACKAGE_ID.match(package_id):
        fail(f"{path}: invalid package_id {package_id!r}")
    if data.get("status") != "no_claim_update_lab_package_template":
        fail(f"{path}: status must be no_claim_update_lab_package_template")

    claim_status = text(data.get("claim_status")).lower()
    boundaries = [
        item.lower() for item in require_string_list(data, "unsupported_boundaries", "lab package")
    ]
    boundary_text = " ".join([claim_status, *boundaries])
    for phrase in REQUIRED_LAB_PACKAGE_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing unsupported lab-package phrase: {phrase}")

    sources = set(require_string_list(data, "source_records", "lab package"))
    missing_sources = sorted(REQUIRED_LAB_PACKAGE_SOURCES - sources)
    if missing_sources:
        fail(f"{path}: source_records missing: {', '.join(missing_sources)}")

    package_status = data.get("package_status")
    if not isinstance(package_status, dict):
        fail(f"{path}: package_status must be an object")
    status_keys = {
        "executable_package_manifest",
        "update_metadata_parser",
        "signature_threshold_tests",
        "staged_install_tests",
        "rollback_migration_tests",
        "production_keys_present",
        "owner_reviewed",
        "current_scope",
    }
    extra_status = sorted(set(package_status) - status_keys)
    if extra_status:
        fail(f"{path}: package_status has unsupported fields: {', '.join(extra_status)}")
    missing_status = sorted(status_keys - set(package_status))
    if missing_status:
        fail(f"{path}: package_status missing: {', '.join(missing_status)}")
    for key in sorted(status_keys - {"current_scope"}):
        if package_status.get(key) is not False:
            fail(f"{path}: package_status.{key} must be false for the no-claim template")
    current_scope = text(package_status.get("current_scope")).lower()
    for term in [
        "no executable package manifest",
        "no update metadata parser",
        "no signature threshold test",
        "no staged install test",
        "no rollback migration test",
        "no production keys",
    ]:
        if term not in current_scope:
            fail(f"{path}: package_status.current_scope must mention {term}")

    manifest_fields = set(require_string_list(data, "manifest_fields", "lab package"))
    missing_fields = sorted(REQUIRED_PACKAGE_FIELDS - manifest_fields)
    if missing_fields:
        fail(f"{path}: manifest_fields missing: {', '.join(missing_fields)}")
    check_no_duplicates(list(manifest_fields), "manifest fields")

    behavior_axes = set(require_string_list(data, "metadata_behavior_axes", "lab package"))
    missing_axes = sorted(REQUIRED_UPDATE_BEHAVIORS - behavior_axes)
    if missing_axes:
        fail(f"{path}: metadata_behavior_axes missing: {', '.join(missing_axes)}")
    check_no_duplicates(list(behavior_axes), "metadata behavior axes")

    lifecycle = require_list(data, "lab_lifecycle")
    lifecycle_stages: list[str] = []
    lifecycle_text = ""
    for item in lifecycle:
        if not isinstance(item, dict):
            fail(f"{path}: lab_lifecycle entries must be objects")
        allowed_lifecycle = {"stage", "required_record"}
        extra_lifecycle = sorted(set(item) - allowed_lifecycle)
        if extra_lifecycle:
            fail(f"{path}: lab_lifecycle entry has unsupported fields: {', '.join(extra_lifecycle)}")
        stage = text(item.get("stage"))
        record = text(item.get("required_record"))
        if not stage or len(record) < 30:
            fail(f"{path}: lab_lifecycle entries need stage and descriptive required_record")
        lifecycle_stages.append(stage)
        lifecycle_text += " " + record.lower()
    if lifecycle_stages != REQUIRED_LAB_LIFECYCLE:
        fail(f"{path}: lab_lifecycle stages must remain in the required order")
    for term in [
        "fake",
        "local metadata",
        "tamper",
        "replay",
        "wrong-target",
        "rollback",
        "privacy",
        "cleanup",
    ]:
        if term not in lifecycle_text:
            fail(f"{path}: lab_lifecycle must mention {term}")

    fixture_policy = data.get("fixture_policy")
    if not isinstance(fixture_policy, dict):
        fail(f"{path}: fixture_policy must be an object")
    fixture_keys = {
        "fake_signing_keys_required",
        "offline_root_keys",
        "stable_channel_prohibited",
        "local_metadata_only",
        "fake_profiles_required",
        "bounded_temp_roots_required",
        "cleanup_required",
    }
    extra_fixture = sorted(set(fixture_policy) - fixture_keys)
    if extra_fixture:
        fail(f"{path}: fixture_policy has unsupported fields: {', '.join(extra_fixture)}")
    missing_fixture = sorted(fixture_keys - set(fixture_policy))
    if missing_fixture:
        fail(f"{path}: fixture_policy missing: {', '.join(missing_fixture)}")
    if text(fixture_policy.get("offline_root_keys")) != "prohibited":
        fail(f"{path}: fixture_policy.offline_root_keys must be prohibited")
    for key in sorted(fixture_keys - {"offline_root_keys"}):
        if fixture_policy.get(key) is not True:
            fail(f"{path}: fixture_policy.{key} must be true")

    rules = require_list(data, "rejection_rules")
    rules_text = ""
    for item in rules:
        if not isinstance(item, dict):
            fail(f"{path}: rejection_rules entries must be objects")
        allowed_rule = {"rule", "condition"}
        extra_rule = sorted(set(item) - allowed_rule)
        if extra_rule:
            fail(f"{path}: rejection_rules entry has unsupported fields: {', '.join(extra_rule)}")
        rule = text(item.get("rule"))
        condition = text(item.get("condition"))
        if not rule or len(condition) < 30:
            fail(f"{path}: rejection_rules entries need rule and descriptive condition")
        rules_text += f" {rule.lower()} {condition.lower()}"
    for term in REQUIRED_LAB_REJECTION_TERMS:
        if term not in rules_text:
            fail(f"{path}: rejection_rules must mention {term}")

    commands = require_string_list(data, "validation_commands", "lab package")
    for command in [
        "python3 -B tools/validate_research_package_update_lab.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in commands:
            fail(f"{path}: validation_commands must include {command}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[DEFAULT_INVENTORY, DEFAULT_LAB_PACKAGE],
        help="Research package/update lab inventory or package JSON files to validate.",
    )
    args = parser.parse_args()
    inventories = 0
    lab_packages = 0
    for path in args.paths:
        payload = load_json(path)
        if not isinstance(payload, dict):
            fail(f"{path}: payload must be an object")
        if "lab_id" in payload:
            validate_inventory(path)
            inventories += 1
        elif "package_id" in payload:
            validate_lab_package(path)
            lab_packages += 1
        else:
            fail(f"{path}: expected lab_id or package_id")
    print(
        "research package/update lab validation passed: "
        f"{inventories} inventory file(s), {lab_packages} lab-package template(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
