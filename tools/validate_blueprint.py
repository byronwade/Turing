#!/usr/bin/env python3
"""Validate the Turing Blueprint v1 without third-party Python packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "blueprint-v1"

REQUIRED_DOCS = [
    BLUEPRINT / "README.md",
    *[BLUEPRINT / f"{number:02d}-{slug}.md" for number, slug in [
        (1, "charter-and-principles"),
        (2, "capability-parity"),
        (3, "language-and-dependency-strategy"),
        (4, "system-architecture"),
        (5, "web-engine"),
        (6, "javascript-runtime"),
        (7, "network-storage-media"),
        (8, "security-and-sandbox"),
        (9, "performance-memory"),
        (10, "ai-agent-platform"),
        (11, "product-ui-devtools"),
        (12, "testing-compatibility"),
        (13, "build-release-operations"),
        (14, "roadmap-work-breakdown"),
        (15, "risk-register"),
        (16, "governance-contributing"),
        (17, "architecture-decisions"),
        (18, "source-bibliography"),
    ]],
    ROOT / "prototype" / "Cargo.toml",
    ROOT / "prototype" / "src" / "main.rs",
]

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
STABLE_ID = re.compile(r"\b(?:REQ-[A-Z0-9-]+|R-\d{3}|ADR-\d{4}|[A-Z]+-GATE-\d+)\b")


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}")


def check_required_files() -> None:
    missing = [path.relative_to(ROOT) for path in REQUIRED_DOCS if not path.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(map(str, missing)))


def check_json_registries() -> None:
    requirements_path = BLUEPRINT / "machine" / "requirements.json"
    risks_path = BLUEPRINT / "machine" / "risks.json"
    requirements = load_json(requirements_path)
    risks = load_json(risks_path)
    load_json(BLUEPRINT / "machine" / "benchmark-manifest.schema.json")
    load_json(BLUEPRINT / "machine" / "agent-action.schema.json")
    load_json(BLUEPRINT / "machine" / "process-capabilities.json")

    if not isinstance(requirements, dict) or not isinstance(requirements.get("requirements"), list):
        fail("requirements.json must contain a requirements array")
    if not isinstance(risks, dict) or not isinstance(risks.get("risks"), list):
        fail("risks.json must contain a risks array")

    requirement_ids = [item.get("id") for item in requirements["requirements"]]
    risk_ids = [item.get("id") for item in risks["risks"]]
    if len(requirement_ids) != 46:
        fail(f"expected 46 requirements, found {len(requirement_ids)}")
    if len(risk_ids) != 40:
        fail(f"expected 40 risks, found {len(risk_ids)}")
    if len(requirement_ids) != len(set(requirement_ids)):
        fail("duplicate requirement IDs")
    if len(risk_ids) != len(set(risk_ids)):
        fail("duplicate risk IDs")
    if requirement_ids != sorted(requirement_ids):
        fail("requirements must be sorted by stable ID")
    if risk_ids != [f"R-{index:03d}" for index in range(1, 41)]:
        fail("risk IDs must be contiguous R-001 through R-040")


def check_markdown() -> tuple[int, int]:
    markdown_files = sorted(ROOT.rglob("*.md"))
    links_checked = 0
    identifiers: set[str] = set()

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if "\r" in text:
            fail(f"{path.relative_to(ROOT)} contains CR line endings")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                fail(f"{path.relative_to(ROOT)}:{line_number} has trailing whitespace")
        identifiers.update(STABLE_ID.findall(text))

        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"{path.relative_to(ROOT)} links outside repository: {target}")
            if not resolved.exists():
                fail(f"{path.relative_to(ROOT)} has broken link: {target}")
            links_checked += 1

    if len(markdown_files) < 19:
        fail(f"expected at least 19 Markdown documents, found {len(markdown_files)}")
    if len(identifiers) < 60:
        fail(f"expected at least 60 stable identifiers in prose, found {len(identifiers)}")
    return len(markdown_files), links_checked


def check_source_hygiene() -> None:
    forbidden_suffixes = {".pem", ".key", ".p12", ".pfx"}
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            fail(f"forbidden secret-like file: {path.relative_to(ROOT)}")


def main() -> int:
    try:
        check_required_files()
        check_json_registries()
        markdown_count, links_checked = check_markdown()
        check_source_hygiene()
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "validation passed: "
        f"{markdown_count} Markdown files, {links_checked} relative links, "
        "46 requirements, 40 risks, 5 machine-readable registries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
