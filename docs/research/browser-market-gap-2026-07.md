# Turing Browser Market Gap and Differentiation Research

Status: market research and product-strategy proposal; not an implementation or support claim  
Owner: product strategy, research, architecture, security, performance, accessibility, and developer experience  
Research date: 2026-07-16  
Canonical evidence path: `docs/research/browser-market-gap-2026-07.md`  
Canonical design book: `docs/market-strategy/README.md`

## Executive conclusion

The strongest defensible opportunity is not “another browser with more features.” The market already contains browsers with excellent isolated features:

- Chrome provides compatibility, a dominant extension ecosystem, synchronized tab groups, and increasingly deep AI integration.
- Edge provides workspaces, sleeping tabs, a performance detector, and strong Windows integration.
- Firefox provides containers, vertical tabs, a configurable sidebar, and a newly shipped split view.
- Vivaldi provides deep customization, workspaces, tab stacks, tab tiling, and web panels.
- Arc and Zen popularized project-oriented vertical tabs, spaces, folders, compact layouts, and persistent split views.
- Opera provides Tab Islands, context-scoped browser AI, sidebars, and split layouts supporting up to four tabs.
- Safari synchronizes profiles, tab groups, bookmarks, history, and open tabs across Apple devices.
- Brave combines privacy defaults, a built-in AI assistant, and an isolated-profile approach to early agentic browsing.

The market gap is the absence of one browser that combines these ideas into a coherent, open, project-native system with:

1. persistent workspaces that include identity, layout, data, tools, and policies;
2. a versioned session “time machine” with reliable recovery and portable export;
3. transparent resource ownership and user-controlled lifecycle decisions;
4. capability-scoped, auditable AI that never receives ambient browser authority;
5. a first-class research and comparison canvas;
6. developer-grade causal observability;
7. an open Plug-in and embedding platform;
8. low-friction migration and user-owned encrypted sync.

The proposed position is:

> **Turing is the open project browser for people and agents: it remembers the work, explains the cost, and keeps the user in control.**

## Research method

This study compared current official documentation and public product material for Chrome, Edge, Firefox, Vivaldi, Opera, Brave, Safari, Arc, and Zen. It also reviewed public user-demand signals from Mozilla Connect, Chrome support discussions, and Zen’s GitHub issue and discussion trackers.

The evidence is directional rather than a statistically representative worldwide survey. Community requests over-represent power users, and vendor pages describe intended product behavior rather than independently measured quality. Every proposed differentiator therefore requires user research, prototypes, security review, and reproducible measurement before becoming a requirement.

## Market constraints

### Chrome-class switching cost

StatCounter reported the following worldwide desktop browser shares for June 2026:

| Browser | Desktop share |
|---|---:|
| Chrome | 72.24% |
| Edge | 10.45% |
| Firefox | 6.31% |
| Safari | 5.18% |
| Opera | 1.81% |

This concentration means product novelty is not enough. Turing must reduce switching cost through migration, compatibility, Plug-in support, profile portability, familiar defaults, and excellent recovery.

### Feature convergence

Vertical tabs, workspaces, split view, sidebars, synchronized tab groups, performance controls, and browser AI are becoming expected rather than novel. A durable advantage must come from integrating these features around a better data model and trust model.

### AI is becoming standard, but trust remains unresolved

Chrome, Brave, Opera, Edge, and other browsers are adding page-aware and agentic AI. At the same time, browser vendors and security research identify indirect prompt injection, cross-origin action abuse, memory/context manipulation, and accidental harmful actions as systemic risks. Turing should compete on authority control, isolation, explainability, and audit—not merely model access.

## Competitive pattern matrix

| Capability | Notable current references | Remaining gap |
|---|---|---|
| Workspaces | Edge, Vivaldi, Arc, Zen | Identity, data, tools, resource policy, and sync are not consistently one coherent object |
| Vertical tabs and folders | Firefox, Arc, Zen, Vivaldi | Inconsistent cross-device persistence and recovery |
| Split and tiled views | Arc, Brave, Firefox, Vivaldi, Opera | Limited linked comparison, provenance, shared commands, and research workflows |
| Profiles and containers | Safari, Chrome, Edge, Firefox, Arc | Profiles, workspaces, routing rules, Plug-ins, and permissions remain fragmented |
| Resource saving | Edge sleeping tabs and performance detector; Chrome memory saving | Little semantic ownership, user-visible reasoning, state-loss guarantees, or per-project budgets |
| Cross-device continuity | Safari, Chrome, Firefox, Vivaldi, Brave | Weak full-workspace restoration, conflict handling, selective sync, and portable backup |
| AI assistance | Chrome Gemini, Brave Leo, Opera AI, Edge Copilot Mode | Ambient-authority and prompt-injection risk; weak portable audit and policy controls |
| Extension ecosystems | Chrome/Chromium and Firefox ecosystems | Broad authority, opaque resource use, uneven portability, and weak provenance |
| Developer tooling | Chrome DevTools, Firefox DevTools, Edge tooling | Developer tools remain separated from everyday project and recovery workflows |
| Migration | Basic bookmark/password/history import | Spaces, folders, split layouts, extension settings, profile relationships, and project state are frequently lost |
| Collaboration | Arc shared snapshots, previous Edge collaborative workspaces, Safari shared tab groups | Revocable, continuously synchronized, encrypted project sharing is uncommon |
| Content provenance | Chrome is adding C2PA and SynthID verification | Open, inspectable, cross-provider provenance and change history are not yet a browser-wide norm |

## User-demand signals

Repeated public requests cluster around the same needs:

1. **Context organization:** workspaces, persistent pinned tabs, folders, compact vertical tabs, and separate web panels.
2. **Workspace identity:** assigning containers, profiles, bookmarks, history, search engines, and site-routing rules to a workspace.
3. **Reliable synchronization:** syncing workspace tabs across devices and windows, not only workspace names or generic open-tab lists.
4. **Backup and restoration:** exporting browser configuration, Plug-in settings, sessions, and workspace state; recovering after crashes or automatic tab closure.
5. **Multi-pane workflows:** comparing information, research, shopping, travel planning, messaging, translation, and AI alongside primary content.
6. **Web apps and panels:** first-class PWA support and persistent side applications.
7. **Performance without lost work:** resource reclamation that does not unexpectedly reload pages, lose edits, reset scroll position, or silently close inactive tabs.
8. **AI with control:** page-aware assistance is attractive, but users need AI to be optional, scoped, private, understandable, and unable to act beyond the task.

## Core market gap

The central unserved job is:

> **“Let me treat the browser as a durable project environment rather than a pile of tabs, while preserving identity separation, performance, privacy, portability, and control over automation.”**

Current browsers solve pieces of this job. None consistently models a project workspace as the unit that owns:

- tabs, folders, pinned references, and split layouts;
- profile/container identity and credentials;
- history, bookmarks, reading items, notes, and files;
- side panels and installed web applications;
- Plug-ins and their capabilities;
- AI context, memory, model/provider, and action grants;
- resource budgets and lifecycle policy;
- synchronization, collaboration, export, and recovery history.

That integrated object should be Turing’s primary product abstraction.

# Proposed feature portfolio

## OP-001 — Turing Spaces: project-native workspaces

Priority: P0  
Target users: everyday multitaskers, power users, developers, researchers, teams

A Turing Space is a durable project object, not a visual tab filter. It contains:

- nested tab folders and persistent pinned items;
- one-to-four-pane layouts;
- optional left and right side panels;
- a bound profile or container identity;
- domain-routing rules;
- workspace-specific bookmarks, history, search shortcuts, and downloads;
- notes, tasks, selected files, citations, and saved page snapshots;
- Plug-in set and capability grants;
- AI provider, memory scope, and allowed actions;
- resource and background-work policy;
- synchronization, sharing, export, and retention settings.

### Differentiation

Arc, Zen, Vivaldi, Edge, Firefox Containers, and Safari Profiles each demonstrate parts of this demand. Turing should make the workspace the authoritative data and policy boundary.

### Required invariants

- Closing a window does not delete a Space.
- A Space can be paused, resumed, exported, imported, duplicated, and transferred.
- Space identity is independent from any one window or device.
- Site data never crosses Space identity boundaries without an explicit operation.
- Every background task, Plug-in, and agent is charged to a Space or a clearly identified shared service.
- Users can choose local-only, selected-device, encrypted-cloud, or self-hosted synchronization.

## OP-002 — Workspace Time Machine

Priority: P0  
Target users: all users, especially high-tab and research workflows

Provide automatic, versioned snapshots of browser work:

- tab and folder topology;
- split layouts and focused pane;
- scroll position and selection where safely restorable;
- form-dirty and unsaved-work protection signals;
- navigation history and back/forward state;
- notes, citations, and research artifacts;
- lifecycle state;
- Plug-in and agent session state where replay is safe;
- crash and update recovery points.

### User experience

Users can view a timeline, inspect differences, restore one tab or an entire Space, fork an old state, and export a recovery bundle.

### Safety rules

Consequential actions are never automatically replayed. Credentials, private data, and page content follow retention and encryption policy. Snapshot capture is bounded and transparent.

## OP-003 — Resource Truth Center

Priority: P0  
Target users: everyday users, power users, developers, IT administrators

Existing browsers can sleep or discard tabs, but users often cannot see exactly why an action happened or what state may be lost. Turing should expose:

- physical and attributed memory;
- CPU, GPU, network, disk, energy, wakeups, and model cost;
- ownership by Space, tab, worker, Plug-in, agent, and shared service;
- lifecycle state and last transition reason;
- state-loss risk;
- protection reasons such as audio, capture, call, upload, unsaved edit, DevTools, or confirmation;
- predicted savings before sleep, freeze, serialize, discard, or terminate;
- revival time and restored-state quality after the action.

### Standout behavior

A user can set per-Space resource budgets and policies. The browser explains a pressure decision in plain language and offers reversible actions where possible.

## OP-004 — Trustworthy Agent Mode

Priority: P0 for read-only assistance; P2 for consequential action  
Target users: everyday users, developers, enterprises, researchers

The agent operates as a distinct principal in an isolated task session with:

- an explicit task statement;
- a visible observation manifest;
- selected origins and data classes;
- typed action capabilities;
- provider and local/remote data-flow disclosure;
- CPU, memory, network, time, and token budgets;
- dry-run planning;
- step-by-step preview;
- deterministic confirmation before sensitive actions;
- browser-enforced postconditions;
- complete local audit and replay;
- immediate stop and grant revocation.

### Market differentiation

Competing browsers are rapidly adding agentic actions, while vendors and researchers acknowledge prompt injection as a systemic threat. Turing should make the security model the product.

### Non-negotiable rules

- Web content and model output cannot expand authority.
- The model never receives raw credential values.
- Agent browsing is visually and technically distinct from ordinary browsing.
- Sensitive actions require browser-owned confirmation at execution time.
- The user can choose no AI, local models, or remote providers.
- Local inference does not remove prompt-injection risk and does not bypass policy.

## OP-005 — Research and Comparison Canvas

Priority: P1  
Target users: researchers, students, shoppers, analysts, developers

Extend split view into a structured comparison environment:

- one-to-four resizable panes;
- persistent layouts saved in a Space;
- linked scrolling and optional synchronized navigation;
- side-by-side DOM/text/image diff;
- quote and screenshot capture with source URL, timestamp, and page version;
- citation-aware notes;
- duplicate-claim and source-conflict detection;
- AI restricted to the selected source set;
- export to Markdown, JSON, PDF, citation managers, and local knowledge tools;
- page-change monitoring and evidence snapshots.

### Standout behavior

The browser can answer “where did this claim come from?” and preserve enough provenance to revisit the source later.

## OP-006 — Identity Routing and Context Firewall

Priority: P1  
Target users: users with multiple accounts, developers, privacy-conscious users, enterprises

Unify profiles, containers, workspaces, and link routing:

- bind a domain to a Space or identity container;
- separate credentials, cookies, cache, storage, history, permissions, and Plug-ins;
- choose per-Space DNS, proxy, VPN, certificate, and download policy;
- visually identify the active context without allowing page spoofing;
- route external links through a preview that shows destination identity;
- prevent accidental work/personal account crossover;
- offer temporary task identities and disposable containers.

## OP-007 — Migration and Portability as a First-Class Product

Priority: P0 for launch adoption  
Target users: all switchers and embedders

Support high-fidelity migration from Chrome, Edge, Firefox, Safari, Arc, Zen, Vivaldi, Brave, and Opera:

- bookmarks, history, passwords/passkeys where platforms permit;
- open and saved tabs;
- tab groups, Spaces, folders, and pinned items;
- profile/container relationships;
- split views and web panels;
- search shortcuts;
- supported extension/Plug-in mappings;
- extension settings where legally and technically possible;
- session history and recovery bundles;
- transparent import report listing what migrated, transformed, or could not be imported.

All Turing state should export to a documented, versioned, user-owned format.

## OP-008 — Plug-in Trust Platform

Priority: P1  
Target users: everyday users, developers, enterprises

Build on the existing Turing Plug-in architecture with:

- capability-based manifests;
- WebAssembly Component Model execution;
- WebExtensions compatibility through an adapter;
- resource budgets;
- signed provenance and reproducible packages;
- store review and transparent permission history;
- per-Space installation;
- session-only grants;
- deterministic revocation;
- Plug-in diagnostics and performance attribution;
- portable SDKs and conformance tests.

First-party features should use the same constrained platform whenever feasible, proving the API and avoiding hidden privileges.

## OP-009 — Developer Causal Mode

Priority: P1  
Target users: web developers, browser developers, agent developers

Move beyond panels that show state. Explain causes:

- why style or layout invalidated;
- why a request was blocked, redirected, cached, or retried;
- why a process was selected;
- why a tab slept, woke, or lost state;
- who retains memory;
- which task delayed input;
- which permission or agent rule denied an operation;
- how a page changed across a replay;
- where behavior diverges from another browser or specification test.

Provide deterministic record/replay, trace diff, minimal test reduction, redacted diagnostic bundles, and workspace-local DevTools state.

## OP-010 — Encrypted Collaborative Spaces

Priority: P2  
Target users: teams, families, classrooms, researchers

Create revocable shared Spaces with:

- item-level sharing rather than all-or-nothing profile sharing;
- live tab/folder/note updates;
- roles and capabilities;
- explicit authenticated-content handling;
- comments and task handoff;
- end-to-end encryption;
- local audit;
- expiration and revocation;
- export and fork;
- no accidental sharing of cookies, credentials, private history, or unselected page content.

## OP-011 — Web App Fabric

Priority: P1  
Target users: productivity users, developers, enterprises

Treat installable web apps and persistent web panels as first-class Space components:

- install, pin, tile, suspend, and route web apps;
- offline and update status;
- per-app identity and permissions;
- integrated notifications and badge policy;
- app-specific Plug-ins and shortcuts;
- deterministic packaging metadata;
- portable export;
- clear distinction between trusted browser UI and web content.

## OP-012 — Privacy Receipts and Content Authenticity

Priority: P1  
Target users: all users, journalists, enterprises, researchers

Provide a per-site and per-task receipt showing:

- network destinations and tracker categories;
- cookies, storage, permissions, and device access;
- Plug-in observations and actions;
- AI data sent locally or remotely;
- retention and clearing behavior;
- credential use without exposing the credential;
- content provenance such as C2PA credentials when available;
- AI-generation indicators from supported verification systems;
- changes to a page since it was cited or saved.

The receipt should be inspectable, exportable, and understandable without requiring DevTools.

## OP-013 — Accessibility and Focus as Differentiators

Priority: P1  
Target users: disabled users, keyboard users, people managing attention and cognitive load

Include:

- complete keyboard command discovery;
- screen-reader and switch-control support;
- workspace and split-view semantics;
- focus-visible navigation history;
- page structure and reading-order inspection;
- user-controlled contrast, typography, motion, and distraction policies;
- cognitive focus modes that preserve security indicators;
- accessible comparison and citation workflows;
- AI-generated assistance clearly labeled and never substituted for authoritative accessibility semantics.

## OP-014 — Cross-Device Continuity Without Lock-In

Priority: P1  
Target users: multi-device users and teams

Synchronize or hand off:

- Space topology;
- exact active project;
- selected panes;
- recent navigation and scroll state where safe;
- notes, citations, and tasks;
- Plug-in inventory and compatible settings;
- resource/lifecycle intent;
- AI memory and grants only when explicitly selected;
- open web apps and panels.

Offer end-to-end encryption, selective data classes, recovery keys, local backup, conflict resolution, server transparency, and a documented self-hosting path.

# Priority matrix

Scores are directional hypotheses from 1 (low) to 5 (high).

| Opportunity | User value | Differentiation | Adoption effect | Technical complexity | Security risk | Recommended phase |
|---|---:|---:|---:|---:|---:|---|
| Turing Spaces | 5 | 5 | 5 | 4 | 3 | M1–M5 |
| Workspace Time Machine | 5 | 5 | 5 | 4 | 3 | M1–M5 |
| Resource Truth Center | 5 | 5 | 4 | 5 | 2 | M1–M7 |
| Trustworthy Agent Mode | 4 | 5 | 4 | 5 | 5 | Read-only M5–M6; action M7+ |
| Research Canvas | 4 | 4 | 4 | 3 | 2 | M2–M6 |
| Identity Routing | 5 | 4 | 4 | 4 | 4 | M1–M5 |
| Migration and Portability | 5 | 4 | 5 | 3 | 4 | M1 onward |
| Plug-in Trust Platform | 4 | 5 | 5 | 5 | 5 | M5–M8 |
| Developer Causal Mode | 4 | 5 | 4 | 5 | 3 | M2 onward |
| Collaborative Spaces | 4 | 4 | 3 | 5 | 5 | M7+ |
| Web App Fabric | 4 | 3 | 4 | 4 | 4 | M4–M7 |
| Privacy Receipts | 4 | 5 | 3 | 4 | 2 | M4 onward |
| Accessibility and Focus | 5 | 4 | 3 | 4 | 2 | M1 onward |
| Cross-device Continuity | 5 | 4 | 5 | 5 | 4 | M4 onward |

# Recommended product sequence

## Foundation

1. Vertical and horizontal tab modes.
2. Turing Spaces with folders, pinned items, profiles/containers, and window-independent persistence.
3. Two-pane split view, web panels, and keyboard-first command palette.
4. Crash-safe session journal and initial Time Machine.
5. Resource Truth Center with explicit lifecycle state.
6. High-fidelity import and open export.

## Differentiated developer preview

1. Four-pane Research Canvas with citations and snapshots.
2. Identity routing and temporary task containers.
3. Local-first encrypted Space sync.
4. Web App Fabric.
5. Developer Causal Mode.
6. Initial first-party Plug-ins.
7. Read-only AI assistant with selected-source grounding and no ambient action authority.

## Beta differentiation

1. Resource budgets and predictive pressure controls.
2. Full workspace history and selective cross-device handoff.
3. Privacy receipts and page-change provenance.
4. WebExtensions compatibility expansion.
5. Advanced developer record/replay and reduction.
6. Optional isolated agent mode for low-risk actions.

## Later, after security evidence

1. Consequential agentic actions.
2. Encrypted collaborative Spaces.
3. Enterprise-managed shared policies.
4. Broad third-party Plug-in store.
5. Self-hosted sync and organization services.
6. Content-authenticity integrations at scale.

# Validation program

## Study 1 — Workspace switching and recovery

Compare Chrome tab groups, Edge Workspaces, Vivaldi Workspaces, Arc/Zen-style workflows, and a Turing prototype.

Measure:

- task-switch time;
- lost or duplicated tabs;
- accidental identity crossover;
- recovery success after window and browser closure;
- user confidence;
- time to resume after one day and one week.

## Study 2 — Thirty-tab resource comprehension

Give users 30 active/background tabs, media, uploads, unsaved forms, Plug-ins, and an agent.

Measure:

- whether users correctly identify high-cost principals;
- whether they understand freeze versus discard;
- data-loss mistakes;
- memory reclaimed;
- revival latency;
- trust in automated decisions.

## Study 3 — Migration completion

Import realistic profiles from major browsers.

Measure:

- percentage of state migrated;
- manual repair time;
- failed logins;
- lost organization;
- extension/Plug-in substitution success;
- confidence that the old browser can be removed.

## Study 4 — AI trust and control

Compare ordinary sidebar chat, an isolated Turing agent, and a no-AI control.

Measure:

- task completion;
- unintended actions;
- prompt-injection resistance;
- confirmation fatigue;
- understanding of data flow;
- stop/revoke success;
- willingness to use the feature again.

## Study 5 — Research Canvas

Run travel, shopping, technical debugging, academic research, and policy-comparison tasks.

Measure:

- tab switching;
- source errors;
- citation completeness;
- time to produce an export;
- ability to reproduce the conclusion;
- cognitive load and accessibility.

## Study 6 — Developer Causal Mode

Compare common debugging tasks against Chrome and Firefox DevTools.

Measure:

- time to identify root cause;
- false hypotheses;
- trace setup time;
- diagnostic bundle usefulness;
- successful minimal reproduction;
- keyboard and screen-reader completion.

# Documentation expansion plan

Recommended new canonical book:

```text
docs/market-strategy/
├── README.md
├── 01-market-method-and-segments.md
├── 02-competitive-feature-matrix.md
├── 03-user-demand-and-switching-barriers.md
├── 04-project-native-workspaces.md
├── 05-time-machine-and-continuity.md
├── 06-resource-truth-and-lifecycle-control.md
├── 07-trustworthy-ai-and-agent-differentiation.md
├── 08-research-canvas-and-developer-mode.md
├── 09-migration-portability-collaboration-and-sync.md
├── 10-feature-prioritization-and-validation.md
└── machine/
    └── feature-opportunities.json
```

Also update:

- `docs/README.md`
- `docs/blueprint-v1/02-capability-parity.md`
- `docs/blueprint-v1/09-performance-memory.md`
- `docs/blueprint-v1/10-ai-agent-platform.md`
- `docs/blueprint-v1/11-product-ui-devtools.md`
- `docs/blueprint-v1/14-roadmap-work-breakdown.md`
- `docs/blueprint-v1/15-risk-register.md`
- `docs/blueprint-v1/20-definition-of-done.md`
- `docs/blueprint-v1/21-product-requirements.md`
- `docs/blueprint-v1/22-research-program.md`
- `docs/product-experience/`
- `docs/performance/`
- `docs/security-engine/`
- `docs/ai/`
- `docs/developer-experience/`
- `docs/plugins/`
- `docs/embedding/`
- requirements, risks, work packages, ownership, traceability, repository map, and validation when proposals become accepted.

# Proposed headline

> **Turing is the browser that remembers your projects, explains its resource use, and gives AI only the authority you approve.**

# Sources

## Market and browser share

- StatCounter desktop browser market share: https://gs.statcounter.com/browser-market-share/desktop

## Chrome

- Chrome Help index and feature surface: https://support.google.com/chrome/
- Manage tabs and synchronized tab groups: https://support.google.com/chrome/answer/2391819
- Chrome AI strategy and multi-tab context: https://blog.google/products-and-platforms/products/chrome/chrome-reimagined-with-ai/
- Chrome agentic auto browse on Android: https://blog.google/products-and-platforms/products/chrome/bringing-chrome-ai-to-android/
- Chrome support discussion on synchronized-group management: https://support.google.com/chrome/thread/291270103/
- Chrome support discussion on inactive-tab loss: https://support.google.com/chrome/thread/379023216/

## Edge

- Edge performance features, sleeping tabs, and performance detector: https://support.microsoft.com/en-us/edge/learn-about-performance-features-in-microsoft-edge
- Edge Workspaces: https://support.microsoft.com/en-us/edge/getting-started-with-microsoft-edge-workspaces

## Firefox and Mozilla community

- Firefox sidebar and vertical tabs: https://support.mozilla.org/en-US/kb/use-sidebar-access-tools-and-vertical-tabs
- Firefox Split View: https://support.mozilla.org/en-US/kb/split-view-firefox
- Firefox Multi-Account Containers: https://support.mozilla.org/en-US/kb/containers
- Mozilla Connect demand for workspaces, container assignment, sync, backup, and web panels: https://connect.mozilla.org/t5/discussions/features-that-increase-efficiency-and-usability-should-be-added/td-p/81049
- Mozilla Connect demand for persistent pinned tabs, folders, and web panels: https://connect.mozilla.org/t5/discussions/workspace-persintent-pinned-tabs-folders-zen-browser-and-web/td-p/131009

## Vivaldi

- Workspaces: https://vivaldi.com/features/workspaces/
- Sync and end-to-end encryption: https://help.vivaldi.com/desktop/tools/sync/

## Opera

- Opera One R3, Tab Islands, scoped AI, and four-way Split Screen: https://blogs.opera.com/news/2026/01/opera-one-r3-new-browser-update/
- Opera features and split screen: https://help.opera.com/en/latest/features/

## Brave and agentic security

- Brave Split View: https://support.brave.com/hc/en-us/articles/35087087593997-How-do-I-use-Split-view-in-Brave
- Brave Leo: https://brave.com/leo/
- Brave agentic browsing safety model: https://brave.com/blog/ai-browsing/
- Prompt injection in agentic browsers: https://brave.com/blog/comet-prompt-injection/
- Agentic browser security series: https://brave.com/series/security-privacy-in-agentic-browsing/

## Safari

- Safari profile and tab-group sync: https://support.apple.com/guide/icloud/what-you-can-do-with-icloud-and-safari-mm9b8da4f328/icloud
- Safari Profiles: https://support.apple.com/en-euro/105100

## Arc and Zen

- Arc profiles and Space assignment: https://resources.arc.net/hc/en-us/articles/19227964556183-Profiles-Separate-Work-Personal-Browsing
- Arc Split View: https://resources.arc.net/hc/en-us/articles/19335393146775-Split-View-View-Multiple-Tabs-at-Once
- Arc sharing: https://resources.arc.net/hc/en-us/articles/19228534606743-Share-Spaces-Folders-Splits-with-Anyone
- Zen workspace/window session persistence request: https://github.com/zen-browser/desktop/issues/7079
- Zen cross-device workspace tab sync request: https://github.com/zen-browser/desktop/issues/6981
- Zen PWA and Chrome-extension demand: https://github.com/zen-browser/desktop/issues/285
- Zen workspace gesture demand: https://github.com/zen-browser/desktop/discussions/827

## Security research

- WASP web-agent prompt-injection benchmark: https://arxiv.org/abs/2504.18575
- ceLLMate browser-agent sandboxing: https://arxiv.org/abs/2512.12594
- Context manipulation attacks against web-agent memory: https://arxiv.org/abs/2506.17318
- MUZZLE adaptive red-teaming of web agents: https://arxiv.org/abs/2602.09222
- USENIX research on network-level prompt and trait leakage: https://www.usenix.org/conference/usenixsecurity26/presentation/jeong
