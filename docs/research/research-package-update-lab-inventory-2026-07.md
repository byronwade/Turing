# Research Package Update Lab Inventory - July 2026

Status: no-claim planning inventory and checked update-lab package template
Owner: release operations, security, storage, and documentation-research
Related gate: `PB-017` Research package identity and updater laboratory
Updated: 2026-07-18

## Question

Can `PB-017` move from release-operations prose into checked planning evidence and a checked no-claim lab-package template without implying that production signing, offline roots, a stable channel, a real updater, public binary distribution, real user profile migration, rollback safety, migration safety, release readiness, or supported security exists?

## Short Answer

Yes, for planning only. The new [`research-package-update-lab.json`](../release-operations/machine/research-package-update-lab.json) registry, [`research-package-update-lab-package.schema.json`](../release-operations/machine/research-package-update-lab-package.schema.json), checked no-claim [`no-claim-update-lab-template.json`](../release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json), and [`validate_research_package_update_lab.py`](../../tools/validate_research_package_update_lab.py) validator make the research-package and update-lab terms concrete enough to continue release and security work. They define required package identity fields, update metadata behaviors, rollback/migration boundaries, privacy-preserving event expectations, future fake-key local lab package handoff fields, and unsupported production boundaries.

This is not a package implementation, updater implementation, signing system, release channel, or migration safety claim.

## Inputs

- [Release Operations book](../release-operations/README.md)
- [Build Identity and Hermetic Toolchains](../release-operations/01-build-identity-and-hermetic-toolchains.md)
- [Reproducible Builds, Provenance, and SBOM](../release-operations/02-reproducible-builds-provenance-and-sbom.md)
- [Signing Keys and Package Attestation](../release-operations/03-signing-keys-and-package-attestation.md)
- [Update Metadata, Rollout, and Rollback](../release-operations/05-update-metadata-rollout-and-rollback.md)
- [Profile Migrations and Downgrade Protection](../release-operations/06-profile-migrations-and-downgrade-protection.md)
- [Update, Supply Chain, and Vulnerability Response](../security-engine/05-update-supply-chain-and-vulnerability-response.md)
- [Blueprint 13](../blueprint-v1/13-build-release-operations.md)
- [`research-package-update-lab.schema.json`](../release-operations/machine/research-package-update-lab.schema.json)
- [`research-package-update-lab.json`](../release-operations/machine/research-package-update-lab.json)
- [`research-package-update-lab-package.schema.json`](../release-operations/machine/research-package-update-lab-package.schema.json)
- [`no-claim-update-lab-template.json`](../release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json)
- [`validate_research_package_update_lab.py`](../../tools/validate_research_package_update_lab.py)

## Inventory Scope

The checked inventory covers package identity fields:

- source commit, build ID, channel, platform, architecture, toolchain, feature set, SBOM, provenance, symbols, notices, artifact hashes, artifact sizes, and no-stable-support label.

It also covers update and recovery behaviors:

- role separation, signature threshold, expiry, minimum secure version, rollout, mirrors, staged install, tamper, replay, wrong-target, partial-write, disk-full, power-loss, rollback, vulnerable version refusal, migration, downgrade, crash-loop, and privacy-preserving local events.

The checked no-claim update-lab package template adds the handoff shape for a future fake-key local package lab:

- manifest fields, metadata behavior axes, lifecycle stages, fixture policy, rejection rules, unsupported boundaries, and validation commands;
- false status booleans for executable package manifest, update metadata parser, signature threshold tests, staged install tests, rollback migration tests, production keys, and owner review.

## Decision

`PB-017` can move from `not_started` to `partial` because the inventory, checked update-lab package template, and validator now exist. The status must not move beyond `partial` until executable evidence beyond the checked no-claim update-lab package template exists: package manifests, metadata parsing, signature/threshold verification, tamper/replay/wrong-target/expiry/mirror/partial-write/disk-full/power-loss tests, authorized rollback tests, vulnerable-version refusal tests, migration/downgrade/crash-loop tests, privacy review, release-operations review, and owner approval.

## Unsupported Boundaries

The inventory explicitly keeps these outside the proof:

- no production signing keys;
- no offline root keys;
- no stable channel;
- no real updater;
- no public binary distribution;
- no real user profile migration;
- no rollback safety claim;
- no migration safety claim;
- no release readiness claim;
- no supported security claim;
- no production updater claim.

## Next Proof Required

To advance beyond partial planning evidence and beyond the checked no-claim update-lab package template, `PB-017` needs:

1. executable research-package manifest generation and validation beyond the template;
2. no-production-key signature and threshold verification fixtures beyond the template;
3. update metadata parser tests beyond the template for tamper, replay, wrong-target, expiry, mirror, size, hash, channel, platform, and architecture cases;
4. staged-install failure tests for partial-write, disk-full, power-loss, interrupted cleanup, and restart;
5. rollback tests proving only authorized known-good targets can restore and vulnerable versions are refused;
6. migration, downgrade, and crash-loop behavior tied to the `PB-016` profile/session format terms without using real user profiles;
7. privacy-preserving local event tests that redact profile contents, credentials, private-session data, and secrets;
8. release-operations, security, storage, and owner review.

## Affected Records

- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json)
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json)
- [`research-package-update-lab-package.schema.json`](../release-operations/machine/research-package-update-lab-package.schema.json)
- [`no-claim-update-lab-template.json`](../release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json)

## Validation

Run:

```bash
python3 -B tools/validate_research_package_update_lab.py
python3 -B tools/validate_blueprint.py
```

The aggregate Windows wrapper also runs the blueprint validator:

```powershell
.\tools\check.ps1
```
