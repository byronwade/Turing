# JavaScript Front End, Bytecode, and Interpreter

Status: research and design baseline  
Owner: JavaScript front-end and interpreter  
Purpose: Define a correct, inspectable path from source text to reference execution.

## Relationship to the Turing program

This document expands [Blueprint 06](../blueprint-v1/06-javascript-runtime.md) and supplies experiments for RQ-07. Web embedding is defined in [WebAssembly, Web IDL, modules, and the event loop](05-webassembly-webidl-and-event-loop.md).

## Source representation and indexing

Source text must support ECMAScript indexing rules, source URLs, line and column maps, source maps, modules, eval origins, debugger locations, and bounded retention. The implementation should avoid assuming one byte equals one source position. Source slices used by errors or DevTools are represented by checked offsets into versioned source objects. Large sources may retain summaries or compressed backing after compilation, but debugger behavior and error spans must remain explicit.

The source manager owns origin metadata, response URL, source-map provenance, encoding outcome, integrity state, script goal, realm, and document epoch. Cross-profile or cross-origin source reuse is prohibited unless the cache key proves policy equivalence.

## Lexer and parser

The lexer and parser implement current ECMA-262 grammar, automatic semicolon insertion, contextual keywords, template literals, regular-expression lexical goals, private names, Unicode escapes, early errors, strict mode, script/module goals, and proposal features only after their standards stage and support policy permit them.

Parsing is cancellable and bounded by source size, nesting, literal size, identifier count, scope count, and diagnostic volume. Diagnostics preserve expected-token context and recovery without allowing malformed input to produce partially trusted executable state. Fuzz builds expose token and AST traces suitable for reduction.

## Scopes, bindings, and modules

Scope analysis records lexical, variable, function, class, private-name, catch, parameter, and module environments. It determines captures, temporal dead zones, hoisting, arguments behavior, direct eval effects, private-brand checks, and dynamic-name lookups before bytecode generation where semantics permit.

Module parsing produces import/export tables and dependency requests without performing network or policy work. Fetching, linking, instantiation, and evaluation remain distinct operations. Cycles, top-level await, dynamic import, import maps, MIME checks, CORS, and cancellation are integrated through the host layer rather than hidden parser callbacks.

## Bytecode format

The first format should be register-based or hybrid, selected by RQ-07 evidence. Every instruction has a documented operand encoding, stack/register effect, exception behavior, source location, safepoint behavior, and validation rule. Functions carry explicit exception regions, constant pools, liveness metadata, inline-cache sites, and version identity.

Bytecode is validated before execution and after deserialization. The cache format includes runtime version, architecture-independent semantic version, feature set, source hash, realm policy, and security mode. Invalid or stale entries are discarded.

## Reference interpreter

The interpreter is intentionally simple enough to audit and use as a differential oracle. Dispatch strategy, register storage, call frames, exception unwinding, generators, async suspension, and debugger hooks must be deterministic in test modes. Host calls pass through generated bindings and explicit completion records.

Profiling counters are separate from semantics. A counter overflow, disabled profiler, or debugger attachment cannot change observable execution. The interpreter supports forced-GC, randomized task, interrupt, and tiering schedules for stress tests.

## Interrupts, cancellation, and budgets

Execution polls at bounded points for termination, navigation, process shutdown, debugger pause, memory pressure, watchdog deadlines, agent cancellation, and background policy. Interrupt handling cannot run arbitrary script inside an unsafe runtime critical section.

Instruction, stack, recursion, allocation, regular-expression, worker, and wall-clock budgets have explicit outcomes. Product policy may terminate a runaway context, but the reason is surfaced to diagnostics and never confused with a language exception.

## Non-negotiable invariants

- No malformed source or cache entry reaches execution without structural validation.
- The interpreter is the reference oracle for all later tiers.
- Source positions, exception ranges, and safepoints are checked and versioned.
- Host effects occur only through explicit bindings and task sources.
- Cancellation and termination cannot leave a partially committed module or corrupted VM state.

## Required evidence

- Pinned Test262 results for every enabled syntax and semantic feature.
- Parser differential and grammar-aware fuzzing with minimized cases.
- Bytecode validation, round-trip, malformed-cache, and version-mismatch tests.
- Interpreter traces compared across architectures and randomized schedules.
- Source-map, debugger-location, exception, module-cycle, and cancellation tests.
- Code size, parse time, bytecode size, dispatch cost, and memory by source class.

## Known risks and unresolved questions

- Grammar recovery can hide incorrect early-error behavior.
- Direct eval and dynamic scope can distort otherwise compact environment representations.
- An overly clever bytecode format can harm diagnostics, baseline lowering, and maintenance.
- Unbounded source retention can dominate memory in developer-heavy sessions.

## Primary sources

- ECMA-262 — https://tc39.es/ecma262/
- Test262 — https://github.com/tc39/test262
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html
- SpiderMonkey documentation — https://firefox-source-docs.mozilla.org/js/index.html

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
