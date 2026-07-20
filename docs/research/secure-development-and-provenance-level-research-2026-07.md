# Secure Development and Provenance Level Research - July 2026

Status: deferred `RQ-64` research packet; no maturity level, certification, or release claim
Owner: security, architecture, build, release operations, supply chain, quality, and legal-community
Question: Which NIST SSDF, SP 800-218A, SLSA Source/Build, SBOM, review-attestation, and reproducibility controls are achievable and useful at each maturity?

This packet defines a decision route. It does not declare Turing compliant with SSDF, SLSA, a regulation, a certification, a reproducible-build level, or a release-security standard. The governing security and release books remain authoritative for requirements and implementation boundaries.

## Source-backed observations

NIST SP 800-218 SSDF 1.1 is a set of high-level secure software development practices that can be integrated into an SDLC. NIST describes it as a common vocabulary for reducing vulnerabilities, mitigating undetected or unaddressed vulnerabilities, and addressing root causes. It is a practice framework, not a pass/fail product certification. [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)

SLSA 1.2 is an approved specification with separate Source and Build tracks, increasing levels, recommended attestation formats, and distinct producer, distributor, verifier, and build-platform concerns. Its Build Provenance model records the build definition, external parameters, resolved dependencies, builder identity, execution metadata, and output subjects. Provenance describes how an artifact was produced; it does not by itself authorize an update, prove vulnerability absence, establish legal approval, or prove that a browser is safe. [SLSA specification v1.2](https://slsa.dev/spec/v1.2/) and [SLSA Build Provenance](https://slsa.dev/spec/v1.2/build-provenance)

An evidence claim must therefore name the exact framework version, track, predicate, scope, artifact, source revision, builder, dependencies, review method, and limitations. A passing local check, a signed artifact, a populated SBOM, or a matching rebuild is one evidence class; none is a substitute for the others.

## Turing maturity model

The owner decision should select a maturity profile per scope, not one blanket label for the repository:

| Maturity | Evidence intent | Minimum boundary | Must not claim |
|---|---|---|---|
| `M0 documented` | Policies, ownership, threat model, required evidence, and no-claim templates are discoverable | Canonical requirements, risks, task boundaries, review roles, and evidence schemas | Secure implementation, provenance, reproducibility, or release integrity |
| `M1 controlled development` | Changes have review, testing, dependency/source records, provenance inputs, and reproducible commands | Protected review paths, vulnerability intake, dependency identity, SBOM generation route, retained logs, and negative tests | Independent verification, artifact integrity, or production support |
| `M2 verified build evidence` | Independent builds or replayable evidence corroborate source, inputs, builder, and outputs | Pinned environment, external or clean-host reproduction, artifact hashes, provenance verification, dependency closure, and discrepancy handling | SLSA level, secure release, or vulnerability absence unless the exact criterion is met |
| `M3 release-controlled` | Release artifacts and update decisions are authorized, reviewable, recoverable, and supported | Signed package identity, update trust, two-person control, incident response, rollback/recovery, supported lifecycle, and owner review | Stable or production safety without the complete release and support gate |

These labels are proposed Turing bookkeeping terms, not NIST or SLSA levels. A scope can remain at a lower maturity while another scope advances; the lowest relevant maturity and its residual risk must remain visible for any release claim.

## Evidence contract

Every future maturity record must identify:

- scope, repository revision, platform, build profile, dependency and toolchain lock state, and exact framework/specification versions;
- the claim being evaluated, its threat model, required control, evidence type, reviewer, date, retention, and expiration or re-review trigger;
- source and dependency identity, SBOM format and completeness limits, generator/version, transitive inputs, native assets, generated output, and license/advisory boundary;
- build definition, external parameters, resolved dependencies, builder identity, invocation, output subjects, artifact hashes, and provenance verification result;
- independent replay or clean-host comparison, environment differences, nondeterminism classification, acceptable variance policy, and unresolved discrepancy disposition;
- code review, security review, test evidence, fuzzing/negative cases, vulnerability intake, remediation, exception, and rollback records;
- release and update authorization, signer or threshold policy, package identity, minimum secure version, incident path, support term, and owner-approved claim boundary.

Evidence must distinguish observed facts, reviewer judgments, framework mappings, and Turing proposals. Generated records must identify their source and regeneration command. Logs and attestations must not contain credentials, signing secrets, profile contents, private-session data, or unnecessary personal information.

## Cross-framework separation

- SSDF organizes secure-development practices and communication; it does not select Turing's architecture, prove every control is implemented, or issue a certification.
- SLSA Source/Build provides a vocabulary and graduated supply-chain properties; a SLSA track or level cannot be claimed without the exact versioned requirements and evidence.
- SBOMs describe component inventories and relationships; they do not prove vulnerability absence, license acceptance, provenance, or safe native packaging.
- Reproducible builds show an output relationship under defined inputs and environments; they do not alone prove source trust, independent builder integrity, review quality, or update authorization.
- Signatures and attestations bind an assertion or artifact to a key or identity; they do not establish freshness, authorized release policy, safe installation, profile migration safety, or support status.

## Decision and evidence sequence

Before selecting a maturity level, the owner review should:

1. freeze the scope and claim vocabulary, including unsupported claims;
2. map SSDF practices and SLSA track requirements to Turing requirements, risks, tasks, and owners;
3. capture source, dependency, generated-output, native-package, SBOM, and license/advisory identity;
4. execute controlled review, test, vulnerability, provenance, and reproducibility evidence with retained artifacts;
5. independently verify the evidence and record discrepancies, exceptions, expiry, rollback, and residual risk;
6. reconcile the decision with `ADR-0009`, `PB-002`, `PB-008`, `PB-009`, `PB-017`, `PB-018`, `PB-019`, and `PB-020` wherever the scope overlaps source, build, release, update, incident, ownership, or support authority.

The next acceptable artifact is an owner-reviewed, scope-specific maturity record backed by retained evidence. A template, source manifest, research packet, local build, or passing repository check is preparation only.

## Current disposition

`RQ-64` remains deferred. This packet makes the maturity and provenance evidence route explicit without selecting a compliance target, changing active/deferred counts, authorizing broad implementation, or changing the `90%` contained-M0 / `0%` full-build measures.

## Retrieval record

- Retrieved 2026-07-19.
- NIST SP 800-218 SSDF 1.1: https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA specification v1.2: https://slsa.dev/spec/v1.2/
- SLSA Build Provenance v1: https://slsa.dev/spec/v1.2/build-provenance
