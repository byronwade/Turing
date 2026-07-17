# 03 — Language and Dependency Strategy

## Decision summary

Use **Rust as the primary language** for the browser kernel, engine, JavaScript runtime, IPC, network/storage policy, agent policy, test infrastructure, and most cross-platform UI logic. Use small, audited amounts of C/C++ only at unavoidable ABI boundaries. Use Objective-C/Swift, C++/WinRT, and C or Rust FFI shims for platform frameworks where native APIs require them. Python and TypeScript are tooling languages, not trusted runtime languages.

This decision optimizes the program’s total risk-adjusted performance, not synthetic language speed alone. Browser failures are dominated by memory safety, concurrency, parser complexity, privilege boundaries, latency tails, and maintainability. Rust offers deterministic layout and control comparable to C++, zero-cost abstractions when used carefully, strong data-race prevention, expressive type-state modeling, and a growing systems ecosystem.

## Evaluation criteria

Each candidate is judged on:

1. predictable memory layout and allocation control;
2. memory safety in hostile parsers and JIT-adjacent code;
3. concurrency safety and async support;
4. FFI with OS, GPU, codec, font, database, and security libraries;
5. compiler and linker maturity across macOS, Windows, and Linux;
6. debugging, profiling, sanitizers, fuzzing, coverage, and reproducible builds;
7. binary size, startup, incremental compilation, and build throughput;
8. ability to express capability boundaries and invalid-state prevention;
9. ecosystem supply-chain quality and long-term staffing;
10. suitability for interpreters, garbage collectors, JITs, SIMD, and unsafe low-level code.

## Candidate analysis

### Rust

Strengths:

- ownership and borrowing eliminate broad classes of use-after-free, double-free, iterator invalidation, and unsynchronized mutation;
- enums, traits, newtypes, lifetimes, and `Send`/`Sync` constraints encode process roles, origin scopes, lifecycle states, and permission decisions;
- no mandatory garbage collector for the browser core;
- good C ABI interoperability and access to native APIs;
- strong Cargo workspace, test, benchmark, documentation, and fuzzing workflows;
- unsafe code can be isolated, reviewed, linted, and measured rather than spread through the codebase.

Costs:

- compile time and monomorphization can become material;
- borrow-driven architecture requires discipline around graph structures such as DOM and GC heaps;
- JITs, tracing collectors, self-referential structures, platform callbacks, and intrusive data structures still require unsafe code or carefully designed indirection;
- ecosystem quality varies, and dependency count can become a supply-chain problem.

Mitigation: maintain an unsafe-code ledger, restrict dependencies, use profile-guided builds, define stable internal ABIs between large components, and prefer arenas/handles over pervasive reference-counted graphs.

### C++

Strengths:

- unmatched ecosystem for browser, graphics, media, operating-system, compiler, and performance tooling;
- direct control over allocation, layout, SIMD, JIT memory, and low-level APIs;
- large pool of experienced browser engineers.

Costs:

- memory corruption remains a primary browser vulnerability source;
- ownership and thread-safety conventions are largely social or library-specific;
- undefined behavior and ABI complexity increase long-term security cost;
- refactoring large concurrent subsystems is riskier.

Decision: permit C++ only behind narrow interfaces where a mature dependency or platform API justifies it. Do not use C++ as the default language for new Turing-owned parsers, DOM, layout, IPC, or security policy.

### C

C offers simple ABIs and broad platform reach but insufficient safety and abstraction for a modern engine codebase. Use only for thin ABI shims or upstream libraries, never as the primary architecture language.

### Zig

Zig provides explicit allocation, straightforward C interoperability, cross-compilation strengths, and simple language semantics. It is attractive for isolated tooling or experiments, but its ecosystem, language stability, package story, and mature browser-scale concurrency/safety evidence are less favorable than Rust’s. Reevaluate for build tools or platform shims; do not make it the primary language in v1.

### Swift

Swift is productive and increasingly capable for Apple-platform UI and systems work, with ARC and native framework integration. Cross-platform maturity, ABI/runtime size, deterministic low-level control, and Windows/Linux UI ecosystem make it unsuitable as the core engine language. It may be used in a small macOS shell adapter when that materially improves integration.

### Kotlin/Java

Managed runtimes are strong for Android product layers but impose runtime startup, memory, GC, and platform assumptions unsuited to the desktop engine kernel. Kotlin may be used only for a later Android shell if the mobile architecture is approved.

### Go

Go has excellent tooling and concurrency ergonomics, but its garbage collector, runtime model, limited control over object layout, C interoperability costs, and lack of systems-level abstractions make it a poor fit for DOM/layout/JIT/rendering internals. It may be used for remote infrastructure, not the browser runtime.

### C#/.NET

C# offers strong productivity and desktop tooling, but managed-runtime memory behavior, platform packaging, native interop, and startup constraints are unfavorable for the core. It may be useful for external Windows tooling, not trusted engine code.

### TypeScript/JavaScript

Use TypeScript for generated protocol clients, documentation sites, and selected DevTools UI if measured. Do not implement browser chrome in Electron or run privileged policy in JavaScript. DevTools frontend code executes in a separate trusted-tool process with a constrained protocol, strict content security policy, and no direct renderer authority.

### Python

Use Python for repository validation, corpus generation, test orchestration, and data analysis. Release-critical scripts must pin versions, avoid network-dependent nondeterminism, and produce machine-readable output. Python does not ship in the browser runtime.

## Component language map

| Component | Primary language | Notes |
|---|---|---|
| Browser kernel/process broker | Rust | deny-by-default capabilities, typed IPC, lifecycle policy |
| HTML/DOM/CSS/layout/paint | Rust | arenas and stable handles; parallelism only after deterministic baseline |
| JavaScript frontend/runtime/GC | Rust | Cranelift may be evaluated as backend; frontend and semantics remain Turing-owned |
| Network and storage policy | Rust | protocol libraries behind Turing policy and partitioning layers |
| GPU compositor | Rust | direct Metal/D3D12/Vulkan adapters or a narrowly pinned abstraction |
| Cross-platform product state/UI model | Rust | retained scene graph and command model |
| macOS adapter | Rust plus Objective-C/Swift shim | NSWindow, input, accessibility, Keychain, sandbox, notarization |
| Windows adapter | Rust plus C++/WinRT shim | Win32/WinUI, UIA, Credential Manager, AppContainer, signing |
| Linux adapter | Rust plus C shim as needed | Wayland/X11 transition, AT-SPI, portals, seccomp/namespaces |
| DevTools frontend | TypeScript or Rust/WASM after benchmark | isolated tool process; no ambient browser privileges |
| Build/test/data tools | Python and Rust | Python for orchestration, Rust for high-throughput corpus tools |
| Update/telemetry services | Rust or Go | server choice independent from client trust boundary |

## Memory architecture choices

Rust alone does not guarantee low memory. Turing adopts explicit allocation policy:

- region/arena allocation for DOM nodes, style data, layout fragments, display items, and short-lived parser state;
- compact IDs and side tables instead of pointer-rich object graphs;
- string interning with profile/site lifetime boundaries and caps;
- copy-on-write or immutable shared data for parsed stylesheets, fonts, decoded resources, bytecode, and protocol schemas where isolation permits;
- per-subsystem budgets with pressure callbacks and hard ceilings;
- generational tracing GC only for JavaScript-managed objects, with DOM wrappers represented through stable handles;
- no default use of `Arc<Mutex<T>>` as architecture; ownership and actor/message boundaries are explicit;
- bounded channels and bounded queues; overload produces backpressure or cancellation rather than unbounded memory.

## Unsafe-code policy

All `unsafe` blocks require:

1. a `SAFETY:` comment describing preconditions and invariants;
2. an owner and review from the relevant subsystem;
3. Miri, sanitizer, fuzz, or model-check coverage appropriate to the operation;
4. no expansion of lifetime or thread-safety claims without proof;
5. entry in the generated unsafe inventory for release builds.

Unsafe code is expected in allocators, GC, JIT memory, SIMD, FFI, GPU mappings, shared memory, and some intrusive structures. The objective is not zero unsafe code; it is minimal, auditable, well-tested unsafe surface.

## Dependency acceptance policy

A new runtime dependency requires a decision record containing:

- exact functionality and why a local implementation is not justified;
- repository, maintainers, release cadence, minimum supported version, and bus-factor assessment;
- license and patent considerations;
- transitive dependency count;
- use of build scripts, proc macros, native code, networking, filesystem, or code generation;
- security advisory and update process;
- fuzz targets and boundary validation;
- supported platforms and deterministic-build behavior;
- replacement cost and abstraction boundary.

Dependencies are grouped:

- **Foundation:** cryptography, TLS, Unicode, font shaping/rasterization, codecs, compression, SQLite, GPU interfaces. High scrutiny, long-lived.
- **Build-only:** code generators, bindgen-like tools, documentation, test runners. Never included in runtime artifacts unless explicit.
- **Convenience:** small formatting, collection, or utility crates. Prefer local code when the dependency tree or maintenance cost exceeds the benefit.
- **Prohibited:** another browser engine, hidden network services, unreviewed binary blobs, ad/analytics SDKs, or crates requiring broad ambient authority.

## Initial dependency posture

The executable bootstrap intentionally uses only the Rust standard library. This validates architecture and keeps the first review legible. Production implementation will inevitably add dependencies, but only after interfaces, threat models, benchmarks, and license checks exist.

## Decision review triggers

Reopen the primary-language decision only if one of the following is demonstrated with a reproducible prototype:

- Rust prevents a required platform, JIT, or graphics capability;
- compile or binary-size costs remain outside published budgets after architectural mitigation;
- a different language materially reduces both security and performance risk for a clearly bounded subsystem;
- staffing or toolchain viability changes enough to threaten program continuity.

Preference or benchmark micro-wins alone are insufficient.

## Detailed technology selection

The [Technology Stack](../technology-stack/README.md) documents candidates and adoption gates. A named library is not approved without exact source/version, owner, license/provenance, unsafe/native and hostile-input review, fuzzing, platform/performance/build evidence, Turing-owned adapter, and replacement plan.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native browser-chrome toolkit research

The release shell uses Rust for durable state, commands, policy, recovery, and diagnostics. A compiled native toolkit may be used behind a replaceable adapter. Slint is the initial candidate; Vizia and Floem or GPUI are required comparisons. React/TypeScript may support a separate design lab, but React, JavaScript, Node, Electron, Tauri, and system webviews are excluded from trusted release chrome.
