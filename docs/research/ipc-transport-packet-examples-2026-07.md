# IPC Transport Packet Examples - July 2026

Status: no-claim sample packet shape for `PB-011`, `TASK-000003`, and `TASK-000011`; no wire encoding, transport, process-isolation, renderer-security, or production IPC claim
Owner: architecture, API/protocol, security, quality, performance, and independent review
Research date: 2026-07-19

## Purpose

The [IPC Transport and Authority Closure Preparation](ipc-transport-and-authority-closure-preparation-2026-07.md) defines the evidence order, while the [IPC Capability Boundary Inventory](ipc-capability-boundary-inventory-2026-07.md) and [IPC Wire-Encoding Decision Preparation](ipc-wire-encoding-decision-prep-2026-07.md) define the current M0 boundary and candidate decision criteria. This page gives a sample-only packet shape showing how schema provenance, control-envelope identity, peer authentication, lifecycle, negative cases, resource accounting, and platform limits should be retained together.

All values are fictitious placeholders. They do not establish a wire codec, generator, transport, authenticated peer, process isolation, or security result.

## Packet identity and schema provenance

```yaml
packet_status: sample_only_no_claim
packet_id: IPC-SAMPLE-TRANSPORT-0001
task_id: TASK-000003
reference_task_id: TASK-000011
source_commit: SAMPLE-COMMIT-REPLACE-BEFORE-USE
schema_source: SAMPLE-SCHEMA-SOURCE
generator_or_codec: SAMPLE-GENERATOR-OR-CODEC
generator_version: SAMPLE-VERSION
toolchain: SAMPLE-TOOLCHAIN-MANIFEST
feature_profile: SAMPLE-FEATURE-PROFILE
generated_output_sha256: SAMPLE-GENERATED-HASH
wire_encoding_status: decision_not_selected_in_sample
platform: windows-x64
transport_adapter: sample-not-implemented
```

Generated output, schema source, codec, generator, toolchain, and artifact hashes must be retained together. Editing generated output directly or treating a validator as wire/transport evidence is a rejection condition.

## Control-envelope record

Every message record carries authority and resource context outside page-controlled payload values.

```yaml
message:
  kind: navigation_intent
  protocol_version: SAMPLE-VERSION
  sender_role: renderer
  receiver_role: browser_kernel
  sender_process_epoch: SAMPLE-PROCESS-EPOCH
  receiver_process_epoch: SAMPLE-PROCESS-EPOCH
  channel_id: SAMPLE-CHANNEL
  sequence: SAMPLE-SEQUENCE
  correlation_id: SAMPLE-CORRELATION
  document_epoch: SAMPLE-DOCUMENT-EPOCH
  profile_id: SAMPLE-PROFILE
  origin_site_frame: SAMPLE-ORIGIN-SITE-FRAME
  required_capability: SAMPLE-ATTENUATED-CAPABILITY
  encoded_length: SAMPLE-LENGTH
  queue_byte_charge: SAMPLE-CHARGE
  deadline: SAMPLE-DEADLINE
  cancellation_token: SAMPLE-CANCELLATION
  terminal_outcome: sample_not_run
```

Unknown versions, principals, epochs, routes, capabilities, sizes, and resource owners must fail closed or enter an explicitly quarantined state according to message class.

## Peer and channel binding

| Axis | Required retained evidence | Sample status |
|---|---|---|
| Process identity | OS or broker-observed process identity, role, restart epoch | `not_run` |
| Channel registration | Trusted registrar, channel ID, endpoint, role pair, lifecycle | `not_run` |
| Peer authentication | Kernel/OS transport identity bound to registered process | `not_run` |
| Endpoint binding | Sender/receiver/channel/document/profile/site binding | `not_run` |
| Handle or shared-memory lease | Owner, bounds, generation, transfer, revocation, cleanup | `not_run` |
| Backpressure | Item/byte limits, admission charge, queue wait, terminal release | `not_run` |

An in-process policy test or helper process cannot substitute for the claimed transport and peer identity.

## Negative and lifecycle matrix

| Case | Required record | Valid outcome classes | Sample status |
|---|---|---|---|
| Malformed/truncated/oversized | bytes, parser boundary, allocation before/after, rejection | rejected, bounded error | `not_run` |
| Unknown version/field/capability | message class, policy, sender/receiver, result | rejected, quarantined | `not_run` |
| Wrong principal/role/channel | trusted and submitted identity, route decision | rejected | `not_run` |
| Stale process/document epoch | old/new epoch, restart, replay result | rejected | `not_run` |
| Duplicate/reordered/replayed | sequence/correlation, state transition, result | rejected, idempotent by policy | `not_run` |
| Timeout/cancellation | deadline, cancellation owner, queue state, terminal result | cancelled, timed_out, bounded failure | `not_run` |
| Close/half-close/crash/reconnect | channel state, pending work, new epoch, cleanup | closed, recovered, rejected | `not_run` |
| Resource exhaustion | queue/allocation/CPU/handle charge, release record | rejected, bounded backpressure | `not_run` |
| Compromised client | forged capability/path/handle/origin/epoch | rejected | `not_run` |

Failures, unsupported platform behavior, skipped cases, timeouts, crashes, and cleanup errors remain in the denominator.

## Authority and resource checks

The packet must prove with negative cases that page content, extension input, DevTools input, model output, or agent observations cannot mint capabilities, widen routes, alter peer identity, bypass confirmation, or select privileged handles. It must account for queue bytes/items, allocations, copies, CPU, deadlines, cancellation, handles, shared-memory leases, and cleanup so terminal failure cannot retain authority or resources.

## Platform matrix

| Platform | Required transport evidence | Sample status |
|---|---|---|
| Windows | authenticated endpoint/process binding, handle transfer, close/reconnect, job/resource behavior | `not_run` |
| Linux | authenticated endpoint/process binding, descriptor transfer, namespace/resource behavior, close/reconnect | `not_run` |
| macOS | authenticated endpoint/process binding, XPC/Mach or selected transport behavior, handle/resource lifecycle | `not_run` |

The matrix records platform differences and unsupported rows. It does not imply that an unexecuted adapter is supported or that the platforms are equivalent.

## Rejection rules and review handoff

Reject the packet when generated output lacks provenance, decoding allocates before bounds checks, peer identity is client-supplied, stale epochs are accepted, cancellation leaks work, failure bypasses resource limits, only in-process success tests exist, or a template/self-test/helper is cited as transport readiness.

The next acceptable artifact is an independent `TASK-000011` review packet tied to the exact source commit, followed by an owner-approved immutable `TASK-000003` package for one wire/transport/platform scope. It must replace sample fields with retained evidence, failure accounting, and named review before any process-isolation, renderer-security, or production IPC claim.

## Claim boundary

This page is sample-only documentation. It does not select CBOR, Protocol Buffers, FlatBuffers, or a Turing-owned codec; approve a generator or transport; establish peer authentication, process isolation, site isolation, renderer security, agent security, production IPC, Chrome-class security, or implementation readiness.
