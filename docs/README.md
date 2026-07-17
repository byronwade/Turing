# Turing Documentation

This directory is the canonical source of truth for the Turing browser program. Root Markdown is limited to repository discovery and agent-control files. Product, architecture, engineering, research, security, performance, compatibility, and operating documentation belongs here.

Documentation changes are part of implementation. Every change must update every affected document, requirement, risk, ADR, work package, machine registry, owner, test plan, and support statement.

## Orientation and operating policy

| Document | Purpose |
|---|---|
| [Start here](start-here.md) | Scope, maturity, definitions, and reading order |
| [Documentation policy](documentation-policy.md) | Same-change rules and enforcement |
| [Repository map](repository-map.md) | Durable source, documentation, tooling, and evidence layout |
| [Contributing](contributing.md) | Engineering process and provenance |
| [Security policy](security.md) | Current security status and private reporting |
| [Architecture prototype](prototype.md) | Exact purpose and limits of `prototype/` |
| [Research index](research/README.md) | Dated evidence and experiment queue |
| [Blueprint v1](blueprint-v1/README.md) | Normative product and architecture baseline |
| [Pre-build checklist](project-buildout/11-pre-build-readiness-checklist.md) | Current M0 build authorization and remaining blockers |

## Detailed engineering books

| Book | Scope |
|---|---|
| [Browser engine engineering](engine/README.md) | HTML/DOM, CSS, layout, paint, GPU, text, media, input, accessibility, memory, and observability |
| [JavaScript runtime engineering](javascript/README.md) | Parser, bytecode, interpreter, objects, GC, JIT, Web IDL, WebAssembly, testing, and performance |
| [Browser security engineering](security-engine/README.md) | Threats, isolation, brokers, hardening, side channels, updates, and assurance |
| [Developer experience and DevTools](developer-experience/README.md) | Protocols, tracing, replay, automation, SDKs, and diagnosis |
| [API design](api-design/README.md) | Identity, authority, async work, schemas, versioning, SDKs, and redaction |
| [Performance engineering](performance/README.md) | Critical paths, allocation, scheduling, energy, startup, profiling, and regression control |
| [AI and agent engineering](ai/README.md) | Observations, grants, actions, confirmation, audit, planning, providers, and evaluation |
| [Competitive browser and engine studies](competitive/README.md) | Chromium, WebKit, Gecko, Servo, Ladybird, products, and adoption rules |
| [Networking engineering](networking/README.md) | Network service, DNS, proxies, TLS, HTTP, Fetch, cache, cookies, transports, and diagnostics |
| [Storage and recovery engineering](storage/README.md) | Storage keys, quotas, databases, service workers, migrations, corruption, clearing, and repair |
| [Media, documents, and printing](media-documents/README.md) | Decoders, media, WebRTC, codecs, DRM, PDF, printing, testing, and energy |
| [Native platform and browser chrome](platform/README.md) | Windows, surfaces, input, IME, macOS, Windows, Linux, credentials, packaging, and power |
| [Accessibility engineering](accessibility/README.md) | Semantics, platform bridges, browser UI, latency, testing, and release gates |
| [Release operations](release-operations/README.md) | Hermetic builds, provenance, signing, packages, updates, rollback, incidents, and support |
| [Extensions, enterprise, accounts, and sync](extensions-enterprise/README.md) | Isolation, grants, background work, policies, accounts, encryption, conflicts, and quotas |
| [Open web governance](web-platform/README.md) | Standards, tests, interoperability, privacy, accessibility, experiments, and deprecation |
| [Benchmark laboratory](benchmark-lab/README.md) | Hardware, OS images, corpora, startup, latency, memory, energy, statistics, and claims |
| [Quality assurance](quality-assurance/README.md) | Conformance, fuzzing, models, differential tests, chaos, review, and release evidence |
| [Product experience](product-experience/README.md) | Tabs, Spaces, onboarding, permissions, resources, recovery, settings, and usability |
| [Technology stack](technology-stack/README.md) | Languages, frameworks, libraries, build/test tools, and dependency lifecycle |
| [Turing Plug-ins](plugins/README.md) | Capabilities, Wasm/WIT, WebExtensions adapter, first-party portfolio, store, and SDK |
| [Embedding SDK](embedding/README.md) | Rust API, C ABI, generated SDKs, lifecycle, surfaces, packaging, and conformance |
| [Professional buildout](project-buildout/README.md) | Phase gates, ownership, review, traceability, repository, coding, operations, and sustainability |
| [Market strategy](market-strategy/README.md) | Competitive evidence, Spaces, Time Machine, resource truth, agents, migration, and validation |
| [Native UI runtime](ui-runtime/README.md) | Framework selection, toolkit-neutral Rust contracts, page surfaces, design lab, and budgets |
| [Agent execution](agent-execution/README.md) | Task authority, protected review, provenance, independent evidence, rollback, and escalation |
| [Production readiness](production-readiness/README.md) | Stable scope, platforms, SLOs, updates, services, support, signing, and release authority |

## Active research and implementation evidence

| Study | Status and purpose |
|---|---|
| [Browser engine landscape — July 2026](research/browser-engine-landscape-2026-07.md) | Competitive engine architecture and measurement hypotheses |
| [Documentation expansion audit — July 2026](research/documentation-expansion-audit-2026-07.md) | Original documentation gap analysis |
| [Performance, security, developer, and systems audit — July 2026](research/performance-security-developer-expansion-audit-2026-07.md) | Detailed subsystem expansion |
| [Professional buildout audit — July 2026](research/professional-buildout-gap-audit-2026-07.md) | Ownership, traceability, operations, legal, and sustainability |
| [Browser market gap and differentiation research — July 2026](research/browser-market-gap-2026-07.md) | `OP-001` through `OP-014` product hypotheses |
| [Native UI framework evaluation — July 2026](research/native-ui-framework-evaluation-2026-07.md) | Slint-first comparison hypothesis and browser-specific risks |
| [Pre-build readiness audit — July 2026](research/pre-build-readiness-gap-audit-2026-07.md) | `PB-001` through `PB-020` |
| [Agent execution and production-readiness audit — July 2026](research/agent-execution-production-readiness-audit-2026-07.md) | Agent authority and stable-release controls |
| [M0 build foundation — July 2026](research/m0-build-foundation-2026-07.md) | First buildable workspace, toolchain, ledgers, commands, CI, and remaining limits |

Research reports inform decisions but do not silently promote requirements or support claims.

## Blueprint v1

1. [Charter and principles](blueprint-v1/01-charter-and-principles.md)
2. [Capability parity](blueprint-v1/02-capability-parity.md)
3. [Language and dependency strategy](blueprint-v1/03-language-and-dependency-strategy.md)
4. [System architecture](blueprint-v1/04-system-architecture.md)
5. [Web engine](blueprint-v1/05-web-engine.md)
6. [JavaScript runtime](blueprint-v1/06-javascript-runtime.md)
7. [Network, storage, media, and platform services](blueprint-v1/07-network-storage-media.md)
8. [Security, privacy, and sandbox](blueprint-v1/08-security-and-sandbox.md)
9. [Performance, memory, energy, and 30-tab contract](blueprint-v1/09-performance-memory.md)
10. [AI assistant and agent platform](blueprint-v1/10-ai-agent-platform.md)
11. [Product UI, accessibility, and developer experience](blueprint-v1/11-product-ui-devtools.md)
12. [Testing, compatibility, fuzzing, and quality gates](blueprint-v1/12-testing-compatibility.md)
13. [Build, release, distribution, and operations](blueprint-v1/13-build-release-operations.md)
14. [Roadmap and work breakdown](blueprint-v1/14-roadmap-work-breakdown.md)
15. [Risk register](blueprint-v1/15-risk-register.md)
16. [Governance and contributing](blueprint-v1/16-governance-contributing.md)
17. [Architecture decisions](blueprint-v1/17-architecture-decisions.md)
18. [Source bibliography](blueprint-v1/18-source-bibliography.md)
19. [Initial backlog](blueprint-v1/19-initial-backlog.md)
20. [Definition of done](blueprint-v1/20-definition-of-done.md)
21. [Product requirements](blueprint-v1/21-product-requirements.md)
22. [Research and measurement](blueprint-v1/22-research-program.md)

Machine-readable records live under the owning `machine/` directory and must remain synchronized with prose and source.
