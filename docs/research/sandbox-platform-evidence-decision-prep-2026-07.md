# Sandbox Platform-Evidence Decision Preparation - July 2026

Status: no-claim `PB-012` platform-evidence research; no sandbox policy, platform adapter, or security gate is approved
Owner: security, platform, architecture, quality, release, and documentation-research
Related gate: `PB-012` Reference sandbox probe harness
Research date: 2026-07-20

Freshness note: on 2026-07-20 the checked platform-source manifest and all four sandbox validators were re-run from the repository checkout. This revalidates document identity and no-claim contract alignment only; it is not effective-policy capture or containment evidence.

## Question

What platform-specific facts must be captured before Turing can compare sandbox behavior across Windows, Linux, and macOS without treating a source policy, a failed launch, or one primitive as proof of containment?

## Sources checked

- Microsoft [AppContainer isolation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation).
- Microsoft [Create Process In Sandbox APIs](https://learn.microsoft.com/en-us/windows/win32/secauthz/createprocessinsandbox).
- Microsoft [process mitigation policy](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy).
- Linux kernel [Seccomp BPF](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html).
- Linux kernel [Landlock](https://www.kernel.org/doc/html/latest/userspace-api/landlock.html).
- Linux kernel [user namespaces and resource control](https://docs.kernel.org/admin-guide/namespaces/resource-control.html).
- Apple [Hardened Runtime](https://developer.apple.com/documentation/security/hardened-runtime).
- Turing [Sandbox Brokers and Platform Containment](../security-engine/02-sandbox-brokers-and-platform-containment.md), [Sandbox Probe Inventory](sandbox-probe-inventory-2026-07.md), and [WP-003 Sandbox Probe Contract](wp-003-sandbox-probe-plan-2026-07.md).

These sources document platform mechanisms and limitations. They do not prove a Turing role is contained, and they do not replace packaged probes, effective-policy capture, or owner review.

The checked [sandbox platform-source manifest](../security-engine/machine/sandbox-platform-source-manifest.json), validated by [`validate_sandbox_platform_sources.py`](../../tools/validate_sandbox_platform_sources.py), is the machine identity record for these observations. It tracks source identity and evidence axes only; it does not make any source an effective policy artifact or Turing result.

## Findings that affect Turing's evidence contract

- Windows AppContainer is a least-privilege execution environment that can isolate file, registry, network, process, device, credential, and window access, with selected resources granted or brokered. A Turing result must record the effective identity, token/capabilities, inherited handles, job limits, mitigations, package-identity assumptions, and broker behavior; naming AppContainer alone is insufficient.
- Windows process mitigations are a separate policy surface. Dynamic-code, child-process, image-load, control-flow, win32k, CFG/CET, and related settings must be captured as effective process policy and tested for the selected role. A mitigation that prevents launch is not a passing deny probe.
- The Windows sandbox-launch specification exposes separate AppContainer, integrity, capability, filesystem, network, UI-restriction, and mitigation controls, and documents that several controls are ineffective when AppContainer is disabled. Turing must capture the effective launch mode and reject configurations that record requested restrictions without proving the underlying isolation mode was enabled; the API documentation itself is not evidence that a Turing process is contained.
- Linux seccomp filters reduce the exposed system-call surface, but the kernel documentation explicitly states that syscall filtering is not a complete sandbox. Turing must combine it with the selected namespace, privilege, filesystem, resource, descriptor, and broker controls and report each layer independently.
- Linux Landlock lets an unprivileged process restrict its own ambient rights and supports filesystem and, depending on ABI, network rules. The available ABI and handled access rights vary by kernel. The probe record must capture the detected ABI, handled rights, ignored/unsupported rights, ruleset digest, and the result of each expected-deny operation rather than treating best-effort application as equivalent to a fixed policy.
- Linux kernel guidance warns that user namespaces can expose systems to resource misuse and recommends memory control groups when they are enabled. A Turing Linux probe must therefore capture namespace limits and cgroup/resource-control state alongside privilege and filesystem policy; namespace creation alone is not a bounded-resource or containment result.
- macOS evidence must bind App Sandbox or seatbelt configuration, entitlements, code signature, hardened-runtime state, library validation, JIT policy, XPC/Mach-service identity, inherited descriptors, and broker behavior to the exact executable and OS build. Entitlement presence is not proof that the effective process cannot reach an unapproved resource.
- Across all platforms, the same role must run allowed-control probes and expected-deny probes from the same launch path and package configuration. Unsupported primitives are recorded as `unsupported`, never as `pass`; launch failure, application-level stubs, or an absent fixture cannot be counted as denial evidence.

## Cross-platform evidence matrix

| Evidence axis | Windows | Linux | macOS |
|---|---|---|---|
| Identity and launch | token, integrity level, AppContainer/capabilities, package identity, sandbox-launch mode, parent and child process IDs | uid/gid, user namespace, PID namespace, parent-death policy, capabilities, process IDs | code-signing identity, entitlements, sandbox profile, audit/process identity, XPC peer identity |
| Filesystem and profile | AppContainer file grants, broker paths, registry keys, inherited handles | mount/root view, Landlock ABI/ruleset, open descriptors, broker paths | sandbox container, security-scoped access, seatbelt profile, inherited descriptors |
| Network and IPC | network capability, COM/RPC/named-pipe exposure, broker endpoints | network namespace, seccomp rules, Landlock network ABI, Unix sockets, broker descriptors | XPC/Mach services, network entitlement/policy, inherited descriptors, broker endpoints |
| Process and code loading | job object, child-process and dynamic-code/image-load mitigations, debugger access | seccomp actions, `no_new_privs`, ptrace restrictions, namespace transitions | hardened runtime, library validation, JIT policy, debugger/task-port access |
| Resource controls | job limits, handle allowlist, memory/CPU limits | cgroups, namespace limits, rlimits, namespaces, descriptor limits | role-specific limits, launch constraints, descriptor and helper limits |
| Effective-policy artifact | OS/build, executable hash, token/capability dump, mitigation query, policy digest | kernel/build, detected ABI, namespace/cgroup/rlimit state, seccomp and Landlock artifacts, policy digest | OS/build, signature/hash, entitlements, hardened-runtime/library-validation state, profile/policy digest |

The rows are evidence requirements, not a claim that the platforms offer equivalent primitives. A cross-platform readiness review must preserve those differences and identify the narrowest supported role and platform rather than averaging them away.

## Probe and review gates

Before a platform can contribute to `PB-012` readiness, the package must prove:

1. The exact executable, launch command, parent, environment allowlist, working directory, package identity, and policy/configuration hashes.
2. Effective policy capture after launch, including kernel/OS/build, architecture, mitigation or ruleset state, inherited handles/descriptors, and broker identity.
3. Allowed-control probes that demonstrate the harness can observe a permitted operation.
4. Expected-deny probes for file, socket, process, debug, credential, device, shared-memory, profile, and IPC surfaces appropriate to the role.
5. A separate unsandboxed control where safe, so an absent capability is not confused with a broken probe.
6. Malformed and compromised-client cases that forge process IDs, origins, epochs, handles, paths, lengths, ordering, retries, and disconnect state.
7. Cleanup and host-safety evidence proving temporary roots, fake credentials, loopback-only endpoints, and probe-owned fixtures were removed without touching real user data.
8. Explicit `unsupported`, `not-run`, `unexpected-allow`, `unexpected-deny`, crash, timeout, and harness-error accounting.
9. Platform owner, security owner, quality owner, and release-operations review before any `SEC-GATE-1`, `SEC-GATE-6`, sandbox, renderer-security, site-isolation, hostile-browsing, or production-safety claim.

## Current conclusion

`PB-012` remains `partial` and `TASK-000004` remains proposed. This report sharpens platform evidence and degradation rules but does not select a sandbox strategy, approve a platform adapter, provide effective-policy artifacts, or promote any security gate. The existing probe catalog, package template, and readiness-review template remain the controlling no-claim records until executable packaged probes and owner-reviewed evidence exist.

## Required registry impact

This report strengthens the documented research evidence for `PB-012`, `WP-003`, and `TASK-000004`. It does not change readiness status or support sandbox, renderer-security, site-isolation, hostile-browsing, production-safety, or implementation claims.
