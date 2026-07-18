# 14 — Roadmap, Milestones, and Work Breakdown

## 1. Planning rule

The destination is a Chrome-class general-purpose browser; the execution path is a sequence of independently testable systems. Dates are not promised before team capacity and measured throughput exist. Milestones are gate-based and may run in parallel only when interfaces and owners are clear.

A solo or small-team project should expect years, not months, to approach broad compatibility. Production safety requires sustained security response and review beyond implementation. The roadmap therefore creates useful artifacts early without labeling them a safe daily browser.

## 2. Program tracks

- **A — Product and UI:** shell, windows/tabs/profiles, commands, settings, accessibility, resource manager.
- **B — Kernel and IPC:** processes, identities, navigation, lifecycle, brokers, crash recovery.
- **C — Web engine:** HTML/DOM/CSS/layout/paint/compositing/input/accessibility.
- **D — JavaScript:** parser, interpreter, runtime, GC, bindings, JIT, WebAssembly.
- **E — Network/storage:** Fetch, protocols, cookies, cache, databases, service workers, downloads, credentials.
- **F — Platform/media:** GPU, fonts, images, audio/video, PDF, printing, devices, OS adapters.
- **G — Security/privacy:** sandbox, site isolation, web policy, supply chain, incident response.
- **H — DevTools/automation:** protocol, frontend, headless, WebDriver BiDi, test tooling.
- **I — AI/agents:** observations, policy, actions, provider adapters, audit, evaluations.
- **J — Quality/operations:** WPT/Test262, fuzzing, benchmarks, CI, packaging, signing, updater, support.

## 3. Milestone M0 — Repository and evidence foundation

Purpose: make every later claim reviewable.

Deliverables:

- charter, requirements, capability matrix, architecture decisions, threat model, risk register, source bibliography;
- Rust workspace and code-quality policy;
- schemas for requirements, risks, processes, IPC, DevTools, agent actions, benchmarks, and release evidence;
- documentation/link/schema/ID validation;
- initial CI and contribution/security policies;
- reference hardware and generated offline corpus definitions;
- dependency and unsafe-code ledgers.

Exit gates:

- all top-level requirements have stable IDs and owners or explicit unowned status;
- architecture and security invariants have tests in the bootstrap model;
- no production-safety claim;
- repository can be built/validated from clean instructions.

## 4. Milestone M1 — Native shell and process laboratory

Purpose: prove product responsiveness, platform adapters, process launch, IPC, lifecycle, and resource attribution without rendering the open web.

Deliverables:

- native windows, tab strip, address field, commands, profiles, session journal, accessibility semantics;
- browser kernel, renderer test process, network/storage mock services, GPU surface process;
- typed bounded IPC and handle broker;
- platform sandbox prototypes and negative tests;
- process/resource manager and trace viewer;
- 30 synthetic tab/process pressure simulator;
- crash/hang/restart and update-package laboratory.

Exit gates:

- shell remains responsive under process hangs and pressure;
- renderer test process has no prohibited ambient capabilities on each target platform;
- lifecycle state and memory accounting are visible;
- signed research packages may be produced, labeled non-browser prototype.

## 5. Milestone M2 — Static document engine

Purpose: render a meaningful, script-free standards subset.

Deliverables:

- URL/encoding, HTML tokenizer/tree builder, DOM, CSS parser/cascade, basic selectors;
- block/replaced layout, text shaping/line layout, fonts/images, basic SVG;
- display lists, CPU reference raster, GPU compositor integration;
- scrolling, hit testing, selection, links, forms without script, accessibility tree;
- static-page DevTools and semantic rendering traces;
- WPT subset, differential/reduced tests, parser/style/layout/image/font fuzzing.

Exit gates:

- declared static subset passes its conformance threshold;
- deterministic rendering on reference configurations;
- malicious pages remain in sandbox and respect resource caps;
- no JavaScript support is implied.

## 6. Milestone M3 — JavaScript interpreter and dynamic DOM

Purpose: execute modern language and page event behavior through the reference runtime.

Deliverables:

- JS lexer/parser, bytecode, interpreter, object model, exceptions, functions, classes, modules subset;
- exact stop-the-world GC, rooted handles, DOM wrappers, Web IDL generator;
- event loop, tasks/microtasks, timers, events, dynamic DOM/style/layout;
- console and debugger foundations;
- Test262 subset, GC stress, differential interpreter tests, runtime fuzzing.

Exit gates:

- published Test262 feature map;
- no known wrapper identity/lifetime leaks across navigation loops;
- dynamic DOM reduced tests and WPT subset pass;
- arbitrary-web browsing still labeled unsafe/incompatible.

## 7. Milestone M4 — Navigation, Fetch, storage, and multipage applications

Purpose: support controlled applications and realistic browsing flows.

Deliverables:

- network service HTTP/1.1/TLS, redirects, cache, cookies, Fetch/CORS/security policy subset;
- navigation transactions, frames, process swaps, history, BFCache subset;
- local/session storage, IndexedDB subset, Cache Storage, service-worker foundation;
- downloads, file chooser handles, permissions foundation;
- forms/editing/clipboard, workers/structured clone;
- network/storage DevTools and hermetic protocol test servers.

Exit gates:

- cross-origin and cross-profile tests pass for implemented APIs;
- storage crash/migration/quota tests pass;
- compromised renderer cannot open arbitrary sockets/files;
- supported-app corpus runs with documented gaps.

## 8. Milestone M5 — Layout breadth and product alpha

Purpose: cover mainstream layout and deliver a coherent developer preview.

Deliverables:

- inline/bidi/writing modes, flexbox, grid, tables, floats, positioning, fragmentation foundations;
- transitions/animations/transforms, advanced paint, retained display lists, compositor scrolling;
- richer SVG/canvas, accessibility breadth, browser permissions/download/history/bookmark/settings UX;
- HTTP/2, service workers/offline, improved storage;
- Elements, Network, Sources, Performance, Accessibility, Storage DevTools;
- headless and automation protocol alpha;
- signed auto-updating developer channel.

Exit gates:

- sandbox/site-isolation subset and update gates pass;
- compatibility report shows exact WPT/Test262 scope;
- product UI accessibility baseline passes;
- security team can ship emergency developer-channel fixes;
- release remains “developer preview,” not safe replacement claim.

## 9. Milestone M6 — Baseline JIT, media, extensions, and agent preview

Purpose: improve application performance and introduce bounded ecosystem features.

Deliverables:

- baseline JIT with W^X, inline caches, deoptimization, tier differential testing;
- WebAssembly reference/compiler track;
- audio/video pipeline and disclosed codec matrix; PDF/printing foundations;
- WebExtensions-compatible restricted subset and isolated extension host;
- agent semantic observations, action protocol, policy engine, local audit, one local and one remote provider adapter;
- prompt-injection and stale-action evaluation suite;
- 30-tab lifecycle manager with frozen/serialized/discarded states.

Exit gates:

- JIT security and equivalence gates pass;
- agent Class 3/4 actions cannot bypass confirmation;
- media/parser processes are sandboxed and fuzzed;
- extension permissions and resource attribution work;
- 30-tab results publish lifecycle and isolation truth.

## 10. Milestone M7 — Compatibility and performance beta

Purpose: move from architecture proof to serious daily-use candidate for non-sensitive volunteers.

Deliverables:

- broader CSS/HTML/JS/WebAssembly/network/storage/media/device coverage;
- optimizing JIT initial tier;
- HTTP/3, stronger service-worker/background behavior;
- robust crash recovery, profile migrations, sync design/implementation if funded;
- mature DevTools, WebDriver BiDi, extension API breadth;
- phishing/malware reputation strategy or explicit supported alternative;
- cross-platform installers, staged updates, rollback, symbols, SBOM/provenance;
- fixed-hardware performance, energy, and compatibility laboratory.

Exit gates:

- independent security review and critical findings resolved;
- sustained fuzzing with no unresolved release-critical crashes;
- broad published conformance thresholds chosen from actual results;
- update/incident response staffed;
- accessibility and platform matrices pass;
- beta risk disclosure accepted by release owners.

## 11. Milestone M8 — Stable general-purpose release candidate

Purpose: support normal users within a documented compatibility and platform envelope.

Deliverables:

- security patch SLA, supported OS list, end-of-life policy;
- strong compatibility on top-site and standards corpora with no hidden denominator;
- credential/passkey, permissions, downloads, media, printing, PDF, accessibility, extension, DevTools, automation, and agent support statements;
- reliable signed update, rollback, profile recovery, and support tooling;
- privacy and telemetry documentation;
- independent security/accessibility review and public release evidence.

Exit gates:

- zero open critical security/data-loss/update issues;
- all stable security and release gates pass;
- proprietary gaps such as DRM/vendor services are explicit;
- staffing can maintain supported platforms and urgent fixes;
- release board approves “stable” based on evidence.

## 12. Milestone M9 — Chrome-class parity campaign

Purpose: close long-tail web, enterprise, media, extension, localization, accessibility, and performance gaps.

Work includes:

- current standards and continuous WPT/Test262 movement;
- advanced graphics/WebGPU, media, devices, printing/PDF, internationalization;
- enterprise policy and deployment;
- extension compatibility and ecosystem tooling;
- mobile architecture only after desktop foundation proves portable;
- sync/accounts/services under separate privacy and operations review;
- proprietary licensing negotiations where desired;
- ongoing compiler/GC/layout/network/GPU optimization;
- security research, exploit mitigations, bug bounty, and rapid update capability.

There is no honest fixed end date. The web platform evolves continuously.

## 13. Initial work packages

### WP-001 — Repository validation

Create stable requirement/risk/ADR schemas, link checks, source policy, and CI.

### WP-002 — Rust kernel types

Process roles, identities, origins/sites, profiles, document epochs, capabilities, bounded IPC, errors.

### WP-003 — Tab lifecycle simulator

State machine, protection reasons, memory pressure, accounting, trace export, 30-tab scenarios.

### WP-004 — Sandbox probes

Per-platform child process that attempts forbidden operations and reports effective restrictions.

### WP-005 — Native shell spike

Window, tab strip, command field, accessibility, compositor surface, event trace.

### WP-006 — HTML tokenizer

Spec-state implementation, streaming decoder interface, parser traces, WPT/reduced tests, fuzzer.

### WP-007 — DOM arena

Generational handles, tree mutation, attributes, text, traversal, epochs, wrapper hooks.

### WP-008 — CSS parser/cascade

Tokenizer, rules, declarations, selectors, specificity, cascade, computed-value skeleton.

### WP-009 — Block/text layout reference

Fragments, intrinsic sizing, line shaping, bidi adapter, paint geometry, semantic traces.

### WP-010 — Display-list reference

Paint properties, display items, CPU raster, screenshot and trace harness.

### WP-011 — JS language kernel

Parser, bytecode, interpreter, values, objects, functions, exceptions, Test262 runner.

### WP-012 — Exact GC

Heap, roots, handles, tracing, stress mode, weak processing plan, external-memory accounting.

### WP-013 — Navigation/process assignment model

Browsing contexts, sites, origins, commits, redirects, process swaps, history, BFCache eligibility.

### WP-014 — Network request context

URL/origin, HTTP/1.1/TLS adapter, request policy, cache/cookie skeleton, hermetic server.

### WP-015 — Agent policy reference

Principal/grant/action schema, risk classifier, epoch validation, confirmation simulator, adversarial tests.

### WP-016 — Trace and resource model

Stable event schema, process/tab attribution, local viewer, redaction, benchmark exporter.

## 14. Staffing reality

A credible stable browser needs dedicated ownership across engine/layout, JS/compiler/GC, networking/storage, GPU/media, security/sandbox, platform UI/accessibility, DevTools/automation, release/update, compatibility/testing, and incident response. One person can build meaningful prototypes and foundational subsystems, but cannot responsibly promise continuous Chrome-level compatibility and zero-day response alone.

The project should recruit or develop maintainers by subsystem, document bus factor, and stop expanding supported platforms/features when security maintenance exceeds capacity.

## 15. Decision checkpoints

At the end of each milestone answer:

- Which requirements passed and which remain unsupported?
- Did architecture assumptions survive measurement?
- What is the current attack surface and sandbox evidence?
- What resource targets were met under what lifecycle state?
- What dependencies or licensing constraints changed?
- Is the next milestone still the highest-value path?
- Should a component be simplified, delayed, replaced behind its interface, or abandoned?

The long-term vision is fixed; implementation choices remain empirical.

## Professional buildout prerequisite

Before substantial production implementation, resolve ADR-0009, accept the workspace/toolchain/interface contracts, activate ownership/traceability/review records, reproduce bootstrap on fresh hosts, and staff backup ownership. The checked [Backup Ownership Gap Inventory](../research/backup-ownership-gap-inventory-2026-07.md), checked no-claim [backup-owner qualification template](../project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json), and checked no-claim [backup-ownership readiness-review template](../project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json) document the current `PB-019` blocker but do not provide named qualified backups, two-person control, or owner-reviewed backup ownership readiness. This refines M0 without changing WP-001 through WP-018 status.

<!-- MARKET-STRATEGY-2026-07 -->
## Market-opportunity sequencing

- M0: validate target segments, jobs, open export, and Space data model; keep `OP-*` non-normative.
- M1: prototype shell-level Spaces, identity indicators, journal, migration report, and resource attribution.
- M2–M5: add split/Research Canvas foundations, Time Machine restoration, identity routing, privacy receipts, and Developer Causal Mode alongside engine maturity.
- M5–M6: first-party Plug-ins and read-only selected-source AI.
- M7+: optional encrypted sync, low-risk isolated agent actions, collaboration, and wider Plug-in ecosystem after security and operations gates.

An opportunity enters the executable backlog only after promotion through evidence and ownership.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI and pre-build sequencing

Before M1 shell code expands, complete the toolkit-neutral UI contracts, select one reference desktop platform, build equivalent Slint/Vizia/Floem-or-GPUI shells, prove page-surface/accessibility/IME/crash integration, and review licensing. These are controlled M0/M1 experiments, not a reason to delay unrelated parser, schema, sandbox, or benchmark research.

`PB-GATE-0` tracks the minimum applicable evidence for implementation kickoff; preview and stable operational gates remain later milestones.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent execution and production sequencing

- M0: establish protected review, task/run/evidence schemas, agent authority, root workspace, and provenance.
- M1–M4: permit contained component tasks with independent review; no production claim.
- M5+: activate preview gates only after update, security, migration, accessibility, and incident evidence.
- Beta and stable: require `PRG-001` through `PRG-020`, numeric SLOs, supported platform contracts, qualified backup ownership, and human release authority.
