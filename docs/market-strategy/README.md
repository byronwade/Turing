# Market Strategy and Differentiation

Status: market research and product-strategy baseline; not an implementation or support claim  
Owner: market strategy, product, architecture, security, performance, accessibility, developer experience, Plug-ins, embedding, and research  
Last researched: 2026-07-16

This book converts competitive patterns and user-demand signals into falsifiable Turing product opportunities. It does not turn popularity, community requests, or vendor marketing into requirements. The canonical evidence artifact is the [browser market-gap report](../research/browser-market-gap-2026-07.md).

## Proposed position

> **Turing is the open project browser for people and agents: it remembers the work, explains the cost, and keeps the user in control.**

## Competitive performance posture

The long-horizon positioning for this program is a credible Chrome-class browser with measurable performance advantage only where the full benchmark evidence pipeline is complete.

Current claim boundary:

- `PB-013` remains the hard gate for Chrome-class and extreme-performance claims.
- No public "faster/lower-memory/lower-energy/daily-driver/chrome-equivalent" statement may be made until owner-reviewed benchmark readiness, statistics analysis, and claim bundles are complete.
- A supported claim requires fixed-hardware equivalence, raw browser-run artifact retention, 30-tab and recovery scenario evidence, and review against the benchmark claim-expiry and acceptance rules.
- Task lane to this claim remains [TASK-000005](../project-buildout/17-build-readiness-task-queue.md).

This means market strategy can prioritize performance opportunities, but pricing, marketing, and roadmap claims must stay out-of-scope until evidence gates are complete.

## Chrome-class performance evidence lane

Competitiveness is tracked through explicit benchmark-readiness gates rather than feature-list parity:

- [Chrome-class and extreme-performance readiness lane map](../benchmark-lab/chrome-class-performance-readiness-lane.md)
- [Performance benchmark readiness packet](../research/performance-benchmark-readiness-packet-2026-07.md)
- [Chrome-class performance runbook](../research/chrome-class-performance-runbook-2026-07.md)
- [Benchmark engine baseline harness readiness map](../research/benchmark-engine-baseline-harness-readiness-map-2026-07.md)

## Reading order

1. [Market Method, Segments, and Positioning](01-market-method-and-segments.md)
2. [Competitive Feature Matrix and Convergence](02-competitive-feature-matrix.md)
3. [User Demand and Switching Barriers](03-user-demand-and-switching-barriers.md)
4. [Project-Native Workspaces and Identity](04-project-native-workspaces.md)
5. [Workspace Time Machine and Continuity](05-time-machine-and-continuity.md)
6. [Resource Truth and Lifecycle Control](06-resource-truth-and-lifecycle-control.md)
7. [Trustworthy AI and Agent Differentiation](07-trustworthy-ai-and-agent-differentiation.md)
8. [Research Canvas and Developer Causal Mode](08-research-canvas-and-developer-mode.md)
9. [Migration, Portability, Collaboration, and Sync](09-migration-portability-collaboration-and-sync.md)
10. [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md)

## Machine-readable opportunity registry

The [feature opportunity registry](machine/feature-opportunities.json) records `OP-001` through `OP-014`, target segments, dependencies, risks, priority, and evidence requirements. An opportunity remains research until the Blueprint, requirements, risks, work packages, owners, traceability, tests, and support statements are deliberately synchronized.

## Portfolio discipline

The primary integrated hypothesis is a project-native Space that owns organization, identity, recovery, resource policy, Plug-ins, and scoped agent authority. The project must resist implementing fourteen disconnected features. User studies and architecture experiments should determine which opportunities combine coherently, which belong in Plug-ins, and which should be rejected.

<!-- MARKET-RQ-ID-CORRECTION-2026-07 -->
## Research-question ownership

Market validation is owned by `RQ-49` through `RQ-54`. `RQ-45` through `RQ-48` remain assigned to professional project controls, reproducible environments, traceability, and sustainability. Research-question identifiers are globally unique and contiguous.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native implementation constraint

Market differentiation must not drive Turing into a second browser runtime. Spaces, Time Machine, Resource Truth, Research Canvas, and agent UI are evaluated on the native toolkit-neutral model. Visual prototyping speed is valuable only when production security, footprint, accessibility, and recovery remain intact.
