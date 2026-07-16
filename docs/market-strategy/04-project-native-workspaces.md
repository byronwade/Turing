# Project-Native Workspaces and Identity

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Define the proposed Turing Space as a durable project, identity, policy, and resource boundary rather than a visual tab filter.

## Proposed model

A Turing Space may contain:

- windows, tabs, nested folders, pinned references, and one-to-four-pane layouts;
- left and right panels, installed web applications, and commands;
- a bound profile or container identity and domain-routing rules;
- workspace-scoped history, bookmarks, downloads, notes, tasks, citations, and selected files;
- Plug-ins, capabilities, and resource budgets;
- agent provider, observation scope, memory, action grants, and audit;
- synchronization, sharing, export, retention, and recovery policy.

## Invariants

- Closing a window does not delete a Space.
- Space identity is independent of a device, process, or window.
- A Space can be paused, resumed, duplicated, exported, imported, and deleted with visible consequences.
- Site data never crosses identity boundaries without an explicit, audited operation.
- Every process, worker, Plug-in, and agent is charged to a Space or an identified shared service.
- Browser-trusted identity indicators cannot be obscured by page content.
- A Space remains usable without AI, sync, collaboration, or third-party Plug-ins.

## Identity routing

Domains may be routed to a Space, profile, disposable task container, or user prompt. Routing decisions show the current identity before navigation. External links may enter a preview that identifies destination profile, credentials, policies, and expected data boundary.

Per-Space network policy is a later research area: proxy, DNS, VPN, certificates, downloads, permissions, and device access must not fragment web semantics or permit page-controlled policy selection.

## Open questions

- Is one profile per Space too expensive or too rigid?
- Which state belongs to the Space versus the profile or site?
- How are same-site links handled across Spaces?
- How are keyboard, screen-reader, and mobile representations kept understandable?
- Can shared services remain efficient without creating cross-Space channels?

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
