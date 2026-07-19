# ADR-0009 Source-Strategy Packet Examples - July 2026

Status: fictitious no-claim handoff example
Owner: architecture, provenance, legal-community, and documentation research
Related gate: `PB-002` and `ADR-0009`
Scope: review-packet shape only; no source selection, source import, component approval, or release-code authorization

## Purpose

This page gives a maintainer one complete example of the information that must travel together when an `ADR-0009` option is reviewed. The values below are deliberately fictitious and must not be copied into the real decision record. The example complements the [ADR-0009 source-strategy closure preparation](adr-0009-source-strategy-closure-preparation-2026-07.md), [decision packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md), [evidence traceability matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md), and checked no-claim decision-review template.

## Packet identity

| Field | Fictitious example | Required rule |
|---|---|---|
| packet_id | `ADR9-PACKET-EXAMPLE-2026-07-19-A` | Stable identifier; never reuse after scope changes |
| decision_id | `ADR-0009` | Must match the machine registry and decision draft |
| readiness_gate | `PB-002` | Must match the pre-build readiness record |
| packet_status | `example_only` | Must not be interpreted as observed, reviewed, decided, or authorized |
| source_commit | `0000000000000000000000000000000000000000` | Placeholder is invalid in a real packet |
| source_archive | `example-source.tar.gz` | Record URL or controlled source path, hash, size, and retrieval time |
| feature_profile | `example-minimal-dev` | Name every feature, target, native package, and generated-output family |
| target_profile | `windows-x86_64-reference` | Record OS build, compiler, linker, SDK, CPU, and relevant policy |
| owner | `unassigned-example-owner` | Real packet requires a named accountable owner |
| independent_reviewer | `unassigned-example-reviewer` | Must be independent of the author and cannot be a placeholder |
| decision_expiry | `2099-01-01` | Example only; real exceptions require a useful expiry and revisit trigger |

## Option record

The real packet must evaluate all five options using the same fields. This sample shows the shape for one fictitious option and does not recommend it.

| Field | Fictitious example |
|---|---|
| option_id | `OPTION-B-EXAMPLE` |
| option_name | `selective reviewed components` |
| proposed_use | `research-only component comparison in an external workspace` |
| explicitly_excluded_use | `no source import, release binary, generated output, native artifact, or production dependency` |
| charter_effect | `undetermined; owner must compare against the independent-engine boundary` |
| decision | `unresolved` |
| rationale | `Example has no authority to select, reject, or defer the option` |
| predecessor_conditions | `ADR9-EV-001 through ADR9-EV-018 reviewed or covered by an approved exception` |

## Evidence closure matrix

Every evidence item needs an immutable input identity, observation, maturity, limitation, owner disposition, and downstream claim effect. A passing validator or linked report is not a decision.

| Evidence | Input identity | Observed result | Maturity | Missing or limiting fact | Disposition in example |
|---|---|---|---|---|---|
| `ADR9-EV-001` source identity | `example-source-commit`, archive hash, Git tree hash | Git tree and archive were compared | `observed` | full blob and legal review absent | `hold` |
| `ADR9-EV-002` build reproduction | runner `example-runner-v1`, clean target id | build completed on one named host | `reproduced` | independent clean-host replay absent | `hold` |
| `ADR9-EV-003` dependency/SBOM | lockfile hash, profile, SBOM tool version | dependency list was generated | `observed` | owner-selected SBOM policy and advisory snapshot absent | `hold` |
| `ADR9-EV-004` legal/notices | license inventory hash | notices were enumerated | `observed` | patent, source-offer, codec, and native review absent | `hold` |
| `ADR9-EV-005/006` native packages/downloads | package manifest and asset hashes | package inputs were recorded | `observed` | source-build or time-bounded binary exception absent | `hold` |
| `ADR9-EV-007/008` generated output/side effects | generator manifest and trace id | one generated family was regenerated | `partial` | feature-correct full regeneration and dynamic side-effect review absent | `hold` |
| `ADR9-EV-009/010` unsafe and FFI | unsafe inventory and ABI manifest | candidate boundaries were listed | `partial` | block-level safety, ABI, lifetime, and platform evidence absent | `hold` |
| `ADR9-EV-011/012` component/runtime | dependency graph and runtime profile | component and JavaScript reachability were mapped | `partial` | option-specific replacement, GC, Web IDL, and Test262 decision absent | `hold` |
| `ADR9-EV-013` compatibility | corpus manifest and harness id | local fixtures passed shape validation | `observed` | browser-run WPT/Test262 denominator absent | `hold` |
| `ADR9-EV-014` performance | hardware, OS, runner, workload ids | a benchmark plan was recorded | `observed` | raw equal-workload browser results and statistics absent | `hold` |
| `ADR9-EV-015/016` security/maintenance | threat model and ownership record ids | risks and upstream obligations were listed | `partial` | compromised-process evidence, patch capacity, and backup coverage absent | `hold` |
| `ADR9-EV-017/018` claims/decision | proposed diff manifest | unsupported claims were listed | `reviewed` | no owner decision or synchronized canonical diff exists | `hold` |

The maturity value is monotonic for a specific immutable packet input, but higher maturity does not imply acceptance. A reviewed rejected experiment remains rejected evidence.

## Boundary and authority check

The packet must answer these questions before any option can be selected:

| Check | Fictitious result | Required rejection condition |
|---|---|---|
| source identity | `recorded, not accepted` | reject if commit, archive, generated output, or package identity is ambiguous |
| release-critical code | `undetermined` | reject if generated, native, runtime, build-script, or proc-macro reachability is unbounded |
| process and sandbox authority | `mapped, not tested` | reject if the option expands process, network, storage, credential, update, or UI authority |
| JavaScript runtime | `unresolved` | reject if runtime adoption or replacement is inferred from package presence |
| compatibility denominator | `not run` | reject compatibility or Chrome-class claims without browser-run raw artifacts |
| performance denominator | `not run` | reject speed, memory, energy, or extreme-performance claims without fixed-workload statistics |
| maintenance and ownership | `incomplete` | reject support or release claims without primary/backup ownership and patch capacity |
| legal and advisory posture | `unreviewed` | reject source or dependency approval without current license, notice, patent, advisory, and SBOM review |

## Authorization record shape

A real packet can authorize only a bounded scope after the decision is accepted. The example remains unresolved:

```text
decision_status: unresolved
selected_option: null
source_baseline: null
accepted_component_boundaries: []
authorized_work: []
prohibited_work:
  - source import
  - Servo-derived release code
  - production dependency approval
  - public compatibility, security, performance, or Chrome-class claim
  - release or distribution authorization
exception_records: []
owner_approval: null
independent_review: null
```

When a real decision is made, the authorization record must name the exact task manifest, allowed paths, feature profile, target profile, expiry, rollback, and required document and registry diffs. It must not authorize work by implication.

## Rejection and handoff rules

- Reject the packet if any evidence item is missing, stale, unscoped, or linked only by a mutable branch or warm checkout.
- Reject a selected option if source, generated output, native package, build-script, proc-macro, runtime, or FFI provenance is not traceable to the selected baseline and feature profile.
- Reject a legal or security exception without an owner, reviewer, risk linkage, support-boundary change, expiry, and rollback path.
- Reject compatibility or performance claims when the browser-run denominator, raw artifacts, workload, lifecycle, or statistical method is absent.
- Reject source import or release-code authorization when the decision record, task manifest, ownership, security, and release records are not synchronized.
- Keep `PB-002` blocked when the packet is `example_only`, `unresolved`, or merely validated.

## Claim boundary

This example proves only that a source-strategy review packet can keep evidence identity, option scope, authority boundaries, maturity, limitations, and authorization fields together. It does not select or reject Servo, establish source equivalence, approve a component, prove compatibility or performance, authorize source import, or promote `PB-002`/`ADR-0009`.

## Next proof

Use the real `ADR9-EV-*` inputs to replace the example with an owner-reviewed packet tied to an exact source baseline and feature profile. Then update the decision draft, evidence registry, pre-build readiness, task queue, risks, requirements, ownership, support, release, and public-claim boundaries atomically.
