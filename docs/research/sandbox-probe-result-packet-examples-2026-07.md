# Sandbox Probe Result Packet Examples - July 2026

Status: no-claim sample packet shape for `PB-012` and `TASK-000004`; no packaged probe, effective-policy, containment, or security-gate claim
Owner: security, platform, architecture, quality, release operations, and independent review
Research date: 2026-07-19

## Purpose

The [Sandbox Probe Execution and Containment Closure Preparation](sandbox-probe-execution-and-containment-closure-preparation-2026-07.md) defines the required evidence order, and the [Sandbox Platform-Evidence Decision Preparation](sandbox-platform-evidence-decision-prep-2026-07.md) defines platform-specific controls. This page gives a sample-only packet shape for one renderer role so a future probe run records effective policy, allowed controls, expected denials, compromised-client cases, unsupported primitives, and cleanup in one traceable unit.

All values below are fictitious placeholders. They do not describe a real Turing process, operating-system policy, executable, denial, or security result.

## Packet identity

```yaml
packet_status: sample_only_no_claim
packet_id: SANDBOX-SAMPLE-RENDERER-WINDOWS-0001
task_id: TASK-000004
source_commit: SAMPLE-COMMIT-REPLACE-BEFORE-USE
role: renderer
platform: windows-x64
os_build: SAMPLE-OS-BUILD
architecture: x86_64
executable_path: runner-owned-sample-path
executable_sha256: SAMPLE-EXECUTABLE-HASH
launch_path: same-role-runner-as-claimed-configuration
parent_process: SAMPLE-BROKER-IDENTITY
environment_allowlist_hash: SAMPLE-ENV-HASH
working_directory: runner-owned-temporary-root
policy_configuration_hash: SAMPLE-POLICY-HASH
fixture_root: runner-owned-temporary-root
fixture_policy: fake-profile-fake-credentials-loopback-only-no-real-user-data
```

## Effective-policy record

The runner must collect the policy after launch, not only the requested configuration. The same record shape applies to Windows, Linux, and macOS, with platform-specific fields preserved rather than flattened into an equivalence claim.

| Field | Sample placeholder | Required interpretation |
|---|---|---|
| Process identity | `SAMPLE-PID-EPOCH` | Identity of the launched claimed role, not a helper or test stub. |
| Parent and broker | `SAMPLE-PARENT-BROKER` | The actual parent, broker, endpoint, and authentication binding. |
| Effective policy | `SAMPLE-TOKEN-ENTITLEMENT-NAMESPACE-DIGEST` | OS-observed token, entitlement, namespace, mitigation, ruleset, or profile state. |
| Inherited authority | `SAMPLE-HANDLE-DESCRIPTOR-MANIFEST` | Handles, descriptors, environment, working directory, devices, and shared memory actually inherited. |
| Resource limits | `SAMPLE-LIMIT-MANIFEST` | Job/cgroup/rlimit/role limits and charge ownership. |
| Platform identity | `SAMPLE-OS-KERNEL-SIGNING-BUILD` | OS/kernel build, architecture, signature or package identity, and policy API versions. |

Requested policy, source configuration, or a policy name without this observed state is not an effective-policy result.

## Allowed-control and denial records

Each operation receives one record. The expected result is bound to the role, target, policy, and fixture; an unavailable operation is not automatically a denial.

```yaml
- operation_id: SAMPLE-ALLOWED-LOOPBACK-OUTPUT
  surface: socket
  principal: renderer:SAMPLE-PID-EPOCH
  target: loopback-fixture-only
  expected_result: allowed
  actual_result: sample_not_run
  status: not_run
  exit_code: null
  policy_layer: SAMPLE-POLICY-LAYER
  artifact_hashes: []
  cleanup_status: not_run

- operation_id: SAMPLE-DENY-OTHER-PROFILE-READ
  surface: profile
  principal: renderer:SAMPLE-PID-EPOCH
  target: fake-other-profile-root
  expected_result: denied_by_os_policy
  actual_result: sample_not_run
  status: not_run
  exit_code: null
  policy_layer: SAMPLE-POLICY-LAYER
  artifact_hashes: []
  cleanup_status: not_run

- operation_id: SAMPLE-DENY-CHILD-PROCESS
  surface: process
  principal: renderer:SAMPLE-PID-EPOCH
  target: fake-child-process
  expected_result: denied_by_os_policy
  actual_result: sample_not_run
  status: not_run
  exit_code: null
  policy_layer: SAMPLE-POLICY-LAYER
  artifact_hashes: []
  cleanup_status: not_run
```

The actual record must distinguish at least `pass`, `unexpected_allow`, `unexpected_deny`, `unsupported`, `not_run`, `timeout`, `crash`, and `harness_error`. `unsupported` and `not_run` remain unresolved evidence; neither is a passing denial.

## Hostile-client and lifecycle records

The packet must include malformed and lifecycle cases using fake identifiers and bounded fixtures:

| Case | Required fields | Sample status |
|---|---|---|
| Forged identity or epoch | submitted identity, trusted identity, decision, artifact hash | `sample_not_run` |
| Forged path or handle | submitted target, re-derived target, broker decision, cleanup | `sample_not_run` |
| Oversized or reordered request | size/order, limit, rejection, queue charge release | `sample_not_run` |
| Broker disconnect | process state, pending authority, terminal result, cleanup | `sample_not_run` |
| Process crash/restart | old epoch, new epoch, stale replay result, fixture cleanup | `sample_not_run` |
| Timeout/cancellation | deadline, cancellation owner, terminal outcome, resource release | `sample_not_run` |

## Platform minimums

Use separate platform records; do not turn missing platform primitives into a cross-platform pass.

| Platform | Effective artifacts required in the packet |
|---|---|
| Windows | Token/integrity/AppContainer or restricted identity, capabilities, package identity assumptions, job limits, child-process and dynamic-code/image-load mitigations, Win32k or equivalent policy, inherited-handle manifest, broker endpoints |
| Linux | Kernel/build, user/PID/mount/network/IPC namespace map, capabilities and `no_new_privs`, seccomp disposition, Landlock ABI/ruleset where used, mount view, cgroups/rlimits, broker descriptors |
| macOS | OS/build, code-signing identity, entitlements, App Sandbox/seatbelt profile, hardened runtime and library validation, JIT policy, XPC/Mach-service identity, inherited descriptors, broker extensions |

The matrix records platform differences and unsupported rows. It does not assert equivalent security between operating systems.

## Packet completion and rejection

Before review, the packet must contain redacted stdout/stderr, policy artifacts, operation results, raw trace references where needed, artifact hashes, complete setup/control/deny/hostile/lifecycle denominator, and fixture cleanup evidence. Reject the packet when:

- a helper, mock, application preflight, or missing fixture substitutes for the claimed role;
- effective policy is inferred from requested configuration;
- an unavailable or unsupported primitive is recorded as a denial pass;
- a failure, timeout, crash, skipped probe, or cleanup leak is omitted from the denominator;
- real profiles, credentials, secrets, devices, public network endpoints, or destructive host paths are used;
- a broker trusts client-supplied identity, origin, path, handle, epoch, or capability without re-derivation;
- a template, passing validator, screenshot, or single denial is cited as sandbox readiness.

The next acceptable artifact is a reviewed immutable `TASK-000004` package for one role and one platform. It must replace sample fields with retained evidence and named review; it must not generalize beyond its executed matrix.

## Claim boundary

This page is sample-only documentation. It does not establish sandbox containment, renderer security, site isolation, hostile-browsing safety, platform equivalence, `SEC-GATE-1`, `SEC-GATE-6`, production safety, Chrome-class security, or implementation readiness.
