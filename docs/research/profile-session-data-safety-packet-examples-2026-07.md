# Profile and Session Data-Safety Packet Examples - July 2026

Status: no-claim sample packet shape for `PB-016` and `TASK-000007`; no executable schema, migration, real-profile, credential, sync, or data-loss claim
Owner: storage, profile data, migration, recovery, privacy-data, product, security, quality, and release operations
Research date: 2026-07-19

## Purpose

The [Profile/Session Execution and Data-Safety Closure Preparation](profile-session-execution-and-data-safety-closure-preparation-2026-07.md) defines the required evidence sequence, and the [Profile and Session Data-Lifecycle Decision Preparation](profile-session-data-lifecycle-decision-prep-2026-07.md) defines the state-class and durability distinctions. This page supplies a sample-only packet for a synthetic profile migration so future work records identity, privacy, fault injection, recovery, and cleanup together.

All values are fictitious placeholders. They do not describe a real profile format, migration result, credential vault, sync behavior, or data-loss outcome.

## Packet identity and fixture policy

```yaml
packet_status: sample_only_no_claim
packet_id: PROFILE-SAMPLE-MIGRATION-0001
task_id: TASK-000007
source_commit: SAMPLE-COMMIT-REPLACE-BEFORE-USE
fixture_kind: generated_synthetic_profile
fixture_root: runner-owned-temporary-root
fixture_manifest_sha256: SAMPLE-FIXTURE-MANIFEST-HASH
real_user_profile: prohibited
real_credentials: prohibited
fake_credentials: required-and-disposable
private_session_fixture: included-and-excluded-from-normal-persistence
protected_work_fixture: fake-unsaved-work-marker
retention: bounded-until-review-complete
destruction_record: required
```

## State-class manifest

Every record must identify its owner, identity, privacy class, durability, retention, export, deletion, and recovery behavior. Sharing a storage engine does not merge these classes.

| State class | Sample identity | Durability | Export/deletion rule | Sample outcome |
|---|---|---|---|---|
| Profile metadata | `profile:SAMPLE-P1` | strict | explicit profile operation | `sample_not_run` |
| Space layout | `profile:SAMPLE-P1/space:SAMPLE-S1` | strict | Space-scoped export/delete | `sample_not_run` |
| Session recovery | `profile:SAMPLE-P1/session:SAMPLE-SE1/epoch:SAMPLE-E1` | bounded checkpoint | excludes private state | `sample_not_run` |
| Snapshot | `snapshot:SAMPLE-SN1/source_epoch:SAMPLE-E1` | policy-selected | redacted and non-authoritative | `sample_not_run` |
| Origin storage | `storage-key:SAMPLE-ORIGIN-PARTITION` | API-specific | origin-scoped clear | `sample_not_run` |
| Credential reference | `vault:SAMPLE-V1/origin:SAMPLE-O1` | vault-specific | separate revoke/export policy | `sample_not_run` |
| Private session | `private:SAMPLE-PS1` | ephemeral | excluded from normal persistence/export | `sample_not_run` |
| Protected work | `work:SAMPLE-W1` | explicit user-data policy | never silently discard | `sample_not_run` |

## Migration lifecycle record

```yaml
- stage: classify_source
  source_schema: SAMPLE-V1
  target_schema: SAMPLE-V2
  source_profile: profile:SAMPLE-P1
  source_epoch: SAMPLE-E1
  status: sample_not_run
- stage: validate_input
  checks: [identity, checksum, privacy_class, bounded_size, downgrade_policy]
  status: sample_not_run
- stage: plan_migration
  journal_id: SAMPLE-J1
  rollback_checkpoint: SAMPLE-CHECKPOINT-OLD
  protected_work_policy: preserve-or-quarantine
  status: sample_not_run
- stage: write_temporary_snapshot
  snapshot_id: SAMPLE-SN1
  snapshot_sha256: SAMPLE-SNAPSHOT-HASH
  redaction_manifest: SAMPLE-REDACTION-MANIFEST
  status: sample_not_run
- stage: commit_or_rollback
  commit_marker: SAMPLE-COMMIT-MARKER
  previous_checkpoint_readable: sample_not_run
  status: sample_not_run
- stage: repair_or_quarantine
  unsupported_or_corrupt_records: retained-and-classified
  status: sample_not_run
- stage: verify_privacy_and_cleanup
  private_state_excluded: sample_not_run
  fake_credentials_destroyed: sample_not_run
  temporary_root_removed: sample_not_run
  status: sample_not_run
```

## Fault and recovery matrix

Each fault is injected at a named journal or checkpoint boundary and remains in the denominator.

| Fault | Required record | Valid result classes | Sample status |
|---|---|---|---|
| Disk full | boundary, bytes available, prior checkpoint, cleanup | recovered, quarantined, failed, blocked | `sample_not_run` |
| Power loss/interruption | injection point, journal marker, restart state | resumed, rolled back, quarantined, failed | `sample_not_run` |
| Partial write/corruption | damaged record/hash, detection, preserved source | rejected, quarantined, repaired, failed | `sample_not_run` |
| Lock contention | owner, timeout, cancellation, retry | bounded retry, timeout, failed | `sample_not_run` |
| Unavailable vault | vault state, credential reference, user-visible result | explicit unavailable, no secret substitution | `sample_not_run` |
| Private-session crash | private identifiers, crash/restart, persistence scan | excluded, residual-found, failed | `sample_not_run` |
| Stale epoch replay | submitted and trusted epoch, decision | rejected, quarantined | `sample_not_run` |
| Protected-work failure | work class, loss/restoration/quarantine, user-visible notice | preserved, restored, quarantined, explicit loss | `sample_not_run` |

`success` is not a sufficient outcome without the boundary, failure classification, prior-checkpoint readability, recovery result, and cleanup result.

## Privacy and export checks

The packet must prove separately that:

- origin-partitioned clearing does not delete browser-owned profile or Space state;
- credential-vault unavailability is not represented as an empty credential set;
- private-session state does not enter normal profile, session, snapshot, diagnostic, or export records;
- exports identify included and excluded classes, redact secrets, preserve integrity markers, and classify quarantined data;
- real user paths, raw page content, account identifiers, and production credentials are absent from fixtures, logs, traces, and artifacts;
- deletion and cleanup records identify what was removed, what was retained under policy, and what remains unresolved.

## Rejection rules and review handoff

Reject the packet when it uses a real profile or credential, treats a version number or successful write as migration proof, silently accepts downgrade/corruption, discards protected work, conflates origin clearing with profile deletion, hides fault or cleanup failures, or cites the schema template, self-test, or placeholder reviewer as readiness.

The next acceptable artifact is a reviewed immutable `TASK-000007` package for synthetic fixtures and a declared schema scope. It must replace sample fields with executable schema, migration, fault, privacy, recovery, redaction, hash, cleanup, and named-review evidence before any real-profile or production-format decision.

## Claim boundary

This page is sample-only documentation. It does not establish a profile format, migration safety, sync, credential storage, private-session readiness, protected-work recovery, data-loss safety, user-data handling readiness, compatibility, production readiness, or implementation readiness.
