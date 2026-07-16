# Sandbox Brokers and Platform Containment

Status: research and design baseline  
Owner: platform sandbox engineering  
Purpose: Define deny-by-default process launch, broker interfaces, platform evidence, and negative capability tests.

## Relationship to the Turing program

This document supplies the detailed implementation and evidence for SEC-GATE-1 and SEC-GATE-6 in [Blueprint 08](../blueprint-v1/08-security-and-sandbox.md).

## Sandbox contract

A sandbox profile is a generated implementation of a role's capability manifest. Default access is denied. Allowed filesystem, socket, process, device, registry, keychain, window-server, graphics, shared-memory, dynamic-code, and platform IPC operations are listed deliberately.

The effective policy, not merely source configuration, is captured in release evidence. Launch failure does not fall back to an unsandboxed process.

## Broker design

A broker converts a narrow authorized request into an OS operation. Requests carry trusted process identity, typed resource scope, origin/profile/document context where relevant, size and count limits, timeout, cancellation, and audit reason. The broker resolves paths, handles, destinations, and policy itself rather than trusting renderer-normalized values.

Broker APIs are task-specific: open approved font, read selected file handle, create download destination, resolve credential for origin, allocate bounded shared memory, or request a GPU resource. Generic file-open, arbitrary syscall, or pass-through native APIs are prohibited.

## macOS containment

The macOS plan combines App Sandbox/seatbelt policy where applicable, hardened runtime, code signing, library validation, entitlements, JIT restrictions, Mach service controls, file descriptors/handles passed at launch, and platform-specific broker processes. Every entitlement is justified by role.

The release records signature identity, hardened-runtime flags, entitlements, notarization state, JIT policy, loaded-library policy, and negative tests for files, processes, debugging, devices, Apple events, keychain, and Mach services.

## Windows containment

Windows roles use restricted tokens, integrity levels, AppContainer where viable, capabilities, job objects, handle allowlists, process mitigation policies, DLL search restrictions, dynamic-code policy, control-flow protection, win32k restrictions where compatible, and brokered access.

Evidence records effective token/capabilities, job limits, inherited handles, mitigations, package identity assumptions, file/registry/device/network tests, COM/RPC exposure, and debugger/process creation attempts.

## Linux containment

Linux roles combine user, mount, PID, network, and IPC namespaces as appropriate; seccomp filters; dropped capabilities; no-new-privileges; Landlock where useful; chroot/pivoted mount views; portal-mediated desktop resources; cgroups/rlimits; and explicit broker descriptors.

Distribution, kernel, container, Wayland/X11, GPU, audio, accessibility, and packaging differences are versioned. Unsupported kernels or missing primitives cause a documented degraded mode or block the safety claim rather than silently broad access.

## Shared memory and handles

Shared memory is created by a trusted service with purpose, size, access direction, owner, lifetime, and revocation. Receivers validate offsets, lengths, formats, generations, and sequence numbers. Executable shared memory and writable mappings of trusted metadata are prohibited unless a reviewed subsystem requires them.

Handle inheritance and descriptor passing use allowlists generated from launch configuration. Unexpected open handles are a test failure.

## Negative capability testing

Sandbox probes attempt prohibited filesystem reads/writes, sockets, DNS, process creation, debugger attach, ptrace, registry/configuration access, keychain/credential APIs, camera/microphone/display capture, USB/Bluetooth/HID, clipboard, window enumeration, dynamic library loading, executable mapping, kernel/platform IPC, and access to other profiles.

Tests run from real process roles in packaged builds, not only unit-test mocks.

## Non-negotiable invariants

- A process that cannot be sandboxed to its declared role does not launch in a claimed-safe configuration.
- Broker inputs are untrusted and re-derived from trusted identity and policy.
- No ambient filesystem, socket, credential, device, process, or debugger authority reaches renderers.
- Shared memory and inherited handles are bounded, typed, purpose-specific, and revocable.
- Effective platform policy and negative-test results are release artifacts.

## Required evidence

- Per-platform generated policy, entitlements/capabilities, mitigation, and handle manifests.
- Packaged-build negative tests on each supported OS/version.
- Broker protocol fuzzing, path/handle race tests, timeout, cancellation, and compromised-client tests.
- Effective-policy inspection and comparison against intended manifests.
- Kernel/OS version matrix with degraded and unsupported states.
- Independent review before developer-preview safety claims.

## Known risks and unresolved questions

- Platform APIs may require broad privileges that undermine clean role separation.
- OS updates can change sandbox semantics or break assumptions.
- GPU, accessibility, input, and media integration often create complex broker paths.
- A broker can become a confused deputy if it trusts paths, identities, or state from the client.

## Primary sources

- Chromium sandbox design — https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md
- Windows AppContainer isolation — https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation
- Windows process mitigation policy — https://learn.microsoft.com/en-us/windows/win32/procthread/process-mitigation-policy
- Apple Platform Security — https://support.apple.com/guide/security/welcome/web
- Apple Hardened Runtime — https://developer.apple.com/documentation/security/hardened-runtime
- Linux seccomp filters — https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html
- Linux Landlock — https://www.kernel.org/doc/html/latest/userspace-api/landlock.html

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
