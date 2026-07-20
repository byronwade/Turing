# 22 — Research and Measurement Program

Turing's high-risk architectural choices must be tested against alternatives before they become irreversible. This document defines the initial research questions and required evidence.

The checked [research-question coverage audit](machine/research-question-coverage.json), [schema](machine/research-question-coverage.schema.json), and [validator](../../tools/validate_research_question_coverage.py) distinguish the 37 questions currently routed through the active readiness crosswalk from 29 questions explicitly deferred outside current pre-build closure lanes. Deferred status preserves each question, owner route, revisit trigger, and future evidence requirement; it does not answer or reject the question.

## RQ-01 — Can compact Rust data structures materially reduce engine memory?

Compare DOM, style, fragment, display-list, and protocol representations using generated and captured legal corpora. Measure live bytes, reserved bytes, pointer/metadata overhead, allocation count, construction, mutation, traversal, destruction, and cache behavior. Compare arena handles, intrusive indexes, reference counting, and alternative compact layouts. Include safety and implementation complexity. The [Memory Object Representation and Tab Lifecycle Research](../research/memory-object-representation-and-tab-lifecycle-research-2026-07.md) defines the deferred experiment and evidence handoff.

Decision output: accepted representations and size/performance budgets by object class.

## RQ-02 — What process topology gives the best isolation-adjusted memory?

Simulate and later measure per-site, per-browsing-context-group, and security-equivalent process pools. Vary 8/16/32 GiB systems, 5/15/30/100 tabs, iframe composition, workers, media, extensions, and agent hosts. Report security equivalence, process overhead, shared resources, crash blast radius, IPC latency, and revival. The [Process Topology and Isolation-Adjusted Memory Research](../research/process-topology-isolation-adjusted-memory-research-2026-07.md) defines the active no-claim experiment and evidence handoff.

Decision output: process assignment and pressure policy; never a cross-site coalescing shortcut.

## RQ-03 — How much memory can freezing reclaim without discard?

Instrument allocator pages, JS heap, DOM/style/layout/display list, images/fonts, network buffers, workers, and GPU resources before and after throttling/freeze. Test working-set trimming and safe cache dropping. Measure revival latency and semantic effects. The [Memory Object Representation and Tab Lifecycle Research](../research/memory-object-representation-and-tab-lifecycle-research-2026-07.md) defines the no-claim lifecycle, recovery, and user-protection evidence route.

Decision output: frozen-state budget and eligible resource-release contract.

## RQ-04 — Which UI stack meets latency, accessibility, and platform goals?

Prototype retained Rust scene graph with native adapters, selective native controls, and at least one alternative. Measure startup, key-to-paint, frame pacing, memory, text/IME, drag/drop, menus, screen readers, high contrast, and platform fidelity. Avoid evaluating only visual mockups.

Decision output: UI renderer and native-control policy.

## RQ-05 — Direct graphics APIs or a Rust GPU abstraction?

Prototype a basic compositor on Metal, D3D12, and Vulkan through direct adapters and a pinned abstraction such as wgpu. Measure binary/build complexity, startup, memory, command validation, device loss, driver coverage, debugging, performance, and ability to constrain the GPU process.

Decision output: backend abstraction boundary with replacement and security strategy.

## RQ-06 — Which text stack balances consistency and native behavior?

Compare platform-native shaping/rasterization, HarfBuzz/FreeType, and hybrid adapters across scripts, variable/color fonts, bidi, vertical text, IME, selection geometry, accessibility, screenshots, memory, and startup.

The [Text Shaping, Fonts, and Input Research](../research/text-shaping-fonts-and-input-research-2026-07.md) defines the deferred source-backed comparison, corpus, oracle, and measurement route.

Decision output: shaping/raster/fallback architecture per platform.

## RQ-07 — Register or stack bytecode for the interpreter?

Implement representative language kernels in both forms. Compare code size, dispatch, compile time, exception handling, debug mapping, stack maps, baseline JIT lowering, memory, and Test262 diagnostics. Do not use microbenchmarks alone.

The [JavaScript Bytecode Representation Research](../research/javascript-bytecode-representation-research-2026-07.md) defines the deferred source-backed comparison, semantic oracle, and evidence route.

Decision output: bytecode format v1 and versioning policy.

## RQ-08 — GC heap representation and DOM wrapper strategy

Prototype tracing roots, handles, wrapper maps, nursery/mature spaces, external memory, weak maps, finalization, and document teardown. Stress cycles between JS and DOM. Compare movable versus nonmoving mature spaces and handle-indirection costs.

The [JavaScript and DOM Wrapper Lifetime Research](../research/javascript-dom-wrapper-lifetime-research-2026-07.md) defines the deferred source-backed comparison, identity oracle, teardown, and memory-accounting route.

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

The [IPC Capability Boundary Inventory - July 2026](../research/ipc-capability-boundary-inventory-2026-07.md), [WP-002 kernel identity and IPC reference](../research/wp-002-kernel-ipc-2026-07.md), [TASK-000011 WP-002 Review Handoff](../research/task-000011-wp002-review-handoff-2026-07.md), and checked no-claim [TASK-000011 evidence capture](../agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json) are current `PB-011` planning, review-handoff, and non-accepting evidence-capture records for this question. They record current M0 bounded-envelope, oversized-message, typed-identity, role-capability, process-capability, generated-reference, source-commit artifact-binding, checked IPC schema-source template, and checked IPC readiness-review template evidence while keeping `TASK-000011` acceptance, accepted independent evidence-bundle completion, wire encoding, connection authentication, owner-reviewed IPC readiness, timeout/cancellation behavior, stale-epoch receiver proof on a real transport, malformed/reordered/wrong-principal transport tests, fuzz/model tests, renderer security, agent security, process isolation, site isolation, production IPC, and implementation outside the proof.

## RQ-14 — Storage engine and process model

Evaluate SQLite-backed and custom append/log approaches for cookies, history, bookmarks, session journal, IndexedDB metadata, and settings. Test transactions, concurrency, corruption, migrations, disk full, power loss, profile size, encryption boundary, and repair.

Decision output: store-specific backends and shared transaction/recovery policy.

## RQ-15 — Compatibility prioritization

Analyze WPT/Test262 taxonomy and a controlled application corpus to identify dependencies that unlock the greatest useful surface without embedding site-specific hacks. Track normative prerequisites and security interactions.

Decision output: milestone feature ordering and explicit unsupported map.

The [Servo local compatibility corpus and WPT/Test262 evidence report](../research/servo-local-compatibility-corpus-2026-07.md) is a first-pass denominator and corpus-planning input for this question; it is not a compatibility result.

## RQ-16 — Which competitive engine patterns survive equivalent measurement?

Use the [July 2026 engine landscape study](../research/browser-engine-landscape-2026-07.md) as the hypothesis source, then compare current stable Chromium, WebKit/Safari where available, Firefox/Gecko, and runnable Servo/Ladybird builds on fixed hardware and equivalent local corpora.

Measure startup, input-to-present latency, frame pacing, page stages, JavaScript warm-up, process topology, isolation state, memory categories, energy, recovery, compatibility, accessibility, and unsupported behavior. Distinguish observed architecture from inferred cause. Never attribute a benchmark difference to a design feature without a controlled experiment.

Decision output: an evidence-ranked list of architecture patterns to adopt, reject, or prototype, with confidence and revisit triggers.

## RQ-17 — What public developer protocol can lead on stability and observability?

Prototype WebDriver BiDi integration plus a schema-generated Turing engine-instrumentation protocol. Compare capability negotiation, versioning, generated clients, command/event latency, streaming, backpressure, cancellation, authentication, redaction, replay, malformed input, and support-window cost.

The [Public Developer Protocol Stability and Observability Research](../research/public-developer-protocol-stability-and-observability-research-2026-07.md) defines the deferred source-backed comparison and evidence route.

Evaluate common developer workflows across Chromium CDP, Firefox remote protocols, WebKit Inspector Protocol, and Turing's proposal without making another engine's protocol the internal source of truth.

Decision output: protocol layering, version policy, stable and experimental domains, client-generation plan, security boundary, and compatibility-adapter policy.

## RQ-18 — Which pipeline artifact and invalidation model is most correct, compact, and observable?

Prototype versioned parser output, DOM mutation epochs, computed-style blocks, layout fragments, paint chunks, display lists, accessibility snapshots, and compositor state. Compare mutable object graphs, immutable epoch artifacts, hybrid retention, and full-recomputation oracles across static, mutation-heavy, animation, editing, accessibility, and adversarial pages.

Measure bytes, allocations, rebuild scope, invalidation correctness, trace clarity, parallel publication, cancellation, and stale-artifact rejection.

The [Rendering Artifacts and Invalidation Research](../research/rendering-artifacts-and-invalidation-research-2026-07.md) defines the deferred source-backed comparison, oracle, and evidence route.

Decision output: engine artifact identity, lifetime, invalidation, retention, and diagnostic contracts.

## RQ-19 — Which runtime tiering and collector architecture gives the best interaction-adjusted performance?

Build a constrained but semantically precise interpreter, object/shape model, exact collector, baseline compiler, and optional simple mid-tier. Compare register/hybrid bytecode, compiler backend, code memory, warm-up, GC pause distribution, external-memory accounting, deoptimization, no-JIT mode, and end-to-end application interaction.

The [JavaScript Runtime Tiering and Collector Research](../research/javascript-runtime-tiering-and-collector-research-2026-07.md) defines the deferred source-backed comparison, semantic oracle, and measurement route.

Security, Test262 coverage, debugger fidelity, and platform W^X/signing evidence accompany every result.

Decision output: runtime tier responsibilities, GC baseline, code-generation boundary, and revisit trigger for a high-optimization tier.

## RQ-20 — What platform sandbox and broker design can be proven on macOS, Windows, and Linux?

Generate role-specific capability manifests and effective sandbox policies for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater processes. Compare App Sandbox/seatbelt and hardened runtime, AppContainer/tokens/jobs/mitigations, and namespaces/seccomp/Landlock/portals.

Run packaged-build negative tests for files, sockets, processes, debugging, devices, credentials, platform IPC, dynamic code, shared memory, and other profiles. Measure process launch, broker latency, compatibility, and policy complexity.

The [Sandbox Probe Inventory](../research/sandbox-probe-inventory-2026-07.md), checked [WP-003 Sandbox Probe Contract](../research/wp-003-sandbox-probe-plan-2026-07.md), checked no-claim [sandbox probe-package template](../security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json), checked no-claim [sandbox readiness-review template](../security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json), [`probe-catalog.json`](../../schemas/sandbox/probe-catalog.json), [`probe-evidence.schema.json`](../../schemas/sandbox/probe-evidence.schema.json), and [`validate_sandbox_contracts.py`](../../tools/validate_sandbox_contracts.py) are the current `PB-012` no-claim planning evidence for these targets, surfaces, operation catalog, evidence schema, platform artifacts, package handoff fields, readiness-review handoff fields, and blockers. They must be followed by packaged expected-deny execution beyond the template, unsandboxed control runs, unsupported platform primitive handling, application-level stub rejection, effective platform-policy capture, host-safe fixtures, and owner-reviewed sandbox readiness review beyond the checked no-claim sandbox readiness-review template before `RQ-20` can support sandbox or security-gate claims.

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

The [Window Input Accessibility Spike Inventory - July 2026](../research/window-input-accessibility-spike-inventory-2026-07.md) is the current checked no-claim `PB-015` handoff for windowing, input, IME, accessibility-tree, page-tree composition, clipboard, drag-drop, localization, zoom, contrast, motion, crash recovery, renderer hang, GPU-loss, platform assistive-technology rows, and evidence blockers. It does not provide manual assistive-technology transcripts, screen-reader coverage, page-tree proof, latency samples, accessibility readiness, `UI-GATE-7`, `UI-GATE-10`, or release-path UI approval.

## RQ-31 — Which reproducible-build, signing, update, migration, and incident process can meet browser emergency timelines?

Run clean rebuilds, provenance/SBOM verification, key-compromise drills, update tamper/replay/rollback tests, migration interruption, crash-report redaction, and emergency patch exercises. Decision output: release trust, packaging, update metadata, rollout, support lifecycle, and staffing gates.

## RQ-32 — Which extension, enterprise-policy, account, and sync subset is useful without recreating ambient authority and background waste?

Prototype isolated worlds/processes, optional host grants, event-driven lifetimes, rules, native messaging, policy precedence, encrypted sync, conflicts, quotas, and audit. Decision output: supported extension surface, policy schema, account boundary, sync envelope, and compatibility gaps.

## RQ-33 — Which open-web feature lifecycle best aligns user needs, standards, tests, privacy, accessibility, and compatibility?

Build dependency graphs from specifications, WPT, Interop, application needs, security controls, and platform work. Study experimental APIs, deprecation, and public compatibility interventions. Decision output: proposal checklist, maturity stages, experiment rules, and public dashboard.

## RQ-34 — Which fixed-hardware benchmark-laboratory design produces comparable, repeatable, decision-grade browser evidence?

Version machines, OS images, corpora, servers, power/thermal controls, adapters, raw result formats, statistics, and publication. Decision output: lab inventory, benchmark manifests, acceptance thresholds, regression policy, and claim-expiry rules.

The [Performance Benchmark Readiness Packet - July 2026](../research/performance-benchmark-readiness-packet-2026-07.md) and checked no-claim [benchmark readiness-review template](machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json) are the current `PB-013` handoff for this question. They keep the work at evidence-queue status until fixed hardware, corpus, runner, raw artifacts, pinned competitor versions, owner-reviewed result bundles, and owner-reviewed benchmark readiness review beyond the checked no-claim benchmark readiness-review template exist.
The [Chrome-Class Performance Runbook - July 2026](../research/chrome-class-performance-runbook-2026-07.md) is the current `PB13-EV-009` and `PB13-EV-010` handoff for competitor comparison controls, suite usage, no-claim manifest claim metadata, and claim-expiry policy. It does not provide a benchmark result or public performance claim.
The [Benchmark Hardware and OS Manifest - July 2026](../research/benchmark-hardware-os-manifest-2026-07.md) is the current `PB13-EV-001` and `PB13-EV-002` handoff for a checked Tier H current-host candidate. It does not provide a clean lab image, Tier L/Tier M denominator, benchmark result, or performance claim.
The [Benchmark OS and Update-Control Manifest - July 2026](../research/benchmark-os-update-control-manifest-2026-07.md) is the current `PB13-EV-002` handoff for current-host Windows update policy, Insider channel, service, driver, firmware, power, display, clock, and unsupported-control evidence. It does not provide a clean image, approved update freeze, driver freeze, thermal control, network isolation, benchmark result, or performance claim.
The [Semantic Resource Attribution Taxonomy - July 2026](../research/semantic-resource-attribution-taxonomy-2026-07.md) is the current `PB13-EV-011` handoff for checked semantic owner classes, metric names, shared-resource policy, collection-plan fields, and UI/reporting disclosures. It does not provide browser trace instrumentation, per-tab resource measurements, GPU accounting output, raw runner artifacts, UI fixtures, or a performance claim.
The [Benchmark Competitor Version Manifest - July 2026](../research/benchmark-competitor-version-manifest-2026-07.md) is the current `PB13-EV-009` handoff for official release-catalog candidate versions of Chrome Stable, Edge Stable, Firefox Stable, Safari Stable, and Safari Technology Preview. It does not provide local executable pins, binary hashes, profiles, settings, command lines, benchmark output, comparison evidence, or a performance claim.
The [Benchmark Competitor Local Install Inventory - July 2026](../research/benchmark-competitor-local-install-inventory-2026-07.md) is the current `PB13-EV-009` handoff for current Windows high-end host executable paths, hashes, signatures, and version-state caveats for Chrome and Edge. It does not provide owner-reviewed browser pins, channel proof, profiles, settings, command lines, Firefox/Safari local install evidence, benchmark output, comparison evidence, or a performance claim.
The [Benchmark Browser Pin Capture Contract - July 2026](../research/benchmark-browser-pin-capture-contract-2026-07.md) is the current `PB13-EV-005` and `PB13-EV-009` handoff for no-real-profile browser-reported version and settings capture. `tools/capture_benchmark_browser_pins.py --self-test` exercises the no-browser temp-profile, prohibited-path, and artifact-hash path only. The [Benchmark Browser Pin Local Diagnostic Capture - July 2026](../research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md) records current-host Chrome `Chrome/150.0.7871.115` and Edge `Edg/151.0.4129.21` diagnostic browser-reported versions from isolated temporary profiles. These artifacts do not provide owner-reviewed benchmark-ready pins, benchmark output, comparison evidence, or a performance claim.
The [Servo Performance Baseline Preparation - July 2026](../research/servo-performance-baseline-2026-07.md) is the current `ADR9-EV-014` source-strategy handoff. It records reference-host, artifact, command-surface, fixture-inventory, and run-record requirements only; it does not replace runner-generated raw performance, memory, energy, process, lifecycle, or failure-denominator evidence.
The no-claim benchmark manifest sample and `tools/validate_benchmark_manifests.py` provide schema-shape, current Tier H hardware-registry cross-check, current OS-control registry cross-check, resource-attribution registry cross-check, and no-claim claim-metadata evidence only; they do not replace runner-generated raw results or fixed-hardware measurements.
The no-claim corpus manifest, [Benchmark Corpus Expansion - July 2026](../research/benchmark-corpus-expansion-2026-07.md), and `tools/validate_benchmark_corpus.py` provide expanded generated local fixture contracts across static, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract shapes only; they do not replace a reviewed representative offline corpus.
The no-claim local static network profile, `tools/validate_benchmark_network_profile.py`, `tools/serve_benchmark_profile.py --self-test`, `tools/run_benchmark_server_profile.py --self-test`, and `tools/run_benchmark_smoke.py --self-test` provide a loopback HTTP/1.1 route, Host-header DNS behavior, cache contract, static-server self-test, checked runner-managed server lifecycle self-test, and hardware/OS-control/resource-attribution-linked smoke runner artifact package only; they do not replace browser-run server evidence, browser runs, TLS, HTTP/2, HTTP/3, proxy, authentication, or network-shaping evidence.

## RQ-35 — Which data-layout, allocator, virtual-memory, and reclamation strategies minimize sustained working set and latency?

Compare compact handles, field splitting, arrays, arenas, slabs, general allocators, page release, huge/guard pages, frozen-tab trimming, cache locality, and hardware tiers. The [Memory Object Representation and Tab Lifecycle Research](../research/memory-object-representation-and-tab-lifecycle-research-2026-07.md) defines the source-backed experiment matrix and rejection rules. Decision output: representation budgets, allocator classes, page policy, and unsafe boundaries.

## RQ-36 — Which IPC, shared-memory, serialization, copy, batching, and backpressure choices dominate isolation-adjusted performance?

Measure message sizes, copies, mappings, validation, cache coherency, priorities, batching delay, queue pressure, cancellation, crash cleanup, and semantic attribution. Decision output: domain encodings, shared-buffer contracts, queue budgets, and overload policy.

Use the [IPC Capability Boundary Inventory - July 2026](../research/ipc-capability-boundary-inventory-2026-07.md) as the current boundary inventory before measuring or implementing IPC performance choices. The inventory is not a performance, wire-format, schema-generator, or production IPC claim.

## RQ-37 — Which PGO, LTO, binary-layout, process-launch, and preinitialization techniques improve startup without harming reproducibility or memory?

Compare profiles, Thin/full LTO, function ordering, hot/cold splitting, demand paging, library layout, warm pools, preinitialized immutable state, and invalidation. Decision output: release profile, binary layout, startup architecture, and rollback triggers.

## RQ-38 — Which layered native, heap, JIT, and side-channel containment mechanisms produce the best security/performance frontier?

Compare process isolation, RLBox/Wasm-like compartments, heap cages, pointer tables, W^X, CFI/PAC/CET, timer policy, site isolation, and mitigations on equivalent workloads. Decision output: compartment strategy, threat assumptions, platform matrix, and residual risks.

## RQ-39 — Which deterministic replay and causal-observability model makes difficult browser bugs reproducible and explainable?

Prototype virtual time/random/network/input, state capture, trace causality, divergence detection, redaction, automatic reduction, source maps, and cross-domain policy explanations. Decision output: trace/replay schema, capture boundary, SDKs, and developer workflow targets.

The checked no-claim [Deterministic Replay and Causal Observability Research](../research/deterministic-replay-and-causal-observability-research-2026-07.md) expands the deferred route with replay alternatives, causal identity, privacy and authority boundaries, divergence oracles, overhead controls, and promotion rules. It does not select a replay runtime or trace format, prove deterministic replay, or establish a release diagnostic claim.

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

The [Technology and Dependency Decision Research](../research/technology-and-dependency-decision-research-2026-07.md) defines the deferred source-backed comparison for language safety, dependency resolution, provenance, unsafe/FFI and build-script boundaries, licensing, maintenance, reproducibility, replaceability, and rejection evidence. It does not select a technology or approve a dependency.

## RQ-42 — Native Plug-ins

Which capability/Wasm/WebExtensions architecture is safest and most useful?

## RQ-43 — Embedding contract

Which Rust/C/generated-SDK contract remains simple without freezing internals?

## RQ-44 — Servo relationship

Which clean, selective, upstream, derived, or charter-change option best serves Turing?

The [Servo unsafe and FFI contract review](../research/servo-unsafe-ffi-contract-review-2026-07.md) is the current first-pass evidence for `ADR9-EV-009` and `ADR9-EV-010`; it does not approve any unsafe block, C API, ABI contract, component boundary, source, dependency, or release code.
The [Servo component boundary and JavaScript conflict analysis](../research/servo-component-boundary-analysis-2026-07.md) is the current first-pass evidence for `ADR9-EV-011` and `ADR9-EV-012`; it does not approve a component boundary or supersede `ADR-0004`.
The [Servo local compatibility corpus and WPT/Test262 evidence report](../research/servo-local-compatibility-corpus-2026-07.md), checked [local compatibility corpus manifest](machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json), generated no-claim fixture root, HTTP route self-test, and checked [HTTPS host-alias harness plan](machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json) are the current first-pass evidence for `ADR9-EV-013`; they do not support a Servo, Turing, WPT/Test262 pass-rate, or Chrome-class compatibility claim.
The [Servo performance baseline preparation report](../research/servo-performance-baseline-2026-07.md) is the current first-pass evidence for `ADR9-EV-014`; it does not support a performance, memory, energy, or speed claim.
The [Servo security and maintenance implications report](../research/servo-security-maintenance-implications-2026-07.md) is the current first-pass evidence for `ADR9-EV-015` and `ADR9-EV-016`; it does not approve Servo sandboxing, security posture, release code, support obligations, or an upstream relationship.
The [ADR-0009 decision draft and public-claim impact template](../project-buildout/16-adr-0009-decision-draft.md) is the current first-pass evidence for `ADR9-EV-017`; it does not select an option, accept source, or approve public claims.

## RQ-45 — Project controls

Which ownership, review, traceability, phase, and evidence controls reduce defects without blocking work?

## RQ-46 — Reproducible environment

Which bootstrap, cache, linker, test runner, and host matrix is fast and maintainable?

Current `PB-008`/`PB-009` planning evidence starts with the checked [Build Information Readiness Ledger](../research/build-information-readiness-ledger-2026-07.md), [Fresh Host Reproduction Inventory](../research/fresh-host-reproduction-inventory-2026-07.md), checked run-record template, and checked no-claim [fresh-host readiness-review template](../project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json). It must become an independent toolchain/host run or owner-approved clean-VM equivalent with retained compiler, SDK, linker, Rust, Cargo, Git, shell, bootstrap, doctor, check, and `xtask` facts, exact OS, cache, target-directory, temp-directory, source-tree cleanliness, failure classification, rollback notes, and owner-reviewed toolchain/fresh-host readiness beyond the checked no-claim template before the research question can support reproducibility, `PB-008`/`PB-009` readiness, release confidence, preview, beta, stable, production, implementation, or Chrome-class claims.

## RQ-47 — Traceability at browser scale

Can requirement-to-evidence records remain accurate and useful?

The [Traceability at Browser Scale Research](../research/traceability-at-browser-scale-research-2026-07.md) defines the active source-backed route for typed bidirectional edges, status and freshness, change impact, generated views, orphan/stale detection, cross-boundary identity, and independent traceability audits. It does not prove coverage, implementation, verification, readiness, or support.

## RQ-48 — Capacity and sustainability

What staffing, funding, infrastructure, and support capacity is required at each maturity?

The [Capacity and Sustainability Research](../research/capacity-and-sustainability-research-2026-07.md) defines the active source-backed route for role coverage, review and incident bandwidth, infrastructure, support scope, SLO/error-budget controls, maturity promotion, and rejection evidence. It does not name staff, approve funding, set SLOs, or establish support capacity.

<!-- MARKET-STRATEGY-2026-07 -->
## Market differentiation research questions

## RQ-49 — Project-native Spaces

Does a project-native Space reduce resumption time, identity mistakes, and lost organization across longitudinal workflows?

## RQ-50 — Workspace Time Machine

What snapshot, retention, encryption, and restoration model provides useful recovery without unsafe replay or sensitive over-retention?

## RQ-51 — Resource Truth Center

Can users understand and safely control semantic resource attribution and lifecycle decisions under 30-tab pressure?

## RQ-52 — Trustworthy Agent Mode

Does isolated capability-scoped Agent Mode reduce harmful actions and improve trust without unusable confirmation burden?

## RQ-53 — Migration and open export

What migration and open-export coverage materially reduces browser switching cost while protecting credentials and profile integrity?

Current `PB-016` planning evidence starts with the checked [Profile Session Format Inventory](../research/profile-session-format-inventory-2026-07.md), checked no-claim [schema-package template](../storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json), and checked no-claim [readiness-review template](../storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json). It must become executable profile, Space, session, snapshot, and migration schemas beyond the schema-package template plus owner-reviewed profile/session readiness review beyond the readiness-review template with disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, data-loss, unsupported sync, credential-storage, real-profile migration, user-data handling, release-path, and production profile-format boundaries before the research question can support product or release claims.

## RQ-54 — Research, causality, receipts, sync, and collaboration

Do the Research Canvas, causal diagnostics, privacy receipts, selective sync, and collaboration improve task accuracy and continuity enough to justify their complexity?

Each study records cohort, task, comparator version, configuration, raw outcomes, accessibility, failures, confidence, and evidence that would reject the hypothesis.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## RQ-55 — Native UI framework selection

Which Slint, Vizia, Floem/GPUI, or alternative configuration gives the best complete browser-shell result across accessibility, page composition, startup, memory, binary, input latency, frame pacing, energy, development speed, licensing, maintenance, and replacement?

Current `PB-003` planning evidence starts with the checked [Toolkit-Neutral UI Adapter Contract Inventory](../research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md). It must become accepted `ADR-0013`, complete toolkit-neutral state, command, surface, accessibility, diagnostic, and adapter contracts, native adapter prototype evidence, no-toolkit-owned navigation/profile/permission/credential/agent/Plug-in/persistence/update authority negative tests, and owner review before this research question can support native-shell, trusted-chrome, accessibility, page-surface, toolkit-selection, or release-path UI approval.

Current `PB-004` planning evidence starts with the checked [Native UI Framework Bake-Off Inventory](../research/native-ui-framework-bakeoff-inventory-2026-07.md). It must become executable equivalent reference-shell adapter evidence for Slint, Vizia, and Floem or GPUI or owner-approved reduced scope, plus accepted `ADR-0014`, accessibility, IME, keyboard, crash, GPU-loss, startup, memory, binary, latency, frame-pacing, energy, license, dependency, provenance, replacement, package, runtime-exclusion, and owner-review evidence before this research question can support toolkit selection or release-path UI approval.

The checked no-claim [native UI readiness-review template](../ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json) now ties `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006` into one future review shape. It must become an owner-reviewed native UI readiness review beyond the template before any toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production claim, or implementation claim.

## RQ-56 — Browser page-surface composition

Should Turing own the window swapchain and compose toolkit chrome with page textures, use a stable toolkit custom-render hook, or use constrained platform child surfaces? Measure damage, scale, input, accessibility, capture, device loss, security, and portability.

Current `PB-005` planning evidence starts with the checked [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md). It must become executable `UI-GATE-7` evidence for typed page-surface handles, brokered surface handles, renderer-produced page frames, resize, scale, damage, input, IME, accessibility, occlusion, capture, renderer crash, GPU device loss, software fallback, latency, frame pacing, stale-handle negative tests, `ADR-0016`, compositor ownership, and owner review before the research question can support page-surface approval or toolkit selection.

## RQ-57 — React design workflow without a shipped React runtime

Can shared tokens, components, fixtures, and generated bindings provide React-speed design exploration while native components remain authoritative and drift is machine-detected? Compare against native live-preview workflows.

Current planning evidence starts with the checked [Native UI component fixture inventory](../research/native-ui-component-fixture-inventory-2026-07.md); rendered or adapter-specific fixtures remain unproven.

## RQ-58 — Pre-build readiness control

Does `PB-001` through `PB-020` prevent unresolved interfaces and operational claims from hardening prematurely without blocking useful contained prototypes?

Current `PB-020` planning evidence starts with the checked [Implementation Kickoff Review Inventory](../research/implementation-kickoff-review-inventory-2026-07.md), checked [Build Readiness Dependency Graph](../research/build-readiness-dependency-graph-inventory-2026-07.md), checked [Documentation Readiness Completion Audit](../research/documentation-readiness-completion-audit-2026-07.md), and checked no-claim [build-readiness closure-review template](../project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json). They must become owner-reviewed closure of remaining P0 source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, backup-ownership, owner-review, release-authority, task-dependency, decision-gate, documentation-completion, and build-readiness closure records before this research question can support broad M1 implementation, task approval, readiness promotion, preview, beta, stable, production, Chrome-class, performance, compatibility, security, accessibility, release, all-information-ready-for-building, or daily-driver claims.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## RQ-59 — Agent task and authority model

Which task decomposition, capability, provenance, and escalation design produces useful autonomous engineering without self-approval, scope drift, or hidden authority?

## RQ-60 — Independent verification for agent-generated browser code

Which combinations of separate agents, human review, conformance suites, fuzzing, formal/model tests, fixed-hardware measurement, and accessibility evaluation provide sufficiently independent evidence?

Current preparation starts with the active no-claim [Independent Verification for Agent-Generated Browser Code research packet](../research/independent-verification-for-agent-generated-code-research-2026-07.md), the agent task/provenance controls, and the independent-verification baseline. It must become task-scoped evidence with independent oracle and verifier identity, complete denominators, raw artifacts, negative and recovery cases, common-mode analysis, and reviewer disposition before it can support task acceptance, security, accessibility, performance, compatibility, release, production, or Chrome-class claims.

## RQ-61 — Stable-v1 scope and platform contract

What finite capability and support boundary provides meaningful daily use while remaining maintainable by the actual team?

Current preparation starts with the no-claim [Stable v1 Scope and Platform Contract research packet](../research/stable-v1-scope-and-platform-contract-research-2026-07.md), the targetless stable-scope registry, supported-platform matrix, and `PB-006` scorecard. It must become an owner-reviewed finite capability/support record with complete workflow denominators, platform and hardware scope, accessibility, security, compatibility, recovery, SLO, ownership, legal, update, incident, and support evidence before it can support stable scope, supported-platform, compatibility, accessibility, performance, production, or daily-driver claims.

## RQ-62 — Product SLOs and error budgets

Which numeric reliability, performance, energy, compatibility, accessibility, migration, update, and agent-safety targets predict a supportable stable browser?

Current preparation starts with the no-claim [Product SLOs and Error Budgets research packet](../research/product-slos-and-error-budgets-research-2026-07.md) and the targetless [production-readiness SLO catalog](../production-readiness/04-product-slos-and-error-budgets.md). It must become owner-approved user workflows, SLI definitions, denominators, fixed-platform baselines, raw evidence, privacy-preserving telemetry review, candidate target tradeoffs, and an owner-reviewed SLO/error-budget decision before it can support numeric release gates, support commitments, performance or reliability claims, accessibility or data-safety claims, update/migration claims, agent-safety claims, or stable readiness.

## RQ-63 — Update trust and compromise recovery

Which TUF-style role, key, delegation, threshold, expiration, rollback, and emergency-recovery architecture best fits Turing channels and platforms?

Current `PB-017` planning evidence starts with the checked [Research Package Update Lab Inventory](../research/research-package-update-lab-inventory-2026-07.md), checked no-claim [update-lab package template](../release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json), and checked no-claim [readiness-review template](../release-operations/machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json). It must become executable package manifests and update metadata parsers beyond the update-lab package template, no-production-key signature/threshold fixtures, tamper, replay, wrong-target, expiry, mirror, partial-write, disk-full, power-loss, rollback, vulnerable-version refusal, migration, downgrade, crash-loop, privacy-preserving event tests, and owner-reviewed package/update readiness beyond the readiness-review template before the research question can support update-trust, release-readiness, supported-security, production-updater, signing, stable-channel, public-distribution, or implementation claims.

## RQ-64 — Secure-development and provenance level

Which NIST SSDF, SP 800-218A, SLSA Source/Build, SBOM, review-attestation, and reproducibility controls are achievable and useful at each maturity?

Current preparation starts with the no-claim [Secure Development and Provenance Level research packet](../research/secure-development-and-provenance-level-research-2026-07.md). It must become a scope-specific, owner-reviewed maturity record with exact framework versions, source/dependency/generated-output identity, SBOM and advisory boundaries, provenance verification, independent replay or clean-host evidence, review/testing/vulnerability records, release/update controls, residual risk, and synchronized `ADR-0009`/`PB-002`/`PB-008`/`PB-009`/`PB-017`/`PB-018`/`PB-019`/`PB-020` decisions before it can support a secure-development, provenance, reproducibility, release-integrity, compliance, or production claim.

## RQ-65 — Service and offline architecture

Which optional services materially improve safety or continuity, and how should the browser degrade, export, self-host, or shut down without lock-in?

Current preparation starts with the no-claim [Service and Offline Architecture research packet](../research/service-and-offline-architecture-research-2026-07.md) and the targetless [Service Dependencies and Offline Behavior](../production-readiness/10-service-dependencies-and-offline-behavior.md) contract. It must become owner-reviewed service classifications, data and authority boundaries, offline/degraded workflow evidence, export/self-hosting/shutdown decisions, privacy and support terms, and synchronized profile, agent, update, incident, SLO, and `PB-020` records before it can support service, continuity, self-hosting, privacy, availability, production, or release claims.

## RQ-66 — Human release, legal, and incident capacity

What staffing, separation of duties, legal approval, signing ceremony, support term, on-call, and incident-rehearsal evidence is necessary before beta and stable?

Current preparation starts with the no-claim [Human Release, Legal, and Incident Capacity research packet](../research/human-release-legal-and-incident-capacity-research-2026-07.md), alongside the incident-response, backup-ownership, package/update, SLO, and production-readiness records. It must become a named, qualified, independently reviewed capacity and rehearsal record with support scope, separation of duties, legal boundaries, signing authority, on-call coverage, incident exercises, exceptions, and synchronized `PB-016` through `PB-020` evidence before it can support beta, stable, release, supported-security, legal, production, or implementation claims.

Current `PB-018` planning evidence starts with the checked [Incident Patch Rehearsal Inventory](../research/incident-patch-rehearsal-inventory-2026-07.md), checked no-claim [incident patch rehearsal template](../security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), and checked no-claim [incident/patch readiness-review template](../security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json). It must become executed private-intake tabletop records beyond the rehearsal template, emergency patch dry-run evidence, incident-class workflow exercises, timing/escalation/secret-rotation drills, role review, backup-owner coverage, coordinated disclosure rehearsal, and owner-reviewed incident/patch readiness beyond the readiness-review template before the research question can support incident-response readiness, emergency patch capacity, supported-security, stable-promotion, signing-authority, disclosure authority, incident-closure authority, implementation, or production-safe browsing claims.

Current `PB-019` blocked evidence starts with the checked [Backup Ownership Gap Inventory](../research/backup-ownership-gap-inventory-2026-07.md), checked no-claim [backup-owner qualification template](../project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json), and checked no-claim [backup-ownership readiness-review template](../project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json). It must become named qualified backup owners beyond the qualification template, role-level and subsystem-competence evidence, representative path coverage, review records, availability, succession, recusal, inactivity, removal, emergency replacement, CODEOWNERS and access reconciliation, two-person-control evidence, and owner-reviewed backup ownership readiness beyond the readiness-review template before this research question can support owner coverage, release authority, signing authority, update trust, supported-version changes, security-disclosure authority, legal approval, incident closure, production authority, broad readiness, or implementation claims.
