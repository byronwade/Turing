# Documentation Policy

Status: mandatory repository policy  
Scope: all human and software-agent changes  
Primary goal: keep implementation, architecture, risks, requirements, and project claims consistent over time

## 1. Policy

Documentation is a required part of the engineering change, not follow-up work.

Every addition, modification, rename, or removal must update every affected canonical document in the same commit or pull request. A change is incomplete while any document contains a stale claim, path, command, interface, dependency, risk, requirement, status, owner, acceptance criterion, or support statement.

Canonical prose belongs under `docs/`. Root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md`, plus GitHub workflow templates under `.github/`, are discovery and control exceptions.

The policy requires completeness, not artificial churn. Do not edit unrelated documents merely to show activity. Review all affected documents and change the ones whose truth changed.

## 2. Sources of truth

Each fact should have one canonical owner.

| Information | Canonical owner |
|---|---|
| project mission and prohibited claims | `blueprint-v1/01-charter-and-principles.md` |
| Chrome-class capability inventory | `blueprint-v1/02-capability-parity.md` |
| language and dependency policy | `blueprint-v1/03-language-and-dependency-strategy.md` |
| process model and architecture | `blueprint-v1/04-system-architecture.md` |
| web engine design | `blueprint-v1/05-web-engine.md` |
| JavaScript and WebAssembly design | `blueprint-v1/06-javascript-runtime.md` |
| networking, storage, media, credentials, platform services | `blueprint-v1/07-network-storage-media.md` |
| threat model, sandbox, privacy, site isolation | `blueprint-v1/08-security-and-sandbox.md` |
| performance, memory, energy, tab-lifecycle measurement | `blueprint-v1/09-performance-memory.md` |
| AI observation, grant, action, provider, audit model | `blueprint-v1/10-ai-agent-platform.md` |
| UI, accessibility, DevTools, automation | `blueprint-v1/11-product-ui-devtools.md` |
| compatibility, conformance, fuzzing, quality gates | `blueprint-v1/12-testing-compatibility.md` |
| build, signing, update, release, incident operations | `blueprint-v1/13-build-release-operations.md` |
| milestones and work sequencing | `blueprint-v1/14-roadmap-work-breakdown.md` |
| program risks | `blueprint-v1/15-risk-register.md` and `blueprint-v1/machine/risks.json` |
| governance and contribution process | `blueprint-v1/16-governance-contributing.md` and `contributing.md` |
| architectural decisions | `blueprint-v1/17-architecture-decisions.md` |
| primary references | `blueprint-v1/18-source-bibliography.md` |
| work packages | `blueprint-v1/19-initial-backlog.md` and `blueprint-v1/machine/backlog.json` |
| completion criteria | `blueprint-v1/20-definition-of-done.md` |
| product requirements | `blueprint-v1/21-product-requirements.md` and `blueprint-v1/machine/requirements.json` |
| research methods and unresolved questions | `blueprint-v1/22-research-program.md` |
| repository structure and file placement | `repository-map.md` |
| security reporting | `security.md` |
| executable prototype purpose | `prototype.md` |
| agent operating rules | root `AGENTS.md` |

Indexes summarize and link; they must not silently redefine the canonical owner.

### Detailed engineering books

The directories `engine/`, `javascript/`, `security-engine/`, `developer-experience/`, `api-design/`, `performance/`, `ai/`, and `competitive/` are detailed research and design companions. They expand subsystem contracts, experiments, evidence requirements, risks, and implementation questions. They do not replace Blueprint ownership or change requirement, risk, ADR, milestone, backlog, or support status unless the owning records are updated in the same change.

Where a Blueprint topic has a detailed book, both must be inspected. The Blueprint owns the accepted summary; the book owns detailed research depth and must link back to the Blueprint.

## 3. Mandatory impact review

Every change must answer:

1. What user-visible and developer-visible behavior changes?
2. What architecture, process, IPC, lifecycle, data-flow, or privilege boundary changes?
3. What security, privacy, origin, profile, credential, update, logging, extension, DevTools, automation, or agent authority changes?
4. What compatibility, platform, accessibility, localization, media, printing, PDF, enterprise, or migration behavior changes?
5. What performance, memory, startup, latency, energy, tab lifecycle, or resource-accounting behavior changes?
6. What dependencies, licenses, unsafe code, generated code, schemas, protocols, profile formats, or build/release steps change?
7. Which Blueprint chapters, detailed books, requirements, risks, ADRs, milestones, work packages, tests, benchmarks, support statements, and registries are affected?
8. Which documents were updated, and why are the remaining documents unaffected?

Writing “none” is acceptable only after the category was considered.

## 4. Change matrix

At minimum, inspect these documents:

| Change | Documents and registries |
|---|---|
| product scope or claim | charter, capability parity, requirements, risk register, competitive scorecard |
| dependency or language | language strategy, bibliography, build/release, license notices |
| architecture, process role, IPC, lifecycle | system architecture, threat model, security-engine book, ADRs, requirements, risks |
| engine parsing, DOM, CSS, layout, paint | web engine, engine book, compatibility/testing, roadmap, backlog |
| JavaScript, GC, JIT, WebAssembly, bindings | JavaScript runtime, JavaScript book, threat model, compatibility/testing |
| network, storage, credential, media, PDF, printing | platform services, threat model, engine media chapter, compatibility/testing |
| performance or memory optimization | performance contract, performance book, benchmark schema, roadmap, risks |
| AI capability | AI platform, AI book, threat model, agent schema, requirements, risks |
| UI, accessibility, DevTools, automation | UI/DevTools, developer-experience and API books, testing, requirements, capability parity |
| signing, update, release, telemetry, incident response | build/release, threat model, security policy, security-engine book, risks |
| new or changed requirement | requirements prose and JSON, roadmap, backlog, tests, affected detailed books |
| new or changed risk | risk prose and JSON, mitigation owner, affected roadmap/ADR/books |
| new or changed ADR | ADR document, affected architecture, detailed books, and risk documents |
| new or changed work package | backlog prose and JSON, dependencies, milestones, detailed design owner |
| repository file or directory added/removed/renamed | repository map, documentation index, links, validation, CI |
| command, tool, or workflow changed | contributing guide, repository map, agent instructions, CI docs |

This matrix is a floor. Cross-cutting changes usually require more than one row.

## 5. Research documentation

Research entries must record enough context to reproduce the conclusion:

- question and decision pressure;
- source title, owner, version, retrieval date, and stable locator;
- tested commit, build flags, platform, hardware, and configuration;
- method, workload, sample count, and statistical treatment;
- observations separated from inferences;
- contradictory evidence and unresolved questions;
- security, licensing, accessibility, compatibility, performance, and operational implications;
- resulting Blueprint, detailed-book, requirement, risk, ADR, benchmark, backlog, or design changes.

Use primary sources where possible. Secondary material may identify leads but should not be the sole authority for security or architecture decisions. Dated product and project studies must state when information may become stale.

## 6. Feature and status language

Use exact maturity labels: `unplanned`, `specified`, `prototype`, `partial`, `conformant-subset`, `release-gated`, or `supported`.

Do not use “implemented,” “compatible,” “secure,” “production-ready,” “faster,” “lower memory,” “Chrome-equivalent,” “number one,” or similar unqualified language unless the required evidence and comparison definition are present.

Document unsupported cases, failure behavior, recovery behavior, and residual risk beside successful behavior.

## 7. File lifecycle

### Add

- Place new prose under `docs/` as `.md`.
- Choose one canonical owner or identify the owning Blueprint chapter for a detailed companion.
- Link it from `docs/README.md` or an indexed child.
- Update `repository-map.md`.
- Add required-file or registry validation when omission would make the repository inconsistent.
- Add source and regeneration information for generated or machine-readable files.

### Rename or move

- Update all relative links, commands, issue templates, workflow paths, source references, and validation rules.
- Preserve history through a Git rename when using a local checkout.
- Update `docs/README.md` and `repository-map.md`.
- Do not leave duplicate compatibility copies unless a platform requires a short pointer file.

### Remove

- Remove or replace every inbound reference.
- Record why the information is obsolete or where it moved.
- Update Blueprint chapters, detailed books, requirements, risks, ADRs, milestones, and support statements that depended on it.
- Update `docs/README.md`, `repository-map.md`, and validation.

## 8. Review and enforcement

`tools/validate_blueprint.py` enforces repository structure, required documents, detailed-book topology, JSON registries, Markdown hygiene, link integrity, index coverage, legacy-path removal, and source hygiene.

`tools/check_documentation_change.py` enforces the minimum same-change rule in pull requests:

- non-documentation changes require a canonical Markdown change under `docs/`;
- added, deleted, or renamed paths require `docs/repository-map.md`;
- documentation topology changes require `docs/README.md`;
- prototype changes require `docs/prototype.md`.

Automation cannot prove semantic completeness. Reviewers and agents remain responsible for the full impact matrix.

During the current single-owner research phase, the repository owner may use the controlled documentation-only direct-main exception defined in [Blueprint 16](blueprint-v1/16-governance-contributing.md). The exception does not apply to implementation, accepted architecture, machine-registry status, security fixes, release operations, or embargoed findings, and it never bypasses validation.

## 9. Definition of done

Documentation is complete when:

- all affected Blueprint chapters, detailed books, and policies agree;
- machine-readable and prose records agree;
- every new or moved document is indexed;
- all relative links resolve;
- no obsolete path or claim remains;
- commands are executable;
- risks and unsupported behavior are explicit;
- evidence supports status and performance claims;
- validation passes.

## 10. Detailed research library coverage

Changes to networking, storage, media/documents, native platform integration, accessibility, release operations, extensions/enterprise/sync, web-platform governance, benchmark operations, quality assurance, or everyday product workflows must inspect the corresponding detailed book in addition to the owning Blueprint chapters. Performance, security, and developer-tool changes must also inspect their advanced chapters for locality, allocation, IPC, startup, profiling, side channels, native/JIT containment, capability provenance, replay, reduction, SDKs, and cross-domain diagnostics.

A dated research report remains evidence, not an accepted decision. Book topology, child links, repository mapping, research logs, bibliography, questions, and validation change together.

## Professional control-plane records

Changes must inspect the professional ownership, traceability, phase, review, and exception registries under `blueprint-v1/machine/`, the project-buildout handbook, and the relevant technology, Plug-in, embedding, and template records. Research recommendations never silently change accepted implementation or support status.

<!-- MARKET-STRATEGY-2026-07 -->
## Market opportunity changes

A new or changed `OP-*` record requires synchronized updates to the market-strategy book, dated evidence report or source notes, feature-opportunity registry, research log, ownership, relevant product/security/performance/accessibility/AI/Plug-in/embedding documents, and validation. Promotion to accepted scope additionally requires requirements, risks, ADRs where needed, work packages, traceability, and support statements.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI documentation impact

A change to shell state, commands, toolkit adapters, design tokens, components, page surfaces, windowing, input, accessibility, backend/renderer features, design-lab tooling, or UI budgets updates the Native UI Runtime book, repository map, framework/budget registries, pre-build readiness, affected Blueprint chapters, tests, benchmarks, ownership, and support language in the same change.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent and release-control impact

Changes produced by agents must include task/run provenance and independent evidence when applicable. Any production-scope, platform, SLO, release-channel, update, incident, support, signing, or legal change must update `docs/production-readiness/` and its machine registries. Any agent-authority, task, tool, credential, provenance, review, or escalation change must update `docs/agent-execution/`.
