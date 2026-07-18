# Build Readiness Task Queue

Status: proposed task handoff; not execution approval
Owner: program, architecture, security, quality, release operations, performance, UI runtime, storage, and documentation-research
Last updated: 2026-07-18

## Purpose

This queue turns the current build-readiness blockers into explicit `TASK-*` handoff records. It does not replace the [Build Readiness Operating Board](13-build-readiness-operating-board.md), checked [Implementation Kickoff Review Inventory](../research/implementation-kickoff-review-inventory-2026-07.md), checked [Build Readiness Dependency Graph](../research/build-readiness-dependency-graph-inventory-2026-07.md), checked [Documentation Readiness Completion Audit](../research/documentation-readiness-completion-audit-2026-07.md), checked no-claim [build-readiness closure-review template](machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json), [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json), [`backlog.json`](../blueprint-v1/machine/backlog.json), or the [Agent Execution book](../agent-execution/README.md).

The machine companion is [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json). Tasks in that registry use the execution-task shape from [`execution-task.schema.json`](../agent-execution/machine/execution-task.schema.json).
The checked no-claim [Task approval template](../agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json), validated by [`validate_task_approval_templates.py`](../../tools/validate_task_approval_templates.py), defines what an owner must fill before any proposed row becomes an immutable reviewed execution manifest.

## Authorization Boundary

Every task is currently `proposed`. A proposed task is not approved, not running, not accepted, and not release-gated. Before execution, an owner must convert the task into an immutable reviewed task manifest, assign an independent reviewer, confirm allowed paths and resource budgets, and define the evidence bundle location.

These task records cannot authorize:

- Servo-derived or other browser-engine release code;
- broad M1 subsystem implementation;
- public compatibility, security, memory, speed, Chrome-class, or production claims;
- weakened sandbox, site-isolation, certificate, update, or permission policies;
- self-approval by the implementation agent.

## Ordered Queue

| Task | Gates advanced | Work packages | Why it is next | Current execution status |
|---|---|---|---|---|
| `TASK-000001` Source-strategy closure packet | `PB-002`, `ADR-0009` | Blocks broad engine-source decisions | The Servo/source-strategy decision is the first broad-web-engine blocker and controls what later source evidence can mean | Proposed only |
| `TASK-000002` Fresh-host bootstrap reproduction | `PB-009`, `PB-020` | `WP-001` | The build foundation is ready for contained M0, but needs fresh-host reproduction and owner-reviewed fresh-host readiness before broader implementation confidence | Proposed only; checked no-claim inventory, run-record template, and readiness-review template exist |
| `TASK-000003` IPC schema and capability negative tests | `PB-011` | `WP-002` | Kernel identity and bounded IPC are the nearest safe implementation foundation after M0 | Proposed execution only; checked no-claim inventory, schema-source template, and IPC readiness-review template exist |
| `TASK-000004` Sandbox probe harness | `PB-012` | `WP-003` | Security probes must exist before renderer, network, storage, GPU, decoder, extension, DevTools, agent, or updater roles are trusted | Proposed execution only; checked no-claim inventory, operation/evidence contract, package template, and sandbox readiness-review template exist |
| `TASK-000005` Browser-launch benchmark runner contract | `PB-013` | `WP-005`, `WP-018` | Chrome-class and extreme-performance goals need raw, no-claim, equal-workload evidence infrastructure, no-real-profile browser-pin capture, and local competitor-version pins before any result | Proposed only |
| `TASK-000006` Native shell adapter bake-off | `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015` | `WP-004` | Toolkit-neutral shell work can proceed only with the checked no-claim adapter contract, framework bake-off, component, page-surface composition, window/input/accessibility inventories, native UI readiness-review template, equivalent adapter scope, accessibility evidence, and no webview runtime in trusted chrome | Proposed only; checked inventories and no-claim review template exist |
| `TASK-000007` Profile, Space, session, snapshot, and migration schemas | `PB-016` | `WP-004`, `WP-014`, `WP-017` | Session and migration formats need privacy, recovery, downgrade, and data-loss behavior before real profile data exists | Proposed execution only; checked no-claim inventory, schema-package template, and readiness-review template exist |
| `TASK-000008` Backup ownership closure | `PB-019`, `PB-020` | Program control | The project cannot claim broad readiness while build-critical scopes have no qualified backup owners | Proposed only; checked blocked inventory, backup-owner qualification template, and readiness-review template exist |
| `TASK-000009` Research package identity and updater lab | `PB-017` | `WP-017` | Research packages and update metadata need signed identity, tamper/replay/rollback failure tests, and explicit no-production-key boundaries before updater work is trusted | Proposed execution only; checked no-claim inventory, update-lab package template, and readiness-review template exist |
| `TASK-000010` Security incident and patch rehearsal | `PB-018` | `WP-017` | Private intake, emergency patch, disclosure, and role separation need a rehearsal before developer preview, beta, stable, or supported-security claims | Proposed execution only; checked no-claim inventory, incident patch rehearsal template, and readiness-review template exist |

## Intake Snapshot

The exact owners, reviewers, allowed paths, prohibited paths, budgets, dependencies, rollback evidence, and expiration dates live in [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json). This snapshot is for human triage only.

`TASK-000001` Source-strategy closure packet:

- Start only if the work remains documentation/research and no Servo-derived code enters a release path.
- Proves progress by closing or explicitly preserving every `ADR9-EV-001` through `ADR9-EV-018` evidence state, including source baseline, provenance, license, SBOM, native package, generated-output, unsafe, FFI, local compatibility corpus browser runs and WPT/Test262 denominator, performance, security, maintenance, and public-claim impacts.
- Reject if evidence presence is treated as dependency, component, compatibility, security, performance, memory, or release approval.
- Start any real ADR-0009 decision review from the checked no-claim [decision-review template](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json), replacing null option, baseline, feature profile, owner reviewer, independent reviewer, and false decision flags with owner-reviewed evidence or explicit blocked status.
- Reject if the checked no-claim decision-review template is cited as an accepted ADR, source baseline, source adoption, component approval, release-code authorization, `PB-002` readiness promotion, or implementation evidence.
- Must not claim Servo adoption, source approval, broad engine readiness, or Chrome-class capability.

`TASK-000002` Fresh-host bootstrap reproduction:

- Start only from the checked [Fresh Host Reproduction Inventory](../research/fresh-host-reproduction-inventory-2026-07.md), checked [run-record template](machine/fresh-host-runs/no-claim-run-record-template.json), and checked no-claim [fresh-host readiness-review template](machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json) with an independent fresh reference host or owner-approved clean-VM equivalent.
- Proves progress with dated bootstrap, doctor, check, and `xtask` output plus exact OS, shell, Rust, Cargo, Git, cache, target-directory, temp-directory, source-tree cleanliness, retained-log, failure-classification, rollback-note, and owner-reviewed fresh-host readiness beyond the checked no-claim template.
- Reject if a same-host rerun is presented as independent reproduction, a clean VM lacks explicit waiver and expiry, command failures or exit codes are hidden, source-tree status is omitted, or tools/installers land in source control.
- Reject if the checked no-claim fresh-host readiness-review template is cited as owner-reviewed fresh-host readiness, `PB-009` readiness, release confidence, production readiness, implementation, or Chrome-class evidence.
- Must not promote `PB-009` to ready without independent reproduction evidence and owner-reviewed fresh-host readiness beyond the checked no-claim template.

`TASK-000003` IPC schema and capability negative tests:

- Start after `PB-009` is reproduced or explicitly waived by an owner and the checked [IPC Capability Boundary Inventory](../research/ipc-capability-boundary-inventory-2026-07.md), checked no-claim [IPC schema-source template](../blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), and checked no-claim [IPC readiness-review template](../blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json) remain current.
- Proves progress with the checked no-claim inventory and templates, then a canonical IPC schema or generator proposal, reviewed wire encoding decision, bounded queues/backpressure, connection authentication, stale-epoch rejection, timeout/cancellation behavior, negative tests for malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases, and owner-reviewed IPC readiness beyond the checked no-claim IPC readiness-review template.
- Reject if page content, DevTools, extensions, or agents can mint authority, if tests cover only success paths, if the IPC schema-source template is cited as schema-generator approval, or if the IPC readiness-review template is cited as owner-reviewed IPC readiness, `PB-011` readiness, renderer-security, agent-security, process-isolation, site-isolation, production IPC, or implementation evidence.
- Must not claim renderer, agent, process-security, site-isolation, schema-generator, schema-source, wire-encoding, timeout/cancellation, or production IPC readiness beyond the tested M0 boundary; no schema-generator approval exists.

`TASK-000004` Sandbox probe harness:

- Start after authority and IPC boundaries are reviewed or explicitly scoped out and the checked [Sandbox Probe Inventory](../research/sandbox-probe-inventory-2026-07.md), checked [WP-003 Sandbox Probe Contract](../research/wp-003-sandbox-probe-plan-2026-07.md), checked no-claim [probe-package template](../security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), and checked no-claim [sandbox readiness-review template](../security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json) remain current.
- Proves progress with the checked no-claim inventory, operation catalog, evidence schema, and templates, then executable expected-deny probes for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater roles across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC access, with unsandboxed control runs, unsupported platform primitive handling, application-level stub rejection, effective platform-policy capture, host-safe fixtures, broker fixtures, compromised-client harnesses, platform matrix evidence, and owner-reviewed sandbox readiness beyond the checked no-claim sandbox readiness-review template.
- Reject if the checked no-claim sandbox readiness-review template is cited as owner-reviewed sandbox readiness, `PB-012` readiness, sandbox-readiness, renderer-security, site-isolation, SEC-GATE, production-safety, or implementation evidence.
- Reject if the no-claim probe-package template, operation catalog, or evidence schema is cited as execution approval, platform containment proof, or SEC-GATE evidence; if a demo bypasses denial checks; if unsupported platform primitives count as passes; if an application-level stub is counted as a sandbox denial; if untrusted input broadens authority; or if a failure is swallowed as success.
- Must not claim sandbox, renderer security, site isolation, hostile-browsing safety, platform containment, SEC-GATE-1, SEC-GATE-6, or production safety until platform-enforced evidence and owner review exist.

`TASK-000005` Browser-launch benchmark runner contract:

- Start with validated no-claim hardware, OS-control, corpus, network-profile, tab-scenario, artifact-package, launch-runner, resource-attribution registries, the checked [Benchmark Engine Baseline Harness Readiness Map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md), the checked no-claim statistics-analysis contract, and the checked no-claim benchmark readiness-review template.
- Proves progress with the expanded generated no-claim corpus seed, a no-claim runner contract, checked runner-managed server lifecycle self-test, and checked no-browser browser launch-runner self-test that record server startup/shutdown, timeout, repetition, cache/profile reset, temporary-profile isolation, prohibited-path checks, viewport, checked browser launch-runner planning, trace/artifact package generation, statistics-analysis plan references, redaction and retention review, failures, cleanup, artifact hashes, resource attribution, 30-tab mixed/all-live scenario handling, and browser-pin candidate evidence.
- Reject if smoke/sample data can produce an approved claim or if failures, unknown resource buckets, tab discards, site-isolation state, or unequal workload settings are hidden.
- Reject if the checked no-claim benchmark readiness-review template is cited as owner-reviewed benchmark readiness, statistics-analysis plan acceptance, benchmark-ready status, public performance, faster, lower-memory, lower-energy, Chrome-class, competitor-result, daily-driver, production, or implementation evidence.
- Must not claim faster, lower-memory, lower-energy, Chrome-class, compatibility, public performance, or benchmark-ready competitor results until owner-reviewed statistics-analysis plan scope, benchmark readiness, and claim-bundle evidence exist.

`TASK-000006` Native shell adapter bake-off:

- Start after IPC and command authority are reviewed or the shell prototype is explicitly isolated.
- Proves progress with the checked no-claim [Toolkit-Neutral UI Adapter Contract Inventory](../research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md), checked no-claim [Native UI Framework Bake-Off Inventory](../research/native-ui-framework-bakeoff-inventory-2026-07.md), checked no-claim [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md), checked no-claim [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md), checked no-claim [Window Input Accessibility Spike Inventory](../research/window-input-accessibility-spike-inventory-2026-07.md), checked no-claim [native UI readiness-review template](../ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json), accepted `ADR-0013`, toolkit-neutral state, command, surface, accessibility, diagnostic, and adapter contract evidence, native adapter prototype evidence, no toolkit-owned authority negative tests, equivalent Slint, Vizia, and Floem or GPUI adapter scope, accepted `ADR-0014`, typed page-surface handles, brokered surface handles, document and device generations, `UI-GATE-7`, `ADR-0016`, page-surface and page-tree composition, rendered design-token and component fixtures, input, accessibility, IME, keyboard, clipboard, drag-drop, localization, zoom, high contrast, reduced motion, screen-reader, manual assistive-technology, crash, renderer-hang, GPU-loss, software fallback, startup, memory, binary, latency, frame-pacing, energy, license, dependency, provenance, replacement, package/runtime-exclusion evidence, and owner-reviewed native UI readiness beyond the checked no-claim template.
- Reject if trusted chrome depends on Electron, Tauri, a system webview, Node, runtime React, runtime JavaScript, runtime DOM, runtime CSS parser, or adapter-specific state as the product source of truth.
- Must not accept `ADR-0013`, claim a native adapter prototype, select a UI toolkit, accept `ADR-0014`, decide compositor ownership, use the native UI readiness-review template as owner review, or claim native-shell, trusted-chrome, accessibility, screen-reader, page-tree, page-surface, `UI-GATE-7`, `UI-GATE-10`, or release-path UI readiness without ADR and review.

`TASK-000007` Profile, Space, session, snapshot, and migration schemas:

- Start only with consistent terms, the checked no-claim schema-package template and checked no-claim readiness-review template current, and no real user profile data fixtures.
- Proves progress with the checked no-claim [Profile Session Format Inventory](../research/profile-session-format-inventory-2026-07.md), checked no-claim [schema-package template](../storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json), and checked no-claim [readiness-review template](../storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json), then executable versioned profile, Space, session, snapshot, and migration schema proposals plus owner-reviewed profile/session readiness beyond the template covering disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, and data-loss behavior.
- Reject if schemas can silently discard user work, leak private-session data, treat corrupt/downgrade input as a successful migration, cite the checked no-claim schema-package template as executable schema approval, or cite the checked no-claim readiness-review template as data-loss safety, user-data handling readiness, production profile-format approval, release-path approval, sync support, credential-storage support, or implementation evidence.
- Must not claim owner-reviewed profile/session readiness, real-profile migration, sync, credential storage, data-loss safety, user-data handling readiness, release-path approval, or production profile-format readiness.

`TASK-000008` Backup ownership closure:

- Start only when candidate backup maintainers and qualification evidence are known and the checked no-claim [backup-owner qualification template](machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json) plus checked no-claim [backup-ownership readiness-review template](machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json) remain current.
- Proves progress with named qualified backups beyond the checked no-claim backup-owner qualification template or explicit checked blocked status from the [Backup Ownership Gap Inventory](../research/backup-ownership-gap-inventory-2026-07.md) for build-critical program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data scopes.
- Proves progress with role level, subsystem competence, representative path coverage, recent review record, availability, succession, recusal, inactivity, removal, emergency replacement, CODEOWNERS, review-rule, escalation-policy, support, signing, disclosure, package, CI, service, repository-access, no stale privileged access, and two-person control evidence.
- Proves progress with owner-reviewed backup ownership readiness beyond the checked no-claim readiness-review template, replacing null inventory, qualification-record-set, owner-reviewer, independent-reviewer, security-reviewer, release-operations-reviewer, legal-reviewer, and support-reviewer fields with retained evidence.
- Reject if placeholder names, CODEOWNERS routing, intent, self-nomination, undocumented availability, title-only ownership, stale privileged access, ownerless protected paths, single-owner residual risk, primary-only release/signing/disclosure/support/incident paths, or the checked no-claim backup-owner qualification template are treated as qualified backup ownership, owner coverage, two-person control, release authority, signing authority, disclosure authority, legal approval, incident closure, production authority, broad readiness, or implementation evidence.
- Reject if the checked no-claim backup-ownership readiness-review template is cited as owner-reviewed backup ownership readiness, owner coverage, two-person control, release authority, signing authority, disclosure authority, legal approval, incident closure, production authority, broad readiness, or implementation evidence.
- Must not claim owner-reviewed backup ownership readiness, broad readiness, production authority, release authority, release promotion, stable signing, update trust, supported-version changes, security-disclosure authority, irreversible migration approval, incident closure, legal approval, or owner coverage from documentation intent.

`TASK-000009` Research package identity and updater lab:

- Start only with an isolated research lab, the checked no-claim update-lab package template and checked no-claim readiness-review template current, no production signing keys, no offline root keys, no stable channel, no public binary distribution, no real updater, and no real user profile migration.
- Proves progress with the checked no-claim [Research Package Update Lab Inventory](../research/research-package-update-lab-inventory-2026-07.md), checked no-claim [update-lab package template](../release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json), and checked no-claim [readiness-review template](../release-operations/machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json), then an executable signed research-package manifest binding source commit, build ID, channel, platform, architecture, toolchain, feature set, SBOM, provenance, symbols, notices, artifact hashes, artifact sizes, and no-stable-support label.
- Proves progress with update metadata role separation, signature threshold, expiry, minimum secure version, rollout, mirrors, staged install, tamper, replay, wrong-target, partial-write, disk-full, and power-loss evidence.
- Proves progress with authorized rollback, vulnerable-version refusal, migration, downgrade, crash-loop, and privacy-preserving local event evidence.
- Reject if tamper, replay, wrong-target, expiry, mirror, partial-write, disk-full, power-loss, revoked-version, vulnerable-version, rollback, downgrade, crash-loop, or migration failure can be reported as a successful update, or if the checked no-claim update-lab package template is cited as executable package manifest, metadata-parser, signature-threshold, staged-install, rollback-safety, migration-safety, release-readiness, supported-security, or production-updater evidence.
- Reject if the checked no-claim readiness-review template is cited as owner review, release readiness, supported security, production updater, stable-channel, public-distribution, signing-readiness, or implementation evidence.
- Must not claim owner-reviewed package/update readiness, production updater, stable support, public distribution, signing readiness, rollback safety, migration safety, security readiness, supported-security readiness, implementation readiness, or release readiness.

`TASK-000010` Security incident and patch rehearsal:

- Start only when private handling is available, the checked no-claim incident patch rehearsal template and checked no-claim readiness-review template remain current, and the exercise keeps agent, release, signing, disclosure, severity, and stable-promotion authority separated.
- Proves progress with the checked no-claim [Incident Patch Rehearsal Inventory](../research/incident-patch-rehearsal-inventory-2026-07.md), checked no-claim [incident patch rehearsal template](../security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), and checked no-claim [readiness-review template](../security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json), then private intake tabletop, access control, acknowledgement, reproduction, severity and asset analysis, affected-version statement, embargo handling, sanitized evidence preservation, protected patch branch, embargoed CI, regression test, backport decision, signing/update dry run, staged rollout, minimum secure version, revocation, release notes, user/admin communication, CVE/credit handling, coordinated disclosure, and postmortem remediation beyond the template.
- Proves progress with incident-class workflow coverage for active exploitation, update or signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension or provider, and service outage.
- Proves progress with a role matrix, timing targets, escalation path, and secret rotation plan that keeps agent disclosure, stable promotion, and signing authority unavailable.
- Reject if public issue flow retains exploitable details, agents decide severity or disclosure, missing update capacity is hidden, missing owner coverage is hidden, regression evidence is absent, support targets remain unstated, or the checked no-claim incident patch rehearsal template is cited as executed private-intake, emergency patch, regression, backport, disclosure, postmortem, role-review, backup-coverage, incident-response readiness, emergency patch capacity, supported-security, or production-safe browsing evidence.
- Reject if the checked no-claim readiness-review template is cited as owner review, incident-response readiness, emergency patch capacity, supported security versions, production-safe browsing, disclosure authority, stable promotion, signing authority, incident closure, or implementation evidence.
- Must not claim owner-reviewed incident/patch readiness, production-safe browsing, supported security versions, incident-response readiness, emergency patch capacity, disclosure authority, stable promotion, signing authority, incident closure, or implementation readiness.

## Execution Rules

Use the queue this way:

1. Select the first task whose preconditions can be satisfied.
2. Create or approve an immutable task manifest using the [agent task template](../templates/agent-task.md) and checked [Task approval template](../agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json).
3. Confirm the owner, independent reviewer, allowed paths, prohibited paths, resource budget, rollback plan, and evidence bundle location.
4. Execute only the approved task scope.
5. Update every affected Blueprint chapter, detailed book, readiness record, risk, requirement, backlog item, registry, and validation rule in the same change.
6. Keep task status as proposed until owner review changes it.

## Evidence Requirements

Every task must preserve these common evidence rules:

- exact command output or raw artifacts for any build, test, benchmark, or probe claim;
- explicit unsupported behavior and residual risk;
- negative tests for security, compatibility, recovery, and resource-accounting behavior where applicable;
- source-tree cleanliness and generated-output policy;
- validation output from the repository checks;
- independent review before promotion.

## Handoff Rule

A maintainer should be able to answer, for any queued task:

1. Which `PB-*`, `WP-*`, requirement, risk, and ADR records does it touch?
2. Which paths may it change, and which paths are prohibited?
3. What evidence proves success?
4. What evidence would reject the task?
5. What must not be claimed after the task finishes?

If those answers are missing or stale, update the task queue and the owning registry before implementation begins.
