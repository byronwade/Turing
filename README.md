# Turing Browser

Turing is an independent, Rust-first browser and web-engine program focused on minimalism, speed, security, developer experience, accessibility, open integration, and capability-scoped AI.

> **Current status:** M0 research and build-foundation stage. The repository contains extensive architecture and product documentation, a dependency-free architecture prototype, the first buildable production-workspace skeleton, and a complete M0–M9 implementation game plan. It is not yet a usable browser, is not safe for sensitive or hostile browsing, and is not ready for production or stable release.

Release paths must not embed Chromium, WebKit, Gecko, Electron, CEF, an operating-system webview, or remote rendering.

## Build status

The repository is ready for **contained M0 implementation tasks**. Broad parallel construction remains gated by the machine-readable pre-build checklist, accepted dependencies, ADRs, and independent review.

Implemented build foundation:

- a root Cargo workspace using resolver 3;
- Rust `1.97.1`, Rust 2024 for new crates, rustfmt, Clippy, and rust-src pinned by `rust-toolchain.toml`;
- an Ubuntu 24.04 / `x86_64-unknown-linux-gnu` M0 CI reference environment, which is not yet a product-support promise;
- toolkit-neutral typed identity, IPC-envelope, kernel-capability, UI-model, and build-identity crates;
- an M0 `turing-shell` laboratory binary with no native UI or web runtime;
- repository `xtask`, bootstrap, doctor, and full-check commands;
- machine-readable workspace, toolchain, dependency, unsafe-code, native-code, generated-code, provenance, implementation-graph, milestone, interface-freeze, evidence, and task-sequence records;
- CI for documentation, build-foundation validation, formatting, Clippy, workspace tests, shell self-test, and the architecture prototype.

Run:

```bash
sh tools/bootstrap.sh
sh tools/doctor.sh
sh tools/check.sh
```

Equivalent Cargo commands:

```bash
cargo run --locked -p xtask -- bootstrap
cargo run --locked -p xtask -- doctor
cargo run --locked -p xtask -- check
cargo run --locked -p turing-shell -- --self-test
```

The current shell is a command-line laboratory only. It does not create native windows, render pages, connect to the network, persist profiles, run Plug-ins, or execute AI models.

## Implementation game plan

The [Implementation Master Plan](docs/project-buildout/implementation-plan/README.md) is the canonical agent-facing build sequence. It defines:

- the M0 through M9 critical path;
- WP-001 through WP-018 dependencies and execution playbooks;
- required ADR and dependency gates;
- interface freeze points;
- exact agent startup, stop, review, rollback, and handoff rules;
- milestone entry, deliverable, exit-evidence, and prohibited-claim contracts;
- security, privacy, performance, accessibility, compatibility, reliability, operational, and documentation evidence classes;
- staffing and scope-reduction rules;
- preview, beta, stable, and continuous-maintenance sequencing.

The plan does not authorize one agent to build the entire browser as one task. An agent implements only a reviewed `TASK-*` manifest whose dependencies are accepted on `main`.

## M0 workspace

| Package | Purpose | Current status |
|---|---|---|
| `turing-types` | Stable non-zero typed identities | Buildable M0 foundation |
| `turing-build-info` | Build identity and maturity labels | Buildable M0 foundation |
| `turing-ipc` | Typed bounded control envelopes | Buildable schema foundation; no production wire transport yet |
| `turing-kernel` | Process roles and deny-by-default capabilities | Buildable policy skeleton |
| `turing-ui-model` | Toolkit-neutral shell snapshots and commands | Buildable UI contract skeleton |
| `turing-shell` | M0 shell laboratory | No native UI yet |
| `xtask` | Bootstrap, doctor, and validation commands | Active repository tool |
| `turing-architecture-prototype` | Earlier executable invariant model | Research-only prototype |

The authoritative component and dependency map is [`workspace-components.json`](docs/blueprint-v1/machine/workspace-components.json).

## Why Turing

Turing is designed around six differentiators:

1. **Independent standards-driven engine.** Rust-first ownership, explicit process boundaries, and audited foundations rather than a shell around an existing browser.
2. **Project-native browsing.** Spaces can eventually own organization, identity, recovery, tools, resource policy, and scoped agent authority.
3. **Explainable performance.** CPU, memory, GPU, network, disk, energy, Plug-in, and model costs are attributed to their semantic owners.
4. **Trustworthy AI.** Models are untrusted principals; deterministic browser policy controls observations and actions.
5. **Developer-grade causality.** Tooling explains why rendering, networking, storage, lifecycle, security, and agent decisions occurred.
6. **Open integration.** Capability-bounded Plug-ins and a stable multi-language embedding contract.

> **Product hypothesis:** Turing is the open project browser for people and agents: it remembers the work, explains the cost, and keeps the user in control.

## Feature status

| Status | Meaning |
|---|---|
| **Buildable foundation** | Source exists and passes the M0 workspace checks |
| **Prototype** | Represented only by a research or architecture prototype |
| **Accepted direction** | Normative Blueprint or requirement; generally not implemented |
| **Proposed opportunity** | `OP-*` market hypothesis requiring evidence and promotion |
| **Deferred or gated** | Postponed or dependent on licensing, platform, staffing, or commercial access |

Canonical status lives in the [requirements](docs/blueprint-v1/machine/requirements.json), [work-package graph](docs/blueprint-v1/machine/backlog.json), [implementation execution graph](docs/blueprint-v1/machine/implementation-execution-graph.json), [roadmap](docs/blueprint-v1/14-roadmap-work-breakdown.md), [pre-build readiness](docs/blueprint-v1/machine/pre-build-readiness.json), [market opportunities](docs/market-strategy/machine/feature-opportunities.json), and [production release gates](docs/production-readiness/machine/release-gates.json).

## Planned browser surface

### Everyday shell

Accepted direction includes windows, profiles, private sessions, tabs, groups, folders, horizontal or vertical tab presentation, Spaces, address/search/command entry, history, bookmarks, downloads, credentials, permissions, printing, page information, settings, updates, side panels, web applications, crash recovery, safe mode, keyboard operation, IME, clipboard, drag-and-drop, and accessible trusted chrome.

### Market-differentiation research

| ID | Proposed capability |
|---|---|
| `OP-001` | Turing Spaces |
| `OP-002` | Workspace Time Machine |
| `OP-003` | Resource Truth Center |
| `OP-004` | Trustworthy Agent Mode |
| `OP-005` | Research and Comparison Canvas |
| `OP-006` | Identity Routing and Context Firewall |
| `OP-007` | High-fidelity Migration and Open Portability |
| `OP-008` | Plug-in Trust Platform |
| `OP-009` | Developer Causal Mode |
| `OP-010` | Encrypted Collaborative Spaces |
| `OP-011` | Web App Fabric |
| `OP-012` | Privacy Receipts and Content Authenticity |
| `OP-013` | Accessibility and Focus Differentiation |
| `OP-014` | Cross-Device Continuity Without Lock-In |

These remain proposals, not implemented or accepted requirements.

### Performance and reliability

The program targets a responsive browser UI during renderer failures and 30-tab pressure, explicit Active/Background/Frozen/Discarded/Restoring lifecycle states, protected unsaved work, predictable revival, complete resource attribution, bounded queues and caches, fixed-hardware measurement, transactional storage, crash diagnostics, and signed rollback-capable updates.

### Security and privacy

The architecture requires deny-by-default processes, site isolation, typed bounded IPC, platform sandbox evidence, brokered files and devices, isolated profiles, secret-preserving credential brokers, web-security policy, hostile parser/codec/JIT/GPU containment, reproducible signed updates, anti-phishing and trusted UI, minimal telemetry, private vulnerability handling, and independent review.

### Independent engine

The long-term engine covers HTML, DOM, CSS, layout, text, paint, raster, compositing, accessibility, JavaScript, garbage collection, WebAssembly, Fetch, HTTP, QUIC, TLS, cookies, cache, storage, service workers, media, PDF, printing, workers, permissions, and standards conformance.

### Developer platform

Planned tools include Elements, Styles, Layout, Accessibility, Console, Sources, Network, Performance, Memory, Storage, Security, Service Workers, Rendering, Protocol, and Issues; WebDriver BiDi; deterministic headless profiles; virtual time; fault injection; causal traces; replay; reduction; and generated protocol clients.

### AI and agents

The optional assistant and agent platform uses visible provider choice, scoped semantic observations, redaction, typed actions, browser-enforced grants, trusted confirmation, stop and revoke, browser-held secrets, isolated task profiles, prompt-injection evaluation, local-model budgets, and capability-mediated tools.

### Turing Plug-ins

Turing calls extensions **Plug-ins**. Proposed execution tiers include isolated first-party packages, WebAssembly Component Model packages with WIT capabilities, a restricted WebExtensions adapter, and visible developer-only packages.

The initial product-research portfolio contains Turing Assistant, Developer Copilot, Screenshot Studio, Interaction Recorder, translation, reading and writing tools, dark/contrast/focus modes, privacy inspection, filter lists, workspace organization, notes and clipping, archive/export, JSON/API inspection, accessibility inspection, performance profiling, framework inspection, shopping comparison, and meeting/media notes.

### Embedding

The planned embedding surface uses an idiomatic Rust API, a minimal opaque C ABI, generated SDKs for major languages, explicit lifecycle and cancellation, interactive/offscreen/headless modes sharing one security model, signed packages, provenance, and host conformance.

### Native shell

Trusted chrome will not ship Electron, Tauri, a system webview, React, Node, a DOM, or a runtime browser CSS engine. Pure Rust owns state and commands; a replaceable native adapter owns presentation. Slint is the first candidate to prototype against Vizia and Floem or GPUI. No toolkit is selected.

## What remains before broad M1 expansion

- accepted Servo/source strategy;
- production UI toolkit and page-surface composition;
- product support platform matrix;
- canonical generated IPC wire transport and negative harness;
- packaged sandbox evidence;
- fixed-hardware benchmark infrastructure;
- design tokens and component fixtures;
- profile, Space, session, and migration formats;
- updater and signed package laboratories;
- qualified backup maintainers;
- beta or stable release gates.

Contained tasks can proceed; broad parallel implementation and production claims remain blocked until their gates pass.

## Start here

- [Implementation master plan](docs/project-buildout/implementation-plan/README.md)
- [Documentation index](docs/README.md)
- [Pre-build readiness](docs/project-buildout/11-pre-build-readiness-checklist.md)
- [M0 build-foundation report](docs/research/m0-build-foundation-2026-07.md)
- [Blueprint v1](docs/blueprint-v1/README.md)
- [Roadmap](docs/blueprint-v1/14-roadmap-work-breakdown.md)
- [Agent execution](docs/agent-execution/README.md)
- [Production readiness](docs/production-readiness/README.md)
- [Native UI](docs/ui-runtime/README.md)
- [Technology stack](docs/technology-stack/README.md)
- [Repository map](docs/repository-map.md)
- [Security policy](docs/security.md)
- [Contributing](docs/contributing.md)
- [Agent instructions](AGENTS.md)

## Documentation governance

All durable prose belongs under `docs/`. Every code, configuration, dependency, interface, feature, risk, benchmark, or repository-structure change must update every affected document, registry, owner, review rule, and support statement in the same reviewed change.
