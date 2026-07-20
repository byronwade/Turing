# Bounded API and Protocol Contract Research - July 2026

Status: active `RQ-13`/`RQ-22`/`RQ-36` source-backed protocol and API route; no wire-format, schema, transport, IPC, DevTools, automation, agent, compatibility, security, performance, or production claim
Owner: architecture, IPC, API, developer-experience, security, quality, performance, and agent-platform owners
Research date: 2026-07-19
Related questions: `RQ-13`, `RQ-22`, `RQ-36`
Related gates: `PB-011`, `PB-020`

## Question

Which API and protocol conventions minimize misuse, authority leakage, resource exhaustion, and long-term compatibility cost while supporting bounded binary and structured encodings, streaming, cancellation, diagnostics, and generated clients?

This packet consolidates the shared contract questions for IPC, DevTools, headless automation, agents, traces, and future public APIs. It does not select an encoding, transport, schema language, or public protocol.

## Source-backed observations

### Schemas define structure, not authority

JSON Schema defines a JSON media type for describing data structure, validation, references, vocabularies, and annotation. A schema can constrain shape, but it cannot by itself authenticate a peer, authorize an operation, preserve process/document identity, enforce resource budgets, or determine whether a command is safe.

Schema validation must therefore be one layer in a receiver-side policy pipeline, never the policy boundary itself.

### Errors need machine-readable semantics

RFC 9457 defines a machine-readable problem-detail format for HTTP API errors. The relevant principle for Turing is stable error identity and structured diagnostic fields, while keeping sensitive information out of the response. Internal, IPC, and browser-facing protocols may need different encodings, but each must separate stable error class, retryability, correlation, authority, and redaction from incidental text.

### Bidirectional browser protocols separate commands, results, and events

The W3C WebDriver BiDi working draft defines modules, commands, results, events, sessions, capabilities, errors, and bidirectional transport. It explicitly models asynchronous commands that may complete out of order and event streaming. This is useful evidence for protocol shape, not a mandate to adopt WebDriver BiDi internally or to copy its authority model.

### Wire encoding has compatibility and resource consequences

Protocol Buffers documentation separates the definition language, generated code, runtime libraries, serialized format, and wire encoding. Its encoding documentation also describes unknown/missing fields, field ordering, size limits, and the fact that ordinary serialization is not necessarily deterministic. Any binary candidate must define canonicalization needs, unknown-field policy, size limits, recursion limits, allocation accounting, and version behavior rather than assuming a serialization library supplies them.

These observations do not establish that JSON, CDDL, Protocol Buffers, or any other candidate is correct for Turing.

## Contract layers

Every protocol must specify these layers separately:

1. **Schema:** message kinds, fields, types, versions, optionality, unknown-field policy, and generated source.
2. **Identity:** sender/receiver principal, process and restart epoch, profile/site/frame/document identity, channel, request correlation, and capability context.
3. **Authority:** operation authorization, attenuation, confirmation, peer authentication, origin/profile policy, and receiver-side recomputation.
4. **Resource:** encoded and decoded byte limits, recursion, item count, queue charge, CPU/time budget, memory, shared buffers, handles, and external resources.
5. **Lifecycle:** deadline, cancellation, timeout, retry, idempotency, ordering, duplicate handling, crash/reconnect, and terminal state.
6. **Transport:** local or remote channel, framing, authentication, encryption, backpressure, fairness, connection limits, and handle transfer.
7. **Semantics:** success, partial result, structured error, redaction, diagnostic detail, and user-visible consequence.
8. **Compatibility:** version negotiation, feature discovery, deprecation, migration, generated clients, support window, and unsupported behavior.
9. **Evidence:** schema source, generator/version, exact wire bytes, corpus, fuzzing, negative tests, performance, security, accessibility, and independent review.

## Shared conventions to compare

| Concern | Required candidate comparison | Rejection condition |
|---|---|---|
| Schema source | JSON Schema, CDDL, Protocol Buffers, or another reviewed source with generated bindings | hand-written duplicated schemas drift across languages or domains |
| Encoding | bounded structured and binary formats with exact size/CPU/allocation measurements | parser accepts unbounded length, recursion, nesting, or allocation |
| Errors | stable code/class, retryability, correlation, redaction, and remediation fields | callers must parse human text or error details leak secrets |
| Identity | typed principal, epoch, document/profile/site context, channel, and correlation | receiver trusts caller-provided origin, scope, or process identity |
| Authority | receiver-side capability and policy check with attenuation and explicit confirmation where required | schema or model output can expand authority |
| Streaming | event ordering, subscription scope, backpressure, cancellation, and replay/retention policy | producer can overwhelm consumer or event scope crosses principals |
| Failure | malformed, unknown, duplicate, reordered, stale, oversized, unauthorized, timeout, cancellation, crash, and reconnect behavior | failure is swallowed, retried indefinitely, or changes security state ambiguously |
| Evolution | version negotiation, unknown fields, feature flags, deprecation, and migration | new sender silently changes old receiver semantics |
| Generated clients | source/version binding, deterministic regeneration, language mappings, and conformance suite | generated output is edited by hand or provenance is absent |
| Diagnostics | causal correlation, bounded trace fields, redaction, retention, and access control | logs contain secrets, raw page data, or unbounded payloads |

## Candidate domains

Do not force one protocol to satisfy every domain. Compare at least:

- kernel and privileged IPC;
- renderer/network/storage/GPU/decoder process messages;
- shared-memory and platform-handle leases;
- DevTools and headless diagnostics;
- WebDriver-compatible automation and Turing-specific instrumentation;
- agent observations, actions, grants, providers, and audit events;
- benchmark traces and evidence artifacts;
- public embedding or SDK boundaries if that scope is later accepted.

Each domain must declare whether it is internal, local-only, remote-capable, public, experimental, or stable, and must not inherit authority from a domain with a different trust model.

## Evidence and test contract

For each candidate domain and encoding, retain:

- schema source, dialect/version, generator, runtime, generated-output hash, and source commit;
- representative valid, invalid, truncated, unknown, duplicate, reordered, stale, oversized, deeply nested, and resource-exhaustion messages;
- peer, principal, process epoch, document epoch, profile, site, frame, channel, and capability fixtures;
- deadline, timeout, cancellation, retry, idempotency, crash, reconnect, and partial-result cases;
- queue/backpressure, fairness, memory, CPU, allocation, copy, shared-memory, handle, and transport measurements;
- structured errors, redaction, audit, causal trace, privacy, and access-control records;
- compatibility matrix across versions, feature negotiation, unknown fields, downgrade, and migration behavior;
- fuzz/model/property tests, generated-client conformance, differential parser checks, and independent review;
- owner, reviewer, limitations, unsupported behavior, claim scope, and evidence expiry.

## Rejection and promotion rules

Reject a candidate when the receiver cannot independently recompute authority, identity, limits, or lifecycle state; when malformed input can cause unbounded work; when cancellation and crash cleanup are undefined; when version evolution changes semantics silently; when diagnostics expose secrets or page data; when generated output lacks provenance; or when performance claims omit isolation, copies, queue pressure, and failure behavior.

Promote a domain only after its source schema, bounded implementation, negative/failure/recovery tests, compatibility policy, security review, accessibility implications, resource measurements, and independent evidence are accepted by the owner. A schema validator, generated code, self-test, or protocol comparison does not approve production IPC or public API compatibility.

## Current status and claim boundary

`RQ-13`, `RQ-22`, and `RQ-36` remain active in the IPC/process-authority crosswalk. This packet closes a shared research-route and contract-definition gap only. It does not select Protocol Buffers, JSON Schema, CDDL, a wire format, a transport, a public protocol, or an IPC implementation, and it does not change `PB-011`, `PB-020`, or the current `90%` contained-M0 / `0%` full-build closure metrics.

## Next question

Which owner-approved domain should receive the first generated schema and real-transport negative-test trial, and which resource, authority, or compatibility failure must reject the candidate?

## Sources

- [JSON Schema 2020-12 core](https://json-schema.org/draft/2020-12/json-schema-core.html)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [W3C WebDriver BiDi](https://www.w3.org/TR/webdriver-bidi/)
- [Protocol Buffers encoding](https://protobuf.dev/programming-guides/encoding/)
- [Protocol Buffers overview](https://protobuf.dev/overview/)
