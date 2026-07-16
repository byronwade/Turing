# Layout, Intrinsic Sizing, and Fragmentation

Status: research baseline; formatting-context contracts require prototypes  
Owner: layout  
Purpose: Define a deterministic fragment-based layout system that can grow from correct block/inline formatting to flex, grid, tables, writing modes, and fragmentation without binding DOM identity to box identity.

## Relationship to the Turing program

Text shaping details are in [Text, fonts, and internationalization](06-text-fonts-and-i18n.md); scheduling details are in the [performance book](../performance/README.md).

## Core model

Layout consumes styled elements and formatting-context inputs, then emits immutable fragments for a layout epoch. Generated boxes, anonymous wrappers, pseudo-elements, continuations, repeated table headers, and fragmentation descendants have independent identities.

A `ConstraintSpace`-like input records available sizes, percentage bases, writing mode, direction, fragmentation context, containing-block facts, float/exclusion state, baseline needs, and query/container information. A fragment records geometry, overflow, baselines, break tokens, child placement, paint identity, hit-test geometry, and accessibility ranges.

## Formatting-context boundaries

Each formatting context exposes explicit intrinsic-size and layout operations. Contexts do not mutate neighboring objects through implicit global state. Initial contexts:

1. replaced and basic block;
2. inline formatting with text shaping and bidi;
3. floats and positioning;
4. flex;
5. grid;
6. tables;
7. multicolumn, pagination, and printing;
8. advanced writing modes, ruby, subgrid, containment, and specialized modules.

Contexts may call child contexts through stable contracts. Cyclic percentages and intrinsic queries use explicit dependency resolution and cycle rules.

## Inline layout

Inline layout is a collaboration among DOM text runs, style boundaries, Unicode segmentation, bidi resolution, shaping, line breaking, hyphenation, justification, ruby, vertical metrics, selection, and caret geometry. Shaped runs are cached only when font, script, language, direction, features, variation settings, scale, and text identity agree.

Line boxes are not the sole source of truth; fragment ranges preserve mapping to source text and accessibility. Editing and selection require stable positions across incremental relayout.

## Fragmentation

Break opportunities, forced breaks, avoid constraints, widows/orphans, repeated content, margin handling, and fragmentation tokens are modeled explicitly. A break token identifies the exact continuation state needed to resume layout in a new fragmentainer.

Printing and multicolumn layout share primitives but have distinct pagination, page-margin, color, and resource behavior. Fragmentation tests use semantic fragment traces in addition to pixels.

## Incremental and parallel layout

The first implementation can relayout a conservative root. Incremental layout is introduced with a dependency graph that records intrinsic-size and containing-block relationships. Parallel layout is allowed only for subtrees with proven independent inputs and immutable outputs.

A scheduler estimates work size and synchronization cost. Small trees remain serial. Any parallel result can be replayed deterministically in a serial diagnostic mode.

## Geometry consumers

Paint, scrolling, hit testing, accessibility, DevTools, Intersection/Resize Observers, script geometry APIs, and agents consume versioned fragment geometry. Geometry queries can force synchronization; the engine records the forcing call, work performed, and latency.

Stale geometry never authorizes an input or agent action. Cross-origin fragment data is composed through restricted interfaces rather than shared object access.

## Non-negotiable invariants

- DOM nodes and layout boxes/fragments are not assumed one-to-one.
- Layout results are immutable for an epoch and published atomically.
- Incremental and parallel results match deterministic full layout.
- Large dimensions, deep fragmentation, and adversarial intrinsic-size graphs are bounded.
- Text, hit testing, accessibility, and script geometry share one coordinate and epoch model.

## Required evidence

- Semantic fragment traces for every implemented formatting context.
- WPT and reduced tests for intrinsic sizing, percentages, bidi, writing modes, flex, grid, tables, and fragmentation.
- Full-versus-incremental and serial-versus-parallel equivalence suites.
- Object-size, allocation, cache, layout-root breadth, and p95/p99 latency measurements.
- Fault tests for OOM, font completion, resize storms, navigation cancellation, and print interruption.

## Known risks and unresolved questions

- A fragment model can become too verbose for common documents.
- Cross-context intrinsic dependencies can defeat parallelism and incremental layout.
- Text shaping and platform metrics can make deterministic cross-platform pixels impossible.
- Script geometry queries can create unavoidable synchronization cliffs.

## Primary sources

- Chromium LayoutNG — https://developer.chrome.com/docs/chromium/layoutng
- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- CSS Working Group drafts — https://drafts.csswg.org/
- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- Unicode Bidirectional Algorithm — https://unicode.org/reports/tr9/
- Web Platform Tests — https://web-platform-tests.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
