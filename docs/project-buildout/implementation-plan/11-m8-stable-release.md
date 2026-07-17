# 11 — M8: Stable General-Purpose Release Candidate

Status: implementation game plan; stable is a finite evidence-backed support contract  
Owner: human release authority, release board, security, legal, support, accessibility, operations, and subsystem owners

## 1. Objective

M8 produces a stable release candidate for normal users within an explicit platform, hardware, compatibility, feature, service, and support envelope. Stable does not mean every Chrome feature exists. It means the advertised scope is dependable, supportable, secure enough for its stated use, updatable, recoverable, accessible, and honestly documented.

## 2. Stable-scope contract

Before release-candidate promotion, ADR-0018 and `PRG-001` define:

- supported operating systems and minimum versions;
- CPU architectures and required instruction sets;
- supported graphics backends and software fallback;
- installer/package formats;
- included web-platform and JavaScript feature maps;
- supported profile, migration, Plug-in, embedding, DevTools, automation, and agent API versions;
- media/codec/PDF/printing/DRM matrix;
- accessibility technology matrix;
- online services that are required, optional, or unavailable;
- support duration and end-of-life policy;
- known proprietary gaps and non-goals;
- privacy, telemetry, crash, sync, AI, and account behavior;
- minimum hardware and resource expectations.

Anything outside this contract is experimental, preview-only, disabled, or unsupported.

## 3. Production release gates

Every applicable `PRG-001` through `PRG-020` must be ready with linked evidence. At minimum:

- finite accepted scope and platform matrix;
- effective sandbox and site isolation;
- signed update, rollback, freeze/rollback resistance, and minimum secure version;
- reproducible builds, SBOM, provenance, symbols, notices, and source identity;
- numeric reliability, performance, and recovery SLOs;
- compatibility and conformance thresholds;
- independent security review;
- accessibility and usability conformance;
- migration, data-loss, corruption, and recovery evidence;
- vulnerability response and on-call staffing;
- service outage, disaster recovery, and offline behavior;
- legal, privacy, licensing, distribution, codec, trademark, and AI-provider approval;
- signing-key ceremony and role separation;
- protected main and independent review enforcement;
- installation/update/rollback rehearsal on every supported platform;
- human production-readiness approval.

## 4. Artifact and update integrity

Release artifacts include:

- exact source commit and build manifest;
- deterministic/reproducible build result or explained variance;
- SBOM and third-party notices;
- dependency, native, generated, and unsafe inventories;
- signed provenance attestation;
- split debug symbols and crash compatibility;
- package digest and signatures;
- update metadata with root, targets, snapshot, timestamp, delegation, expiry, and rollback/freeze protection or an accepted equivalent;
- offline-root and threshold-key records;
- staged rollout cohort, pause, rollback, and emergency revocation controls;
- profile compatibility range and downgrade policy.

Implementation agents cannot hold production signing keys or approve stable promotion.

## 5. Final verification

The release candidate is tested as installed artifacts, not only as source builds:

- clean install, upgrade from every supported prior version, repair, uninstall, reinstall, and rollback;
- interrupted download, disk full, power loss, clock skew, metadata expiry, mirror failure, and corrupted package;
- profile migration, downgrade block, backup, restore, export, and corruption repair;
- launch, browsing, media, printing, permissions, credentials, downloads, Plug-ins, DevTools, automation, and agents within stable scope;
- sandbox and mitigation evidence from packaged binaries;
- crash, hang, GPU reset, network/storage service restart, and session recovery;
- accessibility critical flows with real assistive technology;
- privacy/telemetry data inspection;
- service outage and offline behavior;
- fixed-hardware SLO and error-budget review.

## 6. Release decision

The human release authority reviews:

- unresolved critical/high risks and approved expiring exceptions;
- security and accessibility reports;
- SLO and error-budget state;
- conformance and top-workflow results;
- support/on-call staffing;
- update/signing readiness;
- legal approvals;
- rollback and stop conditions;
- exact release notes and unsupported behavior.

A release is denied when evidence is missing, not merely when a test is red.

## 7. Post-release obligations

Stable launch starts, rather than ends, the support lifecycle:

- active vulnerability monitoring and patching;
- continuous WPT/Test262 and compatibility tracking;
- crash, performance, energy, update, migration, and service monitoring;
- public known issues and security advisories;
- regular key rotation, restore, and incident exercises;
- deprecation and end-of-life communication;
- accessibility regression prevention;
- dependency and license updates;
- capacity to halt rollout or revoke a release.

## 8. M8 exit criteria

- zero open critical security, update, data-loss, or signing issues;
- all applicable stable gates pass;
- independent security and accessibility reviews are complete;
- supported platform and feature contracts are published;
- staffing can maintain every supported platform and urgent fix path;
- release board and human authority approve stable based on evidence;
- the exact artifact digest, signatures, update metadata, and support statement are published.
