# API Design Principles

Status: research and design baseline  
Owner: API architecture  
Purpose: Establish consistent rules for internal and public interfaces.

## Relationship to the Turing program

This document applies to internal IPC, Turing Engine Protocol, agent actions, traces, schemas, and future extension surfaces. Web APIs remain owned by the relevant standards and Blueprint chapters.

## User and developer need

Every new API starts with a concrete user or developer problem, alternatives, expected callers, interoperability context, privacy/security impact, accessibility impact, and maintenance owner. Implementation convenience or exposure of an existing internal method is insufficient.

Web-facing features require standards interest, feature detection, tests, secure defaults, and a path to interoperability. Turing-only interfaces remain clearly namespaced outside ordinary page semantics.

## Explicit identity and context

Calls carry typed session, profile, site, origin, frame, process, document epoch, agent, extension, or developer principal identity when relevant. Context is issued or verified by trusted code rather than reconstructed from untrusted strings. Optional identity is not used where ambiguity changes authority.

Target objects use stable opaque handles with generation/epoch checks and documented invalidation.

## Least authority

An API exposes the smallest operation and data required. A caller that needs “save a download to this approved destination” does not receive arbitrary filesystem access. A debugging client that needs layout fragments does not receive generic kernel IPC. A model that needs credential fill receives an opaque action, not the secret.

Authentication proves who is connected; authorization separately proves what that identity may do now.

## Predictability and composability

Names, units, timestamps, identifiers, enums, pagination, filters, ordering, errors, and lifecycle conventions are consistent. APIs do not perform hidden navigation, network requests, permission prompts, provider fallback, retries, or durable mutation unless specified.

Read operations avoid side effects. Mutation operations describe preconditions, idempotency, expected effects, and conflict behavior.

## Bounded behavior

Every input collection, string, blob, nesting depth, recursion, page size, queue, stream, timeout, concurrency, memory allocation, and output is bounded or negotiated. Over-limit behavior returns a defined error or partial result with continuation; it never silently allocates until OOM.

Server work is charged to a principal and can be rate- or budget-limited.

## Observability and failure

Operations expose accepted, queued, running, blocked, waiting-for-confirmation, completed, cancelled, timed-out, partially-completed, and failed states where applicable. Failure identifies stable reason, target identity, retryability, and redacted diagnostics. Unsupported behavior is distinct from temporary failure.

Metrics and traces use the same stable reason codes without leaking sensitive payload.

## Accessibility and internationalization

APIs that describe user-visible text, input, controls, accessibility, locale, time, numbers, fonts, or keyboard behavior preserve semantic and internationalized data rather than reducing everything to pixels or ASCII. Generated clients use Unicode-safe types and explicit units.

## Non-negotiable invariants

- No public API is a thin unreviewed wrapper around privileged internals.
- Identity, authority, lifetime, limits, and failure semantics are explicit.
- Read operations do not hide consequential side effects.
- Web-facing APIs require standards, interoperability, and test strategy.
- Unsupported behavior and experimental status are feature-detectable.
- Secrets are represented by operations or opaque handles whenever possible.

## Required evidence

- Problem statement, alternatives, threat model, privacy and accessibility review.
- Schema validation, property tests, malformed input, rate, and resource-exhaustion tests.
- Cross-language generated-client usability and type-safety review.
- Workflow studies and latency/allocation measurements.
- Compatibility and feature-detection tests.
- Documented owner, support window, deprecation, and incident path.

## Known risks and unresolved questions

- APIs can freeze accidental internal architecture.
- Too many Turing-specific surfaces can fragment the developer ecosystem.
- Implicit retries or effects can cause duplicate or unsafe actions.
- Generic APIs can become permanent privilege backdoors.

## Primary sources

- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- Web IDL — https://webidl.spec.whatwg.org/
- WHATWG working mode — https://whatwg.org/working-mode

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
