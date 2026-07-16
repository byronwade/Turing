# Open Web Platform Governance Engineering Book

Status: detailed research and design baseline  
Owner: web-platform standards and interoperability  
Canonical overview: [Blueprint owner](../blueprint-v1/12-testing-compatibility.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Turing should not become a private web platform. New behavior starts with user or developer need, interoperable specification work, tests, abuse review, feature detection, and a credible multi-implementer path.

## Reading order

1. [User Needs and Design Principles](01-user-needs-and-design-principles.md)
2. [Feature Lifecycle and Standards Participation](02-feature-lifecycle-and-standards-participation.md)
3. [Tests, Interoperability, and Dependency Graphs](03-tests-interop-and-dependency-graphs.md)
4. [Privacy, Security, Accessibility, and Abuse Review](04-privacy-security-accessibility-and-abuse-review.md)
5. [Experiments, Deprecation, and Compatibility Interventions](05-experiments-deprecation-and-compatibility-interventions.md)
6. [Governance Evidence and Public Dashboard](06-governance-evidence-and-public-dashboard.md)

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

- https://whatwg.org/working-mode
- https://www.w3.org/TR/design-principles/
- https://www.w3.org/TR/ethical-web-principles/
- https://web-platform-tests.org/
- https://wpt.fyi/interop

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.
