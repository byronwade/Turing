# Turing Browser

Turing is an independent, Rust-first browser and web-engine program focused on minimalism, speed, security, developer experience, accessibility, open integration, and capability-scoped AI.

> **Current status:** M0 research and implementation stage. The repository contains extensive architecture and product documentation, a dependency-free architecture prototype, a buildable workspace, and the first generated kernel/IPC policy reference. The active WP-002 execution manifest is `TASK-000011` and remains `review_pending`, not accepted; its [review handoff](docs/research/task-000011-wp002-review-handoff-2026-07.md) is an evidence map, not an approval. Turing is not yet a usable browser, is not safe for sensitive or hostile browsing, and is not ready for production or stable release.

Release paths must not embed Chromium, WebKit, Gecko, Electron, CEF, an operating-system webview, or remote rendering.

## Current stop/resume path

Start with [`docs/start-here.md`](docs/start-here.md). It is the first human entry point for the current build-preparation state.

Before continuing implementation work:

- confirm gate truth in the [Build Readiness Operating Board](docs/project-buildout/13-build-readiness-operating-board.md), [Pre-build Readiness Checklist](docs/project-buildout/11-pre-build-readiness-checklist.md), [Documentation Readiness Evidence Matrix](docs/project-buildout/18-documentation-readiness-evidence-matrix.md), and machine [`pre-build-readiness.json`](docs/blueprint-v1/machine/pre-build-readiness.json);
- use the checked [Implementation Kickoff Review Inventory](docs/research/implementation-kickoff-review-inventory-2026-07.md) before broadening work across unresolved `PB-*` lanes; it is a no-claim stop/resume inventory, not task approval or readiness promotion;
- use the checked [Build Readiness Dependency Graph](docs/research/build-readiness-dependency-graph-inventory-2026-07.md) before changing task order, task dependencies, or cross-lane sequencing;
- use the checked [Documentation Readiness Completion Audit](docs/research/documentation-readiness-completion-audit-2026-07.md) and checked no-claim [build-readiness closure-review template](docs/project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json) before calling the documentation preparation complete; they prove contained-M0 continuation only and explicitly keep all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, and accessibility claims unsupported;
- use the checked [Chrome-Class Capability Traceability Map](docs/research/chrome-class-capability-traceability-map-2026-07.md) to route Chrome-class product, engine, security, accessibility, DevTools, AI, update, and performance domains to current owners, blockers, next proof, and no-claim boundaries without treating that map as capability evidence;
- use the [Implementation Master Plan](docs/project-buildout/implementation-plan/README.md) only as dependency-ordered execution documentation for reviewed, bounded tasks; it does not approve broad implementation or any release path;
- use the checked [GitHub Issue Handoff](docs/project-buildout/19-github-issue-handoff.md) after issue or branch cleanup to map live coordination issues to `WP-*`, `PB-*`, and `TASK-*` records without treating open or closed issues as task approval or readiness promotion;
- use the [core program registries](docs/repository-map.md#core-program-registries) before changing requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas;
- choose the next source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership evidence lane and `RQ-*` crosswalk from the [Research Index](docs/research/README.md#current-implementation-research-lanes);
- use the proposed [Build Readiness Task Queue](docs/project-buildout/17-build-readiness-task-queue.md) and checked no-claim [task approval template](docs/agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json) only to shape reviewed task manifests;
- resolve the `ADR-0009` source-strategy blocker through the [source packet](docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md), [evidence matrix](docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md), [decision draft](docs/project-buildout/16-adr-0009-decision-draft.md), and checked no-claim [decision-review template](docs/blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json);
- continue fresh-host build confidence from the checked [Fresh Host Reproduction Inventory](docs/research/fresh-host-reproduction-inventory-2026-07.md), checked [fresh-host run-record template](docs/project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json), and checked no-claim [fresh-host readiness-review template](docs/project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json), but treat independent reproduction, owner-approved clean-VM equivalence, owner-reviewed fresh-host readiness, `PB-009` readiness, preview/beta/stable readiness, production readiness, release confidence, implementation, and Chrome-class claims as unproven;
- continue IPC work from the checked [IPC Capability Boundary Inventory](docs/research/ipc-capability-boundary-inventory-2026-07.md), [WP-002 kernel identity and IPC reference](docs/research/wp-002-kernel-ipc-2026-07.md), [TASK-000011 WP-002 review handoff](docs/research/task-000011-wp002-review-handoff-2026-07.md), checked no-claim [TASK-000011 evidence capture](docs/agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json), checked no-claim [IPC schema-source template](docs/blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), and checked no-claim [IPC readiness-review template](docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json), but keep `TASK-000011` acceptance, accepted independent evidence bundle, wire encoding, timeout/cancellation behavior, owner-reviewed IPC readiness, `PB-011` readiness, renderer-security, agent-security, process-isolation, site-isolation, production IPC, and implementation claims as unproven;
- continue sandbox work from the checked [Sandbox Probe Inventory](docs/research/sandbox-probe-inventory-2026-07.md), checked [WP-003 Sandbox Probe Contract](docs/research/wp-003-sandbox-probe-plan-2026-07.md), checked no-claim [sandbox probe-package template](docs/security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), and checked no-claim [sandbox readiness-review template](docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json), but treat packaged probes, stable operation/evidence contract execution, effective platform policy, owner-reviewed sandbox readiness, sandbox readiness, renderer security, site isolation, hostile-browsing safety, SEC-GATE evidence, production safety, and implementation claims as unproven;
- continue native-shell adapter-contract work from the checked [Toolkit-Neutral UI Adapter Contract Inventory](docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md), but treat `ADR-0013`, native adapter prototypes, complete state/command/surface/accessibility/diagnostic/adapter contracts, no-toolkit-owned-authority negative tests, trusted-chrome readiness, accessibility readiness, page-surface approval, toolkit selection, and release-path UI approval as unproven;
- continue native-shell framework work from the checked [Native UI Framework Bake-Off Inventory](docs/research/native-ui-framework-bakeoff-inventory-2026-07.md), but treat `ADR-0014`, toolkit selection, equivalent adapter runs, accessibility, IME/keyboard, page-surface, crash/GPU-loss, performance, memory, energy, license/provenance, and release-path UI approval as unproven;
- continue native-shell page-surface work from the checked [Page Surface Composition Inventory](docs/research/page-surface-composition-inventory-2026-07.md), but treat `UI-GATE-7`, `ADR-0016`, typed/brokered surface handles, renderer-texture composition, compositor ownership, resize/scale/damage, capture, crash/GPU-loss, software fallback, and latency/frame-pacing proof as unproven;
- continue native-shell accessibility work from the checked [Window Input Accessibility Spike Inventory](docs/research/window-input-accessibility-spike-inventory-2026-07.md), but treat reference-platform workflows, manual assistive-technology coverage, page-tree composition, IME correctness, renderer-hang, crash, GPU-loss, and accessibility readiness as unproven;
- continue profile/session schema work from the checked [Profile Session Format Inventory](docs/research/profile-session-format-inventory-2026-07.md) and checked no-claim [schema-package template](docs/storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json), but treat executable profile, Space, session, snapshot, migration, real-profile migration, sync, credential storage, data-loss safety, user-data handling, and production profile-format behavior as unproven;
- treat Chrome-class and extreme-performance work as no-claim evidence until the [Performance Benchmark Readiness Packet](docs/research/performance-benchmark-readiness-packet-2026-07.md), [Benchmark Corpus Expansion](docs/research/benchmark-corpus-expansion-2026-07.md), [Chrome-Class Performance Runbook](docs/research/chrome-class-performance-runbook-2026-07.md), [Benchmark Engine Baseline Harness Readiness Map](docs/research/benchmark-engine-baseline-harness-readiness-map-2026-07.md), benchmark manifests, server lifecycle evidence, browser-pin records, diagnostics, launch-runner contract and self-test evidence, raw artifacts, statistics, the checked no-claim [claim-bundle template](docs/blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json), checked no-claim [benchmark readiness-review template](docs/blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json), owner-reviewed claim bundles, and owner-reviewed benchmark readiness exist.

This path supports contained M0 and no-claim evidence work only. It does not approve broad M1 implementation, Servo adoption, benchmark-ready browser pins, Chrome-class comparison, speed, memory, energy, compatibility, security, accessibility, production, beta, stable, or daily-driver claims.

## Build status

The repository is now ready for **contained M0 implementation tasks**. The documentation library currently contains twenty-seven detailed engineering and product books, including native UI, agent-execution, production-readiness, build-readiness, research, and validation controls.

Implemented foundation:

- a root Cargo workspace using resolver 3;
- Rust `1.97.1`, Rust 2024 for new crates, rustfmt, Clippy, and rust-src pinned by `rust-toolchain.toml`;
- an Ubuntu 24.04 / `x86_64-unknown-linux-gnu` M0 CI reference environment, which is not yet a product-support promise;
- restart-safe typed process identities;
- a canonical JSON control-plane schema generating process roles, capabilities, launch rights, message kinds, route allowlists, document-scope rules, size limits, and queue budgets;
- bounded envelopes, broker-registered channels, exact channel sequence validation, stable admission-time queue charging, explicit backpressure, and no silent eviction;
- a deny-by-default kernel registry that rejects stale epochs, unauthorized launches, capability escalation, invalid routes, reused channel endpoints, and missing capabilities;
- toolkit-neutral UI-model and build-identity crates;
- an M0 `turing-shell` laboratory that exercises the kernel/IPC reference model without a native UI or web runtime;
- repository `xtask`, bootstrap, doctor, generation, and full-check commands;
- machine-readable workspace, toolchain, dependency, unsafe-code, native-code, generated-code, provenance, capability, and traceability records;
- CI for documentation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation, deterministic generation, committed-diff whitespace, build-foundation validation, evidence-bundle validation, formatting, Clippy, workspace tests, shell self-test, and the architecture prototype.

Aggregate checks include CI for documentation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation, committed-diff whitespace, build-foundation validation, evidence-bundle validation, deterministic generation, formatting, Clippy, workspace tests, shell self-test, and the architecture prototype.

Run on POSIX shells:

```bash
sh tools/bootstrap.sh
sh tools/doctor.sh
sh tools/check.sh
```

Run on Windows PowerShell:

```powershell
.\tools\bootstrap.ps1
.\tools\doctor.ps1
.\tools\check.ps1
```

Equivalent Cargo and generator commands:

```bash
python3 -B tools/generate_ipc.py --check
cargo run --locked -p xtask -- bootstrap
cargo run --locked -p xtask -- doctor
cargo run --locked -p xtask -- check
cargo run --locked -p turing-shell -- --self-test
```

Use the wrappers for handoff validation when possible. Direct Cargo commands are behavior-equivalent, but they inherit the caller's `CARGO_TARGET_DIR`; set it outside the repository when source-tree cleanliness evidence matters.

`xtask check` runs documentation validation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation, build-foundation validation, evidence-bundle validation, local unstaged and staged diff whitespace checks, Rust formatting, Clippy with warnings denied, workspace tests, the shell self-test, and the architecture prototype smoke path.

The current shell is a command-line laboratory only. It does not create native windows, render pages, connect to the network, persist profiles, run Plug-ins, or execute AI models.

## M0 workspace

| Package | Purpose | Current status |
|---|---|---|
| `turing-types` | Stable non-zero IDs and restart-safe process identities | Buildable M0 reference |
| `turing-build-info` | Build identity and maturity labels | Buildable M0 foundation |
| `turing-ipc` | Generated roles/messages, bounded envelopes, queues, and sequence state | Buildable policy reference; no OS transport or wire codec yet |
| `turing-kernel` | Process registry, launch policy, capability attenuation, and message authorization | Buildable deterministic policy oracle; no OS launcher yet |
| `turing-ui-model` | Toolkit-neutral shell snapshots and commands | Buildable UI contract skeleton |
| `turing-shell` | M0 integration laboratory | No native UI yet |
| `xtask` | Bootstrap, doctor, generation, and validation commands | Active repository tool |
| `turing-architecture-prototype` | Earlier executable invariant model | Research-only prototype |

The authoritative component and dependency map is [`workspace-components.json`](docs/blueprint-v1/machine/workspace-components.json). The canonical generated control-plane source is [`schemas/ipc/control-plane.json`](schemas/ipc/control-plane.json).

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
| **Buildable reference** | Source exists and passes the M0 workspace checks, but platform integration and independent verification may remain |
| **Prototype** | Represented only by a research or architecture prototype |
| **Accepted direction** | Normative Blueprint or requirement; generally not implemented |
| **Proposed opportunity** | `OP-*` market hypothesis requiring evidence and promotion |
| **Deferred or gated** | Postponed or dependent on licensing, platform, staffing, or commercial access |

Canonical status lives in the [requirements](docs/blueprint-v1/machine/requirements.json), [traceability](docs/blueprint-v1/machine/professional-traceability.json), [roadmap](docs/blueprint-v1/14-roadmap-work-breakdown.md), [pre-build readiness](docs/blueprint-v1/machine/pre-build-readiness.json), [market opportunities](docs/market-strategy/machine/feature-opportunities.json), and [production release gates](docs/production-readiness/machine/release-gates.json).

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

The program targets a responsive browser UI during renderer failures and 30-tab pressure, explicit Active/Background/Frozen/Discarded/Restoring lifecycle states, protected unsaved work, predictable revival, complete resource attribution, bounded queues and caches, fixed-hardware measurement, transactional storage, crash diagnostics, and signed rollback-capable updates. The M0 control plane now demonstrates count and byte budgets with explicit backpressure; production values still require workload measurement.

### Security and privacy

The architecture requires deny-by-default processes, site isolation, typed bounded IPC, platform sandbox evidence, brokered files and devices, isolated profiles, secret-preserving credential brokers, web-security policy, hostile parser/codec/JIT/GPU containment, reproducible signed updates, anti-phishing and trusted UI, minimal telemetry, private vulnerability handling, and independent review. The M0 kernel now provides a deterministic process/capability/route policy oracle, but it is not an operating-system sandbox or transport.

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

Trusted chrome will not ship Electron, Tauri, a system webview, React, Node, a DOM, or a runtime browser CSS engine. Pure Rust owns state and commands; a replaceable native adapter owns presentation. The checked [Toolkit-Neutral UI Adapter Contract Inventory](docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md) records the no-claim `PB-003` state, command, surface, accessibility, diagnostic, adapter, and denied-authority boundaries. Slint is the first candidate to prototype against Vizia and Floem or GPUI, and the checked [Native UI Framework Bake-Off Inventory](docs/research/native-ui-framework-bakeoff-inventory-2026-07.md) defines the no-claim evidence axes. No toolkit is selected.

## What remains before M1

The M0 workspace still does not resolve:

- the Servo/source strategy;
- toolkit-neutral adapter-contract proof beyond the checked no-claim inventory;
- production UI toolkit selection beyond the checked no-claim framework bake-off inventory;
- page-surface/compositor composition beyond the checked no-claim inventory;
- a product support platform matrix;
- an operating-system IPC transport and canonical wire codec;
- channel authentication and shared-memory handle transfer on each platform;
- packaged sandbox probes, compromised-process tests, and owner-reviewed sandbox readiness beyond the checked no-claim Sandbox Probe Inventory, sandbox probe-package template, and sandbox readiness-review template;
- fixed-hardware benchmark infrastructure and production queue budgets;
- rendered design-token/component fixtures beyond the checked no-claim inventory;
- reference-platform window/input/IME/accessibility/page-tree workflows and manual assistive-technology coverage beyond the checked no-claim inventory;
- executable profile, Space, session, snapshot, and migration schemas beyond the checked no-claim schema-package template;
- executable updater and signed research-package laboratories beyond the checked no-claim update-lab package template;
- executable incident-response and emergency patch rehearsal beyond the checked no-claim incident patch rehearsal template;
- qualified backup maintainers beyond the checked [Backup Ownership Gap Inventory](docs/research/backup-ownership-gap-inventory-2026-07.md) and checked no-claim backup-owner qualification template;
- beta or stable release gates.

Contained tasks can proceed; broad parallel implementation and production claims remain blocked.

## Start here

- [Start here](docs/start-here.md)
- [Documentation index](docs/README.md)
- [Research index](docs/research/README.md)
- [Build readiness operating board](docs/project-buildout/13-build-readiness-operating-board.md)
- [Pre-build readiness](docs/project-buildout/11-pre-build-readiness-checklist.md)
- [Build readiness task queue](docs/project-buildout/17-build-readiness-task-queue.md)
- [GitHub issue handoff](docs/project-buildout/19-github-issue-handoff.md)
- [M0 build-foundation report](docs/research/m0-build-foundation-2026-07.md)
- [WP-002 kernel and IPC report](docs/research/wp-002-kernel-ipc-2026-07.md)
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
