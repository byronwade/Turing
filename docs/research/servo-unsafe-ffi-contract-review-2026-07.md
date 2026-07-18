# Servo Unsafe and FFI Contract Review - July 2026

Status: dated external review for `ADR9-EV-009` and `ADR9-EV-010`; no unsafe, FFI, component, source, dependency, or release-code approval
Owner: security, engine, embedding, architecture, release operations, and documentation-research owners
Review date: 2026-07-18
Confidence: medium for source-shape counts and C API surface inventory; low for safety conclusions until the selected `ADR-0009` option has block-level unsafe review, C conformance tests, sanitizer/fuzz evidence, and owner review

## Question

What unsafe-code and FFI contract evidence is needed before any Servo-derived component boundary can be proposed for Turing release-path use?

This review is the first dedicated continuation output for [`ADR9-EV-009`](../project-buildout/15-adr-0009-evidence-traceability-matrix.md) and [`ADR9-EV-010`](../project-buildout/15-adr-0009-evidence-traceability-matrix.md). It does not approve Servo, approve unsafe code, approve the C API, approve SpiderMonkey or WebGL integration, or move `PB-002` out of blocked status.

## Inputs

External checkout:

- workspace: `C:\ts\servo`;
- remote: `https://github.com/servo/servo.git`;
- commit: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- commit date: 2026-07-17T15:50:14Z;
- commit subject: `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)`;
- local status during this pass: `main...origin/main [behind 2]` with no tracked-file modifications reported by `git status --short --branch`.

This report inspected the external checkout in place. No Servo source file, generated output, C header, native artifact, build output, or Cargo metadata file was copied into this repository.

## Method

The pass used source-shape queries to separate:

- unsafe blocks;
- unsafe functions and impls;
- `SAFETY:` explanations;
- C/Rust/system ABI markers;
- cbindgen-facing C API functions;
- null-pointer checks, string conversions, ownership transfer, and panic edges;
- JavaScript tracing/rooting boundaries;
- WebGL thread and GL context boundaries.

Representative commands:

```powershell
git -C C:\ts\servo status --short --branch
git -C C:\ts\servo log -1 --format="%H|%cI|%s"
rg -n '\bunsafe\b' C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n 'unsafe\s*\{' C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n 'unsafe\s+fn\b|unsafe\s+impl\b' C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n 'extern\s+"(C|system|Rust)"|#\[no_mangle\]|#\[export_name|#\[link\(' C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n 'pub\s+(unsafe\s+)?extern\s+"C"\s+fn\s+' C:\ts\servo\ffi\capi --glob '*.rs'
```

Counts are useful only as triage. They do not prove whether an unsafe block is correct, reachable, covered by tests, or acceptable under Turing policy.

## Source-Shape Summary

| Pattern | Matches | Files | Decision implication |
|---|---:|---:|---|
| `unsafe` mentions | 2280 | 241 | Review scope is too large for an unbounded adoption decision. |
| unsafe blocks | 1629 | 207 | Any selected component boundary needs a block-level inventory. |
| unsafe functions or impls | 328 | 80 | Trait, threading, GC, rooting, and FFI invariants must be explicit. |
| `SAFETY:` comments | 157 | 51 | Current comment count is far below unsafe-site count and cannot substitute for Turing review. |
| FFI/export/link markers | 217 | 40 | ABI and caller-obligation contracts are decision blockers. |

Top unsafe-block files in this pass:

| File | Unsafe-block matches | Primary review pressure |
|---|---:|---|
| `components/webgl/webgl_thread.rs` | 263 | GL context, driver calls, WebRender coordination, channel and context lifetime. |
| `components/script/script_runtime.rs` | 63 | SpiderMonkey runtime, GC roots, JS context, callbacks, thread markers. |
| `components/script/dom/window/windowproxy.rs` | 51 | JS proxy, cross-compartment/window identity, trace callback behavior. |
| `components/script/dom/console.rs` | 45 | JS-visible console integration and runtime value handling. |
| `components/script/dom/bindings/buffer_source.rs` | 40 | JS buffer view, pointer, length, and Rust slice boundaries. |
| `components/script/script_module.rs` | 31 | Module loading and JS runtime interaction. |
| `components/script/dom/bindings/structuredclone.rs` | 27 | Structured clone buffers and cross-realm data movement. |
| `ffi/capi/options.rs` | 26 | C API configuration handles, C strings, file paths, and option mutation. |
| `components/fonts/platform/macos/font.rs` | 25 | Platform font handles and native text resources. |
| `components/layout/layout_impl.rs` | 25 | Layout internals and pipeline state. |

Top unsafe function or unsafe impl files:

| File | Unsafe fn/impl matches | Primary review pressure |
|---|---:|---|
| `components/script_bindings/trace.rs` | 49 | `JSTraceable` and custom trace graph invariants. |
| `components/script_bindings/root.rs` | 18 | Rooting, unrooting, and stable trace-object identity. |
| `components/script_bindings/conversions.rs` | 15 | JS/Rust conversion rules. |
| `components/script_bindings/reflector.rs` | 14 | DOM reflection and object identity. |
| `components/script/dom/bindings/root.rs` | 10 | DOM root handles and lifetimes. |

Top FFI/export marker files:

| File | Marker matches | Primary review pressure |
|---|---:|---|
| `ports/servoshell/egl/android/mod.rs` | 28 | Platform EGL and Android loader boundary. |
| `components/script/script_runtime.rs` | 21 | JS runtime ABI callbacks. |
| `ffi/capi/options.rs` | 21 | C configuration API. |
| `components/script/dom/window/windowproxy.rs` | 15 | JS engine callback boundary. |
| `ffi/capi/preferences.rs` | 10 | Preference C API and string ownership. |
| `ffi/capi/webview.rs` | 10 | WebView lifecycle, URL strings, screenshot output, and ownership transfer. |

## C API Contract Inventory

The `ffi/capi` tree exposes 52 `pub extern "C"` functions in this pass:

| Function family | Count | Examples | Required Turing contract before reuse |
|---|---:|---|---|
| Builder | 6 | `servo_builder_create`, `servo_builder_build`, `servo_builder_free` | Ownership transfer, reentrancy, thread confinement, event-loop callback lifetime, failure behavior. |
| Options | 21 | `servo_options_set_*`, `servo_options_free` | Valid ranges, path encoding, string lifetime, sensitive option handling, panic-free error contract. |
| Preferences | 10 | `servo_preferences_set_*`, `servo_preferences_get_*` | Type conversion, string allocation/freeing, unknown-key behavior, caller-owned output lifetime. |
| Rendering context | 2 | software context create/free | Surface identity, backend lifetime, failure return shape. |
| Servo handle | 3 | free, spin event loop, logging setup | Thread ownership, shutdown ordering, logging and secret redaction. |
| WebView | 9 | builder, load, paint, screenshot, free | URL parsing, delegate callback lifetime, screenshot buffer ownership, paint/reentrancy, WebView lifetime. |
| Other | 1 | default event-loop callback | Callback semantics and no-op behavior. |

Observed C API contract classes:

- null pointers are commonly rejected with assertions rather than a stable error code;
- several C string conversions panic on invalid UTF-8 through `unwrap` or `expect`;
- ownership transfers use raw `Box::from_raw` and `Box::into_raw`;
- caller-side thread affinity is documented in comments for several handles, but this pass did not find a Turing-owned executable thread-affinity test;
- callbacks and delegate function pointers need lifetime, panic, reentrancy, and cross-thread rules before any embedding decision;
- screenshot, preference string, and path outputs need explicit allocation and free contracts;
- option setters expose security-sensitive switches such as sandbox, certificate behavior, local script source, shader path, config path, random pipeline closure behavior, and debug options that require deny-by-default Turing policy if any API shape is reused.

For Turing, a C API is not acceptable because it compiles. It needs a versioned ABI specification, panic boundary, allocator/freeing rule, thread rule, callback rule, error taxonomy, conformance tests, sanitizer coverage, fuzz input set, and support/deprecation policy.

## JavaScript Rooting and Tracing Review Classes

The highest-pressure unsafe fn/impl files are in `components/script_bindings`. The reviewed query output shows:

- `trace_reflector`, `trace_object`, and related helpers call into SpiderMonkey tracer APIs;
- `CustomTraceable`, `JSTraceable`, `StableTraceObject`, `DomRoot`, and `RootedTraceableBox` encode GC reachability and root-list invariants;
- implementations cover containers, DOM handles, style data, tokenizer/tree-builder shapes, and "no trace" wrappers;
- correctness depends on all live JS-managed values being traced and no untraced pointer outliving the JS runtime or document epoch.

This conflicts directly with Turing's accepted JavaScript-runtime direction unless a future `ADR-0009` option explicitly remains research-only or isolates Servo script/runtime code outside release paths. Any release-path proposal touching script bindings must provide:

- selected component boundary and feature profile;
- generated binding provenance;
- SpiderMonkey reachability decision;
- complete root/tracer invariant list;
- stale document/realm tests;
- GC stress tests;
- Miri/sanitizer/fuzz evidence where applicable;
- owner review from JavaScript, security, and architecture scopes.

## WebGL and Driver Boundary Review Classes

`components/webgl/webgl_thread.rs` remains the largest unsafe-block cluster. The pass shows GL calls, context maps, WebRender swap-chain coordination, routed message receivers, async context deletion, context-busy tracking, WebXR commands, and device/context lookup paths.

A Turing release-path proposal touching this area must prove:

- which process owns GL/WebGPU/WebRender resources;
- how renderer, GPU, and compositor identities cross IPC;
- context lifetime and deletion behavior under renderer crash, GPU loss, resize, and WebRender in-flight usage;
- which driver calls are inside an OS sandbox;
- how hostile page commands are validated before reaching driver APIs;
- timeout, cancellation, queue, and backpressure behavior;
- shader and buffer input validation;
- fault injection and negative tests for stale, duplicate, wrong-context, oversized, and unauthorized commands.

This is not just an unsafe-code review. It is also a process-boundary, GPU-sandbox, IPC, and benchmark-denominator blocker.

## Decision Impact

This report improves `ADR9-EV-009` and `ADR9-EV-010` from a generic "unsafe/FFI inventory needed" gap into a concrete review plan:

1. Pick the exact `ADR-0009` candidate boundary first.
2. Generate a block-level unsafe ledger only for that selected boundary, including file, function, unsafe operation class, caller preconditions, owner, release relevance, test/fuzz/sanitizer/Miri evidence, and residual risk.
3. Generate a C ABI ledger for `ffi/capi` only if an embedding or shell option actually includes it.
4. Reject or isolate Servo script/runtime and WebGL code unless SpiderMonkey, rooting/tracing, generated bindings, GL context lifetime, and GPU-sandbox evidence can meet Turing's independent-engine policies.
5. Treat `SAFETY:` comments in upstream code as input evidence, not as Turing approval.

## Missing Before Owner Review

`ADR9-EV-009` still needs:

- selected candidate component boundary;
- block-level unsafe ledger for that boundary;
- `SAFETY:` coverage map;
- invariant and precondition classification;
- release relevance classification;
- owner assignment;
- test, fuzz, sanitizer, Miri, or equivalent evidence;
- stale-epoch, crash, cancellation, and resource-exhaustion evidence where the unsafe operation crosses browser boundaries.

`ADR9-EV-010` still needs:

- versioned ABI specification;
- cbindgen/header provenance and generated-output policy;
- allocator/freeing rules;
- panic and unwind policy;
- pointer, string, buffer, callback, and thread-affinity rules;
- C conformance tests;
- sanitizer/fuzz coverage for invalid pointers, invalid UTF-8, double-free, use-after-free, wrong-thread, reentrant callback, null, truncated, oversized, and wrong-lifetime inputs;
- support and deprecation policy.

## What This Does Not Prove

This report does not prove:

- Servo unsafe code is correct or incorrect;
- Servo's C API is stable, safe, or suitable for Turing;
- SpiderMonkey integration can coexist with Turing's JavaScript-runtime direction;
- WebGL or GPU driver calls are sandbox-safe;
- any component can be isolated from generated bindings, native packages, or platform APIs;
- Servo is compatible, secure, accessible, faster, lower memory, Chrome-class, production-ready, or supportable;
- `ADR-0009`, `PB-002`, `ADR9-EV-009`, or `ADR9-EV-010` is ready for owner approval.

## Affected Records

This review updates evidence for:

- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [ADR-0009 Source Strategy Inventory](servo-source-strategy-inventory-2026-07.md);
- [Blueprint Research Program](../blueprint-v1/22-research-program.md);
- [Research Index](README.md);
- [Research Log](../research-log.md);
- [Repository Map](../repository-map.md);
- [Pre-build Readiness Gap Audit](pre-build-readiness-gap-audit-2026-07.md).

`PB-002` remains blocked and `ADR-0009` remains unresolved.
