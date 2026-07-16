# Turing Engineering Templates

Status: mandatory starting structures  
Owner: architecture, quality, security, and documentation governance

Use the smallest applicable structure and delete instructional text. Every accepted artifact includes stable ID, owner, status, requirements, risks, unsupported behavior, evidence, and related records.

## RFC / design note

Metadata; summary; user need; goals/non-goals; proposed architecture; identities/authority/lifecycle; alternatives; security/privacy; accessibility/product; compatibility/standards; performance/resources; operations/licensing; implementation/rollout/rollback; evidence; open questions/dissent; decision.

## ADR

ID/status/date; context; decision; prohibited alternatives; consequences; evidence; migration; revisit trigger; supersession chain.

## API or embedding proposal

Audience/stability/version; minimum safe workflow; operations/types/identity/authority; ownership/threading/cancellation/backpressure/errors; security responsibilities; compatibility/deprecation; language bindings; conformance; performance.

## Dependency proposal

Exact source/version; owner; need/alternatives; privilege/hostile input; unsafe/native/transitive/build scripts; license/patent/provenance; security history/fuzzing; platform/performance/build cost; Turing adapter; replacement; decision/review date.

## Threat model and security review

Scope; assets; actors; trust assumptions; processes/data flow; attack surfaces; threats/abuse; mitigations; residual risk; verification; findings/severity/owners/dates; release implications.

## Performance or benchmark plan

Question/hypothesis; correctness/security/accessibility guardrails; critical path; metrics/budgets; fixed environment; workloads; repetitions/statistics; failure denominator; raw artifacts; regression/rollback.

## Migration, experiment, risk acceptance, deprecation, postmortem, and release readiness

Each records exact versions/builds, owner, preconditions, method, failure/recovery, evidence, user impact, rollback, expiry, communication, and changes required in requirements/risks/ADRs.

## Plug-in proposal

User job; publisher; execution tier; manifest/capabilities/origins/data; lifecycle/resource budgets; UI/accessibility; threat model; signing/update/revocation; store; conformance/support.

<!-- MARKET-STRATEGY-2026-07 -->
## Product and market strategy

- [Market opportunity proposal](market-opportunity.md) — target segment, job, evidence, alternatives, risks, validation, promotion, expiry, and removal.
