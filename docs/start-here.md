# Turing Browser Program — Start Here

Turing is the working codename for an independent, Rust-first browser and web-engine program. The project is deliberately not a Chromium, WebKit, Gecko, Electron, CEF, operating-system web-view, or remote-rendering wrapper.

The long-term target is broad modern-web compatibility, a materially lower and more accountable resource footprint under large tab sets, developer-grade tooling, a restrained native interface, and an AI-agent surface designed as a security boundary rather than hidden automation.

This repository is an architecture, research, and execution baseline, not a production browser. A browser that safely handles arbitrary hostile web content is an operating-system-scale project. Every release must state exactly which standards, security controls, media formats, accessibility functions, extension APIs, enterprise controls, platform integrations, and update obligations are implemented and independently tested.

## Reading order

1. [Documentation policy](documentation-policy.md)
2. [Blueprint v1 index](blueprint-v1/README.md)
3. [Charter and principles](blueprint-v1/01-charter-and-principles.md)
4. [Capability parity](blueprint-v1/02-capability-parity.md)
5. [Language and dependency strategy](blueprint-v1/03-language-and-dependency-strategy.md)
6. [System architecture](blueprint-v1/04-system-architecture.md)
7. [Security and sandbox](blueprint-v1/08-security-and-sandbox.md)
8. [Performance and memory](blueprint-v1/09-performance-memory.md)
9. [AI and agent platform](blueprint-v1/10-ai-agent-platform.md)
10. [Roadmap and work breakdown](blueprint-v1/14-roadmap-work-breakdown.md)
11. [Pre-build readiness checklist](project-buildout/11-pre-build-readiness-checklist.md)
12. [Build readiness start guide](project-buildout/21-build-readiness-start-guide.md)
13. [Build continuity readiness pack](project-buildout/20-build-continuation-readiness-pack.md)
14. [Build readiness operating board](project-buildout/13-build-readiness-operating-board.md)
15. [Build readiness task queue](project-buildout/17-build-readiness-task-queue.md)
16. [Implementation master plan](project-buildout/implementation-plan/README.md)
17. [Risk register](blueprint-v1/15-risk-register.md)
18. [Detailed engineering books](README.md#detailed-engineering-books)
19. [Active research](research/README.md)
20. [Repository map](repository-map.md)

The Blueprint is the normative overview. The detailed books expand implementation research and evidence requirements without silently changing accepted decisions.

## Non-negotiable definitions

**Independent engine** means Turing owns the DOM, CSS/style system, layout, display-list construction, browser process model, navigation lifecycle, JavaScript integration, permissions, storage partitioning, developer tooling, and agent protocol. It does not mean reimplementing cryptography, Unicode tables, font shaping, image codecs, compression, or operating-system sandbox primitives without a security justification.

**Chrome-class capability** is a tracked destination, never a marketing shortcut. It includes the web platform, accessibility, internationalization, media, printing, PDF, downloads, credentials, extensions, developer tools, automation, sync, updates, enterprise policy, crash recovery, security response, and distribution—not merely successful page rendering.

**Low memory** means measured private working set and resident memory on a published workload, with tab lifecycle, process count, site-isolation state, page types, background activity, and discard policy disclosed. Discarding most tabs is not represented as equivalent to keeping hostile sites fully live.

**AI assistance** is capability-scoped. Models do not receive ambient access to cookies, credentials, cross-origin content, downloads, local files, clipboard, camera, microphone, payments, messages, or destructive actions. Page content and model output cannot expand authority. Consequential operations require deterministic policy checks and visible confirmation where specified.

**Beautiful UI** means a restrained, coherent, accessible, platform-appropriate interface with excellent keyboard behavior, diagnostics, and latency. Visual polish does not excuse hidden work, inaccessible controls, excessive memory, or misleading security states.

**Number one** means a current, reproducible, multi-dimensional result across compatibility, latency, memory, energy, security, accessibility, stability, developer APIs, everyday usability, and open-source health. It never means one synthetic benchmark or a comparison with unequal feature/security settings.

## Current documentation state

The repository currently contains:

- the normative product and engineering Blueprint;
- twenty-seven detailed engineering, product, operating, and competitive research books;
- dated engine-landscape, market, Servo/source-strategy, readiness, and documentation-gap research;
- a human build-readiness operating board plus machine-readable pre-build gates;
- machine-readable requirements, risks, work packages, process capabilities, benchmark and agent-action schemas;
- repository validation and documentation-governance checks;
- a dependency-free Rust architecture prototype.

Detailed books now cover networking, storage, media/documents, native platforms, accessibility, release operations, extensions/enterprise/sync, open-web governance, benchmark operations, quality assurance, everyday product experience, browser-engine internals, JavaScript runtime/compiler design, security containment and response, DevTools/developer workflows, API conventions, performance/memory/energy, AI agents and tools, and competitive engine/product studies. These are research and design baselines, not evidence that the systems exist.

## Current implementation state

The prototype encodes typed process roles, bounded messages, legal tab lifecycle transitions, ordered rendering stages, scoped network identity, and deterministic agent authorization. The first contained source task, [`TASK-000011`](agent-execution/machine/tasks/TASK-000011.json), has implemented the M0 reference portion of `WP-002` and is `review_pending`; the [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md) maps candidate evidence for independent review, and the checked no-claim [TASK-000011 evidence capture](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json) binds candidate artifacts to the green source commit. Neither record is acceptance, an independent evidence-bundle decision, or production readiness. The prototype does not parse HTML, render pages, execute JavaScript, create native windows, or open network connections.

## Current build-readiness state

Turing is ready for contained M0 implementation tasks only. It is not ready for broad M1 expansion, developer preview, beta, stable release, or Chrome-class claims.

Use this stop/resume map before continuing:

- Status and gate truth: use the [Build Readiness Start Guide](project-buildout/21-build-readiness-start-guide.md) first, then the [Build Continuation Readiness Pack](project-buildout/20-build-continuation-readiness-pack.md), [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md), [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md), [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md), and machine [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json).
- Implementation kickoff continuity: use the checked [Implementation Kickoff Review Inventory](research/implementation-kickoff-review-inventory-2026-07.md) before broadening work across unresolved `PB-*` lanes. It records first next actions, owner-only decisions, prohibited claims, and release-authority boundaries without approving tasks or promoting readiness.
- Sequencing control: use the checked [Build Readiness Dependency Graph](research/build-readiness-dependency-graph-inventory-2026-07.md) before changing task order, task dependencies, decision-gate relationships, or parallel no-claim lane boundaries.
- Documentation readiness completion audit: use the checked [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md) and checked no-claim [build-readiness closure-review template](project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json) before calling documentation preparation complete. They confirm contained-M0 continuation only and keep all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, and accessibility claims unsupported.
- Contained M0 start state: use the checked [Contained M0 Start State Inventory](research/contained-m0-start-state-inventory-2026-07.md) and [`contained-m0-start-state.json`](project-buildout/machine/contained-m0-start-state.json) before answering whether a session can start building. They permit no-claim docs/research and `TASK-000011` review-handoff maintenance, require owner-approved manifests before executing proposed `TASK-000001` through `TASK-000010`, and keep broad product work blocked.
- Build information readiness: use the checked [Build Information Readiness Ledger](research/build-information-readiness-ledger-2026-07.md) and [`build-information-readiness-ledger.json`](project-buildout/machine/build-information-readiness-ledger.json) before claiming all information is ready for broad building. They keep the missing source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, backup-ownership, task-authority, and Chrome-class product evidence visible without approving broad work.
- Chrome-class capability traceability: use the checked [Chrome-Class Capability Traceability Map](research/chrome-class-capability-traceability-map-2026-07.md) to route product, engine, runtime, security, accessibility, DevTools, AI, update, and performance capability domains to owning requirements, `PB-*`, `WP-*`, `TASK-*`, next proof, and prohibited claims. It is not Chrome-class, Chrome-equivalent, production, security, compatibility, accessibility, performance, or all-information-ready-for-building evidence.
- Implementation execution documentation: use the checked [Implementation Master Plan](project-buildout/implementation-plan/README.md), [Full implementation game plan audit](research/full-implementation-game-plan-audit-2026-07.md), and implementation graph registries only to order reviewed, bounded tasks. They do not approve work packages, replace `TASK-*` manifests, or promote broad implementation.
- GitHub issue handoff: use the checked [GitHub Issue Handoff](project-buildout/19-github-issue-handoff.md) and machine snapshot before treating live issue or PR cleanup as current. It maps issues to `WP-*`, `PB-*`, and `TASK-*` records, but it does not approve tasks, promote readiness, prove implementation, or replace live GitHub verification.
- Core registry navigation: use the [core program registries](repository-map.md#core-program-registries) before changing requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas.
- Research lane selection: use the [Research Index](research/README.md#current-implementation-research-lanes) to choose the source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership lane, then use its [build-readiness research crosswalk](research/README.md#build-readiness-research-crosswalk) to connect the work to primary `RQ-*`, `PB-*`, and `TASK-*` records.
- Task shaping: use the proposed [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md) and checked no-claim [task approval template](agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json) only to create reviewed task manifests. No proposed `TASK-*` item is execution approval. The template is not execution approval either.
- Source-strategy blocker: the first broad-web-engine blocker is the Servo/source strategy in `PB-002`; use the [ADR-0009 source packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md), [ADR-0009 evidence matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md), [ADR-0009 decision draft](project-buildout/16-adr-0009-decision-draft.md), and checked no-claim [ADR-0009 decision-review template](blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json) before any source-strategy-dependent implementation.
- Fresh-host build status: `PB-009` has a checked no-claim [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md) and project-buildout machine registry, but no independent fresh-host run, owner-approved clean-VM equivalent, retained clean-host bootstrap/doctor/check/xtask logs, cache/target-directory proof, source-tree cleanliness proof, `PB-009` readiness promotion, preview/beta/stable readiness, production readiness, or Chrome-class claim.
- IPC boundary status: `PB-011` has a checked no-claim [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md), [WP-002 kernel identity and IPC reference](research/wp-002-kernel-ipc-2026-07.md), [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md), checked no-claim [TASK-000011 evidence capture](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json), checked no-claim [IPC schema-source template](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), checked no-claim [IPC readiness-review template](blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json), and machine registry, but no accepted `TASK-000011`, accepted independent evidence-bundle instance, wire encoding decision, timeout/cancellation implementation, no owner-reviewed IPC readiness, renderer-security claim, agent-security claim, process-isolation readiness, site-isolation claim, production IPC claim, or implementation claim.
- Sandbox probe status: `PB-012` has a checked no-claim [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md), checked [WP-003 Sandbox Probe Contract](research/wp-003-sandbox-probe-plan-2026-07.md), security-engine machine registry, checked no-claim [probe-package template](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), and checked no-claim [sandbox readiness-review template](security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json), but no packaged expected-deny probes, stable operation/evidence contract execution, effective platform-policy capture, no owner-reviewed sandbox readiness, sandbox-readiness claim, renderer-security claim, site-isolation claim, hostile-browsing safety claim, SEC-GATE-1 claim, SEC-GATE-6 claim, production-safety claim, or implementation claim.
- Native-shell adapter-contract status: `PB-003` has a checked no-claim [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md) and UI-runtime machine registry, but no accepted `ADR-0013`, native adapter prototype, complete state/command/surface/accessibility/diagnostic/adapter contract, no-toolkit-owned-authority negative tests, trusted-chrome readiness, accessibility readiness, page-surface approval, toolkit selection, or release-path UI approval.
- Native-shell framework status: `PB-004` has a checked no-claim [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md) and UI-runtime machine registry, but no equivalent Slint/Vizia/Floem-or-GPUI adapter evidence, accepted `ADR-0014`, accessibility readiness, IME/keyboard proof, page-surface approval, crash/GPU-loss proof, startup/memory/binary/latency/frame-pacing/energy result, license/provenance approval, toolkit selection, trusted-chrome readiness, or release-path UI approval.
- Native-shell page-surface status: `PB-005` has a checked no-claim [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md) and UI-runtime machine registry, but no executable `UI-GATE-7` prototype, accepted `ADR-0016`, typed page-surface handles, brokered surface handle proof, compositor ownership decision, renderer-texture composition proof, resize/scale/damage proof, input/IME/accessibility routing proof, occlusion/capture proof, renderer-crash/GPU-loss proof, software fallback, latency/frame-pacing trace, or page-surface approval.
- Native-shell accessibility status: `PB-015` has a checked no-claim [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md) and accessibility machine registry, but no executable reference-platform workflow matrix, manual assistive-technology coverage, screen-reader coverage, page-tree composition proof, IME correctness, renderer-hang, crash, GPU-loss, UI-GATE-7, UI-GATE-10, or accessibility-readiness claim.
- Chrome-class and extreme-performance evidence: use the [Chrome-class performance readiness lane map](benchmark-lab/chrome-class-performance-readiness-lane.md), [Performance Benchmark Readiness Packet](research/performance-benchmark-readiness-packet-2026-07.md), [Benchmark Corpus Expansion](research/benchmark-corpus-expansion-2026-07.md), [Chrome-Class Performance Runbook](research/chrome-class-performance-runbook-2026-07.md), [Benchmark Engine Baseline Harness Readiness Map](research/benchmark-engine-baseline-harness-readiness-map-2026-07.md), benchmark manifests, server lifecycle evidence, browser-pin capture records, diagnostic records, launch-runner contract and self-test evidence, smoke-runner evidence, checked no-claim [claim-bundle template](blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json), and checked no-claim [benchmark readiness-review template](blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json) before any owner-reviewed statistics-analysis plan scope, owner-reviewed claim bundle, or performance measurement plan becomes build-ready. Use the lane sequence explicitly: fixed-hardware controls -> browser-run instrumentation -> raw-result capture -> statistics analysis -> claim-review. There is no owner-reviewed benchmark readiness, benchmark-ready status, public performance claim, faster claim, lower-memory claim, lower-energy claim, Chrome-class claim, competitor-result claim, daily-driver claim, production claim, or implementation claim.
- Operating controls: use the [project-buildout handbook](project-buildout/README.md) and [Agent Execution book](agent-execution/README.md) before delegating implementation or converting evidence into a task.

All of the above still supports contained M0 and no-claim evidence work only. It does not approve broad M1 expansion, source adoption, benchmark-ready browser pins, Chrome-class comparison, speed, memory, energy, compatibility, security, accessibility, production, beta, stable, or daily-driver claims.

## Validation Before Handoff

Before handing work to another maintainer or expanding a contained task, run the aggregate check for your shell:

```bash
sh tools/check.sh
```

```powershell
.\tools\check.ps1
```

Both wrappers delegate to the same locked `xtask check` path and keep Cargo build
output outside the repository when `CARGO_TARGET_DIR` is unset. If a direct
`xtask check` still fails with `forbidden legacy paths remain: target`, remove
the stale local `target` directory first and rerun. The direct command family is
listed in the [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md#validation-commands). A passing check proves only the current M0 repository validation scope, not broad implementation readiness or product support.

## Current safety statement

Do not use current or early Turing builds for sensitive accounts, private data, financial activity, or arbitrary hostile browsing. General safety claims remain prohibited until sandboxing, site isolation, update signing, fuzzing, compatibility, incident response, and independent review gates pass.

## Documentation rule

All canonical project documentation lives under `docs/`. Every feature, code, configuration, dependency, interface, risk, requirement, benchmark, or repository-structure change must update every affected document in the same change. See [the documentation policy](documentation-policy.md) and the root [`AGENTS.md`](../AGENTS.md).

## Professional implementation controls

Read the [project-buildout handbook](project-buildout/README.md), [technology stack](technology-stack/README.md), [Plug-in platform](plugins/README.md), [embedding SDK](embedding/README.md), and [templates](templates/README.md) before implementation work.

<!-- MARKET-STRATEGY-2026-07 -->
## Product differentiation research

After reading the professional buildout controls, use the [Market Strategy and Differentiation book](market-strategy/README.md) to understand proposed product opportunities and their validation requirements. Treat `OP-*` records as hypotheses, not roadmap commitments.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI status

The project has a documented native-shell working hypothesis, checked no-claim adapter contract inventory, checked no-claim framework bake-off inventory, checked no-claim page-surface composition inventory, checked no-claim component fixture inventory, and checked no-claim window/input/accessibility workflow inventory, but no accepted `ADR-0013`, native adapter prototype, selected toolkit, equivalent adapter run, accepted `ADR-0014`, rendered fixture pack, executable `UI-GATE-7` prototype, compositor ownership decision, reference-platform workflow matrix, manual assistive-technology coverage, or page-tree composition proof. Slint, Vizia, and Floem or GPUI require equivalent prototypes. React is restricted to a non-shipping design lab. See the [Native UI Runtime book](ui-runtime/README.md), [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md), [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md), [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md), [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md), [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md), and [pre-build readiness audit](research/pre-build-readiness-gap-audit-2026-07.md).

## Profile/session format status

The project has a checked no-claim [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md) and checked no-claim [schema-package template](storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json) for `PB-016`, but no executable profile, Space, session, snapshot, or migration schemas beyond that template and no real-profile migration. Sync, credential storage, user-data handling readiness, data-loss safety, and production profile-format behavior remain blocked until executable schemas, fault tests, fixture policy, and owner review exist.

## Research package/update status

The project has a checked no-claim [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md) and checked no-claim [update-lab package template](release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json) for `PB-017`, but no executable package manifest, metadata parser, signature/threshold verifier, staged installer, rollback lab, real updater, stable channel, production signing path, or public distribution path beyond that template. Rollback safety, migration safety, release readiness, and supported-security claims remain blocked.

## Incident-response rehearsal status

The project has a checked no-claim [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md) and checked no-claim [incident patch rehearsal template](security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json) for `PB-018`, but no executed private-intake tabletop, emergency patch dry run, coordinated disclosure rehearsal, postmortem evidence, role review, backup-owner coverage, or proven response capacity beyond that template. Incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, signing authority, stable promotion, incident closure authority, and production-safe browsing claims remain blocked.

## Backup ownership status

The project has a checked blocked [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md) and checked no-claim [backup-owner qualification template](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json) for `PB-019`, but no named qualified backup owners for build-critical scopes beyond that template. Current owner records and CODEOWNERS remain provisional and primary-only. Broad readiness, production authority, release authority, stable signing, update trust, supported-version changes, security-disclosure authority, irreversible migration approval, incident closure, legal approval, and owner-coverage claims remain blocked.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Implementation-agent and production status

Turing permits contained, reviewed implementation tasks; it does not authorize a single agent to build and release the browser autonomously. Read the [Agent Execution book](agent-execution/README.md), [Production Readiness book](production-readiness/README.md), and machine release gates before implementation work.
