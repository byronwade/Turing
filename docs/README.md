# Turing Documentation

This directory is the canonical source of truth for the Turing browser program. Root-level Markdown is limited to repository discovery and agent-control files. Product, architecture, engineering, research, security, performance, compatibility, and operating documentation belongs here.

Documentation changes are part of the implementation. Every addition, modification, rename, or removal must update every affected document, index, requirement, risk, ADR, backlog entry, registry, and support statement in the same change.

## Orientation and operating policy

| Document | Purpose |
|---|---|
| [Start here](start-here.md) | Project scope, current maturity, definitions, and reading order |
| [Documentation policy](documentation-policy.md) | Same-change documentation rules, impact mapping, review requirements, and enforcement |
| [Repository map](repository-map.md) | Durable directory structure, source-of-truth boundaries, and file-placement rules |
| [Contributing](contributing.md) | Engineering process, pull-request evidence, coding standards, and provenance |
| [Security policy](security.md) | Current security status, private reporting, scope priorities, and disclosure |
| [Architecture prototype](prototype.md) | Exact purpose, commands, invariants, and limitations of `prototype/` |
| [Research log](research-log.md) | Chronological record of material research and documentation-governance decisions |
| [Research index](research/README.md) | Dated evidence reports, competitive studies, hypotheses, and experiment queues |
| [Blueprint v1](blueprint-v1/README.md) | Normative product, engine, runtime, platform, security, performance, AI, UI, testing, release, roadmap, risk, requirements, and research baseline |

## Detailed engineering books

The Blueprint owns accepted high-level architecture. These books expand it into subsystem contracts, experiments, invariants, evidence requirements, risks, and implementation questions. They do not silently change requirements or make implementation claims.

| Book | Scope |
|---|---|
| [Browser engine engineering](engine/README.md) | Pipeline artifacts, HTML/DOM, CSS, invalidation, layout, paint, GPU, text, media, input, accessibility, memory, and observability |
| [JavaScript runtime engineering](javascript/README.md) | Front end, bytecode, interpreter, values, objects, inline caches, GC, JIT, Web IDL, event loop, WebAssembly, testing, and performance |
| [Browser security engineering](security-engine/README.md) | Threat model, isolation, sandbox brokers, native/JIT hardening, side channels, trusted UI, updates, and assurance |
| [Developer experience and DevTools](developer-experience/README.md) | Protocols, workflows, causal tracing, replay, automation, SDKs, reduction, and integrated diagnosis |
| [API design](api-design/README.md) | Identity, authority, bounds, async work, streaming, cancellation, schemas, errors, compatibility, SDKs, authentication, and redaction |
| [Performance engineering](performance/README.md) | Critical paths, locality, allocation, virtual memory, IPC, scheduling, graphics, energy, startup, PGO, profiling, and regression governance |
| [AI and agent engineering](ai/README.md) | Trust boundaries, observations, redaction, actions, grants, confirmation, audit, memory, planning, providers, local models, MCP/tools, and evaluation |
| [Competitive browser and engine studies](competitive/README.md) | Chromium, WebKit, Gecko, Servo, Ladybird, browser-product lessons, valid comparison, and adoption rules |
| [Networking Engineering](networking/README.md) | Request identity, the network service, DNS, proxies, TLS, HTTP, Fetch policy, caches, cookies, streaming transports, downloads, diagnostics, testing, and resource budgets. |
| [Storage and Recovery Engineering](storage/README.md) | Storage keys, quotas, IndexedDB, Cache Storage, service workers, cookies, profile stores, migrations, corruption, encryption boundaries, clearing, repair, and recovery. |
| [Media, Documents, and Printing Engineering](media-documents/README.md) | Sandboxed decoders, images, fonts, audio/video, WebRTC, capture, codecs, hardware acceleration, DRM, PDF, printing, accessibility, licensing, testing, and energy. |
| [Native Platform and Browser Chrome Engineering](platform/README.md) | Browser chrome, windows, surfaces, input, IME, clipboard, drag-and-drop, macOS, Windows, Linux, credentials, notifications, external protocols, packaging, startup, power, and support evidence. |
| [Accessibility Engineering](accessibility/README.md) | Engine semantics, accessible names, text ranges, cross-process trees, platform bridges, browser UI, DevTools, automation, agents, latency, testing, and release gates. |
| [Build, Release, Update, and Incident Operations Engineering](release-operations/README.md) | Build identity, hermetic toolchains, reproducibility, provenance, SBOMs, signing, packaging, updates, rollout, rollback, migrations, crash reporting, incident response, and support lifecycle. |
| [Extensions, Enterprise Policy, Accounts, and Sync Engineering](extensions-enterprise/README.md) | Extension processes, worlds, grants, event execution, rules, native messaging, updates, DevTools and agents, enterprise policy, accounts, encrypted sync, conflicts, schemas, and quotas. |
| [Open Web Platform Governance Engineering](web-platform/README.md) | User needs, standards participation, feature lifecycle, dependency graphs, tests, interoperability, privacy/security/accessibility review, experiments, deprecation, compatibility interventions, and evidence dashboards. |
| [Fixed-Hardware Benchmark Laboratory](benchmark-lab/README.md) | Hardware tiers, OS images, corpora, servers, startup, navigation, input, frame pacing, memory, process topology, 30 tabs, energy, accessibility, developer, agent, recovery, statistics, artifacts, and claims. |
| [Quality Assurance, Conformance, and Verification Engineering](quality-assurance/README.md) | Conformance suites, reduced tests, fuzzing, property/model/formal methods, differential testing, fault injection, chaos, longevity, security assurance, independent review, flakes, and release evidence. |
| [Everyday Product Experience Engineering](product-experience/README.md) | Tabs, groups, workspaces, command field, onboarding, migration, profiles, private sessions, permissions, credentials, agents, resource manager, lifecycle, recovery, settings, updates, support, usability, and accessibility. |
| [Technology Stack and Engineering Toolchain](technology-stack/README.md) | Language map, framework/library candidates, build/test/security tooling, and dependency lifecycle |
| [Turing Plug-in Platform](plugins/README.md) | Native Plug-ins, capabilities, Wasm/WIT, WebExtensions adapter, first-party portfolio, store, SDK, accessibility, and resources |
| [Embedding and Multi-language SDK](embedding/README.md) | Rust API, stable C ABI, generated SDKs, lifecycle, surfaces, host security, packaging, and conformance |
| [Professional Project Buildout and Operating Handbook](project-buildout/README.md) | Phase gates, ownership, review, traceability, repository, coding, schemas, cross-cutting review, operations, source strategy, product, and sustainability |

## Active research

| Study | Status and purpose |
|---|---|
| [Browser engine landscape and Turing excellence strategy — July 2026](research/browser-engine-landscape-2026-07.md) | Primary-source comparison of Chromium, WebKit, Gecko, Servo, and Ladybird; proposed performance, API, standards, open-source, and measurement strategy |
| [Documentation expansion audit — July 2026](research/documentation-expansion-audit-2026-07.md) | Repository-wide gap analysis that created the detailed engineering library and records the next documentation priorities |

| [Performance, security, developer, and missing-systems expansion audit — July 2026](research/performance-security-developer-expansion-audit-2026-07.md) | Adds eleven books and advanced performance, security, and developer research; no implementation or support claim |
| [Professional buildout gap audit — July 2026](research/professional-buildout-gap-audit-2026-07.md) | Ownership, traceability, source strategy, technology, Plug-in, embedding, operations, legal, data, product, and sustainability controls |

Research reports are evidence artifacts, not automatic architecture decisions. Any recommendation that changes a requirement, risk, ADR, milestone, interface, or support statement must update the owning Blueprint record in the same change.

## Blueprint v1

Blueprint v1 contains the current architecture and execution baseline:

1. [Charter and principles](blueprint-v1/01-charter-and-principles.md)
2. [Capability parity](blueprint-v1/02-capability-parity.md)
3. [Language and dependency strategy](blueprint-v1/03-language-and-dependency-strategy.md)
4. [System architecture](blueprint-v1/04-system-architecture.md)
5. [Web engine](blueprint-v1/05-web-engine.md)
6. [JavaScript runtime](blueprint-v1/06-javascript-runtime.md)
7. [Network, storage, media, and platform services](blueprint-v1/07-network-storage-media.md)
8. [Security, privacy, and sandbox](blueprint-v1/08-security-and-sandbox.md)
9. [Performance, memory, energy, and the 30-tab contract](blueprint-v1/09-performance-memory.md)
10. [AI assistant and agent platform](blueprint-v1/10-ai-agent-platform.md)
11. [Product UI, accessibility, and developer experience](blueprint-v1/11-product-ui-devtools.md)
12. [Testing, compatibility, fuzzing, and quality gates](blueprint-v1/12-testing-compatibility.md)
13. [Build, release, distribution, and operations](blueprint-v1/13-build-release-operations.md)
14. [Roadmap, milestones, and work breakdown](blueprint-v1/14-roadmap-work-breakdown.md)
15. [Risk register](blueprint-v1/15-risk-register.md)
16. [Governance, contribution, and engineering process](blueprint-v1/16-governance-contributing.md)
17. [Architecture decision records](blueprint-v1/17-architecture-decisions.md)
18. [Primary-source bibliography](blueprint-v1/18-source-bibliography.md)
19. [Initial engineering backlog](blueprint-v1/19-initial-backlog.md)
20. [Definition of done](blueprint-v1/20-definition-of-done.md)
21. [Product requirements](blueprint-v1/21-product-requirements.md)
22. [Research and measurement program](blueprint-v1/22-research-program.md)

Machine-readable requirements, risks, work packages, process capabilities, benchmark manifests, and agent-action schemas live under `blueprint-v1/machine/`. They are evidence-bearing companions to the prose and must change with it.

## Document lifecycle

A new document must:

1. use Markdown and live under `docs/`;
2. have one clear owner and purpose;
3. identify status, assumptions, unsupported behavior, and evidence where applicable;
4. be linked from this index or an indexed child document;
5. avoid duplicating another source of truth;
6. be added to validation when it is required for repository integrity.

A renamed or removed document must have every inbound link, command, registry reference, issue template, and workflow updated in the same change.

See [the documentation policy](documentation-policy.md) for the mandatory impact matrix and CI rules.
