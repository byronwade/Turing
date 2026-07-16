# Benchmarks, Statistics, and Regression Governance

Status: research and design baseline  
Owner: performance measurement program  
Purpose: Make performance evidence reproducible, resistant to gaming, and actionable over time.

## Relationship to the Turing program

This document is the detailed measurement owner for PERF-GATE-1 through PERF-GATE-6 and issue #14's fixed-hardware baseline.

## Benchmark taxonomy

Use component microbenchmarks for diagnosis, synthetic browser suites for comparable signals, generated/local page corpora for controlled product behavior, live sites for supplemental reality checks, fixed user-journey tests for interaction, 30-tab workloads for sustained resource behavior, longevity loops for leaks, and fault tests for recovery.

Speedometer, JetStream, and MotionMark families are named diagnostics, not a combined truth score.

## Environment control

Manifests record machine identity, CPU topology, RAM, GPU/driver, storage, OS build, firmware where relevant, power source/mode, thermal state, display/refresh, background services, browser build/flags, profile, extensions, agents, caches, network, corpus, process/isolation, and tab lifecycle. Warm-up and cold-cache procedures are explicit.

Runs outside control bounds are retained and marked rather than silently removed.

## Sampling and statistics

A noise study determines repetitions and meaningful thresholds. Store raw samples, ordering, outliers, failures, and environment. Report median, percentiles, dispersion/confidence intervals, effect size, and test appropriate to distribution and repeated measures. Multiple metrics and comparisons receive correction or interpretation.

A statistically significant change below practical impact may not block; a large practical tail regression can block even with noisy significance.

## Baseline and comparison

Compare against prior Turing commits and current named competitor versions. Competitor tests use equivalent content, activity, security, isolation, lifecycle, cache, and profile state. Unsupported/failed pages count. Architecture causes require controlled follow-up, not correlation from one browser comparison.

Historical baselines expire when hardware, OS, corpus, or browser semantics change materially.

## Regression pipeline

Pull requests run low-noise component and deterministic page checks. Protected merge queues run leak loops and broader interactions. Scheduled fixed hardware runs startup, input, frame, 30-tab, energy, and longevity. Release candidates compare prior release and competitors.

Regressions retain traces, raw data, suspected change range, semantic owner, issue, decision, and waiver expiry. Automated bisection is used where deterministic enough.

## Waivers and budgets

A waiver states affected users/workloads, magnitude, confidence, root cause, security/accessibility/compatibility implications, owner, mitigation, expiry, and follow-up. No benchmark waiver hides test failure or unsupported behavior. Budgets evolve from evidence through reviewed documents.

Benchmark-specific product code paths are prohibited.

## Publication

Public reports include methodology, manifests, raw or sufficiently detailed samples, analysis code, failures, exclusions, limitations, exact versions, and claim wording. Dashboards display compatibility and configuration alongside speed and memory. Results are reproducible without private infrastructure where legally and practically possible.

## Non-negotiable invariants

- Raw samples, failures, exclusions, and environment accompany summaries.
- Equivalent security, page activity, and lifecycle are required for competitor comparison.
- Synthetic benchmarks are diagnostic, not sole release gates.
- Regression thresholds follow measured noise and practical impact.
- Benchmark-specific product paths are prohibited.
- Claims expire when versions, corpora, or configurations materially change.

## Required evidence

- Versioned benchmark manifests validating against the repository schema.
- Noise studies and power/sample-size rationale.
- Raw data plus reproducible analysis scripts.
- Control runs, randomized order, thermal/power monitoring, and failed-run accounting.
- Regression bisection and waiver history.
- Independent reproduction of selected headline results.

## Known risks and unresolved questions

- Public benchmarks invite overfitting.
- Hardware labs can drift or become unavailable.
- Statistical sophistication can obscure practical user impact.
- Live-site data can be legally, privately, or operationally difficult to reproduce.

## Primary sources

- Speedometer — https://browserbench.org/Speedometer3.1/
- MotionMark — https://browserbench.org/MotionMark1.3/
- JetStream — https://browserbench.org/
- Web Platform Tests — https://web-platform-tests.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
