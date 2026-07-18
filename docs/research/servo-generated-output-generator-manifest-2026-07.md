# Servo Generated-Output Generator Manifest - July 2026

Status: first-pass generator manifest for `PB-002` and `ADR9-EV-007`; no generated-output determinism proof, source-to-output license/provenance approval, generated-code approval, source approval, dependency approval, component approval, or release-code authorization

Owner: engine, supply-chain, and quality

Manifest date: 2026-07-18

Confidence: medium for first-party Servo and Stylo generator-family identification on the pinned local checkout; low for clean-target determinism, source-to-output legal provenance, feature-profile completeness, and release suitability until owner review and independent replay exist

## Question

Which generated-output families are visible in the local Servo and Stylo source trees, what source inputs drive them, what build environment facts affect them, and what evidence remains before Turing may rely on any generated output for an `ADR-0009` source-strategy decision?

## Scope

This manifest extends the [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md) and the [Servo Clean Generated-Output Reproduction Probe - July 2026](servo-clean-generated-output-reproduction-2026-07.md). It is intentionally a manifest, not a generated-code approval.

Included:

- first-party Servo `build.rs` files under `components/`, `ports/`, and `tests/`;
- the pinned Cargo git checkout for `servo/stylo`;
- selected warm full-target and package-scoped clean-target output-family observations already retained on the local Windows host;
- source-family directory digests using the method below.

Excluded:

- registry build scripts and proc macros beyond the first-party Servo/Stylo families below;
- dynamic build tracing for filesystem, process, network, compiler, linker, native-copy, or environment access;
- legal review of generated files and generator inputs;
- any approval to copy Servo-generated outputs into Turing release code.

## Source identity

| Source | Local path | Identity | Working-tree note |
|---|---|---|---|
| Servo checkout | `C:\ts\servo` | commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d` | `main...origin/main [behind 2]` when inspected; evidence is tied to this local tree, not current upstream |
| Stylo Cargo git checkout | `C:\Users\bcw19\.cargo\git\checkouts\stylo-482338307e42a9ea\d3de91c` | commit `d3de91cbac7bba38e159239b3c0a360783fce2ee`, tree `d4bd206aeb9bf5d5dfd333cf1cce7a879dbc07e9` | local checkout also had Cargo's untracked `.cargo-ok` marker |

The Servo `Cargo.toml` pins multiple Stylo crates to `https://github.com/servo/stylo` at revision `d3de91cbac7bba38e159239b3c0a360783fce2ee`.

## Method

The manifest was produced by static inspection of `build.rs` files, linked Python generators, retained output directories under the warm Servo target, retained output directories under a package-scoped clean target, and source-family digests.

Directory digest method for this report:

1. recursively enumerate files under the source or output root;
2. sort by full path;
3. append `relative/path<TAB>byte_length<TAB>file_sha256<LF>` for each file;
4. compute SHA-256 of that manifest text.

These are method-local directory digests. They are useful for this report's source-family and output-family comparison, but they must not be treated as interchangeable with older report digests that may have used a different directory hash recipe.

## Generator Inventory

| Family | Generator | Primary inputs | Generated outputs | Environment and tool sensitivity | Remaining gap |
|---|---|---|---|---|---|
| Web IDL and script bindings | `components/script_bindings/build.rs`; `components/script_bindings/codegen/run.py` | `components/script_bindings/webidls`, `components/script_bindings/codegen`, `third_party/WebIDL/parser`, `third_party/ply`, Stylo `css-properties.json`, `Bindings.conf` | `Bindings/`, `ConcreteBindings/`, `WebGPUConcreteBindings/`, `PrototypeList.rs`, `RegisterBindings.rs`, `Globals.rs`, `InterfaceObjectMap.rs`, `InterfaceObjectMapData.json`, `InterfaceObjectMapPhf.rs`, `InterfaceTypes.rs`, `InheritTypes.rs`, `ConcreteInheritTypes.rs`, `GenericUnionTypes.rs`, `UnionTypes.rs`, `DomTypes.rs`, `DomTypeHolder.rs`, `ContentEventHandlerNames.rs`, `doc/apis.html` | Python discovery tries `uv run --frozen python`, then `python3`, then `python`; generator uses `DEP_SERVO_STYLE_CRATE_OUT_DIR`, `OUT_DIR`, `PYTHONDONTWRITEBYTECODE=1`, feature-gated `skip-unless` WebIDL comments, and the Stylo CSS property manifest | Needs feature-profile selection, owner-reviewed input map, source-to-output license/provenance mapping, and feature-correct clean regeneration |
| Script copy outputs | `components/script/build.rs` | `DEP_SCRIPT_BINDINGS_CRATE_OUT_DIR`; generated script-binding roots and `ConcreteBindings/` | Copies selected root files and all `ConcreteBindings/` files into `components/script` `OUT_DIR` | Sensitive to upstream script-bindings output and Cargo dependency output path | Copy-chain provenance must be tracked separately from original generation |
| WebGPU binding copy outputs | `components/script_webgpu/build.rs` | `DEP_SCRIPT_BINDINGS_CRATE_OUT_DIR`; `WebGPUConcreteBindings/` | Copies WebGPU concrete bindings into a local `ConcreteBindings/` directory | Sensitive to feature gating and upstream script-bindings output | Needs WebGPU feature-profile policy and clean-target comparison |
| Stylo CSS properties | `style/build.rs`; `style/properties/build.py` in the pinned Stylo checkout | `style/properties` templates and data files, vendored Python packages, `OUT_DIR`, engine mode | `properties.rs`, `css-properties.json`, `css-properties.html`, documentation under `doc/stylo` for Servo mode | Feature-sensitive (`servo` or `gecko`); Python selected through `PYTHON3` or platform default; aborts on Python object-address pattern in output | Needs owner-reviewed generated source provenance and release-path license review |
| Selectors PHF attributes | `selectors/build.rs` in the pinned Stylo checkout | hardcoded HTML attribute list and `phf_codegen` | `ascii_case_insensitive_html_attributes.rs` | Rust build environment and `OUT_DIR` | Needs generator-version provenance and clean replay under selected profile |
| Stylo atoms | `stylo_atoms/build.rs` in the pinned Stylo checkout | `static_atoms.txt`, `predefined_counter_styles.rs`, `string_cache_codegen` | `atom.rs` | Rust build environment and `OUT_DIR` | Needs atom input review and source-to-output mapping |
| Stylo static prefs | `stylo_static_prefs/build.rs` in the pinned Stylo checkout | `preferences.toml` | `generated.rs`; also prints generated Rust to stdout | TOML parsing, Rust build environment, `OUT_DIR` | Needs stdout/artifact policy and preference provenance review |
| DevTools build id | `components/devtools/build.rs` | current time or `SOURCE_DATE_EPOCH` | `build_id.rs` | Nondeterministic unless `SOURCE_DATE_EPOCH` is pinned | Needs accepted build identity policy before reproducibility claims |
| Servoshell resource and identity outputs | `ports/servoshell/build.rs` | target OS/env, profile inferred from `OUT_DIR`, Windows icon/manifest, macOS C source, OpenHarmony version script, Git checkout | Windows `resource.rc`/`resource.res`, Android `libgcc.a` linker script, macOS C object, link args, `GIT_SHA` environment | Sensitive to `TARGET`, `CARGO_CFG_TARGET_OS`, `CARGO_CFG_TARGET_ENV`, profile path, `git rev-parse`, Windows resource toolchain, macOS compiler, OpenHarmony SDK/linker | Needs per-target native-output policy, profile policy, and Git identity capture |
| Shared embedder profile cfg | `components/shared/embedder/build.rs` | profile inferred from `OUT_DIR` | Rust cfg only; no file output observed | Sensitive to profile path | Needs profile-inference policy if any release path reuses it |
| OpenHarmony media SDK cfg | `components/media/backends/ohos/build.rs` | `OHOS_SDK_NATIVE\oh-uni-package.json` | Rust cfg and warning output only; no file output observed | Sensitive to target env `ohos` and `OHOS_SDK_NATIVE` | Needs SDK provenance policy for any OpenHarmony target |
| C API test install and native copy | `tests/capi/build.rs` | Servo C API package, `ffi/capi`, C test sources, target/profile, ANGLE DLL locations | nested `cargo cinstall` outputs, headers, library files, copied DLLs, compiled C objects | High side-effect test-only build script; invokes nested Cargo, copies native DLLs, compiles C, links `servo_capi` | Needs quarantine policy for test-only native build side effects and release exclusion proof |
| Unit style dummy | `tests/unit/style/build.rs` | `build.rs` only | no meaningful output | none beyond Cargo rerun metadata | No release relevance unless package boundary changes |

## Feature And Environment Sensitivity

The WebIDL generator honors `// skip-unless` comments. The inspected checkout had `556` `.webidl` files and these feature gates:

| Environment variable | Files |
|---|---:|
| `CARGO_FEATURE_BLUETOOTH` | 11 |
| `CARGO_FEATURE_GAMEPAD` | 6 |
| `CARGO_FEATURE_TESTBINDING` | 12 |
| `CARGO_FEATURE_WEBGPU` | 1 |
| `CARGO_FEATURE_WEBXR` | 40 |

Other observed sensitivity:

- `SOURCE_DATE_EPOCH` controls whether the DevTools build id is deterministic or time-derived.
- `PYTHON3`, `uv`, `python3`, and `python` affect Python generator selection.
- `OUT_DIR`, `DEP_SERVO_STYLE_CRATE_OUT_DIR`, and `DEP_SCRIPT_BINDINGS_CRATE_OUT_DIR` determine generator and copy destinations.
- `TARGET`, `CARGO_CFG_TARGET_OS`, `CARGO_CFG_TARGET_ENV`, feature flags, and inferred profile names affect servoshell, OpenHarmony media, Stylo, WebGPU, and script output.
- `git rev-parse --short HEAD` in servoshell affects `GIT_SHA`.
- Native SDK/tool availability affects Windows resources, macOS C compilation, Android linker script behavior, OpenHarmony SDK cfg, and C API test install/copy behavior.

## Source-Family Digests

| Family | Path | Files | Bytes | Method-local digest |
|---|---|---:|---:|---|
| `servo.script_bindings.webidls` | `components\script_bindings\webidls` | 556 | 677548 | `113A26C14B203CE968BE810510E50C6FAEB12A5056DA63415F3C0555C0A019BA` |
| `servo.script_bindings.codegen` | `components\script_bindings\codegen` | 8 | 468627 | `CF0F944DA90C5CC33CDDA1ECF10EC1B42BBFE256654DA78C9124A87AF493537D` |
| `servo.script_bindings.webidl_parser` | `components\script_bindings\third_party\WebIDL\parser` | 85 | 692819 | `623AA1AC4B7994A798CC07D7DC384AD9B456A010CAE891E69AAC5B2B3913A472` |
| `servo.script_bindings.ply` | `components\script_bindings\third_party\ply` | 58 | 407981 | `0C5E89F262BDBF32F8E56FD8BAE0C8B1B33F31820A98A9DA0A5018A8D1C314E2` |
| `servo.script` | `components\script` | 870 | 11199137 | `0CB06BBEC7154CEF7605A2E7F42CBBE37E09C36657AABA8274EE6EB2F40FB1B2` |
| `servo.script_webgpu` | `components\script_webgpu` | 8 | 16591 | `0CADFA7E98D3859BC31AF671647FF0BB1DE3EAC86F94C1C9A9427FEA441B406E` |
| `servo.servoshell.windows` | `ports\servoshell\platform\windows` | 1 | 1148 | `3E33552728EA9A432C661260CC7865313F969DB4C96742D76FFB5E07C910EAC5` |
| `servo.servoshell.macos` | `ports\servoshell\platform\macos` | 3 | 3194 | `3CA7074D6C3CB6B69226F04FB60B26F9E492109A1F48207836ED8BCA4EA77370` |
| `servo.servoshell.openharmony` | `ports\servoshell\platform\openharmony` | 1 | 445 | `D84F553EAACE02E0966FCFC51CD30D3212F18899431372E19999E7EB40CE4B9B` |
| `servo.ffi.capi` | `ffi\capi` | 10 | 77278 | `835E22B405B135A67A374C13F64224C4E63AF698CCD93F8928635B5C781F5697` |
| `servo.tests.capi.c` | `tests\capi\c` | 2 | 18722 | `1AAB9742CFB369DED915A67AEA5A6DD6A7865AFAE071D11354C3138D381598F5` |
| `stylo.style.properties` | `style\properties` | 23 | 957248 | `21FD55319614D359747A1EFF048496867852F0F02FD7690575F0BF0927CC335E` |
| `stylo.stylo_atoms` | `stylo_atoms` | 5 | 5603 | `C5A8DEB28A871D3687E4D7E58667B7853580A9FB862DFE4D14EEDE8EFDA57ADB` |
| `stylo.stylo_static_prefs` | `stylo_static_prefs` | 4 | 7768 | `DF29167F0493183DEA4FBF450893311381C8A55690A316E8D8AA5DFABA9F5822` |
| `stylo.selectors` | `selectors` | 19 | 321474 | `80E08A7E8BFCC2960DA719390E497663FCFECF9E259376BE9F6D33B92B33DF97` |

## Output-Family Observations

Warm full target root: `C:\ts\servo\target\debug\build`

Package-scoped clean target root: `C:\ts\servo-clean-gen-target-dummy-20260718\debug\build`

| Family | Target | Files | Bytes | Method-local digest | Interpretation |
|---|---|---:|---:|---|---|
| `servo-script-bindings` | warm full target | 1631 | 31834655 | `5ED3C006C09694F469CF2F7F18248603208D67DC89947B7CCDCAC4A369324096` | Warm output includes `539` files each under `Bindings`, `ConcreteBindings`, and `WebGPUConcreteBindings` |
| `servo-script-bindings` | package-scoped clean dummy-media target | 1424 | 26512010 | `6EC28EB4E2415983801247F5765DFCF0E48D80409DC9914550A2AD1E9448539A` | Clean package-scoped output includes `470` files each under the binding directories; not comparable as full determinism proof |
| `servo-script` | warm full target | 546 | 1411612 | `9CA16A6C96BED0BD60C25C0EA3218F2BAA2C54FF834900765C14DE1D6ECE4266` | Copy-chain output from script bindings |
| `servo-script-webgpu` | warm full target | 539 | 207471 | `73FA3660BC036278719A83B397166173F74C9A1AFF2C786D880034D3416ADBF8` | WebGPU copy-chain output |
| `servo-devtools` | warm full target | 1 | 40 | `7F664A32E6136B45BAECF3BB98CFA6DE5023F8FF790CEC69DB1070BCC151041C` | Contains `const BUILD_ID: &str = "20260717181128";`; time-derived without pinned `SOURCE_DATE_EPOCH` |
| `servoshell` | warm full target | 2 | 31956 | `D3C35C5CF5E65FD98A3A7C083F7FCE3FEA5DB60653DFED02C6CAE13F769789A0` | Windows resource outputs observed |
| `stylo` | warm full target | 3 | 5285796 | `A126CDCC9E760118692604420EACBA34859B69BEA427B111C01F1BFAE8441431` | Matches the package-scoped clean dummy-media target under this method |
| `stylo` | package-scoped clean dummy-media target | 3 | 5285796 | `A126CDCC9E760118692604420EACBA34859B69BEA427B111C01F1BFAE8441431` | Stable across the two retained local target families under this method |
| `selectors` | warm full and package-scoped clean dummy-media targets | 1 | 1439 | `E628C654EF00D559AA4962134A4BCB647A55C5F0ABAC7C468EA41EE54A6920C9` | Stable across the two retained local target families under this method |
| `stylo_atoms` | warm full and package-scoped clean dummy-media targets | 1 | 64994 | `3D125471ABA923F9C0C6CAD3500777A8224DEEA66EAF712B21BD12D1BA3F949D` | Stable across the two retained local target families under this method |
| `stylo_static_prefs` | warm full and package-scoped clean dummy-media targets | 1 | 15994 | `9EE72B204CC80306A204BDA4FB25084993F2DFF9D2C4968183562730DC4838FD` | Stable across the two retained local target families under this method |

The retained warm and clean package-scoped output families do not prove overall generated-output determinism. In particular, `servo-script-bindings` differs materially between the warm full build and the clean package-scoped dummy-media attempt. That difference is expected to depend on feature profile and build target selection, so the next proof must be feature-correct and tied to an owner-selected profile.

## What This Proves

- First-party Servo and pinned Stylo generator families now have a first-pass manifest with generator paths, primary inputs, output names, and known environment sensitivity.
- The `ADR9-EV-007` gap is narrower than "generator manifest missing"; the remaining blocker is an owner-reviewed generator manifest tied to a selected source baseline, feature profile, target profile, and source-to-output provenance map.
- Some Stylo generated outputs matched across the retained warm and package-scoped clean target observations under this report's digest method.
- The WebIDL/script-bindings family remains feature/profile-sensitive and did not match between the retained warm full output and package-scoped clean dummy-media output.
- The DevTools build id is explicitly time-sensitive unless `SOURCE_DATE_EPOCH` is pinned.
- Servoshell outputs are target/profile/Git-sensitive and require per-target native-output policy.

## What This Does Not Prove

- It does not prove a clean Servo build.
- It does not prove generated-output determinism.
- It does not prove independent-host reproducibility.
- It does not approve any generated file, source file, dependency, native package, unsafe block, FFI contract, component boundary, or Servo source strategy.
- It does not authorize copying Servo source or generated output into Turing release code.
- It does not move `PB-002` out of blocked status.

## Required Next Evidence

Before generated outputs can support an `ADR-0009` decision, Turing still needs:

1. owner-selected Servo source baseline, feature profile, target profile, target platform, and component boundary;
2. owner-reviewed generated-output generator manifest for only that selected baseline/profile;
3. feature-correct full clean-target regeneration diff beyond the package-scoped dummy-media probe;
4. independent-host or owner-approved clean-VM comparison using the same source baseline, features, target, profile, toolchain, environment policy, and digest method;
5. source-to-output license/provenance mapping for every generated family inside any candidate component boundary;
6. accepted policy for time-sensitive, Git-sensitive, platform-sensitive, SDK-sensitive, native-copy, nested-Cargo, and stdout-generated build behavior;
7. dynamic tracing that covers filesystem, process, network, time, environment, compiler, linker, native-copy, and proc-macro behavior;
8. owner approval before any generated-output claim, source import, component approval, or release-code authorization.

## Affected Records

This manifest updates the same `PB-002` and `ADR9-EV-007` queue as:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json);
- checked no-claim [`ADR-0009` decision-review template](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json).

`PB-002` remains blocked and `ADR-0009` remains unresolved.
