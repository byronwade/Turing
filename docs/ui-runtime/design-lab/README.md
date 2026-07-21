# Turing Nova Design Source

Status: primary visual and layout reference; React design-lab artifact only
Owner: product design, UI runtime, accessibility, platform, performance, and developer experience
Captured: 2026-07-19

## Source of truth

[`turing-nova-design-source.jsx`](turing-nova-design-source.jsx) is the supplied Nova concept shell and is the current primary reference for Turing's browser-facing visual language and layout composition. It defines the intended browser chrome, tab strip, address field, side panels, settings, history, downloads, extensions, Shield, password vault, agent surfaces, DevTools, resource views, themes, density behavior, motion, and responsive surface relationships.

The machine [`design-source-manifest.json`](../machine/design-source-manifest.json) binds this artifact's path, SHA-256, byte length, line count, capture date, authority boundary, and surface inventory. [`validate_design_source.py`](../../../tools/validate_design_source.py) runs in the aggregate repository check.

The checked no-claim [accessibility source manifest](../../accessibility/machine/accessibility-source-manifest.json) is also a governing source-identity input for the accessibility and platform behavior represented by the design handoff. It does not make the React artifact a release UI or establish native accessibility evidence.

The [Nova Surface-to-Contract Map](surface-contract-map.md) is the implementation handoff for translating the visual source into covered, newly represented, and still-unproven toolkit-neutral component contracts.

The captured source content is preserved from the supplied attachment with repository LF line-ending normalization. The manifest records the committed bytes exactly. SHA-256:

`7A85933F7C794F29A5F0B8FBB55DD53C28C0834A3FEF0ECDC73184BB8782148B`

It contains 7,727 lines and is retained as a design reference, not as a release dependency.

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
6. retain the JSX source as the visual regression reference until the native surface is accepted through `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `PB-020`.

No React, Node, DOM, CSSOM, runtime CSS parser, or webview may enter trusted browser chrome because this source is adopted as the visual reference.

## 2026-07-21 amendment: native React-compatible runtime, owner-authorized

The extraction path above was the governing near-term plan for most of 2026-07-21. Later the same day, the owner explicitly reversed that near-term choice: `turing-js`/`turing-browser` are now being extended with a **native, from-scratch, engine-integrated implementation of React's public API surface** (hooks, `memo`, JSX-shaped component composition), built the same way every other subsystem in this repository is (turing-css is not WebKit's CSSOM; turing-layout is not Blink's layout engine) — specifically so this file executes and paints, unmodified, inside `turing-browser` itself.

This does not contradict the line above: the banned technologies are the actual external ones — the real npm `react`/`react-dom`/`lucide-react` packages, Node, another engine's DOM/CSSOM, a webview — none of which enter the engine under this plan. It is a native reimplementation of a compatible API surface, not an import of the real thing. The file itself remains permanently unedited (hash `7A85933F7C794F29A5F0B8FBB55DD53C28C0834A3FEF0ECDC73184BB8782148B`, never modified) — only the engine's own capability to execute it changes.

See the `turing-nova-source-real-scope` and `turing-app-runtime-goal` project memory records for the full decision history and the milestone ladder (static first paint before interactivity). The "Required extraction path" section above is not deleted — extraction remains the correct approach for anything the native runtime cannot yet execute, and its verification method (compare against this file rendered in real React as ground truth) is unchanged and still load-bearing.

## Current claim boundary

This artifact does not select a UI toolkit, establish a native browser shell, prove accessibility, authorize React in a release build, establish page-surface composition, or support a production, Chrome-class, performance, compatibility, or daily-driver claim.
