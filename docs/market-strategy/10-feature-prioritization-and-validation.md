# Feature Prioritization, Validation, and Promotion

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Define how market opportunities become experiments, requirements, work packages, supported features, or rejected ideas without feature sprawl.

## Proposed sequence

### Foundation

- Turing Spaces, vertical/horizontal tabs, folders, pinned items, identity binding.
- Two-pane split view, panels, command palette.
- Crash-safe journal and initial Time Machine.
- Resource Truth Center.
- High-fidelity migration and open export.

### Differentiated developer preview

- Four-pane Research Canvas and citations.
- Local-first encrypted Space sync prototype.
- Web App Fabric.
- Developer Causal Mode.
- Initial first-party Plug-ins.
- Read-only selected-source AI.

### Beta research

- Resource budgets and predictive lifecycle controls.
- Full workspace history and handoff.
- Privacy receipts and provenance.
- WebExtensions compatibility expansion.
- Isolated low-risk agent actions.

### Later gates

- Consequential agent actions.
- Encrypted collaborative Spaces.
- Broad third-party Plug-in store.
- Enterprise shared policy and organization services.

## Promotion pipeline

`OP proposal → evidence plan → prototype → security/privacy/accessibility/performance review → user study → architecture decision if needed → requirement and risk update → owned work package → implementation → verification → support statement`

Promotion requires a named owner, target segment, measurable job, alternatives, complete failure model, dependencies, maintenance cost, raw evidence, and explicit rejected/deferred outcome. An opportunity can be removed without product failure.

## Anti-sprawl rules

- Prefer one coherent data model over overlapping modes.
- New features must identify what they replace or simplify.
- Defaults remain familiar and minimal.
- Advanced capability is progressively disclosed.
- Background work and persistent state have budgets and ownership.
- Every experimental feature has an expiry and removal path.
- A market request cannot bypass security, accessibility, compatibility, or release gates.

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
