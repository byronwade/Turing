# Servo Source and Archive Provenance Audit - July 2026

Status: dated external source/archive provenance audit for `PB-002` and proposed `ADR-0009`; no source, dependency, native package, or license approval
Owner: architecture, security, provenance, release operations, engine, and embedding owners
Audit date: 2026-07-17
Confidence: medium for local Git, Cargo cache, and Windows bootstrap artifact identity; low for adoption, legal, security, native-binary, and reproducible-release conclusions until independent and owner reviews run

Freshness boundary: this audit preserves local artifact observations captured on 2026-07-17. Its references to upstream `main`, the latest release, and the latest package are capture-time observations. For the later official upstream refresh, use [Servo Upstream Refresh and Source-Strategy Delta](servo-upstream-refresh-and-source-strategy-delta-2026-07.md) and [Servo Upstream Source Provenance](servo-upstream-source-provenance-2026-07.md).

## Question

Which exact local source identities, archive digests, Cargo registry cache checks, Stylo git-source checks, and Windows bootstrap artifact summaries exist for the successful external Servo build, and what remains before Turing can decide `ADR-0009`?

This audit does not import Servo source, Stylo source, registry crates, generated output, Cargo metadata, native binaries, or build logs into Turing. It does not approve Servo-derived release code, a source archive, a dependency, a native package, a generated-code pipeline, or any `ADR-0009` option.

## Scope

The audit covers local evidence from:

- clean external Servo checkout: `C:\ts\servo`;
- Cargo git checkout for Servo's Stylo dependency under the user Cargo cache;
- local Cargo registry archive and source caches populated by the Servo metadata/build work;
- Servo Windows bootstrap dependencies under `C:\ts\servo\target\dependencies`;
- locally created `git archive` tar files under `C:\ts`.

The audit does not compare these artifacts with upstream release tarballs, crates.io index signatures beyond Cargo lockfile checksums, vendor source offers, or independent mirror fetches. Follow-up reports compare current upstream `main`, the latest GitHub release, the release source archive, the latest crates.io package, and source-surface equivalence, but still do not approve a source baseline.

## Method

Commands and checks were run outside the Turing repository. The method used:

1. `git status`, `git log`, `git rev-parse`, `git ls-files -s`, `git fsck --connectivity-only`, and `git count-objects` for Servo and Stylo source identity;
2. SHA-256 digests over `git ls-files -s` manifests to capture a deterministic tracked-file identity summary;
3. locally produced `git archive --format=tar` files for Servo and Stylo, then file-size and SHA-256 checks;
4. Node-based Cargo metadata parsing because Servo metadata contains case-distinct feature keys that PowerShell JSON parsing rejects;
5. lockfile checksum verification for every registry `.crate` archive used by the default and all-features metadata profiles;
6. bounded aggregation of native/package/debug files under Servo's Windows bootstrap dependency directory.

No source, dependency archive, generated output, build log, or native artifact was copied into this repository.

## Servo source identity

Observed from `C:\ts\servo`:

| Field | Observation |
|---|---|
| Remote | `https://github.com/servo/servo.git` |
| Checkout | `main...origin/main` |
| Commit | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Commit date | 2026-07-17T15:50:14Z |
| Commit subject | `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)` |
| Tree | `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Tracked files | `193033` |
| Partial clone | `remote.origin.promisor=true`, `partialclonefilter=blob:none` |
| Connectivity check | `git fsck --connectivity-only` exited `0` |
| Object store | `195764` objects in `2` packs, `188.27 MiB` packed size |

Tracked-file manifest digest:

| Manifest | Bytes | SHA-256 |
|---|---:|---|
| Servo `git ls-files -s` joined with LF | `26141112` | `54E852C7337C1913B72A057D5E1E354B0201D8945D14B19F36471B8E9EF72DE7` |

Local source archive:

| Archive | Size | SHA-256 |
|---|---:|---|
| `C:\ts\servo-source-4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe-20260717.tar` | `931993600` | `205530091A7E36977BBF7417F5D48D91D122137B9450985897E54C9A5D00841D` |

Interpretation: this is strong local identity evidence for the inspected checkout and local archive. It is not an upstream release tarball, signed tag, independent mirror verification, legal source-offer package, or approval to import source.

## Stylo git-source identity

Cargo metadata for both default and all-features Servo profiles resolved the same Stylo git source:

```text
git+https://github.com/servo/stylo?rev=d3de91cbac7bba38e159239b3c0a360783fce2ee#d3de91cbac7bba38e159239b3c0a360783fce2ee
```

Packages from that git source:

`selectors`, `servo_arc`, `stylo`, `stylo_atoms`, `stylo_derive`, `stylo_dom`, `stylo_malloc_size_of`, `stylo_static_prefs`, `stylo_traits`, `to_shmem`, and `to_shmem_derive`.

Observed local checkout:

| Field | Observation |
|---|---|
| Checkout path | `C:\Users\bcw19\.cargo\git\checkouts\stylo-482338307e42a9ea\d3de91c` |
| Checkout status | `master...origin/master [gone]`; untracked Cargo cache marker `.cargo-ok` |
| Commit | `d3de91cbac7bba38e159239b3c0a360783fce2ee` |
| Commit date | 2026-07-16T18:37:18Z |
| Commit subject | `Support font-variant-alternates and @font-feature-values for servo (#377)` |
| Tree | `d4bd206aeb9bf5d5dfd333cf1cce7a879dbc07e9` |
| Tracked files | `393` |
| Object store | `126278` objects in `1` pack, `39.61 MiB` packed size |

Tracked-file manifest digest:

| Manifest | Bytes | SHA-256 |
|---|---:|---|
| Stylo `git ls-files -s` joined with LF | `31360` | `8BEFF21ABDEC342993685224CEF578674B117CC9A4E860323B3E77C07D271EDB` |

Local source archive:

| Archive | Size | SHA-256 |
|---|---:|---|
| `C:\ts\stylo-source-d3de91cbac7bba38e159239b3c0a360783fce2ee-20260717.tar` | `6041600` | `323900D70CCF149C61F187A10F47D899A977772E3CE5D7BA82FD83B0DA5D1375` |

Interpretation: Stylo is a separate source-provenance object in the Servo decision packet. Commit pinning and a local archive digest are necessary evidence, but they do not settle license, generated-code, unsafe, shared-memory, CSS-ownership, or maintenance questions.

## Cargo metadata and lockfile posture

Local metadata files:

| File | Size | SHA-256 |
|---|---:|---|
| `C:\ts\servo-metadata-default.json` | `5357766` | `01314363C1E5F7375B5C0024D8C698C8C46EA1F6858CA945CE5560F17F5B3F11` |
| `C:\ts\servo-metadata-all-features.json` | `5649154` | `7E9DB6EFD7BFBB370B57EE72DEF52E8C3D025FF4C602F461444530591C37CB3F` |

Resolved package source counts:

| Metadata profile | Total packages | Registry packages | Git packages | Path packages |
|---|---:|---:|---:|---:|
| Default | `1069` | `983` | `11` | `75` |
| All features | `1120` | `1034` | `11` | `75` |

Cargo lockfile checksum posture:

| Metric | Observation |
|---|---:|
| Package entries | `1120` |
| Checksum entries | `1034` |
| Unique checksums | `1034` |

The checksum entries cover registry crates. They do not cover Servo path packages, Stylo git packages, generated outputs, or downloaded native bootstrap packages.

## Cargo registry cache verification

Registry archive and source checks used:

- source directory base: `C:\Users\bcw19\.cargo\registry\src\index.crates.io-1949cf8c6b5b557f`;
- archive cache base: `C:\Users\bcw19\.cargo\registry\cache\index.crates.io-1949cf8c6b5b557f`;
- Servo `Cargo.lock` checksums.

| Metadata profile | Registry packages | `.crate` archives present | Missing archives | Checksum mismatches | Source dirs present | Missing source dirs | Archive bytes | Archive-set SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Default | `983` | `983` | `0` | `0` | `983` | `0` | `196530372` | `4609FD1ADDDAFD20E03FD709D81DA2F4562C2C461C6F06B6F2BDC2C91A01A03C` |
| All features | `1034` | `1034` | `0` | `0` | `1034` | `0` | `201870061` | `05E2FCF50F987A0D8B584032B1479BD198BC96AC7940043DBF890EC46DD47AB7` |

The archive-set digest is a convenience digest over sorted `crate-name|bytes|sha256` lines for the resolved registry archive set in each profile. It is not a Cargo-native signature or source attestation.

Sample verified registry archives:

| Archive | Size | SHA-256 |
|---|---:|---|
| `ab_glyph-0.2.32.crate` | `20967` | `01C0457472C38EA5BD1C3B5ADA5E368271CB550BE7A4CA4A0B4634E9913F6CC2` |
| `ab_glyph_rasterizer-0.1.10.crate` | `11206` | `366FFBAA4442F4684D91E2CD7C5EA7C4ED8ADD41959A31447066E279E432B618` |
| `accesskit-0.24.0.crate` | `37124` | `5351DCEBB14B579CCAB05F288596B2AE097005BE7EE50A7C3D4CA9D0D5A66F6A` |
| `accesskit_atspi_common-0.18.0.crate` | `28902` | `842FD8203E6DFCF531D24F5BAC792088EDFBA7D6B35844FEAD191603FB32A260` |
| `accesskit_consumer-0.35.0.crate` | `46230` | `53CF47DAED85312E763FBF85CECA136E0D7ABC68E0A7E12ABE11F48172BC3B10` |
| `accesskit_macos-0.26.0.crate` | `27576` | `534BC3FDC89A64A1DB3C46B33C198FDE2B7C3C7D094E5809C8C8BF2970C18243` |
| `accesskit_unix-0.21.0.crate` | `27242` | `90E549DD7C6562B6A2EA807B44726E6241707DB054A817DC4C7E2B8D3B39BFAC` |
| `accesskit_windows-0.32.1.crate` | `57411` | `EFF7009F1A532E917D66970A1E80C965140C6CFBBABBDDE3D64E5431E6C78E21` |

Interpretation: the local Cargo cache is complete for both inspected metadata profiles and matches Servo's lockfile checksums for registry sources. This still does not approve any crate under Turing's dependency, license, advisory, unsafe, native, generated-code, or maintenance policies.

## Native and bootstrap artifacts

Servo bootstrap material under `C:\ts\servo\target\dependencies` remains outside Cargo's normal registry checksum model.

Aggregate:

| Metric | Observation |
|---|---:|
| Total files | `19456` |
| Total bytes | `1582709414` |
| Core DLL/EXE/PDB/MSI files | `1291` |
| Core DLL/EXE/PDB/MSI bytes | `864021659` |
| DLL files | `537` files, `404648238` bytes |
| EXE files | `443` files, `118229869` bytes |
| PDB files | `309` files, `337817600` bytes |
| MSI files | `2` files, `3325952` bytes |
| Additional `.gz` files under the same tree | `3443` files, `17960552` bytes |

Extracted-tree GStreamer MSI artifact hashes:

| File | Size | SHA-256 |
|---|---:|---|
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | `2023424` | `B9D603E73AB5A12884C593446E25D03FE0E9A8344FA9C03CA206575D819864CE` |
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | `1302528` | `B83B7C4107257511AF301EB78992B560D8B631D8433872C721448096ABDB6C1E` |

Follow-up native bootstrap audit confirmed these are smaller post-install artifacts under `target\dependencies`, not the original upstream downloads. The original upstream asset sizes, hashes, and signature status are recorded in the [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md).

Largest native/package/debug examples:

| Relative path under `target\dependencies` | Size | SHA-256 |
|---|---:|---|
| `gstreamer\1.0\msvc_x86_64\bin\avcodec-59.dll` | `97233792` | `B2409ADDB24A83D21DC1DF70889AB5B48E92CA047451BB9D5CB18524CBEFD3B7` |
| `gstreamer\1.0\msvc_x86_64\bin\avformat-59.dll` | `33915398` | `F204E08CDC2C180D9C8B2387A28B3302B5FFB49CA8C43DB4A0C225F9FCAF9926` |
| `moztools\4.0\bin\watchman.exe` | `20640768` | `BE7CC10CDE2712BCFEB800DEF1B30577B8AD7916D87E81BEE2AC4592D9772075` |
| `gstreamer\1.0\msvc_x86_64\bin\harfbuzz.pdb` | `20033536` | `7B9D85FE0D66B588E6A63AD0DB4426CA6F55872B3BD76BCEC9F7B335CDFA462A` |
| `gstreamer\1.0\msvc_x86_64\bin\libstdc++-6.dll` | `19373548` | `22608D10CEE330D75692C8963E26BB8DB46A38AE3DA4CB90DE5F42A515582F3E` |

Interpretation: the Windows bootstrap surface is a major unresolved provenance and release-operations item. A Turing decision still needs source-build versus binary-package policy, license text and notices, codec/patent analysis, native advisories, sandbox and packaging review, and update ownership for these packages.

## What this proves

This audit proves, for the inspected local environment only:

- the external Servo checkout is a clean tracked-file checkout at the recorded commit;
- the Servo tracked-file manifest and local `git archive` tar have recorded SHA-256 identities;
- the Stylo git source used by Servo metadata is pinned and has recorded local checkout, manifest, and archive identities;
- registry `.crate` archives needed by the inspected default and all-features metadata profiles are present locally, match Servo `Cargo.lock` checksums, and have unpacked source directories;
- the Windows bootstrap dependency tree has bounded file counts, sizes, extension counts, and representative hashes.

## What this does not prove

This audit does not prove:

- the Servo or Stylo source archives match an upstream release archive or signed tag artifact;
- any source, generated output, crate, native package, or binary is legally approved for Turing;
- Cargo registry checksums satisfy Turing legal, security, advisory, native, generated-code, or maintenance policy;
- native bootstrap artifacts are rebuildable from source, redistributable, current, patched, sandboxed, or packageable for Turing;
- a clean-target Servo build is reproducible on an independent host;
- Servo is compatible, secure, low memory, high performance, accessible, Chrome-class, production-ready, or suitable for Turing release code;
- `PB-002` can move out of blocked status.

## Resulting gate update

This audit narrows the old broad "source/archive digests" gap. Turing now has local source/archive and registry-cache evidence for Servo, Stylo, and crates.io sources in the inspected profiles.

The remaining gate should be stated more precisely:

1. owner-selected source baseline, signed-tag or equivalent provenance policy, and source-content/release-archive/package equivalence policy for Servo and Stylo;
2. Turing-specific license, notice, source-offer, patent, and advisory decisions;
3. native bootstrap source-build or binary-package exceptions, legal/advisory decisions, package minimization, and final release-package manifests for GStreamer, moztools, and other bootstrap artifacts;
4. clean generated-output regeneration and independent-host comparison;
5. registry/git build-script, proc-macro, native-link, unsafe, and FFI reviews;
6. owner-reviewed component-boundary, JavaScript-runtime, compatibility-corpus, performance, maintenance, and owner-review evidence for `ADR-0009`.

## Affected records

This audit adds evidence for `PB-002` but does not change its blocked status. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md);
- [Servo Supply-Chain Policy Scan - July 2026](servo-supply-chain-policy-scan-2026-07.md);
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Upstream Source Provenance - July 2026](servo-upstream-source-provenance-2026-07.md);
- [Servo Source Baseline Equivalence Policy Prep - July 2026](servo-source-baseline-equivalence-policy-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md);
- [Build, release, distribution, and operations](../blueprint-v1/13-build-release-operations.md);
- [Technology stack](../technology-stack/README.md).
