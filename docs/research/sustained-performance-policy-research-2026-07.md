# Sustained Performance Policy Research - July 2026

Status: active no-claim evidence route for `RQ-23`, `PB-013`, and `TASK-000005`; no browser implementation, benchmark result, energy result, or Chrome-class claim is accepted
Owner: performance engineering, runtime architecture, security, accessibility, release operations, and independent review
Research date: 2026-07-19

## Question

Which scheduling, memory, cache, lifecycle, and energy policies should be compared before Turing can make a sustained-performance claim across interactive, multi-tab, constrained-resource, and recovery workloads?

## Current boundary

The repository already specifies benchmark identity, corpus, host controls, traces, resource attribution, 30-tab scenarios, statistics, and claim-review gates. Those records do not select a scheduler, allocator, cache policy, lifecycle policy, power policy, or implementation. This packet supplies the missing policy comparison and evidence route. It does not prove that any candidate is faster, smaller, lower-energy, more responsive, or more compatible than another browser.

## Source observations

The following are observations from external documentation, not Turing results:

- [Chromium Threading and Tasks](https://chromium.googlesource.com/chromium/src/+/main/docs/threading_and_tasks.md) describes sequences as ordered virtual execution contexts that can move across pool threads, prefers sequences to dedicated physical threads where possible, and warns that blocking or expensive work on UI/IO paths creates user-visible latency. This supports comparing ownership-preserving sequences, bounded pools, explicit priorities, and blocking annotations rather than counting threads as a performance strategy.
- [Chromium Blink scheduling notes](https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md) describes background throttling/freezing and use of worker pools for work that does not require the main thread. This supports testing foreground responsiveness, background progress, freeze eligibility, and revival as one policy rather than optimizing them independently.
- The [Chrome Page Lifecycle API guidance](https://developer.chrome.com/docs/web-platform/page-lifecycle-api) distinguishes hidden, frozen, and discarded states. Frozen pages suspend freezable tasks; discarded pages may have no event callback and must be recoverable on a later load. This supports explicit lifecycle state, durable restoration metadata, and tests for abrupt reclaim without relying on unload-time cleanup.
- [Linux Pressure Stall Information](https://docs.kernel.org/accounting/psi.html) quantifies CPU, memory, and I/O contention and describes dynamic management such as load shedding or pausing restartable work. This supports recording pressure signals and testing bounded escalation instead of using resident memory alone as a pressure proxy.
- Microsoft's [Windows Performance Recorder introduction](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr) documents OS-level capture for application and resource behavior. This supports retaining OS, power, thermal, driver, and trace configuration with browser measurements rather than treating an application timer as an energy result.

These sources do not establish that Turing should copy Chromium, use a particular allocator, expose a particular lifecycle API, or adopt a platform-specific power mode. They define candidate questions and measurement obligations only.

## Candidate policy dimensions

Every candidate must declare ownership, authority, bounded resources, failure behavior, and replacement cost.

1. **Scheduling.** Compare critical-path/deadline hints, FIFO or priority queues, serial sequences, fixed pools, work stealing, adaptive pools, and cooperative cancellation. Preserve document, site, process, and surface identity across task handoff. No task may block a latency-sensitive path without a declared bound and attribution.
2. **Memory.** Compare semantic ownership with arenas, slabs, pools, and general allocation. Record live, reserved, resident, reclaimable, shared, mapped, swap-backed, and peak state by resource owner. A lower allocator counter is not a lower user-visible footprint unless accounting boundaries and security topology match.
3. **Caches.** Define admission, namespace, freshness, size, pressure class, eviction reason, persistence, and revalidation. Test cold, warm, churn, corruption, quota, and cross-profile isolation. Cache hits must not bypass origin, credential, partition, or security policy.
4. **Lifecycle and reclamation.** Define active, background, frozen, discarded, crashed, and recovering states for pages, processes, workers, GPU resources, and caches. Reclamation must be bounded, observable through trusted diagnostics, restart-safe, and reversible where the product contract requires it. User input, unsaved state, media, downloads, accessibility, DevTools, extensions, and agents require explicit protection or documented loss behavior.
5. **Energy and thermal behavior.** Compare foreground responsiveness and background work under declared AC/battery, display, refresh, thermal, OS power, and device conditions. Record wakeups, CPU time, GPU time, package energy where available, temperature/throttling state, and recovery after sustained load. Platform power hints are test inputs, not portable product guarantees.
6. **Isolation-adjusted performance.** Keep site/process isolation, sandbox, broker, IPC, permissions, and audit paths identical across candidates. If a candidate reduces work by weakening a security or accessibility invariant, reject it rather than report a faster result.

## Required experiment matrix

The future runner must retain raw per-sample records and failure rows for at least:

- cold startup, warm startup, first navigation, reload, back/forward, and crash recovery;
- one foreground interactive page, mixed 30-tab foreground/background workload, and all-live 30-tab workload;
- allocation churn, cache cold/warm/churn/corruption, network delay/loss, storage contention, GPU loss, and memory pressure;
- keyboard, pointer, touch, scrolling, accessibility input, DevTools, extension, download, media, and agent workflows where supported;
- AC and battery, controlled refresh/display, declared thermal state, OS power policy, and sustained runs long enough to expose degradation;
- freeze, discard, revival, process restart, renderer/GPU failure, cancellation, timeout, and cleanup paths.

For each run retain source/build/browser identity, hardware and OS image, power/thermal state, security and isolation settings, profile/cache state, workload/corpus/network versions, scheduler and allocator configuration, process/thread topology, raw timing/resource/energy samples, trace configuration, missing-event policy, failure denominator, artifact hashes, and cleanup proof. Trace-enabled runs require an equivalent no-trace control because instrumentation can alter scheduling, wakeups, memory, and energy.

## Metrics and decision rules

Report p50/p75/p95/p99 where meaningful, frame pacing and missed presentations, input-to-present phases, startup phases, throughput, live/reserved/resident/reclaimable memory, cache hit/miss and eviction, CPU/GPU time, wakeups, pressure stalls, package energy, temperature/throttle state, recovery duration, and unsupported/failure counts. Preserve distributions and per-workload results; do not rely on one score or an aggregate that silently omits failures.

An implementation candidate remains proposed until owner review confirms equal workload, equal security/isolation, equal lifecycle/cache/profile state, declared hardware and OS controls, adequate sample count, uncertainty/effect-size treatment, observer-effect controls, and complete failure denominators. A candidate is rejected for hidden flags, silent tab discarding, unreported background work, unmatched process topology, missing resource owners, missing recovery evidence, security weakening, accessibility regression, or energy claims without device-appropriate measurement.

## Next proof

Prepare a reviewed `TASK-000005` extension that names the first scheduler/memory/cache/lifecycle candidates, binds them to the benchmark manifests, adds resource-pressure and recovery scenarios, and defines the exact artifact schema. Run self-tests first. Do not execute competitor comparisons or make performance, memory, energy, Chrome-class, or daily-driver claims until the L1 browser-run evidence route is reviewed.

## Impact

`RQ-23` now has a dedicated source-backed policy route and an explicit sustained-performance experiment matrix. `PB-013` remains `partial`; `TASK-000005` remains proposed-only; no scheduler, allocator, cache, lifecycle, energy, performance, compatibility, security, accessibility, or production decision changed.
