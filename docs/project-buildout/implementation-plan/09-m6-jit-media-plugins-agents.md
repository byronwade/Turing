# 09 — M6: JIT, Media, Plug-ins, and Agent Preview

Status: implementation game plan; every capability remains separately gated
Owner: JavaScript, media, Plug-ins, AI, security, product, performance, and quality

## 1. Objective

M6 adds performance and ecosystem capabilities that significantly increase attack surface: baseline JIT, WebAssembly, media/document pipelines, restricted Plug-ins, and a capability-scoped agent preview. Each track can be delayed independently. None is required merely to make a more impressive demo.

## 2. Baseline JIT

Entry requires a mature interpreter, exact GC reference mode, differential harness, executable-memory policy, and sandbox evidence.

Task sequence:

1. versioned Turing IR and verifier;
2. baseline compiler or reviewed backend adapter;
3. W^X allocation, code signing/entitlements where required, and no writable-executable overlap;
4. stack maps and exact GC integration;
5. inline caches with invalidation and fallback;
6. deoptimization to interpreter/reference state;
7. exceptions, traps, debugging, profiling, and cancellation;
8. interpreter/JIT differential testing for every supported operation;
9. codegen fuzzing and malformed-IR rejection;
10. no-JIT mode and emergency disable switch;
11. performance and energy evidence showing end-to-end value.

An optimizing tier remains later and cannot become the only semantic implementation.

## 3. WebAssembly

- validate modules with explicit limits;
- implement reference interpreter or reviewed compiler boundary;
- use the same W^X, stack-map, trap, memory, and process controls as JIT work;
- bound tables, memories, compilation, code size, recursion, and host calls;
- expose only standards-defined web imports through normal origin and permission policy;
- differentially test tiers and retain a no-JIT/reference path;
- fuzz decoder, validator, interpreter, compiler IR, and host bindings.

## 4. Media, PDF, and printing

Implement through specialized sandboxed processes:

- image/font/media/PDF parser and decoder brokers;
- audio/video clocks, buffering, seeking, tracks, captions, and device routing;
- WebRTC capture and transport only after permission, indicator, broker, privacy, and network review;
- codec matrix with patent/license/distribution status;
- hardware acceleration with fallback and device-loss handling;
- PDF viewing, search, forms, printing, pagination, preview, and platform spoolers;
- DRM/CDM only when licensing and process isolation are available, otherwise explicitly unsupported;
- malformed-input fuzzing, corpus provenance, energy budgets, and crash recovery.

## 5. Turing Plug-in preview

Entry requires ADR-0011 and versioned capability contracts.

Initial scope:

- signed first-party Plug-ins using the same brokered platform intended for third parties;
- WebAssembly Component Model/WIT prototype with explicit imports, memory/fuel/deadline limits, cancellation, and isolated storage;
- restricted WebExtensions adapter for a documented subset;
- per-profile and per-Space installation and grants;
- session-only host grants and private-session rules;
- package provenance, update, rollback, revocation, and diagnostics;
- CPU, memory, network, storage, wakeup, and concurrency attribution;
- accessible UI contribution points that cannot spoof trusted chrome;
- developer tools, conformance tests, and failure simulation.

Arbitrary third-party native code remains prohibited by default.

## 6. Agent preview

Entry requires WP-002 identities/capabilities, WP-007 semantic document model, WP-015 protocol/trace foundation, and accepted agent authority contracts.

Deliver read-only assistance first:

- selected-source semantic observations;
- origin/frame/document labels;
- redaction and secret handles;
- visible provider selection and local/remote data-flow disclosure;
- scoped memory and retention;
- local audit, stop, revoke, and export;
- one local and one remote provider adapter behind the same policy boundary;
- prompt-injection, context-manipulation, stale-target, secret-request, and resource-exhaustion evaluation.

Low-risk actions enter only after:

- typed action schema;
- explicit grants and budgets;
- isolated task profile;
- deterministic preconditions and postconditions;
- browser-owned confirmation where configured;
- idempotency and rollback behavior;
- adversarial evaluation showing the browser, not the model, controls authority.

Consequential actions remain gated beyond an early preview.

## 7. Thirty-tab lifecycle integration

M6 integrates real engine, JS, media, Plug-in, and agent resource owners with WP-005:

- all-live and mixed-state scenarios;
- protected audio/call/upload/edit/DevTools/agent states;
- freeze, serialize, discard, and restore quality;
- process consolidation only for security-equivalent work;
- local model memory and token cost;
- Plug-in wakeups and background work;
- energy, thermal, and recovery behavior;
- user-visible reasons and overrides.

## 8. Exit criteria

- baseline JIT passes semantic equivalence, W^X, deoptimization, fuzzing, and no-JIT gates;
- media/parser processes are effectively sandboxed and fuzzed;
- codec, DRM, PDF, and printing support statements are exact;
- Plug-in permissions, revocation, update, and resource attribution work for the supported subset;
- agent observations and actions cannot expand grants or bypass confirmation;
- prompt-injection evaluation and incident-stop controls are operational;
- 30-tab reports disclose lifecycle and isolation state;
- no beta or stable claim is implied by feature breadth.
