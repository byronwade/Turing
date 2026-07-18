# Servo Native Package Decision Prep - July 2026

Status: dated decision-prep evidence for `ADR9-EV-005` and `ADR9-EV-006`; no native package, source-build, binary-package exception, license, advisory, codec, patent, package-manifest, SBOM, or redistribution approval
Owner: release operations, security, provenance, legal-review, media, architecture, and documentation owners
Retrieval date: 2026-07-17
Confidence: medium for observed Windows bootstrap assets, local hashes, signature posture, copied-package rules, and package counts; low for source-build feasibility, legal approval, advisory status, deterministic download policy, and release-package conclusions until owner review completes

## Question

What native source-build, binary-package exception, deterministic-download verification, package-minimization, notice, and manifest decisions remain before `ADR-0009` can select any Servo relationship that reaches Servo's Windows bootstrap or media package surface?

This report prepares decisions. It does not approve Servo bootstrap artifacts, GStreamer, moztools, MSYS2-derived tools, codec libraries, crypto libraries, `servo-build-deps`, winget packages, ANGLE DLLs, MSVC redistributables, Windows SDK DLLs, or any native binary for Turing release code.

## Scope

Included:

- external Servo checkout at `C:\ts\servo`;
- Servo Windows bootstrap and packaging source behavior;
- `servo/servo-build-deps` release metadata for tag `msvc-deps`;
- locally downloaded `moztools-4.0.zip` and GStreamer MSVC `1.22.8` assets under `C:\ts\servo-native-artifacts-msvc-deps`;
- extracted dependency tree counts under `C:\ts\servo\target\dependencies`;
- selected signature, license-directory, plugin-list, and debug-output package facts.

Excluded:

- legal approval;
- native advisory scan;
- source-build reproduction for any native package;
- binary-package exception approval;
- package minimization approval;
- release package generation;
- copying external native packages, logs, generated output, or Servo source into Turing.

## Evidence Inputs

| Input | Observation |
|---|---|
| Servo remote | `https://github.com/servo/servo.git` |
| External checkout head | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| External checkout tree | `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Checkout state | `## main...origin/main [behind 2]`; shallow repository |
| Bootstrap source report | [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md) |
| Release metadata command | `gh release view msvc-deps --repo servo/servo-build-deps --json tagName,publishedAt,url,assets` |
| Local native asset cache | `C:\ts\servo-native-artifacts-msvc-deps` |
| Extracted dependency tree | `C:\ts\servo\target\dependencies` |
| Debug build output | `C:\ts\servo\target\debug` |

The checkout being behind `origin/main` means this is a dated build-baseline snapshot. Any owner-selected source baseline or Servo bootstrap source different from `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` needs a rerun.

## Bootstrap Source Behavior

The inspected Windows bootstrap source uses `https://github.com/servo/servo-build-deps/releases/download/msvc-deps` as `DEPS_URL`, selects `moztools` version `4.0`, downloads `gstreamer-1.0-msvc-x86_64-1.22.8.msi` and `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi`, and extracts packages under `target\dependencies`.

Observed decision-relevant behavior:

- `download_and_extract_dependency()` downloads `{full_spec}.zip`, extracts it, and removes the ZIP after extraction;
- `_platform_bootstrap_gstreamer()` downloads both GStreamer MSIs into a temporary directory and runs `msiexec.exe /a ... TARGETDIR=<dependencies> /qn`;
- `util.download_file()` supports `.part` resume behavior;
- `util.check_hash()` exists, but the inspected Windows `moztools` and GStreamer bootstrap call sites did not provide expected hashes or signatures;
- `_winget_import()` imports `Kitware.CMake`, `LLVM.LLVM`, `Ninja-build.Ninja`, and `WiXToolset.WiXCLI`;
- only `WiXToolset.WiXCLI` is pinned in the inspected `winget.json`, at version `7.0.0.0`;
- `_ensure_llvm_in_user_path()` can persistently append LLVM to the user `PATH`.

Interpretation: this is acceptable developer-bootstrap evidence, not release-input policy. A Turing release path needs pinned versions, expected hashes, source provenance, mirrors, freshness and revocation rules, and no uncontrolled persistent host mutation.

## Upstream Asset Decision Queue

The relevant `servo-build-deps` release tag is `msvc-deps`, published `2023-04-20T07:41:51Z`. The GitHub release metadata observed for the relevant assets exposed `digest: null`.

| Asset | GitHub size | GitHub updated | GitHub digest | Local SHA-256 | Authenticode status |
|---|---:|---|---|---|---|
| `moztools-4.0.zip` | `143306382` | `2023-09-09T08:46:06Z` | `null` | `CCEB354767EF3DAD8813E63CB95ED081814225BF5FA15BFA083AA8B31A339153` | `UnknownError` |
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | `127258624` | `2024-01-03T09:08:57Z` | `null` | `37F9973FE5C720CE1F1602E7E599336384B9FF3E4878817987DD6B77265F17BB` | `NotSigned` |
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | `225861632` | `2024-01-03T09:08:47Z` | `null` | `2D0CF6E89CF88D94E670CD81087C002408161D1C8843C00D3F27D33CE254C523` | `NotSigned` |

Local hashes are useful identity evidence. They are not enough for a Turing binary-package exception unless owners also accept the source, redistribution terms, advisory posture, update path, mirror policy, and deterministic verification behavior.

## Extracted Package Surface

Observed extracted dependency roots:

| Root entry | Kind | Files | Bytes | SHA-256 if file |
|---|---|---:|---:|---|
| `gstreamer` | directory | `4630` | `1234821863` | n/a |
| `moztools` | directory | `14824` | `344561599` | n/a |
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | file | `1` | `1302528` | `B83B7C4107257511AF301EB78992B560D8B631D8433872C721448096ABDB6C1E` |
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | file | `1` | `2023424` | `B9D603E73AB5A12884C593446E25D03FE0E9A8344FA9C03CA206575D819864CE` |

The extracted-tree GStreamer `.msi` files are post-install or administrative-install artifacts, not the original upstream downloads.

Authenticode checks over extracted `.dll`, `.exe`, and `.msi` files under `target\dependencies` found:

| Status | Files | Bytes |
|---|---:|---:|
| `NotSigned` | `981` | `525775835` |
| `Valid` | `1` | `428224` |

The one valid signed extracted file observed in the prior native audit was `moztools\4.0\bin\vswhere.exe`, signed by Microsoft.

## License and Notice Surface

Package-directory license roots observed:

| Root | Directories | Files | Bytes |
|---|---:|---:|---:|
| `gstreamer\1.0\msvc_x86_64\share\licenses` | `69` | `155` | `1141093` |
| `moztools\4.0\msys2\usr\share\licenses` | `24` | `28` | `178136` |

The broader native audit also recorded `374` license-like files across GStreamer and moztools when including documentation and package-specific notice locations. Turing needs final notice/source-offer generation from the selected release package manifest, not from a directory count alone.

High-review examples from the observed surface include FFmpeg-family libraries, OpenSSL libraries, x264, OpenH264, LAME, libjpeg-turbo, harfbuzz, fontconfig, freetype, cairo, zlib, bzip2, MSYS2 tools, 7-Zip, UPX, Watchman, SQLite, xz, and zstd.

## Runtime Copy and Package-Minimization Surface

Servo's Windows GStreamer packaging source defines:

- `29` Windows dependency DLL names;
- `21` GStreamer base library names;
- `36` Windows plugin names from `common.rs.in` plus `windows.rs.in`;
- `86` total GStreamer copy candidates before transitive dependency and package availability checks.

The plugin-list inputs had these hashes:

| Source | String count | SHA-256 |
|---|---:|---|
| `common.rs.in` | `35` | `509F9C5F200DC031C3A4C6D990E25505CF5AFFF7A88294B84E884E3408FEDD12` |
| `windows.rs.in` | `1` | `A4CE2475F5885B0825DF5B0B7FCB5872F2FFAE7ACF128CCCB142B25CCBC64E19` |

First plugin examples were `gstcoreelements`, `gstnice`, `gstapp`, `gstaudioconvert`, `gstaudioresample`, `gstgio`, `gstogg`, `gstopengl`, `gstopus`, `gstplayback`, `gsttheora`, and `gsttypefindfunctions`. The Windows-only plugin was `gstwasapi`.

The external debug build output under `target\debug` contained:

| Extension | Files | Bytes |
|---|---:|---:|
| `.dll` | `146` | `289684712` |
| `.exe` | `208` | `770920448` |
| `.pdb` | `263` | `4162707456` |

This is a debug-output footprint, not a release package. It still proves the release package manifest cannot be left implicit.

## Package Family Decision Matrix

| Family | Observed role | Default decision posture | Required owner decision |
|---|---|---|---|
| Winget bootstrap tools | developer bootstrap for CMake, LLVM, Ninja, WiX | build-host convenience only | pinned versions, hashes, offline/mirror policy, or replacement bootstrap |
| `servo-build-deps` release | upstream package distribution point | unapproved source of binaries | accepted source provenance, release trust, mirror, revocation, and freshness policy |
| `moztools-4.0.zip` | build tools and MSYS2-derived utilities | unapproved build-time binary package | source-build recipe or binary-package exception, advisory scan, notices, update path |
| GStreamer runtime MSI | media/runtime native package | unapproved runtime binary package | source-build recipe or binary-package exception, codec/patent/legal/advisory review |
| GStreamer development MSI | headers/import libraries/tools | unapproved build-time/development package | source-build recipe or binary-package exception, final release exclusion or inclusion rule |
| GStreamer copied DLLs/plugins | possible runtime package surface | unapproved package contents | exact final manifest, minimization, sandbox, codec, notice, and SBOM decisions |
| FFmpeg/libav and codec DLLs | media decode/encode and containers | high-review surface | codec/patent, legal, advisory, sandbox, and update decisions |
| OpenSSL/crypto DLLs | crypto/TLS-related native libraries in package tree | high-review surface | advisory, FIPS/non-FIPS, update, origin, and replacement decisions |
| ANGLE/GPU DLLs | copied build output for graphics paths | unapproved generated/native build output | source provenance, build reproducibility, GPU sandbox, package manifest decision |
| MSVC redistributables and Windows SDK DLLs | platform runtime copying | platform-redistribution surface | redistribution terms, installer model, update model, and exclusion/inclusion rule |
| Debug symbols and PDBs | developer/debug output | not release package by default | symbol server, stripping, retention, privacy, and crash-report policy |

## Deterministic Download Verification Proposal

`ADR9-EV-006` should not be closed until a reviewed bootstrap policy requires all native downloads to:

1. declare package name, version, source URL, source owner, expected size, expected SHA-256, and expected signature posture;
2. fail closed when an expected hash, signature, size, asset ID, or source URL does not match;
3. record retrieval date, TLS source, release/tag identity, asset ID, and mirror identity;
4. validate final content after any resumed `.part` download;
5. avoid relying on GitHub release metadata when `digest` is `null` unless an accepted alternate attestation exists;
6. use a Turing-controlled cache or mirror policy for release inputs;
7. define freshness, revocation, deletion, and emergency replacement behavior;
8. preserve success and failure logs outside the source tree;
9. rerun on an independent host or clean VM for the selected baseline.

## Release Package Manifest Requirements

Before any Servo-related native surface can enter a Turing release path, each native package or copied file needs a manifest record with:

- package family and package name;
- exact version and selected source baseline;
- build-only or shipped-runtime role;
- source URL, release tag, asset ID, and source owner;
- source-build recipe ID or binary-package exception ID;
- expected hash and signature posture;
- final package path and copier script/source;
- license ID, notice path, source-offer obligation, and patent/codec note;
- advisory status and update owner;
- sandbox/process role and exposed attack surface;
- SBOM component identifier;
- owner, reviewer, expiry date, and rerun trigger.

## What This Proves

- The native package surface has a concrete decision structure for `ADR9-EV-005` and `ADR9-EV-006`.
- The relevant Servo Windows bootstrap downloads are identified by URL family, asset name, local hash, size, and signature posture.
- The inspected bootstrap path does not give Turing release-grade hash/signature verification for the relevant native downloads.
- The extracted dependency tree and debug output are large enough that package minimization and final manifests are mandatory.
- GStreamer, moztools, winget, platform redistributables, codec libraries, crypto libraries, and debug symbols each require separate decisions.

## What This Does Not Prove

- source-build feasibility;
- binary-package exception approval;
- legal or advisory clearance;
- codec or patent approval;
- final notice/source-offer completeness;
- deterministic bootstrap reproduction;
- release package contents;
- native sandbox safety;
- performance, compatibility, accessibility, daily-driver, or Chrome-class readiness.

## Gate Impact

`PB-002` remains blocked.

`ADR9-EV-005` remains partial. Existing evidence now includes this native package decision-prep report, but source-build recipes, binary-package exception records, package-minimization decisions, legal/advisory review, and owner approvals remain missing.

`ADR9-EV-006` remains partial. Existing evidence now includes a deterministic-download policy proposal, but accepted hash/signature/mirror policy, implementation, and independent replay evidence remain missing.

## Affected Records

- [`docs/README.md`](../README.md)
- [`docs/research/README.md`](README.md)
- [`docs/repository-map.md`](../repository-map.md)
- [`docs/research-log.md`](../research-log.md)
- [`docs/project-buildout/11-pre-build-readiness-checklist.md`](../project-buildout/11-pre-build-readiness-checklist.md)
- [`docs/project-buildout/13-build-readiness-operating-board.md`](../project-buildout/13-build-readiness-operating-board.md)
- [`docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`](../project-buildout/14-adr-0009-source-strategy-decision-packet.md)
- [`docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`](../project-buildout/15-adr-0009-evidence-traceability-matrix.md)
- [`docs/blueprint-v1/machine/pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [`docs/research/servo-native-bootstrap-provenance-audit-2026-07.md`](servo-native-bootstrap-provenance-audit-2026-07.md)

## Next Experiments

1. Select the exact Servo source baseline and feature profile for the native package review.
2. Draft source-build recipes or binary-package exception records for `moztools-4.0.zip`, both GStreamer MSIs, MSYS2-derived tools, codec/crypto libraries, ANGLE DLLs, MSVC redistributables, and Windows SDK DLLs.
3. Build a trial native package manifest outside the Turing source tree and compare it against copied debug output, GStreamer plugin lists, bootstrap logs, and the native dependency tree.
4. Draft deterministic native download verification rules and test them against the three observed upstream assets.
5. Run native legal/advisory/notice review against the selected manifest.
6. Repeat bootstrap and package capture on an independent Windows host or clean VM.
