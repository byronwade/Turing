# Garbage Collection and Host Lifetimes

Status: research and design baseline  
Owner: garbage collection and host integration  
Purpose: Define exact liveness, bounded pauses, DOM wrapper behavior, and verifiable memory ownership.

## Relationship to the Turing program

This document is the detailed owner for RQ-08 and expands [Blueprint 06](../blueprint-v1/06-javascript-runtime.md). Browser-wide memory pressure is governed by the [performance book](../performance/README.md).

## Baseline collector

The first collector should be exact, stop-the-world, and intentionally conservative in complexity. It establishes root enumeration, object headers, mark state, tracing interfaces, sweeping, large objects, out-of-memory handling, and heap verification before generational, incremental, concurrent, or compacting behavior is introduced.

Heap spaces should distinguish young candidates, mature objects, large objects, executable code and metadata, read-only built-ins, and external backing. The exact partition is an experiment, not a fixed claim.

## Roots and handles

Roots include VM registers and frames, globals, module environments, job queues, promises, debugger state, native handles, Web IDL wrappers, workers, message ports, structured-clone activity, and JIT stack maps. Roots are registered through typed APIs; conservative scanning is not the normal correctness mechanism.

Native code holds rooted handles rather than raw movable pointers across allocation or callbacks. Handle scopes have bounded lifetime and are inspectable in debug builds. Persistent handles identify their owner and teardown path.

## Generational collection

A nursery may be introduced after allocation profiles prove value. Promotion policy must account for arrays, strings, closures, wrappers, and external backing. Remembered sets and write barriers are centralized in generated or audited operations. Barrier verification compares remembered reachability with full tracing.

Minor collections respect interaction deadlines and cannot repeatedly promote hostile short-lived graphs into mature memory without attribution and pressure response.

## Incremental and concurrent work

Incremental marking divides work into bounded slices coordinated with the browser scheduler. Concurrent marking or sweeping is permitted only after tri-color invariants, atomics, publication, object mutation, weak processing, and embedder barriers are model-tested and sanitizer-tested.

A collector may finish synchronously when required for correctness, but latency cliffs and reasons are traced. Background work yields to foreground input, navigation, and frame deadlines.

## Weak references and finalization

Weak maps, weak sets, ephemerons, weak references, and finalization registries require explicit phases and fixed-point processing. Finalizers never run arbitrary script while heap invariants or locks are exposed. Cleanup jobs are ordinary scheduled work with cancellation and lifecycle policy.

Native resources use deterministic ownership where possible. GC finalization is not the only release mechanism for files, sockets, GPU objects, permission handles, or profile resources.

## DOM wrappers and cross-component cycles

DOM nodes use stable engine handles. JavaScript wrappers trace or reference those handles through an explicit wrapper map scoped to the correct realm and document. The liveness contract defines how script-to-DOM and DOM-to-script edges participate in tracing, how detached documents are collected, and how navigation invalidates stale callbacks.

A document teardown test must prove that wrappers, listeners, promises, observers, custom elements, layout attachments, and agent references do not retain an otherwise dead page.

## External memory and pressure

Array-buffer storage, strings, images, canvas, media, WebAssembly memories, GPU allocations, and host resources are charged as external memory. Their owners provide size estimates, pressure callbacks, and release semantics. The GC cannot solve unaccounted native retention.

OS pressure can request collection, cache trimming, or lifecycle transition, but never changes origin isolation or liveness semantics. OOM paths fail closed, preserve profile integrity, and emit bounded diagnostics.

## Heap diagnostics

DevTools exposes per-realm/document estimates, allocation sampling, object graphs, retainers, detached documents, wrapper edges, external memory, collection phases, pause slices, promotion, and barrier failures. Heap snapshots redact sensitive strings by default and cannot execute getters or page code.

## Non-negotiable invariants

- Every live managed object is reachable from an exact root or traced edge.
- Every moving or generational optimization has mechanically checkable barriers and stack maps.
- Finalization does not execute script inside collector critical sections.
- DOM and JavaScript cross-component cycles have one documented tracing contract.
- External memory is charged and pressure-aware rather than hidden from the collector.
- OOM handling cannot corrupt profile, module, or document state.

## Required evidence

- Collect-at-every-allocation and randomized-collection stress modes.
- Barrier verifier, heap graph verifier, poisoning, guard allocation, Miri, sanitizers, and fuzzing.
- Weak/ephemeron/finalization Test262 coverage and randomized scheduling.
- DOM wrapper-cycle, detached-document, navigation, worker, and debugger leak tests.
- Pause-time, throughput, promotion, fragmentation, reserved/resident memory, and energy measurements.
- Fault injection for allocation failure in every collector and host-resource phase.

## Known risks and unresolved questions

- Concurrent collection can introduce rare lifetime races that ordinary tests miss.
- Wrapper maps can retain entire documents or expose stale cross-origin state.
- External memory estimates can make pressure decisions inaccurate.
- Compaction and pointer compression increase unsafe-code and debugger complexity.

## Primary sources

- ECMA-262 — https://tc39.es/ecma262/
- Test262 — https://github.com/tc39/test262
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html
- SpiderMonkey documentation — https://firefox-source-docs.mozilla.org/js/index.html
- Miri — https://github.com/rust-lang/miri

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
