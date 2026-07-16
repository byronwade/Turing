# Engine Pipeline and Versioned Artifacts

Status: research baseline; architecture candidates require prototypes  
Owner: engine architecture  
Purpose: Define the end-to-end rendering pipeline, the identity of every intermediate artifact, and the rules for invalidation, retention, cancellation, and observation.

## Relationship to the Turing program

This document refines the pipeline in [Blueprint 05](../blueprint-v1/05-web-engine.md) and the process identities in [Blueprint 04](../blueprint-v1/04-system-architecture.md).

## Pipeline model

The pipeline begins with an immutable navigation response identity and produces a presented frame plus semantic outputs. Turing should separate logical stages even when an optimized implementation fuses work:

1. response bytes, encoding state, and decoder output;
2. tokenizer tokens and tree-builder operations;
3. DOM mutations and tree-scope epochs;
4. stylesheet parsing, rule storage, selector dependencies, and cascade;
5. computed-style blocks and style-change classification;
6. layout inputs, constraint spaces, fragments, overflow, and scroll geometry;
7. paint properties, display items, chunks, damage, and hit-test data;
8. raster tasks, GPU resources, compositor surfaces, and presentation feedback;
9. accessibility and agent snapshots derived from the same document/layout epoch.

A stage may execute incrementally, but its externally visible output must be explainable as a versioned transformation of declared inputs.

## Artifact identity

Each artifact carries a typed identity rather than a pointer:

- profile, site instance, process, frame, document, and navigation;
- tree scope and DOM mutation epoch;
- stylesheet set and environment epoch;
- style epoch and style-sharing key;
- layout epoch, formatting-context identity, and fragment identity;
- paint epoch, property-tree state, and display-item key;
- raster resource generation and compositor frame token;
- accessibility snapshot version and redaction policy.

Consumers reject stale or cross-document identities. Epoch comparison is explicit; integer wrap, reuse, and serialization rules are defined before optimization.

## Invalidation graph

Invalidation is a first-class graph. A mutation records the dependency class it may affect: selector matching, inherited values, custom properties, container queries, font metrics, intrinsic sizes, layout geometry, paint-only properties, compositing, accessibility, hit testing, or script-visible geometry.

The engine chooses the smallest safe root. Test builds can force a full style/layout/paint rebuild and compare semantic outputs. A fast path is disabled when equivalence cannot be established. The trace records the cause, roots considered, work skipped, work performed, time, bytes allocated, and output changes.

## Scheduling and cancellation

Navigation, lifecycle transitions, resize, zoom, font completion, image decode, device loss, and document destruction can invalidate work already in flight. Every asynchronous stage therefore receives a cancellation token and a document epoch.

Tasks publish results only through an epoch-checked commit point. Expensive work is divided into bounded units with deadlines so foreground input and browser chrome remain responsive. Background work can be preempted, but cancellation must not leave partially visible state or leaked resources.

## Reference and optimized paths

The reference path favors simple data flow and deterministic output. Optimized paths may add caches, retained artifacts, parallel stages, GPU execution, and speculative work. They must:

- consume and produce the same semantic artifact formats;
- expose the same trace vocabulary;
- fall back without changing web-visible behavior;
- survive resource exhaustion and device loss;
- compare against the reference path in continuous differential tests.

The software raster path is retained as a correctness and recovery tool even after GPU acceleration becomes normal.

## Non-negotiable invariants

- A stage never commits output for a stale document or configuration epoch.
- Incremental output must equal full recomputation for all observable semantics.
- Partial failures prefer conservative extra work over missing content or security checks.
- Trace and DevTools schemas describe logical engine truth rather than private implementation accidents.
- Caches are bounded, partition-aware, attributable, and disposable without changing semantics.

## Required evidence

- A runnable pipeline prototype that emits token, DOM, style, fragment, paint, hit-test, accessibility, and frame traces.
- Mutation-generated equivalence tests comparing incremental and full recomputation.
- Cancellation tests at every stage boundary, including navigation and process termination.
- Memory and latency profiles for small documents, application-style documents, and adversarial cases.
- A versioning and serialization specification for diagnostic artifacts.

## Known risks and unresolved questions

- Too many artifact layers can create copying, indirection, and bookkeeping cost.
- Fusing stages can hide invalidation bugs and make diagnostics misleading.
- Epoch schemes can become a substitute for correct ownership if stale references remain reachable.
- A reference path that diverges architecturally from production may stop being a useful oracle.

## Primary sources

- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- WHATWG DOM Standard — https://dom.spec.whatwg.org/
- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- Chromium LayoutNG — https://developer.chrome.com/docs/chromium/layoutng
- Web Platform Tests — https://web-platform-tests.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
