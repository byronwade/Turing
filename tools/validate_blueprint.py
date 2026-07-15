#!/usr/bin/env python3
"""Validate the Turing repository without third-party Python packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLUEPRINT = DOCS / "blueprint-v1"
MACHINE = BLUEPRINT / "machine"

CHAPTERS = [
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
    (19, "initial-backlog"),
    (20, "definition-of-done"),
    (21, "product-requirements"),
    (22, "research-program"),
]

REQUIRED_DOCS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    DOCS / "README.md",
    DOCS / "start-here.md",
    DOCS / "documentation-policy.md",
    DOCS / "repository-map.md",
    DOCS / "contributing.md",
    DOCS / "security.md",
    DOCS / "prototype.md",
    DOCS / "research-log.md",
    BLUEPRINT / "README.md",
    *[BLUEPRINT / f"{number:02d}-{slug}.md" for number, slug in CHAPTERS],
    ROOT / "prototype" / "Cargo.toml",
    ROOT / "prototype" / "src" / "main.rs",
    ROOT / "tools" / "check_documentation_change.py",
    ROOT / ".github" / "workflows" / "repository-validation.yml",
]

REQUIRED_MACHINE_FILES = [
    MACHINE / "agent-action.schema.json",
    MACHINE / "backlog.json",
    MACHINE / "benchmark-manifest.schema.json",
    MACHINE / "process-capabilities.json",
    MACHINE / "requirements.json",
    MACHINE / "risks.json",
]

ALLOWED_MARKDOWN_OUTSIDE_DOCS = {
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / ".github" / "pull_request_template.md",
}

FORBIDDEN_LEGACY_PATHS = [
    ROOT / "START_HERE.md",
    ROOT / "blueprint-v1",
    ROOT / "prototype" / "README.md",
    ROOT / "bootstrap",
    ROOT / ".github" / "workflows" / "blueprint-v1-validation.yml",
    ROOT / ".github" / "workflows" / "bootstrap.yml",
    ROOT / ".github" / "workflows" / "bootstrap-repair.yml",
    ROOT / ".github" / "workflows" / "expand-bootstrap.yml",
]

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
STABLE_ID = re.compile(
    r"\b(?:REQ-[A-Z0-9-]+|R-\d{3}|ADR-\d{4}|WP-\d{3}|[A-Z]+-GATE-\d+)\b"
)


def fail(message: str) -> None:
    raise ValueError(message)


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{relative(path)}: invalid JSON: {error}")


def check_required_files() -> None:
    missing = [
        relative(path)
        for path in [*REQUIRED_DOCS, *REQUIRED_MACHINE_FILES]
        if not path.is_file()
    ]
    if missing:
        fail("missing required files: " + ", ".join(map(str, missing)))

    stale = [relative(path) for path in FORBIDDEN_LEGACY_PATHS if path.exists()]
    if stale:
        fail("forbidden legacy paths remain: " + ", ".join(map(str, stale)))


def check_document_locations() -> None:
    outside = []
    for path in ROOT.rglob("*.md"):
        if path.is_relative_to(DOCS):
            continue
        if path in ALLOWED_MARKDOWN_OUTSIDE_DOCS:
            continue
        outside.append(relative(path))

    if outside:
        fail(
            "canonical Markdown must live under docs/; unexpected files: "
            + ", ".join(map(str, sorted(outside)))
        )

    for path in DOCS.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix == ".md":
            continue
        if path.is_relative_to(MACHINE) and path.suffix == ".json":
            continue
        fail(f"unsupported documentation file type: {relative(path)}")


def check_json_registries() -> None:
    requirements = load_json(MACHINE / "requirements.json")
    risks = load_json(MACHINE / "risks.json")
    backlog = load_json(MACHINE / "backlog.json")
    load_json(MACHINE / "benchmark-manifest.schema.json")
    load_json(MACHINE / "agent-action.schema.json")
    load_json(MACHINE / "process-capabilities.json")

    if not isinstance(requirements, dict) or not isinstance(
        requirements.get("requirements"), list
    ):
        fail("requirements.json must contain a requirements array")
    if not isinstance(risks, dict) or not isinstance(risks.get("risks"), list):
        fail("risks.json must contain a risks array")
    if not isinstance(backlog, dict) or not isinstance(backlog.get("items"), list):
        fail("backlog.json must contain an items array")

    requirement_ids = [item.get("id") for item in requirements["requirements"]]
    risk_ids = [item.get("id") for item in risks["risks"]]
    work_ids = [item.get("id") for item in backlog["items"]]

    if len(requirement_ids) != 46:
        fail(f"expected 46 requirements, found {len(requirement_ids)}")
    if len(risk_ids) != 40:
        fail(f"expected 40 risks, found {len(risk_ids)}")
    if len(work_ids) != 18:
        fail(f"expected 18 work packages, found {len(work_ids)}")

    if len(requirement_ids) != len(set(requirement_ids)):
        fail("duplicate requirement IDs")
    if len(risk_ids) != len(set(risk_ids)):
        fail("duplicate risk IDs")
    if len(work_ids) != len(set(work_ids)):
        fail("duplicate work-package IDs")

    if requirement_ids != sorted(requirement_ids):
        fail("requirements must be sorted by stable ID")
    if risk_ids != [f"R-{index:03d}" for index in range(1, 41)]:
        fail("risk IDs must be contiguous R-001 through R-040")
    if work_ids != [f"WP-{index:03d}" for index in range(1, 19)]:
        fail("work-package IDs must be contiguous WP-001 through WP-018")

    requirement_set = set(requirement_ids)
    work_set = set(work_ids)
    for item in backlog["items"]:
        unknown_dependencies = set(item.get("depends_on", [])) - work_set
        if unknown_dependencies:
            fail(
                f"{item.get('id')}: unknown work-package dependencies: "
                + ", ".join(sorted(unknown_dependencies))
            )
        unknown_requirements = set(item.get("requirements", [])) - requirement_set
        if unknown_requirements:
            fail(
                f"{item.get('id')}: unknown requirements: "
                + ", ".join(sorted(unknown_requirements))
            )


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None

    target = unquote(target.split("#", 1)[0])
    if not target:
        return None

    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"{relative(source)} links outside repository: {target}")
    return resolved


def check_markdown() -> tuple[int, int]:
    markdown_files = sorted(ROOT.rglob("*.md"))
    links_checked = 0
    identifiers: set[str] = set()
    referenced_docs: set[Path] = set()

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if "\r" in text:
            fail(f"{relative(path)} contains CR line endings")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                fail(f"{relative(path)}:{line_number} has trailing whitespace")

        identifiers.update(STABLE_ID.findall(text))

        for raw_target in MARKDOWN_LINK.findall(text):
            resolved = local_target(path, raw_target)
            if resolved is None:
                continue
            if not resolved.exists():
                fail(f"{relative(path)} has broken link: {raw_target}")
            if resolved.is_dir():
                fail(
                    f"{relative(path)} links to a directory instead of an indexed file: "
                    f"{raw_target}"
                )
            if resolved.suffix == ".md" and resolved.is_relative_to(DOCS):
                referenced_docs.add(resolved)
            links_checked += 1

    if len(markdown_files) < 35:
        fail(f"expected at least 35 Markdown documents, found {len(markdown_files)}")
    if len(identifiers) < 80:
        fail(f"expected at least 80 stable identifiers in prose, found {len(identifiers)}")

    canonical_docs = set(DOCS.rglob("*.md"))
    unindexed = sorted(canonical_docs - {DOCS / "README.md"} - referenced_docs)
    if unindexed:
        fail(
            "canonical documents without an inbound Markdown link: "
            + ", ".join(map(str, (relative(path) for path in unindexed)))
        )

    return len(markdown_files), links_checked


def check_policy_markers() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    required_phrases = [
        "Canonical project documentation lives in `docs/`",
        "Every change must update every affected document",
        "docs/repository-map.md",
        "python3 tools/validate_blueprint.py",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in agents]
    if missing:
        fail("AGENTS.md is missing mandatory policy markers: " + ", ".join(missing))

    root_contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    root_security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    if "docs/contributing.md" not in root_contributing:
        fail("root CONTRIBUTING.md must point to docs/contributing.md")
    if "docs/security.md" not in root_security:
        fail("root SECURITY.md must point to docs/security.md")


def check_source_hygiene() -> None:
    forbidden_suffixes = {".pem", ".key", ".p12", ".pfx"}
    forbidden_names = {".env", ".env.local", "id_rsa", "id_ed25519"}

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in forbidden_suffixes or path.name in forbidden_names:
            fail(f"forbidden secret-like file: {relative(path)}")


def main() -> int:
    try:
        check_required_files()
        check_document_locations()
        check_json_registries()
        markdown_count, links_checked = check_markdown()
        check_policy_markers()
        check_source_hygiene()
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "validation passed: "
        f"{markdown_count} Markdown files, {links_checked} relative links, "
        "46 requirements, 40 risks, 18 work packages, 6 machine-readable registries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
