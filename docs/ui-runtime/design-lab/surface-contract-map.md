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
| new tab and web-page shell | `UI-COMPONENT-NEW-TAB-PAGE-SHELL` | `PB-003`, `PB-005`, `PB-015` | Typed page-surface handles, chrome/page focus transfer, loading/error/recovery, stale-generation rejection, and page-tree/accessibility fixtures |
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

## Supporting source-component reconciliation

The Nova source also contains reusable visual primitives, settings subsections, popovers, and message-layout components. They are intentionally not separate product contracts: each is assigned to the parent contract below so the source inventory is complete without multiplying authority boundaries.

| Source components | Owning contract | Boundary |
| --- | --- | --- |
| `Fav`, `FavImg`, `UrlText`, `Skl`, `HRow`, `Row`, `Toggle`, `PerfPill`, `PageHeader` | `UI-COMPONENT-BROWSER-CHROME`, `UI-COMPONENT-TABS`, `UI-COMPONENT-RESOURCE-MANAGER`, or the owning parent fixture | Shared visual primitives carry token, text-fit, focus, density, and accessibility obligations; they do not mint commands or policy authority. |
| `A11ySec`, `DeveloperSec`, `PrivacySec`, `ShieldsSec`, `CookiesSec`, `PerformanceSec`, `AppearanceSec`, `GeneralSec`, `AutofillSec`, `SearchSec`, `AboutSec`, `WorkspaceSec`, `ThemeStudio`, `SW` | `UI-COMPONENT-SETTINGS`, `UI-COMPONENT-SPACES`, `UI-COMPONENT-SHIELD`, or `UI-COMPONENT-VAULT` | Settings subsections remain scoped to Rust preference snapshots, profile/policy identity, accessibility contracts, and typed commands; JSX state is visual input only. |
| `DownloadsSettings`, `ExtensionsInline`, `TrailPop`, `ReceiptPop` | `UI-COMPONENT-LIBRARY` or `UI-COMPONENT-SHIELD` | Inline library and security receipts retain storage, update, origin, permission, and audit boundaries; they are not independent release services. |
| `VaultRow`, `PwMeter`, `VaultPop`, `Bubble`, `Marker`, `Attachment`, `Actions`, `Action`, `Sources`, `Suggestions`, `Suggestion`, `PromptInput`, `PromptInputBody`, `PromptInputToolbar`, `PromptInputTools`, `PromptInputButton`, `PromptInputSubmit`, `MessageScroller`, `Message`, `MessageAvatar`, `MessageBody`, `MessageHeader`, `MessageFooter`, `RichText`, `CodeBlock` | `UI-COMPONENT-VAULT`, `UI-COMPONENT-AGENT-ACTIVITY`, or `UI-COMPONENT-DEVTOOLS` | Credential, provider, message, source, attachment, and code-display elements require redaction, provider/grant identity, keyboard, text-fit, and diagnostic contracts; they do not authorize data access or execution. |

The root `Nova` composition and all 91 named function components are therefore either represented by a primary surface, a source-region row, or this supporting-component reconciliation. This is a source-coverage assertion only; it does not claim that the corresponding native fixtures, accessibility workflows, security controls, or behavior contracts exist.

## Source-region reconciliation

The high-level contracts above are intentionally fewer than the visual source's React function count. The following source regions were reviewed against the committed Nova source and assigned to their owning contract. This prevents a source-level view from becoming an undocumented product surface while preserving one toolkit-neutral behavioral owner for related views.

| Nova source region | Owning contract | Reconciliation note |
| --- | --- | --- |
| `NewTab`, `SitePage`, `ErrorPage` | `UI-COMPONENT-NEW-TAB-PAGE-SHELL` and `UI-COMPONENT-RECOVERY` | New-tab, web content, loading/error, retry, and resource-recovery states remain page-surface and native-state contracts; the JSX is visual input only. |
| `VTabs`, `HistoryPage`, `DownloadsPage`, `ExtensionsPage` | `UI-COMPONENT-TABS` and `UI-COMPONENT-LIBRARY` | Tab lifecycle and library workflows retain separate identity, storage, update, keyboard, and accessibility obligations. |
| `SettingsPage`, `A11ySec`, `ThemeStudio`, `MigrationPage` | `UI-COMPONENT-SETTINGS` and `UI-COMPONENT-RECOVERY` | Preferences, accessibility controls, design tokens, and import/migration states require profile scope, rollback, and platform evidence; visual controls do not define policy. |
| `SecurityPop`, `ShieldPop`, `SiteControls`, `VaultPop`, `PasswordsSec` | `UI-COMPONENT-SHIELD` and `UI-COMPONENT-VAULT` | Trust, permission, credential, and autofill surfaces remain browser-policy and storage authorities, not React callbacks. |
| `FindBar`, `HintLayer`, `TabSearch`, `CapturePop`, `FocusPanel`, `SidePanel` | `UI-COMPONENT-VIEW-TOOLS` | Find, link hints, tab search, capture, focus, reader, and side-panel behaviors require page-generation, input-routing, permission, and accessibility contracts. |
| `ResourcesPage`, `TaskManager`, `LiveVitals` | `UI-COMPONENT-RESOURCE-MANAGER` | Resource views display attributed observations only; they cannot become a source of memory, process, or dangerous-action authority. |
| `AgentPage`, `AgentsPage`, `ApprovalPop`, `AskNova`, `SchedulesSec`, `AgentLogSec`, `AgentPermsSec`, `WatchesSec`, `ConnectionsSec` | `UI-COMPONENT-AGENT-CONFIRMATION` and `UI-COMPONENT-AGENT-ACTIVITY` | Planning, provider conversation, approvals, schedules, watches, connections, and audit history require the existing grant, confirmation, revocation, redaction, and resource-boundary contracts. |
| `CanvasPage`, `InspectorDock`, `CausalList`, `ShortcutsOverlay`, `CommandPalette` | `UI-COMPONENT-DEVTOOLS`, `UI-COMPONENT-COMMAND-FIELD`, and `UI-COMPONENT-SETTINGS` | Developer inspection, causal traces, command discovery, and shortcuts require generated protocol/state contracts and accessible command routing rather than design-lab authority. |
| `ShareSheet`, `SpaceInspector`, `TimeMachinePage` | `UI-COMPONENT-SPACES` and `UI-COMPONENT-RECOVERY` | Workspace sharing, inspection, snapshots, restore, and fork operations require profile identity, export redaction, generation checks, and data-loss controls. |

This reconciliation is a source-coverage audit, not a claim that these views are implemented natively. The committed source hash remains the integrity authority for the visual reference; the component-fixture inventory, Rust state/command model, page-surface contract, accessibility records, security policy, and accepted ADRs remain authoritative for behavior and release decisions.

## Cross-lane evidence coverage

This matrix is a continuation aid, not a second contract registry. It records the minimum evidence lanes that a Nova surface must satisfy before it can move from visual reference to an authorized native fixture. A surface may appear in more than one row. `Planning only` means the route and rejection criteria are documented; it does not mean the evidence has been executed.

| Evidence lane | Nova contracts in scope | Canonical route | Current status |
| --- | --- | --- | --- |
| Page-surface identity and composition | `UI-COMPONENT-NEW-TAB-PAGE-SHELL`, `UI-COMPONENT-VIEW-TOOLS`, `UI-COMPONENT-RECOVERY`, `UI-COMPONENT-DEVTOOLS` | [Page Surface Composition Inventory](../../research/page-surface-composition-inventory-2026-07.md), `PB-005`, `UI-GATE-7`, `ADR-0016` | Planning only; no typed handle, brokered surface, compositor decision, or fault fixture is accepted |
| Platform accessibility and assistive technology | All shell contracts, especially `UI-COMPONENT-BROWSER-CHROME`, `UI-COMPONENT-TABS`, `UI-COMPONENT-COMMAND-FIELD`, `UI-COMPONENT-SETTINGS`, `UI-COMPONENT-NEW-TAB-PAGE-SHELL`, and `UI-COMPONENT-AGENT-CONFIRMATION` | [Native UI and Accessibility Closure Preparation](../../research/native-ui-and-accessibility-closure-preparation-2026-07.md), [accessibility source manifest](../../accessibility/machine/accessibility-source-manifest.json), `PB-015`, `UI-GATE-10` | Planning only; no platform tree snapshots, manual screen-reader transcripts, IME evidence, or composed page/chrome tree review is accepted |
| Trusted-chrome authority and permissions | `UI-COMPONENT-BROWSER-CHROME`, `UI-COMPONENT-PERMISSION-PROMPT`, `UI-COMPONENT-SHIELD`, `UI-COMPONENT-VAULT`, `UI-COMPONENT-AGENT-CONFIRMATION`, `UI-COMPONENT-DEVTOOLS` | [Native UI and Accessibility Closure Preparation](../../research/native-ui-and-accessibility-closure-preparation-2026-07.md), [security and sandbox Blueprint](../../blueprint-v1/08-security-and-sandbox.md), `PB-003`, `PB-012`, `PB-011` | Planning only; no toolkit, page, extension, DevTools, agent, or renderer callback may become authority |
| Profile, storage, credentials, and recovery | `UI-COMPONENT-SPACES`, `UI-COMPONENT-SETTINGS`, `UI-COMPONENT-VAULT`, `UI-COMPONENT-LIBRARY`, `UI-COMPONENT-RECOVERY`, `UI-COMPONENT-AGENT-ACTIVITY` | [Profile/Session Execution and Data-Safety Closure Preparation](../../research/profile-session-execution-and-data-safety-closure-preparation-2026-07.md), `PB-016`, `PB-017`, `PB-019` | Planning only; no production profile format, credential, migration, update, or backup-ownership evidence is accepted |
| Fault, resource, and performance behavior | `UI-COMPONENT-TABS`, `UI-COMPONENT-RESOURCE-MANAGER`, `UI-COMPONENT-RECOVERY`, `UI-COMPONENT-VIEW-TOOLS`, `UI-COMPONENT-AGENT-ACTIVITY` | [Native UI and Accessibility Closure Preparation](../../research/native-ui-and-accessibility-closure-preparation-2026-07.md), [Benchmark Evidence and Claim Closure Preparation](../../research/benchmark-evidence-and-claim-closure-preparation-2026-07.md), `PB-013`, `PB-015` | Planning only; no renderer/GPU fault, 30-tab, latency, memory, energy, or Chrome-class result is accepted |

The matrix prevents two common handoff errors: treating visual coverage as behavioral coverage, and treating a component's presence in Nova as permission to invent an authority path. When a Nova source change affects one of these lanes, the owning route, machine registry, fixture inventory, and research log must be updated together.

## Required follow-up

1. Bind each component to the Nova source region and shared token registry before screenshot or visual-diff review.
2. Add native fixture coverage for keyboard, focus, screen reader, forced colors, high contrast, reduced motion, density, localization, and error/recovery states.
3. Reconcile page-surface, profile, credential, agent, update, and security records before treating a visual surface as executable browser behavior.
4. Produce rendered or semantic fixture evidence and owner review before any component moves beyond no-claim planning status.

The map does not promote `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, or `PB-020`, and does not establish a usable browser, accessibility readiness, security readiness, Chrome-class capability, performance, or production claim.
