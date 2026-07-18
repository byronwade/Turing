# M0 Build Foundation — July 2026

Status: implemented repository foundation; not a browser capability or production claim  
Owner: architecture, release operations, security, UI runtime, quality, and documentation  
Implementation baseline: `agent/m0-build-foundation`

## Question

What is the smallest professional source and tooling foundation that allows Turing implementation to begin without prematurely choosing a browser engine source strategy, native UI framework, network stack, storage backend, or external runtime dependency?

## Decision

Create a dependency-free root Rust workspace that establishes stable ownership and validation boundaries before subsystem implementation expands.

The M0 reference uses:

- Rust `1.97.1`;
- Rust 2024 for new crates;
- Cargo workspace resolver 3;
- rustfmt, Clippy, and rust-src;
- Ubuntu 24.04 LTS and `x86_64-unknown-linux-gnu` as the reproducible M0 CI reference;
- no external runtime or build dependencies;
- unsafe Rust and native code forbidden by default;
- build output outside the repository in CI and wrapper commands.

The reference environment is a development and CI baseline, not a stable product-support commitment.

## Workspace components

- `turing-types`: stable typed identities.
- `turing-build-info`: version and maturity metadata.
- `turing-ipc`: bounded typed control envelopes; no accepted wire format yet.
- `turing-kernel`: deny-by-default process-role and capability skeleton.
- `turing-ui-model`: toolkit-neutral immutable presentation snapshots and typed commands.
- `turing-shell`: command-line M0 shell laboratory; no native windowing.
- `xtask`: bootstrap, doctor, and full repository checks.
- `turing-architecture-prototype`: earlier standalone invariant model.

Component ownership, privilege, hostile-input exposure, unsafe policy, dependencies, platforms, and failure boundaries are recorded in [`workspace-components.json`](../blueprint-v1/machine/workspace-components.json).

## Commands

POSIX shells:

```bash
sh tools/bootstrap.sh
sh tools/doctor.sh
sh tools/check.sh
```

Windows PowerShell:

```powershell
.\tools\bootstrap.ps1
.\tools\doctor.ps1
.\tools\check.ps1
```

`bootstrap` is intentionally non-installing during M0. It verifies the environment and prints the next action. `doctor` is read-only. `check` runs documentation validation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation, build-foundation validation, evidence-bundle validation, contained M0 start-state validation, build-information readiness validation, local unstaged and staged diff whitespace checks, formatting, Clippy with warnings denied, workspace tests, shell self-test, and the architecture prototype. The POSIX and PowerShell wrappers delegate to the same `xtask` commands and set `CARGO_TARGET_DIR` outside the repository when unset.

## Security posture

The initial workspace has:

- zero external runtime dependencies;
- zero external build dependencies;
- zero unsafe-code entries;
- zero native-code or FFI entries;
- zero committed generated-source entries;
- no build scripts;
- no network access in repository validation;
- no UI toolkit, graphics library, async runtime, database, TLS stack, compiler backend, or model runtime.

Future additions require the normal dependency, security, provenance, licensing, performance, and replacement review.

## Why Rust 1.97.1

Rust 1.97.1 was published on July 16, 2026 as a point release correcting an LLVM miscompilation risk in 1.97.0. The workspace pins the point release rather than a floating `stable` channel.

Source: https://blog.rust-lang.org/2026/07/16/Rust-1.97.1/

## Why Ubuntu 24.04 for M0

Ubuntu 24.04 provides a reproducible public CI environment and supports the initial pure-Rust workspace without establishing permanent product priority. macOS and Windows platform work remains required before any cross-platform preview claim.

## Evidence

- `Cargo.toml`
- `Cargo.lock`
- `rust-toolchain.toml`
- `docs/blueprint-v1/machine/workspace-components.json`
- `docs/blueprint-v1/machine/toolchains.json`
- `security/*.json`
- `tools/validate_build_foundation.py`
- `tools/xtask/`
- `.github/workflows/repository-validation.yml`

## What this enables

Contained work may now create:

- typed kernel identities and policies;
- bounded IPC schema experiments;
- UI model and adapter experiments;
- sandbox probes;
- benchmark runners;
- design-system fixtures;
- profile and session schema prototypes;
- deterministic test tools.

## What remains blocked

This foundation does not select Servo strategy, a native UI toolkit, page compositor ownership, stable platforms, external dependencies, network/storage implementations, update trust, signing, production services, or stable release scope.

## Revisit trigger

Revisit the workspace structure when one of the following is demonstrated:

- a crate boundary creates measurable build or runtime cost without an ownership benefit;
- a required platform or subsystem cannot fit the dependency direction;
- a public SDK boundary must be separated;
- an accepted ADR changes the engine or UI source strategy;
- a dependency requires a stronger isolation or build boundary.
