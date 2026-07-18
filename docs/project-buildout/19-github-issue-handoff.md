# GitHub Issue Handoff

Status: coordination snapshot; no task approval
Owner: program, documentation-research, engineering operations, and issue triage
Last refreshed: 2026-07-18

## Purpose

This handoff records the current GitHub issue and pull-request cleanup state in durable project documentation. GitHub issues remain a coordination surface; canonical status still lives in the Blueprint, machine registries, readiness board, task queue, research reports, and implementation master plan.

Use this file when stopping or resuming work after branch cleanup, issue cleanup, or PR consolidation. It prevents stale closed PRs or open issue titles from being mistaken for accepted implementation state.

## Source Snapshot

Observed with:

```bash
gh issue list --state all --limit 100 --json number,title,state,url,closedAt,createdAt,updatedAt
gh pr list --state all --limit 100 --json number,title,state,mergedAt,headRefName,url
git rev-parse HEAD
```

Baseline commit at observation: `ff114a26b4240c9756ba168b5eb226e8f74ff97a`.

The checked machine snapshot is [`github-issue-handoff.json`](machine/github-issue-handoff.json), validated by [`tools/validate_github_issue_handoff.py`](../../tools/validate_github_issue_handoff.py).

## Current Issue Board

| Issue | GitHub state | Canonical records | Current disposition | Next proof | Must not claim |
|---|---|---|---|---|---|
| [#1](https://github.com/byronwade/Turing/issues/1) - M0 repository validation | Closed | `WP-001`, `PB-001`, M0 | Closed after the M0 repository validation and evidence foundation landed on `main`. | Reopen only if validation, CI, required docs, or source hygiene drift. | Broad M1, production, release, Chrome-class, compatibility, security, accessibility, or daily-driver readiness. |
| [#2](https://github.com/byronwade/Turing/issues/2) - kernel identities and bounded IPC | Open | `WP-002`, `PB-011`, `TASK-000003` | M0 reference exists, but the machine backlog keeps `WP-002` in progress. | Authenticated OS transport, canonical wire codec, shared-memory/handle contracts, compromised-process negative harness, cancellation/reconnect state machines, fuzz/model tests, and independent security review. | Production IPC, process-isolation readiness, renderer-security readiness, or `WP-002` completion. |
| [#3](https://github.com/byronwade/Turing/issues/3) - renderer sandbox probe harnesses | Open | `WP-003`, `PB-012`, `TASK-000004` | Contract, catalog, schema, templates, and issue body are current on `main`; executable probes are still missing. | Packaged expected-deny probes, unsandboxed controls, effective platform-policy capture, broker fixtures, compromised-client harnesses, platform matrix evidence, and owner-reviewed sandbox readiness. | Sandbox readiness, site-isolation safety, hostile-browsing safety, `SEC-GATE-*`, production safety, or implementation proof. |
| [#4](https://github.com/byronwade/Turing/issues/4) - native accessible shell | Open | `WP-004`, `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, `TASK-000006` | Native-shell lane has checked no-claim inventories and review template only. | Toolkit-neutral contracts, equivalent reference shells, `ADR-0013`, `ADR-0014`, `ADR-0016`, rendered fixtures, page-surface proof, accessibility transcripts, and owner-reviewed native UI readiness. | Toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI, or implementation completion. |
| [#5](https://github.com/byronwade/Turing/issues/5) - tab lifecycle and 30-tab simulator | Open | `WP-005`, `PB-013`, `TASK-000005` | Prototype has lifecycle concepts; full resource attribution and 30-tab evidence remain open. | Executable simulator, mixed-state and all-live 30-tab artifacts, memory/resource attribution, pressure behavior, state-loss checks, and benchmark-ready owner review. | Low-memory, lower-energy, 30-tab leadership, or Chrome-class performance. |
| [#6](https://github.com/byronwade/Turing/issues/6) - static document engine | Open | `WP-006`, `WP-007`, `WP-008`, `WP-009`, M2 | Static engine work is sequenced but not started as an accepted build task. | HTML, DOM, CSS, layout, display-list, raster, accessibility, WPT/reduced tests, fuzzing, and evidence bundles within reviewed tasks. | Web compatibility, page rendering support, accessibility support, or safe hostile browsing. |
| [#7](https://github.com/byronwade/Turing/issues/7) - JavaScript, GC, Web IDL, tiering | Open | `WP-010`, `WP-011`, M3/M6 | Runtime work remains future milestone scope. | Interpreter, Test262 harness, exact GC, Web IDL bindings, WebAssembly track, JIT gates, differential tests, and security review. | JavaScript support, WebAssembly support, JIT readiness, or application compatibility. |
| [#8](https://github.com/byronwade/Turing/issues/8) - navigation, networking, storage | Open | `WP-012`, `WP-013`, `WP-014`, M4 | Network/storage/navigation work remains gated by process, IPC, sandbox, and schema decisions. | Navigation transactions, site assignment, scoped network service, HTTP/TLS subset, cookies/cache, storage broker, migration/fault tests, and cross-origin negative tests. | Safe browsing, network compatibility, storage safety, or production profile behavior. |
| [#9](https://github.com/byronwade/Turing/issues/9) - DevTools, tracing, headless, automation | Open | `WP-015`, M2/M5 | Protocol and tooling are planned but not executable product capability. | Versioned schemas, trace causality, headless profile security, WebDriver BiDi coverage, generated clients, and conformance tests. | Stable DevTools, automation compatibility, or remote-control safety. |
| [#10](https://github.com/byronwade/Turing/issues/10) - capability-safe agent reference | Open | `WP-016`, M6 | Agent architecture is documented; reference implementation and adversarial suite remain open. | Observation/action schemas, provider adapters, prompt-injection corpus, confirmation tests, stale-target tests, audit records, and capability enforcement. | Autonomous browser authority, safe consequential actions, provider trust, or production AI-agent readiness. |
| [#11](https://github.com/byronwade/Turing/issues/11) - package/update/release lab | Open | `WP-017`, `PB-017`, `TASK-000009` | Research package/update lab has checked no-claim templates only. | Executable package manifest, metadata parser, fake-key signature verification, staged install, rollback/migration/fault tests, privacy review, and owner-reviewed package/update readiness. | Stable channel, production updater, supported security, signing readiness, rollback safety, or release readiness. |
| [#12](https://github.com/byronwade/Turing/issues/12) - fixed-hardware lab | Open | `WP-018`, `PB-013`, `TASK-000005` | Benchmark planning evidence exists; no browser benchmark result exists. | Owner-approved hardware tiers, clean OS controls, benchmark-ready browser pins, implemented launch runner, raw artifacts, statistics, claim bundles, and owner-reviewed benchmark readiness. | Faster, lower memory, lower energy, competitor-result, Chrome-class, or public performance claim. |
| [#14](https://github.com/byronwade/Turing/issues/14) - fixed-hardware browser-engine baseline harness | Open | `RQ-16`, `PB-013`, `TASK-000005`, `EXP-ENGINE-001` | Research issue remains open because the harness has not produced browser-run evidence. | Equivalent workload harness across competitor pins, offline corpus, process topology capture, raw samples, unsupported denominators, and reproducible analysis. | Engine winner, competitor result, Chrome-class comparison, speed, memory, energy, or production claim. |

Issue number `#13` is not a missing backlog issue in this snapshot. GitHub's shared issue and pull-request number sequence assigned `#13` to the bootstrap pull request.

## Pull-Request Cleanup

| PR | State | Branch | Cleanup disposition | Superseding evidence |
|---|---|---|---|---|
| [#42](https://github.com/byronwade/Turing/pull/42) - WP-003 sandbox plan | Closed, not merged | `agent/wp-003-sandbox-plan` | Remote branch deleted because raw merge would have deleted current repository state. | `1af4b61` on `main` contains the ported WP-003 sandbox contract. |
| [#43](https://github.com/byronwade/Turing/pull/43) - implementation master plan | Closed, not merged | `docs/full-implementation-game-plan` | Remote branch deleted because raw merge would have deleted current repository state. | `ff114a2` on `main` contains the ported implementation master plan. |

## Continuation Rules

- Update this file and [`github-issue-handoff.json`](machine/github-issue-handoff.json) when canonical issue state, PR cleanup state, issue-to-work-package mapping, or live handoff guidance changes.
- Do not close an issue because a planning document, template, or no-claim validator exists. Close only when the issue's acceptance criteria are satisfied or deliberately superseded with an explicit replacement.
- Do not reopen a stale branch for merge if its raw diff would remove current repository state. Port additive evidence onto current `main`, validate it, and record the superseding commit.
- Treat open GitHub issues as coordination pointers. They are not task approval, owner review, readiness promotion, implementation proof, benchmark evidence, release evidence, or product support.

## Validation

Run:

```bash
python3 -B tools/validate_github_issue_handoff.py
python3 -B tools/validate_blueprint.py
cargo run --locked -p xtask -- check
```

A passing issue-handoff validation proves only that the offline snapshot is internally consistent with the documented issue cleanup state. It does not contact GitHub, approve tasks, or prove current live issue state.
