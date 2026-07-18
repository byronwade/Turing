# Security Verification and Release Gates

Status: research and design baseline  
Owner: security assurance  
Purpose: Define continuous adversarial testing, evidence bundles, severity, waivers, and maturity gates.

## Relationship to the Turing program

This document operationalizes SEC-GATE-1 through SEC-GATE-8 in [Blueprint 08](../blueprint-v1/08-security-and-sandbox.md) and the release evidence model in [Blueprint 12](../blueprint-v1/12-testing-compatibility.md).

## Verification layers

Security evidence includes unit and property tests, schema validation, compromised-process integration tests, sandbox probes, web-security conformance, fuzzing, sanitizers, model checking, fault injection, static analysis, dependency review, binary hardening inspection, red-team exercises, and independent audits. No single layer is treated as proof.

Tests run against the same packaged roles, policies, and mitigations used by the claimed release configuration.

## Compromised-principal harnesses

Harnesses emulate arbitrary renderer, extension, DevTools, agent, decoder, network, storage, and GPU process behavior. They forge IDs, origins, epochs, handles, sizes, paths, ordering, retries, disconnections, races, and resource exhaustion against every privileged interface.

The expected result is deny, bounded failure, revoked session, or narrowly authorized effect with an auditable reason.

## Fuzzing program

Continuous fuzzing covers parsers, protocols, state machines, IPC, caches, storage, update metadata, JIT/GC, graphics, codecs, extensions, DevTools, agent actions, and redaction. Corpora use grammar-aware generation, dictionaries, crossover, coverage, randomized scheduling, OOM, timeouts, cancellation, and minimization.

Crashes are classified by root cause and reachable privilege. Potentially exploitable artifacts remain private.

## Release evidence bundle

Each release candidate includes process/capability manifests, effective sandbox evidence, site-isolation tests, web-policy conformance, unsafe/native dependency inventories, fuzz status, sanitizer results, update tests, binary hardening flags, supported feature/security statement, known residual risks, security contact, and independent review status.

Evidence is tied to the exact artifact hash and cannot be borrowed from another configuration.

## Severity and waiver policy

Security failures receive severity based on assets, boundary crossed, attacker control, prerequisites, default reachability, persistence, and user impact. A test waiver records issue, owner, rationale, affected configurations, compensating controls, expiry, and release decision. Sandbox escapes, cross-profile leaks, update bypass, credential disclosure, and unauthorized high-risk agent actions cannot be waived for stable release.

Flaky security tests are failures until root cause is known; retries do not convert them to passing evidence.

## Maturity gates

Research builds may lack containment and are marked unsafe. Engine preview requires explicit unsupported security boundaries and no sensitive-use claim. Developer preview requires platform sandbox evidence, site isolation for supported paths, signed updates, private response, fuzzing, and crash recovery. Beta requires sustained conformance, hardening, patch drills, and broader review. Stable requires independent audit, supported-version policy, rapid updates, and closure or explicit acceptance of release-critical findings.

## Metrics and transparency

Track security-test inventory, fuzzing CPU time and coverage proxies, unique root causes, time to triage, patch latency, unsafe/native surface, dependency age, sandbox negative-test coverage, process/capability changes, and open high-severity findings. Metrics are interpreted; raw volume is not equated with safety.

## Non-negotiable invariants

- Security evidence is configuration- and artifact-specific.
- Compromised-process tests cover every privileged interface.
- Critical boundaries cannot be waived into a stable release.
- Flaky or skipped security tests remain visible and owned.
- Potential exploits use confidential handling and coordinated disclosure.
- A release maturity label is determined by gates, not visual completeness or schedule.

## Required evidence

- Automated evidence bundle generated from the release artifact.
- Continuous fuzzing and sanitizer results with retained minimized corpora.
- Platform sandbox and site-isolation negative tests.
- Red-team and independent-audit findings tracked to closure.
- Emergency patch, signing, update, rollback, and incident tabletop drills.
- Published residual-risk and unsupported-security map.

The checked [Sandbox Probe Inventory](../research/sandbox-probe-inventory-2026-07.md) and checked no-claim [sandbox probe-package template](machine/sandbox-probe-packages/no-claim-expected-deny-template.json) are current no-claim `PB-012` planning evidence for role targets, access surfaces, package handoff fields, platform evidence requirements, host-safety requirements, and blocker records. They do not satisfy SEC-GATE-1, SEC-GATE-6, sandbox readiness, site-isolation, hostile-browsing safety, or release evidence until packaged probes run against the effective platform policies for the claimed artifacts.

The checked [Incident Patch Rehearsal Inventory](../research/incident-patch-rehearsal-inventory-2026-07.md), checked no-claim [incident patch rehearsal template](machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), and checked no-claim [incident/patch readiness-review template](machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json) are current `PB-018` planning evidence for private intake, emergency patch, incident-class, role, timing, escalation, secret-rotation, fixture-policy, lifecycle, rejection-rule, owner-review handoff, and unsupported-boundary terms. They do not satisfy the emergency patch, incident tabletop, owner-reviewed incident/patch readiness, supported-security, stable-release, implementation, or production-safe browsing gates until actual tabletop, dry-run, and owner-review evidence exists beyond the templates.

## Known risks and unresolved questions

- Coverage metrics can create false confidence without attacker-oriented review.
- Audit findings can outpace available remediation capacity.
- Evidence collection can drift from release configuration.
- Security transparency must avoid publishing exploit-enabling details before users are protected.

## Primary sources

- Web Platform Tests — https://web-platform-tests.org/
- Rust Fuzz Book — https://rust-fuzz.github.io/book/
- Chromium sandbox design — https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
