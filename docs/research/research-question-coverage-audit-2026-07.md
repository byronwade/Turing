# Research-Question Coverage Audit - July 2026

Status: checked no-claim program coverage audit

## Result

The numbered research program contains 66 questions. The active readiness crosswalk currently routes 37 questions into pre-build closure lanes. The remaining 29 questions are now explicitly recorded as deferred outside the current pre-build crosswalk in the [coverage registry](../blueprint-v1/machine/research-question-coverage.json), with an owner route, revisit trigger, and future evidence requirements for each.

This distinction is intentional. Active crosswalk membership means a question is relevant to a current readiness lane; it does not mean the question is answered or that its gate is ready. Deferred status means the question remains in the canonical research program and must be mapped before it becomes a milestone, implementation task, requirement, or support claim.

## Control

The [coverage schema](../blueprint-v1/machine/research-question-coverage.schema.json) and [validator](../../tools/validate_research_question_coverage.py) derive the 66-question denominator from `docs/blueprint-v1/22-research-program.md` and require the active set to match `research-readiness-crosswalk.json` exactly. They reject missing, duplicate, or silently omitted questions.

## Claim boundary

This audit does not answer a research question, establish compatibility, security, accessibility, performance, production, or Chrome-class evidence, approve a task, promote a readiness gate, or replace owner review. The 37 active questions and 29 deferred questions all remain research work until their required evidence and decisions exist.
