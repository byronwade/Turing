# Research-Question Coverage Audit - July 2026

Status: checked no-claim program coverage audit
Owner: research and documentation governance

## Result

The numbered research program contains 66 questions. The active readiness crosswalk currently routes 37 questions into pre-build closure lanes. The remaining 29 questions are now explicitly recorded as deferred outside the current pre-build crosswalk in the [coverage registry](../blueprint-v1/machine/research-question-coverage.json), with an owner route, revisit trigger, and future evidence requirements for each.

This distinction is intentional. Active crosswalk membership means a question is relevant to a current readiness lane; it does not mean the question is answered or that its gate is ready. Deferred status means the question remains in the canonical research program and must be mapped before it becomes a milestone, implementation task, requirement, or support claim.

## Semantic alignment control

The machine registry is not allowed to treat a structurally valid `RQ-*` identifier as sufficient routing evidence. Each deferred row must be checked against the exact question title in [Blueprint 22](../blueprint-v1/22-research-program.md), and its owner route, revisit trigger, and required future evidence must address that question rather than a neighboring research domain. This control caught shifted routes for `RQ-24`, `RQ-26`, `RQ-28`, `RQ-32`, `RQ-41`, `RQ-42`, `RQ-43`, `RQ-51`, `RQ-52`, `RQ-58`, `RQ-59`, `RQ-61`, `RQ-62`, and `RQ-65`; those rows are now aligned to their canonical titles. `RQ-39` was separately aligned to deterministic replay and causal observability.

This is a routing correction, not an answer to any research question. The coverage validator now carries a narrow semantic-term guard for the corrected rows so a future unrelated route fails validation instead of passing on identifier shape alone. Deferred status, evidence requirements, owner review, and all readiness and claim boundaries remain unchanged.

## Control

The [coverage schema](../blueprint-v1/machine/research-question-coverage.schema.json) and [validator](../../tools/validate_research_question_coverage.py) derive the 66-question denominator from `docs/blueprint-v1/22-research-program.md` and require the active set to match `research-readiness-crosswalk.json` exactly. They reject missing, duplicate, or silently omitted questions.

The validator also requires every active question to have at least one `docs/research/` evidence route, resolves every `evidence_start` entry in the readiness crosswalk inside the repository, checks each lane's requirements, risks, and work packages against its proposed task binding, and checks the matching count in the [build-readiness progress snapshot](../project-buildout/22-build-readiness-progress-snapshot.md). The current crosswalk routes all 37 active questions to research evidence; it has 10 lanes and 260 evidence-start entries, all of which resolve to an existing file or directory. This catches missing research coverage, stale route references, task-to-requirement/risk/work-package drift, and stale maintainer-facing counts during documentation changes while preserving no-claim status. It does not verify that the referenced evidence is sufficient, independently reviewed, or accepted for implementation.

## Claim boundary

This audit does not answer a research question, establish compatibility, security, accessibility, performance, production, or Chrome-class evidence, approve a task, promote a readiness gate, or replace owner review. The 37 active questions and 29 deferred questions all remain research work until their required evidence and decisions exist.
