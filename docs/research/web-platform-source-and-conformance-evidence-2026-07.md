# Web-Platform Source and Conformance Evidence - July 2026

Status: checked no-claim source and evidence route
Owner: web-platform, architecture, conformance, and documentation research
Primary gates: `PB-002`, `PB-020`
Active crosswalk questions: `RQ-44`, `RQ-46`, `RQ-47`, `RQ-15`, `RQ-16`, `RQ-25`, `RQ-31`

Deferred context question: `RQ-33` (supporting source context only; it remains outside the active pre-build crosswalk)

## Result

The repository now has one machine-checked source manifest for the web-platform standards, language specification, test suites, interoperability context, automation protocol, and governance principles that must inform future compatibility work. The [manifest](../web-platform/machine/web-platform-source-manifest.json), [schema](../web-platform/machine/web-platform-source-manifest.schema.json), and [validator](../../tools/validate_web_platform_sources.py) record the active PB-002 source-strategy questions separately from deferred `RQ-33` context. They are linked to the existing PB-002 source-strategy route; they do not create a new task or authorize implementation.

The current record identifies source families and the evidence consequences of using them. It does not pin a standards revision, execute WPT or Test262, establish a denominator, retain browser-run artifacts, compare implementations, or select a feature. The local compatibility corpus and ADR-0009 source-strategy records remain separate required evidence.

## Required evidence order

1. Pin each normative specification, suite commit, harness, environment, and local patch set.
2. Generate the dependency graph and complete denominator, including pass, fail, timeout, crash, harness-error, leak, excluded, and not-run outcomes.
3. Execute the selected WPT, Test262, protocol, and local compatibility cases with retained artifacts.
4. Run differential and multi-implementation comparisons, preserving known differences and unsupported rows.
5. Review security, privacy, accessibility, abuse, and resource-exhaustion consequences.
6. Record feature lifecycle, experiment, deprecation, compatibility-intervention, and owner-review decisions.

## Claim boundary

This report does not claim HTML, DOM, CSS, Fetch, ECMAScript, WPT, Test262, Interop, WebDriver BiDi, browser compatibility, standards conformance, Chrome-class behavior, security, accessibility, performance, or production readiness. `PB-002` remains blocked and `PB-020` remains partial.
