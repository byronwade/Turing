# Semantic Observations and Redaction

Status: research and design baseline  
Owner: agent observation architecture  
Purpose: Produce useful model context while preserving origin, sensitivity, accessibility, and user expectations.

## Relationship to the Turing program

This document is the detailed owner for RQ-10 and AI-GATE-2/AI-GATE-4. Engine accessibility semantics are defined in the [engine book](../engine/08-input-editing-accessibility.md).

## Observation layers

Observation can include browser/session metadata, document and frame identity, accessibility semantics, visible text structure, form/control state, geometry/occlusion, selected DOM/CSS/layout diagnostics, network/console/performance summaries, screenshots, selected local files, tool results, and prior task memory. Each layer requires an explicit grant and sensitivity policy.

The default everyday snapshot favors user-perceivable semantics rather than raw DOM or pixels.

## Semantic snapshot

A snapshot contains origin, URL class, title, document epoch, frame ancestry, landmarks, headings, lists, tables, text excerpts, links, buttons, forms, dialogs, alerts, controls, accessible names/descriptions, roles, states, relationships, values when non-sensitive, bounds, focus, selection, validation, visibility, occlusion, and stable session-local references.

The schema is versioned, paginated, bounded, and deterministic enough for testing. References expire on document or relevant mutation epoch.

## Cross-origin and hidden content

Frames retain origin and process ownership. Cross-origin content is omitted unless an explicit grant permits a named frame/origin and the user can see that scope. Hidden, inert, display-none, offscreen, collapsed, metadata, comments, accessibility-only, and script-generated content carry source/visibility labels and are excluded by default unless needed.

The browser never treats hidden page instructions as trusted system policy.

## Sensitive data taxonomy

Sensitive classes include passwords, one-time codes, cookies, auth headers, passkey/credential material, payment data, hidden autofill, private messages, health/legal/government data, source code, local files/paths, enterprise content, precise location, device data, browser internal UI, and private-session context. Policies determine omit, redact, summarize, tokenize, or opaque-handle behavior.

Redaction occurs before provider serialization. Secrets cannot rely on model instruction to remain unused.

## Screenshots and vision

Vision is optional, visibly indicated, bounded to selected tab/region, and excludes browser chrome unless separately approved. Captures have origin, geometry, scale, color, timestamp, and sensitivity metadata. Remote transmission is previewable and governed by provider policy.

OCR or vision output remains untrusted page-derived content and cannot upgrade hidden pixels into authority.

## Developer observations

Developer grants may expose DOM, CSS, fragments, paint, accessibility, source maps, console, network, traces, tests, and selected workspace files. Cross-origin and secret rules remain. Local source requires explicit repository/file handles; an agent cannot walk the filesystem.

Large diagnostics are summarized with links or bounded streams instead of copying everything into model context.

## Context reduction

The reducer selects task-relevant data, preserves source and origin labels, deduplicates, summarizes, budgets tokens, and records what was omitted. It does not erase contradictory evidence or merge principals. Model context has an auditable manifest of observation versions, hashes, sensitivity, destination, and transformations.

## Non-negotiable invariants

- Default observations exclude secrets, browser internals, unrelated tabs, and ungranted cross-origin content.
- Every observation item retains source, origin/frame, visibility, sensitivity, and epoch context.
- Redaction occurs before data reaches a provider adapter.
- Screenshots and local files require explicit visible scope.
- Semantic references expire when the document or relevant target changes.
- Context reduction cannot merge authority or hide omitted-data uncertainty.

## Required evidence

- Schema golden tests and mutation/epoch invalidation tests.
- Secret, cross-origin, hidden-content, screenshot, local-file, and private-session leakage tests.
- Task-success, token size, latency, stale-target, and accessibility comparison against screenshot-first control.
- Provider payload manifests and secret scanning.
- User studies for data-scope comprehension.
- Adversarial pages using alt text, comments, metadata, overlays, and hidden instructions.

## Known risks and unresolved questions

- Accessibility semantics can expose content not visually apparent.
- Redaction can remove context needed for correct decisions.
- Screenshots may capture notifications or unrelated sensitive pixels.
- Stable node references can become tracking or stale-target hazards.

## Primary sources

- WAI-ARIA — https://www.w3.org/TR/wai-aria/
- Accessible Name and Description Computation — https://www.w3.org/TR/accname-1.2/
- Model Context Protocol architecture — https://modelcontextprotocol.io/docs/learn/architecture

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
