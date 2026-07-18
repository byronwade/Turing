# Servo Clean Generated-Output Reproduction Probe - July 2026

Status: partial clean-target generated-output probe for `PB-002` and `ADR9-EV-007`; no clean Servo build, generated-output determinism proof, generated-code approval, source approval, dependency approval, component approval, or release-code authorization
Owner: architecture, engine, supply-chain, release operations, and quality owners
Probe date: 2026-07-18
Confidence: medium for the local Windows log, target-directory, and hash observations; low for determinism, provenance, and source-strategy conclusions until a feature-correct full clean-target replay and independent-host comparison exist

## Question

Can selected Servo generated outputs be regenerated from a clean external target directory without relying on the previously warm Servo target, and what remains before `ADR9-EV-007` can be treated as decision-grade generated-output evidence?

This probe does not import Servo source, generated Rust, Cargo output, native binaries, build logs, Cargo timing HTML, or target directories into Turing. It does not approve Servo, generated outputs, build scripts, proc macros, native packages, dependencies, or any `ADR-0009` option.

## Inputs

External checkout:

- workspace: `C:\ts\servo`;
- remote: `https://github.com/servo/servo.git`;
- commit: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- tree: `daa2bc0e189e1981fb021501065fc3466159b00d`;
- branch status: `main...origin/main [behind 2]`;
- tracked files: `193033`;
- tracked-file changes before and after the probe: `0`.

Reference environment:

| Tool | Observation |
|---|---|
| Rust | `rustc 1.95.0 (59807616e 2026-04-14)` |
| Cargo | `cargo 1.95.0 (f2d3ce0bd 2026-03-21)` |
| Python | `Python 3.12.10` |
| `uv` | `uv 0.11.29 (901092ee1 2026-07-15 x86_64-pc-windows-msvc)` |
| MSVC compiler | `Microsoft (R) C/C++ Optimizing Compiler Version 19.44.35221 for x64` |
| MSVC linker | `Microsoft (R) Incremental Linker Version 14.44.35221.0` |
| LLVM linker | `LLD 22.1.8` at `C:\Program Files\LLVM\bin\lld-link.exe` |

External evidence locations:

- first target: `C:\ts\servo-clean-gen-target-20260718`;
- second target: `C:\ts\servo-clean-gen-target-dummy-20260718`;
- first stdout log: `C:\ts\servo-clean-gen-20260718.out.log`;
- first stderr log: `C:\ts\servo-clean-gen-20260718.err.log`;
- second stdout log: `C:\ts\servo-clean-gen-dummy-20260718.out.log`;
- second stderr log: `C:\ts\servo-clean-gen-dummy-20260718.err.log`.

No external evidence file was copied into this repository.

## Method

The probe used two isolated Cargo target directories outside the Turing repository:

1. A package-scoped clean-target attempt with default media configuration:

```powershell
$env:CARGO_TARGET_DIR = "C:\ts\servo-clean-gen-target-20260718"
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64 && set "PATH=C:\Program Files\LLVM\bin;%PATH%" && cd /d C:\ts\servo && powershell -NoProfile -ExecutionPolicy Bypass -File .\mach.ps1 build --dev -j 8 -p servo-script-bindings'
```

2. A package-scoped clean-target attempt with `--media-stack dummy` to bypass the missing GStreamer prerequisite:

```powershell
$env:CARGO_TARGET_DIR = "C:\ts\servo-clean-gen-target-dummy-20260718"
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64 && set "PATH=C:\Program Files\LLVM\bin;%PATH%" && cd /d C:\ts\servo && powershell -NoProfile -ExecutionPolicy Bypass -File .\mach.ps1 build --dev -j 8 --media-stack dummy -p servo-script-bindings'
```

The retained stdout and stderr logs are treated as the authoritative run evidence. The shell wrapper exit code alone is not sufficient because the package-scoped runs can leave a wrapper success value even when the `mach` log records a build failure.

## Run Results

| Run | Target | Result | Evidence |
|---|---|---|---|
| Default media stack | `C:\ts\servo-clean-gen-target-20260718` | Failed before Cargo build output because GStreamer libraries were not present | stdout downloaded and extracted `moztools-4.0`, then reported `FileNotFoundError: GStreamer libraries not found (>= version 1.18).Please see installation instructions in README.md` |
| Dummy media stack | `C:\ts\servo-clean-gen-target-dummy-20260718` | Reached Cargo generation and compilation, then failed in `mozjs_sys` | stdout reported `Failed in 0:02:20`; stderr reported `error: failed to run custom build command for mozjs_sys v140.12.0-2`, `jit feature is NOT enabled. Building from source directly.`, and a panic at `build.rs:686:35` from `called Option::unwrap() on a None value` |

Log and target facts:

| Artifact | Observation |
|---|---|
| First stdout SHA-256 | `B8464FC690F1FB0853F83C3E9953AFC25E529E18899C83042D1D5EFC9CE8B6BA` |
| First stderr SHA-256 | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| First target size | `14824` files, `344561599` bytes |
| First target Cargo `out` directories | none under `debug\build` |
| Second stdout SHA-256 | `1F5FEA9D76E81563243C1F29DA75DB1C73F4C18D148CB86F8A2810CD4A099209` |
| Second stderr SHA-256 | `70AA8D697DCFB5D6AE1892A8E8D8D7360130CA788E477BA8EBEB406CB7F5A591` |
| Second target size | `19725` files, `2105768633` bytes |
| Second target Cargo `out` directories | `48` under `debug\build` |
| Second target build-script output logs | `46` files, `1702323` bytes |
| Cargo timing report | `C:\ts\servo-clean-gen-target-dummy-20260718\cargo-timings\cargo-timing-20260718T164818040Z-d205ee0048504b27.html` |

## Generated-Output Observations

The dummy-media package-scoped target generated a substantial, but not feature-equivalent, `servo-script-bindings` output before the `mozjs_sys` failure.

| Output directory | Files | Bytes | Directory SHA-256 |
|---|---:|---:|---|
| `servo-script-bindings-e7e1371e7b6326b3` | `1424` | `26512010` | `0576F946AF4A2E26ABE1333B35EDB9842CB158885903C114DBD0642159B6DE63` |
| `glslopt-42be922f7e1180b7` | `136` | `19221348` | `4CA9B34C5FDB31D47741F6D48B17919E123A95D4837E8137169E59E7DC78E364` |
| `stylo-d222bd4454629256` | `3` | `5285796` | `1605814BDF161E52DA3C7E779055CEC7053E4F7FF6D0DD4CFFBC1FA2E9DB74E9` |
| `libz-sys-6ed10ecd54b32212` | `20` | `1462860` | `02D160E3392EA23921F2D487370BECB6477E5133BED7C1E92D8321788AB56BD1` |
| `gleam-d7a377f8199cf740` | `3` | `1364185` | `A4544105B6BC493CA5E46FA779848F2AE610E1EC820CF39EEA7AE155869E3BE9` |
| `web_atoms-bb84045715bd7c2a` | `2` | `653207` | `236927C2759AC5C74BB53523A5F4DD1FD47E3DE19C9423F86B054C491C421608` |
| `stylo_atoms-ec994d10fe67cec5` | `1` | `64994` | `CB27A8C4CD5EEED33399DABB51DD232D4493F44ADF847D28F17EFF8B3659F7C2` |
| `clang-sys-2faeddfae27c04d3` | `3` | `25120` | `D5DC2C12D3A13CCA3CFC1DE5219ED2587F298B3AFE25C108A6452127EE201563` |
| `stylo_static_prefs-fdd95d678c9fb0d5` | `1` | `15994` | `24E74F605315D06D00CAB239AF8FD1F46C4C06BB132A793C06F5F932F807CC45` |
| `khronos_api-2775874ed2f945f8` | `1` | `6360` | `A0568767563402475FEDBDF0DD95CB9EBD69AF0813E01C58CBB1F7F75BA5D29F` |

The `servo-script-bindings` output contained:

- `1423` `.rs` files and `1` `.json` file;
- immediate directories `Bindings`, `cache`, `ConcreteBindings`, and `WebGPUConcreteBindings`;
- large binding outputs including `CSSStyleDeclarationBinding.rs` at `4567498` bytes, `WebGL2RenderingContextBinding.rs` at `936730` bytes, `WindowBinding.rs` at `848159` bytes, `DocumentBinding.rs` at `778160` bytes, and `WebGLRenderingContextBinding.rs` at `546159` bytes.

The previous warm full dev build from the [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md) observed `servo-script-bindings-760806860634f27a\out` with `1631` files, `31834655` bytes, and directory digest `8154347D4FDD1025460FE34F8FF0F6DE122A99D3E98AB1855EACAB3044194407`.

The package-scoped dummy-media clean-target output is therefore smaller by `207` files and `5322645` bytes. It is not equivalent to the prior full `servoshell` development-build output.

## Interpretation

Observations:

- The default clean-target package build currently fails on the reference Windows host before Cargo generated-output inspection because the GStreamer runtime prerequisite is missing.
- The dummy-media package-scoped build bypasses the GStreamer blocker and emits substantial Servo Web IDL binding, Stylo, GLSL, atom, zlib, and Khronos output under an isolated target directory.
- The dummy-media package-scoped build still fails before a successful clean build because `mozjs_sys` enters a source-build path with JIT disabled and panics in its build script.
- The package-scoped dummy-media output differs in file count and size from the earlier warm full dev build output, so it cannot stand in for a feature-correct full generated-output regeneration proof.

Inference:

This probe advances `ADR9-EV-007` from a purely warm-target/no-op-rebuild observation to a partial clean-target generation observation. It also narrows the next failure surface: GStreamer must be installed or deliberately excluded through an owner-accepted profile, and the `mozjs_sys` feature/profile shape must match the selected `ADR-0009` baseline before clean-target output digests can be compared.

The evidence remains insufficient for generated-output determinism, source-to-output provenance, generated-code approval, or component approval.

## What This Does Not Prove

This probe does not prove:

- Servo can be built successfully from a clean target on this host;
- the dummy-media package-scoped generated outputs match a full `servoshell` development build;
- generated outputs are deterministic across clean targets;
- generated outputs are reproducible across hosts;
- generated outputs have accepted source-to-output license or provenance mapping;
- GStreamer, MozJS, SpiderMonkey, Stylo, WebRender, GLSL, Web IDL, Python, PLY, proc-macro, native, registry, or git build-script behavior is acceptable under Turing policy;
- any generated output can be imported, copied, rewritten, or used in Turing release code;
- Servo is compatible, secure, lower-memory, high-performance, Chrome-class, accessible, production-ready, or approved for a source-strategy decision.

## Next Evidence Required

Before `ADR9-EV-007` can close, produce:

1. an owner-selected source baseline, feature profile, target platform, and component boundary for the generated-output question;
2. a feature-correct full clean-target generated-output regeneration run for that baseline and profile, not only a package-scoped dummy-media probe;
3. retained success and failure logs with wrapper exit handling, `mach` exit status, stdout and stderr hashes, target-directory hashes, environment records, and source-tree cleanliness proof;
4. an independent-host or clean-VM comparison for the same commit, feature set, target, profile, environment policy, and generator inputs;
5. generator manifests for Web IDL, CSS properties, WebGPU, DevTools build IDs, C API headers, bindgen outputs, proc macros, shaders, native build glue, and SDK-driven outputs;
6. source-to-output license, notice, and provenance mapping for each generated-output family;
7. accepted policy for GStreamer presence or exclusion, MozJS/SpiderMonkey feature selection, JIT posture, `SOURCE_DATE_EPOCH`, Python or `uv` discovery, git-derived versions, `OUT_DIR` profile inference, nested Cargo, native copying, SDK discovery, and platform resource tools;
8. dynamic build-script and proc-macro tracing tied to the selected baseline and profile.

## Affected Records

This probe adds evidence for `PB-002` and `ADR9-EV-007`, but it does not change `PB-002` blocked status or select an `ADR-0009` option. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Documentation Readiness Evidence Matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md);
- [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md);
- [Testing, compatibility, fuzzing, and quality gates](../blueprint-v1/12-testing-compatibility.md);
- [Build, release, distribution, and operations](../blueprint-v1/13-build-release-operations.md).
