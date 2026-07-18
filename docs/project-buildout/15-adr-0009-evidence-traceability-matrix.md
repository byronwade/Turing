# ADR-0009 Evidence Traceability Matrix

Status: operating traceability matrix; no source-strategy decision
Owner: architecture, engine, security, provenance, release operations, quality, performance, compatibility, embedding, and documentation owners
Last updated: 2026-07-18

## Purpose

This matrix turns the current Servo/source-strategy evidence into a continuation queue for `ADR-0009`. It connects the blocked `PB-002` readiness gate to the exact evidence reports, missing outputs, owner scopes, and acceptance checks needed before any Servo relationship can be accepted, rejected, or superseded.

This document does not approve Servo, Stylo, WebRender, SpiderMonkey, GStreamer, moztools, `servo-build-deps`, or any transitive dependency for Turing release code. It does not authorize copying Servo source into this repository. The machine source of truth for readiness status remains [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json); the executable `ADR9-EV-*` status companion is [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json); the narrative packet remains [ADR-0009 Source Strategy Decision Packet](14-adr-0009-source-strategy-decision-packet.md).

## Status Legend

- **Captured:** local evidence exists for the named scope, but may still need owner review.
- **Partial:** useful evidence exists, but the evidence does not cover the required decision scope.
- **Missing:** no decision-grade evidence exists yet.
- **Owner review required:** evidence may exist, but the accountable owner has not accepted, rejected, or time-bounded an exception.
- **Blocked:** a predecessor must complete before this item can be decided.

## Current Verdict

`PB-002` remains blocked. The current evidence proves a clean external Servo checkout can be bootstrapped and built on the reference Windows host and that several source, dependency, generated-code, native-bootstrap, unsafe, and FFI surfaces are now mapped. It does not prove source approval, dependency approval, compatibility, performance, maintenance viability, legal clearance, or architectural fit with Turing's independent-engine and Turing-owned JavaScript-runtime decisions.

## Evidence Matrix

| ID | Decision area | Status | Existing evidence | Missing decision-grade output | Owner scope |
|---|---|---|---|---|---|
| `ADR9-EV-001` | Source identity and checkout trust | Partial | second Windows preflight; [source/archive provenance audit](../research/servo-source-archive-provenance-audit-2026-07.md); [upstream source provenance report](../research/servo-upstream-source-provenance-2026-07.md); [independent source verification](../research/servo-independent-source-verification-2026-07.md); [source-baseline equivalence policy prep](../research/servo-source-baseline-equivalence-policy-2026-07.md) | owner-selected source baseline, signed-tag or equivalent provenance decision, owner-accepted equivalence policy, full blob/legal review for the selected baseline, rerun plan if selected baseline differs from the current build baseline | architecture, supply-chain |
| `ADR9-EV-002` | Reference build reproduction | Partial | second Windows preflight; bootstrap and build logs outside repo; [source strategy inventory](../research/servo-source-strategy-inventory-2026-07.md); [build reproduction evidence and replay-protocol draft](../research/servo-independent-build-reproduction-2026-07.md) | owner acceptance of the replay protocol, clean-target reproduction on an independent host or VM, target/cache isolation replay, success and failure log bundle | release-operations, quality |
| `ADR9-EV-003` | Cargo dependency and SBOM posture | Partial | [dependency/provenance inventory](../research/servo-dependency-provenance-inventory-2026-07.md); [supply-chain policy scan](../research/servo-supply-chain-policy-scan-2026-07.md); [license/advisory/SBOM decision prep](../research/servo-license-advisory-decision-prep-2026-07.md) | owner-selected SBOM format and toolchain, full SBOM for the selected source baseline and feature profile, yanked/advisory snapshot with timestamps, duplicate-version decisions, generated-output/native-package inclusion rules | security, supply-chain, legal-community |
| `ADR9-EV-004` | Turing license, notice, patent, and source-offer decisions | Partial | [license/advisory/SBOM decision prep](../research/servo-license-advisory-decision-prep-2026-07.md); Servo's own `cargo-deny` result under Servo policy; native GStreamer license-surface counts in native audits | Turing license acceptance list, third-party notices, source-offer obligations, codec and patent review, native license review, accepted exceptions | legal-community, release-operations |
| `ADR9-EV-005` | Native bootstrap source-build or binary-package exceptions | Partial | [native bootstrap provenance audit](../research/servo-native-bootstrap-provenance-audit-2026-07.md); [native package decision prep](../research/servo-native-package-decision-prep-2026-07.md) | source-build recipes or explicit binary-package exception records for GStreamer, moztools, MSYS2-derived tools, codec/crypto libraries, `servo-build-deps`, ANGLE outputs, platform redistributables, package-minimization decisions, final manifests, and owner approvals | release-operations, security, legal-community |
| `ADR9-EV-006` | Deterministic native download verification | Partial | upstream asset hashes and signature posture in native bootstrap audit; deterministic-download policy proposal in native package decision prep | accepted hash/signature/mirror policy, revocation and freshness rule, bootstrap verification implementation, independent replay result | release-operations, security |
| `ADR9-EV-007` | Generated-output determinism and provenance | Partial | [build-script/generated-output audit](../research/servo-build-script-generated-output-audit-2026-07.md); [clean generated-output reproduction probe](../research/servo-clean-generated-output-reproduction-2026-07.md) | feature-correct full clean-target regeneration diff beyond the package-scoped dummy-media probe, independent-host comparison, generator manifest, source-to-output license/provenance mapping | engine, supply-chain, quality |
| `ADR9-EV-008` | Registry, git, and path build-script and proc-macro side effects | Partial | [generated/native/unsafe/FFI classification](../research/servo-generated-native-unsafe-classification-2026-07.md); [build-script/generated-output audit](../research/servo-build-script-generated-output-audit-2026-07.md); [build-script/proc-macro side-effect audit](../research/servo-build-script-proc-macro-side-effect-audit-2026-07.md) | selected baseline/profile/component boundary, accepted side-effect policy, dynamic tracing for filesystem/process/network/time/env/compiler/linker/native-copy actions, proc-macro provenance and expansion-risk review, owner approval | security, release-operations, engine |
| `ADR9-EV-009` | Unsafe-code review | Partial | heuristic unsafe counts and clusters in generated/native/unsafe/FFI classification; [unsafe and FFI contract review](../research/servo-unsafe-ffi-contract-review-2026-07.md) | block-level unsafe inventory with `SAFETY:` coverage, invariants, owner, tests, fuzz/sanitizer/Miri evidence, release relevance | security, engine |
| `ADR9-EV-010` | FFI and ABI contracts | Partial | FFI/export/link marker inventory in generated/native/unsafe/FFI classification; [unsafe and FFI contract review](../research/servo-unsafe-ffi-contract-review-2026-07.md) | C API and platform ABI contracts, lifetime/threading/panic policy, C conformance tests, header/source provenance | embedding, security, engine |
| `ADR9-EV-011` | Candidate component boundaries | Partial | ADR packet option scorecard; dependency and unsafe clusters; [component-boundary and JavaScript conflict analysis](../research/servo-component-boundary-analysis-2026-07.md) | owner-selected ADR-0009 option, source baseline, feature profile, target platform, per-option release-path dependency-closure reports with normal/build/dev/target separation, in/out component lists, accepted APIs, generated-output policy, replacement contracts, SpiderMonkey/Stylo/WebRender/GStreamer reachability decision, owner-reviewed maintenance boundaries | architecture, engine |
| `ADR9-EV-012` | JavaScript-runtime conflict analysis | Partial | accepted `ADR-0004`; Servo metadata showing default `js_jit` and MozJS/SpiderMonkey cluster; [component-boundary and JavaScript conflict analysis](../research/servo-component-boundary-analysis-2026-07.md) | owner-reviewed option-by-option JavaScript impact decision, no-JIT proof and SpiderMonkey dependency analysis, Web IDL replacement or supersession plan, GC/wrapper/realm/cross-origin identity model, debugger/DevTools impact decision, Test262 strategy that attributes the actual runtime | javascript, architecture |
| `ADR9-EV-013` | Compatibility corpus and WPT/Test262 evidence | Partial | successful external `servoshell.exe` build; [local compatibility corpus and WPT/Test262 evidence](../research/servo-local-compatibility-corpus-2026-07.md); checked [local compatibility corpus manifest](../blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json); checked [HTTPS host-alias harness plan](../blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json); generated local fixture root under `benchmarks/compatibility/adr0009/no-claim-tiny/`; checked validators in `tools/validate_servo_local_compatibility_corpus.py` and `tools/validate_servo_local_compatibility_https_harness.py`; checked HTTP route self-test in `tools/serve_servo_local_compatibility_corpus.py` | HTTPS harness execution and host-alias browser run for the checked fixtures, tiny local corpus browser runs with raw logs, certificate fingerprints, host-alias cleanup proof, route artifacts, and hashes, focused WPT subset run for the selected ADR-0009 option, disabled-test/expected-failure/timeout/crash/unsupported-API accounting, failure denominator, flakiness policy, separate Turing Test262 harness plan for `ADR-0004` | quality |
| `ADR9-EV-014` | Fixed-hardware performance and memory baseline | Partial | reference host hardware recorded in preflight; [performance benchmark readiness packet](../research/performance-benchmark-readiness-packet-2026-07.md); [semantic resource attribution taxonomy](../research/semantic-resource-attribution-taxonomy-2026-07.md); [Servo performance baseline preparation](../research/servo-performance-baseline-2026-07.md) | runner-generated local corpus baseline with raw samples and artifact hashes, owner-approved fixed-host hardware and OS image manifest, process/site-isolation disclosure, lifecycle state, browser-emitted private working set/resident/committed/shared/compressed/swap/semantic-owner/GPU memory data, startup/input/frame pacing/CPU/wakeup/energy measures, equal-security/equal-workload comparison denominator | performance, release-operations |
| `ADR9-EV-015` | Security model and sandbox implications | Partial | generated/native/unsafe/FFI and native-bootstrap risk notes; [security and maintenance implications](../research/servo-security-maintenance-implications-2026-07.md) | owner-reviewed process authority map for each option, Windows/macOS/Linux sandbox boundary delta with effective-policy evidence, negative sandbox tests for file/socket/process/registry/device/debug/shared-memory/profile/credential/IPC access, site/profile/origin/browsing-context-group/service-worker/storage/cookie/cache/DevTools/extension/agent identity review, native/media/GPU/JavaScript runtime/JIT/WebDriver/Bluetooth/update risk review, fuzzing/sanitizer/crash/memory-corruption/compromised-process evidence for any accepted component boundary | security, architecture |
| `ADR9-EV-016` | Maintenance and upstream relationship model | Partial | Servo public activity and LTS notes in source inventory; [security and maintenance implications](../research/servo-security-maintenance-implications-2026-07.md) | patch ownership for each option, upstream cadence and selected-baseline policy, LTS/security-response split between upstream and Turing, merge burden estimate, breakage/rollback/source-refresh handling, named primary and backup owners plus reviewer/release/security/legal-community owners | program, architecture |
| `ADR9-EV-017` | Public claims, requirements, risks, and support impact | Partial | current docs prohibit Servo adoption claims and Chrome-class claims; [decision draft and public-claim impact](16-adr-0009-decision-draft.md) | owner-selected option, owner-applied document and registry diff, final unsupported behavior, final residual risk, final support language, final claim boundaries | documentation-research, product, program |
| `ADR9-EV-018` | ADR-0009 decision and review | Blocked | ADR packet template, evidence reports, decision draft, checked no-claim [decision-review template](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json), and [decision-review schema](../blueprint-v1/machine/adr-0009-decision-review.schema.json) | accepted/rejected/superseded ADR text, owner approvals, rejected options, time-bounded exceptions, post-decision work packages, and real decision-review record beyond the checked no-claim template | architecture, program |

## Continuation Queue

Use this order unless an owner deliberately reprioritizes the work:

1. Complete `ADR9-EV-001` and `ADR9-EV-002` so all later evidence is tied to a selected source baseline and reproducible build environment.
2. Complete `ADR9-EV-003` through `ADR9-EV-006` before any dependency, native package, or redistribution decision is considered.
3. Complete `ADR9-EV-007` and `ADR9-EV-008` before trusting generated outputs, build scripts, or proc macros in any candidate component.
4. Complete `ADR9-EV-009` and `ADR9-EV-010` before proposing a Servo component boundary that reaches unsafe or FFI code.
5. Complete `ADR9-EV-011` and `ADR9-EV-012` before scoring selective, upstream-first, Servo-derived, or charter-change options.
6. Complete `ADR9-EV-013` and `ADR9-EV-014` before making compatibility, speed, memory, energy, or Chrome-class inferences.
7. Complete `ADR9-EV-015` and `ADR9-EV-016` before accepting any release-path relationship with Servo or its ecosystem.
8. Complete `ADR9-EV-017` and `ADR9-EV-018` last, after the evidence can support a coherent ADR and synchronized documentation updates.

## Required Output Names

The following filenames are reserved as expected continuation outputs. They are proposals for organization only; creating any of them still requires the usual documentation impact review and validation.

| Output | Primary evidence IDs |
|---|---|
| `docs/research/servo-upstream-source-provenance-2026-07.md` | `ADR9-EV-001` |
| `docs/research/servo-independent-source-verification-2026-07.md` | `ADR9-EV-001` |
| `docs/research/servo-source-baseline-equivalence-policy-2026-07.md` | `ADR9-EV-001` |
| `docs/research/servo-independent-build-reproduction-2026-07.md` | `ADR9-EV-002` |
| `docs/research/servo-license-advisory-decision-prep-2026-07.md` | `ADR9-EV-003`, `ADR9-EV-004` |
| `docs/research/servo-native-package-decision-prep-2026-07.md` | `ADR9-EV-005`, `ADR9-EV-006` |
| `docs/research/servo-clean-generated-output-reproduction-2026-07.md` | `ADR9-EV-007` |
| `docs/research/servo-build-script-proc-macro-side-effect-audit-2026-07.md` | `ADR9-EV-008` |
| `docs/research/servo-unsafe-ffi-contract-review-2026-07.md` | `ADR9-EV-009`, `ADR9-EV-010` |
| `docs/research/servo-component-boundary-analysis-2026-07.md` | `ADR9-EV-011`, `ADR9-EV-012` |
| `docs/research/servo-local-compatibility-corpus-2026-07.md` | `ADR9-EV-013` |
| `docs/blueprint-v1/machine/servo-local-compatibility-corpus.schema.json` | `ADR9-EV-013` |
| `docs/blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json` | `ADR9-EV-013` |
| `docs/blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json` | `ADR9-EV-013` |
| `docs/blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json` | `ADR9-EV-013` |
| `benchmarks/compatibility/adr0009/no-claim-tiny/` | `ADR9-EV-013` |
| `tools/validate_servo_local_compatibility_corpus.py` | `ADR9-EV-013` |
| `tools/validate_servo_local_compatibility_https_harness.py` | `ADR9-EV-013` |
| `tools/serve_servo_local_compatibility_corpus.py` | `ADR9-EV-013` |
| `docs/research/servo-performance-baseline-2026-07.md` | `ADR9-EV-014` |
| `docs/research/servo-security-maintenance-implications-2026-07.md` | `ADR9-EV-015`, `ADR9-EV-016` |
| `docs/project-buildout/16-adr-0009-decision-draft.md` | `ADR9-EV-017`, `ADR9-EV-018` |

## Acceptance Checks

Before `ADR-0009` can advance, each evidence item must have:

- exact source, version, retrieval date, platform, command, and configuration;
- observations separated from inference and recommendation;
- unsupported behavior and residual risk;
- security, compatibility, accessibility, performance, operational, and legal impact review;
- affected Blueprint chapters, detailed books, requirements, risks, work packages, registries, and indexes updated or explicitly deemed unaffected;
- validation commands rerun and recorded;
- no Servo source, native binary, generated output, registry archive, or build log copied into Turing unless a reviewed task and source/provenance policy explicitly allow it.

## Handoff Rule

A maintainer continuing `PB-002` should update this matrix whenever an evidence item moves from missing to partial, partial to captured, or captured to owner-reviewed. If this matrix disagrees with the machine readiness registry, the registry wins and this matrix is stale.

The same status move must update [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json) in the same change. [`tools/validate_adr_0009_evidence.py`](../../tools/validate_adr_0009_evidence.py) and `tools/validate_blueprint.py` enforce the `ADR9-EV-001` through `ADR9-EV-018` IDs, owner scopes, unresolved-output fields, registry-to-matrix synchronization, existing evidence file paths, and the rule that `PB-002` remains blocked while the source-strategy decision is unresolved.
