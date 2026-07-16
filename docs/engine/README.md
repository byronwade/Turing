# Browser Engine Engineering Book

Status: detailed research and design baseline  
Owner: engine architecture  
Canonical overview: [Blueprint 05 — Web engine](../blueprint-v1/05-web-engine.md)

This book expands the web-engine chapter into subsystem contracts that can guide prototypes, reviews, benchmarks, and eventual implementation. It does not make any browser-compatibility or performance claim. The Blueprint remains the normative architectural owner; this book supplies deeper implementation questions and evidence requirements.

## Reading order

1. [Pipeline and versioned artifacts](01-pipeline-and-artifacts.md)
2. [HTML parser and DOM](02-html-parser-and-dom.md)
3. [CSS, cascade, selectors, and invalidation](03-css-cascade-and-invalidation.md)
4. [Layout, intrinsic sizing, and fragmentation](04-layout-and-fragmentation.md)
5. [Paint, compositor, raster, and GPU](05-paint-compositor-and-gpu.md)
6. [Text, fonts, and internationalization](06-text-fonts-and-i18n.md)
7. [Images, media, SVG, and canvas](07-images-media-svg-and-canvas.md)
8. [Input, editing, scrolling, and accessibility](08-input-editing-accessibility.md)
9. [Memory, data structures, and observability](09-memory-data-structures-and-observability.md)

## Engine-wide thesis

Turing should use a deterministic, inspectable pipeline whose outputs are versioned artifacts rather than mutable cross-subsystem object graphs. Correctness begins with a serial oracle. Incrementality, retention, parallelism, GPU acceleration, and specialized fast paths are accepted only when they preserve observable semantics and can be compared against the oracle.

The architecture should optimize the complete user path:

`network bytes → decode → parse → DOM → style → layout → paint → raster → composite → present → accessible interaction`

Every stage must identify its inputs, output identity, invalidation causes, ownership, memory budget, cancellation points, failure behavior, trace schema, and test oracle.

## Cross-cutting contracts

- Web content is hostile and can force worst-case parser, selector, layout, paint, graphics, text, and accessibility behavior.
- A document, tree scope, layout epoch, paint epoch, and compositor frame are different identities.
- No raw pointer from one document or process is accepted as durable identity.
- Full recomputation remains available in test builds to validate incremental results.
- Accessibility, hit testing, selection, and agent semantics derive from the same engine truth as pixels.
- The GPU process validates bounded display and resource commands; renderers do not submit arbitrary native handles.
- Resource ownership is semantic: document, frame, worker, cache, shared service, extension, DevTools, or agent.
- Platform libraries may provide shaping, rasterization, codecs, and GPU primitives, but Turing owns web-visible behavior, policy, accounting, and tests.
- Unsupported behavior is explicit and visible in conformance reports.

## Implementation sequence

The minimum useful sequence is:

1. streaming decoder and HTML tokenizer;
2. DOM arena with mutation epochs;
3. CSS parser, selector matching, cascade, and computed values;
4. block and inline layout with deterministic fragment output;
5. software paint/raster reference path;
6. hit testing, text selection, accessibility snapshots, and input routing;
7. retained display lists and damage tracking;
8. GPU compositor and isolated decoders;
9. incremental invalidation and adaptive parallelism;
10. advanced layout, media, graphics, and high-refresh optimization.

## Leadership criteria

Turing should not call its engine top-tier until it can publish:

- pinned WPT results with full failure and timeout accounting;
- reduced semantic traces for parser, style, layout, paint, hit testing, and accessibility;
- fixed-hardware latency, memory, energy, and recovery results;
- deterministic differential testing against multiple engines;
- fuzzing and fault-injection coverage;
- platform accessibility results;
- public unsupported-feature and residual-risk maps.

## Related material

- [JavaScript runtime book](../javascript/README.md)
- [Security engineering book](../security-engine/README.md)
- [Performance engineering book](../performance/README.md)
- [Developer experience book](../developer-experience/README.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Research program](../blueprint-v1/22-research-program.md)
