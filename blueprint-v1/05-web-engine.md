# 05 — Web Engine Design

## 1. Engine pipeline

The initial deterministic pipeline is:

`bytes → decoder → HTML tokenizer → tree builder → DOM mutation → style invalidation → selector matching/cascade → computed values → layout tree → fragments → paint properties → display list → raster/composite graph → pixels`

Input, style, layout, paint, accessibility, and script can invalidate different stages. The engine records why a stage ran, which nodes or fragments were affected, and how much time and memory were consumed. Optimization is accepted only if the invalidation model remains observable and testable.

## 2. DOM representation

The DOM uses stable generational handles into arenas rather than raw cross-component pointers. Goals:

- compact node header and tagged node-kind representation;
- document-scoped allocation and bulk destruction;
- generation checks to reject stale handles;
- side tables for infrequent data such as event listeners, custom-element state, rare attributes, layout attachment, accessibility metadata, and DevTools annotations;
- interned names and qualified names with bounded lifetime;
- explicit wrapper map between JavaScript objects and native nodes;
- mutation epochs for live collections, style invalidation, layout, accessibility, and agent snapshots;
- no renderer-global registry that allows a handle from one document to resolve in another.

Parent/child/sibling relationships begin as compact indices. Alternate structures require benchmark evidence across mutation-heavy and read-heavy workloads.

## 3. HTML parsing

The tokenizer and tree builder implement the standard algorithms with state-machine code generated or verified against compact tables. Requirements include:

- streaming input and encoding restarts where permitted;
- parser-blocking script behavior and speculative preload discovery without violating ordering;
- foster parenting, adoption agency behavior, templates, foreign content, fragments, quirks modes, and error recovery;
- reentrancy and `document.write` behavior isolated behind explicit parser states;
- byte/character/source mapping for DevTools without forcing full-source retention for all documents;
- hard limits and cancellation for pathological tokens, nesting, attributes, and mutation loops while preserving defined behavior where feasible.

Reduced test cases are generated for every parser defect. Differential comparison may use established engines as an oracle hint, never as the normative specification.

## 4. CSS architecture

### 4.1 Parsing and values

CSS parsing produces compact immutable rule data where possible. Declarations preserve enough source information for DevTools while computed style uses typed values. Custom properties retain token streams and dependency edges. Unknown or unsupported syntax is handled according to forward-compatible parsing rules, not treated as a fatal error.

### 4.2 Selector engine

Selectors are compiled into match programs keyed from the rightmost compound selector. Candidate indexes include ID, class, local name, attribute presence, state, pseudo-element, and universal buckets. The engine tracks dependencies for structural, stateful, relational, shadow-DOM, and `:has()` selectors so mutations invalidate the smallest safe region.

Optimization rules:

- fast rejection data must never alter semantics;
- bloom filters and ancestor summaries are scoped and invalidated correctly;
- selector caches include document/style epochs and tree-scope identity;
- style sharing is denied when custom properties, container queries, animations, form state, shadow scope, or inherited dependencies make equivalence uncertain.

### 4.3 Cascade and computed values

Cascade ordering includes origin, importance, layers, encapsulation, specificity, scope, and source order. Computed-value construction records dependencies on fonts, viewport, root style, environment variables, custom properties, container features, and user preferences. Values use compact representations and shared immutable blocks for common groups.

## 5. Layout architecture

Layout consumes styled DOM and emits immutable fragment trees for a layout epoch. A layout object is not the DOM node; generated boxes, anonymous wrappers, pseudo-elements, continuations, and fragmentation require separate identity.

Initial order of implementation:

1. replaced elements and basic block formatting;
2. inline formatting, shaping, bidi, line breaking, selection geometry;
3. floats and positioning;
4. flexbox;
5. grid;
6. tables;
7. fragmentation, columns, printing;
8. writing modes, ruby, advanced containment, subgrid, and specialized modules.

Each formatting context has:

- explicit inputs and available-space constraints;
- intrinsic sizing methods;
- percentage and cyclic-dependency rules;
- break opportunities and fragmentation tokens;
- baseline and alignment outputs;
- scrollable/ink overflow;
- hit-test and accessibility geometry.

Parallel layout is deferred until the fragment model, dependency graph, and deterministic test oracle are stable. Parallelism will operate on proven independent subtrees, not shared mutable layout objects.

## 6. Text and fonts

Text is a first-class subsystem, not a string painted at coordinates. It handles:

- Unicode segmentation, bidi, script runs, language, font matching and fallback;
- shaping, kerning, ligatures, variation fonts, color fonts, emoji, vertical metrics, ruby, text emphasis, decorations, and synthetic styles;
- line breaking, hyphenation policy, justification, white-space processing, tabs, soft wraps, selection, caret positions, hit testing, IME composition, and accessibility ranges;
- asynchronous font loading and metric changes without unbounded layout churn;
- glyph and shaped-run caches with profile/document accounting and pressure eviction.

HarfBuzz/FreeType/CoreText/DirectWrite may be used behind adapters after dependency review. Turing owns CSS font selection, fallback policy, layout metrics, privacy behavior, and cache accounting.

## 7. Paint and display lists

Layout fragments emit paint chunks with stable property-tree references:

- transform tree;
- clip tree;
- effect/opacity/filter tree;
- scroll tree;
- stacking and hit-test order.

Display items are immutable, bounded, and validated by the GPU service. Retained display lists reuse unchanged chunks across epochs. Damage tracking produces conservative regions; correctness failures prefer extra paint over missing pixels.

Large dimensions, filters, shadows, gradients, paths, text runs, images, and nested clips are budgeted to prevent memory or GPU denial of service.

## 8. Compositing

The compositor selects layers based on scrolling, transforms, animation, video, canvas, WebGL/WebGPU, filters, isolation, and damage—not arbitrary DOM elements. Promotion is budget-aware. Layer churn is measured and visible in DevTools.

The frame scheduler coordinates:

- input sampling and prediction;
- script/style/layout deadlines;
- raster priorities;
- compositor-only animations;
- viewport and scroll updates;
- missed-frame attribution;
- display refresh rates from 60 Hz through high-refresh devices;
- occlusion and background suppression.

## 9. Events, input, and editing

Native input is normalized by the platform adapter and routed through hit testing to event targets. Security-sensitive notions such as transient user activation are kernel/renderer-coordinated and cannot be forged by agent or script messages.

Editing is a dedicated model covering selection, caret navigation, composition, beforeinput/input events, undo grouping, clipboard sanitization, spellcheck interfaces, form controls, password fields, drag/drop, and accessibility actions. Agents use structured editing commands rather than synthetic trusted events.

## 10. Scrolling

Scroll state is compositor-owned when possible, synchronized to the renderer with epochs. The engine supports nested scrolling, overscroll policy, scroll anchoring, snap points, smooth scrolling, fixed/sticky positioning, viewport units, visual/layout viewport distinction, and accessibility scroll actions. Main-thread scroll dependencies are reported.

## 11. Images, canvas, SVG, and graphics

Image metadata is parsed before allocation. Decode occurs in sandboxed utility processes with dimension, pixel-count, frame-count, duration, and memory limits. Decoded data is tiled or downsampled when safe.

Canvas 2D begins with a recorded command model and CPU reference backend, then GPU acceleration. Readback and origin cleanliness are enforced. SVG uses shared CSS, DOM, layout, paint, filter, text, and hit-test primitives where semantics align. WebGL and WebGPU are later tracks because their validation and GPU attack surface require dedicated staffing.

## 12. Accessibility tree

Accessibility is derived during semantic/layout updates, not scraped from pixels. Nodes include role, name, description, value, state, relationships, actions, bounds, text ranges, live-region behavior, table semantics, and hidden/inert policy. Cross-origin subtrees remain separately owned and exposed only through platform-authorized composition.

The accessibility tree powers native assistive technologies and a redacted agent semantic snapshot. The agent representation excludes password values, hidden fields, browser-internal UI, ungranted cross-origin frames, and policy-designated sensitive regions.

## 13. Engine observability

Per document and frame, DevTools can inspect:

- parser states and blocking resources;
- style invalidation reasons and matched-rule costs;
- layout roots, fragment tree, intrinsic sizing, and forced synchronous layouts;
- paint chunks, damage, raster tasks, layer reasons, and GPU memory;
- event listeners, task queues, long tasks, animation deadlines, and input latency;
- accessibility-tree differences;
- retained memory by DOM, style, layout, display lists, images, fonts, JS wrappers, and caches.

Instrumentation is compiled out or sampled in stable builds where overhead requires it, but the same event schema remains.

## 14. Correctness strategy

Every feature moves through:

1. normative algorithm notes and data model;
2. parser/model unit tests;
3. reduced rendering tests;
4. Web Platform Tests where available;
5. differential screenshots and DOM/layout traces against multiple engines;
6. fuzzing and mutation testing;
7. accessibility and input tests;
8. performance baselines;
9. explicit unsupported list.

Pixel diffs alone are insufficient because multiple incorrect layouts can resemble each other. The reference engine can emit fragment, paint, hit-test, and accessibility traces in a stable diagnostic format.
