# Turing Nova Design Source

Status: versioned primary visual, layout, and intended component-authoring source; executable Turing-owned runtime target remains gated
Owner: product design, UI runtime, accessibility, platform, performance, and developer experience
Captured: 2026-07-19

## Source of truth

[`turing-nova-design-source.jsx`](turing-nova-design-source.jsx) is the supplied Nova concept shell and is the current primary reference for Turing's browser-facing visual language and layout composition. It defines the intended browser chrome, tab strip, address field, side panels, settings, history, downloads, extensions, Shield, password vault, agent surfaces, DevTools, resource views, themes, density behavior, motion, and responsive surface relationships.

The machine [`design-source-manifest.json`](../machine/design-source-manifest.json) binds this artifact's path, SHA-256, byte length, line count, capture date, authority boundary, and surface inventory. [`validate_design_source.py`](../../../tools/validate_design_source.py) runs in the aggregate repository check.

The checked no-claim [accessibility source manifest](../../accessibility/machine/accessibility-source-manifest.json) is also a governing source-identity input for the accessibility and platform behavior represented by the design handoff. It does not make the React artifact a release UI or establish native accessibility evidence.

The [Nova Surface-to-Contract Map](surface-contract-map.md) is the implementation handoff for translating the visual source into covered, newly represented, and still-unproven toolkit-neutral component contracts.

The captured source content is preserved from the supplied attachment with repository LF line-ending normalization. The manifest records the committed bytes exactly. SHA-256:

`C812F5545C8EF4B6FEB4E488CCA091E96787042493623B57CB7AAEE0366B50D5`

It contains 7,723 lines and 501,515 bytes. It is retained as the source artifact for the intended Turing-owned JSX build path, not as an external React release dependency.

## Authority boundaries

The Nova source is authoritative for:

- visual hierarchy, spacing, sizing, color roles, typography roles, icon placement, density, themes, motion intent, and panel composition;
- named browser-facing surfaces and their design states;
- interaction-story coverage that native fixtures must represent;
- the first visual baseline for screenshot and component-fixture review.

It is not authoritative for:

- navigation, origin, permission, credential, profile, agent, Plug-in, update, process, sandbox, or release authority;
- IPC, persistence, network access, page rendering, accessibility implementation, or security decisions;
- production toolkit selection or trusted-chrome runtime architecture.

Rust state, typed commands, native accessibility contracts, page-surface contracts, security policy, and accepted ADRs remain authoritative for behavior. A visual match does not prove native input, accessibility, security, performance, or compatibility.

## Required extraction path

Before native implementation begins, the design lab must extract the source into the shared design system described by [React Design Lab, Tokens, and Authoring Workflow](../06-react-design-lab-tokens-and-authoring-workflow.md):

1. identify semantic tokens for typography, spacing, color/state, focus/motion, iconography, density, and theme;
2. inventory each browser surface and state represented by the source;
3. bind every actionable visual state to a typed command or read-only snapshot field;
4. create native component fixtures for light, dark, high-contrast, forced-color, reduced-motion, localization, keyboard, focus, fault, and density axes;
5. compare the selected native adapter and the design lab against the same token and fixture records;
6. retain the JSX source as the versioned input and visual regression reference until the Turing-owned runtime is accepted through `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `PB-020`; any intentional source edit updates this manifest and its evidence.

No React, Node, DOM, CSSOM, runtime CSS parser, or webview may enter trusted browser chrome because this source is adopted as the visual reference.

## 2026-07-21 amendment: Turing-owned JSX runtime target

The owner-directed target is now a **Turing-owned, from-scratch JSX/component runtime** with a compatible React-shaped authoring surface where that compatibility is useful. The target is built from the repository's own typed runtime, layout, scene, accessibility, and command contracts, not from the external `react`, `react-dom`, Node, webview, or another browser engine. The design source remains the versioned visual/layout source of truth.

This target does not authorize production implementation by itself. The runtime must first prove parsing/compilation, lifecycle, state, input, accessibility, fault, resource, and performance contracts. The 2026-07-22 source revision removes the design-lab presentation frame so the Nova root is the browser viewport and adds the development engine-command adapter used by the Servo proof. The [Turing Platform Architecture](../../application-runtime/01-turing-platform-architecture.md) is the repository source for this target; no out-of-repository memory record is normative.

The "Required extraction path" section above is not deleted — extraction remains the correct approach for anything the native runtime cannot yet execute, and its verification method (compare against the design-lab source and approved fixtures) remains load-bearing.

## Current claim boundary

This artifact does not select a UI toolkit, establish a native browser shell, prove accessibility, authorize React in a release build, establish page-surface composition, or support a production, Chrome-class, performance, compatibility, or daily-driver claim.
