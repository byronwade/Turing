# Package/Update Execution and Release-Safety Closure Preparation - July 2026

Status: no-claim `PB-017` and `TASK-000009` execution/review preparation; no package format, updater, signing key, stable channel, production release, or user-profile migration claim
Owner: release operations, security, build, storage, quality, privacy, support, and documentation-research
Related gate: `PB-017` Research package identity and updater lab
Research date: 2026-07-19

## Purpose

The [Research Package Update Lab Inventory](research-package-update-lab-inventory-2026-07.md) and [Package, Update Trust, and Recovery Decision Preparation](package-update-trust-and-recovery-decision-prep-2026-07.md) define the trust vocabulary and decision questions. This report defines the evidence packet that must exist before package/update work is treated as executable or release-relevant.

## Source-boundary carry-forward

The source-backed decision preparation reviewed on 2026-07-19 remains the canonical interpretation route:

| Source role | Canonical source | What it can inform | What it cannot decide by itself |
|---|---|---|---|
| Update metadata trust | [TUF metadata](https://theupdateframework.io/docs/metadata/) and [TUF security properties](https://theupdateframework.io/docs/security/) | Role separation, thresholds, freshness, target binding, expiry, rollback and freeze attack classes | Turing's package layout, profile migration, UI, supported channel, or production policy |
| Build provenance | [SLSA](https://slsa.dev/) and [in-toto](https://in-toto.io/docs/getting-started/) | Source/build-step/materials provenance and authorized functionaries | Update authorization, platform installation, key recovery, or user-data migration safety |
| Signing and transparency | [Sigstore signing](https://docs.sigstore.dev/cosign/signing/overview/), [Sigstore bundles](https://docs.sigstore.dev/about/bundle/), and [Microsoft Windows signing/verification](https://learn.microsoft.com/en-us/windows/win32/seccrypto/using-signtool-to-verify-a-file-signature) | Identity-bound signing, transparency evidence, Windows verification policy, signer inspection, and platform-specific result handling | Offline-root suitability, privacy policy, emergency recovery, channel policy, package-format choice, or supported-security scope |

The checked no-claim [package/update source manifest](../release-operations/machine/package-update-source-manifest.json), [manifest schema](../release-operations/machine/package-update-source-manifest.schema.json), and [`validate_package_update_sources.py`](../../tools/validate_package_update_sources.py) preserve these official observations across eight evidence axes. They are source identity and decision-input records only; they do not select TUF, SLSA, in-toto, Sigstore, a Windows package format, a signing hierarchy, an updater, a channel, or a release policy.

The future fake-key lab must record which source role each assertion uses and keep metadata authorization, provenance, artifact signature, installation transaction, profile transition, and support decision as separate states. No source framework is selected by this route.

## Required evidence sequence

1. Freeze the research package identity contract: source revision, build ID, toolchain, target, features, artifact digest/size, SBOM, notices, provenance, symbols, platform, architecture, channel, and minimum secure version.
2. Use fake keys, local metadata, synthetic packages, bounded temporary roots, and disposable channels. Production signing keys, offline roots, stable distribution, real updater services, and real user profiles are prohibited.
3. Implement a dependency-reviewed parse/validate/verify harness for package manifests and update metadata. It must reject unknown targets, expired metadata, wrong channel/platform/architecture, digest or size mismatch, invalid thresholds, replay, and unsupported rollback.
4. Exercise staged installation, atomic activation, restart, crash-loop handling, disk-full, power-loss, partial-write, interrupted download, mirror disagreement, quarantine, cleanup, and recovery to a known-good path.
5. Exercise profile-transition boundaries with synthetic schemas only: migration, downgrade refusal, rollback compatibility, export, repair, and unavailable profile state. Package verification must not imply migration safety.
6. Record privacy-preserving local events for accepted, rejected, expired, mismatched, retried, quarantined, rolled-back, and recovered operations. Logs must exclude secrets, credentials, profile contents, private-session data, and production signing material.
7. Review the packet with named release-operations, security, quality, privacy, storage, support, and independent reviewers. The review must cite retained artifacts, hashes, failure denominators, cleanup results, and residual limitations.

## Evidence matrix

| Axis | Required evidence | Reject when |
|---|---|---|
| Identity and provenance | Versioned manifest, source/build/artifact identity, provenance, SBOM, notices | A digest, signature, or provenance record is treated as the whole trust decision |
| Metadata authorization | Role/threshold, freshness, target binding, channel, platform, architecture, minimum secure version | Expired, replayed, wrong-target, or mirror metadata is accepted |
| Installation transaction | Staging, atomic activation, restart, cleanup, quarantine, known-good recovery | Partial writes or crash loops are hidden or counted as success |
| Rollback and migration | Authorized rollback, vulnerable-version refusal, synthetic profile migration/downgrade tests | Rollback is assumed from version numbers or real profiles are used |
| Privacy and telemetry | Redaction manifest, event classification, retention, access review | Credentials, profile data, private-session state, or key material enters logs |
| Fixture and key safety | Fake-key/local-only fixture provenance, destruction record, no production-key access | A production key, stable channel, real updater, or real user profile is used |
| Owner review | Named owner and independent review with retained evidence | A template, self-test, or title-only approval is cited as readiness |

## Rejection and claim boundary

Reject the packet if it silently accepts stale metadata, conflates signature validity with freshness or provenance, installs after target mismatch, hides a failed denominator, treats rollback or migration as safe without fault evidence, or leaks secrets. Until this route is completed and reviewed, `PB-017` remains `partial`, `TASK-000009` remains proposed-only, and the repository must not claim a production updater, package format, signing readiness, stable channel, public distribution, rollback safety, migration safety, supported security, release readiness, or implementation readiness.

## Handoff

This route is compatible with the checked [update-lab package template](../release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json) and [package/update readiness-review template](../release-operations/machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json). Those templates define the future packet shape; they are not execution or release evidence. The next acceptable artifact is a fake-key, local-only lab packet with redacted logs, hashes, fault coverage, rollback/migration transitions, cleanup evidence, and named review.

The [Package and Update Lab Packet Examples](package-update-lab-packet-examples-2026-07.md) supplies a fictitious local fake-key packet covering trust-state separation, metadata verification, install faults, rollback/migration, privacy events, cleanup, and review rejection rules. It is a handoff example only and does not satisfy `PB-017` evidence.

## PB-020 closure dependency

Any future `PB-017` readiness decision must be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and the [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md) route. A fake-key lab result, accepted metadata contract, rollback rehearsal, package/update readiness review, or release-operations decision cannot independently close `PB-020`, authorize production signing, establish a stable channel, approve public distribution, support migration or rollback safety, or grant release, supported-security, Chrome-class, or broad implementation claims. The final closure record must preserve exact source/build/artifact identities, key and fixture boundaries, failure denominators, named owner and independent reviewers, exceptions and expiry, and synchronized readiness, task, requirement, risk, support, signing, and release records.

## Validation

```powershell
python -B tools/validate_research_package_update_lab.py
python -B tools/validate_research_package_update_readiness_review.py
python -B tools/validate_blueprint.py
.\tools\check.ps1
```
