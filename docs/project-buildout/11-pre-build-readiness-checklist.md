# Pre-build Readiness Checklist

Status: canonical operating checklist; contained M0 implementation authorized  
Owner: program, architecture, security, UI runtime, release operations, quality, and subsystem owners  
Last audited: 2026-07-17

## Purpose

Turn “ready to build” into a bounded, reviewable claim. The machine companion is [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json), and the dependency-ordered execution guide is the [Implementation Master Plan](implementation-plan/README.md).

## Current authorization

Turing is ready for **contained M0 implementation**, not broad parallel browser construction and not production use.

The documentation game plan is complete enough to tell an agent:

- which milestone and WP comes next;
- which dependencies and ADRs block it;
- how to create a bounded task;
- which negative tests and evidence classes apply;
- when interfaces freeze;
- how work is independently reviewed, handed off, rolled back, or stopped;
- what preview, beta, stable, and continuous-maintenance gates require.

That plan does not make unresolved technical or staffing evidence ready.

## Implemented foundation

- buildable root Cargo workspace;
- pinned Rust toolchain;
- M0 reference CI environment;
- typed identity, IPC, kernel, UI-model, build-info, shell-laboratory, and repository-tool crates;
- bootstrap, doctor, and complete check commands;
- dependency, unsafe-code, native-code, generated-code, and provenance ledgers;
- machine-checked component and dependency records;
- agent task/run/evidence controls;
- implementation execution graph, milestone gates, interface freezes, evidence catalog, and planned task waves;
- CI that compiles and tests the root workspace.

Evidence is summarized in the [M0 build-foundation report](../research/m0-build-foundation-2026-07.md).

## Readiness classes

- **Ready:** required evidence exists for the named scope.
- **Ready for contained M0:** sufficient for bounded foundational tasks, not preview or stable support.
- **Partial or proposed:** design exists but source, tests, measurement, review, or decision evidence is incomplete.
- **Not started:** no executable evidence.
- **Blocked:** predecessor, staffing, legal, or external dependency prevents completion.

## Work now allowed

- source crates under the accepted M0 dependency direction;
- typed identity, process-policy, and bounded IPC implementation;
- toolkit-neutral UI state and command work;
- native UI comparison prototypes isolated from production crates;
- sandbox probe contracts and contained laboratories;
- benchmark and corpus tooling;
- profile, Space, session, and migration schema prototypes;
- parser/runtime research tasks that do not bypass ADR-0009 or source provenance;
- tests, fuzz targets, fixtures, and diagnostic tooling.

Every task must follow the [Agent Execution](../agent-execution/README.md) controls and the [agent operating protocol](implementation-plan/02-agent-operating-protocol.md), and remain independently reviewable and revertible.

## Still blocked before broad M1 expansion

- accepted Servo/source strategy for production engine source;
- UI toolkit, licensing, and page-surface/compositor ownership;
- production platform support matrix;
- accepted IPC wire codec, authenticated transports, handle transfer, and compromised-sender harness;
- packaged sandbox evidence;
- fixed-hardware laboratory;
- design token and component system;
- profile/session persistence formats;
- updater laboratory;
- qualified backup ownership.

## Still blocked before preview, beta, or stable

- implemented M1–M4 subsystem evidence;
- signed update and migration reliability;
- supported-platform accessibility and security matrices;
- numeric SLOs and conformance thresholds;
- incident response and support staffing;
- independent security and accessibility review;
- legal, privacy, licensing, distribution, and signing approval;
- all applicable `PRG-*` release gates.

## Commands

```bash
sh tools/bootstrap.sh
sh tools/doctor.sh
sh tools/check.sh
```

## PB-GATE-0

PB-GATE-0 passes only for a named contained task whose prerequisites are ready or covered by a reviewed expiring exception. It does not imply M1 completion, preview safety, beta support, or stable readiness.

## Kickoff decision

An agent may start a contained task after all checklist and task-manifest conditions pass. It may not reinterpret this document as permission to build all milestones autonomously or to merge unreviewed source.
