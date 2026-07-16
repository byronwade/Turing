# Profile Stores, History, Bookmarks, Settings, and Journals

Status: detailed research and design baseline  
Owner: storage, profile data, migration, and recovery engineering  
Book index: [README](README.md)  
Canonical overview: [Blueprint owner](../blueprint-v1/07-network-storage-media.md)

## Purpose

This chapter defines the research contract for **profile stores, history, bookmarks, settings, and journals**. It is not an implementation or support claim. The design must remain compatible with the owning Blueprint, requirements, risks, security model, performance contract, accessibility obligations, and documentation policy.

## Scope

The study covers:

- store separation;
- append journals;
- indexes;
- lazy loading;
- sync hooks;
- session restore;
- backups;
- user export;

The scope includes normal use, hostile input, compromised-process assumptions, low-memory systems, cancellation, timeout, crash, restart, migration where applicable, accessibility, diagnostics, and operational ownership.

## Design objectives

1. Preserve profile, origin, site, frame, process, document-epoch, capability, and resource-owner identity wherever the subsystem crosses a boundary.
2. Make limits, state transitions, failure, cancellation, retry, recovery, and unsupported behavior explicit.
3. Minimize privileged code, ambient authority, copies, allocations, unbounded queues, hidden wakeups, and duplicate state.
4. Keep a deterministic correctness path and semantic trace before accepting incremental, concurrent, cached, hardware-accelerated, or speculative paths.
5. Treat accessibility, privacy, security, developer observability, energy, and maintainability as coequal design constraints.

## Architecture questions

- What are the authoritative inputs, outputs, identities, epochs, owners, and lifetime boundaries?
- Which data may be immutable, shared, cached, moved, serialized, persisted, or recomputed without widening authority?
- Which operations require a broker, user activation, permission, confirmation, platform API, or release-time capability?
- Where can a renderer, extension, DevTools client, model, corrupted store, native dependency, or remote peer act maliciously?
- Which work belongs on the user's critical path, and which work can yield, cancel, batch, degrade, or move to an isolated worker?
- How does the subsystem expose causality without logging secrets or retaining sensitive payloads?

## Data and lifecycle contract

Every durable design note must enumerate:

- typed identifiers and their issuer;
- state machine, valid transitions, guards, side effects, and terminal states;
- ownership, allocation class, byte/task/queue/time budget, and pressure behavior;
- synchronization, ordering, atomicity, idempotency, and stale-epoch behavior;
- persistence, schema/versioning, migration, rollback, clearing, and recovery where relevant;
- platform-specific behavior and the portable semantic core;
- exact unsupported cases and the safe failure mode.

## Performance and resource requirements

Measurements report p50, p95, and p99 latency where interaction is involved; live, reserved, committed, resident, shared, compressed, swapped, and GPU memory where relevant; CPU time, queue wait, wakeups, network/disk bytes, energy, and thermal state; and the effect of site isolation, process count, tab lifecycle, extensions, DevTools, and agents.

An optimization is not accepted from a microbenchmark alone. It must preserve conformance, security mitigations, accessibility paths, failure behavior, and a default-equivalent configuration. Tail regressions, extra process launches, larger working sets, or increased recovery cost remain visible.

## Security and privacy requirements

- Validate untrusted sizes, counts, enums, offsets, recursion, nesting, handles, paths, versions, and identities before privileged work or large allocation.
- Revalidate capability, profile, origin, site, target, and epoch after asynchronous delay.
- Redact secrets at the source; routine traces use IDs, classifications, hashes, sizes, and reason codes rather than raw content.
- Bound retries, concurrency, queues, caches, streams, logs, diagnostic exports, and persistent records.
- Define compromised-component tests and the assets that remain inaccessible after compromise.
- Do not weaken isolation, certificate or update verification, trusted UI, permissions, confirmation, or data partitioning to improve compatibility or a benchmark.

## Developer and accessibility requirements

The subsystem exposes stable, schema-defined diagnostics for state, ownership, causality, limits, policy decisions, errors, cancellation, and recovery. The UI and protocol distinguish physical totals from charged estimates and current facts from inferred causes. Keyboard, screen-reader, zoom, contrast, localization, text input, and reduced-motion behavior are considered whenever the subsystem affects users or developer tools.

## Failure and recovery

Research must cover malformed input, timeout, cancellation, process crash, browser crash, restart, low memory, allocation failure, disk full, network loss, GPU/device loss, sleep/resume, clock change, stale handles, version mismatch, partial operation, and repeated failure. Recovery must not silently lose user work, widen authority, accept stale state, or loop indefinitely.

## Falsifiable experiments

1. Prototype and measure store separation under representative, adversarial, failure, cancellation, and pressure conditions.
2. Prototype and measure append journals under representative, adversarial, failure, cancellation, and pressure conditions.
3. Prototype and measure indexes under representative, adversarial, failure, cancellation, and pressure conditions.
4. Prototype and measure lazy loading under representative, adversarial, failure, cancellation, and pressure conditions.
5. Prototype and measure sync hooks under representative, adversarial, failure, cancellation, and pressure conditions.

Each experiment records commit, platform, hardware, build flags, corpus, security configuration, process topology, tab state, sample count, raw samples, statistical treatment, failures, unsupported cases, and confidence. A result that cannot be reproduced remains exploratory.

## Evidence gates

- specification and data-model review;
- unit, property/model, malformed-input, negative-capability, timeout, cancellation, recovery, and OOM tests;
- WPT, Test262, protocol, platform, accessibility, or other primary conformance evidence where applicable;
- structure-aware fuzzing and corpus minimization for parsers, protocols, state machines, and persisted formats;
- semantic trace or full-recomputation/reference oracle;
- fixed-hardware latency, memory, energy, and longevity baselines;
- explicit residual risks, owner, revisit trigger, and unsupported matrix.

## Risks

Primary risks are semantic divergence, confused-deputy behavior, stale identity, unbounded work, memory retention, cross-profile or cross-origin leakage, native or platform compromise, hidden performance cliffs, inaccessible failure UI, unreliable recovery, and documentation becoming more certain than the evidence.

## Primary sources

- https://storage.spec.whatwg.org/
- https://w3c.github.io/IndexedDB/
- https://w3c.github.io/ServiceWorker/
- https://sqlite.org/
- https://w3c.github.io/webappsec-clear-site-data/

Source URLs are starting points. An implementation records the exact revision, retrieval date, local patches, license, test commit, and behavior supported.

## Change discipline

This document is non-normative research until an accepted decision updates the owning Blueprint chapter, relevant ADRs, requirements, risks, work packages, tests, and machine-readable records in the same change.
