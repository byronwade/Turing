# Compatibility Prioritization and Closure Preparation - July 2026

Status: no-claim compatibility-prioritization and evidence handoff
Owner: compatibility, web-platform, quality, security, accessibility, performance, and product owners
Primary question: `RQ-15`
Related gates: `PB-002`, `PB-013`, `PB-020`
Related work: `WP-006` through `WP-013`, `TASK-000001`, `TASK-000005`
Research date: 2026-07-19

## Purpose

This packet defines how Turing should prioritize compatibility work and report compatibility evidence without turning a feature list, a single site, or a pass-rate slice into a Chrome-class claim. It complements the [Chrome-Class Capability Traceability Map](chrome-class-capability-traceability-map-2026-07.md), [Web-Platform Source and Conformance Evidence](web-platform-source-and-conformance-evidence-2026-07.md), [capability parity matrix](../blueprint-v1/02-capability-parity.md), and [testing and compatibility chapter](../blueprint-v1/12-testing-compatibility.md). It does not select an implementation feature, establish browser compatibility, approve a source baseline, or authorize a task.

## Source-backed observations

- The [web-platform-tests project](https://github.com/web-platform-tests/wpt) is a cross-browser suite whose value depends on a pinned revision, harness, test selection, environment, and retained results. Its tooling includes manifest generation and browser execution; a repository checkout alone is not a Turing result.
- WPT's [expectation metadata](https://web-platform-tests.org/tools/wptrunner/docs/expectation.html) distinguishes expected outcomes, intermittent outcomes, disabled tests, and configuration conditions. Expected failures and flaky outcomes therefore need explicit classification and cannot be silently removed from a denominator.
- WPT's [local-run documentation](https://web-platform-tests.org/running-tests/from-local-system.html) describes storing and loading expected results for regression tracking. Turing must retain the raw report and the expectation revision used for each run.
- Test262 is the ECMAScript conformance suite associated with the [ECMAScript specification](https://tc39.es/ecma262/). Its results must remain separate from host APIs, browser integration, and performance measurements.
- The [Interop project](https://wpt.fyi/interop) provides shared prioritization and cross-implementation context, but it is not a complete Turing support contract or a substitute for Turing-owned failure accounting.

These observations establish an evidence shape, not a compatibility result.

## Prioritization model

Every capability row should be assigned one planning priority before implementation scope is proposed:

| Priority | Meaning | Required treatment |
|---|---|---|
| `P0-release-critical` | A failure would break core navigation, security boundaries, data safety, accessibility, or a primary supported workflow. | Must have an owner, normative source, executable tests, negative tests, failure triage, unsupported behavior, and a release-gate decision before the affected support claim. |
| `P1-high-value` | A capability is important to common sites, developer workflows, or cross-browser interoperability but is not a prerequisite for every supported workflow. | Must have a pinned test route, explicit support statement, regression tracking, and an owner before entering a supported profile. |
| `P2-experimental` | A capability is useful, emerging, platform-specific, proprietary, or not yet justified for the current support profile. | Remains explicitly unsupported or experimental until a feature-promotion packet supplies user need, standards/interoperability context, security/privacy/accessibility review, and rollback or deprecation rules. |

Priority is not a pass threshold. An unimplemented `P0` row remains a blocker for the corresponding profile; a passing `P1` row does not compensate for a failed `P0` row.

## Required capability row

The canonical capability-parity row and its evidence packet must identify:

- stable capability ID and domain;
- user workflow and supported-profile relevance;
- normative specification and exact revision or retrieval identity;
- WPT, Test262, WebDriver BiDi, local-corpus, accessibility, security, or other test identifiers;
- implementation surfaces and dependencies, including process, IPC, storage, UI, and native-platform effects;
- platform, locale, input, assistive-technology, and feature-configuration conditions;
- priority, maturity state, owner, independent reviewer, and next decision;
- denominator inclusion rules for pass, fail, timeout, crash, leak, harness error, not-run, disabled, expected failure, and unsupported outcomes;
- raw artifact paths and hashes, harness version, environment, source/test commits, local patches, and expectation metadata;
- known differences, user-visible limitation, security/privacy/accessibility consequences, and rollback or deprecation path;
- claim scope: supported, experimental, unsupported, or not evaluated.

No row may use “works in Chrome,” a site-specific success, or a feature name as a substitute for this evidence.

## Evidence order

1. Define the supported product profile, platforms, locales, input modes, and primary workflows.
2. Partition capability rows into `P0`, `P1`, and `P2`; record the rationale and owner without treating the priority as a result.
3. Pin normative sources, suite commits, harnesses, local patches, browser/reference versions, and test manifests.
4. Generate the complete denominator before execution, including disabled, expected, excluded, and not-run rows with reasons.
5. Execute WPT, Test262, protocol, accessibility, security, and Turing-owned corpus tests under the declared profile; retain raw reports and failure artifacts.
6. Run differential comparisons where useful, then resolve disagreements against the normative source rather than majority behavior.
7. Classify every failure as implementation defect, harness/environment failure, known interop difference, unsupported feature, expected failure, flaky result, or untriaged; preserve the original outcome and denominator.
8. Review cross-domain effects on origin policy, process isolation, storage, credentials, accessibility, resource use, privacy, and agent authority.
9. Require owner and independent-review disposition before changing a capability from specified or prototype to conformant-subset, release-gated, or supported.
10. Synchronize the parity matrix, requirements, risks, work package, task manifest, support statement, claim bundle, and dashboard in one change.

## Rejection rules

Reject a compatibility claim or promotion when:

- the test tree, browser version, harness, expectation metadata, or environment is unpinned;
- failures, crashes, timeouts, leaks, harness errors, disabled tests, or not-run rows are omitted from the denominator;
- a smaller suite, selected website list, user-agent override, or hidden compatibility intervention is presented as general compatibility;
- a reference-engine disagreement is treated as the normative answer without specification or standards review;
- security, privacy, accessibility, data recovery, or resource-exhaustion consequences are excluded from the capability row;
- a proprietary service, codec, DRM module, extension store, account system, or platform integration is represented as open-web parity without an explicit external-dependency boundary;
- a validator, source manifest, research report, or proposed task is treated as an execution result or owner approval.

## Current handoff

The repository now has a concrete compatibility-prioritization and closure route for `RQ-15`, while the following remain missing:

- an owner-selected supported profile and `P0`/`P1`/`P2` assignments;
- pinned WPT, Test262, protocol, accessibility, security, and local-corpus runs;
- a generated denominator and retained raw artifacts;
- differential and standards-based triage;
- owner-reviewed support statements and claim bundles.

The next executable proof is a reviewed capability-row manifest for one narrowly scoped profile after source strategy, task authority, and the relevant engine/security prerequisites are accepted. Until then, `PB-002`, `PB-013`, and `PB-020` remain unresolved.

## Claim boundary

This packet improves compatibility planning and handoff organization only. It does not establish HTML, DOM, CSS, ECMAScript, WPT, Test262, WebDriver BiDi, accessibility, security, performance, Chrome-class, production, or daily-driver readiness.
