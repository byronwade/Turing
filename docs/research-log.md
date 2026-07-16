# Research Log

This log records material research-program and documentation-governance changes. Detailed technical conclusions belong in the owning Blueprint chapter, requirement, risk, ADR, benchmark, backlog entry, indexed engineering book, or dated research report.

## 2026-07-16 — Performance, security, developer, and missing-systems research expansion

Question:

Which browser-scale domains still lacked implementation-grade research contracts after the first eight detailed books?

Sources and versions:

- Turing main at the 95-document engineering-library baseline;
- official WHATWG, W3C, RFC, TC39, WPT, platform, accessibility, reproducible-build, update-security, benchmark, and primary security sources retrieved 2026-07-16;
- existing Turing requirements, risks, work packages, benchmark schema, process capability registry, and prototype.

Method and environment:

Repository-wide architecture and documentation audit followed by deterministic generation of eleven new books, sixteen advanced performance/security/developer chapters, a dated audit, navigation, research questions, bibliography, and validator topology. No implementation, benchmark, conformance run, independent audit, or supported-feature evidence was produced.

Observations:

- network, storage, media/document, platform, accessibility, release, extension/enterprise/sync, web-platform governance, benchmark, quality, and everyday product areas required independent owners and evidence contracts;
- performance leadership requires locality, allocation, virtual-memory, IPC, startup, PGO, tail-latency, causal-trace, energy, pressure, and recovery work;
- security leadership requires native/JIT compartments, side-channel policy, capability provenance, privileged developer/extension/agent controls, trusted UI, phishing defense, update response, and independent assurance;
- developer leadership requires deterministic replay, safe local-workspace integration, automatic reduction, generated SDKs, and cross-domain causal explanations.

Decision:

- add eleven detailed books and 81 chapters;
- add sixteen advanced chapters to performance, security, and developer experience;
- publish the [expansion audit](research/performance-security-developer-expansion-audit-2026-07.md);
- add RQ-26 through RQ-40 and corresponding experiment families;
- strengthen the repository validator to require 204 Markdown documents and nineteen book indexes.

Security/privacy impact:

The research strengthens least authority, partitioning, brokered devices and sockets, native/JIT containment, update integrity, trusted UI, phishing defenses, redaction, private reporting, and explicit unsafe early-release warnings. It changes no current security claim.

Compatibility/accessibility impact:

The expansion adds open-web feature governance, full-denominator conformance, platform accessibility bridges, assistive-technology latency, browser UI workflows, and cross-browser protocol studies. It changes no support matrix.

Performance/memory/energy impact:

The expansion defines measurement and experiments for data locality, allocators, pages, IPC, scheduling, startup, PGO/LTO, GPU, 30 tabs, energy, thermal behavior, background work, and recovery. All proposed advantages remain unmeasured hypotheses.

Affected requirements, risks, ADRs, work packages, and documents:

- requirement count remains 46; risk count remains 40; work-package count remains 18;
- no ADR or status changes;
- all nineteen detailed book indexes, the documentation and Blueprint indexes, repository map, research index/log/program, bibliography, definition of done, policies, and validator are synchronized.

Next evidence required:

Run the fixed-hardware baseline, then execute the representation, process, sandbox, networking, storage, replay, accessibility, release, and product experiments defined by RQ-26 through RQ-40.

## 2026-07-16 — Detailed browser engineering research library

Question:

Where was the initial Blueprint too compressed to guide implementation research, and which detailed subsystem books were required before architecture experiments and code could proceed without inventing undocumented assumptions?

Sources and versions:

- complete Turing Blueprint and repository policies at merge commit `70f151f74a6e199415c7125169230ae1231fb561`;
- official Chromium, WebKit, Gecko, Servo, Ladybird, Rust, platform sandbox, W3C/WHATWG, WPT, BrowserBench, WebDriver BiDi, MCP, and browser-product sources retrieved 2026-07-16;
- W3C Web Platform Design Principles Group Note dated 2026-02-24;
- current MCP specification version identified as 2025-11-25 at retrieval;
- current official product/project pages recorded in the new competitive studies.

Method and environment:

Repository-wide documentation audit. The audit tested whether each major area had enough detail to define identities, inputs, outputs, ownership, lifetimes, invalidation, failure, security, accessibility, limits, observability, experiments, and acceptance evidence. No implementation, fixed-hardware benchmark, or independent security review was performed.

Observations:

- the 22 Blueprint chapters covered the correct browser-scale surface but several combined too many independently reviewable subsystems;
- implementation research needed deeper contracts for rendering, runtime, security, developer protocols, APIs, performance, agents, and comparative adoption;
- the existing documentation governance could support nested engineering books if indexes, repository mapping, research status, and validation were updated together;
- networking, storage, media, PDF, printing, native platform adapters, accessibility bridges, extensions, enterprise/sync, and release operations remain future detailed-book candidates.

Inference:

Keeping the Blueprint as the normative overview while adding indexed detailed books gives the project enough depth for experiments without prematurely freezing implementation. A large body of prose is useful only if status, ownership, evidence, and change discipline remain explicit.

Decision:

- add a [browser engine engineering book](engine/README.md);
- add a [JavaScript runtime engineering book](javascript/README.md);
- add a [browser security engineering book](security-engine/README.md);
- add a [developer experience and DevTools book](developer-experience/README.md);
- add an [API design book](api-design/README.md);
- add a [performance engineering book](performance/README.md);
- add an [AI and agent engineering book](ai/README.md);
- add [competitive browser and engine studies](competitive/README.md);
- publish the [documentation expansion audit](research/documentation-expansion-audit-2026-07.md);
- add RQ-18 through RQ-25 to the research program;
- document the repository-owner, documentation-only direct-main exception requested for the single-owner research phase;
- strengthen repository validation so the complete detailed-book topology is required.

Alternatives rejected:

- expanding only the existing Blueprint chapters, because they would become difficult to navigate and own;
- creating disconnected essays without canonical relationships, because they would drift;
- changing requirements, risks, ADRs, or work-package status based only on desk research;
- treating competitor architecture descriptions or vendor benchmarks as measured Turing evidence.

Security/privacy impact:

The new security and AI books deepen containment, platform sandbox evidence, unsafe/native governance, trusted UI, update response, semantic redaction, tool/MCP boundaries, and adversarial evaluation. They do not change the existing warning that Turing is not safe for hostile or sensitive browsing.

Compatibility/accessibility impact:

The engine, runtime, DevTools, API, competitive, and AI books reinforce standards-first development, full WPT/Test262 accounting, explicit unsupported behavior, semantic accessibility, platform assistive technology, keyboard workflows, and cross-browser automation.

Performance/memory/energy impact:

The performance and subsystem books establish representation budgets, critical-path graphs, semantic resource attribution, adaptive parallelism, cache and pressure policy, tail-latency rules, energy/startup/recovery measurement, and benchmark governance. These remain hypotheses until experiments run.

Licensing/operational impact:

The MPL-2.0 direction is unchanged. External implementations remain research and differential references. Primary sources are linked; no external source code was copied. The expansion increases maintenance load and requires future owners to refresh changing product/project information.

Affected requirements, risks, ADRs, work packages, and documents:

- no requirement, risk, ADR, or work-package status changed;
- root `README.md`;
- `AGENTS.md`;
- `docs/README.md`;
- `docs/start-here.md`;
- `docs/repository-map.md`;
- `docs/research/README.md`;
- `docs/blueprint-v1/README.md`;
- `docs/blueprint-v1/16-governance-contributing.md`;
- `docs/blueprint-v1/18-source-bibliography.md`;
- `docs/blueprint-v1/22-research-program.md`;
- `tools/validate_blueprint.py`;
- all new documents under the eight detailed book directories;
- the dated documentation audit.

Unresolved questions:

See RQ-18 through RQ-25 and each new book's evidence and risk sections. The most immediate empirical gap is the fixed-hardware cross-engine baseline.

Next evidence required:

Execute issue #14, then build the smallest engine-artifact, process-topology, platform-sandbox, protocol, runtime-tiering, and scheduling prototypes needed to falsify the proposed designs.

## 2026-07-16 — Browser engine landscape and excellence strategy

Question:

Which documented lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should guide a top-tier independent engine for developers and everyday users?

Sources and versions:

- official engine architecture and source documentation retrieved 2026-07-16;
- WebDriver BiDi Editor's Draft dated 2026-07-15;
- W3C Web Platform Design Principles Group Note dated 2026-02-24;
- Interop 2026 material published 2026-02-12;
- current WPT and BrowserBench documentation.

Method and environment:

Architecture and standards comparison only. No comparative fixed-hardware performance run was performed, so the report does not rank engines by unmeasured speed, memory, energy, security, or compatibility.

Observations:

- production engines converge on multiprocess isolation, specialized services, staged rendering, and tiered JavaScript execution;
- Chromium provides the broadest developer-protocol and compatibility reference;
- WebKit and Gecko provide additional process, broker, platform, runtime, and observability lessons;
- Servo and Ladybird are the closest independent-engine research peers;
- stable APIs, adaptive parallelism, semantic resource ownership, and standards-aligned tests are major opportunities for differentiation.

Inference:

Turing should pursue a measured synthesis rather than clone one architecture. “Number one” must be a reproducible multi-dimensional scorecard covering compatibility, latency, memory, energy, security, accessibility, stability, developer APIs, and open-source health.

Decision:

- add a permanent [research index](research/README.md);
- publish the [browser engine landscape and Turing excellence strategy](research/browser-engine-landscape-2026-07.md);
- add formal research questions for competitive architecture measurement and developer-protocol design;
- keep all recommendations exploratory until falsifiable experiments and existing decision gates are satisfied.

Security/privacy impact:

The study reinforces site isolation, capability-separated processes, brokered privileged access, authenticated developer attachment, bounded protocols, trusted UI, and data minimization.

Compatibility/accessibility impact:

The study reinforces WPT, Test262, WebDriver BiDi, Interop tracking, explicit unsupported behavior, accessibility semantics, and manual assistive-technology validation.

Performance/memory/energy impact:

The study prioritizes end-to-end user latency, adaptive parallelism, immutable/versioned artifacts, semantic resource accounting, fixed-hardware baselines, tail latency, 30-tab disclosure, and energy measurement.

Licensing/operational impact:

The MPL-2.0 decision is unchanged. The study adds open benchmark data, public protocol schemas, reproducible results, and contributor-health metrics as leadership criteria.

Affected records:

- root `README.md`;
- `docs/README.md`;
- `docs/repository-map.md`;
- `docs/blueprint-v1/README.md`;
- `docs/blueprint-v1/22-research-program.md`;
- this research log;
- the two documents under `docs/research/`.

Unresolved questions:

See the study's experiment queue and unresolved-question section.

Next evidence required:

A fixed-hardware, versioned, reproducible reference-engine baseline using equivalent workloads, security settings, process disclosure, and compatibility accounting.

## 2026-07-15 — Canonical documentation system

Decision:

- place canonical prose under `docs/`;
- retain root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md` only for discovery and repository control;
- place the complete Blueprint under `docs/blueprint-v1/`;
- keep machine-readable requirements, risks, backlog, process capabilities, benchmark manifests, and agent-action schemas beside the Blueprint;
- require same-change documentation for code, configuration, dependencies, interfaces, features, risks, and repository structure;
- add static link, location, registry, index-coverage, and diff-based documentation validation;
- remove temporary transfer and self-modifying bootstrap machinery from the durable repository structure.

Rationale:

A browser project has too many cross-cutting security, compatibility, performance, accessibility, and operational obligations for documentation to be optional or scattered. Centralizing canonical prose and requiring impact review reduces silent drift while preserving standard GitHub discovery files.

Affected records:

- root `AGENTS.md`;
- `docs/documentation-policy.md`;
- `docs/repository-map.md`;
- `docs/contributing.md`;
- GitHub issue and pull-request templates;
- repository validation workflow and tools.

Residual risk:

Automation can verify location, links, registries, and minimum same-change behavior, but it cannot prove that prose is semantically complete. Human and agent review must still apply the full impact matrix.

## Entry template

```text
## YYYY-MM-DD — Topic

Question:
Sources and versions:
Method and environment:
Observations:
Inference:
Decision:
Alternatives rejected:
Security/privacy impact:
Compatibility/accessibility impact:
Performance/memory/energy impact:
Licensing/operational impact:
Affected requirements, risks, ADRs, work packages, and documents:
Unresolved questions:
Next evidence required:
```
