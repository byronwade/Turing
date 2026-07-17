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

<!-- MARKET-STRATEGY-2026-07 -->
## Market-driven trust boundaries

Spaces, identity routing, migration, Time Machine, privacy receipts, sync, collaboration, Plug-ins, and agent mode each create security boundaries. Market demand cannot widen ambient authority or bypass trusted UI, data minimization, isolation, review, or incident obligations.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Trusted UI toolkit boundary

The native UI toolkit is privileged presentation infrastructure, not a policy authority. Toolkit callbacks emit typed commands; browser services revalidate identity, epoch, profile, permission, credential, Plug-in, and agent policy. Dynamic UI source loading, runtime interpreters, arbitrary scripts, generic kernel bridges, and page-controlled trusted overlays are prohibited in normal release builds.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Coding-agent threat surface

AI-assisted implementation is part of the supply-chain threat model. Repository content, build output, issues, tools, dependencies, and model responses are untrusted; task-scoped authority, provenance, independent review, no signing access, and security escalation are mandatory.
