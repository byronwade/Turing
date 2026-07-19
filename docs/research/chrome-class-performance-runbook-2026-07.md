# Chrome-Class Performance Runbook - July 2026

Status: `PB-013` evidence draft; no benchmark runner, result, competitor result, or performance claim
Owner: performance measurement, benchmark operations, quality, security, accessibility, and release operations
Research date: 2026-07-19
Confidence: medium for current suite and runbook shape; low for product readiness until hardware, corpus, runner, and raw results exist

## Question

What current primary sources and runbook rules should shape Turing's first Chrome-class and extreme-performance measurement program without allowing premature speed, memory, energy, compatibility, security, or daily-driver claims?

## Primary Sources Checked

Retrieved on 2026-07-17:

- BrowserBench Speedometer 3.1: https://browserbench.org/Speedometer3.1/
- WebKit Speedometer repository: https://github.com/WebKit/Speedometer
- BrowserBench JetStream 3.0 in-depth analysis: https://browserbench.org/JetStream3.0/in-depth.html
- WebKit JetStream repository: https://github.com/WebKit/Jetstream
- BrowserBench MotionMark: https://browserbench.org/MotionMark/
- BrowserBench MotionMark about page: https://browserbench.org/MotionMark/about.html
- Chromium Telemetry documentation: https://chromium.googlesource.com/catapult/+/HEAD/telemetry/
- Web Vitals: https://web.dev/articles/vitals
- Chrome UX Report overview: https://developer.chrome.com/docs/crux
- Chrome DevTools Performance reference: https://developer.chrome.com/docs/devtools/performance/reference
- WebPageTest agent JSON test options: https://github.com/catchpoint/WebPageTest.agent/blob/master/docs/test_options.md
- Chrome Releases: https://chromereleases.googleblog.com/

Official BrowserBench methodology refresh retrieved on 2026-07-19:

- Speedometer 3.1 methodology: https://www.browserbench.org/Speedometer3.1/about.html
- Speedometer 3.1 run instructions: https://www.browserbench.org/Speedometer3.1/instructions.html
- Speedometer 3.1 announcement: https://www.browserbench.org/announcements/speedometer3.1/
- JetStream 3.0 announcement: https://browserbench.org/announcements/jetstream3/
- JetStream 3.0 in-depth methodology: https://browserbench.org/JetStream3.0/in-depth.html
- MotionMark methodology: https://browserbench.org/MotionMark/about.html
- MotionMark developer controls: https://browserbench.org/MotionMark/developer.html

Current competitor and regression-policy sources retrieved on 2026-07-19:

- Google Chrome performance announcement: https://blog.google/chromium/a-double-victory-for-web-speed-chrome-breaks-records-again-on-speedometer-31-and-jetstream-3/
- Chromium competitive-benchmark regression policy: https://chromium.googlesource.com/chromium/src/+/main/docs/benchmark_performance_regressions.md
- JetStream 3 announcement: https://blog.google/chromium/jetstream-3-a-modern-benchmark-for-high-performance-compute-intensive-web-applications/
- Web Platform Tests documentation: https://web-platform-tests.org/

Updated release-catalog check on 2026-07-18:

- Chrome Releases: https://chromereleases.googleblog.com/
- Microsoft Edge Stable release notes: https://learn.microsoft.com/en-us/deployedge/microsoft-edge-relnote-stable-channel
- Firefox release notes: https://www.firefox.com/en-US/releases/
- Safari release notes: https://developer.apple.com/documentation/safari-release-notes/safari-26_5-release-notes
- Safari resources and Technology Preview: https://developer.apple.com/safari/resources/

These sources define useful measurement surfaces and competitor-version capture points. They do not prove anything about Turing's performance.

The checked [benchmark-source manifest](../blueprint-v1/machine/benchmark-source-manifest.json), validated by [`validate_benchmark_sources.py`](../../tools/validate_benchmark_sources.py), records the official suite, methodology, regression-policy, telemetry, compatibility, and vendor-context sources used by this runbook. It tracks measurement consequences only; it does not provide a Turing run, competitor result, statistical approval, or performance claim.

### 2026-07-19 official methodology findings

- Speedometer 3.1 is an interaction-driven web-application responsiveness diagnostic. The 3.1 release corrected harness measurement issues, so the runner must pin the exact suite version and record the harness revision. A subtest that produces no duration is a failed run, not a zero or an omitted sample. Official instructions also require a clean profile, a focused benchmark page, a quiet host, and controlled power and thermal conditions.
- JetStream 3.0 reports per-workload results and combines them with a geometric mean. Startup, worst-case, and average behavior are separately represented, with the documented first-iteration treatment; results from different JetStream versions are not comparable. Turing must retain per-workload output and never replace missing or unsupported workloads with a silently reduced aggregate.
- MotionMark warms up, adjusts drawing complexity around a target frame rate, estimates a change point, and uses bootstrap confidence intervals and a geometric mean. Frame-rate and display-refresh controls affect the result; cross-browser comparisons must normalize the target refresh rate and record viewport class, orientation, and GPU/power state.
- These controls are suite-specific validity rules. They do not make BrowserBench scores interchangeable with local corpus, trace, memory, energy, accessibility, compatibility, or Chrome-class evidence.

### 2026-07-19 competitor-performance posture

- Google reports a Chrome Speedometer 3.1 score of 61 and JetStream 3 score of 469, measured on an M5 MacBook Pro running macOS 26.0.1. This is a dated vendor-reported observation, not an independently reproduced Turing result. Any use in planning must preserve the hardware, operating-system, suite-version, and disclosure boundary rather than treating the numbers as universal targets.
- Chromium's published competitive-benchmark policy treats regressions as actionable engineering signals and names Speedometer, MotionMark, and JetStream as competitive benchmarks. Turing should adopt the useful control principle of detecting and triaging regressions, while retaining its stricter requirements for failure denominators, security settings, accessibility, recovery, resource attribution, and independent review.
- JetStream 3.0's 2026 release reinforces the version-pinning rule: older JetStream results cannot be combined with JetStream 3.0 results. The benchmark registry must therefore store the exact suite URL/revision and invalidate stale comparison records when the suite or competitor release changes.
- WPT remains the shared cross-browser compatibility corpus and provides test-runner documentation, but browser-in-browser execution cannot cover crash or hang edge cases. Compatibility planning must retain out-of-process crash/hang evidence and must not convert WPT pass rates into a Chrome-class product claim by themselves.

## Observations

BrowserBench suites remain useful diagnostics, but each measures only a slice of browser behavior:

- Speedometer 3.1 measures web-application responsiveness through simulated user actions in demo applications.
- JetStream 3.0 combines JavaScript and WebAssembly workloads and balances startup, worst-case, and average behavior across many subtests.
- MotionMark focuses on graphics animation capacity around a target frame rate and is sensitive to viewport and refresh-rate controls.

Chrome-class comparison requires more than BrowserBench scores:

- Chromium Telemetry treats performance tests as browser automation plus trace and metric collection over story sets, and calls out Web Page Replay as a way to reduce page drift.
- Web Vitals and CrUX provide field-experience context for loading, interaction, and visual stability, but CrUX reflects eligible real Chrome users on popular public destinations and is not a Turing lab result.
- Chrome DevTools exposes trace inspection, self time, total time, and event-log views that can shape trace-review expectations, but DevTools UI output is not a stable raw-artifact schema by itself.
- WebPageTest agent options show the control surface that public web performance work usually needs: runs, first/repeat view, video, bandwidth, latency, packet loss, viewport, DPR, CPU throttling, browser choice, user-agent behavior, TLS ignoring, timeline, Lighthouse, netlog, and profiler capture.
- Chrome release metadata changes frequently. Any competitor run must record exact stable/dev/canary channel, version, platform, release date, command line, profile, and security-fix posture at run time.

## Non-Goals and Unsupported Claims

This runbook does not:

- run Turing, Chrome, Edge, Firefox, Safari, Servo, Ladybird, or any other browser;
- approve a benchmark corpus or hardware tier;
- establish a fastest-browser, lower-memory, lower-energy, Chrome-class, secure, compatible, or production-ready claim;
- allow comparison between different BrowserBench versions, display refresh rates, viewport classes, process models, sandbox states, or lifecycle policies without labeling the result invalid for public claims.

## Runbook Levels

Use three levels so the project can grow evidence without overstating it.

### Level 0: Harness Smoke

Purpose: prove that schemas, validators, local static serving, and artifact hashing work.

Allowed inputs:

- no-claim local corpus fixtures;
- no browser launch or an explicitly non-browser prototype;
- one sample manifest;
- synthetic metrics that only prove harness shape.

Allowed language:

Harness smoke evidence only.

Not allowed:

- any score comparison;
- any web-compatibility or browser-performance language.

### Level 1: Local Browser Pipeline

Purpose: prove the runner can launch one browser, drive local offline corpus cases, capture raw artifacts, and classify failures.

Required controls:

- one pinned Tier M hardware manifest;
- OS image, power, thermal, display, driver, and update-control manifest;
- local static server artifact with route map and content hashes;
- browser executable path, version, channel, build profile, command line, feature flags, and profile directory hash;
- cold, warm, and repeat-view policies;
- timeout, cancellation, retry, crash, unsupported-feature, and failure-denominator rules;
- raw trace, log, screenshot/video when applicable, memory, CPU/wakeup, GPU, and artifact-index hashes.

Allowed language:

Local runner pipeline evidence.

Not allowed:

- competitor comparison;
- Chrome-class claim;
- speed, memory, energy, or compatibility headline.

### Level 2: Competitor Diagnostic Comparison

Purpose: compare Turing against current stable competitors on identical hardware and workloads, with equivalent security and lifecycle settings.

Minimum competitors:

- Chrome Stable;
- Edge Stable when available on the same platform;
- Firefox Stable;
- Safari Stable on macOS/iOS only;
- Servo or Ladybird only when the selected research question needs them and their unsupported cases remain in the denominator.

Required browser evidence:

- product name, channel, version, build date when available, executable hash when locally practical, command line, profile source, update state, extension state, energy/memory-saving settings, site-isolation and sandbox settings, process count, cache state, and user-agent policy;
- Chrome runs must record the release blog entry or equivalent channel metadata current on the run date;
- non-Chrome browsers must record equivalent official release metadata before comparison.

Required workloads:

- local offline corpus startup, navigation, input, scroll, 30-tab mixed-state, and 30-tab all-live scenarios;
- Speedometer 3.1 only after the browser under test can run the suite without invalid subtest failures;
- JetStream 3.0 only after JavaScript and WebAssembly behavior is in scope for the tested browser;
- MotionMark only after rendering/compositing and display-refresh controls are in scope;
- Web Vitals-style page-stage and interaction metrics on the local corpus, reported as lab metrics and not CrUX field data.

Allowed language:

Diagnostic comparison on named hardware, named versions, named workloads, and named limitations.

Not allowed:

- public fastest, lower-memory, lower-energy, or Chrome-class claim.

### Level 3: Public Claim Candidate

Purpose: produce an owner-reviewed bundle that may support a narrow public performance claim.

Required evidence bundle:

- Level 2 artifacts for at least Tier L, Tier M, and Tier H hardware or an explicit narrower platform claim;
- reviewed representative offline corpus and selected live/replay corpus policy;
- raw samples, runner-generated trace package with ETW or equivalent traces, Perfetto-compatible traces where applicable, logs, screenshots/video where relevant, memory snapshots, power/energy artifacts, process topology, and artifact hashes;
- owner-reviewed statistics analysis beyond the checked no-claim statistics-analysis contract, including statistical method, sample count, warmup policy, randomization or paired order, outlier policy, confidence intervals or uncertainty statements, effect size, multiple-comparison interpretation, metric-family summaries, and failure denominator;
- equal-security and equal-workload statement;
- accessibility, recovery, DevTools, extension, profile, and agent overhead included when the claim touches those workflows;
- claim owner, reviewer, expiration date, rerun triggers, supported platform, unsupported behavior, and public wording.

Allowed language:

Only the exact owner-approved claim text.

Not allowed:

- broad browser leadership statements from a single suite;
- claims that hide crashes, unsupported APIs, disabled mitigations, tab discarding, unequal cache state, unequal lifecycle state, or unequal process/security settings.

## Synthetic Suite Rules

| Suite | Required before use | Reported as | Invalidates public claim if |
|---|---|---|---|
| Speedometer 3.1 | exact URL or mirrored asset hash, viewport at least required size, no missing-duration subtests, browser settings recorded, repetitions recorded | web-app responsiveness diagnostic | suite version differs across browsers, subtests fail silently, viewport differs, or failures are removed from denominator |
| JetStream 3.0 | exact URL or mirrored asset hash, JavaScript/Wasm runtime in scope, per-workload output retained, unsupported workloads classified | JS/Wasm diagnostic | compared against another JetStream version, shell/browser modes mixed without labeling, or runtime unsupported cases are hidden |
| MotionMark 1.3.x | exact served version, viewport class, display refresh rate, orientation, screen sleep disabled, repetitions recorded | graphics animation diagnostic | refresh rate, viewport class, orientation, or GPU/power state differs across browsers |
| Web Vitals-style lab metrics | local corpus steps, event timing source, LCP/INP/CLS-style definitions, raw events, browser lifecycle state | local lab user-experience diagnostic | reported as CrUX field data, mixed with real-user data, or captured on non-equivalent pages |

## Competitor Version Pinning

Each competitor run must include:

- browser name, channel, exact version, platform, architecture, and release date source;
- executable path and hash where practical;
- command line and environment variables;
- profile directory source, extension state, sync/account state, and feature flags;
- update status before and after run;
- security, sandbox, site isolation, JIT, cache, lifecycle, power, memory saver, energy saver, and background-throttling settings;
- reason if a setting differs from default.

Chrome and Edge cannot be treated as static competitors because release trains and security fixes move quickly. A result expires automatically when the tested competitor channel receives a stable update, when benchmark suite versions change, when hardware/driver/OS images change, or after 30 days, whichever comes first.

The checked [current desktop release-candidate competitor-version manifest](../blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json) records official release-catalog observations for Chrome Stable, Edge Stable, Firefox Stable, Safari Stable, and Safari Technology Preview. It is release-catalog evidence only. It does not record local executable paths, hashes, profiles, command lines, settings, update state, or benchmark output, and it cannot support a comparison claim.

The checked [current Windows high-end competitor local-install manifest](../blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json) records local Chrome and Edge executable paths, hashes, signatures, registry observations, and version-state caveats. It is executable-inventory evidence only. Chrome local metadata is inconsistent across executable, BLBeacon, uninstall, and version-directory observations, while Edge local metadata is newer than the recorded Stable release catalog and has an unresolved channel/update-state question. The manifest does not record browser-reported versions, profiles, command lines, settings, update state before and after a run, benchmark output, or comparison evidence.

The checked [current Windows high-end browser-pin capture plan](../blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json) defines how a runner must capture browser-reported versions and effective settings without touching real user profiles. It requires temporary profiles under a runner-owned `%TEMP%` root, rejects real profile paths, runs offline by default, prohibits account/sync attachment, records cleanup and artifact hashes, and keeps failed or blocked captures in the denominator. The companion [`tools/capture_benchmark_browser_pins.py --self-test`](../../tools/capture_benchmark_browser_pins.py) path validates temp-profile cleanup, prohibited configured-path rejection, artifact hashes, and no-claim metadata without launching a browser. The checked [Chrome/Edge browser-pin diagnostic capture](benchmark-browser-pin-local-diagnostic-capture-2026-07.md) records no-claim current-host browser-reported versions from isolated temporary profiles, but it is unreviewed diagnostic evidence only and no pin is benchmark-ready.

The checked [Benchmark trace/artifact package contract](benchmark-trace-artifact-package-contract-2026-07.md) records the package-root, trace, artifact-class, redaction, retention, prohibited-content, unsupported-behavior, and missing-proof requirements for `PB13-EV-007`. It is a no-claim contract only. Level 1 or higher evidence still requires a runner-generated trace package with ETW or equivalent traces, Perfetto-compatible traces where applicable, raw samples, failure records, memory/power artifacts, redaction review, and SHA-256 manifests.

The checked [Benchmark browser launch-runner contract](benchmark-browser-launch-runner-contract-2026-07.md) records the planned command path, required and forbidden arguments, stage contract, timeout/cancellation policy, cache/profile policy, failure finalization, trace/artifact policy, and no-claim finalization requirements for `PB13-EV-005`. The companion [`tools/run_benchmark_browser_launch.py --self-test`](../../tools/run_benchmark_browser_launch.py) path is a checked no-browser browser launch-runner self-test for command parsing, forbidden arguments, registry references, artifact-root handling, and no-claim finalization. Both are no-claim evidence only. Level 1 or higher evidence still requires an implemented browser launch runner, reviewed browser pins, runner-managed server artifacts, real browser-run artifacts, negative tests, timeout/cancellation behavior, cleanup records, and result finalization.

The checked [Benchmark statistics analysis contract](benchmark-statistics-analysis-contract-2026-07.md) records the sample-design, warmup, randomization or paired order, noise-study, uncertainty, effect-size, outlier, multiple-comparison, metric-family, denominator, and rejection requirements for `PB13-EV-006`. It is a checked no-claim statistics-analysis contract only. Level 3 evidence still requires runner-generated raw samples and owner-reviewed statistics analysis before any public performance, Chrome-class, faster, lower-memory, lower-energy, or competitor-result claim can be considered.

## Claim Expiry Policy

Every candidate public performance claim must include:

- claim ID;
- owner and reviewer;
- exact claim text;
- supported hardware tiers and operating systems;
- competitor versions and dates;
- workload and suite versions;
- raw artifact bundle hash;
- unsupported behavior and failure denominator;
- expiration date;
- rerun triggers.

Default expiry:

- 30 days for competitor comparison claims;
- 14 days for claims tied to active nightly/dev/canary competitors;
- immediate expiry when a security, sandbox, lifecycle, benchmark, corpus, hardware, driver, OS, or browser-version input changes;
- immediate expiry when an unsupported or failed case is found to have been omitted from the denominator.

Expired claims must be removed from public docs, release notes, website copy, README files, issue templates, benchmark dashboards, and market material until rerun evidence exists.

The checked no-claim [claim-bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json), validated by [`validate_benchmark_claim_bundles.py`](../../tools/validate_benchmark_claim_bundles.py), is the current machine-readable shape for a future Level 3 owner-reviewed claim bundle. It binds claim text, owner and reviewer scopes, benchmark manifest, hardware, OS control, corpus, network profile, resource attribution, tab scenarios, trace package, statistics-analysis plan, browser launch runner, browser pins, competitor manifests, statistical controls, equivalence controls, denominator controls, overhead controls, expiry, publication rules, and rejection rules. The validator cross-checks the `statistics_analysis_plan_id` against the checked no-claim statistics-analysis plan before any claim text can be reviewed. It is a template only: no public claim is approved.

## Required Registry Impact

The [Benchmark Competitor Runbook Examples](benchmark-competitor-runbook-examples-2026-07.md) provides sample-only Chrome Stable and Firefox Stable records for the identity, lab, workload, collection, outcome, and review fields below. It is a documentation example only; it does not satisfy any `PB13-EV-*` execution or review requirement.

This report advances `PB13-EV-009` and `PB13-EV-010` from generic partial evidence to documented runbook evidence. It does not move `PB-013` out of `documented_no_runner`.

The remaining `PB-013` implementation blockers are:

- Tier L and Tier M hardware manifests plus owner-reviewed approval or replacement of the current Tier H candidate;
- approved clean OS image and update-control manifests for every selected tier; the current Tier H OS-control candidate is inventory evidence only;
- reviewed representative offline corpus beyond the expanded generated no-claim seed;
- runner-managed local server artifact;
- implemented browser benchmark launch runner;
- runner-generated raw result files;
- runner-generated trace package with ETW or equivalent traces, Perfetto-compatible traces where applicable, logs, screenshots, memory snapshots, power data, raw samples, failure records, redaction review, retention decision, and SHA-256 manifest;
- runner-generated 30-tab mixed/all-live raw artifacts from the checked no-claim scenario manifest;
- owner-reviewed statistics analysis beyond the checked no-claim statistics-analysis contract;
- semantic resource attribution;
- owner-reviewed benchmark-ready browser pins plus locally pinned competitor-version manifests with isolated browser-reported versions, channel proof, profiles, settings, and command lines; the current release-catalog, local executable, capture-plan, browser-pin no-browser self-test, launch-runner no-browser self-test, and no-claim Chrome/Edge diagnostic artifacts are only candidate evidence;
- accessibility, recovery, DevTools, and agent workload fixtures;
- owner-reviewed claim bundle generated from actual results beyond the checked no-claim claim-bundle template.

## Next Actions

1. Add competitor-runbook examples for Chrome Stable and Firefox Stable using sample-only records.
2. Capture Tier M and Tier L hardware manifests and decide whether the current Tier H candidate is approved or replaced.
3. Define approved clean OS image and update-control manifests for each approved hardware tier.
4. Owner-review the no-claim Chrome/Edge browser-pin diagnostic artifacts, fill channel/settings evidence, then extend the checked browser launch-runner contract and checked no-browser browser launch-runner self-test into an implemented browser launch runner that can produce Level 1 evidence.
5. Extend the checked no-claim statistics-analysis contract into owner-reviewed analysis only after runner-generated raw samples, noise-study, uncertainty, denominator, and practical-impact evidence exists.
6. Keep every output labeled no-claim until Level 3 owner review passes.
