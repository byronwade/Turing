# Benchmark Competitor Local Install Inventory - July 2026

Status: `PB13-EV-009` local executable evidence; no benchmark-ready competitor pin, browser run, competitor result, or performance claim
Owner: performance measurement, benchmark operations, release operations, and quality
Capture date: 2026-07-17 20:33:44 -04:00
Confidence: medium for executable metadata and hashes on the current Windows host; low for benchmark readiness until owner-reviewed browser pins, profiles, settings, channel proof, and runner artifacts exist

Freshness boundary: this inventory is a capture-time snapshot from 2026-07-17. “Current host” means the Windows host and executable state observed during that capture; it is not a current vendor-release or benchmark-ready pin. Re-run the inventory and browser-reported diagnostic capture before any owner-reviewed comparison uses these files.

## Question

Which competitor browser executables are present on the current Windows high-end host, and what still prevents them from becoming benchmark-ready local pins?

This report complements the [release-catalog competitor-version manifest](benchmark-competitor-version-manifest-2026-07.md). Release catalogs say what vendors currently publish. This inventory says what executable files are present on this host. Neither one is a benchmark result.

The later [browser-pin local diagnostic capture](benchmark-browser-pin-local-diagnostic-capture-2026-07.md) records current-host Chrome and Edge browser-reported versions from isolated temporary profiles. That diagnostic report updates the browser-reported-version gap for Chrome and Edge only; this executable inventory remains local-install evidence and is not benchmark-ready pin evidence by itself.

## Capture Method

PowerShell captured only machine-level executable and registry metadata:

- standard Chrome, Edge, and Firefox executable paths under `Program Files` and `Program Files (x86)`;
- `Get-Item` file version, product version, size, and last-write time;
- `Get-FileHash -Algorithm SHA256`;
- `Get-AuthenticodeSignature`;
- Windows App Paths entries for Chrome and Edge;
- selected Chrome and Edge `BLBeacon` values;
- selected uninstall `DisplayVersion` values.

The capture did not read user browser profiles, history, cookies, account state, extension data, cache directories, downloads, bookmarks, passwords, session state, crash reports, or browsing data.

## Observations

The checked machine record is [current Windows high-end competitor local installs](../blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json), governed by the [benchmark competitor local-install schema](../blueprint-v1/machine/benchmark-competitor-local-install.schema.json) and validated by [`tools/validate_benchmark_competitor_local_installs.py`](../../tools/validate_benchmark_competitor_local_installs.py).

Observed executables:

| Product | Path | File/product version | SHA-256 status | Benchmark status |
|---|---|---|---|---|
| Google Chrome | `C:\Program Files\Google\Chrome\Application\chrome.exe` | `150.0.7871.115` | captured | not eligible |
| Microsoft Edge | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` | `151.0.4129.21` | captured | not eligible |

Not observed on this Windows host:

- Firefox was not found in the standard `Program Files` or `Program Files (x86)` locations checked, and no filtered Firefox uninstall entry was returned.
- Safari Stable and Safari Technology Preview require macOS host evidence and cannot be pinned from this Windows host.

## Version-State Issues

Chrome local metadata is internally inconsistent:

- executable file/product version: `150.0.7871.115`;
- Chrome `BLBeacon`: `150.0.7871.115`;
- uninstall `DisplayVersion`: `150.0.7871.127`;
- application version directories: `150.0.7871.115` and `150.0.7871.127`;
- `chrome.exe --version` did not return a version string because it reported an existing browser session.

Chrome is also older than the release-catalog Chrome Stable candidate recorded in the release-catalog manifest.

Edge local metadata is also internally inconsistent:

- executable file/product version and uninstall `DisplayVersion`: `151.0.4129.21`;
- Edge `BLBeacon`: `151.0.4129.15`;
- `msedge.exe --version` returned no version output.

The Edge executable metadata is newer than the Edge Stable release-catalog candidate recorded in the release-catalog manifest, so channel and update-ring classification must be resolved before Edge can be used as a Stable competitor.

## Impact

This report strengthens `PB13-EV-009` by adding local executable paths, hashes, signatures, and version-state caveats for Chrome and Edge on the current Windows high-end host. It does not complete competitor pinning because the following are still missing:

- owner-reviewed benchmark-ready browser pin evidence beyond the later no-claim Chrome/Edge diagnostic capture;
- channel proof and update-state classification;
- profile source and profile hash;
- extension, sync/account, cache, feature-flag, command-line, environment, sandbox, site-isolation, lifecycle, memory-saver, energy-saver, power, and user-agent settings;
- Firefox local install evidence on Windows or an explicit install decision;
- Safari Stable and Safari Technology Preview evidence on macOS;
- runner-generated benchmark manifests, raw artifacts, traces, failure denominator, statistical summary, and owner review.

## Unsupported Claims

This inventory does not support:

- Chrome-class, fastest, lower-memory, lower-energy, lower-CPU, lower-wakeup, compatibility, security, accessibility, daily-driver, or production claims;
- any ranking or comparison between Turing and Chrome, Edge, Firefox, Safari, Servo, Ladybird, or any other browser;
- treating Edge `151.0.4129.21` as Stable without channel evidence;
- treating Chrome's local metadata as a benchmark-ready browser version without owner-reviewed browser-pin evidence.

`PB-013` remains `documented_no_runner`.
