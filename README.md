# Turing Browser

Turing is the working codename for an independent, Rust-first browser and web-engine program focused on minimalism, speed, security, developer experience, accessibility, open integration, and capability-scoped AI.

> **Current status:** research, architecture, documentation, and executable policy prototype. Turing is not yet a production browser and is not safe for sensitive or arbitrary hostile browsing.

The long-term target is a general-purpose browser with a Turing-owned web engine, JavaScript runtime architecture, browser shell, developer platform, Plug-in system, embedding SDK, and agent authorization model. Release paths must not embed Chromium, WebKit, Gecko, Electron, CEF, an operating-system web view, or remote rendering.

## Feature status

This README summarizes the complete currently documented feature surface. It does **not** claim that the features are implemented.

| Status | Meaning |
|---|---|
| **Prototype** | Represented by the small executable Rust model under `prototype/` |
| **Accepted direction** | Part of the normative Blueprint or accepted product requirements, but generally not implemented yet |
| **Proposed opportunity** | Market or product hypothesis recorded as `OP-*`; requires research, review, requirements, risks, ownership, and evidence before acceptance |
| **Deferred or externally gated** | Deliberately postponed or dependent on licensing, platform, staffing, or commercial access |

The canonical status sources are the [Product Requirements Document](docs/blueprint-v1/21-product-requirements.md), [roadmap](docs/blueprint-v1/14-roadmap-work-breakdown.md), [market opportunity registry](docs/market-strategy/machine/feature-opportunities.json), and [requirements registry](docs/blueprint-v1/machine/requirements.json).

## Why Turing

Turing is designed around six product and engineering differentiators:

1. **An independent, standards-driven engine** with Rust-first ownership and explicit security boundaries.
2. **Project-native browsing** where Spaces can own organization, identity, recovery, tools, resource policy, and scoped agent authority.
3. **Explainable performance** with semantic CPU, memory, GPU, network, disk, energy, Plug-in, and model attribution.
4. **Trustworthy AI** in which models are untrusted principals and deterministic browser code controls authority.
5. **Developer-grade causality** that explains why rendering, networking, storage, lifecycle, security, and agent decisions occurred.
6. **Open integration** through bounded Turing Plug-ins and a stable multi-language embedding contract.

The proposed product position is:

> **Turing is the open project browser for people and agents: it remembers the work, explains the cost, and keeps the user in control.**

<!-- FEATURE-CATALOG-2026-07 -->
## Planned feature catalog

### Everyday browsing and browser shell

Accepted product direction includes:

- multiple windows, profiles, isolated private sessions, tabs, tab groups, folders, and workspaces;
- vertical and horizontal tab presentations where supported by the product design;
- a unified address, search, and command field with clearly identified result types;
- navigation, reload, stop, back/forward history, zoom, find, print, save, view source, and external-protocol handling;
- history, bookmarks, downloads, settings, credentials, passkeys where platform support permits, page information, permissions, and updates;
- native keyboard, pointer, touch or pen where supported, input-method editing, clipboard, drag-and-drop, menus, and platform integration;
- side panels, web panels, installed web applications, and persistent project tools;
- accessible trusted browser chrome that remains available when a renderer hangs or crashes;
- crash-loop handling, safe mode, session journaling, and selective recovery;
- clear research, preview, beta, stable, support, and unsupported-feature labels.

See [Product Experience Engineering](docs/product-experience/README.md) and [Native Platform and Browser Chrome Engineering](docs/platform/README.md).

### Project-native workflow and market differentiators

The following remain proposed opportunities rather than accepted requirements:

| ID | Proposed feature | Intended value |
|---|---|---|
| `OP-001` | **Turing Spaces** | Durable project environments containing tabs, folders, layouts, identity, notes, tools, Plug-ins, agents, and policy |
| `OP-002` | **Workspace Time Machine** | Versioned snapshots, selective restoration, branching, crash recovery, and encrypted recovery bundles |
| `OP-003` | **Resource Truth Center** | Explainable ownership, lifecycle state, predicted savings, restoration cost, and state-loss risk |
| `OP-004` | **Trustworthy Agent Mode** | Isolated tasks, visible observations, typed authority, dry runs, confirmation, audit, stop, and revoke |
| `OP-005` | **Research and Comparison Canvas** | Persistent multi-pane comparison, linked navigation, citations, snapshots, diffing, and reproducible export |
| `OP-006` | **Identity Routing and Context Firewall** | Domain-to-Space routing and separation of credentials, cookies, storage, history, permissions, and Plug-ins |
| `OP-007` | **Migration and Portability** | High-fidelity import plus a documented, versioned, user-owned export format |
| `OP-008` | **Plug-in Trust Platform** | Capability-scoped, signed, resource-bounded native Plug-ins with a compatibility adapter |
| `OP-009` | **Developer Causal Mode** | Cross-subsystem explanations, deterministic replay, trace comparison, and reduced-test generation |
| `OP-010` | **Encrypted Collaborative Spaces** | Revocable, item-level, encrypted project sharing without sharing credentials or ambient profile state |
| `OP-011` | **Web App Fabric** | Installable web apps and panels as identity-aware, lifecycle-managed Space components |
| `OP-012` | **Privacy Receipts and Content Authenticity** | Readable records of site, Plug-in, agent, credential, storage, network, AI, and provenance behavior |
| `OP-013` | **Accessibility and Focus Differentiation** | Keyboard, assistive-technology, cognitive-load, typography, contrast, motion, and focus leadership |
| `OP-014` | **Cross-Device Continuity Without Lock-In** | Selective encrypted synchronization, handoff, recovery keys, open export, and a self-hosting path |

See the [Market Strategy and Differentiation book](docs/market-strategy/README.md) and [browser market-gap report](docs/research/browser-market-gap-2026-07.md).

### Performance, memory, energy, and reliability

Accepted direction includes:

- responsive browser UI during renderer hangs, crashes, and heavy tab pressure;
- lifecycle states such as active, background, frozen, discarded, and restoring;
- explicit keep-active, freeze, discard, inspect, trace, and terminate controls;
- protection for audio, calls, capture, uploads, downloads, devices, unsaved work, debugging, and confirmations;
- predictable revival with visible reload, restoration, and state-loss behavior;
- attribution of CPU, physical and logical memory, GPU allocation, network, disk, wakeups, energy, Plug-in work, and model cost;
- per-Space, per-tab, per-worker, per-Plug-in, per-agent, and shared-service accounting;
- bounded queues, caches, buffers, surfaces, workers, parsers, recursion, and hostile-input allocations;
- pressure-aware reclamation that does not silently weaken site isolation or misrepresent discarded tabs as live tabs;
- startup, address-field readiness, navigation, input-to-present, frame pacing, memory, energy, recovery, and 30-tab benchmarks;
- fixed-hardware comparison with disclosed process topology, security settings, cache state, tab lifecycle, unsupported pages, and raw results;
- transactional storage, migration recovery, disk-full handling, corruption handling, fault injection, crash diagnostics, signed update rollback, and profile downgrade protection.

See [Performance Engineering](docs/performance/README.md), the [Fixed-Hardware Benchmark Laboratory](docs/benchmark-lab/README.md), and [Storage and Recovery Engineering](docs/storage/README.md).

### Security and privacy

Accepted direction includes:

- a deny-by-default, capability-separated multiprocess architecture;
- browser-kernel, renderer, network, storage, GPU, media or decoder, Plug-in, DevTools, agent, updater, and crash-process roles;
- site isolation based on site instances and browsing-context groups;
- typed, bounded, versioned IPC with stale-identity and document-epoch rejection;
- operating-system sandbox evidence for macOS, Windows, and Linux;
- brokered files, sockets, devices, credentials, clipboard, shared memory, platform services, and privileged operations;
- isolated profiles and ephemeral private sessions;
- credential and passkey brokers that do not expose raw secrets to pages, Plug-ins, DevTools, or models;
- CORS, CSP, CORP, COOP, COEP, mixed-content, cookie, permission, and origin enforcement;
- native parser, codec, PDF, font, image, media, JIT, GPU, extension, automation, and agent containment;
- signed, reproducible, rollback-capable updates with provenance, SBOMs, notices, symbols, and key-rotation policy;
- anti-phishing, trusted-origin UI, international-domain handling, reputation strategy, and spoofing resistance;
- minimal opt-in telemetry, bounded redacted diagnostics, clear remote-provider data flow, and user-visible clearing or export;
- private vulnerability reporting, embargoed fixes, security patch operations, independent review, and release gates.

See [Browser Security Engineering](docs/security-engine/README.md), [Security and Sandbox](docs/blueprint-v1/08-security-and-sandbox.md), and [Release Operations](docs/release-operations/README.md).

### Independent web engine and web platform

The long-term engine surface includes:

- URL, encoding, HTML tokenization and tree construction;
- DOM, events, forms, editing, selection, focus, and input;
- CSS tokenization, parsing, selectors, cascade, computed values, inheritance, invalidation, and animations;
- block, inline, text, bidirectional, writing-mode, flexbox, grid, table, float, positioned, transformed, and fragmented layout tracks;
- retained paint, display lists, damage tracking, hit testing, scrolling, rasterization, compositing, and GPU integration;
- Unicode, international text, fonts, shaping, fallback, color, zoom, and input-method behavior;
- images, SVG, canvas, audio, video, WebRTC, capture, PDF, printing, codecs, and hardware acceleration where support and licensing permit;
- engine-generated accessibility semantics and cross-process platform accessibility trees;
- JavaScript parsing, bytecode, interpreter, objects, modules, event loop, exact tracing garbage collection, Web IDL, debugger, staged JIT tiers, no-JIT mode, and WebAssembly;
- Fetch, HTTP/1.1, HTTP/2, HTTP/3, QUIC, DNS, proxies, TLS, certificates, cookies, cache, preloading, WebSocket, WebTransport, and downloads;
- local and session storage, IndexedDB, Cache Storage, service workers, quotas, partitioning, transactional migrations, repair, and clearing;
- workers, structured clone, background work, permissions, devices, and evolving standards tracks;
- Web Platform Tests, Test262, differential testing, reduced tests, fuzzing, property testing, formal methods where justified, and interoperability reporting.

The project may use audited foundations for cryptography, TLS, Unicode data, text shaping, codecs, graphics drivers, databases, and operating-system sandbox mechanisms, but those dependencies must not become hidden complete browser engines.

See [Browser Engine Engineering](docs/engine/README.md), [JavaScript Runtime Engineering](docs/javascript/README.md), [Networking Engineering](docs/networking/README.md), and [Open Web Platform Governance](docs/web-platform/README.md).

### Developer platform and DevTools

Accepted direction includes:

- Elements, Styles, Layout, Accessibility, Console, Sources, Network, Performance, Memory, Storage, Security, Application or Service Worker, Rendering, Protocol, and Issues tooling;
- DevTools data derived from the same engine facts used for execution rather than a separate approximate model;
- a versioned Turing engine instrumentation protocol with stable and experimental domains;
- WebDriver BiDi as the standards-facing automation track;
- optional compatibility adapters without making another browser protocol Turing’s internal source of truth;
- deterministic headless and test profiles using the same engine and security model;
- virtual time, deterministic random and network controls, emulation, fault injection, and reproducible profiles;
- cross-subsystem causal tracing, trace comparison, replay divergence, memory retainers, scheduler attribution, and policy reason codes;
- automatic crash and test reduction, safe diagnostic bundles, and local workspace integration with explicit grants;
- generated Rust, TypeScript, Python, and other protocol clients;
- keyboard- and screen-reader-accessible debugging workflows;
- separate developer grants for agents that inspect diagnostics or perform privileged debugging operations.

See [Developer Experience and DevTools](docs/developer-experience/README.md) and [API Design](docs/api-design/README.md).

### AI assistant and agent platform

Accepted direction includes an optional assistant that can explain, summarize, find, organize, and perform only approved actions.

The agent platform is designed around:

- local, remote, and disabled provider choices with no silent fallback;
- visible data-flow manifests, model identity, budgets, latency, cost, and resource use;
- semantic observations with source, origin, frame, profile, document epoch, sensitivity, visibility, and redaction labels;
- optional screenshots as explicitly labeled observations rather than automatic ambient vision;
- typed actions with preconditions, postconditions, risk class, idempotency, cancellation, and expiry;
- scoped grants bound to profile, origin, frame, document epoch, action class, time, usage, and data sensitivity;
- deterministic browser authorization rather than model self-approval;
- trusted confirmation for consequential actions;
- stop, revoke, timeout, crash recovery, and complete local audit;
- browser-held credentials and secret handles instead of exposing raw secret values;
- isolated automation or agent profiles where appropriate;
- prompt-injection, stale-target, secret-request, cross-origin, memory manipulation, and resource-exhaustion evaluations;
- local-model loading, unloading, memory, accelerator, thermal, and 30-tab interaction budgets;
- MCP or tool connections mediated by browser capabilities rather than ambient external authority.

See [AI and Agent Engineering](docs/ai/README.md) and [AI Agent Platform](docs/blueprint-v1/10-ai-agent-platform.md).

### Turing Plug-ins

Turing calls browser extensions **Plug-ins**. The proposed platform has four execution tiers:

- first-party maintained, separately updateable Plug-ins without blanket kernel privilege;
- portable WebAssembly Components using WIT imports, explicit capabilities, memory limits, interruption, cancellation, and isolated storage;
- a restricted WebExtensions compatibility adapter with a published support matrix;
- visible developer-only local Plug-ins restricted to isolated profiles.

Every Plug-in is intended to be separately identified, signed, revocable, lifecycle-managed, resource-accounted, and denied ambient access to credentials, cookies, sockets, files, unrelated profiles, hidden cross-origin content, browser memory, trusted UI, generic IPC, or agent confirmation authority.

The proposed first-party portfolio is:

1. Turing Assistant
2. Developer Copilot
3. Screenshot Studio
4. Interaction Recorder
5. Translation and Language Tools
6. Reader and Research Mode
7. Writing Assistant
8. Dark, Contrast, and Focus Modes
9. Privacy Inspector
10. Content Filter Lists
11. Tab and Workspace Organizer
12. Notes and Web Clipper
13. Archive and Export
14. JSON and Data Inspector
15. API and Request Toolkit
16. Accessibility Inspector
17. Performance and Resource Profiler
18. Framework and Source Inspector
19. Shopping Comparison
20. Meeting and Media Notes

This portfolio is a workflow research cohort, not an exact worldwide extension ranking and not permission to copy third-party code, names, branding, assets, or behavior.

See the [Turing Plug-in Platform](docs/plugins/README.md).

### Embedding and multi-language SDK

Turing is intended to be usable as an embeddable engine and browser platform through:

- a canonical idiomatic Rust API;
- a minimal stable C ABI with version negotiation and opaque generation-checked handles;
- generated C++, Python, Node.js or TypeScript, Swift, Kotlin or Java, C#, Go, and WIT SDKs;
- explicit Engine, Profile, View, Surface, Navigation, EventStream, CapabilitySet, ResourceBudget, PluginHost, CancellationToken, and typed-identity concepts;
- interactive, offscreen, headless, deterministic-test, automation, and server-rendering modes sharing one security and lifecycle model;
- bounded asynchronous operations with deadlines, cancellation, backpressure, and exactly one terminal result;
- structured input, IME, clipboard, drag-and-drop, accessibility, surface, synchronization, and device-loss contracts;
- separate product, engine, Rust API, C ABI, protocol, profile, Plug-in, and SDK versions;
- signed packages, checksums, SBOMs, provenance, symbols, notices, supported-platform declarations, and host conformance tests;
- versioned migration, Space, session, recovery, and open-export concepts without exposing internal engine layouts.

The target is safe-default integration in a few lines while advanced authority remains explicit. No stable embedding API or SDK exists yet.

See [Embedding and Multi-language SDK](docs/embedding/README.md) and [Technology Stack](docs/technology-stack/README.md).

### Accessibility, internationalization, and inclusive design

Accepted direction includes:

- native semantic browser UI and an engine-generated web accessibility tree;
- keyboard, screen reader, voice control, switch control, magnification, zoom, high contrast, forced colors, and reduced motion;
- accessible tabs, folders, Spaces, split views, side panels, permissions, origin indicators, agent confirmations, DevTools, and recovery flows;
- platform bridges for VoiceOver, UI Automation, and AT-SPI ecosystems;
- international text shaping, bidirectional text, writing modes, font fallback, input methods, locale-aware formatting, and right-to-left browser chrome;
- pseudo-localization, translation workflows, accessible error states, and release-blocking critical-flow defects;
- focus and cognitive-load features that never hide security state;
- assistive-technology latency, event coalescing, and resource-use measurement.

See [Accessibility Engineering](docs/accessibility/README.md).

### Enterprise, synchronization, distribution, and operations

Later product stages include:

- enterprise policy, deployment, proxy, certificate, update, audit, data-control, Plug-in-management, and support surfaces;
- encrypted synchronization with conflict resolution, schema evolution, quotas, selective data classes, recovery keys, and explicit metadata policy;
- local backup, open export, and a researched self-hosting path rather than mandatory account lock-in;
- signed installers and platform packages for supported macOS, Windows, and Linux targets;
- reproducible unsigned builds separated from signing and notarization;
- staged rollout, pause, rollback, minimum secure versions, emergency patches, symbols, crash diagnostics, and supported-version policy;
- release channels such as nightly, preview, developer, beta, and stable, with support obligations increasing by channel;
- explicit proprietary gaps, including DRM, patented codecs, vendor account services, store access, entitlements, and commercial distribution dependencies.

See [Extensions, Enterprise Policy, Accounts, and Sync](docs/extensions-enterprise/README.md) and [Build, Release, Update, and Incident Operations](docs/release-operations/README.md).

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native shell and UI architecture plan

The trusted browser shell is planned as a native Rust application with no Electron, Tauri, operating-system webview, React runtime, Node runtime, DOM, or runtime CSS engine in release packages.

The current working hypothesis is:

- pure Rust owns browser state, typed commands, policy, persistence, recovery, tracing, and resource accounting;
- a replaceable native UI adapter owns presentation only;
- Slint is the initial framework candidate because it compiles declarative UI ahead of time and provides a mature design workflow;
- Vizia and Floem or GPUI provide equivalent comparison prototypes before selection;
- React may be used only in a separate design lab that consumes shared tokens and fixtures and never ships in the browser;
- the decisive experiment is composing renderer-produced page textures with trusted chrome while preserving input, IME, accessibility, scaling, damage, crash recovery, and GPU device loss;
- normal builds compile one selected UI backend/renderer and lazy-load secondary product surfaces.

No UI toolkit has been adopted yet. See [Native UI Runtime and Browser Chrome Engineering](docs/ui-runtime/README.md), the [framework evaluation](docs/research/native-ui-framework-evaluation-2026-07.md), and the [pre-build readiness audit](docs/research/pre-build-readiness-gap-audit-2026-07.md).

## Pre-build readiness

Turing is ready for contained architecture spikes, not broad parallel implementation. `PB-001` through `PB-020` track unresolved source strategy, UI, compositor, platform, workspace, toolchain, sandbox, benchmark, design-system, storage, release, incident, and ownership evidence. The canonical registry is [`pre-build-readiness.json`](docs/blueprint-v1/machine/pre-build-readiness.json).

## What exists today

The repository currently contains:

- the normative 22-chapter Blueprint;
- twenty-seven detailed engineering and product books;
- requirements, risks, work packages, process capabilities, benchmark, agent-action, ownership, traceability, review, phase, exception, and market-opportunity registries;
- architecture, security, performance, compatibility, AI, product, market, Plug-in, embedding, and professional-buildout research;
- repository validation and documentation-consistency controls;
- a dependency-free Rust prototype modeling process roles, bounded IPC, tab lifecycle transitions, rendering invalidation order, scoped request identity, and deterministic agent authorization.

The prototype does **not** parse HTML, render pages, execute JavaScript, open network connections, create production windows, run Plug-ins, provide an AI assistant, expose an embedding SDK, or support normal browsing.

## Deferred, unsupported, or externally gated

Early milestones explicitly do not claim:

- safe arbitrary-web daily use;
- full Chrome-class compatibility;
- mobile browser support;
- proprietary DRM, patented codec, or vendor-service parity;
- a public Plug-in store;
- full enterprise management;
- optimizing JIT support before interpreter and garbage-collector correctness;
- WebGPU or broad device APIs before GPU and sandbox foundations;
- cloud synchronization before local profile integrity;
- remote AI enabled by default;
- performance leadership without complete reproducible evidence;
- stable SDK, ABI, Plug-in, protocol, or profile compatibility promises.

## Start here

- [Project orientation](docs/start-here.md)
- [Documentation index](docs/README.md)
- [Detailed engineering books](docs/README.md#detailed-engineering-books)
- [Product requirements](docs/blueprint-v1/21-product-requirements.md)
- [Roadmap and milestones](docs/blueprint-v1/14-roadmap-work-breakdown.md)
- [Market strategy](docs/market-strategy/README.md)
- [Active research](docs/research/README.md)
- [Blueprint v1](docs/blueprint-v1/README.md)
- [Professional buildout handbook](docs/project-buildout/README.md)
- [Technology stack](docs/technology-stack/README.md)
- [Plug-in platform](docs/plugins/README.md)
- [Embedding SDK](docs/embedding/README.md)
- [Documentation policy](docs/documentation-policy.md)
- [Repository map](docs/repository-map.md)
- [Security policy](docs/security.md)
- [Contributing](docs/contributing.md)
- [Agent instructions](AGENTS.md)

## Validate the repository

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

## Documentation governance

All durable prose documentation belongs under `docs/`. Every code, configuration, dependency, interface, feature, risk, benchmark, product opportunity, or repository-structure change must update every affected document, index, registry, owner, review rule, and support statement in the same reviewed change.

The detailed documents remain the source of truth. This README is the public feature map and must not silently promote research proposals into implemented or supported features.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent execution and production stability

Turing may be implemented by software agents only through bounded, reviewed tasks. Agents cannot define their own scope, weaken validation, approve or merge their own production changes, access production signing keys, decide vulnerability disclosure, or promote a stable release.

The [Agent Execution book](docs/agent-execution/README.md) defines task manifests, authority, provenance, independent verification, rollback, and escalation. The [Production Readiness book](docs/production-readiness/README.md) defines finite stable scope, supported platforms, release channels, SLOs, update trust, incident response, support, legal approval, and human release authority.

Current status remains **not ready for production or stable release**. Contained architecture and implementation tasks may proceed only under the documented pre-build and agent-execution controls.
