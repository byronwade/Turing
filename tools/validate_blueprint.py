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

DOC_SLUGS = [
    "charter-and-principles",
    "capability-parity",
    "language-and-dependency-strategy",
    "system-architecture",
    "web-engine",
    "javascript-runtime",
    "network-storage-media",
    "security-and-sandbox",
    "performance-memory",
    "ai-agent-platform",
    "product-ui-devtools",
    "testing-compatibility",
    "build-release-operations",
    "roadmap-work-breakdown",
    "risk-register",
    "governance-contributing",
    "architecture-decisions",
    "source-bibliography",
    "initial-backlog",
    "definition-of-done",
    "product-requirements",
    "research-program",
]

REQUIRED_DOCS = [
    ROOT / "README.md",
    ROOT / "START_HERE.md",
    BLUEPRINT / "README.md",
    *[
        BLUEPRINT / f"{number:02d}-{slug}.md"
        for number, slug in enumerate(DOC_SLUGS, start=1)
    ],
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "prototype" / "README.md",
    ROOT / "prototype" / "Cargo.toml",
    ROOT / "prototype" / "src" / "main.rs",
]

MACHINE_FILES = [
    BLUEPRINT / "machine" / "requirements.json",
    BLUEPRINT / "machine" / "risks.json",
    BLUEPRINT / "machine" / "benchmark-manifest.schema.json",
    BLUEPRINT / "machine" / "agent-action.schema.json",
    BLUEPRINT / "machine" / "process-capabilities.json",
]

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
STABLE_ID = re.compile(r"\b(?:REQ-[A-Z0-9-]+|R-\d{3}|ADR-\d{4}|[A-Z]+-GATE-\d+)\b")
TEMPORARY_PATHS = [
    ROOT / "bootstrap",
    ROOT / "RESUME_MARKER.md",
    ROOT / ".github" / "workflows" / "bootstrap.yml",
    ROOT / ".github" / "workflows" / "bootstrap-repair.yml",
    ROOT / ".github" / "workflows" / "expand-bootstrap.yml",
]


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}")


def check_required_files() -> None:
    required = [*REQUIRED_DOCS, *MACHINE_FILES]
    missing = [path.relative_to(ROOT) for path in required if not path.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(map(str, missing)))
    leftovers = [path.relative_to(ROOT) for path in TEMPORARY_PATHS if path.exists()]
    if leftovers:
        fail("temporary publication artifacts remain: " + ", ".join(map(str, leftovers)))


def check_json_registries() -> None:
    requirements = load_json(MACHINE_FILES[0])
    risks = load_json(MACHINE_FILES[1])
    for path in MACHINE_FILES[2:]:
        load_json(path)

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


def valid_markdown_trailing_space(line: str) -> bool:
    """Allow no trailing spaces or the exact two-space Markdown hard break."""
    if line.endswith("\t"):
        return False
    stripped = line.rstrip(" ")
    trailing_spaces = len(line) - len(stripped)
    return trailing_spaces in (0, 2)


def check_markdown() -> tuple[int, int]:
    markdown_files = sorted(ROOT.rglob("*.md"))
    links_checked = 0
    identifiers: set[str] = set()

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if "\r" in text:
            fail(f"{path.relative_to(ROOT)} contains CR line endings")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not valid_markdown_trailing_space(line):
                fail(f"{path.relative_to(ROOT)}:{line_number} has invalid trailing whitespace")
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

    if len(markdown_files) < 28:
        fail(f"expected at least 28 Markdown documents, found {len(markdown_files)}")
    if len(identifiers) < 60:
        fail(f"expected at least 60 stable identifiers in prose, found {len(identifiers)}")
    return len(markdown_files), links_checked


def check_source_hygiene() -> None:
    forbidden_suffixes = {".pem", ".key", ".p12", ".pfx"}
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            fail(f"forbidden secret-like file: {path.relative_to(ROOT)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "not yet a usable or security-reviewed browser" not in readme:
        fail("root README must retain the research-build safety warning")


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
