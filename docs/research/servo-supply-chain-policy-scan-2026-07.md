# Servo Supply-Chain Policy Scan — July 2026

Status: dated external supply-chain scan for `PB-002` and proposed `ADR-0009`; no dependency approval
Owner: security, provenance, release operations, architecture, and engine owners
Scan date: 2026-07-17
Confidence: medium for `cargo-deny` policy results against Servo's own config; low for legal, native binary, generated-code, unsafe, and adoption conclusions until Turing-specific reviews run

## Question

Does the clean external Servo checkout pass its own advisory, license, ban, and source policy checks, and what supply-chain evidence remains before Turing can make a source-strategy decision?

This scan does not approve Servo, Stylo, MozJS, WebRender, GStreamer, or any transitive dependency for Turing release code.

Follow-up reports record the same checkout's [Servo License Advisory and SBOM Decision Prep - July 2026](servo-license-advisory-decision-prep-2026-07.md), [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md), [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md), and [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md).

## Inputs

External checkout:

- workspace: `C:\ts\servo`;
- remote: `https://github.com/servo/servo.git`;
- commit: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- commit date: 2026-07-17T15:50:14Z;
- tracked-file status: clean after bootstrap, build, metadata extraction, and scan.

Tools and policy files:

- `cargo-deny 0.19.0`;
- `C:\ts\servo\deny.toml`;
- `C:\ts\servo\about.toml`;
- `C:\ts\servo\Cargo.lock`;
- metadata files from the [Servo Dependency and Provenance Inventory](servo-dependency-provenance-inventory-2026-07.md).

Input hashes:

| File | SHA-256 |
|---|---|
| `C:\ts\servo\Cargo.lock` | `327FDD559E87B0D18A4B24B201D9254E06C56D59C38388EDD37236F25BA47E22` |
| `C:\ts\servo\deny.toml` | `034CA60C05E2CCF9D22FD1BC617338BB5A094546AF711E3DA64B0B671AD04FE5` |
| `C:\ts\servo\about.toml` | `8DDB21BB7A14081C4016BFDB2C9EF48DDB0A09B16B8B3CE1B0C897B7D790EDAE` |
| `C:\ts\servo-metadata-default.json` | `01314363C1E5F7375B5C0024D8C698C8C46EA1F6858CA945CE5560F17F5B3F11` |
| `C:\ts\servo-metadata-all-features.json` | `7E9DB6EFD7BFBB370B57EE72DEF52E8C3D025FF4C602F461444530591C37CB3F` |

## Commands

```powershell
cargo deny check all --show-stats --metadata-path C:\ts\servo-metadata-default.json *> C:\ts\servo-cargo-deny-default.log
cargo deny check all --show-stats --metadata-path C:\ts\servo-metadata-all-features.json *> C:\ts\servo-cargo-deny-all-features.log
```

Both commands used Servo's `deny.toml` from the external checkout. They did not use Turing policy.

## Cargo-deny results

| Metadata profile | Exit code | Advisories | Bans | Licenses | Sources |
|---|---:|---|---|---|---|
| Default metadata | 0 | 0 errors, 0 warnings, 24 notes | 0 errors, 11 warnings, 124 notes | 0 errors, 0 warnings, 987 notes | 0 errors, 0 warnings, 11 notes |
| All-features metadata | 0 | 0 errors, 0 warnings, 24 notes | 0 errors, 0 warnings, 138 notes | 0 errors, 0 warnings, 1036 notes | 0 errors, 0 warnings, 11 notes |

The default metadata warnings were unnecessary duplicate-skip entries in Servo's `deny.toml` for packages that only had one resolved version in that profile: `jni`, `rand_chacha`, `bit-set`, `naga`, `wgpu-core`, `wgpu-core-deps-apple`, `wgpu-core-deps-emscripten`, `wgpu-core-deps-windows-linux-android`, `wgpu-hal`, `wgpu-naga-bridge`, and `wgpu-types`.

## Servo policy posture

Servo's `deny.toml` allows these license identifiers for the scan:

- `Apache-2.0 WITH LLVM-exception`;
- `Apache-2.0`;
- `BSD-2-Clause`;
- `BSD-3-Clause`;
- `BSL-1.0`;
- `CC0-1.0`;
- `CDLA-Permissive-2.0`;
- `ISC`;
- `MIT`;
- `MPL-2.0`;
- `OFL-1.1`;
- `Ubuntu-font-1.0`;
- `Unicode-3.0`;
- `Zlib`.

It also grants a crate-specific `NCSA` exception for `libfuzzer-sys`.

Servo's `deny.toml` denies multiple versions by default but contains an extensive skip list for known duplicates. The default metadata still had 58 duplicate-version package names, and all-features metadata had 69. Passing Servo policy therefore means "duplicates are either absent or covered by Servo exceptions," not "there are no duplicate versions."

Servo's source policy allows GitHub sources from the `servo` organization. The only git-sourced packages in the metadata are the 11 Stylo packages from `https://github.com/servo/stylo` at `d3de91cbac7bba38e159239b3c0a360783fce2ee`.

## Advisory exceptions

Servo's advisory configuration explicitly ignores these RustSec advisories:

| Advisory | Servo note category |
|---|---|
| `RUSTSEC-2024-0436` | `paste` unmaintained |
| `RUSTSEC-2025-0075` | `unic-char-range` unmaintained |
| `RUSTSEC-2025-0080` | `unic-common` unmaintained |
| `RUSTSEC-2025-0081` | `unic-char-property` unmaintained |
| `RUSTSEC-2025-0098` | `unic-ucd-version` unmaintained |
| `RUSTSEC-2025-0100` | `unic-ucd-ident` unmaintained |
| `RUSTSEC-2023-0071` | `rsa` Marvin Attack side-channel; waiting for stable upstream patch |
| `RUSTSEC-2025-0141` | `bincode` unmaintained; pinned in Servo |
| `RUSTSEC-2026-0192` | `ttf-parser` unmaintained |
| `RUSTSEC-2026-0194` | `quick-xml` duplicate-attribute quadratic runtime |
| `RUSTSEC-2026-0195` | `quick-xml` namespace-declaration memory exhaustion |
| `RUSTSEC-2026-0206` | `rustybuzz` unmaintained |

Turing cannot inherit those ignores without its own owner review. The ignored advisories are especially relevant because they touch cryptography, XML parsing, font/text handling, and general maintenance posture.

## Lockfile checksum posture

`Cargo.lock` contained:

- `1120` package entries;
- `1034` registry entries with checksums;
- `11` git entries without Cargo checksums because they are pinned by git source and revision;
- `75` path entries from Servo workspace packages.

The 11 sourced entries without checksums are the Stylo git packages listed in the dependency/provenance inventory. A Turing decision packet still needs source archive digests or equivalent attestation for Servo and Stylo, not only commit IDs.

## Native bootstrap artifacts

Servo bootstrap downloaded and unpacked native Windows dependencies under `C:\ts\servo\target\dependencies`.

Observed aggregate:

- total files under `target\dependencies`: `19456`;
- total size: `1582709414` bytes;
- selected native/package/debug files: `1291`;
- selected native/package/debug size: `864021659` bytes;
- selected extensions: `537` `.dll`, `443` `.exe`, `309` `.pdb`, and `2` `.msi`.

Extracted-tree GStreamer MSI artifact hashes:

| File | Size | SHA-256 |
|---|---:|---|
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | 1302528 | `B83B7C4107257511AF301EB78992B560D8B631D8433872C721448096ABDB6C1E` |
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | 2023424 | `B9D603E73AB5A12884C593446E25D03FE0E9A8344FA9C03CA206575D819864CE` |

Follow-up native bootstrap audit confirmed these are smaller post-install artifacts under `target\dependencies`, not the original upstream downloads. The original upstream asset sizes, hashes, and signature status are recorded in the [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md).

Examples of unpacked native/runtime files include FFmpeg-family DLLs, GStreamer DLLs and tools, OpenSSL DLLs, font/text libraries, image/audio/video codec DLLs, GLib/GIO/GObject files, Direct3D/GPU-related GStreamer DLLs, and `moztools` 7-Zip binaries.

This native bootstrap surface is too large to treat as an implementation detail. It needs license, advisory, provenance, sandbox, codec/patent, update, and packaging review before any Servo-derived or selective-component release path can be considered.

## Interpretation

The scan is useful but narrow:

- Servo passes its own `cargo-deny` policy for the inspected metadata profiles.
- Servo's policy intentionally ignores 12 RustSec advisories and permits many duplicate-version exceptions.
- Cargo checksums cover registry packages, not git/path source or downloaded native bootstrap packages.
- The Windows bootstrap pulls a large native media/tooling surface outside Cargo's normal registry checksum model.
- Turing's current security ledgers still correctly show no Servo dependency, native code, unsafe code, or provenance attestation because nothing was imported.

## Remaining Turing-specific review

Before `PB-002` can move out of blocked status, Turing still needs:

1. a Turing-owned license policy comparison against Servo's allowed licenses and exceptions, using the license/advisory/SBOM decision-prep queue as input;
2. full license text and notice generation, including GStreamer, moztools, and unpacked native files;
3. advisory review for Servo's ignored RustSec entries and native binary packages;
4. owner-selected source-baseline policy, source-content/release-archive/package equivalence, and source-build/source-offer decisions beyond the local Servo, Stylo, registry-cache, upstream source, extracted-tree GStreamer MSI, and native bootstrap asset digests already captured;
5. source-build versus binary-package policy for GStreamer, moztools, and other native dependencies;
6. generated-code, build-script, proc-macro, unsafe, and FFI classifications;
7. owner-reviewed component-boundary analysis before any selective reuse option, using the first-pass boundary report as input;
8. sandbox, codec, media, GPU, JavaScript-runtime, and storage-specific risk review.

## Affected records

This scan adds evidence for `PB-002` but does not change its blocked status. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Dependency and Provenance Inventory — July 2026](servo-dependency-provenance-inventory-2026-07.md);
- [Servo License Advisory and SBOM Decision Prep - July 2026](servo-license-advisory-decision-prep-2026-07.md);
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md);
- [Servo Source Strategy Inventory — July 2026](servo-source-strategy-inventory-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md);
- [Build, release, distribution, and operations](../blueprint-v1/13-build-release-operations.md).
