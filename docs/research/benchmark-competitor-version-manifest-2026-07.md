# Benchmark Competitor Version Manifest - July 2026

Status: `PB13-EV-009` release-catalog evidence; no local browser pins, benchmark output, competitor result, or performance claim
Owner: performance measurement, benchmark operations, release operations, and quality
Research date: 2026-07-19
Confidence: high for official release-catalog observations at retrieval time; low for benchmark readiness until local installed browser pins and runner artifacts exist

## Question

Which current official browser release catalogs should seed Turing's first competitor-version registry before any Chrome-class, fastest, lower-memory, lower-energy, compatibility, security, or production claim is allowed?

This report does not inspect a local browser executable, run a benchmark, choose a comparison platform, or support a ranking. It records release-catalog candidates only so future benchmark manifests can distinguish current vendor metadata from local installed-browser evidence.

## Primary Sources Checked

Retrieved and rechecked on 2026-07-19:

- Chrome Releases: https://chromereleases.googleblog.com/
- Microsoft Edge Stable release notes: https://learn.microsoft.com/en-us/deployedge/microsoft-edge-relnote-stable-channel
- Firefox release notes: https://www.firefox.com/en-US/releases/
- Safari 26.5 release notes: https://developer.apple.com/documentation/safari-release-notes/safari-26_5-release-notes
- Safari resources and Technology Preview: https://developer.apple.com/safari/resources/
- BrowserBench Speedometer 3.1: https://browserbench.org/Speedometer3.1/
- BrowserBench JetStream 3.0 in-depth analysis: https://browserbench.org/JetStream3.0/in-depth.html
- BrowserBench MotionMark: https://browserbench.org/MotionMark/

## Observations

- Chrome Releases reported a Stable Channel Update for Desktop on 2026-07-16 with `150.0.7871.128/.129` for Windows and macOS and `150.0.7871.128` for Linux.
- Microsoft Edge Stable release notes listed latest major version `150` and latest minor version `150.0.4078.83` on 2026-07-17.
- Firefox release notes listed Firefox `152.0.0` with patch releases through `152.0.6` at retrieval time.
- Apple Developer release-note search metadata identified Safari `26.5 (20624.2.5)`, released 2026-05-11. The page is JavaScript-rendered, so this observation is catalog metadata and still requires local Safari version capture before use in a benchmark.
- Apple Safari resources listed Safari Technology Preview Release `247`, posted 2026-07-01.
- BrowserBench identifies Speedometer 3.1, JetStream 3.0, and MotionMark as useful diagnostic surfaces. They do not replace local corpus, raw artifacts, failure accounting, security equivalence, accessibility coverage, or owner-reviewed claim bundles.
- The 2026-07-19 recheck found no catalog-version change for the registry entries above. This is a freshness observation only; it does not create local executable pins or benchmark eligibility.

## Machine Registry

The checked release-catalog manifest is [current desktop release-candidate competitor versions](../blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json), governed by the [benchmark competitor-version schema](../blueprint-v1/machine/benchmark-competitor-version.schema.json) and validated by [`tools/validate_benchmark_competitor_versions.py`](../../tools/validate_benchmark_competitor_versions.py).

The manifest status is `release_catalog_no_local_install_pins`. Every browser entry is `benchmark_eligible: false` because the registry does not include:

- local executable path or platform-specific application bundle evidence;
- executable hash or code-signature/hash strategy;
- browser-reported version capture from the installed product;
- command line, environment, feature flags, profile, extension, sync/account, cache, update, sandbox, site-isolation, memory-saver, energy-saver, lifecycle, and user-agent settings;
- runner-generated benchmark manifest, raw artifacts, traces, samples, failures, or statistical summary.

## Required Next Evidence

Future competitor comparison work must add local pinned browser manifests before any benchmark runner can compare results:

1. Capture each competitor from the same fixed hardware and OS-control manifest that Turing uses.
2. Record product, channel, exact installed version, platform, architecture, executable path, executable SHA-256 or platform-specific hash strategy, and release source URL.
3. Record command line, profile source, extension state, sync/account state, update state before and after run, sandbox/site-isolation settings, memory/energy-saver settings, cache state, user-agent policy, and failure-denominator policy.
4. Link competitor-version IDs from runner-generated benchmark manifests alongside hardware, OS-control, resource-attribution, corpus, and network-profile IDs.
5. Retain raw artifacts, unsupported behavior, failed workloads, statistical method, and owner review before claim language exists.

## Unsupported Claims

This report does not support:

- fastest-browser, Chrome-class, lower-memory, lower-energy, lower-CPU, lower-wakeup, lower-cost, compatibility, security, accessibility, or production claims;
- comparison between Turing and Chrome, Edge, Firefox, Safari, Safari Technology Preview, Servo, Ladybird, or any other browser;
- comparison between different benchmark suite versions, display refresh rates, viewport classes, cache states, lifecycle states, sandbox states, site-isolation states, power states, or browser channels;
- public use of Safari Technology Preview as a stable-browser competitor without an explicit preview-channel label.

## Impact

This report strengthens `PB13-EV-009` from a prose runbook requirement to a checked release-catalog candidate registry. The later [browser-pin local diagnostic capture](benchmark-browser-pin-local-diagnostic-capture-2026-07.md) adds current-host Chrome and Edge browser-reported versions from isolated temporary profiles, but it remains no-claim diagnostic evidence. `PB-013` remains `documented_no_runner` because benchmark-ready local installed-browser pins, browser-launch runner output, raw artifacts, equal-workload competitor runs, and owner-reviewed claim bundles still do not exist.
