# ADR-0009 Owner Decision Briefing - July 2026

Status: checked decision-support briefing; no option selected, no ADR accepted
Owner: architecture and program ownership
Related gate: `PB-002`, `ADR-0009`, `ADR9-EV-018`
Prepared: 2026-07-20

## Question

What does the program owner actually need to decide for `ADR-0009`, in what order, and what does each option cost?

## Short answer

The decision is one sentence: **what relationship may Turing's release code have with Servo source?** Everything else in the eighteen-item evidence set is downstream of that sentence.

This briefing exists because the existing packet, matrix, and draft are each complete and each large. They describe the decision space correctly but do not tell an owner where to start. This is the reading order and the trade-off summary; it does not select an option.

## What is genuinely blocking

`ADR9-EV-018` is `blocked`. The other seventeen items are `partial`. That distribution is easy to misread as "seventeen things are nearly done." It is not what it means.

Reading each item's `next_action` shows a critical path rather than seventeen parallel tasks. At least five items cannot start until a source baseline is chosen:

- `ADR9-EV-009` (unsafe-code review): "Select the ADR-0009 candidate boundary, then complete a block-level unsafe ledger for only that boundary."
- `ADR9-EV-011` (component boundaries): "Select the candidate source baseline and feature profile, then turn the first-pass closure report into owner-reviewed component boundaries."
- `ADR9-EV-013` (compatibility corpus): runs against the selected baseline.
- `ADR9-EV-014` (performance baseline): runs against the selected source baseline.
- `ADR9-EV-017` (public claims): "**After** an owner selects, rejects, or supersedes an ADR-0009 option, apply the matching document, registry, and support-language changes."

So the seventeen partial items are not seventeen units of remaining work that must precede the decision. A large fraction of them are gated *behind* it. `ADR9-EV-001` — select the source baseline model and record the provenance and equivalence policy — is the head of the chain.

This is the single most useful thing in this briefing: **the decision is not waiting on more evidence gathering; a good deal of the evidence gathering is waiting on the decision.**

## The decision that actually forks the program

`ADR9-EV-012` is the question that separates the options from each other more than any other: does the option preserve `ADR-0004` (a Turing-owned JavaScript runtime), treat SpiderMonkey only as a comparator, or explicitly supersede the Turing-owned runtime commitment?

Options A, B, and C preserve the charter. Options D and E replace it. That is a product and identity decision, not an engineering shortcut, and it is why the packet warns that a lower implementation burden does not override charter, security, provenance, legal, compatibility, or maintenance requirements.

## Option comparison on the dimensions that differ

All five are documented at equal depth in the [decision draft](../project-buildout/16-adr-0009-decision-draft.md). Summarized on the axes where they genuinely diverge:

| | Charter | JS runtime | Legal/SBOM load | Maintenance load | Claim risk |
|---|---|---|---|---|---|
| **A. Clean implementation, Servo as research input** | Preserved intact | `ADR-0004` untouched | Lowest — no Servo source enters the supported runtime | Turing owns everything; highest schedule risk | Lowest; claims stay "independent and unfinished" |
| **B. Selective Servo components** | Preserved only for named, reviewed, replaceable components | Untouched unless a component pulls SpiderMonkey | Per-component provenance, license, advisory, SBOM, source-offer, unsafe/FFI ledgers | Hidden coupling and long-term merge burden | Moderate; only the exact named component scope may be discussed |
| **C. Upstream-first collaboration** | Preserved | Untouched | Low | Coordination cost without reducing implementation risk | Low, but easy to overstate externally |
| **D. Servo-derived engine** | Superseded | Likely supersedes `ADR-0004` | Full source, dependency, provenance, legal, SBOM, native-package obligations | Servo-derived code becomes release-critical | High; every independent-engine claim becomes stale |
| **E. Servo browser charter change** | Replaced | Replaced | Full, plus branding/trademark/governance | Rebaselines every gate | Highest; current positioning cannot be reused |

## Analytical recommendation, not an approval

On the documented evidence, **Option A or Option C** is the better first move, and the two are compatible with each other. Reasoning:

1. They preserve the charter, so they do not force a simultaneous rewrite of `ADR-0002`, `ADR-0004`, `REQ-ENG-007`, the roadmap, risks, and definition of done.
2. They are the only options that do not immediately expand the legal, SBOM, advisory, and native-package surface — which matters disproportionately while `PB-019` leaves you without a second reviewer for security or legal scope.
3. They are reversible. A later ADR can narrow toward Option B once component boundaries are actually reviewed. Options D and E are not cheaply reversible; they discard positioning that would have to be rebuilt from evidence.
4. Option B's residual risk — hidden coupling, duplicated architecture, long-term merge burden, support ambiguity — is the hardest of the reversible options to manage with a single maintainer.

This is analysis of documented trade-offs. It is not an owner decision, does not select an option, and does not close `ADR9-EV-018`. The packet requires the owner to record the selected, rejected, or deferred disposition with rationale.

## What accepting ADR-0009 does not unlock

Worth stating plainly, because it is easy to expect more from this decision than it delivers:

- It does not grant broad M1 implementation, release authority, or production authority.
- It does not close `PB-020`; that gate stays `partial` until every remaining P0 owner decision is closed.
- It does not satisfy the independent-review requirement. `owner-decision-synchronization.json` requires an independent architecture and provenance reviewer for this scope and makes self-approval a rejection condition, so an accepted ADR still needs a second qualified person — see the [dependency graph inventory](build-readiness-dependency-graph-inventory-2026-07.md#proposed-review-capacity-finding-not-owner-ratified).

## Required record if a decision is made

The [decision draft](../project-buildout/16-adr-0009-decision-draft.md) lists the full synchronized diff. The minimum a decision record must carry, per the pre-review worksheet:

- option disposition with rationale and rejected alternatives;
- charter and independence effect, with exact affected ADR and requirement paths;
- source boundary: immutable baseline, ref, archive or package identity, feature and target profiles, included and excluded components, and generated-output scope — never `latest` or a bare project name;
- disposition for every `ADR9-EV-001` through `ADR9-EV-018`, with nothing hidden by a general approval;
- named decision owner and independent reviewer, review date, and dissenting evidence.

## Current disposition and next proof

`PB-002` remains blocked and no option is selected. The next proof is an owner ruling on `ADR9-EV-001` — the source baseline model and provenance/equivalence policy — because that unblocks the largest number of downstream evidence items.

## Claim boundary

This briefing is decision support only. It does not select or approve a source strategy, accept or reject any option, authorize Servo source or component adoption, close any `ADR9-EV-*` item, promote `PB-002` or `PB-020`, or support broad M1, Chrome-class, performance, compatibility, security, accessibility, production, release, or all-information-ready-for-building claims.
