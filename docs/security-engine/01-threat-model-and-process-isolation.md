# Threat Model and Process Isolation

Status: research and design baseline  
Owner: security architecture  
Purpose: Define hostile principals, protected assets, process roles, site isolation, and compromise containment.

## Relationship to the Turing program

This document expands [Blueprint 04 — system architecture](../blueprint-v1/04-system-architecture.md) and [Blueprint 08](../blueprint-v1/08-security-and-sandbox.md). The process simulator is governed by RQ-02 and EXP-ENGINE-004.

## Threat actors and assumptions

The baseline attackers include malicious sites and advertisements, compromised third-party scripts, hostile local files and downloads, network influence within configured trust, malicious extensions, compromised renderers or utility processes, prompt-injected models, unauthenticated developer clients, corrupted profiles, update and build-chain attackers, and stolen maintainer credentials.

The design does not assume signed browser code is correct. It distinguishes remote web compromise, local unprivileged attack, user-equivalent malware, physical access, and privileged OS compromise so guarantees are not overstated.

## Protected assets

Protected assets include credentials, cookies, passkeys, authentication state, profile content, private sessions, local files, clipboard, device access, browser settings, enterprise policy, cross-origin data, cross-profile data, trusted UI, update keys, release metadata, model/provider credentials, agent grants, and audit records.

Each asset has an owner, storage location, authorized operations, process access list, lifecycle, logging policy, backup/migration policy, and incident consequence.

## Security principals

Principals include profile, private session, top-level site, origin, frame, browsing-context group, document epoch, process, worker, extension, developer client, automation session, agent, provider, and updater. Typed identities are issued by trusted policy code and never inferred solely from renderer-provided strings.

Authority is granted as bounded capabilities containing operation, resource, principal scope, expiry, usage count, and revocation state. Possessing an IPC channel does not grant every method.

## Process roles

The minimum topology separates browser kernel/policy, browser UI, renderer, network, storage, GPU/compositor, decoder/media, extension, DevTools, agent/model, updater, and crash handling where platform constraints permit. Each process receives an explicit capability manifest and handle allowlist.

Privilege grows only where the role requires it. The network service can open sockets but cannot read credential vault contents directly. The credential broker can approve a credential operation but cannot navigate. The GPU service validates graphics commands but cannot read profile databases.

## Site isolation

Site instances and browsing-context groups determine renderer assignment. Cross-site frames, popups, opener changes, redirects, COOP/COEP, origin-agent clusters, opaque origins, sandboxed documents, internal schemes, extensions, and isolated origins receive explicit process policy.

Cross-process frame composition uses proxy objects and validated surface/geometry metadata rather than shared DOM or script heaps. Process reuse is permitted only for security-equivalent principals. BFCache, speculative rendering, crash recovery, and memory pressure preserve the isolation decision.

## Navigation and document epochs

Navigation is a transaction: request, response policy, process/site selection, provisional document, commit, old-document retirement, history update, and visible state. Every asynchronous callback and privileged operation validates the current document epoch before effect.

A compromised renderer cannot commit a different URL, origin, security state, permission state, or site instance than the browser kernel approved.

## Compromise containment

For each process role, the threat model asks what an attacker gains after arbitrary code execution. A renderer compromise should expose only that renderer's assigned site instances and explicitly delegated resources. A decoder compromise should expose bounded input/output buffers. An agent-host compromise should expose only scoped observations and proposed actions, not credentials or direct browser handles.

Crash blast radius, restart behavior, orphaned resources, revocation, audit, and user-visible recovery are part of containment.

## Non-negotiable invariants

- Mutually hostile sites do not share renderer memory or direct object graphs.
- Profile and private-session boundaries are never treated as UI-only organization.
- Trusted process identity overrides conflicting untrusted message claims.
- Every document-sensitive action validates the current document epoch.
- Memory, performance, or compatibility pressure cannot silently widen authority.
- A compromised utility process receives no capabilities outside its declared role.

## Required evidence

- Machine-readable process/capability matrix and generated launch manifests.
- Site-assignment tests across navigation, redirects, popups, iframes, BFCache, crashes, and pressure.
- Compromised-renderer and compromised-utility harnesses invoking every broker method.
- Cross-profile, cross-origin, and stale-epoch negative tests.
- Crash/restart/revocation tests with orphaned handles and in-flight operations.
- Architecture review mapping every protected asset to reachable processes.

## Known risks and unresolved questions

- Incorrect site computation or process reuse can defeat otherwise strong sandboxing.
- A highly privileged browser kernel remains a valuable target.
- Cross-process frame and accessibility composition can leak data through metadata.
- Process count and launch cost may create pressure to weaken isolation.

## Primary sources

- Chromium process model and site isolation — https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md
- WebKit site isolation — https://docs.webkit.org/Deep%20Dive/SiteIsolation.html
- [Process Topology and Isolation-Adjusted Memory Research](../research/process-topology-isolation-adjusted-memory-research-2026-07.md)
- Firefox process model — https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html
- WHATWG HTML Living Standard — https://html.spec.whatwg.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
