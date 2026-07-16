# Product, Localization, Documentation, and Sustainability

Status: detailed research and professional operating baseline  
Owner: product, accessibility, localization, documentation, community, and program owners  
Last researched: 2026-07-16

## Purpose

Define the design system, trusted content, localization, documentation freshness, staffing, funding, infrastructure, succession, and safe scope reduction required to sustain the browser.

## Governing principles

- Trusted state is unmistakable and resistant to page imitation.
- Every component defines loading, empty, error, offline, crash, stale, and recovery states.
- Examples and commands are tested where practical.
- Supported scope cannot exceed patch, test, release, and communication capacity.
- Funding and material conflicts are disclosed.

## Required contract

- Maintain design tokens, component catalog, command/shortcut registry, trusted-surface rules, semantic/focus behavior, performance budget, and spoofing analysis.
- Maintain localization IDs, translator context, plural/gender, locale fallback, bidi, pseudo-localization, and security-language review.
- Require document owner, status, last/next review, applicable versions, evidence dependencies, and supersession.
- Validate examples, links, anchors, IDs, sources, and stale claims.
- Model staffing, backup, on-call, audits, CI/fuzz hardware, signing, distribution, support, standards, legal, Plug-in services, and AI providers by phase.
- Reduce supported scope when capacity evidence fails; define maintenance, archive, and EOL modes.

## Professional workflow

1. Map product need to workflow and trusted-state review.
2. Prototype all states.
3. Run keyboard, assistive-technology, localization, and comprehension studies.
4. Test docs/examples in CI.
5. Review capacity quarterly.
6. Update support or reduce scope when obligations exceed capacity.

## Evidence and exit gates

- PBO-GATE-14: release docs match the shipped build.
- PBO-GATE-16: stable has an owned design and localization pipeline.
- PBO-GATE-18: scope is reduced when sustained capacity fails.
- No critical service or account depends on one person.

## Risks and failure modes

- Custom UI can lag native behavior.
- Localization can alter security meaning.
- Metadata can be rubber-stamped.
- Funding or burnout can interrupt security response.

## Primary sources

- WAI-ARIA Authoring Practices — https://www.w3.org/WAI/ARIA/apg/
- Unicode CLDR — https://cldr.unicode.org/
- Write the Docs: docs as code — https://www.writethedocs.org/guide/docs-as-code/
- CHAOSS metrics — https://chaoss.community/kb-metrics-and-metrics-models/

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.

<!-- MARKET-STRATEGY-2026-07 -->
## Portfolio sustainability

The `OP-*` portfolio is capacity-constrained. Each promoted differentiator identifies what it replaces, maintenance staffing, localization and support cost, telemetry/data obligations, deprecation path, and conditions for removal. Feature count is not a success metric.
