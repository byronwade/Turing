# IPC Transport and Authority Closure Preparation - July 2026

Status: no-claim execution and review route for `PB-011`, `TASK-000003`, and `TASK-000011`; no transport, wire codec, or production IPC has been approved
Owner: architecture, API/protocol, security, quality, performance, and independent review
Research date: 2026-07-19

## Question

What evidence order lets Turing review the contained `TASK-000011` policy reference, decide the wire representation, and later test a real authenticated transport without confusing those scopes or expanding authority through page content, extensions, DevTools, agents, or generated data?

## Current boundary

The repository has a review-pending M0 policy reference, a non-accepting `TASK-000011` evidence capture, an IPC capability-boundary inventory, a schema-source template, a wire-encoding decision-preparation report, and a no-claim IPC readiness-review template. These records make the missing work reviewable. They do not establish a canonical wire encoding, a schema generator, a platform transport, peer authentication, handle transfer, timeout/cancellation behavior on a real channel, or production IPC.

`TASK-000011` and `TASK-000003` have different scopes:

| Scope | Evidence that may be reviewed | Evidence it must not imply |
|---|---|---|
| `TASK-000011` M0 reference | Generated role/capability records, typed identities, bounded envelopes and queues, deterministic policy checks, route/endpoint authorization, and contained Rust tests on the exact commit. | Accepted transport, process isolation, sandboxing, site isolation, renderer security, production IPC, or approval of `TASK-000003`. |
| Wire decision | Owner-reviewed comparison of candidate encodings, bounded decoding, evolution, generator provenance, deterministic-byte requirements, fuzzability, and performance/security test plan. | Selection of a dependency, generator, schema source, transport, or release path until the decision record is accepted. |
| `TASK-000003` transport work | Reviewed task manifest, canonical schema/codec proposal, platform transport experiment, authenticated peer/channel binding, negative tests, failure-state evidence, and owner-reviewed readiness review. | Broad browser implementation, production IPC, renderer or agent security, site isolation, or Chrome-class readiness without the remaining gates. |

## Required evidence order

The continuation route is:

1. **Review `TASK-000011` first.** Re-run generation, formatting, lint, tests, shell integration, prototype, and documentation checks on the exact review commit. Record an independent evidence bundle that accepts or rejects only the M0 policy-reference scope.
2. **Make the wire decision explicit.** Compare the candidate encodings from the [IPC Wire-Encoding Decision Preparation](ipc-wire-encoding-decision-prep-2026-07.md) against bounded decoding, schema evolution, deterministic diagnostics, generator/source provenance, license/advisory review, fuzzability, allocation/copying cost, and cross-language/platform maintenance. Record selected, rejected, or deferred status for every candidate.
3. **Freeze the control envelope before transport.** Bind message kind, version, source and destination principal, process epoch, document/profile/site context where applicable, channel, sequence, request/response correlation, capability requirement, size/resource charge, deadline, cancellation token, and terminal outcome. Unknown fields, versions, principals, epochs, routes, and capability meanings must fail closed or be explicitly quarantined.
4. **Run one platform transport experiment per supported platform.** Keep the same envelope and policy oracle while testing the platform-specific transport adapter. Capture peer authentication, channel registration, endpoint binding, process-epoch binding, handle-transfer or shared-memory lease rules, queue/backpressure limits, close/half-close, crash/reconnect, timeout, cancellation, and cleanup behavior.
5. **Exercise hostile and adversarial paths.** The evidence set must include malformed, truncated, oversized, nested, duplicate, reordered, stale, unauthorized, wrong-principal, wrong-epoch, unknown-version, unknown-capability, timeout, cancellation, disconnect, retry, replay, resource-exhaustion, and compromised-client cases. Success-only tests are insufficient.
6. **Review authority and resource effects.** Prove that page content, model output, extension input, DevTools input, or agent observations cannot mint capabilities, widen routes, alter peer identity, bypass confirmation, or select privileged handles. Record queue, allocation, copy, CPU, timeout, and cancellation ownership so a failed or abandoned operation cannot retain authority or resources.
7. **Submit one readiness review.** Replace the no-claim IPC readiness-review template with exact source commit, schema/codec identity, platform matrix, raw logs and hashes, test denominator, failure/waiver records, reviewer identities, unresolved limitations, and explicit claim boundaries.

## Evidence matrix

The future evidence bundle must link each axis to an artifact, command or test, result, and reviewer disposition:

| Axis | Minimum proof | Rejection condition |
|---|---|---|
| Schema authority | Canonical source, generator/version or codec provenance, generated-output hashes, drift check | Generated output is edited directly, provenance is missing, or source and output disagree |
| Wire safety | Bounded framing/decoding, length/nesting/offset checks, unknown-value policy, malformed-input tests | Decoder trusts lengths, offsets, tags, or zero-copy views before validation |
| Peer authority | OS transport identity bound to kernel-registered process, role, epoch, channel, and route | Transport identity is accepted without broker/kernel binding or can be replayed after restart |
| Capability authority | Per-message route/capability checks with attenuation-only behavior | Page, extension, DevTools, agent, or model data can mint or widen authority |
| Lifecycle | Timeout, cancellation, close, half-close, crash, reconnect, retry, and stale-epoch state machines | Cancellation leaks work/authority, reconnect accepts stale state, or terminal outcomes are ambiguous |
| Resource bounds | Queue bytes/items, allocation, copy, CPU, deadline, handle/lease, and cleanup accounting | A failure path bypasses limits, hides ownership, or retains resources indefinitely |
| Negative coverage | Hostile, stale, duplicate, reordered, unauthorized, wrong-principal, and exhaustion cases | Only success-path or in-process tests exist |
| Platform coverage | Declared Windows, Linux, and macOS transport/handle behavior with controls and limitations | A platform is called supported from an unexecuted adapter or a stub |
| Independent review | Exact commit, retained logs/hashes, failure denominator, named reviewers, decision and expiry | Template, passing validator, or placeholder reviewer is treated as acceptance |

## Gate and claim effect

`PB-011` remains `partial`. The next useful proof is an independent `TASK-000011` review decision, followed by a reviewed wire/transport task. No report, template, generated reference, or passing M0 test promotes `PB-011`, accepts a schema generator, authorizes a platform transport, or supports renderer-security, agent-security, process-isolation, site-isolation, production IPC, or Chrome-class claims.

The route is compatible with the [IPC Capability Boundary Inventory](ipc-capability-boundary-inventory-2026-07.md), [WP-002 reference](wp-002-kernel-ipc-2026-07.md), [TASK-000011 review handoff](task-000011-wp002-review-handoff-2026-07.md), [IPC wire-encoding decision preparation](ipc-wire-encoding-decision-prep-2026-07.md), and the specified [TASK-000003 manifest](../agent-execution/machine/tasks/TASK-000003.json). Those sources remain authoritative for their respective scopes.

The [IPC Transport Packet Examples](ipc-transport-packet-examples-2026-07.md) supplies a fictitious packet covering schema provenance, control-envelope identity, peer/channel binding, negative and lifecycle cases, resource accounting, platform differences, and review rejection rules. It is a handoff example only and does not satisfy `PB-011` evidence.

Any future `PB-011` decision must also be reconciled through the [PB-020 owner-decision closure board](../project-buildout/23-owner-decision-closure-board.md) and [build-readiness closure preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md). IPC acceptance cannot independently authorize broad implementation, renderer or agent security, site isolation, release, or production claims.

## Next controlled action

Prepare an independent review record for `TASK-000011` on the exact commit. Do not start transport implementation or claim `TASK-000003` readiness until that review, the source/wire decision, and an immutable task approval record exist.
