# Observability, Tracing, and Replay

Status: research and design baseline  
Owner: observability architecture  
Purpose: Make browser behavior explainable with stable events, semantic attribution, safe artifacts, and controlled replay.

## Relationship to the Turing program

This document supports REQ-DEV-001 and performance attribution requirements in [Blueprint 09](../blueprint-v1/09-performance-memory.md).

## Unified event model

Engine and browser services emit versioned events with monotonic time, process/thread/task identity, principal, profile/site/frame/document epoch, category, phase, causal flow, resource owner, and bounded attributes. Stable event names remain consistent between debug and sampled production configurations.

Event production must not block critical threads or allocate without bound. Buffers have quotas, priority, sampling, loss markers, and backpressure policy.

## Causality

Navigation, resource fetch, parser blocking, script tasks, style invalidation, layout roots, paint damage, raster work, frame presentation, input, GC, JIT, storage transactions, process launch, sandbox decisions, permission prompts, and agent actions carry links that allow a developer to follow cause to effect.

Clock synchronization between processes reports uncertainty and does not fabricate total order where none is known.

## Semantic resource attribution

CPU time, queue wait, allocations, resident/charged memory, GPU resources, network bytes, disk I/O, wakeups, energy estimates, model tokens, and provider cost are attributed to documents, frames, workers, extensions, DevTools, agents, browser UI, or shared services. Shared totals show both physical and charged views.

Attribution gaps are represented explicitly rather than silently assigned to the foreground tab.

## Trace file format

Trace artifacts have a versioned manifest, engine/build identity, platform, clock metadata, enabled categories, privacy classification, redaction record, dropped-event counts, compression, chunks, checksums, and indexes. Readers treat traces as untrusted data and never execute embedded scripts.

Schema evolution supports unknown events and fields without corrupting known data. Sensitive payload capture requires explicit local authorization and preview.

## Deterministic recording

Isolated test profiles can record network fixtures, virtual time, random seeds, input, navigation, permission decisions, storage snapshots, process failures, and selected engine events. Reproduction identifies nondeterministic sources and records what was not controlled.

Replay is not promised for arbitrary live sessions. Deterministic actions and local fixtures can be replayed in fresh isolated profiles, never silently against a signed-in profile.

## Diffing and regression analysis

Tools compare traces by semantic phase, causal path, resource owner, task distribution, invalidation, memory category, frame deadline, and policy outcome. Baselines include noise ranges and environment metadata. A regression report links raw samples, trace hashes, affected commits, and suspected owners.

Pixel or aggregate metric differences are supplemented by parser, fragment, paint, accessibility, network, and runtime traces.

## Privacy and retention

Default traces exclude passwords, cookies, authorization, form values, full page text, screenshots, private URL query data, local paths, raw model prompts/completions, and credential material. Export previews list included fields. Retention is local and user-controlled unless an explicit upload workflow is approved.

## Non-negotiable invariants

- Trace events are versioned, bounded, causal where possible, and safe to parse.
- Critical browser threads do not block on trace consumers.
- Loss, sampling, clock uncertainty, and attribution gaps are visible.
- Replay occurs only in isolated profiles with explicit scope.
- Sensitive data is redacted at source by default.
- A trace reader never executes page or embedded content.

## Required evidence

- Schema compatibility and corrupted-trace fuzzing.
- Trace overhead and dropped-event measurements under representative workloads.
- Cross-process clock and causal-flow validation.
- Reproduction studies for selected engine, network, storage, and crash defects.
- Privacy field inventory, export preview, and secret-scanning tests.
- Regression diff accuracy and developer workflow studies.

## Known risks and unresolved questions

- Instrumentation can change scheduling and cache behavior.
- Overly broad traces can leak user data or source code.
- Replay claims can be misleading when external services or nondeterminism remain.
- High-cardinality events can create substantial memory and disk pressure.

## Primary sources

- WHATWG Streams — https://streams.spec.whatwg.org/
- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/
- Firefox Remote Protocol — https://firefox-source-docs.mozilla.org/remote/index.html

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
