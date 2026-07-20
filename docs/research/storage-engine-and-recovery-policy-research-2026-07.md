# Storage Engine and Recovery Policy Research - July 2026

Status: active no-claim evidence route for `RQ-14`, `RQ-27`, `PB-016`, and `TASK-000007`; no backend, durability level, migration policy, or data-loss claim is accepted
Owner: storage, profile data, migration, recovery, security, privacy, performance, and quality engineering
Research date: 2026-07-20

## Question

Which storage-engine and process-model choices can support Turing profile, history, bookmarks, settings, session journals, quota metadata, and web-storage records while preserving bounded authority, crash recovery, migration, privacy partitioning, and measurable performance?

## Scope and boundary

This packet compares policy and evidence obligations for three candidate families:

1. SQLite-backed stores with rollback-journal or WAL modes.
2. Memory-mapped copy-on-write stores such as LMDB.
3. Append/log or store-specific designs with explicit record framing, indexing, checkpoints, compaction, and repair.

The candidates are not interchangeable. The comparison must be made per state class and workload, not by selecting one database for every browser store. Credentials, private-session data, sync, real-profile migration, and production profile formats remain outside the current proof boundary.

## Source observations

The following are source observations retrieved 2026-07-20. They define constraints and test obligations; they do not select a Turing backend.

- SQLite's [atomic-commit documentation](https://www.sqlite.org/atomiccommit.html) describes journal ordering, lock transitions, flush points, rollback after interruption, and the hardware/filesystem assumptions behind atomic-looking commits.
- SQLite's [locking documentation](https://www.sqlite.org/lockingv3.html) describes file-lock states and the single-writer constraint relevant to a multi-process browser profile.
- SQLite's [isolation documentation](https://www.sqlite.org/isolation.html) distinguishes rollback-mode reader/writer blocking from WAL snapshot behavior; a WAL setting is not itself a durability or performance guarantee.
- SQLite's [corruption guidance](https://www.sqlite.org/howtocorrupt.html) identifies broken locking, filesystem behavior, and concurrent access patterns that can corrupt a database; a successful local self-test cannot cover those failure modes.
- SQLite's [file-format documentation](https://www.sqlite.org/fileformat.html) describes WAL frames, commit markers, checkpoints, and format identity; a format version alone is not a migration or repair policy.
- The [LMDB transaction documentation](https://lmdb.readthedocs.io/en/latest/) describes one simultaneous writer, many readers, memory-map sizing, reader lifetime, copy-on-write behavior, and the distinction between atomicity/consistency/isolation and durability when synchronization is relaxed.
- RocksDB's upstream [transaction documentation](https://github.com/facebook/rocksdb/wiki/Transactions) and [write-ahead-log documentation](https://github.com/facebook/rocksdb/wiki/Write-Ahead-Log) describe a log-oriented family with explicit transaction, WAL, recovery, and compaction concerns. These observations do not establish that RocksDB is suitable for a browser profile or approve it as a dependency.

## Candidate comparison

| Candidate family | Strengths to test | Failure and security obligations | Questions that prevent a premature choice |
|---|---|---|---|
| SQLite rollback journal/WAL | Mature transaction semantics, query/index support, compact file identity, multi-record atomicity, inspectable recovery paths | Lock correctness, one-writer contention, WAL growth/checkpoint behavior, filesystem flush assumptions, corruption and extension surface, schema migration | Which state classes need relational queries? Which writes can tolerate writer serialization? What checkpoint and repair policy preserves protected work? |
| Memory-mapped copy-on-write | Read-heavy access, snapshot-like readers, page-level copy-on-write, consistent environment copies | Map-size growth, virtual-address pressure, long-lived readers, one-writer limits, remap invalidation, platform mapping behavior, crash/durability settings | Can bounded map growth and reader lifetime be enforced across browser processes? What is the recovery result when resize or remap is interrupted? |
| Append/log or store-specific | Sequential writes, explicit record history, selective replay, per-record ownership, tailored hot paths | Framing and checksum design, index rebuild, compaction atomicity, tombstone/privacy deletion, unbounded log growth, replay cost, corruption quarantine | Which log records are authoritative? How are checkpoints bounded? How are deletion, export, migration, and repair proven without replaying unsafe effects? |

## Required store-by-store decision matrix

The future decision packet must evaluate at least these state classes separately: profile metadata, Spaces, session journal, history, bookmarks, settings, cookies, Cache Storage metadata, IndexedDB metadata, service-worker state, quota metadata, snapshots, diagnostics, and migration records. For every class record:

- owner and authority boundary;
- identity, partition key, schema/version window, and integrity marker;
- read/write concurrency and process placement;
- transaction atomicity and durability level;
- quota, pressure, retention, clearing, export, and deletion behavior;
- migration, downgrade, repair, quarantine, and recovery behavior;
- private-session, credential, origin, and cross-profile exclusion;
- expected query/index pattern and bounded resource budget;
- observability and redaction rules;
- unsupported cases and exact promotion claim.

## Evidence contract

The future `TASK-000007` packet must use only generated synthetic profiles, fake credentials or credential handles, private-session markers, protected-work fixtures, bounded temporary roots, and corrupt or interrupted journal fixtures. It must retain source/build identity, backend version/configuration, process topology, filesystem and platform identity, fixture hashes, operation sequence, fault point, raw logs, checksums, recovery result, cleanup result, and complete success/failure denominator.

At minimum, the matrix must exercise:

1. concurrent readers and writers, lock contention, cancellation, and process restart;
2. transaction interruption at journal write, flush, commit marker, checkpoint, index update, and compaction boundaries;
3. disk full, short write, power loss, crash, corrupted header/frame/page, stale lock, quota, and unavailable key or vault cases;
4. migration forward, resume, rollback, downgrade rejection, unknown fields, duplicate records, replay, and idempotent restart;
5. profile, Space, origin, private-session, protected-work, credential, export, deletion, and diagnostic redaction boundaries;
6. repair and quarantine without silently discarding protected work or replaying consequential page or agent effects;
7. cold/warm startup, representative lookup/write, checkpoint, compaction, recovery, and bounded-pressure measurements with equivalent security and process topology.

## Decision rules

Reject a candidate when it requires real user data, hides failed fault points, treats a successful write as durable without a declared flush policy, silently accepts downgrade or corruption, relies on unbounded memory maps or logs, conflates origin clearing with profile deletion, stores secrets in ordinary records, or cannot account for protected-work loss and restoration.

Do not aggregate backend results into a single score until workload, profile state, process topology, security settings, durability policy, hardware, OS, cache state, and failure denominator are equivalent. A faster lookup or smaller file does not establish lower browser memory, better recovery, stronger privacy, or Chrome-class performance.

## Next proof

Prepare an owner-approved `TASK-000007` extension that names the first synthetic state classes and candidate backends, pins the dependency and configuration boundary, defines the record and fault artifact schema, and binds the run to the profile/session readiness-review template. Execute self-tests and parser/reference-path tests first. Keep `PB-016` partial until executable schemas, migration/fault/recovery accounting, privacy review, and owner-reviewed readiness beyond the checked no-claim template exist.

## Explicit non-claims

- No storage engine, journal mode, map strategy, log format, or process model is selected.
- No SQLite, LMDB, RocksDB, or custom log dependency is approved for Turing release code.
- No durability, corruption resistance, migration safety, data-loss safety, privacy, credential, sync, profile-format, performance, or Chrome-class claim follows from this packet.
- The packet does not authorize real-profile access, production data, broad implementation, or release behavior.
