# Fresh Host Reproduction Inventory - July 2026

Status: no-claim `PB-009` reproduction inventory, run-record template, and readiness-review template; no independent fresh-host run yet
Owner: release operations, quality, build, documentation-research, and program

## Question

Can Turing make the `PB-009` fresh-host reproduction blocker precise enough for a maintainer to execute later without mistaking current-host check output for independent build confidence?

## Conclusion

Yes, for planning only. The checked [`fresh-host-reproduction.json`](../project-buildout/machine/fresh-host-reproduction.json) registry, checked [`no-claim-run-record-template.json`](../project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json), checked no-claim [`fresh-host readiness-review template`](../project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json), [`validate_fresh_host_reproduction.py`](../../tools/validate_fresh_host_reproduction.py), [`validate_fresh_host_run_records.py`](../../tools/validate_fresh_host_run_records.py), and [`validate_fresh_host_readiness_review.py`](../../tools/validate_fresh_host_readiness_review.py) define the host facts, source identity, command output, cache and target-directory evidence, source-tree cleanliness, failure classification, retained-log hashes, owner-review handoff, and rejection rules required before `PB-009` can move beyond partial.

This inventory does not run on a fresh host. It does not prove the project bootstraps from a clean machine, promote `PB-009` to ready, approve broad implementation, approve preview/beta/stable readiness, or support a Chrome-class claim.

## Current Evidence

The M0 foundation already provides:

- repository bootstrap, doctor, check, and `xtask` commands;
- PowerShell and POSIX wrappers;
- wrapper behavior that sets `CARGO_TARGET_DIR` outside the repository when the caller has not set it;
- aggregate checks covering documentation validation, registries, formatting, clippy, workspace tests, shell self-test, and the prototype run;
- CI validation for the current repository.

That evidence proves the commands exist and validate the current M0 scope. It does not prove an independent clean host can reproduce the environment and result.

## Required Fresh-Host Evidence

`PB-009` still requires an owner-approved independent fresh reference host or clean-VM equivalent with:

- exact OS edition, version, architecture, patch level, shell, locale, timezone, CPU, memory, disk, network posture, and privilege facts;
- a clean checkout at an exact commit with remote URL, branch, commit hash, line-ending/Git configuration facts, and before/after dirty-state output;
- `bootstrap`, `doctor`, `check`, and `xtask` logs with dates, shell, exit code, Rust/Cargo/Git facts, aggregate validation output, formatting, clippy, workspace tests, shell self-test, and prototype output;
- `CARGO_TARGET_DIR`, Cargo/Rustup cache roots, temp directory, ignored-output behavior, and proof that build outputs stayed outside durable source;
- failure logs and rollback notes if anything fails.

Same-host reruns, reused target directories, hidden failures, omitted source-tree status, committed installers, and generated junk in source are rejected as fresh-host evidence.

## Checked No-Claim Run-Record Template

The machine-readable [`fresh-host-run-record.schema.json`](../project-buildout/machine/fresh-host-run-record.schema.json) and checked [`no-claim-run-record-template.json`](../project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json) now define the exact shape of a future evidence record.

The template requires future records to capture:

- independent fresh-host or owner-approved clean-VM identity facts;
- checkout URL, branch, commit, Git version, line-ending configuration, and before/after source-tree status;
- wrapper and direct `xtask` command records for bootstrap, doctor, and check;
- command line, shell, timestamps, exit code, retained output path, SHA-256 output hash, and success/failure classification;
- `CARGO_TARGET_DIR`, Cargo cache root, Rustup toolchain cache, temp directory, cleanup evidence, and generated-output status;
- all attempted commands and failures in the denominator.

The checked template is `template_no_execution` with `execution_status: not_executed`. It explicitly provides no independent fresh-host reproduction, no owner-approved clean-VM equivalent, no command execution evidence, no retained bootstrap/doctor/check/xtask logs, no `PB-009` readiness promotion, and no preview, beta, stable, production, release-confidence, or Chrome-class claim.

## Checked No-Claim Readiness-Review Template

The machine-readable [`fresh-host-readiness-review.schema.json`](../project-buildout/machine/fresh-host-readiness-review.schema.json) and checked [`no-claim-fresh-host-readiness-template.json`](../project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json) define the review object a future maintainer must complete after a real run record exists.

The template requires a future owner-reviewed review to replace null run-record, reference-host, clean-VM-waiver, owner-reviewer, independent-reviewer, release-operations-reviewer, and quality-reviewer fields. It covers:

- independent fresh reference host or owner-approved clean-VM evidence;
- exact host facts, source identity, command output, cache and artifact controls, source-tree cleanliness, retained hashes, failure denominator, rollback, cleanup, and environmental waiver evidence;
- owner, independent, release-operations, quality, and security review axes;
- explicit rejection of same-host reruns, placeholder reviewers, missing command logs, missing host/source identity, dirty source trees, cache ambiguity, success-only denominators, unbounded waivers, and validation-as-release-confidence claims.

The checked readiness-review template provides no owner review, no independent review, no release-operations review, no quality review, no command execution review, no retained clean-host evidence, no `PB-009` readiness promotion, no broad M1 readiness, no preview, beta, stable, production, release-confidence, Chrome-class, or implementation claim.

## Registry And Validator

The machine-readable control files are:

- [`fresh-host-reproduction.schema.json`](../project-buildout/machine/fresh-host-reproduction.schema.json)
- [`fresh-host-reproduction.json`](../project-buildout/machine/fresh-host-reproduction.json)
- [`fresh-host-run-record.schema.json`](../project-buildout/machine/fresh-host-run-record.schema.json)
- [`no-claim-run-record-template.json`](../project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json)
- [`fresh-host-readiness-review.schema.json`](../project-buildout/machine/fresh-host-readiness-review.schema.json)
- [`no-claim-fresh-host-readiness-template.json`](../project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json)
- [`validate_fresh_host_reproduction.py`](../../tools/validate_fresh_host_reproduction.py)
- [`validate_fresh_host_run_records.py`](../../tools/validate_fresh_host_run_records.py)
- [`validate_fresh_host_readiness_review.py`](../../tools/validate_fresh_host_readiness_review.py)

The validator checks:

- no-claim and unsupported-boundary language;
- source-record existence;
- required host, source, command, artifact, failure, run-record, and rejection terms;
- readiness-review false flags, null review-scope fields, owner-review axes, and rejection rules;
- evidence axis coverage;
- `PB-009` status and evidence in [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- `TASK-000002` allowed paths, preconditions, acceptance criteria, and negative tests.

## Build-Readiness Effect

`PB-009` remains `partial`. The inventory, run-record template, and readiness-review template make the missing proof executable and reviewable, but readiness still requires an actual independent run or owner-approved clean-VM equivalent plus retained logs and owner-reviewed fresh-host readiness review beyond the checked no-claim template.

No broad implementation, source-strategy, benchmark, release packaging, preview, beta, stable, production, or Chrome-class claim is supported by this inventory.
