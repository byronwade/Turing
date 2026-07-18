# IPC Capability Boundary Inventory - July 2026

Status: checked no-claim boundary inventory and checked no-claim readiness-review template
Owner: architecture, API/protocol, security, agent-operations, and documentation-research
Related gate: `PB-011` Canonical IPC schema and process capability generation
Updated: 2026-07-18

## Question

Can `PB-011` move from crate evidence and prose into checked planning evidence and a checked no-claim readiness-review handoff without implying that a canonical schema generator, wire encoding, owner-reviewed IPC readiness, production IPC, renderer security, agent security, process-isolation readiness, site-isolation, timeout/cancellation behavior, or broad implementation readiness exists?

## Short Answer

Yes, for boundary planning only. The new [`ipc-capability-boundary.json`](../blueprint-v1/machine/ipc-capability-boundary.json) registry, checked no-claim [IPC schema-source template](../blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), checked no-claim [IPC readiness-review template](../blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json), [`validate_ipc_capability_boundaries.py`](../../tools/validate_ipc_capability_boundaries.py), and [`validate_ipc_readiness_review.py`](../../tools/validate_ipc_readiness_review.py) make the current M0 IPC and process-capability evidence explicit and define the future owner-review handoff. They connect the existing `turing-ipc`, `turing-kernel`, `turing-types`, and [`process-capabilities.json`](../blueprint-v1/machine/process-capabilities.json) records to the missing implemented schema generator evidence beyond the checked no-claim schema-source template, wire encoding decision, bounded queues, authentication, stale-epoch rejection, timeout, cancellation, owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template, and negative-test requirements.

This is not a production IPC protocol, owner-reviewed IPC readiness review, renderer sandbox, process-isolation proof, site-isolation proof, schema-generator approval, schema-source approval, or wire-encoding decision.

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
- [`validate_ipc_capability_boundaries.py`](../../tools/validate_ipc_capability_boundaries.py)
- [`validate_ipc_readiness_review.py`](../../tools/validate_ipc_readiness_review.py)

## Current M0 Evidence

The checked inventory records:

- `ControlEnvelope` stores sender, receiver, sequence, optional document epoch, encoded length, and typed payload;
- `rejects_oversized_control_messages` rejects declared control messages above `MAX_CONTROL_MESSAGE_BYTES`;
- `ProcessRole`, `Capability`, `CapabilitySet`, and `ProcessPolicy` model role defaults;
- focused kernel tests deny renderer network/file access, network profile-storage access, and agent ambient browser authority;
- typed IDs reject zero and preserve explicit routing metadata;
- `process-capabilities.json` lists role capabilities and forbidden authority for the current process model.

## Missing Evidence

The checked inventory keeps `PB-011` partial because the following are still missing:

- implemented schema generator evidence beyond the checked no-claim schema-source template;
- wire encoding decision;
- connection authentication against trusted kernel process state;
- bounded queues and backpressure;
- timeout semantics;
- cancellation semantics;
- stale document epoch rejection;
- fuzz and model tests for decoders, queues, state machines, duplicate delivery, reordering, authorization, wrong principal, timeout, cancellation, and resource exhaustion.

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

Only the oversized declared-length case has an implemented M0 unit test today. The other cases remain missing or not executable until the schema and transport contract exist.

## Checked No-Claim Readiness-Review Template

The checked IPC readiness-review template adds the owner-review handoff shape for a future real `PB-011` readiness review. It keeps the boundary inventory, schema-source template, schema generator, wire encoding decision, owner reviewer, security reviewer, architecture reviewer, API reviewer, and performance reviewer fields null. Every readiness and claim-support flag remains false.

The template records the evidence axes a real review must replace with proof: schema-generator source and generated output, wire encoding, bounded decode, connection authentication, bounded queues and backpressure, timeout and cancellation semantics, stale document epoch rejection, role authority for browser kernel, renderer, network, storage, GPU, media utility, extension host, DevTools, agent host, updater, and crash handler, plus malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, cancellation, fuzz, and model-test evidence.

## Decision

`PB-011` remains `partial`. The new inventory, IPC schema-source template, and IPC readiness-review template are useful because they make the boundary, future generator handoff object, future owner-review handoff object, and missing evidence machine-checkable. They do not approve production IPC work. Any move beyond partial requires an implemented and reviewed schema generator, reviewed wire encoding, per-message capability requirements, authenticated sender/role state, bounded queue and backpressure tests, timeout/cancellation tests, stale-epoch rejection, wrong-principal denial, fuzz/model coverage, and owner-reviewed IPC readiness review beyond the checked no-claim IPC readiness-review template.

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
- no approved schema-source claim;
- no timeout or cancellation implementation claim;
- no implementation readiness claim.

## Next Proof Required

To advance `PB-011`, the next task should produce:

1. implemented schema generator evidence beyond the checked no-claim schema-source template and linked to `process-capabilities.json`;
2. reviewed wire encoding decision and decoder-bound behavior;
3. generated fixtures for malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases;
4. bounded queue, backpressure, control-message priority, and cancellation-starvation tests;
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
