# Agent Memory, Planning, Multi-Agent Operation, and Lifecycle

Status: research and design baseline  
Owner: agent orchestration and memory  
Purpose: Bound reasoning state and delegation without creating hidden surveillance, authority, or resource leaks.

## Relationship to the Turing program

This document expands multi-agent and audit lifecycle design in [Blueprint 10](../blueprint-v1/10-ai-agent-platform.md) and the resource rules in [Blueprint 09](../blueprint-v1/09-performance-memory.md).

## Planning representation

Plans are typed graphs of goals, assumptions, observations, proposed actions, dependencies, checkpoints, confirmation boundaries, budgets, expected effects, and stop conditions. Model prose is stored as untrusted rationale, not executable control flow. The scheduler executes only validated action nodes.

Plans are versioned and invalidated by target/document changes, grant changes, provider change, contradictory observations, or user edits.

## Working memory

Session working memory includes task state, selected facts, references, action results, and unresolved questions within token, byte, time, and sensitivity budgets. It remains scoped to one profile/workspace/session and is cleared at completion, expiry, private-session closure, or user request unless persistence is explicitly approved.

Raw page content is not retained merely because it was once observed.

## Long-term memory

Optional long-term memory stores user-approved preferences, task artifacts, or summaries with provenance, scope, sensitivity, expiry, edit/delete controls, and destination. It is disabled for private sessions by default. Memories cannot become grants or policy.

A memory item records source and confidence so model inference is not later presented as verified fact.

## Multi-agent delegation

Delegation creates a child principal, narrowed grant, explicit task, resource budget, allowed tools, data scope, deadline, and return schema. The parent treats child output as untrusted data unless it is a deterministic browser service result. Delegation chains are bounded in depth and count.

Agents do not share memory, observations, credentials, or confirmation authority by default.

## Concurrency and leases

Concurrent work on one target uses leases or optimistic preconditions tied to document/mutation epochs. Conflicting mutations serialize, fail, or require re-planning. Read-only observations can coexist within budgets. A long-running agent cannot indefinitely block user input or another visible session.

Browser UI always lets the user see active agents and stop individual or all sessions.

## Lifecycle and recovery

Agent sessions survive only documented events. Provider timeout, process crash, browser sleep, network loss, navigation, tab close, profile switch, update, or restart produce paused, failed, expired, or recoverable states. Recovery revalidates grants, targets, data policy, and unfinished effects; it never blindly replays pending consequential actions.

Audit and user-visible status explain what completed and what did not.

## Resource governance

Planning iterations, observations, tokens, wall time, CPU, memory, GPU, network, disk, provider cost, navigation, and mutations have budgets. Repeated ineffective replanning, confirmation loops, or tool retries trigger pause or failure. Local model memory unloads after idle according to policy.

Agent-disabled browser baselines remain the performance reference.

## Non-negotiable invariants

- Plans are proposals; only validated typed actions execute.
- Memory never grants authority or persists by accident across profiles/private sessions.
- Delegated grants can only narrow and chains are bounded.
- Concurrent mutations validate leases/epochs and cannot overwrite user changes silently.
- Recovery revalidates every pending effect and confirmation.
- Agent resources are separately budgeted and observable.

## Required evidence

- Plan invalidation and stale-assumption tests.
- Memory provenance, expiry, scope, private-session, edit/delete, and leakage tests.
- Multi-agent grant-narrowing, collusion, delegation-depth, and conflicting-action tests.
- Crash/restart/navigation/network/provider recovery scenarios.
- Runaway planning, repeated confirmation, tool loop, and budget exhaustion tests.
- Resource and usability measurements for one and multiple agents.

## Known risks and unresolved questions

- Long-term memory can become an opaque behavioral profile.
- Delegation increases attack paths and audit complexity.
- Concurrency can produce surprising external side effects.
- Recovery can duplicate actions if effect state is uncertain.

## Primary sources

- Model Context Protocol architecture — https://modelcontextprotocol.io/docs/learn/architecture
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
