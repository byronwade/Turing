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

- parsing/style/layout/paint/accessibility semantics documented;
- full recomputation and incremental result agree;
- WPT/reduced semantic tests and pixel/geometry tests added;
- invalidation reason and performance trace exposed;
- international text, zoom, writing mode, and accessibility considered;
- pathological complexity and memory capped.

## JavaScript, GC, JIT, or WebAssembly

- Test262 or specification cases added;
- interpreter/reference semantics established;
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
- negative capability tests added on each affected platform;
- exploit chain and residual risk described;
- mitigations enabled in release-equivalent configuration;
- update and incident implications addressed;
- independent review requirement identified.

## Agent feature

- observation fields, sources, redaction, and cross-origin scope documented;
- action schema, preconditions, document epoch, idempotency, and postcondition defined;
- risk classification and confirmation behavior deterministic;
- prompt-injection, stale target, secret request, cancellation, and resource exhaustion tests added;
- provider/local data flow visible and auditable;
- model cannot approve or expand its own grant.

## Performance optimization

- correctness/security/accessibility baseline unchanged or differences explicitly approved;
- before/after raw samples, environment, workload, process topology, lifecycle, and statistical method attached;
- memory attribution reconciled;
- no benchmark-specific path;
- regression threshold and rollback plan defined;
- claimed scope does not exceed measured scope.

## Release or update change

- clean-build, reproducibility, SBOM, provenance, notices, symbols, and build identity aligned;
- tamper, replay, rollback, expiry, disk-full, power-loss, and partial-install tests pass;
- profile migration/downgrade behavior defined;
- signing authority and audit reviewed;
- emergency response and supported-version impact documented.
