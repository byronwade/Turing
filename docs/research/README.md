# Turing Research Index

Status: active evidence index  
Owner: research and architecture  
Update rule: every durable study is indexed here and mapped to its decision owner

Research artifacts inform, challenge, or validate the Blueprint. They do not replace requirements, risks, ADRs, benchmark manifests, work packages, tasks, or implementation evidence.

## Current studies

| Study | Question | Status |
|---|---|---|
| [Browser engine landscape — July 2026](browser-engine-landscape-2026-07.md) | Which current engine patterns should Turing prototype or reject? | Research baseline |
| [Documentation expansion audit — July 2026](documentation-expansion-audit-2026-07.md) | Which detailed books were missing? | Completed documentation audit |
| [Performance, security, developer, and systems audit — July 2026](performance-security-developer-expansion-audit-2026-07.md) | Which advanced subsystem areas required ownership? | Completed documentation audit |
| [Professional buildout audit — July 2026](professional-buildout-gap-audit-2026-07.md) | Which program controls are required for implementation? | Operating baseline |
| [Browser market gap — July 2026](browser-market-gap-2026-07.md) | Which product gaps justify Turing differentiation? | `OP-001` through `OP-014` remain proposed |
| [Native UI framework evaluation — July 2026](native-ui-framework-evaluation-2026-07.md) | How can trusted chrome remain small and native? | Slint-first hypothesis; no selection |
| [Pre-build readiness audit — July 2026](pre-build-readiness-gap-audit-2026-07.md) | Which controls remain before broad implementation? | `PB-001` through `PB-020` |
| [Agent execution and production readiness — July 2026](agent-execution-production-readiness-audit-2026-07.md) | How may agents implement and how is stable defined? | Agent and release control baseline |
| [M0 build foundation — July 2026](m0-build-foundation-2026-07.md) | What minimum executable repository foundation permits contained development? | Implemented workspace skeleton; broader gates remain |
| [Full implementation game plan audit — July 2026](full-implementation-game-plan-audit-2026-07.md) | Could an agent follow one complete M0–M9 plan without inventing order, authority, evidence, or handoffs? | Execution documentation complete; broad implementation remains gated |

## Research operating rules

Every study records:

1. question, date, owner, scope, and confidence;
2. primary sources and relevant versions;
3. facts, inferences, proposals, and decisions separately;
4. contradictory evidence and unsupported conclusions;
5. falsifiable experiments;
6. security, privacy, accessibility, compatibility, performance, operational, and legal effects;
7. relevant Blueprint chapters, ADRs, requirements, work packages, tasks, and implementation-plan effects;
8. raw evidence and a revisit trigger.

## Detailed research libraries

The [documentation index](../README.md#detailed-engineering-books) links all twenty-seven engineering and product books. They remain subordinate to the owning Blueprint chapters.

The [Implementation Master Plan](../project-buildout/implementation-plan/README.md) connects those books to the M0–M9 sequence, WP graph, task protocol, evidence classes, interface freezes, and handoffs.

## Current implementation-research priorities

1. Independently review and merge accepted bounded foundation work before depending on it.
2. Resolve the Servo/source strategy.
3. Complete the authenticated IPC/wire/negative-harness evidence.
4. Implement the sandbox probe contract and effective reference-platform evidence.
5. Run the native UI reference-shell comparison.
6. Prove page-surface, input, IME, accessibility, crash, and GPU-loss composition.
7. Materialize the fixed-hardware benchmark laboratory.
8. Define profile, Space, session, snapshot, and migration schemas.
9. Establish independent ownership and review capacity.

The M0 build foundation and implementation game plan make these experiments reviewable; they do not settle their results.
