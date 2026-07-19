# Repository Map

Status: canonical repository-structure reference
Update rule: required for every file or directory addition, deletion, rename, or ownership change

## Durable top-level structure

```text
.
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── rustfmt.toml
├── clippy.toml
├── .gitattributes
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── .github/
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
│       ├── repository-validation.yml
│       └── implementation-plan-validation.yml
├── benchmarks/
│   ├── compatibility/
│   │   └── adr0009/
│   └── corpus/
├── apps/
│   └── turing-shell/
├── crates/
│   ├── turing-build-info/
│   ├── turing-ipc/
│   │   └── src/
│   │       ├── generated.rs
│   │       ├── envelope.rs
│   │       ├── queue.rs
│   │       └── sequence.rs
│   ├── turing-kernel/
│   ├── turing-types/
│   └── turing-ui-model/
├── schemas/
│   ├── ipc/
│   │   └── control-plane.json
│   └── sandbox/
│       ├── probe-catalog.json
│       └── probe-evidence.schema.json
├── docs/
│   ├── README.md
│   ├── blueprint-v1/
│   ├── research/
│   ├── project-buildout/
│   │   ├── implementation-plan/
│   │   │   ├── README.md
│   │   │   └── 01-17 execution chapters
│   │   ├── 19-github-issue-handoff.md
│   │   └── machine/
│   ├── agent-execution/
│   ├── production-readiness/
│   ├── ui-runtime/
│   ├── accessibility/
│   │   └── machine/
│   └── subsystem engineering books
├── prototype/
├── security/
│   ├── dependencies.json
│   ├── unsafe-code.json
│   ├── native-code.json
│   ├── generated-code.json
│   └── provenance.json
└── tools/
    ├── bootstrap.sh
    ├── bootstrap.ps1
    ├── doctor.sh
    ├── doctor.ps1
    ├── check.sh
    ├── check.ps1
    ├── generate_ipc.py
    ├── capture_benchmark_browser_pins.py
    ├── run_benchmark_browser_launch.py
    ├── run_benchmark_server_profile.py
    ├── run_benchmark_smoke.py
    ├── serve_benchmark_profile.py
    ├── validate_adr_0009_evidence.py
    ├── validate_benchmark_browser_pin_capture.py
    ├── validate_benchmark_browser_pin_diagnostics.py
    ├── validate_benchmark_corpus.py
    ├── validate_benchmark_competitor_local_installs.py
    ├── validate_benchmark_competitor_versions.py
    ├── validate_benchmark_os_controls.py
    ├── validate_benchmark_resource_attribution.py
    ├── validate_benchmark_network_profile.py
    ├── validate_benchmark_tab_scenarios.py
    ├── validate_benchmark_claim_bundles.py
    ├── validate_benchmark_readiness_review.py
    ├── validate_benchmark_statistics_analysis.py
    ├── validate_fresh_host_reproduction.py
    ├── validate_fresh_host_run_records.py
    ├── validate_fresh_host_readiness_review.py
    ├── validate_ui_adapter_contract.py
    ├── validate_framework_bakeoff.py
    ├── validate_ui_component_fixtures.py
    ├── validate_page_surface_composition.py
    ├── validate_window_input_accessibility_spike.py
    ├── validate_native_ui_readiness_review.py
    ├── validate_profile_session_formats.py
    ├── validate_profile_session_readiness_review.py
    ├── validate_research_package_update_lab.py
    ├── validate_research_package_update_readiness_review.py
    ├── validate_incident_patch_rehearsal.py
    ├── validate_incident_patch_readiness_review.py
    ├── validate_backup_ownership_gap.py
    ├── validate_backup_ownership_readiness_review.py
    ├── validate_contained_m0_start_state.py
    ├── validate_build_information_readiness.py
    ├── validate_implementation_plan.py
    ├── validate_github_issue_handoff.py
    ├── validate_task_approval_templates.py
    ├── validate_evidence_bundles.py
    ├── validate_ipc_capability_boundaries.py
    ├── validate_sandbox_probe_inventory.py
    ├── validate_sandbox_contracts.py
    ├── validate_servo_local_compatibility_corpus.py
    ├── validate_blueprint.py
    ├── validate_benchmark_manifests.py
    ├── validate_build_foundation.py
    ├── check_documentation_change.py
    └── xtask/
```

The detailed documentation topology is indexed by [`docs/README.md`](README.md). It is intentionally not duplicated line-for-line here.
The first human continuation stop is [`docs/project-buildout/21-build-readiness-start-guide.md`](project-buildout/21-build-readiness-start-guide.md); the first hard-stop continuation scorecard remains [`docs/project-buildout/20-build-continuation-readiness-pack.md`](project-buildout/20-build-continuation-readiness-pack.md); the ongoing continuation path is [`docs/project-buildout/13-build-readiness-operating-board.md`](project-buildout/13-build-readiness-operating-board.md); it summarizes readiness and handoff state but does not replace machine registries. The documentation-readiness proof point is [`docs/project-buildout/18-documentation-readiness-evidence-matrix.md`](project-buildout/18-documentation-readiness-evidence-matrix.md), with the checked completion audit in [`docs/research/documentation-readiness-completion-audit-2026-07.md`](research/documentation-readiness-completion-audit-2026-07.md) and [`docs/project-buildout/machine/documentation-readiness-completion-audit.json`](project-buildout/machine/documentation-readiness-completion-audit.json). The checked contained M0 session-start router is [`docs/research/contained-m0-start-state-inventory-2026-07.md`](research/contained-m0-start-state-inventory-2026-07.md), backed by [`docs/project-buildout/machine/contained-m0-start-state.json`](project-buildout/machine/contained-m0-start-state.json), [`docs/project-buildout/machine/contained-m0-start-state.schema.json`](project-buildout/machine/contained-m0-start-state.schema.json), and [`tools/validate_contained_m0_start_state.py`](../tools/validate_contained_m0_start_state.py); it is not proposed-task execution approval, `TASK-000011` acceptance, readiness promotion, all-information-ready-for-building evidence, or broad product approval. The checked build-information gap map is [`docs/research/build-information-readiness-ledger-2026-07.md`](research/build-information-readiness-ledger-2026-07.md), backed by [`docs/project-buildout/machine/build-information-readiness-ledger.json`](project-buildout/machine/build-information-readiness-ledger.json), [`docs/project-buildout/machine/build-information-readiness-ledger.schema.json`](project-buildout/machine/build-information-readiness-ledger.schema.json), and [`tools/validate_build_information_readiness.py`](../tools/validate_build_information_readiness.py); it is not all-information-ready-for-building evidence or broad-build approval. The checked implementation execution documentation is [`docs/project-buildout/implementation-plan/README.md`](project-buildout/implementation-plan/README.md), backed by [`docs/research/full-implementation-game-plan-audit-2026-07.md`](research/full-implementation-game-plan-audit-2026-07.md), implementation graph registries, and [`tools/validate_implementation_plan.py`](../tools/validate_implementation_plan.py); it is not broad implementation approval. The checked GitHub cleanup coordination snapshot is [`docs/project-buildout/19-github-issue-handoff.md`](project-buildout/19-github-issue-handoff.md), backed by [`docs/project-buildout/machine/github-issue-handoff.json`](project-buildout/machine/github-issue-handoff.json), [`docs/project-buildout/machine/github-issue-handoff.schema.json`](project-buildout/machine/github-issue-handoff.schema.json), and [`tools/validate_github_issue_handoff.py`](../tools/validate_github_issue_handoff.py); it maps issue/PR cleanup only and is not task approval, readiness promotion, live GitHub proof, implementation evidence, or a product claim. The proposed task-shaped continuation queue is [`docs/project-buildout/17-build-readiness-task-queue.md`](project-buildout/17-build-readiness-task-queue.md), backed by [`docs/blueprint-v1/machine/build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json). It is not execution approval. The active contained `WP-002` execution-task review handoff is [`docs/research/task-000011-wp002-review-handoff-2026-07.md`](research/task-000011-wp002-review-handoff-2026-07.md), and the checked no-claim evidence capture is [`docs/agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json`](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json); they map candidate `TASK-000011` evidence and gaps but are not task acceptance, an accepted independent evidence-bundle instance, `PB-011` readiness, production IPC, or a security claim. The benchmark handoff map for Chrome-class and extreme-performance preparation is [`docs/research/benchmark-engine-baseline-harness-readiness-map-2026-07.md`](research/benchmark-engine-baseline-harness-readiness-map-2026-07.md); it organizes existing no-claim `PB-013` evidence and does not provide a browser run, benchmark result, owner-reviewed readiness, or performance claim. The source-strategy evidence packet is [`docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`](project-buildout/14-adr-0009-source-strategy-decision-packet.md), the remaining evidence queue is [`docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`](project-buildout/15-adr-0009-evidence-traceability-matrix.md), the public-claim/support-impact template is [`docs/project-buildout/16-adr-0009-decision-draft.md`](project-buildout/16-adr-0009-decision-draft.md), and the checked no-claim decision handoff is [`docs/blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json`](blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json). Generated-output provenance evidence for `ADR9-EV-007` includes the first-pass [`Servo generated-output source-to-output provenance map`](research/servo-generated-output-source-provenance-map-2026-07.md), which is not legal approval or release-code authorization.

The cross-domain Chrome-class capability traceability map is [`docs/research/chrome-class-capability-traceability-map-2026-07.md`](research/chrome-class-capability-traceability-map-2026-07.md). It routes target capability domains to current owners, blockers, next proof, and prohibited claims without providing Chrome-class evidence or readiness promotion. The start-guide-driven continuation path is [`docs/project-buildout/21-build-readiness-start-guide.md`](project-buildout/21-build-readiness-start-guide.md), backed by the continuation pack in [`docs/project-buildout/20-build-continuation-readiness-pack.md`](project-buildout/20-build-continuation-readiness-pack.md) for compact hard-stop handoff.

## Root workspace

`Cargo.toml` is the canonical Rust workspace definition. `Cargo.lock` is committed. `rust-toolchain.toml` pins the M0 compiler and required components.
`.gitattributes` keeps Markdown, GitHub YAML, Rust, and repository tooling files on LF line endings across Windows checkouts so documentation diffs, workflow checks, `rustfmt`, and validation behave consistently. The repository enforces changed-range hygiene through local and CI diff checks; historical file renormalization is a separate source-control cleanup and is not implied by the policy file alone.

Workspace membership must match [`workspace-components.json`](blueprint-v1/machine/workspace-components.json). Every component record declares:

- package and path;
- owner;
- privilege;
- hostile-input exposure;
- public or internal status;
- unsafe policy;
- supported development targets;
- internal dependencies;
- failure boundary.

`tools/validate_build_foundation.py` rejects missing components, dependency cycles, manifest/registry drift, toolchain drift, generated IPC drift, unledgered unsafe/native syntax, or M0 external runtime dependencies.

## `benchmarks/`

Benchmark and compatibility fixtures live here when they are executable or served assets rather than prose. The current benchmark seed is `benchmarks/corpus/no-claim-smoke/`, containing generated local HTML fixtures for `PB-013` corpus-shape validation across static, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract shapes. The current source-strategy compatibility seed is `benchmarks/compatibility/adr0009/no-claim-tiny/`, containing generated local HTML fixtures referenced by the checked `ADR9-EV-013` no-claim local compatibility corpus manifest and HTTPS host-alias harness plan. These files are not benchmark results, browser-run results, compatibility results, accessibility results, service-worker results, media results, security evidence, or Chrome-class evidence.

## `apps/`

Application binaries live here.

`turing-shell` is currently a command-line M0 integration laboratory. It exercises toolkit-neutral shell state plus the generated process/capability/IPC policy reference. It has no native UI, web engine, operating-system IPC transport, networking, storage, Plug-in, or AI capability.

Future application directories require an accepted purpose, owner, maturity label, support boundary, and package/update implications.

## `crates/`

Production-oriented Rust libraries live here. Crates are split by authority, ownership, replacement, and failure boundary rather than convenience.

Current crates:

- `turing-types`: shared non-zero identities, including restart-safe process identities;
- `turing-build-info`: build and maturity identity;
- `turing-ipc`: generated role/message contracts, bounded envelopes, exact sequence state, and bounded queues;
- `turing-kernel`: process registration, role launch policy, capability attenuation, route authorization, and channel binding;
- `turing-ui-model`: toolkit-neutral shell state and commands.

A toolkit, platform, GPU, network, storage, serializer, or runtime dependency may not enter these crates merely to accelerate a demo.

## `schemas/`

Canonical machine-readable interface definitions live here when they generate source or cross-language contracts.

`schemas/ipc/control-plane.json` owns the M0 control-plane protocol version, stable process-role and capability IDs, default capability sets, launch authority, message IDs, role-pair routes, document-scope rules, encoded-size limits, and queue budgets.

The schema is untrusted input to the generator. `tools/generate_ipc.py` validates it before producing committed Rust and documentation outputs. Schema changes require review of compatibility, authority, resource limits, generated diffs, tests, and migration implications.

`schemas/sandbox/probe-catalog.json` and `schemas/sandbox/probe-evidence.schema.json` own the checked no-claim `WP-003` operation catalog and evidence-bundle contract for future sandbox probe packages. They are validated by `tools/validate_sandbox_contracts.py`; they do not execute probes, approve platform sandbox adapters, prove effective policy, or support sandbox-readiness, renderer-security, site-isolation, SEC-GATE, production-safety, or implementation claims.

## Generated IPC output

`tools/generate_ipc.py` deterministically generates:

- `crates/turing-ipc/src/generated.rs`;
- `docs/blueprint-v1/machine/process-capabilities.json`.

Run:

```bash
python3 -B tools/generate_ipc.py
python3 -B tools/generate_ipc.py --check
```

Generated output must not be edited directly. The source, generator, command, outputs, owner, and review boundary are registered as `GEN-IPC-001` in [`security/generated-code.json`](../security/generated-code.json).

## `prototype/`

The dependency-free architecture prototype remains a research executable. It is a reference model, not the production browser implementation.

## `docs/project-buildout/implementation-plan/`

The implementation-plan handbook is the checked execution documentation for dependency ordering, task sizing, milestone gates, interface freezes, evidence classes, handoffs, and stop/replan criteria from M0 through M9. It is backed by `implementation-*.json` records under `docs/blueprint-v1/machine/` and by `tools/validate_implementation_plan.py`.

The plan does not approve any work package, replace reviewed `TASK-*` manifests, select Servo or a UI toolkit, promote broad M1 implementation, or create preview, beta, stable, production, Chrome-class, security, compatibility, accessibility, performance, or daily-driver claims.

## `security/`

Machine-readable source and supply-chain ledgers live here.

- `dependencies.json`: exact external runtime, build, and toolchain dependencies;
- `unsafe-code.json`: every approved unsafe island;
- `native-code.json`: FFI, native libraries, platform SDKs, build scripts, and dynamic code;
- `generated-code.json`: schemas, generators, commands, ownership, deterministic-output checks, and review boundaries;
- `provenance.json`: original-source license, contribution, source, and build attestations.

These files are not prose. Governing explanation remains under `docs/`.

## `tools/`

Repository-owned tools live here.

- `bootstrap.sh` and `bootstrap.ps1`: non-installing M0 environment entry point;
- `doctor.sh` and `doctor.ps1`: read-only environment diagnostics;
- `check.sh` and `check.ps1`: complete local check;
- `capture_benchmark_browser_pins.py`: dependency-free no-claim browser-pin capture runner with a checked no-browser self-test, temp-profile/prohibited-path validation, artifact hashing, and optional future local Chrome/Edge diagnostic capture;
- `xtask`: cross-platform Rust implementation of bootstrap, doctor, and check;
- `generate_ipc.py`: deterministic control-plane schema validator and generator;
- `run_benchmark_browser_launch.py`: dependency-free no-claim browser launch-runner self-test that validates command parsing, forbidden arguments, registry references, artifact-root handling, hashed artifacts, and no-claim finalization without launching a browser;
- `run_benchmark_server_profile.py`: dependency-free no-claim benchmark server lifecycle self-test that starts the checked local profile server, validates routes, records shutdown, hashes artifacts, and launches no browser;
- `run_benchmark_smoke.py`: dependency-free no-claim benchmark smoke runner that captures static-server self-test output plus benchmark hardware, OS-control, and resource-attribution registry IDs into a hashed artifact package;
- `serve_benchmark_profile.py`: dependency-free loopback static server and no-claim self-test for benchmark network profiles;
- `validate_adr_0009_evidence.py`: dependency-free validation for the `ADR9-EV-*` source-strategy registry, evidence links, owner scopes, and matrix synchronization;
- `validate_benchmark_browser_pin_capture.py`: dependency-free validation for no-claim browser-pin capture plans, temporary-profile isolation, and no-real-profile evidence boundaries;
- `validate_benchmark_browser_pin_diagnostics.py`: dependency-free validation for no-claim Chrome/Edge browser-pin diagnostic captures, browser-reported versions, temp-profile cleanup, and unsupported-claim boundaries;
- `validate_benchmark_corpus.py`: dependency-free validation for no-claim benchmark corpus manifests, generated fixture hashes, and local-only fixture constraints;
- `validate_benchmark_competitor_local_installs.py`: dependency-free validation for current-host competitor executable/hash inventories and no-claim local-pin blockers;
- `validate_benchmark_competitor_versions.py`: dependency-free validation for release-catalog competitor-version manifests and no-claim local-pin blockers;
- `validate_benchmark_network_profile.py`: dependency-free validation for no-claim benchmark network profiles, route-to-corpus coverage, loopback DNS, cache headers, and unsupported protocol/authentication/shaping declarations;
- `validate_benchmark_tab_scenarios.py`: dependency-free validation for no-claim 30-tab mixed-state and all-live scenario manifests, lifecycle state counts, corpus references, network-profile coverage, and unsupported-claim boundaries;
- `validate_benchmark_claim_bundles.py`: dependency-free validation for no-claim benchmark public-claim bundle templates, required registry references including the checked statistics-analysis plan, evidence inputs, statistical controls, equivalence controls, denominator controls, overhead controls, expiry policy, publication controls, rejection rules, and unsupported Chrome-class/performance claim boundaries;
- `validate_benchmark_artifact_packages.py`: dependency-free validation for no-claim trace/artifact package contracts, runner-owned artifact roots, required trace classes, redaction/retention fields, required artifact classes, SHA-256 manifest records, and unsupported-claim boundaries;
- `validate_benchmark_launch_runners.py`: dependency-free validation for no-claim browser launch-runner contracts, required and forbidden arguments, stage coverage, timeout/cancellation, cache/profile, failure finalization, artifact, trace, and resource-attribution controls;
- `validate_benchmark_readiness_review.py`: dependency-free validation for checked no-claim benchmark readiness-review templates, null statistics-analysis plan scope, false readiness flags, `PB-013` evidence, `TASK-000005` scope, crosswalk coverage, rejection rules, and unsupported benchmark-ready, public-performance, Chrome-class, competitor-result, production, and implementation boundaries;
- `validate_benchmark_statistics_analysis.py`: dependency-free validation for checked no-claim benchmark statistics-analysis contracts, sample design, warmup, randomization or paired order, noise-study, uncertainty, effect-size, outlier, denominator, rejection rules, and unsupported performance-claim boundaries;
- `validate_fresh_host_reproduction.py`: dependency-free validation for no-claim fresh-host reproduction inventories, clean-host scope, source identity, bootstrap/doctor/check/xtask logs, cache and target-directory behavior, `PB-009` evidence, `TASK-000002` scope, and unsupported readiness boundaries;
- `validate_fresh_host_run_records.py`: dependency-free validation for checked no-claim fresh-host run-record templates, required host/source facts, bootstrap/doctor/check/xtask command records, retained-output hashes, cache/target-directory controls, source-tree cleanliness, failure denominator, prohibited evidence, and unsupported readiness boundaries;
- `validate_fresh_host_readiness_review.py`: dependency-free validation for checked no-claim fresh-host readiness-review templates, false readiness flags, `PB-009` evidence, `TASK-000002` scope, crosswalk coverage, rejection rules, and unsupported independent-reproduction, readiness-promotion, release-confidence, production, implementation, and Chrome-class boundaries;
- `validate_ui_adapter_contract.py`: dependency-free validation for no-claim toolkit-neutral UI adapter contract inventories, state/command/surface/accessibility/diagnostic/adapter contract areas, current M0 model invariants, denied toolkit-owned authority, `PB-003` evidence, `TASK-000006` scope, and unsupported native-shell/readiness boundaries;
- `validate_framework_bakeoff.py`: dependency-free validation for no-claim native UI framework bake-off inventories, candidate summaries, equivalent adapter scope, evidence axes, disqualifiers, `PB-004` evidence, `TASK-000006` scope, and unsupported toolkit/readiness boundaries;
- `validate_ui_component_fixtures.py`: dependency-free validation for no-claim native UI component-fixture inventories, semantic token groups, required shell surfaces, fixture axes, accessibility contracts, and authority boundaries;
- `validate_page_surface_composition.py`: dependency-free validation for no-claim page-surface composition inventories, surface contract fields, composition alternatives, `UI-GATE-7` workflow rows, failure cases, identity boundaries, `PB-005` evidence, `TASK-000006` scope, and unsupported page-surface/readiness boundaries;
- `validate_window_input_accessibility_spike.py`: dependency-free validation for no-claim window/input/accessibility workflow inventories, required workflow axes, core shell workflows, platform assistive-technology rows, evidence blockers, `PB-015` evidence, `TASK-000006` scope, and unsupported accessibility/readiness boundaries;
- `validate_native_ui_readiness_review.py`: dependency-free validation for checked no-claim native UI readiness-review templates, false readiness flags, `PB-003`/`PB-004`/`PB-005`/`PB-014`/`PB-015` evidence, `TASK-000006` scope, crosswalk coverage, rejection rules, and unsupported native-shell/readiness boundaries;
- `validate_profile_session_formats.py`: dependency-free validation for no-claim profile, Space, session, snapshot, migration, privacy, authority, data-loss, safe-failure format inventories, and checked no-claim schema-package templates;
- `validate_profile_session_readiness_review.py`: dependency-free validation for checked no-claim profile/session readiness-review templates, false readiness flags, `PB-016` evidence, `TASK-000007` scope, crosswalk coverage, rejection rules, and unsupported profile/session data-safety, migration, sync, credential, production-format, and implementation boundaries;
- `validate_research_package_update_lab.py`: dependency-free validation for no-claim research-package identity, update metadata, rollback, migration, crash-loop, privacy-event, unsupported production-boundary inventories, and checked no-claim update-lab package templates;
- `validate_research_package_update_readiness_review.py`: dependency-free validation for checked no-claim research package/update readiness-review templates, false readiness flags, `PB-017` evidence, `TASK-000009` scope, crosswalk coverage, rejection rules, and unsupported release-readiness, supported-security, production-updater, signing, stable-channel, public-distribution, and implementation boundaries;
- `validate_incident_patch_rehearsal.py`: dependency-free validation for no-claim private-intake, emergency-patch, incident-class, role, timing, escalation, secret-rotation, and authority-boundary inventories plus checked no-claim incident patch rehearsal templates;
- `validate_incident_patch_readiness_review.py`: dependency-free validation for checked no-claim incident/patch readiness-review templates, false readiness flags, `PB-018` evidence, `TASK-000010` scope, crosswalk coverage, rejection rules, and unsupported incident-response readiness, emergency patch capacity, supported-security, production-safe browsing, disclosure, stable-promotion, signing, incident-closure, and implementation boundaries;
- `validate_backup_ownership_gap.py`: dependency-free validation for checked blocked backup-ownership gap inventories, provisional owner records, null backups, CODEOWNERS routing, review-rule linkage, checked no-claim backup-owner qualification templates, and unsupported authority boundaries;
- `validate_backup_ownership_readiness_review.py`: dependency-free validation for checked no-claim backup-ownership readiness-review templates, false readiness flags, `PB-019` evidence, `TASK-000008` scope, crosswalk coverage, rejection rules, and unsupported owner-coverage, two-person-control, release-authority, signing, disclosure, legal, incident-closure, production-authority, broad-readiness, and implementation boundaries;
- `validate_task_approval_templates.py`: dependency-free validation for checked no-claim task approval templates, proposed task coverage, owner/reviewer inputs, immutable manifest controls, authority limits, evidence-bundle requirements, rejection rules, and unsupported task/readiness/product claim boundaries;
- `validate_evidence_bundles.py`: dependency-free validation for checked agent evidence-bundles, source-commit artifact hashes, task status boundaries, independent-review controls, and unsupported task/readiness/product claim boundaries;
- `validate_implementation_kickoff_review.py`: dependency-free validation for checked no-claim `PB-020` implementation kickoff inventories, unresolved readiness item status, first next actions, owner-only decisions, prohibited claims, kickoff gates, and release-authority boundaries;
- `validate_implementation_plan.py`: dependency-free validation for the implementation master plan chapters, execution graph, milestone gates, interface freezes, evidence catalog, task sequence, work-package numbering, pre-build readiness status, and production-not-ready boundary;
- `validate_github_issue_handoff.py`: dependency-free validation for offline GitHub issue/PR cleanup handoff snapshots, canonical issue number coverage, stale PR branch cleanup, issue-to-project-record mapping, and unsupported task/readiness/product claim boundaries;
- `validate_build_readiness_dependency_graph.py`: dependency-free validation for checked no-claim build-readiness dependency graphs, readiness-node status, task-node status, task dependencies, readiness-to-task edges, decision gates, `PB-020` edges, and parallel no-claim lanes;
- `validate_documentation_readiness_completion_audit.py`: dependency-free validation for checked no-claim documentation-readiness completion audits and build-readiness closure-review templates, entrypoints, stop/resume continuity, registries, research lanes, task handoff, sequencing, claim boundaries, validation, owner-only decisions, remaining blockers, false closure flags, rejection rules, and `PB-020` evidence;
- `validate_contained_m0_start_state.py`: dependency-free validation for checked no-claim contained M0 start-state records, current start classes, proposed queue task status, `TASK-000011` review-pending status, `PB-020` evidence, and unsupported task/readiness/product claim boundaries;
- `validate_build_information_readiness.py`: dependency-free validation for checked no-claim build-information readiness ledgers, information classes, missing broad-build evidence, task queue boundaries, `PB-020` evidence, and unsupported all-information-ready-for-building/product claim boundaries;
- `validate_ipc_capability_boundaries.py`: dependency-free validation for checked no-claim IPC capability boundary inventories and the IPC schema-source template, current M0 IPC/kernel/type evidence, process-capability role coverage, missing schema/transport blockers, future generator handoff fields, negative-test requirements, and unsupported production IPC boundaries;
- `validate_ipc_readiness_review.py`: dependency-free validation for checked no-claim IPC readiness-review templates, false readiness flags, `PB-011` evidence, `TASK-000003` scope, crosswalk coverage, rejection rules, and unsupported owner-review, schema-generator, wire-encoding, renderer-security, agent-security, process-isolation, site-isolation, production IPC, and implementation boundaries;
- `validate_sandbox_probe_inventory.py`: dependency-free validation for checked no-claim sandbox probe inventories and the no-claim probe-package template, role/surface coverage, platform evidence requirements, package lifecycle fields, result-record requirements, harness blockers, `PB-012` evidence, `TASK-000004` scope, and unsupported sandbox/security/readiness boundaries;
- `validate_sandbox_contracts.py`: dependency-free validation for the checked no-claim WP-003 sandbox operation catalog, evidence-bundle schema, unsandboxed-control requirement, unsupported-as-not-pass rule, application-level stub rejection, `PB-012` evidence, `TASK-000004` scope, and research-index/report links;
- `validate_sandbox_readiness_review.py`: dependency-free validation for checked no-claim sandbox readiness-review templates, false readiness flags, `PB-012` evidence, `TASK-000004` scope, crosswalk coverage, rejection rules, and unsupported sandbox-readiness, renderer-security, site-isolation, hostile-browsing, platform-containment, SEC-GATE, production-safety, and implementation boundaries;
- `validate_servo_local_compatibility_corpus.py`: dependency-free validation for the checked `ADR9-EV-013` no-claim local compatibility corpus manifest, generated fixture paths, SHA-256 hashes, byte counts, LF line endings, local-only origins and URLs, required case categories, artifact expectations, failure denominators, and unsupported compatibility/adoption claims;
- `validate_servo_local_compatibility_https_harness.py`: dependency-free validation for the checked `ADR9-EV-013` no-claim HTTPS host-alias harness plan, corpus origin coverage, SNI/SAN expectations, isolated trust-store policy, host-to-loopback alias controls, cleanup evidence requirements, browser-run record fields, and unsupported compatibility/adoption claims;
- `serve_servo_local_compatibility_corpus.py`: dependency-free HTTP/1.1 loopback route self-test for the checked `ADR9-EV-013` generated fixtures, Host-header origin mapping, fixture response hashes, shutdown behavior, and no-claim browser/WPT/Test262/HTTPS boundaries;
- `validate_blueprint.py`: documentation and program-record validation;
- `validate_benchmark_manifests.py`: dependency-free validation for benchmark manifest fixtures, no-claim claim metadata, and checked raw-artifact hashes;
- `validate_benchmark_hardware.py`: dependency-free validation for benchmark hardware and OS manifests;
- `validate_benchmark_os_controls.py`: dependency-free validation for benchmark OS, update, driver, firmware, power, display, thermal, clock, service, and unsupported-control manifests;
- `validate_benchmark_resource_attribution.py`: dependency-free validation for semantic resource owner taxonomy, metrics, shared-resource policy, collection plan, and UI/reporting contract manifests;
- `validate_build_foundation.py`: executable workspace, toolchain, generated-code, ledger, and source-policy validation;
- `check_documentation_change.py`: pull-request same-change documentation enforcement.

Tools must fail visibly, avoid hidden network access, preserve source-tree cleanliness, and document any generated output.

## Documentation

All durable prose belongs under `docs/`. Root Markdown is limited to repository discovery and agent-control files.

A new document must have an owner, status, unsupported behavior, evidence expectations, and an inbound link. Machine-readable companions use JSON under the owning `machine/` directory.

### Continuation records

Use these files to resume work without mistaking evidence for approval:

- [`docs/README.md`](README.md): documentation index and top-level navigation;
- [`docs/start-here.md`](start-here.md): scope, maturity, definitions, current implementation state, and current build-readiness state;
- [`docs/research/README.md`](research/README.md): dated research studies plus the required implementation-research lane map and build-readiness research crosswalk;
- [`docs/project-buildout/21-build-readiness-start-guide.md`](project-buildout/21-build-readiness-start-guide.md): first continuation stop, session posture reset, and in-session boundary router;
- [`docs/project-buildout/20-build-continuation-readiness-pack.md`](project-buildout/20-build-continuation-readiness-pack.md): continuation scorecard and compact hard-stop boundary summary for session startup;
- [`docs/project-buildout/13-build-readiness-operating-board.md`](project-buildout/13-build-readiness-operating-board.md): continuation board for ongoing readiness handoff and sequencing;
- [`docs/project-buildout/18-documentation-readiness-evidence-matrix.md`](project-buildout/18-documentation-readiness-evidence-matrix.md): evidence matrix for current documentation-readiness and contained-M0 continuation;
- [`docs/research/implementation-kickoff-review-inventory-2026-07.md`](research/implementation-kickoff-review-inventory-2026-07.md): checked no-claim `PB-020` stop/resume inventory across unresolved lanes, first next actions, owner-only decisions, prohibited claims, and release-authority boundaries;
- [`docs/research/build-readiness-dependency-graph-inventory-2026-07.md`](research/build-readiness-dependency-graph-inventory-2026-07.md): checked no-claim sequencing graph across unresolved `PB-*`, proposed `TASK-*`, task dependencies, decision/evidence gates, and parallel no-claim lanes;
- [`docs/research/documentation-readiness-completion-audit-2026-07.md`](research/documentation-readiness-completion-audit-2026-07.md): checked no-claim documentation-readiness completion audit and build-readiness closure-review template for contained M0 continuation only;
- [`docs/research/build-information-readiness-ledger-2026-07.md`](research/build-information-readiness-ledger-2026-07.md): checked no-claim broad-build information gap ledger for source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, backup-ownership, task-authority, and Chrome-class product evidence;
- [`docs/project-buildout/implementation-plan/README.md`](project-buildout/implementation-plan/README.md): dependency-ordered implementation execution documentation, not task approval;
- [`docs/research/full-implementation-game-plan-audit-2026-07.md`](research/full-implementation-game-plan-audit-2026-07.md): checked no-claim audit for the implementation-plan documentation and machine companions;
- [`docs/project-buildout/19-github-issue-handoff.md`](project-buildout/19-github-issue-handoff.md): checked offline issue and stale-PR cleanup snapshot, not task approval, readiness promotion, implementation proof, or live GitHub verification;
- [`docs/project-buildout/17-build-readiness-task-queue.md`](project-buildout/17-build-readiness-task-queue.md): proposed task-shaped queue, not execution approval;
- [`docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`](project-buildout/14-adr-0009-source-strategy-decision-packet.md), [`docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`](project-buildout/15-adr-0009-evidence-traceability-matrix.md), [`docs/project-buildout/16-adr-0009-decision-draft.md`](project-buildout/16-adr-0009-decision-draft.md), and checked no-claim [`ADR-0009 decision-review template`](blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json): source-strategy decision packet, evidence queue, public-claim/support-impact template, and decision-review handoff.

### Core program registries

Use these machine-readable records to find the current source of truth before changing implementation scope, requirements, risks, ownership, tasks, or process authority:

| Control area | Registry or artifact | Owning prose | Boundary |
|---|---|---|---|
| Requirements | [`requirements.json`](blueprint-v1/machine/requirements.json) | [Blueprint 21](blueprint-v1/21-product-requirements.md) | Stable `REQ-*` records only; changes must update owning requirements prose and affected tests |
| Risks | [`risks.json`](blueprint-v1/machine/risks.json) | [Blueprint 15](blueprint-v1/15-risk-register.md) | Risk tracking only; does not prove mitigation or readiness |
| Work packages | [`backlog.json`](blueprint-v1/machine/backlog.json) | [Blueprint 19](blueprint-v1/19-initial-backlog.md) | Dependency and sequencing records only; not task execution approval |
| Pre-build readiness | [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json) | [start guide](project-buildout/21-build-readiness-start-guide.md), [continuation pack](project-buildout/20-build-continuation-readiness-pack.md), [operating board](project-buildout/13-build-readiness-operating-board.md), and [pre-build checklist](project-buildout/11-pre-build-readiness-checklist.md) | `PB-GATE-0` contained/no-claim M0 authorization only; no broad M1, preview, beta, stable, Chrome-class, or production claim |
| Build-information readiness | [`build-information-readiness-ledger.json`](project-buildout/machine/build-information-readiness-ledger.json) and [`build-information-readiness-ledger.schema.json`](project-buildout/machine/build-information-readiness-ledger.schema.json) | [Build Information Readiness Ledger](research/build-information-readiness-ledger-2026-07.md) and [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md) | Gap ledger only; no all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, accessibility, task approval, or daily-driver claim |
| Implementation master plan | [`implementation-execution-graph.json`](blueprint-v1/machine/implementation-execution-graph.json), [`implementation-milestone-gates.json`](blueprint-v1/machine/implementation-milestone-gates.json), [`implementation-interface-freezes.json`](blueprint-v1/machine/implementation-interface-freezes.json), [`implementation-evidence-catalog.json`](blueprint-v1/machine/implementation-evidence-catalog.json), and [`implementation-task-sequence.json`](blueprint-v1/machine/implementation-task-sequence.json) | [Implementation master plan](project-buildout/implementation-plan/README.md) and [Full implementation game plan audit](research/full-implementation-game-plan-audit-2026-07.md) | Execution documentation only; no task approval, broad implementation readiness, preview, beta, stable, production, or release claim |
| GitHub issue handoff | [`github-issue-handoff.json`](project-buildout/machine/github-issue-handoff.json) and [`github-issue-handoff.schema.json`](project-buildout/machine/github-issue-handoff.schema.json) | [GitHub Issue Handoff](project-buildout/19-github-issue-handoff.md) | Coordination snapshot only; no task approval, readiness promotion, live GitHub proof, implementation, or product claim |
| Build-readiness task queue | [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json) | [Build readiness task queue](project-buildout/17-build-readiness-task-queue.md) | Proposed `TASK-*` handoffs only; no execution approval |
| Task approval template | [`task-approval-template.schema.json`](agent-execution/machine/task-approval-template.schema.json) and [`task-approval-templates/no-claim-task-approval-template.json`](agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json) | [Agent Execution](agent-execution/README.md) and [Build readiness task queue](project-buildout/17-build-readiness-task-queue.md) | Checked no-claim approval-manifest shape only; no task approval, running task, accepted task, readiness promotion, release authority, production authority, or product claim |
| Process capabilities | [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json) | [System architecture](blueprint-v1/04-system-architecture.md) and [security](blueprint-v1/08-security-and-sandbox.md) | Deny-by-default role policy draft; no platform sandbox proof |
| IPC capability boundary inventory | [`ipc-capability-boundary.json`](blueprint-v1/machine/ipc-capability-boundary.json), [`ipc-capability-boundary.schema.json`](blueprint-v1/machine/ipc-capability-boundary.schema.json), [`ipc-schema-source.schema.json`](blueprint-v1/machine/ipc-schema-source.schema.json), checked no-claim [IPC schema-source template](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), [`ipc-readiness-review.schema.json`](blueprint-v1/machine/ipc-readiness-review.schema.json), checked no-claim [IPC readiness-review template](blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json), and checked no-claim [`TASK-000011` evidence capture](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json) | [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md), [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md), [System architecture](blueprint-v1/04-system-architecture.md), and [security](blueprint-v1/08-security-and-sandbox.md) | Checked `PB-011` planning, review-handoff, and non-accepting evidence-capture records only; no accepted `TASK-000011`, accepted independent evidence-bundle instance, approved generator source for production use, wire encoding decision, owner-reviewed IPC readiness, renderer-security claim, agent-security claim, process-isolation readiness, site-isolation claim, timeout/cancellation implementation, production IPC, or implementation claim |
| Sandbox probe inventory | [`sandbox-probe-inventory.json`](security-engine/machine/sandbox-probe-inventory.json), [`sandbox-probe-inventory.schema.json`](security-engine/machine/sandbox-probe-inventory.schema.json), [`sandbox-probe-package.schema.json`](security-engine/machine/sandbox-probe-package.schema.json), checked no-claim [probe-package template](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), [`sandbox-readiness-review.schema.json`](security-engine/machine/sandbox-readiness-review.schema.json), and checked no-claim [sandbox readiness-review template](security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json) | [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md), [security](blueprint-v1/08-security-and-sandbox.md), and [security-engine sandbox brokers](security-engine/02-sandbox-brokers-and-platform-containment.md) | Checked `PB-012` planning evidence, package handoff shape, and readiness-review template only; no packaged probes, effective platform policy, owner-reviewed sandbox readiness, sandbox-readiness claim, renderer-security claim, site-isolation claim, hostile-browsing safety claim, SEC-GATE evidence, production-safety claim, or implementation claim |
| WP-003 sandbox probe contract | [`probe-catalog.json`](../schemas/sandbox/probe-catalog.json) and [`probe-evidence.schema.json`](../schemas/sandbox/probe-evidence.schema.json) | [WP-003 Sandbox Probe Contract](research/wp-003-sandbox-probe-plan-2026-07.md), [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md), and [security-engine sandbox brokers](security-engine/02-sandbox-brokers-and-platform-containment.md) | Checked `PB-012` operation/evidence contract only; no executable probes, effective platform policy, owner-reviewed sandbox readiness, sandbox-readiness, renderer-security, site-isolation, SEC-GATE, production-safety, or implementation claim |
| Window/input/accessibility spike | [`window-input-accessibility-spike.json`](accessibility/machine/window-input-accessibility-spike.json) and [`window-input-accessibility-spike.schema.json`](accessibility/machine/window-input-accessibility-spike.schema.json) | [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md), [accessibility testing](accessibility/07-testing-assistive-technology-matrices-and-release-gates.md), and [Native UI Runtime](ui-runtime/README.md) | Checked `PB-015` planning evidence only; no reference-platform workflow run, manual assistive-technology coverage, screen-reader coverage, page-tree proof, IME correctness, fault evidence, accessibility readiness, or release-path UI approval |
| Workspace and toolchains | [`workspace-components.json`](blueprint-v1/machine/workspace-components.json) and [`toolchains.json`](blueprint-v1/machine/toolchains.json) | [Prototype](prototype.md), [repository map](repository-map.md), and [M0 build foundation](research/m0-build-foundation-2026-07.md) | M0 build foundation only; no product platform or release support claim |
| Professional control plane | [`professional-owners.json`](blueprint-v1/machine/professional-owners.json), [`professional-traceability.json`](blueprint-v1/machine/professional-traceability.json), [`professional-phase-gates.json`](blueprint-v1/machine/professional-phase-gates.json), [`professional-review-rules.json`](blueprint-v1/machine/professional-review-rules.json), and [`professional-exceptions.json`](blueprint-v1/machine/professional-exceptions.json) | [Project-buildout handbook](project-buildout/README.md), checked [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md), checked no-claim [backup-owner qualification template](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json), and checked no-claim [backup-ownership readiness-review template](project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json) | Provisional research-phase controls; missing backups keep `PB-019` blocked |
| Agent action schema | [`agent-action.schema.json`](blueprint-v1/machine/agent-action.schema.json) | [AI platform](blueprint-v1/10-ai-agent-platform.md), [AI engineering](ai/README.md), and [API design](api-design/README.md) | Schema control only; no agent authority or provider approval |

### Machine evidence registries

| Evidence area | Registry or artifact | Validator or runner | Boundary |
|---|---|---|---|
| `ADR-0009` source strategy | [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json), checked no-claim [`decision-review template`](blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json), and [`adr-0009-decision-review.schema.json`](blueprint-v1/machine/adr-0009-decision-review.schema.json) | [`validate_adr_0009_evidence.py`](../tools/validate_adr_0009_evidence.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Source evidence and decision-review template only; no source-strategy decision, source baseline, source import, component approval, release-code authorization, or PB-002 readiness promotion |
| `ADR9-EV-013` local compatibility corpus | [`servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json), [`servo-local-compatibility-corpus.schema.json`](blueprint-v1/machine/servo-local-compatibility-corpus.schema.json), [`servo-local-compatibility-https-harness.schema.json`](blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json), [`servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json`](blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json), and `benchmarks/compatibility/adr0009/no-claim-tiny/` | [`validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py), [`validate_servo_local_compatibility_https_harness.py`](../tools/validate_servo_local_compatibility_https_harness.py), [`serve_servo_local_compatibility_corpus.py`](../tools/serve_servo_local_compatibility_corpus.py), and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked source-strategy corpus manifest, generated fixtures, HTTP route self-test, and HTTPS host-alias plan only; no HTTPS/browser execution, WPT/Test262 result, compatibility claim, Servo adoption, or release-code authorization |
| Research readiness crosswalk | [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json) and [`research-readiness-crosswalk.schema.json`](blueprint-v1/machine/research-readiness-crosswalk.schema.json) | [`validate_blueprint.py`](../tools/validate_blueprint.py) | Maps current `RQ-*`, `PB-*`, and `TASK-*` links only; no task approval or readiness promotion |
| Fresh-host reproduction | [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json), [`fresh-host-reproduction.schema.json`](project-buildout/machine/fresh-host-reproduction.schema.json), [`fresh-host-run-record.schema.json`](project-buildout/machine/fresh-host-run-record.schema.json), checked no-claim [`fresh-host-runs/no-claim-run-record-template.json`](project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json), [`fresh-host-readiness-review.schema.json`](project-buildout/machine/fresh-host-readiness-review.schema.json), and checked no-claim [`fresh-host readiness-review template`](project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json) | [`validate_fresh_host_reproduction.py`](../tools/validate_fresh_host_reproduction.py), [`validate_fresh_host_run_records.py`](../tools/validate_fresh_host_run_records.py), [`validate_fresh_host_readiness_review.py`](../tools/validate_fresh_host_readiness_review.py), and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-009` planning inventory, run-record template, and readiness-review template only; no independent fresh-host run, owner-approved clean-VM equivalent, owner-reviewed fresh-host readiness, readiness promotion, release confidence, production readiness, implementation, or Chrome-class claim |
| IPC capability boundary | [`ipc-capability-boundary.json`](blueprint-v1/machine/ipc-capability-boundary.json), [`ipc-capability-boundary.schema.json`](blueprint-v1/machine/ipc-capability-boundary.schema.json), [`ipc-schema-source.schema.json`](blueprint-v1/machine/ipc-schema-source.schema.json), checked no-claim [IPC schema-source template](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json), [`ipc-readiness-review.schema.json`](blueprint-v1/machine/ipc-readiness-review.schema.json), checked no-claim [IPC readiness-review template](blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json), and checked no-claim [`TASK-000011` evidence capture](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json) | [`validate_evidence_bundles.py`](../tools/validate_evidence_bundles.py), [`validate_ipc_capability_boundaries.py`](../tools/validate_ipc_capability_boundaries.py), [`validate_ipc_readiness_review.py`](../tools/validate_ipc_readiness_review.py), and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-011` no-claim boundary inventory, schema-source template, readiness-review template, `TASK-000011` review handoff, and non-accepting evidence capture only; no accepted task, accepted independent evidence-bundle instance, wire encoding, owner-reviewed IPC readiness, process-isolation proof, site-isolation proof, timeout/cancellation implementation, production IPC, or implementation claim |
| Sandbox probe inventory | [`sandbox-probe-inventory.json`](security-engine/machine/sandbox-probe-inventory.json), [`sandbox-probe-inventory.schema.json`](security-engine/machine/sandbox-probe-inventory.schema.json), [`sandbox-probe-package.schema.json`](security-engine/machine/sandbox-probe-package.schema.json), checked no-claim [probe-package template](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), [`sandbox-readiness-review.schema.json`](security-engine/machine/sandbox-readiness-review.schema.json), and checked no-claim [sandbox readiness-review template](security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json) | [`validate_sandbox_probe_inventory.py`](../tools/validate_sandbox_probe_inventory.py), [`validate_sandbox_readiness_review.py`](../tools/validate_sandbox_readiness_review.py), and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-012` no-claim inventory, package template, and readiness-review template only; no packaged expected-deny probes beyond the template, effective platform policy, owner-reviewed sandbox readiness, sandbox readiness, renderer security, site isolation, hostile-browsing safety, SEC-GATE, production-safety, or implementation claim |
| WP-003 sandbox probe contract | [`probe-catalog.json`](../schemas/sandbox/probe-catalog.json) and [`probe-evidence.schema.json`](../schemas/sandbox/probe-evidence.schema.json) | [`validate_sandbox_contracts.py`](../tools/validate_sandbox_contracts.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-012` no-claim operation catalog and evidence schema only; no packaged execution, effective policy capture, platform containment, owner-reviewed sandbox readiness, SEC-GATE, production-safety, or implementation claim |
| Window/input/accessibility spike | [`window-input-accessibility-spike.json`](accessibility/machine/window-input-accessibility-spike.json) and [`window-input-accessibility-spike.schema.json`](accessibility/machine/window-input-accessibility-spike.schema.json) | [`validate_window_input_accessibility_spike.py`](../tools/validate_window_input_accessibility_spike.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-015` no-claim workflow inventory only; no reference-platform workflow execution, manual assistive-technology transcript, screen-reader coverage, page-tree proof, IME correctness, crash/GPU-loss proof, accessibility readiness, UI-GATE evidence, or release-path UI approval |
| Benchmark manifests and raw-artifact index | [`benchmark-manifests/no-claim-runner-smoke.sample.json`](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json) | [`validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py) | No benchmark result or public claim |
| Benchmark hardware | [`benchmark-hardware/current-windows-high-end.candidate.json`](blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json) | [`validate_benchmark_hardware.py`](../tools/validate_benchmark_hardware.py) | Candidate current-host evidence only |
| Benchmark OS controls | [`benchmark-os-controls/current-windows-high-end.candidate.json`](blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json) | [`validate_benchmark_os_controls.py`](../tools/validate_benchmark_os_controls.py) | No clean lab image or freeze approval |
| Resource attribution | [`benchmark-resource-attribution/semantic-owners.v1.json`](blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json) | [`validate_benchmark_resource_attribution.py`](../tools/validate_benchmark_resource_attribution.py) | Taxonomy only; no instrumentation result |
| Competitor versions | [`benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json`](blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json) | [`validate_benchmark_competitor_versions.py`](../tools/validate_benchmark_competitor_versions.py) | Release-catalog candidates only |
| Competitor local installs | [`benchmark-competitor-local-installs/current-windows-high-end.candidate.json`](blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json) | [`validate_benchmark_competitor_local_installs.py`](../tools/validate_benchmark_competitor_local_installs.py) | Current-host executable/hash evidence only |
| Browser-pin capture plan | [`benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json`](blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json) | [`validate_benchmark_browser_pin_capture.py`](../tools/validate_benchmark_browser_pin_capture.py) and [`capture_benchmark_browser_pins.py --self-test`](../tools/capture_benchmark_browser_pins.py) | No real-profile access and no benchmark-ready pins |
| Browser-pin diagnostics | [`benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json`](blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json) | [`validate_benchmark_browser_pin_diagnostics.py`](../tools/validate_benchmark_browser_pin_diagnostics.py) | Current-host no-claim Chrome/Edge diagnostic only |
| Benchmark corpus | [`benchmark-corpora/no-claim-smoke.corpus.json`](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json) plus `benchmarks/corpus/` fixtures | [`validate_benchmark_corpus.py`](../tools/validate_benchmark_corpus.py) | Expanded generated local fixtures only; no reviewed representative corpus |
| Benchmark network profile and smoke package | [`benchmark-network-profiles/no-claim-local-static.profile.json`](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json) | [`validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py), [`serve_benchmark_profile.py --self-test`](../tools/serve_benchmark_profile.py), [`run_benchmark_server_profile.py --self-test`](../tools/run_benchmark_server_profile.py), and [`run_benchmark_smoke.py --self-test`](../tools/run_benchmark_smoke.py) | Loopback/no-claim server lifecycle and smoke evidence only; no browser-run server evidence or performance claim |
| Benchmark 30-tab scenarios | [`benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json`](blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json) | [`validate_benchmark_tab_scenarios.py`](../tools/validate_benchmark_tab_scenarios.py) | Scenario-shape evidence only; no browser run or memory result |
| Benchmark trace/artifact packages | [`benchmark-artifact-packages/no-claim-trace-package.plan.json`](blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json) | [`validate_benchmark_artifact_packages.py`](../tools/validate_benchmark_artifact_packages.py) | Package-contract evidence only; no captured trace, raw sample, memory result, energy result, or performance claim |
| Benchmark browser launch runners | [`benchmark-launch-runners/no-claim-browser-launch.plan.json`](blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json) | [`validate_benchmark_launch_runners.py`](../tools/validate_benchmark_launch_runners.py) and [`run_benchmark_browser_launch.py --self-test`](../tools/run_benchmark_browser_launch.py) | Launch-runner contract and no-browser self-test evidence only; no browser launch, raw sample, competitor result, or performance claim |
| Benchmark statistics analysis | [`benchmark-statistics-analysis.schema.json`](blueprint-v1/machine/benchmark-statistics-analysis.schema.json) and [`benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json`](blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json) | [`validate_benchmark_statistics_analysis.py`](../tools/validate_benchmark_statistics_analysis.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB13-EV-006` no-claim analysis contract only; no raw samples, confidence intervals from measured browser data, benchmark result, competitor result, Chrome-class claim, public performance claim, production claim, or implementation claim |
| Benchmark claim bundles | [`benchmark-claim-bundle.schema.json`](blueprint-v1/machine/benchmark-claim-bundle.schema.json) and [`benchmark-claim-bundles/no-claim-public-claim-template.json`](blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json) | [`validate_benchmark_claim_bundles.py`](../tools/validate_benchmark_claim_bundles.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked Level 3 public-claim bundle template only with checked `statistics_analysis_plan_id`; no browser run, benchmark result, competitor result, raw sample, trace package, Chrome-class claim, faster/lower-memory/lower-energy claim, or public performance claim |
| Benchmark readiness-review template | [`benchmark-readiness-review.schema.json`](blueprint-v1/machine/benchmark-readiness-review.schema.json) and checked no-claim [`benchmark readiness-review template`](blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json) | [`validate_benchmark_readiness_review.py`](../tools/validate_benchmark_readiness_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-013` review shape only with null `statistics_analysis_plan` scope; no owner-reviewed benchmark readiness, approved hardware tiers, clean OS controls, reviewed representative corpus, browser-run server evidence, implemented browser launch runner, raw samples, trace package, benchmark-ready browser pins, statistics, owner-reviewed claim bundle, benchmark-ready status, Chrome-class claim, faster/lower-memory/lower-energy claim, public performance claim, competitor-result claim, production claim, or implementation claim |
| UI adapter contract | [`adapter-contract-inventory.json`](ui-runtime/machine/adapter-contract-inventory.json) and [`adapter-contract-inventory.schema.json`](ui-runtime/machine/adapter-contract-inventory.schema.json) | [`validate_ui_adapter_contract.py`](../tools/validate_ui_adapter_contract.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-003` planning inventory only; no `ADR-0013`, native adapter prototype, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production claim, or implementation claim |
| Native UI framework bake-off | [`framework-bakeoff-inventory.json`](ui-runtime/machine/framework-bakeoff-inventory.json) and [`framework-bakeoff-inventory.schema.json`](ui-runtime/machine/framework-bakeoff-inventory.schema.json) | [`validate_framework_bakeoff.py`](../tools/validate_framework_bakeoff.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-004` planning inventory only; no `ADR-0014`, toolkit selection, equivalent adapter evidence, accessibility readiness, IME/keyboard proof, page-surface approval, license/provenance approval, trusted-chrome readiness, or release-path UI approval |
| UI component fixtures | [`component-fixture-inventory.json`](ui-runtime/machine/component-fixture-inventory.json) and [`component-fixture-inventory.schema.json`](ui-runtime/machine/component-fixture-inventory.schema.json) | [`validate_ui_component_fixtures.py`](../tools/validate_ui_component_fixtures.py) | Checked `PB-014` planning inventory only; no rendered fixture, toolkit selection, accessibility readiness, trusted-chrome readiness, or release-path UI approval |
| Page-surface composition | [`page-surface-composition.json`](ui-runtime/machine/page-surface-composition.json) and [`page-surface-composition.schema.json`](ui-runtime/machine/page-surface-composition.schema.json) | [`validate_page_surface_composition.py`](../tools/validate_page_surface_composition.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-005` planning inventory only; no `UI-GATE-7`, typed handle implementation, brokered handle proof, renderer-texture composition proof, compositor ownership decision, toolkit selection, page-surface approval, software fallback, latency/frame-pacing proof, or release-path UI approval |
| Native UI readiness-review template | [`native-ui-readiness-review.schema.json`](ui-runtime/machine/native-ui-readiness-review.schema.json) and checked no-claim [`native UI readiness-review template`](ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json) | [`validate_native_ui_readiness_review.py`](../tools/validate_native_ui_readiness_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked cross-lane `PB-003`/`PB-004`/`PB-005`/`PB-014`/`PB-015` review shape only; no owner review, `ADR-0013`, `ADR-0014`, `ADR-0016`, `UI-GATE-7`, `UI-GATE-10`, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production claim, or implementation claim |
| Profile/session formats | [`profile-session-format-inventory.json`](storage/machine/profile-session-format-inventory.json), [`profile-session-format-inventory.schema.json`](storage/machine/profile-session-format-inventory.schema.json), checked no-claim [`schema-package template`](storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json), and [`profile-session-schema-package.schema.json`](storage/machine/profile-session-schema-package.schema.json) | [`validate_profile_session_formats.py`](../tools/validate_profile_session_formats.py) | Checked `PB-016` planning inventory and schema-package template only; no executable schemas beyond the template, profile implementation, real-profile migration, sync, credential storage, user-data handling readiness, data-loss safety, production profile format, or implementation claim |
| Profile/session readiness-review template | [`profile-session-readiness-review.schema.json`](storage/machine/profile-session-readiness-review.schema.json) and checked no-claim [`profile/session readiness-review template`](storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json) | [`validate_profile_session_readiness_review.py`](../tools/validate_profile_session_readiness_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-016` review shape only; no owner review, privacy review, executable profile/Space/session/snapshot/migration schemas, migration tests, fault tests, real-profile fixture approval, private-session readiness, protected-work readiness, data-loss safety, user-data handling readiness, production profile-format approval, sync support, credential-storage support, release-path approval, or implementation claim |
| Research package/update lab | [`research-package-update-lab.json`](release-operations/machine/research-package-update-lab.json), [`research-package-update-lab.schema.json`](release-operations/machine/research-package-update-lab.schema.json), checked no-claim [`update-lab package template`](release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json), and [`research-package-update-lab-package.schema.json`](release-operations/machine/research-package-update-lab-package.schema.json) | [`validate_research_package_update_lab.py`](../tools/validate_research_package_update_lab.py) | Checked `PB-017` planning inventory and lab-package template only; no executable package manifest or update metadata parser beyond the template, production signing keys, offline root keys, stable channel, real updater, public binary distribution, rollback safety, migration safety, release readiness, supported security, or production updater claim |
| Research package/update readiness-review template | [`research-package-update-readiness-review.schema.json`](release-operations/machine/research-package-update-readiness-review.schema.json) and checked no-claim [`research package/update readiness-review template`](release-operations/machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json) | [`validate_research_package_update_readiness_review.py`](../tools/validate_research_package_update_readiness_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-017` review shape only; no owner review, release-operations review, security review, privacy review, executable package manifest, update metadata parser, signature threshold tests, staged install tests, tamper/replay tests, rollback/migration tests, production-key separation review, release readiness, supported security, production updater, stable channel, public distribution, signing readiness, or implementation claim |
| Incident patch rehearsal | [`incident-patch-rehearsal.json`](security-engine/machine/incident-patch-rehearsal.json), [`incident-patch-rehearsal.schema.json`](security-engine/machine/incident-patch-rehearsal.schema.json), checked no-claim [`incident patch rehearsal template`](security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), and [`incident-patch-rehearsal-record.schema.json`](security-engine/machine/incident-patch-rehearsal-record.schema.json) | [`validate_incident_patch_rehearsal.py`](../tools/validate_incident_patch_rehearsal.py) | Checked `PB-018` planning inventory and rehearsal-record template only; no executed tabletop beyond the template, incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, incident closure authority, signing authority, stable promotion, or production-safe browsing claim |
| Incident/patch readiness-review template | [`incident-patch-readiness-review.schema.json`](security-engine/machine/incident-patch-readiness-review.schema.json) and checked no-claim [`incident/patch readiness-review template`](security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json) | [`validate_incident_patch_readiness_review.py`](../tools/validate_incident_patch_readiness_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-018` review shape only; no owner review, security review, release-operations review, legal review, support review, executed private-intake tabletop, emergency patch dry run, regression/backport evidence, signing/update dry-run evidence, disclosure rehearsal, postmortem, role matrix review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported security versions, production-safe browsing, disclosure authority, stable promotion, signing authority, incident closure authority, or implementation claim |
| Backup ownership gap | [`backup-ownership-gap.json`](project-buildout/machine/backup-ownership-gap.json), [`backup-ownership-gap.schema.json`](project-buildout/machine/backup-ownership-gap.schema.json), checked no-claim [`backup-owner qualification template`](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json), and [`backup-owner-qualification-record.schema.json`](project-buildout/machine/backup-owner-qualification-record.schema.json) | [`validate_backup_ownership_gap.py`](../tools/validate_backup_ownership_gap.py) | Checked blocked `PB-019` gap inventory and qualification template only; no named qualified backups beyond the template, two-person control, owner coverage, release authority, signing authority, security-disclosure authority, legal approval, incident closure, or production authority claim |
| Backup-ownership readiness-review template | [`backup-ownership-readiness-review.schema.json`](project-buildout/machine/backup-ownership-readiness-review.schema.json) and checked no-claim [`backup-ownership readiness-review template`](project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json) | [`validate_backup_ownership_readiness_review.py`](../tools/validate_backup_ownership_readiness_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-019` review shape only; no owner-reviewed backup ownership readiness, named qualified backups, owner coverage, two-person control, release authority, signing authority, security-disclosure authority, legal approval, incident closure authority, production authority, broad readiness, or implementation claim |
| Implementation kickoff review | [`implementation-kickoff-review.json`](project-buildout/machine/implementation-kickoff-review.json) and [`implementation-kickoff-review.schema.json`](project-buildout/machine/implementation-kickoff-review.schema.json) | [`validate_implementation_kickoff_review.py`](../tools/validate_implementation_kickoff_review.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-020` no-claim stop/resume inventory only; no task approval, readiness promotion, M1 expansion, preview, beta, stable, production, Chrome-class, performance, compatibility, security, accessibility, release, or daily-driver claim |
| Build-readiness dependency graph | [`build-readiness-dependency-graph.json`](project-buildout/machine/build-readiness-dependency-graph.json) and [`build-readiness-dependency-graph.schema.json`](project-buildout/machine/build-readiness-dependency-graph.schema.json) | [`validate_build_readiness_dependency_graph.py`](../tools/validate_build_readiness_dependency_graph.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-020` no-claim sequencing graph only; no task approval, dependency change approval, readiness promotion, M1 expansion, preview, beta, stable, production, Chrome-class, performance, compatibility, security, accessibility, release, or daily-driver claim |
| Documentation-readiness completion audit | [`documentation-readiness-completion-audit.json`](project-buildout/machine/documentation-readiness-completion-audit.json), [`documentation-readiness-completion-audit.schema.json`](project-buildout/machine/documentation-readiness-completion-audit.schema.json), checked no-claim [`build-readiness closure-review template`](project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json), and [`build-readiness-closure-review.schema.json`](project-buildout/machine/build-readiness-closure-review.schema.json) | [`validate_documentation_readiness_completion_audit.py`](../tools/validate_documentation_readiness_completion_audit.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-020` no-claim completion audit and closure-review template only; documentation is organized for contained M0 continuation but not complete for all-information-ready-for-building, M1 expansion, Chrome-class, production, release, performance, compatibility, security, accessibility, or daily-driver claims |
| Contained M0 start state | [`contained-m0-start-state.json`](project-buildout/machine/contained-m0-start-state.json) and [`contained-m0-start-state.schema.json`](project-buildout/machine/contained-m0-start-state.schema.json) | [`validate_contained_m0_start_state.py`](../tools/validate_contained_m0_start_state.py) | Checked `PB-020` no-claim session-start router only; no proposed-task execution approval, `TASK-000011` acceptance, readiness promotion, all-information-ready-for-building evidence, broad M1, Chrome-class, production, release, performance, compatibility, security, accessibility, or daily-driver claim |
| Build-information readiness ledger | [`build-information-readiness-ledger.json`](project-buildout/machine/build-information-readiness-ledger.json) and [`build-information-readiness-ledger.schema.json`](project-buildout/machine/build-information-readiness-ledger.schema.json) | [`validate_build_information_readiness.py`](../tools/validate_build_information_readiness.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked `PB-020` no-claim information gap ledger only; no complete documentation, all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, accessibility, task approval, or daily-driver claim |
| Implementation master plan | [`implementation-execution-graph.json`](blueprint-v1/machine/implementation-execution-graph.json), [`implementation-milestone-gates.json`](blueprint-v1/machine/implementation-milestone-gates.json), [`implementation-interface-freezes.json`](blueprint-v1/machine/implementation-interface-freezes.json), [`implementation-evidence-catalog.json`](blueprint-v1/machine/implementation-evidence-catalog.json), and [`implementation-task-sequence.json`](blueprint-v1/machine/implementation-task-sequence.json) | [`validate_implementation_plan.py`](../tools/validate_implementation_plan.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked execution-documentation only; no work-package approval, task approval, broad implementation readiness, preview, beta, stable, production, release, or product-readiness claim |
| GitHub issue handoff | [`github-issue-handoff.json`](project-buildout/machine/github-issue-handoff.json) and [`github-issue-handoff.schema.json`](project-buildout/machine/github-issue-handoff.schema.json) | [`validate_github_issue_handoff.py`](../tools/validate_github_issue_handoff.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked offline cleanup snapshot only; does not contact GitHub, approve tasks, close backlog, promote readiness, or prove implementation/product claims |
| Task approval template | [`task-approval-template.schema.json`](agent-execution/machine/task-approval-template.schema.json) and [`task-approval-templates/no-claim-task-approval-template.json`](agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json) | [`validate_task_approval_templates.py`](../tools/validate_task_approval_templates.py) and [`validate_blueprint.py`](../tools/validate_blueprint.py) | Checked owner/reviewer, authority, evidence-bundle, rollback, expiry, and rejection template only; no proposed task is approved, running, accepted, release-gated, or product-ready |
| Evidence bundle records | [`evidence-bundle.schema.json`](agent-execution/machine/evidence-bundle.schema.json), [`evidence-bundles/TASK-000011.no-claim.2026-07-18.json`](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json), and [`TASK-000011`](agent-execution/machine/tasks/TASK-000011.json) | [`validate_evidence_bundles.py`](../tools/validate_evidence_bundles.py), [Agent execution](agent-execution/README.md), and [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md) | Checked source-commit artifact binding only; no independent review, accepted evidence bundle, task acceptance, readiness promotion, production IPC, security, performance, Chrome-class, release, or product-ready claim |

### Project-buildout and ownership research reports

These reports must remain linked from the research index and mapped back to the owning project-buildout, readiness, review, production-readiness, and agent-execution records:

- [`docs/research/fresh-host-reproduction-inventory-2026-07.md`](research/fresh-host-reproduction-inventory-2026-07.md);
- [`docs/research/implementation-kickoff-review-inventory-2026-07.md`](research/implementation-kickoff-review-inventory-2026-07.md);
- [`docs/research/build-readiness-dependency-graph-inventory-2026-07.md`](research/build-readiness-dependency-graph-inventory-2026-07.md);
- [`docs/research/documentation-readiness-completion-audit-2026-07.md`](research/documentation-readiness-completion-audit-2026-07.md);
- [`docs/research/chrome-class-capability-traceability-map-2026-07.md`](research/chrome-class-capability-traceability-map-2026-07.md);
- [`docs/research/full-implementation-game-plan-audit-2026-07.md`](research/full-implementation-game-plan-audit-2026-07.md);
- [`docs/research/backup-ownership-gap-inventory-2026-07.md`](research/backup-ownership-gap-inventory-2026-07.md).

### Architecture and API research reports

These reports must remain linked from the research index and mapped back to the owning architecture, API, security, readiness, task-queue, and validation records:

- [`docs/research/ipc-capability-boundary-inventory-2026-07.md`](research/ipc-capability-boundary-inventory-2026-07.md).

### Native UI research reports

These reports must remain linked from the research index and mapped back to the owning Blueprint, readiness, risk, and decision records:

- [`docs/research/native-ui-framework-evaluation-2026-07.md`](research/native-ui-framework-evaluation-2026-07.md);
- [`docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md`](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- [`docs/research/native-ui-framework-bakeoff-inventory-2026-07.md`](research/native-ui-framework-bakeoff-inventory-2026-07.md);
- [`docs/research/native-ui-component-fixture-inventory-2026-07.md`](research/native-ui-component-fixture-inventory-2026-07.md);
- [`docs/research/page-surface-composition-inventory-2026-07.md`](research/page-surface-composition-inventory-2026-07.md);
- [`docs/research/window-input-accessibility-spike-inventory-2026-07.md`](research/window-input-accessibility-spike-inventory-2026-07.md).

### Storage and profile research reports

These reports must remain linked from the research index and mapped back to the owning storage, product, readiness, risk, and release records:

- [`docs/research/profile-session-format-inventory-2026-07.md`](research/profile-session-format-inventory-2026-07.md).

### Release operations research reports

These reports must remain linked from the research index and mapped back to the owning release, security, storage, readiness, risk, and support records:

- [`docs/research/research-package-update-lab-inventory-2026-07.md`](research/research-package-update-lab-inventory-2026-07.md).

### Security and incident research reports

These reports must remain linked from the research index and mapped back to the owning security, release, support, legal-community, readiness, risk, and support records:

- [`docs/research/sandbox-probe-inventory-2026-07.md`](research/sandbox-probe-inventory-2026-07.md);
- [`docs/research/wp-003-sandbox-probe-plan-2026-07.md`](research/wp-003-sandbox-probe-plan-2026-07.md);
- [`docs/research/incident-patch-rehearsal-inventory-2026-07.md`](research/incident-patch-rehearsal-inventory-2026-07.md).

### Benchmark research reports

These reports must remain linked from the research index and mapped back to the owning Blueprint, readiness, risk, and decision records:

- [`docs/research/performance-benchmark-readiness-packet-2026-07.md`](research/performance-benchmark-readiness-packet-2026-07.md);
- [`docs/research/benchmark-corpus-expansion-2026-07.md`](research/benchmark-corpus-expansion-2026-07.md);
- [`docs/research/chrome-class-performance-runbook-2026-07.md`](research/chrome-class-performance-runbook-2026-07.md);
- [`docs/research/benchmark-hardware-os-manifest-2026-07.md`](research/benchmark-hardware-os-manifest-2026-07.md);
- [`docs/research/benchmark-os-update-control-manifest-2026-07.md`](research/benchmark-os-update-control-manifest-2026-07.md);
- [`docs/research/semantic-resource-attribution-taxonomy-2026-07.md`](research/semantic-resource-attribution-taxonomy-2026-07.md);
- [`docs/research/benchmark-competitor-version-manifest-2026-07.md`](research/benchmark-competitor-version-manifest-2026-07.md);
- [`docs/research/benchmark-competitor-local-install-inventory-2026-07.md`](research/benchmark-competitor-local-install-inventory-2026-07.md);
- [`docs/research/benchmark-browser-pin-capture-contract-2026-07.md`](research/benchmark-browser-pin-capture-contract-2026-07.md);
- [`docs/research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md`](research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md);
- [`docs/research/benchmark-server-lifecycle-self-test-2026-07.md`](research/benchmark-server-lifecycle-self-test-2026-07.md);
- [`docs/research/benchmark-30-tab-scenario-contract-2026-07.md`](research/benchmark-30-tab-scenario-contract-2026-07.md);
- [`docs/research/benchmark-trace-artifact-package-contract-2026-07.md`](research/benchmark-trace-artifact-package-contract-2026-07.md);
- [`docs/research/benchmark-browser-launch-runner-contract-2026-07.md`](research/benchmark-browser-launch-runner-contract-2026-07.md);
- [`docs/research/benchmark-statistics-analysis-contract-2026-07.md`](research/benchmark-statistics-analysis-contract-2026-07.md);
- [`docs/research/benchmark-engine-baseline-harness-readiness-map-2026-07.md`](research/benchmark-engine-baseline-harness-readiness-map-2026-07.md);
- [`docs/benchmark-lab/chrome-class-performance-readiness-lane.md`](benchmark-lab/chrome-class-performance-readiness-lane.md).

### Servo and source-strategy research reports

These reports feed `ADR-0009`; they do not approve a Servo-derived release path:

- [`docs/research/servo-source-strategy-inventory-2026-07.md`](research/servo-source-strategy-inventory-2026-07.md);
- [`docs/research/servo-independent-build-reproduction-2026-07.md`](research/servo-independent-build-reproduction-2026-07.md);
- [`docs/research/servo-dependency-provenance-inventory-2026-07.md`](research/servo-dependency-provenance-inventory-2026-07.md);
- [`docs/research/servo-supply-chain-policy-scan-2026-07.md`](research/servo-supply-chain-policy-scan-2026-07.md);
- [`docs/research/servo-license-advisory-decision-prep-2026-07.md`](research/servo-license-advisory-decision-prep-2026-07.md);
- [`docs/research/servo-generated-native-unsafe-classification-2026-07.md`](research/servo-generated-native-unsafe-classification-2026-07.md);
- [`docs/research/servo-unsafe-ffi-contract-review-2026-07.md`](research/servo-unsafe-ffi-contract-review-2026-07.md);
- [`docs/research/servo-build-script-generated-output-audit-2026-07.md`](research/servo-build-script-generated-output-audit-2026-07.md);
- [`docs/research/servo-clean-generated-output-reproduction-2026-07.md`](research/servo-clean-generated-output-reproduction-2026-07.md);
- [`docs/research/servo-generated-output-generator-manifest-2026-07.md`](research/servo-generated-output-generator-manifest-2026-07.md);
- [`docs/research/servo-build-script-proc-macro-side-effect-audit-2026-07.md`](research/servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- [`docs/research/servo-source-archive-provenance-audit-2026-07.md`](research/servo-source-archive-provenance-audit-2026-07.md);
- [`docs/research/servo-upstream-source-provenance-2026-07.md`](research/servo-upstream-source-provenance-2026-07.md);
- [`docs/research/servo-independent-source-verification-2026-07.md`](research/servo-independent-source-verification-2026-07.md);
- [`docs/research/servo-source-baseline-equivalence-policy-2026-07.md`](research/servo-source-baseline-equivalence-policy-2026-07.md);
- [`docs/research/servo-native-bootstrap-provenance-audit-2026-07.md`](research/servo-native-bootstrap-provenance-audit-2026-07.md);
- [`docs/research/servo-native-package-decision-prep-2026-07.md`](research/servo-native-package-decision-prep-2026-07.md);
- [`docs/research/servo-component-boundary-analysis-2026-07.md`](research/servo-component-boundary-analysis-2026-07.md);
- [`docs/research/servo-local-compatibility-corpus-2026-07.md`](research/servo-local-compatibility-corpus-2026-07.md);
- [`docs/research/servo-performance-baseline-2026-07.md`](research/servo-performance-baseline-2026-07.md);
- [`docs/research/servo-security-maintenance-implications-2026-07.md`](research/servo-security-maintenance-implications-2026-07.md).

## Build output and temporary material

Build output, caches, transfer payloads, generated publication scripts, secrets, and local editor state are not durable source.

CI and wrapper commands set `CARGO_TARGET_DIR` outside the repository. The repository validator rejects known generated or temporary paths.

## Change procedure

For any structural change:

1. update this map;
2. update `Cargo.toml` and `workspace-components.json` when workspace membership or dependency direction changes;
3. update CODEOWNERS and professional ownership;
4. update dependency, unsafe, native, generated, and provenance ledgers;
5. update affected Blueprint, book, roadmap, traceability, and readiness records;
6. update validation and deterministic generation checks;
7. run `sh tools/check.sh` or `.\tools\check.ps1`;
8. attach evidence, unsupported behavior, and rollback implications to the review.
