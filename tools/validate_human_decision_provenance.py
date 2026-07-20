#!/usr/bin/env python3
"""Validate that no machine record silently asserts a human decision.

An agent cannot produce an owner approval, only draft one. On 2026-07-20 an
agent nevertheless wrote `"accepted_by": "@byronwade"` with a `decision_date`
into `professional-exceptions.json`, on the strength of an instruction given in
a chat session. Every validator passed: the field was schema-valid, the name was
real, and nothing in the repository distinguished an agent-drafted approval from
an owner-countersigned one. An independent review caught it; no automated check
could have.

This validator encodes the convention the repository already follows everywhere
else. A field that names who decided, approved, reviewed, or signed something
must be one of:

  * null -- the state of every no-claim review template;
  * a role placeholder that says a real name is still required, the state of the
    proposed task manifests ("program reviewer (name required before ready)");
  * an `agent:`-prefixed identity, which claims machine provenance rather than
    human judgement, as the TASK-000011 evidence bundles do;
  * an explicit non-applicability marker such as "not-applicable-no-claim";
  * a real identity ACCOMPANIED by provenance marking it owner-countersigned.

The last case is the one that matters. A populated human-decision field is only
legitimate when the record also carries an explicit countersignature marker, so
the distinction between drafted and approved cannot be lost by omission.

JSON Schema files are skipped for field *definitions* (where the value is a type
object), since those declare shape rather than assert a decision.

This validator is dependency-free, offline, and deterministic.

Usage:
    python3 -B tools/validate_human_decision_provenance.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Fields that assert who decided, approved, reviewed, or signed something.
DECISION_FIELDS = {
    "accepted_by",
    "approved_by",
    "reviewed_by",
    "signed_by",
    "countersigned_by",
    "owner_reviewer",
    "independent_reviewer",
    "reviewer",
}

# Fields that assert *when* a human decision happened. A populated date implies a
# completed decision just as strongly as a name does.
DECISION_DATE_FIELDS = {
    "decision_date",
    "acceptance_date",
    "approval_date",
    "countersignature_date",
}

# Markers anywhere in the containing record that make a populated identity
# legitimate, by stating the approval is real and owner-supplied.
COUNTERSIGNATURE_MARKERS = (
    "countersigned",
    "countersignature",
    "owner_countersigned",
)

# Value shapes that do not assert a human decision.
PLACEHOLDER = re.compile(
    r"(name required|required before|not[- ]applicable|placeholder|tbd|to be named|"
    r"pending|none|n/a|role only)",
    re.IGNORECASE,
)
AGENT_IDENTITY = re.compile(r"^agent:", re.IGNORECASE)
# A bare role word ("program", "security") names a scope, not a person.
ROLE_ONLY = re.compile(r"^[a-z][a-z0-9 \-/]*$")

failures: list[str] = []


def record_has_countersignature(record: dict) -> bool:
    blob = json.dumps(record).lower()
    return any(marker in blob for marker in COUNTERSIGNATURE_MARKERS)


def check_record(record: dict, rel: str, is_schema: bool) -> None:
    for key, value in record.items():
        if key not in DECISION_FIELDS and key not in DECISION_DATE_FIELDS:
            continue
        # Schema type declarations describe shape, not a decision.
        if is_schema and isinstance(value, dict):
            continue
        if value is None:
            continue
        if not isinstance(value, str) or not value.strip():
            continue
        if PLACEHOLDER.search(value) or AGENT_IDENTITY.match(value):
            continue
        if key in DECISION_FIELDS and ROLE_ONLY.match(value.strip()):
            continue
        if record_has_countersignature(record):
            continue
        failures.append(
            f"{rel}: {key}={value!r} asserts a human decision, but the record carries "
            "no countersignature marker. An agent may draft such a record; only an "
            "owner may complete it. Either null the field and mark the record as "
            "agent-drafted, or add explicit countersignature provenance."
        )


def walk(node: object, rel: str, is_schema: bool) -> None:
    if isinstance(node, dict):
        check_record(node, rel, is_schema)
        for value in node.values():
            walk(value, rel, is_schema)
    elif isinstance(node, list):
        for value in node:
            walk(value, rel, is_schema)


def main() -> int:
    scanned = 0
    for path in sorted(ROOT.glob("docs/*/machine/**/*.json")):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(f"{rel}: unparseable JSON: {error}")
            continue
        scanned += 1
        walk(data, rel, rel.endswith(".schema.json"))

    if failures:
        print("human-decision provenance validation failed:", file=sys.stderr)
        for message in failures:
            print(f"  {message}", file=sys.stderr)
        return 1

    print(
        "human-decision provenance validation passed: "
        f"{scanned} registries, no record asserts a human decision without "
        "countersignature provenance"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
