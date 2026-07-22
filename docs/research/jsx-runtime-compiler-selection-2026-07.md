# JSX Runtime Compiler Selection - July 2026

Status: no-claim research recommendation; not an accepted ADR or implementation authorization
Owner: architecture, UI runtime, build, security, accessibility, performance, and developer experience
Research date: 2026-07-22
Source artifact: [`turing-nova-design-source.jsx`](../ui-runtime/design-lab/turing-nova-design-source.jsx)

## Question

What is the smallest, most capable, and lowest-maintenance path for treating the supplied Nova JSX file as the browser face without hand-authoring a second visual shell?

## Executive recommendation

Use a pinned **esbuild build-time JSX front-end** and keep the release renderer entirely Turing-owned:

```text
Nova JSX source
    -> pinned esbuild JSX lowering
    -> Turing React-shaped compatibility shim
    -> bounded Turing component IR / bytecode
    -> Turing layout, semantics, hit testing, paint, and animation
    -> replaceable platform window and accessibility adapters
```

Servo remains the page-surface engine. It can render the web content hosted by a browser tab, but it is not a React/JSX compiler or a trusted-chrome component runtime. Loading the Nova file as an ordinary web page would make browser chrome page DOM and runtime CSS/JavaScript, which conflicts with the repository's current trusted-chrome boundary.

This recommendation reduces language-front-end maintenance. It does **not** eliminate the work of defining Turing-owned component semantics, hooks, event routing, accessibility, resource limits, source maps, and debugging. No claim is made that the full Nova file executes today.

## Evidence

### esbuild

The official esbuild API supports automatic JSX lowering and custom JSX factories, fragments, and import sources. That permits the unchanged source artifact to target a Turing factory instead of `React.createElement`, while keeping parsing and syntax maintenance outside Turing's release runtime. See the [official JSX API documentation](https://esbuild.github.io/api/), especially the JSX factory, fragment, and import-source options.

On the reference Windows development host, `npx --yes esbuild --version` reported `0.28.1`, and the complete Nova source transformed successfully with a custom factory when bundled in a development probe. This is a local observation, not a release reproducibility result; the version must be pinned and its package provenance reviewed before adoption.

### Servo

Servo describes itself as an embeddable Rust web engine and owns browser-web concerns such as HTML, CSS, layout, and rendering. The [Servo project](https://servo.org/) is therefore the correct future owner for a tab's web page surface, subject to the unresolved ADR-0009 source-strategy gate. Servo does not supply React semantics, JSX lowering, or Turing's trusted application-shell state and command model.

### Alternatives considered

- [Dioxus Desktop](https://dioxuslabs.com/learn/0.7/guides/platforms/desktop/) is small and productive, but its documented desktop path uses a system WebView. It would move trusted chrome into a second browser/DOM stack and does not consume this React JSX artifact unchanged.
- [Blitz](https://github.com/DioxusLabs/blitz) is an interesting native HTML/CSS renderer and Dioxus Native is closer to an interactive native path, but the project documents missing interactivity and work-in-progress CSS/runtime areas. It also changes the authoring/runtime ownership model and would add a substantial external renderer dependency.
- [Slint](https://docs.slint.dev/latest/docs/slint/) and [GPUI](https://docs.rs/gpui/latest/gpui/) are credible native UI technologies, but they require translating the Nova source to a different DSL or Rust API. That makes the supplied JSX cease to be the executable design source and adds framework-selection, adapter, and long-term replacement cost.

## Required Turing-owned work

The esbuild recommendation is only the front-end of the solution. Before the full source can drive the application, Turing must provide:

1. a pinned, reproducible build command and provenance record;
2. a React-shaped shim for the hooks actually used by Nova, backed by Turing-owned state slots and invalidation;
3. a lucide icon registry that maps named imports to bounded Turing icon components;
4. a host-factory contract that rejects arbitrary DOM, browser globals, network, file, and unbounded CSS behavior;
5. persistent event identities and typed command mapping for closures such as `onClick={() => ...}`;
6. source maps from JSX locations to component IDs, runtime nodes, semantic nodes, and command records;
7. bounded CSS/token extraction or an explicit supported style subset; and
8. deterministic fixtures for every Nova route, theme, density, motion, focus, keyboard, accessibility, and failure state.

The current `turing-js` parser remains useful as a Turing-owned semantic/runtime research path, but it should not be expanded into a second full JavaScript/JSX front-end merely to accept syntax that a mature build-time tool already handles. Its role should be decided by a future runtime task and evidence, not by the existence of this research recommendation.

## Rejected shortcuts

- Do not use React, React DOM, Node, a system WebView, or a remote browser as the trusted release renderer.
- Do not replace the Nova source with a hand-authored Rust approximation and call it source-driven rendering.
- Do not treat successful esbuild output as proof of React hook, event, accessibility, or visual parity.
- Do not claim Servo renders the Nova JSX file directly; JSX must first be compiled, and Servo would still be the wrong owner for trusted chrome under the current architecture.

## Next proof

Create a bounded development-only transform fixture that compiles the immutable Nova source with the pinned esbuild front-end and Turing factory/shims, then records the transformed module hash and rejects unsupported imports, globals, CSS constructs, and event forms. The next runtime proof must execute a small source slice through the same factory, state, event, layout, and paint path before the full file is promoted into any application launch path.

This document informs the future runtime task and ADR work. It does not select esbuild for production, approve a dependency, close the native UI or Servo gates, or claim that the browser face is implemented.
