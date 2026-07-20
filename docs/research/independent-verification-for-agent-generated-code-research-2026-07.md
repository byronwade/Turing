# Independent Verification for Agent-Generated Browser Code Research - July 2026

Status: active `RQ-60` research packet; no verification, security, accessibility, performance, or release claim
Owner: quality, security, architecture, accessibility, performance, release operations, agent operations, and independent reviewers
Research date: 2026-07-20
Question: Which combinations of separate agents, human review, conformance suites, fuzzing, formal/model tests, fixed-hardware measurement, and accessibility evaluation provide sufficiently independent evidence?

This packet consolidates the [Independent Verification and Adversarial Review](../agent-execution/08-independent-verification-and-adversarial-review.md) baseline with the agent task model and the quality, security, accessibility, benchmark, incident, and release routes. It does not certify any current implementation or treat the current M0 prototype as browser evidence.

## Source observations

The linked evidence policy treats independence as a relationship between implementation, oracle, fixtures, reviewer authority, and acceptance decision rather than as a second command or model invocation. It also requires attempted failures, unsupported cases, common-mode overlap, environment identity, retained artifacts, reviewer disposition, expiry, and rerun triggers to remain visible. These are observations about the repository's verification contract; they are not evidence that any current task, browser subsystem, or release path has been independently verified.

## Independence model

Independence is a property of an evidence relationship, not a job title or a second command invocation. Each evidence item must record:

- the exact implementation revision, task manifest, authoring agent or human, model/tool version, prompt/context boundary where relevant, and environment;
- the verifier identity, authority separation, source of fixtures/oracles, and whether the verifier could modify the implementation or acceptance criteria;
- the failure mode being tested, the oracle, input generation method, seed or corpus identity, resource/time limits, and retained artifacts;
- the overlap between implementation and verification code, data, assumptions, generated outputs, dependencies, and environment;
- the review result, unresolved findings, re-run trigger, expiry, and claim boundary.

An independent test may be run by the same executable only when the oracle, fixture source, and acceptance decision are demonstrably independent; a separate process or agent alone is not sufficient.

## Evidence lanes

| Lane | Independent evidence | Common false inference |
|---|---|---|
| Semantics and compatibility | WPT, Test262, protocol suites, reduced normative tests, differential oracles, and complete pass/fail/unsupported denominators | A unit test or one engine result proves web compatibility |
| Security and authority | Threat-model delta, malformed/oversized/stale/replay/unauthorized cases, fuzzing, sanitizers, Miri where applicable, sandbox/process negative tests, and exploit-chain review | A happy-path test or static policy name proves containment |
| State and model behavior | State-machine/model/property tests, generated transitions, invariant checks, crash/restart/cancellation/recovery cases, and minimized counterexamples | A snapshot or example workflow proves lifecycle correctness |
| Performance and resources | Fixed hardware/OS controls, version-pinned workloads, raw samples, traces, resource attribution, statistical analysis, and independent claim review | A local timing or benchmark harness self-test proves speed or Chrome-class performance |
| Accessibility | Automated semantics plus keyboard, focus, IME, high-contrast/forced-color, reduced-motion, and qualified assistive-technology workflows with transcripts | A semantic tree, screenshot, or automated checker proves accessibility |
| Release and operations | Clean-host rebuild/replay, provenance, signatures, install/update/rollback/migration/crash recovery, incident rehearsal, support and owner review | A passing repository check proves release readiness |

The lanes are complementary. A security review does not replace accessibility or performance evidence; a conformance suite does not replace hostile-input testing; a human approval does not replace missing artifacts.

## Agent-specific controls

Agent-authored tests, generated fixtures, prompts, summaries, and acceptance statements are evidence inputs whose provenance must be retained. The implementation agent must not:

- define its own acceptance criteria as the only oracle;
- approve or merge its own work;
- suppress failures, unsupported rows, timeouts, flaky results, or contradictory evidence;
- widen task scope, capabilities, data access, or release claims through test output or model interpretation;
- substitute a self-review, another invocation of the same model, or a passing smoke test for independent review.

A separate agent can assist verification only when the task manifest grants bounded authority, the verifier's inputs and oracle are independently sourced, and a human or independent reviewer accepts the evidence. The same model family or repository context is a residual common-mode risk and must be recorded.

## Evidence packet sequence

1. Freeze the implementation revision, task scope, requirements, risks, threat model, supported workflow, and prohibited claims.
2. Select at least one independent oracle or fixture source for every acceptance property; identify common-mode failure risks.
3. Run negative, malformed, timeout, cancellation, resource-exhaustion, crash/restart, recovery, and unsupported cases, retaining every attempted outcome in the denominator.
4. Run separate semantic, security, state/model, accessibility, performance/resource, and release lanes as applicable to the claim.
5. Compare raw evidence to the declared oracle, classify failures, minimize reproducible cases, and record environment and tool differences.
6. Obtain independent review of implementation, evidence, claim wording, residual risk, and exceptions; the reviewer must not silently repair the implementation.
7. Synchronize task, evidence bundle, requirements, risks, readiness, SLO, support, release, and owner records, including expiry and rerun triggers.

The next acceptable artifact is a task-scoped evidence bundle with independent verifier identity, oracle provenance, complete denominators, raw artifact hashes, failure classification, and reviewer disposition. The current M0 tests and `check.ps1` are repository evidence only; they do not satisfy browser-level independent verification.

## Current disposition

`RQ-60` remains active in the pre-build research crosswalk. This packet clarifies the independent-evidence route without accepting a task, promoting a gate, or changing the `90%` contained-M0 / `0%` full-build measures.

## Source records

- [Independent Verification and Adversarial Review](../agent-execution/08-independent-verification-and-adversarial-review.md)
- [Agent Execution and Production Readiness Audit](agent-execution-production-readiness-audit-2026-07.md)
- [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md)
- [Benchmark Evidence and Claim Closure Preparation](benchmark-evidence-and-claim-closure-preparation-2026-07.md)
- [Native UI and Accessibility Closure Preparation](native-ui-and-accessibility-closure-preparation-2026-07.md)
