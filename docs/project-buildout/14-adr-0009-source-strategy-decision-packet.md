# ADR-0009 Source Strategy Decision Packet

Status: evidence packet template and current metadata snapshot; no source-strategy decision
Owner: architecture, engine, security, provenance, release operations, embedding, and documentation owners
Last updated: 2026-07-19

## Purpose

`ADR-0009` decides how Turing relates to Servo and other browser-engine source while preserving honest independence claims. This packet defines the evidence required before that ADR can move from proposed to accepted, rejected, or superseded.

The short [ADR-0009 source-strategy closure preparation](../research/adr-0009-source-strategy-closure-preparation-2026-07.md) is the continuation route for the distributed evidence and owner questions. The [ADR-0009 Evidence Traceability Matrix](15-adr-0009-evidence-traceability-matrix.md) is the companion operating queue for the evidence below. The machine-readable [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json) registry, checked no-claim [`ADR-0009 decision-review template`](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json), and [`tools/validate_adr_0009_evidence.py`](../../tools/validate_adr_0009_evidence.py) validator are the executable status companions for `ADR9-EV-*` tracking. Neither replaces this packet or the machine readiness registry, and the template does not select a source strategy.

The fictitious [ADR-0009 source-strategy packet examples](../research/adr-0009-source-strategy-packet-examples-2026-07.md) demonstrates the required field-level handoff without supplying a decision or evidence closure. Any accepted ADR-0009 record must also satisfy the [PB-020 owner-decision closure board](23-owner-decision-closure-board.md) and the [build-readiness closure preparation route](../research/build-readiness-closure-and-owner-decision-preparation-2026-07.md); ADR acceptance alone does not grant broad implementation or release authority.

The packet applies to five options:

1. clean implementation informed by Servo;
2. selective Servo components;
3. upstream-first collaboration;
4. Servo-derived engine;
5. explicit charter change to a Servo browser.

No option is accepted by this document. No Servo-derived release code is authorized.

## Current source snapshot

Metadata gathered on 2026-07-17; official metadata refreshed on 2026-07-19:

| Source | Observation |
|---|---|
| Successful external build baseline | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z |
| Current fetched Servo `origin/main` | `622600e045c2e5ea688a9b19b8671b6f43112817`, committed 2026-07-17T17:01:59Z |
| Latest GitHub release from `gh release view` | `v0.3.0`, published 2026-06-25T15:09:42Z, target `release/v0.3` |
| `v0.3.0` release commit | `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`; lightweight tag, no tag-object signature, GitHub commit verification reported unsigned |
| `v0.3.0` vendored source archive | `servo-v0.3.0-src-vendored.tar.gz`, `364697035` bytes, SHA-256 `C75EFFBDC0AB6F86B318E28D139EB056268224E072A684492B49409C5221C871` |
| Independent non-shallow Git verification | fresh bare partial clone at `C:\ts\servo-independent-source-verify-20260717.git`; current `main`, build baseline, and `v0.3.0` object IDs matched upstream provenance records |
| Source-baseline equivalence comparison | `v0.3.0` vendored archive records `GIT_REVISION` matching the release commit but is not path-equivalent to the Git tree; crates.io `servo 0.4.0` is a `components/servo` package surface, not a whole-repository baseline |
| Latest `cargo search servo` result | `servo = "0.4.0"` |
| `cargo info servo` | version `0.4.0`, license `MPL-2.0`, `rust-version` `1.88.0` |
| crates.io `servo 0.4.0` checksum | `01a05ffce7829e67e41c5cb4e10849924cbd781d0ea0d6332d81afe8476d8a89`; local cached crate hash matched |
| `servo` default features | `baked-in-resources`, `clipboard`, `js_jit` |
| Notable optional features | `bluetooth`, `gamepad`, `gstreamer`, `media-gstreamer`, `native-bluetooth`, `vello`, `webgpu`, `webxr`, tracing and JS diagnostic features |

The 2026-07-19 refresh identifies a later upstream `main` commit, `736ad1bda08c1af419aadc903e82938f8610a65d` (author date `2026-07-19T19:09:15Z`), while the latest published release remains immutable `v0.3.0` and crates.io remains `servo 0.4.0`. The 2026-07-17 build and source-comparison rows remain historical evidence; no build or source-equivalence conclusion transfers to the newer `main` commit.

This metadata is insufficient for adoption. It only proves that the public project and crate are active and that version identifiers must be pinned precisely.

## First isolated Windows preflight

Observed on 2026-07-17 from an external research workspace, not from Turing source:

| Area | Observation | Consequence |
|---|---|---|
| Workspace | `C:\Users\bcw19\AppData\Local\Temp\turing-adr-0009-servo-evidence\servo` | Servo source remains outside this repository |
| Remote identity | `https://github.com/servo/servo.git` at `27f61918dff58b8479d7608ab831d42cd0d5a2dc` | Matches the observed public `main` commit |
| Git integrity | `git ls-files` returned `0`; `git status --porcelain` counted `193074` entries; `git ls-files --error-unmatch README.md` failed even though files exist on disk; `git fsck --connectivity-only` reported many dangling objects | The interrupted checkout is not valid build, provenance, dependency, compatibility, or performance evidence |
| File presence | the tree contained `mach`, `mach.ps1`, `mach.bat`, `README.md`, `.python-version`, and `rust-toolchain.toml` among about `207903` files | Files are useful for prerequisite reading only, not for source inventory trust |
| Servo Windows path | upstream README says Windows builds require `uv`, `rustup`, `winget`, Visual Studio components for Windows 10/11 SDK `>= 10.0.19041.0`, MSVC v143 VS 2022 C++ x64/x86 tools, C++ ATL, `.\mach bootstrap`, then `.\mach build` | The next build attempt must follow upstream tooling rather than direct Cargo commands |
| Servo tool pins | `.python-version` is `3.11`; `rust-toolchain.toml` pins Rust `1.95.0` with `clippy`, `llvm-tools`, `rustc-dev`, `rustfmt`, and `rust-src` | The experiment must isolate Servo's Python and Rust toolchains from Turing's M0 pins |
| Host tools | `git 2.52.0.windows.1`, `gh 2.93.0`, `cargo 1.97.1`, `rustc 1.97.1`, `python3 3.12.10`, `winget v1.29.250` were present | Host has general development tools but not Servo's complete documented path |
| Missing command | `uv` was not on `PATH` | `mach.ps1` cannot run as documented because it invokes `uv run --frozen` |
| MSVC shell state | Visual Studio Professional 2022 `17.14.36717.8` with the queried VC tools, ATL, and Windows 11 SDK component was installed, but `cl` and `link` were not on the normal PowerShell `PATH` | Build evidence needs Developer PowerShell, `vcvars`, or an equivalent scripted compiler environment |
| Host hardware and OS | Windows 11 Pro Insider Preview build `26220`, AMD Ryzen 9 5950X 16-core/32-thread CPU, about 64 GiB RAM, AMD Radeon RX 7900 XTX driver `32.0.22029.1019` | Adequate as a named reference host, but not yet a clean reproducible build environment |
| Direct `mach` probe | `python3 mach --help` is not a valid documented invocation and reported a Windows case-sensitive-path failure in this workspace | Do not treat direct Python invocation as Servo build evidence |

Result: the first preflight found useful metadata and host blockers, but produced no trustworthy Servo build, dependency graph, WPT result, benchmark, or adoption recommendation. `PB-002` remains blocked.

The next attempt needed to create or repair a clean external checkout, verify nonzero tracked files and clean status, install `uv`, run from a Visual Studio developer environment where `cl` and `link` resolve, then capture `.\mach bootstrap` and `.\mach build` logs.

## Second isolated Windows preflight

Observed on 2026-07-17 from a short external path, not from Turing source:

| Area | Observation | Consequence |
|---|---|---|
| Workspace | `C:\ts\servo` | The valid build evidence stays outside this repository and avoids the long-path failure seen in the temporary checkout |
| Remote identity | `https://github.com/servo/servo.git` at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` | Matches the later observed public `main` commit on 2026-07-17 |
| Git integrity | `git ls-files` counted `193033` tracked files; `git status --porcelain` counted `0` tracked-file changes after bootstrap and build | The checkout is valid source-identity evidence; generated virtualenv, Python cache, dependency, and target files are ignored |
| Host prerequisite repair | `uv 0.11.29` was installed through `winget`; `mach.ps1` used CPython `3.11.9`; Servo's Rust override used `1.95.0-x86_64-pc-windows-msvc` | The Servo experiment is isolated from Turing's M0 Rust and Python defaults |
| Bootstrap | `.\mach.ps1 bootstrap` completed with exit `0`; it installed or verified CMake, LLVM, Ninja, WiX, Rust `1.95.0`, `crown`, `moztools-4.0`, and GStreamer MSVC packages under `C:\ts\servo\target\dependencies` | The reference Windows host can complete Servo's documented bootstrap path |
| Compiler environment | Build ran from Visual Studio 2022 Developer Command Prompt `17.14.21`; `cl.exe` and `link.exe` resolved from MSVC `14.44.35207`; `lld-link.exe` resolved after adding `C:\Program Files\LLVM\bin` to `PATH` | A normal PowerShell environment is still insufficient; future scripts must enter the VS environment and expose LLVM tools |
| Build command | `.\mach.ps1 build --dev -j 8` completed with `BUILD_EXIT=0`; stdout reported `Succeeded in 0:09:21`; Cargo reported `Finished dev profile [unoptimized + debuginfo] target(s) in 9m 14s` | Servo can build on the reference host when checked out under a short path with the repaired prerequisite environment |
| Build artifact | `C:\ts\servo\target\debug\servoshell.exe`, size `298702336` bytes | Useful for later local corpus and embedding experiments, but not a Turing artifact |
| Build logs | `C:\ts\servo-bootstrap.log`, `C:\ts\servo-build-dev-vsdevcmd-llvm.out.log`, and `C:\ts\servo-build-dev-vsdevcmd-llvm.err.log` | Logs are local evidence for this dated preflight; they are not imported source |

Result: the second preflight proves that Servo can be fetched, bootstrapped, and built on the current Windows reference host when the checkout uses a short path and the Visual Studio plus LLVM environment is explicit. `PB-002` remains blocked because the build alone does not provide license/provenance review, dependency inventory, owner-reviewed component boundaries, local WPT or corpus results, performance measurement data, maintenance cost, or an accepted `ADR-0009`.

## Build reproduction evidence and gap report

The dated [Servo Build Reproduction Evidence and Gap Report - July 2026](../research/servo-independent-build-reproduction-2026-07.md) records the same-host build environment, log hashes, artifact hash, target/cache footprint, replay protocol draft, and failure notes for `ADR9-EV-002`.

Key observations:

- the external checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, with `193033` tracked files and no tracked-file changes;
- build logs outside Turing had stable SHA-256 hashes, and `servoshell.exe` was `298702336` bytes with SHA-256 `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B`;
- the reference host used CPython `3.11.9`, Servo Rust `1.95.0-x86_64-pc-windows-msvc`, Visual Studio Professional 2022 Developer Command Prompt `17.14.21`, MSVC `14.44.35207`, compiler/linker version `19.44.35221` / `14.44.35221.0`, and `LLD 22.1.8`;
- `C:\ts\servo\target` contained `38370` files and `35941861226` bytes, so the existing warm target must not be treated as clean-target reproduction;
- normal PowerShell still does not expose `cl`, `link`, or `lld-link`, and the replay must explicitly enter the selected Visual Studio developer environment and add the LLVM linker path.
- the replay-protocol draft now names the required external paths, source commit, Visual Studio script, LLVM path, target/cache modes, path-deletion guard, host/tool capture, source identity checks, bootstrap/build log capture, and success/failure evidence bundle.

Result: `ADR9-EV-002` now has a sharper same-host build handoff and a replay-protocol draft, but it remains partial. Turing still needs owner acceptance of the protocol or a derived script, clean-target replay on an independent Windows host or clean VM, target/cache isolation evidence, success and failure log bundle, and reruns if `ADR-0009` selects a source baseline other than the built commit.

## Dependency and provenance metadata pass

The dated [Servo Dependency and Provenance Inventory — July 2026](../research/servo-dependency-provenance-inventory-2026-07.md) adds the first Cargo metadata pass for the clean external checkout at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`.

Key observations:

- default metadata contained `1069` packages: `75` Servo path packages, `983` registry packages, and `11` git packages;
- all-features metadata contained `1120` packages: `75` Servo path packages, `1034` registry packages, and `11` git packages;
- default metadata exposed `157` packages with build scripts, `70` proc-macro packages, and `25` native-link packages;
- the git packages all came from `https://github.com/servo/stylo` at revision `d3de91cbac7bba38e159239b3c0a360783fce2ee`;
- high-impact clusters include MozJS/SpiderMonkey and default `js_jit`, Stylo, WebRender/WebGPU/ANGLE, GStreamer/media, rustls/aws-lc/ring, SQLite, platform UI/input/accessibility crates, DevTools, and WebDriver.

Result: dependency/provenance is now partially inventoried, but not reviewed or accepted. `PB-002` remains blocked until license text and notices, advisory status, owner-selected source-baseline policy, source-content/release-archive/package equivalence, block-level unsafe review, feature-correct full clean generated-output regeneration beyond the package-scoped dummy-media probe, generated-output source/license provenance, accepted build-script and proc-macro side-effect policy plus dynamic tracing, native side-effect and provenance review, FFI ABI contracts, owner-reviewed component boundaries, owner-reviewed JavaScript-runtime conflict decision, local compatibility evidence, runner-generated performance evidence, maintenance model, and `ADR-0009` owner review are complete.

## Supply-chain policy scan

The dated [Servo Supply-Chain Policy Scan — July 2026](../research/servo-supply-chain-policy-scan-2026-07.md) records the first `cargo-deny` and native-bootstrap evidence for the same external checkout.

Key observations:

- `cargo deny check all --show-stats` exited `0` for both default and all-features metadata when using Servo's own `deny.toml`;
- default metadata results were `0` advisory errors, `0` license errors, `0` source errors, and `0` ban errors, with `11` warnings for unnecessary duplicate-skip entries;
- all-features metadata results were `0` errors and `0` warnings across advisories, bans, licenses, and sources;
- Servo's policy explicitly ignores `12` RustSec advisories, including unmaintained crates, `rsa` Marvin Attack, `quick-xml` denial-of-service vulnerabilities, and font/text-stack advisories;
- `Cargo.lock` contained `1034` registry entries with checksums, `11` Stylo git entries without Cargo checksums, and `75` Servo path entries;
- Servo bootstrap unpacked `19456` files under `target\dependencies`, including `537` DLLs, `443` EXEs, `309` PDBs, and `2` extracted-tree GStreamer MSI artifacts.

Result: Servo passes its own policy scan for the inspected metadata profiles, but Turing still has no legal approval, advisory acceptance, native-binary provenance review, source-build policy, block-level unsafe review, feature-correct full clean generated-output regeneration beyond the package-scoped dummy-media probe, generated-output source/license provenance, FFI ABI contract review, or accepted source-strategy decision.

## License, advisory, and SBOM decision prep

The dated [Servo License Advisory and SBOM Decision Prep - July 2026](../research/servo-license-advisory-decision-prep-2026-07.md) converts the Cargo metadata and Servo-policy scan into Turing-specific decision queues for `ADR9-EV-003` and `ADR9-EV-004`.

Key observations:

- the external checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, but the shallow checkout was `2` commits behind `origin/main`, so this is a dated build-baseline snapshot;
- default metadata contained `1069` packages, `48` unique license expressions, `0` packages missing both `license` and `license_file`, and `58` duplicate package names;
- all-features metadata contained `1120` packages, `50` unique license expressions, `0` packages missing both `license` and `license_file`, and `69` duplicate package names;
- top all-features license expressions included `MIT OR Apache-2.0`, `MIT`, `Apache-2.0 OR MIT`, `MPL-2.0`, `MIT/Apache-2.0`, `Unicode-3.0`, `Apache-2.0`, `BSD-3-Clause`, `Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT`, and `Zlib OR Apache-2.0 OR MIT`;
- Servo's `deny.toml` ignores `12` RustSec advisories and has a per-crate `NCSA` exception for `libfuzzer-sys`;
- the observed Windows GStreamer license directory contained `69` package directories, `155` files, and `1141093` bytes of license material;
- no complete Turing SBOM was generated, and `cargo cyclonedx`, `cargo about`, `cargo license`, and `cargo auditable` were not accepted as Turing tooling in this pass.

Result: `ADR9-EV-003` remains partial and `ADR9-EV-004` moves from missing to partial. Turing now has a concrete license/advisory/SBOM decision queue, but still needs owner-selected SBOM tooling and profile, generated SBOM, accepted license list, legal approval, third-party notices, source-offer plan, codec and patent review, native notice review, duplicate-version decisions, advisory exception records, and accepted owner review.

## Generated, native, unsafe, and FFI classification

The dated [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](../research/servo-generated-native-unsafe-classification-2026-07.md) records the first-pass generated-code, build-script, proc-macro, native-link, FFI, and unsafe-code surface for the same clean external checkout.

Key observations:

- source-shape queries found `2280` unsafe mentions across `241` Rust files, including `1629` unsafe-block matches, `224` unsafe functions, `104` unsafe impls, and `157` `SAFETY:` comments;
- unsafe usage clusters in `components/script`, `components/script_bindings`, `components/webgl`, `ffi/capi`, `components/fonts`, `ports/servoshell`, `components/media`, and `components/layout`;
- FFI/export/link markers appeared `217` times across `40` Rust files, led by script runtime/bindings, `ffi/capi`, servoshell platform code, fonts, allocator, and media;
- default Cargo metadata contained `157` build-script packages, `70` proc-macro packages, and `25` native-link packages;
- first-party Servo build scripts generate or copy Web IDL/script/WebGPU bindings, emit DevTools build IDs, infer production cfgs, inspect OpenHarmony SDK metadata, compile platform C/resource files, and run nested `cargo cinstall` for C API tests.

Result: the vague generated/unsafe/FFI review gap is now split into concrete remaining work. Turing still needs block-level unsafe inventory, feature-correct full clean generated-output regeneration beyond the package-scoped dummy-media probe, generated-output source/license provenance, accepted build-script and proc-macro side-effect policy plus dynamic tracing, proc-macro expansion/provenance review, FFI ABI contracts, native source/binary provenance, owner-reviewed component boundaries, and sanitizer/fuzz/Miri/C API evidence before any Servo component can affect release code.

## Unsafe and FFI contract triage

The dated [Servo Unsafe and FFI Contract Review - July 2026](../research/servo-unsafe-ffi-contract-review-2026-07.md) turns `ADR9-EV-009` and `ADR9-EV-010` from broad gaps into a boundary-specific review plan for the same clean external checkout.

Key observations:

- unsafe-block pressure remains concentrated in WebGL/GL integration, JavaScript runtime and bindings, DOM/window proxies, structured clone/buffer sources, C API options, fonts, media, layout, and servoshell platform code;
- C API review pressure includes `52` `pub extern "C"` exports across builder, options, preferences, rendering context, servo, and webview modules;
- observed C API patterns include null-pointer assertions, `CStr::from_ptr`, `Box::from_raw` and `Box::into_raw`, callbacks/delegates, thread-affinity comments, and security-sensitive option toggles;
- JavaScript rooting/tracing and WebGL/driver boundaries need focused review before any selective component proposal can rely on them.

Result: `ADR9-EV-009` and `ADR9-EV-010` are now partial with a concrete triage plan, but they are not complete. Turing still needs an owner-selected candidate boundary, block-level unsafe ledger with invariants and tests, accepted panic/allocator/thread/string/pointer/callback ABI policy, C conformance tests, header/source provenance, fuzz/sanitizer/Miri evidence where applicable, and owner review.

## Build-script and generated-output audit

The dated [Servo Build-Script and Generated-Output Audit - July 2026](../research/servo-build-script-generated-output-audit-2026-07.md) records the first generated-output hash inventory, first-party build-script side-effect audit, and one no-op incremental rebuild stability check for the same external checkout.

Key observations:

- the Windows debug build contained `103` Cargo `out` directories, `3955` files, and `1106039671` bytes of generated or build-script output under `target\debug\build`;
- the largest output directories came from `mozjs_sys`, `mozangle`, `harfbuzz-sys`, `aws-lc-sys`, `fontsan`, `servo-script-bindings`, `glslopt`, `zstd-sys`, `libsqlite3-sys`, and `stylo`;
- first-party Servo outputs included `1631` files and `31834655` bytes from `servo-script-bindings`, `546` files from `servo-script`, `539` files from `servo-script-webgpu`, a generated DevTools build ID, Windows servoshell resource output, and Stylo CSS property output;
- generator inputs included `556` Web IDL files, `8` codegen files, `85` WebIDL parser files, `58` PLY files, `uv.lock`, `.python-version`, `rust-toolchain.toml`, and Stylo `css-properties.json`;
- one incremental no-op rebuild exited `0`, reported `Succeeded in 0:00:03`, and kept the inspected first-party generated-output directory digests unchanged;
- first-party build scripts still depend on Python or `uv`, `SOURCE_DATE_EPOCH`, `OUT_DIR`, git state, target cfg, platform SDK/resource tools, `OHOS_SDK_NATIVE`, nested Cargo, and DLL/resource copying behavior.

Result: generated-output and first-party build-script evidence is sharper, but still not sufficient for adoption. Turing still needs feature-correct full clean-target generation beyond the partial package-scoped probe, independent-host comparison, full build-script and proc-macro side-effect review, owner-reviewed source-to-output license/provenance approval, native artifact packaging review, and a policy for environment-sensitive build inputs.

## Clean generated-output reproduction probe

The dated [Servo Clean Generated-Output Reproduction Probe - July 2026](../research/servo-clean-generated-output-reproduction-2026-07.md) records the first isolated-target attempt to regenerate selected Servo generated outputs without relying on the previously warm Servo target.

Key observations:

- the default package-scoped clean-target attempt failed before Cargo generated-output inspection because the reference Windows host lacked GStreamer libraries;
- the `--media-stack dummy` package-scoped attempt bypassed that blocker, emitted `48` Cargo `out` directories and `46` build-script output logs, then failed in `mozjs_sys` while trying a JIT-disabled source-build path;
- the dummy-media target produced a substantial `servo-script-bindings` output of `1424` files, `26512010` bytes, and digest `0576F946AF4A2E26ABE1333B35EDB9842CB158885903C114DBD0642159B6DE63`;
- the earlier warm full dev build observed `1631` `servo-script-bindings` files and `31834655` bytes, so the package-scoped dummy-media output is not equivalent to the full `servoshell` development-build output;
- the Servo checkout still had `0` tracked-file changes after the probe.

Result: `ADR9-EV-007` remains partial. The probe provides clean-target failure and partial generated-output evidence, but Turing still needs an owner-selected baseline and feature profile, owner-reviewed generated-output generator manifest, feature-correct full clean-target regeneration, independent-host comparison, owner-reviewed source-to-output license/provenance approval, accepted media and MozJS feature policy, and dynamic build-script/proc-macro tracing before generated outputs can be trusted.

## Generated-output generator manifest

The dated [Servo Generated-Output Generator Manifest - July 2026](../research/servo-generated-output-generator-manifest-2026-07.md) maps first-party Servo and pinned Stylo generator families, source inputs, generated outputs, retained output-family observations, feature gates, and environment sensitivity for `ADR9-EV-007`.

Key observations:

- the manifest ties Servo evidence to checkout commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, and Stylo commit `d3de91cbac7bba38e159239b3c0a360783fce2ee`;
- first-party generated-output families now include Web IDL/script bindings, script copy outputs, WebGPU binding copy outputs, Stylo CSS properties, selectors PHF attributes, Stylo atoms, Stylo static prefs, DevTools build ID, servoshell resource/identity outputs, shared embedder cfg, OpenHarmony media SDK cfg, C API test install/copy behavior, and a unit-style dummy script;
- the WebIDL family has `556` `.webidl` files and `skip-unless` gates for Bluetooth, Gamepad, TestBinding, WebGPU, and WebXR features;
- retained warm and package-scoped clean outputs match for Stylo, selectors, Stylo atoms, and Stylo static prefs under the manifest digest method, but `servo-script-bindings` differs materially between the warm full target and the package-scoped dummy-media clean target;
- DevTools output is time-sensitive without `SOURCE_DATE_EPOCH`, and servoshell output is target/profile/Git-sensitive.

Result: `ADR9-EV-007` now has a first-pass generator manifest, but it is not decision-grade. Turing still needs owner review of the manifest for a selected source baseline, feature profile, target profile, output-family set, generator-version set, and environment policy; feature-correct full clean-target regeneration; independent-host comparison; owner-reviewed source-to-output license/provenance approval; dynamic tracing; and owner approval before generated outputs can be trusted.

## Generated-output source-to-output provenance map

The dated [Servo Generated-Output Source-To-Output Provenance Map - July 2026](../research/servo-generated-output-source-provenance-map-2026-07.md) maps observed source and license families into the first-party Servo and pinned Stylo generated-output families identified by the generator manifest.

Key observations:

- Servo root license text is MPL-2.0, and `LICENSE_WHATWG_SPECS` applies BSD 3-Clause terms to WHATWG specification portions incorporated into source;
- `servo-script-bindings` declares `MPL-2.0 AND BSD-3-Clause`, with the BSD-3-Clause signal tied to PLY build-time use;
- all `556` inspected WebIDL files matched MPL license text, and `9` also matched copyright-waiver standard-text markers;
- the WebIDL generator path includes MPL Servo generator code, MPL WebIDL parser code, BSD-3-Clause PLY signals, WebIDL/spec inputs, and Stylo CSS property output;
- the Stylo CSS property generator path includes MPL Stylo templates/data plus MIT Mako, MIT TOML, and BSD-style MarkupSafe license signals;
- DevTools build ID, servoshell resources, OpenHarmony SDK cfg, shared embedder cfg, and C API test install/copy families remain environment, target, native-toolchain, or test-scope sensitive.

Result: `ADR9-EV-007` now has a first-pass source-to-output provenance map, but it is not legal approval, notice approval, generated-code approval, or release authorization. Turing still needs owner-reviewed source-to-output license/provenance approval for the selected source baseline, feature profile, target profile, output-family set, generator-version set, and component boundary, plus feature-correct full clean-target regeneration, independent-host comparison, dynamic tracing, and owner approval before generated outputs can be trusted.

## Build-script and proc-macro side-effect audit

The dated [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](../research/servo-build-script-proc-macro-side-effect-audit-2026-07.md) turns the generated/native/unsafe/FFI classification and build-script audit into the `ADR9-EV-008` side-effect queue.

Key observations:

- default metadata exposed `157` build-script packages and `70` proc-macro packages; all-features metadata exposed `167` build-script packages and `71` proc-macro packages;
- registry packages dominated the default build-script surface with `144` build-script packages and `62` proc-macro packages;
- all-features added `10` build-script packages, `prost-derive`, and `libdbus-sys` as a native-link package;
- static marker triage found `3492` environment/cfg markers, `816` compiler/linker markers, `631` native-copy/package markers, `410` filesystem/write markers, `267` URL/download/fetch markers, `116` process markers, and `18` time/git markers in build scripts;
- proc-macro source roots covered `744` Rust files and `5331698` bytes, with registry macros dominating marker volume;
- high-pressure build scripts included `aws-lc-sys`, `mozjs_sys`, `ring`, `portable-atomic`, `libsqlite3-sys`, `tikv-jemalloc-sys`, `mozangle`, `rav1e`, `av-scenechange`, `servo-capi-tests`, `webrender`, and `servo-script-bindings`.

Result: `ADR9-EV-008` remains partial. Turing has a concrete side-effect review queue, but still needs selected baseline/profile/component boundary, accepted side-effect policy, dynamic tracing, proc-macro expansion review, generated-output provenance, feature-correct full clean-target regeneration beyond the package-scoped dummy-media probe, independent replay, and owner approval.

## Source and archive provenance audit

The dated [Servo Source and Archive Provenance Audit - July 2026](../research/servo-source-archive-provenance-audit-2026-07.md) records local source/archive, Cargo cache, Stylo git-source, and Windows bootstrap artifact identity evidence for the same external checkout.

Key observations:

- the clean Servo checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, with `193033` tracked files and `git fsck --connectivity-only` exit `0`;
- the Servo tracked-file manifest hash was `54E852C7337C1913B72A057D5E1E354B0201D8945D14B19F36471B8E9EF72DE7`;
- the local Servo `git archive` tar was `931993600` bytes with SHA-256 `205530091A7E36977BBF7417F5D48D91D122137B9450985897E54C9A5D00841D`;
- the Stylo git checkout was pinned to `d3de91cbac7bba38e159239b3c0a360783fce2ee`, tree `d4bd206aeb9bf5d5dfd333cf1cce7a879dbc07e9`, with a local archive SHA-256 of `323900D70CCF149C61F187A10F47D899A977772E3CE5D7BA82FD83B0DA5D1375`;
- default and all-features registry `.crate` archives were all present, matched Servo `Cargo.lock` checksums, and had unpacked source directories;
- the Windows bootstrap dependency tree contained `19456` files and `1582709414` bytes, including `537` DLLs, `443` EXEs, `309` PDBs, and `2` extracted-tree GStreamer MSI artifacts.

Result: local source/archive and registry-cache evidence is now captured, but this is still not source approval. Turing still needs owner-selected source-baseline policy, independent-source verification, license/notice/source-offer decisions, native source-build or binary-package exceptions, feature-correct full clean generated-output regeneration beyond the package-scoped dummy-media probe, build-script/proc-macro/native review, owner-reviewed component boundaries, owner-reviewed JavaScript-runtime conflict decision, local compatibility/performance evidence, maintenance review, and an accepted `ADR-0009`.

## Upstream source provenance report

The dated [Servo Upstream Source Provenance - July 2026](../research/servo-upstream-source-provenance-2026-07.md) compares the successful external build baseline, current fetched upstream `origin/main`, latest GitHub release, release source archive, and latest crates.io package.

Key observations:

- the successful external build baseline remains `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- after refreshing tags and `origin` on 2026-07-17, fetched `origin/main` was `622600e045c2e5ea688a9b19b8671b6f43112817`, two commits ahead of the build baseline; the 2026-07-19 official refresh now identifies `736ad1bda08c1af419aadc903e82938f8610a65d` as the later `main` observation;
- the external build checkout is a shallow partial clone, so it is not full-history provenance evidence;
- GitHub commit verification reported the build baseline and current `origin/main` commits as valid, but the `v0.3.0` release commit as unsigned;
- `v0.3.0` and `release/v0.3` point to `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`;
- `v0.3.0` is a lightweight commit tag, so `git tag -v v0.3.0` cannot verify a tag object;
- the downloaded `servo-v0.3.0-src-vendored.tar.gz` matched GitHub's SHA-256 digest and was readable;
- the local cached crates.io `servo-0.4.0.crate` matched the crates.io checksum.

Result: the old upstream release/archive comparison gap is now evidence-backed, but source identity remains unresolved. `ADR-0009` still needs an owner-selected baseline model, signed-tag or equivalent provenance policy, source-content/release-archive/package equivalence policy, and a rerun plan if the selected baseline differs from the current build baseline.

## Independent source verification

The dated [Servo Independent Source Verification - July 2026](../research/servo-independent-source-verification-2026-07.md) records a separate bare, non-shallow, `blob:none` partial clone from `https://github.com/servo/servo.git`.

Key observations:

- the independent clone is bare, non-shallow, and separate from the successful build checkout;
- current `main` resolved to `622600e045c2e5ea688a9b19b8671b6f43112817`, with tree `9d71530fe4d36dd9c94a2a411d75f219fde0dfc9`;
- the successful external build baseline resolved to `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- the non-shallow ancestry check confirmed the build baseline was exactly two commits behind the historical 2026-07-17 `main` observation; it says nothing about the later 2026-07-19 `main` commit;
- `v0.3.0` and `release/v0.3` resolved to `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, with tree `c41b1defccd9ed47a5ac2a8ad40929bc34de80a0`;
- the non-shallow release comparison returned `1 838` for `v0.3.0...main`, showing the release branch is not a simple ancestor of current `main`;
- local signature checks confirmed `v0.3.0` is not a verifiable tag object and that local Git does not have a configured trust root for the GitHub-merged commit signatures.

Result: independent Git object and ancestry verification is now captured for `ADR9-EV-001`. Source identity still remains unresolved because this does not select a baseline, verify every blob, define release-archive or crates.io package equivalence, or accept a signed-tag-equivalent provenance policy.

## Source-baseline equivalence policy prep

The dated [Servo Source Baseline Equivalence Policy Prep - July 2026](../research/servo-source-baseline-equivalence-policy-2026-07.md) compares the `v0.3.0` Git tree, vendored release source archive, and crates.io `servo 0.4.0` package surface.

Key observations:

- the vendored release archive contains `GIT_REVISION` with `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, matching `v0.3.0`;
- the `v0.3.0` Git tree has `191174` files;
- the vendored release archive has `252589` files and `2089732373` file bytes;
- `191078` vendored archive files match release Git paths;
- `61511` vendored archive files are not in the release Git tree, led by `61510` files under `vendor/` plus `GIT_REVISION`;
- `96` release Git files are missing from the vendored archive, mainly under `etc/`;
- crates.io `servo 0.4.0` records VCS commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873` and `path_in_vcs` `components/servo`;
- the crate contains all `30` files from `components/servo` at that commit plus four Cargo package metadata files.

Result: source-content equivalence is now better characterized, but not approved. `ADR-0009` still needs an owner-selected baseline, accepted provenance/equivalence policy, full blob and legal/source-offer review for the selected surface, and a rerun plan if the selected baseline differs from the built commit.

## Native bootstrap provenance and source-build audit

The dated [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](../research/servo-native-bootstrap-provenance-audit-2026-07.md) records Windows bootstrap download behavior, upstream `servo-build-deps` release metadata, original asset hashes, extracted-tree artifact hashes, signature posture, plugin-list inputs, and debug-output packaging footprint for the same external checkout.

Key observations:

- Servo Windows bootstrap downloads `moztools-4.0.zip` and GStreamer MSVC `1.22.8` runtime/development MSIs from `servo/servo-build-deps` release tag `msvc-deps`;
- GitHub release metadata for the relevant assets exposed no asset digest values on 2026-07-17;
- the original upstream GStreamer runtime MSI was `127258624` bytes with SHA-256 `37F9973FE5C720CE1F1602E7E599336384B9FF3E4878817987DD6B77265F17BB` and Authenticode status `NotSigned`;
- the original upstream GStreamer development MSI was `225861632` bytes with SHA-256 `2D0CF6E89CF88D94E670CD81087C002408161D1C8843C00D3F27D33CE254C523` and Authenticode status `NotSigned`;
- the original upstream `moztools-4.0.zip` was `143306382` bytes with SHA-256 `CCEB354767EF3DAD8813E63CB95ED081814225BF5FA15BFA083AA8B31A339153`;
- the two small GStreamer `.msi` files under `target\dependencies` are extracted-tree artifacts, not the original upstream downloads;
- Authenticode checks over extracted `.dll`, `.exe`, and `.msi` files found `981` unsigned files and one valid signed `vswhere.exe`;
- the external debug output under `target\debug` contained `617` `.dll`, `.exe`, and `.pdb` files totaling `5223312616` bytes.

Result: native bootstrap identity evidence is now sharper, but this is not package approval. Turing still needs source-build recipes or explicit binary-package exceptions, native legal/advisory/notice review, package minimization, final package manifests, deterministic download verification, independent-host reproduction, and release SBOM policy.

## Native package decision prep

The dated [Servo Native Package Decision Prep - July 2026](../research/servo-native-package-decision-prep-2026-07.md) turns the native bootstrap audit into package-family decisions for `ADR9-EV-005` and `ADR9-EV-006`.

Key observations:

- the inspected Windows bootstrap path downloads `moztools-4.0.zip` and GStreamer MSVC `1.22.8` runtime/development MSIs from the `servo-build-deps` `msvc-deps` release;
- GitHub release metadata for the three relevant assets still exposed `digest: null`;
- local copies had SHA-256 hashes for `moztools-4.0.zip`, `gstreamer-1.0-msvc-x86_64-1.22.8.msi`, and `gstreamer-1.0-devel-msvc-x86_64-1.22.8.msi`, but the two GStreamer MSIs were not Authenticode-signed;
- the extracted dependency tree had `4630` files under `gstreamer`, `14824` files under `moztools`, and two smaller extracted-tree GStreamer MSI artifacts;
- extracted `.dll`, `.exe`, and `.msi` signature checks found `981` unsigned files and one valid signed `vswhere.exe`;
- the GStreamer packaging sources define `86` Windows GStreamer copy candidates before transitive dependency and package availability checks;
- the debug build output contained `146` DLLs, `208` EXEs, and `263` PDBs, which is package-manifest evidence, not a release footprint.

Result: `ADR9-EV-005` and `ADR9-EV-006` remain partial. Turing now has a package-family decision matrix and deterministic-download policy proposal, but still needs source-build recipes or binary-package exception records, accepted hash/signature/mirror policy, native legal/advisory/notice review, package minimization, final manifests, independent replay, and owner approval.

## Component boundary and JavaScript conflict analysis

The dated [Servo Component Boundary and JavaScript Conflict Analysis - July 2026](../research/servo-component-boundary-analysis-2026-07.md) records first-pass package-closure, direct-dependency, feature-profile, marker-count, replacement-plan, and runtime-conflict evidence for `ADR9-EV-011` and `ADR9-EV-012`.

Key observations:

- the clean external Servo checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- dev-excluded metadata closures were still large for obvious roots: `servoshell` reached `1004` packages, `servo` reached `842`, `servo-layout` reached `766`, `servo-script` reached `764`, `servo-script-bindings` reached `499`, `servo-net` reached `579`, `servo-storage` reached `503`, and `servo-media-gstreamer` reached `422`;
- the `servo` default feature set includes `js_jit`, and `--no-default-features` still reached `mozjs`, `mozjs_sys`, Stylo, and WebRender;
- `servo-layout` directly depends on `servo-script`, `servo-script-traits`, Stylo packages, and `webrender_api`;
- `servo-script` directly depends on `mozjs`, `servo-script-bindings`, Stylo packages, `servo-layout-api`, `servo-net-traits`, and `webrender_api`;
- heuristic marker counts concentrated MozJS/SpiderMonkey, Web IDL, unsafe, and FFI review pressure in `components/script`, `components/script_bindings`, and `ffi/capi`.

Result: `ADR9-EV-011` and `ADR9-EV-012` move from missing to partial. This is not component approval. Turing still needs an owner-selected source baseline and feature profile, per-option dependency closures with target and dependency-kind separation, in/out component lists, owner-reviewed replacement contracts, an accepted JavaScript-runtime conflict decision, and explicit handling of whether each option preserves or supersedes `ADR-0004`.

## Local compatibility corpus and WPT/Test262 evidence

The dated [Servo Local Compatibility Corpus and WPT/Test262 Evidence - July 2026](../research/servo-local-compatibility-corpus-2026-07.md) records first-pass WPT tree, include-rule, metadata-expectation, Test262-vendoring, focus-area, runner-entrypoint, and local-corpus planning evidence for `ADR9-EV-013`.

Key observations:

- the external checkout's upstream WPT tree contained `160978` files under `tests/wpt/tests`, while Servo's upstream WPT metadata root contained `18777` `.ini` expectation files and a `39462596` byte `MANIFEST.json`;
- `tests/wpt/include.ini` begins with `skip: true`, then records `116` `skip: false` entries and `74` `skip: true` entries, so WPT presence is not a compatibility denominator by itself;
- expectation metadata contained large expected-result surfaces, including `154382` expected markers and `145965` fail markers in the upstream metadata root, plus WebGL and WebGPU metadata with their own expected-failure counts;
- focused WPT source-tree file counts include `54344` CSS files, `14154` HTML files, `984` Fetch files, `943` WebDriver files, `830` Wasm files, `797` DOM files, `794` service-worker files, `606` worker files, and smaller JS/Web IDL/accessibility/WebGL/WebGPU subsets;
- Test262 appears through WPT infrastructure and vendored data at revision `b66872a92487694396fb082343e08dd7cca5ddf4`, with `53441` `.js` files under `third_party/test262/test`, not as an accepted Turing-owned Test262 runtime harness.
- the checked [local compatibility corpus manifest](../blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json) now fixes eight no-claim local case categories, required assertion groups, artifacts, fixture paths, fixture hashes, `turing.invalid` origins, WPT focus areas, Test262 attribution language, and failure denominators before any browser run exists.
- the checked HTTP route self-test now serves every generated fixture with Host-header origin mapping, verifies response bytes and hashes, and records no HTTPS, no DNS modification, no browser launch, no WPT result, no Test262 result, and no compatibility result.
- the checked [HTTPS host-alias harness plan](../blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json) now fixes the future local certificate, SNI/SAN, isolated trust-store, host-to-loopback alias, cleanup, browser-visible-origin, per-origin route, raw-log, and denominator record requirements without executing HTTPS or a browser.

Result: `ADR9-EV-013` is partial. This is not a compatibility result. Turing still needs HTTPS harness execution and host-alias browser runs for the checked fixtures, browser-run evidence against the external Servo build, focused WPT runs for the selected `ADR-0009` option, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan for `ADR-0004`.

## Fixed-hardware performance and memory baseline prep

The dated [Servo Performance Baseline Preparation - July 2026](../research/servo-performance-baseline-2026-07.md) records first-pass reference-host, artifact, Servo performance command-surface, fixture-inventory, and run-record evidence for `ADR9-EV-014`.

Key observations:

- the external checkout remained clean at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- the named Windows reference host is `BYRON-HOME`, with Windows 11 Pro Insider Preview build `26220`, AMD Ryzen 9 5950X 16-core/32-thread CPU, about 64 GiB RAM, and AMD Radeon RX 7900 XTX driver `32.0.22029.1019`;
- the current built Servo artifact is the debug `C:\ts\servo\target\debug\servoshell.exe`, `298702336` bytes, SHA-256 `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B`;
- Servo exposes page-load, Dromaeo, Speedometer, jQuery, and macOS PowerMetrics-oriented performance surfaces, but the inspected page-load harness targets release `servoshell`, uses a reduced TP5-style manifest, and explicitly cannot support Servo-versus-Gecko speed conclusions by itself;
- the inspected benchmark-adjacent Servo fixture surfaces include `647` files under `tests/blink_perf_tests`, smaller Dromaeo/jQuery/power surfaces, and only the TP5N manifest under `etc/ci/performance/page_load_test/tp5n`;
- Servo's current performance path may download external pagesets, clone or update WARC infrastructure, install Python packages, and submit to Perfherder, so it is not a Turing no-claim fixed-hardware run without adaptation.

Result: `ADR9-EV-014` moves from missing to partial. This is not a performance result. Turing now has a checked resource-attribution taxonomy, but still needs an owner-approved fixed-host and OS image manifest, a browser-launch no-claim runner, runner-generated local corpus raw samples and artifact hashes, process/site-isolation disclosure, lifecycle state disclosure, browser-emitted private/resident/committed/shared/compressed/swap/semantic-owner/GPU memory data, startup/input/frame-pacing/CPU/wakeup/energy measures, failure denominator, and equal-security/equal-workload comparison runbooks before any speed, memory, energy, or Chrome-class inference.

## Security, sandbox, and maintenance implications

The dated [Servo Security and Maintenance Implications - July 2026](../research/servo-security-maintenance-implications-2026-07.md) records first-pass sandbox, process-authority, origin/profile, native/media/GPU/update, release-workflow, and upstream-maintenance evidence for `ADR9-EV-015` and `ADR9-EV-016`.

Key observations:

- Servo default options set `multiprocess: false` and `sandbox: false`, while `servoshell` exposes `--sandbox` only as a sandbox-if-multiprocess option;
- the inspected Windows sandbox code path logs unsupported sandboxed multiprocess or panics when content-process sandboxing is requested, and the Windows multiprocess spawn path starts an unsandboxed child process;
- macOS and Linux-like sandbox profiles use `gaol` and resource/font file-read allowances, but no Turing effective-policy evidence or negative sandbox tests were run;
- Servo event-loop routing reuses event loops by registered domain except sandboxed-origin contexts, while public/private resource and storage threads and selected origin checks exist as implementation concepts that still need Turing identity-preservation tests;
- initial script state carries many security-relevant senders, including resource/storage, DevTools, font service, paint, memory/time profilers, optional Bluetooth, WebGL/WebXR, privileged URLs, and user-content handles;
- the 2026-07-17 upstream metadata snapshot showed `servo/servo` public, not archived, security-policy-enabled, and pushed/updated that day; the 2026-07-19 refresh shows a later `main` commit while the latest GitHub release remains `v0.3.0`;
- the external checkout contains `22` workflow files, `25` CODEOWNERS rules, `19` Dependabot groups, release workflows with production builds and artifact attestations, and a crates.io publishing path.

Result: `ADR9-EV-015` and `ADR9-EV-016` move from missing to partial. This is not security approval or a maintenance commitment. Turing still needs owner-reviewed process authority maps, Windows/macOS/Linux sandbox deltas with negative tests, origin/site/profile/storage/DevTools/extension/agent identity-preservation evidence, native/media/GPU/runtime/update risk review, fuzzing and compromised-process evidence for any accepted component boundary, patch ownership, upstream cadence policy, security-response expectations, merge-burden estimate, breakage/rollback plan, and named primary/backup owners before any release-path relationship is accepted.

## Decision gates

`ADR-0009` cannot be accepted until all applicable gates below have evidence or an explicitly approved exception.

| Gate | Required evidence | Blocks |
|---|---|---|
| Source identity | exact repo URL, commit SHA, tag, crate version, release branch, archive digest, retrieval date | ambiguous dependency or stale research |
| Build reproduction | host OS, toolchain, bootstrap command, build command, build logs, cache policy, failure logs | claims that Servo is usable on the reference host |
| License and provenance | license files, third-party notices, generated sources, copied code policy, clean-room rule | importing source, snippets, tests derived from implementation |
| Dependency inventory | normal, build, dev, optional, native, generated, unsafe, JIT, media, GPU, network, storage, and platform dependencies, including block-level unsafe review, feature-correct full clean generated-output regeneration beyond the package-scoped dummy-media probe, accepted build-script/proc-macro side-effect policy, dynamic tracing, and generated-output provenance for any candidate component | selective component or release-code use |
| Runtime boundary | JavaScript engine, GC, WebAssembly, Web IDL, DOM wrapper, JIT, and no-JIT behavior | conflict with `ADR-0004` |
| Engine ownership | which DOM, CSS, layout, paint, navigation, storage policy, DevTools, accessibility, and embedding semantics Turing still owns | conflict with `ADR-0002` and `REQ-ENG-007` |
| Security model | process topology, sandbox, broker, origin/site/profile boundaries, update, incident, and vulnerability handling | release-path or preview use |
| Performance method | fixed hardware, local corpus, security-equivalent settings, lifecycle disclosure, process disclosure, raw samples, statistics | speed, memory, energy, or "extreme performance" claims |
| Compatibility method | WPT/Test262 subset, disabled tests, pass-rate denominator, unsupported APIs, web app corpus, failure accounting | compatibility or Chrome-class claims |
| Maintenance model | upstream cadence, patch ownership, LTS scope, security response, API breakage, merge burden, backup owner | broad implementation or support commitment |

## Option scorecard

Use this current posture as decision support before writing the ADR. It is evidence-bounded, not a recommendation.

| Option | Independence fit | Schedule impact | Security risk | Performance evidence | Compatibility evidence | Maintenance cost | Required doc changes if accepted |
|---|---|---|---|---|---|---|---|
| Clean implementation informed by Servo | High; preserves the independent-engine boundary and treats Servo as research input only | Slowest near-term path for engine implementation, but avoids source-import approval work | Lowest Servo-import risk; still needs clean-room, provenance, and no-copy enforcement | No Turing performance evidence; Servo observations can only shape harness design until Turing has raw runs | No compatibility behavior transfers; Turing-owned corpus, WPT, and Test262 evidence remain required | High implementation burden, lower upstream merge burden | likely no charter change; update research, clean-room policy, tests, work packages, and unsupported behavior |
| Selective Servo components | Medium; independence depends on narrow accepted component boundaries and replacement contracts | Could reduce focused subsystem work, but current evidence shows high review overhead before any component is eligible | Medium to high; each component inherits dependency, native, unsafe, FFI, generated-output, sandbox, and identity obligations | No current component-level benchmark evidence; each accepted component needs fixed-hardware raw artifacts and equal-workload disclosure | No compatibility claim transfers; each component needs denominator accounting for affected WPT, Test262, and local corpus cases | High ongoing merge, security-response, native-package, and provenance burden | dependency, provenance, risks, accepted/excluded component lists, API contracts, affected subsystem books, ledgers, and support language |
| Upstream-first collaboration | High while the release boundary stays independent | Uncertain; may improve research and patches but does not by itself unblock implementation | Low direct import risk, medium coordination risk around disclosure, patch custody, and evidence reuse | No Turing performance evidence; upstream results stay external unless reproduced under Turing controls | No compatibility behavior transfers; upstream fixes still need Turing-owned verification | Medium coordination and patch-ownership burden; lower than fork maintenance if no release-path code is adopted | contribution policy, backlog, ownership, upstream map, disclosure coordination, and evidence-ingestion rules |
| Servo-derived engine | Low under the current charter; conflicts with current independent-engine language unless superseded | Could accelerate a demo, but broad legal, security, dependency, JavaScript-runtime, and maintenance evidence becomes mandatory | High; Turing would inherit or rejustify Servo process, sandbox, native, unsafe, FFI, JIT, update, and incident-response surfaces | No Turing fixed-hardware Servo-derived baseline exists; external build success is not speed, memory, energy, or Chrome-class evidence | No Turing compatibility baseline exists; Servo behavior cannot be claimed without selected-baseline runs and denominators | Very high fork/upstream/security-response/release-support burden | supersede `ADR-0002`, `ADR-0004`, `REQ-ENG-007`, roadmap, risks, technology stack, support language, and public claims |
| Explicit Servo browser charter change | Replaces the current charter rather than fitting inside it | Resets roadmap and product framing; may simplify source identity but invalidates current independence assumptions | High governance and support risk; all security, dependency, release, and upstream obligations must be rebaselined | Existing Turing performance plan must be rebuilt around the new charter before claims | Existing Chrome-class and compatibility plan must be rebuilt around the new charter before claims | Very high program, brand, upstream, legal, release, and support burden | rewrite charter, requirements, risks, market strategy, support language, roadmap, governance, and release operations |

## Experiment plan

Run the source-strategy experiment outside this repository unless a reviewed task explicitly changes that rule.

1. Create an isolated workspace under a non-Turing source path.
2. Fetch Servo by exact commit and verify the remote URL.
3. Record host OS, CPU, RAM, GPU, Rust, Python, `uv`, Visual Studio or platform SDK, and environment variables.
4. Run Servo bootstrap and build commands exactly as upstream documents them.
5. Save build logs, failure logs, artifact paths, and cache sizes.
6. Extract dependency metadata without copying Servo source into Turing.
7. Extract the public embedding API inventory from generated docs and crate metadata.
8. Create a tiny local corpus plan that can be used across Servo, Chromium, Firefox, WebKit where available, Ladybird where runnable, and future Turing harnesses.
9. Record what could not be tested and why.
10. Write `ADR-0009` with a recommendation, rejected options, risks, required follow-up work, and status language.

## Required outputs

The ADR packet is incomplete until it includes:

- `ADR-0009` prose in [Blueprint 17](../blueprint-v1/17-architecture-decisions.md) or a linked ADR file if the ADR system is expanded;
- updated [pre-build readiness](../blueprint-v1/machine/pre-build-readiness.json);
- updated source, dependency, unsafe, native, generated-code, and provenance ledgers if any source or dependency enters this repo;
- updated risk and requirement records if the independence boundary changes;
- updated [technology stack](../technology-stack/README.md), [engine](../engine/README.md), [JavaScript](../javascript/README.md), [security-engine](../security-engine/README.md), [embedding](../embedding/README.md), [competitive](../competitive/README.md), and [release operations](../release-operations/README.md) documents as applicable;
- a clear public-claim statement that says what Turing is and is not after the decision.

## Current recommended next step

Use the successful short-path build, build reproduction evidence and gap report, dependency metadata inventory, supply-chain policy scan, license/advisory/SBOM decision prep, generated/native/unsafe/FFI classification, unsafe/FFI contract review, build-script/generated-output audit, clean generated-output reproduction probe, generated-output generator manifest, generated-output source-to-output provenance map, build-script/proc-macro side-effect audit, source/archive provenance audit, upstream source provenance report, independent source verification report, source-baseline equivalence policy prep, native bootstrap provenance audit, native package decision prep, component-boundary and JavaScript conflict analysis, local compatibility corpus and WPT/Test262 evidence, performance-baseline preparation, security/maintenance implications, [ADR-0009 Evidence Traceability Matrix](15-adr-0009-evidence-traceability-matrix.md), and [ADR-0009 Decision Draft and Public-Claim Impact](16-adr-0009-decision-draft.md) to complete the rest of the `ADR-0009` evidence packet: owner-selected source baseline and equivalent provenance policy, owner-accepted equivalence policy, selected-baseline blob/legal review, independent clean-target build replay, Turing-specific license/advisory/SBOM decisions, native source-build or binary-package exception records, final native package notices, package-minimization decisions, package manifests, block-level unsafe review using the unsafe/FFI triage plan, owner-reviewed generated-output generator manifest tied to the selected baseline/profile/output families/generator versions/environment policy, owner-reviewed source-to-output license/provenance approval tied to the selected baseline/profile/component boundary, feature-correct full clean generated-output regeneration beyond the package-scoped dummy-media probe, accepted build-script/proc-macro side-effect policy, dynamic tracing, proc-macro provenance review, accepted FFI ABI contracts, owner-reviewed component boundaries, owner-reviewed JavaScript-runtime conflict decision, Turing-owned local compatibility HTTPS/browser runs beyond the checked harness plan, focused WPT/Test262 denominator accounting, runner-generated fixed-hardware performance and memory baseline with raw artifacts, owner-reviewed security/sandbox implications, owner-approved maintenance/upstream relationship model, owner-applied public-claim/document/registry diffs, and an explicit recommendation. Do not start HTML, DOM, CSS, layout, or JavaScript implementation that assumes a Servo relationship until the decision packet is complete and reviewed.
