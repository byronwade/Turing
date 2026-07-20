# Independent Review Capacity Decision Briefing - July 2026

Status: checked decision-support briefing; no ruling made, no reviewer named, `PB-019` unchanged
Owner: program ownership
Related gate: `PB-019`, `PB-020`, and all eleven owner-decision closure scopes
Prepared: 2026-07-20

## Question

Every owner-decision closure scope requires an independent reviewer, and every build-critical scope currently resolves to one person. Must that reviewer be a fully qualified `PB-019` backup owner, or is a qualified non-author sufficient?

This is the highest-leverage open question in the program. It gates all eleven closure scopes at once, which is more than any single gate decision including `ADR-0009`.

## Why this briefing exists

An earlier analysis in this repository recorded fifteen `proposed_independent_review_dependency` edges from `PB-019` to the other gates, on the reasoning that no independent reviewer exists while every backup is null. Those edges were deliberately marked `proposed_no_claim_pending_owner_ratification` because the equivalence they assume — that an independent reviewer must be a `PB-019` backup owner — is nowhere stated in this repository.

This briefing assembles what the records actually say, so the owner can rule on that equivalence rather than inherit it.

## What the records transcribe

These are direct readings, not inference.

**Independence is defined relative to authorship, not to ownership rank.** [Independent Verification and Adversarial Review](../agent-execution/08-independent-verification-and-adversarial-review.md) defines the implementation lane as "code-owner and architecture review independent of the authoring run", and states that "a verifier cannot silently patch the implementation it is certifying; findings return to a new implementation task." The constraint expressed is non-authorship and non-self-certification.

**The synchronization matrix names roles, not people.** [`owner-decision-synchronization.json`](../project-buildout/machine/owner-decision-synchronization.json) gives each of the eleven scopes an `independent_reviewer_role` — "independent architecture and provenance reviewer", "independent IPC and security reviewer", and so on. Its own `unsupported` list states plainly: "This matrix does not name human owners or reviewers." It also states "A passing validator is not owner review or independent review."

**Two-person control is scoped narrowly, and not to all eleven.** [Ownership, CODEOWNERS, and Maintainer Ladder](../project-buildout/02-ownership-codeowners-and-maintainer-ladder.md) requires two-person control for "stable signing, update trust, supported-version changes, and irreversible migrations." The `PB-019` gap record extends that list to eight: stable signing, update trust, supported-version changes, security disclosure, irreversible profile migration, release promotion, legal approval, and incident closure. Every item on that list is a release-path or authority action. None of them is required to close a contained-M0 evidence gate.

**`PB-019` is about coverage, not review.** Its qualification axes are role level, subsystem competence, representative path coverage, recent review record, availability, succession, recusal, inactivity, removal, and emergency replacement. Succession, inactivity, and emergency replacement are continuity properties. They answer "what happens when the owner is unavailable", which is a different question from "who checks this specific piece of evidence."

**Every scope already has an exception path.** Each of the eleven scopes carries an `exception_policy` requiring that an exception name an owner and linked risk, expire, define rollback, and change support and unsupported-behavior language. The matrix constrains it: "A future exception must update support boundaries and expire; it cannot silently convert a blocker into readiness."

## What is inference

No document states that an independent reviewer must be a `PB-019`-qualified backup owner. No document states the opposite either. The two requirements are defined in different places for different purposes and are never explicitly related.

The reading that follows from the transcribed records — that independence is a non-authorship property while backup ownership is a continuity property, and that they are therefore separable — is the more natural one. It is still a reading. It is exactly the ruling this briefing asks the owner to make.

## The options

| | What it means | What it unlocks | Residual risk |
|---|---|---|---|
| **1. Independence requires a `PB-019` backup owner** | The strict reading. Closure waits on full qualification records for at least one scope. | Nothing until a fully qualified backup exists. | Highest schedule cost. All eleven scopes stay closed indefinitely. Risks conflating continuity with review and stalling the program on the harder problem. |
| **2. Independence requires a qualified non-author** | The reading the records more naturally support. A competent reviewer who did not author the work may certify evidence for closure scopes. Two-person control still applies to the eight release-path and authority actions. | All eleven closure scopes become reachable with a single additional qualified person, who need not carry succession or emergency-replacement obligations. | Requires defining "qualified" per scope. A reviewer without continuity obligations cannot cover owner unavailability, so `PB-019` remains open regardless. |
| **3. Time-bounded exceptions per scope** | Use the existing `exception_policy` to proceed on named scopes with recorded risk and expiry. | Bounded progress on specific gates without any second person. | Cannot convert a blocker into readiness, by the matrix's own rule. Accumulating exceptions with one owner recreates the single-point-of-failure this discipline exists to prevent. Best used sparingly and alongside option 2, not instead of it. |

## Analytical recommendation, not an approval

**Option 2**, with two-person control preserved unchanged for the eight release-path and authority actions.

Reasoning:

1. It matches the definition already written: independence is specified as independence *from the authoring run*, and the prohibition is on self-certification.
2. It separates two problems that are genuinely different. A reviewer who checks IPC negative tests does not need a succession plan; an owner who can sign releases does. Conflating them makes the cheaper problem wait on the harder one.
3. It does not weaken any release-path control. Signing, update trust, supported-version changes, disclosure, irreversible migration, release promotion, legal approval, and incident closure all keep two-person control.
4. It is the only option that converts a single additional person into eleven unlocked scopes.
5. `PB-019` stays blocked under every option, so choosing option 2 gives up nothing that option 1 preserves.

This is analysis of documented trade-offs. It does not rule, does not name a reviewer, does not close any scope, and does not promote `PB-019`.

## What this decision does not do

- It does not close `PB-019`. Backup ownership remains a separate, still-open continuity problem.
- It does not close any gate by itself. Each scope still needs its own evidence.
- It does not grant release, signing, disclosure, legal, incident-closure, or production authority.
- It does not make the documentation "ready for a full build". Closure still requires the evidence each scope names, reviewed by whoever the ruling qualifies.

## Required record if a ruling is made

The ruling should state, in a form the closure board can cite:

- whether independent review requires `PB-019` backup qualification or qualified non-authorship;
- what "qualified" means per scope, at minimum subsystem competence and non-authorship of the evidence under review;
- that two-person control is unchanged for the eight named release-path and authority actions;
- what happens to the fifteen `proposed_independent_review_dependency` edges in [`build-readiness-dependency-graph.json`](../project-buildout/machine/build-readiness-dependency-graph.json) — ratified, narrowed, or removed;
- an expiry or revisit trigger, consistent with the [solo-owner residual-risk acceptance](solo-owner-residual-risk-acceptance-2026-07.md) expiring 2026-10-16.

## Current disposition and next proof

No ruling exists. All eleven scopes remain unclosable and `PB-019` remains blocked. The next proof is the owner ruling itself; it requires no new evidence, only a decision on an existing ambiguity.

## Claim boundary

This briefing is decision support only. It does not rule on the review requirement, name or qualify any reviewer, establish independence, grant two-person control, close or promote any gate, approve a task, or support broad M1, Chrome-class, performance, compatibility, security, accessibility, production, release, or all-information-ready-for-building claims.
