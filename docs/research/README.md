# Turing Research Index

Status: active evidence index  
Owner: research and architecture  
Update rule: add every durable study here and record material conclusions in the research log

This directory contains dated research artifacts that inform, challenge, or validate the Turing Blueprint. A study is not a substitute for a requirement, risk, ADR, benchmark manifest, or implementation plan. Recommendations remain hypotheses until the decision owner accepts them through the normal documentation process.

## Current studies

| Study | Question | Status |
|---|---|---|
| [Browser engine landscape and Turing excellence strategy — July 2026](browser-engine-landscape-2026-07.md) | Which lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should shape a top-tier independent engine for developers and everyday users? | Research baseline; recommendations require experiments |
| [Documentation expansion audit — July 2026](documentation-expansion-audit-2026-07.md) | Where was the Blueprint too compressed for implementation research, what detailed books were required, and what gaps remain? | Completed documentation audit; no implementation claim |

| [Performance, security, developer, and missing-systems expansion audit — July 2026](performance-security-developer-expansion-audit-2026-07.md) | Which performance, security, developer, systems, operations, quality, benchmark, accessibility, and product areas still required detailed ownership? | Completed documentation audit; recommendations require experiments |

## Research operating rules

Every study must:

1. state its question, date, owner, scope, and confidence;
2. prefer standards, official project documentation, source repositories, test suites, and primary research;
3. separate observed facts, inferences, proposals, and accepted decisions;
4. identify versions or retrieval dates for changing systems;
5. disclose unsupported conclusions, missing data, and conflicting evidence;
6. define experiments that could falsify the recommendation;
7. map findings to the relevant Blueprint chapters and research questions;
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
- [Networking Engineering](../networking/README.md)
- [Storage and Recovery Engineering](../storage/README.md)
- [Media, Documents, and Printing Engineering](../media-documents/README.md)
- [Native Platform and Browser Chrome Engineering](../platform/README.md)
- [Accessibility Engineering](../accessibility/README.md)
- [Build, Release, Update, and Incident Operations Engineering](../release-operations/README.md)
- [Extensions, Enterprise Policy, Accounts, and Sync Engineering](../extensions-enterprise/README.md)
- [Open Web Platform Governance Engineering](../web-platform/README.md)
- [Fixed-Hardware Benchmark Laboratory](../benchmark-lab/README.md)
- [Quality Assurance, Conformance, and Verification Engineering](../quality-assurance/README.md)
- [Everyday Product Experience Engineering](../product-experience/README.md)

These libraries are detailed research and design baselines. They remain subordinate to the owning Blueprint chapters and do not silently change accepted status.

## Program links

- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Primary-source bibliography](../blueprint-v1/18-source-bibliography.md)
- [Performance and memory contract](../blueprint-v1/09-performance-memory.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Documentation policy](../documentation-policy.md)

## Next study queue

The next evidence reports should cover:

- fixed-hardware process, compatibility, latency, memory, and energy baselines across current stable engines;
- developer workflow latency and protocol coverage across CDP, WebDriver BiDi, Firefox Remote Protocol, WebKit Inspector Protocol, and the proposed Turing protocol;
- DOM, style, fragment, display-list, bytecode, object, and GC representation experiments in Rust;
- adaptive versus fixed parallelism for parsing, style, layout, raster, compilation, and proven collector phases;
- startup and process-launch cost by platform;
- platform sandbox and broker evidence;
- accessibility-tree architecture, platform bridges, and assistive-technology latency;
- browser-shell UI stacks, native integration, and power behavior;
- networking, storage, media, PDF, printing, extensions, sync, enterprise, and release-operation detailed books;
- open-source governance models, contributor throughput, security response, and release sustainability.

## Professional buildout audit

- [Professional buildout gap audit — July 2026](professional-buildout-gap-audit-2026-07.md)
- [Technology Stack](../technology-stack/README.md)
- [Turing Plug-ins](../plugins/README.md)
- [Embedding SDK](../embedding/README.md)
- [Professional Project Buildout](../project-buildout/README.md)
