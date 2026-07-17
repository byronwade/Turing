# Technology Stack and Engineering Toolchain

Status: candidate evaluation and operating baseline; no dependency approval  
Owner: architecture, build, security, and subsystem owners  
Last researched: 2026-07-16

## Decision model

“Best” means the lowest total cost across correctness, memory safety, latency, memory, energy, accessibility, interoperability, portability, licensing, build/release operations, maintainer health, and replacement—not popularity or one benchmark.

## Language map

| Layer | Preferred language | Rule |
|---|---|---|
| Browser kernel, IPC, engine, JS semantics, network/storage policy, resource model, Plug-in broker, DevTools protocol, agent authorization | Stable Rust, Rust 2024 edition | Default for Turing-owned runtime and hostile-input code |
| Universal public ABI | C | Opaque handles, explicit ownership, version negotiation; not the implementation default |
| GPU/codec/compiler/OS boundaries | C/C++ only when unavoidable | Narrow, reviewed, isolated, fuzzed, replaceable |
| Apple platform adapters | Swift/Objective-C | Thin adapter; no duplicate browser policy |
| Windows adapters | C++/WinRT or Rust windows bindings | Thin adapter with Turing semantic core |
| Android/JVM embedding | Kotlin/Java/JNI | Generated wrapper over stable contract |
| DevTools and constrained Plug-in UI | TypeScript | No privileged policy or ambient browser authority |
| Tests, analysis, benchmarks, release tooling, ergonomic SDK | Python | Not bundled as browser runtime |
| Portable multi-language Plug-ins | WebAssembly Components and WIT | Explicit imports, limits, interruption, no ambient WASI |
| C#, Go, Ruby and other SDKs | Generated bindings | Do not reimplement engine semantics |

## Framework and library candidates

- Text: Unicode/CLDR, HarfBuzz, FreeType, CoreText, DirectWrite behind Turing font/privacy/cache policy.
- Graphics: evaluate wgpu against direct Metal, D3D12, and Vulkan; retain deterministic software rendering; evaluate Vello for vector paths.
- Accessibility: evaluate AccessKit for custom chrome while validating VoiceOver, UI Automation, and AT-SPI directly.
- TLS/network foundations: evaluate rustls, low-level HTTP/2/3 and QUIC crates, and DNS primitives; Turing owns Fetch, CORS, cookies, cache, proxy, certificate UI, and partitioning.
- Storage: SQLite is the leading transactional-store candidate; use store-specific schemas and no general ORM in trusted stores.
- Compiler: Turing-owned interpreter/IR/GC; evaluate Cranelift for lowering and Wasmtime only for Plug-in components, never page JavaScript semantics.
- Async: do not standardize one ambient runtime across the browser. Use explicit schedulers; Tokio/Mio are candidates for isolated services and tooling.
- Testing: rustfmt, Clippy, Miri, sanitizers, Loom, proptest, cargo-fuzz/libFuzzer, cargo-nextest, WPT, Test262, fixed-hardware labs.
- Supply chain: lockfiles, cargo-deny, RustSec/cargo-audit, cargo-vet, SBOM, SLSA, in-toto/Sigstore, reproducible builds.
- Build: Cargo workspace plus a small Rust repository tool; CMake/Ninja for required native dependencies; evaluate sccache and lld/mold with evidence.

## Dependency gate

Every candidate needs exact version/source, owner, privilege, hostile-input exposure, unsafe/native inventory, transitive graph, license/patent review, fuzzing, platform matrix, update response, performance/build cost, Turing-owned adapter, and replacement plan. Mention here is not adoption.

## Primary sources

- Rust — https://www.rust-lang.org/
- Rust 2024 edition — https://doc.rust-lang.org/edition-guide/rust-2024/
- Servo — https://servo.org/
- WebAssembly Component Model — https://component-model.bytecodealliance.org/
- Wasmtime — https://wasmtime.dev/
- wgpu — https://wgpu.rs/
- AccessKit — https://github.com/AccessKit/accesskit
- HarfBuzz — https://harfbuzz.github.io/
- rustls — https://rustls.dev/
- SQLite — https://sqlite.org/
- Cranelift — https://cranelift.dev/

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI framework strategy

Trusted browser chrome uses no Electron, Tauri, system webview, React/JavaScript runtime, DOM, or runtime CSS parser. The working hypothesis is a pure Rust state/command core with a replaceable native adapter. Evaluate Slint first against Vizia and Floem or GPUI; monitor Xilem, Makepad, and Freya; use egui for internal tools; defer a custom TSX compiler until measured evidence justifies its cost.

Slint is not approved. Its license, selected backend/renderer, page-texture integration, accessibility, IME, binary/memory cost, native dependency graph, update policy, and replacement path require the [UI framework experiment](../ui-runtime/02-framework-landscape-and-selection-method.md).
