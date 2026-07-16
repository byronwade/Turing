# JavaScript Runtime Engineering Book

Status: detailed research and design baseline  
Owner: JavaScript runtime and compiler architecture  
Canonical overview: [Blueprint 06 — JavaScript runtime](../blueprint-v1/06-javascript-runtime.md)

This book expands the runtime roadmap into contracts for a Turing-owned ECMAScript implementation. It separates language correctness, host integration, memory management, machine-code generation, security, and developer observability. It does not claim Test262 coverage, web compatibility, or competitive execution speed.

## Reading order

1. [Front end, bytecode, and interpreter](01-front-end-bytecode-interpreter.md)
2. [Values, objects, shapes, and inline caches](02-values-objects-shapes-and-inline-caches.md)
3. [Garbage collection and host lifetimes](03-garbage-collection-and-host-lifetimes.md)
4. [JIT tiering, intermediate representations, and deoptimization](04-jit-tiering-ir-and-deoptimization.md)
5. [WebAssembly, Web IDL, modules, and the event loop](05-webassembly-webidl-and-event-loop.md)
6. [Runtime security, testing, and performance](06-runtime-security-testing-and-performance.md)

## Runtime-wide thesis

Turing should build a precise interpreter as the semantic oracle, then add execution tiers whose observable behavior is continuously compared with that oracle. A fast baseline tier should reduce warm-up cost before the project attempts a complex optimizing compiler. Garbage collection, DOM wrappers, task scheduling, modules, WebAssembly, debugger state, and deoptimization metadata must be designed together rather than attached after the fact.

The runtime is not an isolated benchmark executable. It is part of a hostile, multi-realm web platform with document lifecycles, cross-origin wrappers, user-visible latency deadlines, background throttling, process suspension, memory pressure, debugger attachment, and security mitigations.

## Cross-cutting contracts

- Test262 and explicit implementation notes define language conformance; another engine is only a differential signal.
- Interpreter, baseline, mid-tier, and optimizing tiers must produce equivalent observable behavior.
- Every executable-code path supports write-xor-execute, precise stack maps, bounded metadata, and platform signing requirements.
- A realm, agent cluster, module map, document epoch, and process are distinct identities.
- Host objects are addressed through rooted handles; script never receives raw Rust references or process pointers.
- GC barriers, roots, weak processing, finalization, and external-memory accounting are centralized and stress-verifiable.
- Code caches are optional, versioned, integrity-bound accelerators and never authoritative state.
- The runtime exposes why code tiered, deoptimized, collected, blocked, or consumed memory.
- A no-JIT mode remains supported for hardening, incident response, testing, and constrained platforms.

## Implementation sequence

1. source manager, lexer, parser, scopes, and deterministic diagnostics;
2. explicit bytecode format and interpreter;
3. values, objects, shapes, properties, functions, exceptions, and built-ins;
4. promises, modules, iterators, proxies, typed arrays, regular expressions, and internationalization;
5. exact stop-the-world tracing collector and rooted host handles;
6. Web IDL bindings, realms, tasks, microtasks, workers, and structured clone;
7. fast baseline compiler and polymorphic inline caches;
8. typed mid-tier and controlled deoptimization;
9. optimizing tier only after sustained equivalence, fuzzing, and end-to-end wins;
10. WebAssembly validation and execution behind independent gates.

## Leadership criteria

A top-tier Turing runtime must publish full Test262 accounting by feature and tier, representative web-application traces, parse/compile/warm-up latency, bytecode and machine-code size, GC pause distributions, memory ownership, energy impact, JIT security evidence, debugger fidelity, and every exclusion. A synthetic score without the supported semantics and mitigation configuration is not a product result.

## Related material

- [Browser engine book](../engine/README.md)
- [Security engineering book](../security-engine/README.md)
- [Performance engineering book](../performance/README.md)
- [Developer experience book](../developer-experience/README.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
