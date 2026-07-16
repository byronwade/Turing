# Market Method, Segments, and Positioning

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Define how Turing interprets browser-market evidence, which users it serves, and what positioning can be defended without overstating demand.

## Market thesis

The durable opportunity is not another collection of isolated browser features. Turing should become the open project browser for people and agents: it remembers the work, explains the cost, and keeps the user in control.

The primary product abstraction is a **Space**: a durable project boundary that can own organization, identity, data, tools, resource policy, Plug-ins, agent authority, synchronization, export, and recovery. This is a hypothesis, not an accepted product requirement.

## Segments

- **Everyday users** need familiar navigation, reliable recovery, understandable privacy, low-friction migration, and useful organization without process-model expertise.
- **Power users** need durable workspaces, high tab counts, keyboard control, resource visibility, and predictable lifecycle behavior.
- **Developers** need causal diagnostics, deterministic replay, multi-profile test environments, and an embeddable open engine.
- **Researchers and students** need comparison, citations, provenance, change tracking, and export.
- **Teams and enterprises** eventually need revocable sharing, policy, audit, identity separation, support, and rapid security response.
- **Agent developers** need typed observations/actions, isolated task profiles, deterministic authorization, and reproducible adversarial evaluation.

## Evidence hierarchy

1. Controlled usability and workflow studies.
2. Reproducible product prototypes and task benchmarks.
3. Official browser documentation and public product behavior.
4. Standards, security research, and platform specifications.
5. Community requests and issue trackers as directional signals.
6. Editorial lists and store popularity as discovery signals only.

Community requests are not a representative survey. Vendor pages describe intended behavior, not independently verified quality. Market-share data measures adoption, not satisfaction. No opportunity is promoted from this book alone.

## Positioning constraints

- Do not claim to be the fastest, safest, most private, or best browser without complete evidence.
- Do not imply Chrome-class compatibility from a feature matrix.
- Do not describe a research opportunity as implemented or committed.
- Do not copy product names, branding, proprietary assets, store descriptions, or implementation code.
- Treat switching cost, migration quality, extension compatibility, and recovery as part of the product—not onboarding details.

## Falsifiable questions

- Do Spaces reduce task-resumption time and identity mistakes compared with existing workspaces?
- Does the Resource Truth Center improve correct decisions without overwhelming everyday users?
- Does a capability-scoped agent increase trust and reduce unintended actions?
- Does open export materially lower switching anxiety?
- Does the Research Canvas reduce source and citation errors?

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
