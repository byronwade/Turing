# Quality Assurance, Conformance, and Verification Engineering Book

Status: detailed research and design baseline  
Owner: quality, conformance, fuzzing, and assurance engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/12-testing-compatibility.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

A browser cannot be validated by demos or pixel tests alone. Every subsystem needs the lowest-level semantic oracle, cross-boundary integration tests, adversarial inputs, resource failure, recovery, and a full accounting of unsupported cases.

## Reading order

1. [Conformance Suites and Reduced Tests](01-conformance-suites-and-reduced-tests.md)
2. [Fuzzing, Property Tests, Model Tests, and Formal Methods](02-fuzzing-property-model-and-formal-methods.md)
3. [Differential Testing and Oracles](03-differential-testing-and-oracles.md)
4. [Fault Injection, Chaos, and Long-Duration Testing](04-fault-injection-chaos-and-long-duration.md)
5. [Security Assurance and Independent Review](05-security-assurance-and-independent-review.md)
6. [Flakes, Release Evidence, and Go/No-Go](06-flakes-release-evidence-and-go-no-go.md)

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

- https://web-platform-tests.org/
- https://github.com/tc39/test262
- https://rust-fuzz.github.io/book/
- https://llvm.org/docs/LibFuzzer.html
- https://aflplus.plus/

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.
