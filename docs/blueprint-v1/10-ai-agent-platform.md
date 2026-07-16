# 10 — AI Assistant and Agent Platform

## 1. Product objective

Turing treats AI as a browser principal with explicit authority, not a chat panel that secretly drives mouse and keyboard events. The platform supports explanation, summarization, search, developer assistance, repeatable workflows, and bounded autonomous actions while preserving origin isolation, user consent, credential secrecy, and auditability.

The model may propose. Deterministic browser code decides whether an action is valid, authorized, current, and confirmed.

## 2. Agent architecture

Components:

1. **Agent session manager:** identity, profile, provider/model, task, budgets, lifecycle, visible status, cancellation.
2. **Observation service:** creates a redacted semantic snapshot from DOM/accessibility/layout/network/console state according to grants.
3. **Context reducer:** selects task-relevant content, preserves source/origin labels, limits tokens, and marks untrusted instructions.
4. **Model adapter:** local or remote provider interface with declared data policy and capabilities.
5. **Planner:** converts model output into a typed proposed-action graph. It has no direct browser handles.
6. **Policy engine:** verifies grants, origin, document epoch, action risk, user activation, quotas, enterprise rules, and confirmation.
7. **Executor:** maps approved actions to browser/engine commands, then returns structured outcomes.
8. **Audit log:** append-only local record of observations’ hashes, proposals, policy reasons, confirmations, execution, and effects.
9. **Developer protocol:** inspect and test sessions without granting hidden authority.

The agent host is a separate process. Provider libraries and model runtimes cannot link into the browser kernel.

## 3. Principal and grant model

An `AgentPrincipal` includes:

- stable application/agent identity;
- provider and model identifier/version when known;
- owning profile and optional workspace;
- session creation reason and initiating user gesture;
- allowed origins/sites and frame scope;
- observation classes;
- action classes;
- resource targets such as selected files or download directory handles;
- time-to-live and maximum action count;
- token, monetary, network, CPU, GPU, and wall-clock budgets;
- confirmation policy;
- enterprise/user policy overlays.

A grant is unforgeable and revocable. Grants do not survive profile changes, private-session closure, browser restart, provider switch, or document epoch change unless an explicit persistence policy exists.

## 4. Observation model

### 4.1 Preferred semantic snapshot

The default snapshot is derived from the document and accessibility trees and includes only what a user in that frame context can meaningfully perceive or interact with:

- origin, URL class, title, navigation state, frame ancestry, and document epoch;
- visible headings, landmarks, text excerpts, lists, tables, forms, links, buttons, menus, dialogs, alerts, and controls;
- accessible names, roles, states, values where not sensitive, descriptions, relationships, and bounds;
- stable session-local node references;
- selection, focus, validation, disabled/readonly, expanded/collapsed, and occlusion information;
- selected console/network/performance diagnostics for developer grants.

The snapshot excludes or redacts:

- password and one-time-code values;
- cookies, authorization headers, keychain data, passkey secrets, private keys, tokens, and hidden autofill data;
- hidden/inert/offscreen content unless the task grant permits and the UI discloses it;
- cross-origin frames without explicit frame/origin grant;
- browser internal UI and unrelated tabs;
- full local file paths and unselected file contents;
- protected media and DRM surfaces;
- enterprise-designated sensitive elements.

### 4.2 Screenshot/vision observations

Screenshots are optional and lower-trust because they can include unrelated or sensitive pixels. The user sees when pixels are captured. Captures are scoped to a tab/region, exclude browser chrome unless specifically approved, and are not silently sent to remote providers. OCR/vision output retains source and origin labels.

### 4.3 Developer observations

With a developer grant, the agent may receive structured DOM, CSS, layout, accessibility, console, network, performance, source, and test information. Secrets and cross-origin restrictions still apply. Source maps and local-workspace files require separately selected handles.

## 5. Action protocol

Actions are typed, versioned, and idempotence-aware. Core categories:

- navigate, go back/forward, reload, open/close/select/move tab;
- activate element, focus, scroll, set selection;
- insert/replace text, choose option, toggle control, submit form;
- read permitted semantic content or developer diagnostics;
- wait for a lifecycle, selector/role, network idle, navigation, or stable document epoch;
- download to an approved destination; upload from an approved file handle;
- create bookmark, tab group/workspace, note, or task artifact;
- execute approved DevTools evaluation in a clearly marked developer session;
- invoke extension or local tool through a separately authorized bridge.

Each request contains:

- session, principal, grant, profile, tab/frame, and document epoch;
- target reference plus fallback semantic locator;
- action payload and expected preconditions;
- risk classification and claimed user intent;
- timeout, retry policy, and idempotency key;
- expected postcondition when possible.

The executor re-resolves the target, checks visibility/interactability, verifies the epoch and origin, evaluates policy, requests confirmation if needed, applies the action, waits for stabilization, and returns a structured result. A stale node is never clicked based on screen coordinates from an old page.

## 6. Risk classes

### Class 0 — observe

Read granted public page content, explain UI, summarize, inspect nonsecret diagnostics. Usually no per-action confirmation.

### Class 1 — reversible local organization

Open/select/reorder tabs, scroll, change zoom, create local bookmarks or groups, fill non-sensitive draft text. Session grant may cover repeated actions.

### Class 2 — external but low-impact

Submit a search, follow a link, change a non-security preference, download a low-risk file to a selected location. Confirmation policy is contextual.

### Class 3 — consequential

Send or publish content, upload a file, create/delete cloud data, make a reservation, change account data, grant a site permission, open an external application, run code, expose local source, or initiate a purchase. Requires explicit confirmation at the point of action unless a narrowly defined user policy says otherwise.

### Class 4 — high-risk or prohibited delegation

Financial transfer, purchase completion, security/credential/passkey changes, recovery-code handling, installation of untrusted software/extensions, camera/microphone/display access, destructive bulk actions, legal attestation, medical or government submission, privilege escalation, policy disablement, or bypass of warnings. Requires strong confirmation and may be prohibited from autonomous execution entirely.

The classification is deterministic and may be elevated by page context, destination, amount, data sensitivity, novelty, or enterprise policy. A model cannot downgrade it.

## 7. Confirmation UX

A confirmation shows:

- the agent and model/provider;
- exact action in plain language;
- origin/site and account/profile;
- data that will be sent, uploaded, published, deleted, purchased, or granted;
- price/amount and destination when applicable;
- selected file names without leaking unnecessary paths;
- relevant page excerpt and reason;
- whether this is one-time or part of a bounded batch;
- cancel, modify, approve once, and policy-management options.

The page cannot cover or simulate the trusted confirmation. The agent cannot click it. Accessibility users receive the same information and explicit action separation.

## 8. Prompt-injection defenses

Prompt injection is treated as confused-deputy input, not solvable by a stronger system prompt alone.

Defenses:

- all page/model/tool text is labeled by source and untrusted status;
- page instructions cannot alter grants or policy;
- observations omit secrets and unrelated context before model access;
- tools expose task-specific commands, not generic browser internals;
- action targets and effects are recomputed from live browser state;
- high-impact actions require deterministic confirmation;
- cross-origin content is isolated and identified;
- downloaded files, PDFs, comments, alt text, metadata, and hidden content do not receive higher trust;
- agents cannot disable safe browsing, certificate warnings, CSP, sandbox, extension policy, or confirmation;
- a policy simulator and adversarial corpus test exfiltration, indirect injection, UI deception, stale-page swaps, and multi-agent collusion.

## 9. Secrets and credentials

The model never receives plaintext passwords, passkey private material, cookies, auth headers, keychain contents, recovery codes, payment card numbers, or hidden autofill values. Credential fill is a browser action bound to an approved origin. The model may see a token such as `credential_available: true` and request “fill saved credential,” which policy and the credential broker decide.

One-time codes and sensitive personal data use configurable handling. Where the user explicitly delegates entry, the value should move through an opaque browser handle rather than model text whenever possible.

## 10. Local and remote models

Provider adapters declare:

- local versus remote execution;
- data fields transmitted;
- retention/training policy as configured, not assumed;
- region and endpoint;
- model/version and capabilities;
- authentication method;
- token/cost limits;
- fallback behavior;
- tool-call format and output limits.

No silent provider fallback occurs. A local task does not become remote because the model is slow. Remote transmission has a visible indicator and per-profile setting. Enterprise policy can force local-only, approved-provider, no-retention, region, or disabled modes.

Local models run in a restricted process with explicit memory/GPU budgets, unload when idle, and cannot map browser process memory. Model weights are signed or hash-verified and stored separately from profiles.

## 11. Developer-first agent capabilities

With repository/workspace handles selected by the user, the agent can:

- inspect DOM/CSS/layout and explain rendering;
- correlate a UI element with source maps and local source;
- generate reduced test cases from a page failure;
- record/replay an interaction as a typed script;
- author and run WebDriver BiDi or Turing protocol tests;
- compare performance traces and memory attribution;
- identify long tasks, forced layouts, overdraw, accessibility defects, and network bottlenecks;
- emulate devices, permissions, network, CPU, locale, color scheme, reduced motion, and memory pressure;
- launch isolated test profiles and deterministic local servers;
- propose code changes only through selected local tools, never by arbitrary filesystem access.

Developer mode remains visually distinct from everyday browsing. Evaluation in a page is treated as code execution and requires a developer grant.

## 12. Multi-agent operation

Agents do not share authority by default. Each principal has its own grants and budget. Delegation creates a child grant no broader than the parent and records the chain. Results crossing agents are labeled as untrusted data unless produced by a deterministic browser service.

Concurrent actions on one tab use leases and document epochs. Conflicting mutations serialize or fail. An agent cannot approve another agent’s confirmation.

## 13. Audit and replay

Audit records include:

- session/principal/provider/model identifiers;
- user task and grant summary;
- observation version and content hash, not necessarily raw sensitive content;
- proposed action and policy evaluation reason codes;
- confirmation presentation and response;
- precondition/document epoch;
- execution result, navigation/effect summary, and errors;
- resource use and provider cost where available;
- cancellation/revocation.

Users can inspect, export a redacted record, and clear local history under policy. Deterministic actions can be replayed only in a fresh isolated test profile unless the user explicitly authorizes live replay.

## 14. Agent API and protocol

The protocol is transport-independent and can be exposed locally through authenticated IPC, a loopback endpoint, WebDriver BiDi extensions, or a constrained tool bridge. Remote listening is disabled by default.

Protocol design rules:

- version negotiation and capability discovery;
- typed JSON/CBOR-like schema with strict limits;
- no arbitrary method names or script-eval backdoor;
- session authentication and origin/profile binding;
- bounded observation size and pagination;
- cancellation, deadlines, idempotency, and progress events;
- policy reason codes stable enough for testing;
- test mode can simulate confirmation but stable interactive mode cannot be silently bypassed;
- headless mode still enforces grants and high-risk policy unless launched under an explicit isolated automation profile.

## 15. Evaluation program

Agent quality is measured across:

- task success and correctness;
- unnecessary actions and replans;
- stale-target resistance;
- cross-origin isolation;
- secret-exfiltration attempts;
- direct/indirect prompt injection;
- destructive and financial confirmation compliance;
- accessibility-only operation without coordinates;
- page changes during action;
- authentication/credential handling;
- cancellation latency;
- token, time, memory, energy, and cost;
- audit completeness;
- user ability to understand and correct behavior.

A higher task-success score cannot compensate for unauthorized actions.

## 16. Agent gates

- **AI-GATE-1:** every action maps to a schema and deterministic policy path.
- **AI-GATE-2:** secrets are absent from default observations and provider payloads.
- **AI-GATE-3:** stale document/node actions fail closed.
- **AI-GATE-4:** cross-origin frames require explicit grants and remain labeled.
- **AI-GATE-5:** Class 3/4 actions follow configured confirmation and cannot be approved by page/model input.
- **AI-GATE-6:** stop/revoke interrupts planning, provider calls, and queued actions within a published bound.
- **AI-GATE-7:** adversarial prompt-injection suite passes before agent mode is enabled outside isolated test profiles.
- **AI-GATE-8:** local/remote provider data flow is visible, configurable, and logged.

<!-- MARKET-STRATEGY-2026-07 -->
## Trustworthy Agent Mode research

`OP-004` packages the existing capability model into an isolated, visible task session with observation manifest, provider disclosure, budgets, dry run, execution-time confirmation, postconditions, audit, stop, and revocation. Read-only assistance and consequential action have separate maturity gates.
