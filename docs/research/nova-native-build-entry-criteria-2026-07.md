# Nova Native Build Entry Criteria - July 2026

Status: no-claim design-to-native-build handoff; Nova is the visual/layout reference, not a trusted runtime or implementation approval
Owner: product design, UI runtime, accessibility, platform, performance, security, quality, and architecture
Research date: 2026-07-19
Related gates: `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, `PB-020`
Related ADRs: `ADR-0013`, `ADR-0014`, `ADR-0016`

## Purpose

The supplied [Turing Nova design source](../ui-runtime/design-lab/README.md) is the primary visual and layout reference for the browser face. This packet defines what must happen before a native implementation may use it as an input. It prevents the React/JSX artifact from becoming trusted browser chrome, a behavior source of truth, or an implied toolkit selection.

Nova owns visual language and composition. Rust state, typed commands, identity and epoch rules, accessibility contracts, page-surface contracts, security policy, persistence, and accepted ADRs own behavior and authority.

## Source identity and authority

The committed artifact is [`turing-nova-design-source.jsx`](../ui-runtime/design-lab/turing-nova-design-source.jsx), protected by [`design-source-manifest.json`](../ui-runtime/machine/design-source-manifest.json) and [`validate_design_source.py`](../../tools/validate_design_source.py). The current manifest hash, byte count, line count, capture date, and surface inventory are authoritative for the captured source bytes.

The source may be used for:

- visual hierarchy, spacing, sizing, color roles, typography, icon placement, density, themes, motion intent, and responsive composition;
- named browser-facing surfaces and design states;
- interaction-story coverage for toolkit-neutral fixtures;
- visual regression and screenshot/component review after the native fixture contract exists.

The surface inventory now has an explicit fixture mapping for the new-tab/web-page shell through `UI-COMPONENT-NEW-TAB-PAGE-SHELL`, and the [surface-contract map](../ui-runtime/design-lab/surface-contract-map.md) reconciles all named Nova function components, including shared primitives and nested settings/popover/message sections, to parent contracts. This mapping covers the chrome/page boundary, typed page-surface generations, loading/error/recovery states, focus transfer, and page-tree accessibility work; it does not make the renderer or page surface trusted.

The source may not provide:

- navigation, origin, permission, credential, profile, agent, Plug-in, update, process, sandbox, network, storage, IPC, or release authority;
- page rendering, accessibility implementation, persistence, or security policy;
- a production toolkit, React runtime, DOM, CSSOM, runtime CSS parser, webview, or JavaScript runtime in trusted chrome.

## Native extraction contract

Before native implementation begins, the maintainer must produce versioned, reviewable artifacts from the Nova source:

1. **Semantic design tokens:** typography, spacing, color/state, focus, motion, iconography, density, and theme tokens with source-region references and contrast/forced-color behavior.
2. **Surface inventory:** every Nova surface, state, breakpoint, density, theme, error, loading, empty, recovery, and permission state mapped to a stable component ID.
3. **State and command mapping:** each actionable state mapped to a read-only Rust snapshot field or typed command with validation, identity, epoch, deadline, cancellation, confirmation, rejection, and diagnostic behavior.
4. **Authority map:** each surface identifies its owning service, profile/site/frame/document identity, untrusted inputs, capability boundary, persistence class, and prohibited toolkit/page authority.
5. **Native fixture contract:** each component covers keyboard, focus, IME, screen reader, high contrast, forced color, reduced motion, localization, density, fault, recovery, stale state, and text-fit behavior.
6. **Page-surface contract:** page content is composed through typed brokered handles with origin/site, process, document, device, and generation identity; Nova chrome cannot treat a renderer texture or page event as trusted state.
7. **Visual comparison package:** the captured Nova source, extracted tokens, native fixture outputs, viewport/DPR/theme/density settings, screenshots or semantic snapshots, and difference disposition are retained together.

Extraction must preserve source-region traceability. A token or component that cannot be mapped back to the captured source and forward to a behavioral or fixture contract remains a design-lab hypothesis.

## Build-entry gates

Nova-driven native work may enter an approved implementation task only when all applicable conditions are true:

- the exact Nova manifest identity is validated and the source is unchanged or the change has a reviewed source update;
- `ADR-0013` establishes toolkit-neutral adapter/state/command authority;
- `ADR-0014` records an equivalent framework/adapter evaluation with dependency, license, provenance, build, runtime, memory, startup, accessibility, input, fault, replacement, and rollback evidence;
- `ADR-0016` establishes page-surface/compositor ownership and typed handle identity;
- `UI-GATE-7` page-surface and compositor evidence exists where the native shell composes renderer output;
- `UI-GATE-10` accessibility evidence includes platform tree snapshots, manual assistive-technology workflows, focus, keyboard, IME, live-region, page/chrome composition, and unsupported cases;
- component fixtures cover the Nova surface inventory and are rendered or semantically exercised through the selected native adapter;
- the reference platform, toolchain/fresh-host, IPC, sandbox, profile/session, benchmark, release, and ownership prerequisites required by the task are accepted or held by explicit time-bounded exceptions;
- an approved immutable task manifest names the owner, independent reviewer, allowed paths, evidence bundle, rollback, expiry, dependency digest, and prohibited claims.

Nova visual matching alone cannot satisfy any of these gates.

## Review and rejection rules

Reject the native build handoff when it:

- bundles or executes the JSX source in trusted chrome;
- treats a screenshot, design token, visual diff, or React preview as proof of behavior, accessibility, security, page-surface correctness, or performance;
- lets a toolkit callback, page event, renderer texture, extension, DevTools surface, or agent observation mint authority;
- omits error, loading, empty, recovery, high-contrast, forced-color, reduced-motion, localization, keyboard, IME, screen-reader, or text-fit states;
- changes Nova hierarchy or layout without a source-region trace, token update, fixture update, and review record;
- selects a toolkit or compositor from visual similarity without equivalent adapter, dependency, provenance, accessibility, fault, and performance evidence;
- accepts page content or native UI as one undifferentiated trust domain;
- claims a usable browser, Chrome-class capability, accessibility readiness, security, compatibility, performance, production, or release readiness from the design source.

## Current status and next proof

The Nova source and surface-contract map are validated design references. No toolkit is selected, no native adapter is accepted, no page-surface/compositor decision is accepted, and no UI gate is promoted. The next controlled proof is a reviewed extraction manifest and toolkit-neutral component-fixture package after the relevant owner-approved task and predecessor gates exist.

This packet makes the future design-to-build handoff explicit. It does not authorize native implementation, alter the trusted UI rule, change the 90% contained-M0 documentation organization or 0% full-build closure measures, or supersede the UI runtime book and accepted ADRs.

## Canonical related records

- [Turing Nova Design Source](../ui-runtime/design-lab/README.md)
- [Nova Surface-to-Contract Map](../ui-runtime/design-lab/surface-contract-map.md)
- [UI Runtime](../ui-runtime/README.md)
- [React Design Lab, Tokens, and Authoring Workflow](../ui-runtime/06-react-design-lab-tokens-and-authoring-workflow.md)
- [Native UI and Accessibility Closure Preparation](native-ui-and-accessibility-closure-preparation-2026-07.md)
- [Native UI component fixture inventory](native-ui-component-fixture-inventory-2026-07.md)
- [Build-readiness progress snapshot](../project-buildout/22-build-readiness-progress-snapshot.md)
