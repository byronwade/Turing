# Native UI and Accessibility Closure Preparation - July 2026

Status: no-claim execution and review route for `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006`; no toolkit, native adapter, page-surface path, accessibility readiness, or release-path UI has been approved
Owner: UI runtime, accessibility, platform, product, security, performance, quality, architecture, and release operations
Research date: 2026-07-19

## Question

What evidence order can connect toolkit selection, toolkit-neutral state/command contracts, page-surface composition, component fixtures, input/IME, and assistive technology without allowing a toolkit or page renderer to own browser authority?

## Current boundary

The repository has no-claim inventories for the adapter contract, framework bake-off, component fixtures, page-surface composition, and window/input/accessibility workflows, plus native UI readiness-review templates and machine registries. They define missing evidence and claim boundaries. They do not select Slint, Vizia, Floem, GPUI, or another toolkit; accept `ADR-0013`, `ADR-0014`, or `ADR-0016`; prove a native adapter; prove page-surface composition; satisfy `UI-GATE-7` or `UI-GATE-10`; or establish accessibility, trusted-chrome, or release-path UI readiness.

## Primary accessibility-source observations

The following official platform sources were retrieved or checked on 2026-07-19 and are used to define the evidence boundary:

| Platform source | Observation | Required UI/accessibility evidence consequence |
|---|---|---|
| [Windows accessibility guidance](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/) and [UI Automation](https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/ui-automation-overview) | Windows accessibility is exposed through platform semantic/control patterns and UI Automation clients; a browser's internal semantic model is not itself a Windows accessibility result. | Record Windows version, UI Automation API/client details, tree snapshots, control patterns, focus and event behavior, and the exact Narrator/NVDA version and configuration used. |
| [Apple accessibility documentation](https://developer.apple.com/documentation/accessibility) | macOS accessibility is a platform API and assistive-technology integration surface; VoiceOver interaction must be evaluated against the exposed platform tree and actions. | Record macOS version, accessibility API/runtime details, VoiceOver version/configuration, tree/action snapshots, focus/live-region behavior, and unsupported cases. |
| [AT-SPI 2 API documentation](https://docs.gtk.org/atspi2/) | AT-SPI exposes accessible objects, actions, components, documents, text, selections, states, events, and runtime version information; event timing and object relationships are part of the observable contract. | Record Linux distribution/session, AT-SPI runtime version, desktop/accessibility bus state, Orca version/configuration, object tree, relations, states, events, text/selection results, and timeout behavior. |

These are source and method observations, not accessibility results. A semantic model, screenshot, automated checker, or one platform's tree cannot be generalized into cross-platform accessibility readiness. Every future packet must preserve platform/API/assistive-technology identity, manual transcript or action record, tree snapshots, event timing, unsupported cases, and the complete workflow denominator.

The checked [accessibility-source manifest](../accessibility/machine/accessibility-source-manifest.json), validated by [`validate_accessibility_sources.py`](../../tools/validate_accessibility_sources.py), records these platform source identities and evidence consequences. It is a no-claim source record only; it does not provide accessibility workflow execution, screen-reader coverage, IME correctness, page-tree proof, or UI-gate approval.

The trusted shell remains toolkit-replaceable. A toolkit callback may propose a typed command or render a declared surface, but it cannot own navigation, profile, permission, credential, agent, Plug-in, persistence, update, process, or release authority. Page content and renderer output remain untrusted inputs to the brokered composition path.

## Required evidence order

1. **Freeze toolkit-neutral contracts.** Define versioned state snapshots, commands, identities, epochs, deadlines, cancellation, confirmation, rejection, diagnostics, surface handles, accessibility nodes, focus ownership, and stale-update behavior against `turing-ui-model`. Commands are validated by the service authority, not trusted because a toolkit emitted them.
2. **Run equivalent reference-shell adapters.** Use the same model, command set, component fixtures, page-surface fixtures, input workflows, accessibility scenarios, fault cases, and artifact schema for each candidate or an owner-approved reduced scope. Record dependency/source/license/provenance/build/runtime exclusions and replacement/rollback implications.
3. **Prove authority separation.** Negative tests must show toolkit callbacks, page content, accessibility events, extensions, DevTools, agent input, and renderer-produced textures cannot mint capabilities, navigate profiles, alter permissions, access credentials, persist state, select privileged surfaces, or bypass confirmation.
4. **Exercise page-surface composition.** Test typed/brokered surface handles, document/device generations, resize, scale, damage, input, IME, accessibility, occlusion, capture, renderer crash, GPU loss, stale handles, and deterministic software fallback. Bind every surface to document, origin/site, process epoch, profile, and frame identity.
5. **Render component fixtures.** Cover browser chrome, tabs, Spaces, command field, permission prompts, agent confirmations, resource manager, settings, and recovery UI across keyboard/focus, screen reader, forced color, high contrast, reduced motion, density, localization, error, and authority-boundary states.
6. **Run reference-platform workflows.** Capture windowing, input, IME/dead keys/international text, selection, clipboard, drag/drop, zoom, localization, high contrast, forced colors, reduced motion, page-tree composition, crash recovery, renderer hang, and GPU-loss behavior on each declared platform.
7. **Run manual assistive-technology review.** Preserve transcripts and platform tree snapshots for the supported screen readers and accessibility APIs. Record names, roles, states, focus, live regions, announcements, keyboard alternatives, page/chrome subtree composition, and known unsupported cases.
8. **Measure behavior and recovery.** Retain startup, memory, binary, allocation, wakeup, latency/frame-pacing, energy, input/focus/live-region/tree-update, crash, renderer-hang, GPU-loss, and recovery traces on declared hardware. Measurements are evidence for the reviewed fixture/workflow scope, not toolkit leadership claims.
9. **Submit one cross-lane readiness review.** Replace the no-claim native UI template with exact source/toolkit/dependency identities, rendered artifacts, workflow transcripts, accessibility snapshots, fault evidence, performance traces, negative authority tests, reviewer identities, waivers/expiry, and explicit dispositions for each `PB-*`, ADR, and UI gate.

## Evidence matrix

| Axis | Minimum proof | Rejection condition |
|---|---|---|
| Contract authority | Versioned state/command/surface/accessibility/diagnostic contracts tied to the model and service validation | Toolkit callback or page event is treated as authoritative |
| Toolkit equivalence | Same fixtures, workflows, failure cases, artifacts, dependency/provenance records, and replacement plan across candidates | Different scope or missing candidate is presented as a bake-off result |
| Trusted-chrome authority | Negative tests for navigation, profile, permission, credential, agent, Plug-in, persistence, update, process, and release authority | Toolkit, renderer, page, extension, DevTools, or agent input widens authority |
| Page surface | Brokered typed handles with identity generations, resize/scale/damage/input/IME/accessibility/occlusion/capture/fault evidence | Texture or surface is accepted without origin/site/process/document identity |
| Accessibility | Platform tree snapshots, manual screen-reader transcripts, focus/keyboard/IME/live-region evidence, unsupported cases | A semantic model or automated validator is treated as platform accessibility proof |
| Fault/recovery | Renderer hang, crash, GPU loss, stale handles, recovery, software fallback, and data-preservation results | Failure is swallowed, fallback changes authority, or recovery loses identity |
| Performance/resource | Same hardware controls, startup/memory/binary/latency/frame/energy traces, and failure denominator | One toolkit run or synthetic fixture becomes a leadership claim |
| Review integrity | Exact source/dependency/toolkit identity, artifact hashes, named reviewers, waivers, expiry, and synchronized ADR/gate status | Template, screenshot, or placeholder reviewer is treated as approval |

## Gate and claim effect

The native UI gates remain partial: `PB-003`, `PB-004`, `PB-005`, `PB-014`, and `PB-015`. `TASK-000006` remains proposed-only. No inventory, framework observation, model test, rendered mock, or readiness template selects a toolkit, accepts an ADR, satisfies `UI-GATE-7`/`UI-GATE-10`, proves accessibility or trusted-chrome readiness, or supports release-path, performance, Chrome-class, production, or implementation claims.

## PB-020 closure dependency

Any future native UI readiness decision must be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and the [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md) route. An accepted `ADR-0013`, `ADR-0014`, or `ADR-0016`, a passed `UI-GATE-7` or `UI-GATE-10`, a reviewed adapter, or a platform accessibility result cannot independently close `PB-020`, authorize broad implementation, establish release-path UI support, or support accessibility, performance, Chrome-class, production, or daily-driver claims. The final closure record must preserve the native UI evidence, named owner and independent reviewer, unresolved limitations, exceptions and expiry, and synchronized readiness, task, ADR, risk, support, and release records.

This route is compatible with the [Toolkit-Neutral UI Adapter Contract Inventory](toolkit-neutral-ui-adapter-contract-inventory-2026-07.md), [Native UI Framework Bake-Off Inventory](native-ui-framework-bakeoff-inventory-2026-07.md), [Native UI Component Fixture Inventory](native-ui-component-fixture-inventory-2026-07.md), [Page Surface Composition Inventory](page-surface-composition-inventory-2026-07.md), [Window Input Accessibility Spike Inventory](window-input-accessibility-spike-inventory-2026-07.md), and specified [TASK-000006 manifest](../agent-execution/machine/tasks/TASK-000006.json). Those sources remain authoritative for their respective scopes.

The [Native UI and Accessibility Workflow Examples](native-ui-accessibility-workflow-examples-2026-07.md) supplies a fictitious address-field/page-surface workflow record spanning authority, identity, IME, accessibility trees, assistive technology, faults, and latency. It is a handoff example only and does not satisfy any UI-gate or readiness requirement.

## Next controlled action

Prepare a reviewed immutable `TASK-000006` manifest for one toolkit-neutral reference-shell adapter slice using the shared model, command contract, component fixtures, and one page-surface/accessibility workflow. Do not select a release toolkit or generalize a platform result until the cross-lane evidence and owner review exist.
