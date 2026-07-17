# Native UI Runtime and Browser Chrome Engineering

Status: architecture research and implementation-planning baseline; no framework has been adopted  
Owner: UI runtime, product, platform, accessibility, performance, security, and build engineering  
Last researched: 2026-07-17

This book defines how Turing can ship a small, native, high-performance browser shell without Electron, Tauri, a system webview, a second browser engine, or a JavaScript runtime in trusted browser chrome.

## Working hypothesis

The current hypothesis is:

> Keep browser state, commands, identity, policy, recovery, and resource accounting in pure Rust; place a compiled native UI toolkit behind a narrow replaceable adapter; evaluate Slint first against Vizia and Floem or GPUI; use React only in an optional design lab that never ships in the browser.

This is not a dependency decision. Slint licensing, page-surface composition, accessibility, input-method behavior, binary size, memory, GPU interoperability, failure isolation, and long-term replacement cost must pass the documented experiments before ADR-0014 can be accepted.

## Reading order

1. [Goals, invariants, and trust boundary](01-goals-trust-boundary-and-working-hypothesis.md)
2. [Framework landscape and selection method](02-framework-landscape-and-selection-method.md)
3. [Rust state, command, and adapter architecture](03-rust-state-command-and-adapter-architecture.md)
4. [Page surface, compositor, and process integration](04-page-surface-compositor-and-process-integration.md)
5. [Slint adapter, component model, and exit strategy](05-slint-adapter-component-model-and-exit-strategy.md)
6. [React design lab, tokens, and authoring workflow](06-react-design-lab-tokens-and-authoring-workflow.md)
7. [Windowing, input, IME, accessibility, and platform semantics](07-windowing-input-ime-accessibility-and-platform.md)
8. [Performance, memory, binary, and energy budgets](08-performance-memory-binary-and-energy-budgets.md)
9. [Testing, observability, recovery, and release gates](09-testing-observability-recovery-and-release-gates.md)
10. [Prototype plan, decision record, and migration](10-prototype-plan-decision-record-and-migration.md)

## Machine-readable companions

- [Framework candidates](machine/framework-candidates.json)
- [UI performance and footprint budgets](machine/ui-performance-budgets.json)
- [Pre-build readiness](../blueprint-v1/machine/pre-build-readiness.json)

## Non-negotiable rules

- Trusted browser chrome never depends on page rendering.
- Release builds contain no Electron, Tauri, operating-system webview, React runtime, Node runtime, DOM, CSSOM, or runtime HTML/CSS parser for browser chrome.
- The UI cannot decide navigation, permissions, credential use, profile authority, agent grants, Plug-in authority, or release security policy.
- UI callbacks emit typed commands; trusted Rust services revalidate identity, epoch, state, and authority.
- Only one selected production backend and renderer are compiled into a normal package unless a measured fallback requirement justifies more.
- The UI toolkit is replaceable behind Turing-owned state, command, platform, surface, accessibility, and diagnostic contracts.

## Primary evidence

The dated [native UI framework evaluation](../research/native-ui-framework-evaluation-2026-07.md) records the current framework evidence. The [pre-build readiness audit](../research/pre-build-readiness-gap-audit-2026-07.md) records what must still be resolved before implementation expands beyond controlled spikes.
