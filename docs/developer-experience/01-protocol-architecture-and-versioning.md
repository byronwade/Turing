# Developer Protocol Architecture and Versioning

Status: research and design baseline  
Owner: developer protocol architecture  
Purpose: Define interoperable automation and stable engine introspection without ambient privilege.

## Relationship to the Turing program

This document expands UI-GATE-6 and RQ-17. General API rules are defined in the [API design book](../api-design/README.md).

## Protocol layering

Layer A implements WebDriver BiDi for standards-facing automation and ecosystem portability. Layer B is a Turing-owned Engine Protocol for detailed browser and engine introspection. Adapters such as CDP compatibility translate externally and remain isolated from internal schemas and policy.

The two layers share target identities, session authentication, timestamps, cancellation, redaction, and generated transport primitives but retain separate compatibility promises.

## Target and session model

Targets include browser, profile, window, tab, browsing context, frame, worker, service worker, realm, process, extension, agent, and test fixture. Every target has stable session identity plus document/process epochs where state can become stale. Attachments are explicit leases with privilege class and revocation.

Commands cannot infer a normal signed-in profile when the client requested an automation target. A remote session cannot silently attach to arbitrary existing tabs.

## Schema ownership

A canonical schema defines domain, command, event, type, limits, sensitivity, authentication level, cancellation behavior, streaming behavior, maturity, and version history. Code generation produces Rust server types, Rust/TypeScript/Python clients, validators, docs, compatibility fixtures, and redaction metadata.

Generated code never grants authority by itself. Each server handler maps to explicit browser capabilities and trusted identity checks.

## Version negotiation

Connections negotiate protocol family, major/minor version, domains, commands, optional fields, encodings, limits, compression, and experimental flags. Stable clients use capability discovery rather than browser-version string guesses.

Major versions have published support windows. Additive fields are designed for forward compatibility; removed or semantically changed behavior requires migration notes, compatibility tests, and deprecation telemetry that does not expose page content.

## Transport and flow control

Local authenticated IPC is preferred for desktop attachment. Loopback or remote transport requires explicit launch configuration, authentication, origin/network binding, visible attachment state, encryption where appropriate, and rate limits.

Large snapshots, traces, heap data, screenshots, and network bodies use bounded streaming with backpressure, cancellation, checksums, partial failure, and explicit retention. One slow client cannot block renderer or browser critical paths.

## Errors and causality

Errors have stable codes, structured details, retryability, target/document identity, and redacted diagnostic references. Protocol failures are distinct from page exceptions, navigation failure, policy denial, stale target, unsupported capability, timeout, cancellation, and transport loss.

Events carry monotonic timestamps, wall-clock correlation where safe, causal parent or flow identifiers, sequence/epoch, and target identity. Ordering guarantees are documented per stream.

## Security boundary

Generic kernel evaluation, arbitrary IPC forwarding, filesystem access, cookie/credential dumps, and hidden permission bypasses are prohibited. Evaluation is realm-scoped, visibly powerful, and limited to developer/automation profiles according to policy. Sensitive headers, storage, source, and page data are redacted unless a local user-authorized workflow requires them.

Remote attachment is disabled by default and reflected in browser chrome.

## Non-negotiable invariants

- WebDriver BiDi and Turing-specific introspection remain distinct protocol layers.
- Schema-generated clients and servers do not bypass browser capability checks.
- Every stateful command validates target identity and current epoch.
- Large data uses bounded streaming, flow control, and cancellation.
- Remote attachment is authenticated, visible, scoped, and disabled by default.
- Breaking changes require version negotiation, tests, and migration guidance.

## Required evidence

- Protocol conformance suites, schema round trips, generated-client builds, and compatibility fixtures.
- Malformed message, unknown field, size, rate, cancellation, backpressure, and stale-target fuzzing.
- Latency and allocation measurements for common commands and event streams.
- Security tests for unauthorized profile, target, realm, file, credential, and kernel access.
- WebDriver BiDi WPT coverage and cross-browser automation fixtures.
- Support-window and deprecation drills across client versions.

## Known risks and unresolved questions

- Protocol breadth can become a permanent maintenance burden.
- A compatibility adapter can leak another engine's model into Turing if not isolated.
- Debugging features can become privilege escalation or data-exfiltration paths.
- Unbounded events or snapshots can destabilize the browser being debugged.

## Primary sources

- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/
- Firefox Remote Protocol — https://firefox-source-docs.mozilla.org/remote/index.html
- Web IDL — https://webidl.spec.whatwg.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
