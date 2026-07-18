# 17 — Task Kickoff, Evidence, Handoff, and Release Checklists

Status: normative operational checklist
Owner: program, agent operations, reviewers, and release operations

## 1. Task kickoff checklist

A task may move to `ready` only when:

- [ ] stable `TASK-*` ID exists;
- [ ] parent WP, milestone, requirements, risks, and ADRs are identified;
- [ ] dependencies are accepted on `main`;
- [ ] owner and independent reviewer are named;
- [ ] allowed and prohibited paths are explicit;
- [ ] tools, network, credentials, environment, budget, retries, and expiry are explicit;
- [ ] design source or experiment hypothesis exists;
- [ ] acceptance criteria are objective;
- [ ] negative, failure, cancellation, timeout, recovery, and resource tests are listed;
- [ ] documentation impact map is complete;
- [ ] evidence classes are selected;
- [ ] rollback and escalation are defined;
- [ ] no unresolved ADR blocks implementation;
- [ ] no unapproved dependency, native code, build script, or unsafe block is assumed.

## 2. Agent run checklist

Before writing:

- [ ] record base commit and clean status;
- [ ] run doctor and baseline check;
- [ ] record model, instructions, tools, permissions, environment, and task digest;
- [ ] verify task has not expired or changed;
- [ ] verify branch naming and protected-main rules;
- [ ] read all required subsystem documents.

During work:

- [ ] stay within path and resource bounds;
- [ ] update canonical source, not only generated output;
- [ ] preserve failed experiments and meaningful alternatives;
- [ ] add tests before or with implementation;
- [ ] stop on authority, decision, dependency, secret, scope, or gate conflicts;
- [ ] keep implementation and documentation synchronized.

Before submission:

- [ ] run focused tests;
- [ ] run generator drift checks;
- [ ] run formatting, lint, full tests, fuzz/model checks as applicable;
- [ ] run documentation and repository validation;
- [ ] inspect diff for unrelated changes, secrets, debug output, and generated junk;
- [ ] assemble evidence bundle;
- [ ] update traceability/status honestly;
- [ ] state unsupported behavior and residual risk;
- [ ] verify rollback.

## 3. Pull-request checklist

- [ ] title states the semantic result;
- [ ] body names task/WP/requirements/risks/ADRs;
- [ ] base and head commits are recorded;
- [ ] architecture and authority changes are explained;
- [ ] security/privacy, performance, accessibility, compatibility, operations, and legal impacts are addressed;
- [ ] exact validation commands and immutable artifacts are linked;
- [ ] negative and failure tests are summarized;
- [ ] generated files and commands are listed;
- [ ] migrations and rollback are described;
- [ ] docs/registries/owners/status are synchronized;
- [ ] no self-approval or self-merge is claimed;
- [ ] appropriate code owners and specialists are requested.

## 4. Independent reviewer checklist

The reviewer must:

- [ ] confirm task authority and dependency state;
- [ ] compare implementation with accepted requirements and design;
- [ ] inspect privileged inputs, identities, capabilities, lifetimes, and failure paths;
- [ ] attempt at least one adversarial or boundary case not supplied by the author;
- [ ] verify tests can fail for the defect class;
- [ ] reproduce the most load-bearing evidence independently where required;
- [ ] inspect unsafe/native/dependency/generated-code changes;
- [ ] confirm documentation and status do not overclaim;
- [ ] evaluate rollback and downstream compatibility;
- [ ] leave explicit approval, requested changes, or non-approving commentary.

A resolved comment is not automatically an approval.

## 5. Work-package acceptance checklist

- [ ] all planned task families are accepted or explicitly descoped;
- [ ] requirements have implementation and verification evidence;
- [ ] risk controls and residual risks are current;
- [ ] required ADRs and interface freezes are accepted;
- [ ] conformance denominator and results are published;
- [ ] security, privacy, performance, accessibility, reliability, compatibility, operational, and documentation evidence is complete;
- [ ] downstream conformance or handoff package exists;
- [ ] no blocking critical defect or expired exception remains;
- [ ] work-package status is updated in prose and machine records;
- [ ] unsupported behavior remains explicit.

## 6. Milestone gate checklist

- [ ] every milestone deliverable has an accepted WP or explicit non-scope record;
- [ ] interface freeze points needed by the next milestone are versioned;
- [ ] all blocking requirements and risks have evidence;
- [ ] integrated failure, crash, recovery, and pressure tests pass;
- [ ] product/accessibility/security workflows are tested end-to-end;
- [ ] benchmark and conformance results use the declared environment and denominator;
- [ ] release labels and user warnings match maturity;
- [ ] owner capacity supports the next phase;
- [ ] phase-gate review records proceed, proceed-with-exception, replan, or stop.

## 7. Handoff template

```text
Task / WP:
Merged commit:
Interface versions:
Requirements and risks:
What is implemented:
What is not implemented:
Security and privacy boundary:
Performance/resource baseline:
Accessibility/compatibility status:
Evidence bundle:
Generated artifacts and commands:
Known defects and exceptions:
Rollback:
Downstream tasks now unblocked:
Downstream assumptions that remain blocked:
Owner and reviewer:
Next review/expiry:
```

## 8. Release candidate checklist

- [ ] finite supported scope and platform matrix;
- [ ] all applicable `PRG-*` gates ready;
- [ ] all blocking `SLO-*` targets within budget;
- [ ] exact conformance and compatibility reports;
- [ ] independent security and accessibility reviews;
- [ ] reproducible artifact, SBOM, provenance, symbols, notices, digest, and signatures;
- [ ] install, upgrade, migration, rollback, downgrade, repair, and uninstall evidence;
- [ ] service outage, offline, disaster-recovery, and incident rehearsals;
- [ ] vulnerability response and support staffing;
- [ ] legal/privacy/license/distribution approval;
- [ ] production signing separation and audit;
- [ ] release notes, known issues, support duration, and EOL statement;
- [ ] human release authority approval.

## 9. Post-merge monitoring checklist

For changes that affect supported channels:

- [ ] rollout cohort and stop thresholds defined;
- [ ] crash, performance, compatibility, accessibility, data-loss, update, and service signals monitored;
- [ ] rollback is available and tested;
- [ ] owner/on-call is active;
- [ ] user reports and regressions are triaged;
- [ ] evidence and status are refreshed after the observation window;
- [ ] temporary flags, interventions, or exceptions have owners and expiry.
