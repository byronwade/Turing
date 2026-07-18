# Benchmark Trace/Artifact Package Contract - July 2026

Status: `PB-013` sample-only artifact-package contract; no browser run, no benchmark result, no trace captured, no memory result, no energy result, no Chrome-class claim, and no performance claim
Owner: performance measurement, benchmark operations, security, privacy, quality, release operations, and developer experience
Research date: 2026-07-18
Confidence: high for package-shape validation; low for measurement readiness until a browser-launch runner emits real traces, raw samples, redaction-reviewed artifacts, and owner-reviewed retention records

## Question

Which trace and artifact package records should exist before Turing builds a benchmark runner or stores benchmark evidence that could later support Chrome-class performance claims?

## Inputs

- [Blueprint 09 - Performance, Memory, Energy, and the 30-Tab Contract](../blueprint-v1/09-performance-memory.md)
- [Benchmark laboratory statistics, artifacts, regressions, and claims chapter](../benchmark-lab/07-statistics-artifacts-regressions-and-claims.md)
- [Performance benchmark readiness packet](performance-benchmark-readiness-packet-2026-07.md)
- [Chrome-class performance runbook](chrome-class-performance-runbook-2026-07.md)
- [Benchmark manifest schema](../blueprint-v1/machine/benchmark-manifest.schema.json)
- [No-claim benchmark manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json)
- [No-claim raw-artifact index sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.raw-artifacts.json)
- [No-claim 30-tab scenario manifest](../blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json)
- [Benchmark artifact-package schema](../blueprint-v1/machine/benchmark-artifact-package.schema.json)
- [No-claim trace/artifact package plan](../blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json)
- [Benchmark artifact-package validator](../../tools/validate_benchmark_artifact_packages.py)

## Method

Added a small artifact-package schema and sample-only package plan for `PB13-EV-007`. The contract links the current no-claim benchmark manifest, raw-artifact placeholder index, Tier H hardware candidate, OS-control candidate, smoke corpus, local static network profile, semantic resource-attribution taxonomy, and 30-tab scenario manifest.

The validator checks that the package remains sample-only, preserves no-claim wording, references the current no-claim registries, requires a runner-owned artifact root, prohibits real profile access, defines ETW or equivalent trace capture, defines Perfetto-compatible or equivalent browser trace capture, requires tab lifecycle trace records, lists required artifact classes, requires SHA-256 manifest records, and keeps real trace/raw-artifact proof marked missing.

## Current Evidence

The following evidence now exists:

- `benchmark-artifact-package.schema.json` defines the trace/artifact package contract shape;
- `no-claim-trace-package.plan.json` records the package-root, trace, artifact-class, redaction, retention, prohibited-content, unsupported-behavior, and missing-proof requirements;
- `validate_benchmark_artifact_packages.py` validates references to the current no-claim hardware, OS-control, corpus, network, resource-attribution, tab-scenario, benchmark-manifest, and raw-artifact-index records;
- `PB-013`, the benchmark research lane, and `TASK-000005` point to the artifact-package contract as planning evidence.

This closes the previous documentation gap where `PB13-EV-007` named traces and artifact packages but had no checked machine-readable package contract.

## Unsupported Conclusions

This record does not support:

- a browser benchmark run;
- an ETW, WPR, WPA, Perfetto, browser-internal, memory, power, energy, screenshot, video, raw-sample, or real artifact bundle;
- a comparison against Chrome, Edge, Firefox, Safari, Servo, Ladybird, or any other browser;
- a claim that the current raw-artifact placeholder index is a real benchmark artifact store;
- any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, beta, stable, accessibility, security, compatibility, or benchmark-ready claim.

## Remaining Proof For `PB13-EV-007`

The package contract remains planning evidence until a runner produces:

1. runner-generated trace and artifact package root with SHA-256 manifest;
2. ETW or equivalent Windows trace and Perfetto-compatible browser trace where applicable;
3. runner logs, browser stdout/stderr, environment manifest, and failure denominator records;
4. raw samples, memory snapshots, CPU/GPU counters, power or energy samples, screenshots when relevant, and redaction review;
5. 30-tab lifecycle log with concrete tab IDs, navigation order, process topology, site-instance identity, lifecycle transition timestamps, revival measurements, and state-loss records;
6. owner-reviewed retention, publication, privacy, and claim-bundle decision.

## Registry Impact

This report advances `PB13-EV-007` from unstructured missing proof to checked no-claim trace/artifact package contract evidence. It does not move `PB-013` out of `documented_no_runner`.

Synchronized records:

- `pre-build-readiness.json` now lists the artifact-package schema, plan, validator, and report as `PB-013` evidence while keeping runner-generated trace packages as missing proof.
- `research-readiness-crosswalk.json` and `build-readiness-task-queue.json` now route the benchmark lane and `TASK-000005` through the checked artifact-package plan.
- The performance benchmark readiness packet, research index, repository map, benchmark laboratory, performance book, operating board, and documentation-readiness matrix now link the artifact-package contract.

## Next Actions

1. Extend the benchmark runner so every run writes artifacts to a runner-owned package root and emits a SHA-256 artifact index.
2. Add trace collectors for Windows ETW or equivalent host traces and Perfetto-compatible or equivalent browser traces.
3. Add redaction review for trace providers, paths, command lines, screenshots, logs, and process metadata.
4. Connect raw samples, tab lifecycle logs, memory/power data, and failure denominator records to the package index.
5. Keep the no-claim boundary until Level 3 claim review in the Chrome-class performance runbook passes.
