# IPC Capability Boundary Inventory - July 2026

Status: checked no-claim boundary inventory, review-pending M0 reference evidence, and checked no-claim readiness-review template
Owner: architecture, API/protocol, security, agent-operations, and documentation-research
Related gate: `PB-011` Canonical IPC schema and process capability generation
Updated: 2026-07-18

## Question

Can `PB-011` keep its no-claim boundary inventory coherent after the review-pending `WP-002` M0 reference exists, without implying `TASK-000011` acceptance, wire encoding, owner-reviewed IPC readiness, production IPC, renderer security, agent security, process-isolation readiness, site-isolation, timeout/cancellation behavior, or broad implementation readiness?

The checked no-claim [IPC wire-source manifest](../blueprint-v1/machine/ipc-wire-source-manifest.json) records the official encoding and platform-transport observations that inform this inventory. It does not select an encoding, approve a generator, authenticate a transport, or establish production IPC.

## Short Answer

Yes, for boundary planning, review handoff, and non-accepting evidence capture only. The [`ipc-capability-boundary.json`](../blueprint-v1/machine/ipc-capability-boundary.json) registry, [WP-002 kernel identity and IPC reference](wp-002-kernel-ipc-2026-07.md), [TASK-000011 WP-002 Review Handoff](task-000011-wp002-review-handoff-2026-07.md), checked no-claim [TASK-000011 evidence capture](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json), checked no-claim [IPC schema-source template](../blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), checked no-claim [IPC readiness-review template](../blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json), [`validate_evidence_bundles.py`](../../tools/validate_evidence_bundles.py), [`validate_ipc_capability_boundaries.py`](../../tools/validate_ipc_capability_boundaries.py), and [`validate_ipc_readiness_review.py`](../../tools/validate_ipc_readiness_review.py) make the current M0 IPC and process-capability evidence explicit and define the future owner-review handoff. They connect the existing `turing-ipc`, `turing-kernel`, `turing-types`, generated reference, and [`process-capabilities.json`](../blueprint-v1/machine/process-capabilities.json) records to the missing accepted `TASK-000011` evidence bundle, wire encoding decision, authentication, stale-epoch receiver proof on a real transport, timeout, cancellation, owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template, and transport-level negative-test requirements.

This is not a production IPC protocol, accepted execution task, accepted independent evidence-bundle instance, owner-reviewed IPC readiness review, renderer sandbox, process-isolation proof, site-isolation proof, schema-generator approval for production use, schema-source approval, or wire-encoding decision.

## Inputs

- [System Architecture](../blueprint-v1/04-system-architecture.md)
- [Security, Privacy, and Sandbox Model](../blueprint-v1/08-security-and-sandbox.md)
- [API Design](../api-design/README.md)
- [Schemas, Errors, Versioning, and Compatibility](../api-design/03-schemas-errors-versioning-and-compatibility.md)
- [Asynchrony, Streaming, and Cancellation](../api-design/02-async-streaming-and-cancellation.md)
- [Capability Provenance, Attenuation, and Revocation](../security-engine/10-capability-provenance-attenuation-and-revocation.md)
- [`ipc-capability-boundary.schema.json`](../blueprint-v1/machine/ipc-capability-boundary.schema.json)
- [`ipc-capability-boundary.json`](../blueprint-v1/machine/ipc-capability-boundary.json)
- [`ipc-schema-source.schema.json`](../blueprint-v1/machine/ipc-schema-source.schema.json)
- [`no-claim-control-envelope-template.json`](../blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json)
- [`ipc-readiness-review.schema.json`](../blueprint-v1/machine/ipc-readiness-review.schema.json)
- [`no-claim-ipc-readiness-template.json`](../blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json)
- [WP-002 kernel identity and IPC reference](wp-002-kernel-ipc-2026-07.md)
- [IPC wire-encoding decision preparation](ipc-wire-encoding-decision-prep-2026-07.md)
- [TASK-000011 WP-002 Review Handoff](task-000011-wp002-review-handoff-2026-07.md)
- checked no-claim [TASK-000011 evidence capture](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json)
- [`TASK-000011`](../agent-execution/machine/tasks/TASK-000011.json)
- [`validate_ipc_capability_boundaries.py`](../../tools/validate_ipc_capability_boundaries.py)
- [`validate_ipc_readiness_review.py`](../../tools/validate_ipc_readiness_review.py)

## Current M0 Evidence

The checked inventory records:

- `ControlEnvelope` stores sender, receiver, sequence, optional document epoch, encoded length, and typed payload;
- `rejects_oversized_control_messages` rejects declared control messages above `MAX_CONTROL_MESSAGE_BYTES`;
- `ProcessRole`, `Capability`, `CapabilitySet`, and `ProcessPolicy` model role defaults;
- `schemas/ipc/control-plane.json` drives the review-pending generated role, capability, message, route, limit, and process-capability reference;
- `BoundedQueue` applies item and byte budgets and stores admission-time byte charge;
- `ProcessRegistry` authorizes launches, capability attenuation, channel registration, endpoint binding, generated routes, and sequence state;
- focused kernel tests deny renderer network/file access, network profile-storage access, and agent ambient browser authority;
- typed IDs reject zero and preserve explicit routing metadata;
- `process-capabilities.json` lists role capabilities and forbidden authority for the current process model.

## Missing Evidence

The checked inventory keeps `PB-011` partial because the following are still missing:

- accepted `TASK-000011` evidence bundle for the generated M0 reference;
- wire encoding decision;
- connection authentication against trusted kernel process state;
- operating-system transport binding for bounded queues and backpressure;
- timeout semantics;
- cancellation semantics;
- stale-epoch receiver rejection on a real transport;
- fuzz and model tests for decoders, queues, state machines, duplicate delivery, reordering, authorization, wrong principal, timeout, cancellation, and resource exhaustion.

The dated [IPC wire-encoding decision preparation](ipc-wire-encoding-decision-prep-2026-07.md) records the candidate comparison and decision gates for CBOR, Protocol Buffers, FlatBuffers, and a Turing-owned codec. It is research evidence only: no encoding, dependency, generator, or transport has been selected.

## Negative Coverage

The inventory requires tests or generated fixtures for:

- malformed encodings;
- oversized messages;
- stale document epochs;
- duplicate messages;
- reordered messages;
- unauthorized capabilities;
- wrong-principal routing;
- timeout behavior;
- cancellation behavior.

The [TASK-000011 WP-002 Review Handoff](task-000011-wp002-review-handoff-2026-07.md) maps current M0 unit tests for oversized messages, zero identity, document-epoch scope, duplicate/skipped sequences, queue overcommit, unauthorized launch, capability escalation, stale process epochs, removed-process relaunch, denied routes, missing attenuated capabilities, unregistered channels, unauthorized and duplicate channel registration, endpoint binding, and mutable encoded-size accounting. Transport-level malformed, reordered, wrong-principal, timeout, cancellation, compromised-client, crash/reconnect, and hostile decoder cases remain missing or not executable until the wire and transport contract exists.

## Checked No-Claim Readiness-Review Template

The checked IPC readiness-review template adds the owner-review handoff shape for a future real `PB-011` readiness review. It keeps the boundary inventory, schema-source template, schema generator, wire encoding decision, owner reviewer, security reviewer, architecture reviewer, API reviewer, and performance reviewer fields null. Every readiness and claim-support flag remains false.

The template records the evidence axes a real review must replace with proof: schema-generator source and generated output, wire encoding, bounded decode, connection authentication, bounded queues and backpressure, timeout and cancellation semantics, stale document epoch rejection, role authority for browser kernel, renderer, network, storage, GPU, media utility, extension host, DevTools, agent host, updater, and crash handler, plus malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, cancellation, fuzz, and model-test evidence.

## Decision

`PB-011` remains `partial`. The inventory, review-pending WP-002 reference, `TASK-000011` review handoff, IPC schema-source template, and IPC readiness-review template are useful because they make the boundary, future schema-source handoff object, future owner-review handoff object, and missing evidence machine-checkable. They do not approve production IPC work. Any move beyond partial requires accepted `TASK-000011` evidence, reviewed wire encoding, per-message capability requirements on a real transport, authenticated sender/role state, timeout/cancellation tests, stale-epoch receiver rejection, wrong-principal denial, fuzz/model coverage, and owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template.

## Unsupported Boundaries

The inventory explicitly keeps these outside the proof:

- no renderer-security claim;
- no agent-security claim;
- no process-isolation readiness claim;
- no site-isolation claim;
- no production IPC claim;
- no owner-reviewed IPC readiness claim;
- no `PB-011` readiness promotion;
- no wire encoding decision claim;
- no schema generator claim;
- no accepted `TASK-000011` claim;
- no accepted independent evidence-bundle instance claim;
- no approved schema-source claim;
- no timeout or cancellation implementation claim;
- no implementation readiness claim.

## Next Proof Required

To advance `PB-011`, the next task should produce:

1. independent review of `TASK-000011` with an evidence bundle tied to the exact source commit;
2. reviewed wire encoding decision and decoder-bound behavior;
3. generated fixtures for malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases;
4. real-transport bounded queue, backpressure, control-message priority, and cancellation-starvation tests;
5. per-message sender role, receiver role, capability, profile, origin/site, document epoch, and resource-owner checks;
6. fuzz or model tests for decoder and state-machine behavior;
7. owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template;
8. security and architecture owner review before any process-isolation, renderer-security, agent-security, or production IPC claim.

## Validation

Run:

```bash
python3 -B tools/validate_ipc_capability_boundaries.py
python3 -B tools/validate_ipc_readiness_review.py
python3 -B tools/validate_blueprint.py
```

The aggregate Windows wrapper also runs the blueprint validator:

```powershell
.\tools\check.ps1
```
