#!/usr/bin/env python3
"""Validate that machine registries are consistent with each other.

The existing validators each check one registry against its schema and against
specific named assertions. Nothing checked the registry layer as a whole. This
validator closes that gap with two global invariants:

1. Every `REQ-*`, `WP-*`, `PB-*`, `RQ-*`, and `RISK-*` identifier referenced by
   any registry under `docs/*/machine/` exists in the registry that owns that
   identifier space. A dangling identifier means a record points at a
   requirement, work package, gate, research question, or risk that does not
   exist.

2. Every repository path referenced by any registry exists on disk. URLs are
   stripped before extraction, because a URL tail such as
   `https://turing.invalid/schemas/foo-v1.json` or a Chromium docs link is not
   a repository path and must not be treated as one.

It also asserts that the active and deferred research-question sets stay
disjoint, since several documents compute a denominator from their sum.

This validator is dependency-free, offline, and deterministic, so it is safe in
the aggregate check path.

Usage:
    python3 -B tools/validate_registry_cross_references.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Each owning registry stores its records under a different key, so the key is
# named explicitly rather than guessed. A wrong key must fail loudly instead of
# silently yielding an empty set, which would make every reference look valid.
OWNERS = {
    "REQ": ("docs/blueprint-v1/machine/requirements.json", "requirements"),
    "WP": ("docs/blueprint-v1/machine/backlog.json", "items"),
    "PB": ("docs/blueprint-v1/machine/pre-build-readiness.json", "items"),
    "RISK": ("docs/blueprint-v1/machine/risks.json", "risks"),
}

COVERAGE = "docs/blueprint-v1/machine/research-question-coverage.json"

# Risk identifiers are `R-###` in this repository, not `RISK-###`. An earlier
# revision used the wrong prefix, which made the risk invariant a silent no-op
# while still printing a reassuring RISK count in the pass line.
ID_PATTERNS = {
    "REQ": re.compile(r"\bREQ-[A-Z0-9]+-\d+\b"),
    "WP": re.compile(r"\bWP-\d{3}\b"),
    "PB": re.compile(r"\bPB-\d{3}\b"),
    "RQ": re.compile(r"\bRQ-\d{2}\b"),
    "RISK": re.compile(r"\bR-\d{3}\b"),
}

URL = re.compile(r"https?://\S+")
REPO_PATH = re.compile(
    r"\b(?:docs|tools|crates|apps|schemas|security|benchmarks|prototype)"
    r"/[A-Za-z0-9_.\-/]+\.(?:md|json|py|rs|toml|ps1|sh)\b"
)

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def main() -> int:
    registries: dict[str, object] = {}
    for path in sorted(ROOT.glob("docs/*/machine/**/*.json")):
        key = str(path.relative_to(ROOT)).replace("\\", "/")
        try:
            registries[key] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            fail(f"{key}: unparseable JSON: {error}")

    if not registries:
        print("registry cross-reference validation failed: no registries found", file=sys.stderr)
        return 1

    # Authoritative identifier sets.
    valid: dict[str, set[str]] = {}
    for kind, (rel, key) in OWNERS.items():
        data = registries.get(rel)
        if not isinstance(data, dict):
            fail(f"missing owning registry for {kind}: {rel}")
            valid[kind] = set()
            continue
        items = data.get(key) or []
        valid[kind] = {
            item.get("id") for item in items if isinstance(item, dict) and item.get("id")
        }
        if not valid[kind]:
            fail(f"{rel}: no {kind} identifiers found under '{key}'")

    coverage = registries.get(COVERAGE)
    if not isinstance(coverage, dict):
        fail(f"missing research-question coverage registry: {COVERAGE}")
        active, deferred = set(), set()
    else:
        active = set(coverage.get("active_question_ids", []))
        deferred = {
            q.get("question_id")
            for q in coverage.get("deferred_questions", [])
            if isinstance(q, dict) and q.get("question_id")
        }
    valid["RQ"] = active | deferred
    # An empty authoritative set makes every reference look valid, so a missing
    # or renamed key must fail loudly rather than silently passing.
    if not active:
        fail(f"{COVERAGE}: no research questions found under 'active_question_ids'")
    if not deferred:
        fail(f"{COVERAGE}: no research questions found under 'deferred_questions'")

    both = active & deferred
    if both:
        fail(
            "research questions appear in both active_question_ids and "
            f"deferred_questions: {sorted(both)}"
        )

    # Dangling identifier references.
    dangling: dict[str, dict[str, set[str]]] = {k: defaultdict(set) for k in ID_PATTERNS}
    missing_paths: dict[str, set[str]] = defaultdict(set)

    for key, data in registries.items():
        blob = json.dumps(data)
        for kind, pattern in ID_PATTERNS.items():
            if not valid.get(kind):
                continue
            for ident in set(pattern.findall(blob)):
                if ident not in valid[kind]:
                    dangling[kind][ident].add(key)
        for ref in set(REPO_PATH.findall(URL.sub(" ", blob))):
            if not (ROOT / ref).exists():
                missing_paths[ref].add(key)

    for kind, entries in dangling.items():
        for ident, sources in sorted(entries.items()):
            fail(
                f"{ident} is referenced by {len(sources)} registry file(s) but is not "
                f"defined in the owning {kind} registry: {', '.join(sorted(sources)[:3])}"
            )

    for ref, sources in sorted(missing_paths.items()):
        fail(
            f"registry references a repository path that does not exist: {ref} "
            f"(from {', '.join(sorted(sources)[:3])})"
        )

    if failures:
        print("registry cross-reference validation failed:", file=sys.stderr)
        for message in failures:
            print(f"  {message}", file=sys.stderr)
        return 1

    counts = " ".join(f"{k}={len(v)}" for k, v in sorted(valid.items()))
    print(
        "registry cross-reference validation passed: "
        f"{len(registries)} registries, no dangling identifiers ({counts}), "
        "active/deferred research questions disjoint, all referenced repository paths exist"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
