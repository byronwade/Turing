# Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026

Status: dated side-effect audit for `ADR9-EV-008`; no build-script, proc-macro, generated-output, native, dependency, or source approval
Owner: security, release operations, provenance, engine, architecture, and documentation owners
Retrieval date: 2026-07-17
Confidence: medium for Cargo metadata counts and static marker triage; low for behavioral conclusions until dynamic tracing, sandboxed execution, expansion review, and owner acceptance complete

## Question

Which Servo registry, git, and path build scripts and proc macros need side-effect review before `ADR-0009` can trust any candidate component boundary?

This report prepares the `ADR9-EV-008` decision queue. It does not approve executing Servo build scripts, proc macros, generated outputs, registry packages, Stylo git packages, native tools, compiler/linker actions, or any Servo-derived release code in Turing.

## Scope

Included:

- external Servo checkout at `C:\ts\servo`;
- default and all-features Cargo metadata generated outside this repository;
- static marker scans of build-script source files and proc-macro crate source roots present in the local Cargo registry/git/path cache;
- first-party side-effect observations from the existing generated-output audit.

Excluded:

- dynamic syscall, process, filesystem, network, or compiler tracing;
- proc-macro expansion diff review;
- clean-target rebuild proof;
- independent-host reproduction;
- source or dependency approval;
- copying external source, metadata, generated output, or build logs into Turing.

## Evidence Inputs

| Input | Observation |
|---|---|
| Servo remote | `https://github.com/servo/servo.git` |
| External checkout head | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| External checkout tree | `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Checkout state | `## main...origin/main [behind 2]`; shallow repository |
| Default metadata | `C:\ts\servo-metadata-default.json`, `1069` packages |
| All-features metadata | `C:\ts\servo-metadata-all-features.json`, `1120` packages |
| Prior generated-output audit | [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md) |
| Prior surface classification | [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md) |

The checkout being behind `origin/main` means this is a dated build-baseline snapshot. Any owner-selected source baseline, feature profile, target, or Cargo lockfile different from this snapshot needs a rerun.

## Method

This pass parsed Cargo metadata and inspected local source files referenced by metadata targets:

- packages with a `custom-build` target were counted as build-script packages;
- packages with a `proc-macro` target were counted as proc-macro packages;
- source kind was classified as path, git, or registry from Cargo metadata;
- static marker scans counted references to process execution, filesystem writes, URL/download/fetch strings, environment reads, compiler/linker directives, time/git inputs, and native-copy/package strings.

Marker counts are triage signals. A URL in a comment, a generated test fixture, or a documented example can produce a hit. Conversely, a build script can perform important side effects without matching these patterns. Owner review and dynamic tracing are still required.

## Metadata Surface

| Profile | Packages | Build-script packages | Proc-macro packages | Native-link packages |
|---|---:|---:|---:|---:|
| Default metadata | `1069` | `157` | `70` | `25` |
| All-features metadata | `1120` | `167` | `71` | `26` |

Default build-script packages by source:

| Source | Count |
|---|---:|
| Registry | `144` |
| Path | `9` |
| Git | `4` |

Default proc-macro packages by source:

| Source | Count |
|---|---:|
| Registry | `62` |
| Path | `6` |
| Git | `2` |

All-features metadata adds these build-time surfaces beyond the default profile:

- build scripts: `gstreamer-gl-wayland-sys 0.25.0`, `gstreamer-gl-x11-sys 0.25.0`, `jni 0.19.0`, `libdbus-sys 0.2.7`, `naga 29.0.4`, `valuable 0.1.1`, `vello_shaders 0.9.0`, `wgpu 29.0.4`, `wgpu-core 29.0.4`, and `wgpu-hal 29.0.4`;
- proc macros: `prost-derive 0.12.6`;
- native links: `libdbus-sys 0.2.7`, `links=dbus`.

Interpretation: the selected feature profile is a first-order security and release-operations input. All-features review is not interchangeable with the default build, and neither is sufficient for a selected component boundary without a reachable dependency closure.

## Build-Script Static Marker Summary

Default metadata build scripts had these static marker counts:

| Marker class | Count |
|---|---:|
| Environment reads and Cargo cfg/profile variables | `3492` |
| Compiler/linker directives or tool names | `816` |
| Native-copy/package strings | `631` |
| Filesystem writes or `OUT_DIR` references | `410` |
| URL/download/fetch strings | `267` |
| Process execution strings | `116` |
| Time or git-derived inputs | `18` |

Build-script markers by source:

| Source | Scripts | Process | Filesystem/write | URL/download/fetch | Env/cfg | Compiler/linker | Time/git | Native-copy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Git | `4` | `3` | `10` | `5` | `42` | `0` | `0` | `8` |
| Path | `9` | `10` | `68` | `17` | `269` | `17` | `7` | `38` |
| Registry | `144` | `103` | `332` | `245` | `3181` | `799` | `11` | `585` |

High-marker build scripts in the default profile:

| Package | Source | License metadata | Total markers | Review pressure |
|---|---|---|---:|---|
| `aws-lc-sys 0.42.0` | registry | complex ISC/Apache/MIT/BSD expression | `657` | crypto C build, toolchain, env, native output |
| `mozjs_sys 140.12.0-2` | registry | `MPL-2.0` | `599` | SpiderMonkey/JS engine build, process/toolchain, env, native output |
| `ring 0.17.14` | registry | `Apache-2.0 AND ISC` | `349` | crypto assembly/C build and env policy |
| `portable-atomic 1.13.1` | registry | `Apache-2.0 OR MIT` | `343` | target cfg/env feature probing |
| `libsqlite3-sys 0.36.0` | registry | `MIT` | `234` | native SQLite build/link behavior |
| `tikv-jemalloc-sys 0.6.1+...` | registry | `MIT/Apache-2.0` | `210` | allocator native build and env policy |
| `mozangle 0.6.0` | registry | `BSD-3-Clause` | `179` | ANGLE/GPU native build output |
| `rav1e 0.8.1` | registry | `BSD-2-Clause` | `178` | codec build flags and native outputs |
| `av-scenechange 0.14.1` | registry | `MIT` | `177` | codec-adjacent build flags |
| `servo-capi-tests 0.4.0` | path | `MPL-2.0` | `128` | nested Cargo, C API test build, DLL copying |
| `webrender 0.70.0` | registry | `MPL-2.0` | `102` | GPU/render generated assets and env policy |
| `servo-script-bindings 0.4.0` | path | `MPL-2.0 AND BSD-3-Clause` | `88` | Web IDL/Python/Stylo code generation |
| `zstd-sys 2.0.16+zstd.1.5.7` | registry | `MIT/Apache-2.0` | `86` | native compression build |
| `libz-sys 1.1.29` | registry | `MIT OR Apache-2.0` | `86` | native compression build |
| `rustix 1.1.4` | registry | LLVM exception/Apache/MIT expression | `74` | platform cfg/env build behavior |

These are not the only scripts requiring review. They are the highest-pressure scripts from the static marker scan and prior output-log evidence.

## First-Party Build-Script Queue

The existing generated-output audit already identified first-party path scripts and their roles. This pass turns them into an explicit side-effect queue:

| Package | Side-effect classes needing owner review |
|---|---|
| `servo-script-bindings` | Python/`uv` command resolution, Web IDL input discovery, Stylo `css-properties.json` dependency, generated Rust outputs, fallback to host Python |
| `servo-script` | copying generated binding subsets from another package's `OUT_DIR` |
| `servo-script-webgpu` | copying WebGPU binding subsets from broader generated outputs |
| `servo-devtools` | `SOURCE_DATE_EPOCH` or current-time build ID |
| `servo-embedder-traits` | production/non-production cfg inferred from `OUT_DIR` path |
| `servoshell` | git revision string, Windows resource compilation, platform link arguments, platform SDK/toolchain behavior |
| `servo-media-ohos` | `OHOS_SDK_NATIVE` metadata reads and OpenHarmony cfg emission |
| `servo-capi-tests` | nested `cargo cinstall`, C compilation, target directory isolation, Windows DLL copying |
| `style_tests` | dummy `OUT_DIR` exposure |

Turing cannot trust any generated output or build result until these effects are either out of scope for the selected component boundary or covered by an accepted side-effect policy.

## Git Build-Script and Proc-Macro Queue

Default metadata includes four Stylo git build-script packages from `https://github.com/servo/stylo` at `d3de91cbac7bba38e159239b3c0a360783fce2ee`:

- `selectors`;
- `stylo`;
- `stylo_atoms`;
- `stylo_static_prefs`.

Default metadata also includes two Stylo git proc macros:

- `stylo_derive`;
- `to_shmem_derive`.

The Stylo git packages lack Cargo registry checksums and are pinned by git revision. They need source archive attestation, side-effect review, proc-macro expansion-risk review, and owner-reviewed component-boundary reachability before any selected option can rely on them.

## Proc-Macro Static Marker Summary

Default metadata proc-macro packages covered `744` Rust source files and `5331698` bytes of local source in the inspected cache.

Proc-macro marker totals:

| Marker class | Count |
|---|---:|
| Environment/cfg strings | `4102` |
| Native-copy/package strings | `2941` |
| URL/download/fetch strings | `565` |
| Filesystem/write strings | `391` |
| Compiler/linker strings | `353` |
| Process execution strings | `42` |
| Time/git strings | `29` |

Proc-macro markers by source:

| Source | Packages | Rust files | Rust bytes | Process | Filesystem/write | URL/download/fetch | Env/cfg | Compiler/linker | Time/git | Native-copy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Git | `2` | `15` | `100108` | `0` | `0` | `17` | `88` | `2` | `0` | `85` |
| Path | `6` | `7` | `43541` | `0` | `0` | `9` | `12` | `2` | `0` | `33` |
| Registry | `62` | `722` | `5188049` | `42` | `391` | `539` | `4002` | `349` | `29` | `2823` |

Top proc-macro packages by marker count:

| Package | Source | License metadata | Rust files | Rust bytes | Total markers |
|---|---|---|---:|---:|---:|
| `zerocopy-derive 0.8.54` | registry | `BSD-2-Clause OR Apache-2.0 OR MIT` | `90` | `753329` | `1008` |
| `serde_derive 1.0.228` | registry | `MIT OR Apache-2.0` | `28` | `310245` | `880` |
| `jni-macros 0.22.4` | registry | `MIT OR Apache-2.0` | `9` | `311210` | `560` |
| `derive_more-impl 2.1.1` | registry | `MIT` | `35` | `413758` | `538` |
| `tracing-attributes 0.1.31` | registry | `MIT` | `20` | `139560` | `471` |
| `zbus_macros 5.17.0` | registry | `MIT` | `6` | `156472` | `372` |
| `napi-derive-ohos 1.2.0` | registry | `MIT` | `10` | `90042` | `313` |
| `bpaf_derive 0.5.26` | registry | `MIT OR Apache-2.0` | `11` | `147122` | `300` |
| `glib-macros 0.22.6` | registry | `MIT` | `72` | `408783` | `250` |
| `wayland-scanner 0.31.10` | registry | `MIT` | `13` | `255291` | `245` |
| `defmt-macros 1.1.1` | registry | `MIT OR Apache-2.0` | `37` | `86035` | `244` |
| `async-trait 0.1.89` | registry | `MIT OR Apache-2.0` | `27` | `83764` | `188` |
| `stylo_derive 0.19.0` | git | `MPL-2.0` | `12` | `94357` | `184` |
| `strum_macros 0.28.0` | registry | `MIT` | `24` | `140885` | `181` |
| `zerovec-derive 0.10.3` | registry | `Unicode-3.0` | `9` | `76442` | `173` |

Proc macros execute in the compiler context. Turing needs expansion-risk review for any reachable proc macro, even when the macro appears low-risk or common in the Rust ecosystem.

## Required Side-Effect Policy

`ADR9-EV-008` cannot close until the selected Servo baseline, feature profile, and component boundary have an accepted policy for:

1. process execution allowlist and arguments;
2. filesystem writes limited to declared output directories;
3. network access denied by default and separately audited for every exception;
4. environment variable allowlist, including target, host, Cargo, Python, SDK, and path variables;
5. compiler, linker, assembler, resource compiler, CMake, Ninja, bindgen, cbindgen, pkg-config, and platform SDK discovery;
6. time, git, profile-path, and other non-hermetic inputs, including `SOURCE_DATE_EPOCH`;
7. nested Cargo invocations and target/cache isolation;
8. owner-reviewed generated-output source-to-output mapping and license/provenance attribution;
9. proc-macro source provenance, expansion determinism, emitted code review, and denied ambient authority;
10. native artifact copying, DLL/plugin packaging, and release manifest linkage.

## What This Proves

- The `ADR9-EV-008` build-script/proc-macro review surface is now concrete for the inspected snapshot.
- Default metadata exposes `157` build-script packages and `70` proc-macro packages; all-features expands that surface to `167` build-script packages and `71` proc-macro packages.
- Registry packages dominate build-script and proc-macro side-effect marker volume.
- High-review build scripts include JavaScript runtime, crypto, allocator, SQLite, ANGLE/GPU, codec/compression, first-party Web IDL generation, C API tests, and WebRender-related scripts.
- The selected feature profile materially changes the build-time execution surface.

## What This Does Not Prove

- build scripts are safe or unsafe;
- proc macros expand deterministically or safely;
- build scripts avoid network access at runtime;
- generated outputs are deterministic from a feature-correct full clean target;
- owner-reviewed source-to-output license/provenance is complete;
- any package, proc macro, native tool, or generated output is approved for Turing;
- compatibility, performance, accessibility, daily-driver, production, or Chrome-class readiness.

## Gate Impact

`PB-002` remains blocked.

`ADR9-EV-008` remains partial. Existing evidence now includes this side-effect audit, and adjacent `ADR9-EV-007` evidence now includes a first-pass generated-output generator manifest plus a first-pass source-to-output provenance map, but the selected baseline/profile/component boundary, accepted side-effect policy, dynamic tracing, proc-macro expansion review, owner-reviewed generated-output provenance, feature-correct full clean-target regeneration beyond the package-scoped dummy-media probe, independent replay, and owner approval remain missing.

## Affected Records

- [`docs/README.md`](../README.md)
- [`docs/research/README.md`](README.md)
- [`docs/repository-map.md`](../repository-map.md)
- [`docs/research-log.md`](../research-log.md)
- [`docs/research/servo-source-strategy-inventory-2026-07.md`](servo-source-strategy-inventory-2026-07.md)
- [`docs/project-buildout/11-pre-build-readiness-checklist.md`](../project-buildout/11-pre-build-readiness-checklist.md)
- [`docs/project-buildout/13-build-readiness-operating-board.md`](../project-buildout/13-build-readiness-operating-board.md)
- [`docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`](../project-buildout/14-adr-0009-source-strategy-decision-packet.md)
- [`docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`](../project-buildout/15-adr-0009-evidence-traceability-matrix.md)
- [`docs/blueprint-v1/machine/pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [`docs/research/servo-build-script-generated-output-audit-2026-07.md`](servo-build-script-generated-output-audit-2026-07.md)
- [`docs/research/servo-clean-generated-output-reproduction-2026-07.md`](servo-clean-generated-output-reproduction-2026-07.md)
- [`docs/research/servo-generated-output-generator-manifest-2026-07.md`](servo-generated-output-generator-manifest-2026-07.md)
- [`docs/research/servo-generated-native-unsafe-classification-2026-07.md`](servo-generated-native-unsafe-classification-2026-07.md)

## Next Experiments

1. Select the source baseline, feature profile, target triple, profile, and candidate component boundary for the side-effect audit.
2. Run dynamic build-script tracing in a clean target with process, filesystem, environment, network, compiler/linker, and native-copy capture.
3. Generate proc-macro expansion outputs for reachable macros and review emitted code for unsafe, FFI, native, global state, and policy-sensitive effects.
4. Compare build-script and proc-macro outputs across clean-target and independent-host runs.
5. Bind generated outputs to source inputs, license/provenance records, and final package manifests.
