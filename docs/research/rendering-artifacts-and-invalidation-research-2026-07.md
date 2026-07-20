# Rendering Artifacts and Invalidation Research - July 2026

Status: deferred `RQ-18` no-claim research packet
Owner: web engine, layout, paint, accessibility, compositor, performance, and quality
Research date: 2026-07-19
Confidence: high for the standards and public architecture observations; low for any Turing pipeline or performance conclusion until executable oracles and independent measurements exist

## Question

Which pipeline artifact and invalidation model is most correct, compact, and observable across parser, style, layout, paint, accessibility, and compositor stages?

## Why This Matters

Browser rendering is a dependency problem as much as a sequence of functions. A mutation can alter DOM structure, style matching, geometry, paint output, hit testing, accessibility semantics, scrolling, or compositing. An optimization that skips work must prove that no observable output became stale. An optimization that retains every intermediate artifact can preserve correctness while producing unacceptable memory, invalidation, and debugging costs.

This packet defines a source-backed research route for `RQ-18`. It does not select mutable objects, immutable epochs, retained display lists, a compositor model, or a performance strategy.

## Source-backed observations

### DOM mutation delivery is observable

The WHATWG DOM Living Standard defines `MutationObserver`, mutation records, observation options, record queues, and microtask-based notification. It also defines subtree behavior for removed nodes. A rendering pipeline cannot treat mutation batching, ordering, or callback-visible state as an internal implementation detail when those semantics affect script-visible behavior.

Source: [WHATWG DOM Standard](https://dom.spec.whatwg.org/), updated 2026-07-18 and retrieved 2026-07-19.

### Containment creates explicit optimization boundaries

CSS Containment Level 1 defines size, layout, and paint containment as author-visible ways to make a subtree more independent. The specification describes containment as a mechanism for stronger and more predictable optimization, while also defining restrictions and effects that user agents must preserve. Containment is therefore a standards input and test dimension, not a license to assume arbitrary subtree independence.

Source: [W3C CSS Containment Module Level 1](https://www.w3.org/TR/css-contain-1/), retrieved 2026-07-19.

### Public Chromium documentation separates rendering stages

Chromium's rendering documentation describes a critical path and separate rendering architecture diagrams for script/style/layout/paint and composited software or GPU paths. The diagrams and documentation are useful observations of one engine's stage boundaries, not a normative requirement that Turing reproduce its internal objects or use its implementation.

Sources: [Chromium The Rendering Critical Path](https://www.chromium.org/developers/the-rendering-critical-path/), [Chromium Rendering Architecture Diagrams](https://www.chromium.org/developers/design-documents/rendering-architecture-diagrams/), retrieved 2026-07-19.

## Candidate artifact models

The research comparison should measure at least these models:

1. Mutable graph with explicit invalidation flags and dependency edges.
2. Immutable epoch artifacts published at stage boundaries, with bounded retention and cancellation.
3. Hybrid model: stable identity handles plus immutable snapshots for diagnostics and cross-thread publication, with mutable local caches.
4. Full recomputation oracle used only as a correctness reference, not assumed to be a production design.

Each model must define ownership, identity, lifetime, memory accounting, publication, cancellation, stale-result rejection, and recovery behavior for DOM, style, layout, paint, accessibility, hit testing, and compositor outputs.

## Invalidation classes

The experiment manifest should classify mutations by affected dependencies rather than treating every mutation as a full-tree redraw:

- parser/document insertion and removal;
- text and character-data changes;
- attribute, class, ID, and inline-style changes;
- stylesheet insertion, removal, rule change, and media/container-query change;
- viewport, zoom, font, writing-mode, direction, and device-scale changes;
- intrinsic-size, image, font, video, and asynchronous resource completion;
- scroll, transform, animation, focus, selection, and pointer-state changes;
- accessibility semantics, generated content, shadow tree, slot, and hidden-state changes;
- GPU loss, surface resize, occlusion, capture, and software-fallback transitions.

The expected result is a dependency closure and artifact-epoch record, not only a final screenshot. A mutation that leaves pixels unchanged may still require updated accessibility, hit-test, focus, diagnostics, or script-visible state.

## Evidence and oracle design

Before choosing an artifact model, the owner-approved package should provide:

- a static, mutation-heavy, animation, editing, accessibility, containment, international-text, resource-completion, and adversarial corpus;
- a full-recomputation reference path with explicit unsupported cases and deterministic seeds;
- mutation sequences that test batching, order, cancellation, stale publication, repeated changes, and changes during layout or paint;
- per-stage artifact IDs, input dependency IDs, output hashes, invalidation causes, retained bytes, and release events;
- pixel, semantic/accessibility-tree, hit-test, focus/selection, scroll, and script-observable comparison oracles;
- cross-thread and cross-process identity checks for document epoch, frame, origin/site, process, and surface ownership;
- cancellation, timeout, renderer crash, GPU loss, restart, and recovery records;
- trace packages that show whether work was skipped, repeated, coalesced, or incorrectly published;
- independent review of the oracle, corpus, unsupported behavior, and security implications.

## Measurement plan

Measure each model under equivalent workload and security configuration:

- bytes and allocations by artifact class, live and retained;
- invalidation fan-out, stage executions, recomputation, cancellation, and stale-result rejection;
- input-to-present latency, frame pacing, long-task distribution, and recovery latency;
- mutation-to-observable-state latency for pixels, accessibility, hit testing, and script callbacks;
- CPU, wakeups, synchronization, IPC, GPU work, and energy where available;
- trace size, diagnostic overhead, and redaction/retention cost;
- correctness failures, unsupported cases, timeouts, crashes, and cleanup denominator.

No result may be normalized by silently reducing accessibility, disabling containment semantics, discarding difficult pages, or ignoring failed and cancelled work. A smaller artifact graph is not an improvement if it increases stale output, latency variance, recovery cost, or security exposure.

## Rejection rules

Reject the packet as decision evidence when it:

- treats a screenshot or final pixel hash as a complete rendering oracle;
- ignores MutationObserver ordering, microtask delivery, removed-subtree behavior, focus, selection, hit testing, or accessibility output;
- assumes CSS containment or an internal engine stage makes arbitrary descendants independent;
- copies Chromium object boundaries as a Turing design without measuring requirements and alternatives;
- reports only successful frames or omits cancelled, stale, crashed, GPU-loss, unsupported, or recovery cases;
- compares models with different page corpora, security settings, resource state, device scale, or process topology;
- uses a same-agent implementation and oracle as independent evidence;
- retains unbounded artifacts, traces, snapshots, or page content containing secrets.

## Current status and next proof

`RQ-18` remains deferred outside the active pre-build crosswalk. The next proof is an owner-approved artifact identity and dependency schema, followed by a synthetic corpus and full-recomputation oracle with mutation, accessibility, hit-testing, cancellation, and recovery fixtures. No rendering architecture, invalidation policy, compatibility result, accessibility result, performance result, or readiness claim follows from this packet.

## Claim boundary

This is source-backed research preparation only. It does not select a pipeline, artifact representation, invalidation algorithm, compositor model, caching policy, memory budget, performance result, compatibility target, accessibility implementation, or production support claim.
