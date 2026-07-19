# Reference Platform Support Scorecard — July 2026

Status: checked no-claim planning and source record
Owner: platform, UI runtime, accessibility, security, performance, release operations, and quality
Primary gate: `PB-006`
Machine record: [`reference-platform-scorecard.json`](../platform/machine/reference-platform-scorecard.json)
Validator: [`validate_reference_platform_scorecard.py`](../../tools/validate_reference_platform_scorecard.py)

## Purpose

`PB-006` is the gate for selecting the first M1 reference desktop platform. The existing platform engineering book defines the required surfaces, but a platform selection cannot be inferred from a CI runner, a Rust target triple, or a platform API page. This scorecard gives Windows, macOS, and Linux the same planning dimensions and records the evidence still needed before a platform is selected or called supported.

This is a research and handoff artifact. It does not select a platform, authorize native-shell implementation, establish support, or promote any readiness gate.

## Current status

`PB-006` remains `not_selected`. The contained M0 foundation stays platform-neutral. The candidate rows below are deliberately incomplete and unexecuted.

The scorecard separates:

- a platform API or protocol observation;
- a CI image or target-triple fact;
- a local reproducible reference-platform run;
- a supported-platform decision with an owner, test matrix, incident capacity, and explicit unsupported scope.

Only the last category can support a platform decision, and it requires evidence from the dependent native UI, toolchain, sandbox, accessibility, benchmark, package/update, and incident lanes.

## Common dimensions

Every candidate must be evaluated with the same dimensions:

1. Window, display, and lifecycle behavior, including DPI/scale, multi-display, activation, occlusion, sleep, resume, and crash recovery.
2. Input, IME, clipboard, drag-and-drop, keyboard, text selection, and cancellation behavior.
3. Accessibility API, tree, focus, actions, screen-reader, high-contrast, forced-color, reduced-motion, and localization behavior.
4. Graphics and compositor identity, device loss, software fallback, frame pacing, capture, and renderer-surface composition.
5. Sandbox, permission, broker, portal, process, device, credential, and debugging boundaries.
6. Compiler, SDK, linker, target, CI image, dependency, cache, and clean-host reproducibility.
7. Packaging, startup, signing boundary, updates, rollback, migration, crash-loop handling, and recovery.
8. Power, thermal pressure, sleep/resume, background work, wakeups, and low-memory behavior.
9. Fixed-hardware benchmark identity, resource attribution, memory, energy, and failure denominator.
10. Support scope, named ownership, backup coverage, release capacity, incident response, and unsupported behavior.

## Candidate planning rows

| Candidate | Current status | Minimum next evidence | Decision remains open |
|---|---|---|---|
| Windows x64 | Not selected | Versioned Windows image, native-shell workflow, UI Automation evidence, graphics/sandbox/package/crash/sleep traces, clean-host replay, and support-owner record | Minimum Windows build, toolkit and graphics path, sandbox/package boundary, support and incident capacity |
| macOS arm64 | Not selected | Versioned macOS hardware/image, AppKit workflow, VoiceOver evidence, graphics/sleep/package/signing traces, clean-host replay, and support-owner record | Minimum macOS version, trusted-shell composition, permission/signing scope, hardware and incident capacity |
| Linux Wayland x64 | Not selected | Versioned distribution/kernel/compositor/desktop/portal, Wayland workflow, accessibility evidence, graphics fallback, sandbox/portal/package traces, clean-host replay, and support-owner record | Distribution and compositor scope, portal/sandbox combinations, deterministic graphics fallback, packaging and incident model |

The machine record retains the detailed required-evidence and open-question arrays. A missing row is not a passing row; unsupported combinations remain in the denominator.

## Evidence order

1. Name the proposed platform scope, architecture, minimum OS/image, hardware tier, compositor or windowing environment, and owner.
2. Bind the scope to the pinned toolchain and independent clean-host or owner-approved clean-VM reproduction record.
3. Run native window, input, IME, accessibility, page-surface, graphics, sandbox, packaging, recovery, and diagnostic workflows using synthetic and host-safe fixtures.
4. Capture exact versions, configuration, source/build identity, raw logs, traces, screenshots or tree snapshots where relevant, failures, timeouts, unsupported rows, and cleanup results.
5. Run fixed-hardware latency, memory, energy, and stability measurements with the benchmark identity and resource-attribution contracts.
6. Reconcile packaging, update, incident, backup-owner, support, and release-authority capacity before calling the platform supported.
7. Submit an owner-reviewed `PB-006` decision record that updates the Blueprint, platform books, requirements, risks, ADRs, backlog, task scope, support language, and machine registries together.

## Source observations

The checked machine record links official Rust platform support, GitHub runner, Microsoft Windows/UI Automation and Narrator, Apple AppKit/accessibility and VoiceOver, Wayland, XDG Desktop Portal, and GNOME Orca documentation. The assistive-technology records are separate from platform accessibility API records because a tree or control-pattern snapshot is not a screen-reader workflow. These sources establish terminology and evidence consequences. They do not establish Turing support, security, compatibility, accessibility, performance, or release readiness.

## Explicit non-claims

- No reference desktop platform is selected.
- No Windows, macOS, or Linux row has been executed on hardware or a clean host.
- CI availability is not local reproducibility, user support, sandbox proof, or incident capacity.
- A platform API, protocol, or portal is not a native-shell implementation or accessibility result.
- `PB-006` remains `not_selected`; no supported-platform, compatibility, accessibility, performance, security, release, production, or Chrome-class claim follows from this scorecard.

## Continuation

Use this scorecard with the [Native Platform and Browser Chrome Engineering Book](../platform/README.md), the [Native UI and Accessibility Closure Preparation](native-ui-and-accessibility-closure-preparation-2026-07.md), the [Fresh-Host Toolchain Reproduction Closure Preparation](fresh-host-toolchain-reproduction-closure-preparation-2026-07.md), the [Sandbox Probe Execution and Containment Closure Preparation](sandbox-probe-execution-and-containment-closure-preparation-2026-07.md), the [Benchmark Evidence and Claim Closure Preparation](benchmark-evidence-and-claim-closure-preparation-2026-07.md), package/update closure preparation, and incident-response closure preparation. Do not choose a platform from this document alone.
