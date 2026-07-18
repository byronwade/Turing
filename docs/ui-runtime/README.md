# Native UI Runtime and Browser Chrome Engineering

Status: architecture research plus buildable toolkit-neutral M0 model; no UI framework adopted  
Owner: UI runtime, product, platform, accessibility, performance, security, and build engineering  
Last reviewed: 2026-07-18

This book defines a small native browser shell without Electron, Tauri, a system webview, a second browser engine, or a JavaScript runtime in trusted chrome.

## Working hypothesis

> Keep browser state, commands, identity, policy, recovery, and resource accounting in pure Rust; place a compiled native toolkit behind a narrow replaceable adapter; evaluate Slint first against Vizia and Floem or GPUI; use React only in a development design lab that never ships.

Slint is not selected. Licensing, page-surface composition, accessibility, IME, package size, memory, GPU interoperability, failure isolation, and replacement cost must pass the framework experiment before ADR-0014 can be accepted.

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

`PB-014` design-token and component-fixture planning evidence is recorded in [`component-fixture-inventory.json`](machine/component-fixture-inventory.json), checked by [`validate_ui_component_fixtures.py`](../../tools/validate_ui_component_fixtures.py), and summarized in the [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md). This is not a rendered fixture pack, toolkit selection, accessibility-readiness claim, trusted-chrome-readiness claim, or release-path UI approval.

`PB-005` page-surface/compositor planning evidence is recorded in [`page-surface-composition.json`](machine/page-surface-composition.json), checked by [`validate_page_surface_composition.py`](../../tools/validate_page_surface_composition.py), and summarized in the [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md). This is not `UI-GATE-7`, page-surface approval, compositor ownership, typed page-surface handle implementation, brokered handle proof, renderer-texture composition proof, software-fallback proof, latency/frame-pacing proof, toolkit selection, or release-path UI approval.

`PB-015` window/input/IME/accessibility/page-tree planning evidence is recorded in [`window-input-accessibility-spike.json`](../accessibility/machine/window-input-accessibility-spike.json), checked by [`validate_window_input_accessibility_spike.py`](../../tools/validate_window_input_accessibility_spike.py), and summarized in the [Window Input Accessibility Spike Inventory](../research/window-input-accessibility-spike-inventory-2026-07.md). This is not an executable reference-platform workflow matrix, manual assistive-technology coverage, page-tree proof, IME correctness proof, accessibility-readiness claim, `UI-GATE-7` or `UI-GATE-10` result, toolkit selection, or release-path UI approval.

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
- Release builds contain no Electron, Tauri, system webview, React, Node, DOM, CSSOM, or runtime HTML/CSS parser for browser chrome.
- UI code cannot decide navigation, permissions, credentials, profile authority, agent grants, Plug-in authority, or release trust.
- UI callbacks emit typed commands; trusted services revalidate identity, epoch, state, and authority.
- One selected production backend and renderer normally ship.
- Toolkit types remain behind Turing-owned state, command, surface, accessibility, and diagnostic contracts.
