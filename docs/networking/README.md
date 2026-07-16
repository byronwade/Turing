# Networking Engineering Book

Status: detailed research and design baseline  
Owner: networking, Fetch, and transport engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/07-network-storage-media.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

The renderer never owns ambient socket authority. One brokered network service carries kernel-issued profile, site, origin, frame, destination, credential, partition, and document-epoch identity through every redirect and policy decision.

## Reading order

1. [Identity and Request Context](01-identities-and-request-context.md)
2. [Network Service and Capability Brokers](02-network-service-and-brokers.md)
3. [DNS, Proxies, and Connection Racing](03-dns-proxies-and-connection-racing.md)
4. [TLS, Certificates, and Client Authentication](04-tls-certificates-and-client-auth.md)
5. [HTTP/1.1, HTTP/2, HTTP/3, and QUIC](05-http1-http2-http3-and-quic.md)
6. [Fetch, Redirects, CORS, and Security Policy](06-fetch-redirects-cors-and-security-policy.md)
7. [Caching, Preload, Speculation, and Service Workers](07-cache-preload-speculation-and-service-workers.md)
8. [Cookies, Partitioning, and Tracking Resistance](08-cookies-partitioning-and-tracking-resistance.md)
9. [Streaming, WebSocket, WebTransport, and Downloads](09-streaming-websocket-webtransport-and-downloads.md)
10. [Networking Observability, Testing, and Resource Budgets](10-observability-testing-and-resource-budgets.md)

## Cross-cutting rules

- Security and correctness precede benchmark wins and implementation convenience.
- Every boundary preserves typed identity and denies ambient authority.
- Queues, caches, retries, tasks, messages, persistent records, and diagnostic output are bounded.
- A deterministic serial/reference path precedes concurrent, incremental, speculative, cached, hardware, or JIT optimization.
- Physical and semantic resource ownership remain observable.
- Failure, cancellation, crash, restart, migration, pressure, and recovery are part of the supported behavior.
- Accessibility, privacy, localization, developer tooling, and platform differences are designed with the subsystem.
- Research does not change accepted requirements or support status without the normal decision process.

## Leadership criteria

Leadership requires a public evidence package combining conformance, adversarial and fault testing, fixed-hardware latency and resource measurements, accessible workflows, recovery, maintenance cost, security review, and explicit failures. A smaller feature set, weaker isolation, hidden discarding, unmatched caches, omitted failures, or vendor marketing cannot establish leadership.

## Primary sources

- https://fetch.spec.whatwg.org/
- https://url.spec.whatwg.org/
- https://www.rfc-editor.org/rfc/rfc9110
- https://www.rfc-editor.org/rfc/rfc9113
- https://www.rfc-editor.org/rfc/rfc9114
- https://www.rfc-editor.org/rfc/rfc9000
- https://www.rfc-editor.org/rfc/rfc8446
- https://w3c.github.io/webtransport/

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.

<!-- MARKET-STRATEGY-2026-07 -->
## Identity routing and privacy receipts

`OP-006` and `OP-012` require kernel-owned routing context, clear proxy/DNS/certificate policy, destination attribution, and bounded receipt data. Pages cannot select trusted identity or falsify browser-owned receipts.
