# Pre-build Readiness Checklist

Status: canonical operating checklist; contained M0 implementation authorized  
Owner: program, architecture, security, UI runtime, release operations, quality, and subsystem owners  
Last audited: 2026-07-17

## Purpose

Turn “ready to build” into a bounded, reviewable claim. The machine companion is [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json).

## Current authorization

Turing is now ready for **contained M0 implementation**, not broad parallel browser construction and not production use.

The implemented foundation includes:

- a buildable root Cargo workspace;
- pinned Rust toolchain;
- M0 reference CI environment;
- typed identity, IPC, kernel, UI-model, build-info, shell-laboratory, and repository-tool crates;
- bootstrap, doctor, and complete check commands;
- dependency, unsafe-code, native-code, generated-code, and provenance ledgers;
- machine-checked component and dependency records;
- CI that compiles and tests the root workspace.

Evidence is summarized in the [M0 build-foundation report](../research/m0-build-foundation-2026-07.md).

## Readiness classes

- **Ready:** required evidence exists for the named scope.
- **Ready for contained M0:** sufficient for bounded foundational tasks, not preview or stable support.
- **Partial or proposed:** design exists but source, tests, measurement, or decision evidence is incomplete.
- **Not started:** no executable evidence.
- **Blocked:** predecessor, staffing, legal, or external dependency prevents completion.

## Work now allowed

- source crates under the accepted M0 dependency direction;
- typed identity and process-policy implementation;
- bounded IPC and schema experiments;
- toolkit-neutral UI state and command work;
- native UI comparison prototypes isolated from production crates;
- sandbox probes;
- benchmark and corpus tooling;
- profile, Space, session, and migration schema prototypes;
- tests, fuzz targets, fixtures, and diagnostic tooling.

Every task must use the [Agent Execution](../agent-execution/README.md) controls and remain independently reviewable and revertible.

## Still blocked before M1 expansion

- Servo/source strategy;
- UI toolkit and licensing;
- page-surface and compositor ownership;
- production platform support matrix;
- accepted generated IPC wire schema;
- packaged sandbox evidence;
- fixed-hardware laboratory;
- design token and component system;
- profile/session persistence formats;
- updater laboratory;
- qualified backup ownership.

## Commands

```bash
sh tools/bootstrap.sh
sh tools/doctor.sh
sh tools/check.sh
```

## PB-GATE-0

PB-GATE-0 passes only for a named contained task whose prerequisites are ready or covered by a reviewed expiring exception. It does not imply M1 completion, preview safety, beta support, or stable readiness.
