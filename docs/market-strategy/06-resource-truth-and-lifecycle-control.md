# Resource Truth and Lifecycle Control

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Turn memory saving into an explainable, attributable, reversible product contract rather than an opaque background heuristic.

## Resource model

The Resource Truth Center reports physical totals and semantic attribution for CPU, memory, GPU, network, disk, energy, wakeups, and model cost. Ownership is visible by Space, tab, frame/site instance, worker, Plug-in, agent, browser UI, and shared service.

The UI distinguishes measured physical totals from charged estimates. Shared memory is reconciled rather than double-counted. Every lifecycle transition carries a machine-readable reason and plain-language explanation.

## Lifecycle control

Supported states remain explicit: Active, Background, Frozen, Serialized, Discarded, Restoring, Crashed, and Terminated where applicable. Before an action the browser reports:

- predicted savings;
- state-loss risk;
- protection reasons;
- expected revival latency;
- whether network, media, upload, unsaved edits, DevTools, or confirmation are active;
- whether a user override is safe.

Per-Space budgets can guide policy but cannot weaken site isolation, security mitigations, accessibility, update work, or data durability.

## Success measures

- correct user identification of high-cost principals;
- no silent loss of protected work;
- p50/p95/p99 restoration latency;
- memory and energy savings under equivalent security settings;
- low instrumentation overhead;
- accurate attribution reconciliation;
- understandable decisions for everyday and assistive-technology users.

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
