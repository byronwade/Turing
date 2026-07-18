#!/usr/bin/env python3
"""Validate no-claim UI component fixture inventories."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = (
    ROOT / "docs" / "ui-runtime" / "machine" / "component-fixture-inventory.json"
)

INVENTORY_ID = re.compile(r"^UI\.FIXTURE\.[A-Z0-9._-]+$")
TOKEN_GROUP_ID = re.compile(r"^UI-TOKEN-GROUP-[A-Z0-9._-]+$")
COMPONENT_ID = re.compile(r"^UI-COMPONENT-[A-Z0-9._-]+$")
AXIS_ID = re.compile(r"^UI-FIXTURE-AXIS-[A-Z0-9._-]+$")

REQUIRED_SURFACES = {
    "browser_chrome",
    "tabs",
    "spaces",
    "command_field",
    "permission_prompts",
    "agent_confirmations",
    "resource_manager",
    "settings",
    "recovery_ui",
}
REQUIRED_AXES = {
    "UI-FIXTURE-AXIS-KEYBOARD",
    "UI-FIXTURE-AXIS-FOCUS",
    "UI-FIXTURE-AXIS-SCREEN-READER",
    "UI-FIXTURE-AXIS-FORCED-COLOR",
    "UI-FIXTURE-AXIS-HIGH-CONTRAST",
    "UI-FIXTURE-AXIS-REDUCED-MOTION",
    "UI-FIXTURE-AXIS-DENSITY",
    "UI-FIXTURE-AXIS-LOCALIZATION",
    "UI-FIXTURE-AXIS-ERROR-STATE",
}
REQUIRED_TOKEN_GROUPS = {
    "UI-TOKEN-GROUP-TYPOGRAPHY",
    "UI-TOKEN-GROUP-SPACING-DENSITY",
    "UI-TOKEN-GROUP-COLOR-STATE",
    "UI-TOKEN-GROUP-FOCUS-MOTION",
    "UI-TOKEN-GROUP-ICONOGRAPHY",
}
REQUIRED_CLAIM_PHRASES = {
    "no UI toolkit selection",
    "no rendered fixture",
    "no accessibility readiness",
    "no trusted-chrome readiness",
    "no release-path UI approval",
    "no implementation claim",
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


def validate_token_groups(path: Path, value: object) -> set[str]:
    if not isinstance(value, list):
        fail(path, "token_groups must be an array")
    ids: list[str] = []
    for index, group_value in enumerate(value, start=1):
        group = require_object(path, group_value, f"token_groups[{index}]")
        required = {"token_group_id", "name", "purpose", "tokens"}
        reject_extra(path, group, required, f"token_groups[{index}]")
        require_keys(path, group, required, f"token_groups[{index}]")
        group_id = require_string(
            path, group, "token_group_id", f"token_groups[{index}]"
        )
        if not TOKEN_GROUP_ID.fullmatch(group_id):
            fail(path, f"invalid token_group_id: {group_id}")
        ids.append(group_id)
        require_string(path, group, "name", f"token_groups[{index}]")
        require_string(path, group, "purpose", f"token_groups[{index}]")
        require_string_array(path, group, "tokens", f"token_groups[{index}]")
    ensure_unique(path, ids, "token_group_id")
    missing = REQUIRED_TOKEN_GROUPS - set(ids)
    if missing:
        fail(path, "missing required token groups: " + ", ".join(sorted(missing)))
    return set(ids)


def validate_axes(path: Path, value: object) -> set[str]:
    if not isinstance(value, list):
        fail(path, "fixture_axes must be an array")
    ids: list[str] = []
    for index, axis_value in enumerate(value, start=1):
        axis = require_object(path, axis_value, f"fixture_axes[{index}]")
        required = {"axis_id", "name", "purpose", "required_conditions"}
        reject_extra(path, axis, required, f"fixture_axes[{index}]")
        require_keys(path, axis, required, f"fixture_axes[{index}]")
        axis_id = require_string(path, axis, "axis_id", f"fixture_axes[{index}]")
        if not AXIS_ID.fullmatch(axis_id):
            fail(path, f"invalid axis_id: {axis_id}")
        ids.append(axis_id)
        require_string(path, axis, "name", f"fixture_axes[{index}]")
        require_string(path, axis, "purpose", f"fixture_axes[{index}]")
        require_string_array(path, axis, "required_conditions", f"fixture_axes[{index}]")
    ensure_unique(path, ids, "axis_id")
    missing = REQUIRED_AXES - set(ids)
    if missing:
        fail(path, "missing required fixture axes: " + ", ".join(sorted(missing)))
    return set(ids)


def validate_components(path: Path, value: object, axis_ids: set[str]) -> None:
    if not isinstance(value, list):
        fail(path, "components must be an array")
    ids: list[str] = []
    surfaces: set[str] = set()
    for index, component_value in enumerate(value, start=1):
        component = require_object(path, component_value, f"components[{index}]")
        required = {
            "component_id",
            "surface",
            "name",
            "purpose",
            "required_states",
            "required_commands",
            "required_fixture_axes",
            "accessibility_contract",
            "authority_boundary",
        }
        reject_extra(path, component, required, f"components[{index}]")
        require_keys(path, component, required, f"components[{index}]")
        component_id = require_string(
            path, component, "component_id", f"components[{index}]"
        )
        if not COMPONENT_ID.fullmatch(component_id):
            fail(path, f"invalid component_id: {component_id}")
        ids.append(component_id)
        surface = require_string(path, component, "surface", f"components[{index}]")
        surfaces.add(surface)
        require_string(path, component, "name", f"components[{index}]")
        require_string(path, component, "purpose", f"components[{index}]")
        require_string_array(path, component, "required_states", f"components[{index}]")
        require_string_array(path, component, "required_commands", f"components[{index}]")
        component_axes = set(
            require_string_array(
                path, component, "required_fixture_axes", f"components[{index}]"
            )
        )
        unknown_axes = component_axes - axis_ids
        if unknown_axes:
            fail(
                path,
                f"{component_id} references unknown fixture axes: "
                + ", ".join(sorted(unknown_axes)),
            )
        missing_axes = REQUIRED_AXES - component_axes
        if missing_axes:
            fail(
                path,
                f"{component_id} is missing required fixture axes: "
                + ", ".join(sorted(missing_axes)),
            )
        require_string_array(
            path, component, "accessibility_contract", f"components[{index}]"
        )
        boundary = require_string(
            path, component, "authority_boundary", f"components[{index}]"
        )
        if "authority" not in boundary.lower():
            fail(path, f"{component_id}.authority_boundary must discuss authority")
    ensure_unique(path, ids, "component_id")
    missing_surfaces = REQUIRED_SURFACES - surfaces
    if missing_surfaces:
        fail(path, "missing required component surfaces: " + ", ".join(sorted(missing_surfaces)))


def validate_inventory(path: Path, payload: object) -> None:
    inventory = require_object(path, payload, "inventory")
    required = {
        "schema_version",
        "inventory_id",
        "status",
        "updated",
        "claim_status",
        "token_groups",
        "components",
        "fixture_axes",
        "unsupported",
    }
    reject_extra(path, inventory, required, "inventory")
    require_keys(path, inventory, required, "inventory")
    if inventory.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    inventory_id = require_string(path, inventory, "inventory_id", "inventory")
    if not INVENTORY_ID.fullmatch(inventory_id):
        fail(path, "inventory_id has invalid format")
    if require_string(path, inventory, "status", "inventory") != "no_claim_planning_inventory":
        fail(path, "status must remain no_claim_planning_inventory")
    require_string(path, inventory, "updated", "inventory")
    claim_status = require_string(path, inventory, "claim_status", "inventory")
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    unsupported = require_string_array(path, inventory, "unsupported", "inventory")
    for phrase in REQUIRED_CLAIM_PHRASES:
        if not any(phrase in item for item in unsupported):
            fail(path, f"unsupported must mention: {phrase}")

    validate_token_groups(path, inventory.get("token_groups"))
    axis_ids = validate_axes(path, inventory.get("fixture_axes"))
    validate_components(path, inventory.get("components"), axis_ids)


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_INVENTORY]
    try:
        for path in paths:
            validate_inventory(path, load_json(path))
    except ValidationError as error:
        print(f"UI component fixture validation failed: {error}", file=sys.stderr)
        return 1
    print(f"UI component fixture validation passed: {len(paths)} inventory file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
