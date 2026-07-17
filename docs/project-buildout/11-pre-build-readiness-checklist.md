# Pre-build Readiness Checklist

Status: canonical operating checklist  
Owner: program, architecture, security, UI runtime, build, quality, and subsystem owners  
Last audited: 2026-07-17

## Purpose

Turn “ready to build” into a reviewable claim. The machine-readable companion is [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json).

## Readiness classes

- **Ready:** required evidence exists and is linked.
- **Partial or proposed:** design exists but source, tests, measurement, or decision evidence is incomplete.
- **Not started:** no executable evidence.
- **Blocked:** an external decision, staffing, legal, or predecessor dependency prevents completion.

## Controlled work allowed before PB-GATE-0

Documentation, algorithms, throwaway comparison prototypes, benchmark harnesses, UI adapter spikes, sandbox probes, generated schemas, test corpora, and the dependency-free architecture model may continue. These artifacts must remain clearly labeled and must not freeze public compatibility or production trust boundaries accidentally.

## P0 kickoff group

- engine source strategy and Servo relationship;
- toolkit-neutral shell model and commands;
- UI framework comparison and license review;
- page-surface/compositor/accessibility integration;
- reference platform;
- Cargo workspace and dependency direction;
- pinned toolchain, bootstrap, and doctor;
- dependency/unsafe/provenance ledgers;
- process/IPC schemas and sandbox probes;
- benchmark hardware/corpus/runner;
- design system/component/fixture inventory;
- profile/session/migration versioning.

## Review

The program lead reviews the registry at every implementation kickoff and milestone boundary. Exceptions must name the affected item, scope, owner, rationale, risk, compensating controls, expiry, and evidence required for closure. An exception cannot authorize misleading product, security, performance, or compatibility claims.

## Exit

PB-GATE-0 passes for a selected contained milestone when all applicable P0 items are ready or covered by approved time-bounded exceptions. It does not imply beta or stable readiness.
