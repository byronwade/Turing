# 02 — Chrome-Class Capability Parity Matrix

“Render common websites” is a small fraction of a modern browser. Turing tracks parity by capability domain and maturity state. The allowed states are `unplanned`, `specified`, `prototype`, `partial`, `conformant-subset`, `release-gated`, and `supported`. A domain is never marked supported solely because one demo works.

## 1. Core browser product

| Domain | Required surface | Release evidence |
|---|---|---|
| Windows and tabs | multi-window, tab strip, pin/mute/group/move/duplicate, reopen, drag/drop, full screen, kiosk, native menus | cross-platform UI tests, crash recovery, keyboard and accessibility review |
| Navigation | address/search input, redirects, history traversal, reload variants, view source, error pages, captive portal behavior | navigation state-machine tests and hostile redirect corpus |
| Profiles | isolated cookies, storage, history, credentials, permissions, extensions, policies, models, sync keys | no cross-profile data-flow tests |
| Private sessions | ephemeral storage, private downloads/history rules, extension opt-in, memory cleanup | process and disk-forensics tests |
| History/bookmarks | search, folders, import/export, deduplication, recovery | migration and corruption tests |
| Downloads | safe naming, resume, quarantine, danger classifications, user prompts, sandboxed opening | malicious-file and path-confusion suite |
| Permissions | camera, microphone, location, notifications, clipboard, MIDI, serial, USB, Bluetooth, filesystem, display capture | per-origin and per-profile policy tests |
| Credentials | passwords, passkeys/WebAuthn, autofill, keychain integration, breach-warning hooks, export controls | phishing, origin-binding, and secret-redaction tests |
| Session recovery | windows/tabs, form-state policy, crash loops, version migration | forced-kill and corrupted-state scenarios |
| Sync | encrypted bookmarks, history, settings, tabs, optional credentials, conflict resolution, key recovery | protocol versioning, E2E crypto review, offline conflict tests |
| Updates | signed metadata, staged rollout, rollback, delta/full packages, minimum secure version | compromised-mirror and rollback-attack tests |

## 2. Web-platform engine

Turing’s engine backlog follows standards and test coverage rather than feature popularity alone.

### Documents and parsing

- HTML tokenizer, tree builder, quirks modes, templates, custom elements, shadow DOM, declarative shadow DOM, slots, mutation observers, ranges, selections, editing, clipboard events, drag and drop, focus, inertness, popovers, dialogs, forms, validation, autofill hooks, navigation timing, and document lifecycle.
- XML parsing and XML DOM where required by the platform; SVG and MathML integration.
- Character encoding detection and decoding through audited encoding tables.

### CSS and layout

- selectors, cascade layers, specificity, inheritance, custom properties, computed values, media/container/support queries, nesting, pseudo-elements, generated content, counters, fonts, color, backgrounds, borders, masks, filters, transforms, transitions, animations, variables, and typed values;
- block, inline, line breaking, floats, positioning, stacking contexts, flexbox, grid, multicolumn, tables, replaced elements, intrinsic sizing, aspect ratio, fragmentation, writing modes, bidi, vertical text, ruby, scroll snapping, overflow, containment, container queries, and view transitions;
- print layout and paged media as an explicit track, not an afterthought.

### Graphics and media-facing APIs

- Canvas 2D, SVG rendering, images, color management, WebGL compatibility track, WebGPU track, WebCodecs integration, fullscreen, picture-in-picture, media sessions, subtitles, encrypted-media integration subject to licensing, and capture APIs.

### Scheduling and execution environment

- event loop, tasks, microtasks, timers, rendering opportunities, requestAnimationFrame, idle callbacks, workers, shared workers where supported, service workers, worklets, structured clone, message channels, transferable objects, streams, fetch, abort, and lifecycle cancellation.

### Storage and offline

- cookies, partitioned cookies, Storage Access API policy, local/session storage, IndexedDB, Cache Storage, Origin Private File System, quotas, eviction, persistence grants, service-worker update algorithm, and clear-site-data behavior.

## 3. JavaScript and WebAssembly

Parity includes:

- current ECMAScript syntax and semantics tracked against Test262;
- modules, dynamic import, import maps, promises, async functions, iterators, generators, proxies, weak references, regular expressions, internationalization, temporal support when standardized, source maps, and error stacks;
- WebAssembly validation, execution, modules, tables, memories, streaming compilation, reference types, SIMD and threads only after sandbox and memory-model review;
- debugger hooks, coverage, CPU profiling, allocation profiling, heap snapshots, async stacks, and deterministic pause/resume semantics.

## 4. Networking and security behavior

- DNS and proxy policy; HTTP/1.1, HTTP/2, HTTP/3; TLS; certificate verification; HSTS; OCSP/CRL strategy; Alt-Svc; connection coalescing; caching; compression; content negotiation; authentication; WebSocket and WebTransport tracks;
- Fetch, CORS, preflight cache, CORP, COOP, COEP, CSP, Permissions Policy, Referrer Policy, SRI, mixed content, MIME sniffing, download response handling, origin-agent clusters, secure contexts, and private-network access policy;
- partitioning of caches, connections where needed, cookies, storage, service workers, permission decisions, and stateful anti-tracking surfaces.

## 5. Media, documents, and device integration

| Capability | Important constraint |
|---|---|
| Audio/video playback | codec availability and patent/licensing vary by platform and distribution model |
| DRM/encrypted media | Widevine-equivalent access requires commercial licensing and is a hard external dependency |
| PDF | viewer, search, forms, accessibility, printing, downloads, and sandboxing form a separate product surface |
| Printing | preview, pagination, native dialogs, background graphics, headers/footers, PDF output, and enterprise policy |
| Camera/microphone | origin permission, device enumeration privacy, indicators, background policy, and OS consent |
| Screen capture | persistent visible indicator, surface selection, protected-content rules, and agent restrictions |
| USB/serial/Bluetooth/HID | explicit user selection and a privileged broker; renderer never receives raw ambient device authority |
| Filesystem access | user-mediated handles, scoped persistence, revocation, and agent-specific confirmation |

## 6. Accessibility and internationalization

Chrome-class parity requires more than keyboard navigation:

- semantic accessibility tree for HTML, ARIA, SVG, Canvas fallback, forms, tables, live regions, dialogs, popovers, and custom controls;
- platform bridges for UI Automation on Windows, NSAccessibility on macOS, and AT-SPI on Linux;
- screen reader, switch control, voice control, magnification, high contrast, reduced motion, forced colors, caret browsing, zoom, text scaling, and focus visibility;
- Unicode normalization and segmentation, bidirectional text, script shaping, locale-sensitive formatting and collation, IMEs, dead keys, composition, vertical writing, ruby, emoji, and font fallback.

Accessibility-tree correctness is also the preferred semantic observation surface for agents, but agents do not receive hidden or cross-origin accessibility data.

## 7. Developer platform

- Elements/DOM inspector, computed styles, box model, event listeners, accessibility inspection, layout overlays, CSS editing, source mapping, breakpoints, watch expressions, console, snippets, network waterfall, request replay with safety controls, storage inspection, service-worker controls, performance timeline, frame analysis, memory tools, rendering diagnostics, security panel, issues panel, protocol monitor, and crash diagnostics;
- a versioned remote debugging protocol and WebDriver BiDi compatibility track;
- deterministic headless mode using the same engine and security model, not a separate rendering implementation;
- extension developer mode, signing policy, permission review, service-worker/background execution, content scripts, native messaging broker, and store/update model.

## 8. Extensions and ecosystem

The long-term target includes a documented WebExtensions compatibility layer, beginning with a deliberately small Manifest V3-style subset. Compatibility does not imply access to Chrome Web Store distribution or proprietary Google services. Required areas include tabs, windows, navigation, storage, permissions, commands, context menus, content scripts, declarative network rules, downloads, bookmarks, history, DevTools panels, and native messaging.

Extension processes are isolated from renderers and from each other where feasible. Host permissions are visible, revocable, profile-specific, and included in resource attribution. An extension cannot act as an unreported agent-authorization bypass.

## 9. Enterprise and managed environments

- machine/user/profile policy layers; policy precedence; templates and schema; managed bookmarks; proxy and certificate configuration; update channels; extension allow/block lists; URL filtering hooks; data-loss prevention integration points; audit events; browser sign-in policy; device trust; kiosk; and long-term support channels.

Enterprise capability is not a phase-one requirement, but architecture that makes policy impossible would block later parity.

## 10. Proprietary and external parity blockers

The following may prevent literal “no exceptions” parity even after the open web platform is mature:

1. proprietary DRM modules and licensing;
2. patented codec distribution and royalties;
3. access to vendor-owned sync, account, safe-browsing, translation, payment, or extension-store services;
4. platform store rules, signing certificates, notarization, and default-browser restrictions;
5. websites that intentionally gate by user agent or approved browser list;
6. security reputation systems that require large telemetry and abuse-response infrastructure.

Turing documents these as external dependencies. It does not fake support, bypass access controls, or hide incompatible behavior.

## 11. Parity gate

The phrase **Chrome-class general-purpose browser** may be used only after all release-critical rows have owners, tests, support statements, security coverage, and update procedures. The phrase **Chrome-equivalent** is reserved for a versioned comparison report showing the exact tested Chrome version, platform, test corpus, pass rates, unsupported proprietary services, and security caveats.

Use the checked no-claim [Chrome-Class Capability Traceability Map](../research/chrome-class-capability-traceability-map-2026-07.md) to route each parity domain to current requirements, readiness blockers, work packages, proposed task handoffs, next proof, and prohibited claims. That map is traceability only; it is not parity, compatibility, security, accessibility, performance, production, or release evidence.

<!-- MARKET-STRATEGY-2026-07 -->
## Parity versus differentiation

Vertical tabs, workspaces, split views, sidebars, synchronized groups, browser AI, and extension support are increasingly table stakes. The `OP-*` portfolio defines proposed differentiators but does not replace parity requirements. Failed or unsupported sites remain in compatibility denominators even when a differentiated workflow is strong.
