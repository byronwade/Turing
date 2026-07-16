# Trustworthy AI and Agent Differentiation

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Define a browser-agent product whose authority, observations, provider data flow, cost, and actions remain browser-controlled and auditable.

## Product proposition

Turing should compete on authority control, isolation, explainability, and provider choice—not on unrestricted automation. Read-only assistance can arrive earlier; consequential actions require substantially stronger evidence.

## Task session

An agent session declares:

- the user task and expiry;
- isolated task identity or selected Space;
- allowed origins, frames, document epochs, and data classes;
- observation fields and redaction;
- typed action capabilities and risk classes;
- local or remote provider and transmitted data;
- CPU, memory, network, time, token, and cost budgets;
- confirmation and postcondition policy;
- local audit, stop, and revocation.

## Non-negotiable rules

- Page content, retrieved content, Plug-in output, and model output cannot mint or widen grants.
- Models do not receive raw credentials, cookies, tokens, or signing material.
- Browser-owned trusted UI confirms configured sensitive operations at execution time.
- Agent browsing is visually and technically distinguishable from ordinary browsing.
- No-AI and local-only configurations remain first-class.
- Local inference does not remove prompt-injection risk.
- Audit records are bounded, redacted, user-inspectable, and exportable.

## Evaluation

Use indirect prompt injection, stale-target, cross-origin, memory manipulation, malicious tool output, confirmation fatigue, cancellation, timeout, and resource-exhaustion tests. Report task success and harmful-action rate together. A model benchmark alone cannot establish browser-agent safety.

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
