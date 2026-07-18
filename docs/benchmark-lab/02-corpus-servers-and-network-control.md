# Corpus, Servers, and Network Control

Status: detailed research and design baseline  
Owner: performance measurement and benchmark operations  
Book index: [README](README.md)  
Canonical overview: [Blueprint owner](../blueprint-v1/09-performance-memory.md)

## Purpose

This chapter defines the research contract for **corpus, servers, and network control**. It is not an implementation or support claim. The design must remain compatible with the owning Blueprint, requirements, risks, security model, performance contract, accessibility obligations, and documentation policy.

## Scope

The study covers:

- generated/legal pages;
- applications;
- international/a11y content;
- hostile cases;
- local HTTP/2/3/TLS/DNS;
- cache state;
- latency/loss/bandwidth;
- authentication mocks;

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

1. Prototype and measure generated/legal pages under representative, adversarial, failure, cancellation, and pressure conditions.
2. Prototype and measure applications under representative, adversarial, failure, cancellation, and pressure conditions.
3. Prototype and measure international/a11y content under representative, adversarial, failure, cancellation, and pressure conditions.
4. Prototype and measure hostile cases under representative, adversarial, failure, cancellation, and pressure conditions.
5. Prototype and measure local HTTP/2/3/TLS/DNS under representative, adversarial, failure, cancellation, and pressure conditions.

Each experiment records commit, platform, hardware, build flags, corpus, security configuration, process topology, tab state, sample count, raw samples, statistical treatment, failures, unsupported cases, and confidence. A result that cannot be reproduced remains exploratory.

## Evidence gates

- specification and data-model review;
- unit, property/model, malformed-input, negative-capability, timeout, cancellation, recovery, and OOM tests;
- WPT, Test262, protocol, platform, accessibility, or other primary conformance evidence where applicable;
- structure-aware fuzzing and corpus minimization for parsers, protocols, state machines, and persisted formats;
- semantic trace or full-recomputation/reference oracle;
- fixed-hardware latency, memory, energy, and longevity baselines;
- corpus manifests validated by [`tools/validate_benchmark_corpus.py`](../../tools/validate_benchmark_corpus.py), with generated fixture hashes, local-only entry paths, no external network references, and explicit no-claim status;
- the current no-claim smoke corpus seed covers generated static-document, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract fixture shapes only, and still does not replace a reviewed representative corpus;
- network profiles validated by [`tools/validate_benchmark_network_profile.py`](../../tools/validate_benchmark_network_profile.py), with loopback-only serving, route-to-corpus coverage, DNS override policy, cache headers, disabled external network access, and explicit unsupported protocol/authentication/shaping cases;
- static-server self-tests validated by [`tools/serve_benchmark_profile.py --self-test`](../../tools/serve_benchmark_profile.py), with loopback HTTP/1.1 route checks, Host-header DNS behavior, no-store headers, fixture byte checks, and explicit no-claim output;
- runner-managed server lifecycle self-test packages generated by [`tools/run_benchmark_server_profile.py --self-test`](../../tools/run_benchmark_server_profile.py), with `server-startup`, route-check, `server-shutdown`, runner summary, artifact index, file hashes, shutdown proof, and explicit no-browser/no-benchmark status;
- smoke runner self-tests validated by [`tools/run_benchmark_smoke.py --self-test`](../../tools/run_benchmark_smoke.py), with a temporary artifact package, runner summary, benchmark hardware, OS-control, and resource-attribution registry IDs, profile self-test artifact, artifact index, file hashes, and explicit no-browser/no-benchmark status;
- browser-pin self-tests validated by [`tools/capture_benchmark_browser_pins.py --self-test`](../../tools/capture_benchmark_browser_pins.py), with runner-owned temporary profile cleanup, prohibited configured-path checks, artifact hashes, and explicit no-browser/no-benchmark status;
- no-claim Chrome/Edge browser-pin diagnostic summaries validated by [`tools/validate_benchmark_browser_pin_diagnostics.py`](../../tools/validate_benchmark_browser_pin_diagnostics.py), with isolated temporary profiles, browser-reported versions, cleanup status, and explicit no-benchmark/no-claim status;
- browser launch-runner contracts validated by [`tools/validate_benchmark_launch_runners.py`](../../tools/validate_benchmark_launch_runners.py), with required and forbidden arguments, stage coverage, timeout/cancellation policy, cache/profile policy, failure finalization, trace/artifact requirements, and explicit no-claim status;
- checked no-browser browser launch-runner self-test packages generated by [`tools/run_benchmark_browser_launch.py --self-test`](../../tools/run_benchmark_browser_launch.py), with command parsing, forbidden-argument rejection, registry-reference checks, artifact-root handling, no-claim finalization, and explicit no-browser/no-benchmark status;
- explicit residual risks, owner, revisit trigger, and unsupported matrix.

## Current No-Claim Launch Runner Contract

The checked [Benchmark browser launch-runner contract](../research/benchmark-browser-launch-runner-contract-2026-07.md), [no-claim browser launch-runner plan](../blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json), and checked no-browser browser launch-runner self-test define the current `PB13-EV-005` command and stage shape. This is not a browser-run launch implementation, not a browser run, not a benchmark result, and not a memory, energy, Chrome-class, or performance result.

The contract and self-test exist so future runner work cannot skip command parsing, forbidden-argument rejection, checked registry references, artifact-root handling, timeout, cancellation, cache/profile, failure-denominator, artifact, trace, cleanup, or no-claim finalization rules. A real runner still needs a browser-run implementation, reviewed browser pins, runner-managed server artifact, browser-run artifact package, negative tests, and owner-reviewed interpretation.

## Risks

Primary risks are semantic divergence, confused-deputy behavior, stale identity, unbounded work, memory retention, cross-profile or cross-origin leakage, native or platform compromise, hidden performance cliffs, inaccessible failure UI, unreliable recovery, and documentation becoming more certain than the evidence.

## Primary sources

- https://browserbench.org/
- https://browserbench.org/Speedometer3.1/
- https://browserbench.org/MotionMark/
- https://perfetto.dev/
- https://learn.microsoft.com/en-us/windows-hardware/test/wpt/

Source URLs are starting points. An implementation records the exact revision, retrieval date, local patches, license, test commit, and behavior supported.

## Change discipline

This document is non-normative research until an accepted decision updates the owning Blueprint chapter, relevant ADRs, requirements, risks, work packages, tests, and machine-readable records in the same change.
