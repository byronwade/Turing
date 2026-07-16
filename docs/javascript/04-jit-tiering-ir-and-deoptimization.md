# JIT Tiering, Intermediate Representations, and Deoptimization

Status: research and design baseline  
Owner: JIT compiler architecture  
Purpose: Define a staged compiler that improves interaction latency without outrunning conformance or exploit mitigations.

## Relationship to the Turing program

This document expands JS-GATE-4 and JS-GATE-5 in [Blueprint 06](../blueprint-v1/06-javascript-runtime.md). JIT attack-surface requirements are also governed by the [security engineering book](../security-engine/README.md).

## Tiering strategy

The interpreter remains the oracle. A direct bytecode-to-machine-code baseline tier should minimize compilation latency and preserve simple frame mapping. A later mid-tier may use a compact SSA-like representation and inexpensive type/shape specialization. A high-optimization tier is justified only after representative applications show sustained wins beyond the maintenance and security cost.

Tier thresholds consider execution count, loop behavior, function size, code-cache pressure, device class, foreground deadlines, battery state, debugger attachment, and deoptimization history. Tiering itself is observable and bounded.

## Baseline compiler

The baseline tier lowers each validated bytecode instruction through reviewed templates or a compiler backend. It emits safepoints, exception tables, source positions, stack maps, patchable inline-cache sites, and explicit calls to shared semantic helpers. Compilation can occur off-thread only after source, bytecode, realm, and cancellation lifetimes are stable.

Baseline machine code must be easy to discard. It cannot become authoritative for language or debugger state.

## Intermediate representations

A mid-tier begins from bytecode plus profiling facts and produces a typed graph with explicit control, values, memory effects, exceptions, deoptimization exits, and safepoints. Every optimization states its preconditions, preserved semantics, and fallback.

High-tier transformations may include inlining, constant folding, common-subexpression elimination, range analysis, bounds-check elimination, escape analysis, scalar replacement, loop optimization, and representation selection. Operations involving proxies, accessors, detach/resize, user callbacks, cross-realm values, or host effects must model those effects conservatively.

## Guards and deoptimization

Speculation is never trusted without a guard. Deoptimization metadata reconstructs interpreter-visible frames, values, scopes, exceptions, generator state, and debugger positions. Metadata is range-checked and version-bound. A failed reconstruction is a security-critical runtime defect, not a recoverable optimization miss.

On-stack replacement and tier-down require explicit state maps. Repeated deoptimization can disable a site or function to avoid thrashing.

## Code memory and platform policy

Writable and executable mappings are never simultaneous. Code is produced in writable buffers, validated where applicable, sealed with platform APIs, and then executed. macOS hardened-runtime/code-signing constraints, Windows dynamic-code and control-flow mitigations, and Linux memory policy are part of supported-platform gates.

Code pointers, jump tables, relocation records, constants, and call targets are validated. Guard pages, stack limits, CFI, PAC, CET, and indirect-branch protections are used where available and measured.

## Concurrency and code cache

Compiler workers receive immutable bytecode, profile snapshots, and bounded requests rather than VM internals. Publication validates realm/runtime identity and cancellation. A navigation or realm teardown invalidates pending work.

Persistent code caches include engine build, architecture, OS ABI, mitigation mode, source integrity, feature flags, origin/partition policy, and compiler version. The cache is discardable and never loaded from untrusted page-controlled paths without full validation.

## Compiler observability

DevTools records compilation queueing, tier transitions, optimization decisions, guards, deoptimizations, code size, compile time, invalidation, stack maps, and cache hits. Production telemetry uses aggregate reason codes without source or private page content.

## Non-negotiable invariants

- Every tier is continuously differential-tested against the interpreter.
- Executable memory obeys W^X and platform signing/mitigation policy.
- Every speculative assumption has a guard and a complete deoptimization path.
- Stack maps and reconstructed frames are precise and range-validated.
- Compiler workers cannot outlive or publish into the wrong runtime, realm, or document.
- No-JIT mode remains complete and supported.

## Required evidence

- Randomized tiering and interpreter/baseline/mid/high-tier differential fuzzing.
- JIT spraying, malformed metadata, deoptimization, OSR, exception, debugger, and GC stress tests.
- Platform W^X, code-signing, CFI/PAC/CET, and dynamic-code evidence.
- Compile latency, warm-up, code size, memory, energy, and end-to-end application results.
- Security review of every unsafe assembler, relocation, stack-map, and code-memory boundary.
- Cranelift-versus-custom baseline experiment defined by RQ-09.

## Known risks and unresolved questions

- Optimizing compiler complexity can dominate the project and introduce severe security risk.
- Tiering can improve steady-state scores while hurting user-visible warm-up or battery life.
- Incorrect deoptimization can expose stale pointers or wrong realm state.
- A persistent code cache expands supply-chain and parser attack surface.

## Primary sources

- V8 Sparkplug — https://v8.dev/blog/sparkplug
- V8 Maglev — https://v8.dev/blog/maglev
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html
- SpiderMonkey documentation — https://firefox-source-docs.mozilla.org/js/index.html
- Cranelift — https://cranelift.dev/
- Apple Hardened Runtime — https://developer.apple.com/documentation/security/hardened-runtime

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
