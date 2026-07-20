# Fresh-Host Toolchain Reproduction Closure Preparation - July 2026

Status: no-claim continuation route for `PB-008`, `PB-009`, and `TASK-000002`; no independent run has been executed
Owner: release operations, quality, build, documentation-research, and program
Research date: 2026-07-19

## Question

What exact evidence must a maintainer collect to close the pinned-toolchain and fresh-host confidence lane without treating a current-host rerun or a checked template as independent reproduction?

## Decision boundary

The existing [Build Information Readiness Ledger](build-information-readiness-ledger-2026-07.md), [Fresh Host Reproduction Inventory](fresh-host-reproduction-inventory-2026-07.md), run-record schema/template, readiness-review schema/template, and focused validators are sufficient to shape the next no-claim evidence run. They are not evidence of a fresh-host build, toolchain equivalence, reproducibility, release confidence, or broad implementation readiness.

## Primary toolchain-source observations

The following official documentation was retrieved on 2026-07-19 and is used to sharpen the run-record contract:

| Source | Observation | Required run-record consequence |
|---|---|---|
| [Rustup toolchains](https://rust-lang.github.io/rustup/concepts/toolchains.html) | Rustup accepts named channels, dated channels, fully versioned toolchains, and host target tuples. A channel name alone is not a stable compiler identity. | Record the exact Rust toolchain string, host target tuple, rustup version, resolved `rustc --version --verbose`, and installation/channel provenance. Prefer a dated or fully versioned toolchain for reproducibility. |
| [Rustup overrides and toolchain files](https://rust-lang.github.io/rustup/overrides.html) | Rustup can select a toolchain through command-line, environment, directory, or checked-in `rust-toolchain.toml` overrides, with defined precedence; pinned toolchains should normally travel with `Cargo.lock`. | Record the discovered toolchain-file path and hash, override source and precedence, active `rustup show`, requested components/targets/profile, and lockfile identity. A machine default or `rustc --version` alone is insufficient. |
| [Cargo build](https://doc.rust-lang.org/cargo/commands/cargo-build.html) | `--locked` asserts that dependency versions match the existing lockfile; `--offline` changes network behavior and can use only locally available registry state. | Record the lockfile hash, `--locked` use, registry/cache roots, network mode, and whether dependencies were fetched before an offline attempt. A passing `--locked` command does not prove a clean host or identical compiler/SDK/linker. |
| [Microsoft C++ Build Tools](https://learn.microsoft.com/en-us/cpp/overview/acquire-msvc?view=msvc-160) | MSVC Build Tools versions can coexist side by side; the latest released toolset is serviced independently from previews and older supported toolsets. | Record Visual Studio channel, installation instance, workload/component IDs, MSVC toolset version, Windows SDK version, linker path/version, and preview/stable status. Do not identify the environment only as "Visual Studio installed." |
| [Microsoft C++ command-line tools](https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170) | The installed workload and the initialized developer command-line environment jointly determine which compiler, linker, libraries, and target architecture a command can resolve. | Capture the exact Developer Command Prompt or `vcvars` initialization, environment delta, `cl`/`link` paths and versions, target architecture, and LLVM/lld path if used. A normal PowerShell PATH is not equivalent evidence. |
| [Windows SDK overview](https://learn.microsoft.com/en-us/windows/apps/windows-sdk/) | The Windows SDK provides versioned headers, libraries, metadata, and build tools and is a separate input from Visual Studio and the MSVC toolset. | Record the selected SDK version, installation root, header/library/resource-tool paths, target architecture, and discovery mechanism with the compiler and linker records. |

These observations refine the evidence contract only. They do not establish that the current host or any future host satisfies `PB-008` or `PB-009`.

## Reproducibility vocabulary and claim ladder

The lane uses four deliberately separate levels:

| Level | Evidence required | What it permits | What it does not prove |
| --- | --- | --- | --- |
| Repeatable validation | The same checkout passes documented validators or tests on one host, with command output and exit codes | A bounded diagnostic about that host and checkout | Fresh-host independence, bit-for-bit artifact equality, provenance, or release confidence |
| Clean-host replay | An independent fresh host or explicitly approved clean-VM equivalent repeats the commands with source, toolchain, cache, target, and failure records | Candidate evidence that the declared workflow can be reproduced in the declared environment class | Bit-for-bit identical release artifacts, complete provenance, or owner acceptance |
| Reproducible build | Same declared source, dependency, toolchain, environment, and build inputs produce bit-for-bit identical output, with comparison artifacts | Evidence of output determinism for the exact profile and platform | Independent trust, source/dependency review, distribution integrity, or cross-platform equivalence |
| Independently verified reproduction | Two or more genuinely independent build platforms corroborate the declared artifact/provenance and independence assumptions | Stronger provenance corroboration for the exact scope | Complete supply-chain security, owner approval, production support, or release readiness |

This ladder follows the [Reproducible Builds environment-recording guidance](https://reproducible-builds.org/docs/recording/) and SLSA's distinction between reproducible and verified reproducible builds. The run record must name the highest level actually supported and list the missing evidence for every higher level. A passing `check.ps1`, a same-host rerun, a clean-VM run without an approved equivalence record, or a single matching hash must not be labeled independently verified.

## Current-host wrapper diagnostic

On 2026-07-19, the current Windows checkout ran `tools/doctor.ps1 --ci` with `CARGO_TARGET_DIR` explicitly set to `%TEMP%\turing-current-host-doctor`. A same-host refresh on the current continuation session produced the same tool identities: `rustc 1.97.1 (8bab26f4f 2026-07-14)`, `cargo 1.97.1 (c980f4866 2026-06-30)`, `rustfmt 1.9.0-stable (8bab26f4f6 2026-07-14)`, `cargo clippy 0.1.97 (8bab26f4f6 2026-07-14)`, `Python 3.12.10`, and `git version 2.52.0.windows.1`, followed by `doctor: ready for contained M0 development`.

This is a current-host wrapper and toolchain diagnostic only. The output was not retained as a fresh-host run record, the host was not independently provisioned, `bootstrap`, `check`, and direct `xtask` paths were not thereby reproduced, and no gate status changed. It confirms that the documented Windows doctor entry point is executable in this checkout and that the observed tool identities match the pinned M0 baseline; it does not prove clean-host reproduction, toolchain equivalence, source-tree cleanliness after a complete run, release confidence, or readiness for broad implementation.

## 2026-07-20 current-host diagnostic refresh

The current continuation checkout was rechecked with `rustc --version --verbose`, `cargo --version`, `rustfmt --version`, `cargo clippy --version`, `python --version`, `git --version`, `rustup --version`, and `rustup show`. It reported `rustc 1.97.1 (8bab26f4f 2026-07-14)`, Cargo `1.97.1`, rustfmt `1.9.0-stable`, Clippy `0.1.97`, Python `3.12.10`, Git `2.52.0.windows.1`, rustup `1.29.0`, host `x86_64-pc-windows-msvc`, and the active `1.97.1-x86_64-pc-windows-msvc` toolchain selected by this repository's `rust-toolchain.toml`, with the matching target installed. The working tree was clean at the observed commit.

This refresh is same-host diagnostic evidence only. It does not provide a fresh-host run record, independent toolchain equivalence, owner review, or `PB-008`/`PB-009` promotion.

`PB-008` and `PB-009` remain `partial`. This report adds a consolidated replay protocol and terminology so that the next run can be reviewed against one stable contract. It does not authorize `TASK-000002`, promote either gate, or change any product, performance, security, compatibility, accessibility, release, or Chrome-class claim.

The [Fresh-Host Reproduction Packet Examples](fresh-host-reproduction-packet-examples-2026-07.md) provides a fictitious field-level packet for host and source identity, attempted-command denominator, retained hashes, failure classification, cleanup, and readiness-review handoff. It is an example only and does not provide a fresh-host run.

The checked [fresh-host toolchain-source manifest](../project-buildout/machine/fresh-host-toolchain-source-manifest.json), validated by [`validate_fresh_host_toolchain_sources.py`](../../tools/validate_fresh_host_toolchain_sources.py), records official Rustup, Cargo, and Microsoft toolchain, command-environment, and Windows SDK observations used by this route. It tracks run-record consequences only; it does not prove compiler/SDK/linker equivalence or fresh-host readiness.

## Evidence classes

The record must identify which environment was used:

| Class | Meaning | Gate effect |
|---|---|---|
| Reference host | Owner-designated environment whose exact facts are recorded as the comparison baseline. | Baseline only; not independent reproduction. |
| Same-host rerun | A second run on the already-used workstation or checkout. | Useful diagnostic evidence; cannot satisfy fresh-host independence. |
| Clean-VM equivalent | Newly provisioned isolated environment accepted under an explicit owner decision with scope, expiry, and equivalence rationale. | Potential evidence only after waiver and review. |
| Independent fresh host | Separate host or clean image with independently recorded identity, checkout, caches, and command output. | Candidate evidence for both gates after review. |

The run record must not use `independent`, `fresh`, `reproducible`, or `equivalent` without naming the class and retaining supporting facts.

## Fresh-host closure worksheet

The real `PB-008`/`PB-009` review must complete one worksheet for each retained run record. The worksheet keeps environment identity, command coverage, cache behavior, and claim scope together instead of allowing a green final command to hide earlier failures.

| Required field | Run record must retain | Rejection condition |
|---|---|---|
| Host class and identity | `reference host`, `same-host rerun`, `clean-VM equivalent`, or `independent fresh host`; OS/build, architecture, shell, locale, timezone, CPU, memory, disk, privilege, network, virtualization/image facts | Same-host output is called independent, or a clean-VM waiver has no owner, scope, expiry, and equivalence rationale |
| Source checkout identity | Remote URL, branch, exact commit/tree, Git version/configuration, line-ending policy, path, and before/after dirty-state output | Source identity, prior checkout reuse, or generated/ignored output is unexplained |
| Toolchain and commands | Rust/rustup/Cargo, compiler/SDK/linker/Git/Python versions and provenance; bootstrap, doctor, check, xtask commands, timestamps, shell, exit codes, stdout/stderr, and hashes | Success-only output, missing toolchain facts, or wrapper output substitutes for required direct command coverage without disposition |
| Cache and artifact roots | `CARGO_TARGET_DIR`, Cargo/Rustup/cache/temp roots, artifact retention path, installer/archive handling, and proof durable source stayed clean | Target/cache reuse or generated artifacts are not classified and bounded |
| Acquisition and replay mode | Network endpoints, mirrors/proxy/certificate posture, fetched artifact hashes, cache preloading state, offline/controlled-network policy, and equivalence rationale | Acquisition and replay are conflated, or preloaded caches are presented as clean dependency acquisition |
| Failure and cleanup denominator | Every attempted command, retry, timeout, cancellation, failure classification, rollback, cleanup, unresolved warning, and post-run source status | A final green check erases a failed step or missing cleanup evidence |
| Review and promotion | Owner/independent/release/quality reviewers, exact commit and host scope, highest supported reproducibility level, limitations, expiry, rerun trigger, and synchronized PB/task changes | Template or current-host diagnostic promotes PB-008/PB-009, release confidence, production, or Chrome-class readiness |

Until a real run record and owner-reviewed readiness review replace the no-claim templates, every worksheet row is `not_executed`, `PB-008`/`PB-009` remain unresolved, and no reproducibility or release-confidence claim is supported.

## Network and cache modes

The replay must distinguish two related but non-interchangeable modes:

1. **Acquisition mode:** network-enabled setup obtains pinned source, toolchains, and dependencies. Record URLs, refs, mirrors, response or archive hashes, retries, proxy/certificate posture, and downloaded-artifact provenance.
2. **Replay mode:** the declared commands run with empty, preloaded, or controlled caches and either offline or explicitly controlled network access. Record the cache state, network policy, endpoints, and the owner-approved equivalence rationale for any reused cache.

An offline run with preloaded caches is not clean dependency-acquisition evidence. A network-enabled rerun is not equivalent to an offline replay unless the source, tool, dependency, mirror, and cache inputs are captured and the difference is within the reviewed scope. Bootstrap downloads, dependency caches, build outputs, logs, and temporary archives require separate roots and cleanup records.

## Required replay protocol

Before execution, the owner must record:

- host identity, OS edition/build, architecture, locale, timezone, CPU, memory, disk, privilege, network posture, shell, and virtualization or image identity;
- compiler, SDK, linker, Rust, Cargo, Git, Python, and relevant platform-tool versions, including installation and channel provenance;
- source URL, branch, exact commit, Git line-ending/configuration facts, repository path, and expected clean state;
- cache roots, `CARGO_TARGET_DIR`, Rustup/Cargo directories, temporary directory, artifact root, retention location, and cleanup plan;
- intended wrapper and direct commands, timeout policy, expected outputs, and all attempted steps.

The executor must then:

1. provision the declared host or clean image without copying a prior target directory, generated output, unreviewed installer, credential, or source-tree artifact;
2. capture pre-run source-tree status and all environment/toolchain facts;
3. run repository bootstrap, doctor, aggregate check, and direct `xtask` check paths required by the current task manifest;
4. retain command lines, timestamps, shell, exit codes, stdout/stderr, failure classification, and SHA-256 hashes for every attempted command;
5. capture post-run source-tree status and prove target outputs, caches, temporary files, installers, and generated artifacts stayed outside the durable source tree unless explicitly declared;
6. record cleanup, rollback, network/credential handling, unresolved warnings, and every failed or skipped step;
7. submit the completed run record and readiness review for owner, independent, release-operations, quality, and security review as applicable.

The denominator is every attempted command, including setup, retries, failures, and cleanup. A successful final check cannot erase an earlier failure or missing log.

## Acceptance and rejection

Candidate evidence remains unaccepted until the owner-reviewed readiness review confirms host/source identity, toolchain facts, command coverage, retained-log hashes, cache and target-directory controls, source-tree cleanliness, failure accounting, cleanup/rollback, and any clean-VM waiver. The review must identify the exact commit and environment to which it applies.

Reject the run as fresh-host evidence when it reuses a prior target directory or source checkout without identity proof, omits compiler/SDK/linker facts, hides failures or exit codes, records success-only output, lacks before/after source status, places generated or secret material in the repository, uses placeholder reviewers, or relies on an unbounded clean-VM waiver.

The checked no-claim templates remain templates. A completed template with `template_no_execution` or `execution_status: not_executed` is not a run, an owner review, or a gate promotion.

## PB-020 closure dependency

Any future `PB-008` or `PB-009` readiness decision must be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and the [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md) route. A clean-host run, independent reproduction, toolchain manifest, or fresh-host readiness review cannot independently close `PB-020`, authorize broad implementation, establish release confidence, or support production, compatibility, performance, or Chrome-class claims. The final closure record must preserve exact host/source identity, command denominators, hashes, cache and target controls, reviewer identities, waivers, expiry, cleanup, and synchronized readiness and task records.

## Current next step

The next controlled action is a reviewed `TASK-000002` manifest that points to the existing ledger, inventory, schemas, templates, wrappers, and validators, then produces one retained run record and one owner-reviewed readiness review. Until that occurs:

- `PB-008` and `PB-009` remain `partial`;
- `TASK-000002` remains proposed-only and non-executable;
- contained M0 documentation and validation may continue;
- broad engine implementation, source-strategy-dependent work, release packaging, production claims, and Chrome-class comparisons remain gated.

## Canonical inputs

- [Build Information Readiness Ledger](build-information-readiness-ledger-2026-07.md)
- [Primary Source Bibliography](../blueprint-v1/18-source-bibliography.md)
- [Fresh Host Reproduction Inventory](fresh-host-reproduction-inventory-2026-07.md)
- [Build Readiness Task Queue](../project-buildout/17-build-readiness-task-queue.md)
- [Fresh-host reproduction registry](../project-buildout/machine/fresh-host-reproduction.json)
- [Fresh-host run-record schema](../project-buildout/machine/fresh-host-run-record.schema.json)
- [Fresh-host readiness-review schema](../project-buildout/machine/fresh-host-readiness-review.schema.json)
- [Fresh-host reproduction validator](../../tools/validate_fresh_host_reproduction.py)
