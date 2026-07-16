# Engine Memory, Data Structures, and Observability

Status: research baseline; byte budgets require prototypes  
Owner: engine performance and diagnostics  
Purpose: Make memory layout, ownership, cache cost, and diagnostic truth explicit before compatibility breadth creates irreversible object graphs.

## Relationship to the Turing program

The global measurement contract is in [Blueprint 09](../blueprint-v1/09-performance-memory.md) and the [performance book](../performance/README.md).

## Representation principles

Hot structures should use compact IDs, packed flags, arenas, small-vector/common-case storage, immutable blocks, and side tables for rare state. Turing should avoid pervasive reference-counted pointer graphs and global registries.

Every proposed representation reports object size, alignment, pointer/metadata overhead, allocation count, traversal locality, mutation cost, destruction cost, serialization needs, unsafe surface, and debugger visibility across representative corpora.

## Ownership and lifetimes

Document-lifetime data, style-set data, layout-epoch data, paint-epoch data, process caches, profile caches, and shared immutable resources have distinct allocators and release paths. Bulk destruction is preferred where lifetime boundaries are real.

Cross-subsystem references use typed handles. A component can retain another component’s data only through a documented ownership contract and accounting relationship. DevTools and agent observation must not accidentally pin entire documents.

## Cache architecture

Each cache declares key semantics, value cost, owner, admission policy, eviction policy, pressure response, sharing boundary, invalidation, and observability. Caches include atoms, selectors, computed-style blocks, shaped text, glyphs, decoded images, bytecode, compiled code, raster tiles, and protocol metadata.

Cache hits that cross profile, private-session, site, origin, security mode, or font/privacy boundaries are prohibited unless an explicit equivalence proof exists.

## Memory accounting

Allocations are charged or sampled to semantic owners. Reports distinguish live bytes, allocator-reserved bytes, committed virtual memory, resident pages, shared physical pages, compressed memory, swap, mapped files, GPU resources, external JS memory, and disk caches.

Physical and charged totals are both shown; shared pages are not double-counted as physical memory. Uncertainty and platform measurement limits are included in every report.

## Observability schema

Logical trace events have stable names and typed fields for parser, DOM mutation, style invalidation, layout, paint, raster, compositor, input, accessibility, JS/GC, network, storage, lifecycle, process, and agent activity.

Events carry monotonic time, process/thread, target identity, document epoch, task/causal relationship, duration or instant class, semantic owner, and redaction category. Stable builds can sample or omit expensive payloads without changing the schema’s meaning.

## Leak and retention analysis

The resource manager and DevTools connect process totals to native categories, JS heaps, DOM retainers, detached documents, caches, GPU resources, workers, extensions, and agents. Repeated navigation, open/close, BFCache, freeze/discard, DevTools attach, and agent sessions have leak loops.

A leak waiver identifies bytes per cycle, affected owner, severity, platform, expiry, and follow-up issue.

## Non-negotiable invariants

- No representation is accepted as memory-efficient without corpus and lifecycle measurements.
- Every long-lived allocation has a semantic owner and release path.
- Observability must not retain secrets or materially change the workload being measured.
- Cross-profile and cross-origin sharing requires both security equivalence and measured benefit.
- Memory pressure can drop caches and speculative state but cannot weaken isolation or lose protected user work.

## Required evidence

- Object-layout reports and heap profiles for all hot structures.
- Thirty-tab mixed and all-live memory attribution with process and lifecycle disclosure.
- Repeated lifecycle leak tests and allocation-failure injection.
- Cache effectiveness versus resident-memory and energy studies.
- Trace overhead measurements and cross-tool reconciliation with OS/process counters.

## Known risks and unresolved questions

- Instrumentation can perturb allocation and scheduling enough to mislead results.
- Compact encodings may increase CPU cost or unsafe code.
- Shared immutable resources can create covert channels or accounting disputes.
- Allocator reserve and OS compression make one-number memory claims unreliable.

## Primary sources

- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- Chromium LayoutNG — https://developer.chrome.com/docs/chromium/layoutng
- Servo project — https://servo.org/about/
- Miri — https://github.com/rust-lang/miri
- Speedometer — https://browserbench.org/Speedometer3.1/
- Web Platform Tests — https://web-platform-tests.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
