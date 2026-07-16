#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"{path}: expected anchor not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_validator() -> None:
    path = Path("tools/validate_blueprint.py")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'r"\\b(?:REQ-[A-Z0-9-]+|R-\\d{3}|ADR-\\d{4}|WP-\\d{3}|RQ-\\d{2}|"',
        'r"\\b(?:REQ-[A-Z0-9-]+|R-\\d{3}|ADR-\\d{4}|WP-\\d{3}|RQ-\\d{2}|OP-\\d{3}|"',
        1,
    )

    if "def check_professional_controls()" not in text:
        anchor = "\n\ndef check_market_opportunities() -> None:"
        function = '''

def check_professional_controls() -> None:
    owners = load_json(MACHINE / "professional-owners.json")
    rules = load_json(MACHINE / "professional-review-rules.json")
    if not isinstance(owners, dict) or not isinstance(owners.get("owners"), list):
        fail("professional-owners.json must contain an owners array")
    if not isinstance(rules, dict) or not isinstance(rules.get("rules"), list):
        fail("professional-review-rules.json must contain a rules array")

    owner_scopes = [item.get("scope") for item in owners["owners"]]
    if len(owner_scopes) != len(set(owner_scopes)):
        fail("professional owner scopes must be unique")
    required_owner_scopes = {"product", "market-strategy"}
    missing_owner_scopes = required_owner_scopes - set(owner_scopes)
    if missing_owner_scopes:
        fail(
            "missing professional owner scopes: "
            + ", ".join(sorted(missing_owner_scopes))
        )

    allowed_reviewers = set(owner_scopes) | {"owner"}
    rule_ids = [item.get("id") for item in rules["rules"]]
    if len(rule_ids) != len(set(rule_ids)):
        fail("professional review rule IDs must be unique")
    if "REV-MARKET" not in rule_ids:
        fail("professional review rules must include REV-MARKET")
    for rule in rules["rules"]:
        reviewers = rule.get("reviewers")
        if not isinstance(reviewers, list) or not reviewers:
            fail(f"{rule.get('id')}: reviewers must be a non-empty array")
        unknown = set(reviewers) - allowed_reviewers
        if unknown:
            fail(
                f"{rule.get('id')}: unknown reviewer scopes: "
                + ", ".join(sorted(unknown))
            )

    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    if "\n\n| [Market Strategy and Differentiation]" in docs_index:
        fail("docs/README.md separates market strategy from the books table")
    market_research_row = (
        "| [Browser market gap and differentiation research — July 2026]"
    )
    if market_research_row not in docs_index:
        fail("docs/README.md active research table is missing the market-gap report")

    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    if "\n\n- [Market Strategy and Differentiation]" in blueprint_index:
        fail("Blueprint index separates market strategy from the engineering-book list")
    if "../research/browser-market-gap-2026-07.md" not in blueprint_index:
        fail("Blueprint current reports are missing the market-gap report")
'''
        if anchor not in text:
            raise RuntimeError("validator professional-control insertion anchor not found")
        text = text.replace(anchor, function + anchor, 1)

    if "        check_professional_controls()\n" not in text:
        text = text.replace(
            "        check_json_registries()\n",
            "        check_json_registries()\n        check_professional_controls()\n",
            1,
        )
    path.write_text(text, encoding="utf-8")


def patch_governance() -> None:
    path = Path("docs/blueprint-v1/16-governance-contributing.md")
    text = path.read_text(encoding="utf-8")
    addition = (
        "- **Product owner:** user needs, workflow coherence, product requirements, "
        "usability evidence, migration, and support scope.\n"
        "- **Market strategy owner:** competitive method, opportunity evidence, "
        "positioning, contrary evidence, and promotion or rejection of `OP-*` proposals."
    )
    if addition not in text:
        anchor = "- **Program lead:** scope, milestones, release label, staffing, public claims."
        if anchor not in text:
            raise RuntimeError("governance role anchor not found")
        text = text.replace(anchor, anchor + "\n" + addition, 1)
    path.write_text(text, encoding="utf-8")


def patch_research_log() -> None:
    path = Path("docs/research-log.md")
    text = path.read_text(encoding="utf-8")
    heading = "## 2026-07-16 — Market strategy consistency and validator hardening"
    if heading not in text:
        text = (
            text.rstrip()
            + "\n\n"
            + heading
            + "\n\nAfter the market-strategy merge, a repository-wide audit corrected "
            + "canonical table placement, added explicit product ownership, normalized "
            + "release-review scope naming, and extended validation to `OP-*` IDs, "
            + "reviewer-to-owner resolution, and market index invariants. No opportunity "
            + "was promoted and no implementation or support status changed.\n"
        )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_validator()
    patch_governance()
    patch_research_log()


if __name__ == "__main__":
    main()
