# WP-002 Kernel Identity, Capability, and Bounded IPC Reference — July 2026

Status: M0 implementation evidence; not an operating-system IPC transport or production security claim
Owner: architecture, security, performance, quality, and documentation
Related work package: `WP-002`
Related execution task: [`TASK-000011`](../agent-execution/machine/tasks/TASK-000011.json)
Related requirements: `REQ-SEC-003`, `REQ-PERF-004`

## Purpose

Convert the process-role and IPC architecture from prose-only policy into one deterministic, dependency-free Rust reference implementation that later platform launchers and transports must match.

## Implemented reference surface

### Canonical generated control plane

[`schemas/ipc/control-plane.json`](../../schemas/ipc/control-plane.json) is the source for:

- stable process-role IDs;
- stable capability IDs;
- default role capability sets;
- role-to-role launch authority;
- message-kind IDs;
- required sender capability per message;
- role-pair route allowlists;
- document-epoch requirements;
- per-message encoded-size limits;
- queue classes with item and byte budgets.

`python3 -B tools/generate_ipc.py` deterministically produces:

- `crates/turing-ipc/src/generated.rs`;
- `docs/blueprint-v1/machine/process-capabilities.json`.

`--check` fails when either output drifts. Generated output and its review boundary are recorded as `GEN-IPC-001` in `security/generated-code.json`.

### Restart-safe identity

`turing-types` now distinguishes a stable `ProcessId` from a monotonic `ProcessEpoch`. `ProcessIdentity` combines both. Reusing a numeric process ID after restart creates a new identity, and the kernel rejects messages carrying the old epoch.

Channels, operations, sequences, and document epochs use separate non-zero types. Sequence and epoch increments fail on overflow rather than wrapping.

### Envelope validation

`turing-ipc::ControlEnvelope` carries:

- protocol version;
- message kind;
- restart-safe sender and receiver identities;
- channel ID;
- exact sequence number;
- operation ID;
- optional document epoch;
- encoded byte charge;
- typed payload.

Construction rejects a message above its generated kind limit, a required document-scoped message without an epoch, or a process-scoped message with an unexpected epoch.

### Exact channel sequencing

`SequenceTracker` accepts sequence `1` first and then exactly one higher value per message. Duplicate, old, skipped, and exhausted sequences fail without advancing state.

This is intentionally stricter than a reorder buffer. A future transport needing controlled reordering requires a separate reviewed protocol rather than silently weakening the control channel.

### Explicit backpressure

`BoundedQueue` applies both generated item-count and encoded-byte budgets. `try_push` never blocks, evicts, or drops silently. Rejected work and its reason are returned to the caller. The queue stores the byte charge at admission and releases that stored value on dequeue, so mutable or non-idempotent `EncodedSize` behavior cannot corrupt accounting or trigger an internal subtraction failure.

The current queue values are M0 safety defaults, not production performance targets. Fixed-hardware and workload evidence must replace or confirm them before preview.

### Kernel policy oracle

`turing-kernel::ProcessRegistry`:

- creates one privileged browser-kernel identity;
- permits child launch only through the generated role matrix;
- permits capability attenuation but rejects escalation above role defaults;
- caps registered processes and channels;
- permits channel creation only through an authenticated process-broker capability;
- rejects envelopes using an unregistered channel rather than allowing a sender to claim an ID implicitly;
- restarts children with a new process epoch;
- removes channels bound to exited or restarted identities;
- authenticates current sender and receiver identities;
- rejects denied message routes;
- verifies the generated required sender capability;
- binds channel IDs to one endpoint pair;
- validates exact sequence state before authorization.

The result is a deterministic policy oracle. It does not create operating-system processes, transfer handles, authenticate a real socket or shared-memory transport, or prove sandbox containment.

## Test evidence

Unit and integration tests cover:

- zero-ID rejection and process-epoch identity;
- kind-specific message-size rejection;
- document-epoch requirements;
- monotonic sequence acceptance;
- duplicate and gap rejection without state mutation;
- byte-budget backpressure and item recovery;
- immutable admission-charge release on dequeue, including a mutable-size regression case;
- renderer launch denial;
- capability-escalation denial;
- stale identity rejection after restart;
- generated role-route denial;
- missing-capability denial after attenuation;
- broker-only channel registration, unknown-channel rejection, duplicate registration denial, endpoint binding, and sequence enforcement;
- shell-level launch, queue, and authorization integration.

CI also checks deterministic regeneration, formatting, Clippy with warnings denied, all workspace tests, and the shell self-test.

## Security properties established by the reference

- Default policy is deny.
- A role's capabilities are generated from one reviewed schema.
- A child can receive no capability outside its role defaults.
- A message route must be explicitly generated.
- The authenticated sender must possess the message's required capability.
- A restarted process cannot reuse its predecessor's identity.
- An envelope cannot create a channel; a process-broker principal must register its authenticated endpoints first.
- A channel cannot silently switch endpoints.
- Queue accounting uses the charge captured before admission rather than trusting later payload behavior.
- Message, queue, process, and channel resources are bounded.
- Sequence failures and policy denials are explicit results rather than ignored conditions.

## Process-ID reuse hardening

The kernel retains the last issued epoch for every allocated `ProcessId`, including removed processes. Relaunching a previously used ID advances the epoch rather than resetting it, so stale handles and envelopes cannot become current again when process and channel identifiers are reused. The epoch ledger is bounded by the generated process-table limit. A regression test covers launch, channel registration, removal, relaunch, stale replay rejection, and fresh-sequence acceptance.

## Important limitations

The reference does not yet establish:

- operating-system process launch or sandbox policy;
- peer authentication on Unix sockets, Windows ALPC/named pipes, Mach IPC, or another transport, including binding the authenticated transport to the broker-registered channel;
- canonical binary encoding or decoding;
- shared-memory and platform-handle transfer;
- hostile decoder fuzzing of a wire codec;
- cancellation transport and response correlation beyond operation identity;
- channel close, half-close, reconnect, or crash semantics on a real transport;
- per-profile or per-site renderer assignment;
- compromised-process negative testing;
- fixed-hardware production queue budgets;
- side-channel resistance;
- production readiness for arbitrary hostile input.

`REQ-SEC-003` and `REQ-PERF-004` therefore receive M0 reference implementation evidence, not verified or production-complete status.

## Next bounded tasks

1. Define a canonical, fuzzable wire representation without introducing ambient serialization behavior.
2. Add per-platform authenticated transport spikes behind the same envelope and policy API.
3. Define typed handle-transfer and shared-memory lease contracts.
4. Add cancellation, terminal response, timeout, and channel-close state machines.
5. Build a compromised-process harness that emits malformed, stale, unauthorized, duplicate, reordered, and oversized traffic.
6. Connect process launch and negative capability probes from `WP-003`.
7. Measure queue and IPC costs in the fixed-hardware laboratory before changing M0 budgets.

## Status conclusion

`WP-002` is in progress with a buildable M0 policy reference. The work package is not complete until a real authenticated transport, generated wire codec, negative harness, platform process launcher, and independent security evidence exist.
