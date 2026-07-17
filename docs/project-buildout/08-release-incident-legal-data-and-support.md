# Release, Incident, Legal, Data, and Support Operations

Status: detailed research and professional operating baseline  
Owner: release, security, legal, privacy, support, and platform owners  
Last researched: 2026-07-16

## Purpose

Turn release principles into executable build, signing, update, rollback, migration, incident, data, legal, support, and end-of-life operations.

## Governing principles

- A supported release is an operational commitment.
- Users must recover from bad binaries, updates, profiles, dependencies, and services.
- Every distributed byte has known source and license.
- Every remote field has purpose, owner, retention, and deletion.
- Runbooks are exercised before incidents.

## Required contract

- Maintain channel policy, platform matrix, security-patch target, support SLA, and EOL.
- Provide runbooks for exploitation, sandbox escape, signing compromise, dependency zero-day, credential leak, cross-profile leak, data loss, malicious Plug-in/provider, certificate failure, service outage, and rollback.
- Use reproducible unsigned builds, provenance, SBOM, notices, symbols, hardware-backed or threshold signing, staged rollout, rollback, and minimum secure versions.
- Maintain data inventory for profile, crash, update, telemetry, sync, Plug-ins, AI providers, diagnostics, and support bundles.
- Complete MPL/DCO-or-CLA, third-party, trademark, patent, media/codec/DRM, export, privacy, accessibility, app-store, and distribution review.
- Publish code of conduct, safe-harbor intent, moderation, and incident communication.

## Professional workflow

1. Build from protected commit and independent environments.
2. Complete cross-cutting release evidence.
3. Approve rollout and thresholds.
4. Exercise rollback and migration.
5. Run incidents with severity and command structure.
6. Publish postmortem and systemic actions.

## Evidence and exit gates

- PBO-GATE-12: beta/stable has exercised emergency patch and communication paths.
- PBO-GATE-13: broad contribution and distribution wait for legal/provenance review.
- Every remote event is registered and tested for deletion.
- On-call, signing, domain, CI, and package recovery are tested.

## Risks and failure modes

- Rollback can reintroduce known vulnerabilities.
- Crash data can contain secrets.
- Legal duties vary by jurisdiction.
- Runbooks and service ownership can stale.

## Primary sources

- NIST Incident Response SP 800-61 Rev. 3 — https://csrc.nist.gov/pubs/sp/800/61/r3/final
- The Update Framework — https://theupdateframework.io/
- Mozilla Public License 2.0 — https://www.mozilla.org/en-US/MPL/2.0/
- REUSE specification — https://reuse.software/spec/

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Production readiness ownership

The Production Readiness book owns stable scope, platforms, channels, SLOs, update roles, vulnerability SLAs, service dependencies, support, signing, legal approval, and human release authority. Agents may prepare evidence but cannot make these decisions.
