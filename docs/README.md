# Turing Documentation

This directory is the canonical source of truth for the Turing browser program. Root-level Markdown is limited to repository discovery and agent-control files. Product, architecture, engineering, research, security, performance, compatibility, and operating documentation belongs here.

Documentation changes are part of the implementation. Every addition, modification, rename, or removal must update every affected document, index, requirement, risk, ADR, backlog entry, registry, and support statement in the same change.

## Orientation and operating policy

| Document | Purpose |
|---|---|
| [Start here](start-here.md) | Project scope, current maturity, definitions, and reading order |
| [Documentation policy](documentation-policy.md) | Same-change documentation rules, impact mapping, review requirements, and enforcement |
| [Repository map](repository-map.md) | Durable directory structure, source-of-truth boundaries, and file-placement rules |
| [Contributing](contributing.md) | Engineering process, pull-request evidence, coding standards, and provenance |
| [Security policy](security.md) | Current security status, private reporting, scope priorities, and disclosure |
| [Architecture prototype](prototype.md) | Exact purpose, commands, invariants, and limitations of `prototype/` |
| [Research log](research-log.md) | Chronological record of material research and documentation-governance decisions |
| [Research index](research/README.md) | Dated evidence reports, competitive studies, hypotheses, and experiment queues |
| [Blueprint v1](blueprint-v1/README.md) | Complete product, engine, runtime, platform, security, performance, AI, UI, testing, release, roadmap, risk, requirements, and research baseline |

## Active research

| Study | Status and purpose |
|---|---|
| [Browser engine landscape and Turing excellence strategy — July 2026](research/browser-engine-landscape-2026-07.md) | Primary-source comparison of Chromium, WebKit, Gecko, Servo, and Ladybird; proposed performance, API, standards, open-source, and measurement strategy |

Research reports are evidence artifacts, not automatic architecture decisions. Any recommendation that changes a requirement, risk, ADR, milestone, interface, or support statement must update the owning Blueprint record in the same change.

## Blueprint v1

Blueprint v1 contains the current architecture and execution baseline:

1. [Charter and principles](blueprint-v1/01-charter-and-principles.md)
2. [Capability parity](blueprint-v1/02-capability-parity.md)
3. [Language and dependency strategy](blueprint-v1/03-language-and-dependency-strategy.md)
4. [System architecture](blueprint-v1/04-system-architecture.md)
5. [Web engine](blueprint-v1/05-web-engine.md)
6. [JavaScript runtime](blueprint-v1/06-javascript-runtime.md)
7. [Network, storage, media, and platform services](blueprint-v1/07-network-storage-media.md)
8. [Security, privacy, and sandbox](blueprint-v1/08-security-and-sandbox.md)
9. [Performance, memory, energy, and the 30-tab contract](blueprint-v1/09-performance-memory.md)
10. [AI assistant and agent platform](blueprint-v1/10-ai-agent-platform.md)
11. [Product UI, accessibility, and developer experience](blueprint-v1/11-product-ui-devtools.md)
12. [Testing, compatibility, fuzzing, and quality gates](blueprint-v1/12-testing-compatibility.md)
13. [Build, release, distribution, and operations](blueprint-v1/13-build-release-operations.md)
14. [Roadmap, milestones, and work breakdown](blueprint-v1/14-roadmap-work-breakdown.md)
15. [Risk register](blueprint-v1/15-risk-register.md)
16. [Governance, contribution, and engineering process](blueprint-v1/16-governance-contributing.md)
17. [Architecture decision records](blueprint-v1/17-architecture-decisions.md)
18. [Primary-source bibliography](blueprint-v1/18-source-bibliography.md)
19. [Initial engineering backlog](blueprint-v1/19-initial-backlog.md)
20. [Definition of done](blueprint-v1/20-definition-of-done.md)
21. [Product requirements](blueprint-v1/21-product-requirements.md)
22. [Research and measurement program](blueprint-v1/22-research-program.md)

Machine-readable requirements, risks, work packages, process capabilities, benchmark manifests, and agent-action schemas live under `blueprint-v1/machine/`. They are evidence-bearing companions to the prose and must change with it.

## Document lifecycle

A new document must:

1. use Markdown and live under `docs/`;
2. have one clear owner and purpose;
3. identify status, assumptions, unsupported behavior, and evidence where applicable;
4. be linked from this index or an indexed child document;
5. avoid duplicating another source of truth;
6. be added to validation when it is required for repository integrity.

A renamed or removed document must have every inbound link, command, registry reference, issue template, and workflow updated in the same change.

See [the documentation policy](documentation-policy.md) for the mandatory impact matrix and CI rules.
