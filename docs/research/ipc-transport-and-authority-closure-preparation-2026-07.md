# IPC Transport and Authority Closure Preparation - July 2026

Status: no-claim execution and review route for `PB-011`, `TASK-000003`, and `TASK-000011`; no transport, wire codec, or production IPC has been approved
Owner: architecture, API/protocol, security, quality, performance, and independent review
Research date: 2026-07-20

## Question

What evidence order lets Turing review the contained `TASK-000011` policy reference, decide the wire representation, and later test a real authenticated transport without confusing those scopes or expanding authority through page content, extensions, DevTools, agents, or generated data?

## Current boundary

The repository has a review-pending M0 policy reference, a non-accepting `TASK-000011` evidence capture, an IPC capability-boundary inventory, a schema-source template, a wire-encoding decision-preparation report, and a no-claim IPC readiness-review template. These records make the missing work reviewable. They do not establish a canonical wire encoding, a schema generator, a platform transport, peer authentication, handle transfer, timeout/cancellation behavior on a real channel, or production IPC.

## Platform transport identity observations

The [Windows named-pipe security guidance](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights) makes security descriptors and access checks explicit for both ends of a pipe, while Windows impersonation introduces a separate client-token policy. Linux's [`unix(7)` documentation](https://www.man7.org/linux/man-pages/man7/unix.7.html) describes Unix-domain transport and peer-credential facilities such as `SO_PEERCRED`, alongside namespace-specific behavior. Apple's [XPC peer-platform-identity API](https://developer.apple.com/documentation/xpc/xpc_connection_set_peer_platform_identity_requirement(_:_:)) exposes platform identity and audit-session information as a connection policy input.

These sources constrain, but do not select, a Turing transport. Each platform experiment must retain the transport object/namespace, endpoint ACL or permission policy, peer identity evidence, session/namespace or entitlement context, remote-access policy, principal mapping, process epoch, reconnect/replay behavior, and impersonation or handle-transfer policy. A successful connection, credential query, audit token, or security descriptor does not independently authorize a capability or establish renderer/process/site isolation.

### Cross-platform transport worksheet

The following worksheet keeps the platform-specific mechanism separate from the portable Turing authority contract. It is a capture plan, not a recommendation or support matrix.

| Platform | Candidate mechanism and identity signal | Evidence the mechanism may provide | Turing checks that remain mandatory | Unsupported inference |
|---|---|---|---|---|
| Windows | Named pipe plus security descriptor, access check, and explicitly constrained impersonation policy | Endpoint ACL, requested access, client/server session and user context, impersonation token behavior, remote-access setting, close/reconnect result | Bind the observed peer to the broker-registered process ID and epoch; re-check role, channel, route, capability, size, deadline, cancellation, and handle lease | Opening a pipe, reading a token, or passing an ACL does not prove the Turing principal, capability, renderer isolation, or sandbox state |
| Linux | Unix-domain socket with socket namespace/type and peer-credential query such as `SO_PEERCRED` | Socket namespace, credential result, user and mount namespace context, permission policy, abstract-socket behavior, restart and replay result | Bind credentials to the exact channel and process epoch; reject stale/replayed endpoints; retain namespace, broker, route, capability, resource, and cleanup evidence | A peer-credential query or filesystem permission does not prove a stable process identity, capability authorization, or containment across namespaces |
| macOS | XPC connection with peer-platform-identity requirement and audit-session identity | Identity requirement, peer audit/session context, entitlement or signing assumptions, connection lifecycle, interruption and invalidation behavior | Bind the observed peer to the broker role, process epoch, channel, route, capability, deadline, cancellation, and handle/lease policy | An audit token, entitlement, signing identity, or live XPC connection does not prove Turing authority, safe handle transfer, renderer isolation, or release readiness |

Every future row must use the same control envelope and policy oracle. The packet must retain source/build identity, transport object and namespace, endpoint policy, peer identity output, principal/epoch mapping, channel registration, allowed and rejected operations, malformed/oversized/stale/replay/unauthorized cases, timeout and cancellation timing, crash/reconnect behavior, resource and handle cleanup, and unsupported combinations. A platform-specific transport adapter is not allowed to introduce a second authority model.

## IPC closure worksheet

The real `PB-011` review must complete one worksheet for each M0 review, wire decision, or platform transport package. The worksheet keeps the portable authority contract separate from platform mechanism details and prevents a passing in-process test from being mistaken for authenticated production IPC.

| Required field | Review package must retain | Rejection condition |
|---|---|---|
| Scope and maturity | `TASK-000011` M0 reference, wire decision, or `TASK-000003` transport package; exact source commit, schema family, and evidence level | M0 policy evidence is treated as transport or production IPC, or scopes are mixed |
| Schema and wire authority | Canonical schema source, generator/codec identity, generated-output hashes, encoding/version policy, bounded decode, unknown-value behavior, and drift result | Generated output is hand-edited, wire choice is implied, or decoder trusts unvalidated lengths/offsets |
| Peer and channel identity | Platform endpoint/namespace, OS peer evidence, broker process/role/epoch, channel registration, route, capability, profile/site/document scope, and replay policy | A token, ACL, credential, entitlement, or live connection is accepted without Turing principal/epoch binding |
| Negative and lifecycle coverage | Malformed, truncated, oversized, nested, duplicate, reordered, stale, unauthorized, wrong-principal/epoch, timeout, cancellation, disconnect, reconnect, retry, replay, and exhaustion cases | Success-only or in-process tests omit hostile or terminal paths |
| Resource and handle bounds | Queue bytes/items, allocation/copy, deadline, backpressure, handle/shared-memory lease, cleanup, and abandoned-work ownership | Failure, cancellation, or reconnect retains authority/resources or bypasses bounds |
| Platform evidence | Windows/Linux/macOS mechanism, configuration, limitations, exact commands/logs, unsupported platform cases, and security-policy controls | An unexecuted adapter or application stub is called supported |
| Review and promotion | Owner/independent/security/architecture/API/performance reviewers, failure denominator, waivers/expiry, exact allowed scope, rollback, and synchronized PB/task/ADR changes | Template, validator, or placeholder reviewer promotes PB-011 or security claims |

Until a real evidence bundle and owner-reviewed readiness review replace the no-claim templates, every worksheet row is `not_executed`, `PB-011` remains partial, and no production IPC, renderer-security, agent-security, process-isolation, site-isolation, or Chrome-class claim is supported.

### Portable authentication ordering

Every platform experiment must demonstrate the same ordered sequence:

1. observe the operating-system peer, endpoint, session, and policy context;
2. bind that observation to the broker-registered process ID, role, and restart epoch;
3. register and bind the channel before accepting application messages;
4. authorize the route and attenuated capability for each message; and
5. re-check document, profile, site, deadline, cancellation, and resource-charge state before publication or handle use.

The minimum negative set includes authorization attempted before principal binding, stale-channel replay after restart, mismatched peer identity, route or capability mismatch, and timeout or disconnect cleanup. Reconnect, restart, or endpoint replacement must invalidate affected channels, requests, handles, and leases. Platform ACLs, credentials, entitlements, and audit tokens remain evidence inputs to the Turing policy oracle rather than independent authority.

`TASK-000011` and `TASK-000003` have different scopes:

| Scope | Evidence that may be reviewed | Evidence it must not imply |
|---|---|---|
| `TASK-000011` M0 reference | Generated role/capability records, typed identities, bounded envelopes and queues, deterministic policy checks, route/endpoint authorization, and contained Rust tests on the exact commit. | Accepted transport, process isolation, sandboxing, site isolation, renderer security, production IPC, or approval of `TASK-000003`. |
| Wire decision | Owner-reviewed comparison of candidate encodings, bounded decoding, evolution, generator provenance, deterministic-byte requirements, fuzzability, and performance/security test plan. | Selection of a dependency, generator, schema source, transport, or release path until the decision record is accepted. |
| `TASK-000003` transport work | Reviewed task manifest, canonical schema/codec proposal, platform transport experiment, authenticated peer/channel binding, negative tests, failure-state evidence, and owner-reviewed readiness review. | Broad browser implementation, production IPC, renderer or agent security, site isolation, or Chrome-class readiness without the remaining gates. |

## Required evidence order

The continuation route is:

1. **Review `TASK-000011` first.** Re-run generation, formatting, lint, tests, shell integration, prototype, and documentation checks on the exact review commit. Record an independent evidence bundle that accepts or rejects only the M0 policy-reference scope.
2. **Make the wire decision explicit.** Compare the candidate encodings from the [IPC Wire-Encoding Decision Preparation](ipc-wire-encoding-decision-prep-2026-07.md) against bounded decoding, the candidate-independent message-class policy proposal, schema evolution, deterministic diagnostics, generator/source provenance, license/advisory review, fuzzability, allocation/copying cost, and cross-language/platform maintenance. Record selected, rejected, or deferred status for every candidate and every exception to the message-class policy.
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

The checked no-claim [IPC wire-source manifest](../blueprint-v1/machine/ipc-wire-source-manifest.json) and [`validate_ipc_wire_sources.py`](../../tools/validate_ipc_wire_sources.py) keep the external format and platform-identity observations linked to this closure route. They do not replace the owner-reviewed wire decision, real transport experiment, hostile-wire tests, or readiness review.

Any future `PB-011` decision must also be reconciled through the [PB-020 owner-decision closure board](../project-buildout/23-owner-decision-closure-board.md) and [build-readiness closure preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md). IPC acceptance cannot independently authorize broad implementation, renderer or agent security, site isolation, release, or production claims.

## Next controlled action

Prepare an independent review record for `TASK-000011` on the exact commit. Do not start transport implementation or claim `TASK-000003` readiness until that review, the source/wire decision, and an immutable task approval record exist.
