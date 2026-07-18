# Window Input Accessibility Spike Inventory - July 2026

Status: no-claim workflow inventory for `PB-015`; no accessibility readiness, page-tree proof, or toolkit selection
Owner: accessibility architecture, platform, UI runtime, product, quality, security, and performance
Date: 2026-07-18

## Question

Can Turing turn the `PB-015` window/input/IME/accessibility/page-tree spike into checked planning evidence without implying that a native browser UI, accessibility bridge, or page-surface composition path exists?

## Conclusion

Yes, for planning only. The new [`window-input-accessibility-spike.json`](../accessibility/machine/window-input-accessibility-spike.json) registry and [`validate_window_input_accessibility_spike.py`](../../tools/validate_window_input_accessibility_spike.py) validator define the reference workflow axes, core shell workflows, platform assistive-technology matrix, missing evidence blockers, and no-claim boundaries for `PB-015`.

This evidence moves `PB-015` from `not_started` to `partial` because the project now has a checked workflow inventory. It does not prove accessibility readiness, screen-reader coverage, IME correctness, page-tree composition, crash or GPU-loss behavior, UI toolkit selection, trusted-chrome readiness, or release-path UI approval.

## Inputs

- [Blueprint 11 product UI and DevTools](../blueprint-v1/11-product-ui-devtools.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Research program](../blueprint-v1/22-research-program.md)
- [Accessibility Engineering book](../accessibility/README.md)
- [Platform book](../platform/README.md)
- [Native UI Runtime book](../ui-runtime/README.md)
- [Native UI component fixture inventory](native-ui-component-fixture-inventory-2026-07.md)
- [`window-input-accessibility-spike.schema.json`](../accessibility/machine/window-input-accessibility-spike.schema.json)
- [`window-input-accessibility-spike.json`](../accessibility/machine/window-input-accessibility-spike.json)
- [`validate_window_input_accessibility_spike.py`](../../tools/validate_window_input_accessibility_spike.py)

## Method

The inventory was shaped as a dependency-free machine registry with a validator that rejects:

- missing no-claim status and unsupported-claim language;
- missing source records from the owning Blueprint, accessibility, platform, UI-runtime, readiness, task-queue, and crosswalk files;
- missing workflow axes for windowing, input, IME, accessibility tree, page-tree composition, clipboard, drag/drop, localization, zoom, high contrast, forced colors, reduced motion, crash recovery, renderer hang, and GPU loss;
- missing core workflows for browser window lifecycle, tab strip/groups, Spaces side panel, address/command field, permission/agent confirmation, page-surface composition, DevTools docking, resource manager, and settings/recovery;
- missing platform assistive-technology coverage for macOS VoiceOver through AX, Windows Narrator/NVDA through UI Automation, and Linux Orca through AT-SPI;
- missing evidence blockers for reference platform, isolated adapter runner, rendered reference shell, page-surface stub, accessibility tree snapshots, manual assistive-technology matrix, input/IME harnesses, clipboard/drag-drop security fixtures, localization/zoom/appearance fixtures, crash/hang/GPU-loss fault fixtures, latency/resource capture, and owner review.

## Current Evidence

The checked inventory now contains:

- 15 required workflow axes;
- 9 required core shell workflows;
- 3 platform assistive-technology rows;
- 12 evidence blockers;
- source-record linkage to the Blueprint, accessibility book, platform book, UI-runtime book, readiness registry, task queue, and research crosswalk;
- no-claim language that blocks accessibility-readiness, screen-reader, manual assistive-technology, page-tree, IME, keyboard, clipboard/drag-drop, localization, zoom/contrast/motion, crash/recovery, UI gate, release-path, production, and toolkit-selection claims.

`PB-015` can move to `partial` because the inventory and validator now exist. The status must not move beyond `partial` until executable reference-platform workflows, manual assistive-technology transcripts, page-tree composition evidence, latency/resource traces, fault injection, and owner review exist.

## Unsupported Conclusions

This report does not support any of these conclusions:

- a native browser UI exists;
- a UI toolkit is selected;
- browser chrome is trusted or release-ready;
- accessibility readiness exists;
- screen-reader coverage exists;
- VoiceOver, Narrator, NVDA, Orca, AX, UI Automation, or AT-SPI behavior has been tested;
- IME, keyboard, clipboard, drag/drop, localization, zoom, high-contrast, forced-colors, or reduced-motion behavior has been tested;
- browser chrome and page trees compose correctly;
- renderer hang, crash recovery, or GPU-loss behavior has been tested;
- `UI-GATE-7` or `UI-GATE-10` has evidence;
- any performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or daily-driver claim exists.

## Remaining Proof

`PB-015` still requires:

- a reference-platform workflow matrix for windowing, input, IME, accessibility, page-tree composition, clipboard, drag/drop, localization, zoom, high contrast, reduced motion, crash recovery, renderer hang, and GPU-loss behavior;
- manual assistive-technology coverage for supported screen readers before accessibility readiness;
- platform accessibility tree snapshots and composed chrome/page subtree diffs;
- IME, keyboard, clipboard, drag/drop, localization, zoom, high-contrast, forced-colors, and reduced-motion fixture outputs;
- renderer hang, crash recovery, and GPU-loss fault-injection evidence;
- p50, p95, and p99 latency/resource traces for input, focus, live-region, and tree-update events;
- owner review from accessibility, platform, UI runtime, product, security, performance, quality, and release operations.

## Affected Records

- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json)
- [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json)
- [Pre-build Readiness Gap Audit](pre-build-readiness-gap-audit-2026-07.md)
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md)
- [Build Readiness Task Queue](../project-buildout/17-build-readiness-task-queue.md)
- [Documentation Readiness Evidence Matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md)
- [Research index](README.md)

## Validation

Required commands:

```bash
python3 -B tools/validate_window_input_accessibility_spike.py
python3 -B tools/validate_blueprint.py
```

Aggregate handoff validation remains:

```bash
sh tools/check.sh
```

On Windows PowerShell:

```powershell
.\tools\check.ps1
```
