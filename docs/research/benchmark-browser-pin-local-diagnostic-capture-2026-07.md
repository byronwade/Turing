# Benchmark Browser Pin Local Diagnostic Capture - July 2026

Status: `PB13-EV-005` and `PB13-EV-009` current-host diagnostic evidence; no benchmark-ready browser pin, benchmark run, competitor result, or performance claim
Owner: performance measurement, benchmark operations, release operations, privacy, security, and quality
Capture date: 2026-07-18
Confidence: medium for Chrome and Edge browser-reported version observations on the current Windows host; low for benchmark readiness until owner review, channel proof, effective settings, and equal-workload benchmark artifacts exist

Freshness boundary: this diagnostic capture is a dated snapshot from 2026-07-18. “Current host” and “current release-catalog candidate” refer to the identities recorded during that capture and its linked 2026-07-19 catalog; they must be refreshed together before benchmark-ready owner review or comparison use.

## Question

Can the no-claim browser-pin runner capture Chrome and Edge browser-reported versions from isolated temporary profiles without reading or mutating real user profiles?

## Method

The runner command was:

```bash
python3 -B tools/capture_benchmark_browser_pins.py --capture-local --target chrome --target edge --output-dir %TEMP%/turing-browser-pin-local-e2579a92afcc430a80cc37d08d777fe6
```

The checked summary is [current Windows high-end Chrome/Edge browser-pin diagnostic](../blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json), governed by the [benchmark browser-pin diagnostic schema](../blueprint-v1/machine/benchmark-browser-pin-diagnostic.schema.json) and validated by [`tools/validate_benchmark_browser_pin_diagnostics.py`](../../tools/validate_benchmark_browser_pin_diagnostics.py).

The runner used the checked [browser-pin capture plan](../blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json), [current-host local install inventory](benchmark-competitor-local-install-inventory-2026-07.md), and [release-catalog competitor version manifest](benchmark-competitor-version-manifest-2026-07.md). It launched each browser with a runner-owned temporary profile, `about:blank`, no sync, disabled background networking and component update flags, a loopback host resolver rule, and DevTools remote debugging on an ephemeral localhost port.

## Observations

Chrome diagnostic capture:

- browser-reported version: `Chrome/150.0.7871.115`;
- local executable SHA-256: `5718df5f35db255adb85cc8a8305645319f8513e4d8bf818741b8aa491003ce9`;
- temporary profile cleanup: `deleted`;
- prohibited configured-path check: no prohibited access detected;
- local version still differs from the current release-catalog Chrome Stable candidate, so it is not benchmark-ready.

Edge diagnostic capture:

- browser-reported version: `Edg/151.0.4129.21`;
- local executable SHA-256: `7298c2707567e442927cb2069889ee14715e2b268537b4c933bf7d56a6bc840d`;
- temporary profile cleanup: `deleted`;
- prohibited configured-path check: no prohibited access detected;
- the runner had to stop lingering Edge processes tied to the temporary profile path before cleanup;
- local version remains newer than the recorded Edge Stable release-catalog candidate, so channel and update-ring proof remain unresolved.

The runner also exposed and fixed a failure mode: Edge can leave temporary-profile cache files locked after the first diagnostic capture. The runner now records unreadable profile files instead of crashing and scans for browser processes whose command line contains the runner-owned temp profile path before hashing and cleanup.

## Unsupported Claims

This diagnostic capture does not support:

- a benchmark-ready Chrome, Edge, Firefox, Safari, or Safari Technology Preview pin;
- any browser benchmark result;
- any competitor comparison, ranking, regression, release, Chrome-class, fastest, lower-memory, lower-energy, compatibility, security, accessibility, daily-driver, production, or performance claim.

Diagnostic capture arguments are not approved benchmark workload arguments. Browser-reported version capture is useful evidence, but it does not prove channel, update state, sandbox state, site isolation, extensions, cache policy, memory-saver state, energy-saver state, process-tree command line, effective settings, or equal workload.

## Impact

This report strengthens `PB13-EV-005` by proving the no-claim browser-pin runner can produce hashed local diagnostic artifacts for Chrome and Edge from runner-owned temporary profiles. It strengthens `PB13-EV-009` by replacing missing Chrome/Edge browser-reported versions with current-host diagnostic observations.

`PB-013` remains `documented_no_runner`. The evidence is current-host, unreviewed, and diagnostic only. It does not close the need for owner review, Edge channel proof, Firefox/Safari local evidence, fixed hardware approval, expanded corpus, browser benchmark launch runner, raw benchmark artifacts, and equal-workload comparison runs.

## Next Evidence

The next evidence step should produce:

- owner-reviewed capture arguments and artifact package disposition;
- Edge channel and update-ring proof;
- process-tree command-line audit and effective settings capture;
- extension, sync/account, cache, update, sandbox, site-isolation, memory-saver, energy-saver, power, and user-agent records;
- Firefox local-install and browser-reported version evidence on an approved Windows host;
- Safari Stable and Safari Technology Preview evidence on an approved macOS host;
- browser benchmark launch artifacts only after fixed hardware, corpus, network, and claim gates are ready.
