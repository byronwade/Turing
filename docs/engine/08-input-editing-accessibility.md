# Input, Editing, Scrolling, and Accessibility

Status: research baseline; native integration requires platform prototypes  
Owner: interaction and accessibility  
Purpose: Specify one coherent interaction model from native input through hit testing, events, editing, scrolling, focus, and platform accessibility.

## Relationship to the Turing program

Trusted confirmation and agent interaction are expanded in the [security](../security-engine/README.md) and [AI](../ai/README.md) books.

## Input normalization

Platform adapters translate pointer, mouse, touch, pen, keyboard, wheel, gesture, drag, IME, accessibility, and synthesized automation inputs into typed events. Raw platform messages never bypass browser policy.

Each event carries device class, coordinates, buttons/keys, modifiers, timestamp, routing target, profile, frame, document epoch, trusted-source class, and user-activation implications. Only browser-controlled paths can create trusted user activation.

## Hit testing and event dispatch

Hit-test data is produced from committed paint/layout state and versioned with the document and compositor frame. Compositor hit testing may route scrolling or input without blocking the renderer, but DOM event targeting is reconciled against current engine state.

Event dispatch implements composed paths, shadow retargeting, capture/bubble phases, default actions, passive listeners, pointer capture, cancellation, focus, and reentrancy. Stale targets fail safely.

## Editing model

Editing is not implemented as arbitrary DOM mutation. Commands cover selection movement, insertion, deletion, replacement, paragraph operations, formatting where supported, undo grouping, composition, clipboard, drag/drop, spellcheck, and form-control behavior.

`beforeinput` and `input` ordering, mutation observers, selection events, custom editors, password protection, and accessibility actions receive dedicated tests. Undo records have bounded memory and document lifetime.

## Scrolling

Scroll nodes are explicit in layout/paint/compositor state. Scrolling supports nested containers, visual and layout viewports, anchoring, snap, overscroll, smooth behavior, fixed/sticky elements, wheel/touch gestures, keyboard and accessibility actions.

Compositor scrolling uses committed constraints. Main-thread scroll dependencies are reported. Scroll offsets are synchronized with epochs so script and hit testing do not consume unrelated state.

## Accessibility tree

The accessibility tree is generated from DOM semantics, ARIA, style visibility/inertness, layout geometry, text ranges, focus, and platform policy. It includes role, name, description, value, state, relationships, actions, bounds, live-region behavior, table structure, and text navigation.

Cross-origin frame subtrees remain separately owned. Platform bridges compose them without exposing renderer pointers or unauthorized content. The same semantic source can produce a redacted agent snapshot, but accessibility and agent policies remain separate consumers.

## Browser and developer integration

DevTools can inspect event listeners, paths, default actions, hit-test regions, scroll trees, focus order, accessibility name computation, relationships, live-region events, editing commands, and input latency.

Automation uses WebDriver BiDi or the Turing protocol with explicit trusted/untrusted semantics. Agent actions use structured commands and cannot synthesize trusted confirmation clicks.

## Non-negotiable invariants

- Page, extension, automation, and agent messages cannot forge trusted input or user activation.
- Hit-test, selection, accessibility, and event targets are checked against current document epochs.
- Keyboard and assistive-technology paths receive equivalent security and confirmation information.
- Editing operations preserve undo, composition, and selection invariants under script reentrancy.
- Accessibility is release-critical engine output, not post-processing of pixels.

## Required evidence

- WPT and reduced tests for events, input, selection, editing, scrolling, focus, ARIA, and accessibility names.
- Manual VoiceOver, Narrator, NVDA, and Orca/AT-SPI matrices.
- High-refresh input-to-present latency and compositor/main-thread attribution.
- IME, bidi selection, zoom, forced colors, reduced motion, and keyboard-only workflow tests.
- Adversarial tests for stale targets, clickjacking, synthetic activation, cross-origin frames, and spoofed prompts.

## Known risks and unresolved questions

- Platform input and accessibility APIs have substantially different threading and lifecycle models.
- Custom web editors depend on obscure event and selection behavior.
- Asynchronous compositor hit testing can race DOM mutation.
- Agent and accessibility snapshots can accidentally converge into an overprivileged shared API.

## Primary sources

- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- WHATWG DOM Standard — https://dom.spec.whatwg.org/
- WAI-ARIA — https://www.w3.org/TR/wai-aria/
- Accessible Name and Description Computation — https://www.w3.org/TR/accname-1.2/
- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
