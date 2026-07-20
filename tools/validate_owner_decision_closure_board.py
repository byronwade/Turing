#!/usr/bin/env python3
"""Validate the no-claim owner-decision closure board against canonical gates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "docs/project-buildout/23-owner-decision-closure-board.md"
PRE_BUILD = ROOT / "docs/blueprint-v1/machine/pre-build-readiness.json"
LEDGER = ROOT / "docs/project-buildout/machine/build-information-readiness-ledger.json"

EXPECTED_GATES = {
    "PB-002",
    "PB-003",
    "PB-004",
    "PB-005",
    "PB-008",
    "PB-009",
    "PB-011",
    "PB-012",
    "PB-013",
    "PB-014",
    "PB-015",
    "PB-016",
    "PB-017",
    "PB-018",
    "PB-019",
    "PB-020",
}

EXPECTED_ACTION_LINKS = {
    "PB-002": "adr-0009-source-strategy-closure-preparation-2026-07.md",
    "PB-008": "fresh-host-toolchain-reproduction-closure-preparation-2026-07.md",
    "PB-009": "fresh-host-toolchain-reproduction-closure-preparation-2026-07.md",
    "PB-011": "ipc-transport-and-authority-closure-preparation-2026-07.md",
    "PB-012": "sandbox-probe-execution-and-containment-closure-preparation-2026-07.md",
    "PB-013": "benchmark-evidence-and-claim-closure-preparation-2026-07.md",
    "PB-003": "native-ui-and-accessibility-closure-preparation-2026-07.md",
    "PB-004": "native-ui-and-accessibility-closure-preparation-2026-07.md",
    "PB-005": "native-ui-and-accessibility-closure-preparation-2026-07.md",
    "PB-014": "native-ui-and-accessibility-closure-preparation-2026-07.md",
    "PB-015": "native-ui-and-accessibility-closure-preparation-2026-07.md",
    "PB-016": "profile-session-execution-and-data-safety-closure-preparation-2026-07.md",
    "PB-017": "package-update-execution-and-release-safety-closure-preparation-2026-07.md",
    "PB-018": "incident-response-execution-and-disclosure-closure-preparation-2026-07.md",
    "PB-019": "backup-ownership-execution-and-two-person-control-closure-preparation-2026-07.md",
    "PB-020": "build-readiness-closure-and-owner-decision-preparation-2026-07.md",
}

ROW_RE = re.compile(r"^\|\s*(?P<gate>[^|]+?)\s*\|(?P<body>.*)\|\s*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not BOARD.is_file():
        fail(errors, f"missing board: {BOARD.relative_to(ROOT)}")
    if not PRE_BUILD.is_file():
        fail(errors, f"missing pre-build registry: {PRE_BUILD.relative_to(ROOT)}")
    if not LEDGER.is_file():
        fail(errors, f"missing information ledger: {LEDGER.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"validation failed: {error}", file=sys.stderr)
        return 1

    text = BOARD.read_text(encoding="utf-8")
    lowered = text.lower()
    required_phrases = [
        "no-claim owner-decision handoff",
        "every row is currently unresolved",
        "does not create a second status registry",
        "a template, passing validator, research report, or specified task manifest is not an owner decision",
        "required decision record",
        "does not authorize proposed tasks",
        "all-information-ready-for-building",
    ]
    for phrase in required_phrases:
        if phrase not in lowered:
            fail(errors, f"board is missing required no-claim phrase: {phrase}")

    rows: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = ROW_RE.match(line)
        if not match:
            continue
        gate_text = match.group("gate")
        gates = set(re.findall(r"PB-\d{3}", gate_text.upper()))
        if not gates:
            continue
        body_cells = [cell.strip() for cell in match.group("body").split("|")]
        if len(body_cells) != 3 or any(not cell for cell in body_cells):
            fail(errors, f"line {line_number}: decision row must have three non-empty decision cells")
        for gate in gates:
            if gate in rows:
                fail(errors, f"duplicate decision row for {gate}")
            rows[gate] = line

    actual_gates = set(rows)
    missing = sorted(EXPECTED_GATES - actual_gates)
    extra = sorted(actual_gates - EXPECTED_GATES)
    if missing:
        fail(errors, f"missing canonical gate rows: {', '.join(missing)}")
    if extra:
        fail(errors, f"unexpected gate rows: {', '.join(extra)}")

    for gate, line in rows.items():
        cells = [cell.strip().lower() for cell in ROW_RE.match(line).group("body").split("|")]
        if len(cells) != 3:
            continue
        if not any(term in cells[0] for term in ("owner", "accept", "name", "select", "reject", "approve")):
            fail(errors, f"{gate}: owner decision cell does not state a decision/owner requirement")
        if "evidence" not in cells[1] and "proof" not in cells[1] and "review" not in cells[1]:
            fail(errors, f"{gate}: minimum evidence cell lacks evidence/proof/review wording")
        if not any(term in cells[2] for term in ("action", "execute", "complete", "keep", "prepare", "resolve", "shape", "use")):
            fail(errors, f"{gate}: current next-action cell lacks an actionable verb")
        expected_link = EXPECTED_ACTION_LINKS[gate]
        if expected_link not in cells[2]:
            fail(errors, f"{gate}: current next-action cell must link to {expected_link}")

    try:
        pre_build = json.loads(PRE_BUILD.read_text(encoding="utf-8"))
        prebuild_ids = {item.get("id") for item in pre_build.get("items", [])}
        if not EXPECTED_GATES.issubset(prebuild_ids):
            fail(errors, "canonical gate set is not covered by pre-build-readiness.json")
    except (OSError, json.JSONDecodeError) as error:
        fail(errors, f"cannot read pre-build registry: {error}")

    try:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        info_ids = {item.get("id") for item in ledger.get("information_classes", [])}
        required_info = {
            "INFO-SOURCE-STRATEGY",
            "INFO-FRESH-HOST",
            "INFO-IPC",
            "INFO-SANDBOX",
            "INFO-BENCHMARK",
            "INFO-NATIVE-SHELL",
            "INFO-PROFILE-SESSION",
            "INFO-PACKAGE-UPDATE",
            "INFO-INCIDENT-RESPONSE",
            "INFO-BACKUP-OWNERSHIP",
        }
        if not required_info.issubset(info_ids):
            fail(errors, "owner-decision information classes are missing from build-information-readiness-ledger.json")
    except (OSError, json.JSONDecodeError) as error:
        fail(errors, f"cannot read information ledger: {error}")

    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        path = (BOARD.parent / target).resolve()
        if not path.is_file():
            fail(errors, f"board link does not resolve: {target}")

    if errors:
        for error in errors:
            print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print(f"owner-decision closure board validation passed: {len(rows)} canonical gate rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
