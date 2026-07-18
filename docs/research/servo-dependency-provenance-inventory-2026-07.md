# Servo Dependency and Provenance Inventory — July 2026

Status: dated dependency metadata inventory for `PB-002` and proposed `ADR-0009`; no dependency approval
Owner: architecture, security, provenance, release operations, and engine owners
Retrieval date: 2026-07-17
Confidence: medium for Cargo metadata counts; low for license, advisory, native, generated-code, and source-adoption conclusions until dedicated reviews run

## Question

What does the successful external Servo checkout reveal about dependency scale, provenance shape, native/build-script exposure, and source-strategy risk before Turing decides whether to study, reuse, fork, or reject Servo-derived release code?

This inventory does not import Servo source, approve a dependency, approve a component, or promote `PB-002`. It narrows the remaining evidence required by the [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md).

Follow-up reports record [Servo Supply-Chain Policy Scan — July 2026](servo-supply-chain-policy-scan-2026-07.md) results, the [Servo License Advisory and SBOM Decision Prep - July 2026](servo-license-advisory-decision-prep-2026-07.md), the [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md), the [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md), and the [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md) for the same checkout.

## Source identity and local artifacts

Observed from the external checkout `C:\ts\servo`:

- remote: `https://github.com/servo/servo.git`;
- commit: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- commit date: 2026-07-17T15:50:14Z;
- commit subject: `script: Mechanically migrate more to reflect_dom_object_with_proto (#46593)`;
- tracked files: `193033`;
- tracked-file status after bootstrap, build, and metadata extraction: clean.

Local evidence files were written outside the Turing repository:

- `C:\ts\servo-bootstrap.log`;
- `C:\ts\servo-build-dev-vsdevcmd-llvm.out.log`;
- `C:\ts\servo-build-dev-vsdevcmd-llvm.err.log`;
- `C:\ts\servo-metadata-default.json`;
- `C:\ts\servo-metadata-all-features.json`;
- `C:\ts\servo-tree-features-depth1.txt`.

## Method

Commands run from `C:\ts\servo`:

```powershell
cargo metadata --locked --format-version 1 > C:\ts\servo-metadata-default.json
cargo metadata --locked --format-version 1 --all-features > C:\ts\servo-metadata-all-features.json
cargo tree --locked -e features --depth 1 -p servo > C:\ts\servo-tree-features-depth1.txt
```

The `--all-features` metadata command downloaded additional optional crates into the user Cargo cache because not every optional dependency was already present locally. That is external evidence collection, not a Turing source import.

The metadata was parsed with Node because PowerShell `ConvertFrom-Json` rejected Servo metadata containing case-distinct feature keys such as `USB` and `usb`.

## Cargo metadata summary

| Scope | Workspace packages | Total packages | Path packages | Registry packages | Git packages | Packages with build scripts | Proc-macro packages | Native-link packages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Default metadata | 75 | 1069 | 75 | 983 | 11 | 157 | 70 | 25 |
| All-features metadata | 75 | 1120 | 75 | 1034 | 11 | 167 | 71 | 26 |

Dependency edges recorded across package manifests:

| Scope | Normal edges | Build edges | Dev edges | Optional dependency edges |
|---|---:|---:|---:|---:|
| Default metadata | 5268 | 124 | 1856 | 1815 |
| All-features metadata | 5595 | 136 | 1955 | 1956 |

These are Cargo metadata edges, not an audited runtime dependency closure. Target-specific activation, feature unification, generated sources, native libraries, and release packaging still need a dedicated SBOM and build-plan review.

## Feature posture

The `servoshell` default feature set includes `baked-in-resources`, `bundled_freetype`, `gamepad`, `servo/clipboard`, `js_jit`, `max_log_level`, `webgpu`, and `webxr`.

The `servoshell` dependency on the `servo` crate uses `default-features = false` and enables `background_hang_monitor`, `bluetooth`, and `testbinding`; on Windows it also enables `no-wgl`. The feature tree also exposed first-level defaults for WebRender capture, WebGL, canvas, layout, script, network, storage, DevTools, media, profile, wakelock, and webdriver-related crates.

The all-features metadata adds optional surface area such as native Bluetooth, GStreamer media, Vello, tracing backends, platform-specific windowing, additional WebGPU/Naga variants, and other platform support crates. These are evidence targets, not approved Turing capabilities.

## Git-sourced packages

Default metadata contained 11 git-sourced packages, all from the Servo Stylo repository at revision `d3de91cbac7bba38e159239b3c0a360783fce2ee`:

| Package | Version | License |
|---|---:|---|
| `selectors` | 0.39.0 | MPL-2.0 |
| `servo_arc` | 0.4.3 | MIT OR Apache-2.0 |
| `stylo` | 0.19.0 | MPL-2.0 |
| `stylo_atoms` | 0.19.0 | MPL-2.0 |
| `stylo_derive` | 0.19.0 | MPL-2.0 |
| `stylo_dom` | 0.19.0 | MPL-2.0 |
| `stylo_malloc_size_of` | 0.19.0 | MIT OR Apache-2.0 |
| `stylo_static_prefs` | 0.19.0 | MPL-2.0 |
| `stylo_traits` | 0.19.0 | MPL-2.0 |
| `to_shmem` | 0.5.0 | MPL-2.0 |
| `to_shmem_derive` | 0.1.0 | MPL-2.0 |

The Stylo dependency is not a minor library detail. It directly affects style-system ownership, selector matching, shared-memory representation, build provenance, and the meaning of Turing's independent-engine boundary.

## License metadata observations

Cargo metadata reported no package missing both a `license` field and `license_file` in either the default or all-features inventory.

Top license expressions in default metadata:

| License expression | Package count |
|---|---:|
| MIT OR Apache-2.0 | 404 |
| MIT | 201 |
| Apache-2.0 OR MIT | 109 |
| MPL-2.0 | 99 |
| MIT/Apache-2.0 | 51 |
| Unicode-3.0 | 44 |
| Apache-2.0 | 33 |
| BSD-3-Clause | 19 |
| Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT | 16 |
| Zlib OR Apache-2.0 OR MIT | 14 |

This is not a legal clearance. The next review still needs full license text collection, notice generation, patent analysis, source-offer obligations, generated-code ownership, binary dependency review, and comparison against Turing's approved license policy.

## Native-link and build-script exposure

Default metadata exposed 25 packages with Cargo `links` values:

- cryptography and TLS: `aws-lc-rs`, `aws-lc-sys`, `ring`;
- JavaScript runtime: `mozjs_sys`;
- CSS/style: `stylo`;
- generated script bindings: `servo-script-bindings`;
- graphics, codecs, compression, and media-related foundations: `freetype-sys`, `harfbuzz-sys`, `libz-sys`, `mozangle`, `wuff-capi`, `zstd-sys`;
- storage and database: `libsqlite3-sys`, `sqlite-wasm-rs`;
- platform/system integration: `clang-sys`, `libudev-sys`, `objc-sys`, `openxr-sys`, `yeslogic-fontconfig-sys`;
- allocator and runtime support: `tikv-jemalloc-sys`, `rayon-core`;
- encoding and WebAssembly support: `encoding_c`, `encoding_c_mem`, `wasm-bindgen-shared`;
- metadata-only or build-specific entries: `defmt`, `prettyplease`.

The default inventory also contained 157 packages with build scripts and 70 proc-macro packages. These surfaces require classification before selective reuse because they can execute code at build time, generate Rust sources, link native libraries, or hide platform-specific dependencies behind target conditions.

## Duplicate-version pressure

Default metadata contained 58 package names with multiple versions. All-features metadata contained 69. Default examples include:

- `itertools`: `0.10.5`, `0.13.0`, `0.14.0`, `0.15.0`;
- `getrandom`: `0.2.17`, `0.3.4`, `0.4.1`;
- `hashbrown`: `0.15.5`, `0.16.1`, `0.17.1`;
- `read-fonts`: `0.37.0`, `0.39.2`, `0.41.0`;
- `redox_syscall`: `0.4.1`, `0.5.18`, `0.9.0`;
- `skrifa`: `0.40.0`, `0.42.1`, `0.44.0`;
- `http`: `0.2.12`, `1.4.2`;
- `cookie`: `0.16.2`, `0.18.1`.

Duplicate versions are not automatically defects, but they are material to binary size, advisory handling, patch cadence, memory footprint, and long-term maintenance.

## High-impact dependency clusters

The inventory identified dependency clusters that would need separate owner review before any Servo relationship can affect Turing release code:

| Cluster | Examples | Why it matters |
|---|---|---|
| JavaScript runtime | `mozjs`, `mozjs_sys`, default `js_jit` | Direct conflict pressure against `ADR-0004` unless explicitly superseded |
| CSS/style | `stylo`, `selectors`, `stylo_*`, `to_shmem*` | Affects Turing ownership of CSS semantics, shared-memory policy, and style performance claims |
| Rendering/GPU | `webrender`, `wgpu`, `naga`, `mozangle`, `surfman`, GL/EGL/X11/Wayland/Windows/macOS crates | Affects compositor ownership, sandboxing, driver attack surface, and performance baselines |
| Media and WebRTC | GStreamer crates, media and WebRTC Servo path crates | Affects codec policy, native libraries, patent/licensing questions, process isolation, and energy claims |
| Cryptography/TLS | `rustls`, `aws-lc-rs`, `aws-lc-sys`, `ring`, `rustls-platform-verifier` | Requires Turing's foundation-dependency review and certificate/platform verifier analysis |
| Storage | `libsqlite3-sys`, `sqlite-wasm-rs`, `rusqlite` | Affects profile storage, recovery, sandbox, and migration policy |
| Platform UI/input/accessibility | `winit`, `egui`, `accesskit_*`, platform Objective-C/JNI/Windows/Wayland/X11 crates | Affects the native UI rule and trusted-chrome boundary |
| DevTools and automation | `servo-devtools`, `servo-webdriver-server`, `webdriver` | Affects protocol authority, debugging trust boundaries, and agent/automation model |

## Source-strategy implications

1. A Servo-derived or selective-component path would be a major supply-chain and provenance program, not a small Rust dependency addition.
2. The presence of SpiderMonkey/MozJS and default `js_jit` keeps `ADR-0004` as a hard blocker for any release path that imports Servo runtime behavior.
3. Stylo is a separate git source that would need its own exact archive digest, license review, provenance record, generated-code review, and ownership decision.
4. The number of build scripts, proc macros, native-link packages, and duplicate versions means a selective reuse decision must start with a component boundary, not with the whole workspace.
5. The cleanest near-term use of Servo remains research, differential testing, corpus comparison, and architecture study while Turing preserves a clean-room implementation boundary.

## What this does not prove

This inventory does not prove:

- every dependency is acceptable under Turing's license policy;
- every dependency is vulnerability-free or maintained;
- the built `servoshell.exe` is safe for hostile browsing;
- any Servo subsystem is compatible with Turing's process, sandbox, JavaScript, UI, or agent model;
- Servo is faster, lower memory, more secure, more accessible, or Chrome-class;
- Turing should adopt Servo, Stylo, WebRender, SpiderMonkey, or any transitive dependency.

## Next evidence required

Before `ADR-0009` can advance, produce:

1. a full SBOM for the exact Servo checkout and feature profile;
2. license text, notice, source-offer, and patent review for registry, git, path, and downloaded native packages;
3. advisory and yanked-package scan with timestamps and policy;
4. build-script, proc-macro, generated-code, and native-link classifications;
5. owner-selected source-baseline policy, source-content/release-archive/package equivalence, and native bootstrap package source-build or binary-package policy beyond the local Servo, Stylo, registry-cache, upstream source, and native bootstrap identity evidence already captured;
6. unsafe-code and FFI inventory for any candidate component;
7. owner-reviewed component-boundary and JavaScript-runtime conflict decisions for JavaScript, CSS/style, rendering, networking, storage, media, DevTools, embedding, and UI, using the first-pass boundary report as input;
8. local compatibility and performance corpus results under a published method;
9. maintenance model and patch ownership for each option in the ADR-0009 scorecard.

## Affected records

This inventory adds evidence for `PB-002` but does not change its blocked status. It informs:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [Servo Source Strategy Inventory — July 2026](servo-source-strategy-inventory-2026-07.md);
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md);
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md);
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md);
- [Build, release, distribution, and operations](../blueprint-v1/13-build-release-operations.md);
- [Architecture decisions](../blueprint-v1/17-architecture-decisions.md).
