# Accessibility Engineering Book

Status: detailed research and design baseline  
Owner: accessibility architecture and assistive-technology engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/11-product-ui-devtools.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Accessibility is a first-class semantic output and interaction path. It is built with DOM, layout, editing, browser chrome, automation, and agent observations—not reconstructed after pixels exist.

## Reading order

1. [Engine Semantics and Accessibility-Tree Generation](01-engine-semantics-and-tree-generation.md)
2. [Names, Relations, Text Ranges, and Editing](02-names-relations-text-ranges-and-editing.md)
3. [Cross-Process and Cross-Origin Composition](03-cross-process-and-cross-origin-composition.md)
4. [Platform Accessibility Bridges](04-platform-accessibility-bridges.md)
5. [Browser UI, DevTools, Automation, and Agents](05-browser-ui-devtools-automation-and-agents.md)
6. [Accessibility Latency, Event Coalescing, and Resource Use](06-latency-event-coalescing-and-resource-use.md)
7. [Testing, Assistive-Technology Matrices, and Release Gates](07-testing-assistive-technology-matrices-and-release-gates.md)

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

- https://www.w3.org/TR/wai-aria/
- https://www.w3.org/TR/accname-1.2/
- https://www.w3.org/TR/WCAG22/
- https://developer.apple.com/accessibility/
- https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview
- https://gitlab.gnome.org/GNOME/at-spi2-core

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.

<!-- MARKET-STRATEGY-2026-07 -->
## Differentiated accessibility

Spaces, split panes, Time Machine, resource controls, research citations, privacy receipts, and agent confirmation require complete keyboard, screen-reader, magnification, voice, switch, contrast, and cognitive-load design. Accessibility is a market opportunity only when it remains an architecture invariant.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI framework evidence

A framework’s generic accessibility feature is not sufficient. The UI selection must prove browser chrome, tabs, Spaces, split panes, trees, tables, text fields, permission and agent prompts, recovery, and composed web subtrees with the reference platform’s real assistive technologies and measured event latency.

The checked [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md) records required accessibility contracts and fixture axes for planning. The checked [Window Input Accessibility Spike Inventory](../research/window-input-accessibility-spike-inventory-2026-07.md) records the `PB-015` workflow axes, core shell workflows, platform assistive-technology rows, and blockers for windowing, input, IME, accessibility-tree, page-tree composition, clipboard, drag/drop, localization, zoom, high contrast, forced colors, reduced motion, crash recovery, renderer hang, and GPU loss.

The no-claim [Native UI and Accessibility Workflow Examples](../research/native-ui-accessibility-workflow-examples-2026-07.md) demonstrates how a future address-field/page-surface workflow should retain authority, identity, IME, platform-tree, manual assistive-technology, fault, latency, and denominator records. It is sample documentation only; it does not prove accessibility or screen-reader readiness.

These records do not prove screen-reader, forced-color, high-contrast, reduced-motion, keyboard, focus, density, localization, error-state, manual assistive-technology, page-tree composition, IME, crash, GPU-loss, or accessibility readiness until rendered or equivalent adapter-specific fixtures are tested with real platform assistive technologies and owner-reviewed evidence.

Any future accessibility or native UI readiness decision must also be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and `PB-020` closure review. A platform workflow, accessibility snapshot, manual assistive-technology transcript, UI-gate result, or accepted UI ADR cannot independently authorize broad implementation, release-path support, production accessibility, or Chrome-class claims.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Stable-release accessibility evidence

Automated checks assist but do not establish conformance. Production review requires qualified human judgment and supported assistive-technology workflows, including security, agent, update, migration, recovery, and DevTools surfaces.
