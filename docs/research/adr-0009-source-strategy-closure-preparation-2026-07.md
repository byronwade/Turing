# ADR-0009 Source Strategy Closure Preparation - July 2026

Status: no-claim decision-closure preparation
Owner: architecture, engine, security, provenance, release operations, embedding, legal-community, and documentation owners
Related gate: `PB-002` and `ADR-0009`
Updated: 2026-07-20
Research date: 2026-07-20
Scope: decision synthesis only; no source import, component approval, or release-code authorization

## Purpose

This page is the short continuation route for the distributed ADR-0009 evidence set. It does not replace the [source-strategy decision packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md), [evidence traceability matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md), [decision draft](../project-buildout/16-adr-0009-decision-draft.md), or machine [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json). It tells a maintainer what must be true before those records can support an accepted source strategy.

The [ADR-0009 source-strategy packet examples](adr-0009-source-strategy-packet-examples-2026-07.md) provides a fictitious field-level handoff for option scope, evidence maturity, authority boundaries, limitations, and authorization. It is an example only and does not close any `ADR9-EV-*` item.

The checked no-claim [web-platform source manifest](../web-platform/machine/web-platform-source-manifest.json) preserves the standards, conformance, interoperability, and governance source identities relevant to the compatibility portion of this closure route. It does not establish web compatibility or close `ADR-0009`.

## Current decision state

`PB-002` remains `blocked`. The repository has dated source metadata, external build reproduction, dependency/provenance inventories, supply-chain scans, license/advisory/SBOM preparation, generated/native/unsafe/FFI classification, source/archive equivalence work, local compatibility planning, performance preparation, and security/maintenance analysis. These records are evidence inputs, not an accepted decision.

The checked no-claim decision-review template and passing validators prove that the evidence is tracked. They do not prove that an owner selected a source baseline, accepted provenance, approved a component boundary, accepted legal or advisory risk, or authorized release code.

## Options under review

The packet must evaluate the same five options without changing their names between prose, machine records, and owner review:

1. clean Turing implementation informed by Servo research;
2. selective use of reviewed Servo components;
3. upstream-first collaboration without importing Servo-derived release code;
4. a Servo-derived engine path under an explicitly accepted boundary;
5. an explicit charter change to a Servo browser.

The options are not interchangeable. A component reuse decision is not an engine adoption decision, and a charter change is not evidence that the existing independence boundary was satisfied.

## Option normalization matrix

This matrix normalizes the owner review before any option is scored or selected. It is a comparison aid, not a recommendation or decision.

| Option | Current charter relationship | Release-surface consequence | Minimum decision-grade evidence | Claim permitted before acceptance |
|---|---|---|---|---|
| A. Clean implementation informed by Servo | Preserves the current independent-engine boundary if Servo remains research input only | Turing owns the engine, runtime, integration, compatibility, security, and maintenance surface | Evidence that no Servo source, generated output, dependency, or release artifact enters the selected profile; Turing-owned implementation and maintenance plan | Servo is external research context only; no compatibility, performance, or security behavior transfers |
| B. Selective Servo components | May preserve the boundary only for explicitly named, reviewed, replaceable components | Every accepted component adds provenance, license, dependency, API, unsafe/FFI, security, update, and replacement obligations | In/out component list, dependency closure, source baseline, generated-output policy, replacement contracts, runtime/process authority review, and owner-approved maintenance | Only the exact named component scope may be discussed, and only as accepted evidence; no whole-Servo claim |
| C. Upstream-first collaboration | Preserves the release boundary while permitting contribution and evidence exchange | Turing retains release, security, support, and maintenance responsibility; upstream activity does not become a runtime dependency | Contribution policy, patch ownership, review/disclosure route, upstream tracking, evidence-ingestion boundary, and fork/rollback policy | Collaboration and external research activity only; no source adoption or support transfer |
| D. Servo-derived engine | Conflicts with the current independent-engine posture unless the charter and dependent records change first | Servo-derived source, runtime, generated output, native packages, security model, compatibility, release, and maintenance become release-critical | Full source/dependency/provenance, legal/SBOM, runtime, security, compatibility, performance, platform, support, update, and maintenance review plus charter synchronization | No Servo-derived or browser-support claim until the charter and all dependent gates are accepted |
| E. Explicit Servo browser charter change | Replaces the current product identity and independence premise | Requirements, market position, ownership, support, release, security, and roadmap must be rebaselined around a Servo-focused product | Explicit charter change, product and legal review, upstream governance, branding/trademark, support, release, security, and migration plan | No current Turing independent-browser claim may be reused; only an approved new charter can define claims |

The owner must record the selected, rejected, or deferred option, the rationale, the evidence disposition, and the exact claim boundary. A lower implementation burden does not override charter, security, provenance, legal, compatibility, or maintenance requirements.

## Pre-review decision worksheet

The real owner review must complete one worksheet row for each of Options A-E. A row is not complete because an option is described or because evidence exists; it is complete only when the disposition, scope, reviewers, limitations, and synchronized record changes are explicit.

| Required field | What the reviewer must record | Rejection condition |
|---|---|---|
| Option disposition | `selected`, `rejected`, or `deferred`, with rationale and rejected alternatives | Missing rationale, multiple selected options, or a decision inferred from evidence presence |
| Charter and independence effect | Whether the current independent-engine boundary is preserved, narrowed, or replaced, with exact affected ADR/requirement paths | Any release-boundary change without charter and dependent-record review |
| Source boundary | Exact baseline/ref/archive/package, feature and target profiles, included and excluded source/components, generated-output scope, and provenance policy | `latest`, `Servo`, or `upstream` without an immutable identity and equivalence policy |
| Evidence disposition | Status for every `ADR9-EV-001` through `ADR9-EV-018`: observed, reproduced, reviewed, decided, or explicitly held by an expiring exception | Any unresolved evidence hidden by a general approval or omitted from the denominator |
| Authority and review | Named decision owner, independent reviewer, legal/community reviewer where applicable, review date, and dissenting evidence | Self-approval, title-only identity, or missing independent review |
| Authorization scope | Exact implementation, release, dependency, component, platform, and claim scope unlocked; explicit prohibited scope | Planning evidence treated as source import, component approval, or release-code authorization |
| Operations and rollback | Primary/backup ownership, maintenance and security response, rollback, replacement, abandonment, and revisit trigger | No qualified backup, rollback path, expiry, or support-boundary update |
| Synchronized diff | Paths and hashes for the ADR, Blueprint, requirements, risks, work packages, registries, support language, and public claim changes | Any affected canonical or machine record left stale |

Until a real review replaces the no-claim template, every worksheet row is `unresolved_template`, every option disposition is unset, and no authorization scope exists. The worksheet makes the missing owner decision visible; it does not select an option or increase `PB-002` readiness.

## Provenance policy boundary for source identity

The [Git tag documentation](https://git-scm.com/docs/git-tag) distinguishes a lightweight tag, which directly names an object, from an annotated tag object that can carry a message and cryptographic signature; it describes signed annotated tags as the normal release-oriented form. [`git verify-tag`](https://git-scm.com/docs/git-verify-tag) validates signatures on tag objects, so it cannot turn a lightweight tag into a signed release assertion. GitHub's [commit-signature documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) separately describes verified GPG, SSH, and S/MIME commit or tag signatures and notes that repository policy can enforce signed commits.

Implications for `ADR9-EV-001`:

- the evidence record must state whether the accepted source identity is a signed annotated tag, a signed commit at an independently pinned ref, or another explicitly approved provenance model;
- a lightweight release tag, a GitHub `Verified` badge, a local `git verify-commit` result, a source archive digest, and a crates.io checksum are separate observations and must not be silently substituted for one another;
- verification must retain the exact ref, object type, object ID, tree ID, signer identity, verification mechanism, trust-root/key status, retrieval date, revocation or expiry treatment, and independent remote-ref comparison;
- if a GitHub-verified commit is accepted as an equivalent to a signed release tag, the decision must name the key-identity, repository-control, ref-pinning, and replay protections that make the equivalence bounded and auditable;
- a failed local key lookup or a lightweight tag is evidence about the verification environment or object form, not proof that the source is malicious; it remains unresolved until the owner-approved provenance policy classifies it.

These sources define the vocabulary and verification boundary. They do not select Servo, accept GitHub as Turing's trust root, or approve any source baseline.

## Decision criteria

The owner review must score or explicitly disposition every option against the following criteria:

### Independence and charter

- Does the option preserve the independent-engine boundary in `AGENTS.md` and Blueprint 01?
- Which code, generated output, native artifact, build script, proc-macro, or runtime would become release-critical?
- Does the option require a charter change, and where is that change recorded?

### Source identity and provenance

- What exact source baseline, commit, archive, package, submodule, and vendor inputs are selected?
- Are Git tree, release archive, vendored archive, registry package, and generated output equivalence claims tested at the required granularity?
- Are tags, signatures, commit verification, source hashes, generator versions, and environment inputs retained?
- Can an independent reviewer reproduce the selected baseline without relying on an untracked or warm checkout?

### Legal, advisory, and supply chain

- Are licenses, notices, source offers, patents/codecs, native packages, and duplicate versions accepted for the selected profile?
- Are advisory exceptions explicit, current, owner-approved, and bounded by version and feature profile?
- Is the SBOM tool/profile selected and generated for the exact candidate artifact?
- Are build scripts, proc macros, downloads, native binaries, and generated output covered by provenance and side-effect policy?

### Architecture and security

- Are process, sandbox, IPC, identity, site-isolation, storage, update, and credential boundaries compatible with Turing's accepted contracts?
- Are unsafe blocks, FFI ABIs, callbacks, thread affinity, native handles, and privileged paths reviewed at component boundaries?
- Does the option introduce a JavaScript runtime or other dependency that conflicts with the independent-engine boundary?
- Can unsupported or rejected components be removed without leaving hidden authority or untracked generated output?

### Compatibility and performance

- What is the exact WPT/Test262 and local-corpus denominator, and which failures are accepted or unsupported?
- Can the selected candidate run the Turing-owned compatibility corpus through the planned HTTPS/browser harness with raw artifacts?
- Can fixed-hardware performance, memory, energy, startup, and long-run results be generated under equal workloads without hidden tab discarding or unmatched caches?
- Which claims remain explicitly unsupported if the candidate does not meet the product target?

### Maintenance and operations

- Who owns upstream tracking, patch queues, security response, breakage handling, release rebuilds, and deprecation?
- What is the plan when upstream changes the source, generated outputs, native packages, license, advisory state, or toolchain?
- Can the project sustain the maintenance and emergency-patch burden with the current ownership and backup state?
- What is the cost and failure mode of abandoning or replacing the option?

## Evidence maturity rules

Evidence must be evaluated in the following order:

1. **observed**: dated raw observation with source identity and environment;
2. **reproduced**: independent or owner-accepted replay with retained logs and artifacts;
3. **reviewed**: named reviewer accepts scope, method, limitations, and claim impact;
4. **decided**: owner selects, rejects, or defers the option and updates all affected records;
5. **authorized**: the decision unlocks only the exact release or implementation scope stated in the record.

A report can be observed or reproduced without being reviewed. A reviewed experiment can remain a rejected input. A selected option does not authorize source import until the decision record, task manifest, ownership, security, and release boundaries are synchronized.

## Required closure record

The real ADR-0009 decision review must replace the checked template's null fields with:

- selected, rejected, or deferred option and exact rationale;
- source baseline, component boundary, feature profile, target profile, and generated-output scope;
- evidence references for all `ADR9-EV-001` through `ADR9-EV-018` items, including unresolved limitations;
- legal, advisory, SBOM, native-package, license, provenance, FFI, unsafe, runtime, compatibility, performance, security, and maintenance dispositions;
- owner and independent reviewer identities, review date, decision expiry or revisit trigger, and dissenting evidence;
- synchronized changes to Blueprint, requirements, risks, ADR registry, backlog, task queue, ownership, support, release, security, and public-claim language;
- explicit authorization scope and prohibited scope;
- rollback, abandonment, replacement, and incident-response conditions.

## Stop conditions

Keep `PB-002` blocked if any of the following is true:

- the source baseline is selected by assumption, convenience, or the newest observed revision;
- a warm same-host build is presented as independent clean-target reproduction;
- archive, package, Git tree, or generated-output equivalence is asserted without the required comparison;
- a legal, advisory, SBOM, native-package, unsafe, FFI, runtime, compatibility, performance, security, or maintenance gap is hidden in a general approval;
- a component boundary grants more process, network, storage, update, credential, or UI authority than Turing's accepted contracts;
- owner review is replaced by a template, validator, agent recommendation, or chat decision;
- the decision does not update every affected canonical record and public claim boundary;
- the decision would authorize Servo-derived release code before the independent review and task controls are complete.

## PB-020 closure dependency

Any future `PB-002` or `ADR-0009` decision must be reconciled through the [Owner Decision Closure Board](../project-buildout/23-owner-decision-closure-board.md) and the [Build-Readiness Closure and Owner-Decision Preparation](build-readiness-closure-and-owner-decision-preparation-2026-07.md) route. An accepted source option, completed evidence item, legal review, or ADR decision cannot independently close `PB-020`, authorize broad implementation, approve source import or release code, or support compatibility, performance, security, production, or Chrome-class claims. The final closure record must preserve provenance, equivalence, legal/SBOM, component-boundary, reviewer, limitation, exception, expiry, and synchronized registry evidence.

## Next proof

The next action is not another broad source import. It is to complete the remaining `ADR9-EV-*` evidence under the selected replay protocol, have the owner and independent reviewers evaluate the evidence, and replace the no-claim decision-review template with a real decision record. Until then, use the [PB-002 row on the owner-decision closure board](../project-buildout/23-owner-decision-closure-board.md) and keep all source-strategy, adoption, component, compatibility, performance, security, and release claims bounded.

## Claim boundary

This page does not select Servo, reject Servo, approve a Turing engine architecture, authorize source import, authorize release code, establish compatibility or performance, or promote `PB-002`/`ADR-0009`. It is a continuation and decision-closure aid only.
