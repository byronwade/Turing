# JavaScript Runtime Security, Testing, and Performance

Status: research and design baseline  
Owner: runtime quality and performance  
Purpose: Define the evidence required before runtime speed, safety, or compatibility claims.

## Relationship to the Turing program

This document supplies the detailed evidence model for JS-GATE-1 through JS-GATE-6 and complements [testing and compatibility](../blueprint-v1/12-testing-compatibility.md).

## Conformance accounting

Test262 results are published by commit, host harness, feature, built-in, module mode, internationalization support, tier, platform, pass, fail, skip, timeout, crash, and harness error. Unsupported features stay in the denominator or a separately explicit full denominator. Metadata patches and expected failures have owners and expiry.

Web-facing behavior also requires WPT because language conformance alone does not validate bindings, realms, event loops, workers, modules, lifecycle, or security policy.

## Differential execution

Generated and reduced programs run in the interpreter and every enabled compiler tier under randomized tier thresholds, GC schedules, interrupt points, and architecture configurations. Reference engines can help identify disagreements, but ECMA-262, ECMA-402, tests, and reasoned interpretation decide correctness.

Comparisons include values, exceptions, side-effect order, object graphs where observable, module behavior, debugger state, and termination.

## Fuzzing and unsafe verification

Continuous targets cover lexer, parser, AST transforms, bytecode encoder/decoder, verifier, interpreter, object operations, regular expressions, structured clone, Web IDL bindings, GC, stack maps, compiler IR, optimizations, code generation, deoptimization, WebAssembly, and debugger protocol.

Unsafe code uses Miri where applicable, sanitizers, guard pages, fuzzing, model tests, and targeted review. Crashes are reduced by root cause and retained privately when exploitable.

## Performance model

Runtime performance is evaluated as part of page and application interaction. Metrics include parse and compile latency, first execution, warm-up, tier transition, code size, instruction/cache behavior where available, GC pauses, total collection work, heap growth, external memory, worker overhead, energy, and input/frame interference.

JetStream-family results are diagnostics. They cannot outweigh missing semantics, poor Speedometer-style interaction, excessive code memory, GC tails, or disabled mitigations.

## Latency and scheduler integration

Compilation, GC, regex, module loading, and WebAssembly work participate in browser deadlines. Off-thread work has queue limits and cancellation. Long pauses are attributed to stage and principal. Background compilation or collection yields under input, visible frame, thermal, or battery pressure.

A runtime optimization is rejected if it produces better throughput while worsening validated p95/p99 interaction beyond budget without a justified product tradeoff.

## Security release evidence

Each release records no-JIT behavior, executable-memory policy, platform mitigations, unsafe inventory, fuzzing duration/coverage, known JIT or GC gaps, code-cache policy, Test262 coverage, WPT embedding coverage, and emergency feature-disable controls.

## Developer diagnostics

Developers can inspect bytecode, tier, inline-cache states, shape churn, compile queues, optimization reasons, deoptimization, GC phases, allocation, retainers, code memory, and task causality. Diagnostics are bounded, redacted, and versioned so the tools do not become a privileged backdoor.

## Non-negotiable invariants

- No performance result is valid without conformance coverage and mitigation configuration.
- All tiers are differentially tested under randomized schedules.
- Fuzzing includes resource exhaustion, cancellation, malformed caches, and metadata.
- Background runtime work cannot starve browser input or rendering indefinitely.
- Security-sensitive failures remain confidential until coordinated disclosure.

## Required evidence

- Pinned Test262 and WPT dashboards with raw counts and exclusions.
- Continuous fuzzing, sanitizers, Miri, model tests, and minimized corpora.
- Fixed-hardware application, startup, warm-up, memory, GC, code-size, and energy results.
- No-JIT equivalence and emergency-disable drills.
- Developer workflow studies for runtime diagnosis and memory leaks.
- Long-duration tab churn, worker, module, debugger, and navigation leak tests.

## Known risks and unresolved questions

- Microbenchmarks can overfit compiler heuristics and misrepresent product performance.
- Instrumentation overhead can distort the behavior it observes.
- A small team may not sustain rapid JIT vulnerability response across platforms.
- Internationalization and regular-expression completeness can lag headline language scores.

## Primary sources

- Test262 — https://github.com/tc39/test262
- Web Platform Tests — https://web-platform-tests.org/
- JetStream — https://browserbench.org/
- Speedometer — https://browserbench.org/Speedometer3.1/
- Miri — https://github.com/rust-lang/miri
- Rust Fuzz Book — https://rust-fuzz.github.io/book/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
