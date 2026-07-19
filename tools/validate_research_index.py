#!/usr/bin/env python3
"""Validate that durable research artifacts are indexed and index links resolve."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research"
INDEX = RESEARCH / "README.md"
MARKDOWN_LINK = re.compile(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)")


def fail(message: str) -> None:
    print(f"research-index validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not INDEX.is_file():
        fail("docs/research/README.md is missing")

    index_text = INDEX.read_text(encoding="utf-8")
    indexed_paths: set[Path] = set()
    stale_links: list[str] = []

    for match in MARKDOWN_LINK.finditer(index_text):
        href = match.group(1)
        target = (RESEARCH / href).resolve()
        if target.parent != RESEARCH:
            continue
        if not target.is_file():
            stale_links.append(href)
            continue
        indexed_paths.add(target)

    if stale_links:
        fail(f"stale research-index links: {', '.join(sorted(stale_links))}")

    durable_files = {
        path.resolve()
        for path in RESEARCH.glob("*.md")
        if path.name != "README.md"
    }
    missing = sorted(path.name for path in durable_files - indexed_paths)
    if missing:
        fail(f"unindexed durable research files: {', '.join(missing)}")

    print(
        "research-index validation passed: "
        f"{len(durable_files)} durable research files, "
        f"{len(indexed_paths)} indexed local Markdown links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
