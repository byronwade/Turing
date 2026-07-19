# Package, Update Trust, And Recovery Decision Preparation - July 2026

Status: no-claim source-backed decision preparation
Owner: release operations, security, build, storage, and documentation-research
Related gate: `PB-017`
Retrieval date: 2026-07-19
Tested configuration: documentation and research only; no updater, signing key, package, or user profile was executed

## Question

What trust and recovery properties must the Turing package/update design preserve before `PB-017` can move beyond planning evidence, and which properties are supplied by established frameworks rather than invented locally?

## Decision status

No package format, update framework, signing model, key hierarchy, channel, or recovery policy is selected by this report. It converts external standards into decision criteria and keeps the implementation boundary explicit.

The current repository remains at `PB-017: partial`. The checked update-lab inventory and no-claim package template are planning evidence only. They do not prove an executable package manifest, metadata parser, signature verification, staged installation, rollback, migration, privacy, release, or supported-security behavior.

## Source-backed observations

### TUF separates update trust roles

The [TUF roles and metadata guidance](https://theupdateframework.io/docs/metadata/) defines Root, Targets, Snapshot, and Timestamp roles. It records target hashes and sizes, uses expiration, and separates frequently refreshed timestamp metadata from the more stable repository view. TUF's [security guidance](https://theupdateframework.io/docs/security/) treats rollback, fast-forward, indefinite-freeze, key-compromise, arbitrary-installation, and resource-exhaustion attacks as separate classes with distinct checks.

Implications for Turing:

- a future metadata contract must identify role, key set, threshold, version, expiry, target digest, target size, channel, platform, architecture, and minimum secure version;
- the client must distinguish stale metadata from an unavailable service and must not silently treat either as a successful update check;
- mirror selection, cache behavior, and retry policy must not bypass metadata freshness or target identity checks;
- rollback and downgrade are policy decisions layered on top of metadata verification, not synonyms for signature validity.

TUF supplies a framework for update metadata trust. It does not decide Turing's package layout, profile migration semantics, installer transaction model, UI, or supported-channel policy.

### SLSA describes build provenance, not update authorization

The [SLSA v1.2 build provenance specification](https://slsa.dev/spec/v1.2/build-provenance) defines provenance as verifiable information about where, when, and how an artifact was produced. The [SLSA build tracks](https://slsa.dev/spec/v1.2/build-track-basics) distinguish provenance existence from stronger hosted and hardened build guarantees.

Implications for Turing:

- provenance must bind the artifact to source, build definition, builder identity, inputs, and build metadata;
- a provenance record is evidence about production, not permission for a client to install an artifact;
- the package identity ledger must retain the distinction between unsigned reproducible payload, provenance, artifact signature, update metadata authorization, and platform installer acceptance;
- a claimed SLSA level must name the exact version and track rather than using “SLSA compliant” as an unbounded release claim.

### in-toto describes authorized supply-chain steps

The [in-toto getting-started documentation](https://in-toto.io/docs/getting-started/) describes a signed layout that lists supply-chain steps and authorized functionaries, with link metadata recording the materials and products of each step.

Implications for Turing:

- a future release evidence bundle should identify which roles may produce, transform, sign, attest, publish, and promote each artifact;
- step authorization and artifact signature verification should be recorded separately;
- a valid signature on a package cannot prove that an unauthorized build or packaging step was absent;
- the evidence bundle needs a failure denominator for missing, rejected, expired, or mismatched step metadata.

### Sigstore provides one possible signing and transparency model

The [Sigstore signing overview](https://docs.sigstore.dev/cosign/signing/overview/) describes identity-bound short-lived certificates and transparency-log records. Its [bundle documentation](https://docs.sigstore.dev/about/bundle/) explains that verification material can include certificates, signatures, and signed timestamps or transparency-log evidence.

Implications for Turing:

- keyless signing is not automatically appropriate for a browser's offline-root, channel, privacy, or emergency-recovery requirements;
- identity and transparency metadata may disclose signer information and must receive a privacy review before adoption;
- a future decision must compare Sigstore, managed long-lived keys, hardware-backed keys, and threshold-controlled offline roles against recovery, offline verification, revocation, audit, privacy, and platform constraints;
- signing evidence must retain the artifact digest and verification material without placing secrets, profile contents, credentials, or private-session data into logs.

Sigstore is a candidate integration or evidence format, not a Turing decision in this report.

## Required trust-state separation

The following states must remain distinct in the package/update model:

1. source identity: exact source revision and dependency/vendor inputs;
2. build identity: toolchain, target, features, generator inputs, and builder record;
3. artifact identity: digest, size, package contents, symbols, notices, and SBOM;
4. provenance: evidence describing how the artifact was produced;
5. artifact signature: cryptographic authorization over an identified object;
6. update metadata authorization: channel, target, freshness, rollout, platform, architecture, and minimum secure-version policy;
7. installation transaction: staging, verification, atomicity, restart, recovery, and cleanup;
8. profile transition: schema migration, downgrade refusal, rollback compatibility, and user-data recovery;
9. support decision: whether a channel/version/platform is actually supported and patched.

No state may be inferred solely from another state. In particular, a valid signature does not prove freshness, provenance, package safety, migration safety, or support status.

## Recovery and fault matrix to preserve

The executable lab must eventually produce retained evidence for, at minimum:

| Fault or adversarial condition | Required observable result |
| --- | --- |
| stale or expired metadata | update is rejected or clearly reported as unable to establish freshness |
| rollback or fast-forward metadata | version policy rejects unsafe movement and records the reason |
| wrong channel/platform/architecture | target is rejected before installation |
| digest or size mismatch | payload is deleted/quarantined and never executed |
| mirror disagreement | metadata trust and target identity decide; mirror order cannot weaken policy |
| interrupted download or partial write | previous install remains usable or recovery enters an explicit failure state |
| disk full or power loss | transaction recovery is bounded, repeatable, and does not claim success without verification |
| post-install crash loop | health policy stops repeated activation and preserves a known-good path where authorized |
| migration failure or downgrade | profile remains recoverable; unsupported downgrade is explicit |
| compromised or revoked signer | trust metadata and revocation policy reject the signer or require controlled recovery |
| diagnostic/event capture | no credentials, profile contents, private-session data, or secrets are emitted |

This matrix is a test-planning contract, not evidence that any row is implemented.

## Decision questions before implementation

The owner review must answer, with selected versions and evidence:

- Is TUF used directly, adapted, or replaced, and which roles are online versus offline?
- Is provenance represented with SLSA/in-toto-compatible attestations, and what exact predicate/version is accepted?
- Is Sigstore used, self-hosted, combined with another trust root, or rejected due to privacy/offline/recovery constraints?
- What is the initial trust-root delivery and out-of-band recovery mechanism?
- Which artifact, metadata, channel, platform, architecture, and minimum-secure-version fields are mandatory?
- Which failures block installation, which permit retry, and which require operator or user action?
- What profile schema versions can be opened, migrated, rolled back, exported, or repaired?
- What package/update evidence is retained, for how long, and under which access controls?

## Next proof

`PB-017` remains partial until a task-scoped research lab produces executable, fake-key or otherwise non-production evidence for package identity, metadata parsing, threshold/signature checks, freshness, target binding, staged-install faults, authorized rollback, vulnerable-version refusal, migration/downgrade/crash-loop behavior, and privacy-preserving events. The owner must then review the retained evidence against the package/update readiness-review template. No production keys, offline roots, stable channel, public distribution, real updater, or real user profile is required or permitted for that contained proof.

## Claim boundary

This report does not select TUF, SLSA, in-toto, Sigstore, a package format, an updater architecture, a signing hierarchy, a release channel, a supported platform, or a profile migration policy. It makes no claims of production security, rollback safety, migration safety, release readiness, supported security, Chrome-class performance, or implementation.

## References

- [TUF roles and metadata](https://theupdateframework.io/docs/metadata/)
- [TUF security properties](https://theupdateframework.io/docs/security/)
- [TUF FAQ and key compromise guidance](https://theupdateframework.io/docs/faq/)
- [SLSA v1.2 build provenance](https://slsa.dev/spec/v1.2/build-provenance)
- [SLSA v1.2 build tracks](https://slsa.dev/spec/v1.2/build-track-basics)
- [in-toto getting started](https://in-toto.io/docs/getting-started/)
- [Sigstore signing overview](https://docs.sigstore.dev/cosign/signing/overview/)
- [Sigstore bundle format](https://docs.sigstore.dev/about/bundle/)
