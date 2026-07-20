# Turing Implementation Master Plan

Status: canonical execution plan for bounded implementation; not a production-readiness claim
Owner: program, architecture, security, quality, release operations, product, accessibility, and subsystem owners
Last reviewed: 2026-07-20

This handbook converts Turing's research library, Blueprint, requirements, work packages, agent controls, and release gates into one dependency-ordered game plan that an implementation agent can follow without inventing scope or silently bypassing unresolved decisions.

It is subordinate to accepted requirements and ADRs. When this plan conflicts with a machine-readable registry, accepted ADR, security rule, or requirement, the stricter and more authoritative record wins and the inconsistency must be corrected before implementation continues.

## Current authorization

Turing is ready for contained M0 tasks. It is not ready for broad parallel implementation, preview distribution, or an autonomous stable-release campaign.

An agent starts only a named `TASK-*` whose dependencies are accepted, paths and authority are bounded, acceptance criteria and negative tests are complete, and an independent reviewer is identified. An agent never receives the instruction "build the entire browser" as one task.

## Pre-build readiness handoff

Before selecting a milestone or shaping implementation work, read the checked [Documentation Readiness Completion Audit](../../research/documentation-readiness-completion-audit-2026-07.md), [Build Information Readiness Ledger](../../research/build-information-readiness-ledger-2026-07.md), [Owner Decision Closure Board](../23-owner-decision-closure-board.md), and [Build-Readiness Closure and Owner-Decision Preparation](../../research/build-readiness-closure-and-owner-decision-preparation-2026-07.md). These records are the current stop/resume handoff for the ten source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell/accessibility, profile/session, package/update, incident-response, and ownership closure routes. They establish contained-M0 continuation only; they do not approve proposed tasks, close `PB-020`, authorize broad M1 implementation, or establish all-information-ready-for-building, Chrome-class, production, release, performance, compatibility, security, or accessibility claims.

## Canonical source hierarchy

1. Accepted requirements and risks under `docs/blueprint-v1/machine/`.
2. Accepted ADRs in [`17-architecture-decisions.md`](../../blueprint-v1/17-architecture-decisions.md).
3. The machine work-package graph in [`backlog.json`](../../blueprint-v1/machine/backlog.json).
4. Agent authority and task schemas under [`docs/agent-execution/`](../../agent-execution/README.md).
5. This implementation plan and its machine companions.
6. Detailed engineering books and dated research.
7. Issues, pull requests, and chat context, which are never the sole canonical source.

## Reading order

1. [Program sequence and critical path](01-program-sequence-and-critical-path.md)
2. [Agent operating protocol](02-agent-operating-protocol.md)
3. [Architecture decisions and interface freezes](03-architecture-decisions-and-interface-freezes.md)
4. [M0–M1: foundation, shell, process, sandbox, and resource laboratory](04-m0-m1-foundation-shell-security.md)
5. [M2: static document engine](05-m2-static-web-engine.md)
6. [M3: JavaScript runtime and dynamic DOM](06-m3-javascript-runtime.md)
7. [M4: navigation, network, storage, and multipage applications](07-m4-navigation-network-storage.md)
8. [M5: coherent developer preview](08-m5-developer-preview.md)
9. [M6: JIT, media, Plug-ins, and agent preview](09-m6-jit-media-plugins-agents.md)
10. [M7: beta hardening](10-m7-beta-hardening.md)
11. [M8: stable release candidate](11-m8-stable-release.md)
12. [M9: parity and continuous maintenance](12-m9-parity-and-continuous-maintenance.md)
13. [Cross-cutting verification and evidence](13-cross-cutting-verification-and-evidence.md)
14. [Staffing, delivery, and capacity model](14-staffing-delivery-and-capacity.md)
15. [Stop, replan, replace, and abandon criteria](15-stop-replan-and-risk-controls.md)
16. [WP-001 through WP-020 playbooks](16-work-package-playbooks.md)
17. [Task kickoff, evidence, handoff, and release checklists](17-delivery-checklists-and-handoffs.md)

## Machine-readable companions

- [`implementation-execution-graph.json`](../../blueprint-v1/machine/implementation-execution-graph.json)
- [`implementation-milestone-gates.json`](../../blueprint-v1/machine/implementation-milestone-gates.json)
- [`implementation-interface-freezes.json`](../../blueprint-v1/machine/implementation-interface-freezes.json)
- [`implementation-evidence-catalog.json`](../../blueprint-v1/machine/implementation-evidence-catalog.json)
- [`implementation-task-sequence.json`](../../blueprint-v1/machine/implementation-task-sequence.json)

## Master execution rule

Every implementation change follows this chain:

```text
accepted requirement or bounded research question
→ accepted design or explicit experiment hypothesis
→ owner-reviewed immutable ready TASK manifest with bounded authority
→ isolated implementation branch
→ implementation plus negative tests
→ generated evidence bundle
→ independent review
→ protected merge
→ downstream handoff
→ release gate when applicable
```

Skipping a stage is a defect. A green build does not substitute for security, compatibility, accessibility, performance, recovery, or operational evidence.

## What this plan does not claim

This handbook does not select Servo, a UI framework, a stable ABI, a supported platform matrix, production queue budgets, a release date, or a stable feature set. It specifies when and how those decisions are made, what evidence is required, and what work must stop until the evidence exists.
