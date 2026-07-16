# Turing API Design Book

Status: detailed research and design baseline  
Owner: API and protocol architecture  
Canonical owners: [Blueprint 11](../blueprint-v1/11-product-ui-devtools.md) and [Blueprint 10](../blueprint-v1/10-ai-agent-platform.md)

This book defines principles for public developer protocols, internal service interfaces, generated SDKs, browser actions, traces, and future extension surfaces. It is not a promise that every proposed API will ship. Web-facing APIs remain governed by standards and interoperability; Turing-specific APIs must justify their existence and remain outside page semantics unless standardized.

## Reading order

1. [Design principles](01-design-principles.md)
2. [Asynchrony, streaming, and cancellation](02-async-streaming-and-cancellation.md)
3. [Schemas, errors, versioning, and compatibility](03-schemas-errors-versioning-and-compatibility.md)
4. [SDK generation, authentication, and redaction](04-sdk-generation-authentication-and-redaction.md)

## API thesis

The best API is difficult to misuse, explicit about identity and authority, bounded under hostile input, observable when it fails, cancellable when it waits, evolvable without guesswork, and consistent across languages. APIs should model domain concepts—not expose internal pointers or generic privileged calls.

Every interface declares its caller, callee, trust level, principal identities, input and output limits, ownership, lifetime, timeouts, cancellation, idempotency, partial failure, retryability, authentication, authorization, redaction, versioning, and compatibility policy.

## API families

- Internal typed IPC between process roles.
- WebDriver BiDi standards-facing automation.
- Turing Engine Protocol for introspection and diagnostics.
- Agent observation/action protocol.
- Trace and benchmark artifact schemas.
- Generated local SDKs and test clients.
- Extension and embedder surfaces only after separate threat and sustainability review.

## Leadership criteria

- Schema and docs are generated from one source of truth.
- Clients discover capabilities instead of parsing version strings.
- Long operations report progress, stream with backpressure, and cancel.
- Errors are stable, structured, actionable, and redacted.
- Authentication and authorization are separate and explicit.
- Stable and experimental surfaces have different support commitments.
- API changes include compatibility tests, migration notes, and sunset dates.
- Measured common workflows require less glue and produce better diagnostics than reference tools.

## Related material

- [Developer experience book](../developer-experience/README.md)
- [AI engineering book](../ai/README.md)
- [Security engineering book](../security-engine/README.md)
- [Web platform design principles](../research/browser-engine-landscape-2026-07.md)
