# Fixed-Hardware Benchmark Laboratory Book

Status: detailed research and design baseline  
Owner: performance measurement and benchmark operations  
Canonical overview: [Blueprint owner](../blueprint-v1/09-performance-memory.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

A benchmark result is a versioned experiment, not a screenshot. Every result binds workload, feature coverage, security configuration, process topology, lifecycle state, raw samples, uncertainty, failures, and recovery behavior.

## Reading order

1. [Hardware, OS, Power, and Thermal Control](01-hardware-os-power-and-thermal-control.md)
2. [Corpus, Servers, and Network Control](02-corpus-servers-and-network-control.md)
3. [Startup, Navigation, and Input Latency](03-startup-navigation-and-input-latency.md)
4. [Frame Pacing, Raster, Composite, and GPU](04-frame-pacing-raster-composite-and-gpu.md)
5. [Memory, Process Topology, and Thirty Tabs](05-memory-process-topology-and-thirty-tabs.md)
6. [Energy, Accessibility, Developer, Agent, and Recovery Workloads](06-energy-accessibility-developer-agent-and-recovery.md)
7. [Statistics, Artifacts, Regressions, and Claims](07-statistics-artifacts-regressions-and-claims.md)

## Cross-cutting rules

- Security and correctness precede benchmark wins and implementation convenience.
- Every boundary preserves typed identity and denies ambient authority.
- Queues, caches, retries, tasks, messages, persistent records, and diagnostic output are bounded.
- A deterministic serial/reference path precedes concurrent, incremental, speculative, cached, hardware, or JIT optimization.
- Physical and semantic resource ownership remain observable.
- Failure, cancellation, crash, restart, migration, pressure, and recovery are part of the supported behavior.
- Accessibility, privacy, localization, developer tooling, and platform differences are designed with the subsystem.
- Research does not change accepted requirements or support status without the normal decision process.

## Leadership criteria

Leadership requires a public evidence package combining conformance, adversarial and fault testing, fixed-hardware latency and resource measurements, accessible workflows, recovery, maintenance cost, security review, and explicit failures. A smaller feature set, weaker isolation, hidden discarding, unmatched caches, omitted failures, or vendor marketing cannot establish leadership.

## Primary sources

- https://browserbench.org/
- https://browserbench.org/Speedometer3.1/
- https://browserbench.org/JetStream3.0/
- https://browserbench.org/MotionMark/
- https://chromium.googlesource.com/catapult/+/HEAD/telemetry/
- https://web.dev/articles/vitals
- https://developer.chrome.com/docs/crux
- https://developer.chrome.com/docs/devtools/performance/reference
- https://github.com/catchpoint/WebPageTest.agent/blob/master/docs/test_options.md
- https://chromereleases.googleblog.com/
- https://perfetto.dev/
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)
- [Performance benchmark readiness packet](../research/performance-benchmark-readiness-packet-2026-07.md)
- [Benchmark corpus expansion](../research/benchmark-corpus-expansion-2026-07.md)
- [Chrome-class performance runbook](../research/chrome-class-performance-runbook-2026-07.md)
- [Benchmark hardware and OS manifest](../research/benchmark-hardware-os-manifest-2026-07.md)
- [Benchmark OS and update-control manifest](../research/benchmark-os-update-control-manifest-2026-07.md)
- [Semantic resource attribution taxonomy](../research/semantic-resource-attribution-taxonomy-2026-07.md)
- [Benchmark competitor version manifest](../research/benchmark-competitor-version-manifest-2026-07.md)
- [Benchmark competitor local install inventory](../research/benchmark-competitor-local-install-inventory-2026-07.md)
- [Benchmark browser pin capture contract](../research/benchmark-browser-pin-capture-contract-2026-07.md)
- [Benchmark browser pin local diagnostic capture](../research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md)
- [Benchmark server lifecycle self-test](../research/benchmark-server-lifecycle-self-test-2026-07.md)
- [Benchmark 30-tab scenario contract](../research/benchmark-30-tab-scenario-contract-2026-07.md)
- [Benchmark trace/artifact package contract](../research/benchmark-trace-artifact-package-contract-2026-07.md)
- [Benchmark browser launch-runner contract](../research/benchmark-browser-launch-runner-contract-2026-07.md)
- [Benchmark browser launch-runner self-test](../../tools/run_benchmark_browser_launch.py)
- [No-claim benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json)
- [Benchmark readiness-review validator](../../tools/validate_benchmark_readiness_review.py)
- [Servo performance baseline preparation](../research/servo-performance-baseline-2026-07.md)
- [No-claim benchmark manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json)
- [Benchmark manifest validator](../../tools/validate_benchmark_manifests.py)
- [No-claim benchmark corpus manifest](../blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json)
- [Benchmark corpus validator](../../tools/validate_benchmark_corpus.py)
- [No-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json)
- [Benchmark network profile validator](../../tools/validate_benchmark_network_profile.py)
- [Benchmark server lifecycle self-test](../../tools/run_benchmark_server_profile.py)
- [Current desktop release-candidate competitor-version manifest](../blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json)
- [Benchmark competitor-version validator](../../tools/validate_benchmark_competitor_versions.py)
- [Current Windows high-end competitor local-install manifest](../blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json)
- [Benchmark competitor local-install validator](../../tools/validate_benchmark_competitor_local_installs.py)
- [Current Windows high-end browser-pin capture plan](../blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json)
- [Benchmark browser-pin capture validator](../../tools/validate_benchmark_browser_pin_capture.py)
- [Benchmark browser-pin capture self-test runner](../../tools/capture_benchmark_browser_pins.py)
- [Current Windows high-end Chrome/Edge browser-pin diagnostic](../blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json)
- [Benchmark browser-pin diagnostic validator](../../tools/validate_benchmark_browser_pin_diagnostics.py)
- [No-claim 30-tab scenario manifest](../blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json)
- [Benchmark tab scenario validator](../../tools/validate_benchmark_tab_scenarios.py)
- [No-claim trace/artifact package plan](../blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json)
- [Benchmark artifact-package validator](../../tools/validate_benchmark_artifact_packages.py)
- [No-claim browser launch-runner plan](../blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json)
- [Benchmark launch-runner validator](../../tools/validate_benchmark_launch_runners.py)
- [Benchmark browser launch-runner self-test](../../tools/run_benchmark_browser_launch.py)
- [Benchmark profile static-server self-test](../../tools/serve_benchmark_profile.py)
- [Benchmark smoke runner self-test](../../tools/run_benchmark_smoke.py)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.

The checked no-claim benchmark readiness-review template is a future owner-review shape only. It does not provide owner-reviewed benchmark readiness, benchmark-ready browser pins, benchmark results, public performance claims, Chrome-class claims, speed, memory, energy, production, daily-driver, or implementation evidence.

<!-- MARKET-STRATEGY-2026-07 -->
## Product workflow laboratory

Add controlled Space switching, recovery, migration, 30-tab resource comprehension, Research Canvas, agent trust, cross-device conflict, and Developer Causal Mode tasks. Report completion, errors, loss, accessibility, latency, resource use, and user confidence together.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## UI framework bake-off

The laboratory runs identical Slint, Vizia, and Floem/GPUI reference shells on one pinned platform before architectural selection. Empty-window data is retained but cannot outweigh 100-tab, split-view, page-surface, IME, accessibility, failure, and recovery results.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## SLO evidence

The laboratory owns reproducible methods and raw artifacts used to set and verify `SLO-*` targets. An implementation agent cannot select only favorable samples or change the workload after seeing a result.
