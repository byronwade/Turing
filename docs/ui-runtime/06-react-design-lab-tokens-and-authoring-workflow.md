# React Design Lab, Tokens, and Authoring Workflow

Status: development-tool proposal  
Owner: product design, UI runtime, accessibility, localization, and developer experience

## Boundary

React may be used in a separate design and documentation application. React, React Compiler output, Node, a DOM, CSSOM, or a webview is not bundled into trusted browser chrome.

React Compiler optimizes React applications through build-time memoization; it does not transform React components into native Rust widgets or eliminate the React runtime. TypeScript supports implementation-specific JSX transforms, but a complete TSX-to-native compiler would itself require a language, semantics, diagnostics, source maps, hot reload, accessibility, code generation, and compatibility program.

## Shared source of truth

Use versioned design data:

```text
design/
├── tokens.json
├── components.json
├── commands.json
├── icons/
├── localization/
└── fixtures/
```

Generate Rust constants, selected-toolkit declarations, optional React CSS variables, documentation tables, contrast checks, screenshots, and fixture data from this source.

The current primary visual/layout reference is the captured [Turing Nova design source](design-lab/README.md) and its verbatim [JSX artifact](design-lab/turing-nova-design-source.jsx). Until its visual contracts are extracted into the shared design data, changes to browser-facing hierarchy, panel composition, spacing, typography, themes, density, motion intent, or named surface states must be reconciled against that artifact. This elevates the supplied concept shell to the design reference without making React the product runtime or behavioral source of truth.

`tools/validate_design_source.py` verifies that `design/tokens.json` names
this source and carries its current SHA-256. A source revision therefore
cannot pass repository validation while leaving shared token provenance on an
older artifact; token values still require an intentional extraction review.

## Design lab capabilities

- component gallery and state fixtures;
- light, dark, high-contrast, forced-color, reduced-motion, density, and RTL previews;
- token editing and change review;
- keyboard and focus-path simulation;
- accessible-name and relationship preview;
- screenshot and visual-diff generation;
- product-flow prototypes that emit no browser authority.

## Anti-drift rules

- No business or security logic exists only in React.
- Native components and the design lab consume the same tokens and named states.
- Visual similarity is not proof of native accessibility, input, timing, or platform correctness.
- Every stable component fixture must run in the native test kit.
- The design lab is separately packaged and never a release dependency.
- The Nova JSX artifact is versioned source input and a visual regression reference; external React is never bundled into trusted browser chrome. Intentional edits refresh the source manifest and require source-fidelity evidence.

## Turing-owned JSX compilation target

The current research recommendation is to preserve this JSX artifact as the authoring source and use a pinned build-time JSX front-end such as esbuild to lower syntax into Turing-owned factories. The compiler front-end is not the runtime: the release path must still provide bounded component IR, state slots, lifecycle, typed commands, accessibility semantics, source maps, and deterministic invalidation.

The full Nova file currently uses React-shaped hooks, icon imports, browser-like values, and event closures. Those require an explicit Turing compatibility shim and capability audit. They must not be silently replaced by a native approximation or by importing the external React implementation.
