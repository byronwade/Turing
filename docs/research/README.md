# Turing Research Index

Status: active evidence index  
Owner: research and architecture  
Update rule: add every durable study here and record material conclusions in the research log

This directory contains dated research and implementation-evidence artifacts that inform, challenge, or validate the Turing Blueprint. A study is not a substitute for a requirement, risk, ADR, benchmark manifest, or implementation plan. Recommendations remain hypotheses until the decision owner accepts them through the normal process.

## Current studies

| Study | Question | Status |
|---|---|---|
| [Browser engine landscape and Turing excellence strategy — July 2026](browser-engine-landscape-2026-07.md) | Which lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should shape a top-tier independent engine? | Research baseline; recommendations require experiments |
| [Documentation expansion audit — July 2026](documentation-expansion-audit-2026-07.md) | Where was the Blueprint too compressed and which detailed books were required? | Completed documentation audit |
| [Performance, security, developer, and missing-systems expansion audit — July 2026](performance-security-developer-expansion-audit-2026-07.md) | Which cross-cutting engineering areas required detailed ownership? | Completed documentation audit |
| [Professional buildout gap audit — July 2026](professional-buildout-gap-audit-2026-07.md) | Which ownership, traceability, operations, legal, and sustainability controls were missing? | Professional operating baseline |
| [Browser market gap and differentiation research — July 2026](browser-market-gap-2026-07.md) | Which user and market gaps might distinguish Turing? | `OP-001` through `OP-014`; no automatic promotion |
| [Native UI framework evaluation — July 2026](native-ui-framework-evaluation-2026-07.md) | How can Turing achieve a small native shell with rapid design iteration and no shipped web runtime? | Slint-first hypothesis; no framework adopted |
| [Pre-build readiness gap audit — July 2026](pre-build-readiness-gap-audit-2026-07.md) | Which decisions and executable controls remain before broad implementation? | `PB-001` through `PB-020`; broad implementation not authorized |
| [Agent execution and production-readiness audit — July 2026](agent-execution-production-readiness-audit-2026-07.md) | How must agents, reviews, release authority, and stable gates be constrained? | Operating baseline; production remains blocked |
| [M0 build foundation — July 2026](m0-build-foundation-2026-07.md) | What first source, toolchain, workspace, ledger, and CI foundation can be built without freezing major choices? | Implemented contained-M0 foundation |
| [WP-002 kernel identity, capability, and bounded IPC reference — July 2026](wp-002-kernel-ipc-2026-07.md) | Can one generated schema drive deny-by-default roles, capabilities, routes, limits, and a deterministic Rust policy oracle? | M0 reference implemented; transport and sandbox evidence remain |

## Research operating rules

Every study must:

1. state its question, date, owner, scope, and confidence;
2. prefer standards, official project documentation, source repositories, test suites, and primary research;
3. separate observed facts, inferences, proposals, implemented references, and accepted decisions;
4. identify versions or retrieval dates for changing systems;
5. disclose unsupported conclusions, missing data, and conflicting evidence;
6. define experiments that could falsify the recommendation;
7. map findings to relevant Blueprint chapters and research questions;
8. update the [research log](../research-log.md);
9. update requirements, risks, ADRs, work packages, or machine registries only when their meaning changes.

## Detailed research libraries

- [Browser engine engineering](../engine/README.md)
- [JavaScript runtime engineering](../javascript/README.md)
- [Browser security engineering](../security-engine/README.md)
- [Developer experience and DevTools](../developer-experience/README.md)
- [API design](../api-design/README.md)
- [Performance engineering](../performance/README.md)
- [AI and agent engineering](../ai/README.md)
- [Competitive browser and engine studies](../competitive/README.md)
- [Networking engineering](../networking/README.md)
- [Storage and recovery engineering](../storage/README.md)
- [Media, documents, and printing engineering](../media-documents/README.md)
- [Native platform and browser chrome engineering](../platform/README.md)
- [Accessibility engineering](../accessibility/README.md)
- [Build, release, update, and incident operations](../release-operations/README.md)
- [Extensions, enterprise policy, accounts, and sync](../extensions-enterprise/README.md)
- [Open web platform governance](../web-platform/README.md)
- [Fixed-hardware benchmark laboratory](../benchmark-lab/README.md)
- [Quality assurance, conformance, and verification](../quality-assurance/README.md)
- [Everyday product experience](../product-experience/README.md)
- [Native UI runtime and browser chrome](../ui-runtime/README.md)
- [Agent execution and autonomous engineering](../agent-execution/README.md)
- [Production readiness and stable release](../production-readiness/README.md)

These libraries are detailed research and design baselines. They remain subordinate to the owning Blueprint chapters and do not silently change accepted status.

## Program links

- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Primary-source bibliography](../blueprint-v1/18-source-bibliography.md)
- [Performance and memory contract](../blueprint-v1/09-performance-memory.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Documentation policy](../documentation-policy.md)

## Next study and implementation-evidence queue

The next evidence should cover:

- authenticated operating-system IPC transport and wire encoding;
- shared-memory and handle-transfer leases;
- compromised-process malformed-message harnesses;
- platform sandbox and process-launch evidence;
- fixed-hardware process, compatibility, latency, memory, and energy baselines;
- native UI reference-shell bake-off and page-surface composition;
- accessibility-tree architecture and assistive-technology latency;
- DOM, style, fragment, display-list, bytecode, object, and GC representation experiments;
- adaptive versus fixed parallelism;
- startup and process-launch cost by platform;
- contributor throughput, security response, and release sustainability.

## Market, agent, and production programs

The browser-market program uses `RQ-49` through `RQ-54`. Native UI and pre-build research uses `RQ-55` through `RQ-58`. Agent execution and production readiness uses `RQ-59` through `RQ-66`.

The market opportunity registry remains research-only, and the production release-gate registry remains `not_ready_for_production` until deliberately promoted with evidence.
