# 06 — M3: JavaScript Runtime and Dynamic DOM

Status: implementation game plan  
Owner: JavaScript, GC, Web IDL, DOM, security, performance, and quality

## 1. Objective

M3 introduces an interpreter-first JavaScript runtime, exact tracing GC, DOM bindings, event loops, timers, and dynamic style/layout while preserving a trustworthy semantic reference for later JIT tiers.

## 2. Entry gates

- WP-007 DOM handles, lifetimes, mutation epochs, and event skeleton are stable enough for bindings.
- WP-010 may start independently after WP-001, but WP-011 waits for both DOM and runtime contracts.
- Test262 revision and feature map are pinned.
- Realm, process, document-epoch, cancellation, OOM, and trace identities are defined.
- Runtime code runs inside the renderer sandbox and has no ambient broker authority.
- Code generation, executable-memory, and JIT permissions remain absent in M3 unless an explicit experiment is isolated and non-production.

## 3. WP-010 — language kernel

Task sequence:

1. UTF-16/code-point/source-location contract;
2. lexer and automatic semicolon insertion;
3. parser and early errors;
4. AST or direct bytecode lowering decision;
5. versioned bytecode and verifier;
6. stack-based or register-based interpreter reference;
7. primitive values, strings, symbols, big integers, and numeric semantics;
8. objects, property descriptors, prototypes, arrays, functions, closures, and environments;
9. exceptions, completion records, iterators, generators, and async foundations;
10. classes and modules subset;
11. realm, intrinsics, global object, and host-hook boundaries;
12. Test262 runner, feature manifest, differential tests, and reducer;
13. parser/bytecode/runtime fuzzing and resource caps.

The interpreter defines correctness. Later tiers must be differentially equivalent.

## 4. WP-011 — exact tracing GC and Web IDL

### GC sequence

- heap object header and type metadata;
- explicit roots and rooted handle API;
- exact trace implementation;
- stop-the-world mark/sweep reference collector;
- allocation budgets, collection triggers, OOM propagation, and external-memory accounting;
- weak references and finalization only after lifecycle semantics are tested;
- stress mode collecting at nearly every allocation boundary;
- heap verification and poisoning in research builds;
- document/realm teardown and leak detection;
- later write-barrier and generational/concurrent designs behind equivalence tests.

### Binding sequence

- canonical Web IDL subset and parser/generator;
- interface, dictionary, enum, callback, overload, conversion, exception, and nullable handling;
- wrapper identity and one-wrapper-per-realm rules;
- DOM-to-JS and JS-to-DOM lifetime ownership;
- current document epoch and realm validation;
- security-origin and exposure checks outside generated convenience code;
- deterministic generated-code review and drift checks;
- binding conformance and fuzz tests.

## 5. Event loop and page integration

Implement:

- tasks and microtasks with explicit sources;
- timer IDs, minimums, nesting, cancellation, and background policy hooks;
- event dispatch, default actions, and user activation tokens;
- promise jobs and unhandled rejection reporting;
- dynamic DOM mutation and style/layout scheduling;
- script parser integration with pause/resume and document.write policy only when defined;
- module loading interface without production network loading until M4;
- structured clone reference subset;
- workers as a later bounded task after main-realm semantics are stable.

Every asynchronous callback validates realm, frame, document epoch, and cancellation state.

## 6. Security requirements

- No `eval` or dynamic-code shortcut bypasses parser/bytecode validation.
- Stack, recursion, source, bytecode, object, property, string, array, promise, task, and microtask growth are bounded.
- Host objects expose only reviewed Web IDL operations.
- Runtime errors never reveal cross-origin or secret state.
- Debugger attachment is explicit and visible.
- Time and memory instrumentation is not silently disabled for compatibility.
- JIT and WebAssembly executable memory remain outside the M3 production surface.

## 7. Developer tooling

M3 adds research-grade:

- console evaluation in the attached realm;
- parser and bytecode views;
- breakpoints and single-step interpreter hooks;
- call stack, scope, value, exception, promise, task, and microtask inspection;
- GC allocation, collection, root, retain-path, and external-memory diagnostics;
- wrapper and document-epoch diagnostics;
- deterministic trace/replay for supported inputs.

## 8. Verification

- published Test262 feature map and exact denominator;
- parser and interpreter differential testing against multiple references where licenses and harnesses permit;
- bytecode verifier negative corpus;
- GC stress and heap verification;
- wrapper identity, realm, navigation, teardown, and cross-origin tests;
- event loop ordering and timer tests;
- dynamic DOM/style/layout WPT subset;
- OOM, cancellation, timeout, stack overflow, process crash, and restart tests;
- fuzzing for parser, bytecode, runtime values, structured clone, and bindings;
- fixed-hardware interpreter, allocation, GC pause, memory, and dynamic-layout baselines;
- sandbox and secret-redaction review.

## 9. Exit criteria

- declared JavaScript subset reaches its chosen Test262 threshold;
- no known wrapper identity or lifetime leak survives repeated navigation/realm teardown stress;
- exact GC remains available as a reference mode;
- dynamic DOM reduced tests and WPT subset pass;
- failures and unsupported features are visible rather than web-compatibility hacks;
- M4 receives stable host hooks for modules, Fetch, workers, navigation, and storage;
- arbitrary-web browsing remains explicitly unsafe and incompatible.
