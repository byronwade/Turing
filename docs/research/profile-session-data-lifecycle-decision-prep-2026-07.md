# Profile and Session Data-Lifecycle Decision Preparation - July 2026

Status: no-claim `PB-016` lifecycle research; no profile format, migration, sync, credential, or real-user-data policy is approved
Owner: storage, profile data, migration, recovery, privacy-data, product, security, and release operations
Related gate: `PB-016` Profile, Space, session, and migration formats
Research date: 2026-07-20

## Question

How should Turing classify, persist, clear, migrate, recover, and report browser state without conflating origin storage with browser-owned profile state or treating a successful write as proof of durability and data-loss safety?

## Sources checked

- WHATWG [Storage Standard](https://storage.spec.whatwg.org/), including storage-key identity and storage buckets.
- W3C [Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB/), including transaction durability hints and commit failures.
- W3C [Clear-Site-Data](https://www.w3.org/TR/clear-site-data/), including origin-scoped clearing of caches, cookies, storage, and execution contexts.
- SQLite [Atomic Commit](https://sqlite.org/atomiccommit.html) and [How To Corrupt An SQLite Database File](https://sqlite.org/howtocorrupt.html), including journal, sync, locking, corruption, and durability limits.
- Microsoft [Flushing System-Buffered I/O Data to Disk](https://learn.microsoft.com/en-us/windows/win32/fileio/flushing-system-buffered-i-o-data-to-disk), including buffered-write, flush, write-through, and performance behavior on Windows.
- Turing [Profile Session Format Inventory](profile-session-format-inventory-2026-07.md), [Storage and Recovery book](../storage/README.md), [Blueprint 07](../blueprint-v1/07-network-storage-media.md), and [Product Experience book](../product-experience/README.md).

The checked no-claim [profile/session source manifest](../storage/machine/profile-session-source-manifest.json), [manifest schema](../storage/machine/profile-session-source-manifest.schema.json), and [`validate_profile_session_sources.py`](../../tools/validate_profile_session_sources.py) preserve these web-platform observations across nine evidence axes. They are source identity and decision-input records only; they do not define Turing's profile format, migration journal, credential vault, sync protocol, real-profile policy, or data-loss readiness.

The web specifications define web-visible semantics. They do not define Turing's browser profile format, migration journal, credential vault, sync protocol, or user-data recovery policy.

## State classes that must not be merged

| State class | Identity and owner | Durability expectation | Clear/migrate rule | Failure boundary |
|---|---|---|---|---|
| Browser-owned profile metadata | profile ID, installation/channel, settings, permission policy, recovery journal; browser kernel/storage owner | strict for committed settings and migration journals | explicit user/admin operation; versioned migration with rollback | never silently discard accepted settings or protected work |
| Space/workspace state | profile + Space ID; product/state owner | strict for layout, membership, and protected-work references | export/delete/migrate with user-visible scope and confirmation | preserve or quarantine on corruption; no partial success |
| Session and tab recovery state | profile + Space + session ID + document/site identity and epoch | bounded checkpoint; freshness and loss window explicit | private sessions excluded; crash recovery is not normal close | stale or partial records cannot revive the wrong document or origin |
| Snapshot and diagnostic state | snapshot ID, source epoch, retention owner | policy-selected and discardable unless protected | redacted export; cache-like data may be evicted | never treat a snapshot as authoritative live state |
| Origin-partitioned web storage | storage key including origin and applicable partition identity | API-specific; durable transactions and relaxed cache behavior remain distinct | origin-scoped clearing must not delete browser-owned state | quota, abort, corruption, and unavailable storage are explicit outcomes |
| Credentials and secrets | profile/account/origin plus vault identity; security owner | vault-specific and opaque to ordinary profile/session records | separate revoke/clear/export policy; never copy into snapshots | missing/locked vault is not an empty credential set |
| Private-session state | private profile/session identity; privacy owner | ephemeral by default and excluded from normal persistence | close, crash, export, diagnostics, and migration must prove exclusion | remnants and in-memory retention remain a separate review axis |

The categories are deliberately separate even when they share a storage engine. A storage key or origin does not authorize access to browser-owned profile data, and a successful transaction does not establish power-loss durability for every state class.

The checked lifecycle matrix in [`profile-session-format-inventory.json`](../storage/machine/profile-session-format-inventory.json) now gives each browser-owned record class an explicit state vocabulary and transition boundary. It is planning evidence only: transition strings describe the evidence a future harness must produce, not behavior already implemented. In particular, `recovering`, `restoring`, and `running` transitions must reject stale identity, corrupt input, privacy violations, unsupported versions, and incomplete journal state rather than silently falling back to a successful-looking record.

## Research findings that affect the format contract

- The Storage Standard's storage-key model requires Turing to preserve origin and partition identity at the web-storage boundary. Browser profile, Space, and session IDs are additional browser-owned identities and must not be substituted for a web storage key.
- IndexedDB 3.0 distinguishes durability hints. `strict` can require stronger persistence before completion at a cost in latency and power, while `relaxed` is appropriate for ephemeral data such as caches. Turing must assign durability classes per record family and test the actual crash/power-loss behavior rather than infer it from a successful commit event.
- SQLite's atomic-commit and corruption guidance makes the persistence assumptions visible: journal/WAL mode, locking, sync behavior, filesystem and hardware ordering, concurrent access, and direct-file interference all affect what can be recovered. On Windows, ordinary writes are buffered and explicit flush/write-through policy affects both persistence and latency. Turing must treat backend and platform behavior as an experiment boundary, not as an automatic guarantee from choosing SQLite or calling a write API.
- Clear-Site-Data describes origin-scoped clearing of cookies, cache, DOM-accessible storage, and execution contexts. Turing must make clear-site-data behavior distinct from user profile deletion, private-session close, browser cache pressure, and credential revocation, including ordering and partial-failure reporting.
- Migration must be journaled and resumable. A version number alone cannot prove that a partially written profile, snapshot, or migration was either committed or safely rolled back.
- Export is a data-class policy, not a raw directory copy. It must identify included/excluded classes, redact secrets, exclude private-session state unless explicitly authorized, preserve integrity markers, and record unsupported or quarantined records.
- Recovery must distinguish user-visible protected work from recomputable state. Tab placement, unsaved form state, downloads/uploads, pending agent actions, credentials, and caches have different loss and replay risks.

## Required decision gates

Before `PB-016` can move beyond partial, the decision package must contain:

1. Executable versioned records for profile, Space, session, snapshot, and migration with distinct identities and owners.
2. A state-class matrix assigning durability, retention, encryption, export, deletion, quota, and recovery behavior.
3. A journal/commit protocol with crash, interruption, partial-write, rollback, resume, quarantine, and repair states.
4. A real-profile fixture policy that prohibits production user data until privacy and security owners approve scope, redaction, retention, and destruction.
5. Tests for malformed input, downgrade, corruption, disk full, power loss, quota pressure, private-session close/crash, protected-work recovery, deletion, export, and data-loss accounting.
6. Cross-boundary checks preserving profile, Space, origin, site, document, process, capability, and epoch identity after asynchronous delay or restart.
7. Redacted diagnostics and export manifests that prove credentials, private-session state, raw page content, and secrets are excluded by default.
8. Compatibility linkage to `PB-017` package/update rollback and `PB-018` incident response before a schema is used by a release path.
9. Owner-reviewed privacy, storage, product, security, quality, and release-operations readiness beyond the checked no-claim template.

## Recommended no-claim experiment

Use only generated fake profiles with fake credentials, private-session fixtures, protected-work markers, corrupt journals, quota limits, and bounded temporary roots. Exercise:

- normal checkpoint and restart;
- interrupted migration before and after journal commit;
- disk-full and power-loss simulation at each write phase;
- private-session close and crash recovery;
- export, deletion, and Clear-Site-Data-like origin clearing;
- credential-vault unavailable/locked behavior;
- stale document/process epoch replay;
- quarantine and repair of unknown or corrupt records.

Retain schema versions, journal transitions, hashes, redacted manifests, failure denominators, cleanup results, and data-class inclusion/exclusion records. This experiment is not evidence that real user data is safe.

## Current conclusion

`PB-016` remains `partial`. This report makes state-class, durability, clearing, migration, export, privacy, and recovery distinctions explicit, but it does not define executable schemas or approve real-profile data, sync, credentials, migration, data-loss safety, or production profile behavior.

## Required registry impact

This report strengthens the documented research evidence for `PB-016` and `TASK-000007`. It does not change readiness status or support production profile, migration, sync, credential, privacy, compatibility, or implementation claims.
