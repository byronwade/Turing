# Nova Surface-to-Contract Map

Status: no-claim design traceability map; no native UI readiness or implementation claim
Owner: product design, UI runtime, accessibility, platform, performance, security, and developer experience
Source: [Turing Nova design source](turing-nova-design-source.jsx)
Manifest: [`design-source-manifest.json`](../machine/design-source-manifest.json)

## Purpose

This map turns the Nova visual/layout reference into an implementation handoff. It identifies which source surfaces have a toolkit-neutral component-fixture contract and which still require executable fixture or protocol work. The visual source owns appearance and composition; Rust state, typed commands, accessibility contracts, page-surface contracts, security policy, and accepted ADRs own behavior and authority.

## Covered component contracts

| Nova source surface | Existing component contract | Primary gates | Next evidence |
| --- | --- | --- | --- |
| window chrome, origin/profile indicators, navigation controls | `UI-COMPONENT-BROWSER-CHROME` | `PB-003`, `PB-014`, `PB-015` | Native window, focus, trusted-state, accessibility, and command fixtures |
| tabs, tab groups, pinned/muted/captured/frozen/discarded tabs | `UI-COMPONENT-TABS` | `PB-003`, `PB-014`, `PB-015`, `PB-013` | Lifecycle, density, keyboard, screen-reader, and 30-tab fixture evidence |
| Spaces, workspace rail, layouts, developer bindings | `UI-COMPONENT-SPACES` | `PB-003`, `PB-014`, `PB-016` | Profile boundary, export redaction, layout recovery, and localization fixtures |
| address/search/command field, command palette, tab search | `UI-COMPONENT-COMMAND-FIELD` | `PB-003`, `PB-015` | URL/search/command separation, stale-result rejection, IME, and accessible-combobox fixtures |
| permission prompts, site controls, capture/microphone/location indicators | `UI-COMPONENT-PERMISSION-PROMPT` | `PB-003`, `PB-015`, `PB-012` | Origin/profile/document-epoch binding, focus trap, and policy-denial evidence |
| agent confirmation, approval queue, audit and stop controls | `UI-COMPONENT-AGENT-CONFIRMATION` | `PB-003`, `PB-011`, `PB-012` | Risk-class, stale-target, revocation, provider-flow, and keyboard confirmation fixtures |
| Resource Truth Center, task manager, performance/resource views | `UI-COMPONENT-RESOURCE-MANAGER` | `PB-003`, `PB-013`, `PB-015` | Physical-versus-charged accounting, 30-tab pressure, dangerous-action, and trace-export fixtures |
| settings, theme studio, privacy, shields, accessibility, and developer settings | `UI-COMPONENT-SETTINGS` | `PB-003`, `PB-014`, `PB-015`, `PB-016`, `PB-017` | Profile/policy scope, forced-color, text-fit, reset, migration, and update-state fixtures |
| crash, hang, safe mode, session restore, profile repair, rollback | `UI-COMPONENT-RECOVERY` | `PB-003`, `PB-005`, `PB-015`, `PB-016`, `PB-017` | Renderer/GPU failure, data-loss warning, stale snapshot, and rollback evidence |

## Newly represented Nova component contracts

These surfaces are now represented in the component-fixture inventory as no-claim planning records. They are not stable product surfaces until their executable, accessibility, security, storage, and owner-review evidence exists:

| Nova source surface | Component contract | Primary gates | Current boundary |
| --- | --- | --- | --- |
| Turing Shield, tracker categories, security receipts, site permission popovers | `UI-COMPONENT-SHIELD` | `PB-003`, `PB-012`, `PB-015` | No security decision or Shield readiness |
| password vault and autofill surfaces | `UI-COMPONENT-VAULT` | `PB-003`, `PB-016`, `PB-019` | No credential or autofill implementation |
| DevTools, project inspector, causal traces, network/sources/performance/storage panels | `UI-COMPONENT-DEVTOOLS` | `PB-003`, `PB-005`, `PB-011`, `PB-015` | No DevTools protocol or diagnostic authority |
| history, bookmarks, reading list, notes, downloads, and extensions | `UI-COMPONENT-LIBRARY` | `PB-003`, `PB-016`, `PB-017`, `PB-019` | No storage, extension, or update implementation |
| split view, reader, capture, find-in-page, link hints, tab search | `UI-COMPONENT-VIEW-TOOLS` | `PB-005`, `PB-015`, `PB-016` | No page-surface or input-routing proof |
| Nova streaming assistant, watched pages, schedules, and agent activity log | `UI-COMPONENT-AGENT-ACTIVITY` | `PB-011`, `PB-012`, `PB-016`, `PB-018`, `PB-019` | No agent authority or automation readiness |

## Required follow-up

1. Bind each component to the Nova source region and shared token registry before screenshot or visual-diff review.
2. Add native fixture coverage for keyboard, focus, screen reader, forced colors, high contrast, reduced motion, density, localization, and error/recovery states.
3. Reconcile page-surface, profile, credential, agent, update, and security records before treating a visual surface as executable browser behavior.
4. Produce rendered or semantic fixture evidence and owner review before any component moves beyond no-claim planning status.

The map does not promote `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, or `PB-020`, and does not establish a usable browser, accessibility readiness, security readiness, Chrome-class capability, performance, or production claim.
