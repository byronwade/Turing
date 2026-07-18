# Memory, Allocation, and Cache Policy

Status: research and design baseline
Owner: memory architecture
Purpose: Control representation cost, allocator behavior, caches, sharing, pressure, and lifecycle reclamation.

## Relationship to the Turing program

This document expands RQ-01, RQ-03, REQ-PERF-002, and REQ-PERF-003. Engine representations are detailed in [engine memory and observability](../engine/09-memory-data-structures-and-observability.md).

## Semantic ownership

Every major allocation is directly charged or statistically attributed to browser UI/profile, document/frame/site instance, JavaScript heap/code, DOM/style/layout/paint/accessibility, image/font/media/canvas, network, storage, GPU, extension, DevTools, agent/model, or shared service. Unknown remains explicit.

Shared resources report physical size and charged ownership without double counting. Cross-profile sharing requires privacy and policy equivalence.

The current checked taxonomy is [`semantic-owners.v1.json`](../blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json), validated by [`tools/validate_benchmark_resource_attribution.py`](../../tools/validate_benchmark_resource_attribution.py). It is a no-claim owner model only; no browser instrumentation or memory result exists yet.

## Representation budgets

Hot object classes receive byte budgets before feature breadth: DOM node, attribute, name, event listener, computed style, selector program, layout fragment, paint item, hit-test entry, accessibility node, JS value/object/shape, task, IPC envelope, request, cache entry, and protocol event.

Budgets include allocator overhead, side tables, indexes, and retained capacity. Corpus distributions matter more than isolated `size_of` values.

## Allocation strategy

Document and epoch-lifetime data favor arenas and bulk destruction. Common fixed-size objects use slabs or size classes. Rare state moves to side tables. Compact generational IDs replace pointer-rich graphs where measured. Immutable data can be shared only within allowed security/profile boundaries.

Large buffers, media, canvas, WebAssembly, and GPU resources use explicit reservation and commit, not optimistic overcommit without policy.

## Allocator integration

The allocator exposes live, reserved, committed, resident, dirty, reusable, and fragmentation views by subsystem. Per-thread caches and arenas are bounded and trimmed at lifecycle or pressure points. Memory release behavior uses platform mechanisms and is measured rather than inferred from logical frees.

Allocation failure is a normal tested outcome at every untrusted size boundary.

## Cache governance

Every cache declares key, value, owner, security partition, cost metric, budget, eviction, invalidation, persistence, pressure behavior, and observability. Entry admission considers reuse probability, creation cost, size, recency/frequency, foreground relevance, and energy. One site cannot evict all useful browser state without limits.

Caches cannot be required for correctness. Invalid entries are discarded rather than partially trusted.

## Tab lifecycle and reclamation

Active, background, throttled, frozen, serialized, discarded, and crashed states have explicit retained-resource contracts. Freezing can stop work and release caches, allocator pages, decoded data, layout/paint state, workers, and GPU resources only where semantics permit. Serialization retains only deliberately designed state; discard reloads.

Protected activity and user keep-active choices remain visible. Reclamation cannot change site isolation or silently lose unsaved work.

## Pressure controller

The controller combines OS signals, commit/resident/swap, GPU budgets, per-owner growth, foreground deadlines, process health, and user protection. It escalates through cache trim, GC, allocator trim, background throttling, freeze, safe serialization, and discard. Hysteresis prevents oscillation.

Every action and reclaimed amount is traced by owner; failure to reclaim informs later policy.

## Non-negotiable invariants

- Every major byte has a semantic owner or explicit unknown category.
- Shared and charged memory are distinguished from physical totals.
- Caches are bounded, partitioned, observable, and non-authoritative.
- Logical freeing and physical reclamation are measured separately.
- Pressure policy never weakens isolation or silently loses protected work.
- Allocation failure and oversized hostile input fail safely.

## Required evidence

- Object-size distributions and total memory on generated and application corpora.
- Allocator live/reserved/resident/fragmentation reconciliation by platform.
- Cache hit, cost, admission, eviction, pollution, and pressure experiments.
- Freeze/serialize/discard reclamation and revival studies.
- OOM, low-memory, swap, compressed-memory, and GPU-pressure tests.
- Thirty-tab mixed and all-live manifests with per-owner accounting.

## Known risks and unresolved questions

- Fine-grained accounting can add meaningful overhead.
- Arena lifetime mistakes can retain large documents.
- Sharing can cross privacy or profile boundaries.
- Aggressive trimming can cause latency, energy, and network regressions.

## Primary sources

- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- Servo project — https://servo.org/about/
- The Rustonomicon — https://doc.rust-lang.org/nomicon/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
