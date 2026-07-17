# 05 — M2: Static Document Engine

Status: implementation game plan; engine-source decision remains a prerequisite for production code  
Owner: engine, text, graphics, accessibility, security, performance, and quality

## 1. Objective

M2 renders a meaningful, script-free, standards-defined subset from controlled and hostile inputs. It establishes reference semantics for parsing, DOM, CSS, layout, paint, hit testing, text, images, scrolling, selection, forms without script, and accessibility before JavaScript multiplies state and timing complexity.

## 2. Entry gates

Before production M2 implementation:

- ADR-0009 is accepted;
- M1 process/sandbox path can run a renderer-class test process;
- IF-001 and IF-002 identities and page-surface contracts are versioned;
- reference platform, text, font, image, and software-raster dependency candidates have review owners;
- WPT revision, reduced-test format, corpus provenance, and fuzz infrastructure are pinned;
- resource and trace schemas can attribute work to document, frame, process, and phase.

A research tokenizer may precede ADR-0009, but it cannot lock the engine source strategy or import unreviewed source.

## 3. WP-006 — HTML tokenizer and tree builder

Task order:

1. encoding label and byte-stream contract;
2. source locations, decoder errors, replacement behavior, and streaming boundaries;
3. HTML tokenizer state machine with generated/reduced fixtures;
4. named character references and bounded lookup data;
5. token limits, attribute limits, nesting/recursion controls, cancellation, and OOM behavior;
6. tree-construction insertion modes and active formatting elements;
7. parser pause/restart contract reserved for later scripts;
8. tokenizer/tree-builder traces;
9. html5lib/WPT-compatible corpus adapter and differential runner;
10. structure-aware fuzzing and automatic reduction.

The parser never owns filesystem, network, profile, or UI authority.

## 4. WP-007 — DOM arena, mutation epochs, and events

Task order:

- generational node handles and document ownership;
- node types, attributes, text, tree operations, traversal, and validation;
- mutation epochs and iterator invalidation;
- document/frame lifetime and destruction;
- event target/listener storage and propagation skeleton;
- selection/range primitives;
- form-control state without script;
- shadow-tree and custom-element placeholders that fail explicitly until implemented;
- accessibility semantic source representation;
- wrapper hooks for later Web IDL without embedding JS assumptions;
- model/property tests for arbitrary valid and invalid mutation sequences;
- memory accounting per document and node class.

## 5. WP-008 — CSS parser, selectors, cascade, and computed values

Task order:

1. CSS tokenization and error recovery;
2. stylesheet/rule/declaration ownership;
3. property metadata generation;
4. selector parser, specificity, matching, and complexity budgets;
5. origins, importance, layers, inheritance, initial/unset/revert semantics for the declared subset;
6. custom-property token storage and cycle handling;
7. computed-value representation and interning experiments;
8. media and feature query skeletons;
9. style sharing and invalidation reference model;
10. CSSOM read-only diagnostic surface;
11. WPT/reduced tests, differential cases, and fuzzing.

Unknown properties and unsupported syntax follow standards-compatible error handling and never silently become Turing-specific behavior.

## 6. WP-009 — layout, text, display list, and reference raster

Implementation proceeds from a complete recomputation reference path:

- containing blocks and formatting contexts;
- block flow and replaced elements;
- intrinsic/min/max sizing;
- inline formatting and line boxes;
- Unicode segmentation, bidi, shaping, fallback, and font metrics through reviewed foundations;
- whitespace, text alignment, decoration, overflow, and selection geometry;
- basic positioning and stacking;
- scroll frames and hit testing;
- semantic fragments and accessible bounds;
- immutable/versioned display items;
- deterministic CPU reference raster;
- GPU compositor handoff through IF-002;
- screenshot, geometry, tree, and semantic traces;
- incremental invalidation only after equivalence to full recomputation.

## 7. Images, SVG, and forms

The M2 subset includes narrowly scoped:

- safe image metadata and decode-service handoff;
- common raster image display through sandboxed decoders;
- basic SVG shapes, paths, paint, transforms, and text only where tests and bounds exist;
- links, buttons, text fields, checkboxes, radio buttons, labels, focus, selection, and submission intent without network submission;
- native IME and accessibility semantics mapped through platform adapters.

Every decoder and font boundary is separately threat-modeled and fuzzed.

## 8. Developer and diagnostic surface

M2 exposes engine truth, not a polished final DevTools product:

- source/token/tree-construction trace;
- DOM and accessibility tree inspection;
- matched rules, cascade origin, computed values, and invalidation reasons;
- fragment, line, display-list, and hit-test overlays;
- font/fallback/shaping diagnostics;
- resource ownership and phase timing;
- deterministic screenshot and reduced-case export.

## 9. Verification matrix

Required evidence includes:

- declared WPT subset and denominator;
- parser conformance and differential tests;
- DOM mutation model tests;
- CSS parser/selector/cascade WPT and reduced tests;
- full versus incremental style/layout equivalence;
- pixel, geometry, accessibility, hit-test, and selection tests;
- international text, RTL, vertical/writing-mode placeholders, zoom, and high-contrast review;
- parser, selector, image, font, SVG, and layout fuzzing;
- pathological depth, selector, text, table-like, and image-size caps;
- fixed-hardware startup, memory, layout, paint, scroll, and screenshot baselines;
- sandbox negative tests with malicious documents.

## 10. M2 exit criteria

- the declared static subset meets its chosen conformance threshold;
- deterministic reference configurations reproduce semantic and pixel results within documented tolerances;
- renderer crashes do not terminate trusted shell state;
- malformed pages remain inside effective sandbox and resource caps;
- keyboard, focus, selection, and accessibility critical paths pass;
- M3 receives stable DOM, event, style, layout, and wrapper contracts;
- unsupported JavaScript and advanced layout are explicit;
- no general-web compatibility or daily-browser claim is made.
