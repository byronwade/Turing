# Agent Evaluation, Safety, Performance, and Usability

Status: research and design baseline  
Owner: agent evaluation  
Purpose: Measure task quality without allowing success scores to hide unsafe, private, inaccessible, or inefficient behavior.

## Relationship to the Turing program

This document operationalizes AI-GATE-1 through AI-GATE-8 and the agent adversarial suite in [Blueprint 12](../blueprint-v1/12-testing-compatibility.md).

## Evaluation dimensions

Report task success, correctness, unnecessary actions, stale-target failures, unauthorized actions, secret/cross-origin leakage, prompt-injection resistance, confirmation compliance, user correction, cancellation, audit completeness, accessibility, latency, tokens, cost, CPU, memory, GPU, energy, network, and page disruption.

Safety metrics are release gates, not weights that can be offset by higher task completion.

## Task corpus

The corpus covers navigation/research, forms, shopping mock flows, email/document drafting, downloads/uploads with fixtures, account settings, permissions, multi-tab organization, developer debugging, accessibility-only operation, cross-origin frames, changing pages, service workers, extensions, local files, and tool/MCP workflows. Consequential actions use simulated or isolated services.

Tasks include ambiguity, contradiction, unavailable controls, and correct refusal/clarification outcomes.

## Adversarial corpus

Direct and indirect injection appears in visible text, hidden elements, comments, alt text, images, PDFs, emails, metadata, tool descriptions/results, MCP resources, extensions, service workers, cross-origin frames, and other agents. Cases attempt credential theft, data exfiltration, confirmation spoofing, policy disablement, stale page swap, destructive actions, infinite loops, and resource exhaustion.

Unauthorized action rate and data exposure are primary.

## Human factors

Studies measure whether users understand agent status, observed data, provider destination, grant scope, confirmation, batch actions, audit, stop/revoke, failures, and recovery. Include keyboard, screen-reader, magnification, voice, reduced-motion, cognitive-load, and low-vision users.

Fast approval is not success if users misunderstand effect.

## Performance and browser impact

Measure observation generation, redaction, provider latency, model warm-up, streaming, planning, policy, confirmation, execution, stabilization, replans, local RAM/VRAM, CPU/GPU, energy, network, and tab/page overhead. Compare agent-disabled, idle-enabled, local, and remote configurations under 1- and 30-tab workloads.

Dormant AI has a near-zero active-resource target apart from minimal configuration state.

## Model/provider variation

Results identify model, version, provider, decoding/tool settings, context, prompt templates, local hardware, and date. Model changes require re-evaluation. No single vendor benchmark is generalized to the platform architecture.

Deterministic policy tests are model-independent and run continuously.

## Release gates and transparency

Publish capability scope, tasks, failures, unauthorized-action rate, leakage results, accessibility, resource costs, provider data policy, unsupported behavior, and limitations. High-risk classes remain disabled outside isolated testing until policy and confirmation gates pass. User-facing claims are versioned and expire with material model/provider changes.

## Non-negotiable invariants

- Task success cannot compensate for unauthorized action or secret leakage.
- Consequential evaluations use isolated or simulated services.
- Model, provider, version, settings, and date accompany every result.
- Agent-disabled and idle-enabled baselines are reported.
- Accessibility and user comprehension are first-class gates.
- Policy and schema tests remain model-independent.

## Required evidence

- Versioned benign, ambiguous, adversarial, and refusal task corpora.
- Unauthorized action, leakage, stale target, confirmation, stop, and audit metrics.
- Human factors and accessibility studies.
- Fixed-hardware local/remote latency, resource, energy, and 30-tab results.
- Cross-model/provider repeatability and regression tracking.
- Public limitations, unsupported cases, and residual-risk report.

## Known risks and unresolved questions

- Evaluation corpora can become known and overfit.
- Real-world consequences and social manipulation are difficult to simulate.
- Model/provider changes can invalidate prior results quickly.
- User studies may not represent high-risk or vulnerable populations sufficiently.

## Primary sources

- Model Context Protocol specification — https://modelcontextprotocol.io/specification/2025-11-25
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- WAI-ARIA — https://www.w3.org/TR/wai-aria/
- Speedometer — https://browserbench.org/Speedometer3.1/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
