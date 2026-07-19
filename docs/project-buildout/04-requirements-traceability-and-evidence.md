# Requirements Traceability and Evidence

Status: detailed research and professional operating baseline  
Owner: quality, architecture, and documentation owners  
Last researched: 2026-07-16

## Purpose

Define the authoritative chain from user need to requirement, design, source, tests, evidence, release gate, supported status, and current owner.

The machine-readable [`requirement-verification-matrix.json`](../blueprint-v1/machine/requirement-verification-matrix.json) and its [human handoff](24-requirement-verification-matrix.md) are the planned verification layer for this contract. They map every accepted requirement to a bounded evidence lane without claiming that implementation, tests, reviews, or evidence already exist.

## Governing principles

- A requirement without verification is an intention.
- Evidence identifies exact commit, build, environment, configuration, and result.
- Negative, failure, recovery, security, and accessibility evidence are first-class.
- Unsupported, crash, timeout, and not-run outcomes remain visible.
- Traceability is generated from stable IDs, not an unaudited spreadsheet.

## Required contract

- Link every requirement to owner, milestone, RFC/ADR, risks, source scopes, tests, conformance, fuzz targets, benchmarks, reviews, release gates, and evidence.
- Represent specified, implemented, verified, release-gated, and supported separately.
- Record platforms, configurations, freshness, expiry, and limitations.
- Validate references in both directions.
- Allow access-controlled references for embargoed security evidence without hiding debt.

## Professional workflow

1. Create or change requirement and owner.
2. Add design and risk links.
3. Register source and verification plan.
4. Attach evidence as work completes.
5. Run CI validation.
6. Reconcile stale and waived evidence at milestones.
7. Invalidate evidence when code or assumptions change.

The verification plan must be present before a task is approved. It must name the requirement lane, work package, evidence classes, positive test layers, negative/failure cases, required artifacts, and next proof. Actual test, review, and evidence references remain separate records and cannot be inferred from the plan.

## Evidence and exit gates

- PBO-GATE-5: every release-critical requirement has current evidence.
- No supported claim points only to prose.
- Evidence build IDs match released artifacts.
- No release requirement lacks owner or verification method.

## Risks and failure modes

- Traceability can become enormous; generate views instead of duplicating records.
- A passing test can prove the wrong behavior.
- External suite revisions can invalidate interpretation.
- Embargoed evidence needs controlled visibility.

## Primary sources

- NIST Secure Software Development Framework — https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA specification — https://slsa.dev/spec/v1.2/
- Semantic Versioning — https://semver.org/
- JSON Schema 2020-12 — https://json-schema.org/draft/2020-12

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.

<!-- MARKET-STRATEGY-2026-07 -->
## Opportunity-to-requirement boundary

`OP-*` records are not requirements. Promotion creates or updates `REQ-*`, `R-*`, `WP-*`, ADR, owner, tests, evidence, and support records in one reviewed change. Rejected and deferred opportunities retain rationale and evidence.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Task and run traceability

Accepted implementation records link requirement -> design -> `TASK-*` -> source -> tests -> agent run manifest -> evidence bundle -> independent review -> release gate. Missing links remain visible rather than inferred from a merged commit.
