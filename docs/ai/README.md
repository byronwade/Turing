# AI and Agent Engineering Book

Status: detailed research and design baseline  
Owner: AI agent architecture and safety  
Canonical overview: [Blueprint 10 — AI assistant and agent platform](../blueprint-v1/10-ai-agent-platform.md)

This book expands the capability-safe agent model into observations, actions, planning, memory, providers, MCP/tool integration, multi-agent operation, evaluation, performance, and usability. It does not claim that Turing currently has an AI assistant or autonomous browser agent.

## Reading order

1. [Agent architecture and trust boundaries](01-agent-architecture-and-trust-boundaries.md)
2. [Semantic observations and redaction](02-semantic-observations-and-redaction.md)
3. [Actions, grants, confirmation, and audit](03-actions-grants-confirmation-and-audit.md)
4. [Memory, planning, multi-agent operation, and lifecycle](04-memory-planning-multi-agent-and-lifecycle.md)
5. [Providers, local models, MCP, and tools](05-providers-local-models-mcp-and-tools.md)
6. [Evaluation, safety, performance, and usability](06-evaluation-safety-performance-and-usability.md)

## Agent thesis

A model is an untrusted reasoning component, not a browser authority. Turing supplies filtered observations and accepts typed proposals. Deterministic browser code validates identity, current document state, grant scope, action class, limits, policy, and user confirmation before effect. Page, document, model, extension, tool, and other-agent text never expands authority.

Semantic observations should be the default because they are more accessible, compact, attributable, and actionable than screenshot-only control. Vision remains optional and visibly scoped. Credentials remain in brokers. Remote providers receive only declared data. Local models run in restricted, unloadable processes with separate resource budgets.

## Agent leadership criteria

- Unauthorized consequential action rate is zero within the published evaluation set.
- Secret and cross-origin leakage are measured independently from task success.
- Stale-page and target-swap actions fail closed.
- Stop/revoke interrupts model calls, planning, queued actions, and execution within a published bound.
- Users can understand what data is observed, where it goes, and what action will occur.
- Keyboard and screen-reader users receive equivalent confirmation and control.
- Agent memory is scoped, inspectable, clearable, and excluded from private sessions by default.
- Local/remote AI cost, RAM, GPU, energy, latency, and browser impact are reported separately.
- MCP and external tools remain subordinate to browser grants and do not create ambient authority.

## Related material

- [Security engineering book](../security-engine/README.md)
- [API design book](../api-design/README.md)
- [Developer experience book](../developer-experience/README.md)
- [Performance engineering book](../performance/README.md)
