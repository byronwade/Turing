# Fresh-Host Reproduction Packet Examples - July 2026

Status: fictitious no-claim run-record handoff example
Owner: build reproducibility, release operations, and documentation research
Related gates: `PB-008` and `PB-009`
Related task: `TASK-000002`
Scope: packet shape only; no fresh-host execution, toolchain approval, readiness promotion, or release claim

## Purpose

This page gives a maintainer one complete example of the information required for a pinned-toolchain and fresh-host run packet. Every value is fictitious. It complements the [Fresh Host Reproduction Inventory](fresh-host-reproduction-inventory-2026-07.md), [Fresh-Host Toolchain Reproduction Closure Preparation](fresh-host-toolchain-reproduction-closure-preparation-2026-07.md), checked run-record and readiness-review templates, and `TASK-000002`.

## Packet identity

| Field | Fictitious example | Required rule |
|---|---|---|
| record_id | `FRESH-HOST-RUN-EXAMPLE-2026-07-19-A` | Stable identifier for one immutable attempt set |
| related_gates | `PB-008`, `PB-009` | Must match the task and readiness registries |
| related_task | `TASK-000002` | Must be an approved immutable manifest before execution |
| run_class | `independent_fresh_host` | Must be proven by host/image identity and prior-state evidence |
| execution_status | `example_only` | Never treat as executed evidence |
| source_commit | `0000000000000000000000000000000000000000` | Placeholder is invalid in a real record |
| packet_created_at | `2026-07-19T12:00:00Z` | Record timezone and clock source |
| owner | `unassigned-example-owner` | Real record requires an accountable owner |
| independent_reviewer | `unassigned-example-reviewer` | Must be independent and named |

## Host and prior-state identity

| Field | Fictitious example | Evidence artifact |
|---|---|---|
| host_identity | `clean-image-example-07` | image identity, provisioning timestamp, and host-facts hash |
| OS | `Windows 11 Enterprise example-build x86_64` | edition, build, patch level, locale, timezone, shell, terminal |
| hardware | `example CPU / 64 GiB / 500 GiB free` | CPU, memory, disk, virtualization, and device facts |
| privilege | `standard user with declared build elevation` | privilege and elevation events |
| network | `declared outbound package access; no credentials` | network posture, proxy, DNS, and credential statement |
| toolchain | `Rust example, Cargo example, Git example, Python example, SDK/linker example` | version output, installer/channel provenance, and manifest hashes |
| prior state | `no prior checkout, target, cache, installer, credential, or profile` | pre-run filesystem and cache statement |
| waiver | `none` | If non-empty, owner, reason, scope, expiry, and cleanup are required |

The phrase `independent fresh host` is valid only when the record preserves enough information for a reviewer to distinguish a newly provisioned environment from a reused workstation, checkout, target directory, or cache. A clean-VM equivalent requires an explicit, time-bounded owner waiver.

## Source and artifact identity

| Field | Fictitious example | Rejection condition |
|---|---|---|
| remote_url | `https://example.invalid/turing.git` | Reject an unrecorded or mutable source origin |
| branch | `main` | Record the branch at checkout, but pin the commit |
| commit | `0000000000000000000000000000000000000000` | Reject missing or unverifiable commit identity |
| checkout_command | `git clone --no-local ... && git checkout --detach <commit>` | Retain the exact command and output |
| repository_path | `C:\clean\turing` | Record path and long-path policy |
| git_config | `core.autocrlf=false; core.longpaths=true` | Record relevant line-ending and path settings |
| source_status_before | `clean, tracked files only` | Retain `git status --porcelain=v2` output |
| source_status_after | `clean, tracked files only` | Capture after every required command family |
| target_root | `C:\build-output\turing-target` | Must be outside durable source unless explicitly approved |
| cache_roots | `C:\build-cache\cargo; C:\build-cache\rustup` | Record ownership, isolation, and cleanup |
| artifact_root | `C:\evidence\FRESH-HOST-RUN-EXAMPLE-A` | Retain output and hash manifest outside source |

## Attempted-command denominator

All attempted commands, including setup, retries, failures, skipped commands, and cleanup, remain in the denominator.

| Sequence | Command family | Command | Exit | Classification | Retained output |
|---:|---|---|---:|---|---|
| 1 | host capture | `capture-host-facts.ps1` | 0 | `observed` | `01-host.out`, SHA-256 `example-host-hash` |
| 2 | checkout | `git clone ...` | 0 | `observed` | `02-checkout.out`, SHA-256 `example-checkout-hash` |
| 3 | source identity | `git status`, `git rev-parse`, `git remote -v` | 0 | `observed` | `03-source.out`, SHA-256 `example-source-hash` |
| 4 | bootstrap | `.\tools\bootstrap.ps1` | 0 | `reproduced_candidate` | `04-bootstrap.out/.err`, hashes recorded |
| 5 | doctor | `.\tools\doctor.ps1` | 1 | `environmental_failure` | `05-doctor.out/.err`, hashes recorded |
| 6 | repair | `install-declared-prerequisite` | 0 | `owner-approved_repair` | `06-repair.out`, hashes recorded |
| 7 | doctor retry | `.\tools\doctor.ps1` | 0 | `reproduced_candidate` | `07-doctor-retry.out/.err`, hashes recorded |
| 8 | aggregate check | `.\tools\check.ps1` | 0 | `reproduced_candidate` | `08-check.out/.err`, hashes recorded |
| 9 | direct xtask | `cargo run --locked -p xtask -- check` | 0 | `reproduced_candidate` | `09-xtask.out/.err`, hashes recorded |
| 10 | cleanup | `cleanup-evidence.ps1` | 0 | `cleanup_observed` | `10-cleanup.out`, hashes recorded |

The first doctor failure cannot be erased by the successful retry. The real review must decide whether the repair was permitted by the manifest, whether it changes the declared environment, and whether the result remains comparable to the intended clean-host protocol.

## Required command record fields

For each command, the real packet records:

- exact command line, shell, working directory, environment/profile identifier, and manifest step;
- start and end timestamps with timezone and clock source;
- exit code, timeout/cancellation state, stdout path, stderr path, and SHA-256 hashes;
- toolchain observations before and after any repair;
- failure class: source-controlled, environmental, network-dependent, nondeterministic, timeout, cancellation, or unknown;
- generated-output, cache, target, installer, credential, and source-tree effects;
- retry, skip, rollback, and cleanup rationale;
- reviewer disposition and whether the command remains in the denominator.

## Source-tree and output reconciliation

The real packet must reconcile before/after status and output roots:

| Check | Fictitious result | Required decision |
|---|---|---|
| tracked changes | `none before and after` | retain exact status output |
| untracked source files | `none` | reject committed or unexplained generated junk |
| target directory | `outside source` | record path, size, cleanup, and retention |
| Cargo/Rustup caches | `isolated declared roots` | reject ambiguous warm-cache reuse |
| installers/downloads | `outside source, hashes retained` | record provenance and cleanup |
| secrets/profiles | `not present` | reject credentials or user profiles in evidence |
| temporary files | `enumerated and removed` | retain cleanup result and exceptions |

## Readiness-review handoff

A real run packet is submitted with a separate readiness review that identifies:

1. owner, independent reviewer, release-operations reviewer, quality reviewer, and security reviewer as applicable;
2. exact host/image, source commit, toolchain profile, command denominator, and retained-log manifest;
3. whether the run is accepted as independent, accepted only as a clean-VM equivalent, rejected, or held by exception;
4. every failed, skipped, retried, timed-out, canceled, or repaired step and its effect on reproducibility;
5. cache, target, source-tree, installer, credential, cleanup, rollback, and retention findings;
6. support-boundary and registry changes required by the decision;
7. expiration and revisit trigger for every exception.

The checked readiness-review template does not supply these identities or findings. It is a contract for a future review, not a review result.

## Rejection rules

- Reject fresh-host classification when a prior checkout, target directory, cache, installer, generated output, credential, or profile is reused without an approved waiver and identity proof.
- Reject reproduction claims when compiler, SDK, linker, Rust, Cargo, Git, shell, OS, architecture, or relevant platform facts are omitted.
- Reject success-only evidence when any attempted command, retry, failure, timeout, cancellation, skipped step, or cleanup result is missing.
- Reject source-cleanliness claims when before/after status is absent or generated output is mixed with durable source.
- Reject release or broad-build confidence when evidence is from a same-host rerun, unreviewed clean-VM equivalence, template, validator, or M0 check alone.
- Keep `PB-008`, `PB-009`, and `TASK-000002` below reviewed readiness until the real packet and owner-reviewed readiness review are accepted.

## Claim boundary

This example proves only that fresh-host evidence can be organized as one auditable packet. It does not prove a clean-host reproduction, toolchain equivalence, build reproducibility, release confidence, production readiness, or Chrome-class performance.

## Next proof

Execute the approved `TASK-000002` manifest on an independent fresh host or an explicitly approved clean-VM equivalent, retain every attempted command and hash, complete the readiness review, and synchronize the result across `PB-008`, `PB-009`, the build-information ledger, task queue, owner-decision board, support boundary, and release records.
