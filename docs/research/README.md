# Turing Research Index

Status: active evidence index  
Owner: research and architecture  
Update rule: add every durable study here and record material conclusions in the research log

This directory contains dated research artifacts that inform, challenge, or validate the Turing Blueprint. A study is not a substitute for a requirement, risk, ADR, benchmark manifest, or implementation plan. Recommendations remain hypotheses until the decision owner accepts them through the normal documentation process.

## Current studies

| Study | Question | Status |
|---|---|---|
| [Browser engine landscape and Turing excellence strategy — July 2026](browser-engine-landscape-2026-07.md) | Which lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should shape a top-tier independent engine for developers and everyday users? | Research baseline; recommendations require experiments |

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

## Program links

- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Primary-source bibliography](../blueprint-v1/18-source-bibliography.md)
- [Performance and memory contract](../blueprint-v1/09-performance-memory.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Documentation policy](../documentation-policy.md)

## Next study queue

The next evidence reports should cover:

- fixed-hardware process and memory baselines across current stable engines;
- developer workflow latency and protocol coverage across CDP, WebDriver BiDi, Firefox Remote Protocol, and WebKit Inspector Protocol;
- DOM, style, fragment, and display-list representation experiments in Rust;
- adaptive versus fixed parallelism for parsing, style, layout, raster, and JavaScript compilation;
- startup and process-launch cost by platform;
- accessibility-tree architecture and assistive-technology latency;
- browser-shell UI stacks, native integration, and power behavior;
- open-source governance models, contributor throughput, security response, and release sustainability.
