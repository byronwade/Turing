# Build, Release, Update, and Incident Operations Engineering Book

Status: detailed research and design baseline  
Owner: build, release, update, and security operations  
Canonical overview: [Blueprint owner](../blueprint-v1/13-build-release-operations.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

A browser is only as secure as its ability to reproduce, sign, distribute, update, diagnose, and rapidly patch every supported build. Operational readiness is a release feature, not post-launch administration.

## Reading order

1. [Build Identity and Hermetic Toolchains](01-build-identity-and-hermetic-toolchains.md)
2. [Reproducible Builds, Provenance, and SBOM](02-reproducible-builds-provenance-and-sbom.md)
3. [Signing Keys and Package Attestation](03-signing-keys-and-package-attestation.md)
4. [Platform Packaging and Installers](04-platform-packaging-and-installers.md)
5. [Update Metadata, Rollout, and Rollback](05-update-metadata-rollout-and-rollback.md)
6. [Profile Migrations and Downgrade Protection](06-profile-migrations-and-downgrade-protection.md)
7. [Crash Reporting, Symbols, and Redaction](07-crash-reporting-symbols-and-redaction.md)
8. [Vulnerability Response and Supported Lifecycle](08-vulnerability-response-and-supported-lifecycle.md)

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

- https://reproducible-builds.org/
- https://slsa.dev/
- https://in-toto.io/
- https://theupdateframework.io/
- https://www.sigstore.dev/
- https://spdx.dev/
- https://cyclonedx.org/

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
## Migration, export, sync, and support

Market differentiation creates long-lived formats and services. Release evidence must cover importer safety, export compatibility, snapshot restoration, sync conflicts, key recovery, collaboration revocation, support, and end-of-life.

The checked [Profile Session Format Inventory](../research/profile-session-format-inventory-2026-07.md) and checked no-claim [schema-package template](../storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json) are no-claim `PB-016` planning evidence only. They do not approve executable schemas beyond the template, production profile formats, real-profile migration, sync, credential storage, rollback safety, data-loss safety, or user-data handling readiness.

## Research package/update lab boundary

The checked [Research Package Update Lab Inventory](../research/research-package-update-lab-inventory-2026-07.md), [`research-package-update-lab.json`](machine/research-package-update-lab.json), [`research-package-update-lab-package.schema.json`](machine/research-package-update-lab-package.schema.json), checked no-claim [`no-claim-update-lab-template.json`](machine/research-package-update-lab-packages/no-claim-update-lab-template.json), checked no-claim [`no-claim-research-package-update-readiness-template.json`](machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json), [`validate_research_package_update_lab.py`](../../tools/validate_research_package_update_lab.py), and [`validate_research_package_update_readiness_review.py`](../../tools/validate_research_package_update_readiness_review.py) provide no-claim `PB-017` planning evidence for research-package identity, update metadata, rollback, migration, crash-loop, privacy-preserving event behavior, future fake-key local update-lab package handoff fields, and a package/update readiness-review handoff shape. They do not implement an updater, provide an executable package manifest or metadata parser beyond the template, approve owner-reviewed package/update readiness, approve production signing keys, approve offline roots, create a stable channel, permit public binary distribution, prove rollback or migration safety, create supported-security evidence, authorize a production updater, or create release readiness.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## UI package profiles

Release manifests record the selected UI toolkit, exact source, license choice, backend, renderer, native libraries, feature flags, assets, locales, and build identity. Normal packages must not accidentally include multiple renderers, runtime UI interpreters, design-lab assets, React/Node dependencies, or webviews.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Stable release and agent boundary

Release operations must implement the Production Readiness machine gates, SLOs, update roles, vulnerability SLA activation, source/build provenance, service failure behavior, signing separation, and human authorization. Coding agents never receive offline root keys or stable-promotion authority.

The checked [Incident Patch Rehearsal Inventory](../research/incident-patch-rehearsal-inventory-2026-07.md), checked no-claim [incident patch rehearsal template](../security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), and checked no-claim [incident/patch readiness-review template](../security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json) are `PB-018` planning evidence only. They do not approve executed incident rehearsal, owner-reviewed incident/patch readiness beyond the template, incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, incident closure authority, signing authority, stable promotion, implementation, or production-safe browsing.
