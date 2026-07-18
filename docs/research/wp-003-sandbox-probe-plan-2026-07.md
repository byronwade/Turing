# WP-003 Sandbox Probe Contract - July 2026

Status: no-claim implementation-planning contract
Owner: security, platform, architecture, quality, release, performance, and documentation-research
Related readiness: `PB-012`
Related task: `TASK-000004`
Related work package: `WP-003`
Related requirement: `REQ-SEC-001`
Inspected baseline: main after `WP-002` landed at `5f4eacd`
Research date: 2026-07-18

## Question

Can `WP-003` move from a sandbox-probe inventory into a stable operation catalog, evidence-bundle schema, and validator without implying a packaged sandbox harness, effective platform policy, sandbox readiness, renderer security, site isolation, hostile-browsing safety, `SEC-GATE-*` evidence, production safety, or implementation approval?

## Short Answer

Yes, for planning only. The versioned [`probe-catalog.json`](../../schemas/sandbox/probe-catalog.json), [`probe-evidence.schema.json`](../../schemas/sandbox/probe-evidence.schema.json), and [`validate_sandbox_contracts.py`](../../tools/validate_sandbox_contracts.py) now define the first stable no-claim operation and evidence contract that future executable sandbox work must replace with retained platform evidence.

This is not a working sandbox launcher, sandbox profile, platform adapter, packaged probe run, owner-reviewed sandbox readiness review, renderer-security proof, site-isolation proof, hostile-browsing safety claim, production-safety claim, or implementation claim.

## Current Inputs

- [Sandbox Probe Inventory](sandbox-probe-inventory-2026-07.md)
- [`sandbox-probe-inventory.json`](../security-engine/machine/sandbox-probe-inventory.json)
- [`sandbox-probe-package.schema.json`](../security-engine/machine/sandbox-probe-package.schema.json)
- [`no-claim-expected-deny-template.json`](../security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json)
- [`sandbox-readiness-review.schema.json`](../security-engine/machine/sandbox-readiness-review.schema.json)
- [`no-claim-sandbox-readiness-template.json`](../security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json)
- [`process-capabilities.json`](../blueprint-v1/machine/process-capabilities.json)
- [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json)
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [Security, Privacy, and Sandbox Model](../blueprint-v1/08-security-and-sandbox.md)
- [Sandbox Brokers and Platform Containment](../security-engine/02-sandbox-brokers-and-platform-containment.md)

## Contract

The catalog records 21 no-destructive-host operations:

- three unsandboxed or explicitly granted controls: assigned output write, assigned input read, and monotonic clock read;
- file probes for arbitrary read and write outside the assigned root;
- dynamic-code probe for untrusted library loading;
- socket probes for outbound connect, listening socket, and raw socket creation;
- process and debug probes for child creation, debug attach, cross-process memory read, and unexpected inherited handles;
- credential, clipboard, device, platform IPC, registry/preference, secret environment, unsafe working directory, and broker-disconnect probes.

An unsandboxed control run is mandatory. A harness that cannot observe allowed controls cannot prove denied operations.

The evidence schema requires build identity, platform family, architecture, OS/kernel/build, effective sandbox feature capture, sandbox-policy digest, process and broker identity, granted handles, environment allowlist, probe executable and catalog digests, redaction policy, per-probe results, enforcement source, durations, and summary counters.

Unsupported platform primitives are recorded as `unsupported` and never counted as a pass. Application-level stub denial is not enough; expected-deny probes must prove operating-system, broker, or launch-policy enforcement. Unexpected allows block readiness, and unexpected denials require review.

## Platform Staging

Linux laboratory work must record namespace, cgroup, `no_new_privs`, seccomp, Landlock, file-descriptor, environment, working-directory, resource-limit, and parent-death evidence. Seccomp alone is not a complete sandbox claim.

Windows laboratory work must record AppContainer or restricted-token shape, integrity level, job object limits, inherited handle state, process mitigations, dynamic-code/image-load/extension-point/child-process/win32k/CFG/CET behavior where applicable, brokered access, and effective token evidence.

macOS laboratory work must record App Sandbox or seatbelt shape, helper entitlement scope, code signature, hardened runtime, library validation, XPC peer identity, security-scoped access behavior, file-descriptor inheritance, environment, working directory, dynamic loader behavior, Apple Events, device, clipboard, and Mach-service exposure.

No strategy is approved by this plan. Each first platform adapter needs dependency, native-code, unsafe-code, FFI, license, fuzz, replacement, and owner-review evidence before it can become implementation work.

## Safe Probe Targets

Probe execution must use only probe-owned temporary files and directories, loopback-only listeners, inert sibling processes, isolated test clipboard sentinels where available, empty fake credential namespaces, harmless fake devices or unavailable dummy paths, local denied D-Bus/XPC/COM/RPC/named-pipe endpoints, synthetic environment sentinels, and dedicated probe-only preference or registry keys.

Raw-socket probes may attempt creation only and must not transmit external traffic. Credential, clipboard, profile, and page-content probes must never use real user data.

## Relationship To `TASK-000004`

`TASK-000004` remains proposed. It can start only after authority and IPC boundaries are reviewed or explicitly scoped out, the checked sandbox inventory and no-claim templates remain current, and an owner converts the proposed task into a reviewed execution manifest.

The next real proof must add executable packaged expected-deny probes for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater roles across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC access. It must also include effective platform-policy capture, host-safe fixtures, broker fixtures, compromised-client harnesses, platform matrix evidence, cleanup checks, and owner-reviewed sandbox readiness beyond the checked no-claim readiness-review template.

## Unsupported Claims

This contract does not support:

- `PB-012` readiness promotion;
- sandbox-readiness or platform-containment claims;
- renderer-security, site-isolation, or hostile-browsing safety claims;
- `SEC-GATE-1`, `SEC-GATE-6`, or other release-gate evidence;
- production-safety, preview, beta, stable, daily-driver, or support claims;
- implementation approval, task approval, platform adapter approval, or dependency approval.

## Validation

Run:

```bash
python3 -B tools/validate_sandbox_contracts.py
python3 -B tools/validate_sandbox_probe_inventory.py
python3 -B tools/validate_sandbox_readiness_review.py
python3 -B tools/validate_blueprint.py
```

The aggregate wrappers remain:

```bash
sh tools/check.sh
```

```powershell
.\tools\check.ps1
```
