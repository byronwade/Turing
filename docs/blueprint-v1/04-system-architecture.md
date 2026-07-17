# 04 — System Architecture

## 1. Architectural objective

Turing is a capability-separated multi-process system. Web content is hostile. Extensions are semi-trusted. Developer tools are powerful but not ambiently privileged. AI agents are distinct principals. Browser product code is not assumed correct merely because it is signed. Every process receives only the handles and services required for its current role.

The design optimizes three properties together:

- **containment:** a renderer compromise must not become filesystem, credential, device, or cross-profile compromise;
- **accountability:** CPU, memory, GPU, network, disk, wakeups, and model actions must map to responsible principals;
- **adaptability:** process topology can expand for isolation and contract under pressure without silently violating security boundaries.

## 2. Process graph

### 2.1 Browser kernel

The kernel is the root coordinator, not a place for all features. It owns:

- profile and window registries;
- browsing-context groups and site-instance assignment;
- process launch, sandbox profiles, capability grants, and liveness;
- navigation commit arbitration;
- permission and agent-policy decisions;
- UI command routing;
- lifecycle and resource-pressure policy;
- crash recovery and session checkpoints;
- update state and security minimum-version enforcement.

It does not parse arbitrary response bodies, decode media, execute JavaScript, render pages, or directly implement large database operations.

### 2.2 Renderer processes

A renderer hosts one or more compatible site instances, subject to site isolation and resource policy. It contains:

- HTML parser and DOM;
- CSS/style/layout/paint and accessibility-tree production;
- JavaScript realm/runtime instances;
- frame-local event loops, workers where assigned, editing, forms, and page APIs;
- display-list generation and hit testing.

A renderer has no unrestricted socket API, arbitrary filesystem access, keychain access, device enumeration, update access, or ability to choose its effective origin. It requests operations from brokers using typed messages containing process-assigned identity.

### 2.3 Network service

The network service owns protocol connections, proxy resolution, DNS policy, certificate verification integration, HTTP cache storage, cookie attachment decisions, content decoding, request prioritization, and network diagnostics. Requests are accepted only with kernel-issued context containing profile, network partition, top-level site, requesting origin, destination, mode, credentials mode, redirect policy, and initiator metadata.

The network process does not trust renderer-supplied cookie headers, security origins, referrer eligibility, or permission assertions.

### 2.4 Storage service

The storage service brokers cookies, local/session storage persistence, IndexedDB, Cache Storage, service-worker data, origin-private files, quota, eviction, and clear-site-data operations. Keys include profile and partition dimensions. Renderer processes receive logical handles, not database file paths.

Corrupt stores are isolated per profile/origin where possible. Schema migrations are transactional, versioned, rollback-aware, and fuzzed against interrupted writes.

### 2.5 GPU/compositor service

The GPU service validates display lists, resource sizes, texture formats, shader inputs, surface ownership, and command budgets before using Metal, D3D12, or Vulkan. It owns compositing, raster scheduling, surface presentation, and GPU telemetry. WebGL/WebGPU command streams require stricter validation and may use separate utility processes depending on backend maturity.

A GPU reset invalidates resources and triggers recoverable re-creation rather than browser termination.

### 2.6 Media utility processes

Audio/video demuxing, codec execution, image decoding, PDF parsing, font processing, archive extraction, and other high-risk native libraries run in specialized sandboxed utility processes. Privileges and filesystem access vary by task and are never inherited from the browser kernel.

### 2.7 Extension host

Extensions execute outside page renderers. The host enforces extension identity, declared permissions, host grants, incognito policy, quotas, and API availability. Content scripts enter a distinct execution world with explicit bridges. Native messaging runs through a separate broker with install-time registration and user-visible policy.

### 2.8 DevTools service and frontend

The DevTools service exposes a versioned protocol representing engine truth. The frontend is an isolated trusted-tool application. Attaching a debugger is a powerful action recorded by profile and target. Remote debugging requires explicit enablement, authentication, loopback defaults, and visible indicators.

### 2.9 Agent host

The agent host runs model-provider adapters, planning loops, semantic snapshot reduction, and tool orchestration outside renderers and outside the kernel. It receives redacted, policy-approved observations and submits structured action requests. The deterministic policy engine remains authoritative; model output is untrusted input.

### 2.10 Update and crash services

The updater verifies signed metadata and artifacts in a minimal process. Crash collection removes secrets, applies user/enterprise policy, and is incapable of reading arbitrary profile data. Symbolication occurs out of process or server-side.

## 3. Identity model

Every relevant object carries typed identity:

- `ProfileId`
- `PrivateSessionId` when applicable
- `BrowsingContextGroupId`
- `SiteInstanceId`
- `FrameId`
- `DocumentEpoch`
- `Origin`
- `TopLevelSite`
- `NetworkPartitionKey`
- `StoragePartitionKey`
- `ProcessId` and `ProcessRole`
- `ExtensionId`
- `AgentPrincipalId`
- `GrantId`

IDs are unguessable or scoped handles where spoofing matters. Renderers cannot mint identities accepted as authoritative. On navigation commit, document epoch changes and stale handles/actions fail closed.

## 4. Navigation transaction

A top-level or frame navigation is a transaction:

1. renderer/UI submits a navigation intent;
2. kernel validates initiator, sandbox flags, user activation, target context, and policy;
3. kernel chooses or creates a browsing-context group, site instance, and renderer;
4. network service performs request under a kernel-issued request context;
5. redirects are revalidated, including origin/site changes and download disposition;
6. response metadata is classified before body exposure;
7. kernel decides commit eligibility and target process;
8. renderer receives a bounded stream and provisional document identity;
9. commit atomically replaces the old active document and increments epoch;
10. history, permissions, UI security state, agent grants, and lifecycle hooks update;
11. old document enters destruction or eligible back/forward cache according to policy.

No renderer self-commits a privileged origin or reuses authority across an unapproved navigation.

## 5. IPC design

IPC is schema-first and capability-oriented.

Rules:

- every message has a version, sender role, receiver role, maximum encoded size, and timeout/cancellation semantics;
- unknown message variants fail closed across trust boundaries;
- large data uses validated shared-memory regions with immutable or single-writer ownership states;
- handles are typed and scoped to the connection; raw OS handles are not passed without broker mediation;
- queues are bounded; overload propagates backpressure, cancellation, coalescing, or process termination;
- privileged receivers recompute or verify security-sensitive data;
- request/response IDs cannot be reused across epochs;
- messages containing origins, URLs, paths, dimensions, counts, offsets, lengths, codecs, fonts, or GPU resources are range-checked;
- protocol changes include compatibility tests and threat-model review.

The preferred encoding is generated from a compact internal schema with Rust types on both ends. Serialization libraries are evaluated for bounds behavior, zero-copy safety, forward compatibility, and fuzzability.

## 6. Threading and execution model

Each process uses a small number of explicit execution domains:

- main/event-loop thread for role-specific state;
- bounded worker pools for CPU tasks;
- dedicated I/O reactors where required;
- compositor/raster scheduling threads in GPU service;
- JavaScript mutator thread per realm group initially, with parallel parsing/compilation and concurrent GC added only after correctness;
- database lanes serialized per logical store when required for transactions.

Tasks carry cancellation tokens and budget metadata. Background tabs receive scheduling classes rather than arbitrary sleeps. Priority inheritance prevents a visible page waiting indefinitely on work classified as background.

## 7. Memory topology

Memory is tracked by process and semantic owner. Shared resources have explicit chargeback rules. The memory coordinator receives:

- allocator and mapped-memory totals;
- JavaScript heap committed/live bytes;
- DOM/style/layout/display-list bytes;
- decoded image/font/media caches;
- GPU resource estimates;
- network/cache buffers;
- storage transactions;
- DevTools, extension, and agent allocations.

Pressure policy escalates through cache trimming, timer/network throttling, renderer working-set reduction, tab freezing, safe serialization, process consolidation where security-equivalent, and finally discard. Each action emits an observable lifecycle event.

## 8. Platform adapter boundary

The engine exposes platform-neutral interfaces for:

- windows and surfaces;
- keyboard, pointer, touch, pen, gesture, drag/drop, IME, and clipboard;
- accessibility tree updates and actions;
- fonts and fallback;
- audio/video devices;
- printing and PDF destinations;
- keychain/credential storage;
- notifications, share sheets, open/save panels, and portals;
- process launch and sandbox configuration;
- code signing, updates, crash capture, power/thermal state, and memory pressure.

Adapters translate native events into versioned internal types and never make web security decisions.

## 9. Data directories

A profile directory uses explicit sub-stores and version files. Secrets are stored in the OS credential service or encrypted with keys protected by it. Logs and crash data exclude URLs, query strings, form values, cookies, tokens, page text, model prompts, and file paths by default. Private sessions use ephemeral keys and directories with best-effort secure cleanup, while documentation avoids claiming guaranteed physical erasure on modern filesystems.

## 10. Recovery behavior

- Renderer crash: replace process, show per-tab recovery, preserve last committed URL and safe session state.
- GPU crash/reset: recreate service and surfaces; fall back to software only under explicit, visible policy.
- Network crash: restart service; retry only idempotent or user-approved requests.
- Storage crash: abort transactions, reopen stores, quarantine corrupt origin data if necessary.
- Agent-host crash: revoke in-flight grants and require replanning against a fresh document epoch.
- Kernel crash: external supervisor relaunches; session journal restores eligible windows/tabs without auto-replaying unsafe form submissions or agent actions.
- Update failure: retain known-good signed version and rollback within policy.

## 11. Architecture invariants

- **ARCH-001:** A renderer cannot create an unrestricted network socket.
- **ARCH-002:** A renderer cannot open an arbitrary filesystem path.
- **ARCH-003:** Browser-trusted identity is assigned outside the renderer.
- **ARCH-004:** Cross-profile objects never share writable state.
- **ARCH-005:** Site-isolation exceptions require an explicit equivalent-security proof and test.
- **ARCH-006:** Every queue crossing a process or trust boundary is bounded.
- **ARCH-007:** Every action against a document validates the current document epoch.
- **ARCH-008:** Secret material is never intentionally included in agent observations, logs, crash reports, or general telemetry.
- **ARCH-009:** Resource reclamation cannot silently change security policy.
- **ARCH-010:** Headless, automation, and agent modes use the same navigation, origin, storage, permission, and sandbox machinery as interactive mode.

<!-- MARKET-STRATEGY-2026-07 -->
## Proposed Space principal

`OP-001` researches whether a Space should become a first-class product, identity, resource, Plug-in, recovery, and agent-policy principal. No kernel or process identity changes until an RFC/ADR defines ownership, profile relationship, lifetime, IPC identity, cross-Space sharing, and compatibility behavior.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Browser-shell UI boundary

The product shell is split into toolkit-neutral Rust state/commands, a replaceable presentation adapter, platform services, and page-surface composition. The toolkit cannot own navigation, profile, permission, credential, agent, Plug-in, persistence, or update authority. Renderer and GPU surfaces use typed handles with document and device generations.

<!-- WP-002-KERNEL-IPC-2026-07 -->
## M0 generated control-plane reference

`WP-002` now has a dependency-free M0 policy reference generated from [`schemas/ipc/control-plane.json`](../../schemas/ipc/control-plane.json). The schema owns stable role, capability, and message IDs; default capability sets; process-launch authority; message route allowlists; document-scope rules; encoded-size limits; and queue budgets. `tools/generate_ipc.py --check` rejects source/generated drift.

`turing-types::ProcessIdentity` combines a stable process ID with a monotonic restart epoch. `turing-kernel::ProcessRegistry` is the deterministic authorization oracle for launch, capability attenuation, stale-process rejection, route validation, broker-only channel registration, endpoint binding, and exact sequence state. `turing-ipc` supplies bounded envelopes and explicit count/byte backpressure whose byte charge is frozen at admission.

This reference is not an operating-system launcher or transport. It does not yet authenticate platform peers, encode hostile wire bytes, transfer handles or shared memory, compose site instances, or prove sandbox containment. Platform implementations must match this policy and add independent negative evidence before `REQ-SEC-003` or `WP-002` can be considered complete.
