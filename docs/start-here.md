# Turing Browser Program — Start Here

Turing is the working codename for an independent, Rust-first browser and web-engine program. The project is deliberately not a Chromium, WebKit, Gecko, Electron, CEF, operating-system web-view, or remote-rendering wrapper.

The long-term target is broad modern-web compatibility, a materially lower and more accountable resource footprint under large tab sets, developer-grade tooling, a restrained native interface, and an AI-agent surface designed as a security boundary rather than hidden automation.

This repository is an architecture, research, and execution baseline, not a production browser. A browser that safely handles arbitrary hostile web content is an operating-system-scale project. Every release must state exactly which standards, security controls, media formats, accessibility functions, extension APIs, enterprise controls, platform integrations, and update obligations are implemented and independently tested.

## Reading order

1. [Documentation policy](documentation-policy.md)
2. [Blueprint v1 index](blueprint-v1/README.md)
3. [Charter and principles](blueprint-v1/01-charter-and-principles.md)
4. [Capability parity](blueprint-v1/02-capability-parity.md)
5. [Language and dependency strategy](blueprint-v1/03-language-and-dependency-strategy.md)
6. [System architecture](blueprint-v1/04-system-architecture.md)
7. [Security and sandbox](blueprint-v1/08-security-and-sandbox.md)
8. [Performance and memory](blueprint-v1/09-performance-memory.md)
9. [AI and agent platform](blueprint-v1/10-ai-agent-platform.md)
10. [Roadmap and work breakdown](blueprint-v1/14-roadmap-work-breakdown.md)
11. [Risk register](blueprint-v1/15-risk-register.md)
12. [Detailed engineering books](README.md#detailed-engineering-books)
13. [Active research](research/README.md)
14. [Repository map](repository-map.md)

The Blueprint is the normative overview. The detailed books expand implementation research and evidence requirements without silently changing accepted decisions.

## Non-negotiable definitions

**Independent engine** means Turing owns the DOM, CSS/style system, layout, display-list construction, browser process model, navigation lifecycle, JavaScript integration, permissions, storage partitioning, developer tooling, and agent protocol. It does not mean reimplementing cryptography, Unicode tables, font shaping, image codecs, compression, or operating-system sandbox primitives without a security justification.

**Chrome-class capability** is a tracked destination, never a marketing shortcut. It includes the web platform, accessibility, internationalization, media, printing, PDF, downloads, credentials, extensions, developer tools, automation, sync, updates, enterprise policy, crash recovery, security response, and distribution—not merely successful page rendering.

**Low memory** means measured private working set and resident memory on a published workload, with tab lifecycle, process count, site-isolation state, page types, background activity, and discard policy disclosed. Discarding most tabs is not represented as equivalent to keeping hostile sites fully live.

**AI assistance** is capability-scoped. Models do not receive ambient access to cookies, credentials, cross-origin content, downloads, local files, clipboard, camera, microphone, payments, messages, or destructive actions. Page content and model output cannot expand authority. Consequential operations require deterministic policy checks and visible confirmation where specified.

**Beautiful UI** means a restrained, coherent, accessible, platform-appropriate interface with excellent keyboard behavior, diagnostics, and latency. Visual polish does not excuse hidden work, inaccessible controls, excessive memory, or misleading security states.

**Number one** means a current, reproducible, multi-dimensional result across compatibility, latency, memory, energy, security, accessibility, stability, developer APIs, everyday usability, and open-source health. It never means one synthetic benchmark or a comparison with unequal feature/security settings.

## Current documentation state

The repository currently contains:

- the normative product and engineering Blueprint;
- nineteen detailed engineering and competitive research books;
- dated engine-landscape and documentation-gap research;
- machine-readable requirements, risks, work packages, process capabilities, benchmark and agent-action schemas;
- repository validation and documentation-governance checks;
- a dependency-free Rust architecture prototype.

Detailed books now cover networking, storage, media/documents, native platforms, accessibility, release operations, extensions/enterprise/sync, open-web governance, benchmark operations, quality assurance, everyday product experience, browser-engine internals, JavaScript runtime/compiler design, security containment and response, DevTools/developer workflows, API conventions, performance/memory/energy, AI agents and tools, and competitive engine/product studies. These are research and design baselines, not evidence that the systems exist.

## Current implementation state

The prototype encodes typed process roles, bounded messages, legal tab lifecycle transitions, ordered rendering stages, scoped network identity, and deterministic agent authorization. It does not parse HTML, render pages, execute JavaScript, create native windows, or open network connections.

## Current safety statement

Do not use current or early Turing builds for sensitive accounts, private data, financial activity, or arbitrary hostile browsing. General safety claims remain prohibited until sandboxing, site isolation, update signing, fuzzing, compatibility, incident response, and independent review gates pass.

## Documentation rule

All canonical project documentation lives under `docs/`. Every feature, code, configuration, dependency, interface, risk, requirement, benchmark, or repository-structure change must update every affected document in the same change. See [the documentation policy](documentation-policy.md) and the root [`AGENTS.md`](../AGENTS.md).
