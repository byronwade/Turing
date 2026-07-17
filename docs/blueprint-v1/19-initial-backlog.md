# 19 — Initial Engineering Backlog

The GitHub issues are the executable front door for this plan. This document preserves their intended dependency order even if issue numbers change. The authoritative machine graph is [`backlog.json`](machine/backlog.json), and the agent-facing execution details are in the [Implementation Master Plan](../project-buildout/implementation-plan/README.md).

## Canonical work-package order

1. **WP-001 — Repository validation and evidence foundation.**
2. **WP-002 — Kernel identities, process roles, capabilities, and bounded IPC.**
3. **WP-003 — Cross-platform renderer sandbox probes.**
4. **WP-004 — Native accessible browser-shell spike.**
5. **WP-005 — Tab lifecycle, resource attribution, and 30-tab simulator.**
6. **WP-006 — HTML tokenizer and tree builder.**
7. **WP-007 — DOM arena, mutation epochs, and events.**
8. **WP-008 — CSS parser, selectors, cascade, and computed values.**
9. **WP-009 — Block/text layout, display list, and CPU reference raster.**
10. **WP-010 — JavaScript parser, bytecode, interpreter, and Test262 harness.**
11. **WP-011 — Exact tracing GC and Web IDL bindings.**
12. **WP-012 — Navigation transactions, site instances, and renderer swaps.**
13. **WP-013 — Scoped HTTP/TLS request context, cache, cookies, and hermetic server.**
14. **WP-014 — Storage broker, quota, transactional migrations, and service-worker foundation.**
15. **WP-015 — Versioned DevTools/automation protocol and local trace viewer.**
16. **WP-016 — Capability-safe agent reference implementation.**
17. **WP-017 — Signed package/update laboratory with rollback and profile migration.**
18. **WP-018 — Fixed-hardware compatibility, performance, memory, and energy laboratory.**

## Task decomposition rule

A WP is never assigned to one agent as a monolithic task. Each WP is decomposed into `TASK-*` records for design, implementation, conformance, security, performance, accessibility, recovery, documentation, and release evidence as applicable.

A task starts only when:

- dependencies are accepted on `main`;
- required ADRs and interface freezes are ready;
- allowed paths, authority, reviewer, evidence, tests, budgets, rollback, and expiry are explicit;
- no hidden source, dependency, platform, or licensing assumption is required.

The [work-package playbooks](../project-buildout/implementation-plan/16-work-package-playbooks.md) define the minimum task families, negative tests, evidence, handoff, and non-scope for WP-001 through WP-018.

## Current sequencing rule

Use [`implementation-task-sequence.json`](machine/implementation-task-sequence.json) for planned waves and [`implementation-execution-graph.json`](machine/implementation-execution-graph.json) for dependencies. A plan wave does not authorize implementation; only a reviewed task with status `ready` does.

## Required issue content

Every work-package or task issue must reference stable requirement/risk/ADR/WP/task IDs and include:

- purpose and exact scope;
- dependencies and decision gates;
- allowed/prohibited paths and authority;
- acceptance criteria and negative/failure tests;
- security, privacy, performance, accessibility, compatibility, operational, and legal effects;
- evidence classes and immutable artifacts;
- unsupported behavior and residual risk;
- rollback, expiry, reviewer, and downstream handoff.

Work must not leapfrog a missing security, identity, persistence, update, accessibility, or release boundary merely to produce a more impressive demo.

<!-- MARKET-STRATEGY-2026-07 -->
## Market-opportunity research queue

`OP-001` through `OP-014` remain outside the accepted WP-001 through WP-018 executable backlog. Candidate additions include a market-validation harness, Space data-model prototype, migration/export corpus, Time Machine journal experiment, and Resource Truth usability study. New WP entries require reviewed promotion, requirement/risk mapping, ownership, and dependency analysis.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native shell refinement

WP-004 produces a toolkit-neutral Rust state/command contract, equivalent Slint/Vizia/Floem-or-GPUI reference shells, page-surface and accessibility composition evidence, a reference-platform decision, design tokens/components, and ADR-0013 through ADR-0016 before a framework becomes production direction.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent execution and production readiness

The `TASK-*` graph, protected review, run/evidence records, tool and secret boundaries, stable-scope draft, SLO methods, update laboratory, incident exercises, supported-platform evidence, and release review procedure are part of implementation—not optional work after features are written.
