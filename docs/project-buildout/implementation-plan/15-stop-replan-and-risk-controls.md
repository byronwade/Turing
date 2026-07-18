# 15 — Stop, Replan, Replace, and Abandon Criteria

Status: normative decision discipline for implementation
Owner: program, architecture, security, quality, and affected subsystem owners

## 1. Purpose

Turing's vision is ambitious, but no architecture, framework, feature, or schedule is entitled to survive contrary evidence. This chapter prevents sunk-cost escalation and unsafe demos from becoming permanent product direction.

## 2. Immediate stop conditions

A task or release stops when:

- a critical security, update, signing, data-loss, or cross-profile defect is discovered;
- implementation conflicts with an accepted requirement or ADR;
- the selected dependency/license cannot support intended distribution;
- platform sandbox evidence shows prohibited ambient authority;
- trusted UI can be spoofed or hidden;
- migration or rollback can irreversibly corrupt supported profiles;
- an accessibility-critical workflow becomes unusable;
- benchmark or conformance evidence is fabricated, selectively omitted, or materially incomparable;
- a required independent reviewer is unavailable;
- agent authority, credentials, or path boundaries are exceeded;
- a failing gate would need to be weakened to continue;
- production signing or private vulnerability material is exposed.

Work resumes only after containment, root-cause analysis, updated design, regression evidence, and authorized review.

## 3. Replan triggers

Replan a subsystem when:

- measured performance, memory, energy, binary, or build cost misses the agreed envelope materially;
- interface churn repeatedly breaks dependents;
- conformance progress stalls because the representation cannot express required semantics;
- unsafe/native surface grows beyond the reviewed boundary;
- dependency update or security cadence exceeds owner capacity;
- platform behavior diverges enough that a common abstraction becomes misleading;
- user studies reject the workflow or cannot understand its safety model;
- accessibility requires structural redesign rather than incremental patches;
- the team cannot maintain the claimed support scope;
- a standards direction changes the underlying requirement.

A replan produces new hypotheses, options, migration cost, stop criteria, and a bounded experiment—not an unbounded rewrite.

## 4. Replace criteria

Replace a framework, library, protocol, or internal design when an alternative demonstrates a better total result across:

- correctness and standards fit;
- containment and attack surface;
- accessibility and platform fidelity;
- startup, latency, memory, energy, and package cost;
- maintenance and reviewer availability;
- license and provenance;
- interoperability and ecosystem;
- observability and testability;
- migration and rollback cost;
- long-term replacement flexibility.

A microbenchmark alone cannot justify replacement. The selected alternative must pass equivalent end-to-end workloads and failure tests.

## 5. Simplify criteria

Prefer simplification when:

- a feature can be a Plug-in rather than trusted kernel code;
- a platform service safely replaces custom specialist code;
- a stable C/WIT/schema boundary avoids multiple implementations;
- a smaller standards subset provides a coherent milestone;
- a local-only mode avoids premature account/service infrastructure;
- one reference platform can validate architecture before broad porting;
- a deterministic reference path can precede parallel/incremental optimization;
- a feature's user value does not justify permanent authority or background work.

## 6. Abandon criteria

A proposed feature or approach may be abandoned when:

- it cannot meet the project's independent-engine or open-web charter without an explicit charter change;
- security cannot be made acceptable within a maintainable design;
- legal or licensing access is unavailable;
- accessibility cannot be provided for the supported workflow;
- users do not value it after controlled research;
- operational cost exceeds sustainable funding;
- compatibility burden creates more harm than value;
- a standards-based or external product is clearly better and safely interoperable;
- no qualified owner accepts long-term maintenance;
- repeated experiments falsify the core performance or simplicity hypothesis.

Abandonment is recorded with evidence and migration/removal effects. It is not hidden by leaving permanent experimental flags.

## 7. Exception policy

An exception must be:

- specific to one gate and scope;
- justified by evidence;
- approved by the required owner/reviewer;
- time-bounded with expiry;
- visible in machine records and release notes where user-relevant;
- accompanied by compensating controls and rollback;
- prohibited for critical security, signing, secret exposure, or known irreversible data-loss conditions.

Expired exceptions block the next merge or release until renewed or removed.

## 8. Incident-to-design feedback

Every material incident asks:

- which assumption failed;
- why tests/review/monitoring did not catch it;
- whether the defect class exists elsewhere;
- which requirement, ADR, interface, task template, test suite, runbook, and training material must change;
- whether support scope or rollout should contract;
- what independent evidence is required before reactivation.

## 9. Rewrite control

A rewrite is authorized only when:

- the current system's failure is evidenced;
- incremental alternatives were evaluated;
- compatibility and migration are designed;
- reference tests preserve semantics;
- staffing and schedule are credible;
- the old implementation remains available until the replacement passes gates;
- the rewrite does not become an excuse to suspend security fixes.

## 10. Decision record

Every stop/replan/replace/abandon decision records:

- affected IDs and versions;
- evidence and confidence;
- user/security/accessibility/compatibility/operational impact;
- alternatives;
- chosen action and owner;
- migration/rollback;
- review date;
- conditions for reconsideration.
