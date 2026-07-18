# Schemas, Errors, Versioning, and Compatibility

Status: research and design baseline  
Owner: schema and compatibility governance  
Purpose: Keep interfaces evolvable, testable, and diagnosable over long support windows.

## Relationship to the Turing program

This document is the compatibility owner for Turing-specific protocols and artifact formats. Web IDL behavior remains governed by the Web IDL and web-platform standards.

## Canonical schemas

The schema repository is the source of truth for types, commands, events, constraints, limits, sensitivity, maturity, capability requirements, error codes, and documentation. Generators emit language bindings, validators, protocol docs, fixtures, redaction rules, and compatibility tests.

Hand-written transport objects are prohibited where generated types exist. Generated files identify source and regeneration command.

Current `PB-011` work has a review-pending M0 generator/reference in the [WP-002 kernel identity and IPC reference](../research/wp-002-kernel-ipc-2026-07.md) and [TASK-000011 WP-002 Review Handoff](../research/task-000011-wp002-review-handoff-2026-07.md), plus a checked no-claim [TASK-000011 evidence capture](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json), while the checked [IPC Capability Boundary Inventory](../research/ipc-capability-boundary-inventory-2026-07.md), checked no-claim [IPC schema-source template](../blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), and checked no-claim [IPC readiness-review template](../blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json) still record the broader `PB-011` owner-review boundary. The remaining proof includes accepted `TASK-000011` evidence beyond the non-accepting capture, wire encoding, timeout/cancellation, stale-epoch receiver behavior on a real transport, owner-reviewed IPC readiness, and transport-level negative tests. The templates have no approved generator source for production use, no owner-reviewed IPC readiness, and do not approve a schema source or transport encoding.

## Type design

Use explicit records, enums with unknown-value handling, tagged unions, opaque identifiers, timestamps with clock domain, units in field names or types, bounded strings/bytes, and optional fields only when absence has defined meaning. Avoid “any”, untyped dictionaries, generic method names, and sentinel magic values.

Identifiers are not user-visible labels. User text remains separate, localized, and Unicode-safe.

## Error taxonomy

Errors distinguish invalid request, malformed encoding, unauthenticated, unauthorized, stale target, unsupported capability, policy denial, confirmation required, conflict, resource limit, timeout, cancellation, partial effect, target crash, transport loss, internal defect, and unavailable dependency. Stable codes are machine-actionable; messages are diagnostic and may evolve.

Error details are bounded and redacted. Stack traces or internal paths are not sent to untrusted clients by default.

## Compatibility rules

Additive optional fields and new enum values are preferred. Receivers ignore unknown optional fields while preserving required validation. Removing fields, changing units or semantics, narrowing ranges, changing defaults, or reordering effects is breaking.

Major versions identify breaking sets. Minor versions identify additive behavior. Capability negotiation covers optional domains and experimental flags. The exact scheme may vary by artifact, but every family documents it.

## Deprecation and sunset

Deprecations include rationale, replacement, first-warning version, support window, telemetry/privacy plan if used, migration examples, and removal version. Stable protocol behavior is not removed solely because the internal implementation changed. Experimental behavior can change faster but remains namespaced and capability-gated.

A small project should prefer fewer durable APIs over unsustainable promises.

## Compatibility testing

Golden fixtures exercise old/new encoders and decoders, unknown fields/enums, missing optional values, boundary values, malformed input, capability negotiation, migration, and downgrade behavior. Generated clients are built against supported server versions. Trace/schema readers remain safe against newer untrusted artifacts.

Compatibility dashboards list supported combinations and failures.

## Data and profile schemas

Persistent profile, cache, trace, benchmark, protocol, and audit schemas include format version, writer identity, integrity where needed, migration path, rollback policy, and unknown-field behavior. Untrusted persistent data is validated on every read; a previous Turing build is not automatically trusted.

## Non-negotiable invariants

- One canonical schema generates types, docs, validation, and compatibility fixtures.
- Unknown optional data is handled deliberately; unknown required semantics fail safely.
- Error codes are stable and separate policy, transport, target, and internal failures.
- Breaking changes require a major version or equivalent explicit boundary.
- Deprecation has an owner, replacement, support window, and migration guidance.
- Persistent artifacts are validated even when produced by an older Turing version.

## Required evidence

- Cross-version encoder/decoder and generated-client matrix.
- Malformed, boundary, unknown-field, downgrade, and migration fuzzing.
- Error-code coverage and developer usability studies.
- Schema diff tooling that classifies breaking changes.
- Support-window cost and version-adoption tracking.
- Profile/trace corruption and rollback fault tests.

## Known risks and unresolved questions

- Versioning promises can exceed project maintenance capacity.
- Loose schemas move validation bugs into privileged handlers.
- Overly strict readers can make additive evolution impossible.
- Error details can leak sensitive or exploit-relevant internals.

## Primary sources

- Web IDL — https://webidl.spec.whatwg.org/
- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- Model Context Protocol specification — https://modelcontextprotocol.io/specification/2025-11-25

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
