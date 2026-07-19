# Browser Security Engineering Book

Status: detailed research and design baseline
Owner: browser security architecture
Canonical overview: [Blueprint 08 — security, privacy, and sandbox](../blueprint-v1/08-security-and-sandbox.md)

This book expands the threat model into subsystem contracts, platform evidence, exploit mitigations, trusted UI, release security, and verification. It does not claim that Turing is safe for arbitrary hostile browsing. No general-use security claim is permitted until the documented gates pass on every supported platform and the project can sustain emergency updates.

## Reading order

1. [Threat model and process isolation](01-threat-model-and-process-isolation.md)
2. [Sandbox brokers and platform containment](02-sandbox-brokers-and-platform-containment.md)
3. [Memory safety, JIT, and exploit hardening](03-memory-safety-jit-and-exploit-hardening.md)
4. [Web security, privacy, and trusted UI](04-web-security-privacy-and-trusted-ui.md)
5. [Update, supply chain, and vulnerability response](05-update-supply-chain-and-vulnerability-response.md)
6. [Security verification and release gates](06-security-verification-and-release-gates.md)

## Security thesis

Turing must assume that every parser, renderer, decoder, runtime, extension, developer tool, model adapter, storage file, and network response can become malicious or compromised. Safety comes from reducing bug classes, minimizing privileged code, separating mutually hostile principals, validating every boundary, limiting available capabilities, preserving trusted user decisions, and maintaining a credible patch pipeline.

A memory-safe language materially improves the baseline but does not replace isolation, logic security, origin policy, update integrity, or incident response.

## Defense layers

1. standards-correct web security policy;
2. memory-safe implementation and audited unsafe/native boundaries;
3. site and profile isolation;
4. least-privileged processes and capabilities;
5. OS sandbox and brokers;
6. validated typed IPC;
7. JIT/GPU/codec hardening;
8. trusted UI and user confirmation;
9. signed reproducible updates and rollback controls;
10. continuous fuzzing, red teaming, independent review, and rapid response.

## Non-negotiable release posture

- An engine preview is explicitly unsafe for sensitive or hostile browsing.
- A renderer may be compromised without exposing arbitrary files, sockets, credentials, other profiles, or browser-internal authority.
- Memory pressure cannot collapse hostile sites into one process.
- Developer, extension, automation, and AI features use the same policy boundaries rather than bypasses.
- Security warnings, origin display, permission prompts, and agent confirmation remain browser-controlled and accessible.
- Every supported release has a private reporting path, owned triage, reproducible patch pipeline, and published support statement.
- Missing anti-phishing, reputation, codec, DRM, or platform security services are disclosed.

## Leadership criteria

Security leadership means measurable containment and response, not absence of public incidents. Turing should publish sandbox evidence, process/capability maps, fuzzing status, unsafe/native dependency inventories, update provenance, release-hardening flags, supported-version policy, independent review results, and closed systemic lessons without exposing active users to unnecessary risk.

## Advanced research

7. [Speculation, Timers, and Side Channels](07-speculation-timers-and-side-channels.md)
8. [Native Parser and Codec Isolation](08-native-parser-and-codec-isolation.md)
9. [Heap Sandboxes, Pointer Tables, and JIT Compartments](09-heap-sandboxes-pointer-tables-and-jit-compartments.md)
10. [Capability Provenance, Attenuation, and Revocation](10-capability-provenance-attenuation-and-revocation.md)
11. [Developer, Extension, Automation, and Agent Attack Surfaces](11-developer-extension-automation-and-agent-attack-surfaces.md)
12. [Anti-Phishing, Reputation, Abuse Resistance, and Trusted UI](12-anti-phishing-reputation-and-trusted-ui.md)

## Related material

- [Browser engine book](../engine/README.md)
- [JavaScript runtime book](../javascript/README.md)
- [AI engineering book](../ai/README.md)
- [Build and release operations](../blueprint-v1/13-build-release-operations.md)
- [Security policy](../security.md)
- [Servo security and maintenance implications](../research/servo-security-maintenance-implications-2026-07.md)
- [Sandbox Probe Inventory](../research/sandbox-probe-inventory-2026-07.md)
- [Sandbox Platform-Evidence Decision Preparation](../research/sandbox-platform-evidence-decision-prep-2026-07.md)
- [`sandbox-platform-source-manifest.json`](machine/sandbox-platform-source-manifest.json)
- [`validate_sandbox_platform_sources.py`](../../tools/validate_sandbox_platform_sources.py)
- [WP-003 Sandbox Probe Contract](../research/wp-003-sandbox-probe-plan-2026-07.md)
- [Sandbox Probe Execution and Containment Closure Preparation](../research/sandbox-probe-execution-and-containment-closure-preparation-2026-07.md)
- [Incident Patch Rehearsal Inventory](../research/incident-patch-rehearsal-inventory-2026-07.md)
- [Incident Response and Emergency Patch Decision Preparation](../research/incident-response-and-emergency-patch-decision-prep-2026-07.md)
- [Incident-Response Execution and Disclosure Closure Preparation](../research/incident-response-execution-and-disclosure-closure-preparation-2026-07.md)
- [Incident-Response and Patch-Rehearsal Packet Examples](../research/incident-response-patch-rehearsal-packet-examples-2026-07.md)

## Incident and patch readiness boundary

The checked no-claim [incident patch rehearsal template](machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), checked no-claim [incident/patch readiness-review template](machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json), focused [`validate_incident_patch_readiness_review.py`](../../tools/validate_incident_patch_readiness_review.py), and [Incident-Response Execution and Disclosure Closure Preparation](../research/incident-response-execution-and-disclosure-closure-preparation-2026-07.md) provide `PB-018` owner-review handoff shape only. They do not approve executed private-intake tabletop output, emergency patch dry-run records, owner-reviewed incident/patch readiness, incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, stable promotion, signing authority, incident closure authority, implementation, or production-safe browsing. Any future incident decision also remains subject to the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md), `PB-020` closure, and independent review.

The checked no-claim [sandbox probe-package template](machine/sandbox-probe-packages/no-claim-expected-deny-template.json), [sandbox readiness-review template](machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json), and [Sandbox Probe Execution and Containment Closure Preparation](../research/sandbox-probe-execution-and-containment-closure-preparation-2026-07.md) are the `PB-012` evidence-order handoff. They do not prove packaged probes, effective platform policy, owner-reviewed sandbox readiness, renderer security, site isolation, hostile-browsing safety, or production containment.

<!-- MARKET-STRATEGY-2026-07 -->
## Market-driven trust boundaries

Spaces, identity routing, migration, Time Machine, privacy receipts, sync, collaboration, Plug-ins, and agent mode each create security boundaries. Market demand cannot widen ambient authority or bypass trusted UI, data minimization, isolation, review, or incident obligations.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Trusted UI toolkit boundary

The native UI toolkit is privileged presentation infrastructure, not a policy authority. Toolkit callbacks emit typed commands; browser services revalidate identity, epoch, profile, permission, credential, Plug-in, and agent policy. Dynamic UI source loading, runtime interpreters, arbitrary scripts, generic kernel bridges, and page-controlled trusted overlays are prohibited in normal release builds.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Coding-agent threat surface

AI-assisted implementation is part of the supply-chain threat model. Repository content, build output, issues, tools, dependencies, and model responses are untrusted; task-scoped authority, provenance, independent review, no signing access, and security escalation are mandatory.
