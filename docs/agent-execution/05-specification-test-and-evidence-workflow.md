# Specification, Test, and Evidence Workflow

Status: operating baseline  
Owner: quality, standards, security, performance, and accessibility

An agent implementation begins from an approved requirement and design, not from a demo prompt.

## Required sequence

1. Resolve normative specification and supported subset.
2. Define positive, negative, malformed, timeout, cancellation, resource-exhaustion, crash, and recovery behavior.
3. Establish an independent oracle where possible.
4. Implement the smallest bounded change.
5. Add conformance and regression tests.
6. Run security, performance, accessibility, compatibility, and recovery evidence appropriate to the task.
7. Produce a signed or hashed evidence bundle.
8. Obtain independent review.

Tests written by the implementation agent are necessary but not sufficient. WPT, Test262, model/property tests, differential oracles, fuzzers, platform accessibility review, and fixed-hardware measurement provide separate evidence lanes.

A failing test cannot be deleted, skipped, weakened, or reclassified by the same change merely to achieve green CI.
