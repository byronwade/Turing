# 06 — JavaScript Runtime and WebAssembly Plan

## 1. Scope and honesty rule

A competitive JavaScript engine is a multi-year compiler, runtime, garbage-collector, security, and conformance program. Turing will not hide this behind an embedded V8, JavaScriptCore, SpiderMonkey, QuickJS, or system runtime. Early builds intentionally execute a limited language subset through a Turing-owned interpreter. Performance claims begin only after Test262 coverage, web bindings, GC stability, and exploit mitigations are measured.

A compiler backend such as Cranelift may generate machine code from Turing-owned intermediate representation. That does not outsource ECMAScript semantics, object layout, inline caches, deoptimization, garbage collection, Web IDL, event-loop integration, or security policy.

## 2. Runtime layers

1. **Source manager:** UTF-16-compatible source indexing, line maps, source URLs, source maps, and bounded retention.
2. **Lexer/parser:** current ECMAScript grammar, early errors, modules, script goals, and recoverable diagnostics for DevTools.
3. **AST and scope analysis:** bindings, closures, private names, strict mode, hoisting, captures, and module dependencies.
4. **Bytecode compiler:** register or hybrid bytecode with explicit exception regions, source positions, liveness, and inline-cache sites.
5. **Interpreter:** portable reference execution and profiling counters.
6. **Runtime/object model:** values, objects, shapes, properties, prototypes, arrays, typed arrays, functions, promises, proxies, iterators, generators, regular expressions, dates, errors, collections, weak references, and internationalization bridge.
7. **Garbage collector:** exact tracing, generational collection, incremental/concurrent phases only after barriers are proven, ephemerons, weak processing, finalization, and external-memory accounting.
8. **Baseline JIT:** fast bytecode-to-machine-code lowering with inline caches and safepoints.
9. **Optimizing JIT:** typed IR, speculative guards, inlining, escape analysis, scalar replacement, common-subexpression elimination, bounds-check elimination, deoptimization, and tiering policy.
10. **Embedding/Web IDL:** generated bindings, realms, wrappers, exception translation, security checks, task queues, and lifecycle cancellation.
11. **Debugger/profiler:** breakpoints, stepping, scopes, async stacks, coverage, sampling, allocation tracking, heap snapshots, and protocol events.
12. **WebAssembly:** validation, interpreter/reference tier, compiler backend, imports/exports, memories, tables, and feature staging.

## 3. Value and object representation

The first implementation uses a clear tagged-value representation with architecture-specific optimization hidden behind an interface. NaN-boxing or pointer compression is adopted only after portability, sanitizer, debugger, and memory benefits are demonstrated.

Objects use hidden classes/shapes with transition tables, compact property storage, and dictionary fallback. Shape identity is realm-aware. Proxies, accessors, indexed properties, typed arrays, module namespaces, exotic objects, and host objects use dedicated operation tables rather than undefined shortcuts.

Security invariants:

- no pointer bits or uninitialized memory leak into script-visible values;
- integer overflow and length arithmetic are checked before allocation;
- array-buffer detachment and transfer are explicit states;
- JIT code never trusts a speculative type without a guard and deoptimization path;
- object and code pointers are not accepted from serialized renderer messages;
- executable memory follows write-xor-execute and platform code-signing requirements.

## 4. Interpreter-first sequence

### Phase JS-0 — language kernel

Implement values, lexical environments, expressions, statements, functions, objects, property lookup, exceptions, and a deterministic bytecode interpreter. No web DOM dependency is required. Gate: selected Test262 language core and differential traces.

### Phase JS-1 — modern language semantics

Add classes, modules, promises, async functions, generators, iterators, proxies, typed arrays, collections, symbols, weak references, regular expressions, and internationalization bridge. Gate: published Test262 pass map with exclusions categorized.

### Phase JS-2 — web embedding

Generate Web IDL bindings; integrate realms, event loop, tasks/microtasks, timers, DOM wrappers, events, fetch promises, workers, structured clone, modules, and lifecycle cancellation. Gate: engine/web tests plus memory-leak and wrapper-identity tests.

### Phase JS-3 — baseline JIT

Compile hot bytecode using a backend or minimal native assembler layer. Add polymorphic inline caches, safepoints, stack maps, on-stack replacement where justified, and deoptimization to interpreter/baseline state. Gate: W^X enforcement, JIT fuzzing, tier-equivalence tests, and platform signing support.

### Phase JS-4 — optimizing JIT

Introduce a typed SSA-like IR and speculation based on observed shapes/types. Every optimization must pass randomized differential execution against the interpreter. Optimization is disabled for unsupported or high-risk constructs rather than producing unsound code.

### Phase JS-5 — sustained competitiveness

Profile-guided tiering, concurrent compilation, code cache policy, pointer compression only where safe, advanced regular-expression engine, WebAssembly optimization, and workload-specific tuning. At this phase, performance is compared to named browser versions on fixed hardware and corpora.

## 5. Garbage collection

The GC begins stop-the-world and exact so correctness is tractable. The target architecture is generational with incremental marking and optional concurrent work.

Heap spaces may include:

- nursery/young generation;
- mature movable or segregated spaces;
- large-object space;
- code and metadata spaces;
- read-only/shared immutable built-ins where safe;
- external backing stores for array buffers, strings, canvas/media, and host objects.

Requirements:

- exact roots from VM stacks, handles, globals, modules, job queues, embedder wrappers, and JIT stack maps;
- write barriers mechanically centralized and stress-tested;
- weak maps/sets and ephemerons reach a correct fixed point;
- finalizers never run arbitrary script in GC-internal critical sections;
- DOM wrapper liveness and cross-component cycles have a defined tracing contract;
- per-realm and per-document memory is estimated for attribution;
- collection scheduling respects interaction deadlines and background lifecycle;
- pressure signals can request collection but cannot violate invariants;
- heap snapshots redact sensitive strings unless explicit local developer authorization is active.

GC verification modes run in CI: collect at every allocation opportunity, randomize collection schedules, poison freed memory, validate barriers, and compare heap graphs.

## 6. Web IDL and host bindings

Bindings are generated from reviewed interface definitions. Generated code handles argument conversion, overload resolution, dictionaries, unions, promises, callbacks, exceptions, brand checks, realm selection, exposure sets, secure-context requirements, permissions, user activation, and lifecycle state.

Host objects do not expose Rust references directly. They use rooted handles and document/frame identity. A callback against a destroyed or navigated document fails through epoch validation.

Cross-origin wrappers expose only specified operations. Agent tools never invoke private binding shortcuts; they submit browser actions through the agent protocol.

## 7. Event loop

Each agent cluster/realm group has explicit task sources and microtask checkpoints. Rendering opportunities, timers, networking, parser tasks, posted messages, user interaction, lifecycle transitions, and idle work follow the platform ordering model.

The scheduler records task source, enqueue time, start/end, principal, document epoch, cancellation, and attribution. Background policy may clamp timers or defer task sources only where platform behavior permits. A page cannot escape throttling by spawning unbounded workers or recursive cross-context messages.

## 8. Modules

The module loader separates fetch, parse, link, instantiate, and evaluate. It supports URL resolution, import maps, credentials/referrer policy, MIME checks, CORS, cycles, top-level await, dynamic import, workers, and module scripts. Module maps are partitioned by the required environment and do not leak across profiles or incompatible origins.

Compiled-code caching stores versioned, integrity-bound metadata. Cache input includes engine version, architecture, feature flags, source hash, origin/partition policy, and security mode. Invalid cache entries are discarded, never partially trusted.

## 9. Regular expressions and internationalization

Regular expressions require dedicated denial-of-service testing, stack/heap limits, Unicode correctness, and JIT isolation. Begin with a safe interpreter/NFA-oriented implementation and add optimized paths behind equivalence tests.

Internationalization uses audited locale, collation, number/date, plural, segmentation, and time-zone data through a narrow adapter. Turing owns ECMAScript-visible semantics and version reporting but does not invent locale data.

## 10. WebAssembly

WebAssembly launches after the JS embedding and sandbox foundation are stable. Sequence:

1. binary decoder and validator with strict bounds;
2. reference interpreter;
3. compiler backend with explicit memory/table guards;
4. streaming compile and cache;
5. SIMD, reference types, multiple memories, threads, GC, exceptions, and component-related features only when standardized and threat-modeled.

Native code follows W^X, control-flow protections where available, guard pages, signal/exception isolation, stack limits, and deterministic trap mapping. Shared-memory threads require cross-origin isolation policy and memory-model tests.

## 11. JIT security

JIT-specific controls include:

- writable and executable mappings are never simultaneous;
- code pages are sealed through platform APIs before execution;
- constant pools and jump tables are bounds-validated;
- indirect branches use available CFI/PAC/CET protections;
- generated code contains safepoints and precise stack maps;
- deoptimization metadata is range-checked;
- tier transitions are randomized in fuzzing;
- interpreter, baseline, and optimizing tiers are differentially compared;
- a no-JIT mode remains supported for hardening, platforms, testing, and incident response;
- code cache is non-authoritative and version-bound.

## 12. Performance methodology

Performance suites include language microtests only as diagnostics. Release decisions prioritize representative page and application workloads, startup, parse/compile latency, interaction responsiveness, memory, GC pauses, code size, and energy.

Every result reports:

- exact build and feature flags;
- hardware, OS, thermal/power state;
- cold/warm cache state;
- interpreter/JIT tier state;
- iteration count and statistical treatment;
- correctness/conformance coverage of the tested feature set;
- failures, timeouts, and exclusions.

A faster result obtained by omitting language behavior or disabling mitigations is labeled as an experiment, not a product result.

## 13. Runtime gates

- **JS-GATE-1:** deterministic interpreter passes the declared Test262 core subset and tier/reference differential harness.
- **JS-GATE-2:** web bindings pass identity, exception, lifecycle, cross-origin, and leak tests.
- **JS-GATE-3:** GC survives stress, fuzzing, weak-reference, wrapper-cycle, and OOM-injection suites.
- **JS-GATE-4:** baseline JIT passes W^X, sanitizer, randomized-tier, and deoptimization tests on all supported platforms.
- **JS-GATE-5:** optimizing JIT shows statistically meaningful end-to-end wins without conformance or security regression.
- **JS-GATE-6:** WebAssembly is disabled by default until validator, trap, memory, and sandbox gates pass.
