# Task Decomposition and Execution Graph

Status: operating baseline  
Owner: program, architecture, quality, and subsystem owners

“Build the browser” is not an executable task. Work decomposes as:

```text
program objective
  -> milestone
    -> capability
      -> component
        -> design task
        -> implementation task
        -> conformance task
        -> security task
        -> performance task
        -> accessibility task
        -> release task
```

Every agent task has a stable ID, owner, independent reviewer, allowed paths, prohibited paths, requirements, risks, ADRs, preconditions, acceptance criteria, negative tests, resource budget, evidence outputs, dependencies, rollback, and expiry.

A task cannot enter `ready` state while its acceptance criteria are vague, its authority is broader than necessary, its dependencies are unresolved, or its rollback is missing.

## Task states

`proposed -> specified -> reviewed -> ready -> running -> evidence_pending -> review_pending -> accepted | rejected | rolled_back | superseded`

Only reviewed tasks may run against production source. A blocked task remains blocked; an agent cannot reinterpret the blocker as optional.
