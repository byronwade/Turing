# Servo Native Bootstrap Provenance and Source-Build Audit - July 2026

Status: dated external native/bootstrap provenance audit for `PB-002` and proposed `ADR-0009`; no native package, source-build, license, advisory, codec, patent, packaging, or redistribution approval
Owner: provenance, release operations, security, architecture, engine, media, and legal-review owners
Audit date: 2026-07-17
Confidence: medium for observed Windows bootstrap script behavior, upstream release metadata, local artifact hashes, and local file counts; low for adoption, source-build, redistribution, legal, advisory, sandbox, package-minimization, and release conclusions until owner reviews run

## Question

What native packages and toolchain inputs does Servo's Windows bootstrap path download or install, what identity and signature evidence exists for those inputs on the reference host, and what source-build or binary-package decisions remain before Turing can make `ADR-0009`?

This audit does not import Servo source, generated output, build logs, native packages, native binaries, downloaded archives, MSI files, or package metadata into Turing. It does not approve Servo-derived release code, Servo bootstrap artifacts, GStreamer, moztools, `servo-build-deps`, winget packages, native runtime libraries, codec libraries, OpenSSL libraries, or a binary redistribution model.

Follow-up [Servo Native Package Decision Prep - July 2026](servo-native-package-decision-prep-2026-07.md) converts this identity evidence into `ADR9-EV-005` and `ADR9-EV-006` source-build, binary-package exception, deterministic-download, package-minimization, notice, and manifest decision queues. It remains decision prep only.

## Scope

The audit covers observed evidence from:

- clean external Servo checkout: `C:\ts\servo`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- local bootstrap log: `C:\ts\servo-bootstrap.log`;
- Servo Windows bootstrap and packaging sources under `C:\ts\servo\python\servo`;
- GStreamer plugin-list templates under `C:\ts\servo\components\servo\gstreamer_plugin_lists`;
- upstream release metadata from `servo/servo-build-deps` tag `msvc-deps`;
- locally downloaded upstream release assets under `C:\ts\servo-native-artifacts-msvc-deps`;
- extracted Windows bootstrap dependency tree under `C:\ts\servo\target\dependencies`;
- external dev build output under `C:\ts\servo\target\debug`.

No files from those external locations were copied into this repository.

## Method

The audit used:

1. `git -C C:\ts\servo status`, `rev-parse`, and `log` to bind evidence to the inspected Servo checkout;
2. `rg` over Servo bootstrap sources to locate URL constants, installer calls, winget import behavior, and package-copy logic;
3. `Get-FileHash -Algorithm SHA256` for source files, downloaded release assets, extracted MSI artifacts, and representative runtime binaries;
4. `Get-AuthenticodeSignature` for downloaded upstream artifacts and extracted `.dll`, `.exe`, and `.msi` files;
5. `gh release view msvc-deps --repo servo/servo-build-deps --json tagName,publishedAt,url,assets`;
6. bounded PowerShell aggregation of extension counts, root counts, manifest digests, license-like files, and debug-output size.

This is an identity and provenance audit, not a legal review, vulnerability scan, source-build reproduction, package minimization, performance test, or redistribution decision.

## Inspected bootstrap source identity

| Source input | Size | SHA-256 |
|---|---:|---|
| `C:\ts\servo\python\servo\platform\windows.py` | `8851` | `A9A4E3557C27E8AAC04D8721E3B5A225CA0BC7461008D0B1D05017FA4E5F98A0` |
| `C:\ts\servo\python\servo\util.py` | `11176` | `FF12F6086DEE59C0A6EBA6BA42531F3D3E1666A4485251FF16B07CE80CF3B62B` |
| `C:\ts\servo\python\servo\gstreamer.py` | `11282` | `1199CBBF0131A2516DABB94DAE6B55B88D2FD2DF0A3C6EFCC6DFCFF9867F9359` |
| `C:\ts\servo\python\servo\build_commands.py` | `17783` | `8FB7C2D37790B4541483D86151B5F1C3ABE739B0EF9D86F51F19A9F5738F7C50` |
| `C:\ts\servo\python\servo\platform\windows\winget.json` | `849` | `E0238DEE5C402D8F22E8A7A3F9941EC9B9893D0009AED2CF060CEB1067AC9943` |
| `C:\ts\servo\components\servo\gstreamer_plugin_lists\common.rs.in` | `908` | `509F9C5F200DC031C3A4C6D990E25505CF5AFFF7A88294B84E884E3408FEDD12` |
| `C:\ts\servo\components\servo\gstreamer_plugin_lists\windows.rs.in` | `248` | `A4CE2475F5885B0825DF5B0B7FCB5872F2FFAE7ACF128CCCB142B25CCBC64E19` |

Observed script behavior:

- `windows.py` sets `DEPS_URL` to `https://github.com/servo/servo-build-deps/releases/download/msvc-deps`.
- `windows.py` lists `moztools` version `4.0`.
- `windows.py` downloads `gstreamer-1.0-msvc-x86_64-1.22.8.msi` and `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi`.
- `download_and_extract_dependency()` downloads `{full_spec}.zip`, extracts it under `target\dependencies`, and removes the ZIP after extraction.
- `_platform_bootstrap()` runs passive bootstrap, `winget import`, LLVM PATH persistence, and GStreamer bootstrap.
- `_platform_bootstrap_gstreamer()` downloads both GStreamer MSIs to a temporary directory, runs elevated `msiexec.exe /a ... TARGETDIR=<dependencies> /qn`, and then the temporary directory is removed.
- `util.download_file()` supports `.part` resume behavior but the inspected Windows bootstrap call sites do not provide expected hashes or signatures for `moztools` or GStreamer artifacts.
- `util.check_hash()` exists, but this audit did not find it wired into the inspected Windows `moztools` or GStreamer bootstrap path.
- `build_commands.py` copies ANGLE DLLs, curated GStreamer DLLs and plugins, and MSVC/Windows SDK DLLs into the built binary directory.
- `gstreamer.py` defines Windows GStreamer dependency DLLs and loads the plugin list from Rust-compatible template files.

## Winget package inputs

`winget.json` imports from `https://cdn.winget.microsoft.com/cache`.

| Package identifier | Version pinned in Servo manifest |
|---|---|
| `Kitware.CMake` | No |
| `LLVM.LLVM` | No |
| `Ninja-build.Ninja` | No |
| `WiXToolset.WiXCLI` | `7.0.0.0` |

Bootstrap log result: the reference host reported CMake, LLVM, Ninja, and WiX already installed or verified; Servo then used Rust `1.95.0-x86_64-pc-windows-msvc` and replaced or installed `crown v0.0.1`.

Interpretation: the winget path is convenient for a developer bootstrap but not a reproducible Turing release input by itself. Three package versions are not pinned in the Servo manifest, winget source state is external, and `_ensure_llvm_in_user_path()` mutates persistent user environment state.

## Upstream release metadata and downloaded artifact hashes

Release metadata source:

- repository: `servo/servo-build-deps`;
- repository URL: `https://github.com/servo/servo-build-deps`;
- default branch observed through GitHub CLI: `main`;
- repository license observed through GitHub CLI: MPL-2.0;
- release tag: `msvc-deps`;
- release URL: `https://github.com/servo/servo-build-deps/releases/tag/msvc-deps`;
- release published at: `2023-04-20T07:41:51Z`.

Relevant assets observed through GitHub CLI on 2026-07-17:

| Asset | GitHub size | GitHub created | GitHub updated | GitHub digest | Observed download count |
|---|---:|---|---|---|---:|
| `moztools-4.0.zip` | `143306382` | `2023-09-09T08:45:43Z` | `2023-09-09T08:46:06Z` | `null` | `43991` |
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | `127258624` | `2024-01-03T09:08:47Z` | `2024-01-03T09:08:57Z` | `null` | `28357` |
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | `225861632` | `2024-01-03T09:08:29Z` | `2024-01-03T09:08:47Z` | `null` | `28233` |

Locally downloaded copies under `C:\ts\servo-native-artifacts-msvc-deps`:

| Asset | Local size | SHA-256 | Authenticode status |
|---|---:|---|---|
| `moztools-4.0.zip` | `143306382` | `CCEB354767EF3DAD8813E63CB95ED081814225BF5FA15BFA083AA8B31A339153` | `UnknownError` |
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | `127258624` | `37F9973FE5C720CE1F1602E7E599336384B9FF3E4878817987DD6B77265F17BB` | `NotSigned` |
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | `225861632` | `2D0CF6E89CF88D94E670CD81087C002408161D1C8843C00D3F27D33CE254C523` | `NotSigned` |

Interpretation: Turing now has local hashes for the observed upstream assets, but GitHub release metadata did not expose asset digests, the inspected Servo bootstrap script does not verify these hashes during bootstrap, and the two GStreamer MSI assets were not Authenticode-signed. This is not enough for a release source-build or binary-package exception.

## Corrected GStreamer MSI interpretation

Earlier local scans recorded two small `.msi` files under `C:\ts\servo\target\dependencies`. This audit confirms those are post-install or administrative-install artifacts left under the extracted dependency tree, not the original upstream downloads. The original downloads were placed in a temporary directory during bootstrap and removed when bootstrap exited.

| Package | Original upstream asset size | Original upstream asset SHA-256 | Extracted-tree MSI size | Extracted-tree MSI SHA-256 |
|---|---:|---|---:|---|
| GStreamer runtime | `127258624` | `37F9973FE5C720CE1F1602E7E599336384B9FF3E4878817987DD6B77265F17BB` | `1302528` | `B83B7C4107257511AF301EB78992B560D8B631D8433872C721448096ABDB6C1E` |
| GStreamer development | `225861632` | `2D0CF6E89CF88D94E670CD81087C002408161D1C8843C00D3F27D33CE254C523` | `2023424` | `B9D603E73AB5A12884C593446E25D03FE0E9A8344FA9C03CA206575D819864CE` |

The extracted-tree MSI hashes remain useful local identity evidence, but they must not be described as the downloaded upstream MSI hashes.

## Extracted bootstrap dependency tree

Root: `C:\ts\servo\target\dependencies`

| Root entry | Files | Bytes |
|---|---:|---:|
| `gstreamer` | `4630` | `1234821863` |
| `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi` | `1` | `2023424` |
| `gstreamer-1.0-msvc-x86_64-1.22.8.msi` | `1` | `1302528` |
| `moztools` | `14824` | `344561599` |
| Total | `19456` | `1582709414` |

Top extension groups:

| Extension | Files | Bytes |
|---|---:|---:|
| no extension | `7210` | `19359850` |
| `.gz` | `3443` | `17960552` |
| `.h` | `1857` | `26117610` |
| `.mo` | `1325` | `62128828` |
| `.pl` | `644` | `4979944` |
| `.pm` | `630` | `11993099` |
| `.dll` | `537` | `404648238` |
| `.a` | `456` | `511051804` |
| `.exe` | `443` | `118229869` |
| `.pdb` | `309` | `337817600` |

Extracted-root manifest digests:

| Root | Files | Bytes | Manifest bytes | Manifest SHA-256 |
|---|---:|---:|---:|---|
| `gstreamer\1.0\msvc_x86_64` | `4630` | `1234821863` | `188999` | `16B251D5FD7C17B68ABA62AF84994F5B3ADEE3D66C1BF45DAC9BC3A8681C158D` |
| `moztools\4.0` | `14824` | `344561599` | `693161` | `FAAA7521A41A7D41F2529A4041DEE31616D038A22FA9F55AC51323A80405CA9D` |

License-like files observed under the dependency tree:

| Root | License-like files | Distinct package/license directories | Bytes |
|---|---:|---:|---:|
| GStreamer | `155` | `69` | `1141093` |
| Moztools | `219` | `41` | `4530982` |
| Total | `374` | `110` | `5672075` |

Examples of license-bearing or high-review native surfaces include FFmpeg-family DLLs, OpenSSL libraries, x264, OpenH264, LAME, libjpeg-turbo, libpng, harfbuzz, fontconfig, freetype, cairo, zlib, bzip2, MSYS2, 7-Zip, UPX, Watchman, SQLite, xz, and zstd. These examples identify review areas only; they are not license approvals or package acceptance decisions.

## Signature posture

Authenticode checks over extracted `.dll`, `.exe`, and `.msi` files under `C:\ts\servo\target\dependencies` produced:

| Status | Files | Bytes |
|---|---:|---:|
| `NotSigned` | `981` | `525775835` |
| `Valid` | `1` | `428224` |

The one signed extracted file observed was:

| File | SHA-256 | Signer |
|---|---|---|
| `moztools\4.0\bin\vswhere.exe` | `FC0DCBE3981EF3ABAF1D3A13F0B79406BA3C19C70647C380A8E7D573D147FF98` | `CN=Microsoft Corporation, OU=MOPR, O=Microsoft Corporation, L=Redmond, S=Washington, C=US` |

Representative unsigned native files:

| File | Size | SHA-256 |
|---|---:|---|
| `gstreamer\1.0\msvc_x86_64\bin\avcodec-59.dll` | `97233792` | `B2409ADDB24A83D21DC1DF70889AB5B48E92CA047451BB9D5CB18524CBEFD3B7` |
| `gstreamer\1.0\msvc_x86_64\bin\avformat-59.dll` | `33915398` | `F204E08CDC2C180D9C8B2387A28B3302B5FFB49CA8C43DB4A0C225F9FCAF9926` |
| `moztools\4.0\bin\watchman.exe` | `20640768` | `BE7CC10CDE2712BCFEB800DEF1B30577B8AD7916D87E81BEE2AC4592D9772075` |
| `gstreamer\1.0\msvc_x86_64\bin\libstdc++-6.dll` | `19373548` | `22608D10CEE330D75692C8963E26BB8DB46A38AE3DA4CB90DE5F42A515582F3E` |
| `gstreamer\1.0\msvc_x86_64\bin\libsrt.dll` | `18083093` | `49F9258CC0D53C2393A1800291BB9C7A29258A414AEF760684EDB2C307282839` |
| `gstreamer\1.0\msvc_x86_64\bin\libx264-157.dll` | `12903115` | `B21CA6F2238134A3EFBC0BE51F94CFFFB2567E9447F5805C3D6D9F263B084C6B` |
| `gstreamer\1.0\msvc_x86_64\bin\libcrypto-1_1-x64.dll` | `3439104` | `8A6A2F7C76C7400931A4DFCC9F29CAFC6DB5363B1D1F9FAB4525E25FAC60373E` |
| `gstreamer\1.0\msvc_x86_64\bin\pkg-config.exe` | `3427016` | `7A01618F203DA1091ECB5C6EEFFB22229DD52EBB0E94E2F336E3C07046FE4B21` |

Interpretation: release planning must treat these native artifacts as first-class provenance, advisory, sandbox, codec, notice, and update inputs. The current evidence is sufficient to show scale and local identity; it is not sufficient to approve execution or redistribution.

## GStreamer packaging and plugin subset

`gstreamer.py` defines a curated Windows runtime DLL set and maps plugin list entries to `.dll` filenames.

Plugin-list evidence:

| Source | String count | SHA-256 |
|---|---:|---|
| `common.rs.in` | `35` | `509F9C5F200DC031C3A4C6D990E25505CF5AFFF7A88294B84E884E3408FEDD12` |
| `windows.rs.in` | `1` | `A4CE2475F5885B0825DF5B0B7FCB5872F2FFAE7ACF128CCCB142B25CCBC64E19` |

The Windows-only plugin string observed was `gstwasapi`. Common examples include `gstcoreelements`, `gstnice`, `gstapp`, `gstaudioconvert`, `gstogg`, `gstopengl`, `gstopus`, `gstplayback`, `gsttheora`, `gstvorbis`, `gstdeinterlace`, `gstmpg123`, `gstopenh264`, and `gstrtp`.

Interpretation: a release decision needs an exact final package manifest and codec/patent review for the selected runtime/plugin subset, not just the full bootstrap dependency tree.

## External dev build output footprint

Root: `C:\ts\servo\target\debug`

| Extension | Files | Bytes |
|---|---:|---:|
| `.dll` | `146` | `289684712` |
| `.exe` | `208` | `770920448` |
| `.pdb` | `263` | `4162707456` |
| Total | `617` | `5223312616` |

Largest observed files:

| File | Size |
|---|---:|
| `servoshell.pdb` | `1787731968` |
| `deps\servoshell.pdb` | `1787731968` |
| `servoshell.exe` | `298702336` |
| `deps\servoshell.exe` | `298702336` |
| `avcodec-59.dll` | `97233792` |
| `build\mozangle-a07193457b2ee42d\out\libGLESv2.pdb` | `61480960` |
| `avformat-59.dll` | `33915398` |
| `build\mozangle-a07193457b2ee42d\out\libGLESv2.dll` | `12783616` |
| `libGLESv2.dll` | `12783616` |

Interpretation: the successful dev build is not a minimized release package. The debug output footprint is a release-operations input for binary-size policy, symbol handling, native runtime copying, and packaging manifests.

## What this proves

This audit proves only that:

- the inspected Servo checkout is clean at commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- the inspected Windows bootstrap source and plugin-list files have recorded local hashes;
- Servo's Windows bootstrap path downloads `moztools-4.0.zip` and GStreamer MSVC `1.22.8` MSI assets from the `servo-build-deps` `msvc-deps` release;
- the relevant upstream release assets had no GitHub `digest` values in the observed metadata;
- local copies of those upstream assets have recorded SHA-256 hashes;
- the two downloaded GStreamer MSI assets were not Authenticode-signed;
- the local extracted dependency tree and debug output have bounded counts, sizes, manifest hashes, and representative file identities;
- earlier small GStreamer MSI hashes under `target\dependencies` were extracted-tree artifacts, not original upstream download hashes.

## What this does not prove

This audit does not prove that:

- Servo bootstrap artifacts are acceptable Turing dependencies;
- GStreamer, moztools, MSYS2-derived tools, codec packages, OpenSSL packages, or `servo-build-deps` assets are legally redistributable by Turing;
- license notices, source-offer obligations, patent obligations, or codec restrictions are complete;
- native advisories are reviewed or patched;
- unsigned native binaries are acceptable for release execution;
- the packages can be rebuilt from source by Turing;
- binary-package exceptions are acceptable;
- the bootstrap is hermetic, reproducible, or stable across independent hosts;
- the final release package can or should contain these artifacts;
- the debug build output is a release footprint;
- Servo is compatible, secure, low memory, high performance, accessible, Chrome-class, production-ready, or suitable for Turing release code;
- `PB-002` can move out of blocked status.

## Resulting gate update

The old `PB-002` blocker "native binary provenance and source-build policy" should now be split. Local identity evidence exists for the observed upstream native bootstrap assets and extracted tree, but the remaining decisions are:

1. Turing source-build recipe or explicit binary-package exception for each native package family;
2. upstream source provenance for `servo-build-deps`, GStreamer MSVC packages, moztools, MSYS2-derived tools, and codec/crypto libraries;
3. legal review for redistribution, notices, source-offer obligations, codec and patent posture, and package-specific license terms;
4. advisory and vulnerability review for downloaded native packages and extracted native files;
5. deterministic verification policy for bootstrap downloads, including expected hashes, signatures, mirrors, freshness, and revocation response;
6. package-minimization decision for GStreamer DLLs, plugins, ANGLE, MSVC redistributables, Windows SDK DLLs, and debug symbols;
7. final release package manifest and SBOM policy;
8. independent-host reproduction of the bootstrap and build output;
9. accepted `ADR-0009` source-strategy decision.

## Affected records

This audit adds evidence for `PB-002` but does not change its blocked status. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Pre-Build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md);
- [Servo Supply-Chain Policy Scan - July 2026](servo-supply-chain-policy-scan-2026-07.md);
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Native Package Decision Prep - July 2026](servo-native-package-decision-prep-2026-07.md);
- `docs/blueprint-v1/machine/pre-build-readiness.json`.
