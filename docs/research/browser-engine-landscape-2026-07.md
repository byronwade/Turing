# Browser Engine Landscape and Turing Excellence Strategy — July 2026

Status: research baseline; not an implementation claim  
Date: 2026-07-16  
Owner: research and architecture  
Scope: engine architecture, JavaScript runtime, developer APIs, open-web principles, performance, everyday-user quality, and open-source execution  
Confidence: high on documented architectural patterns; medium on comparative performance until fixed-hardware measurements exist

## 1. Question

What should Turing learn from the strongest current browser engines and independent-engine projects so it can pursue a credible number-one position for developers and everyday users without embedding an existing engine or making unsupported performance claims?

## 2. Executive conclusion

There is no defensible single “best browser engine” across compatibility, latency, memory, energy, security, developer tooling, platform integration, accessibility, and maintainability.

The useful reference leaders are different by dimension:

- Chromium/Blink/V8 is the reference for compatibility breadth, production-scale multiprocess rendering, mature instrumentation, and developer-tool ecosystem.
- WebKit/JavaScriptCore is a reference for a compact multiprocess product boundary, platform integration, brokered privileged access, and a mature tiered runtime.
- Gecko/SpiderMonkey is a reference for an independent standards engine, explicit process specialization, rich memory/performance tooling, and observable runtime internals.
- Servo is the closest architectural reference for a Rust-first, modular, embeddable engine with research roots in safe concurrency.
- Ladybird is the closest current reference for a greenfield, independent, from-scratch engine pursuing a full browser while keeping the project openly inspectable.

Turing should not copy one of these designs wholesale. The strongest strategy is a measured synthesis:

1. a capability-separated process kernel with site isolation and specialized utility processes;
2. immutable or versioned pipeline artifacts with explicit invalidation and ownership;
3. compositor and input paths that remain responsive when page script is busy;
4. adaptive parallelism that activates only when workload size and hardware justify its overhead;
5. an interpreter-first JavaScript runtime that grows through a fast baseline tier, a simple mid-tier, and an optimizing tier only after equivalence and security gates;
6. WebDriver BiDi for standards-facing automation plus a stable, schema-generated Turing protocol for deep engine introspection;
7. first-class resource, scheduling, invalidation, GC, JIT, network, storage, and security observability;
8. WPT- and standards-first development guided by user needs, safety, privacy, compatibility, and trusted UI;
9. public benchmark manifests, raw results, unsupported-feature maps, and open governance.

“Number one” must mean a reproducible multi-dimensional result, not one benchmark score.

## 3. Method and limitations

This study reviewed official architecture documentation, source repositories, standards documents, test-suite documentation, current project status pages, and official benchmark documentation. Sources were retrieved on 2026-07-16 unless another revision date is stated.

The checked no-claim [browser-engine landscape source manifest](machine/browser-engine-landscape-source-manifest.json), its [schema](machine/browser-engine-landscape-source-manifest.schema.json), and [`validate_browser_engine_landscape_sources.py`](../../tools/validate_browser_engine_landscape_sources.py) preserve the source identities and evidence axes used by this study. They improve provenance and freshness tracking only; they do not select an engine, authorize source use, or establish a comparative result.

This is an architectural comparison, not a fixed-hardware benchmark. It does not rank current engines by unmeasured memory, speed, battery life, security incidence, or total compatibility. Product performance varies by operating system, workload, build flags, process topology, extensions, power mode, and tab lifecycle.

No source code from another engine is proposed for copying. Established engines remain differential-test and interoperability references. Normative behavior comes from standards and tests.

## 4. What “number one” means

Turing should claim leadership only when it is on or near the Pareto frontier across all release-critical dimensions.

| Dimension | Required evidence |
|---|---|
| Open-web compatibility | Pinned WPT results with the full denominator, Test262 by feature and tier, Interop focus areas, real-application corpus, failures and exclusions |
| Interaction responsiveness | Cold/warm startup, address-field readiness, input-to-present p50/p95/p99, long-task attribution, frame pacing at multiple refresh rates |
| Memory efficiency | Physical and charged memory, allocator reserve, GPU allocation, process count, site isolation, tab states, revival latency, and state loss |
| Energy efficiency | CPU package energy, GPU activity, wakeups, idle behavior, video, scrolling, background workers, and thermal throttling |
| JavaScript and WebAssembly | Representative applications plus JetStream diagnostics, parse/compile latency, code size, GC pauses, tier state, and correctness coverage |
| Rendering and graphics | Real page corpus plus MotionMark diagnostics, raster/composite costs, layer churn, high-refresh pacing, and software fallback |
| Developer API | Protocol coverage, stability window, generated clients, command/event latency, cancellation, backpressure, replay, and migration cost |
| Observability | Explainable scheduling, invalidation, memory retention, GC/JIT decisions, process topology, network/storage provenance, and security-policy results |
| Security and privacy | Sandbox negative tests, site-isolation tests, capability review, fuzzing, update integrity, vulnerability-response capacity, and data minimization |
| Accessibility | Browser UI and web-content semantics, keyboard paths, platform assistive technologies, zoom/contrast/motion, and latency under load |
| Stability and recovery | Crash/hang/data-loss rates, tab and session recovery, process restart, GPU/device loss, storage fault injection, update rollback |
| Open-source health | Reproducible builds, transparent roadmap, decision records, review latency, contributor onboarding, issue closure, security process, and release continuity |

A result is invalid if Turing uses a smaller supported feature set, weaker security settings, hidden tab discarding, unmatched caches, different page activity, or omitted failures.

## 5. Reference-engine findings

### 5.1 Chromium, Blink, V8, and the Chrome developer ecosystem

Observed strengths:

- RenderingNG documents a staged pipeline spanning animation, style, layout, prepaint, scrolling, paint, commit, layerization, raster, activation, aggregation, and drawing.
- Layout produces an immutable fragment tree, while later stages transform that output into display lists and compositor work.
- Chromium separates browser, renderer, and Viz/GPU responsibilities and uses a compositor thread so selected scrolling and animation work can progress independently from the renderer main thread.
- Site isolation and a multiprocess model are treated as security, stability, and performance architecture rather than optional product features.
- Chrome DevTools Protocol provides a broad domain model and generated protocol descriptions used by a large tooling ecosystem.
- V8 demonstrates the value of multiple execution tiers: an interpreter, a very fast baseline compiler, a fast mid-tier compiler, and a high-optimization tier.

Lessons for Turing:

- Keep the rendering pipeline explicit and expose transitions, invalidation, queueing, and ownership.
- Make fragment, paint, and compositor artifacts immutable or epoch-versioned where practical.
- Preserve a low-latency compositor/input path outside page-script execution.
- Treat process assignment and site isolation as first-class scheduling inputs.
- Build schema-generated developer protocols from engine truth.
- Separate stable protocol versions from rapidly changing experimental domains.
- Use fast compilation tiers to improve interactive workloads before investing in expensive peak optimization.

Do not copy blindly:

- Chromium’s accumulated complexity, process count, compatibility obligations, and API history are not a suitable starting footprint for a new engine.
- CDP tip-of-tree is explicitly unstable. Turing should learn from its breadth while offering stronger version negotiation and support windows.
- Benchmark-specific V8 optimizations are not a substitute for end-to-end browser responsiveness, memory, and energy evidence.

### 5.2 WebKit and JavaScriptCore

Observed strengths:

- WebKit2 separates the UI process, sandboxed web-content processes, and a shared network/storage process.
- Privileged file, clipboard, camera, microphone, and related operations are brokered through more trusted processes rather than granted directly to web content.
- WebKit’s site-isolation design uses remote-frame and browsing-context-group concepts, cross-process synchronization, provisional navigation, and extensive layout-test infrastructure.
- JavaScriptCore uses tiered execution, from a low-level interpreter through baseline and optimizing tiers.
- WebKit’s official documentation connects architecture, testing, ports, and platform integration.

Lessons for Turing:

- Keep browser chrome independent from web-content rendering.
- Use narrow brokers for privileged platform capabilities.
- Model remote frames and cross-process documents as explicit identities, not transparent pointers.
- Design platform adapters as replaceable boundaries while keeping engine semantics common.
- Make site-isolation testing a mode of the general engine test corpus rather than a separate demo suite.

Do not copy blindly:

- Platform-specific product optimization can create behavior divergence if common engine contracts are weak.
- Site-isolation maturity must be measured feature by feature; documentation dated January 2025 described continuing functionality and performance work.
- A small process count is not automatically better if it expands privilege or cross-site blast radius.

### 5.3 Gecko and SpiderMonkey

Observed strengths:

- Firefox documents specialized parent, web-content, GPU, socket, media-decoder, service-worker, inference, and other process roles.
- It distinguishes ordinary shared content processes from per-site isolation and specialized execution environments.
- Separate service-worker execution is used to avoid blocking unrelated main-thread work.
- Firefox exposes detailed memory, profiling, power, heap, allocation, and process tools.
- SpiderMonkey documents lazy parsing, object shapes, bytecode interpretation, baseline compilation, optimizing compilation, garbage collection, and WebAssembly as distinct systems.
- Firefox supports WebDriver BiDi alongside its own remote-control infrastructure.

Lessons for Turing:

- Specialize processes when privilege, failure mode, memory pressure, or scheduling behavior materially differs.
- Measure process-launch overhead and evaluate platform-specific launch acceleration without weakening isolation.
- Make memory analysis and power analysis product capabilities, not only developer builds.
- Use lazy creation and parsing for cold code and rare metadata.
- Give service workers, local inference, decoders, and other background workloads explicit budgets and process policies.
- Expose runtime tiering, deoptimization, heap retention, and task attribution through stable developer tools.

Do not copy blindly:

- More specialized processes add coordination and memory overhead; every role needs a measured justification.
- Existing remote protocols contain historical compatibility constraints. Turing should define a cleaner internal protocol and implement standards-facing compatibility deliberately.

### 5.4 Servo

Observed strengths:

- Servo is a Rust-based, modular, embeddable engine that explicitly targets memory safety, concurrency, and lightweight integration.
- Its current project goals emphasize stable APIs, user interaction, performance, standards, and community growth.
- Governance under Linux Foundation Europe and an open technical steering structure provides an independent project model.
- Servo continues to publish current embedding, layout, DevTools, and release progress.

Lessons for Turing:

- Rust is viable for core engine architecture, but performance must come from data representation, scheduling, and ownership—not language choice alone.
- Engine components should be independently testable and reusable behind stable interfaces.
- Embedding APIs are a product surface and need lifecycle, threading, security, and versioning contracts.
- Open governance, standards participation, and upstream tests are strategic engineering work.

Do not copy blindly:

- Parallelism is not automatically faster. Task creation, synchronization, cache locality, and small workloads can make parallel execution worse.
- Embeddability and a full consumer browser impose different UI, compatibility, update, security-response, and support obligations.
- Current project progress is evidence of feasibility, not proof of Turing’s eventual performance.

### 5.5 Ladybird

Observed strengths:

- Ladybird explicitly pursues an independent engine rather than a Chromium/WebKit/Gecko wrapper.
- Its current architecture uses separate UI, renderer, image-decoder, and request-server processes, with sandboxing for renderer processes.
- The project publicly reports ongoing work in sandboxing, GPU isolation, out-of-process compositing, asynchronous scrolling, WebAssembly JIT, off-thread compilation, and parser work.
- Its code and roadmap provide a useful comparison for greenfield sequencing and contributor-visible progress.

Lessons for Turing:

- A from-scratch engine can expose progress honestly through feature work, tests, monthly reports, and a visible architecture.
- Security boundaries and compositor work must start before compatibility breadth makes retrofits prohibitive.
- Parser, runtime, graphics, and platform work can advance in parallel only with clear subsystem contracts.
- Independent implementation should still rely on reviewed third-party libraries for specialized foundations.

Do not copy blindly:

- Ladybird’s official repository describes the project as pre-alpha. It is not a production security or compatibility baseline.
- Fast visible progress can bias a project toward breadth before conformance, accessibility, memory, and incident operations are ready.
- Turing’s Rust-first policy and agent-security model create different design constraints.

## 6. Cross-engine architecture recommendations

These are research recommendations, not accepted ADRs.

### ENGINE-P-001 — Capability-separated kernel

Every process, worker, extension, developer tool, and agent receives an explicit identity and bounded capabilities. Renderers do not hold unrestricted sockets, files, devices, credentials, clipboard, or browser-internal authority.

### ENGINE-P-002 — Versioned pipeline artifacts

Parser output, DOM epochs, computed style, layout fragments, paint chunks, display lists, accessibility snapshots, and compositor state use stable identities and explicit versions. Consumers validate the epoch before using an artifact.

### ENGINE-P-003 — Demand-driven invalidation

The engine records why work was invalidated, the smallest safe invalidation root, and the cost of recomputation. Full recomputation remains a correctness oracle for incremental paths.

### ENGINE-P-004 — Responsive compositor and input path

Scrolling, compositor-only animations, hit-test state, and frame submission should avoid page-main-thread dependency where semantics permit. Main-thread dependencies are visible in DevTools.

### ENGINE-P-005 — Adaptive parallelism

Parallel execution is selected from workload size, dependency graph, hardware, foreground deadline, memory pressure, and measured overhead. Small tasks remain serial when parallel startup and synchronization would cost more.

### ENGINE-P-006 — Semantic resource ownership

CPU, memory, GPU, network, disk, wakeups, and model costs are charged to documents, frames, workers, extensions, agents, browser UI, and shared services. Shared resources report both physical and charged totals.

### ENGINE-P-007 — Tiered JavaScript with a stable oracle

The interpreter is the semantic oracle. A fast baseline compiler should arrive before a complex optimizer. A simple mid-tier may target interactive application code. Every tier supports differential execution, deoptimization, precise stack maps, and a no-JIT mode.

### ENGINE-P-008 — Stable public developer contract

Portable automation uses WebDriver BiDi. Deep introspection uses a Turing-owned protocol generated from schemas, with explicit version negotiation, bounded messages, cancellation, backpressure, authentication, and support windows.

### ENGINE-P-009 — Standards and tests move together

A web-platform feature is incomplete until specification interpretation, implementation, WPT coverage, negative cases, interoperability review, and unsupported behavior are aligned. Turing does not ship site-specific compatibility hacks as hidden engine semantics.

### ENGINE-P-010 — User quality is an engine requirement

Startup, input latency, smooth scrolling, accessibility, session recovery, tab lifecycle, memory pressure behavior, battery impact, and trusted UI are engine-level success criteria, not shell polish applied later.

## 7. Developer API strategy

### 7.1 Two-layer protocol model

**Layer A: standards-facing automation**

Implement WebDriver BiDi as the portable, interoperable control surface. Track the exact Editor’s Draft revision and WPT implementation report. Keep standards behavior separate from Turing extensions.

**Layer B: Turing engine instrumentation**

Use a working-name “Turing Engine Protocol” until an ADR selects the final name. It should expose engine truth that general automation standards do not attempt to standardize:

- document, frame, site-instance, process, profile, and epoch identity;
- parser and preload state;
- style invalidation, cascade, container/query dependencies, and computed-value provenance;
- fragment trees, intrinsic sizing, fragmentation, paint chunks, damage, raster, layers, and hit testing;
- event-loop queues, scheduler priorities, cancellation, long tasks, and input deadlines;
- JavaScript bytecode, tier state, inline caches, deoptimization, GC phases, heap ownership, and external memory;
- network request context, cache partition, cookie policy, service-worker routing, CORS/CSP decisions, and connection reuse;
- storage transactions, quota, migrations, durability, and clear-site-data effects;
- sandbox, capability, permission, trusted-UI, extension, and agent-policy decisions;
- CPU, memory, GPU, network, disk, wakeups, energy, and AI resource attribution.

### 7.2 Protocol requirements

- Schemas are canonical and code-generating.
- Stable and experimental domains are separate.
- Major versions have published support windows.
- Clients negotiate capabilities rather than guessing by browser version.
- Every command has size, time, memory, and output limits.
- Streaming commands support flow control, cancellation, and partial failure.
- Events carry monotonic timestamps, target identity, document epoch, and causal linkage where possible.
- Sensitive values are redacted by default.
- Remote attachment is authenticated, visible, and disabled by default.
- Generic privileged kernel calls are prohibited.
- Generated clients are provided for Rust, TypeScript, Python, and test infrastructure.
- Trace files are versioned, deterministic enough to diff, and safe to open without executing page content.
- Migration notes and protocol compatibility tests are release requirements.

A future CDP compatibility adapter may be researched as an isolated translation layer for existing tools. It must not define Turing’s internal model, bypass policy, or become an engine dependency.

## 8. Open-web principles

Turing should apply these principles to every new web-facing API and behavior:

1. User needs outrank site convenience and implementation convenience.
2. Visiting a site must be safe by default.
3. Browser-trusted UI cannot be imitated or obscured by page content.
4. Origin, site, profile, frame, process, and document identity remain explicit.
5. Collect, retain, expose, and transmit the minimum data required.
6. APIs should be interoperable, predictable, feature-detectable, and progressively deployable.
7. Asynchronous work should be cancellable and should not require blocking the main thread.
8. Failure modes, limits, permission state, and unsupported behavior should be observable.
9. Specifications, implementations, and tests must converge; Turing does not “write fiction.”
10. New platform features require demonstrated user or developer need, implementer interest, tests, and security/privacy review.
11. Accessibility semantics are part of the platform behavior, not optional metadata.
12. Performance optimizations cannot silently change security or compatibility behavior.
13. Experimental APIs are clearly namespaced, permissioned where necessary, and removable.
14. Site-specific hacks require public justification, expiry, tests, and a standards/interoperability path.

Interop 2026 focus areas provide a current prioritization signal, not a replacement for dependency analysis. Turing should track the focus areas and their prerequisites while reporting unsupported features honestly.

## 9. Performance strategy

### 9.1 Optimize the user’s critical path

The critical path is not total throughput. It is the sequence that determines when a person can type, navigate, scroll, read, interact, recover, or stop an action.

Priority order:

1. browser chrome and address-field readiness;
2. input dispatch and compositor response;
3. visible document work needed for the next frame;
4. navigation, parser, style, layout, paint, raster, and script work needed for useful content;
5. user-visible background activity such as audio, downloads, calls, and active collaboration;
6. speculative and cache work;
7. unprotected background activity;
8. diagnostics and maintenance that can safely yield.

### 9.2 Avoid false parallelism

The engine should first establish a deterministic serial oracle. Parallel work is introduced where dependencies and measurements prove benefit:

- speculative preload discovery beside streaming parse;
- independent stylesheet parsing;
- selector matching on independent subtrees when invalidation permits;
- layout on independent formatting-context subtrees;
- raster by tile and priority;
- image/font decode in isolated workers;
- JavaScript parsing or compilation off-thread;
- GC marking or sweeping only after barriers and latency behavior are proven.

The scheduler must account for task overhead, cache locality, memory bandwidth, hardware class, foreground deadlines, thermal state, and energy mode.

### 9.3 Make memory a design input

Every major representation receives a byte budget and corpus measurement before broad feature growth. Turing should prefer compact handles, arenas, side tables, immutable shared data where isolation permits, lazy rare-state allocation, bounded caches, and bulk lifecycle release.

### 9.4 Measure tails and sustained behavior

Median speed alone hides user pain. Gates should include p95/p99 latency, long-run memory growth, frame-time distributions, process launch, tab revival, crash recovery, background wakeups, and thermal degradation.

## 10. Open-source strategy

Turing’s existing MPL-2.0 direction remains appropriate for an independently developed engine because file-level copyleft preserves improvements to covered files while allowing broader integration. This study does not change the license decision.

The project should make technical leadership inspectable:

- public roadmap, requirements, risks, ADRs, unsupported-feature map, and milestone evidence;
- reproducible builds and published provenance;
- public benchmark definitions, manifests, raw samples, analysis scripts, and regression history;
- open protocol schemas and generated clients;
- upstream WPT/Test262 contributions;
- transparent dependency and unsafe-code ledgers;
- public performance and compatibility dashboards that include failures;
- documented review ownership and security-reporting paths;
- contributor-friendly subsystem boundaries and reduced test cases;
- no private “magic” benchmark mode or hidden compatibility service in the release engine.

Open source alone does not guarantee trust or sustainability. Security response, maintainership, release continuity, code review, standards participation, and user support require durable ownership.

## 11. Research experiments

### EXP-ENGINE-001 — Reference-engine baseline

On fixed Tier L/M/H hardware, measure current stable Chromium, Safari/WebKit where available, Firefox/Gecko, and runnable Servo/Ladybird builds using identical local corpora. Record compatibility subset, process topology, tab lifecycle, memory categories, startup, interaction, frame pacing, energy, crashes, and unsupported pages.

### EXP-ENGINE-002 — Pipeline artifact prototype

Implement a minimal document pipeline with DOM epochs, immutable computed-style blocks, immutable layout fragments, paint chunks, a display list, and a software compositor. Compare rebuild cost, incremental invalidation, memory, deterministic traces, and debugging quality.

### EXP-ENGINE-003 — Adaptive parallelism controller

Compare serial, fixed-worker, work-stealing, and deadline-aware scheduling across small and large documents on Tier L/M/H. Measure total time, tail latency, memory, task overhead, cache misses where available, energy, and determinism.

### EXP-ENGINE-004 — Process topology simulator

Extend the existing prototype to model site instances, cross-origin frames, service workers, decoders, GPU work, DevTools, and agents. Quantify isolation-adjusted memory, launch latency, crash blast radius, and pressure behavior.

### EXP-ENGINE-005 — Developer protocol spike

Define schema-generated target, DOM, layout, performance, memory, and tracing domains. Generate Rust, TypeScript, and Python clients. Measure message size, command latency, stream backpressure, cancellation, version negotiation, and malformed-input behavior.

### EXP-ENGINE-006 — JavaScript tiering kernel

Prototype a bytecode interpreter, direct bytecode-to-machine baseline tier, and simple SSA mid-tier on a constrained language subset. Measure compile latency, code size, warm-up, deoptimization, end-to-end interaction traces, and tier equivalence.

### EXP-ENGINE-007 — Developer workflow study

Measure time and failure rate for common tasks: inspect cascade, diagnose forced layout, trace a slow interaction, identify a memory retainer, inspect a network-policy failure, debug a worker, reproduce a crash, and automate a cross-origin flow.

### EXP-ENGINE-008 — Everyday-user quality study

Measure startup, address-field use, tab search, session restore, permission comprehension, page crash recovery, 30-tab pressure, battery behavior, keyboard operation, and screen-reader workflows.

### EXP-ENGINE-009 — Compatibility dependency graph

Map Interop 2026 and high-value application features to normative prerequisites, WPT directories, security controls, rendering/runtime dependencies, and developer demand. Use the graph to order milestones without site-specific hacks.

### EXP-ENGINE-010 — Open-source execution health

Track review latency, first-contribution success, test reproducibility, issue age, bus factor, subsystem ownership, security-response drills, release repeatability, and standards-test contributions.

## 12. Decision gates

This study recommends no immediate change to the accepted independent-engine, Rust-first, multiprocess, security, or documentation policies.

Before a new architecture decision is accepted:

- at least one falsifiable experiment above must be completed;
- raw data, code, manifests, failures, and limitations must be public;
- the relevant WPT/Test262 or semantic correctness baseline must pass;
- security and accessibility effects must be reviewed;
- memory, latency, energy, and maintenance tradeoffs must be reported;
- the owning Blueprint chapters, ADRs, risks, requirements, work packages, and registries must be updated together.

## 13. Mapping to current Turing records

| Finding area | Existing owner |
|---|---|
| Language, Rust, dependencies, unsafe boundaries | [Language and dependency strategy](../blueprint-v1/03-language-and-dependency-strategy.md) |
| Process roles, capabilities, IPC, site isolation | [System architecture](../blueprint-v1/04-system-architecture.md) and [security model](../blueprint-v1/08-security-and-sandbox.md) |
| Rendering pipeline, layout, paint, compositor | [Web engine design](../blueprint-v1/05-web-engine.md) |
| Interpreter, GC, JIT, WebAssembly | [JavaScript runtime](../blueprint-v1/06-javascript-runtime.md) |
| Performance, memory, energy, 30-tab contract | [Performance and memory](../blueprint-v1/09-performance-memory.md) |
| Developer protocol, UI, accessibility, automation | [Product UI and DevTools](../blueprint-v1/11-product-ui-devtools.md) |
| WPT, Test262, differential tests, benchmarks | [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md) |
| Risks and external blockers | [Risk register](../blueprint-v1/15-risk-register.md) |
| Sources | [Primary-source bibliography](../blueprint-v1/18-source-bibliography.md) |
| Experiments | [Research and measurement program](../blueprint-v1/22-research-program.md) |

## 14. Primary sources reviewed

### Chromium and V8

- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- Chromium process model and site isolation — https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md
- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/
- V8 Sparkplug baseline compiler — https://v8.dev/blog/sparkplug
- V8 Maglev compiler — https://v8.dev/blog/maglev
- Chromium source license — https://chromium.googlesource.com/chromium/src/+/main/LICENSE

### WebKit and JavaScriptCore

- WebKit documentation — https://docs.webkit.org/
- WebKit2 multiprocess architecture — https://docs.webkit.org/Deep%20Dive/Architecture/WebKit2.html
- WebKit site isolation — https://docs.webkit.org/Deep%20Dive/SiteIsolation.html
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html
- WebKit WPT integration — https://docs.webkit.org/Infrastructure/WPTTests.html
- WebKit licensing — https://webkit.org/licensing-webkit/

### Gecko and SpiderMonkey

- Firefox process model — https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html
- SpiderMonkey overview — https://firefox-source-docs.mozilla.org/js/index.html
- Firefox performance documentation — https://firefox-source-docs.mozilla.org/performance/index.html
- Firefox remote protocols — https://firefox-source-docs.mozilla.org/remote/index.html
- Firefox source license — https://github.com/mozilla-firefox/firefox/blob/main/LICENSE

### Independent engines

- Servo project goals and governance — https://servo.org/about/
- Servo repository — https://github.com/servo/servo
- Servo project updates — https://servo.org/blog/
- Servo license — https://github.com/servo/servo/blob/main/LICENSE
- Ladybird project — https://ladybird.org/
- Ladybird repository and architecture overview — https://github.com/LadybirdBrowser/ladybird
- Ladybird license — https://github.com/LadybirdBrowser/ladybird/blob/master/LICENSE

### Standards, principles, tests, and benchmarks

- WHATWG working mode — https://whatwg.org/working-mode
- W3C Web Platform Design Principles, 24 February 2026 Group Note — https://www.w3.org/TR/design-principles/
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- WebDriver BiDi Editor’s Draft — https://w3c.github.io/webdriver-bidi/
- Web Platform Tests — https://web-platform-tests.org/
- Interop 2026 — https://web.dev/blog/interop-2026
- BrowserBench — https://browserbench.org/
- Speedometer — https://browserbench.org/Speedometer3.1/
- MotionMark — https://browserbench.org/MotionMark/

## 15. Unresolved questions

- Which process topology produces the best isolation-adjusted memory on each platform?
- Which engine stages benefit from parallelism on Tier L hardware without increasing energy or tail latency?
- Can a compact Rust DOM/style/fragment design materially beat current production engines after implementing equivalent behavior?
- Which graphics abstraction gives the best combination of launch time, memory, driver coverage, debugging, and GPU-process confinement?
- How much CDP compatibility is required for developer adoption, and can it remain a clean external adapter?
- What stable protocol support window is sustainable for a small open-source team?
- Which application corpus is legally redistributable and representative enough for continuous compatibility measurement?
- What staffing and release process are required before any “number one” claim can remain true through security and web-platform change?

## 16. Next action

The next research deliverable should be EXP-ENGINE-001: a reproducible, fixed-hardware baseline harness and versioned corpus. Architecture optimization should follow measured bottlenecks rather than perceived weaknesses in other browsers.
