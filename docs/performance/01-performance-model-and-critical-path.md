# Performance Model and Critical Path

Status: research and design baseline  
Owner: performance architecture  
Purpose: Define user-visible latency paths, budgets, attribution, and tradeoff rules.

## Relationship to the Turing program

This document deepens the performance philosophy and gates in [Blueprint 09](../blueprint-v1/09-performance-memory.md).

## User journeys

Primary journeys include process start to address-field readiness; address entry to navigation response; response to useful visible content; key/pointer to presented frame; scrolling and animation; tab switch and revival; permission or credential decision; developer inspection; session restore; renderer/GPU/network crash recovery; and agent stop/cancellation.

Each journey has p50, p95, p99, worst-reasonable, failure, and recovery metrics. Aggregate throughput never substitutes for these paths.

## Critical-path graph

Every journey is modeled as a causal graph of queueing and execution across browser UI, kernel, renderer, network, storage, runtime, style, layout, paint, raster, compositor, GPU, OS, and optional agents. The trace distinguishes work required for the next visible milestone from speculative, maintenance, or background work.

Critical-path ownership is explicit so optimizations do not move cost into an unreported service.

## Milestones

Navigation milestones include request accepted, connection/security ready, response start, parser start, first meaningful structure, first paint, largest relevant content, first input readiness, stable viewport, and application-specific readiness. Browser milestones include process load, UI first paint, address-field input, profile metadata ready, session list ready, and restored active tab.

Milestones include validity conditions. A blank interactive window or unresponsive painted page does not satisfy readiness.

## Latency budgets

Subsystem budgets are hypotheses tied to hardware tiers and workload classes. Parser, script, style, layout, paint, raster, composite, queue wait, GC, IPC, and browser chrome each report contribution. A missed budget triggers attribution rather than indiscriminate optimization.

Budget borrowing is allowed only with an end-to-end result and no hidden tail, memory, energy, security, or accessibility regression.

## Responsiveness under contention

Foreground input, browser chrome, visible frame, navigation, audio/call, downloads/uploads, and confirmations have priority over speculative prefetch, background script, indexing, cache cleanup, telemetry, diagnostics, and model maintenance. Priority is not absolute: starvation bounds and correctness constraints remain.

Thirty-tab, developer-tools, extension, and agent scenarios test contention explicitly.

## Recovery performance

Crashes, hangs, GPU loss, network service restart, storage faults, memory pressure, sleep/wake, display changes, and update restart have detection, user feedback, failover, restoration, and state-loss metrics. Fast recovery cannot hide silent data loss or weaker security.

Tab lifecycle transitions record time to freeze, trim, serialize, discard, revive, reload, and regain input readiness.

## Performance contracts and product claims

A product claim identifies scope, version, workload, hardware, confidence, compatibility coverage, and security configuration. Claims expire when the workload, browser version, or architecture materially changes. “Fastest” or “lowest memory” is prohibited without a current multi-dimensional comparison and published raw evidence.

## Non-negotiable invariants

- User-visible milestones have semantic validity conditions.
- Queue wait and execution are measured separately.
- Critical-path work is distinguished from speculative/background work.
- Performance claims include compatibility, security, lifecycle, and failure disclosure.
- Recovery metrics include state loss and integrity.
- No subsystem win is accepted without end-to-end evidence.

## Required evidence

- Versioned user-journey corpus and causal trace schema.
- Fixed-hardware p50/p95/p99 with raw samples and confidence intervals.
- Contention tests across 1, 5, 15, 30, and 100 tabs where applicable.
- Recovery and lifecycle fault-injection results.
- Cross-platform clock/measurement validation.
- Competitor comparisons with equivalent configurations and failed workloads.

## Known risks and unresolved questions

- Milestones can be gamed if semantic validity is weak.
- Trace attribution may omit OS, driver, shared, or asynchronous work.
- Optimizing one hardware tier can harm constrained or battery devices.
- Recovery speed can obscure data loss or repeated crash loops.

## Primary sources

- Speedometer — https://browserbench.org/Speedometer3.1/
- MotionMark — https://browserbench.org/MotionMark/
- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
