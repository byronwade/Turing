# SDK Generation, Authentication, and Redaction

Status: research and design baseline  
Owner: SDK and API security  
Purpose: Produce usable clients without duplicating schemas or weakening browser authority.

## Relationship to the Turing program

This document applies to Turing Engine Protocol, agent tooling, benchmark and trace clients, and future embedders. Release supply-chain requirements are defined in the [security engineering book](../security-engine/README.md).

## Generated SDKs

Rust, TypeScript, and Python are initial client targets. Generation produces types, async operations, stream abstractions, errors, capability negotiation, documentation, examples, and test fixtures from the canonical schema. Clients expose transport and domain layers separately so applications can choose local IPC, loopback, test harness, or embedded channels.

Generated code is deterministic, formatted, linted, and tested. Handwritten convenience layers may compose operations but cannot bypass limits or authorization.

## Authentication

Local attachment can use OS user/session identity, inherited one-time handles, signed challenge tokens, or explicit browser-generated pairing. Loopback and remote transports require strong random credentials, origin/network restrictions, expiry, replay defense, and encrypted transport where needed. Credentials are stored and displayed according to platform security policy.

Authentication events are visible and revocable. Stable browser builds do not open unauthenticated debug listeners.

## Authorization

Sessions receive explicit capabilities by profile, target, domain, method, data class, action risk, duration, and count. Read, evaluate, mutate, download, file, credential, permission, security, update, extension, and agent operations are distinct. Capability narrowing cannot be expanded by the client.

Normal browsing, developer, automation, enterprise, and test sessions use separate launch and confirmation policies.

## Redaction and sensitive types

Schemas mark credentials, cookies, authorization, page text, URLs, local paths, source, screenshots, form values, identifiers, audit data, model prompts, provider responses, and enterprise fields by sensitivity. Server-side redaction occurs before serialization. Opaque handles replace secrets where an operation can be brokered.

Reveal operations require local authorization, limited scope, audit, and no automatic remote propagation.

## Client safety and ergonomics

SDKs make deadlines, cancellation, target epochs, pagination, streams, partial results, and capability checks visible. Defaults are conservative. Sensitive response types avoid casual debug printing. Examples use isolated profiles and never teach disabling security controls as routine setup.

Clients expose raw protocol access for advanced use only under an explicit low-level namespace with the same validation and authority.

## Compatibility and distribution

SDK releases identify supported protocol ranges, browser versions, generated schema commit, language/runtime requirements, license, integrity, and deprecation. Packages are reproducibly built, signed or provenance-attested, and tested against supported servers. Supply-chain dependencies are minimized.

A protocol release is incomplete until SDKs and compatibility tests are available.

## Audit and observability

Connections, authentication, capability grants, sensitive reveal, consequential methods, remote attachment, errors, and revocation emit bounded local audit events. Logs identify IDs and reason codes, not raw sensitive values.

## Non-negotiable invariants

- SDKs derive from canonical schemas and cannot introduce hidden methods.
- Authentication and authorization are distinct.
- Remote or loopback attachment is never anonymously enabled in stable builds.
- Sensitive data is redacted before serialization and represented by opaque operations where possible.
- Examples use isolated profiles and secure defaults.
- SDK and protocol compatibility ranges are tested and published.

## Required evidence

- Generated SDK builds, type tests, examples, and cross-version integration tests.
- Authentication replay, token theft, expiry, origin/network, and revocation tests.
- Authorization matrix and capability-narrowing property tests.
- Secret-scanning and sensitive-type serialization tests.
- Package reproducibility, provenance, dependency, and integrity evidence.
- Developer onboarding and error-recovery studies.

## Known risks and unresolved questions

- Convenience helpers can accidentally hide consequential behavior.
- Remote debugging credentials may be exposed by logs or command lines.
- Language runtimes differ in cancellation and integer/byte semantics.
- A compromised SDK package can become a high-value supply-chain attack.

## Primary sources

- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- Model Context Protocol architecture — https://modelcontextprotocol.io/docs/learn/architecture
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
