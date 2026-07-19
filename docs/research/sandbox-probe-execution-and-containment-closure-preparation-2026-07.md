# Sandbox Probe Execution and Containment Closure Preparation - July 2026

Status: no-claim execution and review route for `PB-012`, `WP-003`, and `TASK-000004`; no packaged probe run, effective policy result, or sandbox readiness has been accepted
Owner: security, platform, architecture, quality, release, and independent review
Research date: 2026-07-19

## Question

What evidence order can turn the checked `WP-003` operation catalog and probe-package template into reviewable platform containment evidence without mistaking an application stub, a policy name, or one successful denial for a sandbox?

## Current boundary

The repository has a checked sandbox-probe inventory, a stable no-claim operation/evidence contract, platform-evidence decision preparation, a no-claim probe-package template, and a no-claim readiness-review template. These records define the future work. They do not launch a constrained process, capture effective operating-system policy, prove containment, satisfy `SEC-GATE-1` or `SEC-GATE-6`, or support renderer-security, site-isolation, hostile-browsing, production-safety, or implementation claims.

## Primary platform-source observations

The following official platform documentation was retrieved on 2026-07-19 and is used to constrain the evidence interpretation:

| Platform source | Observation | Required probe/evidence consequence |
|---|---|---|
| [Windows AppContainer isolation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation) | AppContainer isolates process, file, registry, network, device, credential, and window access through least-privilege capabilities and brokered access. | Capture the effective token, package/capability identity, integrity level, ACLs, broker path, and granted resource set for the exact packaged process. A requested capability list is not effective-policy proof. |
| [Apple App Sandbox](https://developer.apple.com/documentation/security/app-sandbox) | macOS App Sandbox limits system-resource and user-data access through entitlements; the entitlement profile is part of the security boundary. | Capture the signed binary identity, entitlement set, container/profile state, broker/helper relationship, and degraded or unavailable entitlement behavior. Do not transfer Windows or Linux results to macOS. |
| [Linux seccomp](https://docs.kernel.org/userspace-api/seccomp_filter.html) | The Linux kernel documentation explicitly describes seccomp system-call filtering as a tool for sandbox developers, not a complete sandbox; logical behavior and information flow require other controls. | Record seccomp mode, filter hash, architecture checks, no-new-privileges state, namespaces/filesystem policy, broker rules, and residual surfaces. A passing syscall-deny test alone cannot satisfy `PB-012`. |
| [Linux Landlock](https://docs.kernel.org/userspace-api/landlock.html) | Landlock is an additional, stackable restriction layer; filesystem and network rights depend on the running kernel and ABI, which must be detected rather than assumed. | Capture kernel identity, Landlock availability, ABI version, requested and effective rulesets, filesystem/network rights, and unsupported/degraded behavior. Results must be labeled by ABI and kernel configuration. |

These observations are method and interpretation constraints, not sandbox results. They require each future package to retain platform-specific effective-state evidence and prevent a single primitive or platform result from being reported as cross-platform containment.

The probe must evaluate the same process role, executable, launch path, inherited handles/descriptors, broker configuration, mitigation policy, resource limits, and profile used by the claimed configuration. A standalone helper with different authority is diagnostic only.

## Required evidence order

1. **Freeze role and authority scope.** Bind each probe package to one declared role (`renderer`, `network`, `storage`, `GPU`, `decoder/media utility`, `extension host`, `DevTools`, `agent host`, or `updater`), process identity, capability set, parent/broker, executable hash, launch arguments, environment, profile, and platform policy. Page content, extension input, agent output, and model observations cannot alter this scope.
2. **Prepare host-safe fixtures.** Use temporary roots, fake credentials, fake profiles, fake devices, bounded loopback-only network fixtures, non-sensitive registry/preferences, explicit output roots, cleanup checks, and a no-destructive-host policy. Record fixture hashes and before/after host state.
3. **Run unsandboxed and allowed controls.** Verify that the harness can observe assigned input, assigned output, and the declared monotonic clock or other explicitly granted controls. A harness that cannot distinguish an allowed control from an unavailable operation cannot establish an expected denial.
4. **Launch the real constrained role.** Capture the exact OS build, executable and signature/hash, policy/profile/entitlement/token/mitigation state, inherited handles/descriptors, broker identity, namespaces or job limits, network/device rules, and resource limits. A policy name or configuration file without effective-state capture is not proof.
5. **Run expected-deny operations.** Cover file, socket, process, registry/preferences, device, shared-memory, credential, debug, profile, IPC, dynamic-code, secret-environment, working-directory, and broker-disconnect surfaces. Record operation identity, principal, target, expected result, actual result, error/status, policy layer, timestamp, artifact hash, and cleanup outcome.
6. **Run compromised-client and lifecycle cases.** Forge IDs, origins, epochs, handles, paths, sizes, ordering, retries, inherited descriptors, disconnects, and stale state. Exercise process crash, broker crash, timeout, cancellation, restart, cleanup, and resource exhaustion. Unsupported platform primitives are `not_pass`, not implicit success.
7. **Compare platforms explicitly.** Capture distinct Windows, Linux, and macOS policy mechanisms and limitations. A missing primitive, weaker fallback, or different broker path becomes an explicit unsupported row or time-bounded waiver; it does not disappear into a cross-platform pass.
8. **Review the complete denominator.** Include setup, launch, control, expected-deny, compromised-client, retry, failure, cleanup, and skipped operations. Preserve raw redacted logs, policy artifacts, screenshots or traces where needed, SHA-256 manifests, failure classification, and host cleanup evidence.
9. **Submit readiness review.** Replace the no-claim template with exact source commit, package IDs, executable/policy hashes, platform matrix, artifact manifest, failures/waivers, named security/platform/quality/release reviewers, and a claim-by-claim disposition.

## Evidence matrix

| Axis | Minimum proof | Rejection condition |
|---|---|---|
| Role identity | Exact executable, parent/broker, role, capability set, launch path, arguments, environment, and process identity | Helper or demo process is substituted for the claimed role |
| Effective policy | OS-observed token/entitlement/mitigation/namespace/job/descriptor/device/network state tied to the executable | Only a config file, policy name, or requested setting is recorded |
| Allowed controls | Assigned input/output and declared safe controls succeed in the constrained harness | Harness cannot distinguish allowed behavior from unavailable behavior |
| Expected denial | Real OS-enforced denial records across every declared surface, with unsandboxed controls | Application-level stub, preflight refusal, or missing operation is counted as containment |
| Broker authority | Narrow broker operation, caller identity, target validation, audit result, and disconnect behavior | Broker accepts caller-supplied identity, path, origin, handle, or capability without validation |
| Hostile client | Forged identity/epoch/handle/path/size/order/retry and stale/disconnected cases are rejected | Only cooperative clients or success-path probes are tested |
| Lifecycle/resources | Crash, restart, timeout, cancellation, cleanup, limits, and exhaustion evidence | Failed probes leak handles, roots, authority, or resource charges |
| Platform matrix | Windows, Linux, and macOS results or explicit unsupported/waiver records | One platform result is generalized to all platforms |
| Evidence integrity | Redacted logs, hashes, source/policy identity, full denominator, and named review | Template, passing validator, or one screenshot is treated as readiness |

## Gate and claim effect

`PB-012` remains `partial`. The next useful proof is a reviewed `TASK-000004` package that produces retained expected-deny and control results from real constrained roles. No package template, operation catalog, application denial, platform API description, or passing validator promotes `PB-012`, satisfies a security gate, or supports sandbox, renderer-security, site-isolation, hostile-browsing, production-safety, or Chrome-class claims.

The route is compatible with the [Sandbox Probe Inventory](sandbox-probe-inventory-2026-07.md), [WP-003 Sandbox Probe Contract](wp-003-sandbox-probe-plan-2026-07.md), [Sandbox Platform-Evidence Decision Preparation](sandbox-platform-evidence-decision-prep-2026-07.md), and specified [TASK-000004 manifest](../agent-execution/machine/tasks/TASK-000004.json). Those sources remain authoritative for their respective scopes.

The [Sandbox Probe Result Packet Examples](sandbox-probe-result-packet-examples-2026-07.md) supplies a fictitious renderer packet shape for effective-policy, allowed-control, expected-deny, hostile-client, lifecycle, platform, denominator, and cleanup records. It is a handoff example only and does not satisfy any execution or readiness requirement.

Any future `PB-012` decision must also be reconciled through the [PB-020 owner-decision closure board](../project-buildout/23-owner-decision-closure-board.md) and [build-readiness closure preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md). Sandbox acceptance cannot independently authorize site isolation, hostile-browsing safety, release, production, or Chrome-class claims.

## Next controlled action

Prepare a reviewed immutable `TASK-000004` package for one platform and one role, with safe fixtures and an explicit unsandboxed control. Do not generalize its result to other roles or platforms until the declared matrix and owner-reviewed readiness review are complete.
