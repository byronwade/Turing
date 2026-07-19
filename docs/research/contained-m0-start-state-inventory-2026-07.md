# Contained M0 Start State Inventory - July 2026

Status: checked no-claim start-state inventory; not task approval, readiness promotion, or broad implementation approval

Related gate: `PB-020`
Machine record: [`contained-m0-start-state.json`](../project-buildout/machine/contained-m0-start-state.json)
Validator: [`validate_contained_m0_start_state.py`](../../tools/validate_contained_m0_start_state.py)

## Question

Can a maintainer or agent answer "can I start building now?" from one checked record without confusing contained M0 continuation with broad browser implementation readiness?

## Answer

Yes, for start-state routing only. The checked [`contained-m0-start-state.json`](../project-buildout/machine/contained-m0-start-state.json) record says the repository may continue contained M0 documentation, research, validation, no-claim evidence, and review-handoff work, while proposed `TASK-000001` through `TASK-000010` still require owner-approved immutable task manifests before execution.

It also records that `TASK-000011` remains `review_pending`: its review handoff and non-accepting evidence capture may be maintained, but the task cannot be accepted or used to promote `PB-011` without independent accepted evidence.

For future UI work, the start-state route also points to the [Nova design source](../ui-runtime/design-lab/README.md) as the visual and layout reference. Nova is design-lab input only; it does not authorize a toolkit, native shell, trusted-chrome behavior, accessibility implementation, or release path.

The record does not approve broad M1, developer preview, beta, stable, production, Chrome-class, performance, compatibility, security, accessibility, release, daily-driver, or all-information-ready-for-building claims.

For the broader "what information is still missing?" question, use the checked [Build Information Readiness Ledger](build-information-readiness-ledger-2026-07.md) and [`build-information-readiness-ledger.json`](../project-buildout/machine/build-information-readiness-ledger.json). The start-state record routes the current session; the ledger explains the broad-build information gaps.

## Current start classes

| Start class | Current state | Execution answer | Stop before |
|---|---|---|---|
| `START-NO_CLAIM_DOC_RESEARCH` | Allowed now | Documentation, research, registry, validator, no-claim evidence, and task-approval preparation can continue when mapped to current records. | Task approval, readiness promotion, product claims, or implementation claims. |
| `START-TASK_000011_REVIEW_HANDOFF` | Review-pending only | The review handoff, source-commit binding, and non-accepting evidence capture can be maintained. | Accepting `TASK-000011`, promoting `PB-011`, or claiming production IPC/security. |
| `START-PROPOSED_TASKS_000001_000010` | Owner approval required | Execution cannot start from the proposed queue alone. Preparation and owner-review material can continue. | Implementing proposed tasks before reviewed manifests exist. |
| `START-BROAD_M1_OR_PRODUCT` | Blocked | Broad browser construction and product claims cannot start from current evidence. | Source adoption, release UI path, public claims, production work, or Chrome-class comparison. |

## Validator coverage

The validator checks:

- the start-state schema, status, unsupported boundaries, and source records;
- `pre-build-readiness.json` still says contained M0 is allowed and broad implementation is not ready;
- `TASK-000001` through `TASK-000010` remain `proposed`;
- `TASK-000011` remains `review_pending`;
- the immediate, review-pending, owner-approval-required, and blocked start classes all retain their stop conditions;
- `PB-020` lists the start-state record, schema, inventory, and validator as evidence while remaining partial.

## What this changes

This adds a compact control surface for stop/resume sessions. A future maintainer can answer the start question before reading every readiness report:

1. no-claim documentation/research/validator work may continue;
2. review-handoff maintenance for `TASK-000011` may continue;
3. proposed tasks need owner-approved manifests before execution;
4. broad browser/product work remains blocked.

## What remains missing

Before broad building or Chrome-class competition claims, the project still needs owner-reviewed closure or explicit expiring exceptions for source strategy, fresh-host reproduction, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, backup ownership, build-readiness closure, build-information readiness, and release authority. The start-state record intentionally preserves those blockers.
