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
