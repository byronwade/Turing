# 21 — Product Requirements Document

## Problem

Mainstream browsers provide broad compatibility and strong security investment, but users and developers often experience high memory use under large tab sets, opaque resource ownership, limited lifecycle control, developer tooling separated from everyday workflows, and AI automation layered on top without a browser-native authority model.

Turing investigates whether an independent engine and product architecture can improve memory accountability, developer experience, UI quality, and agent safety without sacrificing the long-term capability surface expected of a general-purpose browser.

## Users

### Everyday user

Needs fast startup, reliable sites, clear security and permission state, accessible controls, credentials, downloads, media, printing, profiles, privacy, crash recovery, and updates. Does not want to understand process topology or AI policy to browse safely.

### Power user

Keeps dozens of tabs and workspaces, expects keyboard control, search, organization, resource visibility, strong recovery, and explicit keep-active/discard controls.

### Web developer

Needs accurate DOM/CSS/layout/network/runtime/accessibility inspection, deterministic debugging, performance and memory attribution, automation, local-workspace integration, and reproducible test profiles.

### Agent developer

Needs a stable semantic observation and action protocol, explicit scopes, structured outcomes, deterministic policy reason codes, headless parity, and adversarial test support.

### Enterprise administrator

Eventually needs supported releases, policy, deployment, proxy/certificate/update control, audit, extension management, data controls, accessibility, and rapid security response.

## Jobs to be done

- Open everyday sites and applications without learning a new browsing model.
- Keep 30+ tabs without losing work or letting background pages dominate the machine.
- Understand which tab, worker, extension, or agent uses resources.
- Recover after a page, process, GPU, update, or browser failure.
- Inspect and debug a page from the same truth used by the engine.
- Let an agent perform a bounded task while seeing exactly what it can observe and what it proposes to do.
- Stop, review, or revoke an agent before consequential effects.
- Compare performance and compatibility through reproducible evidence.

## Product principles

- Familiar by default; powerful by disclosure.
- Security state is never traded for minimal visual chrome.
- Low memory is lifecycle-aware and honest.
- The browser remains usable when page processes fail.
- Accessibility and internationalization are architecture, not polish.
- Agents have less authority than the user and cannot mint more.
- Developer tools use versioned engine protocols.
- Unsupported behavior is visible.

## Functional requirements

### Browsing shell

- multiple windows, profiles, private sessions, tabs, groups, and workspaces;
- address/search/command field with clearly separated result types;
- history, bookmarks, downloads, settings, credentials, extensions, page info, and updates;
- navigation, reload/stop, history traversal, zoom, find, print, save, view source, and external-handler policy;
- keyboard, pointer, touch/pen where supported, IME, drag/drop, clipboard, native menus, and system integration;
- session recovery and crash-loop handling.

### Resource behavior

- show CPU, memory categories, GPU, network, disk, energy estimate, lifecycle, process, site instance, worker, extension, and agent attribution;
- allow keep-active, freeze, discard, inspect, trace, and kill with clear data-loss warnings;
- protect audio, calls, capture, transfers, devices, unsaved work, debugging, and active confirmations;
- revive frozen/discarded tabs predictably and indicate reload/state loss.

### Web engine

- standards-driven HTML, DOM, CSS, layout, paint, graphics, input, editing, accessibility, JavaScript, WebAssembly, networking, storage, workers, media, and device tracks;
- site isolation, security policies, permissions, and sandboxing;
- no existing browser engine in release rendering path.

### Developer platform

- Elements, Styles, Layout, Accessibility, Console, Sources, Network, Performance, Memory, Storage, Security, Application/Service Worker, Rendering, Protocol, and Issues tools;
- remote debugging and WebDriver BiDi track;
- deterministic headless/test profiles, virtual time, emulation, fault injection, trace diff, and reduced-test generation;
- local workspace handles with explicit grants.

### AI and agents

- optional assistant that can explain, summarize, find, organize, and perform approved actions;
- provider choice, local/remote visibility, data-flow manifest, budgets, and no silent fallback;
- semantic snapshots, redaction, origin labels, document epochs, action schemas, risk classes, confirmation, stop, revoke, and audit;
- secrets stay in browser brokers; models receive handles or availability indicators;
- developer agents can inspect engine diagnostics under a separate developer grant.

## Nonfunctional requirements

### Security

- deny-by-default multi-process architecture, OS sandbox evidence, typed/bounded IPC, site isolation, signed updates, vulnerability response, supply-chain controls, and independent review before stable.

### Performance

- responsive browser UI under renderer hangs and 30-tab pressure;
- published startup/input/frame/page/memory/energy benchmarks;
- bounded queues/caches, semantic allocation ownership, pressure escalation, and no dormant-model resource reservation.

### Reliability

- process containment, transactional storage/migrations, session journal, update rollback, fault injection, crash diagnostics, and no unsafe automatic replay of consequential actions.

### Accessibility

- native semantic browser UI and web accessibility tree; keyboard/screen-reader/voice/switch/magnification/high-contrast/reduced-motion support; release-blocking critical-flow defects.

### Privacy

- profiles/private sessions separated; minimal opt-in telemetry; sensitive values absent from routine logs/crashes/model payloads; clear remote-provider behavior.

### Compatibility

- pinned WPT/Test262 and other suite revisions; pass/fail/crash/timeout denominator; explicit proprietary and platform gaps; no user-agent-only claim.

### Maintainability

- Rust-first types, documented unsafe code, dependency ledger, generated protocols, stable IDs, ADRs, ownership, reproducible builds, SBOM/provenance, and support limits.

## Initial UX

The first usable shell opens to a simple window with:

- tab strip and address/command field;
- page surface backed initially by a test renderer;
- profile indicator;
- side panel toggle;
- resource indicator that expands into process/tab attribution;
- agent control that is disabled until a provider and grants are configured;
- DevTools toggle;
- clear “research build” status.

The shell must remain interactive when the test renderer hangs or crashes.

## Success metrics by maturity

### Research

- architecture invariants compile and tests pass;
- sandbox probes and process/lifecycle simulator produce evidence;
- static document subset grows through conformance, not screenshots;
- all claims carry maturity labels.

### Developer preview

- signed auto-updating packages;
- renderer sandbox and site-isolation subset verified;
- useful controlled application corpus;
- core DevTools and automation;
- published compatibility/performance/security reports;
- emergency patch workflow.

### Beta

- broad volunteer daily-use compatibility;
- independent security review;
- sustained fuzzing and conformance progress;
- stable profile/update/recovery behavior;
- accessibility and platform matrix;
- bounded extension and agent previews.

### Stable

- documented support/security patch policy;
- broad compatibility and clear proprietary gaps;
- rapid signed updates and incident response;
- no open critical security, data-loss, update, spoofing, or unauthorized-agent-action issues;
- independent security and accessibility evidence.

## Explicit non-goals for early milestones

- claiming safe arbitrary-web daily use;
- mobile browser support;
- proprietary DRM or vendor account/service parity;
- a public extension store;
- full enterprise management;
- optimizing JIT before interpreter/GC correctness;
- WebGPU and broad device APIs before GPU/sandbox foundations;
- sync/cloud services before local profile integrity;
- remote AI enabled by default;
- performance headlines without complete manifests.

## Product launch blockers

- no effective renderer sandbox or site isolation;
- no signed rapid update path;
- credential/cross-origin/profile leak;
- browser UI spoofing in security or agent confirmations;
- data-loss migration or lifecycle bug;
- inaccessible origin/permission/confirmation workflows;
- unbounded agent or extension authority;
- unsupported proprietary behavior presented as parity;
- team cannot maintain supported releases.

<!-- MARKET-STRATEGY-2026-07 -->
## Proposed market opportunities — non-normative

The following remain research proposals, not accepted `REQ-*` entries: `OP-001` Spaces, `OP-002` Time Machine, `OP-003` Resource Truth Center, `OP-004` Trustworthy Agent Mode, `OP-005` Research Canvas, `OP-006` Identity Routing, `OP-007` Migration/Portability, `OP-008` Plug-in Trust Platform, `OP-009` Developer Causal Mode, `OP-010` Collaborative Spaces, `OP-011` Web App Fabric, `OP-012` Privacy Receipts/Authenticity, `OP-013` Accessibility/Focus differentiation, and `OP-014` lock-in-free continuity.

Promotion requires validated user value, architecture and threat review, measurable acceptance criteria, owner, milestone, risk mapping, and synchronized machine requirements.
