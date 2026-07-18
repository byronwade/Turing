# 11 — Product UI, Accessibility, and Developer Experience

## 1. Product design objective

Turing should feel calm, fast, legible, and intentional before it feels novel. Visual quality comes from typography, spacing, motion, hierarchy, platform integration, and responsive state—not gradients or hidden controls. Everyday browsing and deep engineering workflows share one product without forcing ordinary users to understand engine internals.

Critical state is always visible or immediately discoverable: origin, profile, private mode, permission use, downloads, capture, audio, DevTools attachment, agent control, page crash, memory suspension, update status, and security warnings.

## 2. Information architecture

Primary surfaces:

- browser window and tab strip;
- address/command field;
- side panel/workspace rail;
- page area and find UI;
- downloads, history, bookmarks, profiles, passwords/passkeys, extensions, settings, and updates;
- DevTools docking/undocking;
- agent panel, action confirmation, audit history, and stop control;
- resource manager and tab lifecycle inspector.

The address field combines URL entry, search, local history/bookmarks/tabs, commands, settings, and developer actions. Result categories remain visually distinct; a command cannot masquerade as a web result, and a web suggestion cannot silently execute a privileged action.

## 3. Window and tab model

Tabs support:

- conventional horizontal strip by default;
- optional vertical mode without changing tab semantics;
- pin, mute, duplicate, move, group, workspace, send-to-window, keep-active, discard, and close;
- keyboard selection by recency or position;
- preview of origin, profile, audio/capture, lifecycle, memory, crash, and agent state;
- protected-unsaved-state indicator;
- fast bulk search and command operations for 30+ tabs;
- restore closed tab/window and crash-safe session journal.

Tab groups are local organizational objects, not security boundaries. Profiles and private sessions are security boundaries and use unmistakable chrome treatment.

## 4. Workspaces

A workspace is a named view over tabs, groups, selected side panels, DevTools sessions, and optional agent task context within one profile. It cannot merge storage or permissions across profiles. Workspaces support export/import of URLs and layout but exclude secrets and page memory by default.

Developer workspaces can bind to a selected local repository handle, test profile, local server, trace set, and issue/task references. The binding is explicit and revocable.

## 5. Visual system

### 5.1 Tokens

The UI uses semantic design tokens for:

- typography roles and platform font stacks;
- spacing, corner, stroke, elevation, opacity, and icon sizes;
- surfaces, text, borders, focus, selection, accent, danger, warning, success, neutral, and code syntax;
- motion durations/easing and reduced-motion alternatives;
- compact, standard, and touch density;
- light, dark, high-contrast, and forced-color adaptation.

No security meaning relies on color alone. Icons have accessible names where interactive. Minimum targets and focus indicators follow platform and accessibility requirements.

### 5.2 Rendering strategy

Browser chrome uses a Turing-owned retained UI scene graph and command model. Text, icons, controls, menus, animations, hit testing, semantics, and platform integration are measured independently from web content. Native controls may be used where they materially improve accessibility or platform correctness; appearance is unified through tokens, not by reimplementing inaccessible imitations.

The UI never depends on the web engine to render essential browser controls. A renderer crash cannot remove the address bar, permission UI, agent stop control, or crash recovery.

The native toolkit remains unselected. The checked [Native UI Framework Bake-Off Inventory](../research/native-ui-framework-bakeoff-inventory-2026-07.md) records `PB-004` no-claim planning evidence for candidate summaries, equivalent reference-shell scope, evidence axes, disqualifiers, and unsupported runtime boundaries. It does not accept `ADR-0014`, approve Slint or any other toolkit, prove accessibility or IME/keyboard behavior, approve page-surface composition, approve license/provenance, or approve release-path UI.

## 6. Motion

Motion communicates spatial continuity and state changes. It is short, interruptible, and omitted when it delays input. Tab opening/closing, panel transitions, downloads, permission indicators, agent actions, and lifecycle changes have reduced-motion variants.

Performance rule: product animations should remain compositor-driven where possible and must not compete with foreground page input or raster work. A missed-frame trace identifies whether chrome or content caused the miss.

## 7. Keyboard-first operation

Every frequent operation has a command and discoverable shortcut. The command palette supports fuzzy search, parameters, recent commands, and user customization. Conflicts with webpage shortcuts are resolved predictably.

Required keyboard paths include:

- address field, tab/window/workspace navigation;
- page focus and caret browsing;
- back/forward/reload/stop/home;
- find, history, bookmarks, downloads, settings;
- zoom, full screen, reader-style view if implemented;
- DevTools open/dock/target selection;
- agent start/stop/approve/reject/review;
- resource manager, lifecycle controls, and crash recovery.

## 8. Browser accessibility

The product UI exposes native semantic roles, names, values, states, relationships, actions, focus, shortcuts, live regions, and bounds. It supports screen readers, voice control, switch control, keyboard-only operation, magnification, high contrast, forced colors, reduced motion, text scaling, platform zoom, and IME input.

Automated semantics tests are supplemented by manual testing with VoiceOver, Narrator, NVDA, and Orca/AT-SPI combinations appropriate to supported platforms. Accessibility bugs affecting navigation, origin/security information, confirmations, credentials, or agent stop are release-blocking.

## 9. Permission and security UI

Prompts identify the requesting origin and profile. Persistent decisions are reviewable in page info and settings. Active camera, microphone, display capture, location, device, fullscreen, pointer lock, and agent control use persistent indicators.

Certificate errors, malware/phishing reputation, dangerous downloads, external protocols, extension installs, credential use, passkeys, and high-risk agent actions have dedicated trusted UI. Pages cannot style or position these prompts.

## 10. Resource manager

A first-class resource manager replaces the opaque task-manager model. Views include:

- windows, tabs, frames, workers, service workers, extensions, DevTools, agents, and shared services;
- CPU, memory categories, GPU, network, disk, wakeups, energy estimate, model tokens/cost;
- process/site-instance topology and isolation state;
- tab lifecycle and protection reasons;
- cache/shared resource attribution;
- kill, freeze, discard, keep-active, inspect, export trace, and report issue actions.

Dangerous actions explain likely data loss. The manager distinguishes physical totals from charged/shared estimates.

## 11. DevTools architecture

DevTools consumes a versioned protocol from the engine and services. The frontend may be TypeScript or Rust/WASM after evaluation, but it runs in a dedicated process with strict CSP and no generic privileged bridge.

Protocol domains include:

- Target, Session, Browser, Page, Frame, Navigation, Lifecycle;
- DOM, CSS, Layout, Paint, Accessibility;
- Runtime, Debugger, Profiler, Heap, WebAssembly;
- Network, Security, Storage, ServiceWorker, Cache;
- Input, Emulation, Permissions;
- Performance, Tracing, Memory, GPU, Energy;
- Extension and Agent;
- Test and fault injection in non-stable builds.

Commands and events are generated from schemas. Breaking changes require version negotiation and migration notes.

## 12. Elements and layout tools

Elements panel requirements:

- live DOM/shadow tree with mutation tracking;
- search by text, CSS, role, accessibility name, and node reference;
- editable attributes/text with undo;
- event listeners, properties, break-on-mutation;
- styles, matched rules, cascade layers, variables, computed values, pseudo states;
- box model, font, grid/flex/scroll/container overlays;
- layout fragments, paint order, stacking contexts, compositing reasons, hit-test regions;
- accessibility name computation, tree, relationships, contrast, focus order, and issues;
- style invalidation and forced-layout reasons.

## 13. Sources, console, and runtime tools

- scripts/modules/workers/service workers and source maps;
- breakpoints, conditional/log points, DOM/event/XHR/fetch breakpoints;
- stepping, async stacks, scopes, watches, call stack, blackboxing;
- console with explicit target/realm and safe object previews;
- coverage, code cache, parse/compile timing, deoptimization and JIT tier diagnostics;
- WebAssembly disassembly/source mapping where available;
- snippets and local overrides scoped to a developer profile.

Pasting or executing code is visibly powerful. Remote debugging is authenticated and disabled by default.

## 14. Network, performance, and memory tools

Network panel shows request context, initiator, priority, timing, protocol, connection, cache/partition, service worker, redirects, security headers, CORS, cookies, body sizes, streaming, and cancellation. Sensitive headers are redacted unless explicit local reveal is permitted.

Performance tooling includes frame timeline, task queues, script, GC, style, layout, paint, raster, composite, input, network, workers, GPU, memory, energy, and agent events. Traces are deterministic enough for diffing.

Memory tooling includes JS heap snapshots, allocation sampling, DOM retainers, detached documents, native semantic categories, GPU resources, cache entries, process maps, and lifecycle before/after comparisons.

## 15. Developer-first features

- one-command isolated profile and local test server;
- replayable network/interaction fixtures;
- deterministic time/random/network controls in test profiles;
- WPT/Test262 runner integration;
- screenshot, DOM, fragment, paint, accessibility, and trace baselines;
- fault injection for OOM, process crash, GPU reset, network loss, disk full, storage corruption, clock change, and memory pressure;
- cross-browser comparison harness with honest version/config capture;
- reduced-test generator for parser/layout/runtime crashes;
- protocol client generation in Rust, TypeScript, Python, and optionally other languages;
- issue template that attaches redacted environment, trace hashes, and minimized repro without secrets.

## 16. Headless and automation

Headless mode uses the same engine, process model, sandbox, fonts, network, storage, lifecycle, and GPU/software renderer paths as interactive mode unless a difference is explicitly reported. It exposes WebDriver BiDi compatibility plus Turing extensions for engine internals and agent policy.

Automation profiles are isolated and ephemeral by default. Disabling confirmations or permissions requires explicit launch configuration and cannot attach to a normal signed-in profile unnoticed.

## 17. UI release gates

- **UI-GATE-1:** origin/profile/private/permission/capture/agent states are unambiguous in usability and spoofing tests.
- **UI-GATE-2:** all core browser and confirmation workflows are keyboard and screen-reader operable.
- **UI-GATE-3:** chrome remains responsive during renderer hang/crash and under 30-tab pressure.
- **UI-GATE-4:** command palette cannot confuse navigation, search, page content, and privileged commands.
- **UI-GATE-5:** resource manager reports process, lifecycle, isolation, and memory attribution consistently with traces.
- **UI-GATE-6:** DevTools protocol is versioned, bounded, authenticated for remote use, and does not expose ambient kernel methods.

<!-- MARKET-STRATEGY-2026-07 -->
## Proposed product differentiation

Research targets project-native Spaces, Workspace Time Machine, Research Canvas, identity routing, open migration, privacy receipts, Web App Fabric, and Developer Causal Mode. Familiar browsing remains the default. Advanced project capability is progressively disclosed and fully keyboard/screen-reader operable.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## 18. Native UI implementation working hypothesis

Browser state, typed commands, policy, persistence, recovery, tracing, and resource accounting remain pure Rust. A compiled native toolkit is isolated behind a Turing-owned adapter. Slint is evaluated first against Vizia and Floem or GPUI. React is permitted only in a separate design lab consuming shared tokens and fixtures; it does not ship in trusted chrome.

The decisive prototype composes renderer-produced page textures with chrome across resize, scale, damage, input, IME, accessibility, occlusion, capture, renderer crash, and GPU device loss. `UI-GATE-7` through `UI-GATE-12` in the [Native UI Runtime book](../ui-runtime/README.md) govern selection.

The checked [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md) records `PB-005` planning evidence for page-surface contract fields, composition alternatives, `UI-GATE-7` workflow rows, failure cases, identity boundaries, and evidence blockers. It does not prove renderer-produced page texture composition, typed page-surface handles, brokered surface handles, software fallback, `ADR-0016`, `UI-GATE-7`, compositor ownership, toolkit selection, page-surface approval, or release-path UI approval.

The checked [Window Input Accessibility Spike Inventory](../research/window-input-accessibility-spike-inventory-2026-07.md) records `PB-015` planning evidence for windowing, input, IME, accessibility-tree, page-tree composition, clipboard, drag/drop, localization, zoom, high contrast, forced colors, reduced motion, crash recovery, renderer hang, and GPU loss. It does not prove accessibility readiness, screen-reader coverage, page-tree composition, IME correctness, `UI-GATE-7`, `UI-GATE-10`, or release-path UI approval.

The current checked `PB-014` fixture inventory is the [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md). It records planning surfaces, semantic token groups, fixture axes, accessibility contracts, and authority boundaries only; it does not render fixtures, select a toolkit, prove accessibility readiness, or approve trusted chrome.
