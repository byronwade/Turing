# Benchmark Statistics Analysis Contract - July 2026

Status: checked no-claim `PB13-EV-006` statistics-analysis contract; no browser benchmark run, raw result, statistical summary, competitor result, or performance claim
Owner: performance measurement, benchmark operations, quality, security, accessibility, and release operations
Research date: 2026-07-18
Confidence: high for required analysis controls; low for benchmark readiness until runner-generated samples and owner review exist

## Question

What statistical-analysis contract must exist before future raw benchmark samples can support a Turing benchmark result, Chrome-class comparison, low-memory statement, energy statement, or public performance claim?

This report turns the current "raw results and statistics" requirement into a checked no-claim handoff. It adds [`benchmark-statistics-analysis.schema.json`](../blueprint-v1/machine/benchmark-statistics-analysis.schema.json), checked no-claim [`no-claim-statistics-analysis-plan.json`](../blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json), and [`tools/validate_benchmark_statistics_analysis.py`](../../tools/validate_benchmark_statistics_analysis.py). The contract does not run a browser, analyze measured samples, approve a threshold, or support a benchmark result.

## Inputs

Internal inputs:

- [Blueprint 09 - Performance, Memory, Energy, and the 30-Tab Contract](../blueprint-v1/09-performance-memory.md)
- [Benchmark Laboratory statistics chapter](../benchmark-lab/07-statistics-artifacts-regressions-and-claims.md)
- [Performance benchmark governance](../performance/05-benchmarks-statistics-and-regression-governance.md)
- [Performance Benchmark Readiness Packet](performance-benchmark-readiness-packet-2026-07.md)
- [Chrome-Class Performance Runbook](chrome-class-performance-runbook-2026-07.md)
- [Benchmark manifest schema](../blueprint-v1/machine/benchmark-manifest.schema.json)
- [No-claim benchmark manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json)
- [No-claim raw-artifact index fixture](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.raw-artifacts.json)
- [Benchmark trace/artifact package contract](benchmark-trace-artifact-package-contract-2026-07.md)
- [No-claim benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json)
- [No-claim public-claim bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json)
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json)
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json)

External sources already used by the benchmark program remain inputs for suite, trace, and measurement-surface selection:

- BrowserBench: https://browserbench.org/
- Chromium Telemetry: https://chromium.googlesource.com/catapult/+/HEAD/telemetry/
- Web Vitals: https://web.dev/articles/vitals
- Chrome DevTools Performance reference: https://developer.chrome.com/docs/devtools/performance/reference
- WebPageTest agent options: https://github.com/catchpoint/WebPageTest.agent/blob/master/docs/test_options.md
- Windows Performance Toolkit: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/

These sources shape measurement controls. They do not prove Turing performance.

## Current Posture

What exists:

- checked raw-result schema shape in `benchmark-manifest.schema.json`;
- checked no-claim manifest sample and raw-artifact index fixture;
- checked trace/artifact package contract;
- checked browser launch-runner contract and no-browser self-test;
- checked 30-tab scenario contract;
- checked claim-bundle template requiring raw samples, statistics, failure denominators, and owner review;
- checked benchmark readiness-review template that keeps raw result review, statistics review, denominator review, and claim-bundle review false.

What was missing before this change:

- a machine-readable statistics-analysis contract that binds `PB13-EV-006` to sample design, warmup, randomization or paired run order, noise study, confidence or uncertainty, effect size, outlier policy, multiple-comparison interpretation, metric-family summaries, denominator publication, and rejection rules;
- a focused validator that fails if those controls are removed or if the contract implies measured results;
- a research report that explains the boundary between statistics contract evidence and benchmark-result evidence.

## Contract

The checked no-claim plan requires future real analysis records to carry:

1. Runner-generated raw samples, sample order, warmup records, raw-artifact hashes, and failure records.
2. Trace and artifact package hashes for logs, traces, memory, power or energy, screenshots or video when relevant, and artifact indexes.
3. A noise study before thresholds, sample sizes, confidence intervals, and practical-impact cutoffs are accepted.
4. Denominator records for unsupported, failed, timed-out, cancelled, crashed, discarded, revived, state-loss, wrong-target, trace-finalization, cleanup, and profile-isolation cases.
5. Owner, performance, benchmark-operations, quality, security, accessibility, and release-operations review before any benchmark-ready or public-claim wording.

The contract explicitly covers latency, memory, energy, 30-tab behavior, and compatibility/failure metric families. Each family must retain units, summaries, uncertainty, effect size or practical impact where relevant, and failure denominator treatment.

## Claim Boundary

This contract is planning evidence only. It supports no browser benchmark run, no runner-generated raw sample, no real statistical summary, no confidence interval from measured browser data, no benchmark result, no competitor result, no memory result, no energy result, no Chrome-class claim, no faster claim, no lower-memory claim, no lower-energy claim, no public performance claim, no production claim, and no daily-driver claim.

Validation, no-claim templates, no-browser self-tests, smoke output, and diagnostic browser-pin captures are not benchmark results.

## Impact

The benchmark lane now has a checked bridge between raw-result schema shape and future public-claim bundles. A future runner cannot produce persuasive-looking summaries unless it also records enough analysis context to explain noise, sample count, uncertainty, effect size, outliers, failures, unsupported behavior, and denominator scope.

`PB-013` remains `documented_no_runner`. `TASK-000005` remains proposed. This change makes future benchmark evidence harder to overstate; it does not make the benchmark lab ready.

## Validation

Run:

```bash
python3 -B tools/validate_benchmark_statistics_analysis.py
python3 -B tools/validate_blueprint.py
cargo run --locked -p xtask -- check
```

A passing statistics-analysis validation proves only that the no-claim analysis contract is internally consistent and remains tied to the current benchmark registries. It does not analyze measured browser performance.
