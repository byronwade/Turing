# TASK-000011 WP-002 Review Handoff - July 2026

Status: review handoff; not task acceptance, not an evidence-bundle instance, and not a production IPC claim
Owner: architecture, security, quality, performance, documentation, and independent review
Related execution task: [`TASK-000011`](../agent-execution/machine/tasks/TASK-000011.json)
Related work package: `WP-002`
Related report: [WP-002 kernel identity, capability, and bounded IPC reference](wp-002-kernel-ipc-2026-07.md)
Related requirements: `REQ-SEC-003`, `REQ-PERF-004`

## Purpose

This packet gives an independent reviewer one place to evaluate the `review_pending` M0 `WP-002` implementation task without inventing project state from scattered source files, tests, generated output, CI checks, evidence-capture records, and prose.

It does not accept `TASK-000011`. It does not create an accepted independent evidence bundle. It does not promote `PB-011`, complete `WP-002`, approve `TASK-000003`, or establish renderer security, agent security, process isolation, site isolation, production IPC, broad implementation readiness, Chrome-class status, or any security or performance claim.

## Review question

Can `TASK-000011` move from implementation-complete-for-review to independent acceptance for the contained M0 reference scope?

Current answer: the repository has candidate evidence and a checked non-accepting evidence capture for independent review, but acceptance is still unproven until a reviewer reruns the required checks on the exact commit under review, records an independent evidence bundle conforming to [`evidence-bundle.schema.json`](../agent-execution/machine/evidence-bundle.schema.json), and writes an explicit review decision.

## Current baseline and recapture rule

The prior review baseline for this handoff was `12922b46165d8d941e0dc504148196f4497d8e91` (July 19, 2026); the current continuation audit reaches repository head `eb0473eb711d0f7fa68cf9aea0c5971d026af456`. The checked no-claim bundle from July 18 remains intentionally bound to historical source commit `4590aad94f298d380d43bffc7b9a5cb618beccac`; the current July 20 no-claim capture is bound to `eb0473eb711d0f7fa68cf9aea0c5971d026af456`. Both are valid non-accepting records, not evidence of task acceptance or readiness promotion. Before independent review, the reviewer must recapture the required artifacts and command outputs against one exact source commit, record that commit in a new evidence bundle, and keep prior bundles immutable. Documentation-only commits after the selected review baseline also require recapture before acceptance.

## Scope boundary

`TASK-000011` covers only the M0 reference portion of `WP-002`:

- generated process roles, capabilities, message kinds, routes, limits, and process capability records;
- restart-safe process identity in Rust types;
- bounded envelope, sequence, queue, process, and channel checks;
- deterministic kernel authorization and channel binding;
- shell-level M0 integration of the reference model;
- documentation that keeps the remaining transport, sandbox, and production gaps explicit.

The following remain outside this task:

- operating-system process launch;
- authenticated IPC transport;
- canonical wire encoding or fuzzable decoder;
- shared-memory or handle-transfer leases;
- timeout, cancellation, close, half-close, reconnect, and crash semantics on a real transport;
- compromised-process harnesses;
- platform sandbox policy;
- renderer, agent, site-isolation, or production-security proof;
- fixed-hardware production queue-budget evidence.

## Evidence inventory

| Evidence source | Current candidate evidence | Reviewer action |
|---|---|---|
| [`schemas/ipc/control-plane.json`](../../schemas/ipc/control-plane.json) | Canonical M0 control-plane roles, capabilities, launch rights, message kinds, document scope, limits, and queue classes. | Check schema review scope and rerun deterministic generation. |
| [`tools/generate_ipc.py`](../../tools/generate_ipc.py) | Validates the schema and regenerates Rust policy output plus process-capability records. | Run `python3 -B tools/generate_ipc.py --check` on the review commit. |
| [`crates/turing-ipc/src/generated.rs`](../../crates/turing-ipc/src/generated.rs) and [`process-capabilities.json`](../blueprint-v1/machine/process-capabilities.json) | Committed generated output from the canonical schema. | Confirm generated output is not hand-edited and matches the generator. |
| [`security/generated-code.json`](../../security/generated-code.json) | Registers `GEN-IPC-001` source, generator, outputs, command, owner, and review boundary. | Verify generated-code ledger and drift checks cover the new output. |
| [`crates/turing-types/src/lib.rs`](../../crates/turing-types/src/lib.rs) | Non-zero IDs, monotonic sequence increment behavior, and restart-safe `ProcessIdentity`. | Review zero-ID, non-wrapping increment, and process-epoch tests. |
| [`crates/turing-ipc/src/envelope.rs`](../../crates/turing-ipc/src/envelope.rs) | Kind-specific encoded-size checks and generated document-epoch scope enforcement. | Review oversized-message and document-scope tests. |
| [`crates/turing-ipc/src/sequence.rs`](../../crates/turing-ipc/src/sequence.rs) | Exact monotonic sequence acceptance and gap rejection without state advance. | Review duplicate, skipped, and state-preservation behavior. |
| [`crates/turing-ipc/src/queue.rs`](../../crates/turing-ipc/src/queue.rs) | Item and byte backpressure plus immutable admission-time byte charging. | Review overcommit, recovery, dequeue, and mutable-size regression behavior. |
| [`crates/turing-kernel/src/lib.rs`](../../crates/turing-kernel/src/lib.rs) | Process launch authorization, capability attenuation, stale-epoch rejection, channel registration, endpoint binding, route authorization, and sequence enforcement. | Review kernel negative tests and look for confused-deputy or stale-identity gaps. |
| [`apps/turing-shell/src/main.rs`](../../apps/turing-shell/src/main.rs) | Command-line M0 shell exercises the policy reference without native UI, web runtime, network, storage, Plug-in, or AI capability. | Run shell self-test through `xtask check` or `cargo run --locked -p turing-shell -- --self-test`. |
| [`tools/validate_build_foundation.py`](../../tools/validate_build_foundation.py) | Checks workspace, dependency, generated IPC, task status, generated-code ledger, and M0 boundary drift. | Run directly and through `xtask check`; confirm no validator was weakened. |
| [WP-002 reference report](wp-002-kernel-ipc-2026-07.md) | Describes implemented reference surface, security properties, limitations, and next bounded tasks. | Confirm positive evidence and limitations match the source and tests. |
| [`TASK-000011`](../agent-execution/machine/tasks/TASK-000011.json) | Records status, owner, independent reviewer role, allowed paths, acceptance criteria, negative tests, resource budgets, rollback, and expiry. | Keep status `review_pending` until independent review records acceptance or rejection. |

## Acceptance-criteria review map

| `TASK-000011` acceptance criterion | Candidate evidence | Review status |
|---|---|---|
| One canonical schema generates roles, capabilities, messages, routes, limits, and process capability documentation. | `control-plane.json`, `generate_ipc.py`, `generated.rs`, `process-capabilities.json`, `security/generated-code.json`, and generator drift checks. | Candidate evidence exists; reviewer must rerun generation and inspect source-to-output authority. |
| Restart-safe identities reject stale process epochs. | `turing-types::ProcessIdentity`, kernel restart/remove logic, and stale-epoch tests. | Candidate evidence exists for the in-process reference only. |
| Capabilities can be attenuated but not escalated. | `launch_with_capabilities`, role defaults, and kernel capability-escalation tests. | Candidate evidence exists for generated role defaults. |
| Message routes and sender capabilities are deny-by-default. | Generated route allowlists, required capabilities, `authorize`, route-denial test, and missing-capability test. | Candidate evidence exists for the reference policy oracle. |
| Messages, queues, processes, and channels have explicit bounds. | Generated maximum encoded sizes, queue budgets, process table limit, channel table limit, and validator checks. | Candidate evidence exists; production budgets remain unmeasured. |
| Sequence failures do not advance channel state. | `SequenceTracker` gap test and kernel duplicate-sequence test. | Candidate evidence exists; transport reordering remains out of scope. |
| Generation drift, formatting, lint, tests, shell integration, and documentation validation pass. | `tools/generate_ipc.py --check`, `validate_build_foundation.py`, Rust formatting, Clippy, workspace tests, shell self-test, prototype run, and documentation validators. | Acceptance requires fresh command output on the exact review commit. |
| Limitations remain explicit and no production security claim is made. | WP-002 report, start-here status, documentation readiness matrix, Blueprint architecture/security chapters, and pre-build readiness registry. | Candidate evidence exists; reviewer must reject if any positive claim outruns evidence. |
| Only a process-broker principal can register a channel before messages use it. | `register_channel`, `renderer_cannot_register_a_channel`, and `unregistered_channel_is_rejected`. | Candidate evidence exists for the M0 policy oracle. |
| Queue byte accounting uses the immutable charge captured at admission. | `dequeue_uses_the_charge_captured_at_admission` regression test. | Candidate evidence exists for queue accounting behavior. |

## Negative-test review map

| Manifest negative test | Current test or check to inspect |
|---|---|
| zero identity | `typed_ids_reject_zero` in `turing-types` |
| oversized message | `rejects_message_larger_than_generated_kind_limit` in `turing-ipc` envelope tests |
| missing or unexpected document epoch | `enforces_generated_document_scope` in `turing-ipc` envelope tests |
| duplicate or skipped sequence | `rejects_gaps_without_advancing_state` in `turing-ipc`; duplicate sequence in `channel_sequence_and_endpoint_binding_are_enforced` |
| queue byte or item overcommit | `applies_byte_backpressure_without_dropping_item` in `turing-ipc` queue tests |
| unauthorized child launch | `renderer_cannot_launch_processes` in `turing-kernel` |
| capability escalation | `launch_capabilities_can_only_be_attenuated` in `turing-kernel` |
| stale process epoch | `stale_process_epoch_is_rejected_after_restart` in `turing-kernel` |
| remove and relaunch cannot resurrect a prior process identity | `removed_process_id_uses_a_new_epoch_and_rejects_stale_replay` in `turing-kernel` |
| denied role route | `generated_route_and_capability_are_enforced` in `turing-kernel` |
| missing attenuated capability | `attenuated_process_cannot_use_removed_capability` in `turing-kernel` |
| channel endpoint reuse | endpoint mismatch assertion in `channel_sequence_and_endpoint_binding_are_enforced` |
| unregistered channel | `unregistered_channel_is_rejected` in `turing-kernel` |
| unauthorized channel registration | `renderer_cannot_register_a_channel` in `turing-kernel` |
| duplicate channel registration | duplicate registration assertion in `channel_sequence_and_endpoint_binding_are_enforced` |
| mutable encoded-size accounting | `dequeue_uses_the_charge_captured_at_admission` in `turing-ipc` queue tests |

## Required review commands

Run the aggregate wrapper from a clean worktree on the exact commit being reviewed:

```powershell
.\tools\check.ps1
```

The direct command family remains:

```bash
python3 -B tools/validate_blueprint.py
python3 -B tools/validate_adr_0009_evidence.py
python3 -B tools/generate_ipc.py --check
python3 -B tools/validate_build_foundation.py
git diff --check
git diff --cached --check
cargo fmt --all -- --check
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
cargo run --locked -p xtask -- check
```

If the reviewer uses a narrower rerun, the evidence bundle must state which acceptance criteria and negative tests the narrower run does not cover.

## Evidence-bundle gap

Acceptance requires a machine-readable evidence bundle that follows [`docs/agent-execution/machine/evidence-bundle.schema.json`](../agent-execution/machine/evidence-bundle.schema.json). The bundle must at minimum bind:

- `task_id` to `TASK-000011`;
- `source_commit` to the exact 40-hex commit reviewed;
- environment details for OS, shell, Rust, Cargo, Git, and relevant path/tool settings;
- hashed `command_log` artifacts for generation, validation, formatting, linting, tests, shell self-test, and prototype checks; each log must identify a unique command, acceptance/negative-test scope, exact `source_commit`, start time, duration, and `bundle.environment` reference;
- artifact hashes or retained logs for each reviewed command;
- any failure, retry, waiver, or skipped command;
- a reviewer identity distinct from the implementation owner;
- an explicit `accept`, `reject`, or `needs_changes` decision.

The checked no-claim [`TASK-000011.no-claim.2026-07-18.json`](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json) record is a historical, non-accepting evidence capture validated by [`validate_evidence_bundles.py`](../../tools/validate_evidence_bundles.py). The current [`TASK-000011.no-claim.2026-07-20.json`](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-20.json) capture refreshes source identities for commit `eb0473eb711d0f7fa68cf9aea0c5971d026af456`; its reviewer is not independent and its decision is `needs_independent_review`. Neither bundle accepts the task, promotes `PB-011`, or provides production IPC evidence.

The evidence-bundle validator permits this historical no-claim record to omit `command_log` artifacts only because its limitations explicitly state that raw local command logs were not retained. Any future `accepted`, `rejected`, or `needs_changes` bundle must include at least one hashed `command_log` artifact, and the review packet must list the complete command set or explicit skipped/failure records.

No accepted evidence-bundle instance is present in this repository at the time of this packet.

## Rejection triggers

The reviewer should reject or return `TASK-000011` for changes if any of these are true:

- generated output does not match the canonical schema and generator;
- any acceptance criterion lacks source, test, validator, documentation, and command-output evidence;
- stale identities, channel endpoints, sequence state, queues, or capabilities can be confused after restart, removal, attenuation, or duplicate registration;
- the evidence relies on issue state, chat context, or intent rather than committed source and rerunnable commands;
- limitations are weakened or replaced with production, security, compatibility, performance, memory, energy, Chrome-class, release, beta, stable, or daily-driver claims;
- the reviewer and implementation owner are the same principal;
- the evidence bundle is missing, unhashed, not tied to a source commit, or not independently reviewed.

## Next decision

After this handoff, the owner has two coherent continuation choices:

1. assign an independent reviewer to accept, reject, or return `TASK-000011` with an evidence bundle;
2. leave `TASK-000011` in `review_pending` and continue a different contained M0 lane, such as fresh-host reproduction for `TASK-000002` or no-claim IPC hardening for the proposed `TASK-000003`.

Either choice keeps `PB-011` partial. `WP-002` is not complete until authenticated transport, wire codec, handle/shared-memory leases, timeout/cancellation/close/crash behavior, compromised-process negative tests, platform process launch, and independent security evidence exist.
