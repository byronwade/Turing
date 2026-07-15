# 17 — Foundational Architecture Decision Records

These records are accepted for Blueprint v1. A later decision may supersede one, but the original rationale remains visible.

---

## ADR-0001 — Rust-first implementation

Status: accepted.  
Decision date: 2026-07-15.

### Context

A browser handles hostile input through parsers, graph structures, concurrent services, native APIs, a garbage-collected scripting runtime, GPU resources, and JIT-generated code. C++ provides control and ecosystem depth but leaves broad memory-safety and concurrency obligations to convention. Managed languages reduce control over startup, memory layout, and native integration.

### Decision

Rust is the default language for all new Turing-owned runtime code. C/C++, Objective-C/Swift, C++/WinRT, and other languages are restricted to reviewed platform/native boundaries. Tooling may use Python and TypeScript.

### Consequences

- Architecture will favor handles, arenas, ownership transfer, actors/messages, and explicit unsafe islands.
- Compile-time and borrow-model costs are accepted and measured.
- A dependency and unsafe-code policy is mandatory.
- JIT/GC/native boundaries still require specialized security work; Rust is not treated as proof of safety.

### Revisit when

A reproducible subsystem prototype shows Rust blocks a required capability or materially worsens total security/performance cost after mitigation.

---

## ADR-0002 — Independent engine, audited foundations allowed

Status: accepted.  
Decision date: 2026-07-15.

### Context

The project goal excludes a shell around Chromium/WebKit/Gecko or a system web view. Interpreting “from scratch” as implementing cryptography, Unicode data, codecs, font shaping, databases, and OS sandbox primitives would create risk without differentiating browser behavior.

### Decision

Turing owns web-engine and browser semantics: DOM, CSS, layout, paint, navigation, JavaScript integration/runtime architecture, storage/security policy, product UI, DevTools, and agent protocol. It may use narrowly integrated, audited foundational libraries and OS APIs that are not complete browser engines.

### Consequences

- No existing browser engine or remote-rendering fallback in release paths.
- Every foundation dependency receives a ledger entry, security boundary, license record, tests, and replacement strategy.
- Custom cryptography is prohibited.
- Marketing can say “independent engine” only with a disclosed dependency inventory.

### Revisit when

A dependency begins determining web behavior so broadly that Turing no longer owns the engine semantics.

---

## ADR-0003 — Capability-separated multi-process architecture and site isolation

Status: accepted.  
Decision date: 2026-07-15.

### Context

Untrusted pages, scripts, images, fonts, media, PDFs, extensions, GPU commands, and model output can contain exploitable defects. A single-process design maximizes exploit impact. One process per tab is also not a complete security model and can create unnecessary memory cost.

### Decision

Use a browser kernel plus sandboxed renderer, network, storage, GPU, media/decoder, extension, DevTools, agent, update, and crash processes. Renderer assignment is based on site instances and browsing-context groups. Capabilities are explicit, IPC is typed/bounded, and pressure may consolidate only security-equivalent workloads.

### Consequences

- Higher baseline process and IPC complexity is accepted.
- Resource accounting and lifecycle policy are built into the architecture.
- OS sandbox evidence is required per platform.
- “Low memory” cannot be achieved by silently removing site isolation.

### Revisit when

A different topology demonstrates equivalent or stronger containment with lower total cost under the same hostile workload.

---

## ADR-0004 — Turing-owned JavaScript semantics with interpreter-first tiering

Status: accepted.  
Decision date: 2026-07-15.

### Context

Embedding V8, JavaScriptCore, SpiderMonkey, or another complete runtime would accelerate compatibility but undermine the independent-runtime goal and constrain architecture. Building an optimizing JIT before a trustworthy semantic reference would magnify defects.

### Decision

Implement a Turing-owned lexer/parser, bytecode, interpreter, object model, GC, Web IDL integration, debugger, and tiering policy. Add baseline and optimizing JITs only after conformance and differential gates. A general compiler backend such as Cranelift may lower Turing IR to machine code.

### Consequences

- Early web compatibility and speed will be limited.
- Test262, GC stress, tier equivalence, W^X, no-JIT mode, and JIT fuzzing are mandatory.
- Runtime staffing is a critical path.
- Compiler backend dependency does not define language semantics.

### Revisit when

The independent runtime demonstrably makes the overall program nonviable and the project explicitly changes its charter; not merely because initial performance is slow.

---

## ADR-0005 — AI agents use capability grants and deterministic authorization

Status: accepted.  
Decision date: 2026-07-15.

### Context

Browser agents observe adversarial page content and can act with the user’s authenticated session. Prompt-only safeguards cannot prevent confused-deputy behavior, secret leakage, stale-target actions, or consequential mistakes.

### Decision

Agents are distinct principals. Observations are semantic, scoped, labeled, and redacted. Actions use a typed protocol carrying profile/origin/frame/document epoch, preconditions, risk class, and idempotency. A deterministic policy engine validates grants and requires visible confirmation for configured consequential actions. Models never receive ambient credentials or raw browser authority.

### Consequences

- Some tasks require user interaction and may be slower than unrestricted automation.
- Agents cannot synthesize trusted user activation or approve confirmations.
- Provider data flows, local-model resources, audit, cancellation, and adversarial evaluation are product features.
- Headless/automation modes use isolated profiles and explicit policy rather than hidden bypasses.

### Revisit when

A stronger formal capability system is available; never to replace deterministic checks with model judgment alone.

---

## ADR-0006 — MPL-2.0 for original Turing source

Status: accepted for bootstrap.  
Decision date: 2026-07-15.

### Context

The project should remain useful to open research and commercial adopters while requiring improvements to covered source files to remain available under the license. A permissive license would allow proprietary forks without sharing file-level modifications; strong copyleft could complicate embedding and platform integration.

### Decision

License original Turing source under Mozilla Public License 2.0, subject to legal review before broad distribution. Third-party components retain their own compatible licenses. Contribution provenance uses a DCO initially.

### Consequences

- Modified MPL-covered files must follow MPL obligations when distributed.
- Larger works may combine files under other terms subject to MPL boundaries.
- Third-party notices, source availability, and compatibility checks are required.
- Relicensing would require rights from contributors or a different contribution agreement.

### Revisit when

Legal review, contributor strategy, or distribution requirements show a material conflict. Do not imply dual licensing without the necessary rights.

---

## ADR-0007 — Honest lifecycle-aware performance reporting

Status: accepted.  
Decision date: 2026-07-15.

### Context

Browser memory comparisons are easily distorted by tab discard, process topology, cache state, workload differences, and platform accounting. Turing’s main differentiation depends on trustworthy efficiency claims.

### Decision

Publish versioned benchmark manifests, raw samples, semantic memory attribution, mixed-state and all-live 30-tab scenarios, process/site-isolation state, lifecycle counts, revival latency, and lost-state behavior. Competitor comparisons use named current versions and equivalent settings.

### Consequences

- Headline numbers may be less dramatic but are defensible.
- Resource instrumentation is a first-class subsystem.
- A result without complete manifest cannot support product claims.

### Revisit when

Measurement platforms improve; the transparency requirement remains.

---

## ADR-0008 — Browser UI is independent from the web engine

Status: accepted.  
Decision date: 2026-07-15.

### Context

Rendering essential browser chrome through the immature web engine would couple product reliability, security prompts, crash recovery, and performance to untrusted-content code paths. Using Electron or a system web view would violate the engine policy.

### Decision

Build browser chrome with a Turing-owned retained UI model and native platform adapters. Use native controls selectively for platform correctness/accessibility. DevTools may use a separate frontend technology in an isolated process, but trusted browser controls do not depend on page rendering.

### Consequences

- UI infrastructure is a substantial additional project.
- Browser chrome remains available during renderer failure.
- Accessibility semantics and platform text/input behavior must be implemented early.

### Revisit when

The Turing web engine is mature enough for nonessential internal surfaces and a security review approves the boundary; critical trusted controls remain independent.
