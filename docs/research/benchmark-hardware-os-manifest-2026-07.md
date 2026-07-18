# Benchmark Hardware and OS Manifest - July 2026

Status: `PB-013` hardware/OS evidence draft; no benchmark result or performance claim
Owner: performance measurement, benchmark operations, release operations, and platform support
Research date: 2026-07-17
Confidence: high for current-host facts observed through Windows management APIs; low for benchmark readiness until the host is cleaned, frozen, and independently reviewed

## Question

Which local Windows machine facts can be captured now as the first benchmark hardware and OS manifest, and what still prevents that machine from being decision-grade Chrome-class performance evidence?

## Inputs

Machine-readable records:

- [Benchmark hardware schema](../blueprint-v1/machine/benchmark-hardware.schema.json)
- [Current Windows high-end candidate manifest](../blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json)
- [Benchmark OS and Update-Control Manifest - July 2026](benchmark-os-update-control-manifest-2026-07.md)
- [Current Windows high-end OS-control candidate](../blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json)
- [No-claim benchmark manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json)
- [Benchmark hardware validator](../../tools/validate_benchmark_hardware.py)
- [Benchmark manifest validator](../../tools/validate_benchmark_manifests.py)
- [Benchmark smoke runner](../../tools/run_benchmark_smoke.py)
- [Pre-build readiness registry](../blueprint-v1/machine/pre-build-readiness.json)
- [Chrome-Class Performance Runbook - July 2026](chrome-class-performance-runbook-2026-07.md)
- [Performance Benchmark Readiness Packet - July 2026](performance-benchmark-readiness-packet-2026-07.md)

Current-host commands used on 2026-07-17:

- `Get-CimInstance Win32_ComputerSystem`
- `Get-CimInstance Win32_OperatingSystem`
- `Get-CimInstance Win32_Processor`
- `Get-CimInstance Win32_VideoController`
- `Get-CimInstance Win32_BIOS`
- `Get-CimInstance Win32_BaseBoard`
- `Get-CimInstance Win32_PhysicalMemory`
- `Get-CimInstance Win32_DiskDrive`
- `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion`
- `powercfg /getactivescheme`

## Observed Host

The current available Windows host is recorded as `TURING.BENCHMARK.HARDWARE.CURRENT_WINDOWS_HIGH_END.2026_07`.

Observed facts:

- host name: `BYRON-HOME`;
- system manufacturer/model: ASUS `System Product Name`;
- board: ASUSTeK COMPUTER INC. `ROG CROSSHAIR VIII DARK HERO`;
- BIOS: American Megatrends Inc. `5302`;
- CPU: AMD Ryzen 9 5950X, 16 physical cores and 32 logical processors;
- memory: 68,625,825,792 bytes total physical memory reported by the system, 68,719,476,736 bytes installed across 4 modules;
- GPU: AMD Radeon RX 7900 XTX, driver `32.0.22029.1019`;
- current display refresh: 165 Hz;
- OS caption: Microsoft Windows 11 Pro Insider Preview;
- OS version/build: `10.0.26220`, build `26220`, UBR `8491`, display version `25H2`;
- active power scheme: Ultimate Performance;
- fixed storage: Samsung SSD 970 EVO Plus 2TB and Samsung SSD 960 PRO 2TB;
- removable storage attached: USB DISK 3.0 USB Device.

## Interpretation

This is a high-end Windows desktop. It is useful as a Tier H candidate for early runner development and high-ceiling diagnostics, not as a Tier M reference host. It should not be used to infer mainstream user performance.

The manifest partially advances `PB13-EV-001` because it captures CPU, memory, GPU, display-refresh, storage, and host identity. It partially advances `PB13-EV-002` because it captures OS build, UBR, display version, install date, last boot time, and power scheme. It does not make the host reviewed or decision-grade.

The default no-claim benchmark manifest sample and smoke runner now carry this `hardware_id` for traceability. That link is useful for runner development, but it is not a browser launch, fixed-hardware measurement, or raw performance result.

The [Benchmark OS and Update-Control Manifest - July 2026](benchmark-os-update-control-manifest-2026-07.md) now records current-host OS, update policy, Insider channel, service, driver, firmware, power, display, clock, and unresolved control facts against this same `hardware_id`. It improves traceability for `PB13-EV-002`, but it does not approve the host as a clean benchmark image.

## Unsupported Conclusions

This record does not show:

- any Turing browser performance;
- any Servo performance;
- any Chrome, Edge, Firefox, Safari, Servo, or Ladybird comparison;
- any memory, energy, startup, input, frame pacing, 30-tab, or graphics score;
- any claim that the host is stable, clean, frozen, or representative;
- any support for a Chrome-class, fastest, lower-memory, lower-energy, or extreme-performance public claim.

## Remaining Gaps

The host cannot support decision-grade performance results until these are added:

- clean OS image or restore procedure;
- approved Windows Update, driver update, preview-build, target-version, and background-service freeze policy;
- BIOS, firmware, and driver freeze record;
- display refresh-rate normalization, including 60 Hz control for MotionMark-class comparison;
- thermal soak, fan, sensor, and room-condition capture;
- artifact storage policy that excludes removable media unless deliberately approved;
- browser-run benchmark manifests, raw result packages, and trace packages that reference this `hardware_id`;
- independent review and replacement policy;
- Tier L and Tier M host manifests so high-end behavior is not mistaken for the product denominator.

## Readiness Impact

`PB-013` remains `documented_no_runner`. The current host manifest and OS-control candidate reduce ambiguity about available high-end hardware and its current Windows controls, but the fixed-hardware lab still lacks Tier L and Tier M manifests, a clean OS image, approved update/driver/firmware/display/thermal controls, an expanded corpus, a browser-launch runner, raw result artifacts, trace packages, and actual competitor runs.

## Next Actions

1. Capture a Tier M Windows manifest for a mainstream target machine.
2. Capture a Tier L manifest for constrained hardware.
3. Define the clean image or restore process for the current Tier H candidate.
4. Extend the browser-launch benchmark runner so generated benchmark manifests reference `hardware_id` from the hardware registry.
5. Keep all results from this host labeled no-claim until the clean-image and review gates pass.
