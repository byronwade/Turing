# 09 — Performance, Memory, Energy, and the 30-Tab Contract

## 1. Performance philosophy

Turing optimizes end-to-end user-perceived latency and sustained resource use, not a single benchmark score. Correctness, security mitigations, accessibility, and page activity remain enabled unless the experiment explicitly states otherwise.

Every published number includes build, commit, platform, hardware, memory size, power mode, thermal state, browser configuration, profile state, cache state, network conditions, page corpus, extensions, model state, process count, isolation policy, tab lifecycle, repetitions, and statistical summary.

## 2. Primary performance dimensions

- cold and warm startup;
- first window and address-bar readiness;
- navigation response start, first content, largest content, interactive readiness, and visual stability;
- input-to-event, event-to-render, and input-to-present latency;
- page-observable Navigation Timing and Event Timing phases, with page-level responsiveness metrics kept separate from browser chrome and internal process latency;
- scrolling and animation frame pacing at 60/90/120/144 Hz;
- JavaScript parse/compile/execute and GC pauses;
- style, layout, paint, raster, and composite time;
- memory: private working set, resident set, committed virtual memory, swap, GPU allocation, disk cache, and per-principal attribution;
- CPU time, wakeups, network bytes, disk I/O, battery/energy, and thermal behavior;
- recovery latency after tab, renderer, GPU, network, or browser crash;
- agent observation/action latency, token use, local-model memory, and remote-model cost.

## 3. Reference hardware tiers

The benchmark lab defines at least three fixed tiers:

- **Tier L:** 4 performance-class CPU cores, integrated GPU, 8 GiB RAM, constrained SSD;
- **Tier M:** 8 modern cores, integrated or midrange GPU, 16 GiB RAM, mainstream NVMe;
- **Tier H:** 12+ cores, modern discrete/integrated GPU, 32 GiB RAM.

Exact machines and OS builds are versioned in benchmark metadata. Tier M is the primary product gate; Tier L determines degradation and pressure behavior.

## 4. Workload corpus

Synthetic pages are necessary but insufficient. The checked-in/offline corpus includes legally redistributable or generated representatives for:

- static article/documentation;
- image-heavy news/feed;
- email-style application;
- collaborative editor;
- spreadsheet/grid;
- chat/realtime stream;
- mapping/canvas;
- dashboard with charts;
- video page;
- shopping/catalog and checkout mock;
- large code-hosting diff;
- WebAssembly application;
- abusive timers/workers/mutations;
- cross-origin iframe/ad-like composition;
- service-worker offline application;
- accessibility-heavy form and table;
- international text, vertical writing, emoji, and variable fonts.

Live-site measurements are supplementary because content changes. Results identify capture date, authentication state, region, and network.

## 5. The 30-tab contract

The program’s key scenario is a reproducible 30-tab mixed workload. It is not defined as “open 30 URLs and immediately discard them.”

### 5.1 Tab mix

On Tier M:

- 5 foreground/recent interactive application tabs;
- 10 warm background document/application tabs;
- 8 eligible frozen tabs;
- 5 eligible serialized/discarded tabs after pressure escalation;
- 1 audio-playing tab;
- 1 protected unsaved-form or active-download tab.

A second **all-live isolation stress** run keeps all eligible tabs live to expose the actual security/performance cost. Results are reported separately.

The checked [no-claim 30-tab smoke scenario manifest](machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json) records the current mixed-state and all-live denominator shape for `PB13-EV-008`. It is sample-only planning evidence over the generated smoke corpus, not the final Tier M workload, not a browser run, and not a memory, energy, Chrome-class, or performance result.

The checked [no-claim trace and artifact package contract](machine/benchmark-artifact-packages/no-claim-trace-package.plan.json) records the current package-root, trace-class, artifact-class, redaction, retention, prohibited-content, unsupported-behavior, and missing-proof requirements for `PB13-EV-007`. It is not an ETW, Perfetto, memory, energy, Chrome-class, or performance result.

The checked [no-claim browser launch-runner contract](machine/benchmark-launch-runners/no-claim-browser-launch.plan.json) records the current command, stage, timeout/cancellation, cache/profile, failure-finalization, trace/artifact, resource-attribution, and no-claim controls for `PB13-EV-005`. The checked no-browser browser launch-runner self-test validates command parsing, forbidden arguments, registry references, artifact-root handling, and no-claim finalization. This is not a browser launch, trace, raw-sample, memory, energy, Chrome-class, or performance result.

The checked no-claim statistics-analysis contract in [no-claim statistics-analysis plan](machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json) records the current sample-design, warmup, randomization or paired order, noise-study, confidence or uncertainty, effect-size, outlier, multiple-comparison, metric-family, denominator, and rejection controls for `PB13-EV-006`. This is not a browser benchmark run, not a runner-generated raw sample set, and no confidence interval from measured browser data, memory result, energy result, Chrome-class result, competitor result, or performance claim exists.

### 5.2 Required disclosure

For each run publish:

- per-tab URL/corpus class and state;
- renderer/site-instance/process count;
- live, throttled, frozen, BFCache, serialized, and discarded counts;
- pages protected from lifecycle changes and why;
- total and per-process memory categories;
- reload/revival latency and lost in-memory state;
- network/service-worker/background activity;
- site isolation and speculative execution settings;
- swap and system memory pressure.

### 5.3 Initial engineering budgets, not promises

On Tier M with the defined mixed state:

- browser kernel and product UI private working set: target ≤ 180 MiB after steady state;
- network, storage, GPU, extension/agent-disabled shared services combined: target ≤ 350 MiB CPU-side, GPU reported separately;
- median live simple-document renderer incremental private working set: target ≤ 70 MiB;
- median live application renderer incremental private working set: target ≤ 140 MiB;
- frozen eligible tab retained private working set after trimming: target ≤ 30 MiB excluding safely shared resources;
- serialized/discarded tab metadata in memory: target ≤ 3 MiB, with disk snapshot size reported;
- total 30-tab mixed workload: target ≤ 2.5 GiB CPU private working set and ≤ 600 MiB browser-attributed GPU allocation after stabilization;
- foreground tab revival from frozen: p95 ≤ 150 ms to input readiness;
- revival from serialized/discarded state: p95 ≤ 1.5 s on warm network/cache for corpus pages, with full reload clearly indicated.

These targets will change from measurement. They may not be claimed for arbitrary websites.

## 6. Tab lifecycle model

States are explicit:

1. `Active`: visible or recently interacted; normal scheduling.
2. `Background`: not visible; reduced priority but normal semantics.
3. `Throttled`: timers/network/workers constrained within platform rules.
4. `Frozen`: script/task execution paused; renderer memory trimming attempted; no claim of active execution.
5. `Serialized`: Turing-owned safe state checkpoint stored; process may be released. Only data explicitly designed for serialization is retained.
6. `Discarded`: document process state removed; URL/history/session metadata retained; activation reloads.
7. `Crashed`: abnormal loss; distinct UI and recovery.

BFCache is orthogonal: a history entry may hold a frozen document under strict eligibility and budget. It is not used as a euphemism for all tab suspension.

### 6.1 Protection conditions

Tabs are protected from freeze/discard while they have configured critical activity, including:

- audible audio or media session;
- camera, microphone, display capture, WebRTC call;
- active download/upload or filesystem write;
- unsaved form/editor state that cannot be safely preserved;
- WebUSB/serial/Bluetooth/HID session;
- active DevTools debugging or performance recording;
- explicit user “keep active” pin;
- enterprise policy;
- visible agent action awaiting confirmation.

Protection is observable and can be overridden only through explicit user/policy controls.

## 7. Memory accounting

Each allocation is charged directly or sampled to a semantic owner:

- browser UI/profile/session;
- document/frame/site instance;
- JavaScript heap/code/metadata;
- DOM/style/layout/paint/accessibility;
- images/fonts/canvas/media;
- network buffers/cache;
- storage transactions/mappings;
- GPU textures/buffers/pipelines;
- extension;
- DevTools;
- agent/model.

Shared resources use proportional or first-owner-plus-shared accounting, with both physical total and charged total shown. The UI does not sum double-counted shared pages and call it physical memory.

Memory instrumentation distinguishes live bytes, allocator-reserved bytes, committed mappings, resident pages, shared pages, compressed memory, swap, and GPU estimates. Platform limitations are disclosed.

## 8. Allocation strategy

- arenas for document-lifetime and layout-epoch data;
- compact IDs and packed representations for hot node/style/fragment data;
- immutable shared stylesheets, bytecode, fonts, and decoded resources only when profile/security boundaries permit;
- slab/size-class allocation for common objects;
- streaming parsers and bounded buffers;
- image decode to target size/tiles where semantics permit;
- lazy creation of rare DOM/style/layout/DevTools structures;
- cache entry budgets by value, cost, recency, and owner;
- release or `madvise`/working-set trim of free pages at lifecycle transitions;
- no unbounded task, IPC, trace, console, network, mutation-observer, or agent queues.

## 9. CPU and responsiveness

The scheduler uses deadlines and priorities tied to visible work. Core metrics:

- address-bar key-to-paint p95;
- pointer/key input-to-present p50/p95/p99;
- long tasks over 50 ms and their attribution;
- frame deadline misses and stage attribution;
- main-thread blocking from style/layout/script/GC/IPC;
- queue wait versus execution time;
- priority inversion detection;
- background CPU and wakeups with tabs idle.

Background pages receive budget buckets. A page that exhausts its CPU budget is increasingly throttled, with exceptions for user-visible critical activity.

## 10. Startup

Startup is divided into executable load, runtime initialization, profile metadata, window creation, first paint, address-bar readiness, session enumeration, and tab restoration. Tabs restore lazily. Large history/bookmark/extension stores are not fully loaded before first interaction.

Initial Tier M goals:

- warm process start to interactive window p50 ≤ 250 ms, p95 ≤ 450 ms;
- cold start p50 ≤ 650 ms, p95 ≤ 1.2 s;
- first address-bar input accepted before background session restoration;
- no network required for startup.

Numbers are goals pending an implementation and are never presented as achieved until measured.

## 11. Page-load and rendering budgets

Turing tracks internal stage budgets rather than optimizing only external metrics:

- request queue, DNS/connect/TLS, response wait, decode;
- parser and blocking script time;
- stylesheet parse and style calculation;
- layout and fragmentation;
- display-list build, raster, and composite;
- image/font decode and late metric shifts;
- JS parse/compile/execute and GC;
- service-worker and extension overhead.

DevTools can export a portable trace with stable event names. Traces exclude sensitive payload by default.

## 12. Energy

Energy gates include:

- idle browser with one and 30 quiescent tabs;
- background timers and service workers;
- continuous scrolling;
- video playback;
- WebGL/WebGPU workload;
- local AI model active/idle;
- remote AI action loop;
- laptop battery and thermal throttling behavior.

The browser reacts to OS low-power mode, thermal pressure, occlusion, and display refresh changes. It avoids periodic wakeups when no deadline requires them.

## 13. Agent performance

AI features have separate budgets so browser improvements are not masked by model costs:

- semantic snapshot generation time/bytes;
- redaction and policy evaluation;
- provider request latency and token count;
- local-model resident/working memory and accelerator use;
- action execution and stabilization time;
- number of observations/replans per task;
- agent-induced page CPU/network/memory;
- cancellation latency.

Local models are loaded on demand and unloadable. A dormant agent feature must not reserve gigabytes or keep the GPU awake.

## 14. Benchmark governance

- benchmark definitions are versioned and reviewed like APIs;
- test pages and server behavior are pinned;
- results are stored as raw samples plus summary;
- regressions are bisected automatically where infrastructure permits;
- thresholds use noise studies and practical impact, not arbitrary zero-tolerance;
- benchmark-specific code paths are prohibited;
- competitor comparisons use current stable builds, default security settings, clean equivalent profiles, and the same workload;
- failed/unsupported pages count; they are not dropped silently.

Suite-specific methodology controls are mandatory before a synthetic result is used in a comparison: Speedometer 3.1 no-duration subtests invalidate the run; JetStream 3.0 retains per-workload output, documented startup/worst/average treatment, and version identity; MotionMark records target frame rate, refresh rate, viewport class, warmup, and GPU/power state. The dated [Chrome performance announcement](https://blog.google/chromium/a-double-victory-for-web-speed-chrome-breaks-records-again-on-speedometer-31-and-jetstream-3/) reports Speedometer 3.1 and JetStream 3 scores from a specified M5/macOS 26.0.1 setup; it is competitor context only and must not be treated as a Turing result or universal target. These controls support diagnostic validity only and do not establish a Chrome-class or product-performance claim.

The checked no-claim [statistics-analysis contract](machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json), [benchmark readiness-review template](machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json), and [benchmark engine baseline harness readiness map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md) define future `PB-013` analysis, owner-review, and stop/resume handoffs across sample design, uncertainty, denominators, hardware, OS controls, corpus, servers, runners, artifacts, browser pins, statistics, and claim bundles. They are not owner-reviewed statistics analysis or benchmark readiness: there is no owner-reviewed benchmark readiness, benchmark-ready status, public performance claim, faster claim, lower-memory claim, lower-energy claim, Chrome-class claim, competitor-result claim, production claim, or implementation claim from these checked no-claim records.

## 15. Performance gates

- **PERF-GATE-1:** no release-critical memory leak across repeated navigation, open/close, BFCache, worker, media, DevTools, extension, or agent cycles.
- **PERF-GATE-2:** 30-tab mixed and all-live results include complete lifecycle/isolation disclosure.
- **PERF-GATE-3:** p95 interaction latency and frame pacing remain within milestone budgets on Tier M.
- **PERF-GATE-4:** idle background CPU/wakeups remain below published thresholds on Tier L/M.
- **PERF-GATE-5:** memory regressions are attributed to semantic owners before merge or explicitly waived with an issue.
- **PERF-GATE-6:** no optimization disables a security mitigation, accessibility path, correctness test, or active page behavior without labeling the result experimental.

<!-- MARKET-STRATEGY-2026-07 -->
## Resource Truth Center research

`OP-003` proposes per-Space and per-principal attribution, lifecycle reasons, predicted savings, state-loss risk, and revival quality. This extends honest 30-tab reporting but is not yet a supported product contract. Instrumentation overhead and attribution uncertainty remain visible.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Shell footprint and framework selection

UI measurements include binary/package contribution, startup, idle memory, update allocations, input latency, frame pacing, GPU allocation, energy, hidden-window wakeups, 100-tab state, accessibility latency, page-surface composition, and recovery. One empty-window number cannot select a toolkit. Normal builds compile one selected backend/renderer.

<!-- WP-002-KERNEL-IPC-2026-07 -->
## M0 queue and IPC budget reference

The generated control-plane schema now defines queue classes with both item-count and encoded-byte ceilings. `turing-ipc::BoundedQueue` applies explicit non-blocking backpressure, never silently evicts or drops work, returns rejected items to the caller, stores the admitted byte charge beside the item, and releases that exact charge on dequeue. Message kinds also carry generated encoded-size ceilings.

The current values are M0 safety defaults rather than production performance targets. They may change only with fixed-hardware workloads, latency and memory evidence, overload behavior, correctness/security guardrails, and a rollback plan. `REQ-PERF-004` therefore has reference implementation evidence but is not verified for production traffic.
