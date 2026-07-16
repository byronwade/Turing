# 22 — Research and Measurement Program

Turing's high-risk architectural choices must be tested against alternatives before they become irreversible. This document defines the initial research questions and required evidence.

## RQ-01 — Can compact Rust data structures materially reduce engine memory?

Compare DOM, style, fragment, display-list, and protocol representations using generated and captured legal corpora. Measure live bytes, reserved bytes, pointer/metadata overhead, allocation count, construction, mutation, traversal, destruction, and cache behavior. Compare arena handles, intrusive indexes, reference counting, and alternative compact layouts. Include safety and implementation complexity.

Decision output: accepted representations and size/performance budgets by object class.

## RQ-02 — What process topology gives the best isolation-adjusted memory?

Simulate and later measure per-site, per-browsing-context-group, and security-equivalent process pools. Vary 8/16/32 GiB systems, 5/15/30/100 tabs, iframe composition, workers, media, extensions, and agent hosts. Report security equivalence, process overhead, shared resources, crash blast radius, IPC latency, and revival.

Decision output: process assignment and pressure policy; never a cross-site coalescing shortcut.

## RQ-03 — How much memory can freezing reclaim without discard?

Instrument allocator pages, JS heap, DOM/style/layout/display list, images/fonts, network buffers, workers, and GPU resources before and after throttling/freeze. Test working-set trimming and safe cache dropping. Measure revival latency and semantic effects.

Decision output: frozen-state budget and eligible resource-release contract.

## RQ-04 — Which UI stack meets latency, accessibility, and platform goals?

Prototype retained Rust scene graph with native adapters, selective native controls, and at least one alternative. Measure startup, key-to-paint, frame pacing, memory, text/IME, drag/drop, menus, screen readers, high contrast, and platform fidelity. Avoid evaluating only visual mockups.

Decision output: UI renderer and native-control policy.

## RQ-05 — Direct graphics APIs or a Rust GPU abstraction?

Prototype a basic compositor on Metal, D3D12, and Vulkan through direct adapters and a pinned abstraction such as wgpu. Measure binary/build complexity, startup, memory, command validation, device loss, driver coverage, debugging, performance, and ability to constrain the GPU process.

Decision output: backend abstraction boundary with replacement and security strategy.

## RQ-06 — Which text stack balances consistency and native behavior?

Compare platform-native shaping/rasterization, HarfBuzz/FreeType, and hybrid adapters across scripts, variable/color fonts, bidi, vertical text, IME, selection geometry, accessibility, screenshots, memory, and startup.

Decision output: shaping/raster/fallback architecture per platform.

## RQ-07 — Register or stack bytecode for the interpreter?

Implement representative language kernels in both forms. Compare code size, dispatch, compile time, exception handling, debug mapping, stack maps, baseline JIT lowering, memory, and Test262 diagnostics. Do not use microbenchmarks alone.

Decision output: bytecode format v1 and versioning policy.

## RQ-08 — GC heap representation and DOM wrapper strategy

Prototype tracing roots, handles, wrapper maps, nursery/mature spaces, external memory, weak maps, finalization, and document teardown. Stress cycles between JS and DOM. Compare movable versus nonmoving mature spaces and handle-indirection costs.

Decision output: exact baseline collector and wrapper-lifetime contract.

## RQ-09 — Cranelift versus custom baseline code generation

After the interpreter is stable, compare backend integration, compilation latency, code quality, stack maps, deoptimization metadata, W^X support, platform signing, binary size, debugging, fuzzability, and maintenance.

Decision output: baseline JIT backend; optimizing-tier decision remains separate.

## RQ-10 — Semantic agent snapshots versus screenshot-first control

Evaluate task success, token size, latency, accessibility, stale-target rate, cross-origin leakage, hidden-content exposure, and prompt-injection resistance. Screenshots remain an optional labeled observation, not the assumed default.

Decision output: semantic snapshot schema and when vision is permitted.

## RQ-11 — Deterministic policy usability

Test grant/confirmation designs with low-, medium-, and high-impact tasks. Measure comprehension, approval mistakes, habituation, interruptions, cancellation, and audit usefulness. Include keyboard and screen-reader users.

Decision output: risk classifier, confirmation batching limits, and trusted UI.

## RQ-12 — Local model resource envelope

Measure model load time, resident/working memory, KV cache, accelerator allocation, energy, thermal effects, quality, token throughput, unload latency, and interaction with 30-tab workloads across hardware tiers.

Decision output: default local model size classes, on-demand policy, and disabled baseline.

## RQ-13 — Protocol encoding

Compare generated bounded binary formats and compact structured formats for IPC, traces, DevTools, and agents. Measure encode/decode, allocations, zero-copy safety, schema evolution, fuzzability, diagnostics, language clients, and malformed-input behavior.

Decision output: one or more domain-specific encodings with consistent identity/limit conventions.

## RQ-14 — Storage engine and process model

Evaluate SQLite-backed and custom append/log approaches for cookies, history, bookmarks, session journal, IndexedDB metadata, and settings. Test transactions, concurrency, corruption, migrations, disk full, power loss, profile size, encryption boundary, and repair.

Decision output: store-specific backends and shared transaction/recovery policy.

## RQ-15 — Compatibility prioritization

Analyze WPT/Test262 taxonomy and a controlled application corpus to identify dependencies that unlock the greatest useful surface without embedding site-specific hacks. Track normative prerequisites and security interactions.

Decision output: milestone feature ordering and explicit unsupported map.

## RQ-16 — Which competitive engine patterns survive equivalent measurement?

Use the [July 2026 engine landscape study](../research/browser-engine-landscape-2026-07.md) as the hypothesis source, then compare current stable Chromium, WebKit/Safari where available, Firefox/Gecko, and runnable Servo/Ladybird builds on fixed hardware and equivalent local corpora.

Measure startup, input-to-present latency, frame pacing, page stages, JavaScript warm-up, process topology, isolation state, memory categories, energy, recovery, compatibility, accessibility, and unsupported behavior. Distinguish observed architecture from inferred cause. Never attribute a benchmark difference to a design feature without a controlled experiment.

Decision output: an evidence-ranked list of architecture patterns to adopt, reject, or prototype, with confidence and revisit triggers.

## RQ-17 — What public developer protocol can lead on stability and observability?

Prototype WebDriver BiDi integration plus a schema-generated Turing engine-instrumentation protocol. Compare capability negotiation, versioning, generated clients, command/event latency, streaming, backpressure, cancellation, authentication, redaction, replay, malformed input, and support-window cost.

Evaluate common developer workflows across Chromium CDP, Firefox remote protocols, WebKit Inspector Protocol, and Turing's proposal without making another engine's protocol the internal source of truth.

Decision output: protocol layering, version policy, stable and experimental domains, client-generation plan, security boundary, and compatibility-adapter policy.

## RQ-18 — Which pipeline artifact and invalidation model is most correct, compact, and observable?

Prototype versioned parser output, DOM mutation epochs, computed-style blocks, layout fragments, paint chunks, display lists, accessibility snapshots, and compositor state. Compare mutable object graphs, immutable epoch artifacts, hybrid retention, and full-recomputation oracles across static, mutation-heavy, animation, editing, accessibility, and adversarial pages.

Measure bytes, allocations, rebuild scope, invalidation correctness, trace clarity, parallel publication, cancellation, and stale-artifact rejection.

Decision output: engine artifact identity, lifetime, invalidation, retention, and diagnostic contracts.

## RQ-19 — Which runtime tiering and collector architecture gives the best interaction-adjusted performance?

Build a constrained but semantically precise interpreter, object/shape model, exact collector, baseline compiler, and optional simple mid-tier. Compare register/hybrid bytecode, compiler backend, code memory, warm-up, GC pause distribution, external-memory accounting, deoptimization, no-JIT mode, and end-to-end application interaction.

Security, Test262 coverage, debugger fidelity, and platform W^X/signing evidence accompany every result.

Decision output: runtime tier responsibilities, GC baseline, code-generation boundary, and revisit trigger for a high-optimization tier.

## RQ-20 — What platform sandbox and broker design can be proven on macOS, Windows, and Linux?

Generate role-specific capability manifests and effective sandbox policies for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater processes. Compare App Sandbox/seatbelt and hardened runtime, AppContainer/tokens/jobs/mitigations, and namespaces/seccomp/Landlock/portals.

Run packaged-build negative tests for files, sockets, processes, debugging, devices, credentials, platform IPC, dynamic code, shared memory, and other profiles. Measure process launch, broker latency, compatibility, and policy complexity.

Decision output: supported platform/process matrix, broker interfaces, effective evidence format, degraded/unsupported modes, and SEC-GATE-1 criteria.

## RQ-21 — Which developer workflows and protocol surfaces create measurable leadership?

Measure time, errors, required steps, protocol round trips, data volume, accessibility, and success for cascade diagnosis, forced-layout analysis, input latency, memory retainers, network/security policy failure, worker debugging, crash reduction, cross-origin automation, and trace comparison.

Compare WebDriver BiDi, CDP, Firefox remote protocols, WebKit Inspector Protocol where accessible, and the proposed Turing protocol. Domain count alone is not a success metric.

Decision output: stable Turing protocol domains, UI workflow priorities, compatibility adapters, trace schema, and support-window budget.

## RQ-22 — Which API conventions minimize misuse and long-term compatibility cost?

Prototype schema-generated internal/public APIs with typed identity, capability discovery, structured errors, deadlines, cancellation, streaming, backpressure, idempotency, partial failure, authentication, authorization, redaction, and Rust/TypeScript/Python clients.

Measure malformed-input safety, allocation and latency, generated-code quality, developer comprehension, cross-version compatibility, and deprecation cost.

Decision output: common API conventions, schema language/encoding, error taxonomy, versioning model, SDK targets, and prohibited generic interfaces.

## RQ-23 — Which scheduling, memory, cache, and energy policies dominate sustained browser performance?

Compare critical-path/deadline scheduling, serial/fixed/work-stealing/adaptive parallelism, semantic memory ownership, arena/slab/general allocation, cache admission/eviction, pressure escalation, warm process pools, and lifecycle reclamation across Tier L/M/H.

Measure p50/p95/p99 input, frame pacing, startup, 30-tab mixed/all-live, allocator live/reserved/resident state, GPU, swap, wakeups, energy, thermal degradation, recovery, and compatibility.

Decision output: scheduler, pool, allocation, cache, pressure, startup, and benchmark-governance policies.

## RQ-24 — Which agent observation, action, memory, provider, and tool design is safest and most useful?

Compare semantic and vision observations, redaction strategies, opaque credential/file handles, action schemas, risk classification, confirmation, working/long-term memory, multi-agent delegation, recovery, local/remote providers, MCP/tool gateways, and resource budgets.

Report task success separately from unauthorized action, secret/cross-origin leakage, stale-target behavior, user comprehension, accessibility, cancellation, audit, tokens, cost, RAM/VRAM, CPU/GPU, energy, and 30-tab impact.

Decision output: observation schema, provider/tool manifest, memory policy, action/risk/confirmation model, MCP boundary, resource classes, and release evaluation corpus.

## RQ-25 — Which product and open-source practices can sustain a number-one claim?

Study current engine projects and browser products for governance, contributor onboarding, subsystem ownership, review latency, standards/test contributions, security response, release continuity, product workflows, privacy communication, tab/workspace design, accessibility, and support lifecycle.

A number-one claim must be defined as a current multi-dimensional scorecard rather than a synthetic benchmark. Track how quickly evidence and product status become stale.

Decision output: competitive scorecard, adopt/adapt/reject/defer ledger, contributor and security-response targets, product research cadence, and claim-expiry rules.

## RQ-26 — Which network process, Fetch-policy, cache, cookie, and transport architecture is fastest without widening authority?

Prototype kernel-issued request context, a brokered network process, DNS/proxy/TLS/HTTP variants, redirect and Fetch policy, partitioned caches/cookies, streaming, fault injection, and fixed-hardware resource attribution. Decision output: network-service boundaries, protocol stack, policy core, partition keys, budgets, diagnostics, and support matrix.

## RQ-27 — Which storage architecture survives crashes, migrations, corruption, disk pressure, and clearing correctly?

Compare SQLite-backed, log-structured, and store-specific designs for IndexedDB, Cache Storage, service workers, history, bookmarks, settings, sessions, and quotas. Decision output: store backends, transaction/durability levels, migration and recovery policy, encryption boundaries, and repair tools.

## RQ-28 — Which media, codec, DRM, PDF, and printing architecture balances compatibility, containment, energy, and licensing?

Measure decoder processes, software/hardware paths, playback clocks, WebRTC/capture, PDF and print pipelines, malformed inputs, licenses, and unsupported proprietary services. Decision output: process/codec matrix, protected-content boundary, document viewer, printing path, and distribution policy.

## RQ-29 — Which native browser-shell and platform-adapter architecture meets latency, accessibility, containment, and support goals?

Prototype retained browser chrome plus macOS, Windows, and Linux adapters. Measure startup, input/IME, window/surface lifecycle, accessibility, credential/device portals, packaging, power, and sandbox evidence. Decision output: UI scene graph, adapter APIs, native-control policy, and supported platform matrix.

## RQ-30 — Which accessibility architecture minimizes stale semantics and assistive-technology latency across processes?

Prototype semantic epochs, remote frame trees, platform bridges, text ranges, browser UI, DevTools, automation, and agent snapshots. Decision output: tree schema, process composition, event/coalescing policy, platform mappings, latency budgets, and release matrix.

## RQ-31 — Which reproducible-build, signing, update, migration, and incident process can meet browser emergency timelines?

Run clean rebuilds, provenance/SBOM verification, key-compromise drills, update tamper/replay/rollback tests, migration interruption, crash-report redaction, and emergency patch exercises. Decision output: release trust, packaging, update metadata, rollout, support lifecycle, and staffing gates.

## RQ-32 — Which extension, enterprise-policy, account, and sync subset is useful without recreating ambient authority and background waste?

Prototype isolated worlds/processes, optional host grants, event-driven lifetimes, rules, native messaging, policy precedence, encrypted sync, conflicts, quotas, and audit. Decision output: supported extension surface, policy schema, account boundary, sync envelope, and compatibility gaps.

## RQ-33 — Which open-web feature lifecycle best aligns user needs, standards, tests, privacy, accessibility, and compatibility?

Build dependency graphs from specifications, WPT, Interop, application needs, security controls, and platform work. Study experimental APIs, deprecation, and public compatibility interventions. Decision output: proposal checklist, maturity stages, experiment rules, and public dashboard.

## RQ-34 — Which fixed-hardware benchmark-laboratory design produces comparable, repeatable, decision-grade browser evidence?

Version machines, OS images, corpora, servers, power/thermal controls, adapters, raw result formats, statistics, and publication. Decision output: lab inventory, benchmark manifests, acceptance thresholds, regression policy, and claim-expiry rules.

## RQ-35 — Which data-layout, allocator, virtual-memory, and reclamation strategies minimize sustained working set and latency?

Compare compact handles, field splitting, arrays, arenas, slabs, general allocators, page release, huge/guard pages, frozen-tab trimming, cache locality, and hardware tiers. Decision output: representation budgets, allocator classes, page policy, and unsafe boundaries.

## RQ-36 — Which IPC, shared-memory, serialization, copy, batching, and backpressure choices dominate isolation-adjusted performance?

Measure message sizes, copies, mappings, validation, cache coherency, priorities, batching delay, queue pressure, cancellation, crash cleanup, and semantic attribution. Decision output: domain encodings, shared-buffer contracts, queue budgets, and overload policy.

## RQ-37 — Which PGO, LTO, binary-layout, process-launch, and preinitialization techniques improve startup without harming reproducibility or memory?

Compare profiles, Thin/full LTO, function ordering, hot/cold splitting, demand paging, library layout, warm pools, preinitialized immutable state, and invalidation. Decision output: release profile, binary layout, startup architecture, and rollback triggers.

## RQ-38 — Which layered native, heap, JIT, and side-channel containment mechanisms produce the best security/performance frontier?

Compare process isolation, RLBox/Wasm-like compartments, heap cages, pointer tables, W^X, CFI/PAC/CET, timer policy, site isolation, and mitigations on equivalent workloads. Decision output: compartment strategy, threat assumptions, platform matrix, and residual risks.

## RQ-39 — Which deterministic replay and causal-observability model makes difficult browser bugs reproducible and explainable?

Prototype virtual time/random/network/input, state capture, trace causality, divergence detection, redaction, automatic reduction, source maps, and cross-domain policy explanations. Decision output: trace/replay schema, capture boundary, SDKs, and developer workflow targets.

## RQ-40 — Which anti-phishing, trusted-UI, resource-management, recovery, onboarding, and everyday workflows create measurable user leadership?

Study origin comprehension, IDN/lookalikes, reputation privacy, prompts, credentials, agent confirmation, tab/workspace pressure, migration, safe mode, updates, support, keyboard, screen-reader, and recovery tasks. Decision output: trusted UI, reputation approach, resource manager, workflow priorities, and usability gates.

## Research protocol

Every study publishes:

- question and decision owner;
- hypotheses and alternatives;
- prototype commits;
- hardware/software environment;
- corpora and workloads;
- correctness/conformance baseline;
- security/accessibility considerations;
- raw samples and analysis method;
- limitations and failed approaches;
- recommendation, confidence, and revisit trigger.

A benchmark result cannot decide a security boundary alone. A decision that affects open-web semantics also requires conformance evidence. Findings that do not reproduce remain exploratory.

## RQ-41 — Technology and dependency set

Which languages, frameworks, and foundations minimize total security, performance, build, license, and maintenance cost?

## RQ-42 — Native Plug-ins

Which capability/Wasm/WebExtensions architecture is safest and most useful?

## RQ-43 — Embedding contract

Which Rust/C/generated-SDK contract remains simple without freezing internals?

## RQ-44 — Servo relationship

Which clean, selective, upstream, derived, or charter-change option best serves Turing?

## RQ-45 — Project controls

Which ownership, review, traceability, phase, and evidence controls reduce defects without blocking work?

## RQ-46 — Reproducible environment

Which bootstrap, cache, linker, test runner, and host matrix is fast and maintainable?

## RQ-47 — Traceability at browser scale

Can requirement-to-evidence records remain accurate and useful?

## RQ-48 — Capacity and sustainability

What staffing, funding, infrastructure, and support capacity is required at each maturity?

<!-- MARKET-STRATEGY-2026-07 -->
## Market differentiation research questions

- **RQ-45:** Does a project-native Space reduce resumption time, identity mistakes, and lost organization across longitudinal workflows?
- **RQ-46:** What snapshot, retention, encryption, and restoration model provides useful Time Machine recovery without unsafe replay or sensitive over-retention?
- **RQ-47:** Can users understand and safely control semantic resource attribution and lifecycle decisions under 30-tab pressure?
- **RQ-48:** Does isolated capability-scoped Agent Mode reduce harmful actions and improve trust without unusable confirmation burden?
- **RQ-49:** What migration and open-export coverage materially reduces browser switching cost while protecting credentials and profile integrity?
- **RQ-50:** Do the Research Canvas, causal diagnostics, privacy receipts, selective sync, and collaboration improve task accuracy and continuity enough to justify their complexity?

Each study records cohort, task, comparator version, configuration, raw outcomes, accessibility, failures, confidence, and evidence that would reject the hypothesis.
