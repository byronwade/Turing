# Professional Project Buildout and Operating Handbook

Status: detailed research and professional operating baseline
Owner: program architecture and engineering operations
Last researched: 2026-07-18

This handbook is the control plane for turning Turing's research into a multi-year, multi-maintainer implementation. It defines who decides, how work becomes accepted, how evidence is traced, how the repository is structured, how contributors reproduce the environment, and how the product is released and maintained.

## Reading order

1. [01 Program Lifecycle And Phase Gates](01-program-lifecycle-and-phase-gates.md)
2. [02 Ownership Codeowners And Maintainer Ladder](02-ownership-codeowners-and-maintainer-ladder.md)
3. [03 Rfc Adr And Design Review Process](03-rfc-adr-and-design-review-process.md)
4. [04 Requirements Traceability And Evidence](04-requirements-traceability-and-evidence.md)
5. [05 Repository Build Toolchain And Coding Standards](05-repository-build-toolchain-and-coding-standards.md)
6. [06 Api Schema Configuration And Version Governance](06-api-schema-configuration-and-version-governance.md)
7. [07 Cross Cutting Security Performance Accessibility Privacy](07-cross-cutting-security-performance-accessibility-privacy.md)
8. [08 Release Incident Legal Data And Support](08-release-incident-legal-data-and-support.md)
9. [09 Servo Adoption Decision Framework](09-servo-adoption-decision-framework.md)
10. [10 Product Localization Documentation And Sustainability](10-product-localization-documentation-and-sustainability.md)
11. [11 Pre-build Readiness Checklist](11-pre-build-readiness-checklist.md)
12. [12 Agent Execution and Production Readiness](12-agent-execution-and-production-readiness.md)
13. [13 Build Readiness Operating Board](13-build-readiness-operating-board.md)
14. [14 ADR-0009 Source Strategy Decision Packet](14-adr-0009-source-strategy-decision-packet.md)
15. [15 ADR-0009 Evidence Traceability Matrix](15-adr-0009-evidence-traceability-matrix.md)
16. [16 ADR-0009 Decision Draft and Public-Claim Impact](16-adr-0009-decision-draft.md)
17. [17 Build Readiness Task Queue](17-build-readiness-task-queue.md)
18. [18 Documentation Readiness Evidence Matrix](18-documentation-readiness-evidence-matrix.md)
19. [Documentation Readiness Completion Audit](../research/documentation-readiness-completion-audit-2026-07.md)
20. [Implementation Master Plan](implementation-plan/README.md)

## Machine-readable companions

- [Ownership](../blueprint-v1/machine/professional-owners.json)
- [Requirements traceability](../blueprint-v1/machine/professional-traceability.json)
- [Phase gates](../blueprint-v1/machine/professional-phase-gates.json)
- [Review rules](../blueprint-v1/machine/professional-review-rules.json)
- [Exceptions](../blueprint-v1/machine/professional-exceptions.json)
- [Pre-build readiness](../blueprint-v1/machine/pre-build-readiness.json)
- [Build readiness task queue](../blueprint-v1/machine/build-readiness-task-queue.json)
- [Implementation kickoff review](machine/implementation-kickoff-review.json)
- [Build readiness dependency graph](machine/build-readiness-dependency-graph.json)
- [Documentation readiness completion audit](machine/documentation-readiness-completion-audit.json)
- [Implementation execution graph](../blueprint-v1/machine/implementation-execution-graph.json)
- [Implementation milestone gates](../blueprint-v1/machine/implementation-milestone-gates.json)
- [Implementation interface freezes](../blueprint-v1/machine/implementation-interface-freezes.json)
- [Implementation evidence catalog](../blueprint-v1/machine/implementation-evidence-catalog.json)
- [Implementation task sequence](../blueprint-v1/machine/implementation-task-sequence.json)

## Non-negotiable rule

A phase or release is incomplete while an applicable control lacks linked evidence, a time-bounded approved exception, or an explicit declaration that it is outside supported scope.

<!-- MARKET-STRATEGY-2026-07 -->
## Market opportunity control

The [market strategy book](../market-strategy/README.md) feeds this handbook through `OP-*` proposals. An opportunity cannot enter accepted scope until ownership, review class, requirements, risks, work packages, traceability, evidence, and phase gates agree.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent execution and stable-release control

The [Agent Execution book](../agent-execution/README.md) and [Production Readiness book](../production-readiness/README.md) are mandatory before delegating broad implementation or preparing supported binaries.

## Handoff and continuation control

Use this section as the fast continuation path after reading [Start Here](../start-here.md). It does not replace the machine readiness registry; it points people and agents to the records that order the current `PB-*`, `WP-*`, `RQ-*`, `ADR-*`, and proposed `TASK-*` evidence.

### Build-readiness control path

1. Read the [Build Readiness Operating Board](13-build-readiness-operating-board.md) before expanding implementation.
2. Check [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json) for the authoritative gate state.
3. Use the checked [Implementation Kickoff Review Inventory](../research/implementation-kickoff-review-inventory-2026-07.md) before broadening work across unresolved `PB-*` lanes.
4. Use the checked [Build Readiness Dependency Graph](../research/build-readiness-dependency-graph-inventory-2026-07.md) before changing task order, task dependencies, or cross-lane sequencing.
5. Use the checked [Documentation Readiness Completion Audit](../research/documentation-readiness-completion-audit-2026-07.md) before calling documentation preparation complete; it confirms contained M0 continuation only and keeps all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, and accessibility claims unsupported.
6. Use the [Documentation Readiness Evidence Matrix](18-documentation-readiness-evidence-matrix.md) to verify that the entry points, registries, research crosswalk, task controls, and validation commands still support contained M0 continuation.
7. Use the [Implementation Master Plan](implementation-plan/README.md) only as dependency-ordered execution documentation for reviewed, bounded tasks.
8. Use the proposed [Build Readiness Task Queue](17-build-readiness-task-queue.md) and checked no-claim [task approval template](../agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json) only to shape reviewed task manifests.
9. Convert no proposed `TASK-*` item into execution without the owner, reviewer, allowed-path, prohibited-path, budget, rollback, and evidence-bundle controls described in [Agent Execution](../agent-execution/README.md).
10. Keep source strategy, fresh-host reproducibility, IPC boundaries, benchmark claims, native-shell toolkit and page-surface selection, sandbox policy, profile/session behavior, package/update authority, incident-response decisions, backup ownership, readiness promotion, and release authority as owner-only decisions.

### Source-strategy lane

Before any Servo-derived or source-strategy-dependent implementation, inspect:

- [ADR-0009 Source Strategy Decision Packet](14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Decision Draft and Public-Claim Impact](16-adr-0009-decision-draft.md);
- [`ADR-0009` evidence registry](../blueprint-v1/machine/adr-0009-evidence.json);
- [`ADR-0009` evidence validator](../../tools/validate_adr_0009_evidence.py).

Those records route to the Servo source, build reproduction, dependency, supply-chain, license/advisory/SBOM, generated-code, build-script, build-script/proc-macro side-effect, native bootstrap, native package decision-prep, FFI, unsafe, source/archive provenance, upstream source provenance, independent source verification, source-baseline equivalence, component-boundary, JavaScript-conflict, compatibility-denominator, performance-baseline-preparation, security/maintenance-implication, public-claim/support-impact, and packaging evidence.

### Benchmark and performance lane

Before treating fixed-hardware measurement, Chrome-class comparison, low-memory, fastest, or extreme-performance work as build-ready, inspect the current no-claim benchmark package:

- [Performance Benchmark Readiness Packet](../research/performance-benchmark-readiness-packet-2026-07.md);
- [Chrome-Class Performance Runbook](../research/chrome-class-performance-runbook-2026-07.md);
- [Benchmark Hardware and OS Manifest](../research/benchmark-hardware-os-manifest-2026-07.md);
- [Benchmark OS and Update-Control Manifest](../research/benchmark-os-update-control-manifest-2026-07.md);
- [Semantic Resource Attribution Taxonomy](../research/semantic-resource-attribution-taxonomy-2026-07.md);
- [Benchmark Competitor Version Manifest](../research/benchmark-competitor-version-manifest-2026-07.md);
- [Benchmark Competitor Local Install Inventory](../research/benchmark-competitor-local-install-inventory-2026-07.md);
- [Benchmark Browser Pin Capture Contract](../research/benchmark-browser-pin-capture-contract-2026-07.md);
- [Benchmark Browser Pin Local Diagnostic Capture](../research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md);
- [Benchmark Corpus Expansion](../research/benchmark-corpus-expansion-2026-07.md);
- checked no-claim [claim-bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json) before owner-reviewed claim bundles.

The linked machine evidence starts with the [no-claim manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json), [current Windows high-end hardware candidate](../blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json), [current Windows high-end OS-control candidate](../blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json), [semantic owner taxonomy](../blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json), [current desktop release-candidate competitor versions](../blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json), [current Windows high-end competitor local installs](../blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json), [current Windows high-end browser-pin capture plan](../blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json), [current Windows high-end Chrome/Edge browser-pin diagnostic](../blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json), [no-claim corpus manifest](../blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json), [no-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json), checked no-claim [claim-bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json), and the checked [runner-managed server lifecycle self-test](../../tools/run_benchmark_server_profile.py).

Validate benchmark evidence with the [benchmark manifest validator](../../tools/validate_benchmark_manifests.py), [benchmark hardware validator](../../tools/validate_benchmark_hardware.py), [benchmark OS-control validator](../../tools/validate_benchmark_os_controls.py), [benchmark resource-attribution validator](../../tools/validate_benchmark_resource_attribution.py), [benchmark competitor-version validator](../../tools/validate_benchmark_competitor_versions.py), [benchmark competitor local-install validator](../../tools/validate_benchmark_competitor_local_installs.py), [benchmark browser-pin capture validator](../../tools/validate_benchmark_browser_pin_capture.py), [benchmark browser-pin diagnostic validator](../../tools/validate_benchmark_browser_pin_diagnostics.py), [benchmark browser-pin capture self-test runner](../../tools/capture_benchmark_browser_pins.py), [benchmark corpus validator](../../tools/validate_benchmark_corpus.py), [benchmark network profile validator](../../tools/validate_benchmark_network_profile.py), [benchmark server lifecycle self-test](../../tools/run_benchmark_server_profile.py), [benchmark launch-runner validator](../../tools/validate_benchmark_launch_runners.py), [benchmark claim-bundle validator](../../tools/validate_benchmark_claim_bundles.py), [benchmark browser launch-runner self-test](../../tools/run_benchmark_browser_launch.py), [benchmark profile static-server self-test](../../tools/serve_benchmark_profile.py), and [benchmark smoke runner self-test](../../tools/run_benchmark_smoke.py).

### Ownership lane

Before treating `PB-019` as anything other than blocked, inspect:

- [Backup Ownership Gap Inventory](../research/backup-ownership-gap-inventory-2026-07.md);
- [`backup-ownership-gap.json`](machine/backup-ownership-gap.json);
- [`backup-ownership-gap.schema.json`](machine/backup-ownership-gap.schema.json);
- checked no-claim [`backup-ownership readiness-review template`](machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json);
- [backup ownership gap validator](../../tools/validate_backup_ownership_gap.py);
- [backup ownership readiness-review validator](../../tools/validate_backup_ownership_readiness_review.py);
- [`professional-owners.json`](../blueprint-v1/machine/professional-owners.json);
- root [CODEOWNERS](../../.github/CODEOWNERS).

The checked inventory records the current provisional primary-only owner state, and the checked readiness-review template records the future review shape. They do not name qualified backups, grant release or signing authority, prove two-person control, approve owner-reviewed backup ownership readiness, approve security disclosure, approve legal posture, close incidents, or create production authority.

### Claim boundary

The records above support contained M0 and no-claim evidence work only. They do not approve broad M1 implementation, Servo adoption, benchmark-ready browser pins, Chrome-class comparison, speed, memory, energy, compatibility, security, accessibility, production, beta, stable, or daily-driver claims.
