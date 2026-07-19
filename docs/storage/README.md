# Storage and Recovery Engineering Book

Status: detailed research and design baseline  
Owner: storage, profile data, migration, and recovery engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/07-network-storage-media.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Persistent data is an untrusted, versioned, partitioned system. Every store needs an explicit key, owner, quota, transaction model, durability level, migration path, corruption behavior, deletion contract, and recovery tool.

## Reading order

1. [Storage Keys, Buckets, and Partitioning](01-storage-keys-buckets-and-partitioning.md)
2. [Quota, Eviction, and Pressure](02-quota-eviction-and-pressure.md)
3. [IndexedDB Transactions and Durability](03-indexeddb-transactions-and-durability.md)
4. [Cache Storage, Service Workers, and Background Work](04-cache-storage-service-workers-and-background-work.md)
5. [Cookies, Sessions, and Private Data](05-cookies-sessions-and-private-data.md)
6. [Profile Stores, History, Bookmarks, Settings, and Journals](06-profile-history-bookmarks-settings-and-journals.md)
7. [Migrations, Corruption, Disk Full, and Power Loss](07-migrations-corruption-disk-full-and-power-loss.md)
8. [Encryption Boundaries, Credentials, Clearing, and Export](08-encryption-credentials-clearing-and-export.md)
9. [Storage Observability, Repair, and Testing](09-observability-repair-and-testing.md)

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

- https://storage.spec.whatwg.org/
- https://w3c.github.io/IndexedDB/
- https://w3c.github.io/ServiceWorker/
- https://sqlite.org/
- https://w3c.github.io/webappsec-clear-site-data/

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
## Time Machine and continuity research

`OP-002`, `OP-010`, and `OP-014` add journal, snapshot, encryption, conflict, retention, deletion, and recovery questions. No snapshot or sync design may retain private or credential state by accident or replay consequential effects.

The checked [Profile Session Format Inventory](../research/profile-session-format-inventory-2026-07.md), [Profile and Session Data-Lifecycle Decision Preparation](../research/profile-session-data-lifecycle-decision-prep-2026-07.md), and [Profile/Session Execution and Data-Safety Closure Preparation](../research/profile-session-execution-and-data-safety-closure-preparation-2026-07.md), [`profile-session-format-inventory.json`](machine/profile-session-format-inventory.json), checked no-claim [`schema-package template`](machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json), and [`validate_profile_session_formats.py`](../../tools/validate_profile_session_formats.py) provide no-claim `PB-016` planning and execution-handoff evidence for state classes, profile, Space, session, snapshot, migration, privacy, durability, safe failure, synthetic fixtures, fault coverage, recovery accounting, and owner review. They do not implement a profile format, define executable schemas beyond the template, approve real-profile migration, approve sync or credential storage, prove data-loss safety, or make user-data handling production-ready.

The no-claim [Profile and Session Data-Safety Packet Examples](../research/profile-session-data-safety-packet-examples-2026-07.md) demonstrates the field relationships for a future synthetic migration packet. It contains fictitious values only and does not prove schema, migration, privacy, credential, recovery, or data-loss behavior.

Any future profile/session readiness decision remains subject to the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and `PB-020` closure. Schemas, migration tests, privacy review, recovery evidence, and data-safety packets are lane evidence only; none independently grants broad implementation, real-profile, production-format, release-path, or Chrome-class authority.
