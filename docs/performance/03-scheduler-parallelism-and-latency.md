# Scheduler, Parallelism, and Latency

Status: research and design baseline  
Owner: browser scheduling  
Purpose: Coordinate processes, threads, tasks, deadlines, background policy, and adaptive parallel work.

## Relationship to the Turing program

This document owns the detailed experiment behind EXP-ENGINE-003 and complements runtime event-loop policy in [the JavaScript book](../javascript/05-webassembly-webidl-and-event-loop.md).

## Scheduling entities

Entities include browser UI commands, input, navigation, renderer tasks, microtasks, parser work, style/layout/paint, raster, compositor, network, storage, workers, service workers, GC, compilation, decoders, extensions, DevTools, agents, and maintenance. Each task carries principal, target/document epoch, source, enqueue time, deadline or priority, cancellation, cost estimate, and resource owner.

Queues are bounded and expose overload behavior.

## Priority model

Priorities derive from user visibility and semantic need: trusted browser input, visible page input/frame, navigation needed for useful content, protected media/call/download, user-visible background collaboration, speculative work, ordinary background tasks, and maintenance. Priority inheritance handles locks/resources to avoid inversion.

Pages cannot self-label all work as foreground. Browser policy controls classification.

## Deadlines and frame scheduling

Display refresh, input timestamps, compositor deadlines, animation, raster readiness, and presentation feedback shape visible-frame scheduling. Main-thread and compositor work report missed-deadline reasons. High-refresh displays require different budgets rather than assuming 16.7 ms.

Tasks can yield at semantic safe points. Long uninterruptible operations are measured and redesigned.

## Adaptive parallelism

Serial reference paths come first. Parallel work is enabled when dependency graphs, task size, hardware cores, memory bandwidth, cache locality, queue pressure, foreground deadlines, thermal state, and energy mode predict benefit. Small documents or constrained devices may remain serial.

Candidates include stylesheet parsing, independent selector matching, formatting-context layout, tile raster, image/font decode, JS parse/compile, and proven GC phases.

## Worker pools and isolation

Pools are partitioned or scheduled to prevent a hostile site, extension, DevTools session, or agent from monopolizing global workers. Work items hold immutable/versioned inputs and bounded outputs. Cancellation and target teardown prevent publication into stale documents.

Pool size responds to active cores, OS power mode, foreground needs, and process role; “number of cores” alone is insufficient.

## Background and lifecycle policy

Timers, workers, service workers, animations, networking, and compilation are throttled only within platform semantics. Budget buckets track CPU, wakeups, network, and wall time. Protected audio, calls, downloads, uploads, device sessions, and user pins receive exceptions.

Freeze stops eligible task sources; discard ends the document. Lifecycle state is visible and testable.

## Fairness and denial of service

Scheduler fairness operates across principals and task classes with hard caps on queue length, nested work, worker count, IPC, microtasks, mutation observers, and agent replanning. A malicious page cannot prevent browser UI, cancellation, confirmation, or process teardown.

Watchdogs distinguish slow work, deadlock, livelock, priority inversion, and hung process.

## Non-negotiable invariants

- Every queued task has an owner, class, limits, and cancellation behavior.
- Browser policy—not page claims—determines privileged priority.
- Control, input, and cancellation remain serviceable under overload.
- Parallel work publishes only to matching versioned inputs and current epochs.
- Background throttling preserves platform semantics and protected activity.
- Adaptive parallelism must beat serial behavior end to end on the target workload.

## Required evidence

- Serial, fixed-pool, work-stealing, and deadline-aware experiments on Tier L/M/H.
- Queue latency, p95/p99 interaction, frame pacing, CPU, memory, cache, and energy results.
- Priority inversion, starvation, overload, microtask storm, worker flood, and cancellation tests.
- Lifecycle and protected-activity conformance tests.
- Thermal, low-power, core-count, and background contention studies.
- Deterministic schedule/model tests for state machines and publication epochs.

## Known risks and unresolved questions

- Complex scheduling heuristics can be hard to reason about and reproduce.
- Parallelism can increase memory, cache misses, and energy while lowering wall time.
- Incorrect throttling can break applications or accessibility.
- Priority systems can starve maintenance and accumulate debt.

## Primary sources

- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- Servo project — https://servo.org/about/
- WHATWG HTML Living Standard — https://html.spec.whatwg.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
