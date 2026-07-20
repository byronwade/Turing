#!/usr/bin/env python3
"""Validate the no-claim Chrome-class capability traceability map."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "research" / "chrome-class-capability-traceability-map-2026-07.md"

REQUIRED_SECTIONS = (
    "## Inputs Inspected",
    "## Traceability Rules",
    "## Performance objective and claim ladder",
    "## Capability Trace",
    "## Stop/Resume Procedure",
    "## Unsupported Conclusions",
    "## Drift Triggers",
    "## Validation",
)
REQUIRED_LEVELS = ("`L0`", "`L1`", "`L2`", "`L3`")
REQUIRED_DOMAINS = (
    "Browser shell, windows, tabs, profiles",
    "Web engine HTML, DOM, CSS, layout",
    "JavaScript, WebAssembly, garbage collection",
    "Navigation, networking, cookies, storage",
    "Media, PDF, printing, downloads",
    "Accessibility and internationalization",
    "DevTools, headless, WebDriver BiDi",
    "Extensions, enterprise policy, accounts",
    "Performance, memory, energy, 30-tab behavior",
    "Security, privacy, sandboxing, updates",
    "AI and agent authority, observations",
    "Build, compile, clean-host reproducibility",
)
REQUIRED_FIELDS = (
    "Existing source of truth",
    "Current blockers and handoffs",
    "Next proof before any claim",
    "Claim still prohibited",
)
REQUIRED_BOUNDARIES = (
    "turing is chrome-class",
    "chrome-equivalent",
    "usable general-purpose browser",
    "all information needed for building is complete",
    "no readiness promotion",
)


def fail(message: str) -> None:
    raise SystemExit(f"Chrome-class traceability validation failed: {message}")


def local_links(text: str) -> list[str]:
    links: list[str] = []
    for match in re.finditer(r"\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        parsed = urlparse(target)
        if not target or parsed.scheme or target.startswith("//"):
            continue
        links.append(unquote(target))
    return links


def main() -> int:
    try:
        text = MAP.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read map: {exc}")

    if not text.startswith("# Chrome-Class Capability Traceability Map"):
        fail("map title is missing")
    if "Status: no-claim traceability map; no readiness promotion" not in text:
        fail("no-claim status boundary is missing")
    if not re.search(r"Last updated: 2026-07-\d{2}", text):
        fail("Last updated metadata is missing")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(f"required section is missing: {section}")
    for level in REQUIRED_LEVELS:
        if level not in text:
            fail(f"performance evidence level is missing: {level}")
    for domain in REQUIRED_DOMAINS:
        if domain not in text:
            fail(f"capability domain is missing: {domain}")

    trace_start = text.index("## Capability Trace")
    trace_end = text.index("## Stop/Resume Procedure")
    trace = text[trace_start:trace_end]
    header = "| Capability domain | Existing source of truth | Current blockers and handoffs | Next proof before any claim | Claim still prohibited |"
    if header not in trace:
        fail("capability trace table header is missing")
    rows = [line for line in trace.splitlines() if line.startswith("|") and "---" not in line]
    if len(rows) != len(REQUIRED_DOMAINS) + 1:
        fail(f"capability trace must contain {len(REQUIRED_DOMAINS)} data rows")
    for field in REQUIRED_FIELDS:
        if field not in header:
            fail(f"capability trace field is missing: {field}")
    for row in rows[1:]:
        if row.count("|") < 6:
            fail("capability trace row has fewer than five columns")
        if not any(token in row for token in ("PB-", "WP-", "REQ-", "RQ-")):
            fail("capability trace row lacks requirement, gate, work-package, or research references")
        if "claim" not in row.lower():
            fail("capability trace row lacks a claim boundary")

    lowered = text.lower()
    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in lowered:
            fail(f"unsupported boundary is missing: {boundary}")
    if "This traceability map has no standalone validator" in text:
        fail("map still declares that it has no standalone validator")

    for target in local_links(text):
        path = (MAP.parent / target).resolve()
        if not path.is_file() and not path.is_dir():
            fail(f"local reference does not exist: {target}")

    print(
        "Chrome-class capability traceability validation passed: "
        f"{len(REQUIRED_DOMAINS)} domains, {len(REQUIRED_LEVELS)} evidence levels, no-claim"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
