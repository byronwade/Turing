# Build-Readiness Closure and Owner-Decision Preparation - July 2026

Status: no-claim closure-preparation route for `PB-020`.
Owner: program, architecture, security, quality, documentation research, and release operations

This document defines how the checked [build-readiness closure-review template](../project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json) can be replaced by a real, evidence-backed closure review. It does not close `PB-020`, approve a task, establish that all information is ready for building, or authorize broad implementation.

## Purpose

The closure review is the final coordination record for the current documentation and pre-build gates. It must reconcile the human documents, machine registries, proposed task manifests, evidence bundles, owner decisions, independent review, and claim boundaries in one dated record. A passing repository validator is necessary for record integrity but is not product evidence.

The [Owner-Decision Closure Record Examples](owner-decision-closure-record-examples-2026-07.md) shows the field-level handoff for evidence-collected, held-by-exception, unresolved, and closed-shape-only records. It is fictitious and does not close a gate or grant authority.

## Required collection order

1. Freeze the review scope and capture the current source-tree, registry, task-queue, and relevant document digests.
2. Reconcile the implementation kickoff inventory, dependency graph, documentation-readiness audit, build-information ledger, pre-build registry, and owner-decision board.
3. Verify each remaining gate: source strategy; pinned toolchain and fresh host; IPC; sandbox; benchmark; native shell and page surface; profile/session; package/update; incident response; and backup ownership.
4. Verify that every proposed `TASK-*` execution record has an immutable owner-approved manifest, an independent reviewer, bounded authority, evidence requirements, rollback, expiry, and a current dependency digest. A specified task is not an approved task.
5. Attach raw evidence and focused-validator output for every selected decision. Record failures, missing denominators, stale artifacts, exceptions, and unsupported behavior instead of summarizing them away.
6. Obtain named owner review and independent review for every decision record. Human authority remains separate for release, signing, legal, disclosure, supported-version, production, and incident-closure decisions.
7. Update affected requirements, risks, ADRs, backlog items, crosswalks, task records, owner records, review rules, and documentation indexes in the same change.
8. Run focused validators, aggregate validation, and a final semantic consistency review. Record the exact commands, date, platform, configuration, and retained output.
9. Close or hold each gate explicitly. `PB-020` may close only when every required prerequisite is closed or held by an approved, time-bounded exception with a risk reference, support-boundary change, and rollback path.

## Review packet and evidence handling

The eventual review record belongs under `docs/project-buildout/machine/build-readiness-closure-reviews/` and must use a stable `closure_review_id` that includes the review scope and date. Keep the checked no-claim template as the source shape until a real record is approved; do not overwrite the template. A real packet must include:

- the exact commit, source-tree status, platform, shell, toolchain, and configuration used for collection;
- SHA-256 or equivalent digests for the source tree, machine registries, task manifests, selected documents, and each retained evidence bundle;
- the current versions of the pre-build registry, ADR-0009 evidence, implementation kickoff, dependency graph, documentation audit, build-information ledger, owner board, and closure template;
- one decision record for every unresolved `PB-*` gate and `PB-020`, with direct evidence references and explicit `closed`, `held_by_exception`, or `unresolved` status;
- focused-validator output stored with the evidence packet, including failed commands and their disposition rather than only successful summaries;
- redacted logs and raw artifacts with retention, access, destruction, and secret-exclusion records. Production keys, real user data, private vulnerability details, and unapproved personal contact data do not belong in the repository packet.

Use this status progression for each decision record:

1. `unresolved`: evidence or owner review is missing; no implementation or authority follows.
2. `evidence_collected`: the packet is complete enough for review, but no decision has been made.
3. `held_by_exception`: the owner explicitly accepts a bounded residual risk with an expiry, rollback, support-boundary change, and named follow-up; the exception does not silently authorize a broader claim.
4. `closed`: the owner and independent reviewer accept the evidence and the exact scope is synchronized across registries and documentation.

`PB-020` remains unresolved if any prerequisite is `unresolved`, if a digest is stale, if a task manifest is not immutable and independently reviewed, or if a decision record omits a limitation or prohibited claim. Closure-packet presence, a valid JSON shape, or a green repository check cannot move a gate between these states.

## Collection manifest

Before owner review, the maintainer must record the collection manifest in the packet itself. At minimum it must name these source routes and their current status: [ADR-0009/source strategy](adr-0009-source-strategy-closure-preparation-2026-07.md), [toolchain/fresh host](fresh-host-toolchain-reproduction-closure-preparation-2026-07.md), [IPC](ipc-transport-and-authority-closure-preparation-2026-07.md), [sandbox](sandbox-probe-execution-and-containment-closure-preparation-2026-07.md), [benchmark policy](sustained-performance-policy-research-2026-07.md), [benchmark evidence](benchmark-evidence-and-claim-closure-preparation-2026-07.md), [native UI/accessibility](native-ui-and-accessibility-closure-preparation-2026-07.md), [profile/session](profile-session-execution-and-data-safety-closure-preparation-2026-07.md), [package/update](package-update-execution-and-release-safety-closure-preparation-2026-07.md), [incident response](incident-response-execution-and-disclosure-closure-preparation-2026-07.md), and [backup ownership](backup-ownership-execution-and-two-person-control-closure-preparation-2026-07.md). The manifest must also state which routes were not collected and why; omission is not evidence of completion.

## Decision record requirements

For each gate, the closure record must contain:

- a concrete scope covering the relevant `PB-*`, `WP-*`, `TASK-*`, `ADR-*`, and requirement records;
- a selected, rejected, or held decision, never an implied decision from a template;
- named owner and independent reviewer identities with qualification evidence;
- direct evidence references, raw-artifact identifiers, validator output, and source/configuration digests;
- unresolved limitations and prohibited claims;
- any exception's owner, risk references, expiry, rollback, and support-boundary impact;
- the registry and documentation updates made by the decision.

## Rejection rules

Keep `PB-020` partial and keep the full-build gate closed when any of these is true:

- the no-claim template is presented as a completed review;
- a reviewer is missing, a placeholder, title-only, self-approving, or unqualified;
- a required gate remains blocked, partial, documented-without-runner, or lacks an approved exception;
- evidence is same-host-only where fresh-host evidence is required, lacks raw artifacts or denominators, or has a stale digest;
- a proposed task lacks immutable approval, bounded authority, independent review, rollback, expiry, or dependency integrity;
- a passing documentation validator is used as proof of browser behavior, security, compatibility, accessibility, performance, release, or production support;
- an exception has no expiry, risk linkage, support-boundary update, or rollback path;
- release, signing, legal, disclosure, incident, production, or supported-version authority is inferred from documentation or `PB-020` evidence;
- unsupported behavior, residual risk, or a claim boundary is removed without replacement evidence.

## Promotion boundary

The current machine audit remains `9/10 ready_for_contained_m0` and `1/10 blocked_for_full_goal`; it does not support a `ready_for_full_goal` result. The percentage is a documentation-organization measure, not an implementation percentage. Promotion requires the owner decision record to change the audited blocker state after the evidence and review conditions above are satisfied. Do not calculate readiness from document count, validator count, or the existence of this preparation route.

## Canonical records

- [Build-readiness closure-review schema](../project-buildout/machine/build-readiness-closure-review.schema.json)
- [No-claim closure-review template](../project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json)
- [Owner decision closure board](../project-buildout/23-owner-decision-closure-board.md)
- [Implementation kickoff inventory](implementation-kickoff-review-inventory-2026-07.md)
- [Build-readiness dependency graph](build-readiness-dependency-graph-inventory-2026-07.md)
- [Documentation-readiness completion audit](documentation-readiness-completion-audit-2026-07.md)
- [Build-information readiness ledger](build-information-readiness-ledger-2026-07.md)

## Validation

The eventual closure record must retain, at minimum, the focused validators for every selected gate, `python -B tools/validate_build_readiness_closure_review.py`, `python -B tools/validate_documentation_readiness_completion_audit.py`, `python -B tools/validate_owner_decision_closure_board.py`, `python -B tools/validate_blueprint.py`, `git diff --check`, and `.\tools\check.ps1`. These commands validate repository contracts; they do not by themselves close a readiness gate.
