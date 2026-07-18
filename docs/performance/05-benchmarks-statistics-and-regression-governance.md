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
- No-claim manifest fixtures, benchmark hardware registry cross-checks, and checked raw-artifact hashes validated by [`tools/validate_benchmark_manifests.py`](../../tools/validate_benchmark_manifests.py).
- Versioned OS-control manifests validated by [`tools/validate_benchmark_os_controls.py`](../../tools/validate_benchmark_os_controls.py), with clean-image, update, driver, firmware, display, thermal, clock, network, service, and artifact-storage controls visible.
- Versioned resource-attribution taxonomy manifests validated by [`tools/validate_benchmark_resource_attribution.py`](../../tools/validate_benchmark_resource_attribution.py), with semantic owner classes, physical-versus-charged views, unknown buckets, GPU accounting requirements, and reporting disclosures visible.
- Versioned corpus manifests and generated local fixtures validated by [`tools/validate_benchmark_corpus.py`](../../tools/validate_benchmark_corpus.py).
- The current expanded no-claim corpus seed covers generated static-document, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract fixture shapes only; it is not reviewed representative corpus evidence.
- Versioned local server and network profiles validated by [`tools/validate_benchmark_network_profile.py`](../../tools/validate_benchmark_network_profile.py).
- Static-server self-test artifacts generated by [`tools/serve_benchmark_profile.py --self-test`](../../tools/serve_benchmark_profile.py) for route-level loopback and Host-header evidence.
- runner-managed server lifecycle self-test packages generated by [`tools/run_benchmark_server_profile.py --self-test`](../../tools/run_benchmark_server_profile.py), with startup, route checks, shutdown, artifact hashes, and no-claim finalization before browser-run server evidence exists.
- No-claim smoke runner artifact packages with benchmark hardware, OS-control, and resource-attribution registry IDs generated by [`tools/run_benchmark_smoke.py --self-test`](../../tools/run_benchmark_smoke.py) before browser-launch benchmark evidence exists.
- No-browser browser-pin capture self-test packages generated by [`tools/capture_benchmark_browser_pins.py --self-test`](../../tools/capture_benchmark_browser_pins.py), plus the checked no-claim Chrome/Edge diagnostic summary validated by [`tools/validate_benchmark_browser_pin_diagnostics.py`](../../tools/validate_benchmark_browser_pin_diagnostics.py). The diagnostic summary is not benchmark-ready pin or comparison evidence.
- Versioned trace/artifact package contracts validated by [`tools/validate_benchmark_artifact_packages.py`](../../tools/validate_benchmark_artifact_packages.py), with runner-owned root policy, ETW or equivalent trace class, Perfetto-compatible trace class, tab lifecycle log class, required artifact classes, redaction/retention rules, prohibited-content rules, missing-proof fields, and SHA-256 manifest records.
- Versioned browser launch-runner contracts validated by [`tools/validate_benchmark_launch_runners.py`](../../tools/validate_benchmark_launch_runners.py), with required and forbidden arguments, stage coverage, timeout/cancellation policy, cache/profile policy, failure finalization, trace/artifact linkage, resource-attribution linkage, negative-test requirements, and no-claim finalization.
- A checked no-browser launch-runner self-test generated by [`tools/run_benchmark_browser_launch.py --self-test`](../../tools/run_benchmark_browser_launch.py), with command parsing, forbidden-argument rejection, registry-reference checks, artifact-root handling, hashed artifact records, and no-claim finalization before browser-run benchmark evidence exists.
- Versioned statistics-analysis contracts validated by [`tools/validate_benchmark_statistics_analysis.py`](../../tools/validate_benchmark_statistics_analysis.py), with sample design, warmup, randomization or paired order, noise study, confidence or uncertainty, effect size, outlier policy, multiple-comparison interpretation, metric-family summaries, denominator publication, and rejection rules. The checked no-claim contract is not a browser run, measured confidence interval, benchmark result, competitor result, or performance claim.
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
- JetStream — https://browserbench.org/JetStream3.0/
- MotionMark — https://browserbench.org/MotionMark/
- Web Platform Tests — https://web-platform-tests.org/
- Windows Performance Toolkit — https://learn.microsoft.com/en-us/windows-hardware/test/wpt/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
