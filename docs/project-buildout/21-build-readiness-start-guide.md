# Build Readiness Start Guide

Status: one-step continuation handoff for next build session  
Owner: program architecture and engineering operations  
Last updated: 2026-07-19

This guide is for people and agents starting or resuming in-session work. It does not authorize broad implementation. It keeps the current evidence graph, gate posture, and research direction aligned.

## Current build posture

- Use [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json) as the gate truth.
- Current decision is **not ready for broad implementation**.
- Allowed now: contained M0 continuity tasks, validation commands, documentation/research indexing, and no-claim task-handoff maintenance.
- Hard blocks: `PB-002` (source strategy) and `PB-019` (backup ownership), plus all blocked/owner-only gates behind them.

Long-term positioning remains a Chrome-class/extreme-performance competitive target, but this is not yet evidence-approved. Track that lane through the [Chrome-class capability traceability map](../research/chrome-class-capability-traceability-map-2026-07.md), [performance benchmark readiness packet](../research/performance-benchmark-readiness-packet-2026-07.md), [sustained performance policy research](../research/sustained-performance-policy-research-2026-07.md), and the [Chrome-class performance readiness lane](../benchmark-lab/chrome-class-performance-readiness-lane.md). Do not treat any intermediate artifact in this phase as a Chrome-class or performance claim.

When UI work eventually becomes authorized, use the [Nova design source](../ui-runtime/design-lab/README.md) as the visual and layout reference and follow the [Nova Native Build Entry Criteria](../research/nova-native-build-entry-criteria-2026-07.md) plus the [Native UI and Accessibility Closure Preparation](../research/native-ui-and-accessibility-closure-preparation-2026-07.md). Nova does not own browser behavior: Rust state, typed commands, accessibility, page-surface, security, and accepted ADRs remain authoritative, and React remains confined to the design lab.

Use this in the same order every session:

1. [Start here](../start-here.md) for definitions and scope.
2. [Build Readiness Progress Snapshot](22-build-readiness-progress-snapshot.md) for the one-pass current state.
3. [Build Continuation Readiness Pack](20-build-continuation-readiness-pack.md) for the current hard-stop summary and fast-lane scorecard.
4. [Build Readiness Operating Board](13-build-readiness-operating-board.md) for sequencing.
5. [Pre-build Readiness Checklist](11-pre-build-readiness-checklist.md) for check constraints.
6. [Build Information Readiness Ledger](../research/build-information-readiness-ledger-2026-07.md) for unresolved information classes.
7. [Documentation Readiness Evidence Matrix](18-documentation-readiness-evidence-matrix.md) for documentation continuity checks.
8. [Contained M0 Start State Inventory](../research/contained-m0-start-state-inventory-2026-07.md) before deciding whether to execute proposed tasks.

## What to do before broad M1 work

The repository is organized for continuation, but broad implementation is blocked until gate owners run owner-reviewed evidence and accept readiness promotion for each lane:

| Lane | Current gate state | Deep research track to expand |
|---|---|---|
| `PB-002` Source strategy | blocked | `RQ-31`, `RQ-44`, `RQ-46`, `RQ-47`, `RQ-25`, `RQ-16` | Servo/alternative source selection, provenance equivalence, legal/support boundaries, component baseline decisions, generated-output provenance proofs, and the checked no-claim [engine-landscape source manifest](../research/machine/browser-engine-landscape-source-manifest.json). |
| Deferred open-web governance | deferred outside active crosswalk | `RQ-33` and the [feature-lifecycle research packet](../research/open-web-governance-feature-lifecycle-research-2026-07.md) | Feature-specific user need, source identity, interoperability denominator, security/privacy/accessibility review, lifecycle, maintenance, and owner decision before feature selection. |
| `PB-008`/`PB-009` Toolchain and fresh-host confidence | partial | `RQ-31`, `RQ-47` | Versioned compiler/SDK/linker/toolchain manifests plus independent fresh-host run with source-tree cleanliness proof, cache/target controls, and owner-reviewed readiness review. |
| `PB-011` IPC and transport boundaries | partial | `RQ-02`, `RQ-13`, `RQ-22`, `RQ-36` | Canonical transport, wire codec, queue/backpressure behavior, malformed/timeout/cancellation negative tests, independent review packet. |
| `PB-012` Sandbox probes | partial | `RQ-20`, `RQ-38` | Packaged expected-deny probes, unstable-path policy capture, effective platform-policy evidence, and owner review. |
| `PB-013` Benchmark/extreme-performance prep | partial | `RQ-16`, `RQ-23`, `RQ-34`, `RQ-35`, `RQ-37` | The checked no-claim [engine-landscape source manifest](../research/machine/browser-engine-landscape-source-manifest.json) and sustained-performance policy comparison, then fixed-hardware browser runs with reproducible corpus, launch-runner and server lifecycle evidence, raw traces/artifacts, and statistics review. |
| `PB-003`/`PB-004`/`PB-005`/`PB-014`/`PB-015` Native UI | partial | `RQ-04`, `RQ-05`, `RQ-29`, `RQ-30`, `RQ-40`, `RQ-55`, `RQ-56`, `RQ-57` | Adapter contract proofs, toolkit selection via executed bake-off, compositor/page-surface proof, input/accessibility fixtures, `UI-GATE-7` and release-path approvals. |
| `PB-016` Profile/session schemas | partial | `RQ-14`, `RQ-27`, `RQ-49`, `RQ-50`, `RQ-53`, `RQ-54` | Synthetic-fixture executable schemas, migration/fault/recovery accounting, privacy isolation, and owner-reviewed evidence through the [profile/session execution and data-safety closure-preparation route](../research/profile-session-execution-and-data-safety-closure-preparation-2026-07.md); sync and credential behavior remain unsupported until separately reviewed. |
| `PB-017` Package/update lab | partial | `RQ-31`, `RQ-63`, `RQ-64`, `RQ-66` | Signed executable update labs, staged install/rollback/migration tests, production key separation evidence. |
| `PB-018` Incident-response rehearsal | partial | `RQ-31`, `RQ-60`, `RQ-66` | Private intake and patch-rehearsal execution, disclosure workflow, and owner-led readiness review. |
| `PB-019` Backup ownership | blocked | `RQ-25`, `RQ-45`, `RQ-47`, `RQ-48`, `RQ-60`, `RQ-66` | Qualified backups, two-person control, support matrix updates, and release authority closure. |

## Daily continuation cadence

Before each session:

- open this guide and confirm the gate truth in the linked pack/board/ledger files;
- run the relevant checkers for any edited machine registries or research artifacts;
- append a short note to [`research-log.md`](../research-log.md) when a continuity or gate posture change occurs;
- if you open or close a lane, verify `tools/validate_blueprint.py` and `tools/validate_implementation_kickoff_review.py` still pass for the edited scope.

## Required pre-build evidence commands

Run this command set before allowing any implementation-adjacent activity in the current session:

```powershell
python3 -B tools/validate_build_foundation.py
python3 -B tools/validate_blueprint.py
python3 -B tools/validate_implementation_plan.py
python3 -B tools/validate_implementation_kickoff_review.py
python3 -B tools/validate_adr_0009_evidence.py
python3 -B tools/validate_documentation_readiness_completion_audit.py
python3 -B tools/validate_build_information_readiness.py
python3 -B tools/validate_ipc_capability_boundaries.py
python3 -B tools/validate_sandbox_contracts.py
python3 -B tools/validate_github_issue_handoff.py
python3 -B tools/validate_evidence_bundles.py
git diff --check
git diff --cached --check
cargo fmt --all -- --check
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
.\tools\check.ps1
```

Treat any failure in this set as requiring a documentation, registry, or process-capture patch before changing lanes.

If the same command output changed since the last entry in [`research-log.md`](../research-log.md), add a new log row with the changed evidence.

## Claim boundary reminder

This project is in a coherent documented pre-build state for contained M0 continuation only. Nothing in this guide should be treated as approval for:

- broad M1 implementation,
- Chrome-class or extreme-performance public comparison claims,
- production/beta/stable release status,
- security/compatibility/accessibility/performance claims,
- production-updater or incident-response authority claims.

Those remain owner-approved, evidence-heavy promotions beyond this guide.
