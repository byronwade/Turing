# Extensions, Enterprise Policy, Accounts, and Sync Engineering Book

Status: detailed research and design baseline  
Owner: extension, enterprise, account, and sync engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/02-capability-parity.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Ecosystem compatibility cannot recreate ambient authority, persistent background waste, or profile-wide data access. Extensions, enterprise controls, accounts, and sync are separate principals with explicit policy and resource contracts.

## Reading order

1. [Extension Processes, Worlds, and Isolation](01-extension-processes-worlds-and-isolation.md)
2. [Permissions, Host Grants, and User Control](02-permissions-host-grants-and-user-control.md)
3. [Event-Driven Background Work and Quotas](03-event-driven-background-work-and-quotas.md)
4. [Declarative Network Rules and Native Messaging](04-declarative-network-rules-and-native-messaging.md)
5. [Extension Updates, DevTools, and Agents](05-extension-updates-devtools-and-agents.md)
6. [Enterprise Policy Precedence and Audit](06-enterprise-policy-precedence-and-audit.md)
7. [Accounts, Sync, Encryption, Conflicts, and Quotas](07-accounts-sync-encryption-conflicts-and-quotas.md)

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

- https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions
- https://w3c.github.io/webextensions/specification/
- https://www.rfc-editor.org/rfc/rfc7516
- https://www.rfc-editor.org/rfc/rfc5869

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.
