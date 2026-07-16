# WebAssembly, Web IDL, Modules, and the Event Loop

Status: research and design baseline  
Owner: web runtime embedding  
Purpose: Connect language execution to the web platform without bypassing origin, lifecycle, scheduling, or security policy.

## Relationship to the Turing program

This document expands the runtime embedding portion of [Blueprint 06](../blueprint-v1/06-javascript-runtime.md) and is constrained by [network, storage, media, and platform services](../blueprint-v1/07-network-storage-media.md).

## Web IDL generation

Reviewed interface definitions generate argument conversion, overload resolution, dictionaries, unions, callbacks, promises, exceptions, brand checks, exposure sets, secure-context requirements, permissions, user activation, and lifecycle checks. Generated bindings are deterministic and carry the source definition revision.

Bindings use rooted handles, typed frame/document identities, and explicit completion values. They do not expose Rust references, kernel handles, or unvalidated renderer claims. Fast paths remain semantically equivalent to generated reference paths.

## Realms and agent clusters

Each realm has intrinsics, global object, security origin, policy state, module map, debugger identity, and memory attribution. Agent clusters and realm groups follow web-platform requirements; they are not merged merely for memory savings. Cross-origin wrappers expose only standardized operations.

Navigation, BFCache, freeze, discard, and process swap update document epochs and task eligibility. A callback or promise continuation against a stale document fails or is cancelled according to platform semantics.

## Event loop and scheduling

Task sources, microtask checkpoints, rendering opportunities, timers, parser work, networking, user interaction, animation, workers, and lifecycle transitions follow the HTML event-loop model. Queue records include source, principal, realm, document epoch, enqueue time, deadline, cancellation, and semantic owner.

The scheduler can throttle permitted background activity but cannot reorder observable semantics for benchmark convenience. Microtask starvation, runaway posted messages, worker floods, and recursive timers are bounded and diagnosed.

## Modules and loading

Module loading separates resolution, fetch, parse, link, instantiate, and evaluate. URL resolution, import maps, credentials, referrer policy, MIME, CORS, integrity, module maps, workers, dynamic import, cycles, and top-level await use shared network and security policy.

Module and compiled-code caches are partitioned and versioned. Failed, cancelled, or partially linked graphs do not enter authoritative cache state.

## Structured clone and messaging

Structured clone supports standardized values, transferables, errors, cycles, and backing-store ownership with strict bounds. Transfer, detach, serialization, IPC, deserialization, and publication form one transactional operation. A failure leaves the source and destination in a defined state.

Message ports, workers, and cross-process channels preserve origin/profile/agent-cluster identity and cannot smuggle browser capability handles.

## WebAssembly

WebAssembly begins with a bounded binary decoder and validator, then a reference interpreter. Native compilation is a separate gate with explicit memory/table guards, trap mapping, stack limits, W^X, control-flow protections, and sandbox review. Streaming compilation consumes verified bytes and is cancelled with navigation or response failure.

Threads and shared memory require the correct cross-origin isolation state. SIMD, exceptions, reference types, GC, multiple memories, tail calls, and component-related features are staged by specification maturity, conformance, and threat model.

## Debugger and automation integration

Debugging, stepping, async stacks, source maps, worker targets, module graphs, WebAssembly frames, event-loop queues, and task causality use the same runtime truth exposed through the Turing Engine Protocol. Remote or agent access does not obtain hidden evaluation authority.

## Non-negotiable invariants

- Generated Web IDL bindings enforce exposure, realm, origin, permission, user-activation, and lifecycle rules.
- Task and microtask ordering follows the platform model; optimization does not silently reorder effects.
- Module caches, code caches, and structured-clone transfers are partitioned and transactional.
- WebAssembly bytes are validated before execution and native code follows JIT security policy.
- Workers and messaging preserve principal identity and cannot transfer browser capabilities.

## Required evidence

- Web IDL generation golden tests and WPT binding behavior.
- Event-loop, timers, promises, modules, workers, structured-clone, BFCache, freeze, and navigation tests.
- Module graph fault injection for network failure, cancellation, cycles, and partial cache writes.
- WebAssembly specification tests, decoder/compiler fuzzing, trap and memory boundary tests.
- Cross-origin isolation and shared-memory conformance tests.
- Debugger and protocol tests for async causality and stale target behavior.

## Known risks and unresolved questions

- Binding fast paths can accidentally bypass security or lifecycle checks.
- Task scheduling changes can create subtle compatibility failures.
- Structured clone and transferables cross memory, process, and ownership boundaries.
- WebAssembly native execution duplicates much of the JIT security surface.

## Primary sources

- Web IDL — https://webidl.spec.whatwg.org/
- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- WebAssembly specifications — https://webassembly.github.io/spec/
- Web Platform Tests — https://web-platform-tests.org/
- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
