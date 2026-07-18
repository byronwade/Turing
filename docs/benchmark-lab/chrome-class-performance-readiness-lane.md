# Chrome-Class and Extreme-Performance Readiness Lane

Status: operational evidence lane map (no public performance claim)
Owner: performance, security, measurement, compatibility, and buildout teams
Last updated: 2026-07-18

This document is the compact map for the project’s “competitor-to-Chrome + extreme-performance” objective while no public performance claim is yet allowed. It exists so any continuation session can see exactly what is proven, what is planned, and what evidence is still missing before `PB-013` can progress toward readiness promotion.

## Goal and non-goal

### Goal

Establish reproducible, fixed-hardware, claim-grade evidence for startup, memory, energy, frame behavior, tab-pressure durability, and competitive comparison without weakening security, compatibility, accessibility, or release controls.

### Non-goal (today)

- claim “faster/lower-memory/lower-energy/chrome-equivalent” from template artifacts only;
- implying daily-driver status from corpus or self-test output;
- publishing benchmark results without independent statistics analysis and claim-review evidence.

## Current evidence state (`PB-013` lane)

- Hardware and platform controls are tracked by:
  - [Benchmark hardware and OS manifest](../research/benchmark-hardware-os-manifest-2026-07.md)
  - [Benchmark OS and update-control manifest](../research/benchmark-os-update-control-manifest-2026-07.md)
  - [Benchmark competitor version manifest](../research/benchmark-competitor-version-manifest-2026-07.md)
  - [Benchmark competitor local install inventory](../research/benchmark-competitor-local-install-inventory-2026-07.md)
- Tooling and contracts are in place for no-claim execution planning:
  - [Performance benchmark readiness packet](../research/performance-benchmark-readiness-packet-2026-07.md)
  - [Benchmark corpus expansion](../research/benchmark-corpus-expansion-2026-07.md)
  - [Benchmark server lifecycle self-test](../research/benchmark-server-lifecycle-self-test-2026-07.md)
  - [Benchmark browser launch-runner contract](../research/benchmark-browser-launch-runner-contract-2026-07.md)
  - [Benchmark browser-pin and comparator capture contracts](../research/benchmark-browser-pin-capture-contract-2026-07.md)
  - [Benchmark browser pin local diagnostic capture](../research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md)
  - [Benchmark 30-tab scenario contract](../research/benchmark-30-tab-scenario-contract-2026-07.md)
  - [Benchmark trace/artifact package contract](../research/benchmark-trace-artifact-package-contract-2026-07.md)
  - [Benchmark statistics analysis contract](../research/benchmark-statistics-analysis-contract-2026-07.md)
  - [Benchmark engine baseline harness readiness map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md)
  - [Chrome-class performance runbook](../research/chrome-class-performance-runbook-2026-07.md)
  - [No-claim benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json)
  - [No-claim claim-bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json)
- Validators and self-tests exist and run through no-claim schemas, but do not imply implemented performance.

## Deep research progression plan

Treat each phase as a blocker to the next phase, and only one evidence class may carry a positive claim at a time.

### Phase 1 — Fixed-hardware baseline control

- lock and validate candidate hardware/OS control state;
- retain runner setup and server lifecycle outputs;
- preserve browser-pin capture diagnostics.
- required evidence: validated manifests + clean-room artifact checksums.

### Phase 2 — Workload and infrastructure parity

- keep benchmark corpora aligned with the target browser-state matrix;
- run network profile and local static profiles against all test classes;
- validate 30-tab mixed-state and all-live scenarios at equal workload scales;
- keep no-browser launcher self-test artifacts and server lifecycle outputs for pipeline continuity.

### Phase 3 — Browser-run instrumentation and raw result capture

- execute browser launch runner(s) on fixed hardware;
- capture raw traces/artifacts with redaction and retention constraints;
- retain failure, timeout, cancellation, and resource-attribution logs in machine-checked form;
- connect competitor pin diagnostics to benchmark runs.

### Phase 4 — Statistics and claim gating

- complete reviewed statistics-analysis execution;
- publish owner-approved evidence for uncertainty, denominators, outliers, and rejection rules;
- prepare claim bundles with explicit competitor-result and unsupported-case boundary;
- run explicit claim-review before any public statement.

## Missing proof before any claim can graduate

- no owner-approved hardware tier closure;
- no browser-run results for startup, memory, energy, tab-pressure, latency/throughput, and process-attribution;
- no owner-reviewed statistics analysis for equivalent workload outcomes;
- no accepted benchmark readiness review or claim bundle;
- no validated claim-expiry governance with ownership and release constraints.

## Direct control map

- Primary gate: `PB-013` in [implementation-kickoff review](../project-buildout/machine/implementation-kickoff-review.json).
- Primary task: `TASK-000005` in [build-readiness task queue](../project-buildout/17-build-readiness-task-queue.md).
- Primary validators include the entire benchmark validation chain in:
  - [Documentation readiness evidence matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md)
  - `tools/validate_benchmark_manifests.py`
  - `tools/validate_benchmark_hardware.py`
  - `tools/validate_benchmark_os_controls.py`
  - `tools/validate_benchmark_resource_attribution.py`
  - `tools/validate_benchmark_competitor_versions.py`
  - `tools/validate_benchmark_competitor_local_installs.py`
  - `tools/validate_benchmark_browser_pin_capture.py`
  - `tools/validate_benchmark_browser_pin_diagnostics.py`
  - `tools/validate_benchmark_corpus.py`
  - `tools/validate_benchmark_network_profile.py`
  - `tools/validate_benchmark_tab_scenarios.py`
  - `tools/validate_benchmark_artifact_packages.py`
  - `tools/validate_benchmark_launch_runners.py`
  - `tools/validate_benchmark_readiness_review.py`
  - `tools/validate_benchmark_statistics_analysis.py`

## Claim boundary

This lane is for preparation and continuity only. It does not authorize any public performance headline, compatibility parity claim, Chrome-class claim, release claim, production claim, or implementation claim.
