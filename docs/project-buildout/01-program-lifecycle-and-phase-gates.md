# Program Lifecycle and Phase Gates

Status: detailed research and professional operating baseline  
Owner: program, architecture, security, quality, and release owners  
Last researched: 2026-07-16

## Purpose

Define an evidence-gated path from research through prototype, preview, beta, stable release, maintenance, and end-of-life. The existing M0–M9 roadmap remains the product sequence; this chapter makes entry, exit, stop, rollback, and claim rules explicit.

## Governing principles

- Maturity is earned from current evidence, not schedule, feature count, screenshots, or publicity.
- A later feature cannot bypass an earlier security, data-integrity, accessibility, or update boundary.
- Every phase has an owner, entry criteria, exit evidence, stop conditions, rollback path, and prohibited claims.
- Staffing and emergency-patch capacity are release evidence.
- A passed gate can be reopened when its assumptions are invalidated.

## Required contract

- Maintain machine-readable status for M0 through M9.
- Every gate packet includes requirement status, risks, ADRs, conformance, fuzzing, security, accessibility, performance, reliability, operations, legal readiness, staffing, and unsupported behavior.
- Decisions are continue, continue with scope reduction, hold, rollback, or cancel.
- Waivers identify approver, scope, compensating controls, release disclosure, and automatic expiry.
- Security isolation, update verification, credential separation, and misleading maturity claims are non-waivable.

## Professional workflow

1. Confirm entry criteria and ownership.
2. Execute the implementation and evidence plan.
3. Run subsystem and cross-cutting reviews.
4. Assemble exact-commit evidence.
5. Record go/no-go and dissent.
6. Update status, public claims, roadmap, and next-phase plan atomically.

## Evidence and exit gates

- PBO-GATE-1: public maturity label matches machine status.
- PBO-GATE-2: all prerequisite trust boundaries pass before the next phase.
- Rollback or scope-reduction is exercised for irreversible changes.
- No release-critical requirement is complete without evidence.

## Risks and failure modes

- Process can become performative if records are not derived from evidence.
- Single-maintainer approval creates blind spots.
- Waivers can become permanent through inertia.
- Overbroad phases can block indefinitely and need evidence-domain decomposition.

## Primary sources

- NIST Secure Software Development Framework — https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA specification — https://slsa.dev/spec/v1.2/
- Semantic Versioning — https://semver.org/
- JSON Schema 2020-12 — https://json-schema.org/draft/2020-12

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.
