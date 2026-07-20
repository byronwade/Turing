# JavaScript and DOM Wrapper Lifetime Research - July 2026

Status: deferred `RQ-08` no-claim research packet
Owner: JavaScript runtime, DOM, memory, security, storage, accessibility, and quality
Research date: 2026-07-19
Confidence: high for the standards and public runtime observations; low for any Turing heap, wrapper, tracing, or memory conclusion until lifetime oracles and hostile teardown evidence exist

## Question

Which JavaScript heap representation and DOM-wrapper strategy preserves reachability, identity, teardown, cross-boundary safety, and memory accountability without unacceptable tracing or indirection cost?

## Why This Matters

The browser exposes native document objects through JavaScript while the DOM, layout, accessibility, event, storage, and renderer systems retain their own references. A wrapper may outlive a document, a document may be detached while script still holds an object, and a native resource may be retained outside either heap. Incorrect ownership creates leaks, use-after-free, stale-origin behavior, or data exposure; over-retention creates the memory footprint the project is trying to reduce.

This packet defines a deferred research route for `RQ-08`. It does not select tracing GC, reference counting, arenas, handles, pointer compression, wrapper identity, or a DOM memory policy.

## Source-backed observations

### ECMAScript liveness is not a collection schedule

The ECMAScript specification does not guarantee that unreachable objects are collected. Its `WeakRef` and `FinalizationRegistry` model permits implementation and host scheduling freedom and treats liveness as an observable lower bound rather than a promise of prompt reclamation. Cleanup callbacks cannot serve as correctness, teardown, or benchmark completion signals.

Source: [ECMAScript memory management and WeakRef model](https://tc39.es/ecma262/), retrieved 2026-07-19.

### Blink exposes a two-part DOM object model

V8's public tracing documentation describes DOM objects as a JavaScript wrapper plus a C++ object representing the node, with cross-component tracing connecting the graphs. This is a useful observation of one implementation's wrapper/lifetime problem, not a requirement to copy its object model.

Source: [Tracing from JS to the DOM and back again](https://v8.dev/blog/tracing-js-dom), retrieved 2026-07-19.

### Oilpan demonstrates cross-component tracing and explicit pointer policy

V8 documents Oilpan as a trace-based collector for C++ objects that can integrate with V8's heap, including precise heap references, conservative native-stack scanning, weak references, ephemerons, finalizers, and compaction for eligible objects. It also documents pointer compression for `Member` references, heap-cage limits, multiple heaps, and the risk that an apparently safe cage-size optimization can produce out-of-memory failures.

Sources: [Oilpan library](https://v8.dev/blog/oilpan-library), [high-performance C++ garbage collection](https://v8.dev/blog/high-performance-cpp-gc), and [pointer compression in Oilpan](https://v8.dev/blog/oilpan-pointer-compression), retrieved 2026-07-19.

### Multiple allocator and lifetime classes remain necessary

Chromium's memory-management documentation separates garbage-collected objects from other allocation classes and identifies different lifetime and performance purposes. This supports a research requirement to account for JS heap, DOM wrappers, native resources, allocator metadata, images, fonts, GPU objects, and discardable data separately rather than reporting one heap number.

Source: [Chromium memory management in Blink](https://chromium.googlesource.com/chromium/src/%2B/554be8c5f4dfc501ae0825504ffe64440f32387a/third_party/blink/renderer/platform/wtf/Allocator.md), retrieved 2026-07-19.

## Candidate ownership models

The owner-approved comparison should include:

1. Precise tracing for a unified JS/native graph with explicit visitor or generated edge metadata.
2. Reference counting or intrusive ownership with cycle detection and explicit weak edges.
3. Arena or region ownership for document-scoped objects, with handles for longer-lived script identity.
4. Hybrid model: JS-managed wrappers, native document ownership, explicit cross-heap handles, and separate resource budgets.
5. Full lifetime oracle that prioritizes semantic identity and teardown correctness over production speed.

Each model must define wrapper identity, multiple globals/realms, same-origin and cross-origin references, detached nodes, adopted nodes, shadow trees, event listeners, closures, weak maps, finalizers, workers, renderer restart, document epochs, and profile/session teardown.

## Evidence required before a lifetime decision

The owner-approved package should provide:

- wrapper-to-native identity tables across realms, frames, shadow roots, adopted nodes, and document replacement;
- strong, weak, ephemeron, persistent, and stack-root fixtures with explicit expected liveness;
- DOM-to-JavaScript and JavaScript-to-DOM cycles, event-listener closures, observer queues, promises, workers, and pending tasks;
- teardown during script, layout, accessibility, navigation, BFCache-like state, freeze/revival, renderer crash, and process restart;
- external-resource fixtures for images, fonts, media, ArrayBuffers, GPU handles, sockets, storage, and credentials with separate ownership records;
- stale-wrapper, wrong-document, wrong-origin, wrong-process, and stale-agent-action rejection tests;
- moving/compacting, pointer-compression, handle-indirection, and allocation-failure tests where applicable;
- conformance and negative tests for WeakRef, WeakMap, FinalizationRegistry, proxies, symbols, and host objects;
- heap graphs, root sets, wrapper maps, reclamation records, retained bytes, and cleanup/failure denominators;
- independent review of safety, privacy, resource accounting, generated tracing metadata, and native/unsafe boundaries.

## Measurement plan

Measure equivalent workloads and security policies for:

- JS heap, native DOM, wrapper, handle, trace metadata, allocator, external resource, and retained-page bytes;
- allocation rate, root scanning, marking, sweeping, compaction, write barriers, finalization, and pause/tail latency;
- wrapper lookup, property access, event dispatch, DOM mutation, layout invalidation, accessibility updates, and cross-boundary calls;
- document teardown, navigation, freeze/revival, renderer restart, crash recovery, and profile clearing latency;
- pointer compression or handle memory savings, decode cost, cache behavior, address-space limits, and failure behavior;
- leaks, premature reclamation, stale identity, use-after-free, wrong-principal access, timeout, cancellation, and cleanup denominators.

Do not treat a lower heap number as an improvement if it hides native resources, delays reclamation until process death, weakens identity checks, or increases tail latency and recovery risk.

## Rejection rules

Reject the packet as decision evidence when it:

- treats garbage-collection timing or finalizers as deterministic application behavior;
- counts JavaScript wrappers without native DOM objects, or native objects without wrappers and external resources;
- assumes reference counting handles cycles, or tracing handles all unmanaged pointers, without explicit proof;
- compresses pointers or limits heap cages without address-space, multi-heap, out-of-memory, and security evidence;
- allows detached or stale wrappers to access a new document, origin, process, profile, or agent grant;
- omits event listeners, observer queues, workers, async tasks, shadow trees, accessibility, or storage roots;
- validates only steady-state memory and omits navigation, teardown, crash, freeze/revival, and recovery;
- uses same-agent heap graphs or self-generated liveness oracles as independent evidence;
- reports one total memory number that hides allocator, metadata, external-resource, or tracing overhead.

## Current status and next proof

`RQ-08` remains deferred outside the active pre-build crosswalk. The next proof is an owner-approved wrapper identity and root/edge schema, followed by synthetic cross-heap lifetime fixtures, teardown/restart tests, and independent memory/safety review. No heap representation, wrapper strategy, collector, memory result, security result, performance result, or readiness claim follows from this packet.

## Claim boundary

This is source-backed research preparation only. It does not select a garbage collector, heap model, DOM wrapper, pointer representation, ownership policy, finalization behavior, resource budget, memory target, security posture, or production runtime claim.
