# 19 — Initial Engineering Backlog

The GitHub issues created with Blueprint v1 are the executable front door for this plan. This document preserves their intended dependency order even if issue numbers change.

1. Repository validation, schemas, CI, provenance, and quality policy.
2. Kernel identity, process-role, capability, and bounded IPC model.
3. macOS, Windows, and Linux sandbox probe harnesses.
4. Native shell, platform accessibility, and crash-resilient product UI spike.
5. Tab lifecycle, resource attribution, and 30-tab simulator.
6. HTML tokenizer/tree-builder reference implementation and fuzzing.
7. DOM arena, mutation epochs, events, and JS-wrapper boundary.
8. CSS tokenizer/parser/selectors/cascade/computed-value foundation.
9. Block and text layout, fragments, display list, CPU raster reference.
10. JavaScript parser/bytecode/interpreter and Test262 harness.
11. Exact tracing GC and Web IDL binding generator.
12. Navigation transaction, site-instance assignment, and renderer swaps.
13. Scoped HTTP/TLS request context, cache/cookies, and hermetic test server.
14. Storage broker, quota, transactional migrations, and service-worker foundation.
15. Versioned DevTools/automation protocol and local trace viewer.
16. Agent principal, grant, observation, action, policy, confirmation, and adversarial test reference.
17. Signed package/update laboratory with rollback and profile migration fault injection.
18. Fixed-hardware compatibility/performance/memory/energy lab.
19. Baseline JIT, W^X, differential tiering, and no-JIT hardened execution.
20. Everyday product surfaces, history, bookmarks, downloads, and settings workflows.

Each issue must reference stable requirement/risk/ADR IDs, define negative and failure tests, and state what the completion does **not** support. Work should not leapfrog a missing security boundary merely to produce a more impressive demo.

<!-- MARKET-STRATEGY-2026-07 -->
## Market-opportunity research queue

`OP-001` through `OP-014` remain outside the accepted `WP-001` through `WP-020` executable backlog. The first candidate additions are a market-validation harness, Space data-model prototype, migration/export corpus, Time Machine journal experiment, and Resource Truth usability study. New `WP-*` entries require reviewed promotion and dependency mapping.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native shell work-package refinement

`WP-004` remains the native accessible browser-shell spike. Before its implementation hardens around a framework, it produces a toolkit-neutral Rust state/command contract, equivalent Slint/Vizia/Floem-or-GPUI reference shells, page-surface and accessibility composition evidence, a reference-platform decision, and proposed ADR-0013 through ADR-0016. This refinement does not change the 20-work-package registry or claim WP-004 has started.

The [implementation master plan](../project-buildout/implementation-plan/README.md) provides dependency-ordered execution documentation for `WP-001` through `WP-020`. It does not approve any work package, promote broad implementation readiness, or replace reviewed `TASK-*` manifests.

The checked [GitHub Issue Handoff](../project-buildout/19-github-issue-handoff.md) maps the current issue and stale-PR cleanup snapshot back to these `WP-*`, `PB-*`, and `TASK-*` records. It is a coordination handoff only and does not approve work packages, approve tasks, promote readiness, or replace live GitHub verification.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent execution and production-readiness preparation

Before decomposing WP-001 through WP-020 into agent tasks, create the `TASK-*` graph, protected review policy, run/evidence storage, tool and secret boundaries, stable-scope draft, SLO measurement methods, update laboratory, incident exercises, supported-platform evidence, and release review procedure. This does not change existing work-package status.

<!-- WP-002-KERNEL-IPC-2026-07 -->
## WP-002 current evidence

The M0 reference portion of `WP-002` is implemented in `turing-types`, `turing-ipc`, and `turing-kernel`, generated from `schemas/ipc/control-plane.json`, and exercised by the shell self-test. The machine backlog keeps the item in progress and links the [dated evidence report](../research/wp-002-kernel-ipc-2026-07.md).

Remaining acceptance work is authenticated platform transport, generated wire encoding/decoding, safe handle and shared-memory contracts, cancellation and terminal-response state machines, compromised-process negative testing, platform launch/sandbox integration, production measurements, and independent security review.
