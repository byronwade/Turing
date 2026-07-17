#!/usr/bin/env python3
"""Validate the executable M0 build foundation without third-party packages."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_PATH = ROOT / "docs/blueprint-v1/machine/workspace-components.json"
TOOLCHAINS_PATH = ROOT / "docs/blueprint-v1/machine/toolchains.json"
IPC_SCHEMA_PATH = ROOT / "schemas/ipc/control-plane.json"
PROCESS_CAPABILITIES_PATH = ROOT / "docs/blueprint-v1/machine/process-capabilities.json"
TASK_PATH = ROOT / "docs/agent-execution/machine/tasks/TASK-000001.json"

REQUIRED_FILES = [
    ROOT / "Cargo.toml",
    ROOT / "Cargo.lock",
    ROOT / "rust-toolchain.toml",
    ROOT / "rustfmt.toml",
    ROOT / "clippy.toml",
    ROOT / "apps/turing-shell/Cargo.toml",
    ROOT / "apps/turing-shell/src/main.rs",
    ROOT / "crates/turing-build-info/Cargo.toml",
    ROOT / "crates/turing-build-info/src/lib.rs",
    ROOT / "crates/turing-ipc/Cargo.toml",
    ROOT / "crates/turing-ipc/src/lib.rs",
    ROOT / "crates/turing-ipc/src/envelope.rs",
    ROOT / "crates/turing-ipc/src/generated.rs",
    ROOT / "crates/turing-ipc/src/queue.rs",
    ROOT / "crates/turing-ipc/src/sequence.rs",
    ROOT / "crates/turing-kernel/Cargo.toml",
    ROOT / "crates/turing-kernel/src/lib.rs",
    ROOT / "crates/turing-types/Cargo.toml",
    ROOT / "crates/turing-types/src/lib.rs",
    ROOT / "crates/turing-ui-model/Cargo.toml",
    ROOT / "crates/turing-ui-model/src/lib.rs",
    ROOT / "tools/xtask/Cargo.toml",
    ROOT / "tools/xtask/src/main.rs",
    ROOT / "tools/bootstrap.sh",
    ROOT / "tools/doctor.sh",
    ROOT / "tools/check.sh",
    ROOT / "tools/generate_ipc.py",
    IPC_SCHEMA_PATH,
    PROCESS_CAPABILITIES_PATH,
    TASK_PATH,
    COMPONENTS_PATH,
    TOOLCHAINS_PATH,
    ROOT / "security/dependencies.json",
    ROOT / "security/unsafe-code.json",
    ROOT / "security/native-code.json",
    ROOT / "security/generated-code.json",
    ROOT / "security/provenance.json",
]

FORBIDDEN_SOURCE_PATTERNS = [
    re.compile(r"\bunsafe\s*\{"),
    re.compile(r"\bunsafe\s+fn\b"),
    re.compile(r"\bunsafe\s+impl\b"),
    re.compile(r'\bextern\s+"[A-Za-z0-9_-]+"'),
]


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}")


def load_toml(path: Path) -> dict[str, object]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid TOML: {error}")


def check_required_files() -> None:
    missing = [path.relative_to(ROOT) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("missing M0 build files: " + ", ".join(map(str, missing)))


def check_toolchain() -> None:
    toolchain = load_toml(ROOT / "rust-toolchain.toml")
    configured = toolchain.get("toolchain")
    if not isinstance(configured, dict):
        fail("rust-toolchain.toml must contain [toolchain]")
    if configured.get("channel") != "1.97.1":
        fail("M0 Rust channel must be pinned to 1.97.1")
    components = configured.get("components")
    if components != ["clippy", "rustfmt", "rust-src"]:
        fail("M0 Rust components must be clippy, rustfmt, and rust-src")

    manifest = load_json(TOOLCHAINS_PATH)
    if not isinstance(manifest, dict) or manifest.get("status") != "ready_for_contained_m0":
        fail("toolchains.json must declare ready_for_contained_m0")
    rust = manifest.get("rust")
    if not isinstance(rust, dict) or rust.get("channel") != "1.97.1":
        fail("toolchains.json must match rust-toolchain.toml")


def manifest_internal_dependencies(path: Path, package_set: set[str]) -> set[str]:
    manifest = load_toml(path)
    dependencies = manifest.get("dependencies", {})
    if not isinstance(dependencies, dict):
        fail(f"{path.relative_to(ROOT)}: dependencies must be a table")
    return set(dependencies) & package_set


def check_workspace() -> None:
    workspace = load_toml(ROOT / "Cargo.toml")
    table = workspace.get("workspace")
    if not isinstance(table, dict):
        fail("root Cargo.toml must contain [workspace]")
    members = table.get("members")
    if not isinstance(members, list):
        fail("workspace members must be an array")

    components = load_json(COMPONENTS_PATH)
    if not isinstance(components, dict) or not isinstance(components.get("components"), list):
        fail("workspace-components.json must contain a components array")

    records = components["components"]
    packages = [record.get("package") for record in records]
    if len(packages) != len(set(packages)):
        fail("workspace component package names must be unique")

    paths = [record.get("path") for record in records]
    if set(paths) != set(members):
        fail(
            "workspace members and workspace-components paths differ: "
            f"members={sorted(members)}, components={sorted(paths)}"
        )

    package_set = {package for package in packages if isinstance(package, str)}
    graph: dict[str, list[str]] = {}
    for record in records:
        package = record.get("package")
        path = record.get("path")
        dependencies = record.get("dependencies")
        if not isinstance(package, str) or not isinstance(path, str):
            fail("component package and path must be strings")
        if not isinstance(dependencies, list) or not all(
            isinstance(dependency, str) for dependency in dependencies
        ):
            fail(f"{package}: dependencies must be a string array")
        unknown = set(dependencies) - package_set
        if unknown:
            fail(f"{package}: unknown internal dependencies: {sorted(unknown)}")
        manifest_path = ROOT / path / "Cargo.toml"
        if not manifest_path.is_file():
            fail(f"{package}: missing Cargo.toml at {path}")
        actual = manifest_internal_dependencies(manifest_path, package_set)
        if actual != set(dependencies):
            fail(
                f"{package}: manifest dependencies {sorted(actual)} differ from "
                f"workspace-components {sorted(dependencies)}"
            )
        graph[package] = dependencies

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(package: str) -> None:
        if package in visiting:
            fail(f"workspace dependency cycle includes {package}")
        if package in visited:
            return
        visiting.add(package)
        for dependency in graph[package]:
            visit(dependency)
        visiting.remove(package)
        visited.add(package)

    for package in graph:
        visit(package)


def check_ipc_schema() -> None:
    schema = load_json(IPC_SCHEMA_PATH)
    registry = load_json(PROCESS_CAPABILITIES_PATH)
    if not isinstance(schema, dict) or schema.get("schema_version") != 1:
        fail("IPC control-plane schema must be schema version 1")
    for field in ("capabilities", "roles", "queue_classes", "messages"):
        if not isinstance(schema.get(field), list) or not schema[field]:
            fail(f"IPC control-plane {field} must be a non-empty array")
    if not isinstance(registry, dict) or registry.get("schema_version") != 2:
        fail("generated process-capabilities registry must be schema version 2")
    if registry.get("generated_from") != "schemas/ipc/control-plane.json":
        fail("process-capabilities registry must identify its canonical schema")
    if registry.get("protocol_version") != schema.get("protocol_version"):
        fail("process-capabilities protocol version must match IPC schema")
    schema_roles = {item.get("name") for item in schema["roles"] if isinstance(item, dict)}
    registry_roles = registry.get("roles")
    if not isinstance(registry_roles, dict) or set(registry_roles) != schema_roles:
        fail("generated process-capabilities roles differ from IPC schema")


def check_ledgers() -> None:
    dependencies = load_json(ROOT / "security/dependencies.json")
    unsafe = load_json(ROOT / "security/unsafe-code.json")
    native = load_json(ROOT / "security/native-code.json")
    generated = load_json(ROOT / "security/generated-code.json")
    provenance = load_json(ROOT / "security/provenance.json")

    for name, payload in [
        ("dependencies", dependencies),
        ("unsafe-code", unsafe),
        ("native-code", native),
        ("generated-code", generated),
        ("provenance", provenance),
    ]:
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            fail(f"security/{name}.json must be schema version 1")

    if dependencies.get("external_runtime_dependencies") != []:
        fail("M0 skeleton must not add external runtime dependencies")
    if unsafe.get("entries") != []:
        fail("M0 skeleton unsafe-code ledger must remain empty")
    if native.get("entries") != []:
        fail("M0 skeleton native-code ledger must remain empty")

    entries = generated.get("entries")
    if not isinstance(entries, list) or len(entries) != 1:
        fail("generated-code ledger must contain the single IPC generator entry")
    entry = entries[0]
    if not isinstance(entry, dict) or entry.get("id") != "GEN-IPC-001":
        fail("generated-code ledger must identify GEN-IPC-001")
    expected_outputs = {
        "crates/turing-ipc/src/generated.rs",
        "docs/blueprint-v1/machine/process-capabilities.json",
    }
    if set(entry.get("outputs", [])) != expected_outputs:
        fail("GEN-IPC-001 output list is incomplete")



def check_execution_task() -> None:
    task = load_json(TASK_PATH)
    if not isinstance(task, dict) or task.get("schema_version") != 1:
        fail("TASK-000001 must be schema version 1")
    if task.get("id") != "TASK-000001" or task.get("status") != "review_pending":
        fail("TASK-000001 must remain review_pending until independent review")
    if task.get("owner") == task.get("independent_reviewer"):
        fail("TASK-000001 owner and independent reviewer must differ")
    if task.get("requirements") != ["REQ-SEC-003", "REQ-PERF-004"]:
        fail("TASK-000001 must map exactly to REQ-SEC-003 and REQ-PERF-004")
    for field in ("allowed_paths", "preconditions", "acceptance_criteria", "negative_tests"):
        if not isinstance(task.get(field), list) or not task[field]:
            fail(f"TASK-000001 {field} must be a non-empty array")
    rollback = task.get("rollback")
    if not isinstance(rollback, dict) or not rollback.get("strategy"):
        fail("TASK-000001 must define rollback")


def check_source_policy() -> None:
    for directory in ["apps", "crates", "prototype", "tools/xtask"]:
        for path in (ROOT / directory).rglob("*.rs"):
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_SOURCE_PATTERNS:
                if pattern.search(text):
                    fail(
                        f"{path.relative_to(ROOT)} contains unledgered unsafe/native syntax: "
                        f"{pattern.pattern}"
                    )


def main() -> int:
    try:
        check_required_files()
        check_toolchain()
        check_workspace()
        check_ipc_schema()
        check_ledgers()
        check_execution_task()
        check_source_policy()
    except ValueError as error:
        print(f"build foundation validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "build foundation validation passed: "
        "8 workspace members, Rust 1.97.1, generated IPC schema, "
        "0 external runtime dependencies, 0 unsafe entries, 0 native-code entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
