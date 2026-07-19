# Benchmark Evidence and Claim Closure Preparation - July 2026

Status: no-claim execution and claim-review route for `PB-013` and `TASK-000005`; no browser-run result, competitor result, or public performance claim has been accepted
Owner: performance measurement, benchmark operations, quality, security, accessibility, release operations, and independent review
Research date: 2026-07-19

## Question

What evidence transition separates benchmark infrastructure self-tests, browser-run diagnostics, competitor comparisons, and public Chrome-class or extreme-performance claims?

## Current boundary

The repository has a performance readiness packet, Chrome-class runbook, benchmark-lab lane map, fixed-hardware and OS-control candidates, corpus/network/tab/artifact/launch-runner contracts, browser-pin capture plans, competitor inventories, a statistics-analysis contract, and no-claim readiness/claim-bundle templates. These records define the evidence shape. They do not run Turing or a competitor, establish a benchmark-ready browser pin, prove equal workload/security/lifecycle conditions, or support faster, lower-memory, lower-energy, Chrome-class, or daily-driver claims.

The [Benchmark Claim-Bundle Examples](benchmark-claim-bundle-examples-2026-07.md) adds a fictitious human-facing handoff for exact claim wording, evidence hashes, metric and denominator reconciliation, equivalence and safety review, expiry, rerun triggers, publication controls, and rejection rules. It is sample-only and does not satisfy `PB-013` evidence.

The checked [benchmark-source manifest](../blueprint-v1/machine/benchmark-source-manifest.json), validated by [`validate_benchmark_sources.py`](../../tools/validate_benchmark_sources.py), keeps official suite methodology, regression-policy, telemetry, compatibility, and vendor-context observations linked to this closure route. It does not supply a browser run, competitor result, statistics approval, or claim evidence.

## Host-trace integrity boundary

Microsoft's [Windows Performance Recorder guidance](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr) describes WPR/ETW recordings for system and application behavior and resource usage. Microsoft's [ETW overview](https://learn.microsoft.com/en-us/windows/win32/etw/about-event-tracing) separates controllers, providers, and consumers and makes session, buffer, and provider configuration part of the capture model.

For the Windows reference tier, a real L1/L2 package must retain WPR/WPA or equivalent tool identity, profile, start/stop commands, privilege and host controls, provider/session configuration, buffer and event-loss indicators, clock/timestamp facts, process/thread attribution, ETL hash, analysis tool/version, and an explicit missing-event policy. A trace file's existence is not proof that the required events were captured, and a host trace does not replace browser-reported version, workload, lifecycle, security, or failure-denominator evidence.

### Observer-effect and instrumentation boundary

Perfetto's [trace configuration documentation](https://perfetto.dev/docs/concepts/config) makes data sources, buffers, duration, and collection configuration part of the trace definition. Fine-grained browser counters, ETW/WPR providers, Perfetto data sources, memory samplers, and diagnostic logging can change CPU time, wakeups, allocation, cache behavior, queue pressure, latency, thermal state, or energy. A trace-enabled run is therefore a diagnostic condition, not automatically the same condition as a headline performance run.

For every instrumented run, retain an otherwise equivalent no-trace control with the same source/build identity, host image, workload, profile, security and lifecycle settings, warmup, ordering, sample count, and failure denominator. Record the trace configuration, provider/data-source set, buffer sizes, sampling intervals, event-loss indicators, capture duration, collector/analyzer versions, and artifact hashes. Report the measured delta for startup, interaction tails, CPU, wakeups, memory, GPU, and energy where the instrumentation can affect them. If the control and instrumented conditions are not comparable, the result remains diagnostic-only and cannot support a speed, memory, energy, or Chrome-class claim.

## Evidence levels

| Level | Allowed evidence | Required transition proof | Claims prohibited |
|---|---|---|---|
| L0: contract/self-test | Schema, manifest, parser, server, capture, runner, or cleanup self-test without a browser run | Validator output and no-claim artifact package | Any browser, competitor, speed, memory, energy, compatibility, or Chrome-class claim |
| L1: local browser pipeline | One browser on fixed declared host with local corpus, runner-managed server, raw artifacts, traces, failures, and cleanup | Browser-reported pin/settings, exact corpus/network/runner versions, raw hashes, full denominator, and owner acceptance of diagnostic scope | Competitor comparison or public performance headline |
| L2: competitor diagnostic | Turing and pinned Chrome/Edge/Firefox/Safari candidates on identical hardware/workload and disclosed security/lifecycle/profile/cache settings | Complete local executable/browser-reported pins, equal-workload matrix, all failure/unsupported rows, raw samples/traces/resource attribution, and review of validity | Public fastest, lower-memory, lower-energy, Chrome-class, compatibility leadership, or production claim |
| L3: public claim candidate | Reviewed L2 data across declared hardware tiers and representative workloads with statistics and claim bundle | Owner/independent review, uncertainty and effect size, failure denominator, expiry/rerun triggers, supported/unsupported scope, and exact wording | Claims outside the reviewed wording, platform, date, workload, or metric family |

Advancing a level requires retained evidence from the preceding level. A passing self-test is not a browser-run result, a browser-run result is not a competitor comparison, and a comparison is not a public claim.

## Required execution sequence

1. **Freeze the measurement identity.** Record source commit/build ID, browser executable and reported version/channel, platform/architecture, hardware tier, OS/update/driver/firmware state, display/refresh/viewport/DPR, power/thermal/network controls, process/site-isolation and tab-lifecycle settings, profile/cache/extension state, benchmark suite/corpus/network/runner versions, and artifact root.
2. **Validate runner and environment controls.** Run the checked self-tests for browser-pin capture, server lifecycle, launch arguments, artifact roots, corpus/routes, tab scenarios, resource attribution, and statistics-plan parsing. Keep these as L0 evidence and preserve failures.
3. **Execute L1 with a browser.** Launch through the reviewed runner, serve the declared corpus, capture browser-run traces and raw results, record memory/CPU/GPU/energy where applicable, classify every failure and unsupported operation, hash the artifact package, and verify cleanup and source/profile isolation.
4. **Review L1 before comparing.** Reject incomplete browser pins, real-user-profile use, hidden flags, missing traces, missing failure rows, uncontrolled server lifecycle, mismatched suite versions, discarded failures, or unreviewed artifact redaction.
5. **Execute L2 paired diagnostics.** Run Turing and each competitor in randomized or paired order on the same approved image and workload. Capture browser-reported settings, executable/hash/signature, update/channel state, command line, process topology, security/site-isolation/lifecycle settings, raw samples, traces, resource attribution, and unsupported behavior for every participant.
6. **Analyze without silent reduction.** Retain per-workload and per-sample results. Apply the declared warmup, randomization, outlier, uncertainty, effect-size, multiple-comparison, geometric-mean, and missing/failed-sample rules. A missing subtest is failed/unsupported, never zero and never silently omitted from an aggregate.
7. **Review claim scope.** For L3, attach exact claim text, metric family, hardware/OS, workload, competitor versions, artifact hash, owner/reviewer identities, expiry, rerun triggers, limitations, and unsupported behavior. Include accessibility, recovery, DevTools, extension, profile, and agent overhead when the claim touches those workflows.

## Rejection rules

- Do not use local diagnostic browser pins as benchmark-ready pins until browser-reported version, effective settings, profile isolation, command line, update state, and cleanup are retained and reviewed.
- Do not compare release-catalog observations with a local executable as though both were run-time pins.
- Do not mix BrowserBench versions, hardware/driver/OS images, refresh rates, viewport classes, security settings, process models, tab-discard policies, cache/profile states, or competitor channels without invalidating the comparison or narrowing its scope.
- Do not call a benchmark faster, smaller, lower-energy, more compatible, safer, or Chrome-class from a single score, geometric mean, screenshot, or self-test.
- Do not hide failed, blocked, unsupported, timed-out, or incomplete runs; all attempted operations remain in the denominator.
- Do not retain real profiles, accounts, sync state, credentials, or secrets in benchmark artifacts.
- Do not let benchmark instrumentation, browser flags, network shaping, or runner behavior grant capabilities unavailable in the claimed product configuration.

## Review package

The owner-reviewed package must bind these artifacts by hash:

- host/hardware/OS-control and clean-image records;
- browser and competitor version/local-install/browser-reported pin records;
- suite, corpus, network, tab, launch-runner, artifact-package, and resource-attribution manifests;
- raw samples, traces, screenshots/video where relevant, memory/power/energy data, process topology, and failure records;
- statistics-analysis plan, executed analysis, uncertainty/effect-size output, and denominator report;
- redaction/retention review, cleanup proof, claim bundle, reviewer identities, expiry, rerun triggers, and unsupported cases.

`PB-013` remains `partial`. `TASK-000005` remains proposed-only. No report, manifest, browser-pin diagnostic, runner self-test, benchmark score, or statistics template authorizes a public performance or Chrome-class claim.

## Source observations and retrieval record

Retrieved 2026-07-19. These are method observations only; they are not Turing or competitor results, benchmark approvals, or performance claims.

| Source | Version or revision observed | Platform/configuration relevance | Observation retained for the benchmark contract |
|---|---|---|---|
| [Speedometer 3.1 instructions](https://www.browserbench.org/Speedometer3.1/instructions.html) and [about page](https://www.browserbench.org/Speedometer3.1/about.html) | Speedometer 3.1; browser page and instructions observed 2026-07-19 | BrowserBench web workload; device focus and viewport affect execution | Use a clean browser profile, close other tabs/windows, keep the benchmark focused, avoid background work, control charging/thermal state, and record viewport/configuration before comparing runs. |
| [Chromium Catapult Telemetry](https://chromium.googlesource.com/catapult/+/c5f59e09450378c12dfae7f14fbffc07204e1f78/telemetry/) | Catapult `c5f59e09450378c12dfae7f14fbffc07204e1f78` observed from the `HEAD` tree | Cross-platform browser automation and trace-based measurement | Separate browser launching, story/workload definition, measurement, and trace-derived metric computation; retain the trace because it supports later metric analysis and diagnosis. |
| [Telemetry local benchmark instructions](https://chromium.googlesource.com/catapult/+/c5f59e09450378c12dfae7f14fbffc07204e1f78/telemetry/docs/run_benchmarks_locally.md) | Same Catapult revision; local-run instructions observed 2026-07-19 | Windows requires platform-specific setup; exact browser executables and repeat counts are configurable | Record the exact executable/browser pin and runner options; repeated pageset execution is an input to the experiment, not evidence by itself. |
| [Microsoft Windows Performance Recorder introduction](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr) | Microsoft WPR documentation retrieved 2026-07-19 | Windows ETW capture and WPA analysis | Use OS-level traces as a separate artifact family for system/application behavior and resource usage; bind trace version, host controls, collection interval, and artifact hash to the run. |
| [Perfetto trace configuration](https://perfetto.dev/docs/concepts/config) | Perfetto documentation retrieved 2026-07-19 | Browser and system trace configuration | Retain data sources, buffers, duration, clocks, loss indicators, collector/analyzer versions, and a no-trace control so instrumentation overhead is not mistaken for product behavior. |

Before any L1 or L2 execution, replace mutable `HEAD` or website references with exact suite/tool revisions, browser executable hashes and reported versions, host/OS/driver state, workload/corpus hashes, and the tested configuration. The observations above refine the evidence contract only; they do not make `PB-013` ready or support a Chrome-class claim.

## PB-020 closure dependency

Any future `PB-013` readiness or claim decision must be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and the [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md) route. A browser-run result, competitor comparison, statistics analysis, claim bundle, or benchmark readiness review cannot independently close `PB-020`, establish faster/lower-memory/lower-energy leadership, authorize public performance claims, or support production, compatibility, security, accessibility, or Chrome-class claims. The final closure record must preserve runner and browser pins, workload equivalence, raw artifacts, failure denominators, statistics, reviewer identities, scope, expiry, rerun triggers, and synchronized support and release boundaries.

## Next controlled action

Prepare a reviewed immutable `TASK-000005` manifest for an L1 browser-run pipeline using a declared no-real-profile browser pin, fixed host controls, local corpus, runner-managed server, raw artifact package, failure denominator, and cleanup evidence. Do not begin L2 comparison until L1 is reviewed and reproducible.
