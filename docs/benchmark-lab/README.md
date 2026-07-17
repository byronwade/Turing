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
- https://browserbench.org/MotionMark1.3/
- https://perfetto.dev/
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.

<!-- MARKET-STRATEGY-2026-07 -->
## Product workflow laboratory

Add controlled Space switching, recovery, migration, 30-tab resource comprehension, Research Canvas, agent trust, cross-device conflict, and Developer Causal Mode tasks. Report completion, errors, loss, accessibility, latency, resource use, and user confidence together.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## UI framework bake-off

The laboratory runs identical Slint, Vizia, and Floem/GPUI reference shells on one pinned platform before architectural selection. Empty-window data is retained but cannot outweigh 100-tab, split-view, page-surface, IME, accessibility, failure, and recovery results.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## SLO evidence

The laboratory owns reproducible methods and raw artifacts used to set and verify `SLO-*` targets. An implementation agent cannot select only favorable samples or change the workload after seeing a result.
