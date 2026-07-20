# Product SLOs and Error Budgets Research - July 2026

Status: deferred `RQ-62` research packet; no numeric target or release decision
Owner: product, performance, reliability, quality, accessibility, security, support, and release
Question: Which numeric reliability, performance, energy, compatibility, accessibility, migration, update, and agent-safety targets predict a supportable stable browser?

This packet prepares the decision. It does not establish a target, prove that a target is achievable, or promote any metric into a release gate. The canonical targetless catalog remains [Product SLOs and Error Budgets](../production-readiness/04-product-slos-and-error-budgets.md) and [`product-slos.json`](../production-readiness/machine/product-slos.json).

## Source-backed observations

The Google SRE guidance separates a service level indicator (SLI), a quantitative measurement of delivered service, from a service level objective (SLO), a target or range for that SLI, and a service level agreement (SLA), a contract with consequences. An SLO is therefore not just a dashboard label: its measurement method, valid conditions, and consequence path must be explicit. [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

The same guidance warns that averages can hide long-tail behavior, recommends distributions and percentiles where tails matter, and says SLOs need a defined population, aggregation window, included requests, and acquisition method. It also describes an error budget as the allowed rate of SLO misses and connects budget state to release decisions. These are measurement-policy observations, not Turing target values. [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

Google's risk guidance treats reliability as a product tradeoff rather than an absolute maximization problem: the useful target balances user harm, delivery, and operational cost. Turing must still treat security, accessibility, data integrity, and authorization failures as protected constraints; they cannot be traded away to improve speed or release cadence. [Google SRE: Embracing Risk](https://sre.google/sre-book/embracing-risk/)

The SRE workbook frames SLO work as a loop: define user-relevant indicators, choose objectives, instrument them, alert on meaningful violations, and use the result to prioritize reliability work. This supports a staged Turing process in which target selection follows representative workflows and baseline evidence rather than current implementation performance. [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)

## Turing measurement contract

Every candidate metric must record, at minimum:

- user-visible behavior and the harm represented by a bad event;
- numerator, denominator, unit, direction, aggregation window, and percentile or distribution treatment;
- browser revision, build profile, platform, hardware, refresh rate, power mode, network profile, profile state, tab lifecycle state, and security configuration;
- workload corpus, scenario boundaries, warm/cold state, foreground/background state, timeout treatment, exclusions, and missing-data handling;
- measurement point and clock source, including whether the metric is user-observed, browser-observed, or service-observed;
- raw samples, trace/artifact identity, uncertainty treatment, reproducibility requirements, retention, redaction, access control, and privacy limits;
- owning role, review cadence, escalation action, exception expiry, and the release or support decision affected by budget burn.

Candidate families include crash and recovery, startup and address-field readiness, input-to-present latency, frame pacing, memory and resource attribution, wakeups and energy, compatibility regressions, accessibility critical workflows, profile migration and session restoration, update and rollback success, data-loss events, security recovery, and unauthorized agent actions. Each family requires its own denominator and failure semantics; one combined browser score is not an acceptable substitute.

## Error-budget policy to decide

The owner-reviewed policy should define separate budgets for user-visible availability/correctness, performance tails, resource use, data integrity, accessibility, update and migration safety, security response, and agent authorization. A budget must identify:

1. what counts as a bad event;
2. how events are weighted when severity differs;
3. the rolling and review windows;
4. warning, freeze, rollback, and exception actions;
5. who can approve an exception, its expiry, and the evidence required to close it.

Security boundary violations, unauthorized consequential actions, unrecoverable data loss, and loss of required accessibility operation are protected stop conditions. They must not be hidden by a favorable average, offset by a separate performance improvement, or waived by an informal release decision.

## Evidence route

The next evidence package should use the existing targetless catalog and benchmark/readiness lanes to produce:

- owner-approved user workflows and severity classes;
- SLI definitions and denominator fixtures for each catalog entry;
- fixed-hardware, platform, lifecycle, and security-configuration baselines;
- raw samples and trace packages with reproducible analysis;
- false-positive, missing-data, timeout, crash, cancellation, and recovery tests;
- privacy-preserving telemetry and retention review;
- candidate target options with product, support, accessibility, security, and operational tradeoffs;
- owner-reviewed SLO and error-budget decision record, including release actions and exception authority.

Until that evidence exists, the project must not claim that any numeric target is achievable, that the browser meets a target, that a budget is operational, or that performance, reliability, compatibility, accessibility, migration, update, or agent safety is production-ready.

## Current disposition

`RQ-62` remains deferred. This packet closes a documentation-routing gap and makes the evidence shape explicit; it does not change the active/deferred question count, contained-M0 authorization, implementation status, or the `90%` contained-M0 / `0%` full-build readiness measures.

## Retrieval record

- Retrieved 2026-07-19.
- Google SRE Book, “Service Level Objectives”: https://sre.google/sre-book/service-level-objectives/
- Google SRE Book, “Embracing Risk”: https://sre.google/sre-book/embracing-risk/
- Google SRE Workbook, “Implementing SLOs”: https://sre.google/workbook/implementing-slos/
