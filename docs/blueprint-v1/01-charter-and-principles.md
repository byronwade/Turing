# 01 — Charter and Engineering Principles

## 1. Product charter

Turing will be an independent desktop browser for macOS, Windows, and Linux, followed only later by mobile variants. The product serves two audiences from one security model:

- everyday users who need dependable browsing, accessibility, privacy, credentials, downloads, media, printing, profiles, sync, updates, and predictable controls;
- developers and software agents who need inspectable state, deterministic automation, rich diagnostics, reproducible sessions, and explicit authority.

The browser’s differentiation is not a decorative shell around a mature engine. It is the combination of an independent web engine, resource-accountable multi-process architecture, excellent native-feeling UI, first-class DevTools, and an agent interface built into the permission system.

## 2. Scope definition

### 2.1 Built by Turing

Turing owns and tests the following behavior:

- browser chrome, tabs, workspaces, profiles, permissions, history, bookmarks, downloads, session recovery, settings, credential UX, updates, and developer surfaces;
- navigation, frame trees, origin and site computation, browsing-context groups, process assignment, lifecycle policy, and back/forward cache policy;
- HTML tokenization and tree construction; DOM; events; editing and form behavior; CSS parsing, cascade, inheritance, values, style invalidation, layout, fragmentation, painting, hit testing, scrolling, compositing, and accessibility-tree generation;
- Web IDL bindings, event loop, timers, tasks, microtasks, modules, workers, service workers, JavaScript integration, and WebAssembly integration;
- HTTP cache policy, cookie policy, storage partitioning, permissions, content security enforcement, mixed-content checks, CORS, CORP, COOP, COEP, CSP, referrer policy, and download policy;
- DevTools protocols and UI, automation endpoints, extension host boundaries, and agent action protocol.

### 2.2 Foundational dependencies are permitted

“From scratch” does not require unsafe duplication of mature primitives. Dependencies may be used when they are not an existing browser engine and when the dependency decision is documented, pinned, audited, fuzzed at the integration boundary, and replaceable behind a narrow interface. Examples include:

- operating-system windowing, accessibility, keychain, notification, graphics, audio, printing, and sandbox APIs;
- Rust standard library and selected memory-safe crates;
- audited TLS and cryptographic implementations rather than custom cryptography;
- Unicode data and algorithms, IDNA tables, time-zone databases, certificate roots, MIME registries, and public suffix data;
- font rasterization and shaping libraries, image and media codecs, compression libraries, SQLite, and GPU API abstractions;
- a compiler backend such as Cranelift for Turing-owned JavaScript bytecode and intermediate representation;
- conformance suites such as Web Platform Tests and Test262.

Every exception is recorded in the dependency ledger with owner, version, license, update policy, exposed attack surface, fuzz target, and replacement plan.

### 2.3 Explicitly excluded from the engine

The following are prohibited as hidden shortcuts:

- embedding Chromium/Blink/V8, WebKit/JavaScriptCore, Gecko/SpiderMonkey, Servo as a complete engine, Electron, CEF, Qt WebEngine, Android WebView, WKWebView, or equivalent;
- presenting an operating-system browser view as Turing rendering;
- proxying all pages to a remote browser and calling the client an independent engine;
- disabling site isolation, sandboxing, accessibility, standards tests, or background behavior merely to win a benchmark without disclosure;
- implementing cryptographic algorithms ad hoc;
- allowing a model to bypass browser permission prompts or access secrets that the corresponding human page cannot access.

## 3. Product principles

### P-001 — Evidence before claims

No statement such as “Chrome-compatible,” “secure,” “private,” “low memory,” “fastest,” “agent-safe,” or “production-ready” appears without a linked test definition, environment, result, date, and known limitations.

### P-002 — Security is architectural

Security is not a pre-release audit added to a monolith. Untrusted parsing and execution occur in sandboxed processes with minimal capabilities. Privileged services validate every message, treat renderer identity as hostile input, and expose no ambient file, network, credential, device, or cross-origin authority.

### P-003 — Correctness precedes optimization

A fast incorrect engine creates compatibility debt that later optimization makes harder to unwind. Normative behavior is covered by reduced tests before specialized fast paths are accepted.

### P-004 — Resource use is attributable

Memory, CPU, GPU, disk, network, wakeups, and model use are attributed to profiles, tabs, frames, workers, extensions, and agents. The product exposes this attribution to users and developers.

### P-005 — Tab lifecycle is visible and reversible

Background throttling, freezing, process coalescing, back/forward caching, serialization, and discard are separate states. The UI and diagnostics state which occurred. Tabs with audio, calls, capture, downloads, unsaved forms, active debugging, or explicit keep-alive are protected by policy.

### P-006 — Agents are principals, not macros

An agent has an identity, profile, grant set, allowed origins, action classes, quotas, expiration, and audit trail. It cannot inherit the full authority of the signed-in user merely because it can see a page.

### P-007 — Beautiful UI cannot obscure state

Visual polish must coexist with legible origin, profile, permission, download, security, agent, and resource states. Critical controls are not hidden behind ambiguous animation or color alone.

### P-008 — Developer surfaces use the same truth as the engine

DevTools, automation, telemetry, and agent observations consume versioned engine protocols. They do not scrape product UI or rely on a separate approximation of the DOM, network stack, or lifecycle.

### P-009 — Platform integration stays behind adapters

The core engine and browser policy are platform-neutral. macOS, Windows, and Linux adapters own windowing, input, sandbox launch, accessibility bridges, credential stores, printing, notifications, update integration, and graphics-device setup.

### P-010 — Failure is contained

A malformed page, renderer crash, GPU reset, storage corruption, extension failure, model timeout, or failed update cannot take down unrelated profiles or silently lose user state. Recovery behavior is designed and tested.

## 4. Stable top-level requirements

- **REQ-PROD-001:** Open, navigate, reload, stop, duplicate, pin, mute, close, restore, and move tabs without cross-profile state leakage.
- **REQ-PROD-002:** Support multiple isolated profiles and ephemeral private sessions.
- **REQ-ENG-001:** Parse and represent HTML without invoking an existing browser engine.
- **REQ-ENG-002:** Implement a Turing-owned CSS cascade, style system, layout system, display-list builder, and hit-testing model.
- **REQ-JS-001:** Execute ECMAScript through a Turing-owned language frontend and runtime architecture.
- **REQ-SEC-001:** Run untrusted web content in OS-sandboxed processes with no direct ambient filesystem or unrestricted socket access.
- **REQ-SEC-002:** Enforce origin, site, browsing-context-group, and profile separation in process assignment and storage.
- **REQ-PERF-001:** Publish reproducible startup, interaction, page-load, memory, energy, and 30-tab lifecycle benchmarks.
- **REQ-A11Y-001:** Produce a semantic accessibility tree and bridge it to native platform accessibility APIs.
- **REQ-DEV-001:** Provide versioned inspection and automation protocols independent of product UI.
- **REQ-AI-001:** Require deterministic authorization for every model-initiated action and confirmation for configured high-impact actions.
- **REQ-OPS-001:** Ship only signed, reproducible, rollback-capable artifacts from protected release workflows.

## 5. Claim maturity labels

Every public build carries one label:

- **Research:** architecture experiments; not safe for arbitrary browsing.
- **Engine preview:** selected standards work; sandbox and updater may be incomplete.
- **Developer preview:** signed builds, sandbox coverage, crash recovery, and documented compatibility subset; no general safety claim.
- **Beta:** sustained conformance and security gates, automatic updates, supported platforms, and incident response.
- **Stable:** published support policy, rapid security updates, broad compatibility evidence, accessibility validation, and independent security review.

The label is determined by gates, not schedule or visual completeness.
