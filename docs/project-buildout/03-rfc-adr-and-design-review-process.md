# RFC, ADR, and Design-Review Process

Status: detailed research and professional operating baseline  
Owner: architecture and subsystem owners  
Last researched: 2026-07-16

## Purpose

Create one discoverable decision pipeline for architecture, public APIs, data formats, dependencies, security boundaries, performance strategy, deprecation, and operations.

## Governing principles

- Use the smallest sufficient artifact, but durable choices need durable review.
- Alternatives, uncertainty, dissent, and rejected options remain visible.
- Accepted ADRs are immutable and changed through supersession.
- Experiments do not become architecture merely because a prototype works.
- Security and accessibility concerns require explicit risk ownership.

## Required contract

- Classify work as routine, design note, RFC, ADR, security review, incident emergency, or compatibility intervention.
- Require RFCs for new subsystems, stable APIs, profile formats, Plug-in capabilities, embedding contracts, telemetry, sync, and major dependencies.
- Require ADRs for trust boundaries, languages, source strategy, long-lived formats, release trust, license model, and irreversible compatibility promises.
- Assign stable ID, state, owner, reviewers, comment period, implementation issue, and supersession chain.
- Keep proposal, experiment, accepted, implemented, verified, and supported states distinct.

## Professional workflow

1. Start from the indexed template.
2. Classify decision and reviewers.
3. Collect prototypes or research where empirical.
4. Review every cross-cutting dimension.
5. Record outcome and dissent.
6. Link implementation.
7. Verify assumptions after implementation.

## Evidence and exit gates

- PBO-GATE-4: no irreversible decision exists only in chat, commit, or code review.
- Required reviewers and alternatives are complete.
- Migration and rollback are linked.
- Decision status agrees across index, issues, code, and docs.

## Risks and failure modes

- Excess process drives decisions into side channels.
- Consensus can delay urgent work.
- An ADR can overstate weak evidence.
- Retrospective records can rationalize instead of preserve facts.

## Primary sources

- Architecture Decision Records — https://adr.github.io/
- Rust RFC process — https://rust-lang.github.io/rfcs/
- IETF RFC 7282 — https://www.rfc-editor.org/rfc/rfc7282

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.

<!-- MARKET-STRATEGY-2026-07 -->
## Market proposal review

Use `docs/templates/market-opportunity.md`. Workspace identity, sync trust, snapshot retention, agent authority, public interchange, or collaboration cryptography normally requires an RFC and may require an ADR after prototype evidence.
