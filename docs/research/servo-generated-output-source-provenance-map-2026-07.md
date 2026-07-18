# Servo Generated-Output Source-To-Output Provenance Map - July 2026

Status: first-pass source-to-output provenance map for `PB-002` and `ADR9-EV-007`; no legal approval, generated-code approval, source approval, dependency approval, component approval, release-code authorization, or source-strategy decision

Owner: engine, supply-chain, legal-community, release operations, and quality

Map date: 2026-07-18

Confidence: medium for static source and license-signal observations in the pinned local Servo and Stylo checkouts; low for legal conclusions, generated-output notice sufficiency, release redistribution, and component suitability until owner and legal-community review exist

## Question

Which source and license families feed the first-party Servo and pinned Stylo generated-output families already mapped in the [Servo Generated-Output Generator Manifest - July 2026](servo-generated-output-generator-manifest-2026-07.md), and what remains before Turing can treat those generated outputs as decision-grade `ADR-0009` evidence?

This report is not legal advice and does not approve copying, regenerating, vendoring, translating, or distributing Servo source or generated outputs inside Turing.

## Scope

Included:

- first-party Servo generator families under `components/`, `ports/`, `ffi/`, and `tests/` that were identified by the generated-output manifest;
- the pinned Cargo git checkout for `servo/stylo` used by the local Servo build baseline;
- static license-signal inspection of generator source, generator inputs, package metadata, and vendored Python wheel metadata that feeds first-party generated-output families;
- source-to-output provenance handoff rows for each generated-output family.

Excluded:

- legal approval, notice-file approval, source-offer approval, patent review, or redistribution approval;
- per-file generated Rust or generated header review;
- registry build scripts and proc macros except where they are direct generator dependencies named below;
- dynamic tracing of build-script or proc-macro behavior;
- any decision about whether Servo-derived source can enter release code.

## Source Identity

| Source | Local path | Identity | Working-tree note |
|---|---|---|---|
| Servo checkout | `C:\ts\servo` | commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d` | `main...origin/main [behind 2]`; evidence is dated to this local tree |
| Stylo Cargo git checkout | `C:\Users\bcw19\.cargo\git\checkouts\stylo-482338307e42a9ea\d3de91c` | commit `d3de91cbac7bba38e159239b3c0a360783fce2ee`, tree `d4bd206aeb9bf5d5dfd333cf1cce7a879dbc07e9` | Cargo checkout showed an untracked `.cargo-ok` marker; no source approval is inferred |

## Method

The pass used static inspection only:

1. verified local Git commit and tree IDs for Servo and Stylo;
2. inspected Servo root `LICENSE` and `LICENSE_WHATWG_SPECS`;
3. inspected `Cargo.toml` license expressions for `servo-script-bindings`, `stylo`, `selectors`, `stylo_atoms`, and `stylo_static_prefs`;
4. sampled generator source headers for Servo WebIDL binding codegen, WebIDL parser, DevTools build ID, selectors PHF generation, Stylo atom generation, and Stylo CSS property generation;
5. counted WebIDL license markers across the `556` `.webidl` files already identified by the generator manifest;
6. inspected PLY, Mako, TOML, and MarkupSafe license-signal files or wheel metadata where those packages feed the generator pipeline.

No Servo source, generated output, native binary, wheel, package metadata file, or build log was copied into this repository.

## Observed Source And License Signals

| Source family | Observed signal | Provenance implication | Remaining review gap |
|---|---|---|---|
| Servo repository root | Root `LICENSE` is MPL-2.0 text | Servo first-party source appears MPL-covered unless a file or imported source says otherwise | Owner and legal-community review still need selected-baseline file coverage and notice handling |
| WHATWG specification portions | `LICENSE_WHATWG_SPECS` applies BSD 3-Clause terms to WHATWG specification portions incorporated into source | Standards-derived portions need notice and endorsement-condition handling if redistributed | Per-file mapping from WebIDL/spec text into generated outputs remains owner-review material |
| `servo-script-bindings` package | `components/script_bindings/Cargo.toml` declares `MPL-2.0 AND BSD-3-Clause` and attributes BSD-3-Clause to PLY build-time use | The WebIDL binding generator has at least MPL and BSD-3-Clause source/license inputs | The package comment says PLY is build-time and does not end up in produced artifacts; Turing still needs owner/legal acceptance of that conclusion |
| WebIDL source corpus | All `556` `.webidl` files matched MPL license text; `9` files also matched "waived all copyright" standard-text markers | WebIDL inputs are not unlicensed in the observed tree, but they include mixed standard-text provenance signals | A selected component boundary still needs a per-file ledger and generated-output notice policy |
| WebIDL parser | `third_party/WebIDL/parser/WebIDL.py` carries an MPL-2.0 source header | Parser source signal is MPL-2.0 in the sampled primary file | Full parser directory and generated-output obligations need owner review |
| PLY | `third_party/ply/README.md` contains BSD-style redistribution terms; `servo-script-bindings` package metadata identifies BSD-3-Clause | PLY is a build-time parser dependency in the WebIDL generator path | Need final notice/source-offer treatment for build-only generator inputs and the generated-output boundary |
| Stylo crates | `style`, `selectors`, `stylo_atoms`, and `stylo_static_prefs` package manifests declare `MPL-2.0` | First-party Stylo generator crates and source families appear MPL-covered by crate metadata and sampled headers | The Cargo git checkout lacked a top-level license file in the inspected root, so owner review must rely on crate metadata, source headers, upstream records, and selected-baseline policy |
| Stylo CSS generator Python inputs | `style/properties/build.py` imports vendored `mako-1.3.10`, `toml-0.10.2`, and local `markupsafe` | CSS property generation has vendored Python license inputs in addition to MPL Stylo templates/data | Notice treatment for wheel-contained metadata and generated `properties.rs`/JSON/HTML remains unresolved |
| Mako wheel | Wheel metadata and bundled license identify MIT terms | Build-time template engine license needs notice decision if treated as part of generated-output provenance | Legal-community review must decide whether and how build-time MIT notices flow to generated-output notices |
| TOML wheel | Wheel metadata and bundled license identify MIT terms | Build-time TOML parser license needs notice decision if treated as part of generated-output provenance | Legal-community review must decide whether and how build-time MIT notices flow to generated-output notices |
| MarkupSafe vendored source | Local `markupsafe\LICENSE.txt` contains a three-clause BSD-style notice | Build-time escaping dependency has a separate notice family | Legal-community review must normalize the exact expression and notice handling |
| DevTools build ID generator | `components/devtools/build.rs` is MPL-2.0 and emits a timestamp string, using `SOURCE_DATE_EPOCH` when present | Output provenance is primarily generator code plus build environment time input | Release policy must decide deterministic build identity treatment |
| Servoshell resource generator | `ports/servoshell/build.rs` and platform resources are first-party generator inputs but are target-sensitive | Output may include Windows resource files, Git identity, target profile, and native toolchain effects | Per-target resource provenance, icon/manifest review, and package notice treatment remain unresolved |
| C API test install/copy | Test-only generator invokes nested Cargo, copies native files, and compiles C tests | Provenance is high side-effect and should be quarantined from release evidence unless selected | Need test-only exclusion proof or explicit release-boundary review |

## Source-To-Output Map

| Generated-output family | Source and license families observed | Output families affected | What this map proves | What still blocks `ADR9-EV-007` closure |
|---|---|---|---|---|
| Web IDL and script bindings | Servo MPL generator code; `556` MPL-marked WebIDL files; `9` WebIDL files with additional copyright-waiver markers; MPL WebIDL parser; BSD-3-Clause PLY; Stylo CSS properties as upstream generated input | `Bindings/`, `ConcreteBindings/`, `WebGPUConcreteBindings/`, interface maps, inheritance/type files, union files, event handler names, `doc/apis.html` | The major source/license families for WebIDL binding generation are identified at first pass | Needs selected feature profile, per-file WebIDL ledger, source-to-generated-file notice policy, owner-reviewed PLY build-only conclusion, clean full-target regeneration, and independent-host comparison |
| Script copy outputs | Upstream WebIDL/script-binding outputs plus MPL `components/script/build.rs` copy logic | copied root binding files and `ConcreteBindings/` subset | Copy-chain provenance is inherited from the WebIDL generator family rather than newly authored by the copy script | Needs copy-chain ledger and generated-output notice preservation policy |
| WebGPU binding copy outputs | Upstream WebIDL/script-binding outputs plus MPL `components/script_webgpu/build.rs` copy logic | `WebGPUConcreteBindings/` subset copied into local output | WebGPU copy outputs inherit the broader binding provenance and feature gates | Needs WebGPU feature policy and selected component-boundary review |
| Stylo CSS properties | Stylo MPL source/templates/data; Mako MIT wheel; TOML MIT wheel; MarkupSafe BSD-style notice; Python and `OUT_DIR` environment | `properties.rs`, `css-properties.json`, `css-properties.html`, Servo documentation copies | Direct generator and vendored Python package license signals are identified | Needs owner-reviewed notice/source-offer decision for generated Rust/JSON/HTML and wheel-contained license metadata |
| Selectors PHF attributes | Stylo `selectors` MPL source; hardcoded WHATWG-linked attribute list; `phf_codegen` build dependency | `ascii_case_insensitive_html_attributes.rs` | Primary source family and standard reference are visible | Needs dependency/version provenance and generated-output notice decision for selected profile |
| Stylo atoms | Stylo MPL source; `static_atoms.txt`; `predefined_counter_styles.rs`; `string_cache_codegen` build dependency | `atom.rs` | Atom source files and generator crate are identified | Needs atom input review, dependency provenance, and output notice policy |
| Stylo static prefs | Stylo MPL source; `preferences.toml`; Rust `toml` build dependency | `generated.rs` and stdout generated Rust text | Preference source and parser dependency are identified | Needs stdout-generated-artifact policy and dependency notice decision |
| DevTools build ID | Servo MPL `components/devtools/build.rs`; `SOURCE_DATE_EPOCH` or current UTC time | `build_id.rs` | Output is environment-derived and tiny, not standards-derived source content | Needs deterministic release-build identity policy |
| Servoshell resource and identity outputs | Servo MPL build script; Windows icon/manifest/resource data; target cfg; profile path; Git state; platform SDK/resource toolchain | Windows `resource.rc`/`resource.res`, Android linker shim, macOS C object/link args, `GIT_SHA` env | Target/profile/Git/toolchain sensitivity is known | Needs platform-resource provenance, native-toolchain provenance, and per-target package notice review |
| Shared embedder profile cfg | Servo MPL build script; `OUT_DIR` profile inference | Rust cfg only | Profile inference is a build input, not a file source | Needs release profile policy if reused |
| OpenHarmony media SDK cfg | Servo MPL build script; external `OHOS_SDK_NATIVE` package metadata when targeting OpenHarmony | Rust cfg and warnings only | External SDK metadata is a conditional source input | Needs SDK provenance policy before OpenHarmony release work |
| C API test install and native copy | Servo MPL C API/test sources; nested Cargo outputs; native DLL/library/header files | test install outputs, copied DLLs, compiled C objects | The family is high side-effect and test-scoped in the observed manifest | Needs release exclusion proof or a full native/package provenance review if selected |

## What This Proves

- A first-pass source-to-output provenance map now exists for the generated-output families already identified by the generator manifest.
- The WebIDL corpus had `556` `.webidl` files with MPL license markers in the inspected tree; `9` also had copyright-waiver standard-text markers.
- The WebIDL binding generator path includes MPL source families plus BSD-3-Clause PLY signals.
- The Stylo CSS property generator path includes MPL Stylo source plus MIT Mako, MIT TOML, and BSD-style MarkupSafe license signals.
- The remaining `ADR9-EV-007` blocker is narrower than "source-to-output map missing"; it is now owner-reviewed source-to-output license/provenance approval for a selected baseline, feature profile, target profile, output-family set, generator-version set, and component boundary.

## What This Does Not Prove

- It does not approve any license expression, notice file, source-offer obligation, patent posture, generated file, source file, dependency, native package, unsafe block, FFI boundary, component boundary, or Servo source strategy.
- It does not prove clean-target generation, generated-output determinism, independent-host reproducibility, or dynamic build-script behavior.
- It does not prove that build-time dependency notices do or do not flow into generated outputs.
- It does not authorize copying Servo source or generated output into Turing release code.
- It does not move `PB-002` out of blocked status.

## Required Next Evidence

Before generated outputs can support an `ADR-0009` decision, Turing still needs:

1. owner-selected Servo source baseline, feature profile, target profile, target platform, and candidate component boundary;
2. owner-reviewed generated-output generator manifest for only that selected baseline/profile;
3. owner-reviewed source-to-output license/provenance approval for every generated family inside the selected component boundary, including build-time dependency notice treatment;
4. feature-correct full clean-target regeneration diff beyond the package-scoped dummy-media probe;
5. independent-host or owner-approved clean-VM comparison using the same source baseline, feature profile, target profile, toolchain, environment policy, and digest method;
6. accepted policy for time-sensitive, Git-sensitive, platform-sensitive, SDK-sensitive, native-copy, nested-Cargo, stdout-generated, and wheel-contained build inputs;
7. dynamic tracing of filesystem, process, network, time, environment, compiler, linker, native-copy, and proc-macro behavior;
8. owner approval before any generated-output claim, source import, component approval, or release-code authorization.

## Affected Records

This map updates the same `PB-002` and `ADR9-EV-007` queue as:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json);
- checked no-claim [`ADR-0009` decision-review template](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json);
- [Servo Generated-Output Generator Manifest - July 2026](servo-generated-output-generator-manifest-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Clean Generated-Output Reproduction Probe - July 2026](servo-clean-generated-output-reproduction-2026-07.md).

`PB-002` remains blocked and `ADR-0009` remains unresolved.
