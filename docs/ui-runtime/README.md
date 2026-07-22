# Native UI Runtime and Browser Chrome Engineering

Status: architecture research plus buildable toolkit-neutral M0 model; Turing-owned JSX runtime is the target and no release UI framework is adopted
Owner: UI runtime, product, platform, accessibility, performance, security, and build engineering  
Last reviewed: 2026-07-19

This book defines the current native browser-shell boundary and the migration to the Turing-owned JSX application runtime. The current M0 shell contains no external React, Node, system webview, second browser engine, or JavaScript runtime in trusted chrome. The target runtime may accept JSX-shaped authoring and a compatible component API only after compilation to bounded native IR and the relevant security, accessibility, platform, and production gates.

The full target boundary is [`Turing Platform Architecture`](../application-runtime/01-turing-platform-architecture.md). It is the source for the one-visual-composition-system rule across the browser and future Nova applications.

The current visual, layout, and intended component-authoring source of truth is the [Turing Nova design source](design-lab/README.md), backed by the checked [`design-source-manifest.json`](machine/design-source-manifest.json) and [`validate_design_source.py`](../../tools/validate_design_source.py). It is versioned canonical input: intentional changes require a manifest refresh, source-fidelity review, and updated evidence in the same change. The current low-maintenance compiler recommendation is recorded in the [JSX Runtime Compiler Selection study](../research/jsx-runtime-compiler-selection-2026-07.md); that recommendation is not a production dependency decision.

The [Nova Native Build Entry Criteria](../research/nova-native-build-entry-criteria-2026-07.md) is the canonical future handoff for extracting tokens, surface/state/command mappings, authority boundaries, native fixtures, page-surface contracts, and review evidence before Nova can inform authorized native implementation.

## Working hypothesis

> Keep browser state, commands, identity, policy, recovery, and resource accounting in pure Rust; compile JSX-shaped authoring into a Turing-owned component runtime behind replaceable platform adapters; keep external React, Node, webviews, page DOM, and runtime CSS parsers out of the release path.

No native UI framework or JSX compiler is selected. The current research recommendation is to use esbuild only as a pinned build-time JSX front-end and keep the runtime renderer Turing-owned. Licensing, page-surface composition, accessibility, IME, package size, memory, GPU interoperability, failure isolation, and replacement cost remain evidence gates before any ADR is accepted.

## Implemented M0 boundary

`crates/turing-ui-model` now provides the first buildable toolkit-neutral contract:

- immutable `ShellSnapshot`;
- typed window, profile, Space, tab, and view identities;
- explicit tab lifecycle;
- typed shell commands;
- snapshot validation;
- no toolkit, platform, GPU, page, credential, Plug-in, or agent types.

`apps/turing-shell` exercises the model through a command-line self-test. It is not a native UI and must not be presented as one.

The component boundary is recorded in [`workspace-components.json`](../blueprint-v1/machine/workspace-components.json).

`PB-003` toolkit-neutral adapter-contract planning evidence is recorded in [`adapter-contract-inventory.json`](machine/adapter-contract-inventory.json), checked by [`validate_ui_adapter_contract.py`](../../tools/validate_ui_adapter_contract.py), and summarized in the [Toolkit-Neutral UI Adapter Contract Inventory](../research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md). This is not `ADR-0013`, a native adapter prototype, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production approval, or implementation proof.

`PB-004` framework-selection planning evidence is recorded in [`framework-bakeoff-inventory.json`](machine/framework-bakeoff-inventory.json), checked by [`validate_framework_bakeoff.py`](../../tools/validate_framework_bakeoff.py), and summarized in the [Native UI Framework Bake-Off Inventory](../research/native-ui-framework-bakeoff-inventory-2026-07.md). This is not `ADR-0014`, toolkit selection, equivalent adapter evidence, accessibility readiness, IME or keyboard proof, page-surface approval, trusted-chrome readiness, release-path UI approval, performance/memory/energy proof, license/provenance approval, or production approval.

`PB-014` design-token and component-fixture planning evidence is recorded in [`component-fixture-inventory.json`](machine/component-fixture-inventory.json), checked by [`validate_ui_component_fixtures.py`](../../tools/validate_ui_component_fixtures.py), and summarized in the [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md). The inventory now covers ten core shell surfaces, including the new-tab/web-page shell, plus six Nova-specific product surfaces; it remains a no-claim planning record, not a rendered fixture pack, toolkit selection, accessibility-readiness claim, trusted-chrome-readiness claim, or release-path UI approval.

`PB-005` page-surface/compositor planning evidence is recorded in [`page-surface-composition.json`](machine/page-surface-composition.json), checked by [`validate_page_surface_composition.py`](../../tools/validate_page_surface_composition.py), and summarized in the [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md). This is not `UI-GATE-7`, page-surface approval, compositor ownership, typed page-surface handle implementation, brokered handle proof, renderer-texture composition proof, software-fallback proof, latency/frame-pacing proof, toolkit selection, or release-path UI approval.

`PB-015` window/input/IME/accessibility/page-tree planning evidence is recorded in [`window-input-accessibility-spike.json`](../accessibility/machine/window-input-accessibility-spike.json), checked by [`validate_window_input_accessibility_spike.py`](../../tools/validate_window_input_accessibility_spike.py), and summarized in the [Window Input Accessibility Spike Inventory](../research/window-input-accessibility-spike-inventory-2026-07.md). This is not an executable reference-platform workflow matrix, manual assistive-technology coverage, page-tree proof, IME correctness proof, accessibility-readiness claim, `UI-GATE-7` or `UI-GATE-10` result, toolkit selection, or release-path UI approval.

Native UI and accessibility decisions remain subject to the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and `PB-020` closure. Toolkit-neutral contracts, adapter evidence, page-surface evidence, accessibility evidence, and accepted UI ADRs are lane evidence only; none independently grants broad implementation, trusted-chrome release, production, performance, or Chrome-class authority.

## Reading order

1. [Goals, invariants, and trust boundary](01-goals-trust-boundary-and-working-hypothesis.md)
2. [Framework landscape and selection](02-framework-landscape-and-selection-method.md)
3. [Rust state, command, and adapter architecture](03-rust-state-command-and-adapter-architecture.md)
4. [Page surface, compositor, and process integration](04-page-surface-compositor-and-process-integration.md)
5. [Slint adapter and exit strategy](05-slint-adapter-component-model-and-exit-strategy.md)
6. [React design lab](06-react-design-lab-tokens-and-authoring-workflow.md)
7. [Windowing, input, IME, and accessibility](07-windowing-input-ime-accessibility-and-platform.md)
8. [Performance and footprint budgets](08-performance-memory-binary-and-energy-budgets.md)
9. [Testing, observability, and recovery](09-testing-observability-recovery-and-release-gates.md)
10. [Prototype plan and migration](10-prototype-plan-decision-record-and-migration.md)

## Non-negotiable rules

- Trusted chrome never depends on page rendering.
- Release builds contain no Electron, Tauri, system webview, external React/React DOM, Node, page DOM, CSSOM, or runtime HTML/CSS parser for browser chrome. A Turing-owned JSX compiler/runtime remains a gated target, not a current M0 capability.
- UI code cannot decide navigation, permissions, credentials, profile authority, agent grants, Plug-in authority, or release trust.
- UI callbacks emit typed commands; trusted services revalidate identity, epoch, state, and authority.
- One selected production backend and renderer normally ship.
- Toolkit types remain behind Turing-owned state, command, surface, accessibility, and diagnostic contracts.
- Browser chrome, DevTools, and future desktop application surfaces use the same Turing component/runtime IR; no app-specific visual renderer is introduced.
