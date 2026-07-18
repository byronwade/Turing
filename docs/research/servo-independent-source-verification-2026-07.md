# Servo Independent Source Verification - July 2026

Status: independent non-shallow source-verification report for `PB-002` and `ADR9-EV-001`; no source-baseline, dependency, release archive, or license approval
Owner: architecture, provenance, release operations, security, legal-review, engine, and documentation owners
Audit date: 2026-07-17
Confidence: high for independently fetched Git object IDs, refs, ancestry counts, tree IDs, and file counts; medium for local signature posture; low for source approval, full source-contents review, legal approval, release reproducibility, compatibility, performance, and adoption conclusions until owner reviews run

## Question

Can Turing independently verify Servo's current `main`, the successful external build baseline, and the latest GitHub release source objects from a non-shallow Git fetch, and what remains before `ADR-0009` can select a source baseline?

This report does not import Servo source into Turing. It does not approve a Servo source baseline, release archive, crates.io package, dependency, license posture, or any `ADR-0009` option.

## Scope

The report covers a fresh independent bare partial clone:

```text
C:\ts\servo-independent-source-verify-20260717.git
```

The clone is:

- independent from the successful external build checkout at `C:\ts\servo`;
- bare, so it has no working tree checkout;
- non-shallow, so ancestry counts are meaningful;
- partial with `blob:none`, so it verifies commit, tag, tree, and path identity without materializing all source blobs.

The report does not cover:

- full blob-content hashing for every source file;
- legal, notice, source-offer, or license review;
- release-archive contents comparison;
- crates.io package unpacking review;
- generated-output, native-package, unsafe, FFI, compatibility, performance, security-model, or maintenance review;
- owner selection of a source baseline.

## Method

Commands were run outside the Turing repository:

1. `git clone --filter=blob:none --bare https://github.com/servo/servo.git C:\ts\servo-independent-source-verify-20260717.git`;
2. `git --git-dir=<repo> rev-parse`, `config`, `count-objects`, `show`, `rev-list`, `merge-base`, `ls-tree`, `for-each-ref`, `tag -v`, and `verify-commit`;
3. `git --git-dir=<repo> fsck --connectivity-only`;
4. `git -C C:\ts\servo-independent-source-verify-20260717 ls-remote origin refs/heads/main refs/heads/release/v0.3 refs/tags/v0.3.0` from the separate no-checkout clone as an additional remote-ref check.

No Servo source files, release archives, crate archives, generated outputs, native binaries, or build logs were copied into Turing.

## Clone identity

| Field | Observation |
|---|---|
| Repository path | `C:\ts\servo-independent-source-verify-20260717.git` |
| Bare repository | `true` |
| Shallow repository | `false` |
| Remote URL | `https://github.com/servo/servo.git` |
| Promisor remote | `true` |
| Partial-clone filter | `blob:none` |
| Object store | `509771` objects in `1` pack |
| Packed object size | `148.47 MiB` |
| `git fsck --connectivity-only` | exit `0`; reported `82` dangling commits and `153` dangling trees |

Interpretation: this is stronger source-history evidence than the earlier successful build checkout, which was shallow. The dangling objects do not make the connectivity check fail, but they should remain visible in the provenance record.

## Ref identity

Local refs from the independent bare clone:

| Ref | Object type | Object ID | Committer date |
|---|---|---|---|
| `refs/heads/main` | `commit` | `622600e045c2e5ea688a9b19b8671b6f43112817` | 2026-07-17 17:01:59 +0000 |
| `refs/heads/release/v0.3` | `commit` | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` | 2026-06-04 20:29:05 +0200 |
| `refs/tags/v0.3.0` | `commit` | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` | 2026-06-04 20:29:05 +0200 |

Remote-ref check:

| Remote ref | Object ID |
|---|---|
| `refs/heads/main` | `622600e045c2e5ea688a9b19b8671b6f43112817` |
| `refs/heads/release/v0.3` | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` |
| `refs/tags/v0.3.0` | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` |

Interpretation: the independent clone agrees with the remote-ref query and the upstream source provenance report for current `main`, `release/v0.3`, and `v0.3.0`.

## Current `main`

| Field | Observation |
|---|---|
| Commit | `622600e045c2e5ea688a9b19b8671b6f43112817` |
| Tree | `9d71530fe4d36dd9c94a2a411d75f219fde0dfc9` |
| Commit date | 2026-07-17T17:01:59Z |
| Commit subject | `script: Optimize element::has_class() (#46594)` |
| Rev-list count on `main` | `57285` |
| Tree file count | `193033` |

Interpretation: current fetched `main` remains the same as the upstream provenance report and is now verified from a non-shallow object graph. It is not the already built source baseline.

## Successful external build baseline

| Field | Observation |
|---|---|
| Commit | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Tree | `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Commit date | 2026-07-17T15:50:14Z |
| Commit subject | `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)` |
| Relation to current `main` | `rev-list --left-right --count <build>...main` returned `0 2` |
| Merge base with current `main` | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Tree file count | `193033` |

Interpretation: the successful external build baseline is an ancestor of current `main` and is exactly two commits behind it. A decision to use current `main` requires rerunning build, dependency, generated-output, native, compatibility, and performance evidence because the current built artifact was produced from the older tree.

## Latest GitHub release tag and branch

| Field | Observation |
|---|---|
| Tag ref | `refs/tags/v0.3.0` |
| Tag object type | `commit` |
| Tag/branch commit | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3` |
| Release branch | `refs/heads/release/v0.3` points to the same commit |
| Tree | `c41b1defccd9ed47a5ac2a8ad40929bc34de80a0` |
| Commit date | 2026-06-04T20:29:05+02:00 |
| Commit subject | `release: Use stylo 0.18 for 0.3 release` |
| Relation to current `main` | `rev-list --left-right --count v0.3.0...main` returned `1 838` |
| Merge base with current `main` | `61628bb173a5f546688403706c13eac294c1ee84` |
| Tree file count | `191174` |

Interpretation: `v0.3.0` is not an ancestor of current `main` and current `main` is not a simple fast-forward from the release tag. The release branch has one commit not present on current `main`, while current `main` has 838 commits not present on the release tag side of the comparison. A release-source baseline therefore needs its own build and evidence path.

## Signature posture

| Object | Local verification result |
|---|---|
| `v0.3.0` tag | `git tag -v v0.3.0` failed because the ref is a lightweight commit tag, not a tag object |
| Build baseline commit `4a0b2b1a...` | `git verify-commit` found a signature made with RSA key `B5690EEEBB952194`, but exited `1` because the local keyring did not have the public key |
| Current `main` commit `622600e0...` | `git verify-commit` found a signature made with RSA key `B5690EEEBB952194`, but exited `1` because the local keyring did not have the public key |
| Release commit `fb6c9d51...` | `git verify-commit` exited `1`; no local signature details were printed |

Earlier GitHub API checks reported valid GitHub commit verification for the build baseline and current `main` commits, and unsigned status for the release commit. Local Git verification does not replace that GitHub metadata because the local GPG trust root was not configured.

Interpretation: Turing still needs a signed-tag or equivalent provenance policy. A GitHub-verified merge commit is useful source identity evidence, but it is not the same as a signed release tag or a Turing-owned provenance rule.

## What this proves

This report proves, for the inspected date and host only:

- a separate non-shallow bare partial clone can independently fetch Servo's Git object graph;
- current `main`, the successful external build baseline, and `v0.3.0` resolve to the same object IDs and tree IDs recorded in the upstream provenance report;
- the successful external build baseline is exactly two commits behind current `main` in the non-shallow clone;
- `v0.3.0` is a lightweight commit tag, points to the same commit as `release/v0.3`, and has a distinct relationship to current `main`;
- the release tag path and current `main` path cannot share a single build/performance/compatibility evidence bundle without explicit scoping.

## What this does not prove

This report does not prove:

- any source baseline is selected or approved;
- partial-clone tree verification is full blob-content verification;
- commit signatures are trusted under Turing policy;
- GitHub's commit verification is an accepted substitute for a signed release tag;
- release source archive contents are approved as equivalent to the release Git tree or legally complete;
- crates.io package contents are equivalent to a repository source baseline;
- Servo is secure, compatible, accessible, low memory, high performance, Chrome-class, maintainable, or production-ready;
- `PB-002` can move out of blocked status.

## Resulting gate update

This report narrows `ADR9-EV-001` by completing an independent non-shallow Git verification for the main source candidates. `ADR9-EV-001` remains partial because the following decision-grade outputs are still missing:

1. owner-selected source-baseline model, or explicit rejection of all Servo source-baseline models;
2. signed-tag or equivalent provenance policy;
3. owner-accepted blob-content, release-archive, and crates.io package equivalence policy for whichever baseline is selected;
4. rerun plan for build, dependency, generated-output, native, compatibility, and performance evidence if the selected baseline differs from `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
5. legal, notice, source-offer, advisory, generated-code, unsafe, FFI, owner-reviewed component-boundary, JavaScript-runtime, security, maintenance, and public-claim reviews.

## Affected records

This report adds evidence for `PB-002` and `ADR9-EV-001`, but it does not change `PB-002` blocked status or approve any `ADR-0009` option. It informs:

- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Source Baseline Equivalence Policy Prep - July 2026](servo-source-baseline-equivalence-policy-2026-07.md);
- [Servo Upstream Source Provenance - July 2026](servo-upstream-source-provenance-2026-07.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Research Index](README.md);
- [Research Log](../research-log.md).

## Revisit triggers

Revisit this report when:

- `servo/servo` publishes a newer `main`, release branch, or tag;
- Turing selects a source-baseline model for `ADR-0009`;
- Turing defines a signed-tag or equivalent provenance policy;
- an owner-accepted equivalence policy, full blob-content verification, release-archive equivalence check, or crates.io package equivalence check runs;
- a selected baseline requires a refreshed Servo build, dependency graph, generated-output audit, native bootstrap audit, compatibility corpus, or performance baseline.
