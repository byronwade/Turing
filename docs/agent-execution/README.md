# Agent Execution and Autonomous Engineering

Status: professional control-plane baseline; no agent is authorized to build or release Turing autonomously  
Owner: program, architecture, security, quality, release, documentation, and agent operations  
Last researched: 2026-07-17

This book defines how software agents may contribute to Turing without becoming an unreviewed source of architecture, security policy, evidence, or release authority.

## Core rule

> An agent may implement a bounded, approved task. It may not define its own scope, lower its own acceptance criteria, approve its own work, possess production signing authority, or declare the product safe or stable.

## Reading order

1. [Agent trust model and authority](01-agent-trust-model-and-authority.md)
2. [Task decomposition and execution graph](02-task-decomposition-and-execution-graph.md)
3. [Branch, pull request, review, and merge policy](03-branch-pr-review-and-merge-policy.md)
4. [Tools, network, files, secrets, and credentials](04-tools-network-files-secrets-and-credentials.md)
5. [Specification, test, and evidence workflow](05-specification-test-and-evidence-workflow.md)
6. [Model, prompt, environment, and run provenance](06-model-prompt-environment-and-run-provenance.md)
7. [Checkpoints, recovery, retries, and rollback](07-checkpoints-recovery-retries-and-rollback.md)
8. [Independent verification and adversarial review](08-independent-verification-and-adversarial-review.md)
9. [Security embargo, release, and incident boundaries](09-security-embargo-release-and-incident-boundaries.md)
10. [Cost, resource, and concurrency budgets](10-cost-resource-and-concurrency-budgets.md)
11. [Human handoff and escalation](11-human-handoff-and-escalation.md)

## Machine-readable companions

- [Agent capability matrix](machine/agent-capability-matrix.json)
- [Agent run manifest schema](machine/agent-run-manifest.schema.json)
- [Execution task schema](machine/execution-task.schema.json)
- [Evidence bundle schema](machine/evidence-bundle.schema.json)
- [Escalation policy](machine/escalation-policy.json)
- [Prohibited agent actions](machine/prohibited-agent-actions.json)

## Normative baselines

Turing maps these controls to NIST SSDF 1.1, NIST SP 800-218A for AI-related secure development, SLSA source/build provenance, repository rulesets, and Turing's stricter browser-specific threat model. External frameworks guide the control design; Turing's accepted requirements and evidence remain authoritative.
