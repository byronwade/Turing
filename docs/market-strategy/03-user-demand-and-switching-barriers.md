# User Demand and Switching Barriers

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Translate directional demand signals into testable jobs without confusing community enthusiasm with representative market evidence.

## Repeated demand clusters

Public requests repeatedly cluster around project organization, persistent pinned tabs, folders, workspace-bound identities, complete workspace synchronization, configuration backup, web panels, PWA support, reliable restoration, and performance without lost work.

The underlying jobs are:

- resume a project without reconstructing browser state;
- keep personal, work, client, and test identities from crossing;
- understand what uses resources and what will be lost before reclamation;
- compare several sources without losing provenance;
- move between devices and browsers without abandoning organization;
- use page-aware AI without surrendering the authenticated browser session;
- extend the browser without installing opaque, unbounded authority.

## Switching barriers

1. Site compatibility and authentication reliability.
2. Password, passkey, history, bookmark, and open-tab migration.
3. Loss of tab groups, spaces, folders, panels, and extension settings.
4. Missing extension or developer-tool equivalents.
5. Sync lock-in and fear of data loss.
6. Unfamiliar interaction models.
7. Lack of trusted updates and incident response.
8. Inability to return to the previous browser with exported state.

Turing must measure migration completion and repair time. A beautiful empty browser does not overcome the cost of rebuilding years of browsing state.

## Research protocol

Recruit across everyday users, high-tab users, developers, students/researchers, disabled users, multi-account users, and enterprise administrators. Preserve contrary findings. Test longitudinal resumption after one day, one week, and one month—not only first-use reactions.

Opportunity scoring includes user value, segment breadth, differentiation, switching-cost reduction, security risk, accessibility complexity, implementation dependency, maintenance cost, and evidence confidence.

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
