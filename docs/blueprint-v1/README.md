# Turing Browser Blueprint v1

- Status: architecture and execution baseline
- Working codename: Turing
- License decision: MPL-2.0 for original source, with third-party components retaining their own compatible licenses
- Primary implementation language: Rust
- Engine policy: independent web engine; no Chromium, WebKit, Gecko, Electron, CEF, system web-view, or remote-rendering dependency

## Mission

Build a general-purpose browser that is pleasant for everyday users, exceptional for developers, efficient under many tabs, and safe for both humans and software agents. The product should eventually cover the capability surface expected from Chrome-class browsers, but it must earn each compatibility and security claim through tests and published evidence.

This blueprint separates four layers that are often confused:

1. **Browser product:** windows, tabs, profiles, navigation, permissions, downloads, settings, credentials, sync, updates, accessibility, extensions, DevTools, and agent UX.
2. **Web engine:** HTML parsing, DOM, CSS, layout, painting, compositing, events, editing, forms, images, media integration, accessibility-tree production, and standards behavior.
3. **JavaScript runtime:** parsing, bytecode, interpreter, object model, garbage collection, Web IDL bindings, event loop, modules, WebAssembly, and staged JIT compilation.
4. **Trusted platform:** process broker, IPC, sandbox launch, network and storage services, GPU access, certificate handling, updater, crash reporting, policy engine, and signing.

## Program documents

| Document | Decision or question answered |
|---|---|
| [01 — Charter and principles](01-charter-and-principles.md) | What is being built, what “from scratch” means, and what claims are prohibited? |
| [02 — Capability parity](02-capability-parity.md) | What must exist before “Chrome-equivalent” is a defensible statement? |
| [03 — Language and dependency strategy](03-language-and-dependency-strategy.md) | Why Rust, where C/C++ or platform languages remain justified, and which libraries are acceptable? |
| [04 — System architecture](04-system-architecture.md) | What processes, privilege boundaries, services, and data flows make up the browser? |
| [05 — Web engine](05-web-engine.md) | How will parsing, DOM, style, layout, paint, compositing, events, and accessibility be built? |
| [06 — JavaScript runtime](06-javascript-runtime.md) | How can a new runtime progress from interpreter to competitive JIT without pretending the work is small? |
| [07 — Network, storage, media, and platform services](07-network-storage-media.md) | How are protocols, caches, storage, credentials, codecs, printing, and platform integration handled? |
| [08 — Security and sandbox](08-security-and-sandbox.md) | What is the threat model, process policy, site-isolation model, and vulnerability-response standard? |
| [09 — Performance and memory](09-performance-memory.md) | How will 30-tab efficiency, responsiveness, startup, energy, and regressions be measured honestly? |
| [10 — AI and agent platform](10-ai-agent-platform.md) | How can models observe and act without receiving ambient browser authority? |
| [11 — Product UI and developer experience](11-product-ui-devtools.md) | What makes the browser beautiful, usable, inspectable, keyboard-first, and developer-first? |
| [12 — Testing and compatibility](12-testing-compatibility.md) | Which conformance suites, fuzzers, differential tests, and release gates are required? |
| [13 — Build, release, and operations](13-build-release-operations.md) | How are artifacts built, signed, updated, rolled back, observed, and supported? |
| [14 — Roadmap and work breakdown](14-roadmap-work-breakdown.md) | What sequence can produce useful artifacts while preserving the long-term independent-engine goal? |
| [15 — Risk register](15-risk-register.md) | What can fail technically, legally, operationally, or economically, and how will it be exposed? |
| [16 — Governance and contributing](16-governance-contributing.md) | How are decisions, changes, security reports, ownership, and quality controlled? |
| [17 — Architecture decision records](17-architecture-decisions.md) | Which foundational choices are locked and how can they be revisited? |
| [18 — Source bibliography](18-source-bibliography.md) | Which standards and primary references define the program? |
| [19 — Initial engineering backlog](19-initial-backlog.md) | Which dependency-ordered work packages start the implementation program? |
| [20 — Definition of done](20-definition-of-done.md) | What evidence is required for each class of engineering work? |
| [21 — Product requirements](21-product-requirements.md) | Which product, engine, security, performance, accessibility, AI, and operations requirements are normative? |
| [22 — Research and measurement program](22-research-program.md) | Which unknowns must be researched and how will evidence be recorded? |

## Machine-readable companions

The `machine/` directory contains requirements, risks, work packages, process capabilities, benchmark-manifest schemas, and agent-action schemas. These files are not secondary exports: they must remain consistent with the prose in the same change.

## Supporting research

Dated evidence reports live in the [research index](../research/README.md). They inform and challenge this Blueprint but do not silently change accepted requirements or decisions.

Current report:

- [Browser engine landscape and Turing excellence strategy — July 2026](../research/browser-engine-landscape-2026-07.md)

Recommendations from a report become normative only when the owning Blueprint chapters, ADRs, requirements, risks, work packages, and machine registries are updated with the required evidence.

## Executable bootstrap

The code under `prototype/` is not a rendering engine yet. Its canonical description is [`docs/prototype.md`](../prototype.md). It is a small, buildable Rust model of core invariants:

- process roles are explicit and capabilities are deny-by-default;
- IPC messages are typed and bounded;
- tabs move through legal lifecycle transitions only;
- rendering stages are ordered and invalidation is explicit;
- requests carry profile, top-level site, requesting origin, destination, and credential mode;
- agent actions are authorized against origin, profile, grant lifetime, document epoch, action risk, and confirmation state;
- policy decisions produce auditable reason codes.

## Quality gates

A milestone is not complete because a demo looks correct. Every milestone defines:

- normative requirements with stable identifiers;
- functional and negative tests;
- security properties and sandbox evidence;
- performance baselines and regression thresholds;
- accessibility and localization checks;
- documented unsupported behavior;
- crash, hang, data-loss, and recovery behavior;
- source, license, and reproducibility evidence.

## Documentation governance

All changes to the Blueprint, prototype, registries, workflows, or future implementation must follow the [documentation policy](../documentation-policy.md). Repository additions, removals, and renames must also update the [repository map](../repository-map.md).

## Success criteria

Turing succeeds as an engineering project before it succeeds as a consumer browser if it produces independently useful work: a memory-accountable process model, a standards-driven engine architecture, a capability-safe agent protocol, a reproducible benchmark corpus, and a transparent record of tradeoffs.

Production readiness is a later claim requiring sustained compatibility, security response, signed distribution, incident operations, accessibility evidence, and independent review.
