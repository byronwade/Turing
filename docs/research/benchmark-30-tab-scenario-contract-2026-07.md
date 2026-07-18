# Benchmark 30-Tab Scenario Contract - July 2026

Status: `PB-013` sample-only scenario contract; no browser run, no benchmark result, no memory result, no energy result, no Chrome-class claim, and no performance claim
Owner: performance measurement, benchmark operations, architecture, quality, security, accessibility, and release operations
Research date: 2026-07-18
Confidence: high for scenario-shape validation; low for measurement readiness until a browser-launch runner, expanded corpus, process instrumentation, raw artifacts, and owner-reviewed hardware controls exist

## Question

Which machine-readable 30-tab mixed-state and all-live scenario records should exist before Turing builds a benchmark runner or claims Chrome-class resource behavior?

## Inputs

- [Blueprint 09 - Performance, Memory, Energy, and the 30-Tab Contract](../blueprint-v1/09-performance-memory.md)
- [Benchmark laboratory memory, process topology, and thirty-tabs chapter](../benchmark-lab/05-memory-process-topology-and-thirty-tabs.md)
- [Performance benchmark readiness packet](performance-benchmark-readiness-packet-2026-07.md)
- [Chrome-class performance runbook](chrome-class-performance-runbook-2026-07.md)
- [No-claim smoke corpus manifest](../blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json)
- [No-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json)
- [Semantic resource attribution taxonomy](../blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json)
- [Benchmark tab scenario schema](../blueprint-v1/machine/benchmark-tab-scenario.schema.json)
- [No-claim 30-tab scenario manifest](../blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json)
- [Benchmark tab scenario validator](../../tools/validate_benchmark_tab_scenarios.py)

## Method

Added a small tab-scenario schema and a sample-only scenario manifest for `PB13-EV-008`. The manifest defines two denominator-preserving scenario shapes:

- a mixed lifecycle scenario with 30 tabs across active, background, throttled, frozen, serialized, and discarded states;
- an all-live scenario with 30 live tabs and no throttled, frozen, serialized, discarded, or crashed tabs.

The records reference the checked no-claim corpus, local static network profile, and semantic resource-attribution taxonomy. The validator checks that each scenario totals exactly 30 tabs, lifecycle state counts match tab groups, corpus case IDs exist, network routes cover those cases, all-live scenarios contain only live states, mixed scenarios include serialized or discarded states, and all measurement-claim flags remain false.

## Current Evidence

The following evidence now exists:

- `benchmark-tab-scenario.schema.json` defines the sample tab-scenario manifest shape;
- `no-claim-30-tab-smoke.scenarios.json` records one mixed-state and one all-live 30-tab scenario;
- `validate_benchmark_tab_scenarios.py` validates IDs, counts, lifecycle state totals, corpus references, network-profile coverage, and no-claim wording;
- `PB-013`, the benchmark research lane, and `TASK-000005` point to the scenario contract as planning evidence.

This closes the previous documentation gap where the 30-tab workload was described in prose but had no checked machine record.

## Unsupported Conclusions

This record does not support:

- a browser benchmark run;
- a memory, CPU, GPU, wakeup, latency, energy, startup, recovery, or compatibility result;
- a comparison against Chrome, Edge, Firefox, Safari, Servo, Ladybird, or any other browser;
- a claim that discarded or serialized tabs are equivalent to all-live tabs;
- any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, beta, stable, accessibility, security, or compatibility claim.

## Remaining Proof For `PB13-EV-008`

The scenario contract remains planning evidence until a runner produces:

1. concrete tab IDs and navigation order for every tab;
2. process, renderer, site-instance, profile, origin, frame, and document-epoch identity for each tab;
3. lifecycle transition timestamps and reasons;
4. memory, CPU, GPU, wakeup, I/O, and energy attribution using the semantic-owner taxonomy;
5. revival latency, state-loss, and user-visible recovery records for frozen, serialized, and discarded tabs;
6. raw artifacts, traces, logs, screenshots when relevant, and SHA-256 manifest entries;
7. failure-denominator records for unsupported, crashed, timed-out, or cancelled tabs;
8. owner-reviewed interpretation that keeps mixed-state and all-live results separate.

## Registry Impact

This report advances `PB13-EV-008` from prose-only planning to checked no-claim scenario-manifest evidence. It does not move `PB-013` out of `documented_no_runner`.

Synchronized records:

- `pre-build-readiness.json` now lists the tab-scenario schema, manifest, validator, and report as `PB-013` evidence while keeping runner-generated 30-tab artifacts as missing proof.
- `research-readiness-crosswalk.json` and `build-readiness-task-queue.json` now route the benchmark lane and `TASK-000005` through the checked scenario manifest.
- The performance benchmark readiness packet, research index, repository map, benchmark laboratory, performance book, operating board, and documentation-readiness matrix now link the scenario contract.

## Next Actions

1. Extend the browser benchmark launch runner so it can instantiate this scenario manifest and emit a runner-managed raw artifact package.
2. Expand the corpus so 30-tab scenarios include representative documents, app-like pages, accessibility pages, media, hostile cases, service-worker cases, and international content.
3. Add process-topology and site-isolation capture to runner output.
4. Add revival and state-loss measurements for frozen, serialized, and discarded tabs.
5. Keep the no-claim boundary until Level 3 claim review in the Chrome-class performance runbook passes.
