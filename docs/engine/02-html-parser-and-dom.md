# HTML Parser and DOM Architecture

Status: research baseline; no parser implementation exists  
Owner: HTML and DOM  
Purpose: Specify a streaming, standards-driven parser and a compact DOM representation that remain correct under reentrancy, mutation, hostile input, and JavaScript wrapper lifetimes.

## Relationship to the Turing program

The JavaScript lifetime contract is expanded in the [runtime book](../javascript/README.md); security limits are expanded in the [security book](../security-engine/README.md).

## Decoder and source model

The decoder owns byte-to-code-point conversion, encoding detection/restart rules, byte offsets, and bounded source retention. DevTools source mapping must not require retaining every response byte indefinitely. The source manager should support:

- streaming chunks and partial tokens;
- line/column and byte/code-unit mapping;
- decoder restart before the standard’s point of no return;
- source slices referenced by compact ranges;
- redaction and eviction policies for sensitive or very large documents.

Parser diagnostics are not exposed as exceptions unless the platform requires it; HTML error recovery is normal behavior.

## Tokenizer and tree builder

Implement the WHATWG state machines directly from reviewed tables or generated code with readable trace names. Token objects should be short-lived and allocation-light. Tree-builder operations must cover insertion modes, foster parenting, the adoption agency algorithm, templates, foreign content, fragments, quirks modes, parser pauses, and script-induced reentrancy.

A speculative preload scanner may run beside the parser, but its requests remain provisional until policy, base URL, CSP, credentials mode, and document identity are validated. Speculation cannot alter parser ordering.

## DOM storage

The baseline DOM is a document-scoped arena addressed by generational `NodeId` handles. Hot node data should remain compact:

- node kind, parent, first/last child, sibling links, flags, and tree-scope identity;
- names and common atoms interned under bounded document/profile lifetimes;
- attributes stored inline for the common case with spill storage for larger sets;
- rare data in side tables: listeners, custom-element state, shadow roots, style/layout attachment, accessibility data, DevTools annotations, and agent metadata.

Document destruction can reclaim arena regions in bulk. A handle from one document cannot resolve in another even if numeric indices match.

## Mutation and live views

Mutation APIs pass through one coordinator that updates tree structure, ranges, iterators, live collections, custom-element reactions, mutation observers, style dependencies, layout attachment, accessibility, focus, selection, and agent references.

Each mutation produces a typed change record and advances relevant epochs. Live collections use cached query plans plus mutation versions rather than eager global updates. Reentrant callbacks run only at specified checkpoints; internal invariants are restored before script execution.

## Shadow DOM and custom elements

Tree scopes, composed trees, slot assignment, event retargeting, style scoping, focus navigation, accessibility composition, and serialization are distinct concerns. Shadow-root identity is explicit and cannot be inferred from pointer ancestry alone.

Custom-element definition, upgrade, construction stacks, reaction queues, and lifecycle callbacks require deterministic scheduling. Failed construction and navigation cancellation must not leave half-upgraded nodes.

## JavaScript wrappers and lifecycle

DOM wrappers are GC-managed objects that reference rooted engine handles, never borrowed Rust references. Wrapper identity is realm-aware. The tracing contract covers document roots, wrapper maps, event listeners, callbacks, and cycles between JS and DOM.

A wrapper operation validates realm, origin policy, node generation, and current document state. Detached subtrees remain alive only while reachable. DevTools and agents use separately scoped references that expire on document epoch change.

## Non-negotiable invariants

- HTML conformance follows the living standard and pinned tests, not behavior inferred from one engine.
- All parser buffers, token lengths, nesting, attributes, and queued reactions are bounded or pressure-aware.
- DOM mutation cannot bypass style, layout, accessibility, selection, security, or wrapper bookkeeping.
- Document and tree-scope identity are checked at every cross-component lookup.
- Parser tracing and reduced tests preserve enough state to reproduce reentrancy defects.

## Required evidence

- Tokenizer/tree-builder traces for the complete insertion-mode matrix and parser error recovery.
- Pinned WPT parser, DOM, custom-elements, shadow-DOM, and event results.
- Grammar- and mutation-aware fuzzing with OOM and cancellation injection.
- Object-size and traversal benchmarks across article, application, table, shadow-DOM, and mutation-heavy corpora.
- Wrapper-cycle, detached-document, and document-destruction leak tests.

## Known risks and unresolved questions

- Arena compaction and stable identity may conflict without an indirection layer.
- Live collections and ranges can create hidden mutation costs.
- Parser preload speculation can violate policy or waste bandwidth if identity is not revalidated.
- Custom elements and reentrant script can make otherwise local invariants globally observable.

## Primary sources

- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- WHATWG DOM Standard — https://dom.spec.whatwg.org/
- Web IDL — https://webidl.spec.whatwg.org/
- Web Platform Tests — https://web-platform-tests.org/
- Servo project — https://servo.org/about/
- Ladybird project — https://ladybird.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
