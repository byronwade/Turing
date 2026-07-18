# Benchmark OS and Update-Control Manifest - July 2026

Status: `PB-013` OS-control evidence draft; no clean image, benchmark result, or performance claim
Owner: performance measurement, benchmark operations, release operations, and platform support
Research date: 2026-07-17
Confidence: high for current-host facts observed through Windows registry, CIM, service, timezone, and `powercfg` queries; low for benchmark readiness until the image, updates, drivers, display, thermal state, clock, network, and artifact storage are frozen and reviewed

## Question

Which current Windows OS, update, driver, firmware, power, display, thermal, clock, and service facts can be captured now, and what still prevents the current host from being a decision-grade benchmark environment?

## Inputs

Machine-readable records:

- [Benchmark OS-control schema](../blueprint-v1/machine/benchmark-os-control.schema.json)
- [Current Windows high-end OS-control candidate](../blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json)
- [Benchmark OS-control validator](../../tools/validate_benchmark_os_controls.py)
- [Benchmark hardware schema](../blueprint-v1/machine/benchmark-hardware.schema.json)
- [Current Windows high-end hardware candidate](../blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json)
- [Pre-build readiness registry](../blueprint-v1/machine/pre-build-readiness.json)
- [Performance Benchmark Readiness Packet - July 2026](performance-benchmark-readiness-packet-2026-07.md)

Current-host commands used on 2026-07-17:

- `Get-ItemProperty HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate`
- `Get-ItemProperty HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU`
- `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings`
- `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion`
- `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\WindowsSelfHost\Applicability`
- `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\WindowsSelfHost\UI\Selection`
- `Get-Service wuauserv,bits,usosvc,WaaSMedicSvc`
- `Get-CimInstance Win32_OperatingSystem`
- `Get-CimInstance Win32_VideoController`
- `Get-CimInstance Win32_BIOS`
- `Get-CimInstance Win32_BaseBoard`
- `powercfg /getactivescheme`
- `powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN`
- `powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX`
- `Get-TimeZone`
- `w32tm /query /status`

External primary sources checked on 2026-07-17:

- Microsoft Learn, [Configure Windows Update client policies via Group Policy](https://learn.microsoft.com/en-us/windows/deployment/update/waas-wufb-group-policy)
- Microsoft Learn, [Manage additional Windows Update settings](https://learn.microsoft.com/en-us/windows/deployment/update/waas-wu-settings)
- Microsoft Learn, [Powercfg command-line options](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options)
- Microsoft Learn, [PnPUtil command syntax](https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax)
- Microsoft Learn, [Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder)

These sources define relevant control surfaces. They do not prove that the current host is controlled, stable, clean, or suitable for performance claims.

## Observed Controls

The current available Windows host is recorded as `TURING.BENCHMARK.OS_CONTROL.CURRENT_WINDOWS_HIGH_END.2026_07` and links to hardware record `TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07`.

Observed facts:

- OS: Microsoft Windows 11 Pro Insider Preview, version `10.0.26220`, build `26220`, display version `25H2`, UBR `8491`;
- branch and servicing: `ge_release_flt`, LCU `10.0.26100.8491`, `PendingInstall=0`;
- Windows Insider: preview builds enabled, Beta branch, External ring, Mainline content type;
- update policy keys: `DisableWindowsUpdateAccess=1`, `DisableOSUpgrade=1`, and `NoAutoUpdate=1`;
- missing update controls: no target release version, quality update deferral/pause, driver exclusion, or clean update-freeze proof was captured;
- services: `bits` and `usosvc` were running; `wuauserv` was stopped/manual; `WaaSMedicSvc` reported stopped/manual while also returning a permission-denied query note;
- power: Ultimate Performance plan, processor minimum AC 100 percent and maximum AC 100 percent;
- display: 2560x1440 at 165 Hz, not normalized for cross-browser benchmark comparison;
- driver and firmware: AMD Radeon RX 7900 XTX driver `32.0.22029.1019`, BIOS `5302`, baseboard `ROG CROSSHAIR VIII DARK HERO`;
- clock: Eastern time zone; `w32tm /query /status` failed because the time service was not started;
- thermal, network isolation, artifact storage, and background-service freeze were not approved.

## Interpretation

This record is a useful current-host OS-control inventory. It is not a clean benchmark image or an update-freeze approval. The Windows Update policy keys reduce some ambiguity, but the Insider Preview channel, missing target-version policy, missing driver exclusion policy, running update-related services, unverified time service, unnormalized display refresh, and absent thermal procedure make the environment unsuitable for decision-grade Chrome-class comparisons.

The manifest strengthens `PB13-EV-002` by turning vague "OS image and update-control manifest" work into a checked registry entry. It does not complete `PB13-EV-002`, because clean-image creation, restore procedure, target-version pinning, update/driver policy approval, thermal capture, and independent review remain missing.

## Unsupported Conclusions

This record does not show:

- a clean OS image;
- a restorable benchmark image;
- an approved update freeze;
- an approved driver or firmware freeze;
- a stable time-sync source;
- thermal stability;
- isolated network conditions;
- approved artifact storage;
- any Turing, Servo, Chrome, Edge, Firefox, Safari, or Ladybird benchmark result;
- any Chrome-class, fastest, lower-memory, lower-energy, or extreme-performance claim.

## Remaining Gaps

The current host cannot support decision-grade performance results until these are added:

- owner-approved clean image or restore procedure;
- target release version, feature update, quality update, driver update, and preview-build policies;
- full installed driver package inventory and driver freeze policy;
- BIOS and firmware freeze policy;
- display refresh-rate and scale-factor control procedure;
- thermal soak, sensor logging, fan, and room-condition procedure;
- time synchronization and timezone control procedure;
- network isolation and approved artifact storage procedure;
- browser-run benchmark manifest that references this `os_control_id`;
- independent review before treating this as a decision-grade OS-control manifest.

## Readiness Impact

`PB-013` remains `documented_no_runner`. The new OS-control manifest improves handoff clarity for `PB13-EV-002`, but the fixed-hardware lab still lacks Tier L and Tier M manifests, a clean image, an expanded corpus, a browser-launch runner, raw result artifacts, trace packages, and actual competitor runs.

## Next Actions

1. Decide whether the current Tier H host should be cleaned and approved or replaced.
2. Define the clean image or restore process for every approved hardware tier.
3. Add target release version, update deferral, driver exclusion, preview-build, time-sync, display, thermal, network, and artifact-storage policies.
4. Capture a full PnPUtil driver inventory and record the approved driver freeze.
5. Extend browser-run benchmark manifests to reference both `hardware_id` and `os_control_id`.
