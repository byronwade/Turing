# Requirement Verification Matrix

Status: planned verification documentation; no implementation or evidence claim
Owner: quality, architecture, and documentation owners
Last researched: 2026-07-19

## Purpose

The [professional traceability registry](../blueprint-v1/machine/professional-traceability.json) now routes all 46 accepted requirements to canonical design sources. This matrix adds the missing verification layer: every requirement belongs to a bounded domain lane with an owning work package, evidence classes, test layers, negative and failure cases, required artifacts, and a next-proof condition.

The machine-readable source is [`requirement-verification-matrix.json`](../blueprint-v1/machine/requirement-verification-matrix.json). The registry is authoritative for lane membership and planned verification shape; this document explains how to use it and preserves the claim boundary.

## Status and claim boundary

- All 46 accepted requirements are mapped exactly once across 11 verification lanes.
- The matrix is a plan for future implementation evidence, not evidence that implementation exists.
- `professional-traceability.json` remains authoritative for actual source, test, review, and evidence records. Its empty fields must remain empty until those records exist.
- A planned test layer is not a passing test. A required artifact is not a retained artifact. A source document is not independent verification.
- The two current reference-test records (`REQ-SEC-003` and `REQ-PERF-004`) remain unverified and do not satisfy production, security, performance, or release gates.

## Required verification shape

Every lane must define:

1. accepted requirement IDs with no duplicates or omissions;
2. work-package ownership that matches the backlog;
3. existing design and engineering source documents;
4. evidence classes from the implementation evidence catalog;
5. positive test layers appropriate to the domain;
6. negative, timeout, cancellation, recovery, resource-exhaustion, privacy, security, and accessibility cases where applicable;
7. retained artifacts that identify the version, environment, configuration, workload, denominator, result, reviewer, and limitations;
8. a next-proof condition that does not silently authorize implementation or release.

## Evidence lifecycle

The intended lifecycle is:

`accepted requirement -> planned lane -> approved task -> source change -> tests -> evidence bundle -> independent review -> gate decision -> supported statement`

Missing links remain visible. A passing unit test cannot replace conformance, hostile-input, privacy, accessibility, performance, recovery, operational, or independent-review evidence when the lane requires those classes. Evidence expires when code, dependencies, platform assumptions, workloads, or support scope change.

## Domain lanes

The machine registry contains the complete per-lane fields. The lanes are:

- Accessibility and internationalization (`A11Y`)
- Agent authority, observation, and audit (`AI`)
- DevTools, headless, and automation (`DEV`)
- HTML, DOM, CSS, layout, and rendering (`ENG`)
- JavaScript, WebAssembly, garbage collection, and JIT (`JS`)
- Networking and request policy (`NET`)
- Build provenance and operations (`OPS`)
- Performance, memory, energy, and resource attribution (`PERF`)
- Browser product surfaces and lifecycle (`PROD`)
- Sandboxing, site isolation, IPC, updates, and response (`SEC`)
- Storage, quota, migrations, and recovery (`STO`)

## Handoff rule

Before an implementation task is approved, its manifest must select the relevant lane, name the requirement IDs, preserve the listed negative and failure cases, identify the evidence bundle location, and state which planned fields are still unproven. The task may narrow scope, but it may not remove required evidence classes without a reviewed exception and updated risk/requirements records.

## Current next proof

The next proof is not a broad build. It is owner-reviewed selection of the first executable verification lane after the unresolved source-strategy, fresh-host, IPC, sandbox, native-shell, profile/session, package/update, incident-response, backup-ownership, and readiness gates are addressed. Until then, the project remains at **90% contained-M0 documentation organization and 0% full-build closure**.
