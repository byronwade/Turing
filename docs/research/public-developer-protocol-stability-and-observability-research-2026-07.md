# Public Developer Protocol Stability and Observability Research - July 2026

Status: deferred `RQ-17` no-claim research packet
Owner: developer experience, protocol, security, accessibility, and release operations
Research date: 2026-07-19
Confidence: high for the documented protocol distinctions; low for any Turing protocol choice until an owner-approved scope, threat model, compatibility corpus, and implementation evidence exist

## Question

What public developer protocol can lead on stability and observability without creating an ambient-control, privacy, compatibility, or maintenance liability?

## Why This Matters

A browser-facing developer protocol is a product surface, not only a debugging socket. It can expose navigation, targets, DOM and accessibility state, network events, tracing, profiling, storage, emulation, and agent actions. Those capabilities have different authority, privacy, latency, and compatibility requirements. Combining them into one unrestricted endpoint would make the protocol difficult to secure, version, test, and support.

This packet is a research route for `RQ-17`. It does not select a protocol, promise CDP or WebDriver BiDi compatibility, authorize a remote-debugging server, or make a developer-experience or performance claim.

## Source-backed observations

### WebDriver BiDi is a standards-facing control protocol

The W3C WebDriver BiDi Working Draft dated 2026-06-01 defines bidirectional remote control of user agents. It describes commands, results, errors, events, modules, sessions, and WebSocket transport, and it explicitly allows commands to finish out of order. The draft is a work in progress, not a stable implementation contract. Turing must therefore record the exact specification revision and supported-module subset for any future compatibility statement.

Source: [W3C WebDriver BiDi](https://www.w3.org/TR/webdriver-bidi/), retrieved 2026-07-19.

### CDP is an implementation-oriented diagnostic surface

The ChromeDevTools `devtools-protocol` repository publishes protocol definitions and generated TypeScript mappings for Chrome DevTools Protocol. Chrome's Protocol Monitor documents that DevTools uses CDP to instrument, inspect, debug, and profile Chrome, and that requests and responses can be recorded, inspected, downloaded, and sent. This makes CDP a useful observation point for compatibility research, but it does not make CDP a neutral or stable cross-browser standard.

Sources: [ChromeDevTools devtools-protocol](https://github.com/ChromeDevTools/devtools-protocol), retrieved 2026-07-19; [Chrome Protocol Monitor](https://developer.chrome.com/docs/devtools/protocol-monitor), retrieved 2026-07-19.

### Protocol stability has more than one dimension

The source material distinguishes at least four compatibility surfaces:

- wire compatibility: framing, transport, IDs, ordering, errors, and cancellation;
- semantic compatibility: what a command or event means for targets, documents, frames, user contexts, and browser state;
- observability compatibility: whether traces, profiles, accessibility trees, network records, and diagnostics preserve identity and causality;
- lifecycle compatibility: session creation, reconnect, target replacement, browser restart, capability negotiation, and version skew.

Passing a schema or echo test proves only a narrow wire property. It does not establish that a tool receives equivalent state, safe authority, timing, redaction, or failure behavior.

## Candidate surface model

The future research comparison should keep separate lanes rather than force one protocol to own every use case:

1. Standards-facing automation: a bounded WebDriver BiDi-compatible subset where the supported module, revision, session lifetime, target model, and unsupported behavior are explicit.
2. Diagnostic and developer observability: a Turing-owned versioned protocol for traces, logs, layout/debug state, performance counters, accessibility inspection, and deterministic replay controls. Diagnostic reads must not silently grant mutation or user-data authority.
3. Local integration and agents: a capability-scoped API using the same browser identity, policy, confirmation, quota, timeout, cancellation, and audit machinery as interactive browsing. Page content, model output, and protocol payloads must not expand authority.
4. Private test seams: non-public fixtures and harness controls that are not shipped, not exposed on production channels, and not counted as public compatibility.

This is a candidate decomposition, not an architecture decision. A future decision must compare the cost of multiple surfaces against the security and support cost of a single combined surface.

## Evidence required before a protocol decision

The owner-approved research package should contain:

- an explicit user and tool inventory covering DevTools, WebDriver clients, test runners, profilers, accessibility tooling, automation, and agents;
- a command/event capability matrix with read, reversible mutation, consequential mutation, and forbidden operations separated;
- target, origin, site, profile, document-epoch, process, and session identity rules for every message;
- authentication, authorization, confirmation, redaction, secret handling, audit, rate, byte, time, and concurrency budgets;
- a version and support-window policy for wire, schema, semantic, and lifecycle compatibility;
- transport, framing, error, ordering, cancellation, reconnect, backpressure, and oversized-message tests;
- a conformance corpus with positive, negative, stale-identity, wrong-principal, timeout, cancellation, crash, restart, and version-skew cases;
- observability fixtures proving that traces and diagnostics preserve causal identity without retaining secrets or cross-origin data;
- accessibility and assistive-technology workflows for protocol-driven actions and inspection;
- independent review of the public threat model, privacy boundary, release channel, and support burden.

## Measurement plan

Protocol evaluation must report separate distributions rather than one "protocol performance" number:

- command admission, dispatch, and completion latency by operation class;
- event delivery latency, ordering violations, drops, duplicates, and backpressure;
- bytes copied, serialized, buffered, retained, and redacted;
- CPU, memory, wakeups, and battery impact while idle, tracing, profiling, and automation are enabled;
- browser startup and page-load impact with the protocol disabled and enabled;
- failure, timeout, cancellation, reconnect, and browser-crash denominators;
- accessibility-tree freshness and action-result correctness;
- security-policy decisions, rejected requests, and audit completeness.

Measurements require fixed workloads, exact browser and protocol revisions, profile state, network controls, platform facts, sample counts, raw artifacts, and an analysis plan. A lower latency or byte count from a weaker security or observability configuration is not an equivalent result.

## Rejection rules

Reject the packet as decision evidence when it:

- treats the CDP repository, a generated client, or a protocol schema as proof of semantic compatibility;
- presents a W3C Working Draft as a final standard or support commitment;
- exposes cookies, credentials, private profile state, cross-origin content, local files, or destructive actions without an explicit grant and audit path;
- uses a protocol connection to bypass interactive confirmation, origin/site identity, process boundaries, sandbox policy, or agent authority;
- omits out-of-order completion, cancellation, reconnect, stale document, browser restart, or target replacement behavior;
- counts private test seams as public compatibility;
- compares performance while disabling required diagnostics, accessibility, security, or failure accounting;
- relies on same-agent self-review or protocol-generated tests as independent verification;
- hides unsupported modules, version skew, dropped events, timeout cases, or redaction failures.

## Current status and next proof

`RQ-17` remains deferred outside the active pre-build crosswalk. The next proof is an owner-approved protocol inventory and threat-model packet, followed by a synthetic conformance corpus and independent wire/semantic/lifecycle review. No protocol, public API, compatibility promise, automation authority, accessibility result, performance result, or release claim follows from this packet.

## Claim boundary

This is source-backed research preparation only. It does not select WebDriver BiDi, CDP, a Turing protocol, a transport, a public API, a compatibility target, a DevTools implementation, an agent capability, a security posture, a performance result, or a production support window.
