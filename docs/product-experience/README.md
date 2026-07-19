# Everyday Product Experience Engineering Book

Status: detailed research and design baseline  
Owner: browser product, usability, and trusted interaction engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/11-product-ui-devtools.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Everyday quality is measured in fast, comprehensible, recoverable workflows. Minimalism removes hidden work and confusion; it does not hide security state, lifecycle state, data-loss risk, accessibility, or diagnostics.

## Reading order

1. [Tabs, Groups, Workspaces, and the Command Field](01-tabs-groups-workspaces-and-command-field.md)
2. [Onboarding, Migration, Profiles, and Private Sessions](02-onboarding-migration-profiles-and-private-sessions.md)
3. [Permissions, Credentials, Agents, and Trusted UX](03-permissions-credentials-agents-and-trusted-ux.md)
4. [Resource Manager, Tab Lifecycle, and Recovery](04-resource-manager-lifecycle-and-recovery.md)
5. [Settings, Updates, Support, Usability, and Accessibility](05-settings-updates-support-usability-and-accessibility.md)

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

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/TR/design-principles/
- https://support.mozilla.org/
- https://support.google.com/chrome/
- https://support.apple.com/guide/safari/

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
## Market-strategy integration

The proposed product center is a durable Space with folders, layouts, identity, recovery, resource policy, migration, and optional agent/Plug-in context. The [market strategy book](../market-strategy/README.md) owns hypotheses and validation; this book continues to own accepted everyday workflows.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## UI implementation boundary

Product workflows are specified independently from the selected toolkit. Component states, commands, focus, recovery, trusted indicators, and accessibility fixtures must run through every candidate adapter. React may accelerate design exploration, but no product behavior exists only in a React prototype.

The checked [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md) defines the current no-claim `PB-014` component surfaces and fixture axes. It is planning evidence only; rendered fixtures, adapter-specific outputs, and owner-reviewed accessibility evidence remain missing.

## Profile/session format boundary

The checked [Profile Session Format Inventory](../research/profile-session-format-inventory-2026-07.md), [Profile and Session Data-Lifecycle Decision Preparation](../research/profile-session-data-lifecycle-decision-prep-2026-07.md), [Profile/Session Execution and Data-Safety Closure Preparation](../research/profile-session-execution-and-data-safety-closure-preparation-2026-07.md), and checked no-claim [schema-package template](../storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json) define current no-claim `PB-016` planning and execution-handoff evidence for product-facing profile, Space, session, snapshot, migration, recovery, privacy, durability, synthetic-fixture testing, fault accounting, and data-loss boundaries. They do not define executable schemas beyond the template or approve real-profile migration, sync, credential storage, user-data handling readiness, data-loss safety, or production profile-format behavior.
