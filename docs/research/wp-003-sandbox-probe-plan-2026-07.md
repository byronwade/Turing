# WP-003 Renderer Sandbox Probe Plan — July 2026

Status: implementation-planning research; no effective sandbox or platform-support claim  
Owner: security, architecture, platform, quality, release, performance, and documentation  
Related task: `TASK-000002`  
Related work package: `WP-003`  
Related requirement: `REQ-SEC-001`  
Inspected baseline: `main` at `301256ae6ddead1fe7ea376782bb79e81fb01258`  
Research date: 2026-07-17

## Executive decision

Turing must test the restrictions that the operating system actually enforces, not infer safety from an entitlement file, token request, namespace setup, seccomp source, or intended policy.

The sandbox program will therefore be built around three distinct artifacts:

1. a versioned operation catalog defining allowed and denied probes;
2. a platform launcher that applies the intended restrictions and grants only enumerated handles;
3. a probe child that attempts operations and emits redacted evidence through one launcher-provided channel.

An unsandboxed control run is mandatory. A harness that always reports denial can otherwise pass without testing the operating-system boundary.

`WP-003` remains unimplemented. This plan does not choose a supported desktop platform, approve an FFI or native dependency, or claim that any renderer process is currently sandboxed.

## Dependency boundary

Sandbox implementation begins only after:

- `TASK-000001` receives independent acceptance and `WP-002` is merged;
- the launcher can bind a real child identity and evidence channel to the kernel process registry;
- each native or unsafe boundary has a ledger entry, owner, review, fuzz or negative-test plan, and replacement boundary;
- the first platform is explicitly labeled a research laboratory rather than a product-support promise.

Planning, schemas, fixture design, and harmless unsandboxed controls may proceed before those gates.

## Why effective probing is necessary

A browser renderer processes hostile input. Configuration intent is insufficient because capability can leak through:

- inherited file descriptors or handles;
- environment variables and working directories;
- broad entitlements or AppContainer capabilities;
- platform services reachable over ambient IPC;
- dynamic library search paths;
- namespace or Landlock features missing from the running kernel;
- seccomp filters applied too late or to the wrong thread;
- process mitigations applied after images are loaded;
- broker methods that are broader than the renderer role requires;
- test environments whose host ACLs deny an operation even when the sandbox does not.

Every evidence record therefore identifies the enforcement source. A denial caused only by an ordinary host ACL is not evidence that the Turing sandbox policy denied the operation.

## Canonical contracts

### Probe catalog

[`schemas/sandbox/probe-catalog.json`](../../schemas/sandbox/probe-catalog.json) defines:

- stable probe IDs;
- platform applicability;
- sandbox and unsandboxed-control expectations;
- safe harness-owned targets;
- allowed and denied operation classes;
- result values;
- rules preventing unsupported or application-stub behavior from counting as a pass.

The initial catalog includes controls plus filesystem, code-loading, network, process, debugger, cross-process-memory, credential, clipboard, device, platform-IPC, configuration, inherited-handle, environment, working-directory, and broker-disconnect probes.

### Evidence schema

[`schemas/sandbox/probe-evidence.schema.json`](../../schemas/sandbox/probe-evidence.schema.json) binds each run to:

- source commit and build identity;
- maturity and build profile;
- operating-system family, version, architecture, and kernel or build;
- detected sandbox primitives and their versions;
- policy ID, version, digest, role, and explicit grants;
- broker and child process identities;
- granted handles and environment allowlist;
- probe executable and catalog digests;
- expected and actual result;
- enforcement source;
- platform status code or terminating signal;
- timing;
- redaction policy;
- unexpected allows, unexpected denials, and unsupported operations.

Evidence is research-only until the owning release gate is deliberately promoted.

## Common architecture

```text
browser kernel policy oracle
        │
        │ typed launch request and attenuated role
        ▼
platform sandbox launcher
        │
        ├── creates process identity and OS sandbox
        ├── closes every non-allowlisted handle
        ├── supplies synthetic fixtures and one evidence channel
        └── records policy and platform identity
        ▼
renderer-class probe child
        │
        ├── runs allowed controls
        ├── attempts denied operations
        ├── never targets real user data or external systems
        └── emits bounded redacted results
        ▼
evidence verifier
        │
        ├── validates schema and digests
        ├── distinguishes OS, broker, ACL, stub, and unsupported results
        ├── compares against the catalog
        └── fails on unexplained capability growth
```

The probe child does not decide that it is secure. The launcher and verifier independently establish the environment, expected policy, and interpretation.

## Staged implementation

### Stage 0 — Contract and unsandboxed control

Deliverables:

- schema validation;
- deterministic catalog digest;
- probe runner with no sandbox applied;
- harness-owned filesystem, loopback, process, IPC, clipboard, device, and credential fixtures where available;
- evidence redaction tests;
- proof that expected-deny probes are allowed in the control environment when host policy permits;
- explicit classification when host ACLs or unavailable services prevent a meaningful control.

The unsandboxed control must never be installed or described as a browser renderer.

### Stage 1 — Linux research laboratory

The Linux launcher should layer mechanisms instead of treating one feature as the sandbox:

- a new user namespace where supported and policy permits it;
- mount, PID, IPC, UTS, cgroup, and network namespaces as justified;
- an empty or minimal filesystem view with read-only runtime inputs;
- `PR_SET_NO_NEW_PRIVS` before filters or self-restriction;
- a seccomp filter reducing the system-call surface;
- Landlock for additional filesystem and supported network restrictions after runtime ABI detection;
- closed inherited file descriptors except the explicit evidence and fixture handles;
- cleared environment and safe working directory;
- resource limits, cgroup placement, and process-count controls;
- parent-death and broker-disconnect behavior;
- no setuid helper in the default design.

Linux kernel documentation explicitly describes seccomp as a system-call filtering mechanism rather than a complete sandbox. It must be combined with other isolation and information-flow controls. The filter must validate the syscall architecture as well as the number. `no_new_privs` is irreversible and prevents a later `execve` from granting privileges that were unavailable before execution.

Landlock is a stackable Linux Security Module that allows unprivileged processes to restrict ambient rights. The launcher must query the Landlock ABI at runtime and report unsupported handled rights rather than silently assuming the newest kernel behavior. A system without enabled Landlock may still run a separate namespace/seccomp experiment, but it cannot count as complete Linux sandbox evidence.

The initial Linux CI target may use Ubuntu 24.04 on `x86_64-unknown-linux-gnu` because that is the M0 build environment. This is a laboratory selection, not a stable platform commitment.

### Stage 2 — Windows research laboratory

The Windows launcher should evaluate:

- an AppContainer profile and minimal capability SID set;
- low-integrity and token details where relevant to the chosen model;
- a job object with process, memory, lifetime, and UI limits;
- explicit inherited-handle allowlisting;
- process mitigation policies applied before or during initialization;
- dynamic-code, image-load, extension-point, child-process, win32k, CFG, CET, and related mitigations as available;
- network capability separation;
- brokered file, device, clipboard, credential, and registry access;
- package and unpackaged distribution constraints;
- evidence of the effective token, capabilities, job, mitigations, and reachable resources.

Microsoft documents AppContainer as a least-privilege isolation environment covering credentials, devices, files and registry, network, processes, and windows. The probe must test each relevant boundary instead of merely checking for an AppContainer SID. Microsoft also recommends applying process mitigations before or during initialization; some protections cannot be made fully effective after images are loaded.

The project must compare classic AppContainer, newer Win32 app isolation where available, and the browser's packaging requirements. No Windows model is accepted by this plan.

### Stage 3 — macOS research laboratory

The macOS launcher should evaluate:

- App Sandbox on each executable target or helper rather than only the main app;
- the narrowest entitlements per role;
- code-signature and entitlement verification;
- Hardened Runtime with the minimum exceptions;
- XPC or other broker channels with authenticated peer identity;
- security-scoped access only through explicit user or broker grants;
- inherited descriptor, environment, working-directory, dynamic-loader, Apple Events, device, clipboard, and file-access probes;
- distribution differences between development, Developer ID, notarization, and App Store packaging;
- evidence from both codesigning metadata and attempted operations.

Apple documents App Sandbox as limiting access to files, network connections, hardware capabilities, and other protected resources through entitlements. Embedded tools and helper targets require deliberate sandbox configuration. Apple also documents Hardened Runtime as system-enforced runtime restrictions; broad exceptions such as disabling library validation or executable-memory protection remove important barriers and require explicit review.

A valid code signature and entitlement listing are evidence inputs, not substitutes for negative capability probes.

## Probe target safety

The harness must never probe real user data or production services.

Use only:

- temporary files and directories created by the runner;
- loopback listeners created by the runner;
- inert sibling processes owned by the runner;
- isolated test-session clipboard contents;
- empty test credential namespaces;
- virtual or harmless test devices;
- local D-Bus, XPC, COM, RPC, or named-pipe endpoints created by the runner;
- synthetic environment sentinels;
- dedicated external preference domains or registry keys created for the test.

Raw-socket probes create no transmitted traffic. Debug and cross-process-memory probes target only harness-owned children.

## Result semantics

- `allowed`: the operation crossed the target boundary successfully.
- `denied`: the operating system or authenticated broker rejected it.
- `killed`: the sandbox terminated the process because of the attempt.
- `brokered`: an explicitly allowed broker action completed.
- `unsupported`: the platform or kernel lacks the required primitive.
- `not_attempted`: prerequisites for a safe attempt were absent.
- `error`: the harness could not determine the security result.

An expected-deny probe passes only when the enforcement source is the operating system or the authenticated broker policy being tested. `unsupported`, `not_attempted`, host ACL denial, or an application-level stub never counts as an effective sandbox pass.

## Redaction and reproducibility

Evidence must exclude:

- usernames and home-directory paths;
- hostnames and stable machine identifiers;
- credentials, cookies, tokens, or key material;
- clipboard contents;
- real profile or page content;
- device serial numbers;
- external IP addresses.

Fixtures use random run-local paths and synthetic sentinel values. Public evidence may expose normalized platform versions, policy digests, result codes, and timing, but not identifying host metadata.

Each run preserves the exact source commit, toolchain, catalog digest, policy digest, launcher revision, platform image, and test result. A capability increase compared with the accepted baseline blocks the relevant CI lane until explained and reviewed.

## Native and unsafe boundary

The current workspace forbids unsafe Rust and external runtime dependencies. Actual sandbox APIs require platform calls, so implementation must first choose one of these reviewed strategies:

1. a narrow Turing-owned FFI crate with isolated unsafe code and complete ledgers;
2. a maintained Rust platform crate whose exact unsafe and native surface is reviewed;
3. a small separately built native launcher with a stable, bounded protocol;
4. a platform tool used only in research CI, never the product path.

The choice may differ by platform. No strategy is approved by this plan.

Every option requires:

- exact source and version;
- license and provenance;
- syscall or API inventory;
- ownership and patch response;
- negative tests;
- fuzzing where a parser or wire boundary exists;
- deterministic build and package identity;
- replacement plan;
- entries in dependency, native-code, unsafe-code, and generated-code ledgers as applicable.

## Review gates

### Contract gate

- catalog and evidence schema reviewed;
- destructive targets prohibited;
- redaction tests defined;
- unsupported behavior cannot pass;
- task scope and rollback accepted.

### Platform laboratory gate

- exact OS image and hardware/virtualization state recorded;
- unsandboxed control and sandboxed run use equivalent fixtures;
- platform primitives detected at runtime;
- allowed handles enumerated;
- every expected-deny result identifies the enforcement source;
- CI artifact validates against the schema;
- unexplained capability increases fail.

### M1 security gate

- renderer child launched through the kernel broker;
- real transport authenticated to the registered process identity;
- prohibited operations fail on every claimed platform;
- independent security review reproduces the evidence;
- residual unsupported paths are explicit;
- `REQ-SEC-001`, `PB-012`, and `WP-003` are promoted only through their owning records.

## Principal risks

- host ACLs can create false confidence;
- virtualization and CI images can differ from user systems;
- platform feature detection can be wrong or incomplete;
- sandbox policies can be applied after sensitive initialization;
- inherited handles can bypass otherwise correct policy;
- broker APIs can recreate ambient authority;
- JIT, GPU, fonts, shared memory, and accessibility can pressure teams to add broad grants;
- unsupported kernels or packaging models can be mislabeled as passing;
- probe targets can leak private data if fixtures are not isolated;
- the test harness itself can become privileged attack surface.

## Next action

After PR #40 is independently approved and merged, begin `TASK-000002` with Stage 0 only: the shared evidence types, catalog verifier, probe executable, safe fixtures, unsandboxed control, and redaction tests. Platform sandbox adapters remain separate reviewed tasks.

## Primary sources

Retrieved 2026-07-17:

- Apple App Sandbox overview: https://developer.apple.com/documentation/security/app-sandbox
- Apple App Sandbox data protection and verification: https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox
- Apple App Sandbox configuration: https://developer.apple.com/documentation/xcode/configuring-the-macos-app-sandbox
- Apple sandbox violation diagnostics: https://developer.apple.com/documentation/security/discovering-and-diagnosing-app-sandbox-violations
- Apple Hardened Runtime: https://developer.apple.com/documentation/xcode/configuring-the-hardened-runtime
- Microsoft AppContainer isolation: https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation
- Microsoft AppContainer profile API: https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-createappcontainerprofile
- Microsoft process mitigations: https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy
- Linux kernel user-space security APIs: https://docs.kernel.org/userspace-api/index.html
- Linux seccomp filter documentation: https://docs.kernel.org/userspace-api/seccomp_filter.html
- Linux Landlock documentation: https://docs.kernel.org/userspace-api/landlock.html
- Linux `unshare(2)`: https://man7.org/linux/man-pages/man2/unshare.2.html
- Linux `PR_SET_NO_NEW_PRIVS`: https://man7.org/linux/man-pages/man2/PR_SET_NO_NEW_PRIVS.2const.html
