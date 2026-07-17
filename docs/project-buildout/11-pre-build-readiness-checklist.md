# Pre-build Readiness Checklist

Status: canonical operating checklist  
Owner: program, architecture, security, UI runtime, build, quality, and subsystem owners  
Last audited: 2026-07-17

## Purpose

Turn “ready to build” into a reviewable claim. The machine-readable companion is [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json).

## Readiness classes

- **Ready:** required evidence exists and is linked.
- **M0 reference implemented:** deterministic source and tests exist, but platform integration, adversarial evidence, or production measurement is incomplete.
- **Partial or proposed:** design exists but source, tests, measurement, or decision evidence is incomplete.
- **Not started:** no executable evidence.
- **Blocked:** an external decision, staffing, legal, or predecessor dependency prevents completion.

## Controlled work allowed before PB-GATE-0

Documentation, algorithms, bounded implementation references, throwaway comparison prototypes, benchmark harnesses, UI adapter spikes, sandbox probes, generated schemas, test corpora, and the dependency-free architecture model may continue. These artifacts must remain clearly labeled and must not freeze public compatibility or production trust boundaries accidentally.

## Current contained-M0 evidence

The following controls now have executable evidence:

- root Cargo workspace and machine-checked dependency graph;
- pinned M0 Rust toolchain;
- bootstrap, doctor, and complete repository check;
- zero-dependency, unsafe, native, generated-code, and provenance ledgers;
- canonical JSON control-plane schema and deterministic generated Rust/documentation;
- restart-safe process identities;
- generated roles, capabilities, launch rights, message routes, document-scope rules, message limits, and queue budgets;
- bounded envelopes, exact sequences, explicit backpressure, capability attenuation, and kernel route authorization.

The generated IPC work is an M0 policy reference. It does not satisfy real authenticated transport, sandbox, shared-memory, platform handle, wire-codec, compromised-process, or fixed-hardware requirements.

## P0 kickoff group still open

- engine source strategy and Servo relationship;
- toolkit-neutral shell model acceptance and commands;
- UI framework comparison and license review;
- page-surface/compositor/accessibility integration;
- reference platform;
- production operating-system IPC transport and canonical wire codec;
- platform peer authentication, handle transfer, and shared-memory leases;
- sandbox probes and compromised-process harness;
- benchmark hardware/corpus/runner and production queue budgets;
- design system/component/fixture inventory;
- profile/session/migration versioning.

## Review

The program lead reviews the registry at every implementation kickoff and milestone boundary. Exceptions must name the affected item, scope, owner, rationale, risk, compensating controls, expiry, and evidence required for closure. An exception cannot authorize misleading product, security, performance, or compatibility claims.

`WP-002` may continue under contained M0 authorization. It remains in progress until authenticated platform transport, generated wire representation, handle-transfer rules, negative testing, and independent review exist.

## Exit

PB-GATE-0 passes for a selected contained milestone when all applicable P0 items are ready or covered by approved time-bounded exceptions. It does not imply beta or stable readiness.
