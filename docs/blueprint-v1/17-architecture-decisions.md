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

## Proposed decisions requiring review

### ADR-0009 — Servo relationship and source strategy

Status: proposed. Compare clean implementation informed by Servo, selective components, upstream-first collaboration, Servo-derived engine, and explicit charter change. No Servo-derived release code before evidence and acceptance.

### ADR-0010 — Stable C ABI and generated SDKs

Status: proposed. Canonical Rust API, minimal opaque C ABI, generated language SDKs, host responsibility matrix, and conformance suite.

### ADR-0011 — Capability-based Turing Plug-ins

Status: proposed. Prefer WIT/WebAssembly components, isolate WebExtensions, and prohibit ambient authority/native code.

### ADR-0012 — Machine-readable professional control plane

Status: proposed. Ownership, traceability, phase, review, and exception records become canonical Blueprint companions after a usability pilot.

<!-- MARKET-STRATEGY-2026-07 -->
## Decision candidates from market strategy

The market book does not accept new ADRs. Likely future decisions include the Space/profile/identity model, open workspace interchange format, snapshot retention/encryption, sync trust and self-hosting, privacy-receipt semantics, and agent task isolation. Each decision must preserve the accepted security and independence baseline or explicitly supersede it.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI decision candidates

### ADR-0013 — Replaceable native UI adapter and pure Rust shell model

Status: proposed. Durable browser state, commands, policy, recovery, traces, and resources remain toolkit-neutral Rust. Toolkit code is presentation-only and replaceable.

### ADR-0014 — Initial browser-chrome UI toolkit

Status: proposed. Select Slint, Vizia, Floem/GPUI, or another candidate only after equivalent reference-shell, page-surface, accessibility, license, security, footprint, platform, maintenance, and replacement evidence.

### ADR-0015 — React design-lab boundary

Status: proposed. React may consume generated tokens and fixtures in a separate development application but does not own browser logic and is absent from release chrome.

### ADR-0016 — Page-surface and compositor ownership

Status: proposed. Decide whether Turing or the selected toolkit owns the window swapchain and how page textures, damage, input, accessibility, scaling, capture, and device loss compose.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Proposed agent and production decisions

### ADR-0017 — Task-scoped autonomous engineering

Status: proposed. Agents use immutable tasks, deny-by-default tools, run provenance, independent verification, and no self-merge or stable-release authority.

### ADR-0018 — Stable-v1 scope and support contract

Status: proposed. Stable means a finite versioned capability/platform/support contract rather than an open-ended parity claim.

### ADR-0019 — TUF-style update trust separation

Status: proposed. Evaluate root, targets, snapshot, and timestamp roles, threshold signatures, offline roots, expiration, rollback/freeze resistance, delegation, and compromise recovery.

### ADR-0020 — Human release and signing authority

Status: proposed. Production signing, legal approval, vulnerability disclosure, support commitments, and stable promotion remain human-controlled and separated from implementation agents and ordinary CI.

<!-- NOVA-PLATFORM-ARCHITECTURE-2026-07 -->
### ADR-0021 — One Turing component runtime for Nova applications

Status: proposed owner-directed target; not accepted for release implementation. Decision preparation recorded 2026-07-22.

#### Context

The owner-directed Nova platform target makes Turing more than a browser: the browser, future desktop shell, and future Nova applications need one replaceable component/composition system. The pinned Nova JSX source is the visual source of truth, while the current repository has a toolkit-neutral shell model (`turing-ui-model`), a hand-built Nova reference renderer (`turing-chrome`), and a separate page engine (`turing-engine`). Without an explicit boundary, the project would grow a second UI renderer, allow page semantics to own trusted chrome, or import external React/Node/webview technology into a release path.

#### Proposed decision

Create one Turing-owned component runtime contract for application UI. JSX-shaped source may be compiled to bounded native component IR, retained state/command snapshots, layout/semantic output, animation timelines, and a shared scene/display representation. Browser chrome, DevTools, workspaces, and future desktop application surfaces use that contract. Platform APIs for windows, input, IME, clipboard, GPU presentation, and accessibility remain replaceable adapters. Page content remains an engine-owned surface reached through typed, identity-bearing compositor handles.

The external `react`, `react-dom`, Node, system webview, page DOM, and runtime browser CSS parser are not release dependencies. A Turing-owned compatibility surface may implement useful React-shaped APIs only after independent parsing, lifecycle, state, accessibility, fault, resource, performance, and security evidence.

This proposal does not resolve ADR-0009. Servo/networking ownership remains undecided until the source-strategy decision is accepted.

#### Consequences

- Nova becomes the visual/layout source for a shared runtime rather than a one-off chrome port.
- `turing-ui-model` remains the state/command contract; `turing-chrome` remains a reference renderer until runtime parity evidence exists.
- The future runtime must not depend on `turing-engine` page semantics or create a second DOM/state graph.
- A runtime slice requires an immutable `TASK-*` manifest, negative tests, independent review, and the native UI/page-surface/production gates named by the implementation plan.
- The initial cost is higher than retaining separate renderers, but the platform avoids duplicated invalidation, theming, accessibility, diagnostics, and customization models.

#### Required evidence before acceptance

1. Component IR schema and compatibility/versioning rules.
2. State, command, identity, epoch, lifecycle, cancellation, and resource contracts.
3. Nova source-region and token traceability for the initial fixture set.
4. Equivalent native fixtures for keyboard, IME, focus, screen reader, forced colors, reduced motion, localization, fault, and text-fit cases.
5. Page-surface/compositor proof and stale-handle negative tests.
6. Startup, memory, frame-pacing, invalidation, and energy measurements with reproducible manifests.
7. External-runtime exclusion, dependency, provenance, and replacement evidence.
8. Owner decision, independent review, accepted predecessor ADRs, and synchronized registries.

The canonical target contract is [`Turing Platform Architecture`](../application-runtime/01-turing-platform-architecture.md). This proposed ADR does not claim that the runtime exists, that Nova is release chrome, or that the browser is production-ready.
