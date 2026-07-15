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

Each issue must reference stable requirement/risk/ADR IDs, define negative and failure tests, and state what the completion does **not** support. Work should not leapfrog a missing security boundary merely to produce a more impressive demo.
