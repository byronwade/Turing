# 14 — Roadmap, Milestones, and Work Breakdown

## 1. Planning rule

The destination is a Chrome-class general-purpose browser; the execution path is a sequence of independently testable systems. Dates are not promised before team capacity and measured throughput exist. Milestones are gate-based and may run in parallel only when interfaces, dependencies, owners, and reviewers are clear.

A solo or small-team project should expect years, not months, to approach broad compatibility. Production safety requires sustained security response and review beyond implementation. The roadmap creates useful artifacts early without labeling them a safe daily browser.

The detailed agent-facing sequence is the [Implementation Master Plan](../project-buildout/implementation-plan/README.md). The machine dependency source is [`backlog.json`](machine/backlog.json). If prose and machine records differ, implementation stops until they are synchronized.

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

## 3. M0 — Repository and evidence foundation

Purpose: make every later claim reviewable.

Deliverables:

- charter, requirements, capability matrix, architecture decisions, threat model, risk register, source bibliography;
- Rust workspace and code-quality policy;
- schemas for requirements, risks, processes, IPC, DevTools, agent actions, benchmarks, tasks, evidence, and release gates;
- documentation/link/schema/ID validation;
- CI and contribution/security policies;
- reference-hardware and offline-corpus definitions;
- dependency, unsafe, native, generated-code, and provenance ledgers;
- implementation execution graph, milestone gates, interface freezes, evidence catalog, and task sequence.

Exit gates:

- all top-level requirements have stable IDs and owners or explicit unowned status;
- architecture and security invariants have executable reference tests;
- repository builds and validates from clean instructions;
- contained tasks use reviewed `TASK-*` manifests;
- no production-safety claim.

## 4. M1 — Native shell and process laboratory

Purpose: prove product responsiveness, platform adapters, process launch, IPC, lifecycle, sandboxing, and resource attribution without rendering the open web.

Deliverables:

- native windows, tabs, command field, profiles/Spaces placeholders, session journal, and accessibility semantics;
- browser kernel, renderer test process, mock network/storage services, and GPU surface process;
- typed bounded IPC, authenticated transport experiments, handle/shared-memory contracts;
- cross-platform sandbox probes and negative tests;
- process/resource manager and trace viewer;
- 30-tab synthetic pressure simulator;
- crash/hang/restart, profile recovery, and signed research-package laboratory.

Exit gates:

- shell remains responsive under process hangs and pressure;
- renderer test process has no prohibited ambient capabilities on every claimed platform;
- lifecycle state and resource accounting are visible and reconciled;
- keyboard, assistive technology, IME, and trusted-UI critical paths pass on the reference platform;
- signed research packages install and roll back;
- output remains labeled non-browser research prototype.

## 5. M2 — Static document engine

Purpose: render a meaningful, script-free standards subset.

Deliverables:

- URL/encoding, HTML tokenizer/tree builder, DOM, CSS parser/cascade, selectors;
- block/replaced layout, text shaping/line layout, fonts/images, basic SVG;
- display lists, CPU reference raster, GPU compositor integration;
- scrolling, hit testing, selection, links, forms without script, accessibility tree;
- static-page DevTools and semantic rendering traces;
- WPT subset, differential/reduced tests, parser/style/layout/image/font fuzzing.

Exit gates:

- ADR-0009 and required foundation decisions are accepted;
- declared static subset passes its conformance threshold;
- deterministic rendering on reference configurations;
- malicious pages remain in sandbox and respect resource caps;
- no JavaScript or general-browser support is implied.

## 6. M3 — JavaScript interpreter and dynamic DOM

Purpose: execute a declared modern-language subset and page event behavior through a trustworthy reference runtime.

Deliverables:

- JS lexer/parser, bytecode, verifier, interpreter, object model, exceptions, functions, classes, modules subset;
- exact stop-the-world GC, rooted handles, DOM wrappers, Web IDL generator;
- event loop, tasks/microtasks, timers, events, dynamic DOM/style/layout;
- console and debugger foundations;
- Test262 subset, GC stress, differential interpreter tests, runtime fuzzing.

Exit gates:

- published Test262 feature map;
- no known wrapper identity/lifetime leaks across navigation loops;
- dynamic DOM reduced tests and WPT subset pass;
- OOM, cancellation, crash, and teardown behavior is explicit;
- arbitrary-web browsing remains unsafe/incompatible.

## 7. M4 — Navigation, Fetch, storage, and controlled applications

Purpose: support controlled multipage applications and realistic browsing flows.

Deliverables:

- network service HTTP/1.1/TLS, redirects, cache, cookies, Fetch/CORS/security-policy subset;
- navigation transactions, frames, process swaps, history, BFCache subset;
- local/session storage, IndexedDB subset, Cache Storage, service-worker foundation;
- downloads, brokered file handles, permissions foundation;
- forms/editing/clipboard, workers/structured clone;
- network/storage DevTools and hermetic protocol servers.

Exit gates:

- cross-origin and cross-profile tests pass for implemented APIs;
- storage crash/migration/quota tests pass;
- compromised renderer cannot open arbitrary sockets/files or forge request context;
- controlled-application corpus runs with documented gaps.

## 8. M5 — Layout breadth and developer preview

Purpose: cover mainstream layout and deliver a coherent, signed developer preview.

Deliverables:

- inline/bidi/writing modes, flexbox, grid, tables, floats, positioning, fragmentation foundations;
- transitions/animations/transforms, advanced paint, retained display lists, compositor scrolling;
- richer SVG/canvas, accessibility breadth, browser permissions/download/history/bookmark/settings UX;
- HTTP/2 and service-worker/offline breadth when evidence permits;
- Elements, Network, Sources, Performance, Accessibility, Storage DevTools;
- headless and automation protocol alpha;
- signed auto-updating developer channel, rollback, crash symbols, SBOM/provenance.

Exit gates:

- sandbox/site-isolation subset and update gates pass;
- compatibility report shows exact WPT/Test262 scope;
- product UI accessibility baseline passes;
- security owners can ship emergency developer-channel fixes;
- release remains “developer preview,” not a safe replacement claim.

## 9. M6 — Baseline JIT, media, Plug-ins, and agent preview

Purpose: improve application performance and introduce bounded ecosystem features.

Deliverables:

- baseline JIT with W^X, inline caches, deoptimization, tier differential testing;
- WebAssembly reference/compiler track;
- audio/video pipeline and disclosed codec matrix; PDF/printing foundations;
- capability-based Turing Plug-ins and restricted WebExtensions adapter;
- agent semantic observations, typed actions, policy engine, local audit, provider adapters;
- prompt-injection and stale-action evaluation suite;
- real 30-tab lifecycle manager with frozen/serialized/discarded states.

Exit gates:

- JIT security and equivalence gates pass;
- agent consequential actions cannot bypass deterministic authorization and confirmation;
- media/parser processes are sandboxed and fuzzed;
- Plug-in permissions, revocation, update, and resource attribution work;
- 30-tab results publish lifecycle and isolation truth.

## 10. M7 — Compatibility and performance beta

Purpose: move from architecture proof to a serious daily-use candidate for informed, non-sensitive volunteers.

Deliverables:

- broader web-platform, runtime, network, storage, media, device, accessibility, and localization coverage;
- optimizing JIT initial tier;
- HTTP/3 and stronger service-worker/background behavior;
- robust crash recovery, profile migrations, optional sync if funded;
- mature DevTools, WebDriver BiDi, and Plug-in API breadth;
- phishing/malware reputation strategy or explicit alternative;
- cross-platform installers, staged updates, rollback, symbols, SBOM/provenance;
- continuous fixed-hardware compatibility/performance/energy laboratory.

Exit gates:

- independent security review and critical findings resolved;
- sustained fuzzing with no unresolved release-critical crash class;
- broad published conformance thresholds chosen from actual results;
- update/incident response staffed and rehearsed;
- accessibility and platform matrices pass;
- beta risk disclosure accepted by release owners.

## 11. M8 — Stable general-purpose release candidate

Purpose: support normal users within a finite documented compatibility and platform envelope.

Deliverables:

- accepted stable-v1 scope, supported OS/hardware list, security patch and EOL policy;
- strong compatibility on declared standards and workflow corpora with no hidden denominator;
- complete support statements for credentials, permissions, downloads, media, printing, PDF, accessibility, Plug-ins, DevTools, automation, and agents;
- reliable signed update, rollback, profile recovery, and support tooling;
- privacy, telemetry, service, and offline documentation;
- independent security/accessibility review and public release evidence.

Exit gates:

- all applicable `PRG-001` through `PRG-020` gates pass;
- zero open critical security/data-loss/update/signing issues;
- proprietary gaps are explicit;
- staffing can maintain supported platforms and urgent fixes;
- release board and human authority approve stable based on evidence.

## 12. M9 — Chrome-class parity and continuous maintenance

Purpose: close long-tail web, enterprise, media, Plug-in, localization, accessibility, platform, and performance gaps while maintaining supported releases.

Work includes:

- current standards and continuous WPT/Test262 movement;
- advanced graphics/WebGPU, media, devices, printing/PDF, internationalization;
- enterprise policy/deployment and ecosystem tooling;
- mobile architecture only after desktop foundation proves portable and supportable;
- sync/accounts/services under separate privacy and operations review;
- proprietary licensing negotiations where desired;
- ongoing compiler/GC/layout/network/GPU optimization;
- security research, exploit mitigations, bug bounty, and rapid update capability.

There is no honest fixed end date. The web platform evolves continuously.

## 13. Canonical work packages

The following list is synchronized with [`backlog.json`](machine/backlog.json):

1. **WP-001 — Repository validation and evidence foundation.**
2. **WP-002 — Kernel identities, process roles, capabilities, and bounded IPC.**
3. **WP-003 — Cross-platform renderer sandbox probes.**
4. **WP-004 — Native accessible browser-shell spike.**
5. **WP-005 — Tab lifecycle, resource attribution, and 30-tab simulator.**
6. **WP-006 — HTML tokenizer and tree builder.**
7. **WP-007 — DOM arena, mutation epochs, and events.**
8. **WP-008 — CSS parser, selectors, cascade, and computed values.**
9. **WP-009 — Block/text layout, display list, and reference raster.**
10. **WP-010 — JavaScript parser, bytecode, interpreter, and Test262 harness.**
11. **WP-011 — Exact tracing GC and Web IDL bindings.**
12. **WP-012 — Navigation transactions, site instances, and renderer swaps.**
13. **WP-013 — Scoped HTTP/TLS, cache, cookies, and hermetic server.**
14. **WP-014 — Storage broker, quota, migrations, and service-worker foundation.**
15. **WP-015 — Versioned DevTools/automation protocol and trace viewer.**
16. **WP-016 — Capability-safe agent reference implementation.**
17. **WP-017 — Signed update, rollback, and profile-migration laboratory.**
18. **WP-018 — Fixed-hardware compatibility, performance, memory, and energy laboratory.**

Detailed dependencies, task families, negative tests, evidence, handoffs, and non-goals are in the [work-package playbooks](../project-buildout/implementation-plan/16-work-package-playbooks.md) and [`implementation-execution-graph.json`](machine/implementation-execution-graph.json).

## 14. Staffing reality

A credible stable browser needs dedicated ownership across engine/layout, JS/compiler/GC, networking/storage, GPU/media, security/sandbox, platform UI/accessibility, DevTools/automation, release/update, compatibility/testing, and incident response. One person can build meaningful prototypes and foundational subsystems, but cannot responsibly promise continuous Chrome-level compatibility and zero-day response alone.

The project recruits or develops maintainers by subsystem, documents bus factor, and reduces supported platforms/features when security maintenance exceeds capacity.

## 15. Decision checkpoints

At the end of each milestone answer:

- Which requirements passed and which remain unsupported?
- Did architecture assumptions survive measurement?
- What is the current attack surface and sandbox evidence?
- What resource targets were met under what lifecycle state?
- What dependencies or licensing constraints changed?
- Are interface freezes and downstream handoffs complete?
- Is owner/reviewer/support capacity sufficient?
- Should a component be simplified, delayed, replaced, or abandoned?

The long-term vision is fixed; implementation choices remain empirical.

## 16. Market, UI, agent, and release sequencing

- Market opportunities remain outside the executable backlog until promoted through evidence and ownership.
- Native UI work completes toolkit-neutral contracts, equivalent framework prototypes, page-surface/accessibility/IME/crash evidence, licensing review, and ADRs before framework lock-in.
- Agents execute only ready `TASK-*` records and cannot self-approve or self-merge production work.
- Preview gates activate at M5 only after update, security, migration, accessibility, and incident evidence.
- Beta and stable require numeric SLOs, supported-platform contracts, qualified backup ownership, independent review, and human release authority.
