# Native Platform and Browser Chrome Engineering Book

Status: detailed research and design baseline  
Owner: browser shell and platform integration engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/11-product-ui-devtools.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Essential browser controls remain independent from web rendering and responsive during renderer failure. Platform adapters are thin, capability-aware, accessible, measured, and explicit about unavoidable operating-system differences.

## Reading order

1. [Browser Chrome Scene Graph and Trusted Surfaces](01-browser-chrome-scene-graph-and-trusted-surfaces.md)
2. [Windows, Surfaces, Displays, and Lifecycle](02-windows-surfaces-displays-and-lifecycle.md)
3. [Input, IME, Clipboard, and Drag-and-Drop](03-input-ime-clipboard-and-drag-drop.md)
4. [macOS Integration](04-macos-integration.md)
5. [Windows Integration](05-windows-integration.md)
6. [Linux Integration](06-linux-integration.md)
7. [Credentials, Notifications, and External Protocols](07-credentials-notifications-and-external-protocols.md)
8. [Packaging, Startup, Power, and Support Matrix](08-packaging-startup-power-and-support-matrix.md)

## Cross-cutting rules

- Security and correctness precede benchmark wins and implementation convenience.
- Every boundary preserves typed identity and denies ambient authority.
- Queues, caches, retries, tasks, messages, persistent records, and diagnostic output are bounded.
- A deterministic serial/reference path precedes concurrent, incremental, speculative, cached, hardware, or JIT optimization.
- Physical and semantic resource ownership remain observable.
- Failure, cancellation, crash, restart, migration, pressure, and recovery are part of the supported behavior.
- Accessibility, privacy, localization, developer tooling, and platform differences are designed with the subsystem.
- Research does not change accepted requirements or support status without the normal decision process.

## Leadership criteria

Leadership requires a public evidence package combining conformance, adversarial and fault testing, fixed-hardware latency and resource measurements, accessible workflows, recovery, maintenance cost, security review, and explicit failures. A smaller feature set, weaker isolation, hidden discarding, unmatched caches, omitted failures, or vendor marketing cannot establish leadership.

## Primary sources

- https://developer.apple.com/documentation/appkit
- https://learn.microsoft.com/en-us/windows/apps/
- https://wayland.freedesktop.org/
- https://flatpak.github.io/xdg-desktop-portal/
- https://developer.apple.com/accessibility/
- https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## UI runtime relationship

The [Native UI Runtime book](../ui-runtime/README.md) owns toolkit selection and toolkit-neutral state/command contracts. This platform book continues to own windows, displays, menus, input, IME, clipboard, drag/drop, accessibility bridges, notifications, power, packaging, and OS behavior. Toolkit APIs cannot become the public platform contract.

The checked [Window Input Accessibility Spike Inventory](../research/window-input-accessibility-spike-inventory-2026-07.md) records `PB-015` planning evidence for platform workflow axes, but no platform workflow matrix, manual assistive-technology coverage, IME correctness, clipboard/drag-drop safety, page-tree proof, renderer-hang, crash, GPU-loss, or accessibility readiness exists yet.

The checked no-claim [Reference Platform Support Scorecard](../research/reference-platform-support-scorecard-2026-07.md) and [`reference-platform-scorecard.json`](machine/reference-platform-scorecard.json) make `PB-006` candidate scope, cross-platform evidence dimensions, platform and assistive-technology source observations, open questions, and unsupported rows explicit. They do not select Windows, macOS, or Linux, establish support, or replace clean-host, native-shell, accessibility, sandbox, benchmark, packaging, incident, or owner-review evidence.
