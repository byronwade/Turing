# Research Log

This log records material research-program and documentation-governance changes. Detailed technical conclusions belong in the owning Blueprint chapter, requirement, risk, ADR, benchmark, backlog entry, or indexed research report.

## 2026-07-16 — Browser engine landscape and excellence strategy

Question:

Which documented lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should guide a top-tier independent engine for developers and everyday users?

Sources and versions:

- official engine architecture and source documentation retrieved 2026-07-16;
- WebDriver BiDi Editor’s Draft dated 2026-07-15;
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

See the study’s experiment queue and unresolved-question section.

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
