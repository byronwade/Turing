# Research Canvas and Developer Causal Mode

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Combine multi-pane browsing, source provenance, causal diagnostics, replay, and export into workflows that existing split views and DevTools only partially address.

## Research Canvas

The proposed Canvas supports one-to-four panes, persistent layouts, linked scrolling, optional synchronized navigation, text/DOM/image differences, quote and screenshot capture, page-version evidence, citation-aware notes, source-conflict marking, and export to open formats.

AI is grounded only in a user-selected source set. Every extracted claim retains URL, timestamp, content hash or snapshot identity where lawful, selection, and transformation history. The browser distinguishes a live source from a saved snapshot and indicates when a page changed.

## Developer Causal Mode

Developer tooling should answer:

- why style, layout, paint, accessibility, or script work ran;
- why a request was blocked, redirected, cached, retried, or routed;
- why a process or lifecycle state was chosen;
- who retains memory or scheduled a long task;
- which capability or policy denied an operation;
- where deterministic replay diverged;
- which specification or cross-browser behavior differs.

Causal statements identify observed events, inferred links, confidence, missing data, and overhead. Trace collection is bounded and redacted. Record/replay never repeats consequential external effects without explicit simulation or confirmation.

## Workflow studies

Evaluate travel planning, product comparison, academic research, policy analysis, web debugging, performance regression, accessibility diagnosis, and agent failure investigation. Measure time, source errors, false hypotheses, citation completeness, reproducibility, keyboard completion, and screen-reader completion.

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
