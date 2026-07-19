# Package and Update Lab Packet Examples - July 2026

Status: no-claim sample packet shape for `PB-017` and `TASK-000009`; no updater, signing, stable-channel, rollback, migration, supported-security, or release claim
Owner: release operations, security, build, storage, quality, privacy, support, and independent review
Research date: 2026-07-19

## Purpose

The [Package/Update Execution and Release-Safety Closure Preparation](package-update-execution-and-release-safety-closure-preparation-2026-07.md) defines the evidence order, and the [Package, Update Trust, and Recovery Decision Preparation](package-update-trust-and-recovery-decision-prep-2026-07.md) separates source, build, artifact, provenance, signature, metadata, installation, migration, and support trust states. This page gives a sample-only fake-key, local-metadata lab packet so a future run records those states, faults, recovery, privacy, and cleanup without touching production trust.

All values are fictitious placeholders. They do not describe a real package, key, updater, release channel, installation, rollback, migration, or security result.

## Packet identity

```yaml
packet_status: sample_only_no_claim
packet_id: UPDATE-SAMPLE-LOCAL-0001
task_id: TASK-000009
source_commit: SAMPLE-COMMIT-REPLACE-BEFORE-USE
build_id: SAMPLE-BUILD-ID
toolchain: SAMPLE-TOOLCHAIN-MANIFEST
target: windows-x64
architecture: x86_64
feature_set: research-only-no-stable-support
artifact_sha256: SAMPLE-ARTIFACT-HASH
artifact_size: SAMPLE-SIZE
sbom_id: SAMPLE-SBOM
provenance_id: SAMPLE-PROVENANCE
notices_id: SAMPLE-NOTICES
symbols_id: SAMPLE-SYMBOLS
channel: local-lab-only
minimum_secure_version: SAMPLE-VERSION-POLICY
fake_key_set: SAMPLE-FAKE-KEY-SET
production_keys_used: false
offline_root_keys_used: false
real_user_profile_used: false
public_distribution: false
```

## Trust-state records

Each state is recorded independently. A valid signature cannot substitute for freshness, provenance, target binding, installation recovery, migration safety, or support policy.

| State | Required sample record | Sample status |
|---|---|---|
| Source identity | revision, tree status, dependency/vendor inputs, source digest | `sample_not_run` |
| Build identity | toolchain, target, features, builder, build definition | `sample_not_run` |
| Artifact identity | digest, size, contents, symbols, SBOM, notices | `sample_not_run` |
| Provenance | builder, inputs, process, predicate/version, digest binding | `sample_not_run` |
| Fake signature | key ID, role, threshold, verification result, no production-key assertion | `sample_not_run` |
| Update metadata | channel, platform, architecture, target, expiry, rollout, minimum secure version | `sample_not_run` |
| Installation transaction | staging root, activation marker, previous known-good, cleanup | `sample_not_run` |
| Profile transition | synthetic schema versions, migration, downgrade, rollback, recovery | `sample_not_run` |
| Support decision | explicitly no stable/support claim and owner disposition | `sample_not_run` |

## Local metadata and verification record

```yaml
metadata:
  root_role: SAMPLE-FAKE-ROOT
  targets_role: SAMPLE-FAKE-TARGETS
  snapshot_role: SAMPLE-FAKE-SNAPSHOT
  timestamp_role: SAMPLE-FAKE-TIMESTAMP
  key_threshold: SAMPLE-THRESHOLD
  metadata_version: SAMPLE-VERSION
  expires_at: SAMPLE-TIMESTAMP
  target_digest: SAMPLE-ARTIFACT-HASH
  target_size: SAMPLE-SIZE
  channel: local-lab-only
  platform: windows-x64
  architecture: x86_64
  rollout_cohort: fake-cohort-only
  minimum_secure_version: SAMPLE-VERSION-POLICY
verification:
  status: sample_not_run
  expected_failures: [expired, replay, wrong-target, wrong-platform, wrong-channel, under-signed, wrong-key, tampered]
  production_key_access: prohibited
  local_metadata_root: runner-owned-temporary-root
```

The lab may compare TUF-like role separation or another selected candidate, but the sample does not select TUF, a key hierarchy, a package format, or a production trust model.

## Installation and recovery matrix

| Case | Required evidence | Valid result classes | Sample status |
|---|---|---|---|
| Valid staged install | metadata verification, target identity, staging hash, atomic activation, restart | activated, held, failed | `sample_not_run` |
| Tamper/digest mismatch | altered payload, verification result, quarantine, cleanup | rejected/quarantined | `sample_not_run` |
| Expired/replayed metadata | metadata version/expiry, policy result, event record | rejected/blocked | `sample_not_run` |
| Wrong target/channel/platform | requested and actual identities, refusal point | rejected/blocked | `sample_not_run` |
| Partial write/interrupted download | fault point, previous active state, recovery | preserved/rolled-back/failed | `sample_not_run` |
| Disk full/power loss | boundary, journal, restart, known-good path | recovered/held/failed | `sample_not_run` |
| Crash loop | activation count, health policy, hold/quarantine, user-visible result | held/rolled-back/failed | `sample_not_run` |
| Authorized rollback | vulnerable-version policy, fake-key target, profile compatibility | rolled-back/rejected | `sample_not_run` |
| Migration/downgrade | synthetic profile schema, journal, protected work, export/quarantine | migrated/rolled-back/rejected/quarantined | `sample_not_run` |
| Cleanup | staged roots, fake keys, local metadata, fake profiles, retained hashes | complete/failed | `sample_not_run` |

Failed, unsupported, skipped, timeout, crash, and cleanup-error cases remain in the denominator. They are never removed to produce a successful update narrative.

## Privacy-preserving events

The event record may contain only an event ID, timestamp, operation class, target digest, reason code, result, and artifact references. It must exclude credentials, profile contents, private-session state, secrets, raw user paths, exploit details, and production key material. Every event package records retention, access, redaction, and destruction status.

## Rejection rules and review handoff

Reject the packet when it uses production or offline-root keys, a stable/beta channel, public distribution, a real updater service, a real profile, or real credentials; accepts an expired, replayed, wrong-target, under-signed, tampered, or vulnerable target; treats signature validity as complete trust; hides install or migration faults; or cites the template, self-test, or placeholder reviewer as readiness.

The next acceptable artifact is a reviewed immutable `TASK-000009` package for fake keys and local metadata. It must replace sample fields with executable manifest/parser, verification, staged-install, fault, rollback, migration, privacy, cleanup, hash, and named-review evidence before any production or supported-security decision.

## Claim boundary

This page is sample-only documentation. It does not establish a package format, updater, signing readiness, stable channel, public distribution, rollback safety, migration safety, supported security, release readiness, production updater, or implementation readiness.
