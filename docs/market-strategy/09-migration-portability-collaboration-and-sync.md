# Migration, Portability, Collaboration, and Sync

Status: market research and product-design baseline; not an implementation, accepted requirement, or support claim  
Owner: product strategy with affected architecture, security, performance, accessibility, and subsystem owners  
Book index: [Market Strategy and Differentiation](README.md)  
Evidence report: [Browser market gap — July 2026](../research/browser-market-gap-2026-07.md)  
Last researched: 2026-07-16

## Purpose

Reduce switching cost without creating a new lock-in, and define safe paths for import, export, synchronization, and selective sharing.

## Migration

Importers should target Chrome, Edge, Firefox, Safari, Brave, Opera, Vivaldi, Arc, and Zen where formats and platform APIs permit. Candidate data includes bookmarks, history, credentials, open tabs, groups, Spaces, folders, pinned items, profile/container relationships, panels, search shortcuts, compatible extension settings, and web applications.

Every import produces a report of exact imports, transformations, omissions, failures, and required verification. Secrets use platform-approved channels and never pass through logs or generic interchange files.

## Open export

Turing state uses documented, versioned export formats with integrity checks, manifests, selective data classes, and forward/backward compatibility policy. Users can export without a Turing cloud account.

## Collaboration

Collaborative Spaces are later-stage research. Sharing is item-level, revocable, role-scoped, encrypted, and auditable. Cookies, credentials, private history, and unselected page content are excluded. A recipient can fork or export shared state.

## Sync

Sync requires end-to-end encryption where claimed, transparent conflict resolution, recovery keys, key rotation, metadata analysis, selective sync, deletion semantics, offline operation, self-hosting research, and failure testing. Account services must not become required for local browsing or export.

## Cross-cutting review

Any promotion from research must document security and privacy boundaries, accessibility behavior, compatibility implications, resource and energy budgets, migration and recovery, localization, operational ownership, legal/provenance constraints, unsupported behavior, and a removal or rollback path.

## Status discipline

This chapter records a hypothesis and evaluation contract. It does not claim that Turing implements the feature, that users prefer it, or that the feature will ship. Promotion requires the process in [Feature Prioritization, Validation, and Promotion](10-feature-prioritization-and-validation.md).
