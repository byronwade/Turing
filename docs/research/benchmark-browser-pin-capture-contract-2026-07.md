# Benchmark Browser Pin Capture Contract - July 2026

Status: `PB13-EV-005` and `PB13-EV-009` capture-plan, no-browser self-test, and linked current-host diagnostic evidence; no benchmark-ready browser pin, benchmark run, competitor result, or performance claim
Owner: performance measurement, benchmark operations, release operations, privacy, security, and quality
Contract date: 2026-07-17
Confidence: high for the required privacy and evidence boundaries; medium for self-test and diagnostic artifact handling; low for benchmark readiness until owner-reviewed browser pins and complete effective-setting evidence exist

## Question

How should Turing capture benchmark-ready browser pins without reading or mutating the owner's real browser profiles?

The local install inventory found Chrome and Edge executables on the current Windows high-end host, but executable metadata alone is not enough. A benchmark-ready browser pin also needs browser-reported version, channel proof, profile source, command line, settings, update state, extension state, cache state, sandbox/site-isolation state, and artifact hashes. This contract defines the capture boundary before any diagnostic output can be promoted into benchmark-ready evidence.

## Machine Registry

The checked plan is [current Windows high-end browser-pin capture plan](../blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json), governed by the [benchmark browser-pin capture schema](../blueprint-v1/machine/benchmark-browser-pin-capture.schema.json) and validated by [`tools/validate_benchmark_browser_pin_capture.py`](../../tools/validate_benchmark_browser_pin_capture.py). The no-claim runner self-test is [`tools/capture_benchmark_browser_pins.py --self-test`](../../tools/capture_benchmark_browser_pins.py); repository validation runs it and rejects output that omits no-browser, no-claim, artifact-hash, or prohibited-path evidence. The first checked current-host diagnostic summary is [current Windows high-end Chrome/Edge browser-pin diagnostic](../blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json), governed by the [benchmark browser-pin diagnostic schema](../blueprint-v1/machine/benchmark-browser-pin-diagnostic.schema.json), validated by [`tools/validate_benchmark_browser_pin_diagnostics.py`](../../tools/validate_benchmark_browser_pin_diagnostics.py), and described in the [local diagnostic capture report](benchmark-browser-pin-local-diagnostic-capture-2026-07.md).

The plan status is `plan_no_browser_run`. It does not launch Chrome, Edge, Firefox, Safari, Safari Technology Preview, Turing, Servo, or Ladybird.

The runner's default checked path is `--self-test`, which creates and deletes a runner-owned temporary profile marker under `%TEMP%\turing-browser-pin-capture\${run_id}\`, writes a hashed artifact package, and launches no browser. The optional `--capture-local` mode has produced a checked Chrome/Edge diagnostic summary on this host; its output remains no-claim and is not benchmark evidence by itself.

## Privacy Boundary

Allowed reads:

- executable metadata already captured in the local-install manifest;
- runner-owned temporary profiles created for the capture run;
- runner-owned stdout, stderr, process-list, and artifact files.

Prohibited reads:

- real user browser profile directories;
- history, cookies, credentials, bookmarks, downloads, sessions, cache, crash reports, sync data, account data, extension data, or browsing data;
- personal files outside the runner-owned temporary artifact directory.

Allowed writes:

- `%TEMP%\turing-browser-pin-capture\${run_id}\`;
- runner-owned benchmark artifact package directories.

Prohibited writes:

- installed browser application directories;
- real user browser profile directories;
- source-controlled files except reviewed manifest updates.

## Capture Contract

Every browser capture must:

1. create a new temporary profile under the runner-owned temp root;
2. reject existing user profile paths;
3. run offline by default unless an explicit network profile is approved;
4. avoid account, sync, password-manager, credential-store, and platform SSO attachment;
5. capture browser-reported version from a trusted version surface or automation endpoint;
6. capture effective command line, profile path, update state, extension state, cache state, sandbox/site-isolation state, memory-saver or energy-saver state, power state, and user-agent policy;
7. hash every artifact and record cleanup success or failure;
8. keep failed, blocked, timed-out, unsupported, and aborted captures in the denominator.

Capture-only arguments used to prevent first-run, sync, or background network side effects are not automatically valid benchmark workload arguments. A benchmark run must separately record the exact workload command line and justify any setting that differs from default.

## Current Target State

| Target | Local evidence | Capture status | Blocker |
|---|---|---|---|
| Chrome on current Windows host | executable path, hash, signature, inconsistent version metadata, and diagnostic `Chrome/150.0.7871.115` browser-reported version | diagnostic captured, unreviewed | owner review, release-catalog reconciliation, approved workload arguments, full settings, and benchmark artifacts |
| Edge on current Windows host | executable path, hash, signature, unresolved channel/update-ring state, and diagnostic `Edg/151.0.4129.21` browser-reported version | diagnostic captured, unreviewed | owner review, channel proof, approved workload arguments, full settings, and benchmark artifacts |
| Firefox on Windows | not found in standard locations checked | blocked | local install on an approved host |
| Safari Stable | release catalog only | blocked | approved macOS host and profile isolation method |
| Safari Technology Preview | release catalog only | blocked | approved macOS host, preview label, and profile isolation method |

## Unsupported Claims

This contract does not support:

- a benchmark-ready browser pin;
- any browser-run result;
- any comparison against Chrome, Edge, Firefox, Safari, Servo, Ladybird, or Turing;
- Chrome-class, fastest, lower-memory, lower-energy, compatibility, security, accessibility, daily-driver, or production claims.

## Impact

This report strengthens `PB13-EV-005` by defining the browser-launch capture contract, adding a checked no-browser runner self-test, and linking the first no-claim Chrome/Edge diagnostic capture. It strengthens `PB13-EV-009` by defining how competitor pins become benchmark-ready without profile leakage. `PB-013` remains `documented_no_runner` until diagnostic artifacts are owner-reviewed, missing settings and channel proof are filled, and a benchmark runner produces raw benchmark output.

## Next Evidence

The next evidence task must produce:

- owner review of the Chrome and Edge diagnostic capture arguments and artifact package;
- channel proof for Edge;
- full command-line/settings/update/profile/cache/extension/sandbox/site-isolation records;
- Firefox local install evidence on an approved Windows host;
- Safari and Safari Technology Preview evidence on an approved macOS host;
- runner-generated artifact indexes with hashes and no-claim metadata.
