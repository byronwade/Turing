# Profile/Session Execution and Data-Safety Closure Preparation - July 2026

Status: no-claim `PB-016` and `TASK-000007` execution/review preparation; no profile implementation, real-profile migration, sync, credential, or data-loss claim
Owner: storage, profile data, migration, recovery, privacy-data, product, security, quality, and release operations
Related gate: `PB-016` Profile, Space, session, and migration formats
Research date: 2026-07-19

## Purpose

The [Profile Session Format Inventory](profile-session-format-inventory-2026-07.md) and [Profile and Session Data-Lifecycle Decision Preparation](profile-session-data-lifecycle-decision-prep-2026-07.md) define the planning vocabulary. This report defines the evidence sequence that must replace those planning artifacts before profile/session work can be treated as executable or release-relevant. It is a closure route, not an implementation authorization.

The persistence portion of the evidence route must also preserve the SQLite [atomic-commit](https://sqlite.org/atomiccommit.html) and [corruption](https://sqlite.org/howtocorrupt.html) constraints plus Windows [buffered-I/O flush](https://learn.microsoft.com/en-us/windows/win32/fileio/flushing-system-buffered-i-o-data-to-disk) behavior when those technologies are evaluated. These sources constrain the experiment; they do not select SQLite, a journal mode, a flush policy, or a profile format.

## Required evidence sequence

1. Freeze versioned record contracts for profile, Space, session, snapshot, and migration records. Each contract must identify its owner, identity and epoch fields, schema window, integrity marker, authority boundary, privacy class, retention, export, deletion, and downgrade behavior.
2. Use only generated synthetic profiles, fake credentials, private-session markers, protected-work markers, corrupt journals, quota limits, and bounded temporary roots. A current user profile is not a fixture. A fixture policy must state creation, classification, retention, destruction, and review.
3. Implement a dependency-free parse, validate, write, read, and redacted-export harness for the proposed records. It must reject unknown authority, cross-profile references, missing epochs, malformed records, secret material, private-session persistence, and unsupported schema versions.
4. Exercise migration forward, resume, rollback, downgrade rejection, unknown fields, interrupted steps, quarantined records, and idempotent restart. A version number or a successful write is not migration or durability evidence.
5. Inject disk-full, power-loss, partial-write, corruption, crash, lock contention, quota, and unavailable-vault failures at each journal and checkpoint boundary. Retain the complete denominator, failure classification, prior-checkpoint readability, recovery result, and cleanup result.
6. Verify privacy and scope behavior for profile deletion, Space deletion, session close, private-session close/crash, origin-partitioned clearing, export, diagnostics, credential-vault unavailability, and protected work. Prove that Clear-Site-Data-like origin clearing is not profile deletion and that credentials are not ordinary session state.
7. Review data-loss and recovery outcomes by record class. Separate reloadable state, protected work, credentials, private-session state, snapshots, caches, and origin storage; record what is lost, restored, quarantined, or intentionally excluded.
8. Obtain named storage, privacy-data, security, product, quality, and release-operations review, plus an independent reviewer. The review must cite retained artifacts and may not promote a template, successful self-test, or role placeholder into readiness.

## Evidence matrix

| Axis | Required retained evidence | Reject when |
|---|---|---|
| Identity and version | Versioned schemas, profile/Space/session/document epochs, writer and reader bounds | IDs are substituted across boundaries or downgrade is silently accepted |
| Atomicity and durability | Journal transitions, checkpoint hashes, fault points, recovery result | Success-only writes or unclassified partial state are reported |
| Migration | Forward/resume/rollback/downgrade runs with synthetic fixtures | Real data is used, rollback is assumed, or unsupported input is rewritten |
| Privacy and partitioning | Redacted manifests, deletion scope, origin and private-session isolation | Secrets, private state, or raw page data enters records or diagnostics |
| Credentials | Vault boundary and locked/unavailable behavior | Missing vault is treated as an empty credential set |
| Recovery and protected work | Per-class loss/restoration/quarantine accounting and user-visible recovery result | Protected work is silently discarded or consequential actions replay automatically |
| Fixture safety and review | Fixture provenance, retention/destruction record, named independent review | A template, current profile, title-only approval, or self-review is used |

## Rejection and claim boundary

The evidence packet is rejected if it changes a no-claim template into a schema claim, uses a real profile or credential, hides a failed or excluded case, treats a migration as safe without fault injection, silently downgrades or deletes data, conflates origin clearing with profile deletion, or omits the failure denominator and cleanup result.

Until the sequence above is complete and owner-reviewed, `PB-016` remains `partial`, `TASK-000007` remains specified/proposed-only, and the repository must not claim a production profile format, profile implementation, real-profile migration, sync, credential storage, private-session readiness, protected-work readiness, user-data handling readiness, data-loss safety, release-path approval, compatibility, or implementation readiness.

## Handoff

This route is intentionally compatible with the checked [profile/session schema-package template](../storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json) and [readiness-review template](../storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json). Those templates define the shape of a future packet; they are not evidence for any item in the matrix. The next acceptable artifact is a synthetic-fixture execution packet with redacted logs, hashes, fault coverage, migration transitions, recovery accounting, and named owner review.

The [Profile and Session Data-Safety Packet Examples](profile-session-data-safety-packet-examples-2026-07.md) supplies a fictitious synthetic-migration packet covering state-class identity, journal lifecycle, fault injection, privacy/export, protected-work recovery, cleanup, and review rejection rules. It is a handoff example only and does not satisfy `PB-016` evidence.

## PB-020 closure dependency

Any future `PB-016` readiness decision must be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and the [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md) route. Executable schemas, migration tests, privacy review, recovery accounting, or a reviewed profile/session packet cannot independently close `PB-020`, authorize broad implementation, approve real-profile or production-format behavior, or support data-loss, credential, sync, compatibility, release, or Chrome-class claims. The final closure record must retain state-class limitations, fixture and privacy policy, failure denominators, named owner and independent reviewers, exceptions and expiry, and synchronized readiness, task, requirement, risk, support, and release records.

## Validation

```powershell
python -B tools/validate_profile_session_formats.py
python -B tools/validate_profile_session_readiness_review.py
python -B tools/validate_blueprint.py
.\tools\check.ps1
```
