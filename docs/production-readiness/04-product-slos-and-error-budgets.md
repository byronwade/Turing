# Product SLOs and Error Budgets

Status: metric catalog; numeric targets unset  
Owner: performance, reliability, quality, product, support, and release

Stable release requires numeric objectives for crash-free sessions, browser and renderer crashes, startup, address-field readiness, input latency, frame pacing, memory, energy, update success, rollback success, profile migration, session restoration, compatibility regressions, accessibility critical flows, data-loss events, and unauthorized agent actions.

Targets are established from fixed-hardware baselines and real workflows. A metric without a reproducible collection method, denominator, lifecycle state, and failure treatment cannot gate a release.

Error-budget exhaustion pauses promotion or triggers rollback. Product pressure cannot convert a blocking SLO into an informational metric without an approved, expiring exception.

## Performance evidence crosswalk

The performance SLOs are deliberately targetless until the benchmark lab has owner-approved hardware, operating-system controls, browser and workload pins, raw samples, trace packages, and a reviewed analysis. The evidence ladder is defined in the [Chrome-class performance runbook](../research/chrome-class-performance-runbook-2026-07.md):

- **Level 0:** harness and instrumentation smoke only; no browser or product claim.
- **Level 1:** local Turing pipeline evidence; useful for regression detection, not competitor comparison.
- **Level 2:** controlled comparative diagnostic with disclosed configuration and lifecycle state; not a public leadership claim.
- **Level 3:** independently reviewed claim candidate with complete raw evidence, denominator, uncertainty treatment, failure accounting, and expiry.

| SLO | Measurement lane | Related requirements | Minimum evidence before gating | Current state |
|---|---|---|---|---|
| `SLO-004` startup and address-field readiness | cold-start harness, fixed hardware, process and profile state | `REQ-PERF-001` | Level 1 reproducibility; Level 3 for a public comparison | target unset |
| `SLO-005` input-to-present latency | input trace, presentation timestamps, foreground lifecycle state | `REQ-PERF-001` | Level 1 with p95/p99 and timeout denominator; Level 3 for comparison | target unset |
| `SLO-006` frame pacing | version-pinned reference workloads and dropped-frame accounting | `REQ-PERF-001` | Level 1 with workload and refresh-rate controls; Level 3 for comparison | target unset |
| `SLO-007` 30-tab memory | mixed and all-live scenarios with lifecycle disclosures | `REQ-PERF-002`, `REQ-PERF-003` | Level 1 with per-principal attribution; Level 3 for comparison | target unset |
| `SLO-008` wakeups and energy | fixed power profile, thermal state, background policy, and sampling method | `REQ-PERF-001`, `REQ-PERF-003` | Level 1 with energy collection validity; Level 3 for comparison | target unset |

This crosswalk does not make any SLO achievable, verified, or production-ready. It only prevents a target from being promoted into a release gate or a Chrome-class claim without the corresponding evidence package. The machine registry carries the same lane and requirement metadata for tooling and review.
