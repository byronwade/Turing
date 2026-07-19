# Sandbox Probe Inventory - July 2026

Status: checked no-claim probe inventory, package template, and readiness-review template
Owner: security, platform, architecture, quality, and documentation-research
Related gate: `PB-012` Reference sandbox probe harness
Updated: 2026-07-18

## Question

Can `PB-012` move from prose requirements into checked planning evidence, a probe-package handoff template, and a readiness-review handoff template without implying that Turing has a packaged sandbox probe harness, effective OS sandbox evidence, owner-reviewed sandbox readiness, renderer security, site isolation, hostile-browsing safety, `SEC-GATE-1`, `SEC-GATE-6`, production safety, or implementation evidence?

## Short Answer

Yes, for planning only. The [`sandbox-probe-inventory.json`](../security-engine/machine/sandbox-probe-inventory.json) registry, [WP-003 Sandbox Probe Contract](wp-003-sandbox-probe-plan-2026-07.md), checked no-claim [`no-claim-expected-deny-template.json`](../security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), checked no-claim [`no-claim-sandbox-readiness-template.json`](../security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json), [`validate_sandbox_contracts.py`](../../tools/validate_sandbox_contracts.py), [`validate_sandbox_probe_inventory.py`](../../tools/validate_sandbox_probe_inventory.py), and [`validate_sandbox_readiness_review.py`](../../tools/validate_sandbox_readiness_review.py) make the expected-deny probe surface, operation catalog, evidence-bundle shape, future package handoff, and future owner-review handoff explicit for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater roles.

This is not a working sandbox harness, platform policy, packaged-build probe result, owner-reviewed sandbox readiness, renderer-security proof, site-isolation proof, hostile-browsing safety claim, production security claim, or implementation claim.

## Inputs

- [System Architecture](../blueprint-v1/04-system-architecture.md)
- [Security, Privacy, and Sandbox Model](../blueprint-v1/08-security-and-sandbox.md)
- [Testing, Compatibility, Fuzzing, and Quality Gates](../blueprint-v1/12-testing-compatibility.md)
- [Threat Model and Process Isolation](../security-engine/01-threat-model-and-process-isolation.md)
- [Sandbox Brokers and Platform Containment](../security-engine/02-sandbox-brokers-and-platform-containment.md)
- [Security Verification and Release Gates](../security-engine/06-security-verification-and-release-gates.md)
- [Native Platform and Browser Chrome](../platform/README.md)
- [`process-capabilities.json`](../blueprint-v1/machine/process-capabilities.json)
- [`sandbox-probe-inventory.schema.json`](../security-engine/machine/sandbox-probe-inventory.schema.json)
- [`sandbox-probe-inventory.json`](../security-engine/machine/sandbox-probe-inventory.json)
- [WP-003 Sandbox Probe Contract](wp-003-sandbox-probe-plan-2026-07.md)
- [Sandbox Platform-Evidence Decision Preparation](sandbox-platform-evidence-decision-prep-2026-07.md)
- [`probe-catalog.json`](../../schemas/sandbox/probe-catalog.json)
- [`probe-evidence.schema.json`](../../schemas/sandbox/probe-evidence.schema.json)
- [`sandbox-probe-package.schema.json`](../security-engine/machine/sandbox-probe-package.schema.json)
- [`no-claim-expected-deny-template.json`](../security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json)
- [`sandbox-readiness-review.schema.json`](../security-engine/machine/sandbox-readiness-review.schema.json)
- [`no-claim-sandbox-readiness-template.json`](../security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json)
- [`validate_sandbox_contracts.py`](../../tools/validate_sandbox_contracts.py)
- [`validate_sandbox_probe_inventory.py`](../../tools/validate_sandbox_probe_inventory.py)
- [`validate_sandbox_readiness_review.py`](../../tools/validate_sandbox_readiness_review.py)

## Current Evidence

The checked inventory records:

- the required probe roles: renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater;
- the current `process-capabilities.json` role that each probe target maps to, including decoder coverage through `media_utility`;
- the required hostile surfaces: file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC;
- macOS, Windows, and Linux evidence artifacts that a real harness must capture;
- blockers for packaged role launch, effective policy capture, result schema, host-safe execution, broker fixtures, compromised-client behavior, platform coverage, and owner review.

The checked probe-package template adds the handoff shape for the first future expected-deny package: template-only role targets, required access surfaces, platform-specific effective-policy artifacts, lifecycle stages, result-record fields, rejection rules, unsupported boundaries, and validation commands. Its package status fields are deliberately false for packaged harness execution, effective-policy capture, platform-matrix execution, and owner review.

The checked sandbox readiness-review template adds the handoff shape for the first future owner-reviewed sandbox readiness review. Its review fields are deliberately null, every readiness flag is false, and its axes require packaged role runners, effective platform policy, host-safe fixtures, broker fixtures, compromised-client harnesses, role/surface coverage, result records, failure denominator, cleanup, platform matrix evidence, and owner/security/platform/quality/release review beyond the checked no-claim sandbox readiness-review template.

The checked WP-003 contract adds a stable no-claim operation catalog and evidence-bundle schema for the first future executable package. It requires three allowed control probes, expected-deny operation records, unsupported-as-not-pass behavior, rejection of application-level stub denials as sandbox proof, redacted evidence, and `research_evidence_only` release-claim status.

The dated [Sandbox Platform-Evidence Decision Preparation](sandbox-platform-evidence-decision-prep-2026-07.md) records the platform-specific evidence differences for Windows, Linux, and macOS, including the rule that seccomp is not a complete sandbox and that Landlock ABI support must be captured explicitly.

## Missing Evidence

`PB-012` remains partial because the following are still missing:

- packaged expected-deny probes beyond the checked no-claim probe-package template using the same process launch path, handle set, sandbox policy, and mitigation flags as the evaluated configuration;
- real probe output that replaces the checked no-claim operation catalog and evidence schema with retained evidence, unsandboxed control runs, and redacted platform artifacts;
- owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template;
- per-platform effective policy capture for macOS, Windows, and Linux;
- a stable probe result schema and artifact package;
- host-safe temporary roots, fake credentials, fake profiles, bounded network fixtures, cleanup checks, and no destructive host behavior;
- broker fixtures that distinguish ambient authority from narrowly authorized behavior;
- compromised-client probes that forge IDs, origins, epochs, handles, paths, sizes, ordering, retries, and disconnected state;
- role-specific negative probe logs for file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC access;
- owner review before any sandbox, security, site-isolation, hostile-browsing, or production-safety claim.

## Decision

`PB-012` can move from `not_started` to `partial` because checked planning evidence, a no-claim package template, and a no-claim readiness-review template now exist. It cannot move to ready until executable packaged probes run from real process roles, capture effective platform policy plus negative results, and complete owner-reviewed sandbox readiness beyond the checked no-claim sandbox readiness-review template.

`TASK-000004` remains proposed. The inventory, package template, and readiness-review template give that task a starting point; they do not approve execution, satisfy `SEC-GATE-*`, provide owner-reviewed sandbox readiness, or weaken any sandbox gate.

## Unsupported Boundaries

The inventory explicitly keeps these outside the proof:

- no sandbox-readiness claim;
- no renderer-security claim;
- no site-isolation claim;
- no hostile-browsing safety claim;
- no platform containment claim;
- no owner-reviewed sandbox readiness claim;
- no `PB-012` readiness promotion;
- no packaged-build probe claim;
- no effective-policy claim;
- no `SEC-GATE-1` claim;
- no `SEC-GATE-6` claim;
- no production-safety claim.

## Next Proof Required

To advance `PB-012`, the next task should produce:

1. packaged role runner and launch manifests beyond the checked no-claim probe-package template for renderer, network, storage, GPU, decoder/media utility, extension host, DevTools, agent host, and updater;
2. a stable probe result schema with artifact hashes and cleanup status;
3. platform-specific effective policy capture for macOS, Windows, and Linux;
4. safe fake profile, fake credential, fake device, temporary filesystem, and loopback-only network fixtures;
5. brokered allowed-operation fixtures that distinguish narrow authorization from ambient authority;
6. negative probe logs for file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC surfaces;
7. compromised-client tests that forge identity, handles, epochs, paths, sizes, and ordering;
8. owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template;
9. security and platform owner review before any `SEC-GATE-1`, `SEC-GATE-6`, sandbox-readiness, site-isolation, hostile-browsing, production-safety, or implementation claim.

## Validation

Run:

```bash
python3 -B tools/validate_sandbox_contracts.py
python3 -B tools/validate_sandbox_probe_inventory.py
python3 -B tools/validate_sandbox_readiness_review.py
python3 -B tools/validate_blueprint.py
```

The aggregate Windows wrapper also runs the blueprint validator:

```powershell
.\tools\check.ps1
```
