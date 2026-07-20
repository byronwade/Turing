# Servo Upstream Source Provenance - July 2026

Status: dated upstream source-provenance report for `PB-002` and proposed `ADR-0009`; no source, dependency, crate, release archive, or license approval
Owner: architecture, provenance, release operations, security, legal-review, engine, and documentation owners
Audit date: 2026-07-19 local / 2026-07-20 UTC metadata refresh; original evidence capture 2026-07-17
Confidence: medium for observed upstream object IDs, GitHub release metadata, release source-archive digest, and crates.io package checksum; low for source approval, legal approval, full-history provenance, reproducible-release, compatibility, performance, maintenance, and adoption conclusions until owner reviews run

## Question

Which upstream Servo source identities correspond to the successful external Windows build baseline, current upstream `main`, the latest GitHub release, and the latest crates.io `servo` package, and what remains before Turing can select a source baseline for `ADR-0009`?

This report does not import Servo source, generated output, dependency archives, release archives, native binaries, build logs, or crate package contents into Turing. It does not approve a Servo source baseline, release archive, crates.io package, dependency, license posture, or `ADR-0009` option.

## Scope

The report covers:

- external Servo checkout at `C:\ts\servo`;
- upstream remote `https://github.com/servo/servo.git`;
- GitHub release metadata for `servo/servo`;
- GitHub commit verification metadata for the build baseline, current `origin/main`, and latest release tag commit;
- local download and SHA-256 verification of the latest GitHub release source archive under `C:\ts\servo-upstream-source-provenance-20260717`;
- crates.io package metadata and local registry-cache checksum for `servo 0.4.0`.

The report does not cover full source-history review, maintainer identity verification beyond GitHub's commit-verification metadata, independent mirror verification, source-offer completeness, vendored archive contents-level license review, generated-output provenance, owner-reviewed component-boundary suitability, or reproducible release builds.

## Method

Evidence was collected outside the Turing repository using:

1. `git -C C:\ts\servo fetch --tags origin`, `status`, `rev-parse`, `show`, `ls-tree`, `ls-remote`, `tag -v`, and `fsck --connectivity-only`;
2. `gh release view --repo servo/servo --json tagName,targetCommitish,publishedAt,url,isDraft,isPrerelease,tarballUrl,zipballUrl,assets`;
3. `gh api repos/servo/servo/commits/<sha>` for GitHub commit verification metadata;
4. `cargo search servo --limit 5` and `cargo info servo --verbose`;
5. `https://crates.io/api/v1/crates/servo/0.4.0` for crates.io package checksum and publication metadata;
6. `gh release download v0.3.0 --repo servo/servo --pattern servo-v0.3.0-src-vendored.tar.gz --dir C:\ts\servo-upstream-source-provenance-20260717 --clobber`;
7. `Get-FileHash -Algorithm SHA256` for the downloaded release source archive and cached `servo-0.4.0.crate`;
8. Python's `tarfile` module for a bounded readability check of the downloaded release source archive.

No upstream source or release artifact was copied into this repository.

## 2026-07-20 local / 2026-07-20 UTC official metadata refresh

A read-only refresh of the official GitHub repository, branch, release, and crates.io APIs was performed on 2026-07-20 local time. It changes the freshness boundary for repository activity, but it does not replace the dated build, archive, or package evidence captured on 2026-07-17.

| Field | Refreshed observation |
|---|---|
| Repository default branch | `main` |
| Latest observed `main` commit | `f542a355e5565e380aa0570132d4138dde328bae` |
| Latest observed `main` commit author date | Current API head commit; commit-author metadata was not used as a release or build date |
| Repository pushed/updated timestamps | `2026-07-20T03:24:57Z` / `2026-07-20T03:53:53Z` |
| Latest published release | `v0.3.0`, published `2026-06-25T15:09:42Z`, target `release/v0.3` |
| Release immutability | GitHub API reports `immutable: true` |
| Latest crates.io `servo` version | `0.4.0`, metadata updated `2026-07-16T12:14:01.753698Z` |

The refreshed `main` commit is later than the 2026-07-17 `origin/main` row below. Its tree, build status, dependency graph, generated outputs, licenses, security posture, compatibility, and performance have not been inspected by this refresh. The successful external build baseline must therefore no longer be described as merely two commits behind current upstream without a new comparison run.

## Current build checkout and upstream main

Observed from `C:\ts\servo` after `git fetch --tags origin` on 2026-07-17:

| Field | Successful external build baseline | Current `origin/main` |
|---|---|---|
| Commit | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` | `622600e045c2e5ea688a9b19b8671b6f43112817` |
| Commit date | 2026-07-17T15:50:14Z | 2026-07-17T17:01:59Z |
| Commit subject | `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)` | `script: Optimize element::has_class() (#46594)` |
| Tree | `daa2bc0e189e1981fb021501065fc3466159b00d` | `9d71530fe4d36dd9c94a2a411d75f219fde0dfc9` |
| Tracked files by tree listing | `193033` | `193033` |
| Local relation | `HEAD` | `HEAD...origin/main` reported `0 2`; local build baseline is two commits behind |
| GitHub commit verification | `verified: true`, `reason: valid`, verified at 2026-07-17T16:27:37Z | `verified: true`, `reason: valid`, verified at 2026-07-17T17:08:03Z |

The external checkout is a shallow partial clone:

| Field | Observation |
|---|---|
| `git rev-parse --is-shallow-repository` | `true` |
| Remote | `https://github.com/servo/servo.git` with `blob:none` partial-clone filter |
| `rev-list --count HEAD` | `1` |
| `rev-list --count origin/main` | `3` |
| `git fsck --connectivity-only` | exited `0`, with dangling objects reported |

Interpretation: the external checkout remains useful build-baseline evidence because it has the object tree that was bootstrapped and built. It is not full-history provenance evidence. Any owner decision that relies on release ancestry, maintainer history, signed release lineage, or independent mirror comparison still needs a non-shallow source-provenance run.

## Latest GitHub release source

`gh release view --repo servo/servo` observed the latest GitHub release as:

| Field | Observation |
|---|---|
| Tag | `v0.3.0` |
| Release URL | `https://github.com/servo/servo/releases/tag/v0.3.0` |
| Published | 2026-06-25T15:09:42Z |
| Target commitish | `release/v0.3` |
| Draft | `false` |
| Prerelease | `false` |
| GitHub tarball URL | `https://api.github.com/repos/servo/servo/tarball/v0.3.0` |
| GitHub zipball URL | `https://api.github.com/repos/servo/servo/zipball/v0.3.0` |

Local tag and branch checks from the external Servo repository:

| Field | Observation |
|---|---|
| `git cat-file -t v0.3.0` | `commit` |
| `v0.3.0` commit | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` |
| `v0.3.0` tree | `c41b1defccd9ed47a5ac2a8ad40929bc34de80a0` |
| Commit date | 2026-06-04T20:29:05+02:00 |
| Commit subject | `release: Use stylo 0.18 for 0.3 release` |
| Tracked files by tree listing | `191174` |
| `refs/heads/release/v0.3` | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` |
| `refs/tags/v0.3.0` | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` |
| `git tag -v v0.3.0` | failed because `v0.3.0` is a lightweight commit tag, not a tag object |
| GitHub commit verification | `verified: false`, `reason: unsigned` |

Interpretation: `v0.3.0` and `release/v0.3` point to the same unsigned commit object. The release tag is not a signed annotated tag, and GitHub reports the underlying release commit as unsigned. The release still has GitHub release metadata and asset digests, but Turing needs an explicit "signed tag or equivalent provenance" decision before any release archive is accepted as a source baseline.

## Release source archive digest

The latest GitHub release includes a vendored source archive:

| Asset | GitHub metadata |
|---|---|
| Name | `servo-v0.3.0-src-vendored.tar.gz` |
| URL | `https://github.com/servo/servo/releases/download/v0.3.0/servo-v0.3.0-src-vendored.tar.gz` |
| Content type | `application/x-gtar` |
| Created | 2026-06-11T12:38:48Z |
| Updated | 2026-06-11T12:39:08Z |
| Size | `364697035` |
| GitHub digest | `sha256:c75effbdc0ab6f86b318e28d139eb056268224e072a684492b49409c5221c871` |
| Observed download count | `18` |

Local verification under `C:\ts\servo-upstream-source-provenance-20260717`:

| File | Size | SHA-256 |
|---|---:|---|
| `servo-v0.3.0-src-vendored.tar.gz` | `364697035` | `C75EFFBDC0AB6F86B318E28D139EB056268224E072A684492B49409C5221C871` |

Python `tarfile` readability check:

| Check | Observation |
|---|---|
| Archive entries iterated | `271973` |
| First entries | `.`, `./.cargo`, `./.cargo/config.toml`, `./.clippy.toml`, `./.config`, `./.config/nextest.toml` |

Interpretation: the locally downloaded release source archive matches GitHub's release-asset digest and is readable as a gzip-compressed tar archive. This does not prove contents-level license completeness, source-offer adequacy, vendored dependency approval, reproducible generation, or equivalence with the successful external build baseline.

## Latest crates.io `servo` package

Observed through `cargo search servo --limit 5`, `cargo info servo --verbose`, and the crates.io API on 2026-07-17:

| Field | Observation |
|---|---|
| Package | `servo` |
| Version | `0.4.0` |
| crates.io URL | `https://crates.io/crates/servo/0.4.0` |
| Repository | `https://github.com/servo/servo` |
| Documentation | `https://docs.rs/servo/0.4.0` |
| License | `MPL-2.0` |
| Rust version | `1.88.0` |
| Created | 2026-07-16T12:14:01.753698Z |
| Updated | 2026-07-16T12:14:01.753698Z |
| Yanked | `false` |
| crates.io checksum | `01a05ffce7829e67e41c5cb4e10849924cbd781d0ea0d6332d81afe8476d8a89` |
| Local cached crate | `C:\Users\bcw19\.cargo\registry\cache\index.crates.io-1949cf8c6b5b557f\servo-0.4.0.crate` |
| Local cached crate size | `133634` |
| Local cached crate SHA-256 | `01A05FFCE7829E67E41C5CB4E10849924CBD781D0EA0D6332D81AFE8476D8A89` |

Default features:

| Feature set | Observation |
|---|---|
| `default` | `baked-in-resources`, `clipboard`, `js_jit` |
| Notable optional features | `bluetooth`, `gamepad`, `gstreamer`, `media-gstreamer`, `native-bluetooth`, `vello`, `webgpu`, `webxr`, JS diagnostics, and tracing |

Representative dependency posture from `cargo info`:

- many Servo crates are pinned as exact `=0.4.0` dependencies;
- `stylo` and `stylo_traits` are `0.19`;
- rendering/GPU dependencies include `webrender 0.69`, `webrender_api 0.69`, `mozangle 0.5.5`, and `surfman 0.13.0`;
- platform/runtime dependencies include `gaol 0.2.1`, `ipc-channel 0.22`, `accesskit 0.24.0`, `tokio 1`, and optional `gstreamer 0.25`.

Interpretation: crates.io exposes a current `servo 0.4.0` package with a verified local checksum, but it is not the same source object as the successful external build checkout or the `v0.3.0` GitHub release. The crate package is a Rust package surface, not a whole-repository source baseline or release-source archive. Its default `js_jit` feature also reinforces the unresolved conflict analysis required against Turing's Turing-owned JavaScript-runtime strategy.

## Source candidate comparison

| Candidate | Strength | Limitation |
|---|---|---|
| Successful external build baseline `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` | Built successfully on the reference Windows host; local tree, tracked-file count, manifest digest, and local archive digest are already captured | Two commits behind the historical 2026-07-17 `origin/main` observation; newer 2026-07-19 `main` commit has not been compared; not a release tag; no owner-selected source-baseline decision |
| Historical upstream `origin/main` `622600e045c2e5ea688a9b19b8671b6f43112817` | Fetched upstream main on 2026-07-17; GitHub commit verification reports valid | Not yet bootstrapped or built by Turing; shallow partial clone does not establish full history; superseded as the current-main observation by the 2026-07-19 refresh |
| GitHub release `v0.3.0` / `release/v0.3` | Immutable release tag and branch head observed at the same commit; release asset has GitHub digest and local digest match | Lightweight tag, no tag-object signature; release commit is unsigned; release source archive differs from the built main commit |
| GitHub vendored release source archive | Downloaded locally; size and SHA-256 match GitHub release metadata; archive is readable | Contents-level source/license review and reproducible-generation review are not done; archive is not the previously built source tree |
| crates.io `servo 0.4.0` | crates.io checksum matches local cached `.crate`; current package metadata is precise | Package is not a whole-repository source baseline; no full dependency, license, generated-output, or release equivalence decision |

## Decision implications

The safest current statement is:

- Turing has one successfully built external Servo source tree, at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`.
- That build baseline was two commits behind the historical 2026-07-17 fetched `origin/main` observation; the 2026-07-19 `main` refresh is later and has not been compared to the build baseline.
- The latest GitHub release is `v0.3.0`, on `release/v0.3`, at `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`.
- The latest crates.io package is `servo 0.4.0`, published 2026-07-16 with checksum `01a05ffce7829e67e41c5cb4e10849924cbd781d0ea0d6332d81afe8476d8a89`.
- These are four distinct source-candidate surfaces, and none is approved as Turing's source baseline.

`ADR-0009` must explicitly choose one of these baseline models, or reject all of them:

1. freeze the already built main-branch commit and accept that it is not current upstream or a release tag;
2. refresh to current `origin/main`, then rerun bootstrap, build, dependency, generated-output, source/archive, native, compatibility, and performance evidence;
3. use a GitHub release tag and source archive, then accept or reject the lightweight-tag and unsigned-commit provenance posture;
4. use crates.io package surfaces, then accept or reject the fact that package sources are not whole-repository release sources;
5. keep Servo as research only and proceed with a clean Turing-owned implementation plan.

## What this proves

This report proves, for the inspected date and host only:

- the successful external build baseline, current fetched upstream `main`, latest GitHub release tag, latest GitHub release source archive, and latest crates.io package are not the same source object;
- the successful external build baseline was two commits behind the historical 2026-07-17 fetched `origin/main` observation;
- the 2026-07-17 `origin/main` observation is historical; the 2026-07-20 API refresh identifies `f542a355e5565e380aa0570132d4138dde328bae` as a later `main` commit that has not been built or compared in Turing's evidence process;
- GitHub reports valid commit verification for the build baseline and current `origin/main` commits;
- `v0.3.0` is a lightweight tag pointing to an unsigned commit that also heads `release/v0.3`;
- the downloaded `servo-v0.3.0-src-vendored.tar.gz` matches GitHub's asset digest and is readable;
- the local cached `servo-0.4.0.crate` matches the crates.io API checksum.

## What this does not prove

This report does not prove:

- any Servo source baseline is approved for Turing;
- the shallow partial external checkout is full-history provenance evidence;
- GitHub commit verification, GitHub asset digest metadata, or crates.io checksums satisfy Turing's source-trust policy by themselves;
- release archive contents are complete, legally acceptable, reproducible, or equivalent to a selected source tree;
- crates.io `servo 0.4.0` is compatible with Turing's architecture, JavaScript-runtime ownership, security model, dependency policy, or release model;
- Servo is secure, compatible, accessible, low memory, high performance, Chrome-class, maintainable, or production-ready;
- `PB-002` can move out of blocked status.

## Resulting gate update

This report narrows `ADR9-EV-001` from a broad "upstream release/tag/archive comparison" gap to a sharper remaining decision:

1. an owner must select or reject a source-baseline model;
2. the selected model must receive a signed-tag or equivalent provenance decision;
3. the selected model must receive source-content, release-archive, and crates.io package equivalence rules where applicable;
4. if current `origin/main`, release archive, or crates.io package is selected, all existing build, dependency, generated-output, native, compatibility, and performance evidence must be rerun or explicitly scoped as stale;
5. all license, notice, source-offer, native-package, generated-output, unsafe, FFI, owner-reviewed component-boundary, JavaScript-runtime, security, maintenance, and public-claim gates remain blocked or partial until separately reviewed.

The follow-up [Servo Independent Source Verification - July 2026](servo-independent-source-verification-2026-07.md) captures independent non-shallow Git verification for the main, build-baseline, and release source objects. The follow-up [Servo Source Baseline Equivalence Policy Prep - July 2026](servo-source-baseline-equivalence-policy-2026-07.md) compares the release Git tree, vendored source archive, and crates.io package surfaces. Neither follow-up settles the remaining owner, provenance-policy, blob-review, or legal decisions.

## Affected records

This report adds evidence for `PB-002` and `ADR9-EV-001`, but it does not change `PB-002` blocked status or approve any `ADR-0009` option. It informs:

- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Independent Source Verification - July 2026](servo-independent-source-verification-2026-07.md);
- [Servo Source Baseline Equivalence Policy Prep - July 2026](servo-source-baseline-equivalence-policy-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Source bibliography](../blueprint-v1/18-source-bibliography.md);
- [Research Index](README.md);
- [Research Log](../research-log.md).

## Revisit triggers

Revisit this report when:

- `servo/servo` publishes a newer release, tag, or source archive;
- crates.io publishes a newer `servo` package or yanks `servo 0.4.0`;
- Turing chooses a baseline model for `ADR-0009`;
- the external build baseline is refreshed to current upstream;
- signed-tag policy, equivalent provenance policy, owner-accepted equivalence policy, or selected-baseline legal/blob review is completed;
- license/source-offer, dependency, native package, generated-output, unsafe/FFI, compatibility, performance, security, maintenance, or owner-review evidence changes.
