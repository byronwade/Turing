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
CONTINUITY_PATTERNS = {
    "question/scope": re.compile(
        r"(^#{1,3} .*?(question|scope|purpose|finding|problem|objective|decision|what )|"
        r"\b(question|scope|purpose|finding|objective|decision)\s*:)",
        re.IGNORECASE | re.MULTILINE,
    ),
    "evidence/method": re.compile(
        r"\b(evidence|method|source|retrieval|observation|baseline|manifest|validation|"
        r"primary sources|current evidence|source-backed)\b",
        re.IGNORECASE,
    ),
    "disposition/next step": re.compile(
        r"\b(conclusion|disposition|next (action|proof|step)|unresolved|remaining|blocked|"
        r"revisit|limitation|follow-up|handoff|current status|missing|unsupported|does not)\b",
        re.IGNORECASE,
    ),
    "claim boundary": re.compile(
        r"\b(no-claim|does not|not a |not yet|remains|unsupported|blocked|unproven|"
        r"not an implementation)\b",
        re.IGNORECASE,
    ),
}


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

    missing_metadata = []
    for path in sorted(durable_files):
        text = path.read_text(encoding="utf-8")
        missing_fields = [
            field for field in ("Status", "Owner")
            if not re.search(rf"(?m)^{field}:\s*\S", text)
        ]
        if missing_fields:
            missing_metadata.append(f"{path.name} ({', '.join(missing_fields)})")
    if missing_metadata:
        fail("durable research files missing required metadata: " + "; ".join(missing_metadata))

    missing_continuity = []
    for path in sorted(durable_files):
        text = path.read_text(encoding="utf-8")
        missing_fields = [
            field for field, pattern in CONTINUITY_PATTERNS.items() if not pattern.search(text)
        ]
        if missing_fields:
            missing_continuity.append(f"{path.name} ({', '.join(missing_fields)})")
    if missing_continuity:
        fail(
            "durable research files missing continuity fields: "
            + "; ".join(missing_continuity)
        )

    active_quality_gaps = []
    for path in sorted(durable_files):
        text = path.read_text(encoding="utf-8")
        status = re.search(r"(?m)^Status:\s*(.+)$", text)
        if not status or not re.search(r"\bactive\b", status.group(1), re.IGNORECASE):
            continue
        quality_checks = {
            "observations": re.search(r"\bobserv", text, re.IGNORECASE),
            "inference-or-candidate": re.search(
                r"\b(infer|candidate|recommend|proposal|hypothesis)",
                text,
                re.IGNORECASE,
            ),
            "unresolved-next-work": re.search(
                r"\b(next|remaining|unresolved|missing|unsupported|current disposition)",
                text,
                re.IGNORECASE,
            ),
        }
        missing_quality = [name for name, present in quality_checks.items() if not present]
        if missing_quality:
            active_quality_gaps.append(f"{path.name} ({', '.join(missing_quality)})")
        if not re.search(r"(?m)^(Research|Packet|Map|Audit) date:\s*\d{4}-\d{2}-\d{2}", text):
            active_quality_gaps.append(f"{path.name} (dated-source-context)")
        if not re.search(
            r"https?://|\b(version|revision|commit|stable locator)\b|\[.*source records?\]",
            text,
            re.IGNORECASE,
        ):
            active_quality_gaps.append(f"{path.name} (stable-source-locator)")
    if active_quality_gaps:
        fail(
            "active research files must separate observations, candidate inferences or "
            "recommendations, unresolved next work, and dated stable source context: "
            + "; ".join(active_quality_gaps)
        )

    print(
        "research-index validation passed: "
        f"{len(durable_files)} durable research files, "
        f"{len(indexed_paths)} indexed local Markdown links, "
        f"{len(CONTINUITY_PATTERNS)} continuity fields per packet, "
        "active-packet observation/inference/next-work/source-context checks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
