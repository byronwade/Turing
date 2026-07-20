# Servo Build Reproduction Evidence and Gap Report - July 2026

Status: `ADR9-EV-002` build-reproduction evidence and replay-protocol draft; same-host capture; no source-strategy decision
Owner: release operations, quality, architecture, provenance, and documentation owners
Retrieval date: 2026-07-17
Confidence: medium for the reference Windows host; low for independent-host reproducibility until a clean replay runs elsewhere

Freshness boundary: this is a historical same-host build capture from 2026-07-17. The checkout, toolchain, and `origin/main` relation recorded below are evidence for that run and are not a current upstream or reproducibility claim. For later upstream identity, use [Servo Upstream Refresh and Source-Strategy Delta](servo-upstream-refresh-and-source-strategy-delta-2026-07.md); any selected newer source baseline requires a fresh reproduction.

## Question

Can the successful external Servo Windows bootstrap and development build be handed off with enough source, environment, log, artifact, and cache detail for `ADR-0009`, and what still prevents `ADR9-EV-002` from becoming decision-grade independent build evidence?

This report narrows the build-reproduction gap. It does not approve Servo source, dependencies, native packages, generated output, build scripts, performance claims, compatibility claims, security claims, or any Servo-derived Turing release code.

## Scope

The evidence was gathered from the external Servo workspace and logs under `C:\ts`, not from Turing source. No Servo source file, generated output, native binary, registry archive, downloaded package, build log, or build artifact was copied into this repository. This document records bounded metadata, selected result lines, hashes, sizes, and replay instructions.

The pass did not perform a clean-target rebuild, did not run on an independent host, did not run WPT or a local corpus, and did not compare the output against another machine. The replay protocol below is a draft for owner review, not an accepted environment script and not proof that replay has succeeded.

## Source and checkout identity

| Field | Observation |
|---|---|
| External workspace | `C:\ts\servo` |
| Remote | `https://github.com/servo/servo.git` |
| Built commit | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Built tree | `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Branch relation after fetch | `main...origin/main [behind 2]` |
| Checkout shape | shallow checkout |
| Tracked files | `193033` |
| Tracked-file changes after bootstrap/build | `0` |

This checkout remains useful build evidence for the already-built baseline. It is not full-history source provenance evidence; that role is handled separately by the independent non-shallow Git verification report.

## Reference host and toolchain

| Area | Observation |
|---|---|
| Host OS | Windows 11 Pro Insider Preview `10.0.26220`, build `26220` |
| CPU | AMD Ryzen 9 5950X, 16 cores / 32 logical processors |
| RAM | `68625825792` bytes visible memory |
| GPU | AMD Radeon RX 7900 XTX, driver `32.0.22029.1019` |
| `uv` | `uv 0.11.29 (901092ee1 2026-07-15 x86_64-pc-windows-msvc)` from WinGet link path |
| Normal host Python | `Python 3.12.10` |
| Servo bootstrap Python | CPython `3.11.9` at `C:\Users\bcw19\AppData\Local\Programs\Python\Python311\python.exe` |
| Normal host Rust | `rustc 1.97.1`, `cargo 1.97.1` |
| Servo Rust override | `1.95.0-x86_64-pc-windows-msvc`, overridden by `C:\ts\servo\rust-toolchain.toml` |
| Visual Studio instance used for compiler probe | Visual Studio Professional 2022 `17.14.36717.8`, Developer Command Prompt `17.14.21` |
| MSVC tools | `VCToolsInstallDir=C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Tools\MSVC\14.44.35207\` |
| `cl.exe` | `C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe`, version `19.44.35221` |
| `link.exe` | `C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\link.exe`, version `14.44.35221.0` |
| `lld-link.exe` | `C:\Program Files\LLVM\bin\lld-link.exe`, `LLD 22.1.8` |
| `ninja` | `1.13.2` |
| Bootstrap-installed or verified tools | CMake, LLVM, Ninja, WiX, Rust `1.95.0`, `crown`, `moztools-4.0`, and GStreamer MSVC packages were reported by the bootstrap log |

Normal PowerShell remains insufficient for the build because `cl`, `link`, and `lld-link` are not on the normal `PATH`. On this host, the successful compiler probe used the Visual Studio Professional developer prompt and then prepended `C:\Program Files\LLVM\bin` for `lld-link.exe`.

## Replay protocol draft

The replay must run outside the Turing repository from a Visual Studio developer environment. The protocol has two tiers:

- **Tier A same-host replay:** useful for checking that the documented commands still work on the reference machine, but not sufficient for `ADR9-EV-002`.
- **Tier B decision-grade replay:** a clean-target run on an independent Windows host or clean VM using the same protocol, with target/cache isolation and success/failure logs.

An owner-reviewed script should expose these variables explicitly:

| Variable | Required meaning |
|---|---|
| `SERVO_ROOT` | External checkout path, for example `C:\ts\servo-replay\servo`; must not resolve under the Turing repository |
| `LOG_ROOT` | External evidence-log directory, for example `C:\ts\servo-replay-logs\20260717-adr9-ev002` |
| `SERVO_REMOTE` | `https://github.com/servo/servo.git` |
| `SERVO_COMMIT` | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` unless `ADR-0009` selects another baseline |
| `VSDEVCMD` | Exact Visual Studio developer-command script path; must not blindly trust `vswhere -latest` |
| `LLVM_BIN` | Exact LLVM binary directory used to expose `lld-link.exe` |
| `CLEAN_TARGET_MODE` | `delete-target`, `fresh-checkout`, or `external-target`, recorded before running |
| `CACHE_MODE` | `warm-global-caches`, `isolated-cargo-home`, or `empty-cache`, recorded before running |

### Phase 0: path and deletion guard

Before deleting or replacing anything, resolve absolute paths and prove the target directory is inside `SERVO_ROOT` and outside Turing:

```powershell
$ServoRoot = [System.IO.Path]::GetFullPath($env:SERVO_ROOT)
$TuringRoot = [System.IO.Path]::GetFullPath("C:\Users\bcw19\Documents\Codex\2026-07-17\github-plugin-github-openai-curated-remote")
$TargetPath = [System.IO.Path]::GetFullPath((Join-Path $ServoRoot "target"))

if ($ServoRoot.StartsWith($TuringRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "SERVO_ROOT must not be inside the Turing repository"
}

if (-not $TargetPath.StartsWith($ServoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "target path did not resolve under SERVO_ROOT"
}
```

For decision-grade replay, prefer a fresh short-path checkout or a verified `delete-target` pass on an isolated checkout. Reusing `C:\ts\servo\target` is not clean-target evidence.

### Phase 1: host and toolchain capture

Capture these before bootstrap:

```powershell
git --version
uv --version
python --version
python3 --version
rustc --version
cargo --version
winget --version
Get-CimInstance Win32_OperatingSystem
Get-CimInstance Win32_Processor
Get-CimInstance Win32_VideoController
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -all -products * -format json
```

Then enter the selected Visual Studio environment and prove compiler/linker availability:

```bat
call "%VSDEVCMD%" -arch=x64
set "PATH=%LLVM_BIN%;%PATH%"
where cl
cl
where link
link
where lld-link
lld-link --version
```

The script should capture the output even when `cl` or `link` exits with usage status after printing its version.

### Phase 2: source checkout and identity

The source phase must record:

```powershell
git clone --filter=blob:none $env:SERVO_REMOTE $env:SERVO_ROOT
git -C $env:SERVO_ROOT fetch origin $env:SERVO_COMMIT --depth=1
git -C $env:SERVO_ROOT checkout --detach $env:SERVO_COMMIT
git -C $env:SERVO_ROOT rev-parse HEAD
git -C $env:SERVO_ROOT rev-parse "HEAD^{tree}"
git -C $env:SERVO_ROOT rev-parse --is-shallow-repository
git -C $env:SERVO_ROOT remote get-url origin
git -C $env:SERVO_ROOT status --short --branch
git -C $env:SERVO_ROOT ls-files | Measure-Object
```

If the owner requires non-shallow build replay, replace the shallow fetch with a full clone and record `git fsck --connectivity-only`. If the selected source baseline differs from `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, the whole Servo evidence packet must be rerun for that baseline.

### Phase 3: bootstrap and build execution

The core commands remain:

```bat
call "%VSDEVCMD%" -arch=x64
set "PATH=%LLVM_BIN%;%PATH%"
cd /d "%SERVO_ROOT%"
powershell -NoProfile -ExecutionPolicy Bypass -File .\mach.ps1 bootstrap 1>"%LOG_ROOT%\bootstrap.out.log" 2>"%LOG_ROOT%\bootstrap.err.log"
echo BOOTSTRAP_EXIT=%ERRORLEVEL% > "%LOG_ROOT%\bootstrap.exit.txt"
powershell -NoProfile -ExecutionPolicy Bypass -File .\mach.ps1 build --dev -j 8 1>"%LOG_ROOT%\build-dev.out.log" 2>"%LOG_ROOT%\build-dev.err.log"
echo BUILD_EXIT=%ERRORLEVEL% > "%LOG_ROOT%\build-dev.exit.txt"
```

An owner-accepted reproduction script should not blindly use `vswhere -latest` until the selected instance is proven to expose the required VC tools. A current probe found that `vswhere -latest` selected the Build Tools 2022 instance, while the known-good compiler probe used the Professional 2022 instance.

### Phase 4: evidence bundle

Every success or failure bundle must include:

- source identity, tree identity, checkout shape, tracked-file count, and tracked-file status;
- host OS, CPU, RAM, GPU, Visual Studio instance, MSVC tools, LLVM tools, `uv`, Python, Rust, Cargo, Ninja, and `winget` outputs;
- bootstrap stdout, stderr, and exit code;
- build stdout, stderr, and exit code;
- `servoshell.exe` existence, size, timestamp, and hash when produced;
- target, `target\debug`, `target\dependencies`, Cargo registry, and Cargo git cache file counts and byte totals;
- cache mode, target mode, and whether network access was permitted;
- failures for missing `uv`, missing Visual Studio compiler tools, missing `lld-link`, bootstrap download failure, corrupt native package, build failure, and target cleanup failure where observed.

Minimum success criteria for `ADR9-EV-002` remain stricter than a local `BUILD_EXIT=0`: the replay must run from a clean target on an independent host or clean VM, preserve the evidence bundle above, and be accepted by release-operations and quality owners.

## Build logs and artifact identity

| Path | Bytes | Last write time | SHA-256 |
|---|---:|---|---|
| `C:\ts\servo-bootstrap.log` | `1763` | `2026-07-17T14:08:21.0277641-04:00` | `867B42580DCD8FAD52E9A30C5A6292300A46EC3184E2AD90BC3C99BF3BA2AFAC` |
| `C:\ts\servo-build-dev-vsdevcmd-llvm.out.log` | `1337` | `2026-07-17T14:18:02.9233520-04:00` | `BC11CB9EA4AA6066D2725840D3B5714829FAF9F5B885C0AFFE9F6B01D317F4B2` |
| `C:\ts\servo-build-dev-vsdevcmd-llvm.err.log` | `27775` | `2026-07-17T14:17:55.3877220-04:00` | `BD4F9FEB458FEDC760F233A85D4C4603E8D247607C6B0BE6530C055C0F8CEBA3` |
| `C:\ts\servo\target\debug\servoshell.exe` | `298702336` | `2026-07-17T14:17:34.7581979-04:00` | `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B` |

Selected result lines:

- build stdout line `19`: `Succeeded in 0:09:21`;
- build stdout line `20`: `BUILD_EXIT=0`;
- build stderr line `753`: `Finished dev profile [unoptimized + debuginfo] target(s) in 9m 14s`;
- bootstrap log line `1`: CPython `3.11.9` was used;
- bootstrap log line `12`: Rust `1.95.0-x86_64-pc-windows-msvc` was used;
- bootstrap log lines `19` through `23`: `moztools-4.0` and GStreamer MSVC packages were downloaded or installed under `C:\ts\servo\target\dependencies`.

## Target and cache footprint

| Path | Files | Bytes |
|---|---:|---:|
| `C:\ts\servo\target` | `38370` | `35941861226` |
| `C:\ts\servo\target\debug` | `18907` | `34357181865` |
| `C:\ts\servo\target\dependencies` | `19456` | `1582709414` |
| `C:\Users\bcw19\.cargo\registry` | `100209` | `2318157010` |
| `C:\Users\bcw19\.cargo\git` | `404` | `47241599` |

Decision-grade reproduction must not treat this warm target directory as equivalent to a clean build. The next replay should use a verified short external path, delete or isolate only a target directory proven to be outside Turing, record before/after cache state, and state whether Cargo registry/git caches, Servo native bootstrap downloads, and `target\dependencies` were reused or fetched fresh.

## Failure and replay notes

- The first long temporary checkout was not trustworthy because `git ls-files` returned `0`, `git status --porcelain` counted `193074` entries, and `git fsck --connectivity-only` reported dangling objects.
- Normal PowerShell did not expose `cl`, `link`, or `lld-link`; a Visual Studio developer prompt plus explicit LLVM `PATH` entry was required.
- `uv` was missing before the successful preflight and had to be installed through WinGet.
- Host Python `3.12.10` and Rust `1.97.1` differ from Servo's pinned CPython `3.11.9` and Rust `1.95.0`; reproduction must capture Servo's override behavior.
- The current build checkout is shallow and two commits behind refreshed `origin/main`; if `ADR-0009` selects a different baseline, the build, dependency, generated-output, native, compatibility, and performance evidence must be rerun.
- No failure replay exists yet for missing LLVM, missing Visual Studio developer environment, missing `uv`, corrupt native bootstrap downloads, offline bootstrap, or clean-target rebuild after deleting `target`.

## What this proves

The evidence proves that the named Windows reference host built the named Servo commit from an external short-path checkout using Servo's bootstrap path, Servo's pinned language tools, Visual Studio Professional 2022 developer environment, and LLVM linker path. It also preserves hashes for the local logs and resulting `servoshell.exe`.

## What this does not prove

This evidence does not prove:

- independent-host reproducibility;
- clean-target determinism;
- source approval or selected-baseline equivalence;
- dependency, license, advisory, native package, or source-offer approval;
- generated-output trust;
- compatibility with the web platform;
- security, sandbox, or update safety;
- performance, memory, energy, startup, or "extreme performance" claims;
- maintainability or upstream relationship viability;
- that Turing may import Servo source, native artifacts, generated output, or build logs.

## Resulting gate update

`ADR9-EV-002` remains partial. The exact same-host environment, logs, artifact hash, and cache footprint are now captured, so the remaining build-reproduction decision work is narrower:

1. run the protocol from a clean target on an independent Windows host or clean VM;
2. convert this draft into an owner-reviewed script or accept it as the owner-reviewed runbook;
3. record target/cache isolation policy before and after the replay;
4. preserve success and failure logs with hashes;
5. rerun if `ADR-0009` selects a source baseline other than `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`.

## Affected records

This report informs:

- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md)
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md)
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md)
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md)
- [Servo Source Strategy Inventory](servo-source-strategy-inventory-2026-07.md)
- [Servo Source and Archive Provenance Audit](servo-source-archive-provenance-audit-2026-07.md)
- [Servo Build-Script and Generated-Output Audit](servo-build-script-generated-output-audit-2026-07.md)
- [Servo Native Bootstrap Provenance and Source-Build Audit](servo-native-bootstrap-provenance-audit-2026-07.md)
- [Release operations](../release-operations/README.md)
- [Quality assurance](../quality-assurance/README.md)
