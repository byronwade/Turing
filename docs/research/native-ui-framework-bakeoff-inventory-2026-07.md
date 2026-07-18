# Native UI Framework Bake-Off Inventory - July 2026

Status: no-claim framework bake-off inventory for `PB-004`; no toolkit selection or `ADR-0014` approval
Owner: UI runtime, product, accessibility, platform, performance, security, build, release operations, legal, quality, and architecture
Date: 2026-07-18

## Question

Can Turing turn the `PB-004` native UI framework selection blocker into checked planning evidence without implying that Slint, Vizia, Floem, GPUI, or any other framework is selected?

## Conclusion

Yes, for planning only. The new [`framework-bakeoff-inventory.json`](../ui-runtime/machine/framework-bakeoff-inventory.json) registry and [`validate_framework_bakeoff.py`](../../tools/validate_framework_bakeoff.py) validator define the candidate set, external source observations, required equivalent bake-off scope, evidence axes, disqualifiers, and unsupported claim boundaries for `PB-004`.

This evidence moves `PB-004` from `not_started` to `partial` because the missing framework-selection proof is now machine-checkable and indexed. It does not select a UI toolkit, accept `ADR-0014`, approve Slint, approve any license path, prove accessibility readiness, prove page-surface readiness, prove IME/keyboard behavior, prove performance or memory advantage, or approve release-path UI.

## Inputs

- [Blueprint 03 language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md)
- [Blueprint 11 product UI and DevTools](../blueprint-v1/11-product-ui-devtools.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Research program](../blueprint-v1/22-research-program.md)
- [Security policy](../security.md)
- [Security engineering book](../security-engine/README.md)
- [Native UI Runtime book](../ui-runtime/README.md)
- [Framework landscape and selection method](../ui-runtime/02-framework-landscape-and-selection-method.md)
- [Rust state, command, and adapter architecture](../ui-runtime/03-rust-state-command-and-adapter-architecture.md)
- [Page surface, compositor, and process integration](../ui-runtime/04-page-surface-compositor-and-process-integration.md)
- [Performance, memory, binary, and energy budgets](../ui-runtime/08-performance-memory-binary-and-energy-budgets.md)
- [Testing, observability, recovery, and release gates](../ui-runtime/09-testing-observability-recovery-and-release-gates.md)
- [Prototype plan and migration](../ui-runtime/10-prototype-plan-decision-record-and-migration.md)
- [Native UI framework evaluation](native-ui-framework-evaluation-2026-07.md)
- [Native UI component fixture inventory](native-ui-component-fixture-inventory-2026-07.md)
- [Page Surface Composition Inventory](page-surface-composition-inventory-2026-07.md)
- [Window Input Accessibility Spike Inventory](window-input-accessibility-spike-inventory-2026-07.md)
- [`framework-candidates.json`](../ui-runtime/machine/framework-candidates.json)
- [`framework-bakeoff-inventory.schema.json`](../ui-runtime/machine/framework-bakeoff-inventory.schema.json)
- [`framework-bakeoff-inventory.json`](../ui-runtime/machine/framework-bakeoff-inventory.json)
- [`validate_framework_bakeoff.py`](../../tools/validate_framework_bakeoff.py)

## Current Source Refresh

The 2026-07-18 refresh used current primary documentation through Context7 and official project pages:

- Slint documentation shows `.slint` compilation through `slint_build`, Winit backend access, platform abstraction, WGPU renderer integration examples, and texture/rendering hooks relevant to page-surface experiments.
- Slint licensing material still requires written Turing review because the GPLv3, royalty-free, and commercial paths have distribution and attribution implications.
- Vizia documentation shows a declarative/reactive Rust desktop GUI model with signals, events, CSS-style styling, Winit application setup, accessibility features, localization, custom drawing, and animation support.
- Floem documentation shows fine-grained reactive signals, a persistent view tree, CSS-inspired styling, virtualized large-list support, GPU-backed renderers, and CPU fallback.
- GPUI documentation remains useful as a high-density Rust UI reference from the Zed ecosystem, but extraction cost, platform coverage, accessibility, and component-specific license/provenance review remain blockers.
- Tauri documentation describes Rust plus HTML rendered in a WebView, reinforcing the release-shell exclusion of Tauri/WRY/system-webview approaches for trusted chrome.

These observations are source refreshes, not acceptance evidence.

## Method

The inventory was shaped as a dependency-free machine registry with a validator that rejects:

- missing no-claim and unsupported-boundary language;
- missing source records from Blueprint, security, UI-runtime, readiness, task-queue, and crosswalk files;
- drift between the bake-off candidate summaries and [`framework-candidates.json`](../ui-runtime/machine/framework-candidates.json);
- missing required external source observations for Slint, Slint licensing, Vizia, Floem, GPUI, and Tauri/WebView exclusion;
- missing equivalent-adapter scope for Slint, Vizia, and Floem or GPUI;
- missing shared shell tasks such as 100 tabs, Spaces, command field, page-surface hook, prompts, resource manager, IME, accessibility, contrast, localization, renderer hang, crash, GPU loss, and state restoration;
- missing evidence axes for equivalent adapters, accessibility, IME/keyboard/text, page surfaces, crash/GPU recovery, performance/memory/binary/energy, license/dependency/provenance, replacement/maintenance, and build/packaging/runtime exclusions;
- missing disqualifiers for webview/runtime dependencies, toolkit-owned authority, absent accessibility path, absent page-surface path, and license/provenance blockers;
- missing `PB-004` evidence and `TASK-000006` scope.

## Current Evidence

The checked inventory now contains:

- 9 candidate summaries matching `UIF-001` through `UIF-009`;
- 6 current external observation records;
- required adapter scope for Slint, Vizia, and Floem or GPUI;
- 8 equivalent shell-task groups and 5 shared-input requirements;
- 9 evidence axes;
- 5 disqualifiers;
- no-claim language that blocks toolkit selection, `ADR-0014`, equivalent-adapter evidence, accessibility readiness, IME/keyboard proof, page-surface approval, trusted-chrome readiness, release-path UI approval, performance/memory/energy claims, license/provenance approval, and production claims.

`PB-004` can move to `partial` because the inventory and validator now exist. The status must not move beyond `partial` until equivalent adapter runs, raw artifacts, legal/provenance review, accessibility evidence, page-surface evidence, owner review, and `ADR-0014` exist.

## Unsupported Conclusions

This report does not support any of these conclusions:

- Slint, Vizia, Floem, GPUI, or any other toolkit is selected;
- `ADR-0014` is accepted;
- any framework can ship in trusted chrome;
- Slint licensing is accepted;
- equivalent adapter evidence exists;
- accessibility, screen-reader, IME, keyboard, page-surface, renderer-hang, crash, GPU-loss, software-fallback, latency, frame-pacing, memory, binary, energy, package, dependency, license, provenance, or replacement evidence exists;
- release-path UI is approved;
- any performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or daily-driver claim exists.

## Remaining Proof

`PB-004` still requires:

- three-adapter or owner-approved reduced reference-shell bake-off with equivalent Slint, Vizia, and Floem or GPUI scope;
- raw run artifacts for the same UI model, command contract, component fixtures, page-surface fixtures, window/input/accessibility fixtures, and failure fixtures;
- `ADR-0014`;
- platform accessibility snapshots, screen-reader transcripts, manual assistive-technology notes, keyboard/focus traces, and accessibility latency samples;
- IME, dead-key, international text, selection, clipboard, localization, zoom, high contrast, forced colors, reduced motion, and appearance outputs;
- typed page-surface, brokered-handle, resize, scale, damage, input, IME, accessibility, occlusion, capture, renderer crash, GPU device loss, software fallback, latency, and frame-pacing evidence;
- cold/warm startup, binary/package, memory, allocation, wakeup, and energy evidence on the same reference hardware;
- dependency tree, license, advisory, unsafe, native, build-script, proc-macro, source-provenance, update-cadence, and maintainer-health review;
- replacement, migration, toolkit-upgrade, rollback, and owner-coverage evidence;
- package proof that trusted chrome contains no Electron, Tauri, system webview, Node, runtime React/JavaScript, runtime DOM, or runtime CSS parser.

## Affected Records

This inventory updates:

- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json) for `PB-004`;
- [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json) for `TASK-000006`;
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json) for the native-shell lane;
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Task Queue](../project-buildout/17-build-readiness-task-queue.md);
- [Documentation Readiness Evidence Matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Pre-build Readiness Gap Audit](pre-build-readiness-gap-audit-2026-07.md);
- [Research index](README.md);
- [Repository map](../repository-map.md);
- [Research log](../research-log.md);
- [Native UI Runtime book](../ui-runtime/README.md).

## Next Step

Create an owner-reviewed `TASK-000006` execution manifest for the first reference-shell adapter scaffold. The first executable slice should use the shared `turing-ui-model` snapshot and command contract, avoid toolkit-specific durable state, and produce artifacts that can be compared across all candidates.
