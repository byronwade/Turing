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
    re.compile(r"\bextern\s+\"[A-Za-z0-9_-]+\""),
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

    package_set = set(packages)
    graph: dict[str, list[str]] = {}
    for record in records:
        package = record.get("package")
        path = record.get("path")
        dependencies = record.get("dependencies")
        if not isinstance(package, str) or not isinstance(path, str):
            fail("component package and path must be strings")
        if not isinstance(dependencies, list):
            fail(f"{package}: dependencies must be an array")
        unknown = set(dependencies) - package_set
        if unknown:
            fail(f"{package}: unknown internal dependencies: {sorted(unknown)}")
        if not (ROOT / path / "Cargo.toml").is_file():
            fail(f"{package}: missing Cargo.toml at {path}")
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
    if generated.get("entries") != []:
        fail("M0 skeleton generated-code ledger must remain empty")


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
        check_ledgers()
        check_source_policy()
    except ValueError as error:
        print(f"build foundation validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "build foundation validation passed: "
        "8 workspace members, Rust 1.97.1, 0 external runtime dependencies, "
        "0 unsafe entries, 0 native-code entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
