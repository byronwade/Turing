# Embedding and Multi-language SDK

Status: public-contract research; no stable API or SDK exists  
Owner: embedding, API, platform, security, release, and SDK owners  
Last researched: 2026-07-16

Turing must be usable as a secure browser engine/platform without becoming a monolith. A host should create a safe profile and view in a few lines while advanced authority remains explicit.

## Contract layers

1. Canonical idiomatic Rust API: Engine, Profile, View, Surface, Navigation, EventStream, CapabilitySet, ResourceBudget, PluginHost, CancellationToken, and typed IDs.
2. Minimal stable C ABI: one version-negotiated function table, opaque generation-checked handles, pointer-plus-length inputs, explicit alloc/free, stable status/error handles, operation handles, and declared thread affinity.
3. Generated C++, Python, Node/TypeScript, Swift, Kotlin/Java, C#, Go, and WIT SDKs from one schema and conformance corpus.
4. Interactive, offscreen, headless, deterministic-test, automation, and server-render modes share navigation, security, storage, lifecycle, and policy machinery.

## Host and engine responsibilities

Turing owns web semantics, renderer/site isolation, IPC, navigation/origin policy, certificate core, network/storage partitioning, credential broker interfaces, Plug-in/agent authorization, crash containment, and diagnostics. The host owns signed packaging, verified engine delivery, OS entitlements, trusted application chrome, secure profile location, declared services, user disclosures, and incident support. Unsafe configurations fail startup rather than degrade silently.

## Lifecycle and surfaces

Engine, profile, view, navigation, surface, and async operation are explicit state machines. Long operations have deadline, cancellation, exactly one terminal result, bounded event streams, and stale-epoch rejection. Surfaces identify size, scale, color, damage, synchronization, device generation, presentation, and release. Input, IME, clipboard, drag/drop, and accessibility remain structured semantics—not pixels or raw page pointers.

## Versioning and packaging

Product, engine, Rust API, C ABI, protocol schemas, profile format, Plug-in API, and SDKs have separate versions and compatibility ranges. Artifacts include signatures, checksums, SBOM, provenance, symbols, notices, source references, supported platforms, and host conformance. Packages cannot download unverified engines during import/build.

## Minimal design target

```rust
let engine = Engine::builder().secure_defaults().build().await?;
let profile = engine.ephemeral_profile().await?;
let view = profile.create_view().await?;
view.navigate("https://example.com").await?;
```

This is a design target, not an existing API.

## Primary sources

- Rust API Guidelines — https://rust-lang.github.io/api-guidelines/
- Rust FFI guidance — https://doc.rust-lang.org/nomicon/ffi.html
- UniFFI — https://mozilla.github.io/uniffi-rs/
- WebAssembly Component Model/WIT — https://component-model.bytecodealliance.org/
- Servo embedding work — https://servo.org/
- Semantic Versioning — https://semver.org/

<!-- MARKET-STRATEGY-2026-07 -->
## Portability and project-state integration

Embedding research must expose versioned import/export and Space/session concepts without leaking internal engine layouts. Hosts disclose which migration, sync, Plug-in, agent, and recovery responsibilities they implement. Open export remains available without a hosted account.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## UI-runtime optionality

The embeddable engine contract does not require hosts to ship Turing’s browser chrome toolkit. Full-browser distributions may use the selected adapter; embedders may provide their own trusted application UI while conforming to the same surface, input, accessibility, profile, security, lifecycle, and recovery contracts. Headless packages exclude desktop UI dependencies.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Production embedding readiness

Stable SDK and ABI support requires a finite platform/version matrix, host conformance, security responsibility, package provenance, update policy, compatibility window, migration, support term, and human release approval.
