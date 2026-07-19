# Nova Surface-to-Contract Map

Status: no-claim design traceability map; no native UI readiness or implementation claim
Owner: product design, UI runtime, accessibility, platform, performance, security, and developer experience
Source: [Turing Nova design source](turing-nova-design-source.jsx)
Manifest: [`design-source-manifest.json`](../machine/design-source-manifest.json)

## Purpose

This map turns the Nova visual/layout reference into an implementation handoff. It identifies which source surfaces already have a toolkit-neutral component-fixture contract and which require new contract work. The visual source owns appearance and composition; Rust state, typed commands, accessibility contracts, page-surface contracts, security policy, and accepted ADRs own behavior and authority.

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

## Missing component contracts

These surfaces are present in Nova and must be added to the component-fixture inventory before native implementation treats them as stable product surfaces:

| Nova source surface | Required contract focus | Primary gates | Current boundary |
| --- | --- | --- | --- |
| Turing Shield, tracker categories, security receipts, site permission popovers | origin identity, policy explanation, tracker classification, receipt redaction, revoke/manage commands | `PB-003`, `PB-012`, `PB-015` | Visual reference only; no security decision or shield readiness |
| password vault and autofill surfaces | profile/credential identity, unlock state, origin binding, redaction, fill confirmation, breach warnings | `PB-003`, `PB-016`, `PB-019` | Visual reference only; no credential or autofill implementation |
| DevTools, project inspector, causal traces, network/sources/performance/storage panels | diagnostic identity, redaction, trace ownership, page/process boundaries, export safety | `PB-003`, `PB-005`, `PB-011`, `PB-015` | Visual reference only; no DevTools protocol or diagnostic authority |
| history, bookmarks, reading list, notes, downloads, and extensions | profile/Space ownership, persistence, deletion, download safety, extension boundary, localization | `PB-003`, `PB-016`, `PB-017`, `PB-019` | Visual reference only; no storage, extension, or update implementation |
| split view, reader, capture, find-in-page, link hints, tab search | view/document identity, selection, capture permission, keyboard routing, stale-target handling | `PB-005`, `PB-015`, `PB-016` | Visual reference only; no page-surface or input-routing proof |
| Nova streaming assistant, watched pages, schedules, and agent activity log | observation redaction, grant scope, provider flow, scheduling authority, stop/revoke, audit retention | `PB-011`, `PB-012`, `PB-016`, `PB-018`, `PB-019` | Visual reference only; no agent authority or automation readiness |

## Required follow-up

1. Add the missing surfaces to the canonical component-fixture inventory with states, commands, fixture axes, accessibility contracts, and authority boundaries.
2. Bind each component to the Nova source region and the shared token registry before screenshot or visual-diff review.
3. Add native fixture coverage for keyboard, focus, screen reader, forced colors, high contrast, reduced motion, density, localization, and error/recovery states.
4. Reconcile page-surface, profile, credential, agent, update, and security records before treating a visual surface as executable browser behavior.

The map does not promote `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, or `PB-020`, and does not establish a usable browser, accessibility readiness, security readiness, Chrome-class capability, performance, or production claim.
