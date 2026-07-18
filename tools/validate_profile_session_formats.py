#!/usr/bin/env python3
"""Validate no-claim profile/session format inventories."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = (
    ROOT
    / "docs"
    / "storage"
    / "machine"
    / "profile-session-format-inventory.json"
)
DEFAULT_SCHEMA_PACKAGE = (
    ROOT
    / "docs"
    / "storage"
    / "machine"
    / "profile-session-schema-packages"
    / "no-claim-profile-session-schema-template.json"
)

INVENTORY_ID = re.compile(r"^STORAGE\.FORMAT\.[A-Z0-9._-]+$")
RECORD_TYPE_ID = re.compile(r"^STO-FORMAT-[A-Z0-9._-]+$")
BEHAVIOR_ID = re.compile(r"^STO-BEHAVIOR-[A-Z0-9._-]+$")
SCHEMA_PACKAGE_ID = re.compile(r"^PROFILE_SESSION\.SCHEMA_PACKAGE\.[A-Z0-9._-]+$")

REQUIRED_RECORD_TYPES = {
    "STO-FORMAT-PROFILE",
    "STO-FORMAT-SPACE",
    "STO-FORMAT-SESSION",
    "STO-FORMAT-SNAPSHOT",
    "STO-FORMAT-MIGRATION",
}
REQUIRED_BEHAVIORS = {
    "STO-BEHAVIOR-DISK-FULL",
    "STO-BEHAVIOR-POWER-LOSS",
    "STO-BEHAVIOR-CORRUPTION",
    "STO-BEHAVIOR-DOWNGRADE",
    "STO-BEHAVIOR-EXPORT",
    "STO-BEHAVIOR-DELETION",
    "STO-BEHAVIOR-PRIVATE-SESSION",
    "STO-BEHAVIOR-CRASH-RECOVERY",
    "STO-BEHAVIOR-PROTECTED-WORK",
    "STO-BEHAVIOR-PRIVACY",
    "STO-BEHAVIOR-DATA-LOSS",
}
REQUIRED_CLAIM_PHRASES = {
    "no profile implementation",
    "no real-profile migration",
    "no sync support",
    "no credential storage support",
    "no user-data handling readiness",
    "no data-loss safety claim",
    "no production profile-format claim",
    "no implementation claim",
}
REQUIRED_RECORD_TERMS = {
    "schema_version",
    "profile",
    "authority",
    "privacy",
    "failure",
}
REQUIRED_PACKAGE_SOURCES = {
    "docs/research/profile-session-format-inventory-2026-07.md",
    "docs/storage/machine/profile-session-format-inventory.schema.json",
    "docs/storage/machine/profile-session-format-inventory.json",
    "docs/storage/machine/profile-session-schema-package.schema.json",
    "docs/storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/07-network-storage-media.md",
    "docs/storage/README.md",
    "docs/product-experience/README.md",
}
REQUIRED_PACKAGE_CLAIM_PHRASES = {
    "no executable profile schema",
    "no space schema",
    "no session schema",
    "no snapshot schema",
    "no migration schema",
    "no real-profile migration claim",
    "no sync claim",
    "no credential-storage claim",
    "no data-loss safety claim",
    "no user-data handling readiness claim",
    "no production profile-format claim",
    "no implementation claim",
}
REQUIRED_FORMAT_TARGETS = {
    "profile",
    "space",
    "session",
    "snapshot",
    "migration",
}
REQUIRED_BEHAVIOR_AXES = {
    "disk-full",
    "power-loss",
    "corruption",
    "downgrade",
    "export",
    "deletion",
    "private-session",
    "crash-recovery",
    "protected-work",
    "privacy",
    "data-loss",
}
REQUIRED_SCHEMA_RECORD_TERMS = {
    "schema id",
    "schema version",
    "profile id",
    "space id",
    "session id",
    "snapshot id",
    "migration id",
    "created at",
    "updated at",
    "origin or storage key",
    "privacy mode",
    "encryption state",
    "retention policy",
    "downgrade policy",
    "repair policy",
    "deletion policy",
    "export policy",
    "checksum or integrity marker",
}
REQUIRED_MIGRATION_STAGES = [
    "classify_source",
    "validate_input",
    "plan_migration",
    "write_temporary_snapshot",
    "commit_or_rollback",
    "repair_or_quarantine",
    "verify_privacy_and_cleanup",
]
REQUIRED_REJECTION_TERMS = {
    "executable schema",
    "success-only",
    "protected work",
    "private-session",
    "corrupt",
    "downgrade",
    "real user data",
    "sync",
    "credential",
    "production",
    "owner review",
}


class ValidationError(ValueError):
    pass


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(path: Path, message: str) -> None:
    raise ValidationError(f"{relative(path)}: {message}")


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(path, f"invalid JSON: {error}")


def require_object(path: Path, value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(path, f"{label} must be an object")
    return value


def reject_extra(
    path: Path, obj: dict[str, object], allowed: set[str], label: str
) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(
    path: Path, obj: dict[str, object], required: set[str], label: str
) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        fail(path, f"{label}.{key} must be a non-empty array")
    if any(not isinstance(item, str) or not item for item in value):
        fail(path, f"{label}.{key} must contain non-empty strings")
    return value


def ensure_unique(path: Path, values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(path, f"duplicate {label}: {', '.join(duplicates)}")


def validate_record_types(path: Path, value: object) -> None:
    if not isinstance(value, list):
        fail(path, "record_types must be an array")
    ids: list[str] = []
    required = {
        "record_type_id",
        "name",
        "purpose",
        "versioning",
        "authority_boundary",
        "required_fields",
        "privacy_rules",
        "failure_cases",
        "unsupported",
    }
    for index, record_value in enumerate(value, start=1):
        record = require_object(path, record_value, f"record_types[{index}]")
        reject_extra(path, record, required, f"record_types[{index}]")
        require_keys(path, record, required, f"record_types[{index}]")
        record_id = require_string(path, record, "record_type_id", f"record_types[{index}]")
        if not RECORD_TYPE_ID.fullmatch(record_id):
            fail(path, f"invalid record_type_id: {record_id}")
        ids.append(record_id)
        text = " ".join(
            [
                require_string(path, record, "purpose", f"record_types[{index}]"),
                require_string(path, record, "versioning", f"record_types[{index}]"),
                require_string(
                    path, record, "authority_boundary", f"record_types[{index}]"
                ),
                " ".join(
                    require_string_array(
                        path, record, "required_fields", f"record_types[{index}]"
                    )
                ),
                " ".join(
                    require_string_array(
                        path, record, "privacy_rules", f"record_types[{index}]"
                    )
                ),
                " ".join(
                    require_string_array(
                        path, record, "failure_cases", f"record_types[{index}]"
                    )
                ),
                " ".join(
                    require_string_array(
                        path, record, "unsupported", f"record_types[{index}]"
                    )
                ),
            ]
        ).lower()
        require_string(path, record, "name", f"record_types[{index}]")
        missing_terms = [term for term in REQUIRED_RECORD_TERMS if term not in text]
        if missing_terms:
            fail(path, f"{record_id} must discuss: {', '.join(missing_terms)}")
    ensure_unique(path, ids, "record_type_id")
    missing = REQUIRED_RECORD_TYPES - set(ids)
    if missing:
        fail(path, "missing required record types: " + ", ".join(sorted(missing)))


def validate_behaviors(path: Path, value: object) -> None:
    if not isinstance(value, list):
        fail(path, "behavior_matrix must be an array")
    ids: list[str] = []
    required = {"behavior_id", "name", "purpose", "required_conditions", "safe_failure"}
    for index, behavior_value in enumerate(value, start=1):
        behavior = require_object(path, behavior_value, f"behavior_matrix[{index}]")
        reject_extra(path, behavior, required, f"behavior_matrix[{index}]")
        require_keys(path, behavior, required, f"behavior_matrix[{index}]")
        behavior_id = require_string(
            path, behavior, "behavior_id", f"behavior_matrix[{index}]"
        )
        if not BEHAVIOR_ID.fullmatch(behavior_id):
            fail(path, f"invalid behavior_id: {behavior_id}")
        ids.append(behavior_id)
        require_string(path, behavior, "name", f"behavior_matrix[{index}]")
        require_string(path, behavior, "purpose", f"behavior_matrix[{index}]")
        require_string_array(
            path, behavior, "required_conditions", f"behavior_matrix[{index}]"
        )
        safe_failure = require_string(
            path, behavior, "safe_failure", f"behavior_matrix[{index}]"
        )
        if not any(
            term in safe_failure.lower()
            for term in (
                "fail",
                "reject",
                "quarantine",
                "block",
                "abort",
                "stop",
                "discard",
                "do not",
            )
        ):
            fail(path, f"{behavior_id}.safe_failure must define a failure behavior")
    ensure_unique(path, ids, "behavior_id")
    missing = REQUIRED_BEHAVIORS - set(ids)
    if missing:
        fail(path, "missing required behaviors: " + ", ".join(sorted(missing)))


def validate_inventory(path: Path, payload: object) -> None:
    inventory = require_object(path, payload, "inventory")
    required = {
        "schema_version",
        "inventory_id",
        "status",
        "updated",
        "claim_status",
        "record_types",
        "behavior_matrix",
        "unsupported_boundaries",
    }
    reject_extra(path, inventory, required, "inventory")
    require_keys(path, inventory, required, "inventory")
    if inventory.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    inventory_id = require_string(path, inventory, "inventory_id", "inventory")
    if not INVENTORY_ID.fullmatch(inventory_id):
        fail(path, "inventory_id has invalid format")
    if require_string(path, inventory, "status", "inventory") != "no_claim_format_inventory":
        fail(path, "status must remain no_claim_format_inventory")
    require_string(path, inventory, "updated", "inventory")
    claim_status = require_string(path, inventory, "claim_status", "inventory")
    unsupported = require_string_array(
        path, inventory, "unsupported_boundaries", "inventory"
    )
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
        if not any(phrase in item for item in unsupported):
            fail(path, f"unsupported_boundaries must mention: {phrase}")

    validate_record_types(path, inventory.get("record_types"))
    validate_behaviors(path, inventory.get("behavior_matrix"))


def validate_schema_package(path: Path, payload: object) -> None:
    package = require_object(path, payload, "schema_package")
    required = {
        "$schema",
        "schema_version",
        "package_id",
        "status",
        "updated",
        "claim_status",
        "source_records",
        "package_status",
        "format_targets",
        "behavior_axes",
        "schema_record_requirements",
        "migration_lifecycle",
        "fixture_policy",
        "rejection_rules",
        "unsupported_boundaries",
        "validation_commands",
    }
    reject_extra(path, package, required, "schema_package")
    require_keys(path, package, required, "schema_package")
    if package.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    package_id = require_string(path, package, "package_id", "schema_package")
    if not SCHEMA_PACKAGE_ID.fullmatch(package_id):
        fail(path, "package_id has invalid format")
    if (
        require_string(path, package, "status", "schema_package")
        != "no_claim_schema_package_template"
    ):
        fail(path, "status must remain no_claim_schema_package_template")
    require_string(path, package, "updated", "schema_package")
    claim_status = require_string(path, package, "claim_status", "schema_package").lower()
    unsupported = [
        item.lower()
        for item in require_string_array(
            path, package, "unsupported_boundaries", "schema_package"
        )
    ]
    for phrase in REQUIRED_PACKAGE_CLAIM_PHRASES:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
        if not any(phrase in item for item in unsupported):
            fail(path, f"unsupported_boundaries must mention: {phrase}")

    sources = set(require_string_array(path, package, "source_records", "schema_package"))
    missing_sources = REQUIRED_PACKAGE_SOURCES - sources
    if missing_sources:
        fail(
            path,
            "source_records is missing: " + ", ".join(sorted(missing_sources)),
        )

    package_status = require_object(
        path, package.get("package_status"), "package_status"
    )
    status_keys = {
        "executable_schemas",
        "migration_tests_run",
        "fault_tests_run",
        "real_profile_fixture_approved",
        "owner_reviewed",
        "current_scope",
    }
    reject_extra(path, package_status, status_keys, "package_status")
    require_keys(path, package_status, status_keys, "package_status")
    for key in sorted(status_keys - {"current_scope"}):
        if package_status.get(key) is not False:
            fail(path, f"package_status.{key} must be false for the no-claim template")
    current_scope = require_string(path, package_status, "current_scope", "package_status")
    for term in ("no executable schema", "no migration test", "no fault test", "no real-profile"):
        if term not in current_scope.lower():
            fail(path, f"package_status.current_scope must mention {term}")

    targets_value = package.get("format_targets")
    if not isinstance(targets_value, list):
        fail(path, "format_targets must be an array")
    targets: list[str] = []
    target_keys = {
        "target",
        "schema_status",
        "versioning_required",
        "privacy_review_required",
        "downgrade_behavior_required",
        "repair_behavior_required",
        "owner_review_required",
    }
    boolean_keys = sorted(target_keys - {"target", "schema_status"})
    for index, target_value in enumerate(targets_value, start=1):
        target = require_object(path, target_value, f"format_targets[{index}]")
        reject_extra(path, target, target_keys, f"format_targets[{index}]")
        require_keys(path, target, target_keys, f"format_targets[{index}]")
        target_name = require_string(path, target, "target", f"format_targets[{index}]")
        targets.append(target_name)
        if target.get("schema_status") != "template_only":
            fail(path, f"{target_name}.schema_status must remain template_only")
        for key in boolean_keys:
            if target.get(key) is not True:
                fail(path, f"{target_name}.{key} must be true")
    ensure_unique(path, targets, "format target")
    if set(targets) != REQUIRED_FORMAT_TARGETS:
        missing = REQUIRED_FORMAT_TARGETS - set(targets)
        extra = set(targets) - REQUIRED_FORMAT_TARGETS
        detail = []
        if missing:
            detail.append("missing " + ", ".join(sorted(missing)))
        if extra:
            detail.append("unexpected " + ", ".join(sorted(extra)))
        fail(path, "format_targets mismatch: " + "; ".join(detail))

    behavior_axes = set(require_string_array(path, package, "behavior_axes", "schema_package"))
    if behavior_axes != REQUIRED_BEHAVIOR_AXES:
        missing = REQUIRED_BEHAVIOR_AXES - behavior_axes
        extra = behavior_axes - REQUIRED_BEHAVIOR_AXES
        detail = []
        if missing:
            detail.append("missing " + ", ".join(sorted(missing)))
        if extra:
            detail.append("unexpected " + ", ".join(sorted(extra)))
        fail(path, "behavior_axes mismatch: " + "; ".join(detail))

    record_terms = set(
        require_string_array(path, package, "schema_record_requirements", "schema_package")
    )
    missing_record_terms = REQUIRED_SCHEMA_RECORD_TERMS - record_terms
    if missing_record_terms:
        fail(
            path,
            "schema_record_requirements is missing: "
            + ", ".join(sorted(missing_record_terms)),
        )

    lifecycle_value = package.get("migration_lifecycle")
    if not isinstance(lifecycle_value, list):
        fail(path, "migration_lifecycle must be an array")
    lifecycle_keys = {"stage", "required_record"}
    lifecycle_stages: list[str] = []
    lifecycle_text_parts: list[str] = []
    for index, stage_value in enumerate(lifecycle_value, start=1):
        stage = require_object(path, stage_value, f"migration_lifecycle[{index}]")
        reject_extra(path, stage, lifecycle_keys, f"migration_lifecycle[{index}]")
        require_keys(path, stage, lifecycle_keys, f"migration_lifecycle[{index}]")
        stage_name = require_string(
            path, stage, "stage", f"migration_lifecycle[{index}]"
        )
        lifecycle_stages.append(stage_name)
        lifecycle_text_parts.append(
            require_string(
                path, stage, "required_record", f"migration_lifecycle[{index}]"
            )
        )
    if lifecycle_stages != REQUIRED_MIGRATION_STAGES:
        fail(path, "migration_lifecycle stages must remain in the required order")
    lifecycle_text = " ".join(lifecycle_text_parts).lower()
    for term in ("rollback", "repair", "privacy", "cleanup"):
        if term not in lifecycle_text:
            fail(path, f"migration_lifecycle must mention {term}")

    fixture_policy = require_object(path, package.get("fixture_policy"), "fixture_policy")
    fixture_keys = {
        "real_user_profile_data",
        "fake_profile_required",
        "fake_credentials_required",
        "private_session_fixture_required",
        "bounded_temp_roots_required",
        "cleanup_required",
    }
    reject_extra(path, fixture_policy, fixture_keys, "fixture_policy")
    require_keys(path, fixture_policy, fixture_keys, "fixture_policy")
    real_data = require_string(
        path, fixture_policy, "real_user_profile_data", "fixture_policy"
    )
    if "prohibited_until_owner_approved_policy" not in real_data:
        fail(path, "fixture_policy.real_user_profile_data must prohibit real data")
    for key in sorted(fixture_keys - {"real_user_profile_data"}):
        if fixture_policy.get(key) is not True:
            fail(path, f"fixture_policy.{key} must be true")

    rules_value = package.get("rejection_rules")
    if not isinstance(rules_value, list):
        fail(path, "rejection_rules must be an array")
    rule_keys = {"rule", "condition"}
    rule_text_parts: list[str] = []
    for index, rule_value in enumerate(rules_value, start=1):
        rule = require_object(path, rule_value, f"rejection_rules[{index}]")
        reject_extra(path, rule, rule_keys, f"rejection_rules[{index}]")
        require_keys(path, rule, rule_keys, f"rejection_rules[{index}]")
        rule_text_parts.append(require_string(path, rule, "rule", f"rejection_rules[{index}]"))
        rule_text_parts.append(
            require_string(path, rule, "condition", f"rejection_rules[{index}]")
        )
    rule_text = " ".join(rule_text_parts).lower()
    for term in REQUIRED_REJECTION_TERMS:
        if term not in rule_text:
            fail(path, f"rejection_rules must mention {term}")

    commands = require_string_array(path, package, "validation_commands", "schema_package")
    for command in [
        "python3 -B tools/validate_profile_session_formats.py",
        "python3 -B tools/validate_blueprint.py",
        ".\\tools\\check.ps1",
    ]:
        if command not in commands:
            fail(path, f"validation_commands must include {command}")


def main(argv: list[str]) -> int:
    paths = (
        [Path(arg).resolve() for arg in argv]
        if argv
        else [DEFAULT_INVENTORY, DEFAULT_SCHEMA_PACKAGE]
    )
    inventories = 0
    schema_packages = 0
    try:
        for path in paths:
            payload = load_json(path)
            obj = require_object(path, payload, "payload")
            if "inventory_id" in obj:
                validate_inventory(path, obj)
                inventories += 1
            elif "package_id" in obj:
                validate_schema_package(path, obj)
                schema_packages += 1
            else:
                fail(path, "expected inventory_id or package_id")
    except ValidationError as error:
        print(f"profile/session format validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "profile/session format validation passed: "
        f"{inventories} inventory file(s), {schema_packages} schema-package template(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
