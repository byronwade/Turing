# DevTools Workflows and User Interface

Status: research and design baseline  
Owner: DevTools product design  
Purpose: Design tools around high-value debugging outcomes rather than panels copied from another browser.

## Relationship to the Turing program

This document deepens [Blueprint 11](../blueprint-v1/11-product-ui-devtools.md). Protocol contracts are defined in [Protocol architecture and versioning](01-protocol-architecture-and-versioning.md).

## Workflow-first design

The primary design unit is a developer question: why did this style win, why did layout run, what blocked input, what retained memory, why did a request fail policy, which process owns a frame, why did an agent action fail, or how can a defect be reproduced? Panels and views are composed to answer those questions with engine causality.

Every workflow records expected skill level, minimum clicks/commands, keyboard path, screen-reader path, data required, privacy risk, latency budget, and success criteria.

## Elements, styles, and layout

The Elements workflow exposes live DOM and shadow trees, accessible name and role search, mutation history, attributes/text editing with undo, event listeners, custom-element state, matched rules, cascade layers, scoping, variables, computed-value provenance, pseudo state, container queries, animation, font selection, box model, fragments, intrinsic sizes, grids, flex, scroll, stacking, paint order, hit regions, and invalidation reasons.

Editing uses transactions and clearly distinguishes temporary local overrides from page source.

## Sources and runtime

Sources covers scripts, modules, workers, service workers, source maps, WebAssembly, generated code, breakpoints, event/DOM/network breakpoints, stepping, async stacks, realms, scopes, watches, blackboxing, coverage, parse/compile timing, tiers, deoptimization, and code cache. Console evaluation always names its target realm and security context.

Pasting or executing code is visibly privileged; self-XSS and remote attachment warnings are accessible and non-dismissive without becoming obstructive.

## Network and storage

The network workflow exposes initiator, request identity, top-level partition, service worker, redirect chain, priority, DNS/connect/TLS, protocol, connection reuse, cache, credentials mode, cookies, CORS/CSP/mixed-content decisions, streaming, compression, body sizes, cancellation, and security state. Sensitive fields are redacted with an explicit local reveal path.

Storage views show origin/profile/partition, quota, transaction state, schema/migration version, durability, service workers, cache storage, cookies, IndexedDB, and clear-site-data effects.

## Performance and memory

The performance workflow aligns input, tasks, script, GC, style, layout, paint, raster, composite, network, workers, GPU, browser chrome, extensions, agents, energy, and process scheduling on one causal timeline. Developers can jump from a long interaction to source, invalidation root, layout fragment, allocation owner, or network request.

Memory views combine JS heap snapshots, allocation sampling, DOM retainers, detached documents, native semantic categories, GPU resources, cache entries, process maps, shared/charged totals, and lifecycle before/after comparisons.

## Security, accessibility, and agent tools

Security tools explain origin, certificate, secure context, sandbox, isolation, permission, policy header, credential, internal-page, extension, and update state. Accessibility tools expose semantic tree, name calculation, relationships, focus order, keyboard path, live regions, contrast, text ranges, platform mappings, and issues.

Agent tools show observation redaction, source labels, grant, policy result, confirmation, action, effect, budget, provider data flow, and audit. They cannot modify grants invisibly.

## UI architecture

The DevTools frontend runs in a dedicated constrained process, uses strict CSP, versioned protocol clients, virtualized large views, bounded caches, and crash recovery independent from the inspected renderer. Docking, multiple windows, multi-target sessions, high DPI, localization, themes, reduced motion, keyboard, and assistive technology are first-class.

The tool remains responsive under trace, heap, and network volume by streaming, summarizing, and offloading analysis without hiding loss.

## Non-negotiable invariants

- Tools answer documented workflows and expose causal engine truth.
- Temporary edits are transactional, reversible, and distinct from source changes.
- Console and evaluation always identify target realm and privilege.
- Large views remain bounded and report sampling, dropping, or truncation.
- Security, accessibility, and agent diagnostics receive equal product quality.
- A DevTools crash or hang cannot compromise or remove browser trusted UI.

## Required evidence

- Timed developer studies for representative debugging tasks and error rates.
- Keyboard, screen-reader, high-contrast, localization, and large-data usability tests.
- Protocol latency and frontend frame/memory budgets under heavy traces.
- Cross-browser workflow comparison with version/config capture.
- Crash, detach, reconnect, target navigation, and process restart recovery.
- Sensitive-data redaction and reveal-path security review.

## Known risks and unresolved questions

- Panel accumulation can create complexity without improving workflow success.
- Tool instrumentation can perturb performance and memory.
- Local overrides and evaluation can be confused with production behavior.
- High-volume data can cause DevTools to destabilize the target.

## Primary sources

- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/
- Firefox Remote Protocol — https://firefox-source-docs.mozilla.org/remote/index.html
- WAI-ARIA — https://www.w3.org/TR/wai-aria/
- Accessible Name and Description Computation — https://www.w3.org/TR/accname-1.2/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
