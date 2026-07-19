# Memory Object Representation and Tab Lifecycle Research - July 2026

Status: source-backed deferred research and experiment handoff; no representation, allocator, process, freeze, discard, or performance decision accepted
Owner: engine, performance, memory, security, quality, accessibility, and product owners
Research date: 2026-07-19
Related questions: `RQ-01`, `RQ-03`, `RQ-35`
Related requirements: `REQ-PERF-002`, `REQ-PERF-003`

## Question

What evidence is needed to determine whether compact Rust representations and explicit tab lifecycle reclamation can reduce sustained memory and preserve responsiveness without weakening safety, site isolation, accessibility, recovery, or user control?

This packet narrows the deferred research questions into one experiment route. It does not choose an object representation, allocator, process topology, freeze policy, discard policy, or implementation language boundary.

## Source observations

The following primary sources were checked on 2026-07-19:

| Source | Observation | Turing consequence |
| --- | --- | --- |
| [Rust Reference: Type layout](https://doc.rust-lang.org/stable/reference/type-layout.html) | Rust type layout includes size, alignment, field offsets, and enum discriminants, but the default `repr(Rust)` makes only limited layout guarantees; layout may change between compilations. | Representation experiments must measure the exact compiler, target, profile, and commit. Stable cross-boundary layouts require an explicit reviewed representation; internal byte savings cannot be assumed from field order or type spelling. |
| [Rust `alloc::alloc`](https://doc.rust-lang.org/stable/alloc/alloc/) and [`Layout`](https://doc.rust-lang.org/stable/alloc/alloc/struct.Layout.html) | Allocation APIs describe blocks through checked size/alignment layouts, and invalid or overflowing layouts are rejected. | Every compact container, arena, slab, handle table, and decoder must validate sizes and alignment before allocation. Allocation failure, overflow, and cleanup are first-class experiment outcomes. |
| [Chromium tab discarding and reloading](https://chromium.googlesource.com/playground/chromium-org-site/%2B/refs/heads/main/chromium-os/chromiumos-design-docs/tab-discarding-and-reloading.md) | Discarding is a memory-pressure response that releases a tab's memory and requires a reload when the tab is revisited; selection and user-visible reload behavior are part of the lifecycle. | A memory result that hides discard, reload cost, state loss, or user-visible recovery is not comparable. Turing must measure freeze, serialization, discard, revival, and refusal cases separately. |
| [Chromium tab lifecycle source](https://chromium.googlesource.com/chromium/src/%2B/720dadbc215c229ce100bc408edb3aee03b0697e/chrome/browser/resource_coordinator/tab_lifecycle_unit.h) | The lifecycle model distinguishes freezing and discard-related transitions, including requests that freeze before discard. | Lifecycle states, transition reasons, and identity-preserving recovery must be recorded as explicit events rather than inferred from a memory graph. |

These observations are architectural inputs only. They are not measurements of Turing, proof that Chromium's policy is correct for Turing, or permission to copy implementation source.

## Decision boundary

The project should not select compact handles, arenas, intrusive indexes, reference counting, a custom allocator, or a freeze/discard policy from a size-of calculation or a single benchmark. The decision must compare semantic correctness, memory categories, latency tails, allocator behavior, cache locality, recovery quality, security equivalence, accessibility behavior, and implementation complexity on the same corpus and host controls.

The default Rust representation is especially unsuitable as an assumed wire or file format. `repr(C)` or another explicit representation may be appropriate at a reviewed boundary, but it does not by itself solve ownership, validation, versioning, or hostile-input concerns. Packed layouts require separate safety review because unaligned access can invalidate ordinary reference-based code.

## Experiment matrix

### Representation families

Compare at least these families for DOM-like nodes, style data, layout fragments, display-list items, protocol messages, and lifecycle records:

1. Baseline owned Rust structs and enums with ordinary collections.
2. Compact index/handle tables with contiguous arrays and generation checks.
3. Arena or slab allocation with explicit ownership and reclamation epochs.
4. Struct-of-arrays or field-split layouts for hot traversal fields and cold metadata.
5. Reference-counted or shared representations only where ownership and cycle behavior are explicit.
6. Serialized/frozen representations used for lifecycle recovery, measured separately from live mutable state.

Every family needs a replacement and rollback story. A family that wins bytes but creates unbounded retention, opaque authority, difficult diagnostics, or unsafe aliasing is not accepted.

### Workloads

Use a pinned, legal, reproducible corpus with:

- small and large DOM/style/layout trees;
- deep nesting, wide sibling sets, mutation-heavy pages, and repeated style invalidation;
- international text, accessibility metadata, images/fonts, and page-surface records;
- mixed 5/15/30/100-tab scenarios with same-site and cross-site cases;
- active, background, frozen, serialized, discarded, restored, crash-recovered, and refusal-to-discard states;
- extensions, DevTools, uploads, calls/audio, unsaved work, and agent tasks where lifecycle protection must prevent unsafe reclamation.

The corpus identity, generated fixture inputs, browser/profile state, process/site-isolation state, and artifact hashes must be retained. Synthetic workloads are diagnostic and cannot stand in for the complete product workload.

### Measures

Record, per object class and lifecycle state:

- logical live bytes, allocation bytes, reserved/committed/resident/private/shared/compressed/swapped bytes, and GPU bytes where applicable;
- object count, padding, pointer/metadata overhead, capacity slack, allocation count/size distribution, page faults, cache misses where available, and reclamation volume;
- construction, mutation, traversal, destruction, serialization, deserialization, freeze, revival, and input-to-present latency with p50/p95/p99 where relevant;
- CPU time, queue wait, wakeups, energy/thermal state, process count, IPC copies, and cross-process shared-resource attribution;
- state preservation, accessibility tree continuity, focus/IME continuity, origin/profile identity, permissions, credentials, uploads, media, DevTools, and agent-task outcomes;
- every timeout, allocation failure, malformed input, stale handle, crash, renderer hang, GPU loss, low-memory event, cancellation, retry, unsupported case, and cleanup result.

No aggregate may silently remove failed samples, hidden tabs, discarded tabs, security mitigations, accessibility work, or recovery cost.

## Safety and authority constraints

- Do not use `unsafe` for a representation experiment without a reviewed safety explanation and focused tests.
- Validate counts, sizes, alignment, offsets, generations, recursion, and serialized lengths before allocation or indexing.
- Keep handles bound to document, frame, origin/site, process epoch, profile, and lifecycle generation; stale handles must fail closed.
- Do not let a memory-pressure controller discard unsaved work, active calls/uploads, credentials, security prompts, DevTools state, accessibility focus, or agent tasks without the specified user-protection decision.
- Preserve site isolation and capability boundaries while comparing process and shared-memory strategies.
- Keep measurement instrumentation from granting authority, changing scheduling semantics, or using real profiles, credentials, or private browsing data.
- Make memory pressure, freeze, serialization, discard, revival, and refusal visible to the user and diagnosable to the system.

## Required artifacts

Before this lane can influence an accepted architecture or performance budget, retain:

1. A versioned experiment manifest naming source commit, Rust toolchain, target, profile, corpus, workload, hardware, OS, process model, isolation state, tab lifecycle state, and instrumentation.
2. A representation schema describing ownership, identity, mutability, cold/hot fields, alignment assumptions, reclamation, serialization, and failure behavior.
3. A raw per-sample result package with allocation and resource attribution, lifecycle events, traces, failed/unsupported denominator, and SHA-256 manifest.
4. Safety and malformed-input tests for each representation and serialized form.
5. Recovery fixtures proving state, origin/profile identity, accessibility, focus, IME, and user-protection behavior across freeze, revival, discard, crash, and cancellation.
6. A statistical analysis record reporting uncertainty, effect sizes, tail regressions, and whether the comparison is paired and equivalent.
7. An owner-reviewed decision record selecting, rejecting, or deferring each family and updating the relevant ADR, requirement, risk, work package, interface freeze, and benchmark route together.

## Rejection rules

Reject the result as an architecture or performance decision when it:

- relies on undocumented default Rust layout or a warm allocator without recording it;
- reports one memory number without distinguishing logical, allocated, resident, shared, compressed, swapped, GPU, and charged ownership;
- compares active tabs with silently discarded, frozen, or missing tabs;
- removes security, accessibility, DevTools, extensions, agent, recovery, or user-protection work from the workload;
- treats a compact representation as safe because it is smaller, or a serialized form as durable because it round-trips once;
- omits failed, timed-out, unsupported, malformed, low-memory, cancellation, or cleanup paths;
- uses real profiles, credentials, accounts, secrets, or unredacted user content;
- claims Chrome-class, faster, lower-memory, lower-energy, compatible, secure, accessible, or production behavior from this research packet.

## Current status and next proof

`RQ-01`, `RQ-03`, and `RQ-35` remain deferred research questions. `REQ-PERF-002` and `REQ-PERF-003` remain accepted requirements whose implementation, tests, reviews, and evidence are not populated by this packet. `PB-013` remains partial and `TASK-000005` remains proposed-only. The next controlled proof is a reviewed experiment manifest and synthetic fixture package after source-strategy, toolchain/fresh-host, IPC, sandbox, and benchmark task-authority prerequisites are resolved.

This packet improves the research handoff and measurement contract only. It does not select a representation, allocator, lifecycle policy, process model, toolkit, engine source, or browser implementation; it does not change the 90% contained-M0 documentation organization or 0% full-build closure measures.

## Canonical related records

- [Research-question coverage audit](research-question-coverage-audit-2026-07.md)
- [Performance engineering book](../performance/README.md)
- [Memory, allocation, and cache policy](../performance/02-memory-allocation-and-cache-policy.md)
- [Allocators, virtual memory, and page reclamation](../performance/07-allocators-virtual-memory-and-page-reclamation.md)
- [Benchmark evidence and claim closure preparation](benchmark-evidence-and-claim-closure-preparation-2026-07.md)
- [Semantic resource attribution taxonomy](semantic-resource-attribution-taxonomy-2026-07.md)
- [Build-readiness progress snapshot](../project-buildout/22-build-readiness-progress-snapshot.md)
