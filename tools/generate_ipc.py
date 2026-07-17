#!/usr/bin/env python3
"""Generate Turing control-plane Rust and process-capability documentation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/ipc/control-plane.json"
RUST_OUTPUT = ROOT / "crates/turing-ipc/src/generated.rs"
REGISTRY_OUTPUT = ROOT / "docs/blueprint-v1/machine/process-capabilities.json"
NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def fail(message: str) -> None:
    raise ValueError(message)


def rust_name(value: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in value.split("_"))


def load_schema() -> dict[str, object]:
    try:
        payload = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{SCHEMA.relative_to(ROOT)}: invalid JSON: {error}")
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        fail("control-plane schema must be an object with schema_version 1")
    return payload


def require_list(payload: dict[str, object], name: str) -> list[dict[str, object]]:
    value = payload.get(name)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        fail(f"{name} must be an array of objects")
    return value


def validate_named_ids(items: list[dict[str, object]], kind: str, maximum: int) -> None:
    ids: list[int] = []
    names: list[str] = []
    for item in items:
        identifier = item.get("id")
        name = item.get("name")
        if not isinstance(identifier, int) or not 0 <= identifier <= maximum:
            fail(f"{kind} id must be an integer from 0 through {maximum}: {item}")
        if not isinstance(name, str) or NAME_RE.fullmatch(name) is None:
            fail(f"{kind} name must be lower snake case: {item}")
        ids.append(identifier)
        names.append(name)
    if len(ids) != len(set(ids)):
        fail(f"duplicate {kind} ids")
    if len(names) != len(set(names)):
        fail(f"duplicate {kind} names")


def validate(payload: dict[str, object]) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    capabilities = require_list(payload, "capabilities")
    roles = require_list(payload, "roles")
    queues = require_list(payload, "queue_classes")
    messages = require_list(payload, "messages")
    validate_named_ids(capabilities, "capability", 127)
    validate_named_ids(roles, "role", 255)
    validate_named_ids(queues, "queue class", 255)
    validate_named_ids(messages, "message", 65535)

    capability_names = {item["name"] for item in capabilities}
    role_names = {item["name"] for item in roles}
    for role in roles:
        for field in ("may_launch", "capabilities", "forbidden"):
            value = role.get(field)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                fail(f"role {role.get('name')}: {field} must be a string array")
        unknown_launch = set(role["may_launch"]) - role_names
        if unknown_launch:
            fail(f"role {role['name']}: unknown launch roles {sorted(unknown_launch)}")
        unknown_capabilities = set(role["capabilities"]) - capability_names
        if unknown_capabilities:
            fail(
                f"role {role['name']}: unknown capabilities {sorted(unknown_capabilities)}"
            )

    for queue in queues:
        for field in ("maximum_items", "maximum_queued_bytes"):
            value = queue.get(field)
            if not isinstance(value, int) or value <= 0:
                fail(f"queue {queue.get('name')}: {field} must be positive")

    for message in messages:
        maximum = message.get("maximum_encoded_bytes")
        scope = message.get("document_scope")
        required = message.get("required_capability")
        routes = message.get("allowed_routes")
        if not isinstance(maximum, int) or not 0 < maximum <= 65536:
            fail(f"message {message.get('name')}: invalid maximum_encoded_bytes")
        if scope not in {"required", "optional", "forbidden"}:
            fail(f"message {message.get('name')}: invalid document_scope")
        if required is not None and required not in capability_names:
            fail(f"message {message.get('name')}: unknown required capability {required}")
        if not isinstance(routes, list) or not routes:
            fail(f"message {message.get('name')}: allowed_routes must be non-empty")
        normalized: set[tuple[str, str]] = set()
        for route in routes:
            if (
                not isinstance(route, list)
                or len(route) != 2
                or not all(isinstance(item, str) for item in route)
            ):
                fail(f"message {message.get('name')}: invalid route {route}")
            sender, receiver = route
            if sender not in role_names or receiver not in role_names:
                fail(f"message {message.get('name')}: route contains unknown role {route}")
            normalized.add((sender, receiver))
        if len(normalized) != len(routes):
            fail(f"message {message.get('name')}: duplicate allowed route")

    maximum_processes = payload.get("maximum_registered_processes")
    protocol_version = payload.get("protocol_version")
    if not isinstance(maximum_processes, int) or maximum_processes <= 0:
        fail("maximum_registered_processes must be positive")
    if not isinstance(protocol_version, int) or protocol_version <= 0:
        fail("protocol_version must be positive")

    return capabilities, roles, queues, messages


def rust_match_arms(items: list[dict[str, object]], field: str, value) -> list[str]:
    return [f"            Self::{rust_name(str(item['name']))} => {value(item[field])}," for item in items]


def generate_rust(
    payload: dict[str, object],
    capabilities: list[dict[str, object]],
    roles: list[dict[str, object]],
    queues: list[dict[str, object]],
    messages: list[dict[str, object]],
) -> str:
    lines: list[str] = [
        "// @generated by tools/generate_ipc.py from schemas/ipc/control-plane.json.",
        "// Do not edit this file directly.",
        "",
        f"pub const PROTOCOL_VERSION: u16 = {payload['protocol_version']};",
        f"pub const MAX_REGISTERED_PROCESSES: usize = {payload['maximum_registered_processes']};",
        "",
        "#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]",
        "#[repr(u8)]",
        "pub enum Capability {",
    ]
    for item in capabilities:
        lines.append(f"    {rust_name(str(item['name']))} = {item['id']},")
    lines.extend(["}", "", "impl Capability {", "    #[must_use]", "    pub const fn as_str(self) -> &'static str {", "        match self {"])
    lines.extend(rust_match_arms(capabilities, "name", lambda value: f'"{value}"'))
    lines.extend(["        }", "    }", "}", ""])

    lines.extend([
        "#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]",
        "#[repr(u8)]",
        "pub enum ProcessRole {",
    ])
    for item in roles:
        lines.append(f"    {rust_name(str(item['name']))} = {item['id']},")
    lines.extend(["}", "", "impl ProcessRole {"])
    lines.extend(["    #[must_use]", "    pub const fn as_str(self) -> &'static str {", "        match self {"])
    lines.extend(rust_match_arms(roles, "name", lambda value: f'"{value}"'))
    lines.extend(["        }", "    }", ""])
    lines.extend(["    #[must_use]", "    pub const fn default_capability_bits(self) -> u128 {", "        match self {"])
    for role in roles:
        bits = 0
        role_caps = set(role["capabilities"])
        for capability in capabilities:
            if capability["name"] in role_caps:
                bits |= 1 << int(capability["id"])
        lines.append(f"            Self::{rust_name(str(role['name']))} => {bits}_u128,")
    lines.extend(["        }", "    }", ""])
    lines.extend([
        "    #[must_use]",
        "    pub const fn may_launch(self, child: Self) -> bool {",
        "        matches!(",
        "            (self, child),",
    ])
    launch_pairs = [
        (str(role["name"]), str(child))
        for role in roles
        for child in role["may_launch"]
    ]
    if launch_pairs:
        for index, (parent, child) in enumerate(launch_pairs):
            prefix = "            " if index == 0 else "                | "
            lines.append(
                f"{prefix}(Self::{rust_name(parent)}, Self::{rust_name(child)})"
            )
    else:
        lines.append("            _ if false")
    lines.extend(["        )", "    }", "}", ""])

    lines.extend([
        "#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]",
        "pub enum DocumentScope {",
        "    Required,",
        "    Optional,",
        "    Forbidden,",
        "}",
        "",
        "#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]",
        "#[repr(u8)]",
        "pub enum QueueClass {",
    ])
    for item in queues:
        lines.append(f"    {rust_name(str(item['name']))} = {item['id']},")
    lines.extend(["}", "", "impl QueueClass {"])
    lines.extend(["    #[must_use]", "    pub const fn maximum_items(self) -> usize {", "        match self {"])
    lines.extend(rust_match_arms(queues, "maximum_items", str))
    lines.extend(["        }", "    }", ""])
    lines.extend(["    #[must_use]", "    pub const fn maximum_queued_bytes(self) -> usize {", "        match self {"])
    lines.extend(rust_match_arms(queues, "maximum_queued_bytes", str))
    lines.extend(["        }", "    }", "}", ""])

    lines.extend([
        "#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]",
        "#[repr(u16)]",
        "pub enum MessageKind {",
    ])
    for item in messages:
        lines.append(f"    {rust_name(str(item['name']))} = {item['id']},")
    lines.extend(["}", "", "impl MessageKind {"])
    lines.extend(["    #[must_use]", "    pub const fn as_str(self) -> &'static str {", "        match self {"])
    lines.extend(rust_match_arms(messages, "name", lambda value: f'"{value}"'))
    lines.extend(["        }", "    }", ""])
    lines.extend(["    #[must_use]", "    pub const fn maximum_encoded_bytes(self) -> usize {", "        match self {"])
    lines.extend(rust_match_arms(messages, "maximum_encoded_bytes", str))
    lines.extend(["        }", "    }", ""])
    lines.extend(["    #[must_use]", "    pub const fn document_scope(self) -> DocumentScope {", "        match self {"])
    for item in messages:
        lines.append(
            f"            Self::{rust_name(str(item['name']))} => DocumentScope::{rust_name(str(item['document_scope']))},"
        )
    lines.extend(["        }", "    }", ""])
    lines.extend(["    #[must_use]", "    pub const fn required_capability(self) -> Option<Capability> {", "        match self {"])
    for item in messages:
        required = item["required_capability"]
        rendered = "None" if required is None else f"Some(Capability::{rust_name(str(required))})"
        lines.append(f"            Self::{rust_name(str(item['name']))} => {rendered},")
    lines.extend(["        }", "    }", ""])
    lines.extend([
        "    #[must_use]",
        "    pub const fn allows_route(self, sender: ProcessRole, receiver: ProcessRole) -> bool {",
        "        match self {",
    ])
    for item in messages:
        lines.append(f"            Self::{rust_name(str(item['name']))} => matches!(")
        lines.append("                (sender, receiver),")
        for index, route in enumerate(item["allowed_routes"]):
            sender, receiver = route
            prefix = "                " if index == 0 else "                    | "
            lines.append(
                f"{prefix}(ProcessRole::{rust_name(sender)}, ProcessRole::{rust_name(receiver)})"
            )
        lines.append("            ),")
    lines.extend(["        }", "    }", "}", ""])
    return "\n".join(lines)


def generate_registry(payload: dict[str, object], roles: list[dict[str, object]]) -> str:
    registry = {
        "schema_version": 2,
        "generated_from": "schemas/ipc/control-plane.json",
        "protocol_version": payload["protocol_version"],
        "default": "deny",
        "roles": {
            role["name"]: {
                "role_id": role["id"],
                "may_launch": role["may_launch"],
                "capabilities": role["capabilities"],
                "forbidden": role["forbidden"],
            }
            for role in roles
        },
    }
    return json.dumps(registry, indent=2) + "\n"


def write_or_check(path: Path, expected: str, check: bool) -> None:
    if check:
        try:
            actual = path.read_text(encoding="utf-8")
        except OSError as error:
            fail(f"{path.relative_to(ROOT)}: unable to read generated output: {error}")
        if actual != expected:
            fail(
                f"{path.relative_to(ROOT)} is stale; run python3 -B tools/generate_ipc.py"
            )
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    try:
        payload = load_schema()
        capabilities, roles, queues, messages = validate(payload)
        write_or_check(
            RUST_OUTPUT,
            generate_rust(payload, capabilities, roles, queues, messages),
            arguments.check,
        )
        write_or_check(
            REGISTRY_OUTPUT,
            generate_registry(payload, roles),
            arguments.check,
        )
    except ValueError as error:
        print(f"IPC generation failed: {error}", file=sys.stderr)
        return 1
    action = "validated" if arguments.check else "generated"
    print(f"IPC schema {action}: {len(roles)} roles, {len(capabilities)} capabilities, {len(messages)} messages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
