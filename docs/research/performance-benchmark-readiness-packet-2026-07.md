# Performance Benchmark Readiness Packet - July 2026

Status: readiness packet for `PB-013` with checked no-claim benchmark readiness-review template; no owner-reviewed benchmark readiness, browser-run benchmark runner, benchmark result, competitor result, or performance claim
Owner: performance measurement, benchmark operations, architecture, quality, security, accessibility, and release operations
Packet date: 2026-07-17
Confidence: high for evidence requirements; low for implementation readiness until hardware, expanded corpus, runner, and raw-artifact storage exist

## Question

What must exist before Turing can treat performance measurement as build-ready, compare against Chrome-class browsers, or support an extreme-performance claim?

This packet turns the performance Blueprint, benchmark laboratory book, and `PB-013` readiness item into an executable evidence queue. It now also links the checked no-claim [benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json). It does not implement a browser benchmark runner, select final hardware, create a representative corpus, run competitors, provide owner-reviewed benchmark readiness, or move `PB-013` out of `documented_no_runner`.

## Sources and current inputs

Internal inputs:

- [Blueprint 09 - Performance, Memory, Energy, and the 30-Tab Contract](../blueprint-v1/09-performance-memory.md)
- [Fixed-Hardware Benchmark Laboratory](../benchmark-lab/README.md)
- [Browser Performance Engineering](../performance/README.md)
- [Benchmark manifest schema](../blueprint-v1/machine/benchmark-manifest.schema.json)
- [Benchmark corpus schema](../blueprint-v1/machine/benchmark-corpus.schema.json)
- [No-claim smoke corpus manifest](../blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json)
- [Benchmark Corpus Expansion - July 2026](benchmark-corpus-expansion-2026-07.md)
- [Benchmark network profile schema](../blueprint-v1/machine/benchmark-network-profile.schema.json)
- [No-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json)
- [Benchmark Server Lifecycle Self-Test - July 2026](benchmark-server-lifecycle-self-test-2026-07.md)
- [Chrome-Class Performance Runbook - July 2026](chrome-class-performance-runbook-2026-07.md)
- [Benchmark Hardware and OS Manifest - July 2026](benchmark-hardware-os-manifest-2026-07.md)
- [Benchmark OS and Update-Control Manifest - July 2026](benchmark-os-update-control-manifest-2026-07.md)
- [Semantic Resource Attribution Taxonomy - July 2026](semantic-resource-attribution-taxonomy-2026-07.md)
- [Benchmark Competitor Version Manifest - July 2026](benchmark-competitor-version-manifest-2026-07.md)
- [Benchmark Competitor Local Install Inventory - July 2026](benchmark-competitor-local-install-inventory-2026-07.md)
- [Benchmark Browser Pin Capture Contract - July 2026](benchmark-browser-pin-capture-contract-2026-07.md)
- [Benchmark Browser Pin Local Diagnostic Capture - July 2026](benchmark-browser-pin-local-diagnostic-capture-2026-07.md)
- [Benchmark 30-Tab Scenario Contract - July 2026](benchmark-30-tab-scenario-contract-2026-07.md)
- [Benchmark tab scenario schema](../blueprint-v1/machine/benchmark-tab-scenario.schema.json)
- [No-claim 30-tab scenario manifest](../blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json)
- [Benchmark Trace/Artifact Package Contract - July 2026](benchmark-trace-artifact-package-contract-2026-07.md)
- [Benchmark artifact-package schema](../blueprint-v1/machine/benchmark-artifact-package.schema.json)
- [No-claim trace/artifact package plan](../blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json)
- [Benchmark Browser Launch Runner Contract - July 2026](benchmark-browser-launch-runner-contract-2026-07.md)
- [Benchmark launch-runner schema](../blueprint-v1/machine/benchmark-launch-runner.schema.json)
- [No-claim browser launch-runner plan](../blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json)
- [Benchmark browser launch-runner self-test](../../tools/run_benchmark_browser_launch.py)
- [Benchmark readiness-review schema](../blueprint-v1/machine/benchmark-readiness-review.schema.json)
- [No-claim benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json)
- [Benchmark readiness-review validator](../../tools/validate_benchmark_readiness_review.py)
- [Pre-build readiness registry](../blueprint-v1/machine/pre-build-readiness.json)
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md)

External sources checked on 2026-07-17:

- BrowserBench home page: https://browserbench.org/
- Speedometer 3.1 about page: https://browserbench.org/Speedometer3.1/about.html
- Speedometer 3.1 announcement: https://browserbench.org/announcements/speedometer3.1/
- JetStream 3.0 announcement: https://browserbench.org/announcements/jetstream3/
- MotionMark current benchmark page: https://browserbench.org/MotionMark/
- BrowserBench MotionMark about page: https://browserbench.org/MotionMark/about.html
- Chromium Telemetry documentation: https://chromium.googlesource.com/catapult/+/HEAD/telemetry/
- Web Vitals documentation: https://web.dev/articles/vitals
- Chrome UX Report overview: https://developer.chrome.com/docs/crux
- Chrome DevTools Performance reference: https://developer.chrome.com/docs/devtools/performance/reference
- WebPageTest agent JSON test options: https://github.com/catchpoint/WebPageTest.agent/blob/master/docs/test_options.md
- Chrome Releases: https://chromereleases.googleblog.com/
- Windows Performance Toolkit documentation: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/
- Windows Performance Recorder documentation: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder
- Windows Performance Analyzer documentation: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer

The BrowserBench pages are inputs for suite selection, not proof that a single synthetic score is a product result. Chromium, Chrome, Web Vitals, CrUX, DevTools, and WebPageTest sources shape comparison controls and raw-artifact expectations, not Turing results. The Windows Performance Toolkit pages are inputs for the first Windows trace-capture path, not a cross-platform tracing strategy.

## Current posture

What exists:

- performance philosophy, 30-tab contract, and claim discipline in Blueprint 09;
- benchmark-lab book with hardware, corpus, latency, GPU, memory, energy, statistics, artifact, regression, and claim chapters;
- benchmark manifest schema with browser, environment, workload, security, lifecycle, samples, failures, and raw-artifact fields;
- no-claim benchmark manifest sample, raw-artifact index fixture, and validator command for schema-shape enforcement and current hardware-registry cross-checks;
- benchmark corpus schema, no-claim corpus manifest, seven generated local fixtures across static, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract shapes, and corpus validator command for hash and local-only enforcement;
- benchmark network-profile schema, no-claim loopback HTTP/1.1 static profile, route-to-corpus mapping, DNS override contract, cache header contract, unsupported-protocol list, network-profile validator command, repository-owned static-server self-test command, and checked runner-managed server lifecycle self-test package;
- no-claim benchmark smoke runner command that captures the static-server self-test into a temporary artifact package with the current benchmark hardware, OS-control, and resource-attribution registry IDs, file hashes, and explicit unsupported behavior;
- no-claim manifest `claim` metadata plus validator checks that keep claim status explicit before any public result exists;
- benchmark hardware schema, validator, and current high-end Windows Tier H candidate manifest;
- benchmark OS-control schema, validator, and current high-end Windows candidate manifest that records update policy keys, Insider channel, driver/firmware facts, power/display state, time-service failure, service state, unsupported behavior, and missing freeze approvals;
- benchmark resource-attribution schema, validator, and semantic owner taxonomy for memory, CPU, GPU, wakeup, energy, I/O, and agent-cost accounting;
- Chrome-class performance runbook that defines harness-smoke, local-browser-pipeline, competitor-diagnostic, and public-claim-candidate levels;
- checked official release-catalog competitor-version manifest for Chrome, Edge, Firefox, Safari Stable, and Safari Technology Preview; this is not local installed-browser pinning;
- checked current-host local executable inventory for Chrome and Edge with executable paths, file/product versions, hashes, signatures, registry observations, and unresolved version-state caveats; this is not benchmark-ready competitor pinning;
- checked browser-pin capture plan that defines temporary-profile isolation, prohibited real-profile reads/writes, browser-reported version capture, command-line/settings/update/profile artifact requirements, and no-claim rejection rules;
- no-claim browser-pin capture runner self-test that creates and deletes a runner-owned temporary profile marker, writes a hashed artifact package, records prohibited-path checks, and launches no browser;
- current-host no-claim Chrome and Edge browser-pin diagnostic capture with isolated temporary profiles, browser-reported versions, artifact hashes, and cleanup status;
- checked no-claim browser launch-runner contract with planned command path, required and forbidden arguments, registry references, launch stages, sample controls, cache/profile policy, timeout/cancellation policy, failure finalization policy, trace/artifact policy, resource-attribution policy, unsupported behavior, and validator command;
- checked no-browser browser launch-runner self-test that validates command parsing, forbidden argument rejection, checked registry references, artifact-root behavior, no-claim finalization, and explicit no-browser/no-benchmark output;
- checked no-claim 30-tab mixed-state and all-live scenario manifest with lifecycle state counts, corpus references, network-profile coverage, semantic resource-attribution linkage, and validator command;
- checked no-claim trace/artifact package contract with runner-owned root policy, ETW or equivalent trace class, Perfetto-compatible trace class, tab lifecycle log class, required artifact classes, SHA-256 manifest records, redaction/retention rules, prohibited-content rules, and validator command;
- checked no-claim benchmark readiness-review template that ties hardware/OS controls, corpus/network controls, runner/artifact output, browser pins, statistics/denominator controls, claim-bundle review, and owner-reviewed benchmark readiness into one future review shape without approving benchmark-ready status or performance claims;
- competitor version-pinning, synthetic-suite, Web Vitals-style lab metric, and claim-expiry policy drafts;
- M0 Rust workspace and validation commands that can host future benchmark harness crates or tools.

What does not exist:

- no Tier L or Tier M fixed hardware inventory, and no owner-approved Tier H clean-image or replacement decision;
- no clean OS image, approved update freeze, full driver inventory, firmware freeze, normalized display, thermal capture, time-sync control, network isolation, or approved artifact-storage policy;
- no reviewed representative offline corpus beyond the expanded no-claim smoke seed;
- no browser-run server evidence, benchmark-run server artifact beyond the checked runner-managed server lifecycle self-test, DNS override execution outside the self-test Host header, TLS certificate profile, HTTP/2 profile, HTTP/3 profile, proxy profile, authentication mock, cache-revalidation scenario, or latency/loss/bandwidth shaping;
- no browser-run benchmark launch implementation, owner-reviewed benchmark-ready browser pins, scheduler, sample controller, cache controller, or failure collector;
- no runner-generated trace and artifact package root for traces, manifests, logs, screenshots, memory snapshots, raw samples, power data, failure records, and hashes;
- no benchmark-ready competitor baseline for Chrome, Edge, Firefox, Safari, Servo, Ladybird, or other engines;
- no resource-owner instrumentation that emits the checked taxonomy from browser traces, platform counters, UI reports, or runner raw artifacts;
- no accepted claim policy tying performance numbers to compatibility, security, accessibility, failure, and recovery evidence.
- no owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template.

## Benchmark suite baseline

The first benchmark-lab runner should support synthetic suites only as diagnostics:

| Suite | Current source observation | Use in Turing |
|---|---|---|
| Speedometer 3.1 | BrowserBench describes Speedometer 3 as a web-application responsiveness benchmark and the 3.1 announcement as a harness accuracy update | Track web-app responsiveness once Turing can run enough DOM, style, JS, and event-loop behavior to avoid meaningless failure |
| JetStream 3.0 | BrowserBench announced JetStream 3.0 as a JavaScript and WebAssembly suite for computationally intensive modern web workloads | Track JS/Wasm startup, worst-case, and average behavior only after the selected JS/Wasm runtime path is testable |
| MotionMark current `/MotionMark/` page | BrowserBench currently serves MotionMark `1.3.2` from the generic MotionMark URL | Track graphics animation throughput and frame pacing once rendering/compositing exists |
| Windows Performance Toolkit | Microsoft documents WPR and WPA for ETW recording and analysis on Windows | Capture OS-level traces for the Windows reference host; pair with cross-platform trace plans before product claims |

Every run must record the exact suite URL, version, retrieved asset hash when mirrored, browser version, viewport, display refresh, power state, thermal state, cache state, sample count, failures, and unsupported tests. Scores from different suite versions are not interchangeable.

## PB-013 evidence matrix

| Evidence ID | Required output | Current status | Missing proof |
|---|---|---|---|
| `PB13-EV-001` | Fixed hardware inventory for Tier L, Tier M, and Tier H | Partial | checked Tier H current-host candidate manifest records machine ID, CPU, cores, RAM, GPU, display refresh, storage, owner role, and missing controls; Tier L and Tier M manifests plus owner-reviewed Tier H approval or replacement policy remain missing |
| `PB13-EV-002` | OS image and update-control manifest | Partial | checked Tier H current-host hardware and OS-control candidate manifests record Windows caption, version, build, UBR, display version, Insider channel, update policy keys, services, install date, last boot, power scheme, display refresh, timezone, time-service failure, GPU driver, BIOS, and baseboard; clean image, restore procedure, target-version policy, quality update policy, driver exclusion policy, full driver inventory, display normalization, thermal capture, network isolation, approved artifact storage, driver/firmware freeze, and owner review remain missing |
| `PB13-EV-003` | Offline corpus manifest | Partial | no-claim corpus schema, manifest, seven generated local fixtures across static, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract shapes, file hashes, generated-content license notes, expected M0 unsupported behavior, route coverage, and validator exist; the reviewed representative page/app/accessibility/media/hostile/service-worker/international corpus remains missing |
| `PB13-EV-004` | Local server and network profile | Partial | no-claim loopback HTTP/1.1 profile, `turing.invalid` DNS override contract, route-to-corpus mapping, cold-cache/no-store header contract, validator, static-server self-test command, and checked runner-managed server lifecycle self-test with startup, route checks, shutdown, artifact hashes, and no-claim finalization exist; browser-run server evidence, benchmark-run server artifact beyond the lifecycle self-test, DNS execution proof outside the self-test Host header, HTTP/2, HTTP/3/TLS, proxy, authentication mock, cache-revalidation, latency/loss/bandwidth shaping, and benchmark-run evidence remain missing |
| `PB13-EV-005` | Runner design and command contract | Partial | no-claim smoke runner command exists and captures the static-server self-test, current benchmark hardware, OS-control, and resource-attribution registry IDs, runner summary, artifact index, file hashes, and unsupported behavior; checked browser-pin capture plan defines temporary-profile isolation, no-real-profile privacy rules, browser-reported version capture, artifact contract, and validation contract; no-claim browser-pin capture runner self-test creates and deletes runner-owned temp profile evidence, hashes artifacts, and rejects prohibited configured paths; current-host Chrome/Edge diagnostic capture proves the runner can launch each browser with isolated temporary profiles and record browser-reported versions, hashes, and cleanup status; checked no-claim browser launch-runner schema, planned command path, required and forbidden arguments, launch stages, sample controls, cache/profile policy, timeout/cancellation policy, failure finalization policy, trace/artifact policy, resource-attribution policy, unsupported behavior, validator, and checked no-browser browser launch-runner self-test exist; implemented browser benchmark launch runner, sample controller, warmup policy execution, cache reset execution, viewport execution, trace capture, failure capture, cancellation, timeout, cleanup, result finalization, real browser-run artifacts, and negative tests remain missing |
| `PB13-EV-006` | Raw result schema and validator | Partial | schema, a no-claim sample manifest cross-checked against the current Tier H hardware, OS-control, and resource-attribution registry entries, checked raw-artifact index hash, direct validator command, and repository validation hook exist; runner-generated output, trace package, noise/statistics proof, and non-sample artifact storage remain missing |
| `PB13-EV-007` | Trace and artifact package | Partial | checked no-claim trace/artifact package schema, package-root policy, ETW or equivalent trace class, Perfetto-compatible trace class, tab lifecycle log class, required artifact classes, SHA-256 manifest records, redaction/retention rules, prohibited-content rules, and validator exist; runner-generated trace and artifact package root, real ETW or equivalent traces, Perfetto-compatible traces where applicable, logs, screenshots, memory snapshots, power data, raw samples, failure records, redaction review, retention decision, and SHA-256 manifest remain missing |
| `PB13-EV-008` | 30-tab mixed and all-live scenario manifests | Partial | checked no-claim scenario schema, mixed-state manifest, all-live manifest, corpus case IDs, lifecycle state counts, network-profile coverage, semantic resource-attribution linkage, and validator exist; runner-generated concrete tab IDs, navigation order, process topology, site-instance identity, lifecycle transition timestamps, state-transition checks, raw artifacts, revival measurements, and state-loss evidence remain missing |
| `PB13-EV-009` | Competitor comparison method | Partial | [Chrome-class performance runbook](chrome-class-performance-runbook-2026-07.md) defines competitor pinning, suite usage, equal-security/equal-workload controls, and diagnostic comparison levels; checked release-catalog competitor-version schema, manifest, and validator record official current Chrome, Edge, Firefox, Safari Stable, and Safari Technology Preview candidate versions; checked local-install schema, manifest, report, and validator record current-host Chrome and Edge executable paths, hashes, signatures, and unresolved version-state caveats; checked browser-pin capture schema, plan, report, validator, and self-test runner define how browser-reported versions and settings must be captured without real profile access; checked browser-pin diagnostic schema, manifest, report, and validator record current-host Chrome `Chrome/150.0.7871.115` and Edge `Edg/151.0.4129.21` browser-reported versions from isolated temporary profiles; owner-reviewed benchmark-ready pins, channel proof, complete profiles, command lines, settings, Firefox/Safari local install evidence, and run outputs remain missing |
| `PB13-EV-010` | Performance claim gate | Partial | [Chrome-class performance runbook](chrome-class-performance-runbook-2026-07.md) defines claim bundle and expiry policy, and the manifest schema/sample now carry explicit no-claim metadata; no owner-approved claim bundle generated from real results exists |
| `PB13-EV-011` | Semantic resource attribution plan | Partial | checked resource-attribution schema, semantic owner taxonomy, metric list, shared-resource policy, collection-plan fields, UI reporting contract, validator, and no-claim manifest/smoke-runner traceability exist; browser trace instrumentation, per-process collection, per-tab attribution, shared-resource implementation, GPU accounting, unknown-bucket threshold, runner raw artifacts, and UI/reporting fixture remain missing |
| `PB13-EV-012` | Accessibility, recovery, DevTools, and agent workload coverage | Documented only | no fixtures, runner steps, assistive-technology measurement, crash/revival scripts, DevTools overhead scenarios, or agent-cost scenarios exist |
| `PB13-EV-013` | Benchmark readiness-review gate | Template only | checked no-claim benchmark readiness-review template exists for future owner review across hardware/OS, corpus/network, runner/artifact, browser-pin/comparison, statistics/denominator, and claim-review axes; owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template remains missing |

## Minimum first runner scope

The first useful benchmark runner should be small and strict:

1. One Tier M Windows reference host with complete hardware and OS manifest.
2. The expanded no-claim local corpus seed served from the no-claim local static network profile.
3. One startup scenario, one navigation scenario, one input-latency scenario, and one 30-tab manifest dry run.
4. Runner-generated `benchmark-manifest.schema.json` output with raw artifact hashes.
5. Failure records for unsupported or unimplemented browser behavior instead of silently skipping work.
6. A no-claim result label: "harness smoke evidence only."

This scope is enough to test the measurement pipeline. It is not enough for Chrome-class, low-memory, fastest, daily-driver, or production claims.

## Acceptance rules before performance claims

Turing may not claim faster, lower memory, lower energy, Chrome-class, or extreme-performance status until:

1. benchmark and corpus definitions are versioned and reviewed;
2. all failed and unsupported cases remain in denominators;
3. security mitigations, sandboxing, site isolation, accessibility paths, and active page behavior are equivalent or the result is labeled experimental;
4. raw samples, traces, environment manifests, and statistical summaries are stored and reproducible;
5. competitor versions, command lines, settings, profiles, extensions, caches, and network conditions are disclosed;
6. mixed-state and all-live tab results are reported separately;
7. resource savings distinguish physical memory, semantic charged memory, GPU memory, compressed memory, swap, and discarded state;
8. crash, recovery, revival, accessibility, DevTools, and agent overhead are included where the claim touches those workflows;
9. an owner-approved expiry date and rerun trigger exists in the result manifest or linked claim record;
10. public language says exactly which platforms, workloads, versions, and unsupported behaviors the claim covers.

## Required documents and registries to sync

When `PB13-EV-*` work changes meaning, update:

- [Pre-build readiness registry](../blueprint-v1/machine/pre-build-readiness.json)
- [Benchmark manifest schema](../blueprint-v1/machine/benchmark-manifest.schema.json)
- [No-claim benchmark manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json)
- [Benchmark manifest validator](../../tools/validate_benchmark_manifests.py)
- [Benchmark hardware schema](../blueprint-v1/machine/benchmark-hardware.schema.json)
- [Current Windows high-end hardware candidate](../blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json)
- [Benchmark hardware validator](../../tools/validate_benchmark_hardware.py)
- [Benchmark OS-control schema](../blueprint-v1/machine/benchmark-os-control.schema.json)
- [Current Windows high-end OS-control candidate](../blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json)
- [Benchmark OS-control validator](../../tools/validate_benchmark_os_controls.py)
- [Benchmark resource-attribution schema](../blueprint-v1/machine/benchmark-resource-attribution.schema.json)
- [Semantic owner taxonomy](../blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json)
- [Benchmark resource-attribution validator](../../tools/validate_benchmark_resource_attribution.py)
- [Benchmark competitor-version schema](../blueprint-v1/machine/benchmark-competitor-version.schema.json)
- [Current desktop release-candidate competitor-version manifest](../blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json)
- [Benchmark competitor-version validator](../../tools/validate_benchmark_competitor_versions.py)
- [Benchmark competitor local-install schema](../blueprint-v1/machine/benchmark-competitor-local-install.schema.json)
- [Current Windows high-end competitor local-install manifest](../blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json)
- [Benchmark competitor local-install validator](../../tools/validate_benchmark_competitor_local_installs.py)
- [Benchmark browser-pin capture schema](../blueprint-v1/machine/benchmark-browser-pin-capture.schema.json)
- [Current Windows high-end browser-pin capture plan](../blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json)
- [Benchmark browser-pin capture validator](../../tools/validate_benchmark_browser_pin_capture.py)
- [Benchmark browser-pin capture self-test runner](../../tools/capture_benchmark_browser_pins.py)
- [Benchmark browser-pin diagnostic schema](../blueprint-v1/machine/benchmark-browser-pin-diagnostic.schema.json)
- [Current Windows high-end Chrome/Edge browser-pin diagnostic](../blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json)
- [Benchmark browser-pin diagnostic validator](../../tools/validate_benchmark_browser_pin_diagnostics.py)
- [Benchmark browser-pin local diagnostic capture report](benchmark-browser-pin-local-diagnostic-capture-2026-07.md)
- [Benchmark corpus schema](../blueprint-v1/machine/benchmark-corpus.schema.json)
- [No-claim smoke corpus manifest](../blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json)
- [Benchmark corpus expansion](benchmark-corpus-expansion-2026-07.md)
- [Benchmark corpus validator](../../tools/validate_benchmark_corpus.py)
- [Benchmark network profile schema](../blueprint-v1/machine/benchmark-network-profile.schema.json)
- [No-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json)
- [Benchmark network profile validator](../../tools/validate_benchmark_network_profile.py)
- [Benchmark server lifecycle self-test](benchmark-server-lifecycle-self-test-2026-07.md)
- [Benchmark server lifecycle self-test runner](../../tools/run_benchmark_server_profile.py)
- [Benchmark tab scenario schema](../blueprint-v1/machine/benchmark-tab-scenario.schema.json)
- [No-claim 30-tab scenario manifest](../blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json)
- [Benchmark tab scenario validator](../../tools/validate_benchmark_tab_scenarios.py)
- [Benchmark 30-tab scenario contract](benchmark-30-tab-scenario-contract-2026-07.md)
- [Benchmark artifact-package schema](../blueprint-v1/machine/benchmark-artifact-package.schema.json)
- [No-claim trace/artifact package plan](../blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json)
- [Benchmark artifact-package validator](../../tools/validate_benchmark_artifact_packages.py)
- [Benchmark trace/artifact package contract](benchmark-trace-artifact-package-contract-2026-07.md)
- [Benchmark launch-runner schema](../blueprint-v1/machine/benchmark-launch-runner.schema.json)
- [No-claim browser launch-runner plan](../blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json)
- [Benchmark launch-runner validator](../../tools/validate_benchmark_launch_runners.py)
- [Benchmark browser launch-runner self-test](../../tools/run_benchmark_browser_launch.py)
- [Benchmark browser launch-runner contract](benchmark-browser-launch-runner-contract-2026-07.md)
- [Benchmark readiness-review schema](../blueprint-v1/machine/benchmark-readiness-review.schema.json)
- [No-claim benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json)
- [Benchmark readiness-review validator](../../tools/validate_benchmark_readiness_review.py)
- [Benchmark profile static-server self-test](../../tools/serve_benchmark_profile.py)
- [Benchmark smoke runner self-test](../../tools/run_benchmark_smoke.py)
- [Blueprint 09](../blueprint-v1/09-performance-memory.md)
- [Blueprint 12](../blueprint-v1/12-testing-compatibility.md)
- [Blueprint 20](../blueprint-v1/20-definition-of-done.md)
- [Benchmark Laboratory](../benchmark-lab/README.md) and affected chapters
- [Performance Engineering](../performance/README.md) and affected chapters
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md)
- [Research index](README.md), [documentation index](../README.md), [repository map](../repository-map.md), and [research log](../research-log.md)

## Next actions

1. Capture Tier M and Tier L hardware manifests and decide whether the current Tier H candidate is approved or replaced.
2. Define a clean OS image or restore procedure plus update, driver, firmware, display, and thermal controls for each hardware tier.
3. Convert the expanded no-claim corpus seed into the first reviewed local server-ready corpus set.
4. Extend the checked runner-managed server lifecycle self-test into browser-run server evidence with DNS execution proof, benchmark-run server artifacts, richer network profiles, logs, cleanup records, and failure records.
5. Extend the checked trace/artifact package contract into runner-generated trace packages with ETW or equivalent traces, Perfetto-compatible traces where applicable, raw samples, redaction review, and retention records.
6. Owner-review the no-claim Chrome/Edge browser-pin diagnostic capture, resolve Edge channel/update-ring proof, and fill effective settings before using browser pins in benchmark runs.
7. Extend the checked no-claim browser launch-runner contract and checked no-browser browser launch-runner self-test into an implemented runner with timeout, sample, failure, cache, competitor-version, browser-pin, 30-tab scenario, trace/artifact package, resource-attribution, negative-test, and claim-metadata controls.
8. Replace the checked no-claim benchmark readiness-review template with an owner-reviewed benchmark readiness review after real hardware, corpus, runner, raw artifact, browser-pin, statistics, denominator, and claim-bundle evidence exists.

`PB-013` remains `documented_no_runner` until at least the fixed hardware, reviewed representative offline corpus, runner-managed server artifact, implemented browser benchmark launch runner, runner-generated trace and artifact package root, runner-generated 30-tab output, non-sample raw-artifact validation, owner-reviewed claim bundle, and owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template exist.
