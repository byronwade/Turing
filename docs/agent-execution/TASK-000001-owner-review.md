# TASK-000001 Owner Review Handoff

Status: specified, owner review required, not execution approval
Task: `TASK-000001` Source-strategy closure packet
Prepared: 2026-07-19
Source queue: [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json)
Specified manifest: [`TASK-000001.json`](machine/tasks/TASK-000001.json)

## Purpose

This handoff converts the proposed `TASK-000001` queue row into a bounded, machine-shaped specification for owner review. It does not change the queue status, approve execution, select a source baseline, approve Servo adoption, or authorize release-path code.

The source queue SHA-256 is:

`6F6C75429D8DD582EA99149F25C1B6A51522E27044A9B22EAECD80EA2A200CEC`

This digest is the canonical-JSON hash of [`build-readiness-task-queue.json`](machine/../../blueprint-v1/machine/build-readiness-task-queue.json), computed as `sha256(json.dumps(queue, sort_keys=True, separators=(",", ":")))` and rendered uppercase. It is the same value asserted by all ten specified task manifests and enforced by [`validate_specified_task_manifests.py`](../../tools/validate_specified_task_manifests.py). Reproduce it with that method rather than hashing the file bytes, which yields a different and non-authoritative value.

A previous revision of this handoff recorded `617B0BE3B25BB9DF6D112FC8F08D5A0779D703A20FC53F0E7B367D6828A187C0` as the preparation-time digest. That value matches neither the current queue nor the task manifests and must not be used as an acceptance gate.

## Current boundary

- Manifest status is `specified`, not `reviewed` or `ready`.
- Owner and independent reviewer are role placeholders; named identities are required before readiness.
- Allowed paths are limited to ADR-0009/source-strategy records, no-claim compatibility fixtures and validators, and research documentation.
- `apps/`, `crates/`, `prototype/`, release packaging, signing material, and browser-engine source imports remain prohibited.
- `PB-002` remains blocked until owner-reviewed evidence or explicit blocked status is recorded for every ADR-0009 evidence item.

## Owner review inputs

Before changing this manifest to `reviewed` or `ready`, the owner and independent reviewer must confirm:

1. Named owner and independent reviewer identities, with neither being the implementing agent.
2. The source queue digest still matches the manifest precondition, or the manifest is regenerated and re-reviewed.
3. Requirements, risks, ADR-0009 scope, allowed paths, prohibited paths, resource budget, expiry, rollback, and evidence destination are unchanged and sufficient.
4. Network destinations, credentials, and retention rules are explicitly bound, or the task runs with no network and no credentials.
5. The task remains documentation/research-only and cannot modify release-path browser code.
6. A separate agent run manifest and evidence bundle are created before execution.
7. The independent reviewer will review the latest source commit, raw outputs, hashes, validation results, failures, and unsupported boundaries.

## Review sequence

Review the source-strategy packet in this order so later evidence is not interpreted before its prerequisites:

1. Select or explicitly decline a source baseline and define the accepted provenance/equivalence policy.
2. Accept or reject the clean-build replay protocol and require independent-host or approved clean-VM reproduction.
3. Resolve dependency, license, advisory, SBOM, native-package, generated-output, build-script, unsafe, and FFI evidence for the selected baseline and feature profile.
4. Decide component boundaries and the JavaScript-runtime relationship before any selective engine integration is considered.
5. Require compatibility, performance, security, maintenance, and public-claim evidence to use the same selected baseline and disclosed workload.
6. Record an accepted, rejected, or explicitly blocked ADR-0009 decision with synchronized requirements, risks, support language, and residual-risk updates.

No later step can compensate for an unresolved earlier step. In particular, a successful build or benchmark cannot substitute for source provenance, legal review, component-boundary review, or the ADR-0009 decision.

## Rejection conditions

Reject the handoff if it is treated as task approval, if role placeholders remain, if the queue digest is stale, if scope expands into source crates or the prototype, if evidence is summarized without raw artifacts, or if any result is represented as source-strategy approval, compatibility, security, performance, production, or Chrome-class evidence.

## Validation

The specified manifest must validate against [`execution-task.schema.json`](machine/execution-task.schema.json). Repository validation remains required before any later status change. This handoff does not authorize execution by itself.
