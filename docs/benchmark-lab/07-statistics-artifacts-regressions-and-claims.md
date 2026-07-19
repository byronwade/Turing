# Statistics, Artifacts, Regressions, and Claims

Status: detailed research and design baseline  
Owner: performance measurement and benchmark operations  
Book index: [README](README.md)  
Canonical overview: [Blueprint owner](../blueprint-v1/09-performance-memory.md)

## Purpose

This chapter defines the research contract for **statistics, artifacts, regressions, and claims**. It is not an implementation or support claim. The design must remain compatible with the owning Blueprint, requirements, risks, security model, performance contract, accessibility obligations, and documentation policy.

## Scope

The study covers:

- sample design;
- randomization;
- warmup;
- confidence intervals;
- practical thresholds;
- control charts;
- raw traces;
- manifests;

The scope includes normal use, hostile input, compromised-process assumptions, low-memory systems, cancellation, timeout, crash, restart, migration where applicable, accessibility, diagnostics, and operational ownership.

## Design objectives

1. Preserve profile, origin, site, frame, process, document-epoch, capability, and resource-owner identity wherever the subsystem crosses a boundary.
2. Make limits, state transitions, failure, cancellation, retry, recovery, and unsupported behavior explicit.
3. Minimize privileged code, ambient authority, copies, allocations, unbounded queues, hidden wakeups, and duplicate state.
4. Keep a deterministic correctness path and semantic trace before accepting incremental, concurrent, cached, hardware-accelerated, or speculative paths.
5. Treat accessibility, privacy, security, developer observability, energy, and maintainability as coequal design constraints.

## Architecture questions

- What are the authoritative inputs, outputs, identities, epochs, owners, and lifetime boundaries?
- Which data may be immutable, shared, cached, moved, serialized, persisted, or recomputed without widening authority?
- Which operations require a broker, user activation, permission, confirmation, platform API, or release-time capability?
- Where can a renderer, extension, DevTools client, model, corrupted store, native dependency, or remote peer act maliciously?
- Which work belongs on the user's critical path, and which work can yield, cancel, batch, degrade, or move to an isolated worker?
- How does the subsystem expose causality without logging secrets or retaining sensitive payloads?

## Data and lifecycle contract

Every durable design note must enumerate:

- typed identifiers and their issuer;
- state machine, valid transitions, guards, side effects, and terminal states;
- ownership, allocation class, byte/task/queue/time budget, and pressure behavior;
- synchronization, ordering, atomicity, idempotency, and stale-epoch behavior;
- persistence, schema/versioning, migration, rollback, clearing, and recovery where relevant;
- platform-specific behavior and the portable semantic core;
- exact unsupported cases and the safe failure mode.

## Performance and resource requirements

Measurements report p50, p95, and p99 latency where interaction is involved; live, reserved, committed, resident, shared, compressed, swapped, and GPU memory where relevant; CPU time, queue wait, wakeups, network/disk bytes, energy, and thermal state; and the effect of site isolation, process count, tab lifecycle, extensions, DevTools, and agents.

An optimization is not accepted from a microbenchmark alone. It must preserve conformance, security mitigations, accessibility paths, failure behavior, and a default-equivalent configuration. Tail regressions, extra process launches, larger working sets, or increased recovery cost remain visible.

## Security and privacy requirements

- Validate untrusted sizes, counts, enums, offsets, recursion, nesting, handles, paths, versions, and identities before privileged work or large allocation.
- Revalidate capability, profile, origin, site, target, and epoch after asynchronous delay.
- Redact secrets at the source; routine traces use IDs, classifications, hashes, sizes, and reason codes rather than raw content.
- Bound retries, concurrency, queues, caches, streams, logs, diagnostic exports, and persistent records.
- Define compromised-component tests and the assets that remain inaccessible after compromise.
- Do not weaken isolation, certificate or update verification, trusted UI, permissions, confirmation, or data partitioning to improve compatibility or a benchmark.

## Developer and accessibility requirements

The subsystem exposes stable, schema-defined diagnostics for state, ownership, causality, limits, policy decisions, errors, cancellation, and recovery. The UI and protocol distinguish physical totals from charged estimates and current facts from inferred causes. Keyboard, screen-reader, zoom, contrast, localization, text input, and reduced-motion behavior are considered whenever the subsystem affects users or developer tools.

## Failure and recovery

Research must cover malformed input, timeout, cancellation, process crash, browser crash, restart, low memory, allocation failure, disk full, network loss, GPU/device loss, sleep/resume, clock change, stale handles, version mismatch, partial operation, and repeated failure. Recovery must not silently lose user work, widen authority, accept stale state, or loop indefinitely.

## Falsifiable experiments

1. Prototype and measure sample design under representative, adversarial, failure, cancellation, and pressure conditions.
2. Prototype and measure randomization under representative, adversarial, failure, cancellation, and pressure conditions.
3. Prototype and measure warmup under representative, adversarial, failure, cancellation, and pressure conditions.
4. Prototype and measure confidence intervals under representative, adversarial, failure, cancellation, and pressure conditions.
5. Prototype and measure practical thresholds under representative, adversarial, failure, cancellation, and pressure conditions.

Each experiment records commit, platform, hardware, build flags, corpus, security configuration, process topology, tab state, sample count, raw samples, statistical treatment, failures, unsupported cases, and confidence. A result that cannot be reproduced remains exploratory.

## Evidence gates

- specification and data-model review;
- unit, property/model, malformed-input, negative-capability, timeout, cancellation, recovery, and OOM tests;
- WPT, Test262, protocol, platform, accessibility, or other primary conformance evidence where applicable;
- structure-aware fuzzing and corpus minimization for parsers, protocols, state machines, and persisted formats;
- semantic trace or full-recomputation/reference oracle;
- fixed-hardware latency, memory, energy, and longevity baselines;
- benchmark manifests validated by [`tools/validate_benchmark_manifests.py`](../../tools/validate_benchmark_manifests.py), with raw-artifact hashes that fail closed when checked-in fixture bytes drift;
- trace/artifact package contracts validated by [`tools/validate_benchmark_artifact_packages.py`](../../tools/validate_benchmark_artifact_packages.py), with runner-owned roots, required trace classes, required artifact classes, redaction/retention fields, prohibited-content rules, and SHA-256 manifest records;
- statistics-analysis contracts validated by [`tools/validate_benchmark_statistics_analysis.py`](../../tools/validate_benchmark_statistics_analysis.py), with sample design, warmup, randomization or paired order, noise study, uncertainty, effect size, outlier policy, multiple-comparison interpretation, metric-family summaries, denominator publication, and rejection rules;
- explicit residual risks, owner, revisit trigger, and unsupported matrix.

## Current No-Claim Artifact Package Contract

The checked [Benchmark trace/artifact package contract](../research/benchmark-trace-artifact-package-contract-2026-07.md) and [no-claim trace/artifact package plan](../blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json) define the current `PB13-EV-007` package shape. This is not a captured trace bundle, not a benchmark result, and not a memory, energy, Chrome-class, or performance result.

The contract exists so a future runner cannot treat partial files as evidence. A real package still needs ETW or equivalent host traces, Perfetto-compatible traces where applicable, logs, screenshots when relevant, raw samples, memory snapshots, power or energy samples, failure denominator records, redaction review, retention decisions, and SHA-256 hashes.

Trace and instrumentation are separate experimental conditions. A future package must retain an otherwise equivalent no-trace control whenever tracing, counters, sampling, logging, or diagnostic hooks can affect CPU, wakeups, allocation, cache behavior, latency, thermal state, or energy. The package records the trace configuration, providers/data sources, buffers, sampling intervals, duration, event-loss indicators, collector/analyzer versions, and measured control delta. An instrumented trace may diagnose a result, but it cannot silently become the result used for a headline performance claim.

## Current No-Claim Statistics-Analysis Contract

The checked [Benchmark statistics analysis contract](../research/benchmark-statistics-analysis-contract-2026-07.md) and [no-claim statistics-analysis plan](../blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json) define the current `PB13-EV-006` analysis shape. This is not a browser benchmark run, not a runner-generated raw sample set, not a confidence interval from measured browser data, not a competitor result, and not a Chrome-class or public performance claim.

The contract exists so a future runner cannot treat raw artifacts as statistical evidence by themselves. A real analysis still needs runner-generated raw samples, sample order, warmup records, raw-artifact hashes, a noise study, sample-size rationale, uncertainty or confidence interval treatment, effect-size and practical-impact thresholds, outlier policy, multiple-comparison interpretation, denominator publication, and owner-reviewed analysis.

Future public claim bundles must reference the statistics-analysis plan through `registry_references.statistics_analysis_plan_id`, and [`tools/validate_benchmark_claim_bundles.py`](../../tools/validate_benchmark_claim_bundles.py) cross-checks that ID against the checked no-claim plan. A claim bundle that omits the plan or cites stale analysis evidence fails before owner review.

Future benchmark readiness reviews must also fill `review_scope.statistics_analysis_plan` with the owner-reviewed plan they accept. The checked no-claim readiness-review template keeps that field null, so it cannot be cited as statistics review, denominator review, claim-bundle review, benchmark-ready status, Chrome-class evidence, or public performance evidence.

The checked [Benchmark engine baseline harness readiness map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md) organizes the current no-claim `PB-013` evidence into Level 0 through Level 3 stop/resume guidance. It is an evidence-routing aid only and does not provide a browser run, raw sample, owner-reviewed statistics analysis, owner-reviewed benchmark readiness, competitor result, Chrome-class evidence, or public performance claim.

## Risks

Primary risks are semantic divergence, confused-deputy behavior, stale identity, unbounded work, memory retention, cross-profile or cross-origin leakage, native or platform compromise, hidden performance cliffs, inaccessible failure UI, unreliable recovery, and documentation becoming more certain than the evidence.

## Primary sources

- https://browserbench.org/
- https://browserbench.org/Speedometer3.1/
- https://browserbench.org/JetStream3.0/
- https://browserbench.org/MotionMark/
- https://perfetto.dev/
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer

Source URLs are starting points. An implementation records the exact revision, retrieval date, local patches, license, test commit, and behavior supported.

## Change discipline

This document is non-normative research until an accepted decision updates the owning Blueprint chapter, relevant ADRs, requirements, risks, work packages, tests, and machine-readable records in the same change.
