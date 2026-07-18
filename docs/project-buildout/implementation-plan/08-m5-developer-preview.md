# 08 — M5: Coherent Developer Preview

Status: implementation game plan; developer preview is not a safe daily-browser claim
Owner: product, engine, developer experience, accessibility, security, release operations, and quality

## 1. Objective

M5 turns the separate engine and service laboratories into one coherent, signed, auto-updating developer preview for controlled, non-sensitive testing. The priority is a trustworthy integrated product with explicit compatibility gaps, not a broad but opaque demo.

## 2. Entry gates

- M1 shell/process/sandbox laboratory passes on the reference platform.
- M2 static engine and M3 interpreter have declared conformance maps.
- M4 navigation/network/storage boundaries pass cross-origin and recovery tests.
- profile/session formats are versioned with upgrade and rollback rules.
- update laboratory verifies artifact identity and rollback.
- product accessibility baseline and issue-triage process exist.
- emergency developer-channel patching has an owner and rehearsal.

## 3. Engine breadth

Expand the reference engine in measured slices:

- inline layout, bidi, writing modes, vertical text, richer font fallback;
- flexbox, grid, tables, floats, positioning, fragmentation foundations;
- transforms, transitions, animations, stacking, filters where bounded;
- compositor scrolling and retained display-list invalidation;
- richer SVG and Canvas 2D;
- editing, selection, forms, spellcheck interfaces, and clipboard UX;
- accessibility tree breadth and live updates;
- image formats and color management with decoder isolation;
- service-worker/offline breadth and HTTP/2 only after protocol evidence.

Each feature uses WPT/reduced tests, full-recompute equivalence, fuzzing, traces, and performance budgets.

## 4. Product shell

Deliver a coherent but deliberately scoped browser:

- windows, profiles, private sessions, tabs, folders, and initial Spaces;
- address/search/command field;
- history, bookmarks, downloads, page information, permissions, settings, and safe mode;
- session restore and Workspace Time Machine research subset;
- Resource Truth Center showing actual lifecycle/resource facts;
- migration report and open export for supported data classes;
- update status, rollback status, crash recovery, and diagnostics;
- complete keyboard command discovery;
- native accessibility, zoom, contrast, forced colors, reduced motion, and localization foundations.

Proposed market features remain experimental until promoted through requirements and evidence.

## 5. WP-015 — DevTools, automation, and trace viewer

M5 integrates the initial production-shaped developer surface:

- versioned target discovery and attachment;
- Elements/DOM/accessibility inspection;
- styles, cascade, layout, paint, and invalidation explanation;
- Console and interpreter debugger;
- Network, Storage, Security, Service Worker, Performance, and Memory foundations;
- process, lifecycle, resource, and causal trace viewer;
- deterministic headless profiles and virtual-time foundation;
- WebDriver BiDi implementation for the supported draft/revision;
- generated clients, authentication, bounds, cancellation, backpressure, and redaction;
- safe diagnostic bundle and reduced-test export.

## 6. Release and update channel

The developer preview uses:

- signed artifacts and metadata;
- isolated development/preview channels;
- phased rollout, pause, rollback, and minimum secure version;
- build identity, symbols, SBOM, provenance, notices, and source revision;
- profile migration transaction and downgrade protection;
- crash reporting that is opt-in or explicitly configured and redacted;
- documented uninstall/export/recovery behavior.

It does not use production root/signing ceremonies reserved for stable releases unless the same infrastructure has been formally approved.

## 7. Quality gates

- exact WPT/Test262 feature and failure maps;
- no hidden denominator or site-specific compatibility behavior without owner and expiry;
- sandbox/site-isolation evidence for all included hostile-input processes;
- sustained fuzzing for critical parsers and runtime surfaces;
- fixed-hardware startup, input, frame pacing, memory, energy, network, and storage baselines;
- product accessibility critical-flow matrix;
- migration, upgrade, rollback, crash, and data-loss testing;
- security review of trusted UI, permissions, credentials, downloads, DevTools, and updater;
- user study for onboarding, error recovery, resource controls, and switching cost.

## 8. Exit criteria

M5 exits when:

- signed developer-channel packages update and roll back reliably;
- security owners can issue an emergency developer-channel fix;
- the UI accessibility baseline passes on the reference platform;
- exact compatibility reports are public or attached to every build;
- critical data-loss, sandbox, update, and trusted-UI issues are resolved;
- supported developer workflows are reproducible;
- product and engine limitations are visible inside the product and documentation;
- the release remains labeled developer preview and not a secure replacement for established browsers.
