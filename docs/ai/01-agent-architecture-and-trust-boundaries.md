# Agent Architecture and Trust Boundaries

Status: research and design baseline  
Owner: agent platform architecture  
Purpose: Separate model reasoning, browser policy, execution, providers, tools, and user control.

## Relationship to the Turing program

This document expands the architecture and threat model of [Blueprint 10](../blueprint-v1/10-ai-agent-platform.md) and is subordinate to the [security engineering book](../security-engine/README.md).

## Principals and components

Components include session manager, observation service, context reducer, provider adapter, planner, deterministic policy engine, confirmation service, executor, audit store, memory service, tool/MCP gateway, developer protocol, and resource governor. Provider and model runtimes execute outside the browser kernel.

Each agent session has stable principal, profile, workspace, provider/model, initiating user gesture, task, grants, budgets, confirmation policy, lifecycle, and visible status.

## Trust classification

Untrusted inputs include page text, DOM attributes, accessible names, images, PDFs, downloads, emails, comments, metadata, model output, tool output, MCP servers, extensions, network responses, and other agents. Trusted inputs are narrowly defined browser policy state, user confirmation captured through protected UI, kernel-issued identity, and validated broker results.

A source label is not authority. “System”, “admin”, or “security” text inside a page remains page data.

## Control plane and data plane

The control plane manages grants, identity, provider selection, budgets, confirmation, stop/revoke, enterprise policy, and audit. The data plane creates observations, calls models, proposes actions, executes approved operations, and returns effects. Provider adapters and tools cannot modify control-plane state.

Control messages have reserved capacity so resource exhaustion cannot block stop or revoke.

## Process boundaries

The agent host is separate from browser UI, kernel, renderers, credentials, network, storage, extensions, and DevTools. Local model runtimes may use another restricted process or accelerator service. Raw browser memory, cookies, credentials, arbitrary files, devices, and internal IPC are unavailable.

The executor invokes task-specific browser capabilities; it does not expose generic mouse/keyboard or kernel calls as a substitute for policy.

## Session lifecycle

Sessions move through created, observing, planning, awaiting confirmation, executing, waiting/stabilizing, paused, completed, cancelled, revoked, failed, or expired states. Navigation, profile switch, private-session close, provider switch, browser restart, grant expiry, budget exhaustion, or document epoch changes invalidate relevant state.

Stop/revoke cancels provider calls, queued tools, planning, observations, and actions and closes or narrows capabilities.

## Threat scenarios

Threats include direct and indirect prompt injection, cross-origin exfiltration, hidden-content manipulation, UI spoofing, stale target, page swap, malicious extension/service worker, compromised provider, malicious MCP server, tool-result injection, multi-agent collusion, confirmation fatigue, hallucinated target, runaway planning, local model compromise, and resource exhaustion.

Defenses are tested as systems; no system prompt is treated as sufficient.

## Failure containment

A provider or planner failure produces no effect without an approved action. A tool crash or malformed response is untrusted result data. An agent-host compromise is limited to current scoped observations and proposals; execution still requires deterministic authorization. Audit and visible status survive agent-host restart where feasible.

## Non-negotiable invariants

- Models, providers, pages, tools, extensions, and other agents cannot grant authority.
- The deterministic policy engine and trusted confirmation service are outside the model process.
- The executor exposes task-specific capabilities, not generic browser internals.
- Stop and revoke remain available under overload.
- Profile, origin, frame, document epoch, action, time, count, and data scope are explicit.
- A compromised agent host cannot directly access credentials or arbitrary browser memory.

## Required evidence

- Architecture threat model and process/capability matrix.
- Compromised provider, tool, MCP, extension, page, and agent-host harnesses.
- Lifecycle model tests for navigation, expiry, stop, revoke, restart, and budget exhaustion.
- Prompt-injection and confused-deputy adversarial corpus.
- Cross-origin, profile, private-session, and stale-epoch negative tests.
- Control-channel overload and cancellation-latency measurements.

## Known risks and unresolved questions

- Tool ecosystems can reintroduce ambient authority outside browser policy.
- Complex lifecycle and delegation can produce stale or over-broad grants.
- A model can manipulate users even when deterministic policy blocks direct action.
- Local model/process isolation may vary by GPU and OS capabilities.

## Primary sources

- Model Context Protocol specification — https://modelcontextprotocol.io/specification/2025-11-25
- Model Context Protocol architecture — https://modelcontextprotocol.io/docs/learn/architecture
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
