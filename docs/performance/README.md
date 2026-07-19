# Browser Performance Engineering Book

Status: detailed research and design baseline  
Owner: performance, memory, and energy engineering  
Canonical overview: [Blueprint 09 — performance, memory, energy, and the 30-tab contract](../blueprint-v1/09-performance-memory.md)

This book expands Turing's performance contract into models, measurement rules, representation budgets, scheduling policy, graphics and startup work, and regression governance. It does not claim that Turing currently outperforms any browser.

## Reading order

1. [Performance model and critical path](01-performance-model-and-critical-path.md)
2. [Memory, allocation, and cache policy](02-memory-allocation-and-cache-policy.md)
3. [Scheduler, parallelism, and latency](03-scheduler-parallelism-and-latency.md)
4. [Graphics, energy, startup, and recovery](04-graphics-energy-startup-and-recovery.md)
5. [Benchmarks, statistics, and regression governance](05-benchmarks-statistics-and-regression-governance.md)

## Performance thesis

The product target is sustained user-perceived responsiveness with low and explainable resource use. Turing optimizes the path that determines when a person can open the browser, type, navigate, read, scroll, interact, recover, or stop an action. Throughput matters, but not at the expense of p95/p99 latency, correctness, security, accessibility, battery life, memory pressure, or recovery.

Performance is architectural. Data representation, process topology, site isolation, IPC, queues, parser behavior, style invalidation, layout fragments, paint retention, GPU work, JIT tiering, GC, storage, browser chrome, extensions, and agents all participate.

The checked no-claim benchmark readiness-review template is a future owner-review shape only. It does not provide owner-reviewed benchmark readiness, benchmark-ready browser pins, benchmark results, public performance claims, Chrome-class claims, speed, memory, energy, production, daily-driver, or implementation evidence.

## Chrome-class and extreme-performance boundary

The market goal of Chrome-class performance leadership is a future claim and remains blocked by unresolved `PB-013`.

Current status:

- no accepted claim exists yet for lower memory, lower energy, faster startup/interaction, better 30-tab behavior, or Chrome-class compatibility throughput;
- fixed-hardware capture, equal-workload harness proof, raw-browser samples, statistics-analysis plans, and owner-reviewed benchmark readiness remain required;
- required evidence is tracked through `TASK-000005`, [Performance benchmark readiness packet](../research/performance-benchmark-readiness-packet-2026-07.md), [benchmark engine baseline harness readiness map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md), [30-tab scenario contract](../research/benchmark-30-tab-scenario-contract-2026-07.md), [statistics-analysis contract](../research/benchmark-statistics-analysis-contract-2026-07.md), and the checked validators/commands in the [Documentation Readiness Evidence Matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md#validation-commands).

No implementation, production, or Chrome-class positioning claims may rely on pre-ready benchmark evidence.

## Measurement rules

- Every result identifies build, commit, platform, hardware, RAM, power, thermal state, profile, cache, network, corpus, process count, isolation, tab states, extensions, agents, repetitions, and analysis.
- Failed and unsupported workloads remain visible.
- Current stable competitors use default-equivalent security and page activity.
- Mixed-state and all-live tab tests are separate.
- Physical, resident, committed, reserved, shared, charged, compressed, swapped, and GPU memory are not collapsed into one misleading number.
- Synthetic suites are diagnostics; real interactions, long runs, recovery, and energy are product gates.
- A speedup that disables mitigation, accessibility, compatibility, or active behavior is experimental.

## Leadership criteria

Turing should claim performance leadership only from an evidence package showing startup, input-to-present tails, frame pacing, page stages, 30-tab behavior, memory attribution, CPU/wakeups, energy/thermal behavior, crash recovery, developer tooling overhead, AI costs, and compatibility coverage across fixed hardware tiers.

## Advanced research

6. [Data Locality, CPU Caches, and NUMA](06-data-locality-cpu-caches-and-numa.md)
7. [Allocators, Virtual Memory, and Page Reclamation](07-allocators-virtual-memory-and-page-reclamation.md)
8. [IPC, Shared Memory, Serialization, and Batching](08-ipc-shared-memory-serialization-and-batching.md)
9. [PGO, LTO, Binary Layout, and Startup](09-pgo-lto-binary-layout-and-startup.md)
10. [Causal Profiling and Regression Diagnosis](10-causal-profiling-and-regression-diagnosis.md)

## Related material

- [Browser engine book](../engine/README.md)
- [JavaScript runtime book](../javascript/README.md)
- [Developer experience book](../developer-experience/README.md)
- [Fixed-hardware research issue](../research/browser-engine-landscape-2026-07.md)
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
- [Benchmark statistics analysis contract](../research/benchmark-statistics-analysis-contract-2026-07.md)
- [Benchmark engine baseline harness readiness map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md)
- [Memory Object Representation and Tab Lifecycle Research](../research/memory-object-representation-and-tab-lifecycle-research-2026-07.md)
- [Process Topology and Isolation-Adjusted Memory Research](../research/process-topology-isolation-adjusted-memory-research-2026-07.md)
- [Chrome-Class Capability Traceability Map](../research/chrome-class-capability-traceability-map-2026-07.md)
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
- [No-claim statistics-analysis plan](../blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json)
- [Benchmark statistics-analysis validator](../../tools/validate_benchmark_statistics_analysis.py)
- [Benchmark browser launch-runner self-test](../../tools/run_benchmark_browser_launch.py)
- [Benchmark profile static-server self-test](../../tools/serve_benchmark_profile.py)
- [Benchmark smoke runner self-test](../../tools/run_benchmark_smoke.py)

<!-- MARKET-STRATEGY-2026-07 -->
## Resource Truth Center

`OP-003` researches a user-facing layer over semantic resource accounting: per-Space ownership, transition reasons, predicted savings, state-loss risk, and revival quality. Measurements remain equivalent-security and complete-denominator.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native shell footprint

The UI framework bake-off measures stripped and packaged size, startup faulting, idle memory, per-window/component memory, update allocations, input latency, frame pacing, GPU allocation, wakeups, hidden-window behavior, and page-surface composition. Release chrome ships no second browser runtime and normally compiles one backend and renderer.
