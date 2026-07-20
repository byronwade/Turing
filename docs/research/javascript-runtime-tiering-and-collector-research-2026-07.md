# JavaScript Runtime Tiering and Collector Research - July 2026

Status: deferred `RQ-19` no-claim research packet
Owner: JavaScript runtime, compiler, memory, security, performance, and quality
Research date: 2026-07-19
Confidence: high for the standards and public runtime observations; low for any Turing runtime, JIT, collector, or performance conclusion until semantics, security, and interaction-level evidence exist

## Question

Which runtime tiering and collector architecture gives the best interaction-adjusted performance without sacrificing JavaScript semantics, predictable memory behavior, security boundaries, or reproducible evidence?

## Why This Matters

JavaScript performance is a time series, not a single peak score. Parsing, bytecode generation, interpretation, baseline compilation, optimization, deoptimization, garbage collection, code caching, and teardown compete with user-visible work. A runtime that wins a hot loop can still lose on startup, input latency, memory pressure, accessibility, background energy, or recovery.

This packet defines a deferred research route for `RQ-19`. It does not select an interpreter, bytecode format, collector, JIT, Cranelift, tiering policy, or code-cache policy.

## Source-backed observations

### ECMAScript defines behavior, not a required collector

The ECMAScript specification is the semantic oracle for language behavior. Its treatment of `WeakRef` and `FinalizationRegistry` explicitly makes garbage collection timing non-deterministic and permits hosts to schedule cleanup. A runtime experiment must therefore distinguish observable language semantics from implementation-only collection timing and must never use finalization as a correctness or benchmark completion signal.

Source: [ECMAScript Language Specification](https://tc39.es/ecma262/), retrieved 2026-07-19.

### V8 documents tiering as a startup/peak-performance tradeoff

V8's public documentation describes an interpreter and optimizing compiler for JavaScript, and baseline plus optimizing tiers for WebAssembly. It reports that a fast baseline tier can reduce startup cost while an optimizing tier improves peak execution, and that background or dynamic compilation consumes CPU, memory, and scheduling capacity. The observations demonstrate tradeoffs and evidence fields; they do not establish that Turing should copy V8's tiers or heuristics.

Sources: [V8 Sparkplug](https://v8.dev/blog/sparkplug), [V8 Liftoff](https://v8.dev/blog/liftoff), and [V8 WebAssembly dynamic tiering](https://v8.dev/blog/wasm-dynamic-tiering), retrieved 2026-07-19.

### A code generator is a component boundary, not a runtime decision

Wasmtime documents Cranelift as an optimizing code generator used for fast runtime or ahead-of-time WebAssembly compilation, with configuration for different CPU and memory environments. This is evidence that a reviewed code generator can be evaluated as a bounded dependency, not evidence that Cranelift is suitable for Turing's JavaScript semantics, JIT security model, licensing/provenance boundary, or release path.

Source: [Bytecode Alliance Wasmtime](https://github.com/bytecodealliance/wasmtime), retrieved 2026-07-19.

## Candidate runtime models

The owner-approved comparison should include:

1. Semantically precise interpreter with no JIT, serving as a correctness, determinism, and low-complexity baseline.
2. Interpreter plus fast baseline compiler with explicit tier-up and tier-down policy.
3. Interpreter plus baseline and optimizing tiers with guarded assumptions, deoptimization, and invalidation.
4. WebAssembly or other bounded-code paths evaluated separately from JavaScript object semantics and host authority.

Each model must define bytecode identity, stack/register representation, object and shape metadata, inline caches, code lifetime, executable-memory policy, deoptimization state, collector roots, external-memory accounting, and behavior under cancellation, process restart, and memory pressure.

## Collector and lifetime questions

The experiment must distinguish:

- tracing and root discovery cost;
- young/old generation or alternative region policy;
- pause, concurrent, incremental, and mutator-assist behavior;
- weak references and finalization semantics;
- native/DOM wrappers and cross-boundary roots;
- external memory such as images, ArrayBuffers, decoded resources, and host handles;
- code memory, metadata, inline-cache retention, and deoptimization debris;
- process termination, tab freezing, recovery, and profile/session ownership.

No collector may reclaim an object, wrapper, resource, or capability while a browser or script-visible identity remains live. The safety model must cover stale document epochs, cross-origin identity, renderer restart, and agent observations.

## Evidence and oracle design

Before a runtime decision, the owner-approved package should provide:

- ECMAScript conformance and negative tests for every optimized semantic path;
- representative cold-start, short-script, interactive, long-running, allocation-heavy, promise/async, DOM, typed-array, worker, and adversarial workloads;
- warm-up and tier-transition traces with compilation queue, code size, assumptions, deoptimization, and cancellation events;
- GC traces with pause, concurrent work, mutator assistance, reclaimed bytes, fragmentation, external memory, and failure denominators;
- no-JIT, baseline-only, and optimized configurations measured under the same workload and security policy;
- memory snapshots that separate JS heap, native wrappers, code, metadata, allocator overhead, and retained page resources;
- deterministic replay or equivalent semantic oracle for tier transitions and collection-sensitive bugs;
- W^X/executable-memory, sandbox, side-channel, pointer integrity, fuzzing, and crash-recovery evidence;
- independent review of compiler provenance, unsafe code, backend maintenance, licensing, and generated output.

## Measurement plan

Report distributions for:

- startup to first script execution and first interactive action;
- input-to-result latency, long tasks, frame pacing, and event-loop delay;
- warm-up time, tier-up delay, deoptimization frequency, and code-cache hit/miss behavior;
- total CPU, compilation CPU, GC CPU, wakeups, energy, and peak/live/retained memory;
- collector pause quantiles and tail latency under allocation and pressure;
- code and metadata size, executable-memory footprint, and cache eviction;
- correctness failures, timeouts, crashes, unsupported features, and cleanup;
- performance after tab freeze/revival, renderer restart, and resource-pressure recovery.

A peak benchmark score cannot compensate for a worse cold path, tail latency, memory pressure, security configuration, accessibility workflow, or recovery denominator. Results require exact engine revision, compiler/toolchain, CPU, OS, flags, workload, process model, sample count, raw traces, and analysis policy.

## Rejection rules

Reject the packet as decision evidence when it:

- treats a JIT or collector's undocumented behavior as language semantics;
- uses `FinalizationRegistry` timing as a correctness, cleanup, or performance oracle;
- compares hot code without cold-start, warm-up, deoptimization, code-memory, and GC costs;
- hides compilation or collection work in background threads or drops failed samples;
- claims a third-party code generator is approved because it can compile WebAssembly;
- weakens W^X, sandboxing, process identity, origin policy, or side-channel controls for speed;
- omits DOM/native-wrapper roots, external memory, worker state, or renderer restart;
- uses same-agent tests, self-generated oracles, or a single benchmark as independent evidence;
- reports a lower memory number after silently disabling features, accessibility, security, or recovery.

## Current status and next proof

`RQ-19` remains deferred outside the active pre-build crosswalk. The next proof is an owner-approved runtime semantic baseline and measurement manifest, followed by a no-JIT/interpreter oracle and isolated tiering/collector experiments. No runtime architecture, JIT, collector, memory result, performance result, security result, compatibility result, or readiness claim follows from this packet.

## Claim boundary

This is source-backed research preparation only. It does not select a JavaScript engine, bytecode format, interpreter, compiler backend, JIT, collector, tiering policy, code cache, executable-memory policy, performance target, or production support claim.
