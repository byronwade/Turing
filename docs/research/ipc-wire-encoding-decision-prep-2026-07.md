# IPC Wire-Encoding Decision Preparation - July 2026

Status: no-claim decision-preparation research for `PB-011`; no encoding selected, no generator approved, and no production IPC claim
Owner: architecture, API/protocol, security, performance, quality, and documentation-research
Related gate: `PB-011` Canonical IPC schema and process capability generation
Research date: 2026-07-19

## Question

What evidence and decision criteria should govern Turing's IPC wire encoding before a real transport, schema generator, or production-facing message contract is approved?

## Sources checked

- IETF [RFC 8949 - Concise Binary Object Representation](https://datatracker.ietf.org/doc/html/rfc8949), including deterministic-encoding requirements.
- Official [Protocol Buffers encoding documentation](https://protobuf.dev/programming-guides/encoding/) and [language specification](https://protobuf.dev/reference/protobuf/proto2-spec/).
- Official [FlatBuffers schema documentation](https://flatbuffers.dev/schema/) and [schema-evolution rules](https://flatbuffers.dev/evolution/).
- Turing [System Architecture](../blueprint-v1/04-system-architecture.md), [Security and Sandbox Model](../blueprint-v1/08-security-and-sandbox.md), [IPC Capability Boundary Inventory](ipc-capability-boundary-inventory-2026-07.md), and [WP-002 Kernel Identity, Capability, and Bounded IPC Reference](wp-002-kernel-ipc-2026-07.md).

The external specifications describe format capabilities and evolution rules. They do not establish that any candidate is safe for Turing's process model, resource budgets, trust boundaries, or release path.

The checked [IPC wire-source manifest](../blueprint-v1/machine/ipc-wire-source-manifest.json), validated by [`validate_ipc_wire_sources.py`](../../tools/validate_ipc_wire_sources.py), records the source identities and decision consequences for these observations. It is a no-claim source record only; it does not select a codec, approve a generator, authenticate a transport, or establish production IPC.

## Non-negotiable protocol requirements

Any candidate must provide or be wrapped by an explicit Turing protocol that:

- bounds frame, message, nesting, string, vector, map, allocation, and recursion costs before untrusted allocation;
- rejects malformed, truncated, duplicate, reordered, stale, unauthorized, wrong-principal, and unknown-variant traffic according to message class;
- carries protocol version, message kind, sender and receiver identity, channel, sequence, operation, document epoch, and encoded-size accounting outside page-controlled payload claims;
- defines unknown-field and unknown-variant behavior separately for control, request, response, event, and persisted diagnostic messages;
- makes deterministic encoding requirements explicit where bytes are hashed, signed, compared, cached, or used in evidence artifacts;
- supports schema evolution without silently changing capability meaning, authority scope, origin/profile identity, or resource ownership;
- exposes decoder and state-machine seams for fuzzing, model tests, timeout, cancellation, crash/reconnect, and resource-exhaustion tests;
- keeps generated code, schema source, generator version, toolchain, feature profile, and output hashes reviewable;
- does not treat zero-copy access as validation: offsets, alignment, lengths, nesting, lifetimes, and ownership must be checked before use;
- supports platform transport authentication and binds the authenticated peer to the kernel-registered process identity and channel.

## Candidate comparison

| Candidate | Useful properties | Risks and required proof for Turing | Current disposition |
|---|---|---|---|
| CBOR with a Turing control schema | IETF standard; compact typed data model; deterministic encoding is specified as a protocol profile rather than assumed; can support multiple language implementations | Deterministic encoding is not automatic; maps and values may have multiple legal encodings; generic data model can make bounds, unknown variants, and allocation policy less obvious; decoder limits and tag policy must be explicit | Research candidate only; no dependency or schema approval |
| Protocol Buffers with a Turing control schema | Schema-driven field tags and wire types; established generated-code model; additive evolution and unknown-field behavior are useful starting points for mixed-version control paths | Generated runtime and toolchain must be bounded and audited; field presence, unknown-field retention, enum handling, recursion, length-delimited values, and deterministic serialization need explicit policy; generated code does not authenticate peers or enforce capabilities | Research candidate only; no dependency or generator approval |
| FlatBuffers with a Turing control schema | Schema compiler and direct buffer access can reduce copy/allocation work; official evolution rules support additive fields and deprecated fields | Direct access increases the obligation to validate buffer size, offsets, alignment, nesting, strings, vectors, unions, and lifetimes before access; schema evolution rules are easy to violate; zero-copy does not remove hostile-decoder risk | Research candidate only; no dependency or generator approval |
| Turing-owned compact binary codec | Exact control over framing, bounds, identity, versioning, and generated Rust surface; no external serialization semantics need be inherited | Turing owns every encoding, evolution, interoperability, fuzzing, audit, cross-language, and maintenance obligation; custom cryptography or ad-hoc authentication is prohibited; independent review burden is highest | Research candidate only; not a permission to hand-roll a codec |

These observations are architectural tradeoffs, not a scorecard. No candidate is preferred until a bounded prototype measures decode cost, allocation behavior, malformed-input behavior, generated-code auditability, and cross-version handling on representative control messages.

## Candidate-independent message-class policy proposal

The following policy is a portable decision input that must be reviewed and either accepted, amended, or rejected with the selected encoding. It keeps wire compatibility separate from authority compatibility.

| Message class | Unknown fields | Unknown variants or versions | Malformed, oversized, stale, or unauthorized input | Required record |
| --- | --- | --- | --- | --- |
| Control and authority-bearing envelope | Reject unless the field is explicitly declared ignorable by the versioned envelope contract; never let an unknown field widen identity, route, capability, resource, or deadline | Fail closed before dispatch | Reject before state mutation or unbounded allocation; emit bounded redacted diagnostics | Envelope version, field policy, rejection reason, principal/epoch/channel, and resource outcome |
| Request | Ignore only explicitly forward-compatible non-authority fields; preserve the exact decoded field set for diagnostics | Reject unknown operation, capability, principal, epoch, or resource-owner meaning | Reject before handler invocation; cancellation and timeout must produce one terminal outcome | Request schema version, operation, capability, identity context, deadline, cancellation, and terminal result |
| Response | Ignore only explicitly non-authority fields when the request version permits it; never infer success from missing fields | Reject unknown result meaning or incompatible request correlation | Reject and close/quarantine the correlation as specified; never reinterpret an error as success | Correlation, response version, result/error class, resource release, and retry/replay disposition |
| Event and notification | Ignore explicitly optional presentation/diagnostic fields; never ignore identity, epoch, subscription, or resource-owner fields | Reject unknown event meaning or stale subscription epoch | Drop or quarantine according to event criticality, with bounded accounting and no authority grant | Subscription, event version, sequence, coalescing/drop decision, and delivery outcome |
| Persisted diagnostic or evidence record | Preserve unknown fields as opaque data only when integrity and size limits hold; never execute or authorize from them | Mark as unsupported or quarantine rather than reinterpret | Reject integrity/size failures without loading unbounded content | Source/schema version, digest, capture context, parser result, and unsupported fields |

This is a protocol-policy proposal, not a selected encoding or compatibility promise. The owner decision must identify which fields are authority-bearing, which optional fields are safely ignorable, whether unknown data is preserved or discarded, and which version transitions are supported. Every exception needs a bounded version range, test case, and rejection rule.

## Decision gates

Before an owner can select an encoding, the decision packet must contain:

1. A versioned control schema for the current generated process-role, capability, route, limit, and message-kind registry.
2. A framing and length-accounting rule that can reject oversized or truncated input before unbounded allocation.
3. An unknown-field and unknown-variant policy for each message class, including fail-closed behavior for authority-bearing control messages.
4. A deterministic-byte policy for hashes, signatures, artifact identity, and diagnostics; ordinary semantic equality must not be confused with byte equality.
5. A generated-code and generator provenance record containing source revision, generator version, toolchain, feature profile, output hashes, and license/advisory review.
6. A decoder and state-machine test corpus covering malformed, truncated, nested, oversized, duplicate, reordered, stale, unauthorized, wrong-principal, timeout, cancellation, reconnect, and resource-exhaustion cases.
7. A real-transport binding experiment proving peer authentication, channel binding, process-epoch handling, backpressure, cancellation, close, and crash/reconnect behavior.
8. A cross-version compatibility matrix with explicit rejection rather than silent reinterpretation when a field, enum, capability, origin, or resource-owner meaning is incompatible.
9. A security and performance review that treats allocation, copying, cache behavior, queue pressure, and decoder CPU as measured evidence rather than assumed format properties.
10. An owner-reviewed decision record that selects, rejects, or defers each candidate and updates `PB-011`, `TASK-000011`, the API compatibility policy, the security model, and the implementation interface freeze in one change.

## Recommended experiment shape

The next no-claim experiment should use the existing generated control-plane schema and a fixed set of representative messages: navigation intent, network request, storage read, process launch, capability attenuation, cancellation, and crash/reconnect notification. Each candidate implementation should retain:

- encoded bytes and semantic round-trip result;
- allocation count/bytes, decode time, copy count where measurable, and peak temporary memory;
- malformed-input classification and failure-before-allocation evidence;
- unknown-field/variant behavior;
- maximum accepted nesting, vector/string length, and frame size;
- generated-source, dependency, toolchain, and artifact hashes;
- fuzz seed, minimization output, timeout, cancellation, and resource-exhaustion records.

This experiment is diagnostic only. It must not be used as a public performance comparison or as evidence that a candidate is production-safe.

## Current conclusion

`PB-011` remains `partial`. The research now makes the encoding decision criteria and candidate tradeoffs explicit, but it does not select CBOR, Protocol Buffers, FlatBuffers, or a Turing-owned codec. The existing schema-source template, WP-002 reference, and IPC readiness-review template remain the controlling no-claim records until an owner-reviewed wire decision and real-transport evidence exist.

## Required registry impact

This report strengthens the documented research evidence for `PB-011` and `TASK-000003`/`TASK-000011`. It does not change readiness status, approve a dependency, approve a generator, authorize a transport, or support renderer-security, process-isolation, production IPC, implementation, or performance claims.
