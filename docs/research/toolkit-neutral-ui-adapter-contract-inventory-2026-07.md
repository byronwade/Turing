# Toolkit-Neutral UI Adapter Contract Inventory - July 2026

Status: no-claim contract inventory for `PB-003`; no `ADR-0013`, native adapter prototype, toolkit selection, or release-path UI approval
Owner: UI runtime, accessibility, product, security, platform, quality, architecture, and release operations
Date: 2026-07-18

## Question

Can `PB-003` move from a buildable M0 UI model and prose architecture into checked adapter-contract planning evidence without implying a native UI implementation?

## Conclusion

Yes, for planning only. The new [`adapter-contract-inventory.json`](../ui-runtime/machine/adapter-contract-inventory.json) registry and [`validate_ui_adapter_contract.py`](../../tools/validate_ui_adapter_contract.py) validator define the toolkit-neutral state, command, surface, accessibility, diagnostic, and adapter contract areas, the current M0 model invariants, denied adapter authority classes, required evidence, and unsupported claim boundaries for `PB-003`.

This evidence keeps `PB-003` at `partial` because the missing contract proof is now machine-checkable and indexed. It does not accept `ADR-0013`, implement a native adapter, select a UI toolkit, prove trusted-chrome readiness, prove accessibility readiness, approve page-surface composition, or approve release-path UI.

## Inputs

- [`crates/turing-ui-model`](../../crates/turing-ui-model/src/lib.rs)
- [Native UI Runtime book](../ui-runtime/README.md)
- [Rust state, command, and adapter architecture](../ui-runtime/03-rust-state-command-and-adapter-architecture.md)
- [Page surface, compositor, and process integration](../ui-runtime/04-page-surface-compositor-and-process-integration.md)
- [Windowing, input, IME, and accessibility](../ui-runtime/07-windowing-input-ime-accessibility-and-platform.md)
- [Testing, observability, recovery, and release gates](../ui-runtime/09-testing-observability-recovery-and-release-gates.md)
- [Product UI and DevTools Blueprint](../blueprint-v1/11-product-ui-devtools.md)
- [Testing and compatibility Blueprint](../blueprint-v1/12-testing-compatibility.md)
- [Research program](../blueprint-v1/22-research-program.md)
- [Native UI Framework Bake-Off Inventory](native-ui-framework-bakeoff-inventory-2026-07.md)
- [Native UI component fixture inventory](native-ui-component-fixture-inventory-2026-07.md)
- [Page Surface Composition Inventory](page-surface-composition-inventory-2026-07.md)
- [Window Input Accessibility Spike Inventory](window-input-accessibility-spike-inventory-2026-07.md)
- [`adapter-contract-inventory.schema.json`](../ui-runtime/machine/adapter-contract-inventory.schema.json)
- [`adapter-contract-inventory.json`](../ui-runtime/machine/adapter-contract-inventory.json)
- [`validate_ui_adapter_contract.py`](../../tools/validate_ui_adapter_contract.py)

## Method

The inventory was shaped as a dependency-free machine registry with a validator that rejects:

- missing no-claim and unsupported-boundary language;
- missing source records from the M0 UI model, UI-runtime book, Blueprint, readiness, task queue, crosswalk, and related UI inventories;
- missing contract areas for state, command, surface, accessibility, diagnostic, and adapter boundaries;
- drift from the current M0 model invariants in `crates/turing-ui-model`;
- missing denials for toolkit-owned navigation, profile, permission, credential, agent, Plug-in, persistence, or update authority;
- missing required evidence for `ADR-0013`, state, command, surface, accessibility, diagnostic, adapter trait, native adapter prototype, no-toolkit-authority negative tests, and owner review;
- missing `PB-003` evidence and `TASK-000006` scope.

## Current Evidence

The checked inventory now contains:

- 6 contract areas;
- 6 current model invariants from the buildable M0 `turing-ui-model` crate;
- 8 denied adapter authority classes;
- 10 required evidence records;
- no-claim language that blocks `ADR-0013`, native adapter prototype, UI toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production claims, and implementation claims.

`PB-003` can remain `partial` with stronger handoff evidence because the inventory and validator now exist. The status must not move beyond `partial` until `ADR-0013`, complete contracts, native adapter prototype evidence, no-toolkit-authority negative tests, and owner review exist.

## Unsupported Conclusions

This report does not support any of these conclusions:

- `ADR-0013` is accepted;
- a native adapter prototype exists;
- any UI toolkit is selected;
- trusted chrome is ready;
- accessibility readiness exists;
- page-surface composition is approved;
- release-path UI is approved;
- toolkit callbacks cannot own authority in a running adapter;
- Turing has a production UI implementation.

## Remaining Proof

`PB-003` still requires:

- accepted `ADR-0013`;
- complete toolkit-neutral state contract with versioning, stale-version rejection, coalescing, update ordering, and trace semantics;
- complete command contract with identity, epoch, deadline, cancellation, confirmation, rejection, and service-side validation semantics;
- complete surface contract tied to `PB-005`, typed page-surface handles, brokered surface handles, document/device generations, fallback behavior, and `ADR-0016`; the current M0 descriptor is only the bounded metadata subset;
- complete accessibility contract with native roles, names, states, focus, page-tree composition, platform snapshots, and manual assistive-technology evidence;
- complete diagnostic contract with trace events, snapshot hashes, screenshot capture, accessibility capture, fault injection, and redaction rules;
- accepted adapter trait or boundary shape;
- at least one native adapter prototype and equivalent bake-off path for other candidates or owner-approved reduced scope;
- negative tests proving the toolkit cannot own navigation, profile, permission, credential, agent, Plug-in, persistence, or update authority;
- owner review before native-shell, trusted-chrome, accessibility, page-surface, toolkit-selection, or release-path UI claims.

## Affected Records

This inventory updates:

- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json) for `PB-003`;
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

Draft `ADR-0013` and the first adapter trait proposal against `crates/turing-ui-model`, then run a small native adapter prototype that proves toolkit callbacks emit commands only and cannot own navigation, profile, permission, credential, agent, Plug-in, persistence, or update authority.
