# Chrome-Class Capability Traceability Map - July 2026

Status: no-claim traceability map; no readiness promotion
Owner: research, product, architecture, security, quality, performance, accessibility, release operations, and program control
Last updated: 2026-07-19

## Question

Can a maintainer trace the long-term Chrome-class browser destination to the current requirements, work packages, pre-build blockers, task handoffs, evidence owners, and unsupported claims without inventing project state?

## Answer

Yes for routing and missing-proof visibility only. The current documentation set is organized enough to show where each Chrome-class capability domain is specified, which `PB-*`, `WP-*`, `TASK-*`, `RQ-*`, and requirement records control it, and what evidence would be needed next. It does not prove Chrome-class capability, Chrome-equivalent behavior, production readiness, safe hostile-web browsing, compatibility, accessibility, security, speed, memory, energy, daily-driver suitability, broad M1 readiness, or all-information-ready-for-building status.

The current implementation evidence remains limited to the M0 repository foundation, typed identity and bounded IPC/kernel reference behavior, toolkit-neutral shell state, and validation tooling described by the indexed M0 reports. No row below is a supported product capability.

## Inputs Inspected

This map is based on repository documentation and machine records current on 2026-07-19:

- [Start Here](../start-here.md);
- [Capability Parity](../blueprint-v1/02-capability-parity.md);
- [Product Requirements](../blueprint-v1/21-product-requirements.md);
- [Roadmap and work breakdown](../blueprint-v1/14-roadmap-work-breakdown.md);
- [Definition of Done](../blueprint-v1/20-definition-of-done.md);
- [Research and measurement program](../blueprint-v1/22-research-program.md);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](../project-buildout/17-build-readiness-task-queue.md);
- [Documentation Readiness Evidence Matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md);
- machine [`requirements.json`](../blueprint-v1/machine/requirements.json), [`backlog.json`](../blueprint-v1/machine/backlog.json), [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json), [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json), and [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json);
- detailed books for [engine](../engine/README.md), [JavaScript](../javascript/README.md), [security](../security-engine/README.md), [networking](../networking/README.md), [storage](../storage/README.md), [media/documents](../media-documents/README.md), [platform](../platform/README.md), [accessibility](../accessibility/README.md), [developer experience](../developer-experience/README.md), [AI](../ai/README.md), [benchmark lab](../benchmark-lab/README.md), [quality assurance](../quality-assurance/README.md), [extensions/enterprise](../extensions-enterprise/README.md), [release operations](../release-operations/README.md), [product experience](../product-experience/README.md), [project buildout](../project-buildout/README.md), [production readiness](../production-readiness/README.md), and [competitive studies](../competitive/README.md).

No new external browser version, market-share, standards, benchmark, or implementation fact is introduced here. This is an internal traceability artifact.

## Traceability Rules

Use this map only to find the owner, blocker, and next evidence packet for a domain. The owning Blueprint chapter, detailed book, machine registry, task manifest, or accepted ADR remains the source of truth.

A Chrome-class claim is not reviewable until every release-critical row has:

- accepted requirements or explicit unsupported support statements;
- implemented behavior in the relevant product, engine, service, platform, update, or tool path;
- conformance, negative, fault, accessibility, security, performance, and recovery evidence appropriate to the row;
- owner and independent review;
- synchronized risks, ADRs, backlog, readiness records, and documentation;
- release and support language that includes proprietary, platform, and unsupported gaps.

## Capability Trace

| Capability domain | Existing source of truth | Current blockers and handoffs | Next proof before any claim | Claim still prohibited |
|---|---|---|---|---|
| Browser shell, windows, tabs, profiles, private sessions, session recovery, and resource controls | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Product Requirements](../blueprint-v1/21-product-requirements.md), [Product Experience](../product-experience/README.md), [Native UI Runtime](../ui-runtime/README.md), requirements `REQ-PROD-001` through `REQ-PROD-005`, `REQ-A11Y-001`, and work packages `WP-004`, `WP-005`, `WP-017` | `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, `PB-016`, `PB-019`, and proposed `TASK-000006`, `TASK-000007`, `TASK-000008` | Native shell adapter evidence, toolkit decision, page-surface proof, rendered component fixtures, profile/session schemas, crash and migration fault tests, accessibility transcripts, resource attribution, and owner-reviewed native/profile/ownership readiness | Usable browser shell, trusted chrome, profile safety, data-loss safety, accessibility readiness, daily-driver, or Chrome-class product claim |
| Web engine HTML, DOM, CSS, layout, paint, compositing, input, editing, and accessibility tree | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Browser Engine](../engine/README.md), [Web Platform Governance](../web-platform/README.md), [Quality Assurance](../quality-assurance/README.md), requirements `REQ-ENG-001` through `REQ-ENG-007`, and work packages `WP-006` through `WP-009` | `PB-002` source strategy remains blocked; broad engine milestones remain M2+; no release-code source baseline is approved | Turing-owned parser, DOM, CSS, layout, paint, accessibility semantics, WPT and reduced tests, fuzzing, resource caps, differential evidence, and source-strategy resolution | Common-site rendering, compatibility, accessibility tree correctness, hostile-content safety, or Chrome-class engine claim |
| JavaScript, WebAssembly, garbage collection, JIT, Web IDL, and runtime debugging | [Capability Parity](../blueprint-v1/02-capability-parity.md), [JavaScript Runtime](../javascript/README.md), [Quality Assurance](../quality-assurance/README.md), requirements `REQ-JS-001` through `REQ-JS-006`, and work packages `WP-010`, `WP-011`, `WP-019` | Source strategy, Web IDL ownership, runtime architecture, GC/JIT security, and Test262 denominator remain unresolved implementation tracks; `WP-019` is planned for M6 and is not executable | ECMAScript frontend/interpreter, exact GC, generated bindings, Test262 coverage, runtime fuzzing, WebAssembly validation, W^X and tier equivalence evidence, no-JIT equivalence, debugger semantics, and owner-reviewed `WP-019` evidence | Modern web app support, JavaScript compatibility, WebAssembly support, JIT performance, or runtime security claim |
| Navigation, networking, cookies, storage, service workers, permissions, site isolation, and web security policy | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Networking](../networking/README.md), [Storage](../storage/README.md), [Security Engineering](../security-engine/README.md), requirements `REQ-NET-001` through `REQ-NET-004`, `REQ-STO-001` through `REQ-STO-003`, `REQ-SEC-001` through `REQ-SEC-003`, and work packages `WP-012`, `WP-013`, `WP-014` | `PB-011`, `PB-012`, `PB-016`, proposed `TASK-000003`, `TASK-000004`, `TASK-000007`; site-isolation and storage behavior remain future milestones | Authenticated bounded IPC, effective renderer sandbox probes, scoped request context, Fetch/CORS/CSP policy tests, partitioned storage, service-worker lifecycle, migration/fault tests, and owner-reviewed IPC/sandbox/profile readiness | Safe arbitrary-web browsing, site isolation, network compatibility, storage safety, permission correctness, or production-security claim |
| Media, PDF, printing, downloads, credentials, devices, capture, and proprietary services | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Media, documents, and printing](../media-documents/README.md), [Platform](../platform/README.md), [Product Experience](../product-experience/README.md), [Security Engineering](../security-engine/README.md), `REQ-PROD-004`, `REQ-NET-001`, `REQ-SEC-001`, `REQ-SEC-004`, and work packages `WP-013`, `WP-014`, `WP-017` | Codec/licensing, DRM, PDF sandboxing, device brokers, credential storage, downloads, update trust, and profile safety remain unresolved | Decoder process and codec matrix, hostile media/PDF tests, printing/accessibility evidence, brokered device/file/capture permissions, credential redaction, quarantine/download safety, update/package readiness, and explicit proprietary-service gaps | DRM parity, codec completeness, PDF safety, printing support, credential/passkey support, device support, or Chrome-equivalent service claim |
| Accessibility and internationalization across browser chrome and web content | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Accessibility](../accessibility/README.md), [Engine](../engine/README.md), [Platform](../platform/README.md), [Quality Assurance](../quality-assurance/README.md), requirements `REQ-A11Y-001`, `REQ-A11Y-002`, `REQ-ENG-006`, and work packages `WP-004`, `WP-009` | `PB-015`, native shell/page-surface blockers, engine semantics, platform bridges, IME and international-text behavior remain unproven | Reference-platform workflows, platform accessibility bridge mappings, manual assistive-technology transcripts, screen-reader coverage, IME/dead-key/bidi/text-shaping proof, focus/zoom/high-contrast/forced-color/reduced-motion evidence, and release-blocking triage | Accessibility readiness, screen-reader support, internationalization support, agent semantic observation correctness, or UI release-path claim |
| DevTools, headless, WebDriver BiDi, automation, protocol, tracing, and diagnostics | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Developer Experience](../developer-experience/README.md), [API Design](../api-design/README.md), [Quality Assurance](../quality-assurance/README.md), requirements `REQ-DEV-001` through `REQ-DEV-003`, and work package `WP-015` | Protocol schema, engine truth, security model, headless parity, transport, redaction, and automation profile safety depend on engine, IPC, sandbox, and DevTools milestones | Versioned protocols, generated clients, bounded messages, authentication, trace causality, replay limits, redaction tests, same-engine headless execution, WebDriver BiDi compatibility track, and workflow evidence | DevTools parity, headless safety, automation compatibility, remote debugging stability, or developer-leadership claim |
| Extensions, enterprise policy, accounts, sync, and ecosystem surfaces | [Capability Parity](../blueprint-v1/02-capability-parity.md), [Extensions, enterprise, accounts, and sync](../extensions-enterprise/README.md), [Security Engineering](../security-engine/README.md), [Product Requirements](../blueprint-v1/21-product-requirements.md), `RQ-32`, and future M6+ roadmap tracks | Extension isolation, background lifetime, policy precedence, sync encryption, account boundary, store/update model, and enterprise support remain future work; no dedicated pre-build readiness item is readying release support | Restricted WebExtensions subset, isolated extension host, host-grant UI, background quota tests, enterprise policy schemas, sync/key recovery/conflict tests, update path, security review, and support statements | Chrome Web Store parity, extension compatibility, enterprise readiness, account/sync support, or background-work safety claim |
| Performance, memory, energy, 30-tab behavior, resource attribution, and competitor comparison | [Performance](../performance/README.md), [Benchmark Lab](../benchmark-lab/README.md), [Chrome-Class Performance Runbook](chrome-class-performance-runbook-2026-07.md), [Benchmark Engine Baseline Harness Readiness Map](benchmark-engine-baseline-harness-readiness-map-2026-07.md), requirements `REQ-PERF-001` through `REQ-PERF-004`, and work packages `WP-005`, `WP-018` | `PB-013`, proposed `TASK-000005`; local no-claim manifests and self-tests exist, but no browser-run benchmark evidence exists; any future claim also depends on `PB-020` closure reconciliation | Owner-approved hardware/OS controls, complete browser pins, implemented launch runner, raw 30-tab and interaction samples, trace packages, resource attribution, statistics-analysis plan and result review, claim bundles, owner-reviewed benchmark readiness, and a `PB-020` closure record that preserves security, accessibility, support, and release boundaries | Faster, lower memory, lower energy, benchmark-ready, competitor-result, Chrome-class performance, resource leadership, or public performance claim |
| Security, privacy, sandboxing, updates, incident response, supply chain, and production readiness | [Security policy](../security.md), [Security Engineering](../security-engine/README.md), [Release Operations](../release-operations/README.md), [Production Readiness](../production-readiness/README.md), [Definition of Done](../blueprint-v1/20-definition-of-done.md), requirements `REQ-SEC-001` through `REQ-SEC-005`, `REQ-OPS-001`, `REQ-OPS-002`, and work packages `WP-003`, `WP-017` | `PB-012`, `PB-017`, `PB-018`, `PB-019`, `PB-020`, proposed `TASK-000004`, `TASK-000008`, `TASK-000009`, `TASK-000010` | Platform sandbox probes, site-isolation evidence, signed update lab, rollback and migration tests, vulnerability intake tabletop, emergency patch dry run, supported-version policy, backup owners, independent security review, and production-readiness review | Secure browser, privacy-safe browser, supported security, production-ready, stable, beta, release, update safety, incident-response readiness, or hostile-browsing safety claim |
| AI and agent authority, observations, actions, providers, grants, audit, and resource budgets | [AI and Agent Platform](../blueprint-v1/10-ai-agent-platform.md), [AI book](../ai/README.md), [Agent Execution](../agent-execution/README.md), [API Design](../api-design/README.md), requirements `REQ-AI-001` through `REQ-AI-005`, and work package `WP-016` | Agent protocol, semantic observation, action schemas, provider data flow, prompt-injection defense, resource budgeting, and policy evaluation remain M6+ tracks and depend on IPC/sandbox/engine semantics | Semantic snapshot schema, redaction evidence, risk classifier, deterministic confirmation, stop/revoke/audit, stale-target tests, prompt-injection corpus, provider manifest, local/remote data-flow proof, and resource impact measurements | Safe browser AI, autonomous action safety, secret safety, agent productivity, model-provider support, or agent Chrome-class claim |
| Build, compile, clean-host reproducibility, release packaging, maintenance capacity, and ownership | [Project Buildout](../project-buildout/README.md), [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md), [Production Readiness](../production-readiness/README.md), [Release Operations](../release-operations/README.md), [Governance](../blueprint-v1/16-governance-contributing.md), `REQ-OPS-001`, `REQ-OPS-002`, and work packages `WP-001`, `WP-017`, `WP-018` | `PB-001` is ready for canonical docs/validation; `PB-009`, `PB-017`, `PB-018`, `PB-019`, `PB-020` remain partial or blocked; proposed `TASK-000002`, `TASK-000008`, `TASK-000009`, `TASK-000010` | Independent fresh-host run, source-tree cleanliness proof, package/update lab, incident rehearsal, named qualified backup owners, task approvals, release evidence, support policy, and production-readiness review | All-information-ready-for-building, broad M1 readiness, release readiness, stable support, production authority, or autonomous-agent completion claim |

## Stop/Resume Procedure

When resuming work toward the Chrome-class target:

1. Start from [Start Here](../start-here.md) and the [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md).
2. Pick the row above that matches the intended claim or implementation scope.
3. Follow the row to the owning Blueprint chapter, detailed book, machine registry, proposed `TASK-*` record, and current research evidence.
4. If the work changes requirement meaning, risk, ADR status, backlog status, task authority, support language, or gate status, update the owning machine registry and validator in the same change.
5. Keep no-claim language beside positive evidence until the required owner-reviewed proof exists.
6. Run the aggregate repository validation before handoff.

## Unsupported Conclusions

This map must not be cited as evidence that:

- Turing is Chrome-class, Chrome-equivalent, or a usable general-purpose browser;
- the project is ready for broad implementation beyond contained M0 work;
- all information needed for building is complete;
- Servo or any other source baseline is approved;
- compatibility, security, accessibility, performance, memory, energy, update, incident-response, profile, extension, enterprise, sync, media, PDF, DevTools, automation, or AI claims are proven;
- open issues or proposed `TASK-*` entries are approved work.

## Drift Triggers

Update this map when any of these change:

- a capability-parity row becomes supported, release-gated, partial, or explicitly unsupported;
- a `PB-*`, `WP-*`, `TASK-*`, `RQ-*`, requirement, risk, ADR, owner, or review rule changes meaning;
- a detailed book adds, removes, or narrows a Chrome-class capability;
- a new evidence packet changes what is required before a public claim;
- the repository adds a new release, beta, stable, daily-driver, security, compatibility, accessibility, benchmark, performance, memory, energy, or production-readiness claim.

## Validation

This traceability map has no standalone validator. It stays checked through:

- relative-link validation in `tools/validate_blueprint.py`;
- index and research-log coverage;
- `PB-020` evidence linkage in [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- the aggregate repository validation command in [Documentation Readiness Evidence Matrix](../project-buildout/18-documentation-readiness-evidence-matrix.md#validation-commands).
