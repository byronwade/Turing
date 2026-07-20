# Solo-Owner Residual-Risk Acceptance - July 2026

Status: agent-drafted residual-risk record, pending owner countersignature; `PB-019` remains blocked
Owner: program ownership
Related gate: `PB-019` Backup ownership for build-critical scopes
Drafted: 2026-07-20
Countersigned: not yet
Expires: 2026-10-16
Updated: 2026-07-20

> **Provenance caveat.** An agent wrote this record. The owner selected "document as accepted solo-owner risk" in a chat session, which is an instruction to draft, not the owner-review process this repository defines. A chat selection is not a named owner approval: it carries no independent reviewer and synchronizes no registry. Until the owner countersigns in a durable repository record, this is a draft and must not be cited as an owner decision. An independent review of this session's changes raised exactly this point, and it was correct to.

## Question

Can the program owner record an explicit, time-bounded acceptance of single-owner residual risk across the twenty-two build-critical scopes without implying that backup ownership, two-person control, owner coverage, or release authority exists?

## Short Answer

Yes, as a draft pending countersignature. This document records that the owner instructed, in a chat session on 2026-07-20, that the single-owner exposure be documented as accepted, and it sets out the scope, exposure, compensating controls, revisit triggers, and expiry that such an acceptance would carry.

It does not assert that the owner has read the [Backup Ownership Gap Inventory](backup-ownership-gap-inventory-2026-07.md) or any other record, because the drafting agent has no evidence of that. Countersigning this document is the act that supplies it.

It does not change `PB-019`. The gate remains `blocked`.

## Why this record does not unblock `PB-019`

An earlier framing of this decision assumed that accepting the risk would move `PB-019` from `blocked` to an exception state. The repository's own controls reject that framing, and they are correct to.

Two independent enforcement points in [`validate_blueprint.py`](../../tools/validate_blueprint.py) require the blocked status:

- `PB-019 must remain blocked while backup ownership is only checked gap evidence`
- `PB-019 must remain blocked while any professional owner backup is null`

The `PB-019` record in [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json) also names, in its own `evidence_required` list, an `explicit blocked status while backups are null, placeholders, undocumented availability, single-owner research-phase assignments, single-owner residual risk, or primary-only review paths remain`.

Single-owner residual risk is therefore an explicitly enumerated reason to stay blocked, not a route out of it. Owner acceptance of a risk is not the same as remediation of that risk. Only named, qualified, reviewed backup owners can move this gate.

## Scope of the accepted risk

All twenty-two build-critical scopes in [`backup-ownership-gap.json`](../project-buildout/machine/backup-ownership-gap.json) are covered: program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data.

Every one has `@byronwade` as primary and `null` as backup.

## What the owner is accepting

- No second reviewer exists for any build-critical scope.
- No independent review of the primary owner's own changes is possible.
- Owner unavailability halts every scope simultaneously; there is no succession path.
- No recusal path exists for conflicts, legal conflict, or security embargo.
- Repository access, signing material, and disclosure channels have no reviewed second holder.
- Loss of the primary owner's accounts or credentials is an unrecovered single point of failure.

## What remains prohibited regardless of this acceptance

This record does not grant, and must never be cited as, any of the following:

- owner coverage, backup ownership, or two-person control;
- release authority, release promotion, or stable signing authority;
- update-trust changes or supported-version changes;
- security-disclosure authority or incident-closure authority;
- irreversible profile-migration approval or legal approval;
- production authority, broad readiness, or implementation approval.

Every path in the `two_person_control_required` list stays unavailable: stable signing, update trust, supported-version changes, security-disclosure, irreversible profile migration, release promotion, legal approval, and incident closure.

## Compensating controls while the acceptance stands

These are the controls that make contained-M0 continuation defensible under solo ownership. They limit blast radius; they do not substitute for a backup owner.

- Work stays inside the contained-M0 boundary defined by [`contained-m0-start-state.json`](../project-buildout/machine/contained-m0-start-state.json).
- No release, signing, publishing, or distribution path is exercised.
- No production or user-facing data is handled.
- The 78 `tools/validate_*.py` checks act as a mechanical reviewer for registry and documentation consistency, standing in for a human second reviewer on structural questions only, never on judgement or authority questions.
- All owner-only decisions remain queued in the [owner-decision closure board](../project-buildout/23-owner-decision-closure-board.md) rather than being resolved unilaterally under time pressure.

## Revisit triggers

The acceptance ends immediately, before its expiry date, on any of the following:

- any move toward developer preview, beta, stable, or public distribution;
- any request to exercise signing, update-trust, or supported-version changes;
- receipt of a security report requiring coordinated disclosure;
- any irreversible profile or data migration proposal;
- acceptance of `ADR-0009` or any decision that opens broad M1 implementation;
- extended owner unavailability;
- addition of any second contributor with write access.

## Expiry

This acceptance expires on 2026-10-16, the earlier of the two `next_review` dates recorded in the gap inventory: 16 of the 22 build-critical scopes carry 2026-10-16 and the remaining 6 carry 2026-10-17. The earlier date is chosen deliberately so the acceptance never outlives any scope's scheduled review. On expiry the owner must either name qualified backups, renew the acceptance with a fresh dated record, or narrow the scope of work.

An expired acceptance is not self-renewing. If the date passes without action, treat solo operation as unaccepted and stop contained-M0 continuation until the record is refreshed.

## Machine companion

The machine record is `OWN.EXCEPTION.SOLO_OWNER_RESIDUAL_RISK.2026_07` in [`professional-exceptions.json`](../blueprint-v1/machine/professional-exceptions.json).

## Current disposition and next proof

`PB-019` remains blocked. The next proof that changes the gate is not another acceptance record; it is a named qualified backup owner for at least one build-critical scope, carrying role level, subsystem competence, representative path coverage, recent review record, availability, succession, recusal, inactivity, removal, and emergency-replacement evidence, reconciled against CODEOWNERS and the review rules.

## Claim boundary

This record supports contained-M0 continuation and documentation governance only. It is not backup ownership, not owner coverage, not two-person control, not a readiness promotion, and not an implementation, release, security, production, or Chrome-class claim.
