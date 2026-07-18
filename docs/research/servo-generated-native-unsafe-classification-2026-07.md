# Servo Generated, Native, Unsafe, and FFI Classification - July 2026

Status: dated external classification for `PB-002` and proposed `ADR-0009`; no source, unsafe, native, or generated-code approval
Owner: architecture, security, provenance, release operations, engine, and embedding owners
Classification date: 2026-07-17
Confidence: medium for heuristic counts and first-party build-script roles; low for safety conclusions until block-level review, generated-output regeneration, and owner audit run

## Question

What generated-code, build-script, proc-macro, native-link, FFI, and unsafe-code surface does the clean external Servo checkout expose before Turing decides whether Servo is only a research input, a selective component source, an upstream collaboration target, a derived engine, or a rejected release-code dependency?

This classification does not import Servo source, approve Servo-derived release code, approve any unsafe block, approve a native library, approve a generated-code pipeline, or move `PB-002` out of blocked status. It narrows the remaining evidence required by the [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md).

A follow-up [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md) records generated-output hashes, first-party build-script side effects, and one no-op rebuild stability check for the same checkout. The [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md) expands that review queue to registry, git, and path build scripts plus proc macros. A later [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md) records local Servo, Stylo, Cargo registry, and Windows bootstrap artifact identity evidence.

## Inputs

External checkout:

- workspace: `C:\ts\servo`;
- remote: `https://github.com/servo/servo.git`;
- commit: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- commit date: 2026-07-17T15:50:14Z;
- commit subject: `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)`;
- tracked files: `193033`;
- tracked-file status: clean.

Local evidence inputs outside Turing:

- `C:\ts\servo-metadata-default.json`;
- `C:\ts\servo-metadata-all-features.json`;
- clean Servo source tree under `C:\ts\servo`.

No Servo source file, generated binding, native artifact, Cargo metadata file, or build output was copied into this repository.

## Method

The pass combined source-shape queries, Cargo metadata parsing, native-source listing, and manual inspection of first-party Servo build scripts.

Commands and patterns included:

```powershell
git -C C:\ts\servo status --short --branch
git -C C:\ts\servo log -1 --format='%H|%cI|%s'
git -C C:\ts\servo ls-files
rg -n "\bunsafe\b" C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n "unsafe\s*\{" C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n "unsafe\s+fn\b" C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n "unsafe\s+impl\b" C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n "SAFETY:" C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg -n 'extern\s+"(C|system|Rust)"|#\[no_mangle\]|#\[export_name|#\[link\(' C:\ts\servo --glob '*.rs' --glob '!target/**' --glob '!.venv/**'
rg --files C:\ts\servo --glob '!target/**' --glob '!.venv/**' | rg '\.(c|cc|cpp|cxx|h|hpp|m|mm)$'
```

The Cargo metadata counts came from the default metadata profile recorded in the [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md). Node was used to parse the metadata because PowerShell `ConvertFrom-Json` rejects Servo metadata that contains case-distinct feature keys such as `USB` and `usb`.

Heuristic source counts are not a safety audit. They identify where review effort clusters. They do not prove whether a specific unsafe block is justified, documented, reachable, covered by tests, or usable in Turing.

## Summary

| Surface | Observation | Turing implication |
|---|---:|---|
| Unsafe mentions | `2280` matches across `241` Rust files | Requires block-level unsafe ledger before any candidate component can enter a release path |
| Unsafe blocks | `1629` matches across `207` Rust files | High review load, especially around script, WebGL, bindings, fonts, media, and C API paths |
| Unsafe functions | `224` matches across `66` Rust files | Public or cross-module invariants must be classified separately from local unsafe blocks |
| Unsafe impls | `104` matches across `45` Rust files | `Send`, `Sync`, tracing, GC, FFI, and platform invariants need owner review |
| `SAFETY:` comments | `157` matches | Count is lower than unsafe matches and cannot prove compliance because comments may cover multiple sites or be absent |
| FFI/export/link markers | `217` matches across `40` Rust files | ABI, symbol visibility, caller obligations, panic policy, lifetime, and ownership contracts remain unreviewed |
| First-party workspace build scripts | `9` files | First-party generated-code, platform, and C API test orchestration must be classified |
| Packages with build scripts | `157` default-metadata packages | Includes `9` path, `4` git, and `144` registry packages with build-time code execution |
| Proc-macro packages | `70` default-metadata packages | Includes `6` path, `2` git, and `62` registry packages with compile-time code generation |
| Native-link packages | `25` default-metadata packages | Includes `23` registry, `1` path, and `1` git package with Cargo `links` values |
| Generated/codegen markers | `1593` matches for `OUT_DIR`, `include!`, `include_str!`, `bindgen`, `codegen`, or `Codegen` | Generated output needs source hashes, generator versions, rerun policy, and regeneration diff checks |
| Web IDL/binding/codegen markers | `9727` matches under `components` and `python` | Script bindings dominate the generated-code and unsafe-review workload |

## Unsafe-code distribution

Top directories by unsafe mentions:

| Directory | Unsafe mentions | Unsafe blocks |
|---|---:|---:|
| `components/script` | 960 | 733 |
| `components/script_bindings` | 418 | 218 |
| `components/webgl` | 266 | 265 |
| `ffi/capi` | 172 | 71 |
| `components/fonts` | 128 | 116 |
| `ports/servoshell` | 69 | 31 |
| `components/media` | 48 | 42 |
| `components/shared` | 42 | 22 |
| `components/layout` | 39 | 37 |
| `components/webxr` | 28 | 28 |
| `components/background_hang_monitor` | 27 | 21 |
| `components/allocator` | 24 | 11 |
| `components/malloc_size_of` | 21 | 21 |

Top files by unsafe mentions:

| File | Unsafe mentions | Review pressure |
|---|---:|---|
| `components/webgl/webgl_thread.rs` | 263 | WebGL thread, GL/driver boundary, and command safety |
| `components/script/script_runtime.rs` | 92 | JavaScript runtime, SpiderMonkey, and script lifecycle |
| `components/script_bindings/trace.rs` | 75 | Tracing and GC-root invariants |
| `components/script/dom/window/windowproxy.rs` | 69 | Window proxy and cross-compartment behavior |
| `ffi/capi/options.rs` | 67 | C API options and caller-provided data |
| `components/script/dom/console.rs` | 46 | Script-visible console integration |
| `components/script_bindings/root.rs` | 44 | Rooting and lifetime ownership |
| `components/script/dom/bindings/structuredclone.rs` | 44 | Structured clone buffers and JS interop |
| `components/script/dom/bindings/buffer_source.rs` | 43 | JS buffer and Rust memory boundary |
| `components/script/script_module.rs` | 39 | Module loading/runtime interaction |
| `ffi/capi/preferences.rs` | 39 | C API preferences |
| `components/script_bindings/proxyhandler.rs` | 36 | JS proxy handler boundary |
| `components/script_bindings/utils.rs` | 34 | Shared JS binding utilities |
| `ffi/capi/webview.rs` | 33 | C API WebView lifecycle |
| `components/script/window_named_properties.rs` | 32 | JS named-property behavior |

Most unsafe usage clusters around JavaScript, DOM bindings, SpiderMonkey integration, WebGL, C API exposure, font shaping/platform font access, and media/platform backends. That is exactly the area where Turing's accepted policies require independent JavaScript-runtime ownership, hostile-input review, sandbox evidence, generated-code determinism, and explicit FFI contracts.

## FFI and native surface

The FFI/export/link marker distribution was:

| Directory | Marker count |
|---|---:|
| `components/script` | 75 |
| `ffi/capi` | 56 |
| `ports/servoshell` | 37 |
| `components/script_bindings` | 31 |
| `components/fonts` | 7 |
| `components/allocator` | 5 |
| `components/media` | 3 |
| `components/background_hang_monitor` | 1 |
| `components/profile` | 1 |
| `tests/capi` | 1 |

The highest-count FFI marker files were `ports/servoshell/egl/android/mod.rs`, `components/script/script_runtime.rs`, `ffi/capi/options.rs`, `components/script/dom/window/windowproxy.rs`, `components/script_bindings/utils.rs`, `ffi/capi/preferences.rs`, and `ffi/capi/webview.rs`.

Native source files outside `target/` and `.venv/` were limited in this query:

- `ports\servoshell\platform\macos\count_threads.c`;
- `tests\capi\c\test_integration.c`;
- `tests\capi\c\test_api.c`;
- `tests\wpt\tests\jpegxl\resources\make_animation_loop_jxl.c`;
- `tests\wpt\tests\tools\third_party\websockets\src\websockets\speedups.c`;
- `tests\wpt\tests\tools\third_party\packaging\tests\hello-world.c`.

This does not make Servo "mostly non-native" in distribution terms. The separate [Servo Supply-Chain Policy Scan - July 2026](servo-supply-chain-policy-scan-2026-07.md) recorded a large Windows bootstrap native dependency surface under `target\dependencies`, and Cargo metadata recorded `25` native-link packages.

Default metadata native-link packages by category:

| Category | Packages |
|---|---|
| JavaScript runtime | `mozjs_sys` |
| Style and script bindings | `stylo`, `servo-script-bindings` |
| Cryptography and TLS foundations | `aws-lc-rs`, `aws-lc-sys`, `ring` |
| Fonts, text, image, compression, and codec support | `freetype-sys`, `harfbuzz-sys`, `encoding_c`, `encoding_c_mem`, `libz-sys`, `wuff-capi`, `zstd-sys` |
| Storage | `libsqlite3-sys`, `sqlite-wasm-rs` |
| Platform and graphics/system bindings | `clang-sys`, `libudev-sys`, `objc-sys`, `openxr-sys`, `yeslogic-fontconfig-sys` |
| Allocator/runtime/build metadata | `tikv-jemalloc-sys`, `rayon-core`, `wasm-bindgen-shared`, `defmt`, `prettyplease` |

Any selective reuse proposal must state whether these native-link packages are in scope, transitively required, replaceable, or avoided.

## Build scripts, proc macros, and generated code

Default metadata contained `157` packages with build scripts:

- `144` registry packages;
- `4` git packages from Servo Stylo: `selectors`, `stylo`, `stylo_atoms`, and `stylo_static_prefs`;
- `9` Servo path packages: `servo-capi-tests`, `servo-devtools`, `servo-embedder-traits`, `servo-media-ohos`, `servo-script`, `servo-script-bindings`, `servo-script-webgpu`, `servoshell`, and `style_tests`.

Default metadata contained `70` proc-macro packages:

- `62` registry packages;
- `2` git packages from Servo Stylo: `stylo_derive` and `to_shmem_derive`;
- `6` Servo path packages: `servo-config-macro`, `servo-deny-public-fields`, `servo-dom-struct`, `servo-jstraceable-derive`, `servo-media-derive`, and `servo-tracing`.

First-party build-script roles:

| Build script | Observed role |
|---|---|
| `components/script_bindings/build.rs` | Runs `uv run --frozen python` when available, falls back to `python3` or `python`, runs `codegen/run.py`, consumes `css-properties.json` from Stylo output, watches Web IDL/codegen/parser inputs, and writes `InterfaceObjectMapPhf.rs` |
| `components/script/build.rs` | Copies generated binding include files and the `ConcreteBindings` directory from `servo-script-bindings` output into its own `OUT_DIR` |
| `components/script_webgpu/build.rs` | Copies generated WebGPU concrete bindings from `servo-script-bindings` output into its own `OUT_DIR` |
| `components/devtools/build.rs` | Writes `build_id.rs` using `SOURCE_DATE_EPOCH` when present or current time otherwise |
| `components/shared/embedder/build.rs` | Infers production or non-production cfg from the Cargo `OUT_DIR` profile path |
| `ports/servoshell/build.rs` | Emits production cfg, runs `git rev-parse --short HEAD`, compiles macOS `count_threads.c`, writes an Android libgcc shim, emits platform rpath/link/version-script arguments, and compiles Windows resources |
| `components/media/backends/ohos/build.rs` | Reads `OHOS_SDK_NATIVE` metadata and emits OpenHarmony SDK API cfg values |
| `tests/capi/build.rs` | Runs nested `cargo cinstall`, copies Windows DLLs, links the C FFI library, and compiles C API/integration tests |
| `tests/unit/style/build.rs` | Dummy script to expose `OUT_DIR` |

Generated-code review therefore needs more than checking committed Rust files. It must verify generator inputs, Python environment pinning, Stylo-derived outputs, Web IDL parser provenance, generated output hashes, Cargo rerun behavior, environment variables, nested Cargo invocation, and platform-specific side effects.

## Source-strategy implications

1. A Servo-derived path would inherit a large unsafe and generated-code review program concentrated in JavaScript, DOM bindings, WebGL, C API, fonts, media, and shell platform code.
2. A selective-component path must start with a precise boundary. Studying one component without SpiderMonkey, Stylo, generated script bindings, or native dependencies may be possible only for narrow areas; the dependency closure must prove it.
3. The C API and embedding surface are valuable evidence targets, but they are also ABI and lifetime contracts. They cannot be adopted by example without Turing-owned FFI policy, header/source provenance, panic/exception policy, threading policy, and C conformance tests.
4. The `SAFETY:` count is not enough to decide quality. Turing needs a block-level unsafe inventory that maps each unsafe block to preconditions, owner, tests, fuzz/sanitizer/Miri coverage, and release relevance.
5. The first-party build scripts show build-time code execution, generated Rust, platform SDK inspection, nested Cargo invocation, and time-based build ID behavior. Turing needs a deterministic-generation and hermetic-build decision before any reuse.
6. This classification makes `PB-002` more specific but still blocked. It replaces the vague "generated/unsafe/FFI review" gap with named follow-up reviews.

## What this does not prove

This classification does not prove:

- Servo's unsafe code is correct, incorrect, justified, or unjustified;
- generated bindings are deterministic, complete, or acceptable for Turing;
- native-link packages are safe, licensed, sandboxed, or redistributable under Turing policy;
- FFI contracts are stable or compatible with Turing's embedding design;
- any Servo component can be separated cleanly from SpiderMonkey, Stylo, WebRender, WebGPU, media, or platform dependencies;
- Servo is faster, lower memory, secure, accessible, compatible, Chrome-class, or production-ready;
- Turing should adopt Servo, Stylo, WebRender, SpiderMonkey, or any transitive dependency.

## Next evidence required

Before `ADR-0009` can advance, produce:

1. a block-level unsafe inventory for every candidate component, including `SAFETY:` coverage, owner, preconditions, invariants, tests, and release relevance;
2. clean generated-output regeneration and source/license provenance for Web IDL, CSS, WebGPU, PHF, DevTools build ID, headers, cbindgen outputs, and any generated SDKs;
3. accepted build-script and proc-macro side-effect policy plus dynamic tracing that covers filesystem, process, network, environment, time, nested Cargo, platform SDK, compiler, linker, native-copy, and package behavior;
4. proc-macro source/provenance and expansion-risk review for Servo path, Stylo git, and registry proc macros;
5. FFI ABI contracts for `ffi/capi`, script runtime, platform EGL/OpenHarmony paths, fonts, allocator, media, and C API tests;
6. native source, native-link, and downloaded native binary provenance with source-build or binary-package policy, license text, notices, advisories, hashes, and packaging implications;
7. owner-reviewed component-boundary analysis that proves which generated, unsafe, FFI, native, JavaScript, style, WebGL, media, and platform surfaces are in or out of each option, using the first-pass boundary report as input;
8. sanitizer, fuzz, Miri, C API, WebGL, DOM binding, media, font, and SpiderMonkey boundary evidence for any candidate reuse boundary.

## Affected records

This classification adds evidence for `PB-002` but does not change its blocked status. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Source Strategy Inventory - July 2026](servo-source-strategy-inventory-2026-07.md);
- [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Supply-Chain Policy Scan - July 2026](servo-supply-chain-policy-scan-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md);
- [Security, privacy, and sandbox](../blueprint-v1/08-security-and-sandbox.md);
- [Testing, compatibility, fuzzing, and quality gates](../blueprint-v1/12-testing-compatibility.md);
- [Build, release, distribution, and operations](../blueprint-v1/13-build-release-operations.md).
