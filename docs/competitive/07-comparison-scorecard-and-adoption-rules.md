# Competitive Comparison Scorecard and Adoption Rules

Status: research governance baseline  
Owner: competitive measurement and architecture decisions  
Purpose: Define valid comparisons and how external lessons become Turing experiments or accepted decisions.

## Relationship to the Turing program

This document governs RQ-16 and future competitive studies. Accepted architecture remains in Blueprint and ADR records.

## Scorecard dimensions

Score open-web compatibility, JavaScript/WebAssembly, rendering/graphics, startup, interaction tails, frame pacing, memory, energy, background behavior, stability/recovery, security/privacy, accessibility, developer protocol, observability, everyday UX, platform integration, build/release, open-source health, and support continuity. Every dimension has raw evidence and a confidence level.

A single aggregate score may be used only as a view over published dimensions and weights; it cannot hide a critical failure.

## Equivalent comparison

Use exact versions, same hardware/OS/power/thermal/display/network, clean equivalent profiles, default-equivalent mitigations, same page corpus and activity, matched caches, disclosed extensions/agents, and equivalent tab/site-isolation/lifecycle state. Unsupported/failed workloads remain. Product-specific proprietary features are listed rather than scored as silent failure.

Separate browser shell, engine, runtime, service, and platform contributions when causation is known.

## Architecture hypothesis process

An observed competitor strength generates a hypothesis, not an immediate decision. The report states source, observation, inferred mechanism, alternatives, expected benefit, security/accessibility/compatibility risks, maintenance cost, and falsifying experiment. Turing builds the smallest native prototype that can test it.

Correlation between architecture description and benchmark result is not causal evidence.

## Adopt, adapt, reject, defer

Adopt means the pattern passed Turing experiments and entered an ADR/Blueprint. Adapt means the underlying principle passed but implementation differs. Reject records evidence and revisit trigger. Defer records missing prerequisites or capacity. Every status has owner, date, evidence, affected requirements/risks/work packages, and expiry/review trigger.

No code is copied without provenance and license review.

## Standards and ecosystem

For web-visible behavior, standards and tests outrank a competitor's implementation. If engines agree against a standard, investigate test/spec ambiguity and compatibility impact rather than clone behavior silently. Site-specific interventions require public rationale, narrow scope, test, owner, expiry, and standards path.

Developer compatibility adapters remain outer layers.

## Claim policy

“Number one”, “fastest”, “most efficient”, “most compatible”, “most secure”, or equivalent claims require current reproducible evidence across all materially affected dimensions. Claims state scope and date. Turing can claim a specific measured lead, such as lower memory on a defined 30-tab corpus, without generalizing beyond it.

Research builds make no production safety claim.

## Continuous review

Quarterly or milestone reviews refresh current stable versions, standards focus areas, project status, benchmark corpus, security mitigations, product workflows, and Turing results. Stale studies remain historical with dates rather than being rewritten as current fact without evidence.

## Non-negotiable invariants

- Critical security, compatibility, accessibility, or data-loss failures cannot be averaged away.
- Comparisons use equivalent configuration and retain failed/unsupported workloads.
- External architecture observations become falsifiable Turing experiments before decisions.
- Web-visible behavior follows standards/tests, not hidden single-engine cloning.
- Leadership claims are scoped, dated, reproducible, and expire.
- Provenance and license review precede use of external code or test material.

## Required evidence

- Versioned scorecard schema, manifests, raw results, and analysis.
- Confidence and causality labels for every conclusion.
- Adopt/adapt/reject/defer decision ledger with revisit triggers.
- Independent reproduction for selected claims.
- Quarterly/milestone refresh record.
- Standards and upstream test contributions from discovered ambiguities.

## Known risks and unresolved questions

- Scorecards can encode subjective weights or incentives.
- Competitors change faster than long research cycles.
- Public ranking can encourage benchmark gaming.
- Incomplete causal analysis can produce expensive architecture mistakes.

## Primary sources

- Web Platform Tests — https://web-platform-tests.org/
- Speedometer — https://browserbench.org/Speedometer3.1/
- MotionMark — https://browserbench.org/MotionMark/
- JetStream — https://browserbench.org/
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
