# Page Surface Composition Inventory - July 2026

Status: no-claim composition inventory for `PB-005`; no `UI-GATE-7`, page-surface approval, or compositor ownership decision
Owner: UI runtime, compositor, GPU, platform, accessibility, security, performance, quality, and architecture
Date: 2026-07-18

## Question

Can Turing turn the `PB-005` page-surface and compositor composition blocker into checked planning evidence without implying that renderer-produced page textures can already compose with trusted chrome?

## Conclusion

Yes, for planning only. The new [`page-surface-composition.json`](../ui-runtime/machine/page-surface-composition.json) registry and [`validate_page_surface_composition.py`](../../tools/validate_page_surface_composition.py) validator define the page-surface contract fields, composition alternatives, `UI-GATE-7` workflow matrix, failure cases, security identity boundaries, evidence blockers, and unsupported claim boundaries for `PB-005`.

This evidence moves `PB-005` from `not_started` to `partial` because the missing proof is now machine-checkable and indexed. It does not prove page-surface composition, select compositor ownership, select a toolkit, implement typed handles, approve `ADR-0016`, pass `UI-GATE-7`, or support release-path UI approval.

## Inputs

- [Blueprint 04 system architecture](../blueprint-v1/04-system-architecture.md)
- [Blueprint 05 web engine](../blueprint-v1/05-web-engine.md)
- [Blueprint 08 security and sandbox](../blueprint-v1/08-security-and-sandbox.md)
- [Blueprint 11 product UI and DevTools](../blueprint-v1/11-product-ui-devtools.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Research program](../blueprint-v1/22-research-program.md)
- [Paint, compositor, raster, and GPU architecture](../engine/05-paint-compositor-and-gpu.md)
- [Native UI Runtime book](../ui-runtime/README.md)
- [Page surface, compositor, and process integration](../ui-runtime/04-page-surface-compositor-and-process-integration.md)
- [Window Input Accessibility Spike Inventory](window-input-accessibility-spike-inventory-2026-07.md)
- [`page-surface-composition.schema.json`](../ui-runtime/machine/page-surface-composition.schema.json)
- [`page-surface-composition.json`](../ui-runtime/machine/page-surface-composition.json)
- [`validate_page_surface_composition.py`](../../tools/validate_page_surface_composition.py)

## Method

The inventory was shaped as a dependency-free machine registry with a validator that rejects:

- missing no-claim status and unsupported-claim language;
- missing source records from Blueprint, engine, UI-runtime, accessibility, readiness, task-queue, and crosswalk files;
- missing page-surface contract fields for view ID, document epoch, device generation, logical and physical size, scale factor, color space, alpha mode, damage region, synchronization primitive, frame sequence, presentation deadline, release acknowledgement, and brokered surface handle;
- missing composition alternatives for Turing-owned swapchain, toolkit external texture hook, platform child surface, and deterministic software fallback;
- missing workflow tests for resize, scale, damage, input routing, IME routing, accessibility composition, occlusion, capture, renderer crash, GPU device loss, and latency/frame pacing;
- missing failure cases for stale document epoch, stale view, stale device generation, renderer crash recovery UI, GPU-loss rebuild, toolkit failure, release-ack timeout, cross-origin surface isolation, and capture policy denial;
- missing identity boundaries for profile, view, document epoch, process, origin/site/frame, device generation, surface handle, and resource owner;
- missing evidence blockers for page-surface protocol, brokered handles, reference shell adapters, simulated renderer frames, hit-test/input/IME/accessibility routing, resize/scale/damage/occlusion/capture fixtures, crash/GPU-loss faults, latency/frame-pacing traces, and owner review with `ADR-0016`.

## Current Evidence

The checked inventory now contains:

- 14 required surface contract fields;
- 4 composition alternatives;
- 11 workflow test records;
- 9 failure and recovery cases;
- 8 security identity boundaries;
- 9 evidence blockers;
- source-record linkage to the Blueprint, engine book, UI-runtime book, accessibility records, readiness registry, task queue, and research crosswalk;
- no-claim language that blocks `UI-GATE-7`, page-surface approval, compositor ownership, toolkit selection, renderer-texture composition proof, typed-handle implementation, brokered-handle proof, resize/scale/damage proof, input/IME/accessibility routing proof, occlusion/capture proof, renderer-crash/GPU-loss proof, software fallback proof, latency/frame-pacing proof, release-path UI approval, and production claims.

`PB-005` can move to `partial` because the inventory and validator now exist. The status must not move beyond `partial` until a reference shell, simulated renderer frames, typed surface protocol, fault fixtures, latency traces, owner review, and `ADR-0016` evidence exist.

## Unsupported Conclusions

This report does not support any of these conclusions:

- renderer-produced page textures compose with trusted chrome;
- page-surface handles are implemented;
- a brokered surface handle model exists;
- compositor ownership is selected;
- a UI toolkit is selected;
- `ADR-0016` is accepted;
- `UI-GATE-7` passes;
- resize, scale, damage, input, IME, accessibility, occlusion, capture, renderer crash, or GPU device-loss behavior has been tested;
- software fallback exists;
- latency or frame pacing has been measured;
- any accessibility, performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or daily-driver claim exists.

## Remaining Proof

`PB-005` still requires:

- an executable `UI-GATE-7` page-surface prototype;
- accepted `ADR-0016` page-surface and compositor ownership decision;
- typed page-surface protocol and brokered surface-handle implementation;
- simulated renderer frame source and texture/damage stream;
- reference shell adapter evidence for the selected or owner-approved bake-off scope;
- executable resize, scale, damage, input, IME, accessibility, occlusion, capture, renderer crash, GPU device-loss, software-fallback, and latency/frame-pacing fixtures;
- stale-document, stale-view, stale-device, cross-origin, release-ack, capture-denial, and raw-handle negative tests;
- owner review from UI runtime, compositor, GPU, platform, accessibility, security, performance, quality, release operations, and architecture.

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
python3 -B tools/validate_page_surface_composition.py
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
