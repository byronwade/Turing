# Technology Stack and Engineering Toolchain

Status: M0 Rust baseline selected; subsystem dependencies remain candidates  
Owner: architecture, release operations, security, and subsystem owners  
Last reviewed: 2026-07-17

## Decision model

“Best” means the lowest total cost across correctness, security, latency, memory, energy, accessibility, interoperability, portability, licensing, build operations, maintainer health, and replacement—not popularity or one benchmark.

## M0 selected baseline

The contained implementation foundation uses:

- Rust `1.97.1`;
- Rust 2024 for new production crates;
- Cargo resolver 3;
- rustfmt, Clippy, and rust-src;
- a committed lockfile;
- no external runtime or build dependencies;
- unsafe Rust and native code forbidden by default;
- Ubuntu 24.04 / `x86_64-unknown-linux-gnu` as the reproducible M0 CI reference.

The exact machine-readable record is [`toolchains.json`](../blueprint-v1/machine/toolchains.json).

This baseline selects the repository language and tooling, not the browser engine source strategy, UI toolkit, graphics backend, network stack, storage engine, compiler backend, media stack, or production platform matrix.

## Language map

| Layer | Preferred language | Rule |
|---|---|---|
| Kernel, IPC, engine, JS semantics, network/storage policy, resources, Plug-in broker, protocols, agent authorization | Stable Rust | Default for Turing-owned runtime and hostile-input code |
| Universal public ABI | C | Opaque handles and explicit ownership; not implementation default |
| GPU, codec, compiler, and unavoidable OS boundaries | C/C++ only when evidence requires it | Narrow, isolated, reviewed, fuzzed, replaceable |
| Apple integration | Swift/Objective-C | Thin adapter; no duplicate browser policy |
| Windows integration | Rust Windows bindings or C++/WinRT | Thin adapter |
| Android/JVM embedding | Kotlin/Java/JNI | Generated wrapper over stable contract |
| DevTools and development-only design tools | TypeScript | No ambient browser authority |
| Tests, analysis, benchmarks, release tools | Python and Rust | Not part of browser runtime unless explicitly approved |
| Portable Plug-ins | WebAssembly Components and WIT | Explicit imports, limits, cancellation, no ambient WASI |
| Other SDKs | Generated bindings | Do not reimplement engine semantics |

## Candidate foundations

- Text: Unicode/CLDR, HarfBuzz, FreeType, CoreText, DirectWrite.
- Graphics: wgpu versus direct Metal, D3D12, and Vulkan; deterministic software reference; Vello research.
- Accessibility: AccessKit where appropriate, with direct platform verification.
- TLS/network: rustls and low-level protocol primitives; Turing owns browser policy.
- Storage: SQLite is the leading transactional-store candidate.
- Compilation: Turing-owned JS semantics and IR; Cranelift may be evaluated for lowering.
- Plug-ins: Wasmtime and the WebAssembly Component Model are candidates.
- Async: no browser-wide ambient runtime by convenience.
- UI: Slint first prototype; compare Vizia and Floem or GPUI.
- Testing: Miri, sanitizers, Loom, property testing, fuzzing, WPT, Test262, fixed-hardware labs.
- Supply chain: cargo-deny/audit/vet, SBOM, SLSA, in-toto/Sigstore, reproducible builds.

## Dependency gate

Every external dependency requires exact source and version, owner, privilege, hostile-input exposure, unsafe/native/build-script inventory, transitive graph, license and patent review, fuzzing, platform matrix, update response, performance/build cost, Turing-owned adapter, and replacement plan.

Mention in research is not approval.

## Current source-policy records

- [`security/dependencies.json`](../../security/dependencies.json)
- [`security/unsafe-code.json`](../../security/unsafe-code.json)
- [`security/native-code.json`](../../security/native-code.json)
- [`security/generated-code.json`](../../security/generated-code.json)
- [`security/provenance.json`](../../security/provenance.json)

## Primary sources

- Rust 1.97.1 — https://blog.rust-lang.org/2026/07/16/Rust-1.97.1/
- Rust 2024 — https://doc.rust-lang.org/edition-guide/rust-2024/
- Cargo workspaces — https://doc.rust-lang.org/cargo/reference/workspaces.html
- Servo — https://servo.org/
- WebAssembly Component Model — https://component-model.bytecodealliance.org/
- wgpu — https://wgpu.rs/
- rustls — https://rustls.dev/
- SQLite — https://sqlite.org/
- Cranelift — https://cranelift.dev/
