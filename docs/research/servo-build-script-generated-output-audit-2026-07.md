# Servo Build-Script and Generated-Output Audit - July 2026

Status: dated external audit for `PB-002` and proposed `ADR-0009`; no generated-output, build-script, dependency, native, or source approval
Owner: architecture, security, provenance, release operations, engine, and embedding owners
Audit date: 2026-07-17
Confidence: medium for the inspected Windows dev build outputs and first-party Servo build scripts; low for full provenance until clean rebuild, source-to-output mapping, registry/git build-script review, and owner audit run

## Question

What build-script side effects and generated outputs does the clean external Servo Windows development build expose, and what remains before Turing can trust any generated output or build-time behavior for a source-strategy decision?

This audit does not import Servo source, generated Rust, Cargo metadata, build logs, native binaries, or timing artifacts into Turing. It does not approve Servo-derived release code, a generated-code pipeline, a build script, a proc macro, a native package, or an `ADR-0009` option.

A follow-up [Servo Clean Generated-Output Reproduction Probe - July 2026](servo-clean-generated-output-reproduction-2026-07.md) records a partial package-scoped clean-target attempt and failure analysis for `ADR9-EV-007`. The [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md) expands this first-party build-script review into a registry, git, path, and proc-macro side-effect queue. A later [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md) records local source archive, tracked-file manifest, Cargo registry cache, Stylo git-source, and native/bootstrap artifact identity evidence for the same checkout.

## Inputs

External checkout:

- workspace: `C:\ts\servo`;
- remote: `https://github.com/servo/servo.git`;
- commit: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- commit date: 2026-07-17T15:50:14Z;
- commit subject: `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)`;
- tracked files: `193033`;
- tracked-file status after the incremental rebuild: clean.

External evidence locations:

- `C:\ts\servo\target\debug\build`;
- `C:\ts\servo\target\cargo-timings\cargo-timing-20260717T184252676Z-d205ee0048504b27.html`;
- Servo source inputs under `C:\ts\servo\components\script_bindings`;
- Cargo metadata from the earlier [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md).

No external artifact was copied into this repository.

## Method

The audit combined:

1. static inspection of Servo first-party workspace `build.rs` files;
2. aggregation of Cargo `target\debug\build\*\out` directories;
3. hashing of key generated-output directories and generator inputs;
4. aggregation of Cargo build-script `output` logs;
5. one incremental no-op Servo rebuild from a Visual Studio 2022 Developer Command Prompt with `C:\Program Files\LLVM\bin` prepended to `PATH`;
6. before/after digest comparison for the most relevant first-party generated outputs.

The incremental rebuild command was executed outside Turing:

```powershell
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64 && set "PATH=C:\Program Files\LLVM\bin;%PATH%" && cd /d C:\ts\servo && powershell -NoProfile -ExecutionPolicy Bypass -File .\mach.ps1 build --dev -j 8'
```

The rebuild exited `0`, reported `Succeeded in 0:00:03`, and Cargo reported `Finished dev profile [unoptimized + debuginfo] target(s) in 3.26s`.

## Target output aggregate

The Windows debug build had `103` Cargo `out` directories under `target\debug\build`.

| Metric | Observation |
|---|---:|
| Files under `out` directories | `3955` |
| Total bytes under `out` directories | `1106039671` |
| `.rs` files | `2750` |
| `.o` files | `865` |
| `.h` files | `96` |
| `.frag` files | `77` |
| `.vert` files | `77` |
| `.obj` files | `29` |
| `.lib` files | `23` |
| `.a` files | `18` |

Largest `out` directories by byte size:

| Package output directory | Files | Bytes | Directory SHA-256 |
|---|---:|---:|---|
| `mozjs_sys-fdc673c367d9ea26` | 6 | 460924710 | `E9841F427C71D2BAC8D9C17A0183FE93A18A949F9C76354EC478545721218423` |
| `mozangle-a07193457b2ee42d` | 418 | 395961463 | `1A393BD356D402884C5F75C438F722610202C32A1C493F0D0D916B6D24E0220E` |
| `harfbuzz-sys-4359fb0aab0cac3a` | 5 | 68796986 | `FE9F25DC298B1BD35E7B69649A3F8133BA9A99EDDC17808E0D18D607FF08FA0A` |
| `aws-lc-sys-00ec88c29e213980` | 376 | 43979698 | `C385F428D4C15AF59AEB670D5442D59F87FB110BBBCFE6BD403C565FE2619996` |
| `fontsan-5bce5bd082bcf255` | 53 | 38649198 | `3C6F7DF5900E939B7D3C2EA91D1929F3AD718CE2CDEC5493AC16C9D8B2F9CF83` |
| `servo-script-bindings-760806860634f27a` | 1631 | 31834655 | `8154347D4FDD1025460FE34F8FF0F6DE122A99D3E98AB1855EACAB3044194407` |
| `glslopt-ff0702704df06335` | 136 | 19214848 | `5CC8DF6EA417DFFC02C2EE0A9BCD31B175853805B64FB926EBCB065CFA5120CE` |
| `zstd-sys-5b379a33df46b7ce` | 31 | 17456799 | `F57132423D36ECF1632D704C5E79C9A20DB409E624A8A4BC099D6566A867C8B3` |
| `libsqlite3-sys-fef88bcc6c0a01ba` | 4 | 17320303 | `B6D61DD30345B926550BA989CF748002AEB11D9B8ACCE8216C2D843FF261642F` |
| `stylo-2e2b00a19ba7979d` | 3 | 5285796 | `308C691B8C227CBF9E29EBB30E7F518D5F467AF994BE32D84CC02B11DB1D4040` |

Interpretation: Servo's generated and build-script output footprint is dominated by JavaScript runtime bindings/native objects, ANGLE/GPU-related output, cryptography/native library output, font/text output, Stylo CSS property output, and Web IDL script bindings. A selective-component review cannot focus only on Servo workspace `build.rs` files; registry and git build scripts are material.

## First-party generated outputs

First-party Servo outputs relevant to the source-strategy decision:

| Output directory | Files | Bytes | Directory SHA-256 | Role |
|---|---:|---:|---|---|
| `servo-script-bindings-760806860634f27a\out` | 1631 | 31834655 | `8154347D4FDD1025460FE34F8FF0F6DE122A99D3E98AB1855EACAB3044194407` | Web IDL, binding, interface, and PHF generated outputs |
| `servo-script-750c46672604cae6\out` | 546 | 1411612 | `56FDC67766E1EA420191347D97CBBB32B9BC45F23479702B43142F131CB00A03` | Copied binding include files and concrete binding subset |
| `servo-script-webgpu-7bf90398b3102e6f\out` | 539 | 207471 | `DAABC01B09865B28208EE478E85B51769B9793AF3E9E165B208DD3913DD50B76` | Copied WebGPU concrete binding subset |
| `servo-devtools-6a2f983bebc6b196\out` | 1 | 40 | `ABB50A98A282F56561C47CFF6ACC18A274865B1466046DC8DDD475F64823893F` | Generated DevTools build ID |
| `servoshell-f8d8317c93a0c3d2\out` | 2 | 31956 | `6AA9C674E7E55C719F2E0A9BAA12F757BEB72E869BC84CFA30BF7DF0478B5D8F` | Windows resource source and compiled resource |
| `servo-embedder-traits-49064695d4281c26\out` | 0 | 0 | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | No emitted files in this build |

Largest files in `servo-script-bindings` output included:

| File | Bytes |
|---|---:|
| `Bindings/CSSStyleDeclarationBinding.rs` | 4567498 |
| `Bindings/WebGPUBinding.rs` | 1415574 |
| `Bindings/TestBindingBinding.rs` | 1356853 |
| `Bindings/WebGL2RenderingContextBinding.rs` | 939997 |
| `Bindings/WindowBinding.rs` | 859990 |
| `Bindings/DocumentBinding.rs` | 778160 |
| `Bindings/WebGLRenderingContextBinding.rs` | 549941 |
| `Bindings/HTMLElementBinding.rs` | 539182 |
| `Bindings/ElementBinding.rs` | 505976 |
| `Bindings/SVGElementBinding.rs` | 465684 |

Largest files in `servo-script` output included `InterfaceObjectMapPhf.rs`, `ConcreteBindings/WebGPUBinding.rs`, `ConcreteInheritTypes.rs`, `DomTypeHolder.rs`, `InterfaceTypes.rs`, and `ConcreteBindings/mod.rs`.

## Generator inputs

Important source inputs and hashes:

| Input | Files or bytes | SHA-256 |
|---|---:|---|
| `components/script_bindings/webidls` | 556 files, 677548 bytes | `CC8899F014EAEA4D9B8E033A96E1B8FFB984A21A4D09DB9F6190F3320BB9E650` |
| `components/script_bindings/codegen` | 8 files, 468627 bytes | `1186569A18FB1FB8A935D294634BD7CE7D9E2F2AB3309F0AA90B964346E7AF16` |
| `components/script_bindings/third_party/WebIDL/parser` | 85 files, 692819 bytes | `738774A20CBA9E1911ADE599CCE77B77CB078C8616DD5BE4BBDB9DAF9C43C9B3` |
| `components/script_bindings/third_party/ply` | 58 files, 407981 bytes | `5E457D7BD42215DE152DF0CF9549E24332860391238F1E5742F5AA1F3C216CE1` |
| `components/script_bindings/codegen/run.py` | 9450 bytes | `080A8BA53F30EA8F8D34450016DF0EF91D82BCD9286109226140C3890DD99C53` |
| `components/script_bindings/third_party/WebIDL/parser/WebIDL.py` | 341826 bytes | `BFA9D2F3415F83D8E1A98395DA25FFB681A45D8FBDE24A774BA23315176953AA` |
| `target\debug\build\stylo-2e2b00a19ba7979d\out\css-properties.json` | 30777 bytes | `70C7D0548B0DE4581518E359EEDAF73E3D97F299190F0A8007BFB0160731C2C4` |
| `target\debug\build\stylo-2e2b00a19ba7979d\out\properties.rs` | 5200754 bytes | `B892FE3A571F3A84EEECFEA850306EB15799DFE28A61B076D3A110C2ED311D7C` |
| `target\debug\build\servo-script-bindings-760806860634f27a\out\InterfaceObjectMapData.json` | 139097 bytes | `CD3E8BE71B1B548EDD1275584FB31D8A27FBD3332FDE09ABB287A83E0D1D657B` |
| `.python-version` | 5 bytes | `49A506DD32096B010D75205ACF3430C9AE6C40351888129499E5A5E487126C93` |
| `pyproject.toml` | 2030 bytes | `9075A97B263AB5DC50CBAC9C2AF6A706B0157E2A4899FF10A508EA55216757C6` |
| `uv.lock` | 391884 bytes | `CA623E5DFED45A6C66BB57ADAC96BE3C2FFBE0D0ECCA5E1D41C095CB65B96B1C` |
| `rust-toolchain.toml` | 506 bytes | `7E0DB2338E617768287E08D93B3BBE34BF2706F0E7AA58BA61250ED40BE85F2A` |
| `Cargo.lock` | 297294 bytes | `327FDD559E87B0D18A4B24B201D9254E06C56D59C38388EDD37236F25BA47E22` |

Large Web IDL inputs included `WebGPU.webidl`, `WebGL2RenderingContext.webidl`, `WebGLRenderingContext.webidl`, `TestBinding.webidl`, `CanvasRenderingContext2D.webidl`, `SubtleCrypto.webidl`, `Document.webidl`, `EventHandler.webidl`, `Window.webidl`, and `Element.webidl`.

## No-op rebuild stability

The incremental rebuild did not change the inspected generated-output directory digests.

| Output directory | Before | After |
|---|---|---|
| `servo-script-bindings-760806860634f27a\out` | `1631` files, `31834655` bytes, `8154347D4FDD1025460FE34F8FF0F6DE122A99D3E98AB1855EACAB3044194407` | same |
| `servo-script-750c46672604cae6\out` | `546` files, `1411612` bytes, `56FDC67766E1EA420191347D97CBBB32B9BC45F23479702B43142F131CB00A03` | same |
| `servo-script-webgpu-7bf90398b3102e6f\out` | `539` files, `207471` bytes, `DAABC01B09865B28208EE478E85B51769B9793AF3E9E165B208DD3913DD50B76` | same |
| `servo-devtools-6a2f983bebc6b196\out` | `1` file, `40` bytes, `ABB50A98A282F56561C47CFF6ACC18A274865B1466046DC8DDD475F64823893F` | same |
| `stylo-2e2b00a19ba7979d\out` | `3` files, `5285796` bytes, `308C691B8C227CBF9E29EBB30E7F518D5F467AF994BE32D84CC02B11DB1D4040` | same |

This is useful but limited evidence. It proves the inspected directories were stable across one no-op incremental build on the same checkout and host. It does not prove deterministic generation from a clean target directory, independent-host reproducibility, hermeticity, or suitability for Turing.

## Build-script side effects

First-party build-script side effects observed from source inspection and build-script output logs:

| Script | Inputs and side effects | Risk for Turing |
|---|---|---|
| `components/script_bindings/build.rs` | Reads `DEP_SERVO_STYLE_CRATE_OUT_DIR`, `OUT_DIR`, Web IDL files, codegen scripts, WebIDL parser, PLY, and Stylo `css-properties.json`; executes `uv run --frozen python` when available, then falls back to `python3` or `python`; writes binding outputs and `InterfaceObjectMapPhf.rs` | Python/tool resolution, generated binding provenance, Stylo coupling, and fallback behavior need hermetic policy |
| `components/script/build.rs` | Reads `DEP_SCRIPT_BINDINGS_CRATE_OUT_DIR`; copies interface files and `ConcreteBindings` into its own `OUT_DIR`; emits rerun paths | Copy-only outputs still need source-to-output mapping and regeneration checks |
| `components/script_webgpu/build.rs` | Reads `DEP_SCRIPT_BINDINGS_CRATE_OUT_DIR`; copies `WebGPUConcreteBindings` into its own `OUT_DIR` | WebGPU subset depends on broader generated binding output |
| `components/devtools/build.rs` | Reads `SOURCE_DATE_EPOCH`; uses current UTC time when absent; writes `build_id.rs` | Non-deterministic unless release builds set `SOURCE_DATE_EPOCH` |
| `components/shared/embedder/build.rs` | Infers production or non-production cfg from `OUT_DIR` path | Profile detection by path needs policy before release use |
| `ports/servoshell/build.rs` | Runs `git rev-parse --short HEAD`; reads Cargo target cfg; compiles Windows resources in this build; can compile macOS C source, write Android linker shim, and set platform linker arguments | Depends on git state, platform SDK/resource tools, and platform-specific link behavior |
| `components/media/backends/ohos/build.rs` | Reads `CARGO_CFG_TARGET_ENV`; if OpenHarmony, reads `OHOS_SDK_NATIVE` and `oh-uni-package.json`; emits SDK cfg values | Platform SDK metadata becomes a build input |
| `tests/capi/build.rs` | Runs nested `cargo cinstall`; uses a separate `target\cinstall`; copies DLLs on Windows; compiles C API tests | Nested Cargo, DLL copying, C compilation, and MAX_PATH workarounds require isolation |
| `tests/unit/style/build.rs` | Emits rerun path only | Low first-party side-effect surface |

Cargo build-script output logs across all build scripts contained:

| Metric | Count |
|---|---:|
| Build-script `output` logs | `103` |
| Output-log lines | `41890` |
| Output-log bytes | `7587113` |
| `rerun-if-env-changed` markers | `11685` |
| `rerun-if-changed` markers | `11013` |
| `warning` marker occurrences | `4856` |

Largest output logs were from `mozangle`, `aws-lc-sys`, `glslopt`, `mozjs_sys`, `fontsan`, `zstd-sys`, `libz-sys`, `webrender`, `harfbuzz-sys`, and `libsqlite3-sys`. These registry and native-facing build scripts remain unreviewed under Turing policy.

The incremental `mach` build also copied ANGLE, GStreamer, and MSVC DLLs to the binary directory. That copy behavior is part of Servo's local build experience and packaging surface, not just Rust build-script behavior.

## Interpretation

Observations:

- Servo's build produces large generated and build-script outputs even for a Windows debug build.
- The first-party Web IDL binding pipeline is anchored by hundreds of Web IDL files, Python codegen, a vendored WebIDL parser, PLY, and Stylo-generated CSS properties.
- The no-op incremental rebuild kept key first-party output digests stable on the same host.
- Some build behavior is explicitly environment-sensitive: `SOURCE_DATE_EPOCH`, Python command discovery, `OUT_DIR` path profile inference, `OHOS_SDK_NATIVE`, target cfg, git state, platform SDK paths, and native toolchain discovery.
- Registry and git build scripts dominate byte size and output-log volume in high-risk areas such as MozJS, ANGLE, AWS-LC, HarfBuzz, SQLite, GStreamer, zlib, Zstandard, and WebRender.

Inference:

The first-party Servo generated-output pipeline is now partially mapped, but not proven acceptable. A Turing adoption or selective-component proposal still needs a clean, hermetic regeneration check with source-to-output mapping, independent-host reproduction, accepted build-script/proc-macro side-effect policy, dynamic tracing, license/provenance review for generated files, and explicit release controls for environment variables and native tools.

## What this does not prove

This audit does not prove:

- generated outputs are correct, complete, deterministic from a clean tree, or safe;
- Python, WebIDL parser, PLY, Stylo, proc macros, or registry build scripts are acceptable under Turing policy;
- any generated output can be copied, reused, or translated into Turing;
- build scripts avoid network access in every configuration;
- build scripts are hermetic or reproducible across machines;
- environment-sensitive outputs are acceptable for release builds;
- native, JavaScript, GPU, media, storage, or font outputs are licensed, sandboxed, audited, or redistributable;
- Servo is compatible, secure, low memory, high performance, accessible, Chrome-class, or production-ready.

## Next evidence required

Before `ADR-0009` can advance, produce:

1. a feature-correct full clean-target regeneration run beyond the package-scoped dummy-media probe, with before/after source and output hashes;
2. independent-host generated-output comparison for the same commit, features, target, and profile;
3. explicit generator manifests for Web IDL, CSS properties, WebGPU, DevTools build IDs, C API headers, bindgen outputs, proc macros, shaders, native build glue, and SDKs;
4. owner-accepted build-script/proc-macro side-effect policy and dynamic tracing, starting from the [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md), covering process execution, filesystem writes, network behavior, environment variables, compiler/linker invocation, platform SDK discovery, native-copy behavior, and native artifacts;
5. a policy for `SOURCE_DATE_EPOCH`, Python/`uv` fallback, `OUT_DIR` profile inference, git-derived version strings, `OHOS_SDK_NATIVE`, nested Cargo, DLL copying, and platform resource compilation;
6. license/provenance and source-offer review for generated outputs and any generated headers;
7. sandbox and packaging review for native artifacts copied by `mach` or produced by build scripts;
8. generated-output diff review tied to any candidate component boundary.

## Affected records

This audit adds evidence for `PB-002` but does not change its blocked status. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md);
- [Servo Clean Generated-Output Reproduction Probe - July 2026](servo-clean-generated-output-reproduction-2026-07.md);
- [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md);
- [Servo Supply-Chain Policy Scan - July 2026](servo-supply-chain-policy-scan-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md);
- [Security, privacy, and sandbox](../blueprint-v1/08-security-and-sandbox.md);
- [Testing, compatibility, fuzzing, and quality gates](../blueprint-v1/12-testing-compatibility.md);
- [Build, release, distribution, and operations](../blueprint-v1/13-build-release-operations.md).
