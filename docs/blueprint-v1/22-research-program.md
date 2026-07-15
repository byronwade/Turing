# 22 — Research and Measurement Program

Turing’s high-risk architectural choices must be tested against alternatives before they become irreversible. This document defines the initial research questions and required evidence.

## RQ-01 — Can compact Rust data structures materially reduce engine memory?

Compare DOM, style, fragment, display-list, and protocol representations using generated and captured legal corpora. Measure live bytes, reserved bytes, pointer/metadata overhead, allocation count, construction, mutation, traversal, destruction, and cache behavior. Compare arena handles, intrusive indexes, reference counting, and alternative compact layouts. Include safety and implementation complexity.

Decision output: accepted representations and size/performance budgets by object class.

## RQ-02 — What process topology gives the best isolation-adjusted memory?

Simulate and later measure per-site, per-browsing-context-group, and security-equivalent process pools. Vary 8/16/32 GiB systems, 5/15/30/100 tabs, iframe composition, workers, media, extensions, and agent hosts. Report security equivalence, process overhead, shared resources, crash blast radius, IPC latency, and revival.

Decision output: process assignment and pressure policy; never a cross-site coalescing shortcut.

## RQ-03 — How much memory can freezing reclaim without discard?

Instrument allocator pages, JS heap, DOM/style/layout/display list, images/fonts, network buffers, workers, and GPU resources before and after throttling/freeze. Test working-set trimming and safe cache dropping. Measure revival latency and semantic effects.

Decision output: frozen-state budget and eligible resource-release contract.

## RQ-04 — Which UI stack meets latency, accessibility, and platform goals?

Prototype retained Rust scene graph with native adapters, selective native controls, and at least one alternative. Measure startup, key-to-paint, frame pacing, memory, text/IME, drag/drop, menus, screen readers, high contrast, and platform fidelity. Avoid evaluating only visual mockups.

Decision output: UI renderer and native-control policy.

## RQ-05 — Direct graphics APIs or a Rust GPU abstraction?

Prototype a basic compositor on Metal, D3D12, and Vulkan through direct adapters and a pinned abstraction such as wgpu. Measure binary/build complexity, startup, memory, command validation, device loss, driver coverage, debugging, performance, and ability to constrain the GPU process.

Decision output: backend abstraction boundary with replacement and security strategy.

## RQ-06 — Which text stack balances consistency and native behavior?

Compare platform-native shaping/rasterization, HarfBuzz/FreeType, and hybrid adapters across scripts, variable/color fonts, bidi, vertical text, IME, selection geometry, accessibility, screenshots, memory, and startup.

Decision output: shaping/raster/fallback architecture per platform.

## RQ-07 — Register or stack bytecode for the interpreter?

Implement representative language kernels in both forms. Compare code size, dispatch, compile time, exception handling, debug mapping, stack maps, baseline JIT lowering, memory, and Test262 diagnostics. Do not use microbenchmarks alone.

Decision output: bytecode format v1 and versioning policy.

## RQ-08 — GC heap representation and DOM wrapper strategy

Prototype tracing roots, handles, wrapper maps, nursery/mature spaces, external memory, weak maps, finalization, and document teardown. Stress cycles between JS and DOM. Compare movable versus nonmoving mature spaces and handle-indirection costs.

Decision output: exact baseline collector and wrapper-lifetime contract.

## RQ-09 — Cranelift versus custom baseline code generation

After the interpreter is stable, compare backend integration, compilation latency, code quality, stack maps, deoptimization metadata, W^X support, platform signing, binary size, debugging, fuzzability, and maintenance.

Decision output: baseline JIT backend; optimizing-tier decision remains separate.

## RQ-10 — Semantic agent snapshots versus screenshot-first control

Evaluate task success, token size, latency, accessibility, stale-target rate, cross-origin leakage, hidden-content exposure, and prompt-injection resistance. Screenshots remain an optional labeled observation, not the assumed default.

Decision output: semantic snapshot schema and when vision is permitted.

## RQ-11 — Deterministic policy usability

Test grant/confirmation designs with low-, medium-, and high-impact tasks. Measure comprehension, approval mistakes, habituation, interruptions, cancellation, and audit usefulness. Include keyboard and screen-reader users.

Decision output: risk classifier, confirmation batching limits, and trusted UI.

## RQ-12 — Local model resource envelope

Measure model load time, resident/working memory, KV cache, accelerator allocation, energy, thermal effects, quality, token throughput, unload latency, and interaction with 30-tab workloads across hardware tiers.

Decision output: default local model size classes, on-demand policy, and disabled baseline.

## RQ-13 — Protocol encoding

Compare generated bounded binary formats and compact structured formats for IPC, traces, DevTools, and agents. Measure encode/decode, allocations, zero-copy safety, schema evolution, fuzzability, diagnostics, language clients, and malformed-input behavior.

Decision output: one or more domain-specific encodings with consistent identity/limit conventions.

## RQ-14 — Storage engine and process model

Evaluate SQLite-backed and custom append/log approaches for cookies, history, bookmarks, session journal, IndexedDB metadata, and settings. Test transactions, concurrency, corruption, migrations, disk full, power loss, profile size, encryption boundary, and repair.

Decision output: store-specific backends and shared transaction/recovery policy.

## RQ-15 — Compatibility prioritization

Analyze WPT/Test262 taxonomy and a controlled application corpus to identify dependencies that unlock the greatest useful surface without embedding site-specific hacks. Track normative prerequisites and security interactions.

Decision output: milestone feature ordering and explicit unsupported map.

## Research protocol

Every study publishes:

- question and decision owner;
- hypotheses and alternatives;
- prototype commits;
- hardware/software environment;
- corpora and workloads;
- correctness/conformance baseline;
- security/accessibility considerations;
- raw samples and analysis method;
- limitations and failed approaches;
- recommendation, confidence, and revisit trigger.

A benchmark result cannot decide a security boundary alone. A decision that affects open-web semantics also requires conformance evidence. Findings that do not reproduce remain exploratory.
