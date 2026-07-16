# Ownership, CODEOWNERS, and Maintainer Ladder

Status: detailed research and professional operating baseline  
Owner: program and governance owners  
Last researched: 2026-07-16

## Purpose

Convert conceptual roles into an executable ownership model for every subsystem, document, schema, test suite, benchmark, release artifact, service, and incident path.

## Governing principles

- Ownership is responsibility for maintenance, incidents, deprecation, and outcomes—not exclusive control.
- CODEOWNERS routes review but does not prove competence.
- No supported subsystem has a bus factor of one.
- Unowned and provisional scopes remain visible.
- Access is least-privileged and reconciled with current responsibility.

## Required contract

- Record primary, backup, architecture, security, accessibility, performance, release, product, market-strategy, and documentation reviewers.
- Define contributor, reviewer, subsystem maintainer, security maintainer, release maintainer, product maintainer, and program-owner levels.
- Document promotion, probation, recusal, inactivity, removal, succession, and emergency replacement.
- Use two-person control for stable signing, update trust, supported-version changes, and irreversible migrations.
- Review ownership and access quarterly and before every release phase.

## Product and market-strategy ownership

The product owner is accountable for coherent user workflows, product requirements, usability evidence, migration, lifecycle expectations, and supported product scope. The market-strategy owner is accountable for competitive method, source freshness, positioning evidence, contrary evidence, `OP-*` status, and the documented promotion, deferral, rejection, or expiry of market opportunities.

One person may provisionally hold both roles during the research phase, but the responsibilities and review records remain distinct. Product popularity does not override security, accessibility, compatibility, performance, legal, or operational review.

## Professional workflow

1. Propose scope and evidence.
2. Review coverage and conflicts.
3. Update ownership registry, CODEOWNERS, escalation, and support matrix together.
4. Reconcile GitHub, CI, signing, package, disclosure, and service access.
5. Expire provisional assignments unless reaffirmed.

## Evidence and exit gates

- PBO-GATE-3: no beta/stable subsystem is ownerless or single-owner.
- Critical scopes have tested escalation and backup coverage.
- CODEOWNERS patterns match representative paths.
- Departed maintainers retain no privileged access.
- Every reviewer scope named by a machine-readable review rule resolves to a registered owner scope or the change owner.

## Risks and failure modes

- A global wildcard can mask ownership gaps.
- Too-granular ownership creates review bottlenecks.
- Stale access survives social role changes.
- Titles without operational duties create false assurance.
- Market and product roles can collapse into feature advocacy unless contrary evidence and rejection authority remain explicit.

## Primary sources

- GitHub CODEOWNERS — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub rulesets — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Developer Certificate of Origin — https://developercertificate.org/

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.
