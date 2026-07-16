#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def patch_docs_index() -> None:
    path = Path("docs/README.md")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "| [Professional Project Buildout and Operating Handbook](project-buildout/README.md) | Phase gates, ownership, review, traceability, repository, coding, schemas, cross-cutting review, operations, source strategy, product, and sustainability |\n\n| [Market Strategy and Differentiation](market-strategy/README.md)",
        "| [Professional Project Buildout and Operating Handbook](project-buildout/README.md) | Phase gates, ownership, review, traceability, repository, coding, schemas, cross-cutting review, operations, source strategy, product, and sustainability |\n| [Market Strategy and Differentiation](market-strategy/README.md)",
    )
    text = text.replace(
        "| [Documentation expansion audit — July 2026](research/documentation-expansion-audit-2026-07.md) | Repository-wide gap analysis that created the detailed engineering library and records the next documentation priorities |\n\n| [Performance, security, developer, and missing-systems expansion audit — July 2026]",
        "| [Documentation expansion audit — July 2026](research/documentation-expansion-audit-2026-07.md) | Repository-wide gap analysis that created the detailed engineering library and records the next documentation priorities |\n| [Performance, security, developer, and missing-systems expansion audit — July 2026]",
    )
    market_row = "| [Browser market gap and differentiation research — July 2026](research/browser-market-gap-2026-07.md) | Market concentration, competitor workflows, user-demand signals, switching barriers, and OP-001 through OP-014 validation hypotheses |"
    professional_row = "| [Professional buildout gap audit — July 2026](research/professional-buildout-gap-audit-2026-07.md) | Ownership, traceability, source strategy, technology, Plug-in, embedding, operations, legal, data, product, and sustainability controls |"
    if market_row not in text:
        text = text.replace(professional_row, professional_row + "\n" + market_row, 1)
    duplicate = "\n\n<!-- MARKET-STRATEGY-2026-07 -->\n## Market-gap evidence\n\n- [Browser market gap and differentiation research — July 2026](research/browser-market-gap-2026-07.md)\n- [Feature opportunity registry](market-strategy/machine/feature-opportunities.json)\n\nMarket opportunities use `OP-*` identifiers and remain non-normative until promoted through the professional review and traceability process."
    text = text.replace(duplicate, "")
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def patch_blueprint_index() -> None:
    path = Path("docs/blueprint-v1/README.md")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- [Professional Project Buildout and Operating Handbook](../project-buildout/README.md)\n\n- [Market Strategy and Differentiation](../market-strategy/README.md)",
        "- [Professional Project Buildout and Operating Handbook](../project-buildout/README.md)\n- [Market Strategy and Differentiation](../market-strategy/README.md)",
    )
    market_report = "- [Browser market gap and differentiation research — July 2026](../research/browser-market-gap-2026-07.md)"
    professional_report = "- [Professional buildout gap audit — July 2026](../research/professional-buildout-gap-audit-2026-07.md)"
    if market_report not in text:
        text = text.replace(professional_report, professional_report + "\n" + market_report, 1)
    duplicate = "\n\n<!-- MARKET-STRATEGY-2026-07 -->\n## Market strategy integration\n\nThe [browser market-gap report](../research/browser-market-gap-2026-07.md) and [market strategy book](../market-strategy/README.md) provide non-normative product hypotheses. They do not change accepted requirements, risks, ADRs, work packages, or support claims until those owning records are updated through reviewed evidence."
    text = text.replace(duplicate, "")
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def patch_professional_controls() -> None:
    owners_path = Path("docs/blueprint-v1/machine/professional-owners.json")
    owners = json.loads(owners_path.read_text(encoding="utf-8"))
    if not any(item.get("scope") == "product" for item in owners["owners"]):
        owners["owners"].append(
            {
                "scope": "product",
                "status": "provisional",
                "primary": "@byronwade",
                "backup": None,
                "next_review": "2026-10-16",
            }
        )
    owners_path.write_text(json.dumps(owners, indent=2) + "\n", encoding="utf-8")

    rules_path = Path("docs/blueprint-v1/machine/professional-review-rules.json")
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    for rule in rules["rules"]:
        rule["reviewers"] = [
            "release-operations" if reviewer == "release" else reviewer
            for reviewer in rule.get("reviewers", [])
        ]
    rules_path.write_text(json.dumps(rules, indent=2) + "\n", encoding="utf-8")


def patch_governance() -> None:
    governance = Path("docs/blueprint-v1/16-governance-contributing.md")
    text = governance.read_text(encoding="utf-8")
    product_roles = (
        "- **Product owner:** user needs, workflow coherence, product requirements, "
        "usability evidence, migration, and support scope.\n"
        "- **Market strategy owner:** competitive method, opportunity evidence, "
        "positioning, contrary evidence, and promotion or rejection of `OP-*` proposals."
    )
    if product_roles not in text:
        text = text.replace(
            "- **Program lead:** scope, milestones, release label, staffing, public claims.",
            "- **Program lead:** scope, milestones, release label, staffing, public claims.\n"
            + product_roles,
            1,
        )
    governance.write_text(text, encoding="utf-8")

    ownership = Path("docs/project-buildout/02-ownership-codeowners-and-maintainer-ladder.md")
    text = ownership.read_text(encoding="utf-8")
    marker = "<!-- MARKET-STRATEGY-OWNERSHIP-2026-07 -->"
    if marker not in text:
        text = (
            text.rstrip()
            + "\n\n"
            + marker
            + "\n## Product and market-strategy ownership\n\n"
            + "The product owner governs coherent user workflows, requirements, usability, "
            + "migration, and support scope. The market-strategy owner governs competitive "
            + "evidence, research freshness, `OP-*` status, contrary evidence, and promotion "
            + "or rejection. One person may provisionally hold both roles, but the "
            + "responsibilities and review records remain distinct.\n"
        )
    ownership.write_text(text, encoding="utf-8")


def patch_research_log() -> None:
    path = Path("docs/research-log.md")
    text = path.read_text(encoding="utf-8")
    marker = "## 2026-07-16 — Market strategy consistency audit"
    if marker not in text:
        text = (
            text.rstrip()
            + "\n\n"
            + marker
            + "\n\nIntegrated the market book and report into their owning index tables, "
            + "added the product ownership scope required by `REV-MARKET`, normalized "
            + "release review ownership, and strengthened validation so opportunity IDs, "
            + "reviewer scopes, and index placement cannot drift. No opportunity status "
            + "or implementation claim changed.\n"
        )
    path.write_text(text, encoding="utf-8")


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
    owners_path = MACHINE / "professional-owners.json"
    rules_path = MACHINE / "professional-review-rules.json"
    owners = load_json(owners_path)
    rules = load_json(rules_path)
    if not isinstance(owners, dict) or not isinstance(owners.get("owners"), list):
        fail("professional-owners.json must contain an owners array")
    if not isinstance(rules, dict) or not isinstance(rules.get("rules"), list):
        fail("professional-review-rules.json must contain a rules array")
    scopes = {item.get("scope") for item in owners["owners"]}
    required_scopes = {"product", "market-strategy"}
    missing_scopes = required_scopes - scopes
    if missing_scopes:
        fail("missing professional owner scopes: " + ", ".join(sorted(missing_scopes)))
    allowed_reviewers = scopes | {"owner"}
    for rule in rules["rules"]:
        unknown = set(rule.get("reviewers", [])) - allowed_reviewers
        if unknown:
            fail(
                f"{rule.get('id')}: unknown reviewer scopes: "
                + ", ".join(sorted(unknown))
            )

    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    if "\n\n| [Market Strategy and Differentiation]" in docs_index:
        fail("docs/README.md separates the market-strategy row from the books table")
    market_report = "| [Browser market gap and differentiation research — July 2026]"
    if market_report not in docs_index:
        fail("docs/README.md active research table is missing the market-gap report")

    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    if "\n\n- [Market Strategy and Differentiation]" in blueprint_index:
        fail("Blueprint index separates market strategy from the engineering-book list")
    if "../research/browser-market-gap-2026-07.md" not in blueprint_index:
        fail("Blueprint current reports are missing the market-gap report")
'''
        if anchor not in text:
            raise RuntimeError("validator insertion anchor missing")
        text = text.replace(anchor, function + anchor, 1)
    if "        check_professional_controls()\n" not in text:
        text = text.replace(
            "        check_json_registries()\n",
            "        check_json_registries()\n        check_professional_controls()\n",
            1,
        )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_docs_index()
    patch_blueprint_index()
    patch_professional_controls()
    patch_governance()
    patch_research_log()
    patch_validator()


if __name__ == "__main__":
    main()
