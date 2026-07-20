# Project Controls and Review System Research - July 2026

Status: active `RQ-45` source-backed project-control route; no governance, review, task-authority, gate, security, release, or production claim
Owner: program, architecture, quality, security, documentation, release operations, and subsystem owners
Research date: 2026-07-19
Related questions: `RQ-45`, `RQ-47`, `RQ-48`, `RQ-60`
Related gates: `PB-019`, `PB-020`

## Question

Which ownership, review, traceability, phase, exception, and evidence controls reduce defects without blocking legitimate work or allowing unsafe shortcuts?

This packet defines a research and review route. It does not approve the current governance model, name qualified owners, authorize tasks, or promote any readiness gate.

## Source-backed observations

### Technical controls need lifecycle integration

NIST SP 800-218 treats secure development as lifecycle practices that must be integrated into the development model, rather than as a single security review at the end. The control system must therefore connect planning, design, implementation, testing, provenance, vulnerability response, and release rather than treating security as an isolated sign-off.

### Configuration management preserves the known product

NASA systems-engineering guidance describes configuration management as controlling baseline changes, tracking those changes, preserving a true product representation, and keeping product information consistent with the approved design. For Turing, the baseline includes source, generated outputs, schemas, dependencies, toolchain, test corpus, evidence, documentation, support scope, and release metadata.

### Review controls need explicit enforcement and bypass visibility

GitHub documents that protected branches can require pull-request reviews and status checks, while rulesets can target branches or tags and expose active rules to readers. GitHub also documents that bypass actors can be granted explicit authority. These mechanisms are repository controls, not proof that the project has selected the correct reviewers or that evidence is independently valid.

The project must record who can approve, who can bypass, why bypass exists, how it is audited, and which changes are never bypassable. “Protected branch enabled” is not equivalent to independent review or owner coverage.

## Control objectives

The control system should provide:

- clear authority boundaries for program, architecture, security, quality, release, legal, support, and subsystem owners;
- stable IDs and bidirectional traceability from requirement and risk through design, task, source, test, evidence, review, gate, release, and support;
- phase gates that define entry, exit, evidence, owner decisions, exceptions, and prohibited claims;
- task manifests that limit scope, preserve predecessors, name evidence bundles, and prevent self-approval or authority expansion;
- review rules that require the right independent scopes, reject stale approvals where applicable, and make bypass actors visible;
- exception records with owner, independent reviewer, rationale, risk, compensating controls, expiry, rollback, affected support boundary, and prohibited claims;
- configuration control for source revisions, generated output, dependencies, toolchain, schemas, test corpora, benchmark identities, and documentation;
- evidence controls that preserve exact identity, environment, configuration, workload, result, artifact hashes, reviewer, limitations, access classification, and freshness;
- a stop/replan path that pauses unsafe or unowned work while allowing bounded no-claim research and recovery work to continue;
- measures that expose review latency, queue age, stale records, false approvals, bypass use, exception debt, and control burden.

## Control classes

| Class | Required control | Failure that must block |
|---|---|---|
| Authority | named owner, independent reviewer, backup, role scope, and no self-approval | actor approves own task, evidence, gate, release, signing, disclosure, or exception |
| Scope | task manifest, predecessor gates, affected IDs, allowed paths, and no-claim boundary | task silently expands from research to implementation or from contained M0 to broad build |
| Baseline | exact source/build/schema/dependency/toolchain/corpus identity and change record | evidence cannot be tied to the product configuration it describes |
| Verification | planned checks, actual tests, negative/failure/recovery cases, raw artifacts, and independent disposition | passing check proves the wrong behavior or planned evidence is treated as actual evidence |
| Review | required scopes, review freshness, latest-push coverage, conflict/recusal, and review record | stale or common-mode approval remains active after material change |
| Exception | owner, reviewer, risk, compensating controls, expiry, rollback, support impact, and prohibited claims | exception is indefinite, unowned, or used to erase a predecessor gate |
| Gate | explicit entry/exit criteria, evidence status, decision record, and promotion authority | template, validator, or task manifest is treated as gate acceptance |
| Release | artifact identity, signing/update authority, rollback, supported scope, and incident path | release or production claim lacks recovery and response capacity |
| Recovery | stop, rollback, quarantine, replan, and escalation actions with owners | failed check or incident leaves the system in an ambiguous status |

## Phase model

Every phase should distinguish:

1. **Research:** question, sources, alternatives, method, limits, and next proof.
2. **Specified:** stable requirement/design/risk/control records exist.
3. **Task-ready:** predecessors, owner, reviewer, scope, evidence classes, and no-claim boundary are approved for task shaping.
4. **In execution:** source changes, tests, artifacts, failures, and status are retained against an exact task and commit.
5. **Review-pending:** independent review may accept, reject, or request rework; the author cannot convert this state to accepted.
6. **Accepted:** the owner and independent reviewer record the decision and synchronize affected records.
7. **Release-gated:** release-specific evidence, support boundary, incident/update path, and promotion authority are present.
8. **Supported:** ongoing capacity, refresh cadence, response terms, and end-of-life boundaries are accepted.

No phase transition may be inferred from a merged commit, a green check, a completed template, or a passing local self-test.

## Exception and bypass protocol

An exception or bypass record must state:

- exact scope, affected records, configuration, and time window;
- initiating reason and evidence of the underlying failure or constraint;
- named owner and independent reviewer with recusal handling;
- risk linkage, compensating controls, monitoring, and residual risk;
- expiry, renewal authority, rollback/removal action, and support/release impact;
- explicit claims and gate transitions that remain prohibited;
- audit record of use, outcome, cleanup, and follow-up work.

Reject any bypass that changes authority, hides a failed check, permits self-approval, suppresses security/accessibility/recovery evidence, removes a required reviewer without equivalent independence, or has no expiry and rollback path.

## Measurement and falsifiable evaluation

Evaluate candidate control systems on a representative change corpus containing documentation-only, source, schema, dependency, IPC, sandbox, UI/accessibility, benchmark, profile/migration, update, incident, and release changes. Measure:

- escaped defects and late-discovered requirement/design inconsistencies;
- time from change proposal to authorized execution and from failure to safe recovery;
- review latency, queue age, stale approval rate, rework rate, bypass frequency, and exception age;
- orphaned/dangling trace edges, status contradictions, stale evidence, unowned paths, and unsupported claims found;
- false-block rate for bounded safe work and missed-block rate for deliberately invalid changes;
- human comprehension of phase, authority, exception, and claim status across maintainers.

Adversarial fixtures must include forged approvals, changed commits after review, missing code owners, bypassed status checks, expired exceptions, duplicated IDs, deleted evidence, wrong task scope, agent self-approval, hidden generated changes, stale toolchain facts, and release artifacts with mismatched source identity.

## Rejection and promotion rules

Reject a control system when it relies on social convention rather than enforceable or auditable records, cannot distinguish planned from actual evidence, permits self-approval, hides bypass authority, allows unexpired exceptions to accumulate, loses configuration identity, or blocks urgent recovery without a controlled path.

Promote a control only after a bounded trial demonstrates the required negative cases, independent review, measurable false-block/missed-block behavior, traceability synchronization, and recovery. A control that passes its own validator is not thereby effective against a compromised or mistaken actor.

## Current status and claim boundary

`RQ-45` is active in the readiness crosswalk. This packet closes a research-route and control-definition gap only. It does not approve governance, task authority, branch protection, reviewer sufficiency, owner coverage, phase-gate readiness, release authority, security, or production status. The current `90%` contained-M0 / `0%` full-build closure metrics remain unchanged.

## Next question

Which first adversarial control trial should test a proposed task, review, exception, and gate-promotion path, and what failure must prevent the system from advancing?

## Sources

- [NIST SP 800-218: Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [NASA: Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/)
- [NASA: Systems Engineering Technical Management Processes](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL)
- [GitHub: Managing protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub: About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [GitHub: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
