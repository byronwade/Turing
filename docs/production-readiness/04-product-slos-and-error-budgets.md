# Product SLOs and Error Budgets

Status: metric catalog; numeric targets unset  
Owner: performance, reliability, quality, product, support, and release

Stable release requires numeric objectives for crash-free sessions, browser and renderer crashes, startup, address-field readiness, input latency, frame pacing, memory, energy, update success, rollback success, profile migration, session restoration, compatibility regressions, accessibility critical flows, data-loss events, and unauthorized agent actions.

Targets are established from fixed-hardware baselines and real workflows. A metric without a reproducible collection method, denominator, lifecycle state, and failure treatment cannot gate a release.

Error-budget exhaustion pauses promotion or triggers rollback. Product pressure cannot convert a blocking SLO into an informational metric without an approved, expiring exception.
