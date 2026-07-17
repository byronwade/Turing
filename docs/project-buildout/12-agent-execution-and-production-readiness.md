# Agent Execution and Production Readiness

Status: professional operating baseline  
Owner: program, agent operations, security, quality, release, support, legal, and human release authority  
Last researched: 2026-07-17

## Purpose

Define the control plane under which agents may implement Turing and the finite evidence required before any preview, beta, or stable claim.

## Start rule

Contained, reviewed tasks may begin when their individual preconditions are ready. “Build the entire browser” is prohibited as one autonomous task. Broad implementation remains gated by pre-build readiness; production release remains gated by `PRG-001` through `PRG-020`.

## Mandatory boundaries

- protected pull requests for production work;
- no self-approval or self-merge;
- deny-by-default agent tools, files, network, and credentials;
- independent security, performance, accessibility, and release evidence;
- no production signing keys or stable promotion authority for agents;
- finite stable scope, numeric SLOs, update trust, incident staffing, support, and legal approval;
- human release authority as the final gate.

## Canonical sources

- [Agent Execution and Autonomous Engineering](../agent-execution/README.md)
- [Production Readiness and Stable Release Engineering](../production-readiness/README.md)
- [Agent and production readiness audit](../research/agent-execution-production-readiness-audit-2026-07.md)
