# 20 — Definition of Done by Work Type

This checklist prevents architecture work from becoming presentation-only.

## Parser or decoder

- normative source and supported subset documented;
- valid, invalid, truncated, oversized, deeply nested, slow, cancelled, and OOM behavior tested;
- streaming and restart behavior defined where relevant;
- allocation and recursion limits enforced before large work;
- structured fuzzer and seed corpus added;
- output ownership and sandbox boundary documented;
- differential and reduced regression cases included;
- logs contain no input secrets by default.

## State machine or lifecycle

- states, events, guards, side effects, recovery, and terminal behavior explicit;
- invalid transitions fail closed;
- model/property tests cover generated sequences;
- identity and document/profile epochs revalidated after asynchronous work;
- cancellation, timeout, crash, and restart covered;
- trace events and user-visible consequences defined.

## IPC or privileged broker

- sender and receiver roles declared;
- message schema versioned and bounded;
- capability and identity source identified;
- privileged receiver recomputes sensitive policy;
- malformed, stale, duplicate, reordered, oversized, and unauthorized requests tested;
- queue/backpressure behavior defined;
- compromised-process harness and fuzz target updated.

## UI or product workflow

- keyboard, focus, screen-reader, zoom, contrast, forced-color, and reduced-motion paths tested;
- origin/profile/permission/security/agent state cannot be spoofed or hidden;
- loading, empty, error, offline, crash, stale, and recovery states designed;
- responsiveness measured under renderer hang and memory pressure;
- commands and shortcuts documented;
- no critical state relies on color or animation alone.

## Engine rendering feature

- parsing/style/layout/paint/accessibility semantics documented in the owning Blueprint and [engine book](../engine/README.md);
- full recomputation and incremental result agree;
- WPT/reduced semantic tests and pixel/geometry tests added;
- invalidation reason and performance trace exposed;
- international text, zoom, writing mode, and accessibility considered;
- pathological complexity and memory capped.

## JavaScript, GC, JIT, or WebAssembly

- Test262 or specification cases added;
- interpreter/reference semantics established;
- detailed runtime contracts updated in the [JavaScript book](../javascript/README.md);
- GC root/barrier/weak/finalization behavior stress-tested;
- JIT tiers differentially equivalent and W^X enforced;
- deoptimization, traps, exceptions, OOM, and cancellation covered;
- sanitizer, fuzzer, and generated-code validation updated;
- no-JIT behavior remains functional when applicable.

## Network or storage

- profile/origin/site/partition context explicit;
- cross-origin, credentials, redirects, service worker, cache, and security-header behavior tested;
- disk full, corruption, migration interruption, process crash, clock change, and quota covered;
- secrets and sensitive headers redacted;
- retry and idempotency rules defined;
- renderer receives no ambient socket or filesystem capability.

## Security or sandbox

- threat model and protected assets updated;
- [security engineering book](../security-engine/README.md) updated for affected boundaries and evidence;
- negative capability tests added on each affected platform;
- exploit chain and residual risk described;
- mitigations enabled in release-equivalent configuration;
- update and incident implications addressed;
- independent review requirement identified.

## Developer protocol, DevTools, API, or automation

- public and internal contract boundaries documented in the [developer](../developer-experience/README.md) and [API](../api-design/README.md) books;
- schema, identity, authority, bounds, deadlines, cancellation, backpressure, partial failure, and redaction defined;
- stable/experimental status and compatibility support window declared;
- generated clients and conformance tests updated where applicable;
- remote attachment, headless, and automation profile security tested;
- trace/event causality and unsupported behavior visible.

## Agent feature

- observation fields, sources, redaction, and cross-origin scope documented;
- action schema, preconditions, document epoch, idempotency, and postcondition defined;
- detailed trust, provider, planning, memory, and evaluation contracts updated in the [AI book](../ai/README.md);
- risk classification and confirmation behavior deterministic;
- prompt-injection, stale target, secret request, cancellation, and resource exhaustion tests added;
- provider/local data flow visible and auditable;
- model cannot approve or expand its own grant.

## Performance optimization

- correctness/security/accessibility baseline unchanged or differences explicitly approved;
- [performance book](../performance/README.md) updated for affected critical paths, accounting, or measurement;
- before/after raw samples, environment, workload, process topology, lifecycle, and statistical method attached;
- memory attribution reconciled;
- no benchmark-specific path;
- regression threshold and rollback plan defined;
- claimed scope does not exceed measured scope.

## Research or competitive study

- question, sources/versions, method, observation, inference, confidence, limitations, and falsifying evidence recorded;
- official or primary sources preferred and retrieval date recorded for changing systems;
- product, engine, runtime, service, and platform conclusions kept separate;
- recommendations mapped to an experiment and owning Blueprint/detailed book;
- requirements, risks, ADRs, or work-package status changed only when decision evidence justifies it;
- study linked from an indexed document and research log updated.

## Release or update change

- clean-build, reproducibility, SBOM, provenance, notices, symbols, and build identity aligned;
- tamper, replay, rollback, expiry, disk-full, power-loss, and partial-install tests pass;
- profile migration/downgrade behavior defined;
- signing authority and audit reviewed;
- emergency response and supported-version impact documented.

## Networking, storage, media, platform, accessibility, and operations research

- the owning detailed book and Blueprint chapter agree;
- identities, authority, lifetime, limits, failure, recovery, platform variance, and unsupported cases are explicit;
- primary specifications and test-suite revisions are recorded;
- threat, privacy, accessibility, compatibility, performance, memory, energy, licensing, and operational effects are reviewed;
- falsifiable experiments, fixed environments, raw evidence, confidence, owners, and revisit triggers are defined;
- no research statement is presented as implemented or supported.

## Developer tooling or diagnostic workflow

- target, profile, origin, frame, process, realm, and document epoch are explicit;
- protocol messages are versioned, bounded, cancellable, authenticated where remote, and redacted by default;
- trace causality, replay limitations, divergence, failure, and partial output are visible;
- keyboard and screen-reader workflows are tested;
- diagnostic bundles preview included fields and exclude secrets;
- workflow time and failure rate are measured against reference tools where leadership is claimed.

## Framework or dependency adoption

Exact source/version, owner, alternatives, privilege, hostile input, unsafe/native, license/provenance, fuzzing, platforms, performance/build cost, update and replacement are reviewed. Research mention is not adoption.

## Plug-in or embedding feature

Manifest/API, authority, identity, lifecycle, cancellation, resource, data, accessibility, compatibility, packaging, update, conformance, failure, and support are explicit.

## Professional control-plane change

Ownership, traceability, phase, decision class, review, evidence, exception, documentation, release, and capacity records agree.

<!-- MARKET-STRATEGY-2026-07 -->
## Market opportunity or differentiation feature

- stable `OP-*` record, target segment, job, alternatives, and contrary evidence;
- observed evidence separated from inference and product proposal;
- security, privacy, accessibility, compatibility, performance, energy, recovery, migration, localization, legal, and maintenance review;
- prototype and controlled task study with raw evidence;
- simpler core, Plug-in, compatibility adapter, and rejection alternatives considered;
- accepted requirements, risks, ADRs, work packages, ownership, and traceability updated only after promotion;
- experimental expiry, removal, rollback, and support language defined;
- no competitor code, branding, assets, or misleading equivalence claim.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI framework, shell component, or adapter

- toolkit-neutral state, typed commands, identities, epochs, threading, cancellation, error, and recovery behavior documented;
- no product/security logic exists only in toolkit or React design code;
- keyboard, focus, accessibility, IME, clipboard, drag/drop, localization, themes, and failure states tested;
- page-surface, damage, scale, occlusion, capture, renderer crash, and GPU loss covered where applicable;
- binary, package, startup, memory, allocations, input, frame pacing, energy, and hidden-window evidence attached;
- backend, renderer, feature flags, dependencies, unsafe/native surface, license, provenance, updates, and replacement plan reviewed;
- release build contains no prohibited webview, runtime React/JavaScript, Node, runtime UI interpreter, or unused backend;
- owning Native UI Runtime, platform, product, security, performance, accessibility, repository, and readiness records agree.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent-executed production work

- approved `TASK-*` manifest and scoped authority;
- authoring and independent-review identities are distinct;
- run manifest records model, instructions, source, environment, tools, commands, and credentials by identifier;
- failed runs and limitations are preserved;
- evidence bundle reconciles acceptance criteria and negative tests;
- no self-approval, self-merge, signing, disclosure, or stable-promotion authority;
- rollback and escalation are verified.

## Production or stable release

- finite accepted scope and platform matrix;
- all applicable `PRG-*` gates ready with evidence;
- numeric blocking `SLO-*` targets within error budget;
- compatibility, security, accessibility, migration, update, provenance, service, support, legal, and incident evidence complete;
- qualified primary and backup owners active;
- human production-readiness and release approval recorded;
- exact artifact digest, signatures, update metadata, rollback, and supported-version statement published.
