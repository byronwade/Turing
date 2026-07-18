# Research Log

This log records material research-program and documentation-governance changes. Detailed technical conclusions belong in the owning Blueprint chapter, requirement, risk, ADR, benchmark, backlog entry, indexed engineering book, or dated research report.

## 2026-07-18 — Benchmark readiness-review template

Question:

Can `PB-013` and `TASK-000005` gain one checked owner-review handoff object before approved hardware tiers, clean OS-control review, representative corpus review, browser-run server evidence review, implemented browser launch runner review, benchmark-ready browser pin review, trace-artifact review, raw result review, 30-tab artifact review, statistics review, denominator review, equal-workload review, owner-reviewed claim bundles, owner-reviewed benchmark readiness, benchmark-ready status, public performance, faster, lower-memory, lower-energy, Chrome-class, competitor-result, daily-driver, production, or implementation claims exist?

Inputs:

- [Performance Benchmark Readiness Packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [`benchmark-claim-bundle.schema.json`](blueprint-v1/machine/benchmark-claim-bundle.schema.json);
- [`no-claim-public-claim-template.json`](blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json);
- [`benchmark-readiness-review.schema.json`](blueprint-v1/machine/benchmark-readiness-review.schema.json);
- [`no-claim-benchmark-readiness-template.json`](blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json);
- [`tools/validate_benchmark_readiness_review.py`](../tools/validate_benchmark_readiness_review.py).

Method:

Added a checked no-claim benchmark readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null reviewer and evidence fields, hardware/OS axes, corpus/network axes, runner/artifact axes, browser-pin comparison axes, statistics/denominator axes, claim-review axes, rejection rules, validation commands, `PB-013` evidence, `TASK-000005` scope, and benchmark research-lane crosswalk coverage.

Decision:

Keep `PB-013` documented as no-runner. The template defines what a future real owner-reviewed benchmark readiness review must replace, but it does not approve hardware tiers, prove clean OS controls, approve a representative corpus, create browser-run server evidence, implement or review the launch runner, pin benchmark-ready browsers, create trace artifacts, review raw results, run a 30-tab scenario, approve statistics, prove equal workloads, approve claim bundles, approve benchmark readiness, or support performance, memory, energy, Chrome-class, competitor, production, daily-driver, or implementation claims.

Impact:

Future `TASK-000005` work now has a cross-scope readiness-review handoff object in addition to the benchmark readiness packet and claim-bundle template. Any real review must replace null hardware, corpus, server, runner, trace, result, browser-pin, claim-bundle, owner reviewer, performance reviewer, benchmark operations reviewer, quality reviewer, security reviewer, accessibility reviewer, and release-operations reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-013` blocker should become real evidence first: fixed hardware tiers, clean OS controls, corpus/server packaging, launch-runner implementation, trace artifacts, 30-tab output, raw result retention, statistics review, equal-workload proof, or owner-reviewed claim bundles?

## 2026-07-18 — Sandbox readiness-review template

Question:

Can `PB-012` and `TASK-000004` gain one checked owner-review handoff object before packaged expected-deny probes, effective platform policy, host-safe fixture review, broker fixture review, compromised-client harness review, platform matrix review, result-record review, failure-denominator review, cleanup review, `PB-012` readiness promotion, sandbox-readiness, renderer-security, site-isolation, hostile-browsing safety, platform containment, `SEC-GATE-1`, `SEC-GATE-6`, production-safety, or implementation claims exist?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [`sandbox-probe-inventory.json`](security-engine/machine/sandbox-probe-inventory.json);
- [`sandbox-probe-package.schema.json`](security-engine/machine/sandbox-probe-package.schema.json);
- [`no-claim-expected-deny-template.json`](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json);
- [`sandbox-readiness-review.schema.json`](security-engine/machine/sandbox-readiness-review.schema.json);
- [`no-claim-sandbox-readiness-template.json`](security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json);
- [`tools/validate_sandbox_readiness_review.py`](../tools/validate_sandbox_readiness_review.py).

Method:

Added a checked no-claim sandbox readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null inventory/package/reviewer fields, probe-package axes, platform-policy axes, role/surface axes, host-safety axes, broker/compromised-client axes, owner-review axes, rejection rules, validation commands, `PB-012` evidence, `TASK-000004` scope, and sandbox research-lane crosswalk coverage.

Decision:

Keep `PB-012` partial. The template defines what a future real owner-reviewed sandbox readiness review must replace, but it does not execute packaged probes, capture effective platform policy, prove host-safe fixtures, prove broker fixtures, run compromised-client harnesses, complete a platform matrix, review result records, support `SEC-GATE-*`, prove renderer security, prove site isolation, prove hostile-browsing safety, approve production safety, or support implementation claims.

Impact:

Future `TASK-000004` work now has a cross-scope readiness-review handoff object in addition to the sandbox probe inventory and probe-package template. Any real review must replace null probe inventory, probe package, owner reviewer, security reviewer, platform reviewer, quality reviewer, and release-operations reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-012` blocker should become real evidence first: packaged role runner, effective platform policy capture, host-safe fixtures, broker fixtures, compromised-client harnesses, result records, or platform matrix execution?

## 2026-07-18 — IPC readiness-review template

Question:

Can `PB-011` and `TASK-000003` gain one checked owner-review handoff object before an implemented schema generator, approved generator source, wire encoding decision, generated types, generated validators, generated fixtures, connection authentication, bounded queues/backpressure, timeout/cancellation behavior, stale-epoch receiver proof, negative-test review, fuzz/model-test review, process-capability generation review, `PB-011` readiness promotion, renderer-security, agent-security, process-isolation, site-isolation, production IPC, or implementation claims exist?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [`ipc-capability-boundary.json`](blueprint-v1/machine/ipc-capability-boundary.json);
- [`ipc-schema-source.schema.json`](blueprint-v1/machine/ipc-schema-source.schema.json);
- [`no-claim-control-envelope-template.json`](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json);
- [`ipc-readiness-review.schema.json`](blueprint-v1/machine/ipc-readiness-review.schema.json);
- [`no-claim-ipc-readiness-template.json`](blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json);
- [`tools/validate_ipc_readiness_review.py`](../tools/validate_ipc_readiness_review.py).

Method:

Added a checked no-claim IPC readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null boundary/schema/reviewer fields, schema-generator axes, wire-transport axes, authority/identity axes, negative-test axes, owner-review axes, rejection rules, validation commands, `PB-011` evidence, `TASK-000003` scope, and IPC research-lane crosswalk coverage.

Decision:

Keep `PB-011` partial. The template defines what a future real owner-reviewed IPC readiness review must replace, but it does not implement or approve a schema generator, select wire encoding, generate types or validators, authenticate IPC connections, prove bounded queues/backpressure, define timeout/cancellation behavior, reject stale epochs, review negative tests, prove renderer security, prove agent security, prove process isolation, prove site isolation, approve production IPC, or support implementation claims.

Impact:

Future `TASK-000003` work now has a cross-scope readiness-review handoff object in addition to the IPC boundary inventory and schema-source template. Any real review must replace null boundary inventory, schema-source template, schema generator, wire encoding decision, owner reviewer, security reviewer, architecture reviewer, API reviewer, and performance reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-011` blocker should become real evidence first: schema generator source, wire encoding decision, connection authentication, bounded queues/backpressure, stale-epoch receiver rejection, timeout/cancellation behavior, or negative-test fixture generation?

## 2026-07-18 — Fresh-host readiness-review template

Question:

Can `PB-009` and `TASK-000002` gain one checked owner-review handoff object before independent fresh-host reproduction, owner-approved clean-VM equivalence, retained bootstrap/doctor/check/xtask logs, source-tree cleanliness review, failure-denominator review, rollback/cleanup review, environmental-waiver review, `PB-009` readiness promotion, release confidence, production readiness, implementation, or Chrome-class claims exist?

Inputs:

- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json);
- [`fresh-host-reproduction.schema.json`](project-buildout/machine/fresh-host-reproduction.schema.json);
- [`fresh-host-run-record.schema.json`](project-buildout/machine/fresh-host-run-record.schema.json);
- [`no-claim-run-record-template.json`](project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json);
- [`fresh-host-readiness-review.schema.json`](project-buildout/machine/fresh-host-readiness-review.schema.json);
- [`no-claim-fresh-host-readiness-template.json`](project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json);
- [`tools/validate_fresh_host_readiness_review.py`](../tools/validate_fresh_host_readiness_review.py).

Method:

Added a checked no-claim fresh-host readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null run-record/reference-host/clean-VM-waiver/reviewer fields, host-identity axes, source-checkout axes, command-execution axes, cache/artifact axes, failure-review axes, owner-review axes, rejection rules, validation commands, `PB-009` evidence, `TASK-000002` scope, and fresh-host research-lane crosswalk coverage.

Decision:

Keep `PB-009` partial. The template defines what a future real owner-reviewed fresh-host readiness review must replace, but it does not prove an independent fresh-host run, approve a clean-VM equivalent, review command execution, accept retained logs, prove source-tree cleanliness, accept failures or waivers, promote `PB-009`, create release confidence, approve production readiness, authorize implementation, or support Chrome-class claims.

Impact:

Future `TASK-000002` work now has both a per-run evidence record and a cross-scope readiness-review handoff object. Any real review must replace null run record, reference host, clean-VM waiver, owner reviewer, independent reviewer, release-operations reviewer, and quality reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-009` blocker should become real evidence first: reference-host designation, clean-VM waiver policy, retained command-log capture, cache/target-directory proof, source-tree cleanliness proof, or failure-denominator review?

## 2026-07-18 — Backup-ownership readiness-review template

Question:

Can `PB-019` and `TASK-000008` gain one checked owner-review handoff object before named qualified backups, owner identity verification, role-level review, subsystem competence review, path coverage, recent review records, availability evidence, succession evidence, recusal review, inactive-owner replacement, CODEOWNERS reconciliation, review-rule reconciliation, escalation-policy reconciliation, repository-access review, stale-access review, ownerless-path review, primary-only-path review, two-person control, owner coverage, release authority, signing authority, security-disclosure authority, legal approval, incident closure, production authority, broad readiness, or implementation claims exist?

Inputs:

- [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md);
- [`backup-ownership-gap.json`](project-buildout/machine/backup-ownership-gap.json);
- [`backup-ownership-gap.schema.json`](project-buildout/machine/backup-ownership-gap.schema.json);
- [`backup-owner-qualification-record.schema.json`](project-buildout/machine/backup-owner-qualification-record.schema.json);
- [`no-claim-backup-owner-qualification-template.json`](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json);
- [`backup-ownership-readiness-review.schema.json`](project-buildout/machine/backup-ownership-readiness-review.schema.json);
- [`no-claim-backup-ownership-readiness-template.json`](project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json);
- [`tools/validate_backup_ownership_readiness_review.py`](../tools/validate_backup_ownership_readiness_review.py).

Method:

Added a checked no-claim backup-ownership readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null inventory/qualification/reviewer fields, critical-scope coverage, qualification axes, reconciliation axes, two-person-control axes, authority-boundary axes, owner-review axes, rejection rules, validation commands, `PB-019` evidence, `TASK-000008` scope, and ownership research-lane crosswalk coverage.

Decision:

Keep `PB-019` blocked. The template defines what a future real owner-reviewed backup ownership readiness review must replace, but it does not name qualified backups, verify identity, prove role level, prove subsystem competence, prove path coverage, prove review history, prove availability, reconcile CODEOWNERS or access, create two-person control, provide owner coverage, grant release authority, grant signing authority, approve disclosure, approve legal posture, close incidents, create production authority, approve broad readiness, or support implementation.

Impact:

Future `TASK-000008` work now has both per-backup qualification and cross-scope readiness-review handoff objects. Any real review must replace null ownership inventory, qualification record set, owner reviewer, independent reviewer, security reviewer, release-operations reviewer, legal reviewer, and support reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-019` blocker should become real evidence first: named backup candidates, role/subsystem qualification records, CODEOWNERS and review-rule reconciliation, repository access and stale-access review, ownerless/primary-only path review, or two-person-control evidence?

## 2026-07-18 — Incident/patch readiness-review template

Question:

Can `PB-018` and `TASK-000010` gain one checked owner-review handoff object before executed private-intake tabletop output, emergency patch dry-run records, regression/backport evidence, signing/update dry-run evidence, coordinated disclosure rehearsal, postmortem evidence, role matrix review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported security versions, production-safe browsing, disclosure authority, stable promotion, signing authority, incident closure authority, or implementation claims exist?

Inputs:

- [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md);
- [`incident-patch-rehearsal.json`](security-engine/machine/incident-patch-rehearsal.json);
- [`incident-patch-rehearsal.schema.json`](security-engine/machine/incident-patch-rehearsal.schema.json);
- [`incident-patch-rehearsal-record.schema.json`](security-engine/machine/incident-patch-rehearsal-record.schema.json);
- [`no-claim-incident-patch-rehearsal-template.json`](security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json);
- [`incident-patch-readiness-review.schema.json`](security-engine/machine/incident-patch-readiness-review.schema.json);
- [`no-claim-incident-patch-readiness-template.json`](security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json);
- [`tools/validate_incident_patch_readiness_review.py`](../tools/validate_incident_patch_readiness_review.py).

Method:

Added a checked no-claim incident/patch readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null rehearsal/reference/private-channel/reviewer fields, private-intake axes, emergency-patch axes, incident-class axes, role-authority axes, evidence-control axes, owner-review axes, rejection rules, validation commands, `PB-018` evidence, `TASK-000010` scope, and incident/patch research-lane crosswalk coverage.

Decision:

Keep `PB-018` partial. The template defines what a future real owner-reviewed incident/patch readiness review must replace, but it does not approve executed private-intake tabletop output, emergency patch dry-run records, regression/backport evidence, signing/update dry-run evidence, coordinated disclosure rehearsal, postmortem evidence, role matrix review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported security versions, production-safe browsing, disclosure authority, stable promotion, signing authority, incident closure authority, or implementation.

Impact:

Future incident/patch work starts from a checked handoff object tying the inventory, rehearsal template, `PB-018`, and `TASK-000010` together. Any real review must replace null rehearsal record, reference platform, private channel, owner reviewer, independent reviewer, security reviewer, release-operations reviewer, legal reviewer, and support reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-018` blocker should become executable evidence first: private-intake tabletop, emergency patch dry run, regression/backport proof, disclosure rehearsal, role matrix review, or backup-owner coverage?

## 2026-07-18 — Package/update readiness-review template

Question:

Can `PB-017` and `TASK-000009` gain one checked owner-review handoff object before executable package manifests, update metadata parsers, signature threshold tests, staged install tests, rollback/migration tests, production-key separation review, release readiness, supported security, production updater, stable channel, public distribution, signing readiness, or implementation claims exist?

Inputs:

- [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md);
- [`research-package-update-lab.json`](release-operations/machine/research-package-update-lab.json);
- [`research-package-update-lab-package.schema.json`](release-operations/machine/research-package-update-lab-package.schema.json);
- [`no-claim-update-lab-template.json`](release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json);
- [`research-package-update-readiness-review.schema.json`](release-operations/machine/research-package-update-readiness-review.schema.json);
- [`no-claim-research-package-update-readiness-template.json`](release-operations/machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json);
- [`tools/validate_research_package_update_readiness_review.py`](../tools/validate_research_package_update_readiness_review.py).

Method:

Added a checked no-claim research package/update readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null lab-package/reference-platform/fixture-policy/reviewer fields, package, metadata, rollback, fixture, security/release, owner-review axes, rejection rules, validation commands, `PB-017` evidence, `TASK-000009` scope, and package/update research-lane crosswalk coverage.

Decision:

Keep `PB-017` partial. The template defines what a future real owner-reviewed package/update readiness review must replace, but it does not approve executable package manifests, update metadata parsers, signature threshold tests, staged install tests, rollback or migration tests, production-key separation, release readiness, supported security, production updater status, stable channel, public distribution, signing readiness, or implementation.

Impact:

Future package/update work starts from a checked handoff object tying the inventory, update-lab package template, `PB-017`, and `TASK-000009` together. Any real review must replace null lab-package, reference-platform, fixture-policy, owner-reviewer, independent-reviewer, release-operations-reviewer, security-reviewer, and privacy-reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-017` blocker should become executable evidence first: package manifest generation, update metadata parsing, fake-key signature threshold tests, staged install faults, rollback/migration tests, or production-key separation review?

## 2026-07-18 — Profile/session readiness-review template

Question:

Can `PB-016` and `TASK-000007` gain one checked owner-review handoff object before executable profile/session schemas, migration/fault tests, real-profile fixture approval, private-session readiness, protected-work readiness, data-loss safety, user-data handling readiness, production profile-format approval, sync, credential storage, release-path approval, or implementation claims exist?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [`profile-session-format-inventory.json`](storage/machine/profile-session-format-inventory.json);
- [`profile-session-schema-package.schema.json`](storage/machine/profile-session-schema-package.schema.json);
- [`no-claim-profile-session-schema-template.json`](storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json);
- [`profile-session-readiness-review.schema.json`](storage/machine/profile-session-readiness-review.schema.json);
- [`no-claim-profile-session-readiness-template.json`](storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json);
- [`tools/validate_profile_session_readiness_review.py`](../tools/validate_profile_session_readiness_review.py).

Method:

Added a checked no-claim profile/session readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null schema-package/reference-platform/fixture-policy/reviewer fields, format, behavior, migration, fixture, privacy, owner-review axes, rejection rules, validation commands, `PB-016` evidence, `TASK-000007` scope, and profile/session research-lane crosswalk coverage.

Decision:

Keep `PB-016` partial. The template defines what a future real owner-reviewed profile/session readiness review must replace, but it does not approve executable schemas, migration or fault tests, real-profile fixtures, private-session readiness, protected-work readiness, data-loss safety, user-data handling readiness, production profile formats, sync, credential storage, release paths, or implementation.

Impact:

Future profile/session work starts from a checked handoff object tying the inventory, schema-package template, `PB-016`, and `TASK-000007` together. Any real review must replace null schema-package, reference-platform, fixture-policy, owner-reviewer, independent-reviewer, and privacy-reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-016` blocker should become executable evidence first: schema package, migration/fault tests, real-profile fixture policy, private-session/protected-work behavior, or privacy and data-loss review?

## 2026-07-18 — Native UI readiness-review template

Question:

Can `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006` gain one checked owner-review handoff object before any `ADR-0013`, `ADR-0014`, `ADR-0016`, `UI-GATE-7`, `UI-GATE-10`, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production claim, or implementation claim exists?

Inputs:

- [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md);
- [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md);
- [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md);
- [`native-ui-readiness-review.schema.json`](ui-runtime/machine/native-ui-readiness-review.schema.json);
- [`no-claim-native-ui-readiness-template.json`](ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json);
- [`tools/validate_native_ui_readiness_review.py`](../tools/validate_native_ui_readiness_review.py).

Method:

Added a checked no-claim native UI readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null selected toolkit/adapter/platform/reviewer fields, gate axes, adapter/framework/page-surface/fixture/accessibility/release-exclusion/owner-review axes, rejection rules, validation commands, `PB-*` evidence, `TASK-000006` scope, and native-lane crosswalk coverage.

Decision:

Keep `PB-003`, `PB-004`, `PB-005`, `PB-014`, and `PB-015` partial. The template defines what a future real owner-reviewed native UI readiness review must replace, but it does not select a toolkit, accept an ADR, pass a UI gate, approve page-surface or accessibility readiness, authorize release-path UI, or support production or implementation claims.

Impact:

Future native shell work starts from one checked handoff object tying the five partial native UI gates and `TASK-000006` together. Any real review must replace null selected-toolkit, adapter-strategy, reference-platform, owner-reviewer, and independent-reviewer fields with retained evidence beyond the template.

Next question:

Which native UI blocker should become executable evidence first: `ADR-0013` adapter contracts, equivalent framework adapters, `UI-GATE-7` page-surface proof, rendered fixture packs, or reference-platform accessibility workflows?

## 2026-07-18 — ADR-0009 decision-review template

Question:

Can `PB-002` gain a checked ADR-0009 owner-review handoff object before any Servo source strategy, source baseline, component approval, source import, release-code authorization, readiness promotion, or implementation authority exists?

Inputs:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Decision Draft and Public-Claim Impact](project-buildout/16-adr-0009-decision-draft.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [`adr-0009-decision-review.schema.json`](blueprint-v1/machine/adr-0009-decision-review.schema.json);
- [`no-claim-decision-review-template.json`](blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json);
- [`tools/validate_adr_0009_evidence.py`](../tools/validate_adr_0009_evidence.py).

Method:

Added a checked no-claim ADR-0009 decision-review schema and template, then extended ADR-0009 evidence validation to require null option/baseline/reviewer fields, false decision-status flags, all `ADR9-EV-001` through `ADR9-EV-018` axes, option axes, owner-review axes, required document updates, rejection rules, unsupported boundaries, validation commands, and `PB-002` evidence.

Decision:

Keep `PB-002` blocked and keep `ADR-0009` at `no_source_strategy_decision`. The template defines what a future real owner-reviewed decision record must replace, but it does not select an option, approve Servo, import source, approve dependencies/components, change JavaScript runtime direction, authorize release code, or promote readiness.

Impact:

Future `TASK-000001` and `ADR9-EV-018` work now starts from a checked no-claim decision-review handoff object and must replace template-only null selected option, source baseline, feature profile, owner reviewer, independent reviewer, and false status flags with owner-reviewed evidence or explicit blocked status.

Next question:

Which `ADR9-EV-*` item should be closed, explicitly rejected, or converted into an expiring owner-approved exception first before a real ADR-0009 decision review can exist?

## 2026-07-18 — Build-readiness closure-review template

Question:

Can `PB-020` gain a checked no-claim closure-review handoff object before any owner-reviewed broad M1, all-information-ready-for-building, release, production, Chrome-class, performance, compatibility, security, accessibility, task-approval, readiness-promotion, or daily-driver claim exists?

Inputs:

- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [Implementation Kickoff Review Inventory](research/implementation-kickoff-review-inventory-2026-07.md);
- [Build Readiness Dependency Graph](research/build-readiness-dependency-graph-inventory-2026-07.md);
- [`build-readiness-closure-review.schema.json`](project-buildout/machine/build-readiness-closure-review.schema.json);
- [`no-claim-build-readiness-closure-template.json`](project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json);
- [`tools/validate_documentation_readiness_completion_audit.py`](../tools/validate_documentation_readiness_completion_audit.py).

Method:

Added a checked no-claim build-readiness closure-review schema and template, then extended the documentation-readiness completion-audit validator and aggregate blueprint validator to require the template, false closure flags, unresolved gate axes, owner-review axes, release-authority axes, lifecycle stages, rejection rules, validation commands, and `PB-020` evidence.

Decision:

Keep `PB-020` partial. The template defines what a future real build-readiness closure review must replace, but it does not close remaining P0 gates, approve tasks, grant release or production authority, or support all-information-ready-for-building language.

Impact:

Future build-readiness closure work now starts from a checked no-claim handoff object and must replace template-only null reviewers and false status flags with owner-reviewed evidence across source strategy, fresh-host reproduction, IPC, sandbox, benchmark, native-shell, page-surface, profile/session, package/update, incident-response, backup-ownership, owner-review, and release-authority gates.

Next question:

Which unresolved `PB-*` gate should receive owner-reviewed closure evidence first before a real build-readiness closure record can exist?

## 2026-07-18 — Backup-owner qualification template

Question:

Can `PB-019` gain a checked qualification handoff object before any named qualified backups, owner identity verification, role-level review, subsystem competence review, path coverage, availability record, CODEOWNERS reconciliation, stale-access review, two-person control, or owner-coverage authority exists?

Inputs:

- [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md);
- [Project-buildout handbook](project-buildout/README.md);
- [Ownership, CODEOWNERS, and Maintainer Ladder](project-buildout/02-ownership-codeowners-and-maintainer-ladder.md);
- [Release, Incident, Legal, Data, and Support Operations](project-buildout/08-release-incident-legal-data-and-support.md);
- [`backup-owner-qualification-record.schema.json`](project-buildout/machine/backup-owner-qualification-record.schema.json);
- [`no-claim-backup-owner-qualification-template.json`](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json);
- [`tools/validate_backup_ownership_gap.py`](../tools/validate_backup_ownership_gap.py).

Method:

Added a checked no-claim backup-owner qualification schema and template, then extended backup ownership validation to require null candidate fields, false qualification flags, qualification axes, reconciliation axes, two-person-control axes, lifecycle stages, placeholder rejection, authority-boundary rejection rules, unsupported claims, validation commands, and `PB-019` evidence.

Decision:

Keep `PB-019` blocked. The template defines what a future real backup-owner qualification record must replace, but it does not name qualified backups, verify identity, prove role level, prove subsystem competence, prove path coverage, prove review history, prove availability, reconcile CODEOWNERS or access, create two-person control, or provide owner coverage.

Impact:

Future `TASK-000008` work now starts from a checked no-claim backup-owner qualification handoff object and must replace template-only null candidate fields with named qualified backup, role-level, subsystem-competence, representative-path, review-record, availability, succession, recusal, inactivity, removal, emergency-replacement, reconciliation, two-person-control, and owner-review evidence. The current repository still needs backup-owner evidence beyond the checked no-claim backup-owner qualification template before any owner-coverage, release-authority, signing-authority, update-trust, security-disclosure, legal-approval, incident-closure, production-authority, broad-readiness, or implementation claim.

Next question:

Which real backup-owner candidates and qualification records should instantiate the checked template first without using placeholders, private contact details, title-only ownership, or documentation intent as authority?

## 2026-07-18 — Incident patch rehearsal-record template

Question:

Can `PB-018` gain a checked rehearsal handoff object before any executed private-intake tabletop, emergency patch dry run, regression/backport evidence, signing/update dry run, disclosure rehearsal, role review, backup-owner coverage, or incident-response authority exists?

Inputs:

- [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md);
- [Security policy](security.md);
- [Security Verification and Release Gates](security-engine/06-security-verification-and-release-gates.md);
- [Vulnerability Response and Supported Lifecycle](release-operations/08-vulnerability-response-and-supported-lifecycle.md);
- [`incident-patch-rehearsal-record.schema.json`](security-engine/machine/incident-patch-rehearsal-record.schema.json);
- [`no-claim-incident-patch-rehearsal-template.json`](security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json);
- [`tools/validate_incident_patch_rehearsal.py`](../tools/validate_incident_patch_rehearsal.py).

Method:

Added a checked no-claim incident patch rehearsal-record schema and template, then extended incident patch rehearsal validation to require private-intake axes, emergency-patch axes, incident classes, authority roles, lifecycle stages, fake-vulnerability fixture policy, rejection rules, unsupported boundaries, validation commands, `PB-018` evidence, and `TASK-000010` scope.

Decision:

Keep `PB-018` partial. The template defines what a future fake-vulnerability private tabletop and emergency patch dry run must record, but it does not provide executed tabletop output, emergency patch output, regression/backport evidence, signing/update dry-run evidence, disclosure rehearsal, role review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported-security evidence, or production-safe browsing evidence.

Impact:

Future `TASK-000010` work now starts from a checked no-claim incident patch rehearsal handoff object and must replace template-only fields with private tabletop, fake vulnerability, patch-branch, embargoed-CI, regression, backport, signing/update dry-run, disclosure, postmortem, role, backup-owner, cleanup, and owner-review evidence. The current repository still needs executable incident-response and emergency patch evidence beyond the checked no-claim incident patch rehearsal template before any incident-response, emergency-patch, supported-security, disclosure, signing, stable-promotion, incident-closure, or production-safe browsing claim.

Next question:

Which private tabletop and fake emergency patch harness should instantiate the checked template without publishing exploitable details or granting agents severity, disclosure, signing, stable-promotion, or incident-closure authority?

## 2026-07-18 — Research package/update lab-package template

Question:

Can `PB-017` gain a checked update-lab package handoff object before any executable package manifest, update metadata parser, signature threshold tests, staged install tests, rollback migration tests, production signing keys, offline root keys, stable channel, real updater, public distribution, or real-profile migration evidence exists?

Inputs:

- [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md);
- [Release Operations book](release-operations/README.md);
- [Update, Supply Chain, and Vulnerability Response](security-engine/05-update-supply-chain-and-vulnerability-response.md);
- [`research-package-update-lab-package.schema.json`](release-operations/machine/research-package-update-lab-package.schema.json);
- [`no-claim-update-lab-template.json`](release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json);
- [`validate_research_package_update_lab.py`](../tools/validate_research_package_update_lab.py).

Method:

Added a checked no-claim update-lab package schema and template, then extended research package/update lab validation to require manifest fields, metadata behavior axes, lab lifecycle stages, fake-key/local-metadata fixture policy, rejection rules, unsupported boundaries, validation commands, `PB-017` evidence, and `TASK-000009` scope.

Decision:

Keep `PB-017` partial. The template defines what a future executable fake-key local update-lab package must record, but it does not provide executable package manifests, metadata parsers, signature threshold tests, staged install tests, rollback or migration lab evidence, production-key review, owner review, release readiness, rollback safety, migration safety, supported security, or production updater evidence.

Impact:

Future `TASK-000009` work now starts from a checked update-lab package handoff object and must replace template-only fields with executable package-manifest, metadata-parser, signature-threshold, staged-install, rollback/migration, privacy-event, cleanup, and owner-review evidence. The current repository still needs executable update-lab evidence beyond the checked no-claim update-lab package template before any updater, release, rollback, migration, or supported-security claim.

Next question:

Which fake-key local package-manifest generator and update metadata parser should instantiate the checked template without creating a real updater, stable channel, public distribution path, or real-profile migration path?

## 2026-07-18 — Profile/session schema-package template

Question:

Can `PB-016` gain a checked schema-package handoff object before any executable profile, Space, session, snapshot, migration, or real-profile migration evidence exists?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [Storage and Recovery](storage/README.md);
- [Everyday Product Workflows](product-experience/README.md);
- [Network, Storage, Media, and Platform Services](blueprint-v1/07-network-storage-media.md);
- [`profile-session-schema-package.schema.json`](storage/machine/profile-session-schema-package.schema.json);
- [`no-claim-profile-session-schema-template.json`](storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json);
- [`validate_profile_session_formats.py`](../tools/validate_profile_session_formats.py).

Method:

Added a checked no-claim profile/session schema-package schema and template, then extended profile/session validation to require format targets, behavior axes, schema record requirements, migration lifecycle stages, fixture policy, rejection rules, unsupported boundaries, validation commands, `PB-016` evidence, and `TASK-000007` scope.

Decision:

Keep `PB-016` partial. The template defines what a future executable schema package must record, but it does not provide executable schemas, migration tests, fault tests, real-profile fixture approval, owner review, real-profile migration, sync, credential storage, data-loss safety, user-data handling readiness, or production profile-format evidence.

Impact:

Future `TASK-000007` work now starts from a checked schema-package handoff object and must replace template-only fields with executable schema, migration-test, fault-test, fixture-policy, and owner-review evidence. The current repository still needs executable schemas beyond the checked no-claim schema-package template before any profile/session, migration, or data-loss claim.

Next question:

Which executable schema fixture harness should instantiate the checked template for profile, Space, session, snapshot, and migration records without touching real user profiles?

## 2026-07-18 — Sandbox probe-package template

Question:

Can `PB-012` gain a checked expected-deny probe-package handoff object before any packaged sandbox probe, effective platform-policy capture, or security-gate evidence exists?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [Security, Privacy, and Sandbox Model](blueprint-v1/08-security-and-sandbox.md);
- [Sandbox Brokers and Platform Containment](security-engine/02-sandbox-brokers-and-platform-containment.md);
- [Security Verification and Release Gates](security-engine/06-security-verification-and-release-gates.md);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- [`sandbox-probe-package.schema.json`](security-engine/machine/sandbox-probe-package.schema.json);
- [`no-claim-expected-deny-template.json`](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json);
- [`validate_sandbox_probe_inventory.py`](../tools/validate_sandbox_probe_inventory.py).

Method:

Added a checked no-claim sandbox probe-package schema and template, then extended sandbox probe validation to require role targets, required access surfaces, platform-specific policy artifacts, package lifecycle stages, result-record fields, rejection rules, unsupported boundaries, validation commands, `PB-012` evidence, and `TASK-000004` scope.

Decision:

Keep `PB-012` partial. The template defines what a future expected-deny package must record, but it does not provide a packaged harness, effective policy capture, platform matrix execution, owner review, sandbox-readiness claim, renderer-security claim, site-isolation proof, hostile-browsing safety claim, `SEC-GATE-1`, `SEC-GATE-6`, or production-safety evidence.

Impact:

Future `TASK-000004` work now starts from a checked package handoff object and must replace template-only fields with real host-safe execution evidence. The current repository still needs packaged expected-deny probes beyond the checked no-claim template before any sandbox or security-gate claim.

Next question:

Which host-safe renderer or network expected-deny probe should be packaged first without touching real profiles, real credentials, production signing keys, or developer-host state outside bounded fixtures?

## 2026-07-18 — IPC schema-source template

Question:

Can `PB-011` gain a checked schema-source handoff object before any schema generator, generated type, or wire encoding is approved?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [System Architecture](blueprint-v1/04-system-architecture.md);
- [Security, Privacy, and Sandbox Model](blueprint-v1/08-security-and-sandbox.md);
- [Schemas, Errors, Versioning, and Compatibility](api-design/03-schemas-errors-versioning-and-compatibility.md);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- [`ipc-schema-source.schema.json`](blueprint-v1/machine/ipc-schema-source.schema.json);
- [`no-claim-control-envelope-template.json`](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json);
- [`validate_ipc_capability_boundaries.py`](../tools/validate_ipc_capability_boundaries.py).

Method:

Added a checked no-claim IPC schema-source template and extended IPC validation to cover required message metadata, process-capability role links, generator output plans, negative fixture plans for malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases, review gates, unsupported boundaries, and validation commands.

Decision:

Keep `PB-011` partial. The template defines the shape a future generator proposal must satisfy, but it does not approve a generator source, wire encoding, generated type, generated validator, generated fixture, timeout/cancellation implementation, renderer-security claim, agent-security claim, process-isolation claim, site-isolation claim, production IPC claim, or broad implementation readiness.

Impact:

Future `TASK-000003` work now has a checked starting object linked to `process-capabilities.json`, the IPC boundary inventory, and the architecture/security/API docs. The current repository still needs implemented schema-generator evidence beyond the checked no-claim schema-source template before any IPC readiness claim.

Next question:

Which contained IPC generator experiment should produce the first generated fixtures and negative tests without expanding authority?

## 2026-07-18 — Benchmark claim-bundle template

Question:

Can `PB-013` public performance and Chrome-class claim governance gain a checked claim-bundle shape without approving any claim?

Inputs:

- [Chrome-Class Performance Runbook](research/chrome-class-performance-runbook-2026-07.md);
- [`benchmark-claim-bundle.schema.json`](blueprint-v1/machine/benchmark-claim-bundle.schema.json);
- [`no-claim-public-claim-template.json`](blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json);
- [`validate_benchmark_claim_bundles.py`](../tools/validate_benchmark_claim_bundles.py);
- `PB-013`, `TASK-000005`, and the research-readiness crosswalk.

Method:

Added a checked no-claim claim-bundle schema, template, focused validator, and aggregate validator hook covering benchmark registry references, required evidence inputs, statistical controls, workload equivalence, denominator accounting, overhead disclosure, expiry, publication controls, rejection rules, unsupported behavior, missing proof, and validation commands.

Decision:

Keep `PB-013` at `documented_no_runner`. The template proves only the future public-claim evidence shape; it does not approve a benchmark run, result, competitor comparison, trace, raw sample, memory result, energy result, Chrome-class claim, faster claim, lower-memory claim, lower-energy claim, compatibility claim, security claim, accessibility claim, production claim, or daily-driver claim.

Impact:

Future public claims now have a checked handoff object tied to existing benchmark registries and task gating. The current repository still needs owner-reviewed claim bundles from real raw artifacts before any public performance language is supportable.

Next question:

Which benchmark evidence lane should produce the first owner-reviewed artifact bundle and claim-bundle draft from real runs?

## 2026-07-18 — Task approval template control

Question:

Can proposed `TASK-*` rows gain a checked approval-manifest shape before any task is actually approved or executed?

Inputs:

- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Agent Execution](agent-execution/README.md);
- [`execution-task.schema.json`](agent-execution/machine/execution-task.schema.json);
- [`agent-run-manifest.schema.json`](agent-execution/machine/agent-run-manifest.schema.json);
- [`evidence-bundle.schema.json`](agent-execution/machine/evidence-bundle.schema.json);
- [`task-approval-template.schema.json`](agent-execution/machine/task-approval-template.schema.json);
- [`no-claim-task-approval-template.json`](agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json);
- [`validate_task_approval_templates.py`](../tools/validate_task_approval_templates.py).

Method:

Added a checked no-claim approval template and dependency-free validator covering proposed task coverage, owner and independent reviewer inputs, immutable manifest requirements, allowed/prohibited authority, credential and network limits, evidence bundle requirements, rollback, expiry, rejection rules, and unsupported readiness/product boundaries.

Decision:

Keep every queued task proposed. The template defines what an owner must fill before execution; it does not approve a task, start a run, accept evidence, promote readiness, authorize release work, or support Chrome-class, performance, compatibility, security, accessibility, beta, stable, production, release, or daily-driver claims.

Impact:

The handoff from planning evidence to owner-reviewed execution evidence is now checkable. Future `TASK-000001` or `TASK-000002` work can be prepared against a concrete approval-manifest shape instead of relying on prose alone.

Next question:

Which proposed task should receive the first owner-filled approval manifest and independent review?

## 2026-07-18 — Documentation-readiness validator command coverage

Question:

Can the documentation-readiness evidence matrix stay aligned with the growing focused validator family as no-claim machine-readable evidence lanes are added?

Inputs:

- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [`documentation-readiness-completion-audit.json`](project-buildout/machine/documentation-readiness-completion-audit.json);
- [`validate_blueprint.py`](../tools/validate_blueprint.py);
- current `tools/validate_*.py` focused validators.

Method:

Expanded the direct validation-command list to name every current focused `tools/validate_*.py` command before diff and Cargo checks, and added aggregate validation coverage that fails when a focused validator exists without a corresponding documentation-readiness command.

Decision:

Keep documentation readiness scoped to contained M0 only. This change improves handoff fidelity and drift detection; it does not make the documentation complete for broad building, approve tasks, promote any `PB-*` item, or support Chrome-class, performance, compatibility, security, accessibility, production, beta, stable, release, or daily-driver claims.

Impact:

Maintainers debugging documentation-readiness evidence can now follow the matrix without skipping newer focused validators such as fresh-host run records, Servo local-compatibility HTTPS harnesses, benchmark registries, UI adapter contracts, IPC boundaries, or sandbox probes.

Next question:

Which remaining blocker lane should produce owner-reviewed execution evidence first instead of only checked no-claim planning evidence?

## 2026-07-18 — PB-009 fresh-host run-record template

Question:

Can `PB-009` define a checked machine-readable run record before an independent fresh-host run exists, without promoting current-host diagnostics to build confidence?

Inputs:

- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json);
- [`fresh-host-run-record.schema.json`](project-buildout/machine/fresh-host-run-record.schema.json);
- [`no-claim-run-record-template.json`](project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json);
- [`validate_fresh_host_reproduction.py`](../tools/validate_fresh_host_reproduction.py);
- [`validate_fresh_host_run_records.py`](../tools/validate_fresh_host_run_records.py);
- `PB-009`, `TASK-000002`, the research crosswalk, and the pre-build readiness registry.

Method:

Added a checked no-claim run-record schema, a `template_no_execution` record, and a dependency-free validator covering independent host identity, checkout facts, wrapper and direct `xtask` command records, retained-output hashes, cache and target-directory controls, source-tree cleanliness, failure denominator, prohibited evidence, and unsupported readiness boundaries.

Decision:

Keep `PB-009` partial. The run-record template proves only the future evidence shape. It explicitly records no independent fresh-host reproduction, no owner-approved clean-VM equivalent, no command execution evidence, no retained bootstrap/doctor/check/xtask logs, no readiness promotion, and no preview, beta, stable, production, release-confidence, or Chrome-class claim.

Impact:

Future `TASK-000002` work now has a checked target record for retained logs and failure accounting. The next proof remains an actual independent fresh-host or owner-approved clean-VM run with owner review.

Next question:

Which owner-approved reference host or clean VM should fill the checked run record with real bootstrap, doctor, check, and `xtask` evidence?

## 2026-07-18 — ADR-0009 HTTPS host-alias harness plan

Question:

Can the checked `ADR9-EV-013` local compatibility corpus gain a validated HTTPS host-alias execution plan without becoming browser-run compatibility evidence?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`servo-local-compatibility-https-harness.schema.json`](blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json);
- [`no-claim-https-host-alias.plan.json`](blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json);
- [`validate_servo_local_compatibility_https_harness.py`](../tools/validate_servo_local_compatibility_https_harness.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, research crosswalk, and pre-build readiness registry.

Method:

Added a dependency-free validator and checked no-claim harness plan that binds every corpus origin to future SNI/SAN coverage, isolated trust-store handling, transient host-to-loopback aliasing, cleanup proof, browser-visible-origin evidence, per-origin route records, raw logs, certificate fingerprints, and failure-denominator accounting.

Decision:

Keep `PB-002` blocked and `ADR9-EV-013` partial. The harness plan proves only the future HTTPS/browser execution contract. It explicitly records no HTTPS server, no certificate or private key, no trust-store mutation, no host alias, no browser launch, no Servo run, no WPT result, no Test262 result, no Turing compatibility claim, no Chrome-class claim, and no release-code authorization.

Impact:

The remaining `ADR9-EV-013` work is now execution of the checked HTTPS host-alias harness, raw Servo run evidence, focused WPT subset runs, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan.

Next question:

Should the next `ADR9-EV-013` step execute the checked HTTPS host-alias harness against the external Servo build, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — ADR-0009 local compatibility route self-test

Question:

Can the checked `ADR9-EV-013` local fixture set be served and verified through repository-owned route plumbing before any HTTPS, browser, WPT, or Test262 run exists?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- `benchmarks/compatibility/adr0009/no-claim-tiny/`;
- [`serve_servo_local_compatibility_corpus.py`](../tools/serve_servo_local_compatibility_corpus.py);
- [`validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, and the pre-build readiness registry.

Method:

Added a dependency-free HTTP/1.1 loopback route self-test that validates the manifest, starts a temporary server, uses Host headers for the declared `turing.invalid` origins, serves every generated fixture route, verifies status, content type, byte count, SHA-256, no-store cache behavior, shutdown, and closed-port behavior, and emits `ADR9.EV013.NOCLAIM_ROUTE_SELF_TEST.2026_07`.

Decision:

Keep `PB-002` blocked and `ADR9-EV-013` partial. The route self-test proves only local route plumbing for generated fixtures. It explicitly records no HTTPS, no DNS modification, no browser launch, no WPT result, no Test262 result, no Servo adoption, no Turing compatibility claim, no Chrome-class claim, and no release-code authorization.

Impact:

The remaining `ADR9-EV-013` work is now HTTPS harness and host-alias browser execution for the checked fixtures, raw Servo run evidence, focused WPT subset runs, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan.

Next question:

Should the next `ADR9-EV-013` step add local HTTPS and browser execution, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — ADR-0009 local compatibility fixtures

Question:

Can the checked `ADR9-EV-013` tiny local compatibility corpus manifest point at generated local fixtures without becoming browser-run compatibility evidence?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- `benchmarks/compatibility/adr0009/no-claim-tiny/`;
- [`tools/validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, and the pre-build readiness registry.

Method:

Added generated local HTML fixtures for the eight checked case categories, recorded each fixture path, route, origin, byte count, hash, and license in the manifest, and extended the validator to verify file existence, SHA-256, byte counts, LF line endings, local-only `turing.invalid` URLs, and per-origin fixture coverage.

Decision:

Keep `PB-002` blocked and `ADR9-EV-013` partial. The fixtures are no-claim local assets for a future harness; they are not browser-run evidence, WPT/Test262 evidence, Servo approval, Turing compatibility evidence, or Chrome-class evidence.

Impact:

The remaining `ADR9-EV-013` work is now executing the checked HTTPS host-alias harness for the checked fixtures, raw Servo run evidence, focused WPT subset runs, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan.

Next question:

Should the next `ADR9-EV-013` step build the local HTTPS harness and run the checked fixtures, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — ADR-0009 local compatibility corpus contract

Question:

Can the `ADR9-EV-013` tiny local compatibility corpus become a checked no-claim manifest before any Servo, Turing, WPT, or Test262 compatibility result exists?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`servo-local-compatibility-corpus.schema.json`](blueprint-v1/machine/servo-local-compatibility-corpus.schema.json);
- [`no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- [`tools/validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, and the pre-build readiness registry.

Method:

Added a dependency-free validator and checked manifest covering eight local-only compatibility case categories, required assertion groups, required artifacts, `turing.invalid` origins, WPT focus areas, Test262 attribution language, failure denominators, and no-claim boundaries.

Decision:

Keep `PB-002` and `ADR9-EV-013` partial. The manifest is a contract for future routes, fixtures, and runs; it is not browser-run evidence, a WPT/Test262 result, a Servo adoption decision, or a compatibility claim.

Impact:

The source-strategy handoff gained a stable local compatibility corpus contract. The later fixture-materialization log entry supersedes the manifest-only next step.

Next question:

Should the next `ADR9-EV-013` step build the local HTTPS harness and run the checked fixtures, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — Servo unsafe and FFI contract review

Question:

What unsafe-code and C ABI contract evidence is needed before any Servo-derived component boundary can be proposed for `ADR-0009`?

Inputs:

- [Servo Unsafe and FFI Contract Review](research/servo-unsafe-ffi-contract-review-2026-07.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- the clean external Servo checkout at `C:\ts\servo` and prior generated/native/unsafe/FFI classification evidence.

Method:

Added a dedicated `ADR9-EV-009` and `ADR9-EV-010` triage report that counts unsafe and FFI surfaces, identifies C API contract families, and separates JavaScript rooting/tracing and WebGL/driver boundary review classes from release approval.

Decision:

Keep `PB-002` blocked. The report narrows the unsafe/FFI review plan but does not approve Servo, unsafe code, the C API, SpiderMonkey integration, WebGL integration, a component boundary, source adoption, dependency adoption, or release code.

Impact:

The source-strategy evidence registry, matrix, readiness records, and indexes now distinguish unsafe/FFI contract triage from the still-missing block-level unsafe ledger, ABI policy, conformance tests, owner review, and ADR decision.

Next question:

Which `ADR-0009` candidate boundary should get the first block-level unsafe ledger and versioned ABI contract review?

## 2026-07-18 — Documentation readiness completion audit

Question:

Can the documentation-preparation work be audited as organized enough for contained M0 continuation without claiming that all information is ready for broad browser construction, Chrome-class competition, production, release, or performance/security/compatibility/accessibility claims?

Inputs:

- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [`documentation-readiness-completion-audit.json`](project-buildout/machine/documentation-readiness-completion-audit.json);
- [`documentation-readiness-completion-audit.schema.json`](project-buildout/machine/documentation-readiness-completion-audit.schema.json);
- [`tools/validate_documentation_readiness_completion_audit.py`](../tools/validate_documentation_readiness_completion_audit.py);
- first-entry docs, pre-build readiness, kickoff inventory, dependency graph, task queue, research crosswalk, evidence matrix, Definition of Done, and validation records.

Method:

Added a checked no-claim audit and focused validator covering entrypoints, stop/resume continuity, machine registries, research lanes, task handoff, sequencing, claim boundaries, validation, owner-only decisions, and remaining full-goal blockers.

Decision:

Keep `PB-020` partial. The audit supports contained M0 continuation only and explicitly rejects all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, accessibility, and daily-driver claims.

Impact:

The audit makes premature completion language machine-detectable. It does not approve tasks, close blockers, or promote readiness.

Next question:

Which owner-reviewed execution proof should follow first: `TASK-000001` source-strategy closure or `TASK-000002` fresh-host reproduction?

## 2026-07-18 — Build readiness dependency graph

Question:

Can the current build-readiness task order and cross-lane sequencing become a checked dependency graph without approving proposed tasks or promoting readiness?

Inputs:

- [Build Readiness Dependency Graph Inventory](research/build-readiness-dependency-graph-inventory-2026-07.md);
- [`build-readiness-dependency-graph.json`](project-buildout/machine/build-readiness-dependency-graph.json);
- [`build-readiness-dependency-graph.schema.json`](project-buildout/machine/build-readiness-dependency-graph.schema.json);
- [`tools/validate_build_readiness_dependency_graph.py`](../tools/validate_build_readiness_dependency_graph.py);
- pre-build readiness, build-readiness task queue, implementation kickoff inventory, operating board, evidence matrix, research crosswalk, agent-execution, production-readiness, and Definition of Done records.

Method:

Added a checked no-claim graph and focused validator covering unresolved readiness items, proposed task nodes, task dependencies from the task queue, readiness-to-task edges, `ADR-0009`, `ADR-0013`, `ADR-0014`, `ADR-0016`, `UI-GATE-7`, `PB-020` dependency edges, and parallel no-claim lanes.

Decision:

Keep `PB-020` partial. The graph makes sequencing drift visible and machine-checkable, but it does not approve task execution, change dependencies, close blockers, or promote readiness.

Impact:

No task approval, readiness promotion, broad M1 implementation, developer preview, beta, stable, production, Chrome-class, performance, compatibility, security, accessibility, release-readiness, or daily-driver claim is supported.

Next question:

Which graph edge should become owner-reviewed execution evidence first, `TASK-000001` source-strategy closure or `TASK-000002` fresh-host reproduction?

## 2026-07-18 — Implementation kickoff review inventory

Question:

Can `PB-020` become a checked stop/resume inventory for unresolved pre-build lanes without promoting broad implementation readiness or approving tasks?

Inputs:

- [Implementation Kickoff Review Inventory](research/implementation-kickoff-review-inventory-2026-07.md);
- [`implementation-kickoff-review.json`](project-buildout/machine/implementation-kickoff-review.json);
- [`implementation-kickoff-review.schema.json`](project-buildout/machine/implementation-kickoff-review.schema.json);
- [`tools/validate_implementation_kickoff_review.py`](../tools/validate_implementation_kickoff_review.py);
- pre-build checklist, operating board, task queue, evidence matrix, research crosswalk, agent-execution, production-readiness, and Definition of Done records.

Method:

Added a checked no-claim project-buildout registry and validator covering unresolved `PB-002`, `PB-003`, `PB-004`, `PB-005`, `PB-009`, `PB-011`, `PB-012`, `PB-013`, `PB-014`, `PB-015`, `PB-016`, `PB-017`, `PB-018`, and `PB-019` status, current evidence, first next actions, required pre-M1 evidence, owner-only decisions, prohibited claims, kickoff gates, and release-authority boundaries. The aggregate blueprint validator now requires the report, schema, registry, focused validator, and `PB-020` evidence.

Decision:

Keep `PB-020` partial. The inventory improves handoff continuity and drift detection, but it does not close remaining P0 items, approve proposed tasks, authorize M1 expansion, or promote readiness.

Impact:

No broad implementation, developer preview, beta, stable, production, Chrome-class, performance, memory, energy, compatibility, security, accessibility, daily-driver, release-readiness, task-approval, or readiness-promotion claim is supported.

Next question:

Which owner-reviewed lane should close first: `PB-002` source strategy or `PB-009` fresh-host reproduction?

## 2026-07-18 — Toolkit-neutral UI adapter contract inventory

Question:

Can `PB-003` move from a buildable M0 UI model and prose architecture into checked adapter-contract planning evidence without implying `ADR-0013`, native adapter implementation, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, or release-path UI approval?

Inputs:

- [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- [`adapter-contract-inventory.json`](ui-runtime/machine/adapter-contract-inventory.json);
- [`adapter-contract-inventory.schema.json`](ui-runtime/machine/adapter-contract-inventory.schema.json);
- [`tools/validate_ui_adapter_contract.py`](../tools/validate_ui_adapter_contract.py);
- `crates/turing-ui-model`, Native UI Runtime, readiness, task-queue, crosswalk, component, page-surface, and accessibility records.

Method:

Added a checked no-claim UI-runtime registry and validator covering state, command, surface, accessibility, diagnostic, and adapter contract areas; current M0 model invariants; denied toolkit-owned navigation, profile, permission, credential, agent, Plug-in, persistence, and update authority; required `ADR-0013`, contract, adapter prototype, negative-test, and owner-review evidence; and unsupported readiness boundaries.

Decision:

Keep `PB-003` partial. The inventory makes missing adapter-contract proof reviewable; it does not provide accepted `ADR-0013`, complete contracts, a native adapter prototype, no-toolkit-owned-authority negative tests, owner review, or release-path UI approval.

Impact:

No native-shell readiness, trusted-chrome readiness, accessibility readiness, page-surface approval, toolkit selection, release-path UI approval, production, beta, stable, Chrome-class, or implementation claim is supported.

Next question:

Which `ADR-0013` draft and first native adapter trait prototype should `TASK-000006` propose so toolkit callbacks can be proven command-only before framework bake-off work expands?

## 2026-07-18 — Fresh host reproduction inventory

Question:

Can `PB-009` move from a generic "independent fresh-host reproduction" blocker into checked no-claim planning evidence without implying that an independent clean-host run has already happened?

Inputs:

- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json);
- [`fresh-host-reproduction.schema.json`](project-buildout/machine/fresh-host-reproduction.schema.json);
- [`tools/validate_fresh_host_reproduction.py`](../tools/validate_fresh_host_reproduction.py);
- [M0 build foundation](research/m0-build-foundation-2026-07.md);
- Build readiness board, task queue, pre-build readiness registry, research crosswalk, and `xtask` records.

Method:

Added a checked no-claim fresh-host registry and validator covering clean host facts, source checkout identity, bootstrap/doctor/check/xtask logs, cache and target-directory behavior, source-tree cleanliness, failure classification, rollback notes, and rejection rules for same-host reruns or reused build outputs. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-009` evidence, and `TASK-000002` scope.

Decision:

Keep `PB-009` partial. The inventory makes missing clean-host proof reviewable; it does not provide an independent fresh-host run, owner-approved clean-VM equivalent, retained clean-host logs, cache proof, source-tree proof, or owner review.

Impact:

No `PB-009` readiness promotion, broad M1 readiness, preview readiness, beta readiness, stable readiness, production readiness, release confidence, Chrome-class claim, source-strategy approval, or benchmark claim is supported.

Next question:

Which owner-approved host or clean-VM environment should execute `TASK-000002` so clean-host reproduction evidence can become actual proof rather than planning inventory?

## 2026-07-18 — Native UI framework bake-off inventory

Question:

Can `PB-004` move from qualitative native UI framework evaluation into checked no-claim planning evidence without implying toolkit selection, `ADR-0014`, accessibility readiness, page-surface approval, license/provenance approval, trusted-chrome readiness, or release-path UI approval?

Inputs:

- [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md);
- [`framework-bakeoff-inventory.json`](ui-runtime/machine/framework-bakeoff-inventory.json);
- [`framework-bakeoff-inventory.schema.json`](ui-runtime/machine/framework-bakeoff-inventory.schema.json);
- [`tools/validate_framework_bakeoff.py`](../tools/validate_framework_bakeoff.py);
- [Native UI framework evaluation](research/native-ui-framework-evaluation-2026-07.md);
- Native UI Runtime, Blueprint, readiness, task-queue, crosswalk, security, and research-program records.

Method:

Added a checked no-claim framework bake-off registry and validator covering nine candidate summaries, six external source observations, equivalent Slint/Vizia/Floem-or-GPUI adapter scope, evidence axes, disqualifiers, and unsupported claim boundaries. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-004` evidence, and `TASK-000006` scope.

Decision:

Keep `PB-004` partial. The inventory makes missing framework-selection proof reviewable; it does not provide equivalent adapter runs, raw artifacts, legal/provenance review, accessibility evidence, page-surface evidence, package/runtime-exclusion proof, owner review, or `ADR-0014`.

Impact:

No UI toolkit selection, Slint approval, accessibility readiness, IME/keyboard proof, page-surface approval, trusted-chrome readiness, performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or release-path UI claim is supported.

Next question:

Which first reference-shell adapter execution manifest should `TASK-000006` propose so the bake-off can become executable without selecting the production toolkit?

## 2026-07-18 — Page surface composition inventory

Question:

Can `PB-005` move from page-surface/compositor architecture prose into checked no-claim planning evidence without implying `UI-GATE-7`, compositor ownership, typed handle implementation, renderer-texture composition, toolkit selection, or release-path UI approval?

Inputs:

- [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md);
- [`page-surface-composition.json`](ui-runtime/machine/page-surface-composition.json);
- [`page-surface-composition.schema.json`](ui-runtime/machine/page-surface-composition.schema.json);
- [`tools/validate_page_surface_composition.py`](../tools/validate_page_surface_composition.py);
- Native UI Runtime, paint/compositor/GPU, Blueprint, readiness, task-queue, and crosswalk records.

Method:

Added a checked no-claim page-surface registry and validator covering 14 surface contract fields, four composition alternatives, 11 workflow tests, nine failure cases, eight security identity boundaries, evidence blockers, source-record linkage, and unsupported claim boundaries. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-005` evidence, and `TASK-000006` scope.

Decision:

Keep `PB-005` partial. The inventory makes missing page-surface proof reviewable; it does not provide executable `UI-GATE-7` prototype evidence, typed page-surface handles, brokered surface handles, renderer-produced page textures, software fallback, stale-handle negative tests, latency/frame-pacing traces, `ADR-0016`, compositor ownership, or owner review.

Impact:

No page-surface approval, UI toolkit selection, trusted-chrome readiness, accessibility readiness, performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or release-path UI claim is supported.

Next question:

Which isolated reference-shell adapter and simulated renderer frame source should `TASK-000006` propose first so `UI-GATE-7` can become executable without selecting the production toolkit?

## 2026-07-18 — Window input accessibility spike inventory

Question:

Can `PB-015` move from native-shell accessibility prose into checked no-claim workflow evidence without implying accessibility readiness, screen-reader coverage, page-tree proof, IME correctness, crash/GPU-loss behavior, UI toolkit selection, or release-path UI approval?

Inputs:

- [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md);
- [`window-input-accessibility-spike.json`](accessibility/machine/window-input-accessibility-spike.json);
- [`window-input-accessibility-spike.schema.json`](accessibility/machine/window-input-accessibility-spike.schema.json);
- [`tools/validate_window_input_accessibility_spike.py`](../tools/validate_window_input_accessibility_spike.py);
- [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- Blueprint, accessibility, platform, UI-runtime, readiness, task-queue, and crosswalk records.

Method:

Added a checked no-claim accessibility registry and validator covering windowing, input, IME, accessibility-tree, page-tree composition, clipboard, drag-drop, localization, zoom, high contrast, forced colors, reduced motion, crash recovery, renderer hang, GPU-loss, nine core shell workflows, platform assistive-technology rows for VoiceOver, Narrator, NVDA, and Orca, and explicit evidence blockers. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-015` evidence, and `TASK-000006` allowed paths.

Decision:

Keep `PB-015` partial. The inventory makes the workflow matrix and missing proof reviewable; it does not provide executable reference-platform runs, manual assistive-technology transcripts, platform accessibility snapshots, composed chrome/page-tree diffs, IME/clipboard/drag-drop fixtures, renderer-hang/crash/GPU-loss fault evidence, latency/resource traces, or owner review.

Impact:

No accessibility-readiness, screen-reader, manual assistive-technology, page-tree, IME, keyboard, clipboard/drag-drop, localization, zoom/contrast/motion, crash-recovery, renderer-hang, GPU-loss, `UI-GATE-7`, `UI-GATE-10`, release-path UI, toolkit-selection, production, beta, stable, or Chrome-class claim is supported.

Next question:

Which reference-platform workflow runner and manual assistive-technology transcript format should `TASK-000006` propose first so PB-015 evidence can become executable without selecting a toolkit?

## 2026-07-18 — Sandbox probe inventory

Question:

Can `PB-012` move from general sandbox requirements into checked no-claim planning evidence without implying sandbox readiness, renderer security, site isolation, hostile-browsing safety, platform containment, SEC-GATE evidence, or production safety?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [`sandbox-probe-inventory.json`](security-engine/machine/sandbox-probe-inventory.json);
- [`sandbox-probe-inventory.schema.json`](security-engine/machine/sandbox-probe-inventory.schema.json);
- [`tools/validate_sandbox_probe_inventory.py`](../tools/validate_sandbox_probe_inventory.py);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- security, sandbox, platform, testing, and research-program chapters.

Method:

Added a checked no-claim security-engine registry and validator covering renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater probe targets across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC surfaces. The inventory also records macOS, Windows, and Linux evidence requirements, harness blockers, host-safety requirements, and unsupported claim boundaries. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-012` evidence, and `TASK-000004` allowed paths.

Decision:

Keep `PB-012` partial. The inventory makes the target matrix and missing proof reviewable; it does not provide packaged role runners, effective platform-policy capture, broker fixtures, compromised-client harnesses, platform-matrix execution, or owner review.

Impact:

No sandbox-readiness, renderer-security, site-isolation, hostile-browsing safety, platform-containment, SEC-GATE-1, SEC-GATE-6, production-safety, broad M1 readiness, beta, stable, or implementation-readiness claim is supported.

Next question:

Which host-safe packaged probe runner should `TASK-000004` propose first so expected-deny results can be collected without damaging developer machines or weakening sandbox policy?

## 2026-07-18 — IPC capability boundary inventory

Question:

Can `PB-011` move from crate evidence and process-capability prose into checked no-claim boundary evidence without implying a canonical schema generator, wire encoding decision, renderer-security claim, agent-security claim, process-isolation readiness, site-isolation, timeout/cancellation implementation, or production IPC readiness?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [`ipc-capability-boundary.json`](blueprint-v1/machine/ipc-capability-boundary.json);
- [`ipc-capability-boundary.schema.json`](blueprint-v1/machine/ipc-capability-boundary.schema.json);
- [`tools/validate_ipc_capability_boundaries.py`](../tools/validate_ipc_capability_boundaries.py);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- `crates/turing-ipc`, `crates/turing-kernel`, and `crates/turing-types`.

Method:

Added a checked no-claim architecture/API registry and validator covering the current M0 bounded `ControlEnvelope`, oversized-message unit test, typed identities, role-capability model, process-capability role records, schema/transport blockers, negative coverage requirements, and unsupported authority boundaries. The aggregate blueprint validator now requires the registry, report, and focused validator while keeping `PB-011` partial and `TASK-000003` proposed.

Decision:

Keep `PB-011` partial. The inventory makes current evidence and missing proof reviewable; it does not approve generated schemas, choose a wire format, prove connection authentication, implement queues/backpressure, prove stale-epoch rejection, implement timeout/cancellation behavior, or cover malformed, duplicate, reordered, unauthorized, and wrong-principal negative cases beyond the listed M0 oversized-message test.

Impact:

No renderer-security, agent-security, process-isolation, site-isolation, production IPC, schema-generator, wire-encoding, timeout/cancellation, broad M1 readiness, beta, stable, production, or implementation-readiness claim is supported.

Next question:

Which canonical IPC schema source and wire-encoding decision should `TASK-000003` propose before generated negative fixtures and receiver-side authority checks become executable?

## 2026-07-18 — Backup ownership gap inventory

Question:

Can `PB-019` move from ownership prose into checked blocked evidence without implying that named qualified backups, two-person control, release authority, signing authority, security-disclosure authority, incident-closure authority, legal approval, production authority, or owner coverage exists?

Inputs:

- [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md);
- [`backup-ownership-gap.json`](project-buildout/machine/backup-ownership-gap.json);
- [`backup-ownership-gap.schema.json`](project-buildout/machine/backup-ownership-gap.schema.json);
- [`tools/validate_backup_ownership_gap.py`](../tools/validate_backup_ownership_gap.py);
- [`professional-owners.json`](blueprint-v1/machine/professional-owners.json);
- root [CODEOWNERS](../.github/CODEOWNERS).

Method:

Added a checked blocked project-buildout registry and validator covering build-critical program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data scopes. The validator checks provisional primary-only owner records, null backups, CODEOWNERS routing, review-rule linkage, `PB-019` blocked status, `TASK-000008` proposed-only status, required qualification and reconciliation evidence, and unsupported authority boundaries.

Decision:

Keep `PB-019` blocked. The inventory is useful because it makes the blocker reviewable and machine-checkable, not because it satisfies the blocker. `PB-019` can move only after named qualified backups, role-level evidence, subsystem competence, representative path coverage, review records, availability, succession, recusal, inactivity, removal, emergency replacement, access reconciliation, stale-access review, ownerless-path review, primary-only-path review, single-owner residual-risk review, and two-person-control evidence exist.

Impact:

No qualified backup, owner coverage, release authority, signing authority, update trust, supported-version change authority, security-disclosure authority, irreversible migration approval, legal approval, incident closure, broad M1 readiness, beta, stable, production, or implementation claim is supported.

Next question:

Which named backup-owner candidates and qualification records should be collected first without using placeholders or granting release authority from documentation intent?

## 2026-07-18 — Incident patch rehearsal inventory

Question:

Can `PB-018` move from security and release prose into checked no-claim planning evidence without implying that incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, stable promotion authority, signing authority, incident closure authority, or production-safe browsing exists?

Inputs:

- [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md);
- [`incident-patch-rehearsal.json`](security-engine/machine/incident-patch-rehearsal.json);
- [`incident-patch-rehearsal.schema.json`](security-engine/machine/incident-patch-rehearsal.schema.json);
- [`tools/validate_incident_patch_rehearsal.py`](../tools/validate_incident_patch_rehearsal.py);
- [Security policy](security.md);
- [Security Verification and Release Gates](security-engine/06-security-verification-and-release-gates.md);
- [Vulnerability Response and Supported Lifecycle](release-operations/08-vulnerability-response-and-supported-lifecycle.md).

Method:

Added a no-claim security-engine registry and validator covering report access control, acknowledgement, reproduction, severity, asset analysis, affected-version statement, embargo handling, sanitized evidence preservation, protected patch branch, embargoed CI, regression, backport, signing/update dry run, staged rollout, minimum secure version, revocation, release notes, user/admin communication, CVE/credit handling, coordinated disclosure, postmortem remediation, active exploitation, update/signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension/provider, service outage, owner/reviewer/release/security/legal/support/on-call roles, timing targets, escalation path, secret rotation, backup coverage, and unavailable agent, disclosure, signing, stable-promotion, and incident-closure authority.

Decision:

Treat `PB-018` as `partial` because checked planning evidence exists, while requiring executed private-intake tabletop records, emergency patch dry-run records, regression/backport evidence, signing/update dry-run evidence, staged rollout and revocation evidence, coordinated disclosure rehearsal, postmortem evidence, incident-class workflow exercises, role review, timing/escalation/secret-rotation drills, backup-owner coverage, and owner approval before any incident-response, emergency-patch, supported-security, disclosure, signing, stable-promotion, incident-closure, or production-safe browsing claim.

Impact:

No incident-response program, emergency patch capacity, supported security version, disclosure authority, signing authority, stable-promotion authority, incident-closure authority, production-safe browsing, broad M1 readiness, beta, stable, or production claim is supported.

Next question:

Which private tabletop and no-production-key patch dry-run should make the `PB-018` planning inventory executable without publishing exploitable details or granting agents security authority?

## 2026-07-18 — Research package update lab inventory

Question:

Can `PB-017` move from release-operations prose into checked no-claim planning evidence without implying that production signing keys, offline roots, a stable channel, a real updater, public binary distribution, rollback safety, migration safety, release readiness, or supported-security evidence exists?

Inputs:

- [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md);
- [`research-package-update-lab.json`](release-operations/machine/research-package-update-lab.json);
- [`research-package-update-lab.schema.json`](release-operations/machine/research-package-update-lab.schema.json);
- [`tools/validate_research_package_update_lab.py`](../tools/validate_research_package_update_lab.py);
- [Release Operations book](release-operations/README.md);
- [Update, Supply Chain, and Vulnerability Response](security-engine/05-update-supply-chain-and-vulnerability-response.md);
- [Blueprint 13](blueprint-v1/13-build-release-operations.md).

Method:

Added a no-claim release-operations registry and validator covering source commit, build ID, channel, platform, architecture, toolchain, feature set, SBOM, provenance, symbols, notices, artifact hashes, artifact sizes, no-stable-support label, role separation, signature threshold, expiry, minimum secure version, rollout, mirrors, staged install, tamper, replay, wrong-target, partial-write, disk-full, power-loss, rollback, vulnerable-version refusal, migration, downgrade, crash-loop, privacy-preserving local events, and unsupported production boundaries.

Decision:

Treat `PB-017` as `partial` because checked planning evidence exists, while requiring executable package manifests, update metadata parsers, no-production-key signature and threshold fixtures, tamper/replay/wrong-target/expiry/mirror/partial-write/disk-full/power-loss tests, authorized rollback tests, vulnerable-version refusal tests, migration/downgrade/crash-loop tests, privacy review, release-operations review, and owner approval before any updater, signing, release, rollback, migration, or supported-security claim.

Impact:

No package implementation, updater implementation, production signing, offline-root handling, stable channel, public binary distribution, real user profile migration, rollback safety, migration safety, release readiness, supported-security readiness, broad M1 readiness, or production claim is supported.

Next question:

Which no-production-key manifest generator and metadata parser should make the `PB-017` planning inventory executable without creating a real updater or public distribution path?

## 2026-07-18 — Profile/session format inventory

Question:

Can `PB-016` move from prose-only schema expectations into checked no-claim planning evidence without implying that profile formats, migration, sync, credential storage, data-loss safety, or production user-data handling exist?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [`profile-session-format-inventory.json`](storage/machine/profile-session-format-inventory.json);
- [`profile-session-format-inventory.schema.json`](storage/machine/profile-session-format-inventory.schema.json);
- [`tools/validate_profile_session_formats.py`](../tools/validate_profile_session_formats.py);
- [Storage and Recovery book](storage/README.md);
- [Product Experience book](product-experience/README.md);
- [Build and Release Operations book](release-operations/README.md).

Method:

Added a no-claim storage/profile registry and validator covering profile, Space, session, snapshot, migration, disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, data-loss, authority boundaries, unsupported boundaries, and safe-failure behavior.

Decision:

Treat `PB-016` as `partial` because checked planning evidence exists, while requiring executable schemas, malformed/downgrade/corrupt/disk-full/power-loss/private-session/crash/data-loss tests, real-profile fixture policy, migration rehearsal, privacy review, data-loss review, release-operations review, and owner approval before any real profile or production format work.

Impact:

No profile implementation, real-profile migration, sync support, credential-storage support, user-data handling readiness, data-loss safety, production profile-format readiness, broad M1 readiness, or production claim is supported.

Next question:

Which executable schema and fault-test harness should convert the `PB-016` planning inventory into testable format evidence without touching real user profiles?

## 2026-07-18 — Native UI component fixture inventory

Question:

Can `PB-014` move from product/UI prose into checked planning evidence without implying that native UI fixtures, toolkit selection, trusted chrome, or accessibility readiness exist?

Inputs:

- [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- [`component-fixture-inventory.json`](ui-runtime/machine/component-fixture-inventory.json);
- [`component-fixture-inventory.schema.json`](ui-runtime/machine/component-fixture-inventory.schema.json);
- [`tools/validate_ui_component_fixtures.py`](../tools/validate_ui_component_fixtures.py);
- [Native UI Runtime book](ui-runtime/README.md);
- [Accessibility book](accessibility/README.md);
- [Product Experience book](product-experience/README.md).

Method:

Added a no-claim UI component fixture registry and validator covering semantic token groups, browser chrome, tabs, Spaces, command field, permission prompts, agent confirmations, resource manager, settings, recovery UI, keyboard, focus, screen-reader, forced-color, high-contrast, reduced-motion, density, localization, error-state, accessibility contracts, and authority boundaries.

Decision:

Treat `PB-014` as `partial` because checked planning evidence exists, while requiring rendered fixture packs, adapter-specific fixture outputs, real platform accessibility evidence, and owner review before any toolkit, trusted-chrome, accessibility, page-surface, or release-path UI approval.

Impact:

No UI implementation, rendered fixture, toolkit selection, accessibility readiness, trusted-chrome readiness, page-surface approval, production readiness, compatibility, security, performance, memory, energy, Chrome-class, beta, stable, or daily-driver claim is supported.

Next question:

Which adapter-specific rendered fixture pack and reference-platform accessibility output should make the `PB-014` inventory executable?

## 2026-07-18 — Benchmark corpus expansion

Question:

Can `PB13-EV-003` move beyond the initial two-case no-claim seed while preserving generated local provenance, checked hashes, route coverage, and no-claim boundaries?

Inputs:

- [Benchmark corpus expansion](research/benchmark-corpus-expansion-2026-07.md);
- [Benchmark corpus schema](blueprint-v1/machine/benchmark-corpus.schema.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [`tools/validate_benchmark_corpus.py`](../tools/validate_benchmark_corpus.py);
- [`tools/validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Expanded the no-claim corpus manifest from two generated local fixtures to seven generated local fixtures covering static-document, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract shapes. Added matching fixture files, SHA-256 digests, byte counts, category validation, and loopback route coverage in the local static network profile.

Observations:

- the corpus validator now requires every no-claim smoke category and checks every fixture hash and byte count;
- the network-profile validator now checks route coverage for every expanded corpus case;
- the service-worker contract fixture does not register a worker, open Cache Storage, or intercept fetch;
- the expanded corpus remains generated smoke evidence only, not a reviewed representative corpus.

Decision:

Treat `PB13-EV-003` as partially evidenced by the expanded no-claim corpus seed, while keeping the reviewed representative offline corpus, browser-run fixture evidence, and raw artifact package as missing proof.

Impact:

`PB-013` stays `documented_no_runner`. The expansion does not support browser rendering, compatibility, accessibility, service-worker, media, security, speed, memory, energy, Chrome-class, daily-driver, beta, stable, production, or performance claims.

Next question:

What corpus-selection policy, disabled-case denominator, and browser-run artifact shape should turn the expanded no-claim seed into a reviewed benchmark corpus?

## 2026-07-18 — Benchmark server lifecycle self-test

Question:

Does `PB13-EV-004` have checked runner-managed server startup, route-check, shutdown, and artifact-hash evidence before browser benchmark execution exists?

Inputs:

- [Benchmark server lifecycle self-test](research/benchmark-server-lifecycle-self-test-2026-07.md);
- [`no-claim-local-static.profile.json`](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [`serve_benchmark_profile.py`](../tools/serve_benchmark_profile.py);
- [`run_benchmark_server_profile.py`](../tools/run_benchmark_server_profile.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a no-claim server lifecycle runner that loads the checked network profile, starts the local HTTP/1.1 loopback server on an ephemeral port, checks configured corpus routes with the `turing.invalid` Host header, shuts the server down, verifies the port no longer accepts the test connection, writes startup, route-check, shutdown, runner-summary, and artifact-index JSON files, and hashes every artifact.

Decision:

The benchmark network lane needs server lifecycle evidence before browser-run measurement so startup, route coverage, shutdown, cleanup, artifact hashing, DNS-boundary language, and no-claim finalization cannot be invented by later browser-run work.

Impact:

`PB13-EV-004` now has checked runner-managed server lifecycle self-test evidence. This does not produce browser-run server evidence, modify OS DNS resolver state, exercise TLS, HTTP/2, HTTP/3, proxy, authentication, cache-revalidation, or network shaping, launch a browser, capture traces, produce raw samples, prove latency or cache behavior, promote `PB-013`, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, compatibility, or performance claim.

## 2026-07-18 — Benchmark browser launch-runner contract

Question:

Does `PB13-EV-005` have a checked no-claim browser launch-runner contract and no-browser self-test before a browser-run benchmark implementation exists?

Inputs:

- [Benchmark browser launch-runner contract](research/benchmark-browser-launch-runner-contract-2026-07.md);
- [`benchmark-launch-runner.schema.json`](blueprint-v1/machine/benchmark-launch-runner.schema.json);
- [`no-claim-browser-launch.plan.json`](blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json);
- [`validate_benchmark_launch_runners.py`](../tools/validate_benchmark_launch_runners.py);
- [`run_benchmark_browser_launch.py`](../tools/run_benchmark_browser_launch.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a sample-only launch-runner schema, a no-claim browser launch-runner plan, a validator that checks required and forbidden command arguments, current no-claim registry references, launch-stage coverage, timeout/cancellation policy, cache/profile policy, failure finalization, trace/artifact linkage, resource-attribution linkage, unsupported behavior, missing proof, and no-claim wording, plus a checked no-browser browser launch-runner self-test that validates command parsing, forbidden argument rejection, registry references, artifact-root handling, hashed artifacts, and no-claim finalization. Synchronized `PB-013`, the benchmark research lane, `TASK-000005`, the performance packet, indexes, repository map, and related performance books.

Decision:

The browser benchmark launch path needs a checked contract before implementation so timeout, cancellation, cache/profile reset, forbidden arguments, failure denominator, trace/artifact package, cleanup, and no-claim result finalization cannot be skipped by the first runner.

Impact:

`PB13-EV-005` now has no-claim browser launch-runner contract evidence and checked no-browser browser launch-runner self-test evidence beyond the smoke runner and browser-pin records. This does not implement a browser-run launch runner, launch a browser, capture traces, produce raw samples, prove memory or energy behavior, promote `PB-013`, approve benchmark-ready browser pins, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, or compatibility claim.

## 2026-07-18 — Benchmark trace/artifact package contract

Question:

Does `PB13-EV-007` have a checked no-claim trace/artifact package contract before a browser benchmark runner exists?

Inputs:

- [Benchmark trace/artifact package contract](research/benchmark-trace-artifact-package-contract-2026-07.md);
- [`benchmark-artifact-package.schema.json`](blueprint-v1/machine/benchmark-artifact-package.schema.json);
- [`no-claim-trace-package.plan.json`](blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json);
- [`validate_benchmark_artifact_packages.py`](../tools/validate_benchmark_artifact_packages.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a sample-only artifact-package schema, a no-claim trace/artifact package plan, and a validator that checks runner-owned root policy, ETW or equivalent trace class, Perfetto-compatible trace class, tab lifecycle log class, required artifact classes, SHA-256 manifest records, redaction/retention requirements, prohibited-content rules, no-claim wording, and current no-claim registry references. Synchronized `PB-013`, the benchmark research lane, `TASK-000005`, the performance packet, indexes, repository map, and related performance books.

Decision:

Trace and artifact package evidence needs a checked contract before a runner can persist raw benchmark artifacts, and real traces, logs, screenshots, memory snapshots, power samples, failure records, redaction review, retention decisions, and SHA-256 manifests must stay required proof.

Impact:

`PB13-EV-007` now has no-claim package-contract evidence instead of unstructured missing proof. This does not launch a browser, capture ETW or Perfetto traces, produce raw samples, prove memory or energy behavior, promote `PB-013`, approve a benchmark-ready runner, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, or compatibility claim.

## 2026-07-18 — Benchmark 30-tab scenario contract

Question:

Does `PB13-EV-008` have checked mixed-state and all-live 30-tab scenario records before a browser benchmark runner exists?

Inputs:

- [Benchmark 30-tab scenario contract](research/benchmark-30-tab-scenario-contract-2026-07.md);
- [`benchmark-tab-scenario.schema.json`](blueprint-v1/machine/benchmark-tab-scenario.schema.json);
- [`no-claim-30-tab-smoke.scenarios.json`](blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json);
- [`validate_benchmark_tab_scenarios.py`](../tools/validate_benchmark_tab_scenarios.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a sample-only tab-scenario schema, a no-claim 30-tab mixed-state and all-live scenario manifest, and a validator that checks exact 30-tab totals, lifecycle state-count parity, corpus case references, network-profile route coverage, all-live versus mixed-state semantics, and no-claim wording. Synchronized `PB-013`, the benchmark research lane, `TASK-000005`, the performance packet, indexes, repository map, and related performance books.

Decision:

The 30-tab workload needs a checked denominator record before a runner can emit raw artifacts, and mixed-state results must stay separate from all-live results.

Impact:

`PB13-EV-008` now has no-claim scenario-manifest evidence instead of prose-only planning. This does not launch a browser, produce raw artifacts, prove memory or energy behavior, promote `PB-013`, approve a benchmark-ready runner, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, or compatibility claim.

## 2026-07-18 — Direct command and line-ending handoff tightening

Question:

Do the root README and operating board distinguish wrapper-managed handoff validation from direct Cargo invocation while matching the expanded LF policy?

Inputs:

- [README](../README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Repository map](repository-map.md);
- [`.gitattributes`](../.gitattributes);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Clarified in the root README and documentation-readiness matrix that direct Cargo commands are behavior-equivalent to the wrappers but inherit the caller's `CARGO_TARGET_DIR`, so source-tree cleanliness evidence should prefer wrappers or an explicitly external target directory. Updated the operating-board newline evidence row to cover Markdown, GitHub YAML, Rust, JSON, scripts, and repository tooling files instead of only Rust and tooling sources.

Decision:

Handoff docs must not imply direct Cargo invocation provides the same target-directory hygiene as the wrappers unless the caller has set the environment deliberately.

Impact:

Maintainers get clearer local validation guidance and the operating board now matches the repository LF policy. This is documentation and validation alignment only; it does not prove fresh-host reproduction, promote `PB-009`, or change any product-readiness or browser-capability claim.

## 2026-07-18 — Machine wrapper parity

Question:

Do machine readiness records list the PowerShell validation wrappers alongside the POSIX wrappers?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `tools/bootstrap.ps1`, `tools/doctor.ps1`, and `tools/check.ps1` beside the existing POSIX wrapper paths in the pre-build readiness evidence, fresh-host research lane evidence, and `TASK-000002` allowed paths. Updated the operating-board build-validation evidence row to include `tools/check.ps1`.

Decision:

Machine records must expose the same Windows validation entry points as the human-facing handoff docs so task shaping and readiness evidence stay synchronized.

Impact:

Fresh-host, task-queue, and readiness evidence now route Windows maintainers to the implemented wrapper paths. This is machine-record parity only; it does not promote `PB-009`, approve `TASK-000002`, prove independent fresh-host reproduction, or change any browser capability claim.

## 2026-07-18 — First-entry validation handoff surfaces

Question:

Do the Start Here page, documentation index, and build-readiness operating board give maintainers concrete validation entry points before handoff?

Inputs:

- [Start Here](start-here.md);
- [Documentation index](README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added aggregate validation wrapper guidance to the first-entry handoff surfaces: `sh tools/check.sh` for POSIX shells and `.\tools\check.ps1` for Windows PowerShell. Linked the full direct command family back to the documentation-readiness matrix and kept the proof boundary limited to contained M0 repository validation.

Decision:

Stop/resume documents should not only point to gate truth; they should tell the next maintainer exactly how to prove the repository still validates before work continues.

Impact:

Maintainers can find the current validation entry points from the first docs they read. This is handoff guidance only; it does not approve tasks, promote readiness, prove semantic documentation completeness, or change any browser capability claim.

## 2026-07-18 — Agent and PR Windows wrapper handoff alignment

Question:

Do the root agent instructions, PR template, prototype guide, repository map, and documentation-readiness matrix point Windows maintainers to the new PowerShell aggregate-check wrapper?

Inputs:

- [AGENTS.md](../AGENTS.md);
- [Pull request template](../.github/pull_request_template.md);
- [Prototype guide](prototype.md);
- [Repository map](repository-map.md);
- [Documentation readiness matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Replaced stale Windows guidance that asked maintainers to set `CARGO_TARGET_DIR` manually with references to `.\tools\check.ps1`, which delegates to the aggregate `xtask check` path and sets `CARGO_TARGET_DIR` outside the repository when unset. Added the same wrapper note to the prototype guide and documentation-readiness validation section.

Decision:

Agent and pull-request handoff surfaces should name the Windows wrapper directly so a maintainer can resume and validate from PowerShell without reconstructing environment setup from lower-level Cargo commands.

Impact:

Windows handoff guidance now matches the implemented wrapper contract. This is validation ergonomics only; it does not change M0 gate status, product platform support, release support, or browser capability claims.

## 2026-07-18 — Staged diff command-list alignment

Question:

Do the direct local-check command lists include the staged diff hygiene gate now enforced by `xtask check`?

Inputs:

- [AGENTS.md](../AGENTS.md);
- [Contributing](contributing.md);
- [Pull request template](../.github/pull_request_template.md);
- [Documentation readiness matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `git diff --cached --check` beside `git diff --check` in the direct command lists used by agents, contributors, pull requests, and documentation-readiness handoffs. Updated validation markers so those direct handoff surfaces keep the staged-diff check visible.

Decision:

Direct command lists should show both unstaged and staged diff hygiene checks because staged changes can differ from the working tree before handoff.

Impact:

Maintainers who run the listed commands one by one now get the same staged-diff hygiene signal as the aggregate local check. This is handoff hygiene only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim.

## 2026-07-18 — Windows PowerShell validation wrappers

Question:

Can a Windows maintainer run the M0 bootstrap, doctor, and complete local check through first-class PowerShell wrappers instead of relying on POSIX `sh` wrappers?

Inputs:

- [`tools/bootstrap.ps1`](../tools/bootstrap.ps1);
- [`tools/doctor.ps1`](../tools/doctor.ps1);
- [`tools/check.ps1`](../tools/check.ps1);
- [Root README](../README.md);
- [Contributing](contributing.md);
- [Repository map](repository-map.md);
- [M0 build foundation report](research/m0-build-foundation-2026-07.md);
- [`tools/validate_build_foundation.py`](../tools/validate_build_foundation.py);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added PowerShell wrappers that set `CARGO_TARGET_DIR` under the system temporary directory when unset and then delegate to the same locked `xtask` bootstrap, doctor, and check commands as the POSIX wrappers. Updated root, contributor, readiness, repository-map, and M0 build-foundation documentation so Windows and POSIX entry points are visible together.

Decision:

Windows validation entry points are part of the M0 build foundation because the current development and evidence collection happen on Windows as well as the Ubuntu CI reference. The wrappers must stay thin and must not fork validation behavior away from `xtask`.

Impact:

Windows maintainers can run `.\tools\bootstrap.ps1`, `.\tools\doctor.ps1`, and `.\tools\check.ps1` directly from PowerShell. This improves local handoff ergonomics only; it does not change product platform support, cross-platform preview status, readiness gates, or browser capability claims.

## 2026-07-18 — Markdown and workflow line-ending policy

Question:

Does the repository line-ending policy cover Markdown and GitHub workflow templates, the files most likely to carry documentation handoffs and CI control changes?

Inputs:

- [`.gitattributes`](../.gitattributes);
- [Repository map](repository-map.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `*.md`, `*.yml`, and `*.yaml` LF rules to `.gitattributes`, alongside the existing Rust, TOML, JSON, HTML, Python, and shell rules. Updated the repository map to state that Markdown and GitHub YAML are covered, not only Rust and tooling files.

Decision:

Documentation and workflow files are part of the build-readiness control plane, so they need the same stable line-ending policy as source and validation files.

Impact:

Future changed or checked-out Markdown and GitHub YAML should preserve LF before local or CI diff hygiene checks run. Existing historical blobs were not renormalized in this change; changed-range hygiene remains enforced by local and CI diff checks. This is source-control hygiene only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim.

## 2026-07-18 — Local aggregate diff hygiene coverage

Question:

Does the complete local `xtask check` path enforce the same diff whitespace hygiene required by contributor and agent handoff guidance?

Inputs:

- [`xtask`](../tools/xtask/src/main.rs);
- [Root README](../README.md);
- [Contributing](contributing.md);
- [M0 build foundation report](research/m0-build-foundation-2026-07.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `git diff --check` and `git diff --cached --check` to `xtask check` after repository validation and before Rust formatting. Updated the root README, contributor guide, and M0 build-foundation report to state that the aggregate local check covers both unstaged and staged diff whitespace.

Decision:

The aggregate local check should fail on whitespace and line-ending drift even when a maintainer relies on `tools/check.sh` instead of running the listed commands one by one.

Impact:

Local full-check runs now catch unstaged and staged diff hygiene failures before handoff. This is source-hygiene coverage only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim.

## 2026-07-18 — CI committed-diff whitespace enforcement

Question:

Does the GitHub workflow enforce the same `git diff --check` whitespace gate that local contributor, agent, and pull-request handoff guidance requires?

Inputs:

- [Repository validation workflow](../.github/workflows/repository-validation.yml);
- [Root README](../README.md);
- [Contributing](contributing.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a committed-range whitespace check to the repository validation workflow. Pull requests check `base` to `head`; pushes check `before` to `github.sha`; root commits or zero `before` values use `git diff-tree --check --root -r`. The workflow uploads `diff-whitespace.log` with the other validation diagnostics. Updated contributor guidance and the root CI summary to match.

Decision:

CI must enforce committed-diff whitespace because local `git diff --check` only covers the working tree before handoff. This keeps line-ending and trailing-whitespace drift from reappearing after Windows edits, generated docs, or template updates.

Impact:

Pull requests and pushes now fail on committed whitespace errors. This is hygiene enforcement only; it does not prove documentation semantic completeness, promote build readiness, approve tasks, or change any browser capability claim.

## 2026-07-18 — Aggregate xtask ADR evidence coverage

Question:

Does the aggregate `xtask check` path run the same ADR-0009 evidence validator required by the current contributor, agent, and pull-request gates?

Inputs:

- [`xtask`](../tools/xtask/src/main.rs);
- [Repository validation workflow](../.github/workflows/repository-validation.yml);
- [Root README](../README.md);
- [Prototype guide](prototype.md);
- [M0 build foundation report](research/m0-build-foundation-2026-07.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated `xtask check` to run `python3 -B tools/validate_adr_0009_evidence.py` after the Blueprint validator and before build-foundation validation. Updated the repository validation workflow with an ADR-0009 evidence step and uploaded diagnostic log. Updated `xtask` bootstrap/help text to print locked Cargo commands. Updated the root README, prototype guide, and M0 build-foundation report so the aggregate check, CI check, and prototype-only checks describe the current gate shape.

Decision:

The aggregate repository check and CI workflow must include ADR-0009 evidence validation because Servo/source-strategy tracking is an active pre-build blocker. This aligns `tools/check.sh`, `xtask check`, contributor guidance, agent guidance, CI validation, and GitHub handoff guidance.

Impact:

Local full-check runs now fail if ADR-0009 evidence records drift from the matrix or evidence files. This is gate alignment only; it does not resolve ADR-0009, unblock `PB-002`, approve Servo adoption, or promote any M0 foundation work beyond contained research/build readiness.

## 2026-07-18 — GitHub handoff template validation refresh

Question:

Do the GitHub PR and engineering issue templates expose the current validation family, core registry review, and proposed task identifiers?

Inputs:

- [Pull request template](../.github/pull_request_template.md);
- [Engineering issue template](../.github/ISSUE_TEMPLATE/engineering.yml);
- [Core program registries](repository-map.md#core-program-registries);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated the pull request template with proposed task/readiness fields, a core program-registry review line, the current validation command family, and the `CARGO_TARGET_DIR` source-tree-cleanliness note. Updated the engineering issue template placeholder to include `TASK-*` identifiers for proposed build-readiness handoffs.

Decision:

GitHub intake surfaces must use the same vocabulary and validation family as `AGENTS.md`, `docs/contributing.md`, the repository map, and the build-readiness task queue. Template fields do not approve tasks, promote readiness, or prove support status.

Impact:

Contributors opening issues or pull requests are now prompted to include `TASK-*` context, review core registries before changing authority, and run the current checks. No issue, task, readiness, owner, or product claim changed.

## 2026-07-18 — Agent and contributor validation command refresh

Question:

Do the root agent instructions and canonical contributor guide list the current repository checks rather than the older prototype-only subset?

Inputs:

- [AGENTS.md](../AGENTS.md);
- [Contributing](contributing.md);
- [`xtask`](../tools/xtask/src/main.rs);
- [`tools/check.sh`](../tools/check.sh);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated the completion and local-check command blocks to include `python3 -B` validation, `validate_adr_0009_evidence.py`, `git diff --check`, full workspace formatting, prototype checks, and `cargo run --locked -p xtask -- check`. Added the source-tree cleanliness note for `CARGO_TARGET_DIR` outside the repository.

Decision:

Agent and contributor handoff documents must route to the same current validation gate family as the repository validator and aggregate `xtask` check. The command list is validation guidance only; it does not promote readiness, approve a proposed task, or substitute for owner review.

Impact:

Maintainers and agents running from the root instructions or contributing guide now execute the same documented validation family used by the current documentation-readiness work. No code behavior, readiness status, or product claim changed.

## 2026-07-18 — Root and Start Here registry continuity

Question:

Do the two broadest first-entry documents point maintainers to the core program registries before they change scope, authority, readiness, or task status?

Inputs:

- [root README](../README.md);
- [Start Here](start-here.md);
- [Repository map](repository-map.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added core program-registry navigation to the root stop/resume path and Start Here stop/resume map. Both now route maintainers to the repository-map registry table before changes to requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas.

Decision:

The first-entry path must lead to the same machine sources of truth as the docs index, Blueprint index, and repository map. This routing is a governance control only; it does not approve tasks, promote readiness, or prove implementation status.

Impact:

A person resuming from the root README or Start Here can find the core machine registries without reading prior chat history. No requirement, risk, work package, readiness item, owner assignment, task approval, agent authority, or product claim changed.

## 2026-07-18 — Blueprint and docs registry entry points

Question:

Do the main documentation index and Blueprint index route maintainers to the same core program-registry map as the repository map?

Inputs:

- [Documentation index](README.md);
- [Blueprint index](blueprint-v1/README.md);
- [Documentation policy](documentation-policy.md);
- [Repository map](repository-map.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added explicit core machine-registry navigation to the docs index and Blueprint index. The Blueprint index now names the core machine companions for requirements, risks, backlog, readiness, task queue, process capabilities, workspace/toolchains, professional controls, and agent action schema, and links back to the repository map table for boundaries.

Decision:

The docs index, Blueprint index, repository map, and documentation policy must all expose that machine registries are sources of truth for scope and authority, not implementation proof or readiness promotion.

Impact:

A maintainer starting from either index can find the same registry map before changing implementation scope, authority, readiness, or task status. No machine registry status, task approval, readiness promotion, or product claim changed.

## 2026-07-18 — Core machine-registry navigation

Question:

Can a maintainer resuming from the repository map find the core machine-readable sources of truth without confusing them with feature readiness or task approval?

Inputs:

- [Repository map](repository-map.md);
- [`requirements.json`](blueprint-v1/machine/requirements.json);
- [`risks.json`](blueprint-v1/machine/risks.json);
- [`backlog.json`](blueprint-v1/machine/backlog.json);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- [`professional-owners.json`](blueprint-v1/machine/professional-owners.json);
- [`workspace-components.json`](blueprint-v1/machine/workspace-components.json);
- [`agent-action.schema.json`](blueprint-v1/machine/agent-action.schema.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a core program-registry table to the repository map, separate from benchmark/source evidence registries. The table routes requirements, risks, work packages, pre-build readiness, the proposed task queue, process capabilities, workspace/toolchains, professional controls, and the agent action schema to their owning prose and explicit no-claim boundaries.

Decision:

The repository map must expose the machine registries that control scope, readiness, ownership, and authority. These records remain sources of truth for review and handoff, not evidence that features are implemented, tasks are approved, mitigations are complete, or production support exists.

Impact:

People and agents can now resume from the repository map and find the core program-control registries without relying on chat history. No requirement, risk, work package, readiness item, owner assignment, agent authority, task approval, or product claim changed.

## 2026-07-18 — Contained-M0 allowed-now boundary

Question:

Does the machine readiness registry describe allowed work narrowly enough for a maintainer or agent to avoid treating contained M0 work as broad implementation approval?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Narrowed the top-level `allowed_now` registry field from broad shorthand into explicit contained/no-claim M0 categories: documentation, research, root-workspace source tasks, typed kernel/identity/IPC/UI-model foundations, isolated native UI comparison prototypes, expected-deny sandbox probes, benchmark corpus and no-claim measurement tooling, profile/session schema prototypes, research-package/updater lab prototypes without production keys or a real updater, private-intake tabletop documentation, and task-scoped diagnostic tooling.

Decision:

`allowed_now` is an authorization boundary, not a feature roadmap. It must stay aligned with `PB-GATE-0`, the pre-build audit, and the operating board, and it must not imply production update, incident-response, benchmark, UI-toolkit, sandbox, profile, ownership, Chrome-class, or broad M1 approval.

Impact:

The machine source of truth now matches the human handoff language more closely. No readiness item was promoted, no proposed `TASK-*` item was approved, and no implementation, release, benchmark, updater, incident-response, or production claim changed.

## 2026-07-18 — Entry-point lane-set invariant

Question:

Do the first-entry documents name the same current implementation-research lane set as the research index and machine crosswalk?

Inputs:

- [Start Here](start-here.md);
- [root README](../README.md);
- [documentation index](README.md);
- [documentation policy](documentation-policy.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated the stop/resume language in the entry points so the source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, and ownership lanes are all visible before implementation work. Added validation so `start-here.md`, the root README, the docs index, and the research lane table cannot silently omit the package/update or incident-response lanes.

Decision:

The entry points must name the full lane set or link to an index that does. The lane list remains a navigation and handoff control only; it does not approve any proposed task, readiness promotion, package/update work, incident-response authority, ownership coverage, or implementation expansion.

Impact:

A maintainer resuming from the root README, `docs/README.md`, or `docs/start-here.md` now sees the same lane set that the research crosswalk and task queue enforce. No readiness status or support claim changed.

## 2026-07-18 — Ownership readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same evidence required before `PB-019` can move out of blocked status?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`professional-owners.json`](blueprint-v1/machine/professional-owners.json);
- [`professional-review-rules.json`](blueprint-v1/machine/professional-review-rules.json);
- [ownership and maintainer ladder](project-buildout/02-ownership-codeowners-and-maintainer-ladder.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded `PB-019` from a one-line "named qualified backups" blocker into explicit backup-owner evidence for build-critical program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data scopes. Added qualification, path coverage, review record, availability, succession, recusal, inactivity, removal, emergency replacement, CODEOWNERS, review-rule, escalation-policy, support, signing, disclosure, package, CI, service, repository-access, stale-access, ownerless-path, primary-only-path, blocked-status, single-owner-risk, and two-person-control evidence requirements.

Decision:

Keep `PB-019` blocked while any professional owner backup is null, a placeholder, undocumented, primary-only, or not independently reviewable. Documentation may organize the blocker, but it does not name qualified backups or create release, signing, update-trust, supported-version, security-disclosure, irreversible-migration, legal-approval, incident-closure, production-authority, or owner-coverage claims.

Impact:

The ownership and review-capacity continuation lane is now concrete enough for handoff. No owner assignment, backup qualification, access grant, release authority, disclosure authority, signing authority, M1 readiness, preview readiness, or production claim changed.

## 2026-07-18 — Operational readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same package/update and incident-response evidence required across `PB-017`, `PB-018`, `TASK-000009`, and `TASK-000010`?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [release operations book](release-operations/README.md);
- [security policy](security.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded `PB-017` from a signed-package placeholder into signed research-package identity, update-metadata, tamper/replay/wrong-target/expiry/mirror/partial-write/disk-full/power-loss, rollback, vulnerable-version refusal, migration, downgrade, crash-loop, privacy-preserving event, and no-production-key evidence. Expanded `PB-018` from a tabletop placeholder into private intake, access control, severity and asset analysis, embargo, protected patch branch, embargoed CI, regression, backport, signing/update dry run, rollout, revocation, communication, coordinated disclosure, postmortem, incident-class, role, timing, escalation, secret-rotation, and no-agent-authority evidence. Added `TASK-000009` and `TASK-000010` as proposed-only task-shaped handoffs and validation so the registry, board, checklist, audit, task queue, research index, and crosswalk cannot silently narrow these gates.

Decision:

Keep `PB-017` and `PB-018` no higher than partial planning evidence until executable research-package/updater lab and incident/patch rehearsal evidence exists. Proposed tasks do not approve a production updater, stable channel, public distribution, signing readiness, supported security versions, incident-response readiness, emergency patch capacity, disclosure authority, stable promotion, or signing authority.

Impact:

The operational-readiness continuation path is now explicit before broad implementation. No release, updater, stable support, security-support, production-safety, or incident-authority claim changed.

## 2026-07-18 — Native shell readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same native-shell evidence required across `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006`?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded the native-shell lane from short placeholders into explicit readiness evidence: toolkit-neutral state/command/surface/accessibility/diagnostic/adapter contracts, equivalent reference-shell adapters, page-surface composition, design-token and component fixtures, IME, keyboard, accessibility, crash, GPU-loss, startup, memory, binary, latency, frame-pacing, energy, license, dependency, provenance, reference-platform workflow, and assistive-technology coverage. Added validation so the machine readiness registry, proposed task queue, operating board, checklist, audit, research index, and research crosswalk cannot silently narrow the lane.

Decision:

Keep `PB-003` partial, keep `PB-004`, `PB-005`, and `PB-015` not started, and do not move `PB-014` beyond partial planning evidence until equivalent rendered adapter and page-surface evidence exists. This does not select a UI toolkit, approve trusted-chrome readiness, approve accessibility readiness, or convert the command-line shell model into a native UI.

Impact:

The native-shell continuation path is more coherent for product, UI runtime, platform, accessibility, performance, security, build, and release review. No UI toolkit selection, page-surface approval, accessibility readiness, trusted-chrome readiness, release-path UI approval, M1 readiness, or production claim changed.

## 2026-07-18 — PB-016 profile/session readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same profile, Space, session, snapshot, and migration evidence required before `PB-016` can advance?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded `PB-016` from generic profile/session format language to an explicit schema and failure-boundary invariant: versioned profile, Space, session, snapshot, and migration schemas; disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, and data-loss behavior; and unsupported sync, credential storage, real-profile migration, user-data handling, and production profile-format boundaries. Added validation so the machine readiness registry, proposed task queue, operating board, checklist, audit, research index, and research crosswalk cannot silently narrow those requirements.

Decision:

Keep `PB-016` no higher than partial planning evidence until executable schema evidence and the full failure/privacy boundary are reviewed. This shapes the next storage/product handoff; it does not approve real-profile fixtures, sync, credential storage, data-loss safety, or a production profile format.

Impact:

The profile/session continuation path is more coherent for storage, product, migration, and privacy work. No profile implementation, migration support, sync support, credential-storage support, data-loss safety claim, user-data handling readiness, broad M1 readiness, or production claim changed.

## 2026-07-18 — PB-012 sandbox-probe readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same sandbox-probe evidence required before `PB-012` can advance?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Promoted the `PB-012` sandbox-probe handoff from generic packaged sandbox evidence to explicit expected-deny coverage for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater roles across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC access. Added validation so the machine readiness registry, proposed task queue, operating board, checklist, audit, research index, and research crosswalk cannot silently drop the role list or denial surfaces.

Decision:

At that time, `PB-012` stayed `not_started` until checked planning evidence or platform-enforced expected-deny probe evidence existed. The later Sandbox Probe Inventory entry above supersedes only the status portion by moving `PB-012` to partial; this invariant still does not accept a sandbox policy, grant release readiness, or approve execution of `TASK-000004`.

Impact:

The sandbox continuation path is now coherent and reviewable before any renderer, network, storage, GPU, decoder, extension, DevTools, agent, or updater role is trusted. No sandbox implementation, site-isolation readiness, hostile-browsing safety, security claim, M1 readiness, or production claim changed.

## 2026-07-18 — PB-011 readiness invariant propagation

Question:

Do the canonical pre-build readiness records carry the same IPC negative-test invariant as the `TASK-000003` handoff queue?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded the `PB-011` missing-evidence wording from generic negative sender tests to the explicit malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation set. Propagated the same wording into the checklist and readiness audit, then extended validation so the machine readiness registry and human pre-build records cannot drift below that coverage.

Decision:

Keep `PB-011` in `partial` status until schema generation, wire encoding, and the full IPC negative-test set are reviewed. This does not approve execution of `TASK-000003`.

Impact:

The canonical readiness view now matches the task queue and research crosswalk for IPC work. No wire format, process topology, IPC implementation, sandbox readiness, M1 readiness, or production/security claim changed.

## 2026-07-18 — IPC negative-test handoff invariant refresh

Question:

Do the build-readiness board, proposed task queue, machine task registry, and validation agree on the IPC negative-test set required before `PB-011` can advance?

Inputs:

- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Aligned the IPC handoff language so malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases are all required in the human operating board and proposed task queue. Updated the machine task registry for `TASK-000003` and added validation that keeps the human and machine records from dropping timeout, cancellation, or wrong-principal coverage.

Decision:

Treat timeout and cancellation behavior as part of the IPC negative-test invariant, not as optional follow-up coverage. `TASK-000003` remains proposed only and still requires owner review before execution.

Impact:

The process-authority continuation path is more coherent for a maintainer resuming `PB-011`. No IPC implementation, source-strategy decision, process-security claim, sandbox readiness, broad M1 readiness, or production claim changed.

## 2026-07-18 — Current documentation count invariant refresh

Question:

Can root-level build status describe the current documentation library without preserving a historical count phrase as a validator dependency?

Inputs:

- root [`README.md`](../README.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Replaced the root README's historical “grew from twenty-five to twenty-seven” phrasing with direct current-state wording that the documentation library contains twenty-seven detailed engineering and product books. Updated the validator to enforce the current count phrase and refreshed the pre-build checklist audit date for the latest documentation-readiness edits.

Decision:

Keep root build status tied to current documentation topology rather than historical growth wording. The validator should guard the current twenty-seven-book statement, not the older transition phrase.

Impact:

The entry-point status is easier to scan and less brittle for future maintainers. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Documentation handoff definition of done

Question:

Can documentation-readiness and handoff changes be completed against explicit criteria rather than broad documentation hygiene?

Inputs:

- [Definition of Done](blueprint-v1/20-definition-of-done.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a `Documentation readiness or handoff change` work type to the Definition of Done. The criteria require synchronized first-entry documents, objective-to-evidence mapping, human/machine record agreement, stop/resume gate truth, `RQ-*`/`PB-*`/`TASK-*` research mapping, claim-boundary preservation, indexing, research-log updates, validator coverage, and validation output scoped to what the checks prove.

Decision:

Use Blueprint 20 as the canonical completion contract for documentation-readiness and handoff changes. The documentation-readiness matrix now links to that DoD and records that the DoD is part of the evidence surface.

Impact:

Future documentation-control changes have a concrete finish line and cannot rely only on passing link checks. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Documentation readiness evidence matrix

Question:

Can the claim that documentation is organized enough for contained build work be reviewed against concrete evidence instead of broad confidence in the documentation set?

Inputs:

- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Research index](research/README.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a documentation-readiness evidence matrix to the project-buildout handbook. The matrix maps the current user-facing objective to concrete evidence: entry points, stop/resume continuity, machine tracking, research crosswalks, source strategy, benchmark/extreme-performance no-claim evidence, agent task controls, topology validation, and M0 build gates.

Decision:

Treat the matrix as the review surface for `PB-001` documentation-readiness evidence. It supports contained M0 continuation only and must stay synchronized with the machine readiness registry, documentation entry points, research controls, task queue, repository map, and validation commands.

Impact:

Maintainers and agents can now inspect one artifact to see what the current documentation organization proves and what remains outside the proof. No broad M1 expansion, source-strategy decision, task approval, benchmark eligibility, or public product/performance/security claim changed.

## 2026-07-18 — Machine-readable research crosswalk registry

Question:

Can the build-readiness research crosswalk be validated against current `RQ-*`, `PB-*`, and `TASK-*` sources rather than relying only on prose review?

Inputs:

- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`research-readiness-crosswalk.schema.json`](blueprint-v1/machine/research-readiness-crosswalk.schema.json);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json);
- [Build readiness task queue registry](blueprint-v1/machine/build-readiness-task-queue.json);
- [Research program](blueprint-v1/22-research-program.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a machine-readable research-readiness crosswalk and schema. The registry mirrors the eight current implementation-research lanes and records each lane's readiness blockers, proposed task handoff, primary research questions, evidence start points, next proof, and claim boundary.

Decision:

Treat the research crosswalk as a machine companion to the research index. It is a consistency and handoff control only; the registry cannot approve a task, promote a `PB-*` item, accept a source strategy, or authorize benchmark or public claims.

Impact:

Future research additions can be checked against the current research program, readiness registry, and task queue. This improves continuation reliability without changing any implementation authorization, readiness status, or product/performance/security claim.

## 2026-07-18 — Research readiness crosswalk enforcement

Question:

Can deep research stay tied to the build-readiness blockers and proposed task handoffs instead of becoming disconnected study inventory?

Inputs:

- [Research index](research/README.md);
- [Research program](blueprint-v1/22-research-program.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a build-readiness research crosswalk to the research index. Each current implementation-research lane now names the relevant `PB-*` blocker, proposed `TASK-*` handoff, primary `RQ-*` research questions, current evidence start point, next proof, and claim boundary. Extended validation so the crosswalk cannot lose the core `RQ-*`, `PB-*`, and `TASK-*` coverage silently.

Decision:

Keep the detailed research index as the current research-control surface. The lane table answers where to continue; the crosswalk answers which readiness gate and research questions the work advances.

Impact:

Maintainers and agents can connect source strategy, fresh-host reproduction, IPC, sandbox, benchmark, native shell, profile/session, and ownership work back to the research program before creating or executing task manifests. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or performance claim changed.

## 2026-07-18 — Documentation index continuation map enforcement

Question:

Can `docs/README.md` act as both a catalog and a current stop/resume guide without requiring a maintainer to jump back to the root README?

Inputs:

- [Documentation index](README.md);
- [Start Here](start-here.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a current stop/resume path to the documentation index, covering status, gate truth, research lane selection, task shaping, `ADR-0009` source-strategy evidence, Chrome-class and extreme-performance benchmark evidence, and claim boundaries. Added validator coverage for the docs-index continuation map.

Decision:

Keep `docs/README.md` as a catalog plus a current handoff guide. It points to authoritative state records rather than replacing the operating board, research index, task queue, machine registries, ADR packet, or benchmark evidence.

Impact:

Maintainers and agents entering through the canonical docs index now get the same contained-M0/no-claim stop/resume path as root README and `start-here.md`. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Root README continuation map enforcement

Question:

Can someone landing on the repository root find the same build-preparation stop/resume path as `docs/start-here.md`?

Inputs:

- root [`README.md`](../README.md);
- [Start Here](start-here.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a root-level current stop/resume path that points to the gate records, research lane map, proposed task queue, `ADR-0009` source-strategy packet, and no-claim benchmark/performance evidence. Updated the root start-here link list and added validator coverage for the root continuation map.

Decision:

Keep the root README as a discovery surface that sends maintainers into the canonical docs before implementation. It must repeat enough status and claim-boundary information to prevent a root-only reader from treating the repository as build-ready.

Impact:

The repository landing page now preserves the contained-M0/no-claim boundary and points to the current continuation path before build commands. No readiness status, source-strategy decision, task authorization, benchmark eligibility, or public claim changed.

## 2026-07-18 — Start-here continuation map enforcement

Question:

Can a new maintainer start from the top-level entry point and find the current build-preparation lanes without reading lower-level indexes first?

Inputs:

- [Start Here](start-here.md);
- [Documentation index](README.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded the current build-readiness section in `start-here.md` into a stop/resume map covering gate truth, research lane selection, task shaping, source-strategy evidence, Chrome-class and extreme-performance evidence, and operating controls. Added validator coverage so the top-level entry point cannot silently lose that map.

Decision:

Keep `start-here.md` as the first human entry point for continuation, while the operating board, research index, task queue, machine registries, ADR records, benchmark records, and project-buildout handbook remain authoritative for state and approvals.

Impact:

New maintainers and agents can now see the same contained-M0/no-claim continuation path from the first document they read. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Repository map documentation-section normalization

Question:

Can the repository map remain a usable structural reference after the source-strategy and benchmark evidence expansion?

Inputs:

- [Repository map](repository-map.md);
- [Research index](research/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Replaced the dense documentation-section paragraphs with grouped continuation records, machine evidence registries, benchmark research reports, and Servo/source-strategy research reports. Preserved the existing links and no-claim/source-strategy boundaries while making the structure easier to scan.

Decision:

Keep the repository map as a structural reference, not a second source of truth. The research index, operating board, machine registries, and validators remain authoritative for current state.

Impact:

Maintainers and agents can now locate documentation families, evidence registries, and validators from the repository map without parsing a long mixed paragraph or inferring approval from the presence of evidence.

## 2026-07-18 — Research lane-map validator coverage

Question:

Can the current implementation-research lane map remain durable after future documentation changes?

Inputs:

- [Research index](research/README.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added repository validation for the research index lane map, including the required implementation-research heading, lane table shape, required lane names, continuation boundaries, and `Must not claim` coverage.

Decision:

Treat the lane map as a required handoff invariant. This does not change any lane status, owner approval, task authorization, benchmark eligibility, or claim boundary.

Impact:

Future changes cannot silently remove the source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership lanes without failing repository validation.

## 2026-07-18 — Research index implementation-lane map

Question:

Can the research index show the current continuation lanes without forcing a maintainer to parse long bundled priority sentences?

Inputs:

- [Research index](research/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build readiness audit](research/pre-build-readiness-gap-audit-2026-07.md).

Method:

Replaced the dense current-priorities list with a lane map covering source strategy, fresh-host build confidence, kernel/process authority/IPC, sandbox probes, benchmark/performance lab, native shell/page-surface composition, profile/session formats, and ownership/review capacity. Each lane now identifies where to start, the next evidence to produce, and what must not be claimed.

Decision:

Keep the research index as a navigation and continuation aid only. The operating board, machine readiness registry, proposed task queue, ADR records, and benchmark registries remain authoritative for state and approvals.

Impact:

The research index now gives maintainers and agents a clearer stop/resume map for build-preparation work while preserving contained-M0 status and no-claim boundaries.

## 2026-07-18 — Project-buildout handoff guide normalization

Question:

Can a maintainer use the project-buildout handbook as a fast continuation guide without parsing a single dense paragraph of source-strategy and benchmark links?

Inputs:

- [Project buildout handbook](project-buildout/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [ADR-0009 evidence registry](blueprint-v1/machine/adr-0009-evidence.json);
- [benchmark readiness evidence registries](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json).

Method:

Replaced the dense handoff paragraph in the project-buildout handbook with a scan-friendly continuation guide: build-readiness control path, source-strategy lane, benchmark/performance lane, validator list, and claim boundary.

Decision:

Keep the handbook as an operating index rather than a second source of truth. The operating board, machine readiness registry, task queue, ADR-0009 evidence registry, and benchmark registries remain authoritative for exact state.

Impact:

People and agents continuing the project can now find the current source-strategy and performance-readiness evidence in ordered groups without implying Servo adoption, broad implementation, benchmark readiness, Chrome-class comparison, or any public performance/security/compatibility claim.

## 2026-07-18 — Research log chronology normalization

Question:

Can the research log be scanned in a single newest-first chronology after the build-readiness and Servo evidence expansion?

Inputs:

- this research log;
- [documentation policy](documentation-policy.md);
- [documentation index](README.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Reordered dated research-log entries into newest-first order, moved the reusable entry template to the end of the file, preserved entry text, evidence statements, unsupported-claim boundaries, and marker comments, and added validator coverage for the chronology invariant.

Decision:

Keep the research log as a chronological handoff surface rather than a mixed chronology plus template interruption. This changes organization only; it does not promote readiness, approve execution, or alter any research conclusion.

Impact:

Maintainers and agents can now scan the material research and governance history without discovering newer July 17 entries after older July 15 and July 16 material, and repository validation will catch future chronology drift.

## 2026-07-18 — Build readiness action ownership split

Question:

Can the build-readiness handoff distinguish agent-workable evidence tasks from owner-only decisions before broad implementation starts?

Inputs:

- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json);
- [Agent Execution](agent-execution/README.md).

Method:

Added an action-ownership split to the operating board for `PB-002`, `PB-009`, `PB-011`, `PB-012`, `PB-013`, `PB-003` through `PB-005`, `PB-014`, `PB-015`, `PB-016`, and `PB-019`. The split identifies which work an agent can continue as no-claim evidence or documentation, and which decisions require an owner.

Decision:

Keep proposed task work separate from owner-only approvals. Agents may gather evidence, draft schemas, improve validators, run approved checks, and update documentation, but may not select source strategy, UI toolkit, benchmark claims, sandbox policy, profile behavior, backup ownership, readiness promotion, or release authority.

Impact:

The operating board now gives a clearer continuation path for agents and maintainers without changing any readiness status or approving execution of the proposed `TASK-*` queue.

## 2026-07-18 — Build readiness task intake snapshot

Question:

Can a maintainer understand the proposed `TASK-*` queue without opening the machine registry for every precondition and rejection condition?

Inputs:

- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Build readiness task queue registry](blueprint-v1/machine/build-readiness-task-queue.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json).

Method:

Added a human intake snapshot for `TASK-000001` through `TASK-000008`. The snapshot summarizes when each task may start, what would prove progress, what would reject the task, and what must not be claimed. The machine registry remains authoritative for exact owners, reviewers, allowed paths, prohibited paths, budgets, dependencies, rollback evidence, and expiration dates.

Decision:

Keep every queued task `proposed` and non-authorizing. The new snapshot improves handoff readability only; it does not approve execution, source-strategy adoption, broad M1 work, benchmark claims, toolkit selection, profile migration, or ownership promotion.

Impact:

The task queue can now be used as a human triage page before converting any item into an immutable owner-reviewed task manifest.

## 2026-07-18 — Pre-build readiness audit refresh

Question:

Can the repository-level pre-build audit still serve as a compact handoff after the newer source-strategy, task-queue, and no-claim benchmark evidence?

Inputs:

- [Pre-build Readiness Gap Audit - July 2026](research/pre-build-readiness-gap-audit-2026-07.md);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md).

Method:

Refreshed the audit from an older broad-controls summary into a current `PB-001` through `PB-020` status table. The audit now records contained M0 authorization, broad-implementation non-authorization, first continuation sequence, no-claim benchmark evidence, and the handoff rule that `pre-build-readiness.json` remains the source of truth.

Decision:

Keep `PB-GATE-0` limited to named contained tasks. Do not promote broad M1 expansion, developer preview, beta, stable, Servo/source-strategy implementation, or Chrome-class/performance/security/compatibility claims from documentation readiness alone.

Impact:

The research index and documentation index now describe the pre-build audit as the current contained-M0 readiness handoff rather than a historical gap list.

## 2026-07-18 — ADR-0009 option scorecard cleanup

Question:

Can the first source-strategy blocker be handed off without `TBD` option-scoring placeholders?

Inputs:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Decision Draft and Public-Claim Impact](project-buildout/16-adr-0009-decision-draft.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json).

Method:

Replaced the option scorecard placeholders with current evidence-bounded assessments for clean implementation informed by Servo, selective Servo components, upstream-first collaboration, Servo-derived engine, and explicit Servo-browser charter change. The scorecard now separates independence fit, schedule impact, security risk, performance evidence, compatibility evidence, maintenance cost, and required documentation changes without selecting an option.

Decision:

Keep `ADR-0009` unaccepted and `PB-002` blocked. The scorecard is handoff evidence only; owner-selected source baseline, owner-reviewed component boundaries, JavaScript-runtime conflict decision, compatibility/performance evidence, security implications, maintenance model, public-claim diffs, and owner approval remain required.

Impact:

The source-strategy packet no longer contains a placeholder decision table. The traceability matrix now references the scorecard as current partial evidence for `ADR9-EV-011`, not as a template.

## 2026-07-18 — Benchmark browser pin local diagnostic capture

Question:

Can the no-claim browser-pin runner capture Chrome and Edge browser-reported versions from isolated temporary profiles without reading or mutating real user profiles?

Inputs:

- [Benchmark Browser Pin Local Diagnostic Capture - July 2026](research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md);
- [Benchmark browser-pin diagnostic schema](blueprint-v1/machine/benchmark-browser-pin-diagnostic.schema.json);
- [Current Windows high-end Chrome/Edge browser-pin diagnostic](blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json);
- [`tools/validate_benchmark_browser_pin_diagnostics.py`](../tools/validate_benchmark_browser_pin_diagnostics.py);
- [`tools/capture_benchmark_browser_pins.py`](../tools/capture_benchmark_browser_pins.py);
- [Benchmark Browser Pin Capture Contract - July 2026](research/benchmark-browser-pin-capture-contract-2026-07.md).

Method:

Ran `tools/capture_benchmark_browser_pins.py --capture-local --target chrome --target edge` with runner-owned temporary profiles, no sync, disabled background networking and component updates, loopback host resolution, `about:blank`, and DevTools version capture. The checked summary records hashes, cleanup status, unsupported behavior, and remaining evidence gaps while leaving raw current-host diagnostic artifacts outside source control.

Observations:

- Chrome reported `Chrome/150.0.7871.115` from `C:\Program Files\Google\Chrome\Application\chrome.exe`;
- Edge reported `Edg/151.0.4129.21` from `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`;
- both temporary profiles were deleted and prohibited configured-path checks reported no prohibited access;
- the runner exposed and fixed an Edge cleanup failure mode by recording unreadable profile files and stopping lingering browser processes tied to the runner-owned temp profile path;
- Edge channel/update-ring proof, effective settings, process-tree command-line audit, Firefox/Safari evidence, and benchmark artifacts remain missing.

Decision:

Treat `PB13-EV-005` and `PB13-EV-009` as partially strengthened by checked current-host Chrome/Edge diagnostic capture. Keep `PB-013` at `documented_no_runner` because the evidence is unreviewed, no-claim, current-host diagnostic output and not benchmark-ready pin or comparison evidence.

Impact:

Updated the performance readiness packet, Chrome-class runbook, browser-pin capture contract, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, documentation indexes, and repository validator to include browser-pin diagnostic evidence and preserve unsupported-claim boundaries.

Next question:

What owner-reviewed channel proof, effective settings, process-tree audit, and artifact-disposition record is required before the Chrome/Edge diagnostic capture can inform benchmark-ready local pins?

## 2026-07-18 — Benchmark browser pin capture contract and self-test runner

Question:

How should the future benchmark runner capture browser-reported versions, settings, and local pin evidence without reading or mutating the owner's real browser profiles, and how can the artifact path be self-tested before launching a real browser?

Inputs:

- [Benchmark Browser Pin Capture Contract - July 2026](research/benchmark-browser-pin-capture-contract-2026-07.md);
- [Benchmark browser-pin capture schema](blueprint-v1/machine/benchmark-browser-pin-capture.schema.json);
- [Current Windows high-end browser-pin capture plan](blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json);
- [`tools/validate_benchmark_browser_pin_capture.py`](../tools/validate_benchmark_browser_pin_capture.py);
- [`tools/capture_benchmark_browser_pins.py`](../tools/capture_benchmark_browser_pins.py);
- [Benchmark Competitor Local Install Inventory - July 2026](research/benchmark-competitor-local-install-inventory-2026-07.md).

Method:

Defined a no-claim capture plan that requires runner-owned temporary profiles, rejects real user profile paths, runs offline by default, prohibits account/sync attachment, separates capture-only arguments from benchmark workload arguments, and requires browser-reported version, effective command line, settings, update state, profile path, cleanup, and artifact hashes once real-browser capture runs. Added a dependency-free self-test runner that creates a runner-owned temporary profile marker, hashes the artifact package, deletes the profile by default, and launches no browser.

Observations:

- Chrome and Edge can become planned current-host capture targets because executable/hash evidence exists;
- `tools/capture_benchmark_browser_pins.py --self-test` validates temp-profile cleanup, prohibited configured-path checks, artifact hashes, and no-claim metadata without launching a browser;
- Firefox remains blocked until installed on an approved host;
- Safari Stable and Safari Technology Preview remain blocked until approved macOS host evidence and profile-isolation methods exist;
- the checked plan and self-test do not produce reviewed browser-reported versions or benchmark-ready pins.

Decision:

Treat `PB13-EV-005` and `PB13-EV-009` as partially strengthened by a checked browser-pin capture contract and no-browser artifact self-test. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, documentation indexes, and repository validator now include the browser-pin capture plan and no-browser self-test runner.

Next question:

What diagnostic capture evidence should be owner-reviewed before benchmark-ready local pins can be derived?

## 2026-07-18 — Benchmark competitor local install inventory

Question:

Which competitor browser executables are present on the current Windows high-end host, and what still prevents them from becoming benchmark-ready local pins?

Inputs:

- [Benchmark Competitor Local Install Inventory - July 2026](research/benchmark-competitor-local-install-inventory-2026-07.md);
- [Benchmark competitor local-install schema](blueprint-v1/machine/benchmark-competitor-local-install.schema.json);
- [Current Windows high-end competitor local installs](blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json);
- [`tools/validate_benchmark_competitor_local_installs.py`](../tools/validate_benchmark_competitor_local_installs.py);
- [Benchmark Competitor Version Manifest - July 2026](research/benchmark-competitor-version-manifest-2026-07.md).

Method:

Captured standard Windows executable, App Paths, selected BLBeacon, selected uninstall metadata, SHA-256 hashes, and Authenticode signer status for installed competitor browsers. The capture avoided user browser profiles, history, cookies, account state, extension data, cache directories, downloads, bookmarks, passwords, session state, crash reports, and browsing data.

Observations:

- Chrome and Edge executables were present in standard install paths and have captured SHA-256 hashes and valid Authenticode signatures;
- Chrome metadata is inconsistent across executable/product version, BLBeacon, uninstall metadata, and version directories;
- Edge executable and uninstall metadata report `151.0.4129.21`, which is newer than the recorded Edge Stable release catalog and therefore requires channel/update-ring resolution;
- Firefox was not found in the standard Windows paths checked;
- Safari Stable and Safari Technology Preview require macOS host evidence.

Decision:

Treat `PB13-EV-009` as partially strengthened by current-host executable/hash evidence for Chrome and Edge only. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, documentation indexes, and repository validator now include the competitor local-install registry.

Next question:

How should the browser-launch runner capture isolated browser-reported versions, channel proof, update state, profiles, command lines, settings, and raw artifacts without reading or mutating the owner's real browser profiles?

## 2026-07-18 — Benchmark competitor version manifest

Question:

Which official release catalogs should seed `PB13-EV-009` competitor-version records before any Chrome-class, fastest, lower-memory, lower-energy, or public performance claim can exist?

Inputs:

- [Benchmark Competitor Version Manifest - July 2026](research/benchmark-competitor-version-manifest-2026-07.md);
- [Benchmark competitor-version schema](blueprint-v1/machine/benchmark-competitor-version.schema.json);
- [Current desktop release-candidate competitor versions](blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json);
- [`tools/validate_benchmark_competitor_versions.py`](../tools/validate_benchmark_competitor_versions.py);
- [Chrome-Class Performance Runbook - July 2026](research/chrome-class-performance-runbook-2026-07.md).

Method:

Checked official browser release catalogs for Chrome Stable, Edge Stable, Firefox Stable, Safari Stable, and Safari Technology Preview on 2026-07-18. Added a no-claim release-catalog manifest, schema, and validator. Wired the registry into the `PB-013` readiness handoff, task queue, documentation indexes, repository map, benchmark-lab book, performance book, and repository validator.

Observations:

- the manifest records official release-catalog candidate versions only;
- every browser entry remains `benchmark_eligible: false`;
- no local executable path, executable hash, local profile, command line, settings, update state, raw artifacts, benchmark output, competitor result, ranking, or public claim exists;
- Safari stable metadata came from Apple Developer release-note catalog/search metadata and still needs local application version capture before benchmark use.

Decision:

Treat `PB13-EV-009` as partially strengthened by release-catalog candidate evidence only. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, source bibliography, documentation indexes, and repository validator now include the competitor-version registry.

Next question:

Which fixed hardware and local installed-browser pin records should become the first benchmark-eligible competitor-version manifests?

## 2026-07-17 — Build readiness task queue

Question:

How should a future maintainer move from the current `PB-*` blocker list to executable work without inventing scope, weakening gates, or losing traceability?

Inputs:

- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Build readiness task queue registry](blueprint-v1/machine/build-readiness-task-queue.json);
- [Agent Execution and Autonomous Engineering](agent-execution/README.md);
- [Execution task schema](agent-execution/machine/execution-task.schema.json);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json).

Method:

Added a proposed `TASK-*` queue that maps the current Servo/source-strategy, bootstrap reproduction, IPC, sandbox, benchmark, native UI, profile/session, and backup-ownership blockers to task-shaped handoff records. The queue records owners, independent reviewer scopes, requirements, risks, ADRs, allowed and prohibited paths, preconditions, acceptance criteria, negative tests, resource budgets, rollback evidence, and dependencies.

Observations:

- every queued task remains `proposed`, not approved or running;
- `TASK-000001` through `TASK-000008` cover the first continuation path from the operating board;
- the queue improves handoff from readiness records to task manifests, but it does not authorize execution, merge, release, source-strategy selection, or product claims;
- validation now requires the task queue to remain linked, ordered, dependency-consistent, and proposed-only.

Decision:

Treat the task queue as a documentation-control and handoff artifact. Keep broad implementation, source-strategy decisions, and public claims blocked until owner-reviewed task manifests and evidence exist.

Impact:

The documentation index, start-here guide, project-buildout handbook, operating board, repository map, pre-build readiness registry, Blueprint machine-companion summary, research log, and repository validator now include the build-readiness task queue.

Next question:

Which proposed task should be converted into the first owner-approved immutable task manifest?

## 2026-07-17 — Semantic resource attribution taxonomy

Question:

Which semantic owner taxonomy should Turing use before claiming memory, CPU, GPU, energy, wakeup, model, or 30-tab resource advantages over Chrome-class browsers?

Inputs:

- [Semantic Resource Attribution Taxonomy - July 2026](research/semantic-resource-attribution-taxonomy-2026-07.md);
- [Benchmark resource-attribution schema](blueprint-v1/machine/benchmark-resource-attribution.schema.json);
- [Semantic owner taxonomy](blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json);
- [`tools/validate_benchmark_resource_attribution.py`](../tools/validate_benchmark_resource_attribution.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Defined a checked taxonomy for semantic owners, required metrics, shared-resource charging policy, trace fields, collection-plan requirements, and UI/reporting disclosures. Wired the taxonomy into the no-claim benchmark manifest schema, sample manifest, smoke runner output, manifest validator, repository validator, and `PB-013` handoff documents.

Observations:

- the taxonomy ID is `TURING.BENCHMARK.RESOURCE_ATTRIBUTION.SEMANTIC_OWNERS.2026_07`;
- the checked owner classes cover browser UI/profile, documents/frames/site instances, JavaScript heap/code, DOM/style/layout/paint/accessibility, images/fonts/canvas/media, network/cache, storage, GPU, extensions, DevTools, agents, shared services, and unknown resources;
- the metrics include CPU time, queue wait, wakeups, private/resident/committed/shared/compressed/swap memory, GPU allocation, network bytes, disk I/O, energy estimate, model tokens, and provider cost estimate;
- `unknown` remains a first-class owner, and reports must distinguish physical totals from charged views.

Decision:

Treat `PB13-EV-011` as partial taxonomy evidence only. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, research program, benchmark-lab book, performance book, project-buildout handoff, ADR-0009 performance evidence, no-claim benchmark manifest, smoke runner, manifest validator, and repository validator now include the resource-attribution registry. No browser trace instrumentation, per-tab measurements, GPU accounting output, UI fixture, benchmark result, competitor comparison, or public performance claim exists.

Next question:

What trace-event schema and UI/report fixture should turn the taxonomy into browser-run evidence without hiding unknown or shared resource cost?

## 2026-07-17 — Benchmark OS and update-control manifest

Question:

Which current Windows OS, update, driver, firmware, power, display, thermal, clock, service, and artifact-control facts can seed `PB13-EV-002`, and what still prevents the host from being decision-grade benchmark evidence?

Inputs:

- [Benchmark OS and Update-Control Manifest - July 2026](research/benchmark-os-update-control-manifest-2026-07.md);
- [Benchmark OS-control schema](blueprint-v1/machine/benchmark-os-control.schema.json);
- [Current Windows high-end OS-control candidate](blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json);
- [`tools/validate_benchmark_os_controls.py`](../tools/validate_benchmark_os_controls.py);
- [Benchmark Hardware and OS Manifest - July 2026](research/benchmark-hardware-os-manifest-2026-07.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Captured current-host facts from Windows Update policy registry keys, Windows Update UX settings, Windows Insider registry keys, Windows current-version registry keys, selected update-related services, CIM OS/GPU/BIOS/baseboard queries, `powercfg`, timezone state, and `w32tm /query /status`. Stored the result in a checked OS-control manifest, wired its validator into repository validation, and linked the no-claim benchmark manifest and smoke runner output to the current OS-control ID.

Observations:

- the host is Windows 11 Pro Insider Preview `10.0.26220`, display version `25H2`, UBR `8491`, on the Beta/External Insider channel;
- `DisableWindowsUpdateAccess=1`, `DisableOSUpgrade=1`, and `NoAutoUpdate=1` were observed, but target release version, quality update, driver exclusion, and preview-build approval policies are not benchmark-grade;
- `bits` and `usosvc` were running, `wuauserv` was stopped/manual, and `WaaSMedicSvc` returned a permission-denied note while reporting stopped/manual;
- Ultimate Performance is active with processor min/max AC at 100 percent, but the display is still 165 Hz and thermal state is unmeasured;
- `w32tm /query /status` failed because the time service was not started;
- the manifest deliberately excludes product IDs, SIDs, digital product IDs, and other owner/machine secrets.

Decision:

Treat `PB13-EV-002` as partially strengthened by checked current-host OS-control evidence. Keep `PB-013` at `documented_no_runner`.

Impact:

The pre-build readiness registry, performance readiness packet, research program, benchmark-lab book, performance book, documentation indexes, repository map, pre-build checklist, operating board, project-buildout handoff, benchmark manifest validator, smoke runner self-test, and repository validator now include the OS-control manifest. No clean image, approved update freeze, driver freeze, browser-run benchmark result, competitor comparison, or public performance claim exists.

Next question:

Should the current Tier H host be cleaned and approved, or should benchmark lab work move to a separate Tier H host plus Tier M and Tier L reference machines?

## 2026-07-17 — Benchmark hardware and OS manifest

Question:

Which current Windows host facts can seed the `PB-013` hardware registry, and what remains before the host can support decision-grade Chrome-class performance evidence?

Inputs:

- [Benchmark Hardware and OS Manifest - July 2026](research/benchmark-hardware-os-manifest-2026-07.md);
- [Benchmark hardware schema](blueprint-v1/machine/benchmark-hardware.schema.json);
- [Current Windows high-end candidate manifest](blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json);
- [No-claim benchmark manifest sample](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [`tools/validate_benchmark_hardware.py`](../tools/validate_benchmark_hardware.py);
- [`tools/validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py);
- [`tools/run_benchmark_smoke.py`](../tools/run_benchmark_smoke.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [Chrome-Class Performance Runbook - July 2026](research/chrome-class-performance-runbook-2026-07.md).

Method:

Captured current-host facts from Windows CIM, Windows registry version keys, and `powercfg /getactivescheme`, then stored them in a checked benchmark hardware and OS manifest. Added the validator to the repository-wide validation path, wired the no-claim benchmark manifest sample to the current hardware registry entry, and made the smoke runner emit that hardware ID in its artifact package summary.

Observations:

- the available host is a high-end Windows desktop with AMD Ryzen 9 5950X, 64 GiB installed memory class, AMD Radeon RX 7900 XTX, Windows 11 Pro Insider Preview build 26220, and Ultimate Performance power scheme;
- the display is currently observed at 165 Hz, which is not normalized for MotionMark-class cross-browser comparison;
- the OS is not a clean lab image and update, driver, firmware, display, thermal, and artifact-storage controls are not frozen;
- the host is a Tier H candidate, not a Tier M denominator;
- the no-claim sample and smoke runner now carry the Tier H hardware ID for traceability, but they still do not launch a browser, measure performance, or create a result denominator.

Decision:

Treat `PB13-EV-001` and `PB13-EV-002` as partially strengthened by checked Tier H candidate hardware/OS evidence. Keep `PB-013` at `documented_no_runner`.

Impact:

The pre-build readiness registry, performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, documentation indexes, repository map, pre-build checklist, operating board, project-buildout handoff, and repository validator now include the hardware manifest. Benchmark manifest validation also cross-checks the default no-claim sample against the hardware registry. No browser benchmark, competitor comparison, or public performance claim exists.

Next question:

Which Tier M and Tier L machines should be captured next, and should the current high-end host be cleaned and approved or replaced?

## 2026-07-17 — Chrome-class performance runbook and no-claim metadata

Question:

Which current primary sources, competitor controls, and claim-expiry rules should govern Turing's Chrome-class and extreme-performance measurement path before any runner or result exists?

Inputs:

- [Chrome-Class Performance Runbook - July 2026](research/chrome-class-performance-runbook-2026-07.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [Benchmark manifest schema](blueprint-v1/machine/benchmark-manifest.schema.json);
- [No-claim benchmark manifest sample](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [`tools/validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py);
- BrowserBench Speedometer, JetStream, and MotionMark sources;
- Chromium Telemetry, Chrome UX Report, Web Vitals, Chrome DevTools, WebPageTest agent, and Chrome Releases sources.

Method:

Checked current primary benchmark and Chrome measurement sources, then converted them into a four-level runbook covering harness smoke, local browser pipeline, competitor diagnostic comparison, and public claim candidate evidence. Added explicit optional `claim` metadata to the benchmark manifest schema and no-claim sample, with validator enforcement for the default sample.

Observations:

- BrowserBench suites are useful diagnostics but cannot establish broad product leadership alone;
- Chrome-class comparison requires exact browser versions, channels, release metadata, command lines, profiles, security settings, caches, lifecycle settings, hardware, OS image, raw artifacts, and denominator accounting;
- Web Vitals and CrUX inform user-experience metrics, but CrUX is Chrome field data for eligible public destinations and is not a Turing lab result;
- claim text needs owner, reviewer, scope, unsupported behavior, expiration, and rerun triggers before it can appear publicly.

Decision:

Treat the runbook as stronger `PB13-EV-009` and `PB13-EV-010` evidence. Keep `PB-013` at `documented_no_runner` because fixed hardware, expanded corpus, browser launch, runner-generated raw artifacts, actual competitor runs, and owner-reviewed claim bundles do not exist.

Impact:

The research index, documentation index, repository map, performance book, benchmark-lab book, research program, pre-build checklist, build-readiness board, pre-build readiness registry, benchmark schema, sample manifest, and benchmark manifest validator now distinguish no-claim harness evidence from actual Chrome-class performance evidence.

Next question:

Which Tier M Windows hardware and OS image manifest should become the first Level 1 local browser pipeline target?

## 2026-07-17 — ADR-0009 public-claim and support-impact draft

Question:

What public-claim, support-language, requirement, risk, and registry impact would each `ADR-0009` source-strategy option require before owner review?

Inputs:

- [ADR-0009 Decision Draft and Public-Claim Impact](project-buildout/16-adr-0009-decision-draft.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [Start here](start-here.md);
- [Definition of done](blueprint-v1/20-definition-of-done.md).

Method:

Converted the existing source-strategy options into a non-decision template that names allowed claims, unsupported behavior, required document and registry updates, residual risks, and support-language baselines for each outcome.

Observations:

- no `ADR-0009` option is selected;
- Turing still cannot claim Servo adoption, Servo-derived release code, Chrome-class compatibility, production-safe browsing, security posture, memory leadership, speed leadership, or support commitments;
- each option requires different changes to the charter, requirements, risks, detailed engineering books, machine registries, support statements, dependency/provenance records, and work packages;
- final public wording depends on an owner-selected option and cannot be completed by an implementation agent alone.

Decision:

Move `ADR9-EV-017` from missing to partial. Keep `ADR9-EV-018` blocked and keep `PB-002` blocked.

Impact:

The buildout handbook, documentation index, repository map, start-here page, research program, operating board, evidence matrix, and readiness registries now include the decision draft as public-claim/support-impact evidence. No source strategy, public claim, support statement, or release path changed.

Next question:

Which owner-selected `ADR-0009` outcome, if any, should be accepted, rejected, superseded, or time-boxed?

## 2026-07-17 — Servo security and maintenance implications

Question:

What security/sandbox implications and upstream-maintenance signals exist before `ADR-0009` can accept, reject, or supersede a Servo relationship?

Inputs:

- [Servo Security and Maintenance Implications - July 2026](research/servo-security-maintenance-implications-2026-07.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [Security policy](security.md);
- [Security engineering book](security-engine/README.md).

Method:

Inspected Servo sandbox, multiprocess, event-loop, process-manager, option, feature, release, security-policy, CODEOWNERS, Dependabot, and workflow surfaces from the clean external checkout at `C:\ts\servo`, plus current `gh repo view` and release-list metadata for `servo/servo`.

Observations:

- Servo defaults are single-process and unsandboxed unless multiprocess/sandbox options are configured;
- the inspected Windows content-process sandbox path is unsupported, and the Windows multiprocess path spawns an unsandboxed child process;
- macOS/Linux-like `gaol` profiles exist but have no Turing effective-policy evidence or negative sandbox tests;
- event-loop routing, public/private resource/storage threads, and selected origin checks exist as security-relevant implementation concepts but need identity-preservation tests;
- script initial state carries many authority-bearing senders that need an owner-reviewed capability map;
- upstream `servo/servo` is public, not archived, security-policy-enabled, recently pushed/updated, and has release, CODEOWNERS, Dependabot, workflow, nightly, attestation, and crates.io publishing signals;
- those upstream signals do not satisfy Turing's own support, security-response, signing, update, or backup-owner obligations.

Decision:

Move `ADR9-EV-015` and `ADR9-EV-016` from missing to partial. Keep `PB-002` blocked. Treat the report as evidence preparation only, not security approval or an upstream maintenance commitment.

Impact:

The source-strategy packet, evidence matrix, machine registry, build-readiness board, research indexes, repository map, security policy, security book, research program, and pre-build checklist now separate observed Servo security/maintenance surfaces from owner-reviewed Turing acceptance. No source strategy, release-code authorization, security claim, or support statement changed.

Next question:

What exact public-claim, requirement, risk, support-language, and registry diff would each `ADR-0009` option require before an owner can review a decision draft?

## 2026-07-17 — Servo performance baseline preparation

Question:

What fixed-host, artifact, command-surface, fixture, and run-record evidence exists before `ADR-0009` can use Servo performance or memory data?

Inputs:

- [Servo Performance Baseline Preparation - July 2026](research/servo-performance-baseline-2026-07.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json).

Method:

Inspected the clean external Servo checkout at `C:\ts\servo`, the current debug `servoshell.exe` artifact identity, host hardware and OS facts from Windows CIM, Servo performance command surfaces, page-load harness files, TP5-style manifest state, and benchmark-adjacent fixture directories. No browser benchmark was executed.

Observations:

- the external checkout remained clean at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- the named Windows reference host and debug Servo artifact are now recorded for performance-prep traceability;
- Servo exposes page-load, Dromaeo, Speedometer, jQuery, and macOS power-measurement surfaces, but the page-load path is not a Turing fixed-hardware no-claim runner;
- Servo's current performance path can involve external downloads, WARC infrastructure, Python package installation, and Perfherder submission, so it must be adapted or replaced before Turing can use it as decision-grade evidence;
- no raw timing, memory, frame pacing, process, lifecycle, energy, competitor, or BrowserBench result exists.

Decision:

Move `ADR9-EV-014` from missing to partial. Keep `PB-002` blocked and keep `PB-013` at no-claim readiness status. Treat the new report as runbook and evidence-prep material only.

Impact:

The `ADR-0009` packet, evidence matrix, machine registry, build-readiness board, research indexes, repository map, performance book, benchmark-lab book, and pre-build checklist now distinguish performance preparation from performance measurement. No source strategy, dependency approval, component approval, compatibility claim, performance claim, or release-code authorization changed.

Next question:

Which browser-launch no-claim runner should execute the selected Servo source baseline against a Turing-owned local corpus and emit raw traces, memory snapshots, process topology, lifecycle state, failure denominator, and artifact hashes?

## 2026-07-17 — ADR-0009 machine evidence registry

Question:

How can the blocked `PB-002` source-strategy work stay coherent across many Servo evidence reports without relying only on prose tables?

Inputs:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a machine-readable `ADR9-EV-001` through `ADR9-EV-018` registry and JSON schema for the `ADR-0009` source-strategy decision. The registry records decision area, status, owner scopes, existing evidence, missing outputs, blocked dependencies, and next action for each evidence item. Added `tools/validate_adr_0009_evidence.py` and wired it into `tools/validate_blueprint.py` so the IDs, owner scopes, existing evidence paths, matrix synchronization, unresolved-output fields, claim boundaries, and `PB-002` blocked status are checked.

Observations at registry creation time:

- `ADR9-EV-001` through `ADR9-EV-010` have partial evidence but no owner-reviewed decision-grade completion;
- `ADR9-EV-011` through `ADR9-EV-017` were missing at registry creation time;
- `ADR9-EV-018` remains blocked by the unresolved evidence set;
- no Servo source strategy, source baseline, dependency approval, component approval, compatibility claim, performance claim, or release-code authorization exists.

Decision:

Treat the registry as the executable status companion for the prose matrix. Any future evidence-status move must update the registry and matrix together. `PB-002` remains blocked until `ADR-0009` evidence is owner-reviewed and the source-strategy decision is accepted, rejected, or superseded.

Impact:

Continuing agents now have a machine-checked queue for the first broad-build blocker. The registry improves handoff coherence but does not move Turing closer to a release-path Servo dependency by itself.

Next question:

Which `ADR9-EV-001` source-baseline option should be prepared for owner selection, and what exact provenance/equivalence policy would make later evidence reusable?

## 2026-07-17 — Benchmark smoke runner artifact package

Question:

Which runner command should capture the static-server self-test artifact, own a first artifact-package shape, and label unsupported browser behavior without hiding failures?

Inputs:

- [`tools/run_benchmark_smoke.py`](../tools/run_benchmark_smoke.py);
- [`tools/serve_benchmark_profile.py`](../tools/serve_benchmark_profile.py);
- [no-claim benchmark manifest sample](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added `tools/run_benchmark_smoke.py` with a `--self-test` mode that invokes the static-server self-test, writes `profile-self-test.json`, `runner-summary.json`, and `artifact-index.json` into a temporary artifact package, verifies file hashes, and emits a no-claim JSON summary. The command also accepts `--output-dir` for a persisted package during manual runner development. Wired the smoke runner into `validate_blueprint.py`.

Observations:

- the repository can now prove a minimal runner-owned artifact package shape without launching a browser;
- the artifact package records the static-server self-test, runner summary, artifact index, file byte counts, SHA-256 hashes, and unsupported behavior;
- no browser process, Turing page load, competitor page load, timing sample, memory sample, energy sample, accessibility sample, compatibility result, benchmark result, or performance claim exists.

Decision:

Treat `PB13-EV-005` as partial, not ready. The no-claim smoke runner is a command-contract seed only. `PB-013` remains `documented_no_runner` until fixed hardware, expanded corpus, runner-managed server artifacts, browser-launch runner behavior, runner-generated raw benchmark output, traces, non-sample artifact packages, competitor runbooks, and claim-expiry records exist.

Impact:

Future benchmark-runner work has a concrete artifact-package handoff and validation hook. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, compatibility, accessibility, battery, memory, regression, or production claims.

Next question:

Which browser-launch runner interface should add timeout, cancellation, cache reset, viewport, failure capture, and unsupported-case recording while preserving this no-claim artifact package?

## 2026-07-17 — Benchmark static-server self-test command

Question:

What is the smallest repository-owned static-server command that can serve the no-claim network profile, record its bound port and DNS override behavior, and still avoid benchmark or browser claims?

Inputs:

- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- [`tools/serve_benchmark_profile.py`](../tools/serve_benchmark_profile.py);
- [`tools/validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added `tools/serve_benchmark_profile.py` with a `--self-test` mode that validates the profile, starts an ephemeral loopback HTTP/1.1 static server, requests each configured route with a `turing.invalid:{port}` Host header, verifies status, content type, `Cache-Control: no-store`, bytes, and SHA-256, then emits a no-claim JSON artifact. The command also has a `--serve` mode that prints a startup artifact and serves the same profile for manual runner development. Wired the self-test into `validate_blueprint.py` and updated the network profile status to `self_test_only_no_benchmark_result`.

Observations:

- both seeded corpus cases can be served through the profile over `127.0.0.1` with a runner-assigned ephemeral port;
- the DNS behavior is recorded as Host-header self-test behavior only and does not modify the operating-system resolver;
- no browser run, benchmark result, latency result, cache result, TLS result, external DNS result, performance result, or competitor comparison exists.

Decision:

Treat `PB13-EV-004` as partially evidenced by the network-profile schema, no-claim profile, route-to-corpus mapping, validator, and static-server self-test command. Keep `PB-013` at `documented_no_runner` until fixed hardware, an expanded reviewed corpus, runner-managed server artifacts, runner-generated output, and non-sample raw-artifact validation exist.

Impact:

The benchmark lane can now prove the profile is executable without creating performance claims. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, compatibility, TLS, HTTP/2, HTTP/3, network-stack, or production claims.

Next question:

Which runner command should capture this self-test artifact, own server start/stop lifecycle, attach raw artifacts, and label unsupported browser behavior without hiding failures?

## 2026-07-17 — Benchmark local network-profile contract

Question:

What can make the `PB-013` local-server and network-profile requirement concrete before a server command, benchmark runner, fixed hardware, or performance result exists?

Inputs:

- [Benchmark network profile schema](blueprint-v1/machine/benchmark-network-profile.schema.json);
- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- [no-claim sample benchmark manifest](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [`tools/validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added a network-profile schema and a no-claim profile for serving the seeded corpus from the then-future loopback HTTP/1.1 static server path. The profile records `turing.invalid` DNS override requirements, route-to-corpus mapping, cold cache state, no-store response headers, disabled external network, disabled authentication, loopback transport, and explicit unsupported cases. Added a validator that checks loopback-only serving, route coverage against the corpus manifest, corpus entry-path agreement, DNS policy, cache headers, disabled HTTP/2/HTTP/3/TLS/authentication flags, unsupported-case declarations, and no benchmark-run claims. Wired the validator into `validate_blueprint.py`.

Observations:

- the repository had a concrete local serving contract for the then-current two no-claim corpus cases;
- the no-claim sample benchmark manifest points to `TURING.NETWORK.NOCLAIM_LOCAL_STATIC.2026_07`;
- at this earlier stage, the repository still lacked a server process, DNS override execution, TLS certificate profile, HTTP/2 or HTTP/3 profile, proxy profile, authentication mock, latency/loss/bandwidth shaping, browser run, or benchmark result.

Decision:

Treat `PB13-EV-004` as partially evidenced by the network-profile schema, no-claim local static profile, route-to-corpus mapping, and validator. Keep `PB-013` at `documented_no_runner` until runner-managed server evidence, runner-generated output, and non-sample artifact package exist.

Impact:

The benchmark lane now has an enforceable network-profile contract before implementation. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, compatibility, TLS, network-stack, or production claims.

Next question:

What is the smallest repository-owned static-server command that can serve this profile, record its bound port and DNS override behavior, and produce a no-claim runner smoke artifact?

## 2026-07-17 — Benchmark corpus seed and validator

Question:

What can make the `PB-013` offline-corpus requirement concrete before a fixed hardware lab, local server, benchmark runner, or performance result exists?

Inputs:

- [Benchmark corpus schema](blueprint-v1/machine/benchmark-corpus.schema.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- generated static-document fixture under `benchmarks/corpus/no-claim-smoke/static-document/`;
- generated app-like fixture under `benchmarks/corpus/no-claim-smoke/app-like/`;
- [`tools/validate_benchmark_corpus.py`](../tools/validate_benchmark_corpus.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added the initial two local generated HTML fixtures and a machine-readable corpus manifest that records case IDs, categories, entry paths, `turing.invalid` origins, SHA-256 hashes, byte counts, generated-content license notes, expected M0 unsupported behavior, and no-claim status. Added a validator that checks unique case IDs, required categories, local fixture paths, fixture byte counts, SHA-256 hashes, LF line endings, no external network URL references, and no measurement-claim flags. Wired the validator into `validate_blueprint.py`.

Observations:

- the repository gained the initial concrete two-case corpus seed for the first no-claim runner smoke contract;
- the seed covers one static-document case and one app-like JavaScript interaction case;
- fixture bytes and hashes are checked, so local corpus drift fails validation;
- no local server, DNS/TLS profile, browser run, trace, sample statistics, competitor baseline, or performance claim exists.

Decision:

Treat `PB13-EV-003` as partially evidenced by the schema, no-claim corpus manifest, the initial generated local fixtures, and corpus validator. Keep `PB-013` at `documented_no_runner` until a reviewed representative corpus, fixed hardware, runner-generated results, and artifact package exist.

Impact:

Benchmark readiness now has enforceable corpus identity before the runner exists. The seed is not representative enough for compatibility, low-memory, fastest, Chrome-class, daily-driver, or production claims.

Next question:

Which local server, cache, DNS/TLS, and network profile should serve the no-claim corpus cases for the first runner smoke task?

## 2026-07-17 — Benchmark manifest sample and validator

Question:

What evidence can make the `PB-013` raw-result schema requirement concrete before a benchmark runner, fixed hardware, or corpus exists?

Inputs:

- [Benchmark manifest schema](blueprint-v1/machine/benchmark-manifest.schema.json);
- [no-claim sample manifest](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [raw-artifact index fixture](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.raw-artifacts.json);
- [`tools/validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added a sample manifest that exercises the current benchmark-manifest fields without claiming a benchmark result. Added a raw-artifact index fixture and a validator command that checks required fields, rejects unsupported fields, compares lifecycle state counts to tabs, validates SHA-256 format, and verifies the checked raw-artifact hash for the default fixture. Wired the validator into `validate_blueprint.py` so CI and local repository validation enforce the fixture.

Observations:

- the manifest schema now has an executable no-claim fixture;
- the raw-artifact hash path is checked against a committed file, so fixture drift fails validation;
- the sample deliberately records unsupported M0 web-rendering behavior and the note "harness smoke evidence only";
- no hardware, corpus, runner-generated raw result, trace, statistics, competitor baseline, or performance claim was created.

Decision:

Treat `PB13-EV-006` as partially evidenced by the sample manifest, raw-artifact index, direct validator command, and repository validation hook. Keep `PB-013` at `documented_no_runner` until runner-generated results and non-sample artifact packages exist.

Impact:

The benchmark evidence lane is more concrete and harder to drift. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, or production claims.

Next question:

Which Tier M host and first two local corpus cases should generate the first real no-claim runner output using this manifest contract?

## 2026-07-17 — Performance benchmark readiness packet

Question:

What must exist before Turing can treat performance measurement as build-ready, compare against Chrome-class browsers, or support an extreme-performance claim?

Inputs:

- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [Performance, Memory, Energy, and the 30-Tab Contract](blueprint-v1/09-performance-memory.md);
- [Fixed-Hardware Benchmark Laboratory](benchmark-lab/README.md);
- [Browser Performance Engineering](performance/README.md);
- [benchmark manifest schema](blueprint-v1/machine/benchmark-manifest.schema.json);
- official BrowserBench and Microsoft Windows Performance Toolkit pages checked on 2026-07-17.

Method:

Reviewed current performance and benchmark documentation, machine readiness state for `PB-013`, the existing benchmark manifest schema, BrowserBench's current benchmark entry points, and Microsoft WPR/WPA documentation. Converted the broad "fixed hardware, offline corpus, raw result schema" blocker into a `PB13-EV-*` evidence matrix. No benchmark was run and no performance result was created.

Observations:

- the performance Blueprint, benchmark-lab book, and benchmark manifest schema already define measurement discipline, but they do not provide a fixed host, corpus, runner, raw artifact store, or competitor baseline;
- BrowserBench currently exposes Speedometer 3.1, JetStream 3.0, and MotionMark from the generic MotionMark page, which means every benchmark run must pin the exact suite URL and version;
- Windows WPR/WPA are suitable first Windows trace-capture inputs, but they do not solve cross-platform tracing or product claim governance by themselves;
- `PB-013` needed more precise missing evidence: fixed hardware inventory, OS image/update control, offline corpus, local server/network profile, runner command, raw samples, trace package, 30-tab manifests, competitor runbooks, and claim-expiry policy.

Decision:

- add the performance benchmark readiness packet;
- add it to the documentation index, research index, performance book, benchmark-lab book, repository map, project-buildout handoff, build-readiness board, and `pre-build-readiness.json`;
- update benchmark source references to include JetStream 3.0, the current MotionMark entry point, and Windows WPR/WPA documentation;
- keep `PB-013` at `documented_no_runner`.

Impact:

The project now has a concrete performance-readiness queue aligned with the Chrome-class and extreme-performance destination. No benchmark runner exists yet, no competitor comparison exists, and no speed, memory, energy, Chrome-class, daily-driver, accessibility, security, or production claim changed.

Next question:

Which Tier M reference host, OS image, first two local corpus cases, result fixture, and WPR/WPA trace artifact layout should seed the first no-claim benchmark runner smoke test?

## 2026-07-17 — Documentation orientation and audit-status refresh

Question:

Which top-level orientation documents still described earlier documentation snapshots as current state, and what should a maintainer read before continuing build-prep work?

Inputs:

- [Start Here](start-here.md);
- [Documentation index](README.md);
- [Research index](research/README.md);
- [Blueprint index](blueprint-v1/README.md);
- [Documentation Expansion Audit - July 2026](research/documentation-expansion-audit-2026-07.md);
- [Performance, Security, Developer, and Missing-Systems Expansion Audit - July 2026](research/performance-security-developer-expansion-audit-2026-07.md);
- current [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md), [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md), and `pre-build-readiness.json`.

Method:

Scanned orientation and audit documents for stale book counts, old expansion queues, readiness language, and missing handoff links. Updated current-state documents to point maintainers to the readiness board and `ADR-0009` packet before implementation. Preserved older research reports as historical snapshots instead of rewriting their original findings.

Observations:

- `start-here.md` still described the repository as having nineteen detailed books and did not put the readiness board in the primary reading order;
- the first documentation expansion audit still described later networking, storage, media, platform, accessibility, release, extension, web-governance, and benchmark books as a future queue even though those books now exist;
- the second expansion audit described the nineteen-book state as current, while the current documentation index lists twenty-seven detailed books;
- the authoritative build-start controls are now the pre-build checklist, build-readiness board, machine readiness registry, and `ADR-0009` source-strategy packet.

Decision:

- update current orientation to say the repository has twenty-seven detailed engineering, product, operating, and competitive books;
- add the pre-build checklist and build-readiness board to the primary reading order;
- add an explicit current build-readiness section stating that only contained M0 implementation is authorized;
- mark the earlier expansion audits as historical snapshots and route current continuation through the readiness controls;
- keep all implementation, requirement, risk, work-package, source-policy, and support statuses unchanged.

Impact:

Documentation handoff is clearer for a maintainer or agent resuming work. No implementation status changed, no Chrome-class or performance claim was promoted, and broad implementation remains blocked by the readiness gates.

Next question:

Which current readiness item should be converted into the next evidence packet: the native UI reference-shell comparison, packaged sandbox probes, fixed-hardware benchmark laboratory, or profile/session schema work?

## 2026-07-17 — Servo build-script and proc-macro side-effect audit

Question:

Which Servo registry, git, and path build scripts and proc macros need side-effect review before `ADR-0009` can trust any candidate component boundary?

Inputs:

- [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](research/servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- default Cargo metadata with `1069` packages and all-features metadata with `1120` packages;
- local registry, Stylo git, and Servo path source roots referenced by Cargo metadata.

Method:

Parsed Cargo metadata outside Turing, classified build-script and proc-macro packages by source kind, compared default and all-features metadata, and ran static marker scans over locally available build-script files and proc-macro source roots. Marker classes covered process execution, filesystem writes and `OUT_DIR`, URL/download/fetch strings, environment and Cargo cfg variables, compiler/linker/tool names, time/git inputs, and native-copy/package strings. No Servo source, metadata file, generated output, build log, proc-macro expansion, registry archive, or native artifact was copied into Turing.

Observations:

- default metadata exposed `157` build-script packages, `70` proc-macro packages, and `25` native-link packages;
- all-features metadata exposed `167` build-script packages, `71` proc-macro packages, and `26` native-link packages;
- default build-script packages were `144` registry, `9` path, and `4` git packages;
- default proc-macro packages were `62` registry, `6` path, and `2` git packages;
- all-features metadata added `10` build-script packages, `prost-derive`, and `libdbus-sys` as a native-link package;
- build-script marker triage found `3492` environment/cfg markers, `816` compiler/linker markers, `631` native-copy/package markers, `410` filesystem/write markers, `267` URL/download/fetch markers, `116` process markers, and `18` time/git markers;
- proc-macro source roots covered `744` Rust files and `5331698` bytes, with registry proc macros dominating marker volume.

Inference:

The `ADR9-EV-008` blocker is now a concrete review queue instead of a broad "registry/git build-script" gap. The evidence is still static triage only. Turing still needs owner-selected baseline/profile/component boundary, accepted side-effect policy, dynamic tracing, proc-macro expansion review, generated-output provenance, clean-target regeneration, independent replay, and owner approval.

Changes:

- add the [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](research/servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, generated/native/unsafe/FFI classification, build-script/generated-output audit, repository map, project-buildout index, and this log;
- keep `PB-002` blocked and keep `ADR9-EV-008` partial.

Security, privacy, provenance, and release impact:

No build script, proc macro, generated output, native package, dependency, or source baseline was approved. The report improves release safety by requiring deny-by-default network policy, environment allowlists, output-directory bounds, compiler/linker/native-copy tracing, proc-macro expansion review, and owner approval before build-time code can be trusted.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. Build-time code and proc-macro review remain prerequisites for selecting a component boundary, not evidence that any web-platform feature works.

Performance and resource impact:

No performance claim changed. Marker counts and proc-macro source size are build/review-cost inputs, not runtime memory, startup, interaction, energy, or Chrome-class evidence.

Licensing and operational impact:

No license status changed. Build-script outputs, proc-macro expansions, generated files, native-copy behavior, registry crates, Stylo git packages, and path packages still need source-to-output provenance, notices, advisory handling, and package-manifest linkage.

Next question:

Which owner-selected Servo baseline, feature profile, target, build profile, and candidate component boundary should dynamic side-effect tracing and proc-macro expansion review use?

## 2026-07-17 — Servo native package decision prep

Question:

What native source-build, binary-package exception, deterministic-download verification, package-minimization, notice, and manifest decisions remain before `ADR-0009` can select any Servo relationship that reaches Servo's Windows bootstrap or media package surface?

Inputs:

- [Servo Native Package Decision Prep - July 2026](research/servo-native-package-decision-prep-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](research/servo-native-bootstrap-provenance-audit-2026-07.md);
- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- `servo/servo-build-deps` release metadata for tag `msvc-deps`;
- local native asset hashes and signature checks under `C:\ts\servo-native-artifacts-msvc-deps`;
- bounded extracted dependency, license-root, plugin-list, and debug-output counts under `C:\ts\servo`.

Method:

Captured bounded local facts without importing Servo source, native packages, generated output, build logs, downloaded archives, or MSI files into Turing. Rechecked `servo-build-deps` release metadata through GitHub CLI, summarized local asset hashes and Authenticode posture, counted extracted package roots and signature states, parsed GStreamer plugin-list and Windows copy-candidate counts from source files, and converted the prior native provenance audit into source-build, binary-package exception, deterministic-download, and package-manifest decision queues.

Observations:

- the external checkout is still a shallow build-baseline snapshot and is `2` commits behind `origin/main`;
- `servo-build-deps` release metadata for the three relevant assets still exposed `digest: null`;
- local hashes exist for `moztools-4.0.zip` and the two GStreamer MSVC `1.22.8` MSI assets, but the GStreamer MSIs were not Authenticode-signed;
- extracted dependencies contained `4630` files under `gstreamer`, `14824` files under `moztools`, and two smaller extracted-tree GStreamer MSI artifacts;
- extracted `.dll`, `.exe`, and `.msi` signature checks found `981` unsigned files and one valid signed `vswhere.exe`;
- GStreamer packaging source names `86` Windows GStreamer copy candidates before transitive dependency and package availability checks;
- debug output contained `146` DLLs, `208` EXEs, and `263` PDBs, proving a final package manifest cannot be implicit.

Inference:

The native package blocker is now split into explicit package-family decisions. `ADR9-EV-005` needs source-build recipes or binary-package exception records, package-minimization decisions, legal/advisory/notice review, final manifests, and owner approvals. `ADR9-EV-006` needs accepted hash/signature/mirror policy, implementation, and independent replay evidence.

Changes:

- add the [Servo Native Package Decision Prep - July 2026](research/servo-native-package-decision-prep-2026-07.md);
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, native bootstrap audit, repository map, project-buildout index, and this log;
- keep `PB-002` blocked and keep `ADR9-EV-005` and `ADR9-EV-006` partial.

Security, privacy, provenance, and release impact:

No native package was approved. The decision-prep report improves release safety by requiring fail-closed download verification, source-build or binary-package exception records, signature/hash/mirror policy, native advisory review, and final package manifests before any Servo-native surface can affect release code.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. Media and platform package decisions remain prerequisites for later compatibility and accessibility testing, not evidence that those tests pass.

Performance and resource impact:

No performance claim changed. File counts, copied package candidates, and debug-output size are release-footprint inputs, not runtime speed, memory, energy, or Chrome-class evidence.

Licensing and operational impact:

No license status changed. GStreamer, moztools, MSYS2-derived tools, codec libraries, crypto libraries, ANGLE outputs, platform redistributables, notices, source-offer obligations, package minimization, and SBOM component records remain owner-review items.

Next question:

Which owner-selected Servo baseline and feature profile should the native package manifest, source-build recipes, binary-package exception records, deterministic-download implementation, and independent replay use?

## 2026-07-17 — Servo license advisory and SBOM decision prep

Question:

What Turing-specific license, advisory, duplicate-version, native-notice, and SBOM decisions remain before `ADR-0009` can select any Servo relationship?

Inputs:

- [Servo License Advisory and SBOM Decision Prep - July 2026](research/servo-license-advisory-decision-prep-2026-07.md);
- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- Servo `Cargo.lock`, `deny.toml`, `about.toml`, default and all-features Cargo metadata, and rerun `cargo-deny` logs outside the Turing repository;
- bounded native GStreamer license-directory counts from the extracted Windows dependency tree.

Method:

Reran bounded evidence extraction against the external checkout and local metadata. Parsed Cargo metadata for package, source, license-expression, missing-license, git-source, and duplicate-version counts. Read Servo's `deny.toml` advisory comments and license allow-list. Checked the rerun `cargo-deny` log summaries and hashes. Counted the native GStreamer license directory without copying native files, logs, metadata, generated output, or Servo source into Turing.

Observations:

- the external checkout is still a shallow build-baseline snapshot and is `2` commits behind `origin/main`;
- the default metadata has `1069` packages, `48` unique license expressions, `0` packages missing both `license` and `license_file`, and `58` duplicate package names;
- the all-features metadata has `1120` packages, `50` unique license expressions, `0` packages missing both `license` and `license_file`, and `69` duplicate package names;
- the rerun `cargo-deny` logs exited clean under Servo policy for default and all-features metadata, but Servo's policy ignores `12` RustSec advisories;
- the observed GStreamer license directory has `69` package directories, `155` files, and `1141093` bytes of license material;
- no complete Turing SBOM was generated and no Turing SBOM toolchain was selected.

Inference:

The license/advisory gap is no longer unshaped. It is now a specific queue: select baseline and feature profile, select SBOM tooling, generate a complete SBOM, normalize license expressions, decide notices/source-offer obligations, decide duplicate-version policy, accept or reject advisory exceptions, and review native license/notice/source-build obligations.

Changes:

- add the [Servo License Advisory and SBOM Decision Prep - July 2026](research/servo-license-advisory-decision-prep-2026-07.md);
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, dependency inventory, supply-chain scan, repository map, project-buildout index, and this log;
- keep `PB-002` blocked, keep `ADR9-EV-003` partial, and move `ADR9-EV-004` from missing to partial.

Security, privacy, provenance, and release impact:

No dependency, advisory exception, native package, generated output, or source baseline was approved. The report reduces release risk by making unaccepted RustSec ignores, duplicate versions, native license material, and SBOM gaps explicit before any implementation relies on Servo.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. The evidence is supply-chain and legal-readiness input only.

Performance and resource impact:

No performance claim changed. Duplicate-version and native-package counts are resource-risk inputs, not runtime measurements.

Licensing and operational impact:

No license status changed. Legal approval, accepted license list, third-party notices, source-offer handling, codec and patent review, native package notices, generated-output provenance, advisory exceptions, and SBOM generation remain required.

Next question:

Which owner-selected Servo baseline and feature profile should the SBOM, license matrix, advisory exception records, duplicate-version policy, and native package decision prep use?

## 2026-07-17 — Servo build replay protocol draft

Question:

What exact runbook should an owner review before attempting the independent clean-target Servo build replay required by `ADR9-EV-002`?

Inputs:

- [Servo Build Reproduction Evidence and Gap Report - July 2026](research/servo-independent-build-reproduction-2026-07.md);
- current `ADR9-EV-002` evidence matrix row;
- same-host Visual Studio, LLVM, Python, Rust, `uv`, log, artifact, target, and cache observations.

Method:

Extended the existing `ADR9-EV-002` report instead of creating a competing document. Added explicit protocol tiers, required variables, path/deletion guard, host/toolchain capture commands, source checkout and identity checks, bootstrap/build log capture, evidence-bundle requirements, and success criteria. No command was executed and no Servo source, generated output, native binary, registry archive, downloaded package, build log, or build artifact was copied into Turing.

Observations:

- the previous report had enough evidence for same-host handoff but only a minimal command sketch;
- `ADR9-EV-002` needs an owner-accepted protocol or script before the independent clean-target run can be evaluated consistently;
- the protocol must reject Turing-internal paths, avoid blind `vswhere -latest` selection, record cache modes, capture failures, and distinguish same-host replay from decision-grade independent replay.

Inference:

The build-reproduction gap is now narrower: the missing work is no longer "what should the replay capture" but owner acceptance and an actual independent clean-target run using the documented protocol.

Changes:

- expand the build reproduction report with a replay-protocol draft;
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, and this log to name the protocol draft;
- keep `PB-002` blocked and `ADR9-EV-002` partial.

Security, privacy, provenance, and release impact:

No source approval changed. The protocol improves deletion safety and evidence capture by requiring path resolution, external workspace checks, target/cache mode disclosure, and failure logs before any independent replay can be treated as evidence.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. The protocol only builds Servo; it does not run WPT, Test262, accessibility tests, a local corpus, or browser UI workflows.

Performance and resource impact:

No performance claim changed. The protocol records build and cache footprint evidence only; browser runtime measurements remain separate `ADR9-EV-014` work.

Next question:

Can release-operations and quality owners accept this replay protocol, then run it from a clean target on an independent Windows host or clean VM and preserve the required success/failure evidence bundle?

## 2026-07-17 — Servo build reproduction evidence and gap report

Question:

Can the successful external Servo Windows bootstrap and development build be handed off with enough environment, log, artifact, cache, and failure detail for `ADR9-EV-002`, and what still blocks independent build reproduction?

Inputs:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- local build logs under `C:\ts`;
- local `servoshell.exe` under `C:\ts\servo\target\debug`;
- Visual Studio 2022, LLVM, Python, Rust, `uv`, target, Cargo registry, and Cargo git cache observations from the reference Windows host.

Method:

Inspected Git identity, tracked-file status, log sizes and hashes, selected build result lines, artifact size/hash, normal shell tool availability, Visual Studio developer prompt compiler availability, host hardware/OS, and target/cache footprints. No Servo source file, generated output, native binary, registry archive, downloaded package, build log, or build artifact was copied into Turing.

Observations:

- the build checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- `C:\ts\servo-build-dev-vsdevcmd-llvm.out.log` recorded `Succeeded in 0:09:21` and `BUILD_EXIT=0`;
- Cargo reported `Finished dev profile [unoptimized + debuginfo] target(s) in 9m 14s`;
- `servoshell.exe` was `298702336` bytes with SHA-256 `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B`;
- the successful environment used CPython `3.11.9`, Servo Rust `1.95.0-x86_64-pc-windows-msvc`, Visual Studio Professional 2022 Developer Command Prompt `17.14.21`, MSVC `14.44.35207`, compiler/linker version `19.44.35221` / `14.44.35221.0`, and `LLD 22.1.8`;
- normal PowerShell still lacks `cl`, `link`, and `lld-link`;
- `C:\ts\servo\target` contained `38370` files and `35941861226` bytes, so the existing target cannot stand in for clean-target reproduction.

Inference:

The old "build logs outside repo" note is now too vague. Same-host build evidence is captured enough for handoff, but `ADR9-EV-002` is still partial because decision-grade reproduction requires an owner-reviewed replay script, target/cache isolation policy, clean-target replay on an independent Windows host or VM, and success/failure log bundles.

Changes:

- add the [Servo Build Reproduction Evidence and Gap Report - July 2026](research/servo-independent-build-reproduction-2026-07.md);
- link it from the documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, and this log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo source, dependency, native artifact, generated output, build log, or provenance attestation entered the repository.

Security, privacy, provenance, and release impact:

No source approval changed. The report strengthens provenance and release handoff by recording log and artifact hashes, but it also preserves the unresolved risks around a shallow build checkout, warm target directory, shared Cargo caches, native bootstrap downloads, and missing independent replay.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. The report did not run WPT, Test262, accessibility tests, a local corpus, or UI/input workflows.

Performance and resource impact:

No performance claim changed. The build duration, artifact size, and target/cache footprint are build-operational observations only; they do not measure browser startup, memory, energy, layout, rendering, or interaction performance.

Documentation and registry impact:

- `PB-002` has sharper build-reproduction evidence but remains blocked;
- `ADR9-EV-002` remains partial;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, research log, and the new build reproduction report.

Next question:

Can the same Servo commit be rebuilt from a clean target on an independent Windows host or clean VM using an owner-reviewed replay script, with target/cache isolation, success/failure logs, and no hidden dependency on warm local state?

## 2026-07-17 — Servo source-baseline equivalence policy prep

Question:

What source-content, release-archive, and crates.io package equivalence evidence exists for the Servo source candidates, and what policy decisions remain before `ADR-0009` can select or reject a source baseline?

Sources and versions:

- independent bare Servo clone at `C:\ts\servo-independent-source-verify-20260717.git`;
- Servo release tag `v0.3.0` at `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`;
- vendored release source archive `C:\ts\servo-upstream-source-provenance-20260717\servo-v0.3.0-src-vendored.tar.gz`;
- cached crates.io package `servo-0.4.0.crate`;
- crates.io package VCS commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873`.

Method and environment:

Compared Git tree path sets with Python `tarfile` path sets for the vendored source archive and cached `.crate` package. Read only bounded metadata such as `GIT_REVISION` and `.cargo_vcs_info.json`. No Servo source files, release archive, crate archive, generated output, native binary, or build log was copied into Turing.

Observations:

- the vendored release archive records `GIT_REVISION` as `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, matching `v0.3.0`;
- the `v0.3.0` Git tree has `191174` files;
- the vendored release archive has `252589` files and `2089732373` file bytes;
- `191078` vendored archive files match release Git paths;
- `61511` vendored archive files are not in the release Git tree, led by `61510` under `vendor/` plus `GIT_REVISION`;
- `96` release Git files are missing from the vendored archive, mostly under `etc/`;
- crates.io `servo 0.4.0` records VCS commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873` and `path_in_vcs` `components/servo`;
- the crate contains all `30` files from `components/servo` at that commit plus four Cargo package metadata files.

Inference:

The vendored release archive is a derived source package, not the release Git tree. The crates.io package is a component package, not the whole Servo repository. `ADR-0009` cannot reuse evidence across Git trees, vendored archives, and crates.io packages without an owner-accepted equivalence policy.

Decision:

- add the [Servo Source Baseline Equivalence Policy Prep - July 2026](research/servo-source-baseline-equivalence-policy-2026-07.md);
- link it from the documentation index, research index, repository map, build-readiness board, pre-build checklist, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, independent source verification report, source/archive provenance audit, and this log;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- update `ADR9-EV-001` missing output from raw equivalence discovery to owner-selected source baseline, signed-tag or equivalent provenance decision, owner-accepted equivalence policy, selected-baseline blob/legal review, and rerun plan.

Security/privacy impact:

No runtime authority changed. The report prevents source-surface confusion that could otherwise let vendored dependencies or normalized crate packages bypass security and provenance review.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. If an accepted baseline differs from the current build commit, future compatibility, accessibility, and local corpus evidence must be tied to that selected baseline.

Performance/memory/energy impact:

No performance claim changed. The source-surface differences mean performance evidence must not be reused across Git tree, release archive, and crates.io package surfaces without explicit scoping.

Licensing/operational impact:

No license or redistribution status changed. The report identifies vendored dependencies, omitted Git files, and normalized Cargo package metadata as legal/source-offer and operations review inputs.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has sharper equivalence evidence but remains blocked;
- `ADR9-EV-001` remains partial until baseline selection, accepted provenance/equivalence policy, selected-baseline blob/legal review, and rerun policy are complete;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, independent source verification report, source/archive provenance audit, research log, and the new equivalence policy prep report.

Unresolved questions:

Which source baseline model should an owner select or reject, and what provenance, blob-content, legal, source-offer, and rerun rules are acceptable for that model?

Next evidence required:

Choose or reject a source-baseline model, accept or reject a signed-tag/equivalent provenance policy, perform selected-baseline blob/legal/source-offer review, and scope or rerun build/dependency/generated/native/compatibility/performance evidence for the selected baseline.

## 2026-07-17 — Servo independent source verification

Question:

Can Turing independently verify Servo's current `main`, the successful external build baseline, and the latest GitHub release source objects from a non-shallow Git fetch, and what remains before `ADR-0009` can select a source baseline?

Sources and versions:

- independent bare partial clone at `C:\ts\servo-independent-source-verify-20260717.git`;
- Servo remote `https://github.com/servo/servo.git`;
- current Servo `main` `622600e045c2e5ea688a9b19b8671b6f43112817`;
- successful external build baseline `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- Servo release tag and branch `v0.3.0` / `release/v0.3` at `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`.

Method and environment:

Created a fresh bare, non-shallow, `blob:none` partial clone outside Turing. Inspected ref identity, object identity, tree identity, tree file counts, ancestry counts, merge bases, connectivity, tag verification posture, and local commit-signature posture. No Servo source files, release archives, crate archives, generated output, native binaries, or build logs were copied into Turing.

Observations:

- the independent clone is bare, non-shallow, and partial with `blob:none`;
- `git fsck --connectivity-only` exited `0` and reported `82` dangling commits plus `153` dangling trees;
- current `main` resolved to `622600e045c2e5ea688a9b19b8671b6f43112817`, tree `9d71530fe4d36dd9c94a2a411d75f219fde0dfc9`, with `193033` tree files;
- the successful build baseline resolved to `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, with `193033` tree files;
- non-shallow ancestry showed the build baseline is exactly two commits behind current `main`;
- `v0.3.0` and `release/v0.3` resolved to `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, tree `c41b1defccd9ed47a5ac2a8ad40929bc34de80a0`, with `191174` tree files;
- non-shallow ancestry for `v0.3.0...main` returned `1 838`, so the release branch is not a simple ancestor of current `main`;
- `git tag -v v0.3.0` failed because the ref is a lightweight commit tag, not a tag object;
- local `git verify-commit` found signatures on the two GitHub-merged commits but could not check them without the relevant public key; the release commit produced no local signature detail.

Inference:

Independent non-shallow Git object and ancestry verification is now captured for `ADR9-EV-001`. The remaining source-identity work is no longer "can we fetch the object graph independently"; it is owner-selected baseline policy, signed-tag or equivalent provenance policy, blob-content/release-archive/crates.io equivalence, and rerun scoping for whichever baseline is selected.

Decision:

- add the [Servo Independent Source Verification - July 2026](research/servo-independent-source-verification-2026-07.md);
- link it from the documentation index, research index, repository map, build-readiness board, pre-build checklist, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, and this log;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- update `ADR9-EV-001` missing output from independent non-shallow source verification to owner-selected baseline, provenance policy, content/archive/package equivalence, and rerun policy.

Security/privacy impact:

No runtime authority changed. The report improves source-trust evidence while making clear that local GPG verification is not a configured Turing trust root and that source-identity evidence is not security approval.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The source-baseline choice still determines which future WPT, local corpus, accessibility, and platform-surface evidence must be rerun.

Performance/memory/energy impact:

No performance claim changed. The report reinforces that current `main`, the build baseline, and release branch cannot share performance evidence without explicit scoping.

Licensing/operational impact:

No license or redistribution status changed. The report does not inspect full source blob content, release-archive equivalence, crates.io package contents, notices, source-offer obligations, or SBOM posture.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has sharper independent Git evidence but remains blocked;
- `ADR9-EV-001` remains partial until baseline selection, equivalent provenance policy, content/archive/package equivalence, and rerun policy are complete;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, research log, and the new independent source verification report.

Unresolved questions:

Which source baseline model should `ADR-0009` evaluate first, and what does Turing accept as equivalent provenance when a release is represented by a lightweight tag, a GitHub source archive, and a crates.io package surface that are not the same source object?

Next evidence required:

Select or reject a source-baseline model, define signed-tag or equivalent provenance policy, define blob-content/release-archive/crates.io package equivalence checks, and rerun build/dependency/generated/native/compatibility/performance evidence if the selected baseline differs from the current external build baseline.

## 2026-07-17 — Servo upstream source provenance report

Question:

Which upstream Servo source identities correspond to the successful external Windows build baseline, current upstream `main`, the latest GitHub release, and the latest crates.io package, and what remains before `ADR-0009` can select a source baseline?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- successful external build baseline `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- refreshed Servo `origin/main` `622600e045c2e5ea688a9b19b8671b6f43112817`;
- Servo GitHub release `v0.3.0`, published 2026-06-25T15:09:42Z;
- downloaded `servo-v0.3.0-src-vendored.tar.gz` under `C:\ts\servo-upstream-source-provenance-20260717`;
- crates.io `servo 0.4.0`.

Method and environment:

Fetched Servo tags and `origin`, inspected local and remote object IDs, queried GitHub release and commit verification metadata through GitHub CLI, queried crates.io metadata through Cargo and the crates.io API, downloaded the `v0.3.0` vendored source archive outside Turing, verified SHA-256 hashes, and performed a bounded archive readability check. No Servo source, release archive, crate archive, generated output, native binary, or build log was copied into Turing.

Observations:

- the successful external build baseline remains `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- refreshed `origin/main` is `622600e045c2e5ea688a9b19b8671b6f43112817`, two commits ahead of the build baseline;
- the external build checkout is a shallow partial clone, so it is not full-history provenance evidence;
- GitHub commit verification reported the build baseline and current `origin/main` commits as valid;
- `v0.3.0` and `release/v0.3` point to `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`;
- `v0.3.0` is a lightweight tag and its commit was reported unsigned;
- the downloaded `servo-v0.3.0-src-vendored.tar.gz` was `364697035` bytes and matched GitHub's SHA-256 digest `C75EFFBDC0AB6F86B318E28D139EB056268224E072A684492B49409C5221C871`;
- crates.io `servo 0.4.0` was published 2026-07-16, is not yanked, and the local cached `.crate` matched checksum `01A05FFCE7829E67E41C5CB4E10849924CBD781D0EA0D6332D81AFE8476D8A89`.

Inference:

The successful build baseline, current upstream `main`, latest GitHub release source, and latest crates.io package are distinct source surfaces. None is automatically the Turing source baseline. The old "upstream release/archive comparison" gap is now narrowed, but source identity remains unresolved until an owner selects a baseline model and accepts a provenance policy.

Decision:

- add the [Servo Upstream Source Provenance - July 2026](research/servo-upstream-source-provenance-2026-07.md);
- link it from the research index, documentation index, repository map, build-readiness board, pre-build checklist, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, source inventory, source/archive audit, source bibliography, and this log;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- replace current operating gaps that said "upstream release/archive comparison" with owner-selected source baseline, equivalent provenance policy, and independent non-shallow source verification.

Security/privacy impact:

No runtime authority changed. The report clarifies that GitHub commit verification, GitHub asset digests, and crates.io checksums are source-identity inputs, not security approval. It also records that the current build checkout is shallow, which prevents overclaiming full-history provenance.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The source-baseline choice will determine which future WPT, local corpus, accessibility, and platform-surface evidence must be rerun.

Performance/memory/energy impact:

No performance claim changed. Because current `origin/main`, `v0.3.0`, and `servo 0.4.0` differ from the built baseline, any selected baseline other than the current build commit requires fresh fixed-hardware performance and memory evidence.

Licensing/operational impact:

No license or redistribution status changed. The release source archive and crates.io package checksums are evidence for later legal, source-offer, notice, advisory, SBOM, and reproducible-release review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has sharper upstream source evidence but remains blocked;
- `ADR9-EV-001` remains partial until baseline selection, equivalent provenance policy, and independent non-shallow verification are complete;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, dependency/provenance inventory, supply-chain scan, source/archive provenance audit, source bibliography, research log, and the new upstream source provenance report.

Unresolved questions:

Which source baseline model should `ADR-0009` evaluate first: the already built main-branch commit, refreshed current `origin/main`, the `v0.3.0` release source archive, the crates.io `servo 0.4.0` package surface, or no Servo source baseline?

Next evidence required:

Select or reject a source-baseline model, define signed-tag or equivalent provenance policy, perform an independent non-shallow source verification run, and rerun build/dependency/generated/native/compatibility/performance evidence if the selected baseline differs from the current external build baseline.

## 2026-07-17 — ADR-0009 evidence traceability matrix

Question:

How should the remaining Servo/source-strategy evidence be ordered and traced so a maintainer can continue `PB-002` without losing the relationship between evidence reports, owner scopes, missing outputs, and `ADR-0009` acceptance checks?

Sources and versions:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- current Servo research reports indexed in [Research Index](research/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method and environment:

Reviewed the current readiness registry, ADR packet, operating board, research index, documentation policy, dependency policy, release-operations policy, ADR list, and research program. No external source, generated output, dependency, native artifact, build log, or browser-engine code was imported.

Observations:

- `PB-002` had multiple evidence reports but no single ordered matrix showing which `ADR-0009` evidence items were captured, partial, missing, owner-review-required, or blocked;
- the remaining evidence spans source identity, independent build reproduction, Cargo SBOM/license/advisory posture, native package source-build or binary-package decisions, deterministic download verification, generated-output determinism, build-script/proc-macro side effects, unsafe/FFI review, component boundaries, JavaScript-runtime conflict, compatibility, performance, security, maintenance, public claims, and ADR owner review;
- the machine readiness registry remains the status source of truth, while the ADR packet remains the narrative source of truth.

Inference:

A traceability matrix reduces handoff risk without promoting any Servo option. It makes the remaining work auditable and prevents future continuation from treating local identity evidence as dependency approval, performance evidence, compatibility evidence, or a source-strategy decision.

Decision:

- add the [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- link it from the documentation index, research index, project-buildout index, repository map, pre-build checklist, build-readiness board, ADR-0009 packet, and readiness registry;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- keep Turing's dependency, unsafe-code, native-code, generated-code, and provenance ledgers unchanged because no Servo source or dependency entered the repository.

Security/privacy impact:

No authority or runtime security behavior changed. The matrix makes security-sensitive follow-up work explicit, especially native package review, deterministic download verification, unsafe review, FFI contracts, sandbox implications, and update/release provenance.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The matrix records local compatibility corpus, WPT/Test262 evidence, unsupported API accounting, and accessibility-sensitive component boundaries as missing before `ADR-0009`.

Performance/memory/energy impact:

No performance claim changed. The matrix records fixed-hardware startup, memory, interaction, frame pacing, energy, and process-disclosure evidence as missing before any speed, low-memory, energy, or Chrome-class inference.

Licensing/operational impact:

No license status changed. The matrix records license, notice, patent, source-offer, advisory, native source-build, binary-package exception, SBOM, maintenance, and release-manifest work as required before a Servo relationship can be accepted.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has clearer continuation evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, readiness registry, research log, and the new evidence matrix.

Unresolved questions:

Which evidence item should the owner prioritize next: upstream source/archive comparison, independent build reproduction, accepted license/advisory/SBOM decisions, native source-build decisions, clean generated-output reproduction, or component-boundary analysis?

Next evidence required:

Use the matrix order to complete `ADR9-EV-001` and `ADR9-EV-002` first, then proceed through dependency/legal/native, generated/build-script, unsafe/FFI, component-boundary, compatibility, performance, security, maintenance, and ADR owner-review evidence.

## 2026-07-17 — Servo native bootstrap provenance and source-build audit

Question:

Which native packages and toolchain inputs does Servo's Windows bootstrap path download or install, what identity and signature evidence exists for those inputs on the reference host, and what source-build or binary-package decisions remain before `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- Servo Windows bootstrap sources under `C:\ts\servo\python\servo`;
- `servo/servo-build-deps` release tag `msvc-deps`;
- downloaded upstream bootstrap assets under `C:\ts\servo-native-artifacts-msvc-deps`;
- extracted bootstrap dependency tree under `C:\ts\servo\target\dependencies`;
- external debug build output under `C:\ts\servo\target\debug`.

Method and environment:

Inspected Servo bootstrap scripts, release metadata, local asset hashes, Authenticode signatures, extracted dependency tree counts, license-like file counts, plugin-list inputs, and debug output footprint outside the Turing repository. No Servo source, generated output, build log, native binary, downloaded archive, MSI file, or package metadata was copied into Turing.

Observations:

- Servo Windows bootstrap downloads `moztools-4.0.zip` and GStreamer MSVC `1.22.8` runtime/development MSIs from `servo/servo-build-deps` release tag `msvc-deps`;
- GitHub release metadata for the relevant assets exposed `digest: null` on 2026-07-17;
- the original upstream GStreamer runtime MSI was `127258624` bytes with SHA-256 `37F9973FE5C720CE1F1602E7E599336384B9FF3E4878817987DD6B77265F17BB` and Authenticode status `NotSigned`;
- the original upstream GStreamer development MSI was `225861632` bytes with SHA-256 `2D0CF6E89CF88D94E670CD81087C002408161D1C8843C00D3F27D33CE254C523` and Authenticode status `NotSigned`;
- the original upstream `moztools-4.0.zip` was `143306382` bytes with SHA-256 `CCEB354767EF3DAD8813E63CB95ED081814225BF5FA15BFA083AA8B31A339153`;
- the two small GStreamer `.msi` files under `target\dependencies` are extracted-tree artifacts, not the original upstream downloads;
- Authenticode checks over extracted `.dll`, `.exe`, and `.msi` files found `981` unsigned files and one valid signed `vswhere.exe`;
- external debug output under `target\debug` contained `617` `.dll`, `.exe`, and `.pdb` files totaling `5223312616` bytes.

Inference:

The old "native binary provenance" gap is now too broad. Local native bootstrap identity evidence exists for the observed upstream assets and extracted dependency tree, but Turing still lacks source-build recipes or binary-package exceptions, legal/advisory/notice decisions, deterministic download verification, package minimization, final release manifests, SBOM policy, and independent-host reproduction.

Decision:

- add the [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](research/servo-native-bootstrap-provenance-audit-2026-07.md);
- correct older GStreamer MSI wording so extracted-tree MSI artifacts are not confused with original upstream downloads;
- link the audit from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, source/archive provenance audit, pre-build checklist, build-readiness board, project-buildout index, repository map, source bibliography, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo source, dependency, native artifact, generated output, or provenance attestation entered the repository.

Security/privacy impact:

The audit strengthens bootstrap artifact traceability and highlights unsigned native execution surfaces, but no runtime authority, sandbox, dependency, source code, or security claim changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Local corpus, WPT, Web IDL, accessibility, platform, media, and embedding evidence remain required.

Performance/memory/energy impact:

No performance claim changed. The native bootstrap dependency size and debug-output footprint are now explicit build, binary-size, packaging, symbol-handling, and measurement review inputs.

Licensing/operational impact:

No license status changed. GStreamer, moztools, `servo-build-deps`, MSYS2-derived tools, native DLLs, EXEs, PDBs, codec libraries, crypto libraries, notices, source-offer obligations, and redistribution still require Turing-specific legal, advisory, source-build, binary-package exception, and package-manifest review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, source/archive provenance audit, source bibliography, readiness registry, research log, and the new native bootstrap audit.

Unresolved questions:

Which native bootstrap packages can Turing rebuild from source? Which require explicit binary-package exceptions? Which codec, patent, source-offer, notice, advisory, sandbox, update, and package-minimization decisions would be required for each candidate Servo relationship?

Next evidence required:

Run native source-build or binary-package exception review, legal/advisory/notice review, deterministic bootstrap download verification design, independent-host bootstrap reproduction, final release package manifest/SBOM planning, upstream release/archive comparison, clean generated-output regeneration, component-boundary analysis, local corpus experiments, and fixed-hardware performance baseline for `ADR-0009`.

## 2026-07-17 — Servo source and archive provenance audit

Question:

Which local source identities, source archives, Cargo registry cache entries, Stylo git-source records, and native/bootstrap artifact summaries exist for the clean external Servo checkout, and what remains before `ADR-0009` can decide a source strategy?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- Stylo git source `https://github.com/servo/stylo` at `d3de91cbac7bba38e159239b3c0a360783fce2ee`;
- local Cargo registry caches under `C:\Users\bcw19\.cargo\registry`;
- Servo Windows bootstrap dependencies under `C:\ts\servo\target\dependencies`;
- local source archives under `C:\ts`.

Method and environment:

Ran Git identity, tracked-file manifest, archive hash, Cargo metadata, Cargo lockfile checksum, registry cache, Stylo checkout, and bounded native/bootstrap artifact checks outside the Turing repository. No Servo source, Stylo source, registry archive, generated output, metadata file, build log, native binary, or bootstrap artifact was copied into Turing.

Observations:

- the clean Servo checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, with `193033` tracked files and `git fsck --connectivity-only` exit `0`;
- the Servo tracked-file manifest digest was `54E852C7337C1913B72A057D5E1E354B0201D8945D14B19F36471B8E9EF72DE7`;
- the local Servo archive `C:\ts\servo-source-4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe-20260717.tar` was `931993600` bytes with SHA-256 `205530091A7E36977BBF7417F5D48D91D122137B9450985897E54C9A5D00841D`;
- the Stylo checkout was pinned to `d3de91cbac7bba38e159239b3c0a360783fce2ee`, with local archive SHA-256 `323900D70CCF149C61F187A10F47D899A977772E3CE5D7BA82FD83B0DA5D1375`;
- default and all-features registry `.crate` archives were all present, matched Servo `Cargo.lock` checksums, and had unpacked source directories;
- the Windows bootstrap dependency tree contained `19456` files and `1582709414` bytes, including `537` DLLs, `443` EXEs, `309` PDBs, and `2` extracted-tree GStreamer MSI artifacts.

Inference:

The old "source/archive digests" gap is now too broad. Local Servo, Stylo, registry-cache, and native bootstrap identity evidence exists, but it is not adoption evidence. The remaining gate is upstream release/archive comparison, independent source verification, native source-build or binary-package exceptions, legal/advisory decisions, clean generated-output regeneration, build-script/proc-macro/native review, component-boundary analysis, local compatibility and performance evidence, and owner review.

Decision:

- add the [Servo Source and Archive Provenance Audit - July 2026](research/servo-source-archive-provenance-audit-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, pre-build checklist, build-readiness board, project-buildout index, repository map, source bibliography, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo source, dependency, native artifact, generated output, or provenance attestation entered the repository.

Security/privacy impact:

The audit strengthens source and bootstrap artifact traceability, but no runtime authority, sandbox, dependency, source code, or security claim changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Local corpus, WPT, Web IDL, accessibility, platform, and embedding evidence remain required.

Performance/memory/energy impact:

No performance claim changed. The archive sizes, registry cache size, and native bootstrap footprint are now explicit build, binary-size, packaging, and measurement review inputs.

Licensing/operational impact:

No license status changed. Servo, Stylo, registry crates, generated outputs, GStreamer, moztools, native DLLs, EXEs, PDBs, and source-offer obligations still require Turing-specific legal, notice, advisory, source-build, and redistribution review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, source bibliography, readiness registry, research log, and the new provenance audit.

Unresolved questions:

Do the local Servo and Stylo archives match a selected upstream release/tag/source package? Which native bootstrap artifacts can be rebuilt from source, redistributed, minimized, sandboxed, updated, and covered by notices? Which source provenance records would be required if a selective component boundary is proposed?

Next evidence required:

Run upstream release/archive comparison, independent-source fetch verification, source-offer and notice review, native source-build policy review, clean generated-output regeneration, registry/git build-script review, component-boundary analysis, local corpus experiments, and fixed-hardware performance baseline for `ADR-0009`.

## 2026-07-17 — Servo build-script and generated-output audit

Question:

What build-script side effects and generated outputs does the clean external Servo Windows development build expose, and what remains before Turing can trust generated outputs or build-time behavior for `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- generated outputs under `C:\ts\servo\target\debug\build`;
- first-party Servo workspace `build.rs` files;
- local Cargo timing artifact `C:\ts\servo\target\cargo-timings\cargo-timing-20260717T184252676Z-d205ee0048504b27.html`.

Method and environment:

Inspected Cargo `out` directories, first-party build scripts, generator inputs, and build-script `output` logs. Hashed key generated-output directories and generator inputs. Ran one incremental no-op Servo rebuild from Visual Studio 2022 Developer Command Prompt with LLVM on `PATH`. No Servo source, generated output, metadata, build log, native binary, or timing artifact was copied into Turing.

Observations:

- the Windows debug build contained `103` Cargo `out` directories, `3955` files, and `1106039671` bytes under `target\debug\build`;
- largest output directories came from `mozjs_sys`, `mozangle`, `harfbuzz-sys`, `aws-lc-sys`, `fontsan`, `servo-script-bindings`, `glslopt`, `zstd-sys`, `libsqlite3-sys`, and `stylo`;
- first-party generated outputs included `1631` files from `servo-script-bindings`, `546` copied files from `servo-script`, `539` copied files from `servo-script-webgpu`, a generated DevTools build ID, Windows servoshell resource output, and Stylo CSS property output;
- key generator inputs included `556` Web IDL files, Python codegen, a vendored WebIDL parser, PLY, `uv.lock`, `.python-version`, `rust-toolchain.toml`, and Stylo `css-properties.json`;
- one incremental no-op rebuild exited `0`, reported `Succeeded in 0:00:03`, and kept inspected first-party generated-output directory digests unchanged;
- first-party build scripts depend on Python or `uv`, `SOURCE_DATE_EPOCH`, `OUT_DIR`, git state, target cfg, platform SDK/resource tools, `OHOS_SDK_NATIVE`, nested Cargo, and DLL/resource copying behavior;
- build-script `output` logs across all build scripts contained `41890` lines, `11685` `rerun-if-env-changed` markers, `11013` `rerun-if-changed` markers, and many warnings, dominated by registry/native-facing packages.

Inference:

Generated-output and first-party build-script evidence is now concrete enough for the ADR packet, but it is not enough for adoption. Turing still needs clean-target regeneration, independent-host comparison, accepted build-script/proc-macro side-effect policy, dynamic tracing, generated-output source/license provenance, and policy for environment-sensitive build inputs before any candidate component can enter release code.

Decision:

- add the [Servo Build-Script and Generated-Output Audit - July 2026](research/servo-build-script-generated-output-audit-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, pre-build checklist, build-readiness board, project-buildout index, repository map, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo dependency, generated output, native code, or provenance attestation entered the repository.

Security/privacy impact:

The audit identifies build-time process execution, environment-variable sensitivity, generated binding output, native build output, and DLL/resource copying surfaces that must be reviewed before adoption. No Turing runtime authority or source code changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Web IDL, WebGPU, WebGL, DOM, CSS, DevTools, and platform-generated outputs remain evidence targets for local corpus and conformance work.

Performance/memory/energy impact:

No performance claim changed. The output size and large registry/native build outputs are now explicit binary-size, build-time, memory-footprint, and packaging review targets.

Licensing/operational impact:

No license status changed. Generated outputs, generated headers, WebIDL inputs, Stylo outputs, registry/native outputs, DLLs, and toolchain-derived files still need source-to-output provenance, license, notice, and source-offer review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, readiness registry, research log, and the new audit report.

Unresolved questions:

Can the same generated outputs be reproduced from a clean target directory and on an independent host? Which registry and git build scripts execute tools, touch native packages, read environment variables, or generate files relevant to any candidate component boundary? Which generated outputs carry license or source-offer obligations?

Next evidence required:

Run clean generated-output regeneration with diff proof, independent-host comparison, accepted build-script/proc-macro side-effect policy, dynamic tracing, generated-output source/license provenance review, FFI ABI contract review, component-boundary analysis, local corpus experiments, and fixed-hardware performance baseline for `ADR-0009`.

## 2026-07-17 — Servo generated native unsafe and FFI classification

Question:

Where do generated-code, build-script, proc-macro, native-link, FFI, and unsafe-code surfaces concentrate in the clean external Servo checkout before Turing can decide `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- local default Cargo metadata file `C:\ts\servo-metadata-default.json`;
- first-party Servo `build.rs` files under `components`, `ports`, and `tests`.

Method and environment:

Ran `rg` source-shape queries for unsafe, `SAFETY:`, FFI/export/link, generated-code, Web IDL, and native-source markers while excluding `target/` and `.venv/`. Parsed Cargo metadata with Node for build-script, proc-macro, and native-link package counts. Inspected the nine first-party Servo workspace `build.rs` files. No Servo source, generated output, metadata file, or native artifact was copied into Turing.

Observations:

- unsafe queries found `2280` unsafe mentions across `241` Rust files, including `1629` unsafe-block matches, `224` unsafe functions, `104` unsafe impls, and `157` `SAFETY:` comments;
- unsafe usage concentrates in `components/script`, `components/script_bindings`, `components/webgl`, `ffi/capi`, `components/fonts`, `ports/servoshell`, `components/media`, and `components/layout`;
- FFI/export/link markers appeared `217` times across `40` Rust files, led by script runtime/bindings, `ffi/capi`, servoshell platform paths, fonts, allocator, and media;
- default metadata contained `157` packages with build scripts, `70` proc-macro packages, and `25` native-link packages;
- the nine first-party build scripts generate or copy Web IDL/script/WebGPU bindings, emit DevTools build IDs, infer production cfgs, inspect OpenHarmony SDK metadata, compile platform C/resources, and run nested `cargo cinstall` for C API tests.

Inference:

The classification turns a broad generated/unsafe/FFI concern into concrete review queues. Servo-derived or selective-component paths would need block-level unsafe inventory, generated-output provenance, build-script side-effect audit, proc-macro review, FFI ABI contracts, native source/binary provenance, and sanitizer/fuzz/Miri/C API evidence before source adoption could be considered.

Decision:

- add the [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](research/servo-generated-native-unsafe-classification-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, pre-build checklist, build-readiness board, project-buildout index, repository map, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo dependency, native code, unsafe code, generated output, or provenance attestation entered the repository.

Security/privacy impact:

The pass identifies unsafe, FFI, generated-code, build-time execution, and native-link review targets. No Turing runtime authority, dependency, source code, or release claim changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Script bindings, WebGL, WebGPU, C API, platform shell, fonts, media, and accessibility-adjacent generated code remain evidence targets for later local corpus and conformance work.

Performance/memory/energy impact:

No performance claim changed. The unsafe and native-link clusters are now explicit performance, memory, binary-size, and driver/media review targets before any adoption discussion.

Licensing/operational impact:

No license status changed. Proc macros, build scripts, generated outputs, native-link packages, C API headers/tests, Stylo-derived outputs, and downloaded native binaries still need Turing-specific provenance, license, source-offer, and source-build review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, readiness registry, research log, and the new classification report.

Unresolved questions:

Which candidate component boundary, if any, can avoid SpiderMonkey, Stylo, generated script bindings, WebGL/native driver exposure, media/native binary packages, and C API lifetime contracts? Which unsafe blocks and generated outputs are reachable in that boundary, and what sanitizer, fuzzing, Miri, C API, and conformance evidence would be required?

Next evidence required:

Run block-level unsafe review, generated-output provenance and regeneration checks, build-script side-effect audit, proc-macro expansion review, FFI ABI contract review, native source/binary provenance review, component-boundary analysis, and then local corpus/performance experiments for `ADR-0009`.

## 2026-07-17 — Servo supply-chain policy scan

Question:

Does the clean external Servo checkout pass its own advisory, license, ban, and source policy checks, and what supply-chain evidence remains before Turing can decide `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- `cargo-deny 0.19.0`;
- Servo `deny.toml`, `about.toml`, `Cargo.lock`, and the default/all-features Cargo metadata files.

Method and environment:

Ran `cargo deny check all --show-stats` against both default and all-features metadata using Servo's own `deny.toml`. Inspected `Cargo.lock` checksum posture and the unpacked Windows bootstrap dependencies under `C:\ts\servo\target\dependencies`. No Servo source, Cargo metadata, or native artifact was copied into Turing.

Observations:

- default and all-features `cargo-deny` scans both exited `0` under Servo's policy;
- default metadata had `0` advisory, license, source, or ban errors, with `11` unnecessary duplicate-skip warnings;
- all-features metadata had `0` errors and `0` warnings across advisories, bans, licenses, and sources;
- Servo's `deny.toml` ignores `12` RustSec advisories and permits a large duplicate-version skip list;
- `Cargo.lock` contains `1034` registry entries with checksums, `11` Stylo git entries pinned by revision but without Cargo checksums, and `75` path entries;
- Windows bootstrap unpacked `19456` files under `target\dependencies`, including `537` DLLs, `443` EXEs, `309` PDBs, and `2` extracted-tree GStreamer MSI artifacts;
- the extracted-tree GStreamer MSI artifacts were hashed and recorded in the scan report; follow-up native bootstrap audit records the original upstream MSI asset hashes.

Inference:

Passing Servo's own policy is useful evidence, but it is not Turing acceptance. Turing still needs its own advisory decisions, license/legal review, upstream source/archive comparison, native source-build or binary-package exceptions, generated-code review, unsafe/FFI inventory, and component-boundary analysis.

Decision:

- add the [Servo Supply-Chain Policy Scan — July 2026](research/servo-supply-chain-policy-scan-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, pre-build checklist, build-readiness board, and readiness registry;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo dependency entered the repository.

Security/privacy impact:

The scan identifies ignored advisories, native binaries, source-policy exceptions, and checksum gaps that must be reviewed before adoption. No Turing runtime authority, dependency, or source code changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The native media, platform, input, WebDriver, and accessibility-related dependency surfaces remain evidence targets.

Performance/memory/energy impact:

No performance claim changed. The native dependency footprint and duplicate-version exceptions are now explicit performance and packaging review targets.

Licensing/operational impact:

Servo's `cargo-deny` license check passed under Servo policy, but Turing-specific license text, notice, source-offer, patent, native binary, and distribution review remain required.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, dependency ledger, provenance ledger, native-code ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, readiness registry, research log, and the new supply-chain policy scan.

Unresolved questions:

Which of Servo's ignored advisories and duplicate exceptions would Turing accept, reject, patch, or avoid? Can the Windows native bootstrap surface be rebuilt from source, minimized, sandboxed, licensed, and kept current at the level required for a browser release?

Next evidence required:

Run Turing-specific legal/advisory/native provenance reviews, compare upstream source/archive artifacts against the local digest evidence, classify build scripts/proc macros/generated code/unsafe/FFI, then evaluate component boundaries and local corpus/performance evidence for `ADR-0009`.

## 2026-07-17 — Servo dependency and provenance metadata pass

Question:

What dependency and provenance shape does the clean external Servo build expose before Turing can decide `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- local metadata artifacts `C:\ts\servo-metadata-default.json`, `C:\ts\servo-metadata-all-features.json`, and `C:\ts\servo-tree-features-depth1.txt`.

Method and environment:

Ran `cargo metadata --locked --format-version 1`, `cargo metadata --locked --format-version 1 --all-features`, and `cargo tree --locked -e features --depth 1 -p servo` from the external checkout. The all-features metadata command downloaded additional optional crates into the user Cargo cache. No Servo source or generated metadata was copied into Turing.

Observations:

- default metadata contained `1069` packages: `75` Servo path packages, `983` registry packages, and `11` git packages;
- all-features metadata contained `1120` packages: `75` Servo path packages, `1034` registry packages, and `11` git packages;
- default metadata exposed `157` packages with build scripts, `70` proc-macro packages, `25` native-link packages, `58` package names with multiple versions, and no package missing both `license` and `license_file` metadata;
- the git packages all came from `https://github.com/servo/stylo` at revision `d3de91cbac7bba38e159239b3c0a360783fce2ee`;
- high-impact clusters include MozJS/SpiderMonkey and default `js_jit`, Stylo, WebRender/WebGPU/ANGLE, GStreamer/media, rustls/aws-lc/ring, SQLite, platform UI/input/accessibility crates, DevTools, and WebDriver.

Inference:

Servo adoption or selective reuse would be a significant source, dependency, license, native, generated-code, unsafe, and maintenance program. The dependency metadata makes a whole-workspace adoption path more visibly expensive and reinforces the need to evaluate component boundaries before any release-code relationship.

Decision:

- add the [Servo Dependency and Provenance Inventory — July 2026](research/servo-dependency-provenance-inventory-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, pre-build checklist, build-readiness board, and readiness registry;
- keep `PB-002` blocked and preserve the rule that no Servo-derived release code enters Turing before `ADR-0009`.

Security/privacy impact:

No new Turing dependency or source code was added. The inventory identifies native-link, build-script, proc-macro, JavaScript-runtime, crypto/TLS, media, storage, DevTools, and platform review targets that must be classified before adoption.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The report identifies Servo dependencies and feature clusters that later local WPT, corpus, UI/input, and accessibility tests must account for.

Performance/memory/energy impact:

No performance claim changed. Dependency scale, duplicate versions, JIT defaults, GPU/media stacks, and native libraries are now explicit performance and footprint review targets.

Licensing/operational impact:

Cargo metadata had no package missing both `license` and `license_file`, but this is not legal clearance. Full license text, notices, patent review, advisory scan, upstream source/archive comparison, build-script classifications, generated-code review, and maintenance ownership remain required.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, dependency ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, readiness registry, research log, and the new dependency/provenance inventory.

Unresolved questions:

Which Servo component boundaries, if any, can be studied without importing SpiderMonkey/MozJS semantics, Stylo ownership, native build complexity, or unsupported supply-chain obligations into Turing? What are the exact advisory, license, upstream source/archive comparison, generated-code, unsafe, native, WPT, corpus, and benchmark results for the candidate boundary?

Next evidence required:

Run a full SBOM/license/advisory/source-provenance pass for the exact Servo checkout and feature profile, classify build scripts/proc macros/native links/generated code/unsafe/FFI, then perform component-boundary, local corpus, fixed-hardware benchmark, and maintenance-model analysis for `ADR-0009`.

## 2026-07-17 — Build readiness operating board and Servo source inventory

Question:

What does a maintainer or agent need to continue pre-build documentation and research without confusing contained M0 work for broad implementation readiness?

Sources and versions:

- current Turing documentation, readiness, backlog, and research registries at this change;
- Servo home page, repository README, docs.rs crate page, LTS policy, WPT pass-rate page, and recent Servo project updates retrieved 2026-07-17;
- local isolated Windows preflight observations from `C:\Users\bcw19\AppData\Local\Temp\turing-adr-0009-servo-evidence\servo`;
- clean short-path Servo bootstrap and build observations from `C:\ts\servo`.

Method and environment:

Documentation and source-strategy handoff audit plus external preflights only. The pass did not import Servo source into Turing, run WPT, run benchmarks, or change implementation status. The second external preflight installed `uv`, bootstrapped Servo, and built Servo outside this repository.

Observations:

- the repository had strong canonical policy but lacked a single human continuation board that ordered `PB-*`, `WP-*`, `RQ-*`, and `ADR-*` records;
- `PB-002` remained the first blocked broad-web-engine item;
- Servo public sources show active embedding releases and a published crate surface, but also best-effort LTS language, no Servo 1.0 definition, and JavaScript-runtime coupling that conflicts with Turing's accepted Turing-owned runtime goal unless superseded by ADR.
- the external Servo workspace matched the observed public `main` commit, but `git ls-files` returned no tracked files, `git status` counted `193074` entries, and `git fsck` reported dangling objects, so the checkout was invalid for build evidence;
- during the first preflight, the host had Visual Studio Professional 2022 with queried VC tools, ATL, and Windows 11 SDK components, but `uv` was missing and `cl`/`link` were not on the normal PowerShell `PATH`;
- Servo pins Python `3.11` and Rust `1.95.0`, so the source-strategy experiment needs isolated tooling rather than Turing's M0 toolchain alone.
- a clean short-path checkout at `C:\ts\servo` later pointed at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, counted `193033` tracked files, and had no tracked-file changes after bootstrap and build;
- installing `uv 0.11.29`, using Servo's CPython `3.11.9` and Rust `1.95.0` environment, entering the Visual Studio 2022 Developer Command Prompt, and adding `C:\Program Files\LLVM\bin` for `lld-link.exe` allowed `.\mach.ps1 bootstrap` and `.\mach.ps1 build --dev -j 8` to complete;
- the Servo build produced `C:\ts\servo\target\debug\servoshell.exe`, but that build artifact does not authorize Servo-derived Turing code or any compatibility, performance, security, accessibility, or support claim.

Inference:

Handoff clarity and a dated Servo inventory reduce the risk that future work jumps from "contained M0 allowed" to broad browser implementation, or from "Servo is useful to study" to unreviewed Servo-derived release code.

Decision:

- add the [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- add the [Servo Source Strategy Inventory — July 2026](research/servo-source-strategy-inventory-2026-07.md);
- add the [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- add root `.gitattributes` for Rust and tooling line-ending stability on Windows checkouts;
- link both from the relevant indexes;
- add Servo source-strategy evidence to `PB-002` while keeping it blocked;
- record the first Windows preflight blockers and the second short-path bootstrap/build evidence in the Servo inventory, ADR-0009 packet, and build-readiness board.

Security/privacy impact:

No source or dependency was imported. The new inventory reinforces provenance, clean-room, JavaScript-runtime, sandbox, support, and public-claim gates before any Servo relationship can affect release code.

Compatibility/accessibility impact:

The inventory points to WPT and accessibility evidence that must be reproduced before compatibility or accessibility conclusions are accepted. No support matrix changes.

Performance/memory/energy impact:

Servo performance and layout observations remain external evidence leads. Turing still requires fixed-hardware, equal-workload, equal-security measurement before any performance claim.

Licensing/operational impact:

No license status changes. The next ADR packet must include license, LTS, support, maintenance, and patch-ownership evidence.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` now has dated evidence and an operating decision packet but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, or support claim changed;
- affected files and docs: `.gitattributes`, documentation index, research index, repository map, source bibliography, pre-build checklist, project-buildout index, research log, readiness registry, and the new board, inventory, and decision-packet documents.

Unresolved questions:

What exact Servo dependency graph, component boundary, SpiderMonkey implication, WPT/local-corpus result, benchmark baseline, maintenance model, and provenance record should be compared, and which components if any can be studied without conflicting with Turing-owned engine and JavaScript commitments?

Next evidence required:

Create the `ADR-0009` research branch, use the clean short-path build evidence, extract API, dependency, and source-policy inventories, analyze runtime and maintenance implications, and run a small local corpus through the planned comparison harness without copying Servo source into Turing.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## 2026-07-17 — Native UI architecture and pre-build readiness

Added the Native UI Runtime book, Slint/Vizia/Floem/GPUI evaluation, React design-lab boundary, page-surface integration plan, UI framework and budget registries, PB-001 through PB-020 readiness control, proposed ADR-0013 through ADR-0016, RQ-55 through RQ-58, repository-wide cross-references, and validation requirements. No UI framework, dependency, reference platform, performance claim, support claim, or implementation status was accepted.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## 2026-07-17 — Agent execution and production readiness

Added task-scoped agent authority, run and evidence provenance, independent-verification rules, stable-scope and platform contracts, release channels, SLO catalog, production gates, update trust roles, service dependencies, vulnerability SLA framework, secure-development crosswalk, signing separation, and human release authority. Turing remains not ready for production or stable release.

## 2026-07-17 — Servo component boundary and JavaScript conflict evidence

Question:

Which Servo package boundaries and JavaScript-runtime conflicts shape `ADR-0009` before any source-strategy decision?

Sources and versions:

- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- Turing `ADR-0004`, engine, JavaScript, security, project-buildout, and `ADR-0009` evidence records.

Method and environment:

- ran read-only `git`, `cargo metadata`, `rg`, and local summary scripts from the Windows reference host;
- computed package closures for selected Servo roots with dev-only dependency edges excluded;
- counted heuristic unsafe, FFI/export/link, MozJS/SpiderMonkey, Web IDL/binding, WebRender/GPU, and GStreamer/media markers.

Observations:

- `servoshell`, `servo`, `servo-layout`, `servo-script`, `servo-script-bindings`, `servo-net`, `servo-storage`, and `servo-media-gstreamer` closures remain large enough that no obvious package name is a small approved component boundary;
- `servo` defaults include `js_jit`, while `--no-default-features` still reaches `mozjs`, `mozjs_sys`, Stylo, and WebRender;
- `servo-layout` directly reaches `servo-script`, `servo-script-traits`, Stylo packages, and `webrender_api`;
- `servo-script` and `servo-script-bindings` concentrate MozJS/SpiderMonkey, Web IDL, unsafe, and FFI-sensitive markers.

Inference:

`ADR9-EV-011` and `ADR9-EV-012` can move from missing to partial, but no component boundary, JavaScript runtime relationship, dependency, compatibility result, performance result, or source-strategy option is approved.

Affected records:

- `docs/research/servo-component-boundary-analysis-2026-07.md`;
- `docs/blueprint-v1/machine/adr-0009-evidence.json`;
- `docs/blueprint-v1/machine/pre-build-readiness.json`;
- `docs/project-buildout/13-build-readiness-operating-board.md`;
- `docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`;
- `docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`;
- `docs/README.md`;
- `docs/research/README.md`;
- `docs/repository-map.md`.

Next evidence required:

Owner-selected source baseline and feature profile, target-specific dependency closures, in/out component lists, replacement contracts, accepted JavaScript conflict decision, local compatibility corpus, fixed-hardware performance baseline, security/sandbox implications, maintenance model, and final `ADR-0009` review.

## 2026-07-17 — Servo WPT and compatibility denominator evidence

Question:

What WPT/Test262 denominator and local corpus evidence is required before `ADR-0009` can use compatibility results?

Sources and versions:

- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- Servo WPT configuration, include rules, metadata manifests, host aliases, Python testing commands, and WPT-hosted Test262 data.

Method and environment:

- inspected `tests/wpt/` layout, `config.ini`, `include.ini`, `hosts`, `aliases`, `MANIFEST.json` files, metadata `.ini` files, WPT focus directories, and Test262 vendoring;
- used read-only `Get-ChildItem`, `rg`, and Python summary scripts;
- did not run WPT, Test262, local corpus, Servo, or comparison browsers.

Observations:

- Servo's upstream WPT source tree contains `160978` files under `tests/wpt/tests`;
- Servo's upstream WPT metadata root contains `18777` `.ini` files and a `39462596` byte `MANIFEST.json`;
- `include.ini` starts with `skip: true`, then has `116` opt-in entries and `74` skip entries;
- upstream metadata contains `154382` expected markers and `145965` fail markers, with separate WebGL and WebGPU expectation surfaces;
- WPT-hosted Test262 data is vendored from `tc39/test262` at `b66872a92487694396fb082343e08dd7cca5ddf4` and includes `53441` `.js` tests under `third_party/test262/test`.

Inference:

`ADR9-EV-013` can move from missing to partial because WPT/Test262 denominator and corpus-planning evidence now exists. No compatibility result exists, and WPT-hosted Test262 evidence does not satisfy Turing's `ADR-0004` runtime harness requirement.

Affected records:

- `docs/research/servo-local-compatibility-corpus-2026-07.md`;
- `docs/blueprint-v1/machine/adr-0009-evidence.json`;
- `docs/blueprint-v1/machine/pre-build-readiness.json`;
- `docs/project-buildout/11-pre-build-readiness-checklist.md`;
- `docs/project-buildout/13-build-readiness-operating-board.md`;
- `docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`;
- `docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`;
- `docs/README.md`;
- `docs/research/README.md`;
- `docs/repository-map.md`;
- `docs/blueprint-v1/22-research-program.md`.

Next evidence required:

Local compatibility corpus HTTPS harness, browser-run logs against the external Servo build, focused WPT subset runs for the selected `ADR-0009` option, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan for `ADR-0004`.

## 2026-07-16 — Performance, security, developer, and missing-systems research expansion

Question:

Which browser-scale domains still lacked implementation-grade research contracts after the first eight detailed books?

Sources and versions:

- Turing main at the 95-document engineering-library baseline;
- official WHATWG, W3C, RFC, TC39, WPT, platform, accessibility, reproducible-build, update-security, benchmark, and primary security sources retrieved 2026-07-16;
- existing Turing requirements, risks, work packages, benchmark schema, process capability registry, and prototype.

Method and environment:

Repository-wide architecture and documentation audit followed by deterministic generation of eleven new books, sixteen advanced performance/security/developer chapters, a dated audit, navigation, research questions, bibliography, and validator topology. No implementation, benchmark, conformance run, independent audit, or supported-feature evidence was produced.

Observations:

- network, storage, media/document, platform, accessibility, release, extension/enterprise/sync, web-platform governance, benchmark, quality, and everyday product areas required independent owners and evidence contracts;
- performance leadership requires locality, allocation, virtual-memory, IPC, startup, PGO, tail-latency, causal-trace, energy, pressure, and recovery work;
- security leadership requires native/JIT compartments, side-channel policy, capability provenance, privileged developer/extension/agent controls, trusted UI, phishing defense, update response, and independent assurance;
- developer leadership requires deterministic replay, safe local-workspace integration, automatic reduction, generated SDKs, and cross-domain causal explanations.

Decision:

- add eleven detailed books and 81 chapters;
- add sixteen advanced chapters to performance, security, and developer experience;
- publish the [expansion audit](research/performance-security-developer-expansion-audit-2026-07.md);
- add RQ-26 through RQ-40 and corresponding experiment families;
- strengthen the repository validator to require 204 Markdown documents and nineteen book indexes.

Security/privacy impact:

The research strengthens least authority, partitioning, brokered devices and sockets, native/JIT containment, update integrity, trusted UI, phishing defenses, redaction, private reporting, and explicit unsafe early-release warnings. It changes no current security claim.

Compatibility/accessibility impact:

The expansion adds open-web feature governance, full-denominator conformance, platform accessibility bridges, assistive-technology latency, browser UI workflows, and cross-browser protocol studies. It changes no support matrix.

Performance/memory/energy impact:

The expansion defines measurement and experiments for data locality, allocators, pages, IPC, scheduling, startup, PGO/LTO, GPU, 30 tabs, energy, thermal behavior, background work, and recovery. All proposed advantages remain unmeasured hypotheses.

Affected requirements, risks, ADRs, work packages, and documents:

- requirement count remains 46; risk count remains 40; work-package count remains 18;
- no ADR or status changes;
- all nineteen detailed book indexes, the documentation and Blueprint indexes, repository map, research index/log/program, bibliography, definition of done, policies, and validator are synchronized.

Next evidence required:

Run the fixed-hardware baseline, then execute the representation, process, sandbox, networking, storage, replay, accessibility, release, and product experiments defined by RQ-26 through RQ-40.

## 2026-07-16 — Detailed browser engineering research library

Question:

Where was the initial Blueprint too compressed to guide implementation research, and which detailed subsystem books were required before architecture experiments and code could proceed without inventing undocumented assumptions?

Sources and versions:

- complete Turing Blueprint and repository policies at merge commit `70f151f74a6e199415c7125169230ae1231fb561`;
- official Chromium, WebKit, Gecko, Servo, Ladybird, Rust, platform sandbox, W3C/WHATWG, WPT, BrowserBench, WebDriver BiDi, MCP, and browser-product sources retrieved 2026-07-16;
- W3C Web Platform Design Principles Group Note dated 2026-02-24;
- current MCP specification version identified as 2025-11-25 at retrieval;
- current official product/project pages recorded in the new competitive studies.

Method and environment:

Repository-wide documentation audit. The audit tested whether each major area had enough detail to define identities, inputs, outputs, ownership, lifetimes, invalidation, failure, security, accessibility, limits, observability, experiments, and acceptance evidence. No implementation, fixed-hardware benchmark, or independent security review was performed.

Observations:

- the 22 Blueprint chapters covered the correct browser-scale surface but several combined too many independently reviewable subsystems;
- implementation research needed deeper contracts for rendering, runtime, security, developer protocols, APIs, performance, agents, and comparative adoption;
- the existing documentation governance could support nested engineering books if indexes, repository mapping, research status, and validation were updated together;
- networking, storage, media, PDF, printing, native platform adapters, accessibility bridges, extensions, enterprise/sync, and release operations remain future detailed-book candidates.

Inference:

Keeping the Blueprint as the normative overview while adding indexed detailed books gives the project enough depth for experiments without prematurely freezing implementation. A large body of prose is useful only if status, ownership, evidence, and change discipline remain explicit.

Decision:

- add a [browser engine engineering book](engine/README.md);
- add a [JavaScript runtime engineering book](javascript/README.md);
- add a [browser security engineering book](security-engine/README.md);
- add a [developer experience and DevTools book](developer-experience/README.md);
- add an [API design book](api-design/README.md);
- add a [performance engineering book](performance/README.md);
- add an [AI and agent engineering book](ai/README.md);
- add [competitive browser and engine studies](competitive/README.md);
- publish the [documentation expansion audit](research/documentation-expansion-audit-2026-07.md);
- add RQ-18 through RQ-25 to the research program;
- document the repository-owner, documentation-only direct-main exception requested for the single-owner research phase;
- strengthen repository validation so the complete detailed-book topology is required.

Alternatives rejected:

- expanding only the existing Blueprint chapters, because they would become difficult to navigate and own;
- creating disconnected essays without canonical relationships, because they would drift;
- changing requirements, risks, ADRs, or work-package status based only on desk research;
- treating competitor architecture descriptions or vendor benchmarks as measured Turing evidence.

Security/privacy impact:

The new security and AI books deepen containment, platform sandbox evidence, unsafe/native governance, trusted UI, update response, semantic redaction, tool/MCP boundaries, and adversarial evaluation. They do not change the existing warning that Turing is not safe for hostile or sensitive browsing.

Compatibility/accessibility impact:

The engine, runtime, DevTools, API, competitive, and AI books reinforce standards-first development, full WPT/Test262 accounting, explicit unsupported behavior, semantic accessibility, platform assistive technology, keyboard workflows, and cross-browser automation.

Performance/memory/energy impact:

The performance and subsystem books establish representation budgets, critical-path graphs, semantic resource attribution, adaptive parallelism, cache and pressure policy, tail-latency rules, energy/startup/recovery measurement, and benchmark governance. These remain hypotheses until experiments run.

Licensing/operational impact:

The MPL-2.0 direction is unchanged. External implementations remain research and differential references. Primary sources are linked; no external source code was copied. The expansion increases maintenance load and requires future owners to refresh changing product/project information.

Affected requirements, risks, ADRs, work packages, and documents:

- no requirement, risk, ADR, or work-package status changed;
- root `README.md`;
- `AGENTS.md`;
- `docs/README.md`;
- `docs/start-here.md`;
- `docs/repository-map.md`;
- `docs/research/README.md`;
- `docs/blueprint-v1/README.md`;
- `docs/blueprint-v1/16-governance-contributing.md`;
- `docs/blueprint-v1/18-source-bibliography.md`;
- `docs/blueprint-v1/22-research-program.md`;
- `tools/validate_blueprint.py`;
- all new documents under the eight detailed book directories;
- the dated documentation audit.

Unresolved questions:

See RQ-18 through RQ-25 and each new book's evidence and risk sections. The most immediate empirical gap is the fixed-hardware cross-engine baseline.

Next evidence required:

Execute issue #14, then build the smallest engine-artifact, process-topology, platform-sandbox, protocol, runtime-tiering, and scheduling prototypes needed to falsify the proposed designs.

## 2026-07-16 — Browser engine landscape and excellence strategy

Question:

Which documented lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should guide a top-tier independent engine for developers and everyday users?

Sources and versions:

- official engine architecture and source documentation retrieved 2026-07-16;
- WebDriver BiDi Editor's Draft dated 2026-07-15;
- W3C Web Platform Design Principles Group Note dated 2026-02-24;
- Interop 2026 material published 2026-02-12;
- current WPT and BrowserBench documentation.

Method and environment:

Architecture and standards comparison only. No comparative fixed-hardware performance run was performed, so the report does not rank engines by unmeasured speed, memory, energy, security, or compatibility.

Observations:

- production engines converge on multiprocess isolation, specialized services, staged rendering, and tiered JavaScript execution;
- Chromium provides the broadest developer-protocol and compatibility reference;
- WebKit and Gecko provide additional process, broker, platform, runtime, and observability lessons;
- Servo and Ladybird are the closest independent-engine research peers;
- stable APIs, adaptive parallelism, semantic resource ownership, and standards-aligned tests are major opportunities for differentiation.

Inference:

Turing should pursue a measured synthesis rather than clone one architecture. “Number one” must be a reproducible multi-dimensional scorecard covering compatibility, latency, memory, energy, security, accessibility, stability, developer APIs, and open-source health.

Decision:

- add a permanent [research index](research/README.md);
- publish the [browser engine landscape and Turing excellence strategy](research/browser-engine-landscape-2026-07.md);
- add formal research questions for competitive architecture measurement and developer-protocol design;
- keep all recommendations exploratory until falsifiable experiments and existing decision gates are satisfied.

Security/privacy impact:

The study reinforces site isolation, capability-separated processes, brokered privileged access, authenticated developer attachment, bounded protocols, trusted UI, and data minimization.

Compatibility/accessibility impact:

The study reinforces WPT, Test262, WebDriver BiDi, Interop tracking, explicit unsupported behavior, accessibility semantics, and manual assistive-technology validation.

Performance/memory/energy impact:

The study prioritizes end-to-end user latency, adaptive parallelism, immutable/versioned artifacts, semantic resource accounting, fixed-hardware baselines, tail latency, 30-tab disclosure, and energy measurement.

Licensing/operational impact:

The MPL-2.0 decision is unchanged. The study adds open benchmark data, public protocol schemas, reproducible results, and contributor-health metrics as leadership criteria.

Affected records:

- root `README.md`;
- `docs/README.md`;
- `docs/repository-map.md`;
- `docs/blueprint-v1/README.md`;
- `docs/blueprint-v1/22-research-program.md`;
- this research log;
- the two documents under `docs/research/`.

Unresolved questions:

See the study's experiment queue and unresolved-question section.

Next evidence required:

A fixed-hardware, versioned, reproducible reference-engine baseline using equivalent workloads, security settings, process disclosure, and compatibility accounting.

## 2026-07-16 — Professional buildout gap audit

A repository-wide review found that the remaining gap was the project control plane rather than another disconnected subsystem survey. The change adds professional phase, ownership, decision, traceability, repository, build, coding, API/configuration, cross-cutting review, release, legal, data, product, documentation, sustainability, Servo, Plug-in, and embedding baselines. It changes no implementation, requirement, risk, or support status.

<!-- MARKET-STRATEGY-2026-07 -->
## 2026-07-16 — Project-browser market gap

Added the Market Strategy and Differentiation book, dated browser-market study, `OP-001` through `OP-014` registry, opportunity-promotion template, cross-document product hypotheses, and validator coverage. No opportunity became an accepted requirement, implementation claim, risk status, or support promise.

<!-- MARKET-RQ-ID-CORRECTION-2026-07 -->
## 2026-07-16 — Research-question identifier correction

Renumbered market-differentiation studies from the conflicting `RQ-45`–`RQ-50` range to `RQ-49`–`RQ-54`, preserving `RQ-45`–`RQ-48` for the professional-buildout program. Added a repository validator that requires globally unique, contiguous research-question headings. No research conclusion, requirement, risk, work package, implementation status, or support claim changed.

## 2026-07-16 — Market strategy consistency and validator hardening

After the market-strategy merge, a repository-wide audit corrected canonical table placement, added explicit product ownership, normalized release-review scope naming, and extended validation to `OP-*` IDs, reviewer-to-owner resolution, and market index invariants. No opportunity was promoted and no implementation or support status changed.

## 2026-07-15 — Canonical documentation system

Decision:

- place canonical prose under `docs/`;
- retain root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md` only for discovery and repository control;
- place the complete Blueprint under `docs/blueprint-v1/`;
- keep machine-readable requirements, risks, backlog, process capabilities, benchmark manifests, and agent-action schemas beside the Blueprint;
- require same-change documentation for code, configuration, dependencies, interfaces, features, risks, and repository structure;
- add static link, location, registry, index-coverage, and diff-based documentation validation;
- remove temporary transfer and self-modifying bootstrap machinery from the durable repository structure.

Rationale:

A browser project has too many cross-cutting security, compatibility, performance, accessibility, and operational obligations for documentation to be optional or scattered. Centralizing canonical prose and requiring impact review reduces silent drift while preserving standard GitHub discovery files.

Affected records:

- root `AGENTS.md`;
- `docs/documentation-policy.md`;
- `docs/repository-map.md`;
- `docs/contributing.md`;
- GitHub issue and pull-request templates;
- repository validation workflow and tools.

Residual risk:

Automation can verify location, links, registries, and minimum same-change behavior, but it cannot prove that prose is semantically complete. Human and agent review must still apply the full impact matrix.

## Entry template

```text
## YYYY-MM-DD — Topic

Question:
Sources and versions:
Method and environment:
Observations:
Inference:
Decision:
Alternatives rejected:
Security/privacy impact:
Compatibility/accessibility impact:
Performance/memory/energy impact:
Licensing/operational impact:
Affected requirements, risks, ADRs, work packages, and documents:
Unresolved questions:
Next evidence required:
```
