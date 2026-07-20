# JavaScript Bytecode Representation Research - July 2026

Status: deferred `RQ-07` no-claim research packet
Owner: JavaScript runtime, compiler, debugging, memory, security, and quality
Research date: 2026-07-19
Confidence: high for the documented stack/register tradeoffs; low for any Turing bytecode or performance conclusion until semantic, debug, memory, and workload evidence exists

## Question

Should the first JavaScript interpreter use register, stack, or hybrid bytecode, and what format can support semantics, debugging, exceptions, GC, baseline compilation, versioning, and resource limits without excessive size or dispatch cost?

## Why This Matters

Bytecode is an internal execution contract that touches nearly every runtime subsystem. Its operand model affects code size, dispatch, temporary values, stack maps, exception edges, deoptimization, debugger locations, serialization, cache invalidation, and future compiler lowering. Choosing a format from a microbenchmark can create a long-lived ABI before semantics and tooling are stable.

This packet defines a deferred research route for `RQ-07`. It does not select register or stack bytecode, a bytecode ABI, a JIT, a compiler backend, or a cache format.

## Source-backed observations

### V8 documents a register-oriented interpreter tradeoff

V8 describes Ignition as a register-based interpreter with an accumulator and explicit virtual-register operands. Its public documentation connects concise bytecode to reduced memory overhead and describes later compiler tiers consuming the bytecode. V8 also documents that bytecode compilation and metadata ownership affect whether work can move off the main thread. These are observations of V8's design and measurements, not evidence that Turing should reproduce its format.

Sources: [V8 Ignition overview](https://v8.dev/blog/ignition-interpreter), [V8 Ignition documentation](https://v8.dev/docs/ignition), and [V8 background compilation](https://v8.dev/blog/background-compilation), retrieved 2026-07-19.

### WebAssembly specifies a stack-machine abstract semantics

The WebAssembly 3.0 specification defines execution using an abstract machine with an implicit stack containing values, labels, and frames. WebAssembly is a separate language and execution environment, so its stack semantics are not a JavaScript bytecode prescription. It is useful as a formal stack-machine reference and as a warning to keep embedding authority and language semantics separate.

Sources: [WebAssembly 3.0 specification](https://webassembly.github.io/spec/core/), [WebAssembly execution conventions](https://webassembly.github.io/spec/core/exec/conventions.html), released 2026-07-10 and retrieved 2026-07-19.

### Operand representation does not settle the whole runtime

A stack or register choice leaves independent questions about constant pools, environment records, closures, object property access, inline caches, call frames, exception tables, source locations, GC maps, async suspension, generators, debugger stepping, and deoptimization. A bytecode format is successful only if those contracts remain explicit and testable.

## Candidate formats

The experiment should compare at least:

1. Stack bytecode with implicit operand stack and explicit local/constant operations.
2. Register bytecode with virtual registers, accumulator conventions, and compact register encoding.
3. Hybrid bytecode with stack-shaped source lowering and registerized hot/basic-block forms.
4. A semantic reference instruction set that prioritizes clarity and is not optimized for dispatch.

Each candidate must define instruction encoding, operand widths, constants, jumps, calls, returns, exceptions, generators/async state, closures, debug locations, source maps, stack/register maps, GC safepoints, cancellation, and version compatibility.

## Evidence required before a bytecode decision

The owner-approved package should provide:

- representative kernels for arithmetic, objects, arrays, property access, calls, closures, classes, exceptions, generators, async, promises, modules, proxies, typed arrays, and host/DOM boundaries;
- a semantics oracle against ECMAScript conformance tests and targeted negative tests;
- bytecode size, decode, dispatch, branch, register/stack movement, and constant-pool accounting;
- precise source locations and debugger behavior at branches, exceptions, async suspension, and deoptimization;
- GC root maps and safe-point behavior for every instruction that can allocate, call, suspend, or invoke host code;
- baseline compiler lowering and a future optimizing-compiler interface without committing to a JIT;
- malformed bytecode, invalid version, oversized operand, recursion, timeout, cancellation, and resource-limit tests;
- deterministic serialization, cache invalidation, endianness/target policy, and source-revision identity;
- memory and code-size measurements under cold, warm, background, and pressure workloads;
- independent review of interpreter safety, generated code, debugging, provenance, and maintenance cost.

## Measurement plan

Measure under equivalent semantics, workload, toolchain, and security policy:

- source-to-first-execution latency and parse/compile time;
- bytecode bytes, metadata bytes, decoded instruction cache, constant pools, frame size, and stack/register spill cost;
- dispatch rate, branch behavior, instruction decode, call/return overhead, and event-loop impact;
- exception, async, generator, debugger, and deoptimization overhead;
- GC root-map size, safepoint cost, allocation rate, and collector interaction;
- startup, short scripts, interactive tasks, long-running loops, object-heavy apps, DOM workloads, and adversarial inputs;
- memory, CPU, wakeups, energy, crashes, timeouts, unsupported cases, and cleanup denominators.

Do not report a bytecode microbenchmark as browser performance. The relevant result includes source parsing, compilation, runtime calls, GC, DOM/host interaction, user input, and recovery.

## Rejection rules

Reject the packet as decision evidence when it:

- treats V8 or WebAssembly bytecode as a drop-in JavaScript standard;
- measures only arithmetic kernels or dispatch loops;
- omits exceptions, async, generators, closures, proxies, debugger locations, GC maps, or host calls;
- relies on undocumented bytecode layout as a stable ABI;
- reports compact encoding without decode, cache, branch, metadata, and debug costs;
- permits malformed or stale bytecode to bypass source, origin, process, or capability identity;
- uses a self-generated interpreter and oracle as independent evidence;
- hides compilation, validation, deoptimization, GC, or failure work in background tasks.

## Current status and next proof

`RQ-07` remains deferred outside the active pre-build crosswalk. The next proof is an owner-approved semantic instruction inventory and bytecode format comparison, followed by a reference interpreter, conformance corpus, debug/exception/GC-map fixtures, and independent format review. No bytecode format, interpreter, compiler, JIT, memory result, performance result, or readiness claim follows from this packet.

## Claim boundary

This is source-backed research preparation only. It does not select stack or register bytecode, an interpreter ABI, a compiler backend, a debugger format, a code cache, a JIT, a GC-map representation, a performance target, or a production runtime claim.
