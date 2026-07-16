# Asynchrony, Streaming, and Cancellation

Status: research and design baseline  
Owner: API concurrency and flow control  
Purpose: Define non-blocking operations that remain bounded, cancellable, and correct under partial failure.

## Relationship to the Turing program

These rules apply to DevTools, automation, IPC, network/storage brokers, agent providers, and generated SDKs. Browser scheduling is detailed in the [performance book](../performance/README.md).

## Asynchronous operation model

Operations that may wait on network, storage, process launch, user confirmation, page lifecycle, model providers, compilation, tracing, or large serialization return an operation identity and explicit state. The caller can observe progress, completion, cancellation, timeout, or policy denial without occupying a critical thread.

Completion is delivered exactly once at the protocol level even when underlying work has multiple attempts or partial phases.

## Cancellation

Cancellation is a request with defined guarantees: not started, stopped before effect, stopped after a documented partial effect, or too late because an atomic commit completed. Handlers poll or receive cancellation at bounded safe points. Cancellation propagates through dependent network, storage, compiler, page, provider, and stream work.

Cancellation never leaves a transaction, permission prompt, navigation, transfer, or file in an undefined state. Cleanup and revocation are part of the contract.

## Deadlines and timeouts

Calls carry absolute or relative deadlines using monotonic time. Queue wait and execution time are reported separately. Server defaults exist for callers that omit limits. Timeouts return stable state and do not imply that all underlying effects were rolled back unless the contract guarantees it.

Retries use remaining deadlines, idempotency keys, and backoff. The server does not retry consequential mutations silently.

## Streaming

Large bodies, traces, screenshots, heap snapshots, files, semantic observations, and query results use chunked streams. Streams negotiate chunk and window limits, preserve ordering guarantees, identify total size when known, provide integrity/checksum metadata where valuable, and support early termination.

A producer cannot outrun the consumer indefinitely. Flow-control windows, bounded buffers, spill policy, and cancellation prevent one client from consuming unbounded process memory.

## Backpressure and overload

Backpressure is explicit between page tasks, IPC, protocol clients, trace pipelines, network, storage, GPU, and agent providers. Overload policy may reject, coalesce, sample, lower priority, pause, or cancel work according to semantic class. Loss is never hidden.

Control messages and cancellation have reserved capacity so a full data queue cannot prevent shutdown.

## Idempotency and transactions

Mutations declare whether they are idempotent, conditionally idempotent, or non-idempotent. An idempotency key is scoped to principal, method, target, time window, and payload hash. Atomic operations use commit points; multi-resource workflows expose compensation or partial results rather than pretending distributed rollback.

Navigation, storage migrations, downloads, uploads, and agent actions state preconditions and expected postconditions.

## Event subscriptions

Subscribers choose domains, targets, filters, detail levels, and queue budgets. Events include sequence and epoch information. Slow subscribers receive backpressure, sampling, coalescing, or disconnect according to domain policy, with explicit gap events.

Subscriptions end on target destruction, session revocation, permission loss, or version incompatibility.

## Non-negotiable invariants

- Every potentially long operation has a deadline and cancellation path.
- Cancellation and timeout outcomes state whether effects occurred.
- Streams are flow-controlled and bounded end to end.
- Control and cancellation cannot be starved by full data queues.
- Consequential mutations are not silently retried.
- Event loss, coalescing, and sequence gaps are visible.

## Required evidence

- Race and model tests across start, cancellation, timeout, commit, disconnect, and retry.
- Backpressure and slow-consumer tests at every process/protocol boundary.
- Memory and latency measurements for large streams and event storms.
- Fault injection for network loss, process crash, disk full, provider timeout, and target navigation.
- Idempotency and duplicate-delivery tests.
- Structured partial-failure and compensation examples in generated clients.

## Known risks and unresolved questions

- Ambiguous cancellation can cause duplicate or unintended effects.
- Backpressure can create priority inversion or deadlock.
- Streaming protocols can retain large chunks or sensitive data.
- Retry behavior can violate user intent when operations are not idempotent.

## Primary sources

- WHATWG Streams — https://streams.spec.whatwg.org/
- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- Model Context Protocol specification — https://modelcontextprotocol.io/specification/2025-11-25

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
