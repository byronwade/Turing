# Servo Source Baseline Equivalence Policy Prep - July 2026

Status: source-baseline equivalence policy preparation for `PB-002` and `ADR9-EV-001`; no source-baseline, provenance policy, release archive, crate package, dependency, or license approval
Owner: architecture, provenance, release operations, security, legal-review, engine, and documentation owners
Audit date: 2026-07-17
Confidence: high for file-count and path-set comparisons; medium for package-to-repository path equivalence; low for legal, source-offer, blob-content, release-reproducibility, dependency, generated-output, compatibility, performance, and adoption conclusions until owner reviews run

## Question

What source-content, release-archive, and crates.io package equivalence evidence exists for the Servo source candidates, and what policy decisions remain before `ADR-0009` can select or reject a source baseline?

This report does not import Servo source, release archives, crate archives, generated output, native binaries, build logs, or package contents into Turing. It does not approve a source baseline, release archive, crates.io package, dependency, license posture, or `ADR-0009` option.

## Scope

The report compares source surfaces already identified by the upstream provenance and independent verification reports:

- independent bare Servo clone: `C:\ts\servo-independent-source-verify-20260717.git`;
- vendored release source archive: `C:\ts\servo-upstream-source-provenance-20260717\servo-v0.3.0-src-vendored.tar.gz`;
- local crates.io cache: `C:\Users\bcw19\.cargo\registry\cache\index.crates.io-1949cf8c6b5b557f\servo-0.4.0.crate`;
- Git release tag `v0.3.0`;
- crates.io `servo 0.4.0` package metadata and `.cargo_vcs_info.json`.

The report does not compare every file's content hash against Git blobs, rebuild a source archive, validate third-party notices, approve vendored dependencies, run Cargo packaging checks, or choose a source baseline.

## Method

Commands and checks were run outside the Turing repository:

1. `git --git-dir=C:\ts\servo-independent-source-verify-20260717.git ls-tree -r --name-only <ref>` for Git tree path sets;
2. Python `tarfile` iteration over the vendored release archive and cached crates.io `.crate` package;
3. normalized path-set comparisons between the `v0.3.0` Git tree, vendored release archive, current `main`, and the `servo 0.4.0` crate package;
4. bounded reading of small metadata files such as `GIT_REVISION` and `.cargo_vcs_info.json`;
5. Git object verification for the crate package's recorded VCS commit.

No Servo source files, vendored dependencies, release archives, crate archives, generated output, native binaries, or logs were copied into Turing.

## Candidate source identities

| Candidate | Source identity |
|---|---|
| Successful external build baseline | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Current Servo `main` | `622600e045c2e5ea688a9b19b8671b6f43112817`, tree `9d71530fe4d36dd9c94a2a411d75f219fde0dfc9` |
| GitHub release tag and branch | `v0.3.0` / `release/v0.3` at `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, tree `c41b1defccd9ed47a5ac2a8ad40929bc34de80a0` |
| GitHub vendored release archive | `servo-v0.3.0-src-vendored.tar.gz`, SHA-256 `C75EFFBDC0AB6F86B318E28D139EB056268224E072A684492B49409C5221C871` |
| crates.io package | `servo 0.4.0`, SHA-256 `01A05FFCE7829E67E41C5CB4E10849924CBD781D0EA0D6332D81AFE8476D8A89` |
| crates.io package VCS commit | `e8dbc1dfbf6f58621346a5f61ab7a17d01387873`, tree `0d03fc5b2ab6ce9b868115010602940bc368c1a7` |

The crates.io package VCS commit resolved in the independent Git object graph and was committed on 2026-07-13T12:51:34+02:00 with subject `backport: deps: Update crossbeam-epoch from 0.9.18 to 0.9.20 (RUSTSEC-2026-0204) (#46324)`.

## Vendored release archive versus release Git tree

The vendored release archive records `GIT_REVISION` as:

```text
fb6c9d511f67a311f5883ec859aa0c5dd88d19c3
```

That matches the `v0.3.0` / `release/v0.3` commit object.

Path-set comparison:

| Surface | Count |
|---|---:|
| `v0.3.0` Git tree files | `191174` |
| Vendored archive total entries | `271973` |
| Vendored archive directories | `19384` |
| Vendored archive files | `252589` |
| Vendored archive file bytes | `2089732373` |
| Vendored files matching release Git paths | `191078` |
| Vendored files not in release Git paths | `61511` |
| Release Git files missing from vendored archive | `96` |

Top vendored archive roots by entry count:

| Root | Entries |
|---|---:|
| `tests` | `197217` |
| `vendor` | `71527` |
| `components` | `2629` |
| `support` | `216` |
| `python` | `195` |
| `ports` | `56` |
| `.github` | `40` |
| `resources` | `25` |
| `docs` | `18` |

Difference classification:

| Difference | Count | Examples or interpretation |
|---|---:|---|
| Vendored files not in Git release tree | `61511` | `61510` under `vendor/` plus `GIT_REVISION` |
| Git release files missing from vendored archive | `96` | `95` under `etc/` and `1` under `tests/` |

Representative files present in the vendored archive but not in the release Git tree include `vendor/ab_glyph-0.2.32/.cargo-checksum.json`, `vendor/ab_glyph-0.2.32/Cargo.toml`, and `vendor/ab_glyph-0.2.32/src/lib.rs`.

Representative Git release files missing from the vendored archive include `etc/about.hbs`, `etc/blink-perf-test-runner/README.md`, `etc/ci/bencher.py`, and `etc/ci/performance/README.md`.

Interpretation: the vendored source archive is not equivalent to the `v0.3.0` Git tree. It is a derived release source package with a matching `GIT_REVISION`, a large additional `vendor/` dependency tree, and a small set of omitted Git-tracked files. It can be a source candidate only if Turing defines and accepts a derived-archive equivalence policy and reviews the additional vendored source surface.

## crates.io `servo 0.4.0` package versus repository path

The cached `servo-0.4.0.crate` contains `.cargo_vcs_info.json`:

```json
{
  "git": {
    "sha1": "e8dbc1dfbf6f58621346a5f61ab7a17d01387873"
  },
  "path_in_vcs": "components/servo"
}
```

Package surface:

| Surface | Count |
|---|---:|
| `.crate` total entries | `34` |
| `.crate` files | `34` |
| `.crate` file bytes | `615491` |
| `components/servo` files at VCS commit | `30` |
| Crate files matching `components/servo` path | `30` |
| Crate files not in `components/servo` path | `4` |
| `components/servo` files missing from crate | `0` |

The four package-only files are:

- `.cargo_vcs_info.json`;
- `Cargo.lock`;
- `Cargo.toml`;
- `Cargo.toml.orig`.

Interpretation: the crates.io package is a normalized package for `components/servo` at VCS commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873`, not a whole-repository source baseline. It is strongly tied to that component path but cannot stand in for the full Servo tree, release archive, tests, vendor tree, native bootstrap inputs, or current external build baseline.

## Equivalence policy options

Turing should not treat these source surfaces as interchangeable without an accepted policy. The candidate policy choices are:

| Policy choice | What it would mean | Required evidence before use |
|---|---|---|
| Git tree baseline only | A specific Git commit/tree is the source baseline; archives and crates are derived artifacts | signed-tag or equivalent provenance rule, full tree identity, blob-content verification rule, build from that commit, dependency and generated-output evidence tied to that commit |
| Vendored release archive baseline | The upstream vendored source archive is the source baseline | digest verification, `GIT_REVISION` match, path-set delta review, vendored dependency SBOM, license/source-offer review, reproducible archive-generation evidence or accepted exception |
| crates.io component package baseline | The crates.io package is the source baseline for only `components/servo` | `.cargo_vcs_info.json` match, package normalization review, generated `Cargo.toml` versus original review, dependency/SBOM review, explicit scope that it is not a whole-engine baseline |
| Current `main` baseline | The moving upstream branch is pinned at a dated commit | independent non-shallow verification, current build reproduction, complete rerun of dependency/generated/native/compatibility/performance evidence |
| Built baseline freeze | The already built commit remains the source baseline for current evidence | explicit acceptance that it is behind current `main`, no release tag, no derived archive equivalence, and not current crates.io package |
| Research-only Servo | No Servo source baseline is accepted | clean-room research rules, standards/test-only implementation guidance, no Servo-derived release path |

## Recommended policy posture for decision prep

This report does not choose an `ADR-0009` option. For decision prep, the conservative posture is:

1. treat Git commits, release archives, vendored archives, and crates.io packages as separate source surfaces;
2. require an owner-selected source-baseline model before any later evidence is considered decision-grade;
3. require source-content, release-archive, and package-equivalence rules before reusing evidence across surfaces;
4. rerun build, dependency, generated-output, native, compatibility, and performance evidence whenever the selected baseline differs from the evidence baseline;
5. prohibit public or internal claims that Servo source is approved, compatible, high-performance, or production-safe until the selected baseline passes all affected `ADR-0009` evidence items.

## What this proves

This report proves, for the inspected date and host only:

- the vendored release source archive records the same `GIT_REVISION` as `v0.3.0`;
- the vendored release source archive is not path-equivalent to the `v0.3.0` Git tree;
- the vendored release archive adds a large `vendor/` source tree and omits a small set of Git-tracked files;
- the crates.io `servo 0.4.0` package is tied to repository path `components/servo` at commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873`;
- the crates.io package is path-equivalent to that component path plus Cargo package metadata, not to the whole Servo repository.

## What this does not prove

This report does not prove:

- any source baseline is selected or approved;
- the vendored archive is legally complete, reproducible, or acceptable as a Turing source baseline;
- the crates.io package is acceptable as a Turing source baseline;
- every vendored dependency is licensed, noticed, secure, current, source-offer-compliant, or buildable;
- GitHub release metadata, crates.io checksums, or path-set comparison are enough for source trust;
- Servo is compatible, secure, accessible, low memory, high performance, Chrome-class, maintainable, or production-ready;
- `PB-002` can move out of blocked status.

## Resulting gate update

This report narrows `ADR9-EV-001` by turning the vague content-equivalence gap into explicit source-surface rules and current evidence. `ADR9-EV-001` remains partial because the following decision-grade outputs are still missing:

1. owner-selected source-baseline model, or explicit rejection of all Servo source-baseline models;
2. signed-tag or equivalent provenance decision;
3. owner-accepted equivalence policy for Git tree, derived release archive, vendored dependency tree, and crates.io package surfaces;
4. full blob-content and legal/source-offer review for whichever baseline is selected;
5. rerun plan for build, dependency, generated-output, native, compatibility, and performance evidence if the selected baseline differs from `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`.

## Affected records

This report adds evidence for `PB-002` and `ADR9-EV-001`, but it does not change `PB-002` blocked status or approve any `ADR-0009` option. It informs:

- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Upstream Source Provenance - July 2026](servo-upstream-source-provenance-2026-07.md);
- [Servo Independent Source Verification - July 2026](servo-independent-source-verification-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Research Index](README.md);
- [Research Log](../research-log.md).

## Revisit triggers

Revisit this report when:

- `servo/servo` publishes a newer release, release source archive, or current `main`;
- crates.io publishes a newer `servo` package or yanks `servo 0.4.0`;
- Turing selects a source-baseline model for `ADR-0009`;
- Turing defines signed-tag, equivalent provenance, content-equivalence, source-offer, or vendored-dependency policy;
- an accepted baseline requires a refreshed build, dependency graph, generated-output audit, native bootstrap audit, compatibility corpus, or performance baseline.
