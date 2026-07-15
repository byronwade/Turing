#!/usr/bin/env python3
"""Enforce minimum same-change documentation rules for a Git diff."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class Change:
    status: str
    paths: tuple[PurePosixPath, ...]

    @property
    def primary_path(self) -> PurePosixPath:
        return self.paths[-1]


ROOT_DISCOVERY_DOCS = {
    PurePosixPath("README.md"),
    PurePosixPath("AGENTS.md"),
    PurePosixPath("CONTRIBUTING.md"),
    PurePosixPath("SECURITY.md"),
}


def fail(message: str) -> None:
    raise ValueError(message)


def git_diff(base: str, head: str) -> list[Change]:
    command = [
        "git",
        "diff",
        "--name-status",
        "--find-renames",
        "--find-copies",
        base,
        head,
        "--",
    ]
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or "git diff failed")

    changes: list[Change] = []
    for raw_line in result.stdout.splitlines():
        if not raw_line.strip():
            continue
        fields = raw_line.split("\t")
        status = fields[0]
        paths = tuple(PurePosixPath(field) for field in fields[1:])
        if not paths:
            fail(f"unrecognized git diff line: {raw_line}")
        changes.append(Change(status=status, paths=paths))
    return changes


def is_canonical_markdown(path: PurePosixPath) -> bool:
    return len(path.parts) >= 2 and path.parts[0] == "docs" and path.suffix == ".md"


def is_documentation_or_workflow_text(path: PurePosixPath) -> bool:
    if is_canonical_markdown(path) or path in ROOT_DISCOVERY_DOCS:
        return True
    if path.parts[:1] == (".github",) and path.suffix == ".md":
        return True
    if (
        path.parts[:3] == ("docs", "blueprint-v1", "machine")
        and path.suffix == ".json"
    ):
        return True
    return False


def changed_paths(changes: list[Change]) -> set[PurePosixPath]:
    return {path for change in changes for path in change.paths}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: check_documentation_change.py <base-revision> <head-revision>",
            file=sys.stderr,
        )
        return 2

    try:
        changes = git_diff(argv[1], argv[2])
        if not changes:
            print("documentation change check passed: no changed paths")
            return 0

        paths = changed_paths(changes)
        canonical_markdown_changes = {
            path for path in paths if is_canonical_markdown(path)
        }
        non_documentation_changes = {
            path for path in paths if not is_documentation_or_workflow_text(path)
        }

        if non_documentation_changes and not canonical_markdown_changes:
            fail(
                "non-documentation changes require at least one affected Markdown "
                "document under docs/: "
                + ", ".join(map(str, sorted(non_documentation_changes)))
            )

        structural = [
            change
            for change in changes
            if change.status.startswith(("A", "D", "R", "C"))
        ]
        if structural and PurePosixPath("docs/repository-map.md") not in paths:
            fail(
                "added, deleted, renamed, or copied paths require "
                "docs/repository-map.md"
            )

        documentation_topology = [
            change
            for change in structural
            if any(is_canonical_markdown(path) for path in change.paths)
        ]
        if documentation_topology and PurePosixPath("docs/README.md") not in paths:
            fail(
                "documentation additions, removals, renames, or copies require "
                "docs/README.md"
            )

        prototype_changes = {
            path
            for path in paths
            if path.parts[:1] == ("prototype",)
        }
        if prototype_changes and PurePosixPath("docs/prototype.md") not in paths:
            fail("prototype changes require docs/prototype.md")

        print(
            "documentation change check passed: "
            f"{len(changes)} changed entries, "
            f"{len(canonical_markdown_changes)} canonical Markdown updates"
        )
        return 0
    except ValueError as error:
        print(f"documentation change check failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
