# ADR-0009 Decision Draft and Public-Claim Impact

Status: decision-support draft; not accepted
Owner: architecture and program ownership
Evidence gates: `ADR9-EV-017` partial; `ADR9-EV-018` blocked
Last updated: 2026-07-19

This draft records the public-claim, requirement, risk, support-language, and registry updates that each `ADR-0009` source-strategy outcome would require. The checked no-claim [`ADR-0009 decision-review template`](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json) defines the future owner-review shape. Neither this draft nor that template is an accepted ADR, and neither approves a Servo relationship, Servo-derived release code, source import, support commitment, compatibility claim, security claim, memory claim, speed claim, or charter change.

## Current Decision State

No `ADR-0009` option is selected. `PB-002` remains blocked until the preceding evidence gates are owner-reviewed or explicitly rejected with time-bounded exceptions and a real decision-review record replaces the checked no-claim template.

The [normalized option matrix](../research/adr-0009-source-strategy-closure-preparation-2026-07.md#option-normalization-matrix) is the comparison aid for owner review. It distinguishes research input, collaboration, component reuse, engine adoption, and charter change; it does not score, recommend, or select an option.

The only claim currently supported is:

Turing is a research and architecture program with a small M0 Rust prototype, documentation, validation tooling, and external Servo evidence. The repository is not a production-safe browser and has not accepted Servo source, Servo components, a Servo maintenance relationship, a JavaScript-runtime change, a compatibility target, or public binary support.

## Common Claim Boundaries

These limits apply to every option until a reviewed ADR says otherwise:

- Do not say Turing is Servo-based, Servo-derived, Chrome-compatible, production-safe, secure for hostile browsing, faster, lower-memory, lower-energy, or release-ready.
- Do not imply that a successful external Servo build imports source, approves dependencies, or makes Turing build-ready for broad engine implementation.
- Do not cite Servo compatibility, performance, memory, or security behavior as Turing behavior.
- Do not claim support for sensitive browsing, financial activity, private accounts, extension ecosystems, enterprise deployment, synchronization, AI-agent browsing, DevTools compatibility, or binary updates.
- Disclose unsupported cases before presenting any demo or preview path.

## Common Required Diff Template

Every accepted `ADR-0009` outcome must update these records in the same change as the decision:

- `docs/blueprint-v1/17-architecture-decisions.md`: add the accepted decision, rejected options, evidence basis, expiration of any exception, and post-decision work packages.
- `docs/blueprint-v1/machine/pre-build-readiness.json`: update `PB-002` status, evidence, remaining blockers, and allowed work.
- `docs/blueprint-v1/machine/adr-0009-evidence.json`: close, supersede, or explicitly reject every `ADR9-EV-*` item with owner rationale.
- `docs/project-buildout/13-build-readiness-operating-board.md`: replace the evidence queue with the accepted operating path and owner-only blockers.
- `docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`: move from packet to decision record or link the accepted ADR.
- `docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`: mark final evidence status and rejected evidence.
- `docs/start-here.md`, `docs/README.md`, and `README.md`: update public-facing status and onboarding language.
- `docs/blueprint-v1/01-charter-and-principles.md`, `02-capability-parity.md`, `03-language-and-dependency-strategy.md`, `05-web-engine.md`, `06-javascript-runtime.md`, `08-security-and-sandbox.md`, `09-performance-memory.md`, `12-testing-compatibility.md`, `13-build-release-operations.md`, `14-roadmap-work-breakdown.md`, `15-risk-register.md`, `20-definition-of-done.md`, and `21-product-requirements.md`: update all affected scope, requirements, risks, release claims, and gates.
- Detailed books for affected surfaces: `docs/engine/`, `docs/javascript/`, `docs/security-engine/`, `docs/performance/`, `docs/benchmark-lab/`, `docs/release-operations/`, `docs/technology-stack/`, `docs/embedding/`, `docs/developer-experience/`, `docs/api-design/`, and `docs/competitive/`.
- Machine registries for requirements, risks, work packages, ownership, traceability, benchmark manifests, dependency/provenance ledgers, unsafe/native/generated-code ledgers, review rules, exceptions, and support statements when their meaning changes.

## Option A: Clean Implementation Informed by Servo

Public claim:

Turing may use Servo as external research input only. Turing release code remains independently implemented unless a later reviewed ADR accepts a narrower component boundary.

Unsupported behavior:

No Servo compatibility, performance, security, or support behavior transfers to Turing. Servo source is not copied. Servo dependencies do not enter the supported runtime.

Required updates:

- Keep the independent-engine charter intact.
- Preserve `ADR-0004` JavaScript runtime direction unless a separate ADR changes it.
- Update research and bibliography records to distinguish informative Servo observations from adopted architecture.
- Close or supersede Servo adoption work packages that assume source import.
- Add follow-up work packages for Turing-owned HTML, DOM, CSS, layout, paint, networking, storage, JavaScript-binding, compatibility, and benchmark implementation.

Residual risk:

The project may underuse mature upstream work and carry more schedule risk. Claims must emphasize independence and unfinished implementation, not parity.

## Option B: Selective Servo Components

Public claim:

Turing accepts only named Servo-derived or Servo-origin components behind reviewed boundaries. Turing is not Servo-based as a whole.

Unsupported behavior:

Any unselected Servo subsystem remains unsupported. Accepted components do not imply Servo-level compatibility or performance. Components that require SpiderMonkey, WebRender, Stylo, GStreamer, platform bootstrap assets, unsafe/FFI contracts, or generated outputs need explicit acceptance before release use.

Required updates:

- List every accepted component, excluded component, feature profile, source baseline, dependency closure, and replacement contract.
- Update dependency, license, advisory, SBOM, source-offer, native-package, generated-output, unsafe, FFI, and provenance ledgers.
- Add API boundary contracts and tests for every accepted component.
- Update security, sandbox, process authority, origin/profile identity, DevTools, extension, automation, and AI-agent boundaries touched by the component.
- Update support language to say that component acceptance is conditional and narrow.

Residual risk:

Selective adoption can create hidden coupling, duplicated architecture, long-term merge burden, and support ambiguity. Owner-approved maintenance, security-response, and rollback plans are required.

## Option C: Upstream-First Collaboration

Public claim:

Turing collaborates with Servo upstream on shared research or patches while keeping Turing's release boundary independent until a later ADR accepts release-path code.

Unsupported behavior:

Upstream collaboration is not source adoption, redistribution approval, support delegation, or compatibility transfer.

Required updates:

- Add upstream contribution policy, patch ownership, review expectations, issue routing, disclosure coordination, and fork/branch hygiene.
- Update legal/community ownership records and CODEOWNERS-like review expectations.
- Define how upstream changes are mirrored into Turing evidence without importing unreviewed code.
- Keep public status language clear that upstream activity does not create a supported Turing browser.

Residual risk:

Coordination may consume time without reducing implementation risk. Security and maintenance obligations remain Turing-owned for any Turing release.

## Option D: Servo-Derived Engine

Public claim:

Turing changes direction to build a Servo-derived engine or browser. This conflicts with the current independent-engine posture unless the charter and dependent requirements are changed.

Unsupported behavior:

No such claim is allowed until the charter, JavaScript runtime, dependency, security, support, release, and maintenance records are rewritten and approved. Existing independent-engine claims would be stale.

Required updates:

- Supersede or rewrite `ADR-0002`, `ADR-0004`, `REQ-ENG-007`, the charter, technology stack, roadmap, architecture, requirements, risks, and definition of done.
- Accept full source/dependency provenance, license, advisory, SBOM, native-package, generated-output, unsafe, FFI, JavaScript-runtime, security, sandbox, compatibility, performance, and maintenance obligations.
- Define supported platforms, upstream baseline, fork policy, patch policy, release process, update/signing model, vulnerability response, support horizon, and rollback plan.
- Rewrite public copy so it no longer implies a from-scratch independent implementation.

Residual risk:

This is a product and governance change, not just an implementation shortcut. It may violate existing positioning and produce major maintenance obligations.

## Option E: Explicit Servo Browser Charter Change

Public claim:

Turing becomes a Servo-focused browser project, research distribution, or collaboration vehicle.

Unsupported behavior:

The current independent-browser and independent-engine claims would no longer apply. Any everyday-user, developer-first, AI-agent, performance, memory, compatibility, or security positioning must be rebuilt from evidence.

Required updates:

- Rewrite charter, market strategy, product requirements, competitive positioning, risks, roadmap, support policy, contribution model, and release operations around a Servo-first identity.
- Decide whether Turing is a distribution, fork, shell, component host, tooling layer, or research program.
- Establish upstream governance, branding, trademark, legal, security, release, and support boundaries before public launch language changes.
- Rebaseline every build-readiness gate against the new charter.

Residual risk:

This option may simplify identity but discards much of the current source-strategy premise. It needs explicit owner approval and likely broader stakeholder review.

## Support-Language Baseline

Until `ADR-0009` is accepted, use this support language:

Turing has no supported browser release. Security reports are handled on a research best-effort basis. No patch-time guarantee, compatibility guarantee, performance guarantee, update channel, binary support horizon, or production support statement is active.

After any accepted `ADR-0009` outcome, the support statement must name:

- supported and unsupported platforms;
- supported and unsupported source/components;
- vulnerability reporting and response owners;
- patch and update expectations;
- private-data and hostile-browsing limits;
- dependency and upstream-response limits;
- expiration date for any preview or exception.

## Remaining Owner Actions

`ADR9-EV-017` can use this file as partial evidence because it names the required claim boundaries, support language, residual risks, and document/registry diff template for each option.

`ADR9-EV-018` remains blocked. An owner must select, reject, or supersede the options; approve any time-bounded exceptions; replace the checked no-claim decision-review template with a real owner-reviewed record; and assign post-decision work packages before `PB-002` can move out of blocked status.
