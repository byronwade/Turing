# Benchmark Claim-Bundle Examples - July 2026

Status: fictitious no-claim public-claim handoff example
Owner: performance, measurement, statistics, and documentation research
Related gate: `PB-013`
Related task: `TASK-000005`
Scope: claim-bundle shape only; no browser run, benchmark result, competitor result, or public performance claim

## Purpose

This page gives a maintainer one end-to-end example of how measured benchmark evidence would be converted into a narrowly scoped claim bundle. Every value is fictitious and intentionally incomplete. It complements the [Benchmark Evidence and Claim Closure Preparation](benchmark-evidence-and-claim-closure-preparation-2026-07.md), [Benchmark Competitor Runbook Examples](benchmark-competitor-runbook-examples-2026-07.md), checked [public-claim bundle template](../blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json), and [Chrome-class performance readiness lane](../benchmark-lab/chrome-class-performance-readiness-lane.md).

## Bundle identity

| Field | Fictitious example | Required rule |
|---|---|---|
| claim_bundle_id | `PB013-CLAIM-EXAMPLE-2026-07-19-A` | Stable id bound to one immutable evidence set |
| claim_status | `example_only_no_public_claim` | Never treat as an approved claim |
| claim_level | `L3_public_claim_candidate` | L3 requires reviewed L2 comparison evidence first |
| source_build_id | `EXAMPLE-BUILD-DO-NOT-USE` | Pin exact source commit and artifact hash |
| analysis_plan_id | `EXAMPLE-STATISTICS-PLAN` | Must match the executed, owner-reviewed statistics plan |
| hardware_scope | `EXAMPLE-TIER-M` | Exact hardware, OS, driver, firmware, power, and thermal scope |
| owner | `unassigned-example-owner` | Real bundle requires an accountable owner |
| independent_reviewer | `unassigned-example-reviewer` | Must be independent and named after the latest artifact change |
| expires_at | `2099-01-01` | Example only; real claims expire on declared triggers |

## Proposed claim record

The exact sentence must be narrower than the evidence and must state what it does not cover.

```text
claim_text: "Example Turing build completed the declared local startup workload
within the measured interval on the named reference image."
claim_scope:
  product: Turing research build
  metric_family: startup
  hardware: EXAMPLE-TIER-M
  operating_system: EXAMPLE-CLEAN-IMAGE
  workload: EXAMPLE-CORPUS-REVISION
  competitors: none
  date_window: EXAMPLE-DATE-WINDOW
claim_type: diagnostic_only
unsupported:
  - no faster-than-Chrome claim
  - no lower-memory or lower-energy claim
  - no compatibility, security, accessibility, production, or daily-driver claim
  - no cross-hardware or cross-OS generalization
```

This sample sentence is not approved, measured, or publishable. A real claim must be generated from retained evidence and pass owner and independent review.

## Evidence binding

Every input is bound by id, source commit, artifact hash, capture time, and review status.

| Input | Fictitious reference | Required review question |
|---|---|---|
| hardware and OS controls | `EXAMPLE-HARDWARE-MANIFEST`, `EXAMPLE-OS-CONTROL` | Was the image clean, current, and within the approved hardware scope? |
| browser pins | `EXAMPLE-TURING-PIN`, `EXAMPLE-COMPETITOR-PINS` | Do executable hashes, versions, channels, settings, and profiles match what ran? |
| corpus and route map | `EXAMPLE-CORPUS-HASH`, `EXAMPLE-ROUTES-HASH` | Is the workload representative, identical where compared, and complete? |
| runner and server | `EXAMPLE-RUNNER-COMMIT`, `EXAMPLE-SERVER-LIFECYCLE` | Did the reviewed runner launch the intended target and cleanly close the server? |
| raw samples | `EXAMPLE-RAW-SAMPLES` | Are all measured samples retained with order, warmup, and failure state? |
| traces and resources | `EXAMPLE-TRACE-PACKAGE`, `EXAMPLE-RESOURCE-PACKAGE` | Can resource attribution and process/tab lifecycle be independently checked? |
| statistics analysis | `EXAMPLE-ANALYSIS-RESULT` | Does the executed analysis match the approved plan and uncertainty rules? |
| denominator report | `EXAMPLE-DENOMINATOR` | Are failures, unsupported cases, timeouts, crashes, discards, revivals, and cleanup failures visible? |
| redaction and retention | `EXAMPLE-REDACTION-REVIEW` | Are profiles, credentials, accounts, secrets, and personal data absent or redacted? |

No input may be replaced by a release-catalog observation, screenshot, self-test, parser result, or mutable path when the claim requires runner-generated evidence.

## Metric and denominator record

The bundle must preserve per-scenario and per-sample facts rather than only a headline:

| Field | Fictitious example | Required rule |
|---|---|---|
| scenario_count | `12` | Exact scenario manifest and hash required |
| attempted_runs | `36` | Includes setup, retries, and invalid targets where applicable |
| measured_runs | `30` | Must reconcile to the raw artifact index |
| warmup_runs | `6` | State policy before execution |
| failed_runs | `2` | Preserve failure class and raw evidence |
| unsupported_runs | `1` | Never convert to zero or silently omit |
| timeout_or_cancelled | `1` | Preserve timeout/cancellation and cleanup result |
| excluded_samples | `0` | Any exclusion requires predeclared rule and retained sample |
| statistic | `not_collected` | No real statistic exists in this example |
| uncertainty | `not_collected` | No claim may use a point estimate alone |
| effect_size | `not_collected` | Required for comparison interpretation |

The numbers above are placeholders, not a result. The real denominator must be mechanically derived from runner output and reconciled against raw artifacts, traces, failures, and cleanup events.

## Equivalence and safety review

Before a competitor or public claim is considered, the review records:

- exact suite, corpus, route, viewport, DPR, refresh rate, action script, repetitions, warmup, and cache policy;
- executable, version, channel, command line, temporary profile, extensions, account/sync state, feature flags, JIT, sandbox, site-isolation, and lifecycle settings;
- OS image, driver, firmware, power mode, thermal state, network profile, process model, tab-discard policy, and instrumentation overhead;
- accessibility, DevTools, extension, profile, storage, recovery, and agent overhead when the claim touches those workflows;
- unsupported pages/APIs, crashes, timeouts, wrong-target launches, trace failures, cleanup failures, state loss, and profile-isolation failures;
- artifact redaction, retention, reviewer identities, expiry, rerun triggers, and public-copy diff.

Any unmatched control narrows or invalidates the proposed claim. It cannot be hidden in an aggregate.

## Publication and expiration record

```text
publication_status: blocked_example_only
approved_claim_text: null
public_copy_diff: null
owner_approval: null
independent_review: null
benchmark_readiness_review: null
expiry_rule:
  - competitor update
  - source build change
  - suite, corpus, route, or action-script change
  - hardware, OS, driver, firmware, power, thermal, network, sandbox,
    lifecycle, profile, or browser-setting change
  - discovered denominator, security, redaction, or artifact error
rerun_triggers: recorded_before_publication
removal_action: remove expired or invalid text from README, release notes,
  website, dashboards, market material, and comparison reports
```

## Rejection rules

- Reject a bundle without runner-generated browser samples, traces, artifact hashes, and an exact source/build identity.
- Reject a bundle without the referenced statistics-analysis plan, sample count, warmup policy, uncertainty, effect size, outlier policy, and denominator report.
- Reject a comparison with mismatched workload, browser pin, profile, cache, security, sandbox, site-isolation, lifecycle, hardware, OS, driver, power, or instrumentation controls.
- Reject a bundle that removes failed, unsupported, timed-out, canceled, crashed, discarded, revived, state-loss, wrong-target, trace, cleanup, or profile-isolation cases from the denominator.
- Reject a bundle containing real profiles, accounts, sync state, credentials, secrets, or unreviewed personal data.
- Reject public text broader than the exact reviewed hardware, OS, workload, metric, date, browser version, and supported behavior.
- Reject expired claims or claims whose rerun trigger has fired.
- Keep `PB-013` partial and `TASK-000005` proposed-only while the bundle is an example, template, or unreviewed diagnostic.

## Claim boundary

This example proves only that a benchmark claim can be organized as a bounded, hash-linked review package. It does not provide a benchmark result, competitor comparison, speed, memory, energy, compatibility, security, accessibility, production, Chrome-class, extreme-performance, or daily-driver claim.

## Next proof

Execute the reviewed L1 browser-run pipeline, retain raw artifacts and failure denominators, execute the approved statistics plan, complete L2 comparison only after L1 review, and replace this example with an owner- and independently reviewed claim bundle whose wording matches the evidence exactly.
