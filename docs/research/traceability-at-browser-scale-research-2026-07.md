# Traceability at Browser Scale Research - July 2026

Status: active `RQ-47` source-backed traceability and evidence-control route; no coverage, implementation, verification, security, performance, compatibility, accessibility, release, or production claim
Owner: quality, architecture, documentation, security, release operations, and subsystem owners
Research date: 2026-07-19
Related questions: `RQ-44`, `RQ-46`, `RQ-47`, `RQ-48`, `RQ-60`
Related gates: `PB-002`, `PB-008`, `PB-009`, `PB-019`, `PB-020`

## Question

Can requirement-to-evidence records remain accurate, bidirectional, reviewable, and useful as Turing grows from a documented prototype into a multi-process browser with standards, platform, security, accessibility, performance, release, and support obligations?

This packet defines the traceability model and falsifiable controls. It does not claim that the current registries prove implementation, coverage, readiness, or support.

## Source-backed observations

### Traceability is a relationship, not a spreadsheet view

NASA systems-engineering guidance defines traceability as a discernible association between logical entities and bidirectional traceability as the ability to follow an item to its parent and allocated children. It emphasizes that requirements should preserve rationale, assumptions, relationships, constraints, and verification conditions, and that traceability supports impact analysis when a requirement changes.

For Turing, the durable unit is a typed edge between stable records, not a copied table row. A generated view may be convenient, but it cannot become a second source of truth.

### Verification needs alignment and change impact

NASA software-engineering guidance describes a traceability matrix that links requirements through design, implementation, tests, and verification, identifies orphaned or missing links, and records change impact. It also treats test plans, procedures, data, configuration, and non-conformances as managed products rather than informal context.

For Turing, a green validator can prove graph shape or schema validity but cannot prove that the linked test exercises the intended behavior, that the evidence is independent, or that the result still applies after a source, dependency, platform, workload, or support-scope change.

### Security practice requires lifecycle evidence

NIST SP 800-218 SSDF provides a lifecycle vocabulary for preparing organizations, protecting software, producing well-secured software, and responding to vulnerabilities. Traceability must therefore include security findings, dependency/provenance records, reviews, release artifacts, and response evidence rather than stopping at source and unit tests.

These observations are methods and criteria. They do not establish that Turing currently satisfies them.

## Canonical graph model

The graph must preserve stable IDs and typed edges for at least:

- user need, product opportunity, stakeholder expectation, and support statement;
- `REQ-*` requirement, `R-*` risk, `ADR-*` decision, `RQ-*` research question, and `OP-*` opportunity;
- Blueprint chapter, detailed engineering book, design contract, interface, schema, and work package;
- `TASK-*` manifest, source commit, generated output, dependency/source revision, and build identity;
- test, corpus, fuzzer, benchmark, accessibility workflow, negative case, failure/recovery case, and raw artifact;
- evidence bundle, independent review, exception, owner, backup, phase gate, release artifact, and supported/unsupported statement.

Every edge needs a source record, destination record, edge type, creation or update date, authoring authority, status, and limitation. Evidence edges additionally need exact commit/build/environment/configuration/workload, artifact identity or hash, result, reviewer, freshness/expiry, and access policy where evidence is embargoed.

## Required edge types

Use explicit edge types rather than inferring meaning from filenames or prose:

| Edge | Required meaning | Negative case |
|---|---|---|
| `derives_from` | requirement or design was derived from an identified parent/expectation | unparented gold-plating is hidden as a requirement |
| `constrains` | a decision, risk, platform, or policy limits an implementation choice | a design constraint is mistaken for a selected implementation |
| `allocated_to` | requirement or risk is assigned to a component, process, or work package | allocation is missing or spans an unowned boundary |
| `implemented_by` | an exact source revision claims to implement a bounded requirement | a merged commit is treated as implementation without scope |
| `verified_by` | a named test, inspection, analysis, or review checks a requirement | a planned test or passing unrelated test is used as proof |
| `evidenced_by` | retained artifact supports a bounded result under stated conditions | a log without environment, hash, or denominator is treated as evidence |
| `depends_on` | a gate, task, or claim has a predecessor | a downstream claim bypasses an unresolved predecessor |
| `invalidated_by` | a change or expiry makes prior evidence inapplicable | stale evidence silently remains current |
| `supports` | a result supports a specific claim boundary | a local observation is generalized to a product claim |
| `rejects` or `defers` | an option or claim was explicitly rejected or held with rationale | absence is mistaken for rejection or acceptance |

## Status and freshness model

Keep these states separate:

1. specified: a requirement, risk, design, or research question is recorded;
2. planned: an owner, lane, test/evidence shape, and next proof are recorded;
3. implemented: source exists at an exact revision within the declared scope;
4. verified: the required evidence and independent review exist and remain applicable;
5. release-gated: the relevant gate accepted the evidence and boundaries;
6. supported: the product scope, platform, update, incident, accessibility, and maintenance obligations are accepted.

Evidence becomes stale when code, dependencies, toolchain, platform, configuration, process topology, workload, test corpus, security assumptions, support scope, or measurement method changes. Staleness must invalidate or re-open dependent edges; it must not be repaired by changing a label alone.

## Control and scaling strategy

Keep canonical records small and generate views for humans. At minimum, validators should detect:

- duplicate or missing stable IDs;
- dangling edges and references to moved or deleted records;
- requirements without owners, verification plans, or support boundaries;
- risks, decisions, tasks, and evidence with no affected requirement or gate;
- orphan source, test, benchmark, accessibility, security, or release artifacts;
- one-way edges where bidirectional traceability is required;
- status contradictions between prose, machine registries, task manifests, and release records;
- evidence with missing commit, build, environment, configuration, workload, result, reviewer, hash, freshness, or limitation;
- stale evidence whose invalidation trigger has fired;
- claims whose scope exceeds the linked evidence or whose predecessor gate is unresolved;
- inaccessible embargoed records that have no controlled existence, owner, review, or debt marker.

Generated indexes must identify their source registry and regeneration command. Manual edits to generated output must fail validation or be overwritten from the declared source of truth.

## Browser-scale impact analysis

For every change, traverse outward from the changed record through requirements, risks, decisions, interfaces, source, tests, evidence, owners, release, and support edges. The impact report must distinguish:

- affected records that require review;
- evidence that remains valid;
- evidence that is stale or partially applicable;
- unsupported behavior newly exposed;
- required negative, timeout, cancellation, recovery, privacy, security, accessibility, performance, and operational cases;
- owner and independent-review changes;
- claims that must be withdrawn, narrowed, or time-expired.

Cross-process and cross-origin edges must preserve principal, profile, site, frame, document, process, and epoch identity. Benchmark edges must preserve hardware, OS controls, browser pins, corpus, process topology, lifecycle, statistical method, and denominator. Security evidence must preserve restricted access without hiding the existence of unresolved work.

## Measurement and adversarial validation

Measure graph size, edge-validation time, generated-view latency, change-impact traversal, stale-evidence detection, orphan detection, review queue age, and false-positive/false-negative rates on synthetic and repository-scale fixtures. Exercise malformed IDs, duplicate IDs, cycles, dangling references, stale commits, mismatched build IDs, changed workloads, expired exceptions, deleted artifacts, unauthorized evidence access, redacted evidence, and concurrent updates.

Use spot checks and independent review to verify that a link means what its edge type says. A graph that is complete but semantically wrong is a failed control.

## Rejection and promotion rules

Reject a readiness or support claim when traceability is one-way where bidirectional proof is required, when an edge relies on inferred filenames or prose, when evidence lacks identity and conditions, when stale evidence remains active, when an owner or reviewer is missing, or when a claim exceeds the linked scope.

Promote only when the canonical source records, generated views, validators, review records, evidence bundles, exception expiry, and claim boundaries agree. Research presence and graph completeness do not authorize tasks, source adoption, implementation, release, or production support.

## Current status and claim boundary

`RQ-47` is active in the readiness crosswalk. This packet closes a research-route and control-definition gap only. It does not prove that all records are complete, that any requirement is implemented or verified, that any gate is ready, or that Turing has Chrome-class compatibility, performance, security, accessibility, release, or production status. The current `90%` contained-M0 / `0%` full-build closure metrics remain unchanged.

## Next question

Which first executable traceability audit should independently sample the source-strategy, fresh-host, and ownership lanes, and what findings must block a task or claim rather than merely create a warning?

## Sources

- [NASA Systems Engineering Handbook: system design processes](https://www.nasa.gov/reference/4-0-system-design-processes/)
- [NASA Systems Engineering Handbook: crosscutting technical management](https://www.nasa.gov/reference/6-0-crosscutting-technical-management/)
- [NASA Software Engineering Handbook: bidirectional traceability](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604521/SWE-059%2BBidirectional%2BTraceability%2BBetween%2BSoftware%2BRequirements%2Band%2BSoftware%2BDesign)
- [NASA Software Engineering Handbook: traceability matrices](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695453/SWE-071%2BUpdate%2BTest%2BPlans%2Band%2BProcedures)
- [NIST SP 800-218: Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
