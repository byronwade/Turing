# Turing Plug-in Platform

Status: architecture and product research; no Plug-in runtime or store exists  
Owner: Plug-in platform, security, product, ecosystem, and accessibility  
Last researched: 2026-07-16

Turing calls extensibility units **Plug-ins**. Every Plug-in—including first-party packages—is an untrusted, separately identified, revocable, resource-bounded principal.

## Native architecture

- Tier A: first-party maintained, separately updateable component with no kernel linkage or blanket privilege.
- Tier B: portable WebAssembly component using WIT imports, memory/fuel/epoch limits, cancellation, isolated storage, and no ambient WASI.
- Tier C: restricted WebExtensions compatibility adapter with a published API matrix; it does not define native Turing APIs.
- Tier D: visible developer-only local package in isolated profiles; never silently loaded by normal signed builds.
- Unrestricted third-party native code is prohibited by default. Native messaging is a separately installed, allowlisted broker.

## Manifest and package contract

A signed deterministic package declares publisher, package/version/API range, runtime tier, entry points, hashes, provenance, license, capabilities, origins, profiles/private mode, data classes, remote endpoints, user activation, confirmation class, resource budgets, background eligibility, UI/accessibility metadata, update/rollback, and support status. Signatures establish identity and integrity; they do not grant authority.

Plug-ins cannot access raw credentials, cookies, unrestricted sockets, arbitrary files, unrelated profiles, hidden cross-origin content, raw browser memory, generic IPC, trusted browser UI, or agent confirmation authority.

## Resource and lifecycle model

Account CPU, memory, GPU, wakeups, network, disk, storage, model tokens/cost, and logs. States include installed, disabled, idle, starting, active, suspended, terminating, crashed, quarantined, updating, and removed. Background work is event-driven, cancellable, bounded, suspendable, and visible in the resource manager.

## First-party portfolio research

1. Turing Assistant
2. Developer Copilot
3. Screenshot Studio
4. Interaction Recorder
5. Translation and Language Tools
6. Reader and Research Mode
7. Writing Assistant
8. Dark/Contrast/Focus Modes
9. Privacy Inspector
10. Content Filter Lists
11. Tab and Workspace Organizer
12. Notes and Web Clipper
13. Archive and Export
14. JSON and Data Inspector
15. API and Request Toolkit
16. Accessibility Inspector
17. Performance and Resource Profiler
18. Framework and Source Inspector
19. Shopping Comparison
20. Meeting and Media Notes

This is a workflow cohort, not a claim of the exact global top twenty. Google does not publish a stable reproducible worldwide Chrome Web Store ranking. The portfolio learns from recurring demand and Google's 2025 favorite-extension editorial list without copying third-party code, branding, assets, or descriptions.

Start with lower-risk, locally useful packages: Screenshot Studio, Tab/Workspace Organizer, JSON/Data Inspector, Accessibility Inspector, Performance/Resource Profiler, Translation, read-only Turing Assistant, and Developer Copilot. Credentials, user scripts, network modification, media capture, shopping, remote AI, and consequential automation require later gates.

## Store, SDK, and governance

The store links listing to signed package, performs automated and risk-based manual review, shows capabilities/data/resource/accessibility/update history, supports appeal and transparency, and uses signed update metadata with minimum secure versions and narrow revocation. SDKs are generated from schemas and include project generator, manifest linter, capability simulator, test profile, package inspector, DevTools, compatibility report, and conformance suite.

## Primary sources

- Chrome Extensions — https://developer.chrome.com/docs/extensions/
- Chrome Manifest V3 — https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3
- Chrome extension security — https://developer.chrome.com/docs/extensions/mv3/security
- Google favorite extensions of 2025 — https://blog.google/products-and-platforms/products/chrome/our-favorite-chrome-extensions-of-2025/
- MDN WebExtensions — https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions
- WebAssembly Component Model — https://component-model.bytecodealliance.org/

<!-- MARKET-STRATEGY-2026-07 -->
## Space and market-strategy integration

Plug-ins may be installed per Space, receive session-only grants, and appear in resource/privacy receipts. First-party candidates should validate the market portfolio through the same bounded platform. Market popularity never grants privileged APIs.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Plug-in UI composition

Plug-ins do not receive arbitrary native toolkit objects, React execution, or direct access to trusted chrome. Plug-in UI is expressed through constrained schema-backed surfaces or isolated content, with capabilities, accessibility metadata, lifecycle, resource attribution, and user-visible origin. First-party Plug-ins follow the same boundary.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Production Plug-in readiness

A public Plug-in ecosystem requires signed packages, update/revocation, store operations, compatibility windows, capability review, resource SLOs, incident response, support, and stable release gates. Agent popularity or market demand cannot bypass those controls.
