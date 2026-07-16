# Actions, Grants, Confirmation, and Audit

Status: research and design baseline  
Owner: agent authorization and execution  
Purpose: Make every browser effect typed, current, scoped, reviewable, and resistant to prompt injection.

## Relationship to the Turing program

This document expands AI-GATE-1, AI-GATE-3, AI-GATE-5, and AI-GATE-6 in [Blueprint 10](../blueprint-v1/10-ai-agent-platform.md).

## Action schema

Actions cover navigation, tab/window/workspace state, focus/scroll/selection, element activation, text editing, form controls, waits, downloads/uploads, bookmarks/notes, developer evaluation, permission/device requests, credentials, external applications, extension/tool calls, and content publication. Every action identifies session, principal, grant, profile, target/frame, document epoch, semantic locator, payload, preconditions, risk class, timeout, idempotency, and expected effect.

Generic arbitrary IPC, shell, filesystem, or trusted-event injection actions are prohibited.

## Grant model

A grant is unforgeable, revocable, and no broader than user intent. It scopes observation classes, action classes, profile, origins/sites, frames, target resources, selected files/destinations, time-to-live, action count, money/cost, network, token, CPU/GPU, navigation, mutation, and confirmation policy.

Grant persistence is opt-in and cannot silently survive private-session closure, profile switch, provider change, or browser restart.

## Risk classification

Class 0 observes granted non-sensitive data. Class 1 performs reversible local organization. Class 2 has external but low-impact effect. Class 3 sends, publishes, uploads, deletes cloud data, changes account state, grants permissions, exposes source, runs code, or initiates purchases. Class 4 covers high-risk financial, security, credential, recovery, device, destructive bulk, legal, medical, government, privilege, warning-bypass, or software-install actions.

Deterministic context can elevate risk. The model cannot lower it.

## Confirmation

Confirmation is protected browser UI showing agent/provider, exact action, origin/account/profile, destination, data affected, amount, files, permission/device, risk, page excerpt, batch scope, and alternatives. The page cannot cover or activate it; the agent cannot approve it.

Approval is bound to the displayed action hash, current document/target epoch, user identity, expiry, and one-time or bounded batch scope. Material changes require a new confirmation.

## Execution transaction

The executor re-resolves the target, checks origin, visibility, interactability, enabled/read-only state, user activation, policy, grant, epoch, budgets, and confirmation. It applies the smallest operation, observes stabilization, verifies expected postcondition where possible, and returns structured effect.

Navigation or target mutation between proposal and execution fails closed or re-plans without carrying confirmation to a different effect.

## Audit

Append-only local records contain session/principal/provider/model, task/grant summary, observation version/hash, proposed action, risk, policy reason, confirmation presentation/result, preconditions, target epoch, execution, effect, errors, cost/resources, stop/revoke, and delegation chain. Raw sensitive content is omitted or encrypted/retained only under explicit policy.

Users can inspect, export redacted records, and clear history according to policy. Enterprise retention is separately disclosed.

## Batching and delegation

Batch confirmation is limited to predictable homogeneous actions with explicit count, targets, expiry, and stop. It never covers unknown future destinations, financial/security changes, or broad destructive work. Child-agent grants can only narrow parent authority. One agent cannot approve another's confirmation.

## Non-negotiable invariants

- Every effect maps to a typed action and deterministic policy path.
- Grants are scoped, bounded, revocable, and non-expandable by model/page/tool output.
- Class 3/4 actions follow configured confirmation and bind to exact current effect.
- Stale targets, origins, frames, and document epochs fail closed.
- Agents cannot approve trusted confirmation UI.
- Audit records capture policy and effects without default secret retention.

## Required evidence

- Schema, policy, risk-classifier, grant-narrowing, stale-target, and idempotency tests.
- Adversarial prompt injection, page swap, UI spoofing, cross-origin, and malicious-tool cases.
- Confirmation comprehension, error, habituation, keyboard, and screen-reader studies.
- Stop/revoke and cancellation races across provider, plan, queue, and execution.
- Audit completeness, redaction, export, clear, and tamper tests.
- Unauthorized-action rate reported separately from task success.

## Known risks and unresolved questions

- Risk classifiers can miss consequential context or over-prompt users.
- Confirmation fatigue can undermine user understanding.
- Postcondition verification may be impossible for some external effects.
- Audit logs can become sensitive datasets.

## Primary sources

- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/
- Model Context Protocol specification — https://modelcontextprotocol.io/specification/2025-11-25

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
