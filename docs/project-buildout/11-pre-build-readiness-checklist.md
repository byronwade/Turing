# Pre-build Readiness Checklist

Status: canonical operating checklist; contained M0 implementation authorized
Owner: program, architecture, security, UI runtime, release operations, quality, and subsystem owners
Last audited: 2026-07-18

## Purpose

Turn “ready to build” into a bounded, reviewable claim. The first stop for any continuation decision is the [Build Continuation Readiness Pack](20-build-continuation-readiness-pack.md), which records current blockers and allowed M0 scope. The machine companion is [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json). The human handoff view is the [Build Readiness Operating Board](13-build-readiness-operating-board.md). The current documentation-readiness proof point is the [Documentation Readiness Evidence Matrix](18-documentation-readiness-evidence-matrix.md). The checked [`PB-020` Implementation Kickoff Review Inventory](../research/implementation-kickoff-review-inventory-2026-07.md) records unresolved-lane first next actions, owner-only decisions, prohibited claims, and release-authority boundaries without promoting readiness. The checked [Build Readiness Dependency Graph](../research/build-readiness-dependency-graph-inventory-2026-07.md) records task dependencies and decision-gate sequencing without approving execution. The checked [Documentation Readiness Completion Audit](../research/documentation-readiness-completion-audit-2026-07.md) and no-claim [build-readiness closure-review template](machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json) record that documentation is organized for contained M0 continuation only, not that all information is ready for broad building, Chrome-class competition, production, release, performance, compatibility, security, or accessibility claims. The checked [Contained M0 Start State Inventory](../research/contained-m0-start-state-inventory-2026-07.md) and machine [`contained-m0-start-state.json`](machine/contained-m0-start-state.json) make the current "can I start?" answer explicit without approving proposed tasks. The checked [Build Information Readiness Ledger](../research/build-information-readiness-ledger-2026-07.md) and machine [`build-information-readiness-ledger.json`](machine/build-information-readiness-ledger.json) keep the remaining information gaps explicit before any all-information-ready-for-building claim.

## Current authorization

Turing is now ready for **contained M0 implementation and no-claim evidence work**, not proposed-task execution from the queue alone, broad parallel browser construction, or production use.

The implemented foundation includes:

- a buildable root Cargo workspace;
- pinned Rust toolchain;
- M0 reference CI environment;
- typed identity, IPC, kernel, UI-model, build-info, shell-laboratory, and repository-tool crates;
- bootstrap, doctor, and complete check commands;
- dependency, unsafe-code, native-code, generated-code, and provenance ledgers;
- machine-checked component and dependency records;
- CI that compiles and tests the root workspace.

Evidence is summarized in the [M0 build-foundation report](../research/m0-build-foundation-2026-07.md).
The current continuation sequence is summarized in the [Build Readiness Operating Board](13-build-readiness-operating-board.md).

## Readiness classes

- **Ready:** required evidence exists and is linked.
- **M0 reference implemented:** deterministic source and tests exist, but platform integration, adversarial evidence, or production measurement is incomplete.
- **Partial or proposed:** design exists but source, tests, measurement, or decision evidence is incomplete.
- **Not started:** no executable evidence.
- **Blocked:** an external decision, staffing, legal, or predecessor dependency prevents completion.

## Controlled work allowed before PB-GATE-0

- source crates under the accepted M0 dependency direction;
- typed identity and process-policy implementation;
- bounded IPC and schema experiments;
- toolkit-neutral UI state and command work covered by the checked [Toolkit-Neutral UI Adapter Contract Inventory](../research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- native UI comparison prototypes isolated from production crates with the checked [Toolkit-Neutral UI Adapter Contract Inventory](../research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md), checked [Native UI Framework Bake-Off Inventory](../research/native-ui-framework-bakeoff-inventory-2026-07.md), checked no-claim [native UI readiness-review template](../ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json), equivalent adapter scope, page-surface planning from the checked [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md), accessibility, IME, keyboard, crash, GPU-loss, startup, memory, binary, latency, frame-pacing, energy, license, dependency, provenance, replacement, and package/runtime-exclusion evidence;
- sandbox probes;
- benchmark and corpus tooling;
- profile, Space, session, snapshot, and migration schema prototypes with disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, and data-loss behavior;
- signed research-package and updater-laboratory prototypes for source commit, build ID, channel, platform, architecture, toolchain, feature set, SBOM, provenance, symbols, notices, artifact hashes, artifact sizes, no-stable-support, role separation, signature threshold, expiry, minimum secure version, rollout, mirrors, tamper, replay, wrong target, partial write, disk full, power loss, rollback, vulnerable version refusal, migration, downgrade, crash-loop, and privacy-preserving behavior, with no production signing keys, offline root keys, stable channel, public binary distribution, real updater, or real user profile migration;
- private intake tabletop and emergency patch rehearsal documentation that starts from the checked no-claim incident patch rehearsal template and covers access control, acknowledgement, reproduction, severity, asset analysis, affected version, embargo, sanitized evidence, protected patch branch, embargoed CI, regression, backport, signing, update dry run, staged rollout, minimum secure version, revocation, release notes, user and admin communication, CVE, credit, coordinated disclosure, postmortem, incident-class active exploitation, update or signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension, provider, service outage, role matrix, timing targets, escalation, secret rotation, agent limits, disclosure, incident closure, stable promotion, and signing authority outside implementation-agent scope;
- tests, fuzz targets, fixtures, and diagnostic tooling.

## Current contained-M0 evidence

The following controls now have executable evidence:

- root Cargo workspace and machine-checked dependency graph;
- pinned M0 Rust toolchain;
- bootstrap, doctor, and complete repository check;
- zero-dependency, unsafe, native, generated-code, and provenance ledgers;
- canonical JSON control-plane schema and deterministic generated Rust/documentation;
- restart-safe process identities;
- generated roles, capabilities, launch rights, message routes, document-scope rules, message limits, and queue budgets;
- bounded envelopes, exact sequences, explicit backpressure, capability attenuation, and kernel route authorization.

The generated IPC work is an M0 policy reference. It does not satisfy real authenticated transport, sandbox, shared-memory, platform handle, wire-codec, compromised-process, or fixed-hardware requirements.

## P0 kickoff group still open

- Servo/source strategy and `ADR-0009` owner review remain blocked; the source-strategy reports, evidence matrix, decision-review template, local compatibility corpus plan, Servo build evidence, and maintenance/security reports are evidence preparation only.
- Independent fresh-host reproduction remains incomplete beyond the checked [Fresh Host Reproduction Inventory](../research/fresh-host-reproduction-inventory-2026-07.md), checked run-record template, and checked no-claim [fresh-host readiness-review template](machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json); owner-reviewed fresh-host readiness is still required.
- IPC remains partial despite the WP-002 reference implementation, [TASK-000011 WP-002 Review Handoff](../research/task-000011-wp002-review-handoff-2026-07.md), and checked no-claim [TASK-000011 evidence capture](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json); accepted `TASK-000011` evidence, owner-reviewed IPC readiness beyond the checked [IPC Capability Boundary Inventory](../research/ipc-capability-boundary-inventory-2026-07.md), checked no-claim IPC schema-source template, and checked no-claim [IPC readiness-review template](../blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json) still require an accepted independent evidence bundle, operating-system transport, canonical wire codec, peer authentication, handle transfer, malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, cancellation, and stale-epoch receiver rejection coverage, compromised-process fuzzing, and independent review.
- Sandbox readiness remains incomplete beyond the checked [Sandbox Probe Inventory](../research/sandbox-probe-inventory-2026-07.md), checked [WP-003 Sandbox Probe Contract](../research/wp-003-sandbox-probe-plan-2026-07.md), checked no-claim [probe-package template](../security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), and checked no-claim [sandbox readiness-review template](../security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json); packaged expected-deny probes for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater roles across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC access, unsandboxed control runs, stable operation catalog replacement, evidence schema records, compromised-process harnesses, effective platform policy, host-safe fixtures, platform matrix evidence, and owner-reviewed sandbox readiness are still required.
- Benchmark readiness remains no-claim. The [Performance Benchmark Readiness Packet](../research/performance-benchmark-readiness-packet-2026-07.md), benchmark manifests, no-claim [claim-bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json), and checked no-claim [benchmark readiness-review template](../blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json) do not provide owner-reviewed benchmark readiness, benchmark-ready status, public performance, faster, lower-memory, lower-energy, Chrome-class, competitor-result, daily-driver, production, or implementation claims.
- Native-shell readiness remains incomplete beyond the checked toolkit-neutral state, command, surface, diagnostic, adapter, equivalent framework, page-surface, design-token, component, component-fixture, window/input/accessibility, and native UI readiness-review records; `ADR-0013`, `ADR-0014`, `ADR-0016`, `UI-GATE-7`, rendered fixtures, IME, keyboard, page-tree, clipboard, drag-drop, localization, zoom, high contrast, reduced motion, screen-reader, manual assistive-technology, crash, renderer hang, GPU-loss, startup, memory, binary, latency, frame-pacing, energy, license, dependency, provenance, accessibility proof, trusted-chrome readiness, page-surface approval, toolkit selection, and release-path UI approval remain unproven.
- Profile/session, package/update, incident-response, and backup-ownership readiness remain incomplete beyond their checked no-claim inventories and templates; owner-reviewed profile/session readiness for profile, Space, session, snapshot, migration, disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, data-loss, sync, credential storage, real-profile migration, user-data handling, and production profile-format boundaries, package/update readiness, incident/patch readiness, backup ownership readiness, release authority, signing authority, production authority, and broad implementation claims remain blocked.
- Backup ownership remains blocked until named qualified backup owners beyond the checked no-claim backup-owner qualification template cover program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data scopes with role level, subsystem competence, representative path coverage, recent review record, availability, succession, recusal, inactivity, removal, emergency replacement, CODEOWNERS, review-rule, escalation-policy, signing, disclosure, package, CI, service, repository-access, stale privileged access, ownerless protected path, primary-only, blocked status, single-owner residual-risk, two-person control, update trust, supported-version, security-disclosure, irreversible migration, release promotion, legal approval, and incident closure evidence.
- Owner-reviewed implementation kickoff, build-readiness dependency graph, documentation-readiness completion audit, and build-readiness closure review beyond the checked no-claim templates remain required before all-information-ready-for-building, broad M1, task approval, readiness promotion, release, production, Chrome-class, performance, compatibility, security, accessibility, or daily-driver claims.
- Owner-reviewed build-information readiness beyond the checked no-claim ledger remains required before source strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, backup-ownership, task-authority, or Chrome-class product evidence can be represented as all-information-ready-for-building.

Windows PowerShell wrappers are equivalent and delegate to the same `xtask` commands:

```powershell
.\tools\bootstrap.ps1
.\tools\doctor.ps1
.\tools\check.ps1
```

Direct `cargo run --locked -p xtask -- check` is a valid path only when
`CARGO_TARGET_DIR` is set to an out-of-repo directory. When this variable is
unset, the xtask check compiles to `./target` and fails with "forbidden legacy
paths remain: target". Before running it directly, set a workspace-safe target
dir:

```powershell
$env:CARGO_TARGET_DIR = "C:\Users\<you>\AppData\Local\Temp\turing-check-target"
cargo run --locked -p xtask -- check
```

If you still see `forbidden legacy paths remain: target`, clear stale in-repo
build artifacts first:

```powershell
if (Test-Path target) { cmd /c "rmdir /s /q target" }
```

## PB-GATE-0

## Review

The program lead reviews the registry at every implementation kickoff and milestone boundary. Exceptions must name the affected item, scope, owner, rationale, risk, compensating controls, expiry, and evidence required for closure. An exception cannot authorize misleading product, security, performance, or compatibility claims.

`WP-002` may continue under contained M0 authorization only as review-handoff maintenance until independent review changes `TASK-000011`. `TASK-000011` remains `review_pending` until independent review and an evidence bundle accept or reject the contained reference. `WP-002` remains in progress until authenticated platform transport, generated wire representation, handle-transfer rules, negative testing, and independent review exist.

## Exit

PB-GATE-0 passes for a selected contained milestone when all applicable P0 items are ready or covered by approved time-bounded exceptions. It does not imply beta or stable readiness.
