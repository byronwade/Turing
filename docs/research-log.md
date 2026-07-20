# Research Log

## 2026-07-20 - Sandbox containment contract freshness revalidation

Re-ran the platform-source, sandbox-contract, probe-inventory, and sandbox-readiness validators from the repository checkout. All four passed, confirming that the Windows/Linux/macOS evidence matrix, 21-operation catalog, evidence schema, package handoff, and no-claim readiness template remain synchronized. Updated the dated sandbox records to reflect this revalidation. This closes a freshness and internal-consistency check only; `PB-012` remains partial with no packaged probe results, effective platform-policy artifacts, containment claim, or owner review.

## 2026-07-20 - ADR-0009 upstream head freshness refresh

Re-ran read-only official GitHub API observations for `servo/servo` and `servo/mozjs`. Servo's moving `main` head changed to `f542a355e5565e380aa0570132d4138dde328bae`, while `mozjs` remained at `f5cbf8aa6076064fd658a1e9fb16147c2347affb`; updated timestamps and release identities were preserved in the source manifest and upstream delta packet. Marked the changed moving head as a freshness delta that invalidates downstream evidence tied only to that ref. This is no-claim source freshness work; it does not select a baseline, approve Servo, or change PB-002.

## 2026-07-20 - Fresh-host current-toolchain diagnostic refresh

Rechecked the current Windows checkout's Rust, Cargo, rustfmt, Clippy, Python, Git, rustup, host tuple, repository toolchain override, installed target, and clean working-tree state. The observed identities remain aligned with the pinned M0 baseline. Added the dated diagnostic to the fresh-host closure packet while preserving the boundary that same-host facts are not independent fresh-host or owner-reviewed readiness evidence.

## 2026-07-20 - Benchmark suite identity freshness refresh

Rechecked the official Speedometer 3.1 methodology page and found no suite-identity change. Synchronized the benchmark source manifest and performance runbook with the new retrieval date while preserving the no-runner, no-result, no-comparison, and no-performance-claim boundaries. Local browser-version mismatches and missing owner-reviewed runner evidence remain unresolved.

## 2026-07-20 - Nova source-component coverage reconciliation

Compared the 91 named function components in the committed Nova JSX source with the surface-contract map. Added an explicit reconciliation for shared primitives, settings subsections, popovers, vault rows, and assistant/DevTools message elements that are intentionally owned by parent component contracts rather than treated as separate product authorities. This closes source-coverage navigation only; no native fixture, accessibility, security, toolkit, or implementation gate changed.

## 2026-07-20 - IPC message-class policy contract

Added a candidate-independent IPC message-class policy proposal covering control envelopes, requests, responses, events, and persisted diagnostics. It makes unknown-field, unknown-variant, malformed-input, stale-state, authority, resource, and diagnostic handling explicit before codec selection. This improves decision readiness only; no wire format, generator, transport, or `PB-011` status changed.

## 2026-07-20 - Repository-wide source-manifest provenance audit

Audited all thirteen checked source-manifest families and every declared `source_documents` entry. All twelve manifests with document lists resolve to existing files and are referenced by each owning document, including the repository-root `.github/CODEOWNERS` control file. Extended `tools/validate_source_manifest_coverage.py` to enforce this repository-wide identity link invariant so future audits cannot omit non-`docs/` paths. This closes provenance organization only; it does not create implementation evidence or promote M0 or full-build readiness.

## 2026-07-20 - Documentation-readiness manifest count correction

Compared the documentation-readiness evidence matrix with the current metadata validator, source-manifest coverage validator, and repository map. Corrected the matrix's stale eleven-manifest description to thirteen so the primary human evidence contract matches the machine-checked coverage. This is a synchronization correction only; no evidence, gate, task authority, or readiness percentage changed.

## 2026-07-20 - Ownership/control provenance route completion

Question:

Do the ownership, CODEOWNERS, release-operations, backup-gap, and two-person-control records expose the manifest that governs their official governance observations?

Method:

Compared the `GOVERNANCE.OWNERSHIP.SOURCES.2026_07` source-document list with its six missing inbound references. Added direct no-claim manifest links to the two ownership research routes and two project-buildout operating documents, added a source-identity comment to `CODEOWNERS`, and added the manifest to the backup-gap registry's existing `source_registries`. This closes provenance navigation only; ownership remains provisional and `PB-019` remains blocked.

## 2026-07-19 - Incident-response provenance route completion

Question:

Do the incident-response, emergency-patch, security-gate, supported-lifecycle, and machine-rehearsal records expose the manifest that governs their official observations?

Method:

Compared the `SECURITY.INCIDENT.SOURCES.2026_07` source-document list with its six missing inbound references. Added direct no-claim manifest links to the five canonical prose routes, and added an explicit `source_manifest` field to the machine rehearsal inventory, schema, and validator. This closes provenance navigation only; it does not establish incident readiness, emergency patch capacity, disclosure or signing authority, supported-security coverage, or release approval.

## 2026-07-19 - Profile/session provenance route completion

Question:

Do the profile/session data-safety, migration, credential, and machine-format records expose the manifest that governs their official storage observations?

Method:

Compared the `STORAGE.PROFILE_SESSION.SOURCES.2026_07` source-document list with its five missing inbound references. Added direct no-claim manifest links to the closure route, format inventory, migration/recovery book, and credential/clearing book, and added an explicit `source_manifest` field to the machine format inventory and schema. This closes provenance navigation only; it does not establish a profile format, migration safety, credential handling, sync, data-loss safety, or production readiness.

## 2026-07-19 - Package/update provenance route completion

Question:

Do the package/update trust, release-operation, and lab records expose the source manifest that governs their official observations?

Method:

Compared the `RELEASE.UPDATE.SOURCES.2026_07` source-document list with its six missing inbound references. Added direct no-claim manifest links to the decision-preparation, lab-inventory, update, reproducible-build, and signing contracts, and added an explicit `source_manifest` field to the machine lab registry and schema. This closes provenance navigation only; it does not create an updater, signing authority, rollback or migration evidence, release readiness, or supported-security claim.

## 2026-07-19 - Web-platform provenance route completion

Question:

Do the canonical web-platform, compatibility, parity, and source-strategy documents expose the checked web-platform manifest that governs their standards and conformance observations?

Method:

Compared the `WEB_PLATFORM.SOURCES.2026_07` source-document list with its 12 missing inbound references. Added direct no-claim manifest links across the six web-platform chapters, Blueprint parity/testing/bibliography/research routes, the Servo compatibility corpus report, and the ADR-0009 closure preparation. This closes provenance navigation only; it does not establish standards conformance, compatibility, security, accessibility, performance, or implementation evidence.

## 2026-07-19 - IPC, fresh-host, and sandbox provenance handoff audit

Question:

Do the remaining critical IPC, fresh-host, and sandbox closure records expose the source manifests that govern their platform and toolchain observations?

Method:

Compared the source-document lists for `IPC.WIRE.SOURCES.2026_07`, the fresh-host toolchain manifest, and `SEC.SANDBOX.PLATFORM_SOURCES.2026_07` with their canonical records. Added the IPC wire manifest to the capability-boundary inventory, the fresh-host toolchain manifest to the machine reproduction registry's existing `source_records`, and the sandbox platform manifest to the closure-preparation route. This closes provenance navigation only; it does not establish IPC transport, fresh-host reproduction, effective sandbox policy, containment, or readiness.

## 2026-07-19 - Technology and dependency provenance inbound-link audit

Question:

Do the foundational source-strategy documents expose the checked technology/dependency manifest that governs their official observations?

Method:

Compared the `DEPENDENCY.SOURCES.2026_07` source-document list with its five missing inbound references. Added direct no-claim links to the manifest in the M0 foundation, language/dependency strategy, security/sandbox, build/release operations, and ADR-0009 source-strategy packet. This closes provenance navigation only; it does not select a language, dependency, engine source, build policy, or release foundation.

## 2026-07-19 - Research crosswalk count drift control

Question:

Can the maintainer-facing progress snapshot remain synchronized with the machine research crosswalk when evidence routes change?

Method:

Corrected the snapshot's stale `256/256` evidence-path count to the machine-derived `259/259` count and extended the research-question coverage registry and validator with an explicit progress-snapshot source. The validator now rejects a stale snapshot sentence while preserving the 66-question, 37-active, 29-deferred, 10-lane, no-claim boundaries. This improves status tracking only; it does not answer a research question, approve a task, promote readiness, or create build evidence.

## 2026-07-19 - Accessibility source-manifest inbound-link audit

Question:

Do the canonical accessibility and UI-runtime documents listed by the checked accessibility source manifest expose that manifest to a future maintainer?

Method:

Compared the `UI.ACCESSIBILITY.SOURCES.2026_07` source-document list with the five documents that lacked an inbound manifest reference. Added direct no-claim links to the manifest in the window/input inventory, accessibility bridge and testing chapters, the UI-runtime platform contract, and the Nova design-lab index. This closes navigation traceability only; it does not create accessibility workflow, screen-reader, IME, page-tree, native UI, or release-gate evidence.

## 2026-07-19 - Browser-engine landscape provenance control

Question:

Can the `RQ-16`/`RQ-25` engine-landscape hypothesis packet preserve its official architecture, runtime, protocol, standards, governance, and benchmark-context sources in the same checked provenance route as the other high-risk lanes?

Method:

Added a no-claim browser-engine landscape source manifest, schema, and validator; bound them to the source-strategy crosswalk, build-information ledger, documentation-readiness audit, PB-020 closure template, research index, documentation matrix, repository map, and aggregate `xtask` check. Extended the documentation validator's approved machine-registry directories to include `docs/research/machine/`, refreshed the human crosswalk coverage count from 256 to 259 evidence-start entries, linked the manifest from every canonical source document listed by the manifest, and synchronized the maintainer start guide, continuation pack, and human build-information ledger. The records improve source identity and freshness tracking only. They do not select an engine, authorize source use, establish comparative performance, or change the 90% contained-M0 / 0% full-build measures.

## 2026-07-19 - Benchmark source-manifest inbound-link audit

Question:

Do every canonical benchmark source document listed by the checked source manifest expose that manifest to a future reader?

Method:

Compared the `BENCHMARK.SOURCES.2026_07` source-document list with the benchmark readiness packet and Blueprint 09. Added direct links to the checked no-claim source manifest in both documents. The source manifest, validator, evidence axes, and no-claim status are unchanged; this closes navigation traceability only and does not create benchmark, competitor, statistical, performance, or Chrome-class evidence.

## 2026-07-19 - GitHub handoff baseline existence control

Question:

Can the offline GitHub handoff validator reject a correctly shaped but deleted or unavailable baseline commit?

Method:

Updated `validate_github_issue_handoff.py` to resolve `snapshot.baseline_commit` through `git cat-file` as a commit object, and documented the stronger invariant in the repository map. The handoff remains an offline coordination snapshot; this only verifies that its recorded source identity exists locally and does not contact GitHub, approve tasks, or promote readiness.

## 2026-07-19 - TASK-000011 review-baseline wording alignment

Question:

Does the `TASK-000011` review handoff distinguish its historical evidence baseline from the current repository head used for continuation?

Method:

Reconciled the handoff wording with the immutable historical evidence bundle and current `main` head. The document now identifies the prior review baseline and current continuation audit separately, while requiring a new exact-commit evidence bundle before independent acceptance. This prevents historical M0 evidence from being mistaken for current-head evidence and does not change task status or the 90% contained-M0 / 0% full-build measures.

## 2026-07-19 - GitHub handoff source identity refresh

Question:

Does the GitHub issue handoff still identify the repository revision used for its live issue/PR snapshot?

Method:

Re-ran the documented `gh issue list`, `gh pr list`, and `git rev-parse HEAD` commands. The canonical backlog and stale-PR cleanup boundary remain unchanged, while the repository baseline moved from the old recorded commit to `632e8f7f0d3b9f1a5737a1205a1babc4bb031ca0`. Synchronized the human handoff and machine snapshot. This repairs source identity only; GitHub coordination records remain non-authoritative for task approval and readiness.

## 2026-07-19 - Cross-cutting independent-verification route clarification

Question:

Does the research index make clear that active `RQ-60` independent-verification work is consumed by multiple readiness lanes rather than creating an untracked eleventh gate?

Method:

Added an explicit cross-cutting route note to the research index. It binds `RQ-60` to IPC, sandbox, benchmark, native/accessibility, incident-response, and ownership evidence while preserving the machine crosswalk's ten readiness lanes and no-claim boundary. This improves continuation routing only; it does not create a gate, accept evidence, or change the 90% contained-M0 / 0% full-build measures.

## 2026-07-19 - Full-goal percentage wording alignment

Question:

Could the closure-preparation document's `1/10 blocked_for_full_goal` wording be mistaken for 10% full-build completion when the canonical audit measures `0/10 ready_for_full_goal`?

Method:

Clarified the closure-preparation status sentence to show both facts: nine criteria are ready for contained M0, the single owner-decision criterion is blocked for the full goal, and zero criteria are ready for the full goal. This aligns the closure route with the progress snapshot and machine audit without changing any gate or percentage.

## 2026-07-19 - Implementation-plan authority regression guard

Question:

Can the implementation-plan validator prevent the human task-authority chain from drifting back to language that omits owner review or bounded authority?

Method:

Updated `validate_implementation_plan.py` to require the canonical authority phrase in the implementation-plan README, and updated the repository map to describe that check. This converts the prior wording correction into a permanent regression control; it does not approve any task or change the 90% contained-M0 / 0% full-build measures.

## 2026-07-19 - Implementation-plan task-authority wording correction

Question:

Does the master implementation sequence distinguish a task-shaped manifest from an executable, owner-reviewed task authority record?

Method:

Changed the implementation-plan sequence from `ready TASK manifest` to `owner-reviewed immutable ready TASK manifest with bounded authority`. This aligns the master plan with the contained-M0 start-state inventory, task approval template, specified task manifests, and production-agent controls. It removes an ambiguity only; no proposed task became executable and the 90% contained-M0 / 0% full-build measures remain unchanged.

## 2026-07-19 - Owner-decision next-action link control

Question:

Can a future edit leave the owner-decision board's gate rows present while silently detaching a gate from its canonical closure-preparation route?

Method:

Added an explicit gate-to-closure-route map to `validate_owner_decision_closure_board.py` and linked the `PB-019` and `PB-020` rows to their canonical preparation documents. The validator now requires every canonical gate row to retain its expected route link in the current-next-action cell. This improves handoff integrity only; all owner decisions remain unresolved and the 90% contained-M0 / 0% full-build measures do not change.

## 2026-07-19 - Source-manifest coverage regression control

Question:

Can future documentation changes automatically detect when a source manifest, schema, or validator is omitted from its owning lane and the PB-020 control surfaces?

Method:

Added `validate_source_manifest_coverage.py` with an explicit 12-manifest-to-lane map. The aggregate `xtask check` now requires every manifest, schema, and validator to appear in the research crosswalk, build-information ledger, PB-020 audit, closure template, and owning lane. This is a no-claim documentation regression control and does not promote any gate.

The validator also verifies that every declared manifest, schema, and validator exists on disk and that the manifest and validator maps have identical coverage.

## 2026-07-19 - Lane source-manifest crosswalk reconciliation

Question:

Do the machine research crosswalk and build-information ledger expose the same lane-specific source manifests, schemas, and validators that the documentation matrix already tracks?

Method:

Compared every source-manifest family against its fresh-host, IPC, sandbox, native/accessibility, profile, package/update, incident, ownership, benchmark, technology, web-platform, and Nova lanes. Added the missing lane entries to the machine crosswalk and readiness ledger and recorded the no-claim boundary in the human ledger. This is traceability and research-control work only; no architecture, platform, dependency, performance, security, or readiness decision changed.

## 2026-07-19 - Reference platform route synchronization

Question:

Does the native-shell continuation route expose the deferred `PB-006` reference-platform scorecard where toolkit, accessibility, benchmark, and fresh-host work will consume it?

Method:

Added the no-claim reference-platform research report, machine scorecard, schema, and validator to the native-shell crosswalk and human lane index. The platform remains unselected and `PB-006` remains deferred; this change only makes the dependency visible and mechanically checked.

## 2026-07-19 - Chrome-class capability route synchronization

Question:

Does the active readiness crosswalk and PB-020 closure evidence expose the Chrome-class capability traceability map as a cross-domain control, rather than leaving it only in the research index and build-information ledger?

Method:

Bound the no-claim capability traceability map to the ownership/PB-020 crosswalk lane, the human lane index, the PB-020 audit, and the closure-review template. Updated the crosswalk count from 227 to 228 resolved evidence paths. This preserves the distinction between capability routing and actual Chrome-class, compatibility, security, accessibility, performance, or production evidence.

## 2026-07-19 - PB-020 source-control inventory synchronization

Question:

Does the top-level documentation-readiness completion audit enumerate the source manifests and validators used by the current build-readiness lanes?

Method:

Compared every checked source-manifest family under `docs/` with the PB-020 audit snapshot and its validator requirements. Added the accessibility, benchmark, IPC, technology/dependency, fresh-host, sandbox, and Nova schema controls to the audit inventory and validator. This strengthens audit coverage only; it does not close any readiness gate or change the 90% contained-M0 / 0% full-build measurements.

## 2026-07-19 - Nova design authority route synchronization

Question:

Does the canonical native-shell lane expose the Nova visual source, schema, and validator wherever `PB-003` through `PB-015` and `TASK-000006` are continued?

Method:

Compared the native-shell crosswalk, build-information ledger, research index, and operating board with the checked design-source manifest. Added the manifest, schema, and validator to the active machine and human handoffs while preserving the boundary that Nova governs visual/layout intent only; Rust shell state, native accessibility, security, and release policy remain authoritative.

## 2026-07-19 - Benchmark source route synchronization

Question:

Does the canonical benchmark lane expose its checked no-claim source observations wherever `PB-013` and `TASK-000005` owners will use them?

Method:

Compared the machine crosswalk and build-information ledger with the benchmark research index and operating board. Added the benchmark source manifest, schema, and validator to the active route and refreshed the evidence-start count. This closes traceability only; it creates no benchmark result, performance claim, or readiness promotion.

## 2026-07-19 - Build-information ledger dependency-route synchronization

Question:

Does the canonical build-information ledger expose the technology/dependency evidence route wherever `PB-002` and `PB-008`/`PB-009` owners will use it?

Method:

Compared the machine ledger's source-strategy and fresh-host `current_evidence` arrays with the active research crosswalk and the operating board. Added the dependency research packet, source manifest, schema, and validator to the relevant machine and human handoffs.

Decision:

The readiness ledger now exposes the same dependency evidence route as the crosswalk, research index, and operating board. Gate status remains unchanged: `PB-002` is blocked, `PB-008`/`PB-009` remain partial, and the project remains 90% organized for contained M0 and 0% closed for the full build.

Next question:

Which owner-reviewed candidate foundation record and independent clean-host evidence will replace these no-claim route entries before broad implementation?

## 2026-07-19 - Research crosswalk count refresh

Question:

Does adding the dependency source record to the active source-strategy and fresh-host lanes leave the human research-coverage audit and readiness snapshot numerically synchronized with the machine crosswalk?

Method:

Ran `validate_research_question_coverage.py` after the crosswalk update. The machine record increased from 213 to 221 resolving evidence-start entries across the same 10 lanes and 37 active questions; updated the human coverage audit and build-readiness snapshot to the machine-derived count.

Decision:

The human and machine crosswalk counts now agree at `221/221`. This is a navigation and count correction only; it does not answer a research question, establish source or dependency approval, promote a gate, or change the 90% contained-M0 / 0% full-build measures.

Next question:

Which future candidate foundation record will replace the no-claim dependency source route after owner review and independent replay evidence exist?

## 2026-07-19 - Dependency evidence crosswalk synchronization

Question:

Does the machine research crosswalk expose the new technology/dependency source record wherever active `RQ-44` and `RQ-46` work routes through source strategy and fresh-host build confidence?

Method:

Compared the dependency packet's related questions with `research-readiness-crosswalk.json`, the human research index, and the source/dependency readiness records. Added the packet, manifest, schema, and validator to the source-strategy and fresh-host evidence-start arrays while preserving `RQ-41` as deferred and `RQ-44`/`RQ-46` as active.

Decision:

The active crosswalk now reaches the same dependency evidence from both relevant lanes. This closes a navigation and traceability gap without answering the research question, selecting a dependency, approving a source, promoting a gate, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

When source-strategy or fresh-host owners review a candidate foundation, which exact candidate record and independent replay evidence will replace the no-claim source observations?

## 2026-07-19 - Technology and dependency source-manifest closure

Question:

Does the deferred technology/dependency research route have the same machine-checkable source identity, freshness, evidence-axis, and unsupported-boundary controls as the active pre-build source lanes?

Method:

Reviewed the `RQ-41` decision packet against the Rust Reference, Cargo Reference, Cargo source-replacement and build-script documentation, SPDX overview/specification, and SLSA levels. Added a no-claim source manifest and schema with retrieval dates, seven official source records, eight evidence axes, source-document links, and explicit selection/approval boundaries, then added a dedicated validator and aggregate-check entry.

Decision:

The deferred technology/dependency route now has machine-checked source provenance and evidence consequences. This improves deep-research continuity and does not select Rust, Cargo, a framework, a dependency, a runtime, a source strategy, a license, or a release foundation; `RQ-41` remains deferred and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which owner-approved candidate foundation and exact feature profile should receive independent unsafe/FFI, clean-host, legal, maintenance, replacement, and performance review, and what evidence will reject it?

## 2026-07-19 - Proposed-lane closure-route scope audit

Question:

Do the proposed benchmark, native UI, profile/session, ownership, package/update, and incident-response task manifests include the closure-preparation records that their readiness handoffs depend on?

Method:

Audited the queue-owned `allowed_paths` for all ten specified manifests against the canonical closure-preparation routes in the readiness board and build-information ledger. Added the missing exact paths for `TASK-000005` through `TASK-000010`, extended the scope validator to enforce all six routes, and recomputed the queue digest across every specified manifest.

Decision:

All ten proposed manifests now declare the closure route needed by their lane, while remaining non-executable and owner-approval-required. This improves task/document coherence without creating execution evidence, approving a task, promoting a gate, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

When any lane is approved, can the retained evidence bundle and changed-file record demonstrate that execution stayed within this synchronized scope and its prohibited-path boundary?

## 2026-07-19 - Specified-task closure-route scope guard

Question:

Can a specified task manifest claim an acceptance route while its declared `allowed_paths` omit the closure records, source manifests, validators, or research-log entries needed to perform that route?

Method:

Audited the queue and all ten specified task manifests after repairing the sandbox scope omission. Compared each manifest's immutable queue fields and digest with its closure-route records, then extended `tools/validate_specified_task_manifests.py` with explicit exact-path coverage for the IPC and sandbox closure routes, including directory-prefix handling for intentionally broad lane scopes.

Decision:

The validator now rejects a specified manifest when the required IPC or sandbox closure-route files are outside its allowed paths. This closes a task-scope integrity gap without approving, executing, or promoting any task, and without changing the 90% contained-M0 / 0% full-build measures.

Next question:

When a task becomes owner-approved, which independently reviewed evidence bundle will prove that the declared scope was sufficient for the actual execution and that no prohibited path was touched?

## 2026-07-19 - Current-host toolchain diagnostic refresh

Question:

Does the documented Windows doctor path still resolve the exact pinned M0 toolchain, and can that observation be kept distinct from independent fresh-host evidence?

Method:

Ran `tools/doctor.ps1 --ci` in the current checkout with an external `CARGO_TARGET_DIR`, then compared the reported identities with `rust-toolchain.toml`, the M0 build foundation, and the fresh-host closure route.

Decision:

The current host reports `rustc 1.97.1 (8bab26f4f 2026-07-14)`, Cargo `1.97.1`, rustfmt `1.9.0-stable`, Clippy `0.1.97`, Python `3.12.10`, and Git `2.52.0.windows.1`; the doctor path completes with `ready for contained M0 development`. Synchronized the fresh-host closure packet with the exact tool identities. This remains same-host diagnostic evidence only: no fresh-host, clean-VM equivalence, independent review, PB-008/PB-009 promotion, or broad-build claim follows.

Next question:

When a reviewed `TASK-000002` manifest exists, which independent host or owner-approved clean-VM run will retain the complete command denominator and environment evidence?

## 2026-07-19 local / 2026-07-20 UTC - Servo upstream freshness refresh

Question:

Did the official Servo repository activity or source identity change after the prior source-strategy freshness capture, and do any changes alter Turing's source-strategy evidence boundary?

Method:

Ran read-only GitHub API queries for `servo/servo` `main`, the latest release, and repository metadata, then compared the response with the source-provenance, security-maintenance, upstream-delta, and ADR-0009 decision-packet records already in the repository.

Decision:

The `main` commit remains `736ad1bda08c1af419aadc903e82938f8610a65d`; the latest release remains immutable `v0.3.0`; and `servo 0.4.0` remains the latest crates.io package. Repository activity timestamps advanced to `2026-07-20T01:44:34Z` (`pushedAt`) and `2026-07-20T02:09:56Z` (`updatedAt`). Updated the canonical source-strategy reports to preserve the new freshness observation. No build, source-equivalence, dependency, license, security, compatibility, performance, or adoption conclusion changed.

Next question:

When `ADR-0009` receives owner authority and a selected baseline, which exact commit/tag/archive should be rebuilt and compared under the accepted equivalence policy?

## 2026-07-19 - Servo mozjs upstream identity refresh

Question:

Does the companion Servo `mozjs` runtime record preserve an exact current head, release identity, and activity boundary independently from the Servo engine repository?

Method:

Ran read-only GitHub API queries for `servo/mozjs` `main`, repository metadata, and the latest release, then compared the result with the upstream-delta packet and the ADR-0009 source-observation manifest.

Decision:

The `mozjs` head remains `f5cbf8aa6076064fd658a1e9fb16147c2347affb`; the repository activity timestamps are `2026-07-19T19:30:00Z` and `2026-07-19T19:30:03Z`; and the latest release is `mozjs-sys-v140.12.0-2` published 2026-07-10. Synchronized the live upstream-delta table and machine source observation. Null API license/security fields remain unresolved metadata, not a license or security conclusion.

Next question:

Which pinned `mozjs` source/package identity, runtime boundary, and license/security evidence will the owner accept if an ADR-0009 option retains SpiderMonkey-related code?

## 2026-07-19 - Command-log environment and scope binding

Question:

Do command-log artifacts identify enough context for an independent reviewer to replay a result without inferring its scope, source commit, or environment?

Method:

Compared the evidence-bundle schema, validator, TASK-000011 review handoff, and agent evidence workflow. The first command-log contract required only a command and exit code; it did not bind each log to a unique command ID, acceptance or negative-test scope, exact source commit, timing, or the captured environment object.

Decision:

Added required validation fields for command logs: unique `command_id`, `scope`, bundle-matching `source_commit`, `started_at`, non-negative `duration_ms`, and `environment_ref` equal to `bundle.environment`. The schema and review handoff now describe the same contract.

Impact:

Future independent evidence bundles can be reviewed as a set of explicit command records rather than unscoped hashes. This does not create a command log, accept TASK-000011, promote PB-011, or change the 90% contained-M0 / 0% full-build measures.

Next question:

Which retained-log path and artifact-package convention should the first independent reviewer use for command logs outside the repository tree?

## 2026-07-19 - Evidence-bundle command-artifact control

Question:

Does the evidence-bundle schema enforce the review handoff requirement that real decisions retain hashed command artifacts or logs tied to the exact source commit?

Method:

Compared `evidence-bundle.schema.json`, `validate_evidence_bundles.py`, the checked TASK-000011 no-claim capture, and its review handoff. The existing validator verified source-file hashes and reviewer separation but allowed future accepted, rejected, or needs-changes bundles to contain no command artifact, even though the handoff required command-output evidence.

Decision:

Added the `command_log` artifact type with a command and integer exit code, made limitations required in the schema, rejected duplicate artifacts, and required at least one command log for real review decisions. The historical no-claim capture remains valid only through its explicit retained-log limitation.

Impact:

Future evidence cannot be accepted from source-file presence or external CI links alone; command output must be retained and hashed. This strengthens review traceability without accepting TASK-000011, changing its status, promoting PB-011, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

Which command-log fields should bind tool version, environment identity, and artifact retention path for the first independent review bundle?

## 2026-07-19 - Cross-lane readiness-template control

Question:

Do the eleven no-claim ADR, lane-readiness, and PB-020 closure templates preserve the same review-control spine, or can template drift hide missing evidence paths, owner-review fields, or accidentally enabled decision flags?

Method:

Compared the shared fields in the ADR-0009 decision-review template, nine lane readiness-review templates, and PB-020 closure-review template with their schemas and focused validators. The fresh-host template also contained a duplicated `tools/check.ps1` source record, which was removed as part of this invariant.

Decision:

Added `validate_readiness_review_templates.py` to enforce eleven-template discovery, identity/status/date, no-claim status, source-record existence and uniqueness, review scope, owner-review axes, rejection and unsupported-boundary records, validation commands, non-empty evidence axes, and all-false decision flags. Wired it into the locked `xtask check` path and documentation-readiness records.

Impact:

Review templates are now structurally consistent and cannot silently enable a readiness or authority flag. This improves handoff integrity only; it does not create owner review, independent review, accepted evidence, gate closure, task approval, or a change to the 90% contained-M0 / 0% full-build measures.

Next question:

Which shared evidence-bundle fields should be machine-checked against the review-template identity and exact source commit before a real owner decision is recorded?

## 2026-07-19 - Cross-lane source-manifest freshness control

Question:

Do the eleven lane source-observation manifests share machine-enforced freshness and identity rules, or can a valid focused validator still accept stale, duplicate, or missing provenance metadata?

Method:

Inspected the accessibility, ADR-0009, benchmark, fresh-host, IPC, ownership, package/update, incident-response, sandbox, profile/session, and web-platform manifests and their focused validators. The lane validators checked their own schemas and source-document links, but no aggregate invariant covered ISO dates, retrieval/update ordering, duplicate source IDs, consequence fields, or all source-document targets.

Decision:

Added `validate_source_manifest_metadata.py` and wired it into the locked `xtask check` path and documentation-readiness validation commands. The design-source manifest remains outside this rule because it is a single-artifact visual hash contract rather than a source-observation list.

Impact:

Source-observation provenance now has a shared freshness and identity guard across all eleven manifests. This improves documentation continuity only; it does not select a source strategy, approve a dependency, close a readiness gate, establish platform evidence, or change the 90% contained-M0 / 0% full-build measures.

Next question:

Which shared closure-record fields should receive the next cross-lane invariant without replacing owner-controlled review?

## 2026-07-19 - TASK-000011 evidence-baseline recapture control

Question:

Does the `TASK-000011` review handoff distinguish its historical no-claim evidence capture from the current repository head before independent review?

Method:

Compared the task manifest, review handoff, checked no-claim evidence bundle, evidence-bundle validator, and current `main` commit. The bundle is correctly immutable and bound to source commit `4590aad94f298d380d43bffc7b9a5cb618beccac`, but the handoff did not state the current audited head or require recapture after later commits.

Decision:

Recorded current head `12922b46165d8d941e0dc504148196f4497d8e91` in the review handoff and added an explicit rule requiring a new exact-commit evidence bundle before independent acceptance. The historical no-claim bundle remains unchanged and `TASK-000011` remains `review_pending`.

Impact:

The handoff now prevents stale candidate evidence from being mistaken for current acceptance evidence. This does not accept the task, promote `PB-011`, establish production IPC, or change the 90% contained-M0 / 0% full-build measures.

Next question:

Which reviewer-controlled environment and command artifacts will be captured against the exact commit selected for `TASK-000011` review?

## 2026-07-19 - Reference-platform scorecard provenance control

Question:

Does the deferred PB-006 reference-platform scorecard enforce the same unique-document provenance rule as the source-strategy and lane-specific source manifests?

Method:

Compared the Windows, macOS, and Linux candidate scorecard, its eleven source records and evidence dimensions, schema, validator, and dependent native/toolchain/sandbox/benchmark/release routes. Its `source_documents` list was unique but duplicate paths were not rejected.

Decision:

Added `uniqueItems` to the reference-platform scorecard schema and made `validate_reference_platform_scorecard.py` reject duplicate paths.

Impact:

This completes provenance controls for the platform-selection record without selecting a platform, authorizing native UI work, or creating support, accessibility, security, performance, packaging, release, or implementation evidence. `PB-006` remains `not_selected` and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which reference-platform candidate should receive the first owner-approved clean-host and native workflow evidence package when M1 scope is authorized?

## 2026-07-19 - ADR-0009 source-observation provenance control

Question:

Does the primary ADR-0009 source-observation manifest enforce the same unique-document provenance rule as every other source manifest in the repository?

Method:

Audited all schema files containing `source_documents` and their focused validators. ADR-0009 was the final source-observation manifest without a schema uniqueness constraint or validator rejection for duplicate paths; the reference-platform scorecard was excluded because it does not contain a source-document provenance array.

Decision:

Added `uniqueItems` to the ADR-0009 source-observation schema and made `validate_adr_0009_source_observations.py` reject duplicate paths.

Impact:

The source-strategy provenance family is now consistent and machine-enforced. This does not select Servo or any other source, approve dependencies, establish equivalence, or change `PB-002`, `ADR9-EV-018`, or the 90% contained-M0 / 0% full-build measures.

Next question:

Which freshness and selected-baseline identity fields must be bound together when a real ADR-0009 decision-review record replaces the no-claim template?

## 2026-07-19 - Source-manifest provenance invariant completed

Question:

Do all machine source manifests that track `source_documents` enforce the same unique-path provenance rule?

Method:

Audited all repository `*-source-manifest.schema.json` files and their focused validators after applying the rule to web-platform, sandbox, profile/session, and package/update lanes. Six remaining lanes lacked the schema and validator guard: accessibility, benchmark, IPC wire, fresh-host toolchain, incident response, and ownership control.

Decision:

Added `uniqueItems` to each remaining schema and duplicate-path rejection to each focused validator. The design-source manifest is not included because it has no `source_documents` array and uses a different single-artifact manifest contract.

Impact:

All source-manifest provenance lists now have a consistent machine-enforced uniqueness rule. This improves traceability only; it does not create accessibility, benchmark, IPC, fresh-host, incident-response, ownership, security, release, or implementation evidence, and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which source-manifest field should next receive a cross-lane invariant: freshness/expiry identity, or explicit source-document ownership and regeneration policy?

## 2026-07-19 - Package/update source manifest provenance control

Question:

Does the package/update source manifest enforce the same one-entry-per-document provenance rule as the compatibility, sandbox, and profile/session lanes?

Method:

Compared the package/update manifest, schema, validator, eleven-source identity set, eight evidence axes, and release-safety closure route. The source list was unique but duplicate document paths were not rejected by the schema or validator.

Decision:

Added `uniqueItems` to the package/update `source_documents` schema and made `validate_package_update_sources.py` reject duplicate paths.

Impact:

This synchronizes release-safety provenance controls without selecting a package format, updater, signing hierarchy, channel, rollback policy, or release authority. `PB-017` remains partial and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which fake-key, local-only package/update lab record will first satisfy the installation, rollback, migration, privacy, cleanup, and independent-review evidence sequence?

## 2026-07-19 - Profile/session source manifest provenance control

Question:

Does the profile/session source manifest enforce the same one-entry-per-document provenance rule as the web-platform and sandbox source manifests?

Method:

Compared the profile/session source manifest, schema, validator, required source set, nine evidence axes, and the execution/data-safety closure route. The source list was unique but duplicate document paths were not rejected by the schema or validator.

Decision:

Added `uniqueItems` to the profile/session `source_documents` schema and made `validate_profile_session_sources.py` reject duplicate paths.

Impact:

This synchronizes provenance controls for the data-safety lane without creating executable schemas, migration or fault evidence, privacy approval, credential readiness, data-loss safety, or production profile-format evidence. `PB-016` remains partial and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which synthetic profile/session schema package and fault-injection record will first satisfy the execution/data-safety closure route after task authority is approved?

## 2026-07-19 - Sandbox source manifest provenance control

Question:

Does the sandbox platform-source manifest enforce the same one-entry-per-document provenance rule as the web-platform source manifest?

Method:

Compared the sandbox manifest, schema, validator, required platform/source set, and no-claim evidence boundary with the corrected web-platform source controls. The sandbox source list was unique but its schema and validator did not prevent future duplicate paths.

Decision:

Added `uniqueItems` to the sandbox `source_documents` schema and made `validate_sandbox_platform_sources.py` reject duplicate paths.

Impact:

This synchronizes provenance controls for the security lane without creating effective-policy capture, packaged probe execution, sandbox readiness, renderer-security, hostile-browsing, or implementation evidence. `PB-012` remains partial and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which packaged expected-deny probe evidence will demonstrate effective policy on each selected platform after the sandbox task and host controls are approved?

## 2026-07-19 - Web-platform source manifest duplicate-path control

Question:

Can the web-platform source manifest provide a trustworthy one-entry-per-document provenance list for compatibility and conformance research?

Method:

Inspected the manifest, schema, validator, and linked web-platform research route. The manifest listed the ADR-0009 source-strategy closure packet twice, while neither the schema nor validator rejected duplicate document paths.

Decision:

Removed the duplicate path, added `uniqueItems` to the machine schema, and made `validate_web_platform_sources.py` reject duplicate `source_documents` entries.

Impact:

This closes a traceability and provenance defect without changing any source observation, compatibility result, standards revision, gate status, implementation authority, or the 90% contained-M0 / 0% full-build measures.

Next question:

When a compatibility profile is authorized, which reviewed capability-row manifest will bind its exact standards, test, harness, denominator, and unsupported-case identities?

## 2026-07-19 - Extreme-performance definition centralized

Question:

Can the Chrome-competitor and extreme-performance objective be interpreted consistently across the canonical Blueprint, detailed performance book, and benchmark readiness lane?

Method:

Compared the performance dimensions, 30-tab contract, benchmark readiness lane, Chrome-class runbook, claim-expiry rules, and capability traceability map. The documents required the same evidence in practice but did not state one canonical definition for the phrase "extreme performance."

Decision:

Added a canonical Blueprint 09 definition covering latency tails, frame pacing, memory/resource attribution, energy/thermal behavior, 30-tab pressure, recovery, and preserved security, compatibility, accessibility, and failure visibility. Linked the detailed performance book and benchmark lane to that definition.

Impact:

This removes a terminology and status-drift risk without creating a benchmark result, changing `PB-013`, authorizing a claim, or changing the 90% contained-M0 / 0% full-build measures. A single benchmark score remains insufficient by policy.

Next question:

Which fixed-tier workload and competitor evidence package can satisfy the definition after the benchmark runner and owner gates are authorized?

## 2026-07-19 - Nova visual authority added to the canonical-owner map

Question:

Can a new maintainer identify the Nova artifact as the browser-face visual/layout authority without treating the React design lab as trusted runtime behavior or a toolkit decision?

Method:

Compared the documentation-policy source-of-truth table with the Nova design-lab README, design-source manifest, native build-entry criteria, UI runtime book, and current build-readiness stop/resume records.

Decision:

Added separate canonical-owner rows for Nova visual/layout composition and trusted-chrome runtime, page-surface, accessibility, and behavior. The policy now records the authority boundary directly where contributors look for source ownership.

Impact:

This closes an authority-map ambiguity without changing Nova's source hash, selecting a toolkit, authorizing native UI implementation, or changing the 90% contained-M0 / 0% full-build measures. React remains design-lab-only, and accepted UI contracts and ADRs remain behavior-authoritative.

Next question:

Which reviewed extraction manifest and native fixture package will first translate the Nova source into toolkit-neutral contracts after UI implementation is authorized?

## 2026-07-19 - Servo performance capture freshness boundary

Question:

Can the Servo performance preparation packet be used without confusing its dated host and debug-artifact observations with current upstream or benchmark evidence?

Method:

Reviewed the packet's capture date, external checkout identity, reference-host wording, artifact hash, and explicit no-run statement against the later upstream refresh and source-provenance reports.

Decision:

Added a capture-time freshness boundary and a rerun rule tied to source commit, build profile, host configuration, and runner identity. The packet now links the current upstream identity reports instead of leaving “current host” and inspected commit open to temporal ambiguity.

Impact:

This improves `ADR9-EV-014` and `PB-013` evidence handoff clarity without producing performance, memory, energy, speed, benchmark, or comparison claims. `PB-002` remains blocked and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which owner-reviewed host and runner controls must be accepted before the first decision-grade performance run?

## 2026-07-19 - Benchmark competitor capture freshness boundaries

Question:

Can local competitor executable and browser-pin diagnostics remain clearly separated from current vendor catalogs and future benchmark-ready pins?

Method:

Compared the 2026-07-17 local-install inventory and 2026-07-18 Chrome/Edge diagnostic capture with the 2026-07-19 release-catalog manifest. The reports already separated catalog, local executable, and diagnostic evidence, but “current host” wording did not explicitly state the capture-time boundary.

Decision:

Added freshness boundaries to both local reports. They now require rerunning local inventory and browser-reported diagnostics, together with the release catalog, before owner-reviewed benchmark comparison use.

Impact:

This improves `PB-013` handoff clarity without creating browser pins, benchmark results, competitor comparisons, or performance claims. `PB-013` remains `documented_no_runner`, and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which future benchmark artifact classes need the same capture identity and expiry fields before the browser launch runner exists?

## 2026-07-19 - Source equivalence and build replay freshness alignment

Question:

Can the remaining ADR-0009 source-equivalence and build-reproduction packets prevent historical `main` and toolchain observations from being reused as current evidence?

Method:

Compared the 2026-07-17 source-baseline equivalence policy and same-host build-reproduction report with the later upstream refresh and provenance records. Both reports retained valid capture-time evidence but lacked a direct freshness boundary and newer-baseline rerun instruction.

Decision:

Added explicit historical-capture boundaries and links to the current refresh route. The reports now require a new equivalence or reproduction run whenever a later source baseline is selected.

Impact:

This completes the freshness alignment across the ADR-0009 source-strategy evidence chain without changing any source, dependency, build, compatibility, performance, security, or release decision. `PB-002` remains blocked and the 90% contained-M0 / 0% full-build measures remain unchanged.

Next question:

Which benchmark competitor catalogs and host inventories need the same capture-date refresh discipline before they can support future comparison planning?

## 2026-07-19 - ADR-0009 historical packet freshness alignment

Question:

Do the remaining dated Servo source-strategy packets clearly distinguish capture-time upstream values from the later 2026-07-19 refresh?

Method:

Scanned the 2026-07-17 source-archive provenance audit and source-strategy inventory after the independent source-verification freshness correction. Both retained valid historical observations but lacked an explicit route to the later official refresh packet.

Decision:

Added freshness boundaries and links to the later upstream refresh/provenance reports. The older source, release, package, and local-artifact observations remain unchanged and remain historical evidence for ADR-0009.

Impact:

This makes the source-strategy evidence set internally coherent across capture dates. It does not select a source baseline, change `PB-002`, approve a dependency, or change the 90% contained-M0 / 0% full-build measures.

Next question:

Which non-Servo external research packets contain similarly time-sensitive “latest” observations that need a dated refresh route before owner review?

## 2026-07-19 - Historical source-verification freshness boundary

Question:

Could a dated independent Servo source-verification report be mistaken for the current upstream state after a later metadata refresh?

Method:

Compared the 2026-07-17 non-shallow source-verification report with the 2026-07-19 official upstream refresh and provenance packets. The older report's object, ancestry, tree, and file-count observations remain valid for its capture date, but several headings used `current main` without an explicit historical qualifier.

Decision:

Added a freshness boundary to the independent source-verification report, labeled its `main` comparisons as the 2026-07-17 snapshot, and linked the later refresh/provenance packets as the route for current upstream observations.

Impact:

This prevents stale upstream evidence from being reused as current source-strategy evidence. It does not select a source baseline, change `PB-002`, approve Servo or `mozjs`, or change the 90% contained-M0 / 0% full-build measures.

Next question:

Which other dated external-evidence reports should receive explicit freshness labels before their observations are reused in an owner decision?

## 2026-07-19 - Documentation percentage drift control

Question:

Can the narrative documentation-readiness audit and one-screen progress snapshot remain synchronized with the machine completion registry?

Method:

Reviewed `documentation-readiness-completion-audit.json`, `documentation-readiness-completion-audit-2026-07.md`, and `22-build-readiness-progress-snapshot.md`, then ran the focused completion-audit validator on 2026-07-19. The snapshot already checked machine-derived distributions; the narrative audit percentage sentence was not independently checked.

Decision:

Extended `validate_documentation_readiness_completion_audit.py` to validate the narrative audit's contained-M0 and full-build percentage statements against the machine criterion counts. The existing no-claim status and closure boundary remain authoritative.

Impact:

This adds a second human/machine drift control for the readiness percentage surfaces. It does not change the 90% contained-M0 or 0% full-build measures, promote `PB-020`, approve a task, or authorize broad implementation.

Next question:

Which remaining human gate summaries should be linked to machine-derived values before a real owner decision changes the readiness state?

## 2026-07-19 - Research-question coverage drift control

Question:

Can the human research-question coverage audit remain synchronized with the machine crosswalk as evidence routes are added?

Method:

Compared `docs/research/research-question-coverage-audit-2026-07.md` with `research-readiness-crosswalk.json` and ran `validate_research_question_coverage.py` on 2026-07-19. The machine crosswalk resolved 213 evidence-start entries while the human audit still recorded 207.

Decision:

Corrected the human audit to the current 213-entry count and added a validator assertion that the active-question, lane, and evidence-entry sentence in the human audit matches the machine-derived values.

Impact:

This closes a documentation-drift defect and improves continuation reliability. It does not answer a research question, promote a readiness gate, approve a task, or change the 90% contained-M0 / 0% full-build closure measures.

Next question:

Which remaining human status or closure statements should be machine-linked next so that owner-decision and readiness percentages cannot drift from their registries?

## 2026-07-19 - Sustained performance policy research

Question:

Which scheduling, memory, cache, lifecycle, and energy policies should be compared before Turing can make a sustained-performance claim across interactive, multi-tab, constrained-resource, and recovery workloads?

Method:

Checked Chromium's threading/task and Blink scheduling notes, Chrome's Page Lifecycle guidance, Linux Pressure Stall Information documentation, and Microsoft's Windows Performance Recorder guidance on 2026-07-19. Reconciled the observations with `RQ-23`, `PB-013`, `TASK-000005`, the benchmark-lab and performance books, the 30-tab, trace, resource-attribution, statistics, and claim-review contracts, and the research-readiness crosswalk.

Decision:

Added an active no-claim packet that separates scheduler, memory, cache, lifecycle, energy, thermal, and isolation-adjusted policy candidates; defines pressure, freeze/discard/revival, crash/recovery, accessibility, agent, and sustained-run scenarios; and records raw-artifact, failure-denominator, observer-effect, and rejection requirements. Added the packet to the RQ-23 Blueprint route, benchmark crosswalk, research index, and repository map.

Impact:

`RQ-23` now has a dedicated source-backed policy route. `PB-013` remains `partial` and `TASK-000005` remains proposed-only. No scheduler, allocator, cache, lifecycle, energy, performance, compatibility, security, accessibility, production, or Chrome-class claim changed.

Next question:

Which first candidate policy set should an owner approve for the L1 browser-run extension, and what exact pressure/recovery artifact schema should reject incomplete evidence?

## 2026-07-19 - Research packet navigation synchronization

Question:

Do the latest research packets appear in every canonical discovery and build-readiness route required by the documentation policy?

Method:

Compared the top-level documentation index, start-here continuation, research index, repository map, Blueprint research program, research-readiness crosswalk, and documentation-readiness evidence matrix for the recent `RQ-08`, `RQ-13`/`RQ-22`/`RQ-36`, `RQ-23`, `RQ-41`, `RQ-45`, `RQ-47`, and `RQ-48` packets.

Decision:

Added missing top-level index rows and connected the sustained-performance route to the start-here continuation and documentation-readiness evidence matrix. The source packets, research index, repository map, Blueprint routes, and machine crosswalk remain the authority for status and evidence ordering.

Impact:

Recent research additions now have explicit discovery and build-readiness navigation from the top-level docs. No research question, readiness gate, implementation status, owner decision, or claim boundary changed.

## 2026-07-19 - Benchmark owner-handoff synchronization

Question:

Does the owner-decision board, machine synchronization matrix, and final build-readiness collection manifest require the sustained-performance policy route before benchmark closure review?

Method:

Compared the `PB-013` row in the owner-decision closure board, `OWNER-SYNC-06` in the machine synchronization matrix, the benchmark evidence matrix, and the build-readiness closure-preparation collection manifest.

Decision:

Added the sustained-performance policy route to each benchmark owner-handoff surface. The route remains no-claim and policy-comparative; browser-run evidence, owner review, benchmark readiness, and performance claims remain separate requirements.

Impact:

The benchmark closure handoff now consistently requires scheduler, memory, cache, lifecycle, pressure, energy, thermal, recovery, and isolation-adjusted policy coverage before benchmark claim review. No gate, task, implementation status, or claim changed.

## 2026-07-19 - Nova task-handoff synchronization

Question:

Does the specified native UI task carry the Nova visual source's authority boundary and build-entry evidence into its task-scoped file boundary?

Method:

Compared the Nova Native Build Entry Criteria, surface-contract map, design-source manifest and validator, UI runtime book, `TASK-000006` specified manifest, proposed task queue row, native UI readiness template, and `PB-020` documentation/readiness records.

Decision:

Added the Nova entry criteria, surface-contract map, and design-source manifest to the immutable `TASK-000006` allowed paths and mirrored queue record. Added explicit task preconditions and acceptance criteria requiring source identity, extraction traceability, semantic tokens, native fixture mapping, and visual comparison evidence while preserving the rule that Nova is visual/layout input only. Refreshed the specified-manifest source queue digest.

Impact:

The native UI task handoff now carries the same Nova authority boundary as the UI runtime and readiness documents. `TASK-000006` remains specified/proposed and non-executable; no toolkit, native adapter, accessibility, page-surface, UI-gate, implementation, or production decision changed.

## 2026-07-19 - Progress snapshot crosswalk-count correction

Question:

Does the one-screen build-readiness snapshot report the current machine-validated research crosswalk denominator?

Method:

Compared `docs/project-buildout/22-build-readiness-progress-snapshot.md` with the current `validate_research_question_coverage.py` output and `research-readiness-crosswalk.json` after the Nova task-handoff synchronization.

Decision:

Corrected the snapshot from `207/207` to `213/213` resolved crosswalk evidence paths. The active-question denominator remains `37/37`, and the machine audit remains the authority for the 90% contained-M0 and 0% full-build measures.

Impact:

The one-screen continuation document no longer understates the current evidence-route denominator. No question, gate, task, readiness state, implementation status, or claim boundary changed.

## 2026-07-19 - Sustained-performance route added to continuation surfaces

Question:

Do the start guide, progress snapshot, and operating board all direct maintainers to the dedicated `RQ-23` policy route before benchmark execution and claim review?

Method:

Compared the sustained-performance packet, research index, Blueprint `RQ-23` route, benchmark owner board, benchmark evidence matrix, start guide, progress snapshot, and operating board.

Decision:

Added the sustained-performance policy packet to the start guide, progress snapshot, and `PB-013` operating-board evidence route. The sequence now explicitly distinguishes policy comparison from browser-run evidence, statistics review, and public claims.

Impact:

Benchmark continuation surfaces now agree on the full `RQ-23` handoff. No benchmark result, owner decision, task approval, readiness promotion, performance claim, or Chrome-class claim changed.

## 2026-07-19 - Bounded API and protocol contract research

Question:

Which API and protocol conventions minimize misuse, authority leakage, resource exhaustion, and long-term compatibility cost while supporting bounded encodings, streaming, cancellation, diagnostics, and generated clients?

Method:

Checked JSON Schema 2020-12, RFC 9457 Problem Details, the W3C WebDriver BiDi working draft, and Protocol Buffers schema/encoding documentation on 2026-07-19. Reconciled the observations with `RQ-13`, `RQ-22`, `RQ-36`, `PB-011`, `PB-020`, the IPC capability boundary, IPC wire-encoding preparation, API/developer-experience books, security controls, and the research-readiness crosswalk.

Decision:

Added an active no-claim packet separating schema, identity, authority, resource, lifecycle, transport, semantics, compatibility, generated-client, and evidence layers. It defines candidate-domain boundaries, negative/failure/recovery cases, compatibility and provenance requirements, and rejection rules. Added the packet to the IPC crosswalk evidence start. No encoding, transport, schema, public protocol, IPC, security, performance, or production decision changed.

Next question:

Which owner-approved domain should receive the first generated schema and real-transport negative-test trial, and which resource, authority, or compatibility failure must reject the candidate?

## 2026-07-19 - Project controls and review system research

Question:

Which ownership, review, traceability, phase, exception, and evidence controls reduce defects without blocking legitimate work or allowing unsafe shortcuts?

Method:

Checked NIST SP 800-218 SSDF lifecycle practices, NASA technical-management and configuration-management guidance, and GitHub protected-branch, ruleset, and code-owner controls on 2026-07-19. Reconciled the observations with `RQ-45`, `RQ-47`, `RQ-48`, `RQ-60`, `PB-019`, `PB-020`, the professional owner/review/exception/phase registries, task authority controls, traceability route, and documentation policy.

Decision:

Added an active no-claim packet defining authority, scope, baseline, verification, review, exception, gate, recovery, and bypass controls; phase states; adversarial control fixtures; and false-block/missed-block measurements. Added the packet to the ownership/review-capacity crosswalk evidence start. No governance, task-authority, reviewer, gate, release, security, or production decision changed.

Next question:

Which first adversarial control trial should test a proposed task, review, exception, and gate-promotion path, and what failure must prevent the system from advancing?

## 2026-07-19 - Traceability at browser scale research

Question:

Can requirement-to-evidence records remain accurate, bidirectional, reviewable, and useful as Turing grows from a documented prototype into a multi-process browser with standards, platform, security, accessibility, performance, release, and support obligations?

Method:

Checked NASA systems-engineering guidance on bidirectional traceability, requirements rationale, impact analysis, verification matrices, and configuration/change control, plus NIST SP 800-218 SSDF lifecycle evidence on 2026-07-19. Reconciled the observations with `RQ-47`, `RQ-44`, `RQ-46`, `RQ-48`, `RQ-60`, `PB-002`, `PB-008`, `PB-009`, `PB-019`, `PB-020`, the professional traceability registry, requirement verification matrix, crosswalk, and documentation policy.

Decision:

Added an active no-claim packet defining a typed graph model, bidirectional edge types, status/freshness rules, invalidation triggers, browser identity boundaries, generated-view controls, change-impact traversal, adversarial fixtures, and rejection/promotion rules. Added the packet to the source-strategy, fresh-host, and ownership crosswalk evidence starts. No coverage, implementation, verification, readiness, release, or support decision changed.

Next question:

Which first executable traceability audit should independently sample the source-strategy, fresh-host, and ownership lanes, and what findings must block a task or claim rather than merely create a warning?

## 2026-07-19 - Capacity and sustainability research

Question:

What staffing, funding, infrastructure, review capacity, and support capacity are required at each maturity for an independent browser to remain secure, compatible, accessible, performant, diagnosable, and maintainable?

Method:

Checked NIST SP 800-218 SSDF 1.1 and the Google SRE material on service-level objectives, error budgets, production operations, and ownership/automation on 2026-07-19. Reconciled the observations with `RQ-48`, `RQ-25`, `RQ-31`, `RQ-45`, `RQ-47`, `RQ-60`, `RQ-62`, `RQ-66`, the staffing and capacity plan, SLO research, incident-response, ownership, production-readiness, and research-question coverage records.

Decision:

Added an active no-claim packet that treats capacity as role coverage, qualified backups, review and incident bandwidth, infrastructure, evidence throughput, funding, support scope, and maturity-specific promotion gates. It defines browser-specific recurring workload, SLO/error-budget evidence, rejection rules, and the requirement to reduce scope when maintenance capacity is exceeded. No staff, funding, SLO, support, release, security, performance, or production decision changed.

Next question:

What finite first-build scope can the named owners and qualified backups actually maintain through security response, compatibility, accessibility, performance measurement, update recovery, and incident rehearsal?

## 2026-07-19 - Technology and dependency decision research

Question:

Which languages, frameworks, and foundational dependencies minimize total security, performance, build, license, and maintenance cost for an independent browser while preserving replaceability and reproducibility?

Method:

Checked the Rust Reference's unsafe and undefined-behavior boundaries, the Cargo Reference's dependency, source-replacement, workspace, registry, and build-script model, and SPDX 3.0.1 licensing/SBOM metadata on 2026-07-19. Reconciled the observations with `RQ-41`, `RQ-44`, `RQ-46`, `ADR-0009`, `PB-002`, `PB-008`, `PB-009`, `PB-020`, and the research-question coverage registry.

Decision:

Added a deferred no-claim packet that separates language safety from unsafe escape hatches, dependency resolution from provenance, SPDX identification from legal approval, and local build success from reproducibility. It defines candidate foundation classes, evidence fields, measurements, rejection rules, and owner-review promotion conditions. No language, framework, dependency, source strategy, license, security, performance, or release decision changed.

Next question:

Which owner-approved candidate foundation and exact feature profile should receive the first independent source, dependency, unsafe/FFI, clean-host, legal, maintenance, and replacement review?

## 2026-07-19 - JavaScript and DOM wrapper lifetime research

Question:

Which JavaScript heap representation and DOM-wrapper strategy preserves reachability, identity, teardown, cross-boundary safety, and memory accountability without unacceptable tracing or indirection cost?

Method:

Checked the current ECMAScript WeakRef/liveness model, V8's JS-to-DOM tracing documentation, Oilpan library and pointer-compression documentation, and Chromium's Blink memory-management overview on 2026-07-19. Reconciled the observations with `RQ-08`, the JavaScript, DOM, storage, memory, security, accessibility, and quality books, and the research-question coverage registry.

Decision:

Added a deferred no-claim packet separating JS wrappers, native DOM ownership, cross-heap roots/edges, weak/ephemeron behavior, external resources, teardown, pointer compression, and allocator classes. It defines identity, cycle, stale-wrapper, crash/restart, memory, and safety evidence and rejects finalizer timing, one-heap totals, untracked native resources, or unreviewed pointer compression as proof. No heap, wrapper, collector, memory, security, performance, or readiness decision changed.

Next question:

Which owner-approved wrapper identity and root/edge schema should become the first cross-heap lifetime, teardown, restart, and independent safety-review target when this lane enters the active pre-build crosswalk?

## 2026-07-19 - JavaScript bytecode representation research

Question:

Should the first JavaScript interpreter use register, stack, or hybrid bytecode, and what format can support semantics, debugging, exceptions, GC, baseline compilation, versioning, and resource limits without excessive size or dispatch cost?

Method:

Checked V8 Ignition, V8 documentation, V8 background-compilation and interpreter/compiler material, and the WebAssembly 3.0 execution and abstract-machine specification on 2026-07-19. Reconciled the observations with `RQ-07`, the JavaScript runtime, compiler, debugging, memory, security, and quality books, and the research-question coverage registry.

Decision:

Added a deferred no-claim packet separating stack, register, hybrid, and semantic-reference formats. It defines bytecode identity, exceptions, async/generators, source locations, GC maps, baseline lowering, validation, malformed input, versioning, cache, and workload evidence, and rejects treating V8 or WebAssembly formats as a JavaScript standard. No bytecode, interpreter, compiler, JIT, memory, performance, or readiness decision changed.

Next question:

Which owner-approved semantic instruction inventory and reference interpreter should become the first conformance, debug/exception/GC-map, and independent-format review target when this lane enters the active pre-build crosswalk?

## 2026-07-19 - Text shaping, fonts, and input research

Question:

Which text stack balances Unicode correctness, shaping quality, font fallback, raster and platform consistency, accessibility, IME behavior, memory, and performance across supported platforms?

Method:

Checked Unicode UAX #9 and UAX #14, W3C CSS Text Module Level 3, the HarfBuzz manual and shaping API documentation, and ICU documentation on 2026-07-19. Reconciled the observations with `RQ-06`, the text/font, web-engine, accessibility, native-platform, input, security, and performance books, and the research-question coverage registry.

Decision:

Added a deferred no-claim packet separating Unicode data, bidi, line breaking, shaping, font selection/fallback, metrics, rasterization, IME, and accessibility boundaries. It defines multilingual corpus fields, cluster/caret and semantic oracles, font and platform provenance, input workflows, resource measurements, and rejection rules for Latin-only testing or treating a shaping library as a complete text stack. No text stack, font policy, raster policy, IME, accessibility, compatibility, performance, or readiness decision changed.

Next question:

Which owner-approved Unicode/font/IME corpus and version manifest should become the first shaping, line-break, fallback, accessibility, and platform-input review target when this lane enters the active pre-build crosswalk?

## 2026-07-19 - JavaScript runtime tiering and collector research

Question:

Which runtime tiering and collector architecture gives the best interaction-adjusted performance without sacrificing JavaScript semantics, predictable memory behavior, security boundaries, or reproducible evidence?

Method:

Checked the current ECMAScript specification, V8's public Sparkplug, Liftoff, and dynamic-tiering documentation, and the Bytecode Alliance Wasmtime project description for Cranelift's bounded code-generation role on 2026-07-19. Reconciled the observations with `RQ-19`, the JavaScript runtime, performance, memory, security, testing, and source-strategy books, and the research-question coverage registry.

Decision:

Added a deferred no-claim packet separating ECMAScript semantics from interpreter, baseline, optimizing, collector, code-cache, and executable-memory choices. It defines cold/warm/interactive measurement, GC and external-memory accounting, no-JIT and deoptimization oracles, security and provenance evidence, and rejection rules for peak-only benchmarks, finalization timing, hidden background work, or unreviewed backend adoption. No runtime, JIT, collector, memory, security, performance, or readiness decision changed.

Next question:

Which owner-approved semantic baseline and no-JIT measurement manifest should become the first runtime conformance and independent-review target when this lane enters the active pre-build crosswalk?

## 2026-07-19 - Rendering artifacts and invalidation research

Question:

Which pipeline artifact and invalidation model is most correct, compact, and observable across parser, style, layout, paint, accessibility, and compositor stages?

Method:

Checked the WHATWG DOM Living Standard updated 2026-07-18, W3C CSS Containment Level 1, and Chromium's public rendering critical-path and rendering-architecture documentation on 2026-07-19. Reconciled the observations with `RQ-18`, the web-engine, performance, accessibility, security, and testing books, artifact identity rules, and the research-question coverage registry.

Decision:

Added a deferred no-claim packet separating standards-visible mutation and containment semantics from engine-specific artifact choices. It defines mutable, immutable-epoch, hybrid, and full-recomputation models; invalidation classes; pixel, accessibility, hit-test, focus, script, and recovery oracles; measurement fields; and rejection rules for stale output, screenshot-only validation, hidden failures, or copying another engine's pipeline as a decision. No artifact model, invalidation policy, compositor design, compatibility, accessibility, performance, or readiness decision changed.

Next question:

Which owner-approved artifact identity/dependency schema and synthetic mutation corpus should become the first full-recomputation and independent-review target when web-engine pipeline work enters the active pre-build crosswalk?

## 2026-07-19 - Public developer protocol stability and observability research

Question:

What public developer protocol can lead on stability and observability without creating an ambient-control, privacy, compatibility, or maintenance liability?

Method:

Checked the W3C WebDriver BiDi Working Draft published 2026-06-01, the official ChromeDevTools `devtools-protocol` repository, and Chrome's Protocol Monitor documentation on 2026-07-19. Reconciled the observations with `RQ-17`, the API-design and developer-experience books, agent authority rules, IPC and security boundaries, accessibility evidence requirements, protocol versioning requirements, and independent-verification controls.

Decision:

Added a deferred no-claim packet separating standards-facing automation, diagnostic observability, capability-scoped local integrations and agents, and private test seams. It defines wire, semantic, observability, and lifecycle compatibility axes; authority, redaction, identity, budget, ordering, cancellation, reconnect, and version-skew evidence; and rejection rules for treating schemas, generated clients, drafts, or self-review as compatibility or security proof. No protocol, transport, public API, compatibility promise, automation authority, security, accessibility, performance, or release decision changed.

Next question:

Which owner-approved protocol inventory and threat-model packet should become the first synthetic conformance and independent-review target once developer-protocol work enters the active pre-build crosswalk?

## 2026-07-19 - RQ-60 independent verification for agent-generated code

Question:

Which evidence combinations are genuinely independent enough to evaluate agent-generated browser work across semantics, security, state, accessibility, performance, and release operations?

Method:

Reconciled the agent task/provenance controls, independent-verification baseline, QA suites, security/adversarial review, accessibility evaluation, benchmark claim route, incident rehearsal, and release evidence requirements. Defined common-mode risks, oracle independence, denominator rules, verifier boundaries, and the evidence-bundle sequence.

Result:

Added an active `RQ-60` packet that distinguishes independent evidence from a second invocation, separate process, agent-authored test, or passing repository check. It requires task-scoped provenance, independent oracles, negative and recovery cases, raw artifacts, common-mode analysis, and reviewer disposition.

Impact:

The research index, crosswalk lane documentation, repository map, documentation-readiness audit, machine audit source list, and research log now route `RQ-60` to one independent-evidence path. This does not accept a task, promote a gate, or change the `90%` contained-M0 / `0%` full-build measures.

Next question:

Can the first approved task manifest bind its acceptance criteria to independent oracles and verifier roles without allowing the implementation agent to certify its own work?

## 2026-07-19 - RQ-65 service and offline architecture route

Question:

Which optional services improve safety or continuity, and what must remain functional, exportable, replaceable, or safely shut down without lock-in?

Method:

Reconciled the production-readiness service-dependency contract with profile/session, networking, update, privacy, agent, SLO, incident, support, and legal records. Classified service roles by local/remote necessity and authority, then defined failure, offline, export, self-hosting, migration, and shutdown evidence requirements.

Result:

Added a no-claim `RQ-65` packet covering service classification, data and authority boundaries, offline/degraded workflows, stale and replay behavior, export, self-hosting, provider migration, shutdown, privacy, support, and end-of-life evidence.

Impact:

The Blueprint, research index, repository map, documentation-readiness audit, machine audit source list, and research log now route `RQ-65` to one service-continuity evidence path. This does not select a provider, make a self-hosting or availability promise, change active/deferred counts, authorize broad implementation, or change the `90%` contained-M0 / `0%` full-build measures.

Next question:

Can service rows be captured in one owner-reviewed registry without allowing remote availability, model output, stale cache, or provider response to widen local browser authority?

## 2026-07-19 - RQ-61 stable scope and platform contract route

Question:

What finite capability and platform support boundary can provide meaningful daily use without creating an unmaintainable stable promise?

Method:

Reconciled the targetless stable-v1 scope, supported-platform and hardware matrix, `PB-006` reference-platform scorecard, native UI/accessibility route, compatibility denominator policy, benchmark contract, update/recovery, incident, ownership, and support records.

Result:

Added a no-claim `RQ-61` packet that defines the stable-scope record fields, status vocabulary, platform decision sequence, denominator rules, promotion criteria, and rejection cases. It keeps stable scope, platform selection, support, compatibility, accessibility, performance, security, and release decisions separate until owner-reviewed evidence exists.

Impact:

The Blueprint, research index, repository map, documentation-readiness audit, machine audit source list, and research log now route `RQ-61` to one finite-scope/platform evidence path. This does not select a platform or capability set, change active/deferred counts, authorize broad implementation, or change the `90%` contained-M0 / `0%` full-build measures.

Next question:

Can an owner-reviewed stable-scope packet preserve complete workflow and platform denominators while keeping unsupported and not-evaluated cases visible in public support language?

## 2026-07-19 - RQ-66 human release, legal, and incident capacity route

Question:

What evidence is required before Turing can support beta or stable operations with qualified human release, legal, support, signing, and incident capacity?

Method:

Reviewed NIST SP 800-61 Rev. 3 incident-response guidance, GitHub protected-branch controls, and the existing Turing incident-response, backup-ownership, package/update, SLO, secure-development, and production-readiness records. Mapped the shared authority boundaries, capacity fields, rehearsal cases, and synchronization requirements.

Result:

Added a no-claim `RQ-66` packet covering named primary and backup roles, qualification, availability, recusal, two-person control, support scope, legal boundaries, signing, on-call, incident exercises, disclosure, rollback, and independent review. It explicitly rejects role names, templates, automation, and agent output as substitutes for human capacity or authority.

Impact:

The Blueprint, research index, repository map, documentation-readiness audit, machine audit source list, and research log now route `RQ-66` to one cross-lane evidence path. This does not name owners, grant authority, select a support term, change active/deferred counts, authorize broad implementation, or change the `90%` contained-M0 / `0%` full-build measures.

Next question:

Can one owner-reviewed capacity and rehearsal record reconcile the exact support, ownership, incident, update, legal, and release scopes without creating a second status registry?

## 2026-07-19 - RQ-64 secure-development and provenance maturity route

Question:

Which evidence and scope rules are needed before Turing can describe secure development, provenance, reproducibility, release integrity, or compliance maturity?

Method:

Reviewed the final NIST SP 800-218 SSDF 1.1 publication and the approved SLSA 1.2 specification and Build Provenance model. Separated practice frameworks, source/build provenance, SBOMs, reproducibility, signatures, attestations, review, vulnerability handling, and release authorization, then mapped them to Turing's existing source, toolchain, package/update, incident, ownership, and closure gates.

Result:

Added a no-claim `RQ-64` packet with proposed Turing bookkeeping maturities, evidence fields, cross-framework boundaries, and an owner-review sequence. The packet explicitly avoids treating a passing local build, SBOM, signature, attestation, or matching rebuild as proof of a broader security or release property.

Impact:

The Blueprint, research index, repository map, documentation-readiness audit, machine audit source list, and research log now route `RQ-64` to a concrete maturity/provenance evidence path. This does not select a compliance level, claim SLSA or SSDF conformance, authorize implementation, change active/deferred counts, or change the `90%` contained-M0 / `0%` full-build measures.

Next question:

Can a scope-specific maturity record be captured and independently reviewed without turning proposed Turing bookkeeping labels into framework certification claims?

## 2026-07-19 - RQ-62 product SLO and error-budget preparation

Question:

Which evidence and policy structure is required before Turing can choose numeric reliability, performance, energy, compatibility, accessibility, migration, update, and agent-safety targets?

Method:

Reviewed the targetless production-readiness SLO catalog and the official Google SRE guidance on SLI/SLO/SLA distinctions, percentile and denominator design, error budgets, release decisions, and product risk tradeoffs. Mapped those observations to Turing's browser-specific workflows and existing benchmark, quality, security, accessibility, storage, update, and agent-safety lanes.

Result:

Added a no-claim `RQ-62` preparation packet. It requires owner-approved workflows, explicit bad-event and denominator definitions, pinned measurement conditions, raw evidence, privacy review, candidate target tradeoffs, and an owner-reviewed release/error-budget policy. Protected security, accessibility, data-integrity, and authorization failures remain stop conditions rather than metrics that can be offset by performance gains.

Impact:

The research index, Blueprint question, bibliography, repository map, and research log now route `RQ-62` to the canonical targetless SLO catalog and a concrete evidence package. This does not set numeric targets, promote release gates, change active/deferred counts, authorize broad implementation, or change the `90%` contained-M0 / `0%` full-build measures.

Next question:

Can owner-reviewed workflow severity, denominator, and exception policy be captured in the SLO registry without turning candidate values into accepted release targets?

## 2026-07-19 - Deferred research-question routes semantically aligned

Question:

Does every deferred machine `RQ-*` row route to the same question described by the canonical Blueprint, rather than merely passing identifier and shape validation?

Method:

Compared all 29 deferred records in `research-question-coverage.json` with the exact `RQ-*` titles and decision outputs in Blueprint 22, then reviewed owner routes, revisit triggers, and required future evidence for domain fit.

Result:

Found shifted or unrelated routes for `RQ-24`, `RQ-26`, `RQ-28`, `RQ-32`, `RQ-41`, `RQ-42`, `RQ-43`, `RQ-51`, `RQ-52`, `RQ-58`, `RQ-59`, `RQ-61`, `RQ-62`, and `RQ-65`. Corrected the machine registry to match the canonical agent, networking, media, extensions, dependency, Plug-in, embedding, resource, agent-mode, readiness-control, agent-authority, stable-scope, SLO, and service/offline questions. Added a semantic-alignment control to the human coverage audit.

Impact:

Maintainers now receive the correct owner route and evidence shape when following any deferred question. The correction improves tracking integrity without answering a question, changing active/deferred counts, promoting a gate, approving a task, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

Can the same title-to-route semantic check become a validator invariant so future question renumbering or registry edits fail before handoff?

## 2026-07-19 - RQ-39 replay and observability route expanded

Question:

Does the deferred `RQ-39` record match the Blueprint's deterministic-replay and causal-observability question, and does it give future engineers a safe evidence route rather than misrouting the question to generic conformance/fuzzing work?

Method:

Compared the Blueprint research program, deferred-question registry, quality-assurance book, developer-experience and performance trace requirements, and official `rr`, Firefox, Chromium trace-event, Perfetto, and LibFuzzer documentation retrieved or checked on 2026-07-19.

Result:

Corrected the deferred registry's stale conformance/fuzzing route and added a no-claim `RQ-39` packet covering input/state replay, execution replay, semantic snapshots, causal identity, redaction, retention, authority-negative tests, divergence oracles, overhead controls, and unsupported platform cases. Conformance and fuzzing remain supporting evidence classes rather than the research question's title or owner route.

Impact:

The research index, Blueprint, and machine coverage registry now agree on the `RQ-39` question and future proof. This improves traceability for difficult browser bugs and Chrome-class developer tooling without selecting a replay runtime, trace format, or diagnostic release contract, and without changing the 90% contained-M0 / 0% full-build measures.

Next question:

When the relevant engine and IPC work is authorized, can a bounded virtual-time/input replay harness and redacted causal trace prototype be run with a no-trace control and authority-negative tests?

## 2026-07-19 - Nova source regions reconciled to contracts

Question:

Does the Nova source-to-contract handoff account for its concrete view regions, including migration, time machine, assistant, inspector, capture, recovery, and resource surfaces, rather than only the 16 high-level component groups?

Method:

Inspected the committed Nova source manifest and source regions, compared the function-level surfaces with the Nova Surface-to-Contract Map and the checked component-fixture inventory, and assigned each additional region to an existing toolkit-neutral contract. No source bytes, manifest hash, toolkit choice, or runtime behavior were changed.

Result:

The source regions reconcile to the existing contracts for page shell/recovery, tabs/library, settings/migration, Shield/vault, view tools, resources, agent confirmation/activity, DevTools/command field, and Spaces/recovery. The map now records the grouping explicitly so a future native extraction cannot silently omit a visual workflow or treat a React callback as browser authority.

Impact:

Nova remains the primary visual/layout reference, while Rust state, typed commands, page-surface, accessibility, security, profile, agent, and accepted ADR contracts remain authoritative. This improves design handoff completeness without selecting a native toolkit, promoting `PB-003`/`PB-005`/`PB-014`/`PB-015`, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

Can the authorized native fixture work reproduce these reconciled source regions through toolkit-neutral state, command, accessibility, page-surface, fault, and performance evidence?

## 2026-07-19 - Servo source-strategy freshness revalidated

Question:

Do the current official Servo project, repository release, crate, and embedding references change the source-strategy decision inputs or the boundary between an upstream engine observation and Turing approval?

Method:

Rechecked the official Servo repository release API, project/about page, Servo Book embedding overview, and current crate documentation. Compared those observations with the checked `ADR-0009` source-observation manifest and the upstream refresh packet without changing the local Servo checkout or importing source.

Result:

The latest public Servo release remains `v0.3.0` at the previously captured release commit, distinct from the captured `main` head. Official project material continues to describe an embeddable Rust engine whose production-readiness transition and embedding documentation are still in progress; the crate exposes a WebView integration surface, but public API presence does not establish Turing process, security, compatibility, maintenance, or release readiness.

Impact:

The source-strategy packet now records the public project/embedding boundary explicitly. This strengthens `ADR9-EV-001`, `ADR9-EV-002`, `ADR9-EV-012`, and `ADR9-EV-016` routing without selecting Servo, accepting `mozjs`, closing `PB-002`, authorizing source import, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

Which exact source baseline, runtime relationship, component boundary, and independent reproduction scope will the owner and reviewer accept for the chosen `ADR-0009` option?

## 2026-07-19 - Live GitHub handoff refreshed

Question:

Does the durable GitHub issue and pull-request handoff still match the live repository state and current `main` baseline after the documentation refreshes?

Method:

Ran the documented `gh issue list` and `gh pr list` queries against `byronwade/Turing`, checked the issue/PR states and cleanup branches, and compared the result with the checked handoff registry and current `git rev-parse HEAD`.

Result:

The canonical issue set remains `#1` through `#12` plus `#14`; issue `#1` is closed, `#2` through `#12` and `#14` remain open, and the previously cleaned PRs remain closed with their remote branches deleted. The handoff snapshot now records observation date `2026-07-19` and baseline commit `7a1c75f6f912f71cc9ec3f5cd79fb00f1e1dbc1e`.

Impact:

This refresh removes stale snapshot metadata without changing issue dispositions, task authority, readiness, implementation, security, compatibility, performance, release, or Chrome-class claims. GitHub remains a coordination surface only.

Next question:

Can the next accepted task or owner decision update the canonical issue handoff, task records, readiness registries, and research log in one synchronized change?

## 2026-07-19 - Fresh-host acquisition and replay modes separated

Question:

Does the fresh-host contract distinguish dependency/tool acquisition from reproducibility replay, so preloaded caches or network differences cannot be hidden inside a “clean” run?

Method:

Compared the fresh-host closure preparation, reproduction inventory, run-record schema/template, run-record validator, and reproducible-builds release book.

Result:

The machine inventory now requires a separate network/cache evidence axis. The run-record schema and no-claim template require acquisition and replay mode declarations, including cache state, offline or controlled-network behavior, artifact hashes, proxy/certificate posture, and owner-approved equivalence for reused caches. The closure preparation and release book now reject preloaded offline runs as clean acquisition evidence.

Impact:

This removes a reproducibility ambiguity without creating a fresh-host run, proving toolchain equivalence, promoting `PB-008`/`PB-009`, or changing the 90% contained-M0 / 0% full-build measures.

Next question:

Can an approved `TASK-000002` run retain separate acquisition and replay artifacts on an independent host or approved clean VM, including all failures and cleanup evidence?

## 2026-07-19 - ADR-0009 option comparison normalized

Question:

Does the ADR-0009 handoff distinguish external research, upstream collaboration, selective component reuse, engine adoption, and charter change before an owner compares or selects a source strategy?

Method:

Compared the ADR-0009 source-strategy packet, evidence traceability matrix, decision draft, no-claim decision-review template, independent-engine boundary, and current PB-002 owner-decision route.

Result:

Added a normalized option matrix covering charter relationship, release-surface consequence, minimum decision-grade evidence, and the claim permitted before acceptance. The matrix makes explicit that these options are not interchangeable and that a lower implementation burden cannot override provenance, legal, security, compatibility, maintenance, or charter requirements.

Impact:

This improves source-strategy decision coherence without selecting Servo, authorizing source import, closing `PB-002`, or changing any implementation boundary. `ADR9-EV-018` remains blocked, documentation remains 90% organized for contained-M0 continuation, and full-build closure remains 0%.

Next question:

Which normalized option, source baseline, feature profile, and bounded claim scope will the owner and independent reviewer accept after the remaining ADR9 evidence is reviewed?

## 2026-07-19 - Compatibility prioritization and denominator contract added

Question:

Does the compatibility lane tell a maintainer what to prioritize and what evidence is required before a capability becomes a supported or Chrome-class claim, rather than only listing standards and test suites?

Method:

Compared `RQ-15`, the capability-parity matrix, the testing and compatibility chapter, the web-platform source manifest, and official WPT/Test262/Interop documentation observed on 2026-07-19.

Result:

The new no-claim packet defines `P0` release-critical, `P1` high-value, and `P2` experimental planning classes; a capability-row contract; complete pass/fail/timeout/crash/leak/harness-error/not-run/disabled/expected/unsupported accounting; differential and normative-source triage; and promotion/rejection rules. It explicitly separates prioritization from test results and support claims.

Impact:

This closes a compatibility-planning ambiguity and gives `RQ-15` a durable evidence route connected to the parity matrix, WPT/Test262 source work, task sequencing, and support-claim boundaries. It does not select a capability or profile, execute tests, establish compatibility, or change the full-build gate. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Which narrowly scoped supported profile and capability rows should an owner approve for the first executable compatibility manifest after source strategy and task authority are resolved?

## 2026-07-19 - IPC transport authority ordering made portable

Question:

Does the IPC documentation define one enforceable authority ordering across Windows named pipes, Linux Unix-domain sockets, and macOS XPC rather than treating platform identity signals as authorization by themselves?

Method:

Aligned the system-architecture IPC rules, capability-secure IPC rules, and IPC transport closure preparation with the existing platform transport worksheet and source-backed identity observations.

Result:

The canonical ordering is now explicit: observe the OS peer and endpoint context, bind it to the broker process ID, role, and restart epoch, register the channel, authorize route and attenuated capability per message, and re-check scope, deadline, cancellation, and resource state before publication or handle use. Restart, reconnect, and endpoint replacement invalidate affected channels, requests, handles, and leases. Required negative cases now include pre-binding authorization, stale replay, mismatched peer, route/capability mismatch, and timeout or disconnect cleanup.

Impact:

This closes a documentation ambiguity in the portable IPC contract without claiming an accepted transport, production IPC, process isolation, or stale-epoch proof on a real transport. The existing `PB-011`, `TASK-000011`, `TASK-000003`, and full-build gates remain unchanged; documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can an approved transport task demonstrate this ordering and its negative cases on each supported platform with exact source, raw logs, failure records, and independent review?

## 2026-07-19 - Fresh-host reproducibility claim ladder clarified

Question:

Does the `PB-008`/`PB-009` documentation distinguish a repeatable local check, a clean-host replay, a bit-for-bit reproducible build, and independently verified reproduction before using any of those terms in a build or release claim?

Method:

Compared the fresh-host closure preparation, fresh-host reproduction registry and run-record template, repository toolchain standards, and release-operations reproducible-builds book with the Reproducible Builds environment-recording guidance and SLSA's reproducibility FAQ observed on 2026-07-19.

Result:

The documentation now defines a four-level claim ladder: repeatable validation, clean-host replay, reproducible build, and independently verified reproduction. It requires output equality, builder/host independence, provenance, source/dependency review, cache and target controls, and failure accounting to remain separate evidence axes. The fresh-host machine registry now includes an explicit reproducibility-level axis and the toolchain source manifest includes the two official reproducibility sources.

Impact:

This prevents a successful same-host `check.ps1`, a clean-VM run without an approved equivalence record, or a single matching hash from being called independently verified. It strengthens the build-information handoff but does not provide an independent fresh-host run, bit-for-bit artifact comparison, owner-reviewed readiness, release integrity, or production claim. `PB-008`, `PB-009`, `TASK-000002`, and `PB-020` remain unresolved. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can an approved `TASK-000002` run produce a hash-linked build-information record and output comparison on an independent host, while retaining every setup, failure, cleanup, and provenance artifact?

## 2026-07-19 - ADR-0009 live source identities pinned for observation

Question:

Can the current official Servo and `mozjs` repository state be recorded precisely enough to prevent a moving branch, release tag, or independently moving JavaScript binding from being treated as one interchangeable source baseline?

Method:

Ran read-only GitHub API queries for `servo/servo` repository metadata, latest head commit, latest release/tag, and `servo/mozjs` repository metadata and head commit. No repositories were modified. Compared the capture with the existing ADR-0009 source-observation manifest and the upstream refresh report.

Result:

On 2026-07-19, `servo/servo` was public, non-archived, default branch `main`, with head `736ad1bda08c1af419aadc903e82938f8610a65d`; its latest release was `v0.3.0`, published 2026-06-25 at tag commit `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`. `servo/mozjs` was public, non-archived, default branch `main`, with independent head `f5cbf8aa6076064fd658a1e9fb16147c2347affb`. The `mozjs` API response returned null SPDX license and security-policy URL fields, which remain unresolved metadata observations rather than absence claims.

Impact:

The ADR-0009 source-observation manifest now records seven source inputs and keeps moving-head, release-tag, and `mozjs` identities separate. The capture improves provenance and refresh routing but does not select a baseline, prove archive equivalence, resolve licensing/security metadata, approve a dependency or component, or authorize source import or release code. `PB-002`, `ADR-0009`, and `PB-020` remain unresolved. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the owner select an exact Servo/`mozjs` source profile, resolve license/security metadata, and replay it from a clean target with retained dependency, generated-output, compatibility, performance, and security evidence?

## 2026-07-19 - Performance timing-source separation expanded

Question:

Does the `PB-013` performance lane distinguish page-observable timing, user-facing page responsiveness, browser chrome input, and causal trace diagnosis well enough to prevent a web metric from becoming an unsupported browser-wide performance claim?

Method:

Compared the benchmark evidence and claim-closure route, Blueprint 09, the performance statistics book, and the startup/navigation/input benchmark chapter with W3C Navigation Timing, W3C Event Timing, the W3C Long Animation Frames draft, and web.dev's INP guidance as observed on 2026-07-19.

Result:

The documentation now requires separate page-observable, user-facing, and causal-diagnostic views. Future interaction records must retain input arrival, queue delay, processing, rendering/presentation, interaction identity, document/frame/site identity, process/resource owner, cancellation/timeout, and visible/stale/failed outcome. Page metrics remain distinct from chrome input-to-present and browser-wide resource or process measurements. Long Animation Frames remains capability-detected diagnostic evidence with a no-diagnostic control because it is a draft API.

Impact:

The `PB-013` contract is more explicit about metric-family boundaries, privacy minimization, cross-origin limitations, failure denominators, and observer overhead. This does not provide a browser run, benchmark result, owner-reviewed readiness, compatibility result, speed result, energy result, or Chrome-class claim; `PB-013`, `TASK-000005`, and `PB-020` remain unresolved. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the reviewed L1 runner emit these decomposed interaction records and equivalent no-trace controls from a real browser run without leaking page content or silently dropping failed or unsupported interactions?

## 2026-07-19 - Live repository ownership controls captured

Question:

What effective GitHub repository controls exist today for the ownership and independent-review blocker, and can they be treated as proof of backup coverage or two-person control?

Method:

Ran a read-only authenticated GitHub CLI audit against `byronwade/Turing`: repository metadata, `main` branch protection, and repository rulesets. Compared those results with the checked `.github/CODEOWNERS` file and the ownership gap registry. No settings were changed and no credentials were recorded.

Result:

The repository is public with `main` as its default branch. The branch-protection endpoint returned `404 Branch not protected`; the rulesets endpoint returned no rulesets; automatic branch deletion after merge is disabled. The wildcard and listed path classes in `.github/CODEOWNERS` route to provisional `@byronwade` only, with no backup owner.

Impact:

This is dated configuration evidence, not proof of qualification, availability, independent review, two-person control, or release safety. It confirms that repository enforcement and backup ownership remain open controls. `PB-019` remains blocked, and no production, release, signing, disclosure, incident-closure, legal, owner-coverage, or broad-readiness claim changes. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the owner approve and apply a protected `main`/ruleset configuration with independent review, code-owner enforcement, bypass restrictions, status checks, and branch cleanup policy, then reconcile it against named qualified backups and the remaining high-authority control surfaces?

## 2026-07-19 - Nova new-tab and page-shell mapping completed

Question:

Does the Nova source inventory map the browser's new-tab and web-page shell to an explicit native fixture contract, rather than leaving the page surface implied by the chrome components?

Method:

Compared the Nova source manifest and design-lab surface map with the toolkit-neutral component-fixture inventory, native UI book, page-surface composition route, and `validate_ui_component_fixtures.py`. The source manifest contained a new-tab/web-page shell surface, while the machine fixture inventory covered only 15 other component surfaces. Added `UI-COMPONENT-NEW-TAB-PAGE-SHELL` and synchronized its state, command, accessibility, page-generation, and authority-boundary requirements.

Result:

Nova's browser-face coverage now explicitly includes the new-tab/web-page shell. The fixture contract requires loading, error, recovery, stale-generation, focus-transfer, page-tree, and chrome/page trust-boundary evidence, with typed page-surface handles and no renderer authority in chrome.

Impact:

The UI fixture inventory now covers 16 component surfaces: 10 core shell surfaces and 6 Nova-specific product surfaces. `PB-014`, `PB-003`, `PB-005`, `PB-015`, and `PB-020` remain unresolved; no native implementation, toolkit, accessibility, page-surface, security, performance, or production claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future native fixture packet render or semantically exercise this page-shell contract with the selected adapter while preserving page-surface generations, renderer crash recovery, focus, IME, and accessibility evidence?

## 2026-07-19 - Incident repository-coordination boundary expanded

Question:

Does the `PB-018` incident route document how private vulnerability coordination on GitHub relates to, but does not replace, human security and release authority?

Method:

Compared the [Incident-Response Execution and Disclosure Closure Preparation](research/incident-response-execution-and-disclosure-closure-preparation-2026-07.md), incident decision preparation, security-engine and release-operations books, and incident source manifest with GitHub's [repository security advisory guidance](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories). Added the source identity and synchronized the private-access, patch-scope, disclosure, audit, and authority boundary.

Result:

Future rehearsals must retain advisory/repository access, private patch or fork scope, collaborator identities, state transitions, disclosure timing, and audit evidence. GitHub workflow state remains coordination evidence only; severity, containment, signing, release promotion, disclosure, and incident closure require explicit human authority.

Impact:

The `PB-018` source manifest now carries seven source records across incident lifecycle, severity, coordinated disclosure, and repository advisory coordination. `PB-018` and `TASK-000010` remain unresolved and proposed-only; no incident-response, disclosure, signing, supported-security, production, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a private synthetic rehearsal retain repository advisory state, protected patch-branch evidence, fake-key update dry-run data, and redacted disclosure records with a complete timing and failure denominator?

## 2026-07-19 - Package and update platform trust coverage expanded

Question:

Does the `PB-017` package/update evidence route cover platform-specific release trust for Windows, macOS, and Linux rather than inferring it from Windows signing alone?

Method:

Compared the [Package/Update Execution and Release-Safety Closure Preparation](research/package-update-execution-and-release-safety-closure-preparation-2026-07.md), package/update decision preparation, release-operations books, and source manifest with Apple's [macOS notarization guidance](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) and Flatpak's [usage documentation](https://docs.flatpak.org/en/latest/using-flatpak.html). Added platform-specific source identities and synchronized the no-claim boundary.

Result:

Future release records must keep Windows signing, macOS notarization, and Linux remote/runtime/scope identity distinct from TUF metadata, provenance, installation atomicity, rollback, profile migration, privacy, and support decisions. Each platform needs exact artifact/package identity, tool/runtime versions, permission or entitlement context, failure behavior, and unsupported distribution rows.

Impact:

The `PB-017` source manifest now carries eleven source records across update metadata, provenance, supply-chain steps, signing/transparency, and Windows/macOS/Linux release inputs. `PB-017` and `TASK-000009` remain unresolved and proposed-only; no package, updater, signing, channel, rollback, migration, supported-security, or release claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future fake-key, local-only package lab exercise platform-specific verification, offline/network failure, staged activation, rollback, and cleanup with identical trust-state accounting across the declared reference platforms?

## 2026-07-19 - Profile credential-vault boundary expanded

Question:

Does the `PB-016` profile/session evidence route keep operating-system credential vaults separate from ordinary browser-owned session data?

Method:

Compared the [Profile/Session Execution and Data-Safety Closure Preparation](research/profile-session-execution-and-data-safety-closure-preparation-2026-07.md), profile/session format inventory, storage book, schema-package and readiness templates, and source manifest with Microsoft's [Credential Manager](https://learn.microsoft.com/en-us/windows/win32/secauthn/credential-manager), Apple's [Keychain Services](https://developer.apple.com/documentation/security/keychain_services), and freedesktop.org's [Secret Service API](https://specifications.freedesktop.org/secret-service/latest/). Added platform vault source identities and a dedicated evidence row.

Result:

Credential evidence must identify the vault/backend, target or collection identity, access or entitlement boundary, locked/unavailable/prompt behavior, deletion/logout semantics, and unsupported desktop environments. Secret values must remain outside profile/session records, exports, migrations, diagnostics, backups, and fault artifacts. A successful vault lookup is not authorization or durability proof.

Impact:

The `PB-016` source manifest now carries ten source records across web storage, durability, privacy, Windows, macOS, and Linux credential-vault inputs. `PB-016` and `TASK-000007` remain unresolved and proposed-only; no credential, profile, migration, sync, privacy, data-loss, production, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future synthetic profile/session packet exercise vault locked, unavailable, denied, deletion, logout, export, and migration paths without accessing or retaining real credentials?

## 2026-07-19 - Benchmark observer-effect boundary expanded

Question:

How can Turing use host and browser tracing for extreme-performance diagnosis without treating instrumentation overhead as product performance?

Method:

Compared the [Benchmark Evidence and Claim Closure Preparation](research/benchmark-evidence-and-claim-closure-preparation-2026-07.md), benchmark artifact/statistics contracts, performance and benchmark-lab books, and the checked benchmark-source manifest with [Perfetto trace configuration](https://perfetto.dev/docs/concepts/config) and the existing Microsoft WPR/ETW source records. Added the source identity and a paired no-trace control protocol covering configuration, buffers, event loss, sampling, and measured deltas.

Result:

Trace-enabled runs are diagnostic conditions unless an otherwise equivalent no-trace control demonstrates that the instrumentation effect is understood. Future packets must retain trace configuration, providers/data sources, buffers, clocks, sampling intervals, duration, loss indicators, collector/analyzer versions, artifact hashes, and deltas for latency, CPU, wakeups, memory, GPU, and energy where relevant.

Impact:

The benchmark lane now distinguishes raw measurement conditions from diagnostic instrumentation conditions. `PB-013` and `TASK-000005` remain no-claim and proposed-only; no performance, memory, energy, Chrome-class, or competitor result claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the future Level 1 runner generate paired no-trace and trace-enabled artifacts with the same workload, lifecycle, security, profile, failure-denominator, and cleanup identity?

## 2026-07-19 - IPC platform transport worksheet added

Question:

Can the IPC closure route compare Windows, Linux, and macOS transport identity without allowing an OS credential or connection primitive to become Turing authority by implication?

Method:

Reconciled the [IPC Transport and Authority Closure Preparation](research/ipc-transport-and-authority-closure-preparation-2026-07.md), the checked [IPC wire-source manifest](blueprint-v1/machine/ipc-wire-source-manifest.json), the IPC capability boundary, and the no-claim schema/readiness templates. Converted the existing Windows named-pipe, Linux Unix-domain socket, and macOS XPC source observations into one cross-platform capture worksheet.

Result:

The platform mechanism may provide endpoint, peer, session, namespace, entitlement, audit, or credential observations, but Turing must still bind the observed peer to the broker role, channel, process epoch, route, capability, resource limits, timeout, cancellation, and handle or lease policy. The worksheet now requires the same control envelope and policy oracle across platforms and records unsupported inferences explicitly.

Impact:

The IPC documentation is more directly executable as a future evidence packet, while `PB-011`, `TASK-000003`, `TASK-000011`, wire-encoding selection, transport authorization, and all security/readiness claims remain unchanged. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can an independent `TASK-000011` review packet retain these platform identity outputs together with exact source commit, generated policy records, negative cases, and cleanup evidence without treating the M0 policy reference as real transport proof?

## 2026-07-19 - Reference-platform assistive-technology evidence synchronized

Question:

Does the `PB-006` reference-platform scorecard distinguish platform accessibility APIs from actual screen-reader workflows?

Method:

Compared the reference-platform scorecard, platform engineering book, native UI/accessibility closure route, and accessibility source manifest with Microsoft's [Narrator guide](https://support.microsoft.com/en-us/accessibility/windows/narrator/complete-guide-to-narrator), Apple's [VoiceOver User Guide](https://support.apple.com/guide/voiceover/welcome/mac), and GNOME's [Orca guide](https://help.gnome.org/orca/). Added the three assistive-technology source identities to the scorecard and validator and linked each candidate to its platform-specific manual workflow source.

Result:

`PB-006` now requires both platform API observations and assistive-technology workflow evidence. Future runs must retain the exact OS and assistive-technology configuration, navigation mode, keyboard or braille setup, transcript or action record, focus and announcement timing, and unsupported workflows. A platform accessibility tree or control-pattern snapshot alone remains insufficient.

Impact:

The reference-platform scorecard now carries eleven source records across Windows, macOS, Linux, and cross-platform toolchain/CI inputs. No platform selection, support, accessibility, compatibility, security, performance, release, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future platform reference-shell packet bind these manual assistive-technology records to the same page-surface, input/IME, fault, timing, and artifact identity used by the native UI readiness review?

## 2026-07-19 - Assistive-technology workflow evidence expanded

Question:

What must a future native UI review retain to distinguish platform accessibility APIs from actual screen-reader workflows and user interaction evidence?

Method:

Compared the native UI/accessibility closure route, accessibility source manifest, platform bridge and assistive-technology test books, UI readiness template, and existing workflow inventory with Microsoft's [Narrator guide](https://support.microsoft.com/en-us/accessibility/windows/narrator/complete-guide-to-narrator), Apple's [VoiceOver User Guide](https://support.apple.com/guide/voiceover/welcome/mac), and GNOME's [Orca guide](https://help.gnome.org/orca/). Added the three assistive-technology source identities to the manifest and validator and synchronized the closure route, evidence matrix, index, and repository map.

Result:

Accessibility evidence must identify the exact assistive technology and configuration, navigation mode, keyboard/braille setup, transcript or action record, focus and announcement timing, structural navigation/live-region behavior, and unsupported workflows. A platform accessibility tree or semantic model alone is not screen-reader workflow evidence.

Impact:

The native UI accessibility manifest now requires seven primary source records across nine evidence axes and still covers Windows, macOS, and Linux. No accessibility workflow, screen-reader coverage, IME correctness, page-tree proof, UI-gate, readiness, production, or implementation claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future `TASK-000006` reference-shell packet produce matching platform tree snapshots, screen-reader transcripts, focus/event timing, IME behavior, page/chrome composition, and fault-denominator evidence under owner review?

## 2026-07-19 - Benchmark host-trace integrity evidence added

Question:

What host-trace facts must be retained before Windows CPU, memory, power, or energy observations can be treated as auditable benchmark artifacts rather than unverified trace files?

Method:

Compared the PB-013 benchmark source manifest, benchmark evidence/claim closure route, trace/artifact package contract, resource-attribution taxonomy, Windows reference-host controls, and benchmark readiness review with Microsoft's [Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr) and [ETW](https://learn.microsoft.com/en-us/windows/win32/etw/about-event-tracing) documentation. Added both source identities to the manifest and validator and synchronized the closure route and documentation-readiness matrix.

Result:

Host-trace evidence must bind tool/profile, start/stop commands, privilege and host controls, provider/session configuration, buffer and event-loss indicators, clock/timestamp facts, process/thread attribution, ETL hash, analysis tool/version, and missing-event policy. Trace-file existence is not capture-integrity proof and cannot replace browser pins, workload, lifecycle, security, or failure-denominator evidence.

Impact:

The `PB-013` benchmark-source manifest now requires ten primary source records across ten evidence axes. No Turing run, competitor result, statistics approval, performance, memory, energy, Chrome-class, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the reviewed `TASK-000005` L1 packet capture browser results and host traces with matching clocks, resource attribution, raw artifacts, failure denominator, cleanup, and owner review?

## 2026-07-19 - IPC platform identity evidence added

Question:

What platform transport facts must be recorded before Turing can evaluate authenticated IPC without treating a successful local connection or peer-credential query as proof of principal, capability, or process-isolation authority?

Method:

Compared the IPC capability-boundary inventory, wire-encoding decision preparation, transport closure route, schema-source and readiness templates, Blueprint IPC/security sections, and existing M0 tests with Microsoft's [named-pipe security](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights), Linux [`unix(7)`](https://www.man7.org/linux/man-pages/man7/unix.7.html), and Apple's [XPC peer identity](https://developer.apple.com/documentation/xpc/xpc_connection_set_peer_platform_identity_requirement(_:_:)) documentation. Added three platform source identities to the machine manifest and validator and synchronized the transport route and Blueprint boundaries.

Result:

Platform experiments must retain endpoint ACL/permission policy, transport namespace, peer identity evidence, session/namespace or entitlement context, remote-access policy, principal mapping, process epoch, reconnect/replay behavior, and impersonation or handle-transfer policy. Platform identity is necessary evidence but does not itself authorize a capability, validate a wire payload, or prove process/site isolation.

Impact:

The `PB-011` IPC wire-source manifest now requires eight primary source records across nine evidence axes. No encoding, generator, transport, owner-reviewed readiness, renderer-security, process-isolation, site-isolation, production IPC, or implementation claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the reviewed `TASK-000011` evidence and later `TASK-000003` transport packet bind platform peer identity to Turing principal, channel, and process epoch under negative, replay, timeout, cancellation, and compromised-peer tests?

## 2026-07-19 - Fresh-host toolchain identity boundary expanded

Question:

What toolchain-selection and Windows native-build facts must be retained before a future `TASK-000002` run can be compared across hosts without confusing a machine default, an initialized compiler environment, or an installed SDK with the actual build inputs?

Method:

Compared the fresh-host reproduction inventory, closure preparation, run-record contract, toolchain manifest, build-information ledger, repository `rust-toolchain.toml` and `Cargo.lock`, and existing Windows build observations with official [Rustup override](https://rust-lang.github.io/rustup/overrides.html), [Microsoft C++ command-line](https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170), and [Windows SDK](https://learn.microsoft.com/en-us/windows/apps/windows-sdk/) documentation. Added the source identities to the manifest and validator and synchronized the closure route, evidence matrix, repository map, and research log.

Result:

The run record must capture rust-toolchain-file discovery and precedence, active toolchain/components/targets/profile, lockfile identity, Developer Command Prompt or `vcvars` initialization, compiler/linker/LLVM paths and versions, target architecture, and Windows SDK version/root/discovery. `rustc --version`, an installed Visual Studio product, or a passing same-host build is not sufficient equivalence evidence.

Impact:

The `PB-008`/`PB-009` toolchain-source manifest now requires six primary source records across nine evidence axes. No fresh-host run, toolchain equivalence, owner-reviewed readiness, release confidence, implementation, performance, compatibility, security, or Chrome-class claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the reviewed `TASK-000002` run record retain these facts together with independent host identity, command denominator, cache/target controls, source-tree cleanliness, logs, and owner review?

## 2026-07-19 - ADR-0009 provenance policy boundary clarified

Question:

What exactly must an owner decide before Git, GitHub, release archives, or package checksums can be treated as an accepted Servo source-identity policy for `ADR9-EV-001`?

Method:

Compared the ADR-0009 source packet, independent source verification, source/archive equivalence policy, evidence matrix, closure-preparation route, and source bibliography with the official [Git tag](https://git-scm.com/docs/git-tag), [`git verify-tag`](https://git-scm.com/docs/git-verify-tag), and [GitHub signature-verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) documentation.

Result:

A lightweight tag, signed annotated tag, signed commit, GitHub verification status, local keyring result, archive digest, and package checksum are distinct observations. `ADR9-EV-001` must explicitly select one bounded provenance model and retain object type, ref, object/tree IDs, signer and trust-root status, retrieval date, revocation/expiry treatment, and independent remote-ref comparison before later evidence can be reused.

Impact:

The source-strategy closure route now states the provenance-policy alternatives and rejection conditions, and the evidence matrix and ADR packet point to that route. No source baseline, Servo option, dependency approval, source import, release-code authorization, compatibility, performance, security, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the owner review the bounded provenance alternatives together with the selected source baseline, equivalence policy, and clean-target replay protocol without treating a template or remote verification badge as approval?

## 2026-07-19 - Windows package-signing evidence added to PB-017

Question:

What platform-specific signing and verification facts must be preserved before Turing can evaluate Windows package/update behavior without treating an Authenticode result as complete release trust?

Method:

Compared the package/update trust decision packet, execution closure route, signing and update engineering chapters, PB-017 source manifest, and existing unsigned native-dependency observations with Microsoft's [SignTool verification guidance](https://learn.microsoft.com/en-us/windows/win32/seccrypto/using-signtool-to-verify-a-file-signature) and [Windows app code-signing options](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options). Added both source identities to the machine manifest and validator and synchronized the package/update decision, execution, release-book, and documentation-readiness records.

Result:

Windows evidence must preserve verification policy, signer and certificate-chain result, digest, timestamp state, tool/SDK identity, warning and failure disposition, distribution route, package type, private-key custody, rotation, and recovery as separate fields. Authenticode verification is an artifact/platform signal; it does not establish metadata freshness, provenance, authorized supply-chain steps, installer recovery, profile migration safety, or release authority.

Impact:

The `PB-017` source manifest now requires nine primary source records across its eight evidence axes. The existing unsigned native-dependency observations remain an explicit release-input risk. No package format, signing hierarchy, channel, production updater, release, supported-security, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future `TASK-000009` fake-key, local-only lab verify Windows artifacts under an explicitly selected policy while preserving package identity, metadata authorization, provenance, installer recovery, profile-transition, privacy, and owner-review boundaries?

## 2026-07-19 - Profile/session durability evidence refreshed

Question:

What primary storage evidence must be added before Turing can evaluate profile/session durability, migration, and recovery without treating a successful write or database choice as proof of data safety?

Method:

Compared the existing profile/session lifecycle decision packet, execution closure route, storage migration book, checked profile/session source manifest, and `PB-016` readiness records with SQLite's [atomic commit](https://sqlite.org/atomiccommit.html) and [corruption](https://sqlite.org/howtocorrupt.html) documentation and Microsoft's [buffered-I/O flush guidance](https://learn.microsoft.com/en-us/windows/win32/fileio/flushing-system-buffered-i-o-data-to-disk). Added three source identities to the machine manifest and validator and synchronized the lifecycle, execution, and storage research records.

Result:

Persistence evidence must distinguish atomic consistency from durable persistence and must retain journal/WAL mode, sync/flush policy, locking, filesystem and hardware assumptions, concurrent-access behavior, corruption detection, quarantine, and platform-specific failure results. SQLite or an operating-system flush API may inform the experiment but does not select Turing's profile backend or prove a production profile format.

Impact:

The `PB-016` source manifest now requires seven primary source records and preserves the nine profile/session evidence axes. No profile format, migration, credential, privacy, data-loss, production, performance, or readiness claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future `TASK-000007` synthetic-fixture package exercise interrupted commits, power-loss boundaries, corruption, migration rollback, privacy exclusion, and recovery accounting with the selected backend and platform policy?

## 2026-07-19 - Sandbox platform evidence refreshed

Question:

What additional official platform facts must be captured so Turing does not mistake requested sandbox settings or namespace creation for effective containment or bounded resource control?

Method:

Refreshed the canonical [Sandbox Platform-Evidence Decision Preparation](research/sandbox-platform-evidence-decision-prep-2026-07.md) against Microsoft's [Create Process In Sandbox APIs](https://learn.microsoft.com/en-us/windows/win32/secauthz/createprocessinsandbox) and the Linux kernel's [user namespaces and resource control](https://docs.kernel.org/admin-guide/namespaces/resource-control.html), then synchronized the checked platform-source manifest and validator. Compared the findings with the existing AppContainer, process-mitigation, seccomp, Landlock, App Sandbox, Hardened Runtime, probe inventory, and `PB-012` closure route.

Result:

The Windows source makes the dependency between AppContainer mode and several restriction fields explicit, while the Linux source adds a resource-control caveat for user namespaces. Turing's future probes must capture effective launch mode, applied restrictions, namespace limits, and cgroup state; source documentation and requested configuration remain insufficient evidence.

Impact:

The `PB-012` source manifest now contains eight official platform-source records across Windows, Linux, and macOS, and the validator requires the new Windows sandbox-launch and Linux resource-control identities. No sandbox policy, effective-policy result, security gate, performance claim, readiness promotion, or implementation authority changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a future `TASK-000004` package capture these effective states and expected-deny results from the exact constrained process roles on each supported platform without treating unsupported primitives as passes?

## 2026-07-19 - Servo upstream refresh and source-strategy delta

Question:

What current official Servo and `mozjs` observations must be refreshed before `ADR-0009` source, runtime, build, and maintenance decisions can be reviewed?

Method:

Reviewed the official [Servo repository](https://github.com/servo/servo), [Servo pull requests](https://github.com/servo/servo/pulls), and [Servo `mozjs` repository](https://github.com/servo/mozjs) on 2026-07-19, then compared those live observations with the existing source-strategy inventory, provenance/equivalence packets, build-reproduction route, component/runtime analysis, security-maintenance report, ADR evidence matrix, and machine evidence registry. Added a dated no-claim refresh packet that separates live upstream activity from commit-pinned Turing evidence and routes the delta to `ADR9-EV-001`, `002`, `012`, and `016`.

Result:

The upstream surfaces confirm a broad, moving engine and embedding/build ecosystem with explicit native/toolchain, runtime, test, security, and maintenance surfaces. The official project description calls Servo a prototype and publishes platform/build guidance; the `mozjs` project documents a separate SpiderMonkey binding and vendored/upstream workflow. These observations improve freshness and decision routing but do not resolve source identity, reproducible independent builds, Turing-owned JavaScript semantics, or maintenance ownership.

Impact:

The source-strategy lane now has a dated upstream refresh with source URLs, observation-versus-inference rules, freshness controls, evidence-item mapping, and a next-proof sequence. `PB-002` and `ADR9-EV-018` remain blocked; no source, dependency, runtime, compatibility, performance, security, support, or release claim changed. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can an owner freeze one source baseline and runtime relationship, reproduce it on an independent clean host, and accept the resulting maintenance and provenance contract through a real `ADR-0009` review record?

## 2026-07-19 - Nova design authority synchronized into readiness audit

Question:

Can future UI work use the supplied Nova source consistently without allowing a React design-lab artifact to become trusted browser behavior or release-path authority?

Method:

Compared the UI runtime book, Nova design-lab source boundary, surface-contract map, design-source manifest and validator, native UI readiness lanes, documentation-readiness audit, progress snapshot, and documentation evidence matrix. Added the Nova source and its contract map to the central audit evidence set and made the visual-versus-behavioral authority split explicit in the human audit.

Result:

Nova is now represented in the central readiness handoff as the visual and layout reference. Rust state, typed commands, native accessibility, page-surface, security policy, and accepted ADRs remain authoritative for behavior and release-path decisions. No UI toolkit was selected and no native UI or accessibility readiness claim changed.

Impact:

The design instruction is easier to discover from the build-readiness snapshot and completion audit, while the React/JavaScript exclusion for trusted chrome remains enforced by the UI runtime rules and design-source validator. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can the selected native adapter reproduce Nova's visual states through toolkit-neutral contracts, component fixtures, input, accessibility, fault, and performance evidence before `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `PB-020` are promoted?

## 2026-07-19 - Deferred open-web governance route expanded

Question:

What evidence and review packet must exist before a web-platform feature moves from deferred `RQ-33` research into implementation or compatibility support?

Method:

Compared the checked web-platform source manifest, six-chapter web-platform governance book, research-question coverage audit, active PB-002 crosswalk, WHATWG working mode, W3C Web Platform Design Principles, W3C Privacy Principles, WPT, and Interop sources. Added a dated no-claim research packet with feature-promotion fields, evidence order, lifecycle controls, rejection rules, and explicit separation between active PB-002 questions and deferred `RQ-33` context.

Result:

The future `RQ-33` route is now concrete enough for a maintainer to prepare a feature-specific packet without treating a source list or standards URL as a compatibility decision. `RQ-33` remains deferred, no task or feature was selected, and no readiness or product claim changed.

Impact:

The open-web governance lane now has a durable research artifact, an indexed local link, an explicit promotion trigger, and a claim boundary connected to the existing crosswalk and source manifest. Documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

Next question:

Can a real feature-specific packet satisfy the source, test, interoperability, security, privacy, accessibility, lifecycle, maintenance, and owner-review requirements before any feature is selected?

## 2026-07-19 - Research-question coverage made explicit

Question:

Are all numbered research questions either routed to an active pre-build lane or explicitly deferred with a revisit path, so omission cannot be confused with completion?

Method:

Compared the 66 headings in `docs/blueprint-v1/22-research-program.md` with the `RQ-*` IDs in `research-readiness-crosswalk.json`. Added a machine coverage registry, schema, validator, and dated audit. The validator requires the active set to match the crosswalk exactly and requires every remaining question to carry an explicit deferred status, owner route, revisit trigger, and future evidence list.

Result:

All 66 questions are now accounted for: 37 are active in current readiness lanes and 29 are explicitly deferred outside the current pre-build crosswalk. No question was answered, rejected, converted into a task, or promoted into a support or readiness claim.

## 2026-07-19 - Owner-decision synchronization control made executable

Question:

Can each owner-controlled build-readiness decision be handed from evidence collection to a real closure packet without losing role separation, exception expiry, synchronized registry updates, or claim boundaries?

Method:

Added a no-claim synchronization matrix, schema, validator, and dated control report for the 11 canonical PB-020 decision scopes. The matrix is checked against the existing closure-review template, owner-decision board, readiness registries, production controls, and agent-execution controls. It records roles, minimum evidence, exact synchronization paths, exception requirements, and prohibited claims without adding a status or approval registry.

Result:

The owner-decision handoff is more operationally complete and machine-traceable. No human owner was named, no decision was selected, no gate or task was closed, and no authority or product claim changed. The owner-decision criterion remains unresolved; documentation remains 90% organized for contained-M0 continuation and 0% closed for the full-build goal.

## 2026-07-19 - Web-platform source and conformance route made executable

Question:

Can standards, conformance suites, interoperability, automation protocol, and lifecycle evidence be collected as one checked no-claim route without implying browser compatibility or standards conformance?

Method:

Added the web-platform source manifest, schema, validator, and dated evidence report. The route records normative-source identity, suite commit and harness discipline, denominator accounting, interoperability, security/privacy/accessibility review, feature lifecycle, differential testing, and unsupported behavior. It is attached to the existing PB-002 source-strategy evidence route and does not add a task, select a feature, authorize implementation, or establish compatibility.

Result:

The source route is now machine-checked and indexed. No standards snapshot, WPT/Test262 execution, denominator, browser-run artifact, differential result, conformance result, compatibility claim, security claim, accessibility claim, performance claim, or production claim changed. PB-002 remains blocked and PB-020 remains partial.

## 2026-07-19 - Reference platform support scorecard made executable

Question:

Can the deferred `PB-006` reference desktop platform choice be made comparable and source-backed without selecting Windows, macOS, or Linux or treating CI availability and platform API documentation as support evidence?

Method:

Compared the Native Platform and Browser Chrome Engineering Book, the platform window/input/IME/accessibility/packaging chapters, the native UI and accessibility closure route, the fresh-host, sandbox, benchmark, package/update, and incident-response closure routes, and official Rust, GitHub, Microsoft, Apple, Wayland, and XDG Desktop Portal sources. Added a no-claim scorecard with eight source records, eleven evidence dimensions, three candidate rows, open questions, unsupported cases, and an `xtask check` validator.

Decision:

Keep Windows x64, macOS arm64, and Linux Wayland x64 as unselected planning candidates. Require platform identity, clean-host reproduction, native workflow execution, accessibility, graphics, sandbox, packaging, recovery, fixed-hardware resource evidence, support ownership, incident capacity, and owner review before any selection or support claim.

Impact:

`PB-006` remains `not_selected`; no platform selection, supported-platform, compatibility, accessibility, security, performance, release, production, or implementation claim changed.

## 2026-07-19 - Profile/session source identity made executable

Question:

Can the official WHATWG Storage, W3C IndexedDB, Clear-Site-Data, and security/privacy observations used by `PB-016` be tracked as stable inputs without treating web-platform semantics as a Turing profile format, migration protocol, or data-safety result?

Method:

Compared the Profile and Session Data-Lifecycle Decision Preparation, Profile/Session Execution and Data-Safety Closure Preparation, Profile Session Format Inventory, storage books, and official WHATWG/W3C sources. Added a no-claim manifest with four source records, nine evidence axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep origin/partition identity, storage buckets/state classes, transaction durability, abort/quota behavior, origin clearing, browser-owned state separation, migration/recovery, privacy/export, and unsupported cases as separate evidence axes. No profile format, migration protocol, credential vault, sync design, or durability policy is selected.

Impact:

`PB-016` remains partial; no profile/session implementation, migration, durability, privacy, credential, sync, data-loss, production, or implementation claim changed.

## 2026-07-19 - Ownership and two-person-control source identity made executable

Question:

Can official NIST governance/separation-of-duties and GitHub CODEOWNERS/protected-branch observations be tracked as stable `PB-019`/`PB-020` inputs without treating routing or policy documentation as qualified-backup or authority evidence?

Method:

Compared the Backup Ownership and Review Capacity Decision Preparation, Backup-Ownership Execution and Two-Person-Control Closure Preparation, Backup Ownership Gap Inventory, ownership/review books, repository `CODEOWNERS`, and official NIST and GitHub governance documentation. Added a no-claim manifest with five source records, eight evidence axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep roles and authority, separation of duties, qualification/path coverage, CODEOWNERS routing, effective branch rules/bypass, access reconciliation, succession/replacement, and independent review/expiry as separate evidence axes. No backup is named, no access configuration is captured, and no two-person-control or closure decision is made.

Impact:

`PB-019` remains blocked and `PB-020` remains unresolved; no owner coverage, release, signing, disclosure, legal, incident-closure, production, or implementation claim changed.

## 2026-07-19 - Incident-response source identity made executable

Question:

Can the official NIST SP 800-61r3, FIRST CVSS v4.0, and CISA coordinated-disclosure observations used by `PB-018` be tracked as stable incident-response inputs without treating guidance as a Turing incident program or authority decision?

Method:

Compared the Incident Response and Emergency Patch Decision Preparation, Incident-Response Execution and Disclosure Closure Preparation, Incident Patch Rehearsal Inventory, security/release response books, and official NIST, FIRST, and CISA sources. Added a no-claim manifest with six source records, nine evidence axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep incident lifecycle, severity and uncertainty, impact scope, containment and custody, patch/recovery, disclosure, authority separation, privacy/retention, and timing/capacity review as separate evidence axes. No severity policy, disclosure process, incident authority, patch channel, supported-security policy, or readiness decision is selected.

Impact:

`PB-018` remains partial; no incident execution, emergency patch, disclosure, signing, stable-promotion, supported-security, production, or implementation claim changed.

## 2026-07-19 - Package/update source identity made executable

Question:

Can the official TUF, SLSA, in-toto, and Sigstore observations already used by `PB-017` be tracked as stable release-operation inputs without treating framework documentation as an updater, signing, rollback, migration, or release decision?

Method:

Compared the Package, Update Trust, and Recovery Decision Preparation, Package/Update Execution and Release-Safety Closure Preparation, research package/update lab inventory, release-operations books, and official TUF, SLSA, in-toto, and Sigstore sources. Added a no-claim manifest with seven source records, eight evidence axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep metadata roles/thresholds/freshness, target binding/rollback, build provenance, authorized supply-chain steps, signing/transparency, installation recovery, profile transitions, and privacy/claim review as separate evidence axes. No package/update framework, package format, signing hierarchy, updater, channel, or release policy is selected.

Impact:

`PB-017` remains partial; no package/update execution, rollback or migration result, release readiness, supported-security, production, or implementation claim changed.

## 2026-07-19 - Accessibility platform source identity made executable

Question:

Can the official Windows UI Automation, Apple Accessibility, and Linux AT-SPI observations be tracked as stable native UI inputs without treating platform API documentation as accessibility readiness or Nova implementation proof?

Method:

Compared the Native UI and Accessibility Closure Preparation, Window Input Accessibility Spike Inventory, accessibility platform bridge/testing books, UI runtime accessibility guidance, Nova design-lab boundary, and official platform sources. Added a no-claim manifest with four source records, three platforms, nine evidence axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep platform/API/client identity, tree snapshots, role/state/action semantics, focus/events, screen-reader transcripts, IME/text, page-tree composition, timing/failure denominators, and unsupported cases as separate evidence requirements. Nova remains visual authority only.

Impact:

`PB-003`, `PB-005`, and `PB-015` remain partial; no toolkit selection, native adapter, accessibility readiness, UI-gate, release-path, performance, or implementation claim changed.

## 2026-07-19 - Benchmark source identity made executable

Question:

Can the official BrowserBench, Chromium, Web Platform Tests, and vendor-performance observations be tracked as stable `PB-013` inputs without treating methodology or vendor context as a Turing benchmark result?

Method:

Compared the Chrome-Class Performance Runbook, Benchmark Evidence and Claim Closure Preparation, performance readiness packet, benchmark-lab readiness lane, and the official suite, telemetry, regression-policy, compatibility, and vendor-context sources. Added a no-claim manifest with eight source records, ten measurement axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep suite identity, workload integrity, harness controls, statistics, hardware/OS, browser pins, trace artifacts, failure denominator, equal security/lifecycle, and claim expiry as separate evidence axes. Vendor-reported scores remain dated context, not Turing results or universal targets.

Impact:

`PB-013` remains partial; no browser benchmark, competitor comparison, fastest/lower-memory/lower-energy, Chrome-class, or public performance claim changed.

## 2026-07-19 - IPC wire-source identity made executable

Question:

Can the current CBOR, Protocol Buffers, and FlatBuffers research be tracked as stable `PB-011` inputs without treating external format specifications as a codec selection, transport proof, or production IPC approval?

Method:

Compared the IPC Wire-Encoding Decision Preparation, IPC Transport and Authority Closure Preparation, IPC capability inventory, system architecture, security model, and the official IETF, Protocol Buffers, and FlatBuffers sources. Added a no-claim manifest with five source records, nine wire-safety axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep deterministic encoding, bounds/allocation, evolution, unknown values, generated provenance, fuzzability, platform authentication, resource cost, and cross-language maintenance as separate decision axes. No codec or generator is selected.

Impact:

`PB-011` remains partial; no wire-format, generator, transport, renderer-security, process-isolation, production IPC, performance, or implementation claim changed.

## 2026-07-19 - Fresh-host toolchain source identity made executable

Question:

Can the official Rustup, Cargo, and Microsoft toolchain observations already documented for `PB-008`/`PB-009` be tracked as stable run-record inputs without treating them as independent reproduction or readiness evidence?

Method:

Compared the Fresh-Host Toolchain Reproduction Closure Preparation, Fresh Host Reproduction Inventory, build-information ledger, fresh-host registry, and official Rustup, Cargo, and Microsoft documentation. Added a no-claim manifest with three source records, nine evidence axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep exact compiler identity, target tuple, lockfile/network mode, SDK/linker details, cache controls, host independence, source-tree state, command denominator, and retained evidence as separate run-record facts. The source manifest cannot substitute for a real run or owner review.

Impact:

`PB-008` and `PB-009` remain partial; no independent reproduction, compiler/SDK/linker equivalence, release confidence, production, Chrome-class, or implementation claim changed.

## 2026-07-19 - ADR-0009 upstream source observations made executable

Question:

Can current official Servo source and build guidance be tracked as stable ADR-0009/PB-002 observations without treating public documentation as a source selection, equivalence proof, or dependency approval?

Method:

Compared the official Servo repository, Servo Book source/build/dependency guidance, the January 2026 Servo update on pinned Git dependencies, the existing source-strategy inventory, ADR-0009 closure route, and evidence matrix. Added a no-claim manifest with five source records, seven observation axes, source-document links, unsupported boundaries, and an `xtask check` validator.

Decision:

Keep Git trees, vendored source archives, platform bootstrap inputs, prebuilt native artifacts, and lockfile-pinned dependencies as separate source-strategy inputs requiring explicit equivalence, provenance, legal, and owner-review decisions.

Impact:

PB-002 and ADR-0009 remain blocked with no source baseline, dependency approval, source import, compatibility, performance, security, production, or release-code claim. The source-strategy lane is now machine-tracked against upstream observation drift.

## 2026-07-19 - Sandbox platform source identity made executable

Question:

Can the official Windows, Linux, and macOS sandbox source observations be tracked as a stable machine-checked PB-012 input without treating platform documentation as Turing containment evidence?

Method:

Compared the Sandbox Platform-Evidence Decision Preparation report, Sandbox Probe Inventory, security-engine sandbox book, official source URLs, and the PB-012 evidence matrix. Added a no-claim manifest with six source records, three platforms, nine evidence axes, source-document links, and unsupported boundaries, plus a validator wired into xtask check.

Decision:

Treat the manifest as source identity and evidence-axis tracking only. Effective OS policy, packaged expected-deny results, broker fixtures, compromised-client tests, and owner review remain required.

Impact:

Platform research is now machine-tracked and cannot silently lose a platform, source, or evidence axis. PB-012 remains partial; no sandbox, renderer-security, site-isolation, hostile-browsing, production-safety, security-gate, or implementation claim changed.

## 2026-07-19 - Nova coverage added to primary handoff surfaces

Question:

Can a new maintainer discover the complete Nova component-coverage state from the primary start guide and pre-build checklist without reading the design-lab history first?

Method:

Compared the current 15-surface component-fixture inventory and Nova Surface-to-Contract Map with the native UI status paragraphs in `docs/start-here.md` and `docs/project-buildout/11-pre-build-readiness-checklist.md`.

Decision:

Updated both primary handoff surfaces to name the 9 core shell surfaces plus 6 Nova-specific product groups and linked the Nova map from Start Here. The language remains explicitly no-claim and keeps executable fixtures, accessibility evidence, and UI gates as future proof.

Impact:

Nova design coverage is now discoverable from the main continuation path as well as the UI-runtime book. No readiness percentage, gate, toolkit, or implementation claim changed.

## 2026-07-19 - Nova source manifest and coverage wording synchronized

Question:

Do the human-facing Nova design records agree with the committed source hash, repository line-ending policy, and expanded 15-surface component inventory?

Method:

Compared the design-lab README, design-source manifest, source file bytes, component-fixture inventory, Nova surface map, and native UI research record. The source manifest validator confirmed the committed SHA-256, byte length, and line count; a repository search found stale pre-normalization hash and nine-surface wording in the README and research method.

Decision:

Updated the README to state the LF normalization explicitly, display the committed SHA-256, and describe the contract map as covering existing, newly represented, and still-unproven contracts. Updated the research method to describe the complete 15-surface inventory.

Impact:

Human and machine records now agree on Nova source identity and surface coverage. No UI implementation, toolkit, accessibility, security, release, or readiness claim changed.

## 2026-07-19 - Nova surface contracts expanded

Question:

Can the six Nova surface groups previously identified as missing from the native component inventory be represented in the same checked, no-claim contract system before implementation begins?

Method:

Compared the Nova source surface map with the component-fixture schema and validator, then added records for Shield, password vault/autofill, DevTools, history/bookmarks/reading/downloads/extensions, split/reader/capture/find tools, and agent activity. Each record carries states, commands, all required fixture axes, accessibility obligations, and an explicit authority boundary.

Decision:

Expanded `component-fixture-inventory.json` from 9 to 15 component surfaces and synchronized the Nova surface map, UI Runtime book, and component-fixture research record. Kept the inventory at no-claim planning status; visual presence and contract presence do not equal implementation, accessibility readiness, security readiness, or release approval.

Impact:

Nova now has machine-checked planning coverage for the full identified surface delta. Remaining proof is executable native fixtures, page-surface/protocol integration, storage/credential/agent/security behavior, accessibility evidence, and owner review. `PB-014`, the native UI gates, and the 90% contained-M0 / 0% full-build documentation measures remain unchanged.

## 2026-07-19 - Chrome-class benchmark source refresh

Question:

Does the Chrome-class and extreme-performance lane still reflect the current benchmark versions, competitor context, regression policy, and compatibility-test limitations that a future build must preserve?

Method:

Checked the official BrowserBench MotionMark and WPT documentation, the JetStream 3.0 release announcement, Google's current Chrome Speedometer 3.1/JetStream 3 announcement, and Chromium's competitive-benchmark regression policy on 2026-07-19. Compared those observations with the existing performance Blueprint, benchmark-lab contracts, competitor runbook, and no-claim registries.

Decision:

Recorded JetStream 3.0 as the current pinned compute-suite version, recorded Google's M5/macOS 26.0.1 scores as dated vendor context only, adopted regression detection as an engineering control without adopting vendor claims, and retained the requirement for exact suite revisions, failure denominators, equal security/lifecycle settings, raw artifacts, and independent review. WPT browser-in-browser limitations remain explicit for crash/hang coverage.

Impact:

The performance lane is better aligned with current primary-source observations while its claim boundary remains unchanged: `PB-013` is still no-claim and no Turing performance, Chrome-class, compatibility, memory, energy, or production claim was created.

## 2026-07-19 - Nova design-source identity made executable

Question:

Can the supplied Nova visual/layout source be protected from silent drift while remaining explicitly outside the trusted browser runtime?

Method:

Recorded the supplied artifact's exact repository path, SHA-256, byte length, line count, capture date, surface inventory, and visual/behavioral authority split. Added a machine-readable manifest and schema plus a validator that recomputes the file hash and size/count invariants.

Decision:

Wired `tools/validate_design_source.py` into `xtask check` and documented the manifest in the UI runtime book, design-lab README, repository map, and documentation-readiness evidence matrix.

Impact:

The Nova design reference is now an integrity-checked handoff artifact. Drift fails validation, while the no-React-in-trusted-chrome boundary remains unchanged and no UI toolkit or readiness gate is promoted.

## 2026-07-19 - Nova surface contract delta

Question:

Which Nova surfaces already have toolkit-neutral component contracts, and which visual surfaces must be added before native UI implementation can claim complete design coverage?

Method:

Compared the Nova manifest surface inventory with `component-fixture-inventory.json`, page-surface composition, and window/input/accessibility registries. Core shell, tabs, Spaces, command field, permissions, agent confirmation, resource manager, settings, and recovery were already represented; Shield, vault, DevTools, history/bookmarks/reading/downloads/extensions, split/reader/capture/find, and richer agent surfaces were not distinct component records.

Decision:

Added the no-claim [Nova Surface-to-Contract Map](ui-runtime/design-lab/surface-contract-map.md), separating covered contracts from missing component work and linking each gap to its primary `PB-*` gates and required evidence.

Impact:

The Nova reference now has an explicit implementation delta. Visual presence is no longer ambiguous with component-contract coverage, and no UI readiness or product claim changed.

## 2026-07-19 - Nova browser-face design source adopted

Question:

How should the supplied React browser concept become the primary visual/layout reference without violating Turing's native trusted-chrome boundary?

Method:

Inspected the supplied 7,727-line `Nova` JSX concept shell, including its chrome, tabs, address field, side panels, settings, history, downloads, extensions, Shield, vault, agent, DevTools, resource, theme, density, and motion surfaces. Compared its role with the existing React design-lab policy, toolkit-neutral UI contracts, component-fixture inventory, page-surface boundary, and native UI readiness gates.

Decision:

Preserved the supplied source verbatim at `docs/ui-runtime/design-lab/turing-nova-design-source.jsx`, recorded its SHA-256, and made it the current primary visual/layout reference. Added a design-lab README defining visual authority, native behavioral authority, extraction steps, and claim boundaries. No UI toolkit or release runtime was selected.

Impact:

Future native UI work now has one explicit visual baseline for layout and surface coverage while retaining Rust/native contracts as the authority for behavior, security, accessibility implementation, and release architecture. `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `PB-020` remain unresolved.

## 2026-07-19 - Research-index invariant made executable

Question:

Can the repository enforce its rule that every durable research artifact is indexed and every local Markdown link in the research index resolves?

Method:

Compared the 98 Markdown artifacts under `docs/research/` with the local Markdown links in `docs/research/README.md`, then encoded that comparison in `tools/validate_research_index.py`. The validator excludes the index itself, rejects orphaned research Markdown files, rejects stale local Markdown links, and reports the checked counts.

Decision:

Added the focused research-index validator, wired it into `xtask check`, documented it in the research index and documentation-readiness evidence matrix, and added it to the repository map.

Impact:

Research-index completeness is now an aggregate-check invariant. This improves navigation and stop/resume continuity without changing any gate, task, readiness percentage, research conclusion, or product claim.

## 2026-07-19 - Benchmark handoff freshness correction

Question:

Does the benchmark engine baseline handoff map carry the same current date as the benchmark runbook and closure route it summarizes?

Method:

Compared the benchmark research index, performance runbook, benchmark closure preparation, engine-baseline readiness map, machine manifests, and current documentation-readiness records. The map's evidence and no-claim boundaries were current, but its `Map date` remained 2026-07-18.

Decision:

Updated the benchmark engine baseline readiness map date to 2026-07-19. Historical source observations and the recorded source snapshot were not rewritten.

Impact:

The benchmark lane's current stop/resume map now agrees with the current runbook and closure-report freshness. This changes no benchmark status, browser result, claim, or readiness gate.

## 2026-07-19 - IPC closure freshness correction

Question:

Does the IPC closure route carry the same explicit freshness marker as the other nine PB-020 lane closure reports?

Method:

Compared all ten lane closure-report headers after the canonical handoff freshness correction. The IPC report was the only remaining lane without a `Research date` field; its source and execution boundaries were already documented, so no evidence or status change was required.

Decision:

Added `Research date: 2026-07-19` to the IPC transport and authority closure report. No gate, task, readiness, percentage, or claim state changed.

Impact:

All ten PB-020 closure lanes now expose an explicit freshness marker for stop/resume review. The machine audit remains 9/10 contained-M0 criteria and 0/10 full-goal criteria.

## 2026-07-19 - Canonical handoff freshness correction

Question:

Do current ADR and Chrome-class traceability handoffs describe the same repository date as the machine audit and progress snapshot?

Method:

Searched current entrypoints, owner-decision records, closure routes, the ADR-0009 decision draft, and the Chrome-class capability traceability map for stale July 18 freshness statements. Historical research observations were left unchanged; only current handoff documents whose text claimed repository currency were evaluated for correction.

Decision:

Updated the ADR-0009 decision draft and Chrome-class capability traceability map to 2026-07-19, including the map's repository-current statement. No gate, readiness, percentage, or product claim changed.

Impact:

Current canonical handoff material now agrees on the audit date and does not imply that the July 18 snapshot is still the latest repository state. Historical observations remain explicitly historical.

## 2026-07-19 - Closure-report freshness normalization

Question:

Do all ten PB-020 lane closure reports expose an explicit current research date for stop/resume review?

Method:

Compared the ten closure-report headers and the incident-response and backup-ownership decision-preparation reports against the documentation-readiness audit routes. The incident and backup lanes already carried current source-backed retrieval dates and execution-report research dates; the ADR-0009 and benchmark closure reports were the remaining closure reports without an explicit research-date field.

Decision:

Added `Research date: 2026-07-19` to the ADR-0009 source-strategy and benchmark-evidence closure reports. No gate status, percentage, claim, or readiness state changed.

Impact:

All ten lane closure reports now expose a consistent freshness marker for handoff and stop/resume review. The machine audit remains authoritative for the unchanged 90% contained-M0 and 0% full-build measures.

## 2026-07-19 - Cross-lane freshness and status consistency audit

Question:

Do the canonical continuation reports and ADR-0009 traceability matrix expose current research dates after the latest documentation changes?

Method:

Searched the root entry points, documentation indexes, progress snapshot, completion audit, ADR-0009 matrix, machine registries, and lane closure reports for stale July 17/18 dates, progress values, readiness statuses, and `PB-020` boundaries. Confirmed the only semantic drift in the touched routes was the ADR-0009 matrix date; the lane closure reports also lacked explicit research-date fields.

Decision:

Updated the ADR-0009 matrix to 2026-07-19 and added explicit research dates to the fresh-host, sandbox, and native UI/accessibility closure reports. No status, percentage, gate, or claim boundary was changed.

Impact:

The current stop/resume records now distinguish dated source observations from older evidence captures. The machine audit remains authoritative for the unchanged 90% contained-M0 and 0% full-build measures.

## 2026-07-19 - Package/update source-boundary carry-forward

Question:

Does the `PB-017` executable closure route preserve the distinction between update metadata trust, build provenance, artifact signing, installation recovery, profile migration, and support policy?

Method:

Compared the package/update closure route with the dated source-backed TUF, SLSA, in-toto, and Sigstore decision-preparation report and its primary source links.

Decision:

Added a source-boundary table to the package/update closure route. Future fake-key lab packets must identify which source role supports each assertion and must not infer update authorization, migration safety, or support status from a signature or provenance record alone.

Impact:

The package/update handoff now carries the source interpretation into the execution packet. No updater, package format, signing authority, rollback safety, migration safety, or release claim exists.

## 2026-07-19 - Accessibility platform-source and assistive-technology controls

Question:

Does the native UI closure route distinguish an internal semantic model from a real platform accessibility and assistive-technology result?

Method:

Checked official Windows accessibility/UI Automation, Apple accessibility, and AT-SPI 2 documentation on 2026-07-19. Compared their platform tree, action, event, runtime-version, and assistive-technology requirements with the native UI closure route.

Decision:

Added a primary-source observation table requiring platform/API/runtime identity, tree and action snapshots, focus/live-region/event records, manual assistive-technology transcripts, timeout behavior, and unsupported-case accounting for Windows, macOS, and Linux.

Impact:

The accessibility documentation now prevents a screenshot, semantic model, automated checker, or one-platform result from being treated as cross-platform accessibility readiness. No UI-gate result, accessibility run, toolkit selection, or release-path claim exists.

## 2026-07-19 - Sandbox platform semantics and evidence boundaries

Question:

Does the `PB-012` sandbox closure route prevent a single primitive or platform result from being generalized into cross-platform containment?

Method:

Retrieved official Windows AppContainer, Apple App Sandbox, Linux seccomp, and Linux Landlock documentation on 2026-07-19. Compared their stated isolation models, runtime state, and limitations with the checked sandbox probe package and readiness-review contracts.

Decision:

Added a platform-source observation table requiring effective token/capability/entitlement state, package and signature identity, seccomp filter and architecture state, Landlock kernel/ABI and ruleset state, broker relationship, and explicit degraded/unsupported outcomes.

Impact:

The sandbox documentation now distinguishes platform-specific mechanisms and prevents syscall filtering, requested policy, or one-platform evidence from being treated as complete cross-platform containment. No probe run, security-gate promotion, or sandbox readiness claim exists.

## 2026-07-19 - Fresh-host toolchain source controls

Question:

Does the `PB-008`/`PB-009` fresh-host run contract distinguish dependency locking from compiler and native-toolchain identity?

Method:

Retrieved the official Rustup toolchain documentation, Cargo build documentation, and Microsoft C++ Build Tools documentation on 2026-07-19. Compared their version/channel, lockfile, offline, side-by-side-toolset, and servicing semantics with the fresh-host closure route.

Decision:

Added a primary-source observation table requiring exact Rustup toolchain and target identity, lockfile/cache/network-mode records for `cargo --locked` and offline runs, and Visual Studio/MSVC/Windows SDK/component/channel/toolset identity. Added the sources to the canonical bibliography.

Impact:

The fresh-host evidence contract now prevents a successful locked Cargo command or generic "Visual Studio installed" statement from being mistaken for complete environment reproducibility. No fresh-host run or readiness promotion exists.

## 2026-07-19 - Compatibility source-baseline traceability synchronization

Question:

Can a maintainer discover the WPT source-pin requirement from the bibliography and ADR-0009 decision records, not only from the detailed compatibility report?

Method:

Compared the compatibility report's 2026-07-19 source retrieval record with the primary-source bibliography, the ADR-0009 evidence registry, and the evidence traceability matrix.

Decision:

Added the dated compatibility report to the bibliography route, added the exact WPT commit/manifest/denominator requirement to `ADR9-EV-013` missing outputs, and added the same rule to the matrix acceptance checks. Test262 remains separately attributed and pinned in the report.

Impact:

The source-control gap is now visible from the research, bibliography, and decision-traceability entry points. The evidence remains partial and no compatibility or Chrome-class claim is created.

## 2026-07-19 - Compatibility source-baseline retrieval record

Question:

Does the `ADR9-EV-013` compatibility route identify reproducible upstream WPT and Test262 sources before any browser result is compared?

Method:

Inspected the external Servo checkout at commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, its WPT `config.ini`, and `tests/wpt/tests/third_party/test262/vendored.toml` on 2026-07-19. Cross-checked the official WPT repository at `https://github.com/web-platform-tests/wpt` and the official TC39 Test262 project at `https://github.com/tc39/test262`.

Decision:

Recorded that Test262 is pinned to `b66872a92487694396fb082343e08dd7cca5ddf4`, while the inspected WPT configuration uses the older `w3c/web-platform-tests.git` remote and moving `master` branch. Added an explicit requirement to pin the WPT commit and preserve retrieval, local patch, manifest, and denominator metadata before a WPT run can support `ADR-0009`.

Impact:

The compatibility documentation now distinguishes source ownership, source reproducibility, and test results. No WPT/Test262 run, compatibility result, source approval, or Chrome-class claim exists.

## 2026-07-19 - Benchmark primary-source retrieval record

Question:

Does the canonical `PB-013` closure route preserve dated, reproducible observations from the primary benchmark and tracing sources it cites?

Method:

Retrieved the official Speedometer 3.1 instructions/about page, Chromium Catapult Telemetry documentation at observed revision `c5f59e09450378c12dfae7f14fbffc07204e1f78`, local Telemetry run instructions, and Microsoft Windows Performance Recorder documentation on 2026-07-19.

Decision:

Added a source-observation table covering clean-profile/focus/thermal controls, browser-runner and trace separation, exact executable/repeat inputs, and Windows ETW artifact handling. Marked mutable source references as inputs that must be pinned before L1/L2 execution.

Impact:

The benchmark research is more reproducible as a planning record, but no browser run, competitor result, owner review, benchmark readiness, performance claim, or Chrome-class claim exists.

## 2026-07-19 - Central owner-review template closure invariant

Question:

Can any owner-review template lose its lane closure route while the central documentation-readiness audit still passes?

Method:

Added a central mapping for the ten no-claim owner-review templates covering ADR-0009, fresh-host, IPC, sandbox, benchmark, native UI, profile/session, package/update, incident response, and backup ownership. The validator now requires each template in both source lists and checks its `source_records` for the corresponding closure-preparation route.

Decision:

The owner-review templates are now machine-checked as part of the documentation-readiness closure chain. The ADR-0009 template also now names its source-strategy closure route.

Impact:

Template existence, schema validity, and route attachment are separated and all three are checked. This improves continuation integrity only; no owner decision, readiness promotion, task approval, implementation, performance, compatibility, security, accessibility, production, release, or Chrome-class status changed.

## 2026-07-19 - Lane readiness-template closure-route synchronization

Question:

Do the no-claim readiness-review templates for native UI, profile/session, package/update, incident response, backup ownership, fresh-host, IPC, and sandbox name their canonical closure-preparation routes?

Method:

Compared each template's `source_records` with the research index, owner-decision board, documentation-readiness evidence matrix, and the corresponding closure-preparation document.

Decision:

Added the missing closure-preparation route to all eight readiness-review templates, refreshed the older template dates, and added incident-response and sandbox closure routes to the security-engine book's navigation and boundary text.

Impact:

Every lane's human research index and machine readiness template now point to the same evidence-order handoff. The templates remain no-claim; no owner decision, readiness promotion, task approval, implementation, performance, compatibility, security, accessibility, production, release, or Chrome-class status changed.

## 2026-07-19 - Benchmark closure-route source synchronization

Question:

Does the checked `PB-013` benchmark readiness-review template name the same canonical closure route used by the benchmark lane map and evidence matrix?

Method:

Compared the benchmark laboratory index, performance readiness packet, Chrome-class performance lane map, evidence matrix, benchmark readiness-review template, and benchmark closure-preparation report.

Decision:

Added the benchmark closure-preparation report to the readiness-review template source records, refreshed its review date, and linked it from the benchmark laboratory book and performance packet.

Impact:

The benchmark handoff is now discoverable from both human and machine readiness records. The template remains no-claim and does not provide benchmark results, performance claims, Chrome-class claims, owner approval, or implementation readiness.

## 2026-07-19 - Final closure-route chain invariant

Question:

Does every lane-specific closure route link the complete chain from its local gate to the Owner Decision Closure Board and the final build-readiness closure route?

Method:

Checked all ten routes for the board link and final `build-readiness-closure-and-owner-decision-preparation-2026-07.md` handoff. Extended the documentation-readiness validator and evidence matrix to require `PB-020`, the board, and the final closure route in every referenced lane document.

Decision:

All ten routes pass the complete-chain invariant. No gate, task, owner decision, production, release, performance, compatibility, security, accessibility, or implementation status changed.

Impact:

Repository navigation already exposes all ten closure routes through the research index and the relevant top-level/project-buildout maps. Updated `docs/repository-map.md` so its validator inventory and machine-registry row also describe the ten-route semantic handoff invariant; no readiness or implementation status changed.

## 2026-07-19 - Build-information ledger source synchronization

Question:

Does the build-information gap ledger name the same canonical lane closure routes as the documentation-readiness audit?

Method:

Compared the ledger's machine `source_records` and research method references with the ten-route closure chain enforced by `validate_documentation_readiness_completion_audit.py`.

Decision:

Updated the ledger review date and added all ten lane-specific closure-preparation documents as source records and research references.

Impact:

The ledger remains a no-claim gap map: it is more complete and current as a continuation record, but no owner decision, readiness promotion, task approval, implementation, performance, compatibility, security, accessibility, production, release, or Chrome-class status changed.

## 2026-07-19 - Implementation-plan readiness handoff synchronization

Question:

Does the canonical implementation master plan appear in the documentation-readiness audit and route implementers through the current pre-build closure records?

Method:

Compared the implementation-plan entrypoint, documentation-readiness audit source records, build-information ledger sources, and the current ten-route closure handoff.

Decision:

Added the implementation-plan README to the audit source records, refreshed its review date, and added a pre-build readiness handoff linking the audit, gap ledger, owner board, and final closure route.

Impact:

Implementers now encounter the same contained-M0 boundary and owner-decision stop path before reading milestone playbooks. No task approval, readiness promotion, implementation, performance, compatibility, security, accessibility, production, release, or Chrome-class status changed.

## 2026-07-19 - Implementation-plan handoff validator invariant

Question:

Can the implementation plan lose its pre-build readiness handoff while the documentation-readiness audit and closure template still appear structurally valid?

Method:

Extended `validate_documentation_readiness_completion_audit.py` so both the audit and no-claim closure-review source lists must include the implementation-plan README, and its text must name the audit, build-information ledger, Owner Decision Closure Board, and final closure route.

Decision:

The implementation plan is now part of the machine-checked readiness handoff rather than only a prose cross-reference.

Impact:

Removing or detaching the implementation-plan stop/resume handoff will fail validation. This strengthens documentation continuity only; no readiness, task, owner, implementation, performance, compatibility, security, accessibility, production, release, or Chrome-class status changed.

The continuation graph now rejects both missing route records and detached lane documents, preserving a single final closure path for future maintainers.

Next question:

Can a real owner-reviewed closure packet replace the no-claim records without breaking the same route-chain and claim-boundary invariants?

## 2026-07-19 - Lane closure semantic handoff invariant

Question:

Does each lane-specific closure-preparation document explicitly identify both `PB-020` and the owner-decision closure board, rather than merely existing in a source-record list?

Method:

Checked all ten closure-preparation routes. Found detached wording in source strategy, fresh-host, and benchmark routes, added explicit `PB-020` closure-dependency sections, and extended `validate_documentation_readiness_completion_audit.py` to require the semantic terms in every route referenced by both the audit and closure template.

Decision:

All ten routes now pass the semantic handoff invariant. No gate, task, owner decision, production, release, performance, compatibility, security, accessibility, or implementation status changed.

Impact:

Future edits cannot leave a lane-specific closure document detached from the central owner-decision boundary while still passing documentation-readiness validation.

Next question:

Can a future real closure packet preserve these route-level handoffs alongside exact evidence, digests, owner review, exceptions, and synchronized registry updates?

## 2026-07-19 - Global documentation closure-route semantic audit

Question:

Does the global documentation-readiness audit directly track every lane-specific closure route and preserve one consistent contained-M0 versus full-build status without stale or duplicate guidance?

Method:

Compared the machine documentation-readiness audit, human audit, progress snapshot, evidence matrix, owner-decision closure board, closure-preparation route, root and index stop/resume maps, research crosswalk, and all ten lane-specific closure-preparation documents. Added the ten route files to the machine audit source list and removed a duplicated drift-trigger line in the evidence matrix.

Decision:

The audit remains `9/10 ready_for_contained_m0`, `0/10 ready_for_full_goal`, with all five full-goal blocker groups unresolved. No readiness, task, production, Chrome-class, performance, compatibility, security, accessibility, release, or implementation claim changed.

Impact:

The central documentation audit now has direct source-record traceability to each lane closure route, making future semantic drift easier to detect during continuation.

Next question:

Do the final validators and aggregate check continue to prove that the expanded source list, percentages, blocker groups, closure board, crosswalk, indexes, and lane routes remain synchronized?

## 2026-07-19 - Backup ownership and PB-020 closure routing

Question:

Does the backup-ownership lane explicitly reconcile qualified coverage, access control, two-person actions, exceptions, and closure authority with final `PB-020` review?

Method:

Compared the backup-ownership execution and two-person-control closure route, source-backed review-capacity preparation, gap inventory, qualification and readiness templates, `TASK-000008`, ownership baseline, owner-decision board, and pre-build readiness records. Added explicit PB-020 reconciliation language and board links, updated the no-claim readiness template date, and preserved the primary-only/null-backup blocker, access, independence, and production-authority boundaries.

Decision:

No ownership or closure gate changed status. Named candidates, qualification records, access reconciliation, CODEOWNERS, review rules, and two-person exercises remain evidence inputs and cannot independently grant release, signing, disclosure, legal, incident-closure, migration, production, or broad-build authority.

Impact:

Backup ownership now has the same final owner-closure handoff as source strategy, IPC, sandbox, benchmark, native UI, profile/session, package/update, and incident-response lanes.

Next question:

Can a real `TASK-000008` evidence packet prove qualified backup coverage, independence, least-privilege access, two-person control, emergency replacement, and PB-020 synchronization without relying on placeholders or intent?

## 2026-07-19 - Incident response PB-020 closure routing

Question:

Does the incident-response lane explicitly reconcile private intake, containment, patch, disclosure, signing, support, and closure decisions with final `PB-020` closure?

Method:

Compared the incident-response execution and disclosure closure route, source-backed emergency-patch decision preparation, rehearsal inventory, packet and readiness templates, `TASK-000010`, security-engine book, owner-decision board, and pre-build readiness records. Added explicit PB-020 reconciliation language and board links, updated the no-claim readiness template date, and preserved private-intake, human-authority, disclosure, signing, supported-security, and production-safety boundaries.

Decision:

No incident-response gate changed status. A tabletop, emergency-patch dry run, disclosure rehearsal, or readiness review remains lane evidence and cannot independently authorize signing, stable promotion, supported-security coverage, incident closure, production-safe browsing, or broad implementation.

Impact:

Incident response now has the same final owner-closure handoff as source strategy, IPC, sandbox, benchmark, native UI, profile/session, package/update, and ownership lanes.

Next question:

Can a real `TASK-000010` evidence packet preserve private handling, authority separation, timing and failure denominators, patch and recovery proof, disclosure controls, and PB-020 synchronization under independent review?

## 2026-07-19 - Package/update PB-020 closure routing

Question:

Does the package/update lane explicitly reconcile package identity, metadata trust, signing, rollback, migration, and release decisions with final `PB-020` closure?

Method:

Compared the package/update execution and release-safety closure route, source-backed trust and recovery preparation, lab inventory, fake-key packet and readiness templates, `TASK-000009`, release-operations book, owner-decision board, and pre-build readiness records. Added explicit PB-020 reconciliation language, updated the no-claim readiness template date, and preserved production-key, stable-channel, public-distribution, real-profile, and supported-security boundaries.

Decision:

No package/update gate changed status. Lab results, metadata contracts, rollback rehearsals, and release-operations review remain lane evidence and cannot independently authorize production signing, stable distribution, public release, migration safety, release readiness, or broad implementation.

Impact:

Package/update now has the same final owner-closure handoff as source strategy, IPC, sandbox, benchmark, native UI, profile/session, incident, and ownership lanes.

Next question:

Can a real `TASK-000009` evidence packet preserve exact source/build/artifact identity, key separation, freshness and target checks, fault denominators, authorized rollback, and PB-020 synchronization under independent review?

## 2026-07-19 - Profile/session PB-020 closure routing

Question:

Does the profile/session data-safety lane explicitly reconcile schema, migration, privacy, recovery, and real-profile decisions with final `PB-020` closure?

Method:

Compared the profile/session execution and data-safety closure route, lifecycle decision preparation, format inventory, schema-package and readiness-review templates, `TASK-000007`, storage book, owner-decision board, and pre-build readiness records. Added explicit PB-020 reconciliation language, updated the no-claim readiness template date, and preserved the synthetic-fixture, privacy, failure-denominator, and no-production boundaries.

Decision:

No profile/session gate changed status. Executable schemas, migration tests, privacy review, recovery accounting, or a reviewed packet remain lane evidence and cannot independently authorize real-profile behavior, production formats, data-loss safety, release paths, or broad implementation.

Impact:

Profile/session now has the same final owner-closure handoff as source strategy, IPC, sandbox, benchmark, native UI, package/update, incident, and ownership lanes.

Next question:

Can a real `TASK-000007` evidence packet preserve state-class identity, synthetic-fixture isolation, migration rollback, private-session exclusion, protected-work recovery, and PB-020 synchronization under independent review?

## 2026-07-19 - Native UI and accessibility PB-020 closure routing

Question:

Does the native UI and accessibility lane explicitly reconcile its toolkit, page-surface, accessibility, and UI-gate decisions with final `PB-020` closure?

Method:

Compared the native UI closure-preparation route, workflow examples, native readiness-review schema and template, UI runtime book, accessibility book, `TASK-000006`, owner-decision board, and documentation-readiness evidence matrix. Added explicit PB-020 reconciliation language, updated the no-claim template date, and preserved the requirement for named reviewers, retained artifacts, limitations, exceptions, and synchronized registries.

Decision:

No native UI or accessibility gate changed status. A reviewed adapter, platform accessibility result, accepted UI ADR, or UI-gate result remains lane evidence and cannot independently authorize broad implementation, release-path UI, production accessibility, or Chrome-class claims.

Impact:

The native shell lane now has the same final closure handoff as source strategy, IPC, sandbox, benchmark, profile, update, incident, and ownership lanes.

Next question:

Can a real `TASK-000006` evidence packet preserve toolkit neutrality, page/document identity, manual assistive-technology results, fault recovery, performance denominators, and PB-020 synchronization under independent review?

## 2026-07-19 - IPC and sandbox PB-020 closure routing

Question:

Do the IPC and sandbox execution routes preserve the final PB-020 owner-decision boundary instead of allowing a lane-specific security result to become a production claim?

Method:

Compared the IPC transport/authority closure route, IPC packet example, sandbox execution/containment route, sandbox packet example, security-engine handoff, task manifests, readiness-review templates, and PB-020 closure preparation. Added explicit PB-020 reconciliation language and retained the no-claim boundaries for M0 reference tests, probes, site isolation, renderer security, hostile browsing, release, and production.

Decision:

No IPC or sandbox gate changed status. The routes now state that lane acceptance is necessary but not sufficient for broad implementation, production, or Chrome-class claims.

Impact:

Security-critical continuation work has one consistent final closure boundary across source strategy, benchmark, IPC, sandbox, incident, ownership, and release lanes.

Next question:

Can a real IPC or sandbox evidence packet preserve exact source identity, failure denominators, platform scope, authority limits, and PB-020 synchronization under independent review?

## 2026-07-19 - ADR-0009 and PB-020 closure routing

Question:

Does the source-strategy decision packet make clear that an accepted ADR-0009 still requires PB-020 owner-decision closure before broad implementation or release authority?

Method:

Compared the ADR-0009 source packet, evidence matrix, closure-preparation route, no-claim decision-review template, ADR evidence registry, `TASK-000001` manifest, owner-decision board, and research-index source-strategy row. Updated the packet date and added explicit PB-020 routing to the packet, matrix, and research index.

Decision:

The ADR-0009 route remains no-claim and blocked. No source baseline, component, dependency, release-code, implementation, compatibility, security, or performance decision changed.

Impact:

Source strategy is now explicitly connected to the same final owner-closure control as benchmark, sandbox, UI, profile, update, incident, and ownership lanes. This prevents an ADR decision from being interpreted as standalone build authorization.

Next question:

Can the first real ADR-0009 evidence review synchronize source provenance, legal, security, compatibility, performance, maintenance, task authority, and PB-020 records atomically?

## 2026-07-19 - Chrome-class performance closure routing

Question:

Does the Chrome-class and extreme-performance documentation route benchmark evidence through the same PB-020 closure, security, accessibility, support, and release controls as the rest of the browser program?

Method:

Compared the capability traceability map, benchmark-lab lane, benchmark evidence and claim-closure route, claim-bundle examples, PB-013 task/control records, and PB-020 closure preparation. Updated the performance lane date, added explicit PB-020 reconciliation and validator routing, and made the capability map's performance row state the same dependency.

Decision:

The performance objective remains a no-claim evidence lane. No benchmark result, competitor comparison, Chrome-class claim, or readiness status changed.

Impact:

Extreme-performance work cannot be interpreted as a shortcut around sandbox, compatibility, accessibility, ownership, support, release, or production gates. The current documentation status remains 90% contained-M0 organized and 0% full-build closure.

Next question:

Can the first browser-run benchmark packet preserve exact workload, failure denominators, resource attribution, claim expiry, and PB-020 closure evidence without widening the published claim?

## 2026-07-19 - Progress snapshot and closure-control drift audit

Question:

Do the canonical entrypoints, progress snapshot, machine audit, owner board, and closure controls report the same documentation percentage and full-goal blocker scope?

Method:

Compared readiness language and percentage references across the root README, Start Here, project-buildout operating board, progress snapshot, documentation-readiness audit, pre-build registry, PB-020 evidence, owner-decision board, research index, closure schema/template, and closure validator. Checked that the snapshot's pre-build headline blockers are not mistaken for the full five-group closure view, and added the closure validator and record examples to the PB-020 evidence chain and operating-board handoff.

Decision:

No unsupported readiness claim or percentage drift was found. The snapshot now explicitly distinguishes pre-build headline blockers from the full-goal blocker groups, and the canonical PB-020 evidence list includes the real-packet validator and owner-decision examples.

Impact:

A maintainer can start at the operating board or progress snapshot and reach the same 90% contained-M0 / 0% full-build status, the complete closure scope, and the future packet validation control without relying on chat history.

Next question:

Can the first real owner-approved lane packet replace the no-claim examples while preserving the same machine traceability, unsupported-claim boundaries, and aggregate validation?

## 2026-07-19 - Incident-response and patch-rehearsal packet examples

Question:

Can the `PB-018` lane show one complete, no-claim packet shape that keeps private intake, custody, containment, fake-key patch rehearsal, disclosure, cleanup, failure accounting, and authority review distinct?

Method:

Compared the incident rehearsal inventory, decision-preparation report, execution/closure route, rehearsal schema and template, release vulnerability-response book, security verification gates, and `TASK-000010` boundary. Added a fictitious packet with lifecycle records, synthetic fixture policy, containment and patch/update examples, disclosure and cleanup accounting, role separation, and rejection rules.

Decision:

The packet shape is now explicit, but no incident rehearsal, patch dry run, owner review, authority, or readiness status changed. The example prohibits live secrets, real user data, production keys, public exploit details, and stable promotion.

Impact:

The incident lane now has the same field-level research-to-review handoff pattern as the other major blocker lanes. `PB-018` and `TASK-000010` remain no-claim and unresolved for full-goal closure.

Next question:

Can a real private synthetic tabletop and fake-key patch dry run retain failed scenarios, denominators, cleanup, and independent review without widening disclosure or release authority?

## 2026-07-19 - Owner-decision closure record examples

Question:

Can the central `PB-020` handoff show how evidence, owner review, bounded exceptions, authority separation, and synchronized registry updates fit together without turning a template or sample into approval?

Method:

Compared the build-readiness closure-preparation route, owner-decision board, closure-review schema/template, documentation-readiness audit, and all ten lane closure routes. Added fictitious examples for `evidence_collected`, `held_by_exception`, unresolved, and closed-shape-only states, plus a collection manifest, authority matrix, and rejection rules.

Decision:

The record shape is now explicit, but no current gate changed state. The examples retain placeholder identities and digests, deny authority, and preserve the `PB-020` blocker when any prerequisite is unresolved or unsynchronized.

Impact:

The remaining owner-only handoff has a concrete review shape that can be replaced by a real packet without relying on prose interpretation. The documentation-readiness audit remains `9/10` contained-M0-ready and `0/10` full-goal-ready.

Next question:

Can a real owner-approved packet replace the sample only after every lane supplies immutable evidence, independent review, explicit limitations, and atomic canonical-record updates?

## 2026-07-19 - Documentation placeholder and readiness-language sweep

Question:

Did the recent lane-packet additions introduce accidental TODO/TBD markers, stale readiness language, unsupported Chrome-class claims, or continuation references that disagree with the machine audit?

Method:

Searched canonical entrypoints, project-buildout records, Blueprint chapters, detailed books, research reports, and templates for placeholder and readiness-language terms. Compared the results with the documentation-readiness audit, progress snapshot, owner-decision board, pre-build registry, and research crosswalk. Intentional placeholders were retained only where the surrounding document explicitly marks them as template-only, sample-only, unimplemented, or a rejection condition.

Decision:

No accidental documentation drift was found. Entrypoints and machine records continue to agree on `90%` contained-M0 documentation organization and `0%` full-build closure. No readiness, Chrome-class, performance, security, compatibility, accessibility, production, release, or daily-driver claim was upgraded.

Impact:

Future maintainers can treat the remaining placeholder language as bounded control text rather than an untracked implementation promise. The unresolved owner-decision and evidence blockers remain authoritative.

Next question:

Can the next real evidence or owner decision update all affected canonical records atomically without widening any claim boundary?

## 2026-07-19 - Benchmark claim-bundle examples

Question:

Can the `PB-013` lane provide one concrete, reusable claim-bundle packet that connects runner-generated artifacts and statistics to exact wording, scope, expiry, denominator disclosure, equivalence review, and publication rejection without inventing benchmark results?

Method:

Compared the benchmark evidence and claim closure route, competitor runbook examples, statistics-analysis contract, no-claim public-claim template, benchmark readiness-review template, Chrome-class lane map, and `TASK-000005` scope. Added a fictitious packet with claim identity, evidence binding, metric/denominator reconciliation, equivalence and safety controls, publication/expiry fields, and rejection rules.

Decision:

Keep `PB-013` partial and `TASK-000005` proposed-only. The example improves the review handoff but provides no browser run, competitor result, statistics result, benchmark readiness, public claim, Chrome-class comparison, or extreme-performance claim.

Impact:

Future performance work has a concrete boundary between a raw evidence package, a reviewed diagnostic, a competitor comparison, and a narrowly scoped public claim. Failed and unsupported cases remain visible instead of disappearing into aggregates.

Next question:

Can the reviewed L1 browser-run pipeline produce the first immutable raw artifact package and denominator report before any L2 comparison or public claim is considered?

## 2026-07-19 - Fresh-host reproduction packet examples

Question:

Can the `PB-008`/`PB-009` lane provide one concrete, reusable packet that keeps host identity, source identity, toolchain facts, every attempted command, failures, retained hashes, cleanup, and readiness-review handoff together without calling a template or same-host rerun independent evidence?

Method:

Compared the fresh-host inventory, closure-preparation route, build-information ledger, run-record and readiness-review schemas/templates, `TASK-000002` scope, and owner-decision closure board. Added a fictitious packet with host/prior-state identity, source/artifact reconciliation, attempted-command denominator, failure classification, retained-output rules, cleanup, review fields, and rejection rules.

Decision:

Keep `PB-008` and `PB-009` partial and `TASK-000002` proposed-only. The example improves the execution handoff but provides no independent run, toolchain equivalence, reproducibility, owner review, release confidence, or Chrome-class claim.

Impact:

Future fresh-host work has a concrete denominator and can preserve failed setup, repair, retry, cleanup, cache, target-directory, source-cleanliness, and log-hash evidence instead of reporting only the final check result.

Next question:

Can an approved `TASK-000002` run produce a retained packet on an independent fresh host or explicitly accepted clean-VM equivalent before either gate is promoted?

## 2026-07-19 - ADR-0009 source-strategy packet examples

Question:

Can the `PB-002`/`ADR-0009` lane provide a concrete, reusable option-review packet that keeps source identity, evidence maturity, legal and supply-chain posture, generated output, runtime boundaries, compatibility, performance, security, maintenance, authority, and claim limits together without selecting a source strategy?

Method:

Compared the ADR-0009 closure route, source-strategy decision packet, evidence traceability matrix, machine evidence registry, checked decision-review template, Servo research reports, and owner-decision closure board. Added a fictitious packet with stable identity fields, one option record, all `ADR9-EV-001` through `ADR9-EV-018` evidence shapes, authority checks, authorization structure, and rejection rules.

Decision:

Keep `PB-002` blocked and `ADR-0009` at `no_source_strategy_decision`. The example improves the handoff but provides no source selection, source equivalence acceptance, component approval, legal approval, compatibility result, performance result, security approval, source import, or release-code authorization.

Impact:

Future source-strategy review can distinguish observed, reproduced, reviewed, decided, and authorized evidence while keeping missing limitations and downstream document diffs visible.

Next question:

Can the real `ADR9-EV-*` packet be independently reviewed against an owner-selected source baseline and feature profile before any release-critical source or component work is authorized?

## 2026-07-19 - IPC transport packet examples

Question:

Can the `PB-011` lane provide a concrete, reusable sample packet that keeps schema provenance, control-envelope identity, peer/channel binding, lifecycle, negative cases, resource accounting, platform differences, and review boundaries together without selecting a codec or claiming production IPC?

Method:

Compared the IPC capability inventory, WP-002 review handoff, wire-encoding decision preparation, API design book, no-claim schema-source and readiness-review templates, `TASK-000003`/`TASK-000011` scopes, and transport closure route. Added a fictitious packet with schema provenance, envelope fields, peer binding, negative/lifecycle matrix, authority/resource checks, platform rows, and rejection rules.

Decision:

Keep `PB-011` partial, `TASK-000011` review-pending, and `TASK-000003` proposed-only. The example improves the independent-review handoff but provides no wire decision, generator approval, authenticated transport, process isolation, renderer security, or production IPC evidence.

Impact:

Future IPC work has a field-level example that keeps page/model/extension/agent input from expanding authority and retains stale, malformed, unauthorized, cancellation, crash, reconnect, and resource-exhaustion cases in the denominator.

Next question:

Can an independent `TASK-000011` review packet tied to the exact source commit be accepted before a reviewed wire/transport task is authorized?

## 2026-07-19 - Backup owner and two-person-control packet examples

Question:

Can the `PB-019`/`PB-020` lane provide a concrete, reusable sample packet that keeps qualification, protected-path coverage, access reconciliation, absence handling, two-person control, exceptions, and residual risk together without naming people or granting authority?

Method:

Compared the backup ownership gap inventory, ownership/CODEOWNERS baseline, qualification and readiness-review templates, professional owner/review registries, `TASK-000008` scope, and backup-ownership closure route. Added a fictitious single-scope packet with qualification axes, access/routing reconciliation, high-authority two-person exercises, failure/exception records, and rejection rules.

Decision:

Keep `PB-019` blocked, `PB-020` unresolved, and `TASK-000008` proposed-only. The example improves the future owner-review handoff but does not name a backup, prove competence or availability, reconcile access, establish two-person control, or grant release, signing, disclosure, legal, incident, or production authority.

Impact:

Future ownership work has a field-level example that preserves primary-only and ownerless paths, stale access, recusal, succession, emergency replacement, and authority separation as explicit residual risks. CODEOWNERS presence remains routing evidence only.

Next question:

Can an owner-approved immutable `TASK-000008` package produce verified qualification and two-person-control evidence for one scope without exposing private contact details or granting release authority?

## 2026-07-19 - Package/update lab packet examples

Question:

Can the `PB-017` lane provide a concrete, reusable fake-key local packet that keeps source/build/artifact/provenance/signature/metadata/install/migration/support states separate while retaining fault, privacy, rollback, and cleanup evidence?

Method:

Compared the research package/update lab inventory, TUF/SLSA/in-toto/Sigstore decision preparation, update-lab package and readiness-review templates, release-operations book, `TASK-000009` scope, and package/update closure route. Added a fictitious packet with trust-state records, local metadata fields, install/recovery matrix, privacy-event rules, and rejection rules for production keys, stale or wrong-target metadata, hidden faults, and template-as-readiness errors.

Decision:

Keep `PB-017` partial and `TASK-000009` proposed-only. The example improves the fake-key lab and independent-review handoff but provides no executable manifest, metadata parser, signature test, installer, rollback, migration, supported-security, or release evidence.

Impact:

Future update work has a field-level example that prevents signature validity, provenance, metadata freshness, installation success, profile migration, and support status from being conflated. Failed and unsafe cases remain in the denominator.

Next question:

Can an owner-approved immutable `TASK-000009` package produce the first local fake-key metadata and staged-install fault artifacts without touching production keys, stable channels, or real profiles?

## 2026-07-19 - Profile/session data-safety packet examples

Question:

Can the `PB-016` lane provide a concrete, reusable synthetic-migration packet that keeps state-class identity, journal transitions, fault injection, privacy/export, protected-work recovery, cleanup, and review boundaries together without implying real-profile safety?

Method:

Compared the profile/session format inventory, data-lifecycle decision preparation, schema-package and readiness-review templates, storage/recovery book, `TASK-000007` scope, and execution/data-safety closure route. Added a fictitious packet with state-class manifest, migration lifecycle, fault/recovery matrix, privacy/export checks, and rejection rules for real data, downgrade, corruption, private-session leakage, and success-only evidence.

Decision:

Keep `PB-016` partial and `TASK-000007` proposed-only. The example improves the synthetic-fixture and independent-review handoff but provides no executable schema, migration test, fault result, real-profile policy, credential, sync, privacy, or data-loss evidence.

Impact:

Future profile work has a field-level example that preserves distinctions between browser-owned state, origin storage, credentials, private sessions, snapshots, and protected work. Faults and cleanup remain in the denominator instead of being hidden by successful writes.

Next question:

Can an owner-approved immutable `TASK-000007` package produce the first executable synthetic schema and migration/fault artifacts without using real user data or credentials?

## 2026-07-19 - Native UI and accessibility workflow examples

Question:

Can the native UI lane provide a concrete, reusable workflow record that keeps trusted-chrome authority, page-surface identity, input/IME behavior, accessibility trees, manual assistive technology, fault recovery, latency, and failure denominators together without implying toolkit or UI-gate readiness?

Method:

Compared the native UI/accessibility closure route, toolkit-neutral adapter contract, framework bake-off, component fixtures, page-surface composition inventory, window/input/accessibility spike, accessibility book, and `TASK-000006` scope. Added a fictitious address-field/page-surface workflow with authority-negative cases, platform assistive-technology rows, fault and latency fields, and explicit rejection rules.

Decision:

Keep `PB-003`, `PB-004`, `PB-005`, `PB-014`, and `PB-015` partial and `TASK-000006` proposed-only. The sample improves the reference-shell handoff but provides no toolkit selection, rendered fixture, platform tree, manual transcript, IME result, page-surface proof, UI-gate evidence, or release-path claim.

Impact:

Future UI work has a field-level example for one adapter/platform/workflow scope while preserving the rule that platform and assistive-technology results cannot be generalized across rows. Authority, identity, fault, latency, and unsupported cases remain explicit.

Next question:

Can an owner-approved immutable `TASK-000006` package produce the first rendered reference-shell and real assistive-technology workflow artifacts without granting toolkit or page content browser authority?

## 2026-07-19 - Sandbox probe result packet examples

Question:

Can the `PB-012` lane provide a concrete, reusable result-packet example that keeps effective policy, allowed controls, expected denials, hostile-client cases, unsupported primitives, lifecycle failures, platform differences, and cleanup evidence together without making a containment claim?

Method:

Compared the sandbox probe inventory, `WP-003` operation/evidence contract, platform-evidence decision preparation, no-claim probe-package and readiness-review templates, security-engine sandbox contract, `TASK-000004` scope, and the execution/containment closure route. Added a fictitious renderer packet example and explicit rejection rules for helper substitution, requested-versus-effective policy confusion, unsupported primitives, denominator omission, real secrets or profiles, broker authority expansion, and template-as-readiness errors.

Decision:

Keep `PB-012` partial and `TASK-000004` proposed-only. The example improves execution and independent-review handoff but provides no packaged probe, effective-policy artifact, expected-deny result, platform containment, security-gate, hostile-browsing, or production-safety evidence.

Impact:

Future probe work has a field-level example for one role and platform while preserving platform differences and the rule that unsupported or unrun operations are not passes. The sample cannot be generalized beyond its executed role/platform matrix.

Next question:

Can an owner-approved immutable `TASK-000004` package produce the first real expected-deny and allowed-control artifacts on one platform without touching real user data or weakening the sandbox boundary?

## 2026-07-19 - Benchmark competitor runbook examples

Question:

Can the Chrome-class performance lane provide complete, reusable competitor-record examples without turning release-catalog observations, local executable inventories, or browser-pin diagnostics into benchmark results?

Method:

Compared the Chrome-Class Performance Runbook, benchmark evidence/claim closure route, competitor-version and local-install contracts, browser-pin capture rules, trace/artifact package contract, launch-runner contract, statistics contract, and the fixed-hardware benchmark book. Added sample-only Chrome Stable and Firefox Stable record shapes covering identity, profile and security policy, lab controls, workload, collection, outcome, denominator, review, expiry, and invalid-comparison handling.

Decision:

Keep `PB-013` partial and preserve the no-claim boundary. The examples improve future runner and reviewer consistency but contain fictitious values and do not provide browser runs, competitor results, statistics, benchmark readiness, or Chrome-class performance evidence.

Impact:

Future benchmark work has a concrete field-level handoff for two named competitor families while retaining failed and unsupported cases in the denominator. Inventory, diagnostics, and sample records remain distinct from runner-generated raw evidence and owner-reviewed claims.

Next question:

Can the runner produce one complete Level 1 local-browser packet from a temporary profile and the pinned hardware/OS/corpus controls without using real user data or publishing a competitor comparison?

## 2026-07-19 - PB-020 closure packet handling and status-transition contract

Question:

Does the final build-readiness closure route tell a future maintainer exactly where to place the packet, what inputs to freeze, how to handle digests and redaction, and which status transitions are allowed without turning a template or green validator into an owner decision?

Method:

Reviewed the `PB-020` closure schema and no-claim template, owner-decision board, documentation-readiness audit, build-information ledger, dependency graph, task-manifest controls, and all ten lane-specific closure-preparation reports. Added a canonical packet-handling section, an explicit `unresolved`/`evidence_collected`/`held_by_exception`/`closed` lifecycle, a collection manifest requirement, and repository retention boundaries to the closure-preparation route.

Decision:

Keep `PB-020` unresolved and preserve the 90% contained-M0 / 0% full-build measurements. The new contract improves the future owner-review handoff but does not create evidence, approve a task, grant authority, or promote any readiness gate.

Impact:

Future closure work now has a stable packet location, immutable-input and digest expectations, redaction rules, explicit gate status transitions, and a required list of all ten evidence routes. A missing route or stale digest remains visible rather than being silently treated as complete.

Next question:

Which first dependency-graph lane can produce a complete redacted evidence packet and named independent review without requiring production authority?

## 2026-07-19 - ADR-0009 source-strategy closure preparation

- Added a short no-claim continuation route for `PB-002`/`ADR-0009` that consolidates the five source-strategy options, independence/provenance/legal/security/compatibility/performance/maintenance criteria, evidence maturity rules, owner decision fields, and stop conditions.
- Linked it through the ADR packet, evidence matrix, `start-here`, docs index, research crosswalk, repository map, and source-strategy report list. No source baseline, Servo relationship, component boundary, source import, release-code authorization, or `PB-002` readiness status changed.

## 2026-07-19 - Backup ownership and review capacity decision preparation

- Added a dated no-claim `PB-019` report using NIST CSF 2.0 governance outcomes and GitHub CODEOWNERS/protected-branch documentation.
- Separated routing from qualification, branch protection from effective control assessment, and named reviewers from independent two-person authority; added ownership evidence, reconciliation, succession, access, and emergency-replacement criteria.
- Linked the report through the backup-ownership inventory, project-buildout and production-readiness books, docs and research indexes, and repository map. No backup was named, no authority was granted, and `PB-019` remains blocked.

# 2026-07-19 - Incident-response closure-route synchronization

Question:

Can a maintainer reach the incident private-intake, patch rehearsal, disclosure, cleanup, and authority evidence order from the owner and progress records?

Method:

Compared the incident rehearsal inventory, decision preparation, execution/disclosure closure report, rehearsal and readiness-review templates, `TASK-000010`, progress snapshot, and owner-decision board. Added the closure-preparation route to the `PB-018` owner row and the incident lane in the progress snapshot while preserving the proposed-only task and no-claim template boundaries.

Decision:

The route is coherent and discoverable, but `PB-018` remains `partial` and `TASK-000010` remains proposed-only. No incident-response readiness, emergency patch capacity, disclosure authority, signing authority, supported-security, stable-promotion, or production-safe browsing claim is supported.

Impact:

Future incident work starts from one ordered evidence packet covering private synthetic intake, containment, fake-key patch rehearsal, regression and recovery, coordinated disclosure, cleanup, named review, and authority separation. The route does not grant an agent incident, signing, disclosure, release, or closure authority.

Next question:

Which synthetic incident packet can be reviewed without production keys, disclosure authority, real secrets, or exploitable details?

## 2026-07-19 - Incident response and emergency patch decision preparation

- Added a dated no-claim `PB-018` report using NIST SP 800-61 Revision 3, CISA coordinated vulnerability disclosure guidance, and FIRST CVSS v4.0 guidance.
- Separated intake, triage, containment, patch, signing, promotion, disclosure, and closure authority; added evidence requirements and an incident-class matrix for active exploitation, update/signing compromise, dependencies, data loss, privacy leaks, sandbox regressions, malicious extensions/providers, and service outages.
- Linked the report through the incident inventory, security policy, security-engine book, release-operations book, docs and research indexes, and repository map. No incident-response program, severity SLA, disclosure, signing, stable-support, emergency-patch, or production-safety decision was made.

## 2026-07-19 - Package, update trust, and recovery decision preparation

- Added a dated no-claim `PB-017` comparison of TUF update metadata roles and freshness, SLSA build provenance, in-toto authorized supply-chain steps, and Sigstore signing/transparency evidence.
- Separated source/build/artifact identity, provenance, signatures, update authorization, installation transactions, profile transitions, and support decisions; added a fault matrix covering stale metadata, rollback, wrong targets, mirror disagreement, partial writes, disk-full, power loss, crash loops, migration, signer compromise, and privacy-preserving diagnostics.
- Linked the report through the package/update inventory, release-operations book, docs and research indexes, and repository map. No update framework, package format, signing hierarchy, updater, release, or production-security decision was made.

## 2026-07-19 - IPC wire-encoding decision preparation

- Added a dated no-claim comparison of CBOR, Protocol Buffers, FlatBuffers, and a Turing-owned compact codec for the unresolved `PB-011` wire-format decision.
- Recorded mandatory controls for bounded decoding, unknown fields and variants, deterministic bytes, generated-code provenance, zero-copy safety, schema evolution, fuzzability, transport authentication, and resource accounting.
- Linked the report through the IPC inventory, system architecture, security model, research indexes, and repository map. No encoding, dependency, generator, transport, or readiness status was selected.

## 2026-07-19 - Sandbox platform-evidence decision preparation

- Added a dated no-claim comparison of Windows, Linux, and macOS sandbox evidence requirements for `PB-012` and `WP-003`.
- Recorded the platform-specific distinction between Windows identity/mitigation evidence, Linux seccomp and Landlock behavior, and macOS signing/entitlement/hardened-runtime evidence.
- Preserved the rules that seccomp alone is not a complete sandbox, Landlock ABI support must be captured, unsupported primitives are not passes, and launch failure or application stubs cannot substitute for expected-deny evidence.

## 2026-07-19 - Profile and session data-lifecycle decision preparation

- Added a dated no-claim `PB-016` report separating browser-owned profile metadata, Space/workspace state, session recovery, snapshots, origin-partitioned web storage, credentials, and private-session state.
- Recorded durability, clearing, export, migration, recovery, privacy, and protected-work decision gates using current Storage, IndexedDB, and Clear-Site-Data specifications.
- Linked the report through the profile inventory, storage book, product-experience book, research index, docs index, repository map, and research log. No executable schema, real-profile policy, migration, sync, credential, or production-format decision was made.

## 2026-07-19 - IPC wire-encoding decision preparation

- Added a dated no-claim comparison of CBOR, Protocol Buffers, FlatBuffers, and a Turing-owned compact codec for the unresolved `PB-011` wire-format decision.
- Recorded mandatory controls for bounded decoding, unknown fields and variants, deterministic bytes, generated-code provenance, zero-copy safety, schema evolution, fuzzability, transport authentication, and resource accounting.
- Linked the report through the IPC inventory, system architecture, security model, research indexes, and repository map. No encoding, dependency, generator, transport, or readiness status was selected.

## 2026-07-19 - BrowserBench methodology refresh

- Refreshed the Chrome-class performance runbook and `PB-013` readiness packet against the official Speedometer 3.1, JetStream 3.0, and MotionMark methodology pages.
- Recorded suite-specific controls: Speedometer no-duration subtests invalidate a run; JetStream preserves per-workload output, documented startup/worst/average treatment, geometric-mean aggregation, and version identity; MotionMark records warmup, target frame rate, refresh rate, viewport, orientation, GPU/power state, and its change-point/bootstrap method.
- Synchronized Blueprint 09 benchmark governance and `PB13-EV-009`/`PB13-EV-010` evidence language. This is no-claim methodology evidence only; `PB-013` remains `documented_no_runner` and no performance or Chrome-class claim is approved.

## 2026-07-19 - Toolchain and fresh-host continuation route correction

- The semantic audit found the dated pre-build gap report still routed `PB-009` alone even though pinned toolchain `PB-008` and fresh-host `PB-009` are one canonical `TASK-000002` lane.
- Updated the first continuation path to include the build-information ledger and the exact compiler, SDK, linker, Rust, Cargo, Git, shell, cache, target-directory, source-cleanliness, bootstrap, doctor, check, and `xtask` evidence required by the combined lane.
- Added a validator assertion so the human continuation route cannot silently regress while both gates remain partial. This is routing and traceability control only; no readiness gate or build authority changed.

This log records material research-program and documentation-governance changes. Detailed technical conclusions belong in the owning Blueprint chapter, requirement, risk, ADR, benchmark, backlog entry, indexed engineering book, or dated research report.

## 2026-07-19 - Human gate-table status drift control

- The Blueprint validator now compares every `PB-001` through `PB-020` status in the canonical machine readiness registry with the corresponding row in the dated pre-build readiness gap audit.
- This makes the corrected `PB-008` partial status and `PB-006` not-selected status mechanically durable instead of relying on a manual semantic sweep.
- Status matching remains a consistency check only; it does not promote gates or authorize broad implementation.

## 2026-07-19 - Readiness audit status-drift correction

- The semantic-drift sweep found the dated pre-build readiness gap audit still labeled `PB-008` as `Ready` even though the canonical machine registry correctly labels pinned toolchain readiness `partial`.
- Updated the audit date, status, evidence summary, and missing-proof boundary to match the current `PB-008` record and independent fresh-host requirements.
- This removes a stale positive claim; no gate was promoted and the documentation percentages remain unchanged.

## 2026-07-19 - Non-ready gate route enforcement

- Extended the Blueprint validator to require every partial, blocked, documented-no-runner, documented-no-source, or not-started `PB-*` gate to appear in the research-readiness crosswalk.
- The validator now also requires each queue task's structured `readiness_items` mapping to equal the gates assigned to that task by the crosswalk.
- `not_selected` gates remain outside the research-route requirement only when their machine record carries a rationale and revisit trigger, as now required for `PB-006`.
- This closes route ambiguity without changing readiness status or authorizing implementation.

## 2026-07-19 - PB-006 deferred-platform status closure

- The cross-registry audit found `PB-006` marked `not_selected` in the machine readiness registry while the dated gap audit incorrectly described it as a ready M0 reference desktop environment.
- Corrected the human audit and added machine-required `not_selected_reason` and `revisit_trigger` fields. The gate is intentionally deferred until M1 product-support scope, native-shell decisions, and platform budget are accepted.
- This removes a status contradiction; it does not select a platform, authorize M1 implementation, or support platform, compatibility, accessibility, release, or production claims.

## 2026-07-19 - Task-to-readiness gate mapping closure

- The cross-registry audit found that the human task queue listed `PB-*` gates but the machine queue and specified manifests did not carry that relationship as structured data.
- Added immutable `readiness_items` mappings to `TASK-000001` through `TASK-000010` and the active `TASK-000011` record, extended the execution-task schema, and made the specified-manifest validator require queue/manifest equality.
- Replaced the hard-coded queue digest with a canonical SHA-256 digest computed from the queue JSON, so any future queue change invalidates stale manifests until they are regenerated and re-reviewed.
- This closes a traceability and drift-control gap only. It does not approve a task, promote a `PB-*` gate, or change the 90% contained-M0 / 0% full-build measurements.

## 2026-07-19 - Progress snapshot distribution drift control

- The documentation-readiness completion validator now reconciles the one-screen build-readiness progress snapshot with `pre-build-readiness.json`, `adr-0009-evidence.json`, and the documentation audit criteria.
- The check covers the `90%` contained-M0 organization figure, `0%` full-build closure figure, pre-build status counts, ADR-0009 status counts, and the current `PB-002`/`PB-019`/`DOC-READY-OWNER-DECISIONS` blocker markers.
- This prevents a stale human handoff page from reporting an obsolete gate distribution after a machine registry changes. It adds consistency evidence only; it does not alter any gate, approve any task, or promote readiness.

## 2026-07-19 — PB-008 crosswalk and task-authority closure

Audited the canonical readiness registry, research crosswalk, build-readiness queue, specified task manifests, fresh-host controls, implementation plan, and top-level continuation docs. Found that `PB-008` was tracked in project-buildout controls but omitted from the canonical research crosswalk and from `TASK-000002`'s explicit allowed evidence paths. Added the pinned compiler/SDK/linker/toolchain records to `PB-008`, mapped the research lane to `PB-008`/`PB-009`/`PB-020`, expanded `TASK-000002` to own the manifests, preserved its non-executable boundary, and updated the queue digest across all specified manifests and the owner-review handoff.

This closes a traceability gap only. No independent toolchain or fresh-host run exists, `PB-008`/`PB-009` remain partial, no task is approved, and no broad-build, production, performance, compatibility, security, accessibility, release, or Chrome-class claim is supported.

## 2026-07-19 — Toolchain/fresh-host traceability and owner-board source synchronization

Added `PB-008` pinned compiler/SDK/linker/toolchain reproduction to the canonical continuation surfaces alongside `PB-009` fresh-host reproduction. Synchronized the root README, Start Here, documentation index, project-buildout index, start guide, continuation pack, operating board, evidence matrix, progress snapshot, kickoff inventory, dependency graph, information ledger, repository map, owner-decision closure board, and machine source records. The build-information, kickoff, dependency-graph, owner-decision, documentation-audit, Blueprint, and aggregate validators now preserve the same combined lane and require the owner-decision closure board as a source record where owner-only decisions are consumed.

This is a documentation and traceability improvement only. It does not produce independent toolchain or fresh-host evidence, promote `PB-008` or `PB-009`, authorize broad implementation, or support production, performance, compatibility, security, accessibility, release, or Chrome-class claims.

## 2026-07-19 — Servo official-policy refresh

Refreshed Servo's official embedding, LTS, overview, and offline-build documentation for the `ADR-0009` source-strategy packet. The current official material still describes embedding documentation as a work in progress, identifies `servoshell` as the recommended browser path while the WebView surface develops, describes LTS as best effort with no specific guarantees and excludes `servoshell`, and documents a vendored archive path for offline builds. These observations sharpen the support, browser-shell, and source-equivalence questions but do not change `PB-002`, approve Servo, or support security, compatibility, performance, production, or Chrome-class claims.

Affected record: [Servo source strategy inventory — July 2026](research/servo-source-strategy-inventory-2026-07.md).

## 2026-07-19 — ADR-0009 compatibility route self-test verification

Question:
Did the checked local compatibility fixture server still satisfy its no-claim route and cleanup contract after the documentation-readiness changes?

Sources and versions:

- `docs/research/servo-local-compatibility-corpus-2026-07.md`
- `docs/blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json`
- `tools/serve_servo_local_compatibility_corpus.py`
- `tools/validate_servo_local_compatibility_corpus.py`
- `tools/validate_servo_local_compatibility_https_harness.py`

Method and environment:

- local repository: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- command: `python3 -B tools/serve_servo_local_compatibility_corpus.py --self-test`
- validation: corpus manifest and HTTPS harness validators

Observations:

- all 10 declared loopback HTTP routes returned `200` and matched the manifest fixture identities and hashes;
- the server shut down and the port-closed check rejected a follow-up connection;
- no external network, HTTPS certificate, OS DNS/hosts-file mutation, browser launch, Servo run, WPT run, or Test262 run occurred.

Decision:

- retain `ADR9-EV-013` as `partial` and retain the plan-only HTTPS harness status;
- classify the result as route-plumbing and cleanup evidence only, not compatibility evidence or a source-strategy decision.

Remaining gaps:

- execute the isolated HTTPS/browser harness and capture raw browser artifacts, then run the selected WPT subset with complete failure-denominator accounting;
- obtain owner review before any compatibility or source-strategy status promotion.

## 2026-07-19 — Session handoff runbook and evidence verification patch

Question:
What additional documentation control can make pre-build continuity easier to execute safely without weakening gates?

Sources and versions:

- `docs/project-buildout/21-build-readiness-start-guide.md`
- `tools/validate_build_foundation.py` (run output)
- `tools/validate_implementation_plan.py` (run output)
- `tools/validate_implementation_kickoff_review.py` (run output)
- `tools/validate_adr_0009_evidence.py` (run output)
- `tools/validate_documentation_readiness_completion_audit.py` (run output)
- `tools/validate_build_information_readiness.py` (run output)
- `tools/validate_blueprint.py` (run output)
- `tools/validate_ipc_capability_boundaries.py` (run output)
- `tools/validate_sandbox_contracts.py` (run output)
- `tools/validate_github_issue_handoff.py` (run output)
- `tools/validate_evidence_bundles.py` (passed via `.\tools\check.ps1`)
- `.\tools\check.ps1` (full aggregate M0/build/readiness + implementation-plan + issue-handoff + tests)

Method and environment:

- local repository: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- added a mandatory command bundle section to the start guide so every session has one canonical pre-build execution checklist

Observations:

- command-blocking stale artifacts no longer needed during checks (`target/` was already clean prior to this pass);
- `docs/project-buildout/21-build-readiness-start-guide.md` now includes a concrete required command set under one section.
- all core validators and aggregate checks passed again after the doc edit.
- no new implementation evidence was introduced; only documentation and continuity structure changed.

Decision:

- keep no-claim gate posture unchanged:
  - `pre-build-readiness.json` still indicates `not_ready_for_broad_implementation`;
  - hard blocks `PB-002` and `PB-019` remain;
  - broad implementation remains outside current evidence scope.
- this patch is classified as no-claim continuity control only and does not alter implementation rights.

Alternatives rejected:

- allowing sessions to infer full pre-build readiness from partial passing checks without recording the exact command contract;
- leaving the start guide without a direct command sequence in favor of external/in-text references.

Security/privacy/compliance impact:

- unchanged.

Remaining gaps to close before broad implementation:

- `PB-002` and `PB-019` owner-reviewed readiness closure with explicit evidence, and `PB-020` closure review promotion.

## 2026-07-19 — Continuation-entry coherence refinement

Question:
Can the continuation path expose a one-screen readiness view consistently from every major start surface before further research or lane work?

Sources and versions:

- `docs/project-buildout/21-build-readiness-start-guide.md`
- `docs/project-buildout/13-build-readiness-operating-board.md`
- `docs/project-buildout/18-documentation-readiness-evidence-matrix.md`
- `python3 -B tools/validate_blueprint.py`
- `.\tools\check.ps1`

Method and environment:

- local repository: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- added explicit links so the one-screen snapshot is the first handoff checkpoint after start-guide entry.

Observations:

- `docs/project-buildout/21-build-readiness-start-guide.md` now reads snapshot immediately after `Start Here`.
- `docs/project-buildout/13-build-readiness-operating-board.md` now explicitly includes the progress snapshot between Start Guide and the hard-stop pack.
- `docs/project-buildout/18-documentation-readiness-evidence-matrix.md` now includes the progress snapshot in its stop/resume continuity coverage.
- no `pre-build-readiness` gate truth or blocker status changed by this doc-surface harmonization.

Decision:

- keep no-claim continuation boundaries unchanged:
  - `pre-build-readiness.json` remains `not_ready_for_broad_implementation`;
  - `PB-002` and `PB-019` remain blocked;
  - broad implementation remains blocked pending owner-reviewed readiness promotion evidence.

Security/privacy/compliance impact:

- none.

Compatibility/accessibility impact:

- none.

## 2026-07-19 — Documentation stop/resume consistency and check pass

Question:
Can the documentation stop/resume path and pre-build gate signals remain internally consistent after the latest snapshot/cross-reference updates?

Sources and versions:

- `docs/README.md`
- `docs/start-here.md`
- `docs/repository-map.md`
- `docs/project-buildout/22-build-readiness-progress-snapshot.md`
- `docs/project-buildout/21-build-readiness-start-guide.md`
- `tools/check.ps1`
- `python3 -B tools/validate_blueprint.py`
- `python3 -B tools/validate_adr_0009_evidence.py`
- `python3 -B tools/validate_documentation_readiness_completion_audit.py`
- `python3 -B tools/validate_build_information_readiness.py`
- `python3 -B tools/validate_implementation_kickoff_review.py`
- `python3 -B tools/validate_implementation_plan.py`
- `python3 -B tools/validate_contained_m0_start_state.py`
- `cargo fmt --all -- --check`
- `cargo fmt --manifest-path prototype/Cargo.toml -- --check`
- `cargo test --manifest-path prototype/Cargo.toml --all-targets`
- `cargo run --manifest-path prototype/Cargo.toml --quiet`
- `cargo run --locked -p xtask -- check`

Method and environment:

- working directory: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- aggregate checks were run, but the gate wrapper still blocked on `forbidden legacy paths remain: target`, which remains a workspace hygiene issue.

Observations:

- the duplicate `13.` numbering in `docs/README.md` was corrected; the stop/resume sequence now flows from `1` to `23`;
- `tools/check.ps1` failed with `forbidden legacy paths remain: target` in this pass.
- cross-reference routing now aligns between `docs/README.md`, `docs/start-here.md`, and `docs/project-buildout/README.md`.
- required validator outputs passed for `pre-build-readiness`, implementation plan, issue handoff, documentation-readiness, build information readiness, implementation kickoff, and task manifests.

Decision:

- keep implementation unchanged:
  - maintain contained-M0-only continuation;
  - keep `PB-002` and `PB-019` blocked;
  - keep broad implementation promotion pending owner-reviewed evidence and accepted readiness transitions.

Security/privacy/compatibility impact:

- no implementation changes; validation is no-claim continuity and continuity-control documentation.

## 2026-07-19 — Full M0 repository and documentation validation pass

Question:
Can the repository be verified as coherently organized for contained-M0 continuation right now, with no false pre-build promotion from documentation drift?

Sources and versions:

- `tools/check.ps1`
- `tools/validate_blueprint.py` (run output in this turn)
- `tools/validate_implementation_kickoff_review.py` (run output in this turn)
- `tools/validate_adr_0009_evidence.py` (run output in this turn)
- `tools/validate_documentation_readiness_completion_audit.py` (run output in this turn)
- `tools/validate_build_information_readiness.py` (run output in this turn)
- `cargo fmt --all -- --check`
- `cargo fmt --manifest-path prototype/Cargo.toml -- --check`
- `cargo test --manifest-path prototype/Cargo.toml --all-targets`
- `cargo run --manifest-path prototype/Cargo.toml --quiet`
- `cargo run --locked -p xtask -- check` (invoked via `tools/check.ps1`)
- linked continuation docs listed in the root `README.md` and `docs/project-buildout/*` handoff index

Method and environment:

- local repository: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- cleared legacy repository-local `target/` before rerunning aggregate checks (so `xtask` validation used isolated temp target)
- ran required documentation and repository checks from the root `AGENTS.md` validation list

Observations:

- `pre-build-readiness.json` remains `status: not_ready_for_broad_implementation` with `PB-002` and `PB-019` blocked;
- all pre-build readiness/machine/documentation validators passed:
  - `validate_blueprint.py`
  - `validate_implementation_kickoff_review.py`
  - `validate_adr_0009_evidence.py`
  - `validate_documentation_readiness_completion_audit.py`
  - `validate_build_information_readiness.py`
- formatting and test gates passed:
  - `cargo fmt --all -- --check`
  - `cargo fmt --manifest-path prototype/Cargo.toml -- --check`
  - `cargo test --manifest-path prototype/Cargo.toml --all-targets`
  - `tools/check.ps1` full aggregate check, including implementation-plan, issue-handoff, IPC/registry validators, and all-prototype crate tests
- no broad implementation authority was granted; `PB-020` and task manifests remain non-executed, no `TASK-*` status moved to approved in this pass
- no implementation claims were added or promoted by this validation pass

Inference:

The repository remains organized for coherent contained-M0 continuation and can proceed with further execution planning from the same documented gate posture.

Decision:

- keep broad implementation blocked until owner-reviewed `PB-002` and `PB-019` evidence closure + `PB-020` closure-review promotion requirements are met;
- keep all continuation docs and task queue in no-claim scope without changing gate truth from checks alone;
- continue deep-research and task-shape work in the documented lane order.

Alternatives rejected:

- changing `PB-002`/`PB-019` to ready from tooling output alone;
- using successful contained-M0 checks as evidence for production, Chrome-class, performance, security, accessibility, or release readiness.

Security/privacy impact:

- none introduced by this validation sequence.

Compatibility/accessibility impact:

- unchanged (validation checks do not alter compatibility or accessibility assumptions).

Performance/memory/energy impact:

- none introduced; aggregate check was successfully executed using temporary `CARGO_TARGET_DIR`.

Licensing/operational impact:

- no code/documentation licensing changes; reduced local repository state noise by removing legacy `target/` before full check.

Affected requirements, risks, ADRs, work packages, and documents:

- no status changes to requirements, risks, ADRs, or work packages;
- updated continuity evidence in this log only.

Next evidence required:

- owner-approved readiness promotion evidence for:
  - `PB-002` source-strategy decision trail;
  - `PB-019` backup ownership closure;
  - `PB-020` all-information-ready-for-building decision.

## 2026-07-19 — Readiness coherence and deep-research tracking sweep

Question:
Can a maintainer or agent restart from this commit with fully traceable continuity for containment-only work and no false build-readiness signal?

Sources and versions:

- `docs/project-buildout/20-build-continuation-readiness-pack.md`
- `docs/project-buildout/13-build-readiness-operating-board.md`
- `docs/project-buildout/21-build-readiness-start-guide.md`
- `docs/project-buildout/11-pre-build-readiness-checklist.md`
- `docs/research/implementation-kickoff-review-inventory-2026-07.md`
- `tools/validate_blueprint.py` (run output in this turn)
- `tools/validate_implementation_kickoff_review.py` (run output in this turn)
- `tools/validate_adr_0009_evidence.py` (run output in this turn)

Method and environment:

- local repository: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- checked relative-link coverage inside the repository with a full docs traversal
- no source code was modified

Observations:

- gate posture remains `not_ready_for_broad_implementation` with hard blocks `PB-002` and `PB-019` unchanged;
- `PB-020` remains partial and no `TASK-*` execution authorization exists in checked registry form;
- docs-level continuation surfaces are internally aligned on no-claim scope boundaries and the same hard-stop sequence;
- validation commands passed:
  - `validate_blueprint.py`
  - `validate_implementation_kickoff_review.py`
  - `validate_adr_0009_evidence.py`
- no broken relative Markdown links were found in `docs/`.

Inference:

The continuation path is coherent for documentation-aware, research-led M0 work, and no false “ready for broad implementation” claim is supported by documentation drift.

Decision:

- keep the blocker and broad-claim boundaries explicit;
- record this continuity pass in the research log before any task-queue reorder;
- continue deep-research execution only in documented lanes with independent evidence-review expectations.

Alternatives rejected:

- reclassifying broad implementation/readiness status from documentation edits alone;
- changing gate posture without owner-reviewed evidence in required lanes.

Security/privacy impact:

- unchanged.

Compatibility/accessibility impact:

- unchanged (no implementation claims modified).

Performance/memory/energy impact:

- none.

Licensing/operational impact:

- none.

Affected requirements, risks, ADRs, work packages, and documents:

- no requirement/risk/ADR/work-package status changed by this pass;
- added this continuity evidence record and kept gate-boundary wording unchanged in referenced continuation docs.

Unresolved questions:

- which blocked `PB-*` lane (source strategy vs backup ownership vs fresh-host/IPC/sandbox progression) should close next to reduce parallel risk while preserving safety and claim integrity?

Next evidence required:

- owner-reviewed `PB-020` closure review and no-claim-to-accepted evidence transitions for each lane before any broad M1 build posture change.

## 2026-07-19 — Documentation continuity path normalization

Question:
Can any maintainer or agent resume with the same continuity truth after the latest handoff documentation reorganization?

Sources and versions:

- `README.md`
- `docs/README.md`
- `docs/repository-map.md`
- `docs/start-here.md`
- `docs/project-buildout/11-pre-build-readiness-checklist.md`
- `docs/project-buildout/13-build-readiness-operating-board.md`
- `docs/project-buildout/20-build-continuation-readiness-pack.md`
- `docs/project-buildout/21-build-readiness-start-guide.md`

Method and environment:

- local repository under `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- required documentation and startup-checker commands listed in `AGENTS.md`.

Observations:

- handoff path is now ordered consistently to start at the Build Readiness Start Guide;
- pre-build and continuation docs were synchronized so the pack/board sequence is the same everywhere;
- hard blockers (`PB-002`, `PB-019`) and broad claim boundaries remain unchanged.

Inference:

Documentation continuity improved for session transfer, and the allowed scope remains contained-M0 only.

Decision:

- normalize handoff ordering and references first;
- keep blockers and boundary wording unchanged;
- continue gated evidence work before any broad M1 posture changes.

Alternatives rejected:

- updating readiness declarations or product claims from documentation rewrites alone.

Security/privacy impact:

- no implementation or security posture change.

Compatibility/accessibility impact:

- no implementation claim change.

Performance/memory/energy impact:

- none.

Licensing/operational impact:

- none.

Affected requirements, risks, ADRs, work packages, and documents:

- no requirement/risk/ADR/work-package status changed;
- updated continuity and index prose in the listed documents.

Unresolved questions:

- which evidence lane should close first to reduce dependency blocking with minimal risk?

Next evidence required:

- continued owner-reviewed evidence for `PB-002`, `PB-011`, `PB-019`, and all remaining `PB-*` items before broad build posture changes.

## 2026-07-19 — Build-readiness documentation validation sweep

Question:
Are all current continuity and readiness-control documentation invariants still machine-checkable and internally coherent?

Sources and versions:

- `docs/project-buildout/21-build-readiness-start-guide.md`
- `docs/project-buildout/20-build-continuation-readiness-pack.md`
- `docs/project-buildout/18-documentation-readiness-evidence-matrix.md`
- `docs/project-buildout/17-build-readiness-task-queue.md`
- `docs/project-buildout/machine/contained-m0-start-state.json`
- `docs/project-buildout/machine/documentation-readiness-completion-audit.json`
- `docs/README.md`
- `docs/start-here.md`
- `README.md`

Method and environment:

- repository root: `C:\\Users\\bcw19\\Documents\\Codex\\2026-07-17\\github-plugin-github-openai-curated-remote`
- commands:
  - `python3 -B tools/validate_contained_m0_start_state.py`
  - `python3 -B tools/validate_documentation_readiness_completion_audit.py`
  - `python3 -B tools/validate_blueprint.py`
  - `python3 -B tools/validate_implementation_kickoff_review.py`
  - `python3 -B tools/validate_implementation_plan.py`
  - `python3 -B tools/validate_build_readiness_dependency_graph.py`
  - `python3 -B tools/validate_adr_0009_evidence.py`

Observations:

- start-guide/pack/board/registry ordering is coherent across entrypoints.
- gate posture is still **not ready for broad M1/Chrome-class/extreme-performance implementation**.
- hard blockers remain: `PB-002` source strategy and `PB-019` backup ownership.
- the no-claim continuity and research-tracking posture remains the only safe execution state.

Inference:

The repository’s documentation continuity and readiness-control framework is coherent and verifiable for contained-M0 continuation work only; broad implementation still requires owner-reviewed evidence promotions.

Decision:

- keep all implementation status at contained-M0 scope only;
- preserve `PB-002` and `PB-019` blocking posture in continuation docs and machine registries;
- continue deep-research and evidence tracking for all remaining `PB-*` lanes.

Alternatives rejected:

- claiming readiness for broad implementation based on documentation or no-claim templates alone;
- merging owner approvals into template records without reviewed evidence bundles.

Security/privacy impact:

- no implementation or security posture change.

Compatibility/accessibility impact:

- no implementation claim change.

Performance/memory/energy impact:

- none.

Licensing/operational impact:

- none.

Affected requirements, risks, ADRs, work packages, and documents:

- no requirement/risk/ADR/work-package status changed;
- verification references now explicitly include `validate_implementation_plan.py` and `validate_implementation_kickoff_review.py` for continuity-state coherence.

Unresolved questions:

- which remaining `PB-*` items should be prioritized to collapse to an owner-reviewed broad-start point with minimal critical-path delay?

Next evidence required:

- accepted `PB-002` evidence pathway (source strategy), followed by `PB-019` owner-coverage and two-person control closure, before broad implementation claims;
- owner-reviewed fresh-host, transport-level IPC, sandbox, benchmark, native-shell, profile/session, package/update, and incident-response evidence.

## 2026-07-18 - Build-information readiness ledger

Question:

Can the remaining information needed before broad building be made visible in one checked no-claim ledger without claiming that all information is ready?

Inputs:

- [Build Information Readiness Ledger](research/build-information-readiness-ledger-2026-07.md);
- [`build-information-readiness-ledger.json`](project-buildout/machine/build-information-readiness-ledger.json);
- [`build-information-readiness-ledger.schema.json`](project-buildout/machine/build-information-readiness-ledger.schema.json);
- [`validate_build_information_readiness.py`](../tools/validate_build_information_readiness.py);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`contained-m0-start-state.json`](project-buildout/machine/contained-m0-start-state.json).

Method:

Added a checked no-claim gap ledger with information classes for entrypoints, task authority, source strategy, fresh-host reproduction, IPC, sandbox, benchmark, native shell, profile/session, package/update, incident response, backup ownership, and Chrome-class product claims. The validator checks that each lane keeps current evidence, missing information, owner-only decisions, prohibited claims, proposed-task boundaries, `TASK-000011` review-pending status, and `PB-020` evidence synchronized.

Decision:

Use the ledger as the current all-information gap map. It helps a maintainer choose the next no-claim evidence lane or owner-review packet, but it does not approve proposed tasks, accept `TASK-000011`, promote readiness, or authorize broad building.

Impact:

Future maintainers no longer have to infer the missing broad-build information by reading every readiness report first. The ledger keeps source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, backup-ownership, task-authority, and Chrome-class product gaps in one checked surface.

Next question:

Which owner-reviewed information lane should become the first real task manifest: fresh-host reproduction, `TASK-000011` independent review, or source-strategy closure?

## 2026-07-18 - Contained M0 start-state control

Question:

Can the current "can we start building now?" answer become machine-checkable without approving proposed tasks, accepting `TASK-000011`, or promoting broad implementation readiness?

Inputs:

- [Contained M0 Start State Inventory](research/contained-m0-start-state-inventory-2026-07.md);
- [`contained-m0-start-state.json`](project-buildout/machine/contained-m0-start-state.json);
- [`contained-m0-start-state.schema.json`](project-buildout/machine/contained-m0-start-state.schema.json);
- [`validate_contained_m0_start_state.py`](../tools/validate_contained_m0_start_state.py);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`TASK-000011`](agent-execution/machine/tasks/TASK-000011.json).

Method:

Added a checked no-claim start-state record and validator. The validator cross-checks that contained M0 continuation remains allowed, broad implementation remains blocked, proposed `TASK-000001` through `TASK-000010` remain proposed, and `TASK-000011` remains `review_pending`. Wired the validator into `xtask check` and linked the new record from the start-here path, docs index, operating board, task queue, readiness matrix, research index, repository map, and `PB-020` readiness evidence.

Decision:

Use the start-state record as a session router. No-claim documentation, research, validation, task-manifest preparation, and `TASK-000011` review-handoff maintenance can continue. Proposed queue tasks still need owner-approved immutable manifests before execution, and broad product work remains blocked.

Impact:

Future maintainers can answer the start question from one checked artifact before reading the full readiness stack. The artifact does not approve tasks, accept `TASK-000011`, promote readiness, prove all information is ready for building, or support Chrome-class, production, release, performance, compatibility, security, accessibility, beta, stable, or daily-driver claims.

Next question:

Should the owner convert one proposed queue row, most likely fresh-host reproduction or IPC hardening, into a reviewed immutable task manifest so implementation can proceed beyond no-claim preparation?

## 2026-07-18 - TASK-000011 no-claim evidence capture

Question:

Can the review-pending `TASK-000011` source evidence be bound to a checked source commit without converting the task into self-approval or `PB-011` readiness?

Inputs:

- checked no-claim [TASK-000011 evidence capture](agent-execution/machine/evidence-bundles/TASK-000011.no-claim.2026-07-18.json);
- [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md);
- [`TASK-000011`](agent-execution/machine/tasks/TASK-000011.json);
- [`evidence-bundle.schema.json`](agent-execution/machine/evidence-bundle.schema.json);
- [`validate_evidence_bundles.py`](../tools/validate_evidence_bundles.py).

Method:

Added a checked non-accepting evidence-bundle record for source commit `4590aad94f298d380d43bffc7b9a5cb618beccac`, including source-file hashes from that commit and successful GitHub validation run references. Added a validator that verifies bundle shape, source-file hashes from the recorded commit, task status, reviewer independence boundaries, and no-claim limitations, then wired it into `xtask check`.

Decision:

Treat the record as source-commit artifact binding only. It does not accept `TASK-000011`, provide an independent reviewer decision, satisfy the accepted evidence-bundle requirement, promote `PB-011`, approve production IPC, or establish any security, performance, compatibility, Chrome-class, release, beta, stable, production, or daily-driver claim.

Impact:

The next reviewer now has checked source-commit artifact evidence to start from, and future evidence-bundle records are validation-covered. `TASK-000011` remains `review_pending`, and accepted independent review remains required before `PB-011` can advance.

Next question:

Should the owner assign an independent reviewer to rerun the checks and replace this non-accepting capture with an accepted or rejected evidence bundle for the exact review commit?

## 2026-07-18 - TASK-000011 WP-002 review handoff

Question:

Can the review-pending `WP-002` M0 reference task be handed to an independent reviewer without relying on scattered source, tests, generated output, CI context, or chat history?

Inputs:

- [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md);
- [`TASK-000011`](agent-execution/machine/tasks/TASK-000011.json);
- [WP-002 kernel identity and IPC reference](research/wp-002-kernel-ipc-2026-07.md);
- [Agent Execution book](agent-execution/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`validate_ipc_capability_boundaries.py`](../tools/validate_ipc_capability_boundaries.py);
- [`validate_ipc_readiness_review.py`](../tools/validate_ipc_readiness_review.py).

Method:

Added a dated review handoff that maps `TASK-000011` acceptance criteria, manifest negative tests, source/test evidence, required review commands, evidence-bundle gaps, and rejection triggers. Updated the human stop/resume docs, research index, operating board, checklist, repository map, WP-002 report, machine evidence lists, and IPC validators to link the packet and enforce the review-pending boundary without changing readiness status.

Decision:

Treat the packet as candidate independent-review organization evidence only. It does not accept `TASK-000011`, create an accepted independent evidence-bundle instance, promote `PB-011`, complete `WP-002`, approve `TASK-000003`, or establish production IPC, process-isolation, site-isolation, renderer-security, agent-security, Chrome-class, performance, compatibility, accessibility, release, beta, stable, or daily-driver claims.

Impact:

The docs now provide a coherent continuation path for either accepting/rejecting `TASK-000011` through independent review or leaving it `review_pending` while continuing another contained M0 lane. `PB-011` remains partial and broad building remains unsupported.

Next question:

Should the owner assign an independent reviewer to produce the `TASK-000011` evidence bundle, or continue the next contained M0 lane such as fresh-host reproduction for `TASK-000002`?

## 2026-07-18 - Execution task ID collision cleanup

Question:

Can the docs answer whether building has started without reusing one `TASK-*` ID for both a proposed build-readiness handoff and an active execution manifest?

Inputs:

- [Agent Execution book](agent-execution/README.md);
- [`TASK-000011`](agent-execution/machine/tasks/TASK-000011.json);
- [WP-002 kernel identity and IPC reference](research/wp-002-kernel-ipc-2026-07.md);
- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`validate_build_foundation.py`](../tools/validate_build_foundation.py).

Method:

Separated the active `WP-002` M0 execution manifest from the proposed build-readiness queue. The proposed queue keeps `TASK-000001` through `TASK-000010`; the implemented `WP-002` reference task is now `TASK-000011` and remains `review_pending`.

Decision:

Treat `TASK-000011` as contained M0 implementation evidence pending independent review. At that time, treat `TASK-000001` through `TASK-000010` as proposed future handoff records only; current state now has specified, non-executable manifests for each proposed row, with the same no-approval boundary.

Impact:

The docs can now state that contained M0 source work has started, but not that broad building is approved. No proposed queue task is approved, running, accepted, or release-gated, and no Chrome-class, production, compatibility, security, accessibility, speed, memory, energy, or daily-driver claim changed.

Next question:

Should the next owner-reviewed manifest accept or reject `TASK-000011`, or should the project first produce fresh-host reproduction evidence for `TASK-000002`?

## 2026-07-18 - Chrome-class capability traceability map

Question:

Can the long-term Chrome-class browser destination be traced to current requirements, work packages, pre-build blockers, task handoffs, evidence owners, and unsupported claims without inventing implementation state?

Inputs:

- [Chrome-Class Capability Traceability Map](research/chrome-class-capability-traceability-map-2026-07.md);
- [Start Here](start-here.md);
- [Capability Parity](blueprint-v1/02-capability-parity.md);
- [Product Requirements](blueprint-v1/21-product-requirements.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`requirements.json`](blueprint-v1/machine/requirements.json);
- [`backlog.json`](blueprint-v1/machine/backlog.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json).

Method:

Mapped existing documentation and machine records across product shell, engine, JavaScript, network/storage/security, media, accessibility, DevTools, extensions, performance, security/updates, AI, build, and ownership domains. No new external browser, benchmark, market, standards, or implementation fact was introduced.

Decision:

Treat the map as no-claim `PB-020` traceability evidence only. It helps maintainers route Chrome-class questions to owners, blockers, next proof, and prohibited claims, but it does not approve tasks or promote readiness.

Impact:

The docs remain organized enough for contained M0 implementation tasks only. Chrome-class, Chrome-equivalent, broad M1, production, release, compatibility, accessibility, security, performance, memory, energy, daily-driver, and all-information-ready-for-building claims remain unsupported.

Next question:

Which bounded M0 `TASK-*` manifest should be owner-approved first: fresh-host reproducibility, IPC/process authority hardening, sandbox probe packaging, or benchmark launch-runner evidence?

## 2026-07-18 - Benchmark engine baseline harness readiness map

Question:

Can the existing no-claim benchmark contracts, manifests, self-tests, and reports be collapsed into one issue `#14`, `PB-013`, and `TASK-000005` stop/resume path before any browser-run performance evidence exists?

Inputs:

- [Benchmark Engine Baseline Harness Readiness Map](research/benchmark-engine-baseline-harness-readiness-map-2026-07.md);
- [Performance Benchmark Readiness Packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Chrome-Class Performance Runbook](research/chrome-class-performance-runbook-2026-07.md);
- [Benchmark Browser Launch-Runner Contract](research/benchmark-browser-launch-runner-contract-2026-07.md);
- [Benchmark Trace/Artifact Package Contract](research/benchmark-trace-artifact-package-contract-2026-07.md);
- [Benchmark 30-Tab Scenario Contract](research/benchmark-30-tab-scenario-contract-2026-07.md);
- [Benchmark Statistics Analysis Contract](research/benchmark-statistics-analysis-contract-2026-07.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json).

Method:

Reviewed the current benchmark readiness packet, Chrome-class runbook, benchmark no-claim contracts, machine readiness records, task queue, operating board, and documentation-readiness matrix. Added a single handoff map that classifies the benchmark lane from Level 0 harness smoke through Level 3 public claim candidate. No new external source was consulted, no browser was launched, and no benchmark sample or competitor result was produced.

Decision:

Treat the map as no-claim `PB-013` organization evidence only. It gives maintainers one place to answer what exists, what remains missing, what an agent may continue, what remains owner-only, and what must not be claimed before issue `#14` or `TASK-000005` continues.

Impact:

`PB-013` remains `documented_no_runner`. The map does not prove a browser-run benchmark runner, browser-run server evidence, trace package, raw sample, memory result, energy result, competitor result, owner-reviewed statistics analysis, owner-reviewed claim bundle, owner-reviewed benchmark readiness, Chrome-class claim, or performance claim.

Next question:

Which Level 1 local-browser launch mode should be implemented first so it can produce no-claim browser-run server evidence, trace/artifact packages, failure-denominator records, and raw artifact hashes without touching real profiles or allowing benchmark claims?

## 2026-07-18 — Servo generated-output source-to-output provenance map

Question:

Which source and license families feed the first-party Servo and pinned Stylo generated-output families already mapped for `ADR9-EV-007`, and what still prevents those generated outputs from becoming decision-grade source-strategy evidence?

Inputs:

- [Servo Generated-Output Source-To-Output Provenance Map](research/servo-generated-output-source-provenance-map-2026-07.md);
- [Servo Generated-Output Generator Manifest](research/servo-generated-output-generator-manifest-2026-07.md);
- [Servo Build-Script and Generated-Output Audit](research/servo-build-script-generated-output-audit-2026-07.md);
- [Servo Clean Generated-Output Reproduction Probe](research/servo-clean-generated-output-reproduction-2026-07.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- external Servo checkout `C:\ts\servo` at commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` and pinned Stylo commit `d3de91cbac7bba38e159239b3c0a360783fce2ee`.

Method:

Statically inspected Servo and Stylo source/license signals for the already mapped generator families: root license files, package license expressions, sampled generator source headers, WebIDL corpus license markers, PLY README license terms, vendored Python wheel metadata, and MarkupSafe license text. No Servo source, generated output, native binary, wheel, package metadata file, or build log was copied into Turing.

Decision:

Record the source-to-output provenance map as partial `ADR9-EV-007` evidence only. It replaces the broad "source-to-output map missing" gap with a sharper owner-reviewed source-to-output license/provenance approval blocker tied to a selected baseline, feature profile, target profile, output-family set, generator-version set, and component boundary.

Impact:

`PB-002` remains blocked. The report does not prove legal approval, generated-output determinism, clean-target generation, independent-host reproducibility, generated-code approval, component approval, source approval, or release-code authorization.

Next question:

Can the generator manifest and provenance map be owner-reviewed for a selected source baseline and feature profile, then replayed through a feature-correct full clean target and independent host with dynamic build tracing?

## 2026-07-18 — Servo generated-output generator manifest

Question:

Which first-party Servo and pinned Stylo generators, inputs, outputs, and environment sensitivities shape `ADR9-EV-007`, and what still prevents generated outputs from becoming decision-grade source-strategy evidence?

Inputs:

- [Servo Generated-Output Generator Manifest](research/servo-generated-output-generator-manifest-2026-07.md);
- [Servo Build-Script and Generated-Output Audit](research/servo-build-script-generated-output-audit-2026-07.md);
- [Servo Clean Generated-Output Reproduction Probe](research/servo-clean-generated-output-reproduction-2026-07.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- external Servo checkout `C:\ts\servo` at commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` and pinned Stylo commit `d3de91cbac7bba38e159239b3c0a360783fce2ee`.

Method:

Inspected first-party Servo and pinned Stylo `build.rs` families, linked Python generators, retained warm and package-scoped clean output-family observations, WebIDL feature gates, and source-family directory digests.

Decision:

Record the manifest as partial `ADR9-EV-007` evidence only. It replaces the broad "generator manifest missing" gap with a sharper owner-reviewed generator-manifest blocker tied to selected baseline, feature profile, target profile, output families, generator versions, environment policy, clean regeneration, and source-to-output provenance.

Impact:

`PB-002` remains blocked. The report does not prove generated-output determinism, source-to-output license/provenance, generated-code approval, component approval, source approval, or release-code authorization.

Next question:

Can the manifest be owner-reviewed for a selected source baseline and feature profile, then replayed through a feature-correct full clean target and independent host with source-to-output provenance?

## 2026-07-18 — Servo clean generated-output reproduction probe

Question:

Can selected Servo generated outputs be regenerated from a clean external target directory without relying on the previously warm Servo target, and what remains before `ADR9-EV-007` can be treated as decision-grade generated-output evidence?

Inputs:

- [Servo Clean Generated-Output Reproduction Probe](research/servo-clean-generated-output-reproduction-2026-07.md);
- [Servo Build-Script and Generated-Output Audit](research/servo-build-script-generated-output-audit-2026-07.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- external Servo checkout `C:\ts\servo` at commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`.

Method:

Ran two isolated package-scoped clean-target attempts outside the Turing repository. The default-media attempt failed before Cargo output inspection because GStreamer was missing. The dummy-media attempt emitted substantial `servo-script-bindings`, Stylo, GLSL, atom, zlib, and Khronos outputs under a clean target, then failed in `mozjs_sys` while trying a JIT-disabled source build.

Decision:

Record the result as partial `ADR9-EV-007` evidence only. The probe narrows the next clean-target work but does not prove a clean Servo build, generated-output determinism, source-to-output provenance, generated-code approval, component approval, or source-strategy readiness.

Impact:

Future `PB-002` work now distinguishes package-scoped dummy-media output from feature-correct full clean-target regeneration. The next evidence must use an owner-selected baseline/profile, retain success and failure logs, compare independent-host output, and map generated outputs to source, license, and provenance.

Next question:

Can a feature-correct full clean-target Servo build regenerate the selected generated-output families with identical hashes on the reference host and an independent clean host or VM?

## 2026-07-18 — Benchmark statistics-analysis contract

Follow-up:

The benchmark claim-bundle schema and no-claim template now require `registry_references.statistics_analysis_plan_id`, and `tools/validate_benchmark_claim_bundles.py` cross-checks that value against the checked no-claim statistics-analysis plan. Future public claim bundles cannot pass validation while bypassing or drifting from the statistics-analysis contract. This remains no-claim evidence only.

The benchmark readiness-review schema and no-claim template now also carry `review_scope.statistics_analysis_plan`, kept null in the template and covered by `tools/validate_benchmark_readiness_review.py`. A future owner-reviewed benchmark readiness record must name the statistics-analysis plan it accepts before statistics, denominator, claim-bundle, benchmark-ready, Chrome-class, or public-performance review can pass.

Question:

Can `PB13-EV-006` have a checked no-claim statistics-analysis contract before runner-generated raw samples, confidence intervals, owner-reviewed benchmark readiness, benchmark results, competitor results, or public performance claims exist?

Inputs:

- [Benchmark Statistics Analysis Contract](research/benchmark-statistics-analysis-contract-2026-07.md);
- [`benchmark-statistics-analysis.schema.json`](blueprint-v1/machine/benchmark-statistics-analysis.schema.json);
- [`no-claim-statistics-analysis-plan.json`](blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json);
- [`tools/validate_benchmark_statistics_analysis.py`](../tools/validate_benchmark_statistics_analysis.py);
- [Performance Benchmark Readiness Packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Chrome-Class Performance Runbook](research/chrome-class-performance-runbook-2026-07.md).

Method:

Added a checked no-claim analysis plan and validator for sample design, warmup, randomization or paired order, noise study, uncertainty, effect size, outlier policy, multiple-comparison interpretation, metric-family summaries, denominator publication, and rejection rules.

Decision:

The raw-result lane needs a checked analysis contract before a runner can turn raw samples into benchmark evidence. Keep `PB-013` partial and `TASK-000005` proposed.

Impact:

Future benchmark work can now distinguish raw artifact shape from statistical evidence and public-claim eligibility. This does not analyze measured browser performance, produce confidence intervals from real samples, approve thresholds, or support benchmark-ready, public performance, Chrome-class, faster, lower-memory, lower-energy, competitor-result, production, or implementation claims.

Next question:

Which `PB-013` blocker should produce executable evidence first: Tier M/Tier L hardware capture, clean OS controls, browser-run server evidence, implemented browser launch runner, or runner-generated raw samples?

## 2026-07-18 — GitHub issue handoff snapshot

Question:

Can post-cleanup GitHub issue and stale-PR state be recorded as a checked offline handoff without treating issue state as task approval, implementation proof, or readiness promotion?

Inputs:

- [GitHub Issue Handoff](project-buildout/19-github-issue-handoff.md);
- [`github-issue-handoff.json`](project-buildout/machine/github-issue-handoff.json);
- [`github-issue-handoff.schema.json`](project-buildout/machine/github-issue-handoff.schema.json);
- [`tools/validate_github_issue_handoff.py`](../tools/validate_github_issue_handoff.py);
- `gh issue list --state all --limit 100 --json number,title,state,url,closedAt,createdAt,updatedAt`;
- `gh pr list --state all --limit 100 --json number,title,state,mergedAt,headRefName,url`;
- `git rev-parse HEAD`.

Method:

Captured the cleaned-up issue/PR state after closing issue #1, updating issue #3, closing stale PRs #42/#43, deleting their branches, and verifying no open PRs. Added a machine snapshot and validator that require the canonical issue set, explain missing issue number #13, record stale PR branch cleanup, and retain unsupported-claim boundaries.

Decision:

Use GitHub issues as coordination pointers only. The handoff maps current issue state to `WP-*`, `PB-*`, `TASK-*`, `RQ-*`, and milestone records but does not approve tasks, promote readiness, prove implementation, or replace live GitHub checks.

Impact:

A maintainer can now resume after branch or issue cleanup without re-opening stale draft branches or mistaking open/closed issue state for canonical project status. Remaining active issues #2-#12 and #14 stay open because their acceptance evidence remains incomplete.

Next question:

Which open issue should receive the next owner-reviewed task manifest: `#2`/`WP-002` IPC completion, `#3`/`WP-003` sandbox probes, or `#12`/`#14`/`PB-013` benchmark harness evidence?

## 2026-07-18 — Implementation master plan import

Question:

Can the stale draft implementation-plan branch be ported onto current `main` as checked execution documentation without granting work-package approval, broad implementation readiness, preview, beta, stable, production, release, or product-readiness claims?

Inputs:

- [Implementation Master Plan](project-buildout/implementation-plan/README.md);
- [Full implementation game plan audit](research/full-implementation-game-plan-audit-2026-07.md);
- [`implementation-execution-graph.json`](blueprint-v1/machine/implementation-execution-graph.json);
- [`implementation-milestone-gates.json`](blueprint-v1/machine/implementation-milestone-gates.json);
- [`implementation-interface-freezes.json`](blueprint-v1/machine/implementation-interface-freezes.json);
- [`implementation-evidence-catalog.json`](blueprint-v1/machine/implementation-evidence-catalog.json);
- [`implementation-task-sequence.json`](blueprint-v1/machine/implementation-task-sequence.json);
- [`tools/validate_implementation_plan.py`](../tools/validate_implementation_plan.py).

Method:

Ported the additive implementation-plan documentation, machine registries, validator, and CI workflow onto current `main`, then integrated them into the repository map, start-here path, project-buildout handbook, research index, aggregate blueprint validation, and `xtask check`.

Decision:

Treat the plan as dependency-ordered execution documentation only. It can guide sequencing, handoffs, milestone gate criteria, evidence classes, and stop/replan triggers, but only a reviewed `TASK-*` manifest authorizes production implementation.

Impact:

The project now has a checked M0-to-M9 implementation plan and machine-readable execution graph on current `main` without raw-merging the stale draft branch or deleting current repository state. The plan preserves the no-claim boundary for implementation, preview, beta, stable, production, release, compatibility, performance, security, accessibility, and product readiness.

Next question:

Which bounded `TASK-*` manifest should be owner-reviewed first under the implementation plan: source strategy, native shell, IPC, sandbox probes, benchmark runner, profile/storage, release operations, incident response, or ownership controls?

## 2026-07-18 — WP-003 sandbox probe contract

Question:

Can `PB-012` and `TASK-000004` gain a checked operation catalog, evidence-bundle schema, and focused validator before executable packaged probes, effective platform policy, owner-reviewed sandbox readiness, sandbox-readiness, renderer-security, site-isolation, hostile-browsing safety, `SEC-GATE-*`, production-safety, or implementation claims exist?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [WP-003 Sandbox Probe Contract](research/wp-003-sandbox-probe-plan-2026-07.md);
- [`probe-catalog.json`](../schemas/sandbox/probe-catalog.json);
- [`probe-evidence.schema.json`](../schemas/sandbox/probe-evidence.schema.json);
- [`tools/validate_sandbox_contracts.py`](../tools/validate_sandbox_contracts.py);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json).

Method:

Added a checked no-claim WP-003 operation catalog and evidence schema, then added focused and aggregate validation for exact probe IDs, no-destructive-host targets, three allowed controls, result enums, unsupported-as-not-pass behavior, application-level stub rejection, redaction requirements, `research_evidence_only` release claims, `PB-012` evidence, `TASK-000004` scope, and research-index/report links.

Decision:

Keep `PB-012` partial and `TASK-000004` proposed. The contract defines what future executable sandbox probe packages must report, but it does not execute probes, prove platform containment, approve sandbox adapters, complete owner-reviewed sandbox readiness, or support security, release, production, or implementation claims.

Impact:

Future `TASK-000004` work now has a stable no-claim operation/evidence contract in addition to the inventory, package template, and readiness-review template. Any real probe result must replace planning-only fields with retained platform evidence, unsandboxed control runs, redacted artifacts, cleanup checks, and owner-reviewed sandbox readiness beyond the checked no-claim readiness-review template.

Next question:

Which `PB-012` blocker should become executable evidence first: packaged role runner, effective platform-policy capture, safe fixture package, broker fixture, compromised-client harness, result artifact package, or platform matrix execution?

## 2026-07-18 — Benchmark readiness-review template

Question:

Can `PB-013` and `TASK-000005` gain one checked owner-review handoff object before approved hardware tiers, clean OS-control review, representative corpus review, browser-run server evidence review, implemented browser launch runner review, benchmark-ready browser pin review, trace-artifact review, raw result review, 30-tab artifact review, statistics review, denominator review, equal-workload review, owner-reviewed claim bundles, owner-reviewed benchmark readiness, benchmark-ready status, public performance, faster, lower-memory, lower-energy, Chrome-class, competitor-result, daily-driver, production, or implementation claims exist?

Inputs:

- [Performance Benchmark Readiness Packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [`benchmark-claim-bundle.schema.json`](blueprint-v1/machine/benchmark-claim-bundle.schema.json);
- [`no-claim-public-claim-template.json`](blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json);
- [`benchmark-readiness-review.schema.json`](blueprint-v1/machine/benchmark-readiness-review.schema.json);
- [`no-claim-benchmark-readiness-template.json`](blueprint-v1/machine/benchmark-readiness-reviews/no-claim-benchmark-readiness-template.json);
- [`tools/validate_benchmark_readiness_review.py`](../tools/validate_benchmark_readiness_review.py).

Method:

Added a checked no-claim benchmark readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null reviewer and evidence fields, hardware/OS axes, corpus/network axes, runner/artifact axes, browser-pin comparison axes, statistics/denominator axes, claim-review axes, rejection rules, validation commands, `PB-013` evidence, `TASK-000005` scope, and benchmark research-lane crosswalk coverage.

Decision:

Keep `PB-013` documented as no-runner. The template defines what a future real owner-reviewed benchmark readiness review must replace, but it does not approve hardware tiers, prove clean OS controls, approve a representative corpus, create browser-run server evidence, implement or review the launch runner, pin benchmark-ready browsers, create trace artifacts, review raw results, run a 30-tab scenario, approve statistics, prove equal workloads, approve claim bundles, approve benchmark readiness, or support performance, memory, energy, Chrome-class, competitor, production, daily-driver, or implementation claims.

Impact:

Future `TASK-000005` work now has a cross-scope readiness-review handoff object in addition to the benchmark readiness packet and claim-bundle template. Any real review must replace null hardware, corpus, server, runner, trace, result, browser-pin, claim-bundle, owner reviewer, performance reviewer, benchmark operations reviewer, quality reviewer, security reviewer, accessibility reviewer, and release-operations reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-013` blocker should become real evidence first: fixed hardware tiers, clean OS controls, corpus/server packaging, launch-runner implementation, trace artifacts, 30-tab output, raw result retention, statistics review, equal-workload proof, or owner-reviewed claim bundles?

## 2026-07-18 — Sandbox readiness-review template

Question:

Can `PB-012` and `TASK-000004` gain one checked owner-review handoff object before packaged expected-deny probes, effective platform policy, host-safe fixture review, broker fixture review, compromised-client harness review, platform matrix review, result-record review, failure-denominator review, cleanup review, `PB-012` readiness promotion, sandbox-readiness, renderer-security, site-isolation, hostile-browsing safety, platform containment, `SEC-GATE-1`, `SEC-GATE-6`, production-safety, or implementation claims exist?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [`sandbox-probe-inventory.json`](security-engine/machine/sandbox-probe-inventory.json);
- [`sandbox-probe-package.schema.json`](security-engine/machine/sandbox-probe-package.schema.json);
- [`no-claim-expected-deny-template.json`](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json);
- [`sandbox-readiness-review.schema.json`](security-engine/machine/sandbox-readiness-review.schema.json);
- [`no-claim-sandbox-readiness-template.json`](security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json);
- [`tools/validate_sandbox_readiness_review.py`](../tools/validate_sandbox_readiness_review.py).

Method:

Added a checked no-claim sandbox readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null inventory/package/reviewer fields, probe-package axes, platform-policy axes, role/surface axes, host-safety axes, broker/compromised-client axes, owner-review axes, rejection rules, validation commands, `PB-012` evidence, `TASK-000004` scope, and sandbox research-lane crosswalk coverage.

Decision:

Keep `PB-012` partial. The template defines what a future real owner-reviewed sandbox readiness review must replace, but it does not execute packaged probes, capture effective platform policy, prove host-safe fixtures, prove broker fixtures, run compromised-client harnesses, complete a platform matrix, review result records, support `SEC-GATE-*`, prove renderer security, prove site isolation, prove hostile-browsing safety, approve production safety, or support implementation claims.

Impact:

Future `TASK-000004` work now has a cross-scope readiness-review handoff object in addition to the sandbox probe inventory and probe-package template. Any real review must replace null probe inventory, probe package, owner reviewer, security reviewer, platform reviewer, quality reviewer, and release-operations reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-012` blocker should become real evidence first: packaged role runner, effective platform policy capture, host-safe fixtures, broker fixtures, compromised-client harnesses, result records, or platform matrix execution?

## 2026-07-18 — IPC readiness-review template

Question:

Can `PB-011` and `TASK-000003` gain one checked owner-review handoff object before an implemented schema generator, approved generator source, wire encoding decision, generated types, generated validators, generated fixtures, connection authentication, bounded queues/backpressure, timeout/cancellation behavior, stale-epoch receiver proof, negative-test review, fuzz/model-test review, process-capability generation review, `PB-011` readiness promotion, renderer-security, agent-security, process-isolation, site-isolation, production IPC, or implementation claims exist?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [`ipc-capability-boundary.json`](blueprint-v1/machine/ipc-capability-boundary.json);
- [`ipc-schema-source.schema.json`](blueprint-v1/machine/ipc-schema-source.schema.json);
- [`no-claim-control-envelope-template.json`](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json);
- [`ipc-readiness-review.schema.json`](blueprint-v1/machine/ipc-readiness-review.schema.json);
- [`no-claim-ipc-readiness-template.json`](blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json);
- [`tools/validate_ipc_readiness_review.py`](../tools/validate_ipc_readiness_review.py).

Method:

Added a checked no-claim IPC readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null boundary/schema/reviewer fields, schema-generator axes, wire-transport axes, authority/identity axes, negative-test axes, owner-review axes, rejection rules, validation commands, `PB-011` evidence, `TASK-000003` scope, and IPC research-lane crosswalk coverage.

Decision:

Keep `PB-011` partial. The template defines what a future real owner-reviewed IPC readiness review must replace, but it does not implement or approve a schema generator, select wire encoding, generate types or validators, authenticate IPC connections, prove bounded queues/backpressure, define timeout/cancellation behavior, reject stale epochs, review negative tests, prove renderer security, prove agent security, prove process isolation, prove site isolation, approve production IPC, or support implementation claims.

Impact:

Future `TASK-000003` work now has a cross-scope readiness-review handoff object in addition to the IPC boundary inventory and schema-source template. Any real review must replace null boundary inventory, schema-source template, schema generator, wire encoding decision, owner reviewer, security reviewer, architecture reviewer, API reviewer, and performance reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-011` blocker should become real evidence first: schema generator source, wire encoding decision, connection authentication, bounded queues/backpressure, stale-epoch receiver rejection, timeout/cancellation behavior, or negative-test fixture generation?

## 2026-07-18 — Fresh-host readiness-review template

Question:

Can `PB-009` and `TASK-000002` gain one checked owner-review handoff object before independent fresh-host reproduction, owner-approved clean-VM equivalence, retained bootstrap/doctor/check/xtask logs, source-tree cleanliness review, failure-denominator review, rollback/cleanup review, environmental-waiver review, `PB-009` readiness promotion, release confidence, production readiness, implementation, or Chrome-class claims exist?

Inputs:

- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json);
- [`fresh-host-reproduction.schema.json`](project-buildout/machine/fresh-host-reproduction.schema.json);
- [`fresh-host-run-record.schema.json`](project-buildout/machine/fresh-host-run-record.schema.json);
- [`no-claim-run-record-template.json`](project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json);
- [`fresh-host-readiness-review.schema.json`](project-buildout/machine/fresh-host-readiness-review.schema.json);
- [`no-claim-fresh-host-readiness-template.json`](project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json);
- [`tools/validate_fresh_host_readiness_review.py`](../tools/validate_fresh_host_readiness_review.py).

Method:

Added a checked no-claim fresh-host readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null run-record/reference-host/clean-VM-waiver/reviewer fields, host-identity axes, source-checkout axes, command-execution axes, cache/artifact axes, failure-review axes, owner-review axes, rejection rules, validation commands, `PB-009` evidence, `TASK-000002` scope, and fresh-host research-lane crosswalk coverage.

Decision:

Keep `PB-009` partial. The template defines what a future real owner-reviewed fresh-host readiness review must replace, but it does not prove an independent fresh-host run, approve a clean-VM equivalent, review command execution, accept retained logs, prove source-tree cleanliness, accept failures or waivers, promote `PB-009`, create release confidence, approve production readiness, authorize implementation, or support Chrome-class claims.

Impact:

Future `TASK-000002` work now has both a per-run evidence record and a cross-scope readiness-review handoff object. Any real review must replace null run record, reference host, clean-VM waiver, owner reviewer, independent reviewer, release-operations reviewer, and quality reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-009` blocker should become real evidence first: reference-host designation, clean-VM waiver policy, retained command-log capture, cache/target-directory proof, source-tree cleanliness proof, or failure-denominator review?

## 2026-07-18 — Backup-ownership readiness-review template

Question:

Can `PB-019` and `TASK-000008` gain one checked owner-review handoff object before named qualified backups, owner identity verification, role-level review, subsystem competence review, path coverage, recent review records, availability evidence, succession evidence, recusal review, inactive-owner replacement, CODEOWNERS reconciliation, review-rule reconciliation, escalation-policy reconciliation, repository-access review, stale-access review, ownerless-path review, primary-only-path review, two-person control, owner coverage, release authority, signing authority, security-disclosure authority, legal approval, incident closure, production authority, broad readiness, or implementation claims exist?

Inputs:

- [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md);
- [`backup-ownership-gap.json`](project-buildout/machine/backup-ownership-gap.json);
- [`backup-ownership-gap.schema.json`](project-buildout/machine/backup-ownership-gap.schema.json);
- [`backup-owner-qualification-record.schema.json`](project-buildout/machine/backup-owner-qualification-record.schema.json);
- [`no-claim-backup-owner-qualification-template.json`](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json);
- [`backup-ownership-readiness-review.schema.json`](project-buildout/machine/backup-ownership-readiness-review.schema.json);
- [`no-claim-backup-ownership-readiness-template.json`](project-buildout/machine/backup-ownership-readiness-reviews/no-claim-backup-ownership-readiness-template.json);
- [`tools/validate_backup_ownership_readiness_review.py`](../tools/validate_backup_ownership_readiness_review.py).

Method:

Added a checked no-claim backup-ownership readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null inventory/qualification/reviewer fields, critical-scope coverage, qualification axes, reconciliation axes, two-person-control axes, authority-boundary axes, owner-review axes, rejection rules, validation commands, `PB-019` evidence, `TASK-000008` scope, and ownership research-lane crosswalk coverage.

Decision:

Keep `PB-019` blocked. The template defines what a future real owner-reviewed backup ownership readiness review must replace, but it does not name qualified backups, verify identity, prove role level, prove subsystem competence, prove path coverage, prove review history, prove availability, reconcile CODEOWNERS or access, create two-person control, provide owner coverage, grant release authority, grant signing authority, approve disclosure, approve legal posture, close incidents, create production authority, approve broad readiness, or support implementation.

Impact:

Future `TASK-000008` work now has both per-backup qualification and cross-scope readiness-review handoff objects. Any real review must replace null ownership inventory, qualification record set, owner reviewer, independent reviewer, security reviewer, release-operations reviewer, legal reviewer, and support reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-019` blocker should become real evidence first: named backup candidates, role/subsystem qualification records, CODEOWNERS and review-rule reconciliation, repository access and stale-access review, ownerless/primary-only path review, or two-person-control evidence?

## 2026-07-18 — Incident/patch readiness-review template

Question:

Can `PB-018` and `TASK-000010` gain one checked owner-review handoff object before executed private-intake tabletop output, emergency patch dry-run records, regression/backport evidence, signing/update dry-run evidence, coordinated disclosure rehearsal, postmortem evidence, role matrix review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported security versions, production-safe browsing, disclosure authority, stable promotion, signing authority, incident closure authority, or implementation claims exist?

Inputs:

- [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md);
- [`incident-patch-rehearsal.json`](security-engine/machine/incident-patch-rehearsal.json);
- [`incident-patch-rehearsal.schema.json`](security-engine/machine/incident-patch-rehearsal.schema.json);
- [`incident-patch-rehearsal-record.schema.json`](security-engine/machine/incident-patch-rehearsal-record.schema.json);
- [`no-claim-incident-patch-rehearsal-template.json`](security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json);
- [`incident-patch-readiness-review.schema.json`](security-engine/machine/incident-patch-readiness-review.schema.json);
- [`no-claim-incident-patch-readiness-template.json`](security-engine/machine/incident-patch-readiness-reviews/no-claim-incident-patch-readiness-template.json);
- [`tools/validate_incident_patch_readiness_review.py`](../tools/validate_incident_patch_readiness_review.py).

Method:

Added a checked no-claim incident/patch readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null rehearsal/reference/private-channel/reviewer fields, private-intake axes, emergency-patch axes, incident-class axes, role-authority axes, evidence-control axes, owner-review axes, rejection rules, validation commands, `PB-018` evidence, `TASK-000010` scope, and incident/patch research-lane crosswalk coverage.

Decision:

Keep `PB-018` partial. The template defines what a future real owner-reviewed incident/patch readiness review must replace, but it does not approve executed private-intake tabletop output, emergency patch dry-run records, regression/backport evidence, signing/update dry-run evidence, coordinated disclosure rehearsal, postmortem evidence, role matrix review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported security versions, production-safe browsing, disclosure authority, stable promotion, signing authority, incident closure authority, or implementation.

Impact:

Future incident/patch work starts from a checked handoff object tying the inventory, rehearsal template, `PB-018`, and `TASK-000010` together. Any real review must replace null rehearsal record, reference platform, private channel, owner reviewer, independent reviewer, security reviewer, release-operations reviewer, legal reviewer, and support reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-018` blocker should become executable evidence first: private-intake tabletop, emergency patch dry run, regression/backport proof, disclosure rehearsal, role matrix review, or backup-owner coverage?

## 2026-07-18 — Package/update readiness-review template

Question:

Can `PB-017` and `TASK-000009` gain one checked owner-review handoff object before executable package manifests, update metadata parsers, signature threshold tests, staged install tests, rollback/migration tests, production-key separation review, release readiness, supported security, production updater, stable channel, public distribution, signing readiness, or implementation claims exist?

Inputs:

- [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md);
- [`research-package-update-lab.json`](release-operations/machine/research-package-update-lab.json);
- [`research-package-update-lab-package.schema.json`](release-operations/machine/research-package-update-lab-package.schema.json);
- [`no-claim-update-lab-template.json`](release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json);
- [`research-package-update-readiness-review.schema.json`](release-operations/machine/research-package-update-readiness-review.schema.json);
- [`no-claim-research-package-update-readiness-template.json`](release-operations/machine/research-package-update-readiness-reviews/no-claim-research-package-update-readiness-template.json);
- [`tools/validate_research_package_update_readiness_review.py`](../tools/validate_research_package_update_readiness_review.py).

Method:

Added a checked no-claim research package/update readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null lab-package/reference-platform/fixture-policy/reviewer fields, package, metadata, rollback, fixture, security/release, owner-review axes, rejection rules, validation commands, `PB-017` evidence, `TASK-000009` scope, and package/update research-lane crosswalk coverage.

Decision:

Keep `PB-017` partial. The template defines what a future real owner-reviewed package/update readiness review must replace, but it does not approve executable package manifests, update metadata parsers, signature threshold tests, staged install tests, rollback or migration tests, production-key separation, release readiness, supported security, production updater status, stable channel, public distribution, signing readiness, or implementation.

Impact:

Future package/update work starts from a checked handoff object tying the inventory, update-lab package template, `PB-017`, and `TASK-000009` together. Any real review must replace null lab-package, reference-platform, fixture-policy, owner-reviewer, independent-reviewer, release-operations-reviewer, security-reviewer, and privacy-reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-017` blocker should become executable evidence first: package manifest generation, update metadata parsing, fake-key signature threshold tests, staged install faults, rollback/migration tests, or production-key separation review?

## 2026-07-18 — Profile/session readiness-review template

Question:

Can `PB-016` and `TASK-000007` gain one checked owner-review handoff object before executable profile/session schemas, migration/fault tests, real-profile fixture approval, private-session readiness, protected-work readiness, data-loss safety, user-data handling readiness, production profile-format approval, sync, credential storage, release-path approval, or implementation claims exist?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [`profile-session-format-inventory.json`](storage/machine/profile-session-format-inventory.json);
- [`profile-session-schema-package.schema.json`](storage/machine/profile-session-schema-package.schema.json);
- [`no-claim-profile-session-schema-template.json`](storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json);
- [`profile-session-readiness-review.schema.json`](storage/machine/profile-session-readiness-review.schema.json);
- [`no-claim-profile-session-readiness-template.json`](storage/machine/profile-session-readiness-reviews/no-claim-profile-session-readiness-template.json);
- [`tools/validate_profile_session_readiness_review.py`](../tools/validate_profile_session_readiness_review.py).

Method:

Added a checked no-claim profile/session readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null schema-package/reference-platform/fixture-policy/reviewer fields, format, behavior, migration, fixture, privacy, owner-review axes, rejection rules, validation commands, `PB-016` evidence, `TASK-000007` scope, and profile/session research-lane crosswalk coverage.

Decision:

Keep `PB-016` partial. The template defines what a future real owner-reviewed profile/session readiness review must replace, but it does not approve executable schemas, migration or fault tests, real-profile fixtures, private-session readiness, protected-work readiness, data-loss safety, user-data handling readiness, production profile formats, sync, credential storage, release paths, or implementation.

Impact:

Future profile/session work starts from a checked handoff object tying the inventory, schema-package template, `PB-016`, and `TASK-000007` together. Any real review must replace null schema-package, reference-platform, fixture-policy, owner-reviewer, independent-reviewer, and privacy-reviewer fields with retained evidence beyond the template.

Next question:

Which `PB-016` blocker should become executable evidence first: schema package, migration/fault tests, real-profile fixture policy, private-session/protected-work behavior, or privacy and data-loss review?

## 2026-07-18 — Native UI readiness-review template

Question:

Can `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006` gain one checked owner-review handoff object before any `ADR-0013`, `ADR-0014`, `ADR-0016`, `UI-GATE-7`, `UI-GATE-10`, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, release-path UI approval, production claim, or implementation claim exists?

Inputs:

- [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md);
- [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md);
- [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md);
- [`native-ui-readiness-review.schema.json`](ui-runtime/machine/native-ui-readiness-review.schema.json);
- [`no-claim-native-ui-readiness-template.json`](ui-runtime/machine/native-ui-readiness-reviews/no-claim-native-ui-readiness-template.json);
- [`tools/validate_native_ui_readiness_review.py`](../tools/validate_native_ui_readiness_review.py).

Method:

Added a checked no-claim native UI readiness-review schema and template, then added focused and aggregate validation for false readiness flags, null selected toolkit/adapter/platform/reviewer fields, gate axes, adapter/framework/page-surface/fixture/accessibility/release-exclusion/owner-review axes, rejection rules, validation commands, `PB-*` evidence, `TASK-000006` scope, and native-lane crosswalk coverage.

Decision:

Keep `PB-003`, `PB-004`, `PB-005`, `PB-014`, and `PB-015` partial. The template defines what a future real owner-reviewed native UI readiness review must replace, but it does not select a toolkit, accept an ADR, pass a UI gate, approve page-surface or accessibility readiness, authorize release-path UI, or support production or implementation claims.

Impact:

Future native shell work starts from one checked handoff object tying the five partial native UI gates and `TASK-000006` together. Any real review must replace null selected-toolkit, adapter-strategy, reference-platform, owner-reviewer, and independent-reviewer fields with retained evidence beyond the template.

Next question:

Which native UI blocker should become executable evidence first: `ADR-0013` adapter contracts, equivalent framework adapters, `UI-GATE-7` page-surface proof, rendered fixture packs, or reference-platform accessibility workflows?

## 2026-07-18 — ADR-0009 decision-review template

Question:

Can `PB-002` gain a checked ADR-0009 owner-review handoff object before any Servo source strategy, source baseline, component approval, source import, release-code authorization, readiness promotion, or implementation authority exists?

Inputs:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Decision Draft and Public-Claim Impact](project-buildout/16-adr-0009-decision-draft.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [`adr-0009-decision-review.schema.json`](blueprint-v1/machine/adr-0009-decision-review.schema.json);
- [`no-claim-decision-review-template.json`](blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json);
- [`tools/validate_adr_0009_evidence.py`](../tools/validate_adr_0009_evidence.py).

Method:

Added a checked no-claim ADR-0009 decision-review schema and template, then extended ADR-0009 evidence validation to require null option/baseline/reviewer fields, false decision-status flags, all `ADR9-EV-001` through `ADR9-EV-018` axes, option axes, owner-review axes, required document updates, rejection rules, unsupported boundaries, validation commands, and `PB-002` evidence.

Decision:

Keep `PB-002` blocked and keep `ADR-0009` at `no_source_strategy_decision`. The template defines what a future real owner-reviewed decision record must replace, but it does not select an option, approve Servo, import source, approve dependencies/components, change JavaScript runtime direction, authorize release code, or promote readiness.

Impact:

Future `TASK-000001` and `ADR9-EV-018` work now starts from a checked no-claim decision-review handoff object and must replace template-only null selected option, source baseline, feature profile, owner reviewer, independent reviewer, and false status flags with owner-reviewed evidence or explicit blocked status.

Next question:

Which `ADR9-EV-*` item should be closed, explicitly rejected, or converted into an expiring owner-approved exception first before a real ADR-0009 decision review can exist?

## 2026-07-18 — Build-readiness closure-review template

Question:

Can `PB-020` gain a checked no-claim closure-review handoff object before any owner-reviewed broad M1, all-information-ready-for-building, release, production, Chrome-class, performance, compatibility, security, accessibility, task-approval, readiness-promotion, or daily-driver claim exists?

Inputs:

- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [Implementation Kickoff Review Inventory](research/implementation-kickoff-review-inventory-2026-07.md);
- [Build Readiness Dependency Graph](research/build-readiness-dependency-graph-inventory-2026-07.md);
- [`build-readiness-closure-review.schema.json`](project-buildout/machine/build-readiness-closure-review.schema.json);
- [`no-claim-build-readiness-closure-template.json`](project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json);
- [`tools/validate_documentation_readiness_completion_audit.py`](../tools/validate_documentation_readiness_completion_audit.py).

Method:

Added a checked no-claim build-readiness closure-review schema and template, then extended the documentation-readiness completion-audit validator and aggregate blueprint validator to require the template, false closure flags, unresolved gate axes, owner-review axes, release-authority axes, lifecycle stages, rejection rules, validation commands, and `PB-020` evidence.

Decision:

Keep `PB-020` partial. The template defines what a future real build-readiness closure review must replace, but it does not close remaining P0 gates, approve tasks, grant release or production authority, or support all-information-ready-for-building language.

Impact:

Future build-readiness closure work now starts from a checked no-claim handoff object and must replace template-only null reviewers and false status flags with owner-reviewed evidence across source strategy, fresh-host reproduction, IPC, sandbox, benchmark, native-shell, page-surface, profile/session, package/update, incident-response, backup-ownership, owner-review, and release-authority gates.

Next question:

Which unresolved `PB-*` gate should receive owner-reviewed closure evidence first before a real build-readiness closure record can exist?

## 2026-07-18 — Backup-owner qualification template

Question:

Can `PB-019` gain a checked qualification handoff object before any named qualified backups, owner identity verification, role-level review, subsystem competence review, path coverage, availability record, CODEOWNERS reconciliation, stale-access review, two-person control, or owner-coverage authority exists?

Inputs:

- [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md);
- [Project-buildout handbook](project-buildout/README.md);
- [Ownership, CODEOWNERS, and Maintainer Ladder](project-buildout/02-ownership-codeowners-and-maintainer-ladder.md);
- [Release, Incident, Legal, Data, and Support Operations](project-buildout/08-release-incident-legal-data-and-support.md);
- [`backup-owner-qualification-record.schema.json`](project-buildout/machine/backup-owner-qualification-record.schema.json);
- [`no-claim-backup-owner-qualification-template.json`](project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json);
- [`tools/validate_backup_ownership_gap.py`](../tools/validate_backup_ownership_gap.py).

Method:

Added a checked no-claim backup-owner qualification schema and template, then extended backup ownership validation to require null candidate fields, false qualification flags, qualification axes, reconciliation axes, two-person-control axes, lifecycle stages, placeholder rejection, authority-boundary rejection rules, unsupported claims, validation commands, and `PB-019` evidence.

Decision:

Keep `PB-019` blocked. The template defines what a future real backup-owner qualification record must replace, but it does not name qualified backups, verify identity, prove role level, prove subsystem competence, prove path coverage, prove review history, prove availability, reconcile CODEOWNERS or access, create two-person control, or provide owner coverage.

Impact:

Future `TASK-000008` work now starts from a checked no-claim backup-owner qualification handoff object and must replace template-only null candidate fields with named qualified backup, role-level, subsystem-competence, representative-path, review-record, availability, succession, recusal, inactivity, removal, emergency-replacement, reconciliation, two-person-control, and owner-review evidence. The current repository still needs backup-owner evidence beyond the checked no-claim backup-owner qualification template before any owner-coverage, release-authority, signing-authority, update-trust, security-disclosure, legal-approval, incident-closure, production-authority, broad-readiness, or implementation claim.

Next question:

Which real backup-owner candidates and qualification records should instantiate the checked template first without using placeholders, private contact details, title-only ownership, or documentation intent as authority?

## 2026-07-18 — Incident patch rehearsal-record template

Question:

Can `PB-018` gain a checked rehearsal handoff object before any executed private-intake tabletop, emergency patch dry run, regression/backport evidence, signing/update dry run, disclosure rehearsal, role review, backup-owner coverage, or incident-response authority exists?

Inputs:

- [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md);
- [Security policy](security.md);
- [Security Verification and Release Gates](security-engine/06-security-verification-and-release-gates.md);
- [Vulnerability Response and Supported Lifecycle](release-operations/08-vulnerability-response-and-supported-lifecycle.md);
- [`incident-patch-rehearsal-record.schema.json`](security-engine/machine/incident-patch-rehearsal-record.schema.json);
- [`no-claim-incident-patch-rehearsal-template.json`](security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json);
- [`tools/validate_incident_patch_rehearsal.py`](../tools/validate_incident_patch_rehearsal.py).

Method:

Added a checked no-claim incident patch rehearsal-record schema and template, then extended incident patch rehearsal validation to require private-intake axes, emergency-patch axes, incident classes, authority roles, lifecycle stages, fake-vulnerability fixture policy, rejection rules, unsupported boundaries, validation commands, `PB-018` evidence, and `TASK-000010` scope.

Decision:

Keep `PB-018` partial. The template defines what a future fake-vulnerability private tabletop and emergency patch dry run must record, but it does not provide executed tabletop output, emergency patch output, regression/backport evidence, signing/update dry-run evidence, disclosure rehearsal, role review, backup-owner coverage, incident-response readiness, emergency patch capacity, supported-security evidence, or production-safe browsing evidence.

Impact:

Future `TASK-000010` work now starts from a checked no-claim incident patch rehearsal handoff object and must replace template-only fields with private tabletop, fake vulnerability, patch-branch, embargoed-CI, regression, backport, signing/update dry-run, disclosure, postmortem, role, backup-owner, cleanup, and owner-review evidence. The current repository still needs executable incident-response and emergency patch evidence beyond the checked no-claim incident patch rehearsal template before any incident-response, emergency-patch, supported-security, disclosure, signing, stable-promotion, incident-closure, or production-safe browsing claim.

Next question:

Which private tabletop and fake emergency patch harness should instantiate the checked template without publishing exploitable details or granting agents severity, disclosure, signing, stable-promotion, or incident-closure authority?

## 2026-07-18 — Research package/update lab-package template

Question:

Can `PB-017` gain a checked update-lab package handoff object before any executable package manifest, update metadata parser, signature threshold tests, staged install tests, rollback migration tests, production signing keys, offline root keys, stable channel, real updater, public distribution, or real-profile migration evidence exists?

Inputs:

- [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md);
- [Release Operations book](release-operations/README.md);
- [Update, Supply Chain, and Vulnerability Response](security-engine/05-update-supply-chain-and-vulnerability-response.md);
- [`research-package-update-lab-package.schema.json`](release-operations/machine/research-package-update-lab-package.schema.json);
- [`no-claim-update-lab-template.json`](release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json);
- [`validate_research_package_update_lab.py`](../tools/validate_research_package_update_lab.py).

Method:

Added a checked no-claim update-lab package schema and template, then extended research package/update lab validation to require manifest fields, metadata behavior axes, lab lifecycle stages, fake-key/local-metadata fixture policy, rejection rules, unsupported boundaries, validation commands, `PB-017` evidence, and `TASK-000009` scope.

Decision:

Keep `PB-017` partial. The template defines what a future executable fake-key local update-lab package must record, but it does not provide executable package manifests, metadata parsers, signature threshold tests, staged install tests, rollback or migration lab evidence, production-key review, owner review, release readiness, rollback safety, migration safety, supported security, or production updater evidence.

Impact:

Future `TASK-000009` work now starts from a checked update-lab package handoff object and must replace template-only fields with executable package-manifest, metadata-parser, signature-threshold, staged-install, rollback/migration, privacy-event, cleanup, and owner-review evidence. The current repository still needs executable update-lab evidence beyond the checked no-claim update-lab package template before any updater, release, rollback, migration, or supported-security claim.

Next question:

Which fake-key local package-manifest generator and update metadata parser should instantiate the checked template without creating a real updater, stable channel, public distribution path, or real-profile migration path?

## 2026-07-18 — Profile/session schema-package template

Question:

Can `PB-016` gain a checked schema-package handoff object before any executable profile, Space, session, snapshot, migration, or real-profile migration evidence exists?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [Storage and Recovery](storage/README.md);
- [Everyday Product Workflows](product-experience/README.md);
- [Network, Storage, Media, and Platform Services](blueprint-v1/07-network-storage-media.md);
- [`profile-session-schema-package.schema.json`](storage/machine/profile-session-schema-package.schema.json);
- [`no-claim-profile-session-schema-template.json`](storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json);
- [`validate_profile_session_formats.py`](../tools/validate_profile_session_formats.py).

Method:

Added a checked no-claim profile/session schema-package schema and template, then extended profile/session validation to require format targets, behavior axes, schema record requirements, migration lifecycle stages, fixture policy, rejection rules, unsupported boundaries, validation commands, `PB-016` evidence, and `TASK-000007` scope.

Decision:

Keep `PB-016` partial. The template defines what a future executable schema package must record, but it does not provide executable schemas, migration tests, fault tests, real-profile fixture approval, owner review, real-profile migration, sync, credential storage, data-loss safety, user-data handling readiness, or production profile-format evidence.

Impact:

Future `TASK-000007` work now starts from a checked schema-package handoff object and must replace template-only fields with executable schema, migration-test, fault-test, fixture-policy, and owner-review evidence. The current repository still needs executable schemas beyond the checked no-claim schema-package template before any profile/session, migration, or data-loss claim.

Next question:

Which executable schema fixture harness should instantiate the checked template for profile, Space, session, snapshot, and migration records without touching real user profiles?

## 2026-07-18 — Sandbox probe-package template

Question:

Can `PB-012` gain a checked expected-deny probe-package handoff object before any packaged sandbox probe, effective platform-policy capture, or security-gate evidence exists?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [Security, Privacy, and Sandbox Model](blueprint-v1/08-security-and-sandbox.md);
- [Sandbox Brokers and Platform Containment](security-engine/02-sandbox-brokers-and-platform-containment.md);
- [Security Verification and Release Gates](security-engine/06-security-verification-and-release-gates.md);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- [`sandbox-probe-package.schema.json`](security-engine/machine/sandbox-probe-package.schema.json);
- [`no-claim-expected-deny-template.json`](security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json);
- [`validate_sandbox_probe_inventory.py`](../tools/validate_sandbox_probe_inventory.py).

Method:

Added a checked no-claim sandbox probe-package schema and template, then extended sandbox probe validation to require role targets, required access surfaces, platform-specific policy artifacts, package lifecycle stages, result-record fields, rejection rules, unsupported boundaries, validation commands, `PB-012` evidence, and `TASK-000004` scope.

Decision:

Keep `PB-012` partial. The template defines what a future expected-deny package must record, but it does not provide a packaged harness, effective policy capture, platform matrix execution, owner review, sandbox-readiness claim, renderer-security claim, site-isolation proof, hostile-browsing safety claim, `SEC-GATE-1`, `SEC-GATE-6`, or production-safety evidence.

Impact:

Future `TASK-000004` work now starts from a checked package handoff object and must replace template-only fields with real host-safe execution evidence. The current repository still needs packaged expected-deny probes beyond the checked no-claim template before any sandbox or security-gate claim.

Next question:

Which host-safe renderer or network expected-deny probe should be packaged first without touching real profiles, real credentials, production signing keys, or developer-host state outside bounded fixtures?

## 2026-07-18 — IPC schema-source template

Question:

Can `PB-011` gain a checked schema-source handoff object before any schema generator, generated type, or wire encoding is approved?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [System Architecture](blueprint-v1/04-system-architecture.md);
- [Security, Privacy, and Sandbox Model](blueprint-v1/08-security-and-sandbox.md);
- [Schemas, Errors, Versioning, and Compatibility](api-design/03-schemas-errors-versioning-and-compatibility.md);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- [`ipc-schema-source.schema.json`](blueprint-v1/machine/ipc-schema-source.schema.json);
- [`no-claim-control-envelope-template.json`](blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json);
- [`validate_ipc_capability_boundaries.py`](../tools/validate_ipc_capability_boundaries.py).

Method:

Added a checked no-claim IPC schema-source template and extended IPC validation to cover required message metadata, process-capability role links, generator output plans, negative fixture plans for malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases, review gates, unsupported boundaries, and validation commands.

Decision:

Keep `PB-011` partial. The template defines the shape a future generator proposal must satisfy, but it does not approve a generator source, wire encoding, generated type, generated validator, generated fixture, timeout/cancellation implementation, renderer-security claim, agent-security claim, process-isolation claim, site-isolation claim, production IPC claim, or broad implementation readiness.

Impact:

Future `TASK-000003` work now has a checked starting object linked to `process-capabilities.json`, the IPC boundary inventory, and the architecture/security/API docs. The current repository still needs implemented schema-generator evidence beyond the checked no-claim schema-source template before any IPC readiness claim.

Next question:

Which contained IPC generator experiment should produce the first generated fixtures and negative tests without expanding authority?

## 2026-07-18 — Benchmark claim-bundle template

Question:

Can `PB-013` public performance and Chrome-class claim governance gain a checked claim-bundle shape without approving any claim?

Inputs:

- [Chrome-Class Performance Runbook](research/chrome-class-performance-runbook-2026-07.md);
- [`benchmark-claim-bundle.schema.json`](blueprint-v1/machine/benchmark-claim-bundle.schema.json);
- [`no-claim-public-claim-template.json`](blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json);
- [`validate_benchmark_claim_bundles.py`](../tools/validate_benchmark_claim_bundles.py);
- `PB-013`, `TASK-000005`, and the research-readiness crosswalk.

Method:

Added a checked no-claim claim-bundle schema, template, focused validator, and aggregate validator hook covering benchmark registry references, required evidence inputs, statistical controls, workload equivalence, denominator accounting, overhead disclosure, expiry, publication controls, rejection rules, unsupported behavior, missing proof, and validation commands.

Decision:

Keep `PB-013` at `documented_no_runner`. The template proves only the future public-claim evidence shape; it does not approve a benchmark run, result, competitor comparison, trace, raw sample, memory result, energy result, Chrome-class claim, faster claim, lower-memory claim, lower-energy claim, compatibility claim, security claim, accessibility claim, production claim, or daily-driver claim.

Impact:

Future public claims now have a checked handoff object tied to existing benchmark registries and task gating. The current repository still needs owner-reviewed claim bundles from real raw artifacts before any public performance language is supportable.

Next question:

Which benchmark evidence lane should produce the first owner-reviewed artifact bundle and claim-bundle draft from real runs?

## 2026-07-18 — Task approval template control

Question:

Can proposed `TASK-*` rows gain a checked approval-manifest shape before any task is actually approved or executed?

Inputs:

- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Agent Execution](agent-execution/README.md);
- [`execution-task.schema.json`](agent-execution/machine/execution-task.schema.json);
- [`agent-run-manifest.schema.json`](agent-execution/machine/agent-run-manifest.schema.json);
- [`evidence-bundle.schema.json`](agent-execution/machine/evidence-bundle.schema.json);
- [`task-approval-template.schema.json`](agent-execution/machine/task-approval-template.schema.json);
- [`no-claim-task-approval-template.json`](agent-execution/machine/task-approval-templates/no-claim-task-approval-template.json);
- [`validate_task_approval_templates.py`](../tools/validate_task_approval_templates.py).

Method:

Added a checked no-claim approval template and dependency-free validator covering proposed task coverage, owner and independent reviewer inputs, immutable manifest requirements, allowed/prohibited authority, credential and network limits, evidence bundle requirements, rollback, expiry, rejection rules, and unsupported readiness/product boundaries.

Decision:

Keep every queued task proposed. The template defines what an owner must fill before execution; it does not approve a task, start a run, accept evidence, promote readiness, authorize release work, or support Chrome-class, performance, compatibility, security, accessibility, beta, stable, production, release, or daily-driver claims.

Impact:

The handoff from planning evidence to owner-reviewed execution evidence is now checkable. Future `TASK-000001` or `TASK-000002` work can be prepared against a concrete approval-manifest shape instead of relying on prose alone.

Next question:

Which proposed task should receive the first owner-filled approval manifest and independent review?

## 2026-07-18 — Documentation-readiness validator command coverage

Question:

Can the documentation-readiness evidence matrix stay aligned with the growing focused validator family as no-claim machine-readable evidence lanes are added?

Inputs:

- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [`documentation-readiness-completion-audit.json`](project-buildout/machine/documentation-readiness-completion-audit.json);
- [`validate_blueprint.py`](../tools/validate_blueprint.py);
- current `tools/validate_*.py` focused validators.

Method:

Expanded the direct validation-command list to name every current focused `tools/validate_*.py` command before diff and Cargo checks, and added aggregate validation coverage that fails when a focused validator exists without a corresponding documentation-readiness command.

Decision:

Keep documentation readiness scoped to contained M0 only. This change improves handoff fidelity and drift detection; it does not make the documentation complete for broad building, approve tasks, promote any `PB-*` item, or support Chrome-class, performance, compatibility, security, accessibility, production, beta, stable, release, or daily-driver claims.

Impact:

Maintainers debugging documentation-readiness evidence can now follow the matrix without skipping newer focused validators such as fresh-host run records, Servo local-compatibility HTTPS harnesses, benchmark registries, UI adapter contracts, IPC boundaries, or sandbox probes.

Next question:

Which remaining blocker lane should produce owner-reviewed execution evidence first instead of only checked no-claim planning evidence?

## 2026-07-18 — PB-009 fresh-host run-record template

Question:

Can `PB-009` define a checked machine-readable run record before an independent fresh-host run exists, without promoting current-host diagnostics to build confidence?

Inputs:

- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json);
- [`fresh-host-run-record.schema.json`](project-buildout/machine/fresh-host-run-record.schema.json);
- [`no-claim-run-record-template.json`](project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json);
- [`validate_fresh_host_reproduction.py`](../tools/validate_fresh_host_reproduction.py);
- [`validate_fresh_host_run_records.py`](../tools/validate_fresh_host_run_records.py);
- `PB-009`, `TASK-000002`, the research crosswalk, and the pre-build readiness registry.

Method:

Added a checked no-claim run-record schema, a `template_no_execution` record, and a dependency-free validator covering independent host identity, checkout facts, wrapper and direct `xtask` command records, retained-output hashes, cache and target-directory controls, source-tree cleanliness, failure denominator, prohibited evidence, and unsupported readiness boundaries.

Decision:

Keep `PB-009` partial. The run-record template proves only the future evidence shape. It explicitly records no independent fresh-host reproduction, no owner-approved clean-VM equivalent, no command execution evidence, no retained bootstrap/doctor/check/xtask logs, no readiness promotion, and no preview, beta, stable, production, release-confidence, or Chrome-class claim.

Impact:

Future `TASK-000002` work now has a checked target record for retained logs and failure accounting. The next proof remains an actual independent fresh-host or owner-approved clean-VM run with owner review.

Next question:

Which owner-approved reference host or clean VM should fill the checked run record with real bootstrap, doctor, check, and `xtask` evidence?

## 2026-07-18 — ADR-0009 HTTPS host-alias harness plan

Question:

Can the checked `ADR9-EV-013` local compatibility corpus gain a validated HTTPS host-alias execution plan without becoming browser-run compatibility evidence?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`servo-local-compatibility-https-harness.schema.json`](blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json);
- [`no-claim-https-host-alias.plan.json`](blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json);
- [`validate_servo_local_compatibility_https_harness.py`](../tools/validate_servo_local_compatibility_https_harness.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, research crosswalk, and pre-build readiness registry.

Method:

Added a dependency-free validator and checked no-claim harness plan that binds every corpus origin to future SNI/SAN coverage, isolated trust-store handling, transient host-to-loopback aliasing, cleanup proof, browser-visible-origin evidence, per-origin route records, raw logs, certificate fingerprints, and failure-denominator accounting.

Decision:

Keep `PB-002` blocked and `ADR9-EV-013` partial. The harness plan proves only the future HTTPS/browser execution contract. It explicitly records no HTTPS server, no certificate or private key, no trust-store mutation, no host alias, no browser launch, no Servo run, no WPT result, no Test262 result, no Turing compatibility claim, no Chrome-class claim, and no release-code authorization.

Impact:

The remaining `ADR9-EV-013` work is now execution of the checked HTTPS host-alias harness, raw Servo run evidence, focused WPT subset runs, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan.

Next question:

Should the next `ADR9-EV-013` step execute the checked HTTPS host-alias harness against the external Servo build, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — ADR-0009 local compatibility route self-test

Question:

Can the checked `ADR9-EV-013` local fixture set be served and verified through repository-owned route plumbing before any HTTPS, browser, WPT, or Test262 run exists?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- `benchmarks/compatibility/adr0009/no-claim-tiny/`;
- [`serve_servo_local_compatibility_corpus.py`](../tools/serve_servo_local_compatibility_corpus.py);
- [`validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, and the pre-build readiness registry.

Method:

Added a dependency-free HTTP/1.1 loopback route self-test that validates the manifest, starts a temporary server, uses Host headers for the declared `turing.invalid` origins, serves every generated fixture route, verifies status, content type, byte count, SHA-256, no-store cache behavior, shutdown, and closed-port behavior, and emits `ADR9.EV013.NOCLAIM_ROUTE_SELF_TEST.2026_07`.

Decision:

Keep `PB-002` blocked and `ADR9-EV-013` partial. The route self-test proves only local route plumbing for generated fixtures. It explicitly records no HTTPS, no DNS modification, no browser launch, no WPT result, no Test262 result, no Servo adoption, no Turing compatibility claim, no Chrome-class claim, and no release-code authorization.

Impact:

The remaining `ADR9-EV-013` work is now HTTPS harness and host-alias browser execution for the checked fixtures, raw Servo run evidence, focused WPT subset runs, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan.

Next question:

Should the next `ADR9-EV-013` step add local HTTPS and browser execution, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — ADR-0009 local compatibility fixtures

Question:

Can the checked `ADR9-EV-013` tiny local compatibility corpus manifest point at generated local fixtures without becoming browser-run compatibility evidence?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- `benchmarks/compatibility/adr0009/no-claim-tiny/`;
- [`tools/validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, and the pre-build readiness registry.

Method:

Added generated local HTML fixtures for the eight checked case categories, recorded each fixture path, route, origin, byte count, hash, and license in the manifest, and extended the validator to verify file existence, SHA-256, byte counts, LF line endings, local-only `turing.invalid` URLs, and per-origin fixture coverage.

Decision:

Keep `PB-002` blocked and `ADR9-EV-013` partial. The fixtures are no-claim local assets for a future harness; they are not browser-run evidence, WPT/Test262 evidence, Servo approval, Turing compatibility evidence, or Chrome-class evidence.

Impact:

The remaining `ADR9-EV-013` work is now executing the checked HTTPS host-alias harness for the checked fixtures, raw Servo run evidence, focused WPT subset runs, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan.

Next question:

Should the next `ADR9-EV-013` step build the local HTTPS harness and run the checked fixtures, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — ADR-0009 local compatibility corpus contract

Question:

Can the `ADR9-EV-013` tiny local compatibility corpus become a checked no-claim manifest before any Servo, Turing, WPT, or Test262 compatibility result exists?

Inputs:

- [Servo Local Compatibility Corpus and WPT/Test262 Evidence](research/servo-local-compatibility-corpus-2026-07.md);
- [`servo-local-compatibility-corpus.schema.json`](blueprint-v1/machine/servo-local-compatibility-corpus.schema.json);
- [`no-claim-tiny-adr0009.corpus.json`](blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- [`tools/validate_servo_local_compatibility_corpus.py`](../tools/validate_servo_local_compatibility_corpus.py);
- `ADR9-EV-013`, `PB-002`, the ADR-0009 evidence matrix, and the pre-build readiness registry.

Method:

Added a dependency-free validator and checked manifest covering eight local-only compatibility case categories, required assertion groups, required artifacts, `turing.invalid` origins, WPT focus areas, Test262 attribution language, failure denominators, and no-claim boundaries.

Decision:

Keep `PB-002` and `ADR9-EV-013` partial. The manifest is a contract for future routes, fixtures, and runs; it is not browser-run evidence, a WPT/Test262 result, a Servo adoption decision, or a compatibility claim.

Impact:

The source-strategy handoff gained a stable local compatibility corpus contract. The later fixture-materialization log entry supersedes the manifest-only next step.

Next question:

Should the next `ADR9-EV-013` step build the local HTTPS harness and run the checked fixtures, or should source-strategy work return to owner-selected baseline and build-replay prerequisites?

## 2026-07-18 — Servo unsafe and FFI contract review

Question:

What unsafe-code and C ABI contract evidence is needed before any Servo-derived component boundary can be proposed for `ADR-0009`?

Inputs:

- [Servo Unsafe and FFI Contract Review](research/servo-unsafe-ffi-contract-review-2026-07.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- the clean external Servo checkout at `C:\ts\servo` and prior generated/native/unsafe/FFI classification evidence.

Method:

Added a dedicated `ADR9-EV-009` and `ADR9-EV-010` triage report that counts unsafe and FFI surfaces, identifies C API contract families, and separates JavaScript rooting/tracing and WebGL/driver boundary review classes from release approval.

Decision:

Keep `PB-002` blocked. The report narrows the unsafe/FFI review plan but does not approve Servo, unsafe code, the C API, SpiderMonkey integration, WebGL integration, a component boundary, source adoption, dependency adoption, or release code.

Impact:

The source-strategy evidence registry, matrix, readiness records, and indexes now distinguish unsafe/FFI contract triage from the still-missing block-level unsafe ledger, ABI policy, conformance tests, owner review, and ADR decision.

Next question:

Which `ADR-0009` candidate boundary should get the first block-level unsafe ledger and versioned ABI contract review?

## 2026-07-18 — Documentation readiness completion audit

Question:

Can the documentation-preparation work be audited as organized enough for contained M0 continuation without claiming that all information is ready for broad browser construction, Chrome-class competition, production, release, or performance/security/compatibility/accessibility claims?

Inputs:

- [Documentation Readiness Completion Audit](research/documentation-readiness-completion-audit-2026-07.md);
- [`documentation-readiness-completion-audit.json`](project-buildout/machine/documentation-readiness-completion-audit.json);
- [`documentation-readiness-completion-audit.schema.json`](project-buildout/machine/documentation-readiness-completion-audit.schema.json);
- [`tools/validate_documentation_readiness_completion_audit.py`](../tools/validate_documentation_readiness_completion_audit.py);
- first-entry docs, pre-build readiness, kickoff inventory, dependency graph, task queue, research crosswalk, evidence matrix, Definition of Done, and validation records.

Method:

Added a checked no-claim audit and focused validator covering entrypoints, stop/resume continuity, machine registries, research lanes, task handoff, sequencing, claim boundaries, validation, owner-only decisions, and remaining full-goal blockers.

Decision:

Keep `PB-020` partial. The audit supports contained M0 continuation only and explicitly rejects all-information-ready-for-building, broad M1, Chrome-class, production, release, performance, compatibility, security, accessibility, and daily-driver claims.

Impact:

The audit makes premature completion language machine-detectable. It does not approve tasks, close blockers, or promote readiness.

Next question:

Which owner-reviewed execution proof should follow first: `TASK-000001` source-strategy closure or `TASK-000002` fresh-host reproduction?

## 2026-07-18 — Build readiness dependency graph

Question:

Can the current build-readiness task order and cross-lane sequencing become a checked dependency graph without approving proposed tasks or promoting readiness?

Inputs:

- [Build Readiness Dependency Graph Inventory](research/build-readiness-dependency-graph-inventory-2026-07.md);
- [`build-readiness-dependency-graph.json`](project-buildout/machine/build-readiness-dependency-graph.json);
- [`build-readiness-dependency-graph.schema.json`](project-buildout/machine/build-readiness-dependency-graph.schema.json);
- [`tools/validate_build_readiness_dependency_graph.py`](../tools/validate_build_readiness_dependency_graph.py);
- pre-build readiness, build-readiness task queue, implementation kickoff inventory, operating board, evidence matrix, research crosswalk, agent-execution, production-readiness, and Definition of Done records.

Method:

Added a checked no-claim graph and focused validator covering unresolved readiness items, proposed task nodes, task dependencies from the task queue, readiness-to-task edges, `ADR-0009`, `ADR-0013`, `ADR-0014`, `ADR-0016`, `UI-GATE-7`, `PB-020` dependency edges, and parallel no-claim lanes.

Decision:

Keep `PB-020` partial. The graph makes sequencing drift visible and machine-checkable, but it does not approve task execution, change dependencies, close blockers, or promote readiness.

Impact:

No task approval, readiness promotion, broad M1 implementation, developer preview, beta, stable, production, Chrome-class, performance, compatibility, security, accessibility, release-readiness, or daily-driver claim is supported.

Next question:

Which graph edge should become owner-reviewed execution evidence first, `TASK-000001` source-strategy closure or `TASK-000002` fresh-host reproduction?

## 2026-07-18 — Implementation kickoff review inventory

Question:

Can `PB-020` become a checked stop/resume inventory for unresolved pre-build lanes without promoting broad implementation readiness or approving tasks?

Inputs:

- [Implementation Kickoff Review Inventory](research/implementation-kickoff-review-inventory-2026-07.md);
- [`implementation-kickoff-review.json`](project-buildout/machine/implementation-kickoff-review.json);
- [`implementation-kickoff-review.schema.json`](project-buildout/machine/implementation-kickoff-review.schema.json);
- [`tools/validate_implementation_kickoff_review.py`](../tools/validate_implementation_kickoff_review.py);
- pre-build checklist, operating board, task queue, evidence matrix, research crosswalk, agent-execution, production-readiness, and Definition of Done records.

Method:

Added a checked no-claim project-buildout registry and validator covering unresolved `PB-002`, `PB-003`, `PB-004`, `PB-005`, `PB-009`, `PB-011`, `PB-012`, `PB-013`, `PB-014`, `PB-015`, `PB-016`, `PB-017`, `PB-018`, and `PB-019` status, current evidence, first next actions, required pre-M1 evidence, owner-only decisions, prohibited claims, kickoff gates, and release-authority boundaries. The aggregate blueprint validator now requires the report, schema, registry, focused validator, and `PB-020` evidence.

Decision:

Keep `PB-020` partial. The inventory improves handoff continuity and drift detection, but it does not close remaining P0 items, approve proposed tasks, authorize M1 expansion, or promote readiness.

Impact:

No broad implementation, developer preview, beta, stable, production, Chrome-class, performance, memory, energy, compatibility, security, accessibility, daily-driver, release-readiness, task-approval, or readiness-promotion claim is supported.

Next question:

Which owner-reviewed lane should close first: `PB-002` source strategy or `PB-009` fresh-host reproduction?

## 2026-07-18 — Toolkit-neutral UI adapter contract inventory

Question:

Can `PB-003` move from a buildable M0 UI model and prose architecture into checked adapter-contract planning evidence without implying `ADR-0013`, native adapter implementation, toolkit selection, trusted-chrome readiness, accessibility readiness, page-surface approval, or release-path UI approval?

Inputs:

- [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- [`adapter-contract-inventory.json`](ui-runtime/machine/adapter-contract-inventory.json);
- [`adapter-contract-inventory.schema.json`](ui-runtime/machine/adapter-contract-inventory.schema.json);
- [`tools/validate_ui_adapter_contract.py`](../tools/validate_ui_adapter_contract.py);
- `crates/turing-ui-model`, Native UI Runtime, readiness, task-queue, crosswalk, component, page-surface, and accessibility records.

Method:

Added a checked no-claim UI-runtime registry and validator covering state, command, surface, accessibility, diagnostic, and adapter contract areas; current M0 model invariants; denied toolkit-owned navigation, profile, permission, credential, agent, Plug-in, persistence, and update authority; required `ADR-0013`, contract, adapter prototype, negative-test, and owner-review evidence; and unsupported readiness boundaries.

Decision:

Keep `PB-003` partial. The inventory makes missing adapter-contract proof reviewable; it does not provide accepted `ADR-0013`, complete contracts, a native adapter prototype, no-toolkit-owned-authority negative tests, owner review, or release-path UI approval.

Impact:

No native-shell readiness, trusted-chrome readiness, accessibility readiness, page-surface approval, toolkit selection, release-path UI approval, production, beta, stable, Chrome-class, or implementation claim is supported.

Next question:

Which `ADR-0013` draft and first native adapter trait prototype should `TASK-000006` propose so toolkit callbacks can be proven command-only before framework bake-off work expands?

## 2026-07-18 — Fresh host reproduction inventory

Question:

Can `PB-009` move from a generic "independent fresh-host reproduction" blocker into checked no-claim planning evidence without implying that an independent clean-host run has already happened?

Inputs:

- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [`fresh-host-reproduction.json`](project-buildout/machine/fresh-host-reproduction.json);
- [`fresh-host-reproduction.schema.json`](project-buildout/machine/fresh-host-reproduction.schema.json);
- [`tools/validate_fresh_host_reproduction.py`](../tools/validate_fresh_host_reproduction.py);
- [M0 build foundation](research/m0-build-foundation-2026-07.md);
- Build readiness board, task queue, pre-build readiness registry, research crosswalk, and `xtask` records.

Method:

Added a checked no-claim fresh-host registry and validator covering clean host facts, source checkout identity, bootstrap/doctor/check/xtask logs, cache and target-directory behavior, source-tree cleanliness, failure classification, rollback notes, and rejection rules for same-host reruns or reused build outputs. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-009` evidence, and `TASK-000002` scope.

Decision:

Keep `PB-009` partial. The inventory makes missing clean-host proof reviewable; it does not provide an independent fresh-host run, owner-approved clean-VM equivalent, retained clean-host logs, cache proof, source-tree proof, or owner review.

Impact:

No `PB-009` readiness promotion, broad M1 readiness, preview readiness, beta readiness, stable readiness, production readiness, release confidence, Chrome-class claim, source-strategy approval, or benchmark claim is supported.

Next question:

Which owner-approved host or clean-VM environment should execute `TASK-000002` so clean-host reproduction evidence can become actual proof rather than planning inventory?

## 2026-07-18 — Native UI framework bake-off inventory

Question:

Can `PB-004` move from qualitative native UI framework evaluation into checked no-claim planning evidence without implying toolkit selection, `ADR-0014`, accessibility readiness, page-surface approval, license/provenance approval, trusted-chrome readiness, or release-path UI approval?

Inputs:

- [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md);
- [`framework-bakeoff-inventory.json`](ui-runtime/machine/framework-bakeoff-inventory.json);
- [`framework-bakeoff-inventory.schema.json`](ui-runtime/machine/framework-bakeoff-inventory.schema.json);
- [`tools/validate_framework_bakeoff.py`](../tools/validate_framework_bakeoff.py);
- [Native UI framework evaluation](research/native-ui-framework-evaluation-2026-07.md);
- Native UI Runtime, Blueprint, readiness, task-queue, crosswalk, security, and research-program records.

Method:

Added a checked no-claim framework bake-off registry and validator covering nine candidate summaries, six external source observations, equivalent Slint/Vizia/Floem-or-GPUI adapter scope, evidence axes, disqualifiers, and unsupported claim boundaries. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-004` evidence, and `TASK-000006` scope.

Decision:

Keep `PB-004` partial. The inventory makes missing framework-selection proof reviewable; it does not provide equivalent adapter runs, raw artifacts, legal/provenance review, accessibility evidence, page-surface evidence, package/runtime-exclusion proof, owner review, or `ADR-0014`.

Impact:

No UI toolkit selection, Slint approval, accessibility readiness, IME/keyboard proof, page-surface approval, trusted-chrome readiness, performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or release-path UI claim is supported.

Next question:

Which first reference-shell adapter execution manifest should `TASK-000006` propose so the bake-off can become executable without selecting the production toolkit?

## 2026-07-18 — Page surface composition inventory

Question:

Can `PB-005` move from page-surface/compositor architecture prose into checked no-claim planning evidence without implying `UI-GATE-7`, compositor ownership, typed handle implementation, renderer-texture composition, toolkit selection, or release-path UI approval?

Inputs:

- [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md);
- [`page-surface-composition.json`](ui-runtime/machine/page-surface-composition.json);
- [`page-surface-composition.schema.json`](ui-runtime/machine/page-surface-composition.schema.json);
- [`tools/validate_page_surface_composition.py`](../tools/validate_page_surface_composition.py);
- Native UI Runtime, paint/compositor/GPU, Blueprint, readiness, task-queue, and crosswalk records.

Method:

Added a checked no-claim page-surface registry and validator covering 14 surface contract fields, four composition alternatives, 11 workflow tests, nine failure cases, eight security identity boundaries, evidence blockers, source-record linkage, and unsupported claim boundaries. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-005` evidence, and `TASK-000006` scope.

Decision:

Keep `PB-005` partial. The inventory makes missing page-surface proof reviewable; it does not provide executable `UI-GATE-7` prototype evidence, typed page-surface handles, brokered surface handles, renderer-produced page textures, software fallback, stale-handle negative tests, latency/frame-pacing traces, `ADR-0016`, compositor ownership, or owner review.

Impact:

No page-surface approval, UI toolkit selection, trusted-chrome readiness, accessibility readiness, performance, memory, energy, Chrome-class, compatibility, security, production, beta, stable, or release-path UI claim is supported.

Next question:

Which isolated reference-shell adapter and simulated renderer frame source should `TASK-000006` propose first so `UI-GATE-7` can become executable without selecting the production toolkit?

## 2026-07-18 — Window input accessibility spike inventory

Question:

Can `PB-015` move from native-shell accessibility prose into checked no-claim workflow evidence without implying accessibility readiness, screen-reader coverage, page-tree proof, IME correctness, crash/GPU-loss behavior, UI toolkit selection, or release-path UI approval?

Inputs:

- [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md);
- [`window-input-accessibility-spike.json`](accessibility/machine/window-input-accessibility-spike.json);
- [`window-input-accessibility-spike.schema.json`](accessibility/machine/window-input-accessibility-spike.schema.json);
- [`tools/validate_window_input_accessibility_spike.py`](../tools/validate_window_input_accessibility_spike.py);
- [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- Blueprint, accessibility, platform, UI-runtime, readiness, task-queue, and crosswalk records.

Method:

Added a checked no-claim accessibility registry and validator covering windowing, input, IME, accessibility-tree, page-tree composition, clipboard, drag-drop, localization, zoom, high contrast, forced colors, reduced motion, crash recovery, renderer hang, GPU-loss, nine core shell workflows, platform assistive-technology rows for VoiceOver, Narrator, NVDA, and Orca, and explicit evidence blockers. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-015` evidence, and `TASK-000006` allowed paths.

Decision:

Keep `PB-015` partial. The inventory makes the workflow matrix and missing proof reviewable; it does not provide executable reference-platform runs, manual assistive-technology transcripts, platform accessibility snapshots, composed chrome/page-tree diffs, IME/clipboard/drag-drop fixtures, renderer-hang/crash/GPU-loss fault evidence, latency/resource traces, or owner review.

Impact:

No accessibility-readiness, screen-reader, manual assistive-technology, page-tree, IME, keyboard, clipboard/drag-drop, localization, zoom/contrast/motion, crash-recovery, renderer-hang, GPU-loss, `UI-GATE-7`, `UI-GATE-10`, release-path UI, toolkit-selection, production, beta, stable, or Chrome-class claim is supported.

Next question:

Which reference-platform workflow runner and manual assistive-technology transcript format should `TASK-000006` propose first so PB-015 evidence can become executable without selecting a toolkit?

## 2026-07-18 — Sandbox probe inventory

Question:

Can `PB-012` move from general sandbox requirements into checked no-claim planning evidence without implying sandbox readiness, renderer security, site isolation, hostile-browsing safety, platform containment, SEC-GATE evidence, or production safety?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [`sandbox-probe-inventory.json`](security-engine/machine/sandbox-probe-inventory.json);
- [`sandbox-probe-inventory.schema.json`](security-engine/machine/sandbox-probe-inventory.schema.json);
- [`tools/validate_sandbox_probe_inventory.py`](../tools/validate_sandbox_probe_inventory.py);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- security, sandbox, platform, testing, and research-program chapters.

Method:

Added a checked no-claim security-engine registry and validator covering renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater probe targets across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC surfaces. The inventory also records macOS, Windows, and Linux evidence requirements, harness blockers, host-safety requirements, and unsupported claim boundaries. The aggregate blueprint validator now requires the report, registry, schema, focused validator, `PB-012` evidence, and `TASK-000004` allowed paths.

Decision:

Keep `PB-012` partial. The inventory makes the target matrix and missing proof reviewable; it does not provide packaged role runners, effective platform-policy capture, broker fixtures, compromised-client harnesses, platform-matrix execution, or owner review.

Impact:

No sandbox-readiness, renderer-security, site-isolation, hostile-browsing safety, platform-containment, SEC-GATE-1, SEC-GATE-6, production-safety, broad M1 readiness, beta, stable, or implementation-readiness claim is supported.

Next question:

Which host-safe packaged probe runner should `TASK-000004` propose first so expected-deny results can be collected without damaging developer machines or weakening sandbox policy?

## 2026-07-18 — IPC capability boundary inventory

Question:

Can `PB-011` move from crate evidence and process-capability prose into checked no-claim boundary evidence without implying a canonical schema generator, wire encoding decision, renderer-security claim, agent-security claim, process-isolation readiness, site-isolation, timeout/cancellation implementation, or production IPC readiness?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [`ipc-capability-boundary.json`](blueprint-v1/machine/ipc-capability-boundary.json);
- [`ipc-capability-boundary.schema.json`](blueprint-v1/machine/ipc-capability-boundary.schema.json);
- [`tools/validate_ipc_capability_boundaries.py`](../tools/validate_ipc_capability_boundaries.py);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- `crates/turing-ipc`, `crates/turing-kernel`, and `crates/turing-types`.

Method:

Added a checked no-claim architecture/API registry and validator covering the current M0 bounded `ControlEnvelope`, oversized-message unit test, typed identities, role-capability model, process-capability role records, schema/transport blockers, negative coverage requirements, and unsupported authority boundaries. The aggregate blueprint validator now requires the registry, report, and focused validator while keeping `PB-011` partial and `TASK-000003` proposed.

Decision:

Keep `PB-011` partial. The inventory makes current evidence and missing proof reviewable; it does not approve generated schemas, choose a wire format, prove connection authentication, implement queues/backpressure, prove stale-epoch rejection, implement timeout/cancellation behavior, or cover malformed, duplicate, reordered, unauthorized, and wrong-principal negative cases beyond the listed M0 oversized-message test.

Impact:

No renderer-security, agent-security, process-isolation, site-isolation, production IPC, schema-generator, wire-encoding, timeout/cancellation, broad M1 readiness, beta, stable, production, or implementation-readiness claim is supported.

Next question:

Which canonical IPC schema source and wire-encoding decision should `TASK-000003` propose before generated negative fixtures and receiver-side authority checks become executable?

## 2026-07-18 — Backup ownership gap inventory

Question:

Can `PB-019` move from ownership prose into checked blocked evidence without implying that named qualified backups, two-person control, release authority, signing authority, security-disclosure authority, incident-closure authority, legal approval, production authority, or owner coverage exists?

Inputs:

- [Backup Ownership Gap Inventory](research/backup-ownership-gap-inventory-2026-07.md);
- [`backup-ownership-gap.json`](project-buildout/machine/backup-ownership-gap.json);
- [`backup-ownership-gap.schema.json`](project-buildout/machine/backup-ownership-gap.schema.json);
- [`tools/validate_backup_ownership_gap.py`](../tools/validate_backup_ownership_gap.py);
- [`professional-owners.json`](blueprint-v1/machine/professional-owners.json);
- root [CODEOWNERS](../.github/CODEOWNERS).

Method:

Added a checked blocked project-buildout registry and validator covering build-critical program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data scopes. The validator checks provisional primary-only owner records, null backups, CODEOWNERS routing, review-rule linkage, `PB-019` blocked status, `TASK-000008` proposed-only status, required qualification and reconciliation evidence, and unsupported authority boundaries.

Decision:

Keep `PB-019` blocked. The inventory is useful because it makes the blocker reviewable and machine-checkable, not because it satisfies the blocker. `PB-019` can move only after named qualified backups, role-level evidence, subsystem competence, representative path coverage, review records, availability, succession, recusal, inactivity, removal, emergency replacement, access reconciliation, stale-access review, ownerless-path review, primary-only-path review, single-owner residual-risk review, and two-person-control evidence exist.

Impact:

No qualified backup, owner coverage, release authority, signing authority, update trust, supported-version change authority, security-disclosure authority, irreversible migration approval, legal approval, incident closure, broad M1 readiness, beta, stable, production, or implementation claim is supported.

Next question:

Which named backup-owner candidates and qualification records should be collected first without using placeholders or granting release authority from documentation intent?

## 2026-07-18 — Incident patch rehearsal inventory

Question:

Can `PB-018` move from security and release prose into checked no-claim planning evidence without implying that incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, stable promotion authority, signing authority, incident closure authority, or production-safe browsing exists?

Inputs:

- [Incident Patch Rehearsal Inventory](research/incident-patch-rehearsal-inventory-2026-07.md);
- [`incident-patch-rehearsal.json`](security-engine/machine/incident-patch-rehearsal.json);
- [`incident-patch-rehearsal.schema.json`](security-engine/machine/incident-patch-rehearsal.schema.json);
- [`tools/validate_incident_patch_rehearsal.py`](../tools/validate_incident_patch_rehearsal.py);
- [Security policy](security.md);
- [Security Verification and Release Gates](security-engine/06-security-verification-and-release-gates.md);
- [Vulnerability Response and Supported Lifecycle](release-operations/08-vulnerability-response-and-supported-lifecycle.md).

Method:

Added a no-claim security-engine registry and validator covering report access control, acknowledgement, reproduction, severity, asset analysis, affected-version statement, embargo handling, sanitized evidence preservation, protected patch branch, embargoed CI, regression, backport, signing/update dry run, staged rollout, minimum secure version, revocation, release notes, user/admin communication, CVE/credit handling, coordinated disclosure, postmortem remediation, active exploitation, update/signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension/provider, service outage, owner/reviewer/release/security/legal/support/on-call roles, timing targets, escalation path, secret rotation, backup coverage, and unavailable agent, disclosure, signing, stable-promotion, and incident-closure authority.

Decision:

Treat `PB-018` as `partial` because checked planning evidence exists, while requiring executed private-intake tabletop records, emergency patch dry-run records, regression/backport evidence, signing/update dry-run evidence, staged rollout and revocation evidence, coordinated disclosure rehearsal, postmortem evidence, incident-class workflow exercises, role review, timing/escalation/secret-rotation drills, backup-owner coverage, and owner approval before any incident-response, emergency-patch, supported-security, disclosure, signing, stable-promotion, incident-closure, or production-safe browsing claim.

Impact:

No incident-response program, emergency patch capacity, supported security version, disclosure authority, signing authority, stable-promotion authority, incident-closure authority, production-safe browsing, broad M1 readiness, beta, stable, or production claim is supported.

Next question:

Which private tabletop and no-production-key patch dry-run should make the `PB-018` planning inventory executable without publishing exploitable details or granting agents security authority?

## 2026-07-18 — Research package update lab inventory

Question:

Can `PB-017` move from release-operations prose into checked no-claim planning evidence without implying that production signing keys, offline roots, a stable channel, a real updater, public binary distribution, rollback safety, migration safety, release readiness, or supported-security evidence exists?

Inputs:

- [Research Package Update Lab Inventory](research/research-package-update-lab-inventory-2026-07.md);
- [`research-package-update-lab.json`](release-operations/machine/research-package-update-lab.json);
- [`research-package-update-lab.schema.json`](release-operations/machine/research-package-update-lab.schema.json);
- [`tools/validate_research_package_update_lab.py`](../tools/validate_research_package_update_lab.py);
- [Release Operations book](release-operations/README.md);
- [Update, Supply Chain, and Vulnerability Response](security-engine/05-update-supply-chain-and-vulnerability-response.md);
- [Blueprint 13](blueprint-v1/13-build-release-operations.md).

Method:

Added a no-claim release-operations registry and validator covering source commit, build ID, channel, platform, architecture, toolchain, feature set, SBOM, provenance, symbols, notices, artifact hashes, artifact sizes, no-stable-support label, role separation, signature threshold, expiry, minimum secure version, rollout, mirrors, staged install, tamper, replay, wrong-target, partial-write, disk-full, power-loss, rollback, vulnerable-version refusal, migration, downgrade, crash-loop, privacy-preserving local events, and unsupported production boundaries.

Decision:

Treat `PB-017` as `partial` because checked planning evidence exists, while requiring executable package manifests, update metadata parsers, no-production-key signature and threshold fixtures, tamper/replay/wrong-target/expiry/mirror/partial-write/disk-full/power-loss tests, authorized rollback tests, vulnerable-version refusal tests, migration/downgrade/crash-loop tests, privacy review, release-operations review, and owner approval before any updater, signing, release, rollback, migration, or supported-security claim.

Impact:

No package implementation, updater implementation, production signing, offline-root handling, stable channel, public binary distribution, real user profile migration, rollback safety, migration safety, release readiness, supported-security readiness, broad M1 readiness, or production claim is supported.

Next question:

Which no-production-key manifest generator and metadata parser should make the `PB-017` planning inventory executable without creating a real updater or public distribution path?

## 2026-07-18 — Profile/session format inventory

Question:

Can `PB-016` move from prose-only schema expectations into checked no-claim planning evidence without implying that profile formats, migration, sync, credential storage, data-loss safety, or production user-data handling exist?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [`profile-session-format-inventory.json`](storage/machine/profile-session-format-inventory.json);
- [`profile-session-format-inventory.schema.json`](storage/machine/profile-session-format-inventory.schema.json);
- [`tools/validate_profile_session_formats.py`](../tools/validate_profile_session_formats.py);
- [Storage and Recovery book](storage/README.md);
- [Product Experience book](product-experience/README.md);
- [Build and Release Operations book](release-operations/README.md).

Method:

Added a no-claim storage/profile registry and validator covering profile, Space, session, snapshot, migration, disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, data-loss, authority boundaries, unsupported boundaries, and safe-failure behavior.

Decision:

Treat `PB-016` as `partial` because checked planning evidence exists, while requiring executable schemas, malformed/downgrade/corrupt/disk-full/power-loss/private-session/crash/data-loss tests, real-profile fixture policy, migration rehearsal, privacy review, data-loss review, release-operations review, and owner approval before any real profile or production format work.

Impact:

No profile implementation, real-profile migration, sync support, credential-storage support, user-data handling readiness, data-loss safety, production profile-format readiness, broad M1 readiness, or production claim is supported.

Next question:

Which executable schema and fault-test harness should convert the `PB-016` planning inventory into testable format evidence without touching real user profiles?

## 2026-07-18 — Native UI component fixture inventory

Question:

Can `PB-014` move from product/UI prose into checked planning evidence without implying that native UI fixtures, toolkit selection, trusted chrome, or accessibility readiness exist?

Inputs:

- [Native UI component fixture inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- [`component-fixture-inventory.json`](ui-runtime/machine/component-fixture-inventory.json);
- [`component-fixture-inventory.schema.json`](ui-runtime/machine/component-fixture-inventory.schema.json);
- [`tools/validate_ui_component_fixtures.py`](../tools/validate_ui_component_fixtures.py);
- [Native UI Runtime book](ui-runtime/README.md);
- [Accessibility book](accessibility/README.md);
- [Product Experience book](product-experience/README.md).

Method:

Added a no-claim UI component fixture registry and validator covering semantic token groups, browser chrome, tabs, Spaces, command field, permission prompts, agent confirmations, resource manager, settings, recovery UI, keyboard, focus, screen-reader, forced-color, high-contrast, reduced-motion, density, localization, error-state, accessibility contracts, and authority boundaries.

Decision:

Treat `PB-014` as `partial` because checked planning evidence exists, while requiring rendered fixture packs, adapter-specific fixture outputs, real platform accessibility evidence, and owner review before any toolkit, trusted-chrome, accessibility, page-surface, or release-path UI approval.

Impact:

No UI implementation, rendered fixture, toolkit selection, accessibility readiness, trusted-chrome readiness, page-surface approval, production readiness, compatibility, security, performance, memory, energy, Chrome-class, beta, stable, or daily-driver claim is supported.

Next question:

Which adapter-specific rendered fixture pack and reference-platform accessibility output should make the `PB-014` inventory executable?

## 2026-07-18 — Benchmark corpus expansion

Question:

Can `PB13-EV-003` move beyond the initial two-case no-claim seed while preserving generated local provenance, checked hashes, route coverage, and no-claim boundaries?

Inputs:

- [Benchmark corpus expansion](research/benchmark-corpus-expansion-2026-07.md);
- [Benchmark corpus schema](blueprint-v1/machine/benchmark-corpus.schema.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [`tools/validate_benchmark_corpus.py`](../tools/validate_benchmark_corpus.py);
- [`tools/validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Expanded the no-claim corpus manifest from two generated local fixtures to seven generated local fixtures covering static-document, app-like, accessibility, international-text, hostile-markup, media-document, and service-worker-contract shapes. Added matching fixture files, SHA-256 digests, byte counts, category validation, and loopback route coverage in the local static network profile.

Observations:

- the corpus validator now requires every no-claim smoke category and checks every fixture hash and byte count;
- the network-profile validator now checks route coverage for every expanded corpus case;
- the service-worker contract fixture does not register a worker, open Cache Storage, or intercept fetch;
- the expanded corpus remains generated smoke evidence only, not a reviewed representative corpus.

Decision:

Treat `PB13-EV-003` as partially evidenced by the expanded no-claim corpus seed, while keeping the reviewed representative offline corpus, browser-run fixture evidence, and raw artifact package as missing proof.

Impact:

`PB-013` stays `documented_no_runner`. The expansion does not support browser rendering, compatibility, accessibility, service-worker, media, security, speed, memory, energy, Chrome-class, daily-driver, beta, stable, production, or performance claims.

Next question:

What corpus-selection policy, disabled-case denominator, and browser-run artifact shape should turn the expanded no-claim seed into a reviewed benchmark corpus?

## 2026-07-18 — Benchmark server lifecycle self-test

Question:

Does `PB13-EV-004` have checked runner-managed server startup, route-check, shutdown, and artifact-hash evidence before browser benchmark execution exists?

Inputs:

- [Benchmark server lifecycle self-test](research/benchmark-server-lifecycle-self-test-2026-07.md);
- [`no-claim-local-static.profile.json`](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [`serve_benchmark_profile.py`](../tools/serve_benchmark_profile.py);
- [`run_benchmark_server_profile.py`](../tools/run_benchmark_server_profile.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a no-claim server lifecycle runner that loads the checked network profile, starts the local HTTP/1.1 loopback server on an ephemeral port, checks configured corpus routes with the `turing.invalid` Host header, shuts the server down, verifies the port no longer accepts the test connection, writes startup, route-check, shutdown, runner-summary, and artifact-index JSON files, and hashes every artifact.

Decision:

The benchmark network lane needs server lifecycle evidence before browser-run measurement so startup, route coverage, shutdown, cleanup, artifact hashing, DNS-boundary language, and no-claim finalization cannot be invented by later browser-run work.

Impact:

`PB13-EV-004` now has checked runner-managed server lifecycle self-test evidence. This does not produce browser-run server evidence, modify OS DNS resolver state, exercise TLS, HTTP/2, HTTP/3, proxy, authentication, cache-revalidation, or network shaping, launch a browser, capture traces, produce raw samples, prove latency or cache behavior, promote `PB-013`, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, compatibility, or performance claim.

## 2026-07-18 — Benchmark browser launch-runner contract

Question:

Does `PB13-EV-005` have a checked no-claim browser launch-runner contract and no-browser self-test before a browser-run benchmark implementation exists?

Inputs:

- [Benchmark browser launch-runner contract](research/benchmark-browser-launch-runner-contract-2026-07.md);
- [`benchmark-launch-runner.schema.json`](blueprint-v1/machine/benchmark-launch-runner.schema.json);
- [`no-claim-browser-launch.plan.json`](blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json);
- [`validate_benchmark_launch_runners.py`](../tools/validate_benchmark_launch_runners.py);
- [`run_benchmark_browser_launch.py`](../tools/run_benchmark_browser_launch.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a sample-only launch-runner schema, a no-claim browser launch-runner plan, a validator that checks required and forbidden command arguments, current no-claim registry references, launch-stage coverage, timeout/cancellation policy, cache/profile policy, failure finalization, trace/artifact linkage, resource-attribution linkage, unsupported behavior, missing proof, and no-claim wording, plus a checked no-browser browser launch-runner self-test that validates command parsing, forbidden argument rejection, registry references, artifact-root handling, hashed artifacts, and no-claim finalization. Synchronized `PB-013`, the benchmark research lane, `TASK-000005`, the performance packet, indexes, repository map, and related performance books.

Decision:

The browser benchmark launch path needs a checked contract before implementation so timeout, cancellation, cache/profile reset, forbidden arguments, failure denominator, trace/artifact package, cleanup, and no-claim result finalization cannot be skipped by the first runner.

Impact:

`PB13-EV-005` now has no-claim browser launch-runner contract evidence and checked no-browser browser launch-runner self-test evidence beyond the smoke runner and browser-pin records. This does not implement a browser-run launch runner, launch a browser, capture traces, produce raw samples, prove memory or energy behavior, promote `PB-013`, approve benchmark-ready browser pins, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, or compatibility claim.

## 2026-07-18 — Benchmark trace/artifact package contract

Question:

Does `PB13-EV-007` have a checked no-claim trace/artifact package contract before a browser benchmark runner exists?

Inputs:

- [Benchmark trace/artifact package contract](research/benchmark-trace-artifact-package-contract-2026-07.md);
- [`benchmark-artifact-package.schema.json`](blueprint-v1/machine/benchmark-artifact-package.schema.json);
- [`no-claim-trace-package.plan.json`](blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json);
- [`validate_benchmark_artifact_packages.py`](../tools/validate_benchmark_artifact_packages.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a sample-only artifact-package schema, a no-claim trace/artifact package plan, and a validator that checks runner-owned root policy, ETW or equivalent trace class, Perfetto-compatible trace class, tab lifecycle log class, required artifact classes, SHA-256 manifest records, redaction/retention requirements, prohibited-content rules, no-claim wording, and current no-claim registry references. Synchronized `PB-013`, the benchmark research lane, `TASK-000005`, the performance packet, indexes, repository map, and related performance books.

Decision:

Trace and artifact package evidence needs a checked contract before a runner can persist raw benchmark artifacts, and real traces, logs, screenshots, memory snapshots, power samples, failure records, redaction review, retention decisions, and SHA-256 manifests must stay required proof.

Impact:

`PB13-EV-007` now has no-claim package-contract evidence instead of unstructured missing proof. This does not launch a browser, capture ETW or Perfetto traces, produce raw samples, prove memory or energy behavior, promote `PB-013`, approve a benchmark-ready runner, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, or compatibility claim.

## 2026-07-18 — Benchmark 30-tab scenario contract

Question:

Does `PB13-EV-008` have checked mixed-state and all-live 30-tab scenario records before a browser benchmark runner exists?

Inputs:

- [Benchmark 30-tab scenario contract](research/benchmark-30-tab-scenario-contract-2026-07.md);
- [`benchmark-tab-scenario.schema.json`](blueprint-v1/machine/benchmark-tab-scenario.schema.json);
- [`no-claim-30-tab-smoke.scenarios.json`](blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json);
- [`validate_benchmark_tab_scenarios.py`](../tools/validate_benchmark_tab_scenarios.py);
- [Performance benchmark readiness packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method:

Added a sample-only tab-scenario schema, a no-claim 30-tab mixed-state and all-live scenario manifest, and a validator that checks exact 30-tab totals, lifecycle state-count parity, corpus case references, network-profile route coverage, all-live versus mixed-state semantics, and no-claim wording. Synchronized `PB-013`, the benchmark research lane, `TASK-000005`, the performance packet, indexes, repository map, and related performance books.

Decision:

The 30-tab workload needs a checked denominator record before a runner can emit raw artifacts, and mixed-state results must stay separate from all-live results.

Impact:

`PB13-EV-008` now has no-claim scenario-manifest evidence instead of prose-only planning. This does not launch a browser, produce raw artifacts, prove memory or energy behavior, promote `PB-013`, approve a benchmark-ready runner, or support any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, security, accessibility, or compatibility claim.

## 2026-07-18 — Direct command and line-ending handoff tightening

Question:

Do the root README and operating board distinguish wrapper-managed handoff validation from direct Cargo invocation while matching the expanded LF policy?

Inputs:

- [README](../README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Repository map](repository-map.md);
- [`.gitattributes`](../.gitattributes);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Clarified in the root README and documentation-readiness matrix that direct Cargo commands are behavior-equivalent to the wrappers but inherit the caller's `CARGO_TARGET_DIR`, so source-tree cleanliness evidence should prefer wrappers or an explicitly external target directory. Updated the operating-board newline evidence row to cover Markdown, GitHub YAML, Rust, JSON, scripts, and repository tooling files instead of only Rust and tooling sources.

Decision:

Handoff docs must not imply direct Cargo invocation provides the same target-directory hygiene as the wrappers unless the caller has set the environment deliberately.

Impact:

Maintainers get clearer local validation guidance and the operating board now matches the repository LF policy. This is documentation and validation alignment only; it does not prove fresh-host reproduction, promote `PB-009`, or change any product-readiness or browser-capability claim.

## 2026-07-18 — Machine wrapper parity

Question:

Do machine readiness records list the PowerShell validation wrappers alongside the POSIX wrappers?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `tools/bootstrap.ps1`, `tools/doctor.ps1`, and `tools/check.ps1` beside the existing POSIX wrapper paths in the pre-build readiness evidence, fresh-host research lane evidence, and `TASK-000002` allowed paths. Updated the operating-board build-validation evidence row to include `tools/check.ps1`.

Decision:

Machine records must expose the same Windows validation entry points as the human-facing handoff docs so task shaping and readiness evidence stay synchronized.

Impact:

Fresh-host, task-queue, and readiness evidence now route Windows maintainers to the implemented wrapper paths. This is machine-record parity only; it does not promote `PB-009`, approve `TASK-000002`, prove independent fresh-host reproduction, or change any browser capability claim.

## 2026-07-18 — First-entry validation handoff surfaces

Question:

Do the Start Here page, documentation index, and build-readiness operating board give maintainers concrete validation entry points before handoff?

Inputs:

- [Start Here](start-here.md);
- [Documentation index](README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added aggregate validation wrapper guidance to the first-entry handoff surfaces: `sh tools/check.sh` for POSIX shells and `.\tools\check.ps1` for Windows PowerShell. Linked the full direct command family back to the documentation-readiness matrix and kept the proof boundary limited to contained M0 repository validation.

Decision:

Stop/resume documents should not only point to gate truth; they should tell the next maintainer exactly how to prove the repository still validates before work continues.

Impact:

Maintainers can find the current validation entry points from the first docs they read. This is handoff guidance only; it does not approve tasks, promote readiness, prove semantic documentation completeness, or change any browser capability claim.

## 2026-07-18 — Agent and PR Windows wrapper handoff alignment

Question:

Do the root agent instructions, PR template, prototype guide, repository map, and documentation-readiness matrix point Windows maintainers to the new PowerShell aggregate-check wrapper?

Inputs:

- [AGENTS.md](../AGENTS.md);
- [Pull request template](../.github/pull_request_template.md);
- [Prototype guide](prototype.md);
- [Repository map](repository-map.md);
- [Documentation readiness matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Replaced stale Windows guidance that asked maintainers to set `CARGO_TARGET_DIR` manually with references to `.\tools\check.ps1`, which delegates to the aggregate `xtask check` path and sets `CARGO_TARGET_DIR` outside the repository when unset. Added the same wrapper note to the prototype guide and documentation-readiness validation section.

Decision:

Agent and pull-request handoff surfaces should name the Windows wrapper directly so a maintainer can resume and validate from PowerShell without reconstructing environment setup from lower-level Cargo commands.

Impact:

Windows handoff guidance now matches the implemented wrapper contract. This is validation ergonomics only; it does not change M0 gate status, product platform support, release support, or browser capability claims.

## 2026-07-18 — Staged diff command-list alignment

Question:

Do the direct local-check command lists include the staged diff hygiene gate now enforced by `xtask check`?

Inputs:

- [AGENTS.md](../AGENTS.md);
- [Contributing](contributing.md);
- [Pull request template](../.github/pull_request_template.md);
- [Documentation readiness matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `git diff --cached --check` beside `git diff --check` in the direct command lists used by agents, contributors, pull requests, and documentation-readiness handoffs. Updated validation markers so those direct handoff surfaces keep the staged-diff check visible.

Decision:

Direct command lists should show both unstaged and staged diff hygiene checks because staged changes can differ from the working tree before handoff.

Impact:

Maintainers who run the listed commands one by one now get the same staged-diff hygiene signal as the aggregate local check. This is handoff hygiene only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim.

## 2026-07-18 — Windows PowerShell validation wrappers

Question:

Can a Windows maintainer run the M0 bootstrap, doctor, and complete local check through first-class PowerShell wrappers instead of relying on POSIX `sh` wrappers?

Inputs:

- [`tools/bootstrap.ps1`](../tools/bootstrap.ps1);
- [`tools/doctor.ps1`](../tools/doctor.ps1);
- [`tools/check.ps1`](../tools/check.ps1);
- [Root README](../README.md);
- [Contributing](contributing.md);
- [Repository map](repository-map.md);
- [M0 build foundation report](research/m0-build-foundation-2026-07.md);
- [`tools/validate_build_foundation.py`](../tools/validate_build_foundation.py);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added PowerShell wrappers that set `CARGO_TARGET_DIR` under the system temporary directory when unset and then delegate to the same locked `xtask` bootstrap, doctor, and check commands as the POSIX wrappers. Updated root, contributor, readiness, repository-map, and M0 build-foundation documentation so Windows and POSIX entry points are visible together.

Decision:

Windows validation entry points are part of the M0 build foundation because the current development and evidence collection happen on Windows as well as the Ubuntu CI reference. The wrappers must stay thin and must not fork validation behavior away from `xtask`.

Impact:

Windows maintainers can run `.\tools\bootstrap.ps1`, `.\tools\doctor.ps1`, and `.\tools\check.ps1` directly from PowerShell. This improves local handoff ergonomics only; it does not change product platform support, cross-platform preview status, readiness gates, or browser capability claims.

## 2026-07-18 — Markdown and workflow line-ending policy

Question:

Does the repository line-ending policy cover Markdown and GitHub workflow templates, the files most likely to carry documentation handoffs and CI control changes?

Inputs:

- [`.gitattributes`](../.gitattributes);
- [Repository map](repository-map.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `*.md`, `*.yml`, and `*.yaml` LF rules to `.gitattributes`, alongside the existing Rust, TOML, JSON, HTML, Python, and shell rules. Updated the repository map to state that Markdown and GitHub YAML are covered, not only Rust and tooling files.

Decision:

Documentation and workflow files are part of the build-readiness control plane, so they need the same stable line-ending policy as source and validation files.

Impact:

Future changed or checked-out Markdown and GitHub YAML should preserve LF before local or CI diff hygiene checks run. Existing historical blobs were not renormalized in this change; changed-range hygiene remains enforced by local and CI diff checks. This is source-control hygiene only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim.

## 2026-07-18 — Local aggregate diff hygiene coverage

Question:

Does the complete local `xtask check` path enforce the same diff whitespace hygiene required by contributor and agent handoff guidance?

Inputs:

- [`xtask`](../tools/xtask/src/main.rs);
- [Root README](../README.md);
- [Contributing](contributing.md);
- [M0 build foundation report](research/m0-build-foundation-2026-07.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added `git diff --check` and `git diff --cached --check` to `xtask check` after repository validation and before Rust formatting. Updated the root README, contributor guide, and M0 build-foundation report to state that the aggregate local check covers both unstaged and staged diff whitespace.

Decision:

The aggregate local check should fail on whitespace and line-ending drift even when a maintainer relies on `tools/check.sh` instead of running the listed commands one by one.

Impact:

Local full-check runs now catch unstaged and staged diff hygiene failures before handoff. This is source-hygiene coverage only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim.

## 2026-07-18 — CI committed-diff whitespace enforcement

Question:

Does the GitHub workflow enforce the same `git diff --check` whitespace gate that local contributor, agent, and pull-request handoff guidance requires?

Inputs:

- [Repository validation workflow](../.github/workflows/repository-validation.yml);
- [Root README](../README.md);
- [Contributing](contributing.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a committed-range whitespace check to the repository validation workflow. Pull requests check `base` to `head`; pushes check `before` to `github.sha`; root commits or zero `before` values use `git diff-tree --check --root -r`. The workflow uploads `diff-whitespace.log` with the other validation diagnostics. Updated contributor guidance and the root CI summary to match.

Decision:

CI must enforce committed-diff whitespace because local `git diff --check` only covers the working tree before handoff. This keeps line-ending and trailing-whitespace drift from reappearing after Windows edits, generated docs, or template updates.

Impact:

Pull requests and pushes now fail on committed whitespace errors. This is hygiene enforcement only; it does not prove documentation semantic completeness, promote build readiness, approve tasks, or change any browser capability claim.

## 2026-07-18 — Aggregate xtask ADR evidence coverage

Question:

Does the aggregate `xtask check` path run the same ADR-0009 evidence validator required by the current contributor, agent, and pull-request gates?

Inputs:

- [`xtask`](../tools/xtask/src/main.rs);
- [Repository validation workflow](../.github/workflows/repository-validation.yml);
- [Root README](../README.md);
- [Prototype guide](prototype.md);
- [M0 build foundation report](research/m0-build-foundation-2026-07.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated `xtask check` to run `python3 -B tools/validate_adr_0009_evidence.py` after the Blueprint validator and before build-foundation validation. Updated the repository validation workflow with an ADR-0009 evidence step and uploaded diagnostic log. Updated `xtask` bootstrap/help text to print locked Cargo commands. Updated the root README, prototype guide, and M0 build-foundation report so the aggregate check, CI check, and prototype-only checks describe the current gate shape.

Decision:

The aggregate repository check and CI workflow must include ADR-0009 evidence validation because Servo/source-strategy tracking is an active pre-build blocker. This aligns `tools/check.sh`, `xtask check`, contributor guidance, agent guidance, CI validation, and GitHub handoff guidance.

Impact:

Local full-check runs now fail if ADR-0009 evidence records drift from the matrix or evidence files. This is gate alignment only; it does not resolve ADR-0009, unblock `PB-002`, approve Servo adoption, or promote any M0 foundation work beyond contained research/build readiness.

## 2026-07-18 — GitHub handoff template validation refresh

Question:

Do the GitHub PR and engineering issue templates expose the current validation family, core registry review, and proposed task identifiers?

Inputs:

- [Pull request template](../.github/pull_request_template.md);
- [Engineering issue template](../.github/ISSUE_TEMPLATE/engineering.yml);
- [Core program registries](repository-map.md#core-program-registries);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated the pull request template with proposed task/readiness fields, a core program-registry review line, the current validation command family, and the `CARGO_TARGET_DIR` source-tree-cleanliness note. Updated the engineering issue template placeholder to include `TASK-*` identifiers for proposed build-readiness handoffs.

Decision:

GitHub intake surfaces must use the same vocabulary and validation family as `AGENTS.md`, `docs/contributing.md`, the repository map, and the build-readiness task queue. Template fields do not approve tasks, promote readiness, or prove support status.

Impact:

Contributors opening issues or pull requests are now prompted to include `TASK-*` context, review core registries before changing authority, and run the current checks. No issue, task, readiness, owner, or product claim changed.

## 2026-07-18 — Agent and contributor validation command refresh

Question:

Do the root agent instructions and canonical contributor guide list the current repository checks rather than the older prototype-only subset?

Inputs:

- [AGENTS.md](../AGENTS.md);
- [Contributing](contributing.md);
- [`xtask`](../tools/xtask/src/main.rs);
- [`tools/check.sh`](../tools/check.sh);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated the completion and local-check command blocks to include `python3 -B` validation, `validate_adr_0009_evidence.py`, `git diff --check`, full workspace formatting, prototype checks, and `cargo run --locked -p xtask -- check`. Added the source-tree cleanliness note for `CARGO_TARGET_DIR` outside the repository.

Decision:

Agent and contributor handoff documents must route to the same current validation gate family as the repository validator and aggregate `xtask` check. The command list is validation guidance only; it does not promote readiness, approve a proposed task, or substitute for owner review.

Impact:

Maintainers and agents running from the root instructions or contributing guide now execute the same documented validation family used by the current documentation-readiness work. No code behavior, readiness status, or product claim changed.

## 2026-07-18 — Root and Start Here registry continuity

Question:

Do the two broadest first-entry documents point maintainers to the core program registries before they change scope, authority, readiness, or task status?

Inputs:

- [root README](../README.md);
- [Start Here](start-here.md);
- [Repository map](repository-map.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added core program-registry navigation to the root stop/resume path and Start Here stop/resume map. Both now route maintainers to the repository-map registry table before changes to requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas.

Decision:

The first-entry path must lead to the same machine sources of truth as the docs index, Blueprint index, and repository map. This routing is a governance control only; it does not approve tasks, promote readiness, or prove implementation status.

Impact:

A person resuming from the root README or Start Here can find the core machine registries without reading prior chat history. No requirement, risk, work package, readiness item, owner assignment, task approval, agent authority, or product claim changed.

## 2026-07-18 — Blueprint and docs registry entry points

Question:

Do the main documentation index and Blueprint index route maintainers to the same core program-registry map as the repository map?

Inputs:

- [Documentation index](README.md);
- [Blueprint index](blueprint-v1/README.md);
- [Documentation policy](documentation-policy.md);
- [Repository map](repository-map.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added explicit core machine-registry navigation to the docs index and Blueprint index. The Blueprint index now names the core machine companions for requirements, risks, backlog, readiness, task queue, process capabilities, workspace/toolchains, professional controls, and agent action schema, and links back to the repository map table for boundaries.

Decision:

The docs index, Blueprint index, repository map, and documentation policy must all expose that machine registries are sources of truth for scope and authority, not implementation proof or readiness promotion.

Impact:

A maintainer starting from either index can find the same registry map before changing implementation scope, authority, readiness, or task status. No machine registry status, task approval, readiness promotion, or product claim changed.

## 2026-07-18 — Core machine-registry navigation

Question:

Can a maintainer resuming from the repository map find the core machine-readable sources of truth without confusing them with feature readiness or task approval?

Inputs:

- [Repository map](repository-map.md);
- [`requirements.json`](blueprint-v1/machine/requirements.json);
- [`risks.json`](blueprint-v1/machine/risks.json);
- [`backlog.json`](blueprint-v1/machine/backlog.json);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`process-capabilities.json`](blueprint-v1/machine/process-capabilities.json);
- [`professional-owners.json`](blueprint-v1/machine/professional-owners.json);
- [`workspace-components.json`](blueprint-v1/machine/workspace-components.json);
- [`agent-action.schema.json`](blueprint-v1/machine/agent-action.schema.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a core program-registry table to the repository map, separate from benchmark/source evidence registries. The table routes requirements, risks, work packages, pre-build readiness, the proposed task queue, process capabilities, workspace/toolchains, professional controls, and the agent action schema to their owning prose and explicit no-claim boundaries.

Decision:

The repository map must expose the machine registries that control scope, readiness, ownership, and authority. These records remain sources of truth for review and handoff, not evidence that features are implemented, tasks are approved, mitigations are complete, or production support exists.

Impact:

People and agents can now resume from the repository map and find the core program-control registries without relying on chat history. No requirement, risk, work package, readiness item, owner assignment, agent authority, task approval, or product claim changed.

## 2026-07-18 — Contained-M0 allowed-now boundary

Question:

Does the machine readiness registry describe allowed work narrowly enough for a maintainer or agent to avoid treating contained M0 work as broad implementation approval?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Narrowed the top-level `allowed_now` registry field from broad shorthand into explicit contained/no-claim M0 categories: documentation, research, root-workspace source tasks, typed kernel/identity/IPC/UI-model foundations, isolated native UI comparison prototypes, expected-deny sandbox probes, benchmark corpus and no-claim measurement tooling, profile/session schema prototypes, research-package/updater lab prototypes without production keys or a real updater, private-intake tabletop documentation, and task-scoped diagnostic tooling.

Decision:

`allowed_now` is an authorization boundary, not a feature roadmap. It must stay aligned with `PB-GATE-0`, the pre-build audit, and the operating board, and it must not imply production update, incident-response, benchmark, UI-toolkit, sandbox, profile, ownership, Chrome-class, or broad M1 approval.

Impact:

The machine source of truth now matches the human handoff language more closely. No readiness item was promoted, no proposed `TASK-*` item was approved, and no implementation, release, benchmark, updater, incident-response, or production claim changed.

## 2026-07-18 — Entry-point lane-set invariant

Question:

Do the first-entry documents name the same current implementation-research lane set as the research index and machine crosswalk?

Inputs:

- [Start Here](start-here.md);
- [root README](../README.md);
- [documentation index](README.md);
- [documentation policy](documentation-policy.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Updated the stop/resume language in the entry points so the source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, and ownership lanes are all visible before implementation work. Added validation so `start-here.md`, the root README, the docs index, and the research lane table cannot silently omit the package/update or incident-response lanes.

Decision:

The entry points must name the full lane set or link to an index that does. The lane list remains a navigation and handoff control only; it does not approve any proposed task, readiness promotion, package/update work, incident-response authority, ownership coverage, or implementation expansion.

Impact:

A maintainer resuming from the root README, `docs/README.md`, or `docs/start-here.md` now sees the same lane set that the research crosswalk and task queue enforce. No readiness status or support claim changed.

## 2026-07-18 — Ownership readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same evidence required before `PB-019` can move out of blocked status?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`professional-owners.json`](blueprint-v1/machine/professional-owners.json);
- [`professional-review-rules.json`](blueprint-v1/machine/professional-review-rules.json);
- [ownership and maintainer ladder](project-buildout/02-ownership-codeowners-and-maintainer-ladder.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded `PB-019` from a one-line "named qualified backups" blocker into explicit backup-owner evidence for build-critical program, architecture, security, release-operations, human-release-authority, incident-response, legal-community, support, quality, supply-chain, documentation-research, product, platform, engine, JavaScript, networking, storage, performance, accessibility, UI-runtime, agent-operations, and privacy-data scopes. Added qualification, path coverage, review record, availability, succession, recusal, inactivity, removal, emergency replacement, CODEOWNERS, review-rule, escalation-policy, support, signing, disclosure, package, CI, service, repository-access, stale-access, ownerless-path, primary-only-path, blocked-status, single-owner-risk, and two-person-control evidence requirements.

Decision:

Keep `PB-019` blocked while any professional owner backup is null, a placeholder, undocumented, primary-only, or not independently reviewable. Documentation may organize the blocker, but it does not name qualified backups or create release, signing, update-trust, supported-version, security-disclosure, irreversible-migration, legal-approval, incident-closure, production-authority, or owner-coverage claims.

Impact:

The ownership and review-capacity continuation lane is now concrete enough for handoff. No owner assignment, backup qualification, access grant, release authority, disclosure authority, signing authority, M1 readiness, preview readiness, or production claim changed.

## 2026-07-18 — Operational readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same package/update and incident-response evidence required across `PB-017`, `PB-018`, `TASK-000009`, and `TASK-000010`?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [release operations book](release-operations/README.md);
- [security policy](security.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded `PB-017` from a signed-package placeholder into signed research-package identity, update-metadata, tamper/replay/wrong-target/expiry/mirror/partial-write/disk-full/power-loss, rollback, vulnerable-version refusal, migration, downgrade, crash-loop, privacy-preserving event, and no-production-key evidence. Expanded `PB-018` from a tabletop placeholder into private intake, access control, severity and asset analysis, embargo, protected patch branch, embargoed CI, regression, backport, signing/update dry run, rollout, revocation, communication, coordinated disclosure, postmortem, incident-class, role, timing, escalation, secret-rotation, and no-agent-authority evidence. Added `TASK-000009` and `TASK-000010` as proposed-only task-shaped handoffs and validation so the registry, board, checklist, audit, task queue, research index, and crosswalk cannot silently narrow these gates.

Decision:

Keep `PB-017` and `PB-018` no higher than partial planning evidence until executable research-package/updater lab and incident/patch rehearsal evidence exists. Proposed tasks do not approve a production updater, stable channel, public distribution, signing readiness, supported security versions, incident-response readiness, emergency patch capacity, disclosure authority, stable promotion, or signing authority.

Impact:

The operational-readiness continuation path is now explicit before broad implementation. No release, updater, stable support, security-support, production-safety, or incident-authority claim changed.

## 2026-07-18 — Native shell readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same native-shell evidence required across `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006`?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded the native-shell lane from short placeholders into explicit readiness evidence: toolkit-neutral state/command/surface/accessibility/diagnostic/adapter contracts, equivalent reference-shell adapters, page-surface composition, design-token and component fixtures, IME, keyboard, accessibility, crash, GPU-loss, startup, memory, binary, latency, frame-pacing, energy, license, dependency, provenance, reference-platform workflow, and assistive-technology coverage. Added validation so the machine readiness registry, proposed task queue, operating board, checklist, audit, research index, and research crosswalk cannot silently narrow the lane.

Decision:

Keep `PB-003` partial, keep `PB-004`, `PB-005`, and `PB-015` not started, and do not move `PB-014` beyond partial planning evidence until equivalent rendered adapter and page-surface evidence exists. This does not select a UI toolkit, approve trusted-chrome readiness, approve accessibility readiness, or convert the command-line shell model into a native UI.

Impact:

The native-shell continuation path is more coherent for product, UI runtime, platform, accessibility, performance, security, build, and release review. No UI toolkit selection, page-surface approval, accessibility readiness, trusted-chrome readiness, release-path UI approval, M1 readiness, or production claim changed.

## 2026-07-18 — PB-016 profile/session readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same profile, Space, session, snapshot, and migration evidence required before `PB-016` can advance?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded `PB-016` from generic profile/session format language to an explicit schema and failure-boundary invariant: versioned profile, Space, session, snapshot, and migration schemas; disk-full, power-loss, corruption, downgrade, export, deletion, private-session, crash-recovery, protected-work, privacy, and data-loss behavior; and unsupported sync, credential storage, real-profile migration, user-data handling, and production profile-format boundaries. Added validation so the machine readiness registry, proposed task queue, operating board, checklist, audit, research index, and research crosswalk cannot silently narrow those requirements.

Decision:

Keep `PB-016` no higher than partial planning evidence until executable schema evidence and the full failure/privacy boundary are reviewed. This shapes the next storage/product handoff; it does not approve real-profile fixtures, sync, credential storage, data-loss safety, or a production profile format.

Impact:

The profile/session continuation path is more coherent for storage, product, migration, and privacy work. No profile implementation, migration support, sync support, credential-storage support, data-loss safety claim, user-data handling readiness, broad M1 readiness, or production claim changed.

## 2026-07-18 — PB-012 sandbox-probe readiness invariant

Question:

Do the canonical readiness records, research crosswalk, and proposed task queue describe the same sandbox-probe evidence required before `PB-012` can advance?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Promoted the `PB-012` sandbox-probe handoff from generic packaged sandbox evidence to explicit expected-deny coverage for renderer, network, storage, GPU, decoder, extension, DevTools, agent, and updater roles across file, socket, process, registry, device, shared-memory, credential, debug, profile, and IPC access. Added validation so the machine readiness registry, proposed task queue, operating board, checklist, audit, research index, and research crosswalk cannot silently drop the role list or denial surfaces.

Decision:

At that time, `PB-012` stayed `not_started` until checked planning evidence or platform-enforced expected-deny probe evidence existed. The later Sandbox Probe Inventory entry above supersedes only the status portion by moving `PB-012` to partial; this invariant still does not accept a sandbox policy, grant release readiness, or approve execution of `TASK-000004`.

Impact:

The sandbox continuation path is now coherent and reviewable before any renderer, network, storage, GPU, decoder, extension, DevTools, agent, or updater role is trusted. No sandbox implementation, site-isolation readiness, hostile-browsing safety, security claim, M1 readiness, or production claim changed.

## 2026-07-18 — PB-011 readiness invariant propagation

Question:

Do the canonical pre-build readiness records carry the same IPC negative-test invariant as the `TASK-000003` handoff queue?

Inputs:

- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Pre-build Readiness Gap Audit](research/pre-build-readiness-gap-audit-2026-07.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded the `PB-011` missing-evidence wording from generic negative sender tests to the explicit malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation set. Propagated the same wording into the checklist and readiness audit, then extended validation so the machine readiness registry and human pre-build records cannot drift below that coverage.

Decision:

Keep `PB-011` in `partial` status until schema generation, wire encoding, and the full IPC negative-test set are reviewed. This does not approve execution of `TASK-000003`.

Impact:

The canonical readiness view now matches the task queue and research crosswalk for IPC work. No wire format, process topology, IPC implementation, sandbox readiness, M1 readiness, or production/security claim changed.

## 2026-07-18 — IPC negative-test handoff invariant refresh

Question:

Do the build-readiness board, proposed task queue, machine task registry, and validation agree on the IPC negative-test set required before `PB-011` can advance?

Inputs:

- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [`build-readiness-task-queue.json`](blueprint-v1/machine/build-readiness-task-queue.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Aligned the IPC handoff language so malformed, oversized, stale, duplicate, reordered, unauthorized, wrong-principal, timeout, and cancellation cases are all required in the human operating board and proposed task queue. Updated the machine task registry for `TASK-000003` and added validation that keeps the human and machine records from dropping timeout, cancellation, or wrong-principal coverage.

Decision:

Treat timeout and cancellation behavior as part of the IPC negative-test invariant, not as optional follow-up coverage. `TASK-000003` remains proposed only and still requires owner review before execution.

Impact:

The process-authority continuation path is more coherent for a maintainer resuming `PB-011`. No IPC implementation, source-strategy decision, process-security claim, sandbox readiness, broad M1 readiness, or production claim changed.

## 2026-07-18 — Current documentation count invariant refresh

Question:

Can root-level build status describe the current documentation library without preserving a historical count phrase as a validator dependency?

Inputs:

- root [`README.md`](../README.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Replaced the root README's historical “grew from twenty-five to twenty-seven” phrasing with direct current-state wording that the documentation library contains twenty-seven detailed engineering and product books. Updated the validator to enforce the current count phrase and refreshed the pre-build checklist audit date for the latest documentation-readiness edits.

Decision:

Keep root build status tied to current documentation topology rather than historical growth wording. The validator should guard the current twenty-seven-book statement, not the older transition phrase.

Impact:

The entry-point status is easier to scan and less brittle for future maintainers. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Documentation handoff definition of done

Question:

Can documentation-readiness and handoff changes be completed against explicit criteria rather than broad documentation hygiene?

Inputs:

- [Definition of Done](blueprint-v1/20-definition-of-done.md);
- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a `Documentation readiness or handoff change` work type to the Definition of Done. The criteria require synchronized first-entry documents, objective-to-evidence mapping, human/machine record agreement, stop/resume gate truth, `RQ-*`/`PB-*`/`TASK-*` research mapping, claim-boundary preservation, indexing, research-log updates, validator coverage, and validation output scoped to what the checks prove.

Decision:

Use Blueprint 20 as the canonical completion contract for documentation-readiness and handoff changes. The documentation-readiness matrix now links to that DoD and records that the DoD is part of the evidence surface.

Impact:

Future documentation-control changes have a concrete finish line and cannot rely only on passing link checks. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Documentation readiness evidence matrix

Question:

Can the claim that documentation is organized enough for contained build work be reviewed against concrete evidence instead of broad confidence in the documentation set?

Inputs:

- [Documentation Readiness Evidence Matrix](project-buildout/18-documentation-readiness-evidence-matrix.md);
- [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Research index](research/README.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a documentation-readiness evidence matrix to the project-buildout handbook. The matrix maps the current user-facing objective to concrete evidence: entry points, stop/resume continuity, machine tracking, research crosswalks, source strategy, benchmark/extreme-performance no-claim evidence, agent task controls, topology validation, and M0 build gates.

Decision:

Treat the matrix as the review surface for `PB-001` documentation-readiness evidence. It supports contained M0 continuation only and must stay synchronized with the machine readiness registry, documentation entry points, research controls, task queue, repository map, and validation commands.

Impact:

Maintainers and agents can now inspect one artifact to see what the current documentation organization proves and what remains outside the proof. No broad M1 expansion, source-strategy decision, task approval, benchmark eligibility, or public product/performance/security claim changed.

## 2026-07-18 — Machine-readable research crosswalk registry

Question:

Can the build-readiness research crosswalk be validated against current `RQ-*`, `PB-*`, and `TASK-*` sources rather than relying only on prose review?

Inputs:

- [Research index](research/README.md);
- [`research-readiness-crosswalk.json`](blueprint-v1/machine/research-readiness-crosswalk.json);
- [`research-readiness-crosswalk.schema.json`](blueprint-v1/machine/research-readiness-crosswalk.schema.json);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json);
- [Build readiness task queue registry](blueprint-v1/machine/build-readiness-task-queue.json);
- [Research program](blueprint-v1/22-research-program.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a machine-readable research-readiness crosswalk and schema. The registry mirrors the eight current implementation-research lanes and records each lane's readiness blockers, proposed task handoff, primary research questions, evidence start points, next proof, and claim boundary.

Decision:

Treat the research crosswalk as a machine companion to the research index. It is a consistency and handoff control only; the registry cannot approve a task, promote a `PB-*` item, accept a source strategy, or authorize benchmark or public claims.

Impact:

Future research additions can be checked against the current research program, readiness registry, and task queue. This improves continuation reliability without changing any implementation authorization, readiness status, or product/performance/security claim.

## 2026-07-18 — Research readiness crosswalk enforcement

Question:

Can deep research stay tied to the build-readiness blockers and proposed task handoffs instead of becoming disconnected study inventory?

Inputs:

- [Research index](research/README.md);
- [Research program](blueprint-v1/22-research-program.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a build-readiness research crosswalk to the research index. Each current implementation-research lane now names the relevant `PB-*` blocker, proposed `TASK-*` handoff, primary `RQ-*` research questions, current evidence start point, next proof, and claim boundary. Extended validation so the crosswalk cannot lose the core `RQ-*`, `PB-*`, and `TASK-*` coverage silently.

Decision:

Keep the detailed research index as the current research-control surface. The lane table answers where to continue; the crosswalk answers which readiness gate and research questions the work advances.

Impact:

Maintainers and agents can connect source strategy, fresh-host reproduction, IPC, sandbox, benchmark, native shell, profile/session, and ownership work back to the research program before creating or executing task manifests. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or performance claim changed.

## 2026-07-18 — Documentation index continuation map enforcement

Question:

Can `docs/README.md` act as both a catalog and a current stop/resume guide without requiring a maintainer to jump back to the root README?

Inputs:

- [Documentation index](README.md);
- [Start Here](start-here.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a current stop/resume path to the documentation index, covering status, gate truth, research lane selection, task shaping, `ADR-0009` source-strategy evidence, Chrome-class and extreme-performance benchmark evidence, and claim boundaries. Added validator coverage for the docs-index continuation map.

Decision:

Keep `docs/README.md` as a catalog plus a current handoff guide. It points to authoritative state records rather than replacing the operating board, research index, task queue, machine registries, ADR packet, or benchmark evidence.

Impact:

Maintainers and agents entering through the canonical docs index now get the same contained-M0/no-claim stop/resume path as root README and `start-here.md`. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Root README continuation map enforcement

Question:

Can someone landing on the repository root find the same build-preparation stop/resume path as `docs/start-here.md`?

Inputs:

- root [`README.md`](../README.md);
- [Start Here](start-here.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a root-level current stop/resume path that points to the gate records, research lane map, proposed task queue, `ADR-0009` source-strategy packet, and no-claim benchmark/performance evidence. Updated the root start-here link list and added validator coverage for the root continuation map.

Decision:

Keep the root README as a discovery surface that sends maintainers into the canonical docs before implementation. It must repeat enough status and claim-boundary information to prevent a root-only reader from treating the repository as build-ready.

Impact:

The repository landing page now preserves the contained-M0/no-claim boundary and points to the current continuation path before build commands. No readiness status, source-strategy decision, task authorization, benchmark eligibility, or public claim changed.

## 2026-07-18 — Start-here continuation map enforcement

Question:

Can a new maintainer start from the top-level entry point and find the current build-preparation lanes without reading lower-level indexes first?

Inputs:

- [Start Here](start-here.md);
- [Documentation index](README.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Expanded the current build-readiness section in `start-here.md` into a stop/resume map covering gate truth, research lane selection, task shaping, source-strategy evidence, Chrome-class and extreme-performance evidence, and operating controls. Added validator coverage so the top-level entry point cannot silently lose that map.

Decision:

Keep `start-here.md` as the first human entry point for continuation, while the operating board, research index, task queue, machine registries, ADR records, benchmark records, and project-buildout handbook remain authoritative for state and approvals.

Impact:

New maintainers and agents can now see the same contained-M0/no-claim continuation path from the first document they read. No readiness status, task authorization, source-strategy decision, benchmark eligibility, or public claim changed.

## 2026-07-18 — Repository map documentation-section normalization

Question:

Can the repository map remain a usable structural reference after the source-strategy and benchmark evidence expansion?

Inputs:

- [Repository map](repository-map.md);
- [Research index](research/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Replaced the dense documentation-section paragraphs with grouped continuation records, machine evidence registries, benchmark research reports, and Servo/source-strategy research reports. Preserved the existing links and no-claim/source-strategy boundaries while making the structure easier to scan.

Decision:

Keep the repository map as a structural reference, not a second source of truth. The research index, operating board, machine registries, and validators remain authoritative for current state.

Impact:

Maintainers and agents can now locate documentation families, evidence registries, and validators from the repository map without parsing a long mixed paragraph or inferring approval from the presence of evidence.

## 2026-07-18 — Research lane-map validator coverage

Question:

Can the current implementation-research lane map remain durable after future documentation changes?

Inputs:

- [Research index](research/README.md);
- [Documentation policy](documentation-policy.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added repository validation for the research index lane map, including the required implementation-research heading, lane table shape, required lane names, continuation boundaries, and `Must not claim` coverage.

Decision:

Treat the lane map as a required handoff invariant. This does not change any lane status, owner approval, task authorization, benchmark eligibility, or claim boundary.

Impact:

Future changes cannot silently remove the source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership lanes without failing repository validation.

## 2026-07-18 — Research index implementation-lane map

Question:

Can the research index show the current continuation lanes without forcing a maintainer to parse long bundled priority sentences?

Inputs:

- [Research index](research/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build readiness audit](research/pre-build-readiness-gap-audit-2026-07.md).

Method:

Replaced the dense current-priorities list with a lane map covering source strategy, fresh-host build confidence, kernel/process authority/IPC, sandbox probes, benchmark/performance lab, native shell/page-surface composition, profile/session formats, and ownership/review capacity. Each lane now identifies where to start, the next evidence to produce, and what must not be claimed.

Decision:

Keep the research index as a navigation and continuation aid only. The operating board, machine readiness registry, proposed task queue, ADR records, and benchmark registries remain authoritative for state and approvals.

Impact:

The research index now gives maintainers and agents a clearer stop/resume map for build-preparation work while preserving contained-M0 status and no-claim boundaries.

## 2026-07-18 — Project-buildout handoff guide normalization

Question:

Can a maintainer use the project-buildout handbook as a fast continuation guide without parsing a single dense paragraph of source-strategy and benchmark links?

Inputs:

- [Project buildout handbook](project-buildout/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [ADR-0009 evidence registry](blueprint-v1/machine/adr-0009-evidence.json);
- [benchmark readiness evidence registries](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json).

Method:

Replaced the dense handoff paragraph in the project-buildout handbook with a scan-friendly continuation guide: build-readiness control path, source-strategy lane, benchmark/performance lane, validator list, and claim boundary.

Decision:

Keep the handbook as an operating index rather than a second source of truth. The operating board, machine readiness registry, task queue, ADR-0009 evidence registry, and benchmark registries remain authoritative for exact state.

Impact:

People and agents continuing the project can now find the current source-strategy and performance-readiness evidence in ordered groups without implying Servo adoption, broad implementation, benchmark readiness, Chrome-class comparison, or any public performance/security/compatibility claim.

## 2026-07-18 — Research log chronology normalization

Question:

Can the research log be scanned in a single newest-first chronology after the build-readiness and Servo evidence expansion?

Inputs:

- this research log;
- [documentation policy](documentation-policy.md);
- [documentation index](README.md);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Reordered dated research-log entries into newest-first order, moved the reusable entry template to the end of the file, preserved entry text, evidence statements, unsupported-claim boundaries, and marker comments, and added validator coverage for the chronology invariant.

Decision:

Keep the research log as a chronological handoff surface rather than a mixed chronology plus template interruption. This changes organization only; it does not promote readiness, approve execution, or alter any research conclusion.

Impact:

Maintainers and agents can now scan the material research and governance history without discovering newer July 17 entries after older July 15 and July 16 material, and repository validation will catch future chronology drift.

## 2026-07-18 — Build readiness action ownership split

Question:

Can the build-readiness handoff distinguish agent-workable evidence tasks from owner-only decisions before broad implementation starts?

Inputs:

- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json);
- [Agent Execution](agent-execution/README.md).

Method:

Added an action-ownership split to the operating board for `PB-002`, `PB-009`, `PB-011`, `PB-012`, `PB-013`, `PB-003` through `PB-005`, `PB-014`, `PB-015`, `PB-016`, and `PB-019`. The split identifies which work an agent can continue as no-claim evidence or documentation, and which decisions require an owner.

Decision:

Keep proposed task work separate from owner-only approvals. Agents may gather evidence, draft schemas, improve validators, run approved checks, and update documentation, but may not select source strategy, UI toolkit, benchmark claims, sandbox policy, profile behavior, backup ownership, readiness promotion, or release authority.

Impact:

The operating board now gives a clearer continuation path for agents and maintainers without changing any readiness status or approving execution of the proposed `TASK-*` queue.

## 2026-07-18 — Build readiness task intake snapshot

Question:

Can a maintainer understand the proposed `TASK-*` queue without opening the machine registry for every precondition and rejection condition?

Inputs:

- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Build readiness task queue registry](blueprint-v1/machine/build-readiness-task-queue.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json).

Method:

Added a human intake snapshot for `TASK-000001` through `TASK-000008`. The snapshot summarizes when each task may start, what would prove progress, what would reject the task, and what must not be claimed. The machine registry remains authoritative for exact owners, reviewers, allowed paths, prohibited paths, budgets, dependencies, rollback evidence, and expiration dates.

Decision:

Keep every queued task `proposed` and non-authorizing. The new snapshot improves handoff readability only; it does not approve execution, source-strategy adoption, broad M1 work, benchmark claims, toolkit selection, profile migration, or ownership promotion.

Impact:

The task queue can now be used as a human triage page before converting any item into an immutable owner-reviewed task manifest.

## 2026-07-18 — Pre-build readiness audit refresh

Question:

Can the repository-level pre-build audit still serve as a compact handoff after the newer source-strategy, task-queue, and no-claim benchmark evidence?

Inputs:

- [Pre-build Readiness Gap Audit - July 2026](research/pre-build-readiness-gap-audit-2026-07.md);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md).

Method:

Refreshed the audit from an older broad-controls summary into a current `PB-001` through `PB-020` status table. The audit now records contained M0 authorization, broad-implementation non-authorization, first continuation sequence, no-claim benchmark evidence, and the handoff rule that `pre-build-readiness.json` remains the source of truth.

Decision:

Keep `PB-GATE-0` limited to named contained tasks. Do not promote broad M1 expansion, developer preview, beta, stable, Servo/source-strategy implementation, or Chrome-class/performance/security/compatibility claims from documentation readiness alone.

Impact:

The research index and documentation index now describe the pre-build audit as the current contained-M0 readiness handoff rather than a historical gap list.

## 2026-07-18 — ADR-0009 option scorecard cleanup

Question:

Can the first source-strategy blocker be handed off without `TBD` option-scoring placeholders?

Inputs:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [ADR-0009 Decision Draft and Public-Claim Impact](project-buildout/16-adr-0009-decision-draft.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json).

Method:

Replaced the option scorecard placeholders with current evidence-bounded assessments for clean implementation informed by Servo, selective Servo components, upstream-first collaboration, Servo-derived engine, and explicit Servo-browser charter change. The scorecard now separates independence fit, schedule impact, security risk, performance evidence, compatibility evidence, maintenance cost, and required documentation changes without selecting an option.

Decision:

Keep `ADR-0009` unaccepted and `PB-002` blocked. The scorecard is handoff evidence only; owner-selected source baseline, owner-reviewed component boundaries, JavaScript-runtime conflict decision, compatibility/performance evidence, security implications, maintenance model, public-claim diffs, and owner approval remain required.

Impact:

The source-strategy packet no longer contains a placeholder decision table. The traceability matrix now references the scorecard as current partial evidence for `ADR9-EV-011`, not as a template.

## 2026-07-18 — Benchmark browser pin local diagnostic capture

Question:

Can the no-claim browser-pin runner capture Chrome and Edge browser-reported versions from isolated temporary profiles without reading or mutating real user profiles?

Inputs:

- [Benchmark Browser Pin Local Diagnostic Capture - July 2026](research/benchmark-browser-pin-local-diagnostic-capture-2026-07.md);
- [Benchmark browser-pin diagnostic schema](blueprint-v1/machine/benchmark-browser-pin-diagnostic.schema.json);
- [Current Windows high-end Chrome/Edge browser-pin diagnostic](blueprint-v1/machine/benchmark-browser-pin-diagnostics/current-windows-high-end.chrome-edge.no-claim.2026-07.json);
- [`tools/validate_benchmark_browser_pin_diagnostics.py`](../tools/validate_benchmark_browser_pin_diagnostics.py);
- [`tools/capture_benchmark_browser_pins.py`](../tools/capture_benchmark_browser_pins.py);
- [Benchmark Browser Pin Capture Contract - July 2026](research/benchmark-browser-pin-capture-contract-2026-07.md).

Method:

Ran `tools/capture_benchmark_browser_pins.py --capture-local --target chrome --target edge` with runner-owned temporary profiles, no sync, disabled background networking and component updates, loopback host resolution, `about:blank`, and DevTools version capture. The checked summary records hashes, cleanup status, unsupported behavior, and remaining evidence gaps while leaving raw current-host diagnostic artifacts outside source control.

Observations:

- Chrome reported `Chrome/150.0.7871.115` from `C:\Program Files\Google\Chrome\Application\chrome.exe`;
- Edge reported `Edg/151.0.4129.21` from `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`;
- both temporary profiles were deleted and prohibited configured-path checks reported no prohibited access;
- the runner exposed and fixed an Edge cleanup failure mode by recording unreadable profile files and stopping lingering browser processes tied to the runner-owned temp profile path;
- Edge channel/update-ring proof, effective settings, process-tree command-line audit, Firefox/Safari evidence, and benchmark artifacts remain missing.

Decision:

Treat `PB13-EV-005` and `PB13-EV-009` as partially strengthened by checked current-host Chrome/Edge diagnostic capture. Keep `PB-013` at `documented_no_runner` because the evidence is unreviewed, no-claim, current-host diagnostic output and not benchmark-ready pin or comparison evidence.

Impact:

Updated the performance readiness packet, Chrome-class runbook, browser-pin capture contract, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, documentation indexes, and repository validator to include browser-pin diagnostic evidence and preserve unsupported-claim boundaries.

Next question:

What owner-reviewed channel proof, effective settings, process-tree audit, and artifact-disposition record is required before the Chrome/Edge diagnostic capture can inform benchmark-ready local pins?

## 2026-07-18 — Benchmark browser pin capture contract and self-test runner

Question:

How should the future benchmark runner capture browser-reported versions, settings, and local pin evidence without reading or mutating the owner's real browser profiles, and how can the artifact path be self-tested before launching a real browser?

Inputs:

- [Benchmark Browser Pin Capture Contract - July 2026](research/benchmark-browser-pin-capture-contract-2026-07.md);
- [Benchmark browser-pin capture schema](blueprint-v1/machine/benchmark-browser-pin-capture.schema.json);
- [Current Windows high-end browser-pin capture plan](blueprint-v1/machine/benchmark-browser-pin-captures/current-windows-high-end.no-claim.plan.json);
- [`tools/validate_benchmark_browser_pin_capture.py`](../tools/validate_benchmark_browser_pin_capture.py);
- [`tools/capture_benchmark_browser_pins.py`](../tools/capture_benchmark_browser_pins.py);
- [Benchmark Competitor Local Install Inventory - July 2026](research/benchmark-competitor-local-install-inventory-2026-07.md).

Method:

Defined a no-claim capture plan that requires runner-owned temporary profiles, rejects real user profile paths, runs offline by default, prohibits account/sync attachment, separates capture-only arguments from benchmark workload arguments, and requires browser-reported version, effective command line, settings, update state, profile path, cleanup, and artifact hashes once real-browser capture runs. Added a dependency-free self-test runner that creates a runner-owned temporary profile marker, hashes the artifact package, deletes the profile by default, and launches no browser.

Observations:

- Chrome and Edge can become planned current-host capture targets because executable/hash evidence exists;
- `tools/capture_benchmark_browser_pins.py --self-test` validates temp-profile cleanup, prohibited configured-path checks, artifact hashes, and no-claim metadata without launching a browser;
- Firefox remains blocked until installed on an approved host;
- Safari Stable and Safari Technology Preview remain blocked until approved macOS host evidence and profile-isolation methods exist;
- the checked plan and self-test do not produce reviewed browser-reported versions or benchmark-ready pins.

Decision:

Treat `PB13-EV-005` and `PB13-EV-009` as partially strengthened by a checked browser-pin capture contract and no-browser artifact self-test. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, documentation indexes, and repository validator now include the browser-pin capture plan and no-browser self-test runner.

Next question:

What diagnostic capture evidence should be owner-reviewed before benchmark-ready local pins can be derived?

## 2026-07-18 — Benchmark competitor local install inventory

Question:

Which competitor browser executables are present on the current Windows high-end host, and what still prevents them from becoming benchmark-ready local pins?

Inputs:

- [Benchmark Competitor Local Install Inventory - July 2026](research/benchmark-competitor-local-install-inventory-2026-07.md);
- [Benchmark competitor local-install schema](blueprint-v1/machine/benchmark-competitor-local-install.schema.json);
- [Current Windows high-end competitor local installs](blueprint-v1/machine/benchmark-competitor-local-installs/current-windows-high-end.candidate.json);
- [`tools/validate_benchmark_competitor_local_installs.py`](../tools/validate_benchmark_competitor_local_installs.py);
- [Benchmark Competitor Version Manifest - July 2026](research/benchmark-competitor-version-manifest-2026-07.md).

Method:

Captured standard Windows executable, App Paths, selected BLBeacon, selected uninstall metadata, SHA-256 hashes, and Authenticode signer status for installed competitor browsers. The capture avoided user browser profiles, history, cookies, account state, extension data, cache directories, downloads, bookmarks, passwords, session state, crash reports, and browsing data.

Observations:

- Chrome and Edge executables were present in standard install paths and have captured SHA-256 hashes and valid Authenticode signatures;
- Chrome metadata is inconsistent across executable/product version, BLBeacon, uninstall metadata, and version directories;
- Edge executable and uninstall metadata report `151.0.4129.21`, which is newer than the recorded Edge Stable release catalog and therefore requires channel/update-ring resolution;
- Firefox was not found in the standard Windows paths checked;
- Safari Stable and Safari Technology Preview require macOS host evidence.

Decision:

Treat `PB13-EV-009` as partially strengthened by current-host executable/hash evidence for Chrome and Edge only. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, documentation indexes, and repository validator now include the competitor local-install registry.

Next question:

How should the browser-launch runner capture isolated browser-reported versions, channel proof, update state, profiles, command lines, settings, and raw artifacts without reading or mutating the owner's real browser profiles?

## 2026-07-18 — Benchmark competitor version manifest

Question:

Which official release catalogs should seed `PB13-EV-009` competitor-version records before any Chrome-class, fastest, lower-memory, lower-energy, or public performance claim can exist?

Inputs:

- [Benchmark Competitor Version Manifest - July 2026](research/benchmark-competitor-version-manifest-2026-07.md);
- [Benchmark competitor-version schema](blueprint-v1/machine/benchmark-competitor-version.schema.json);
- [Current desktop release-candidate competitor versions](blueprint-v1/machine/benchmark-competitor-versions/current-desktop-release-candidates.2026-07.json);
- [`tools/validate_benchmark_competitor_versions.py`](../tools/validate_benchmark_competitor_versions.py);
- [Chrome-Class Performance Runbook - July 2026](research/chrome-class-performance-runbook-2026-07.md).

Method:

Checked official browser release catalogs for Chrome Stable, Edge Stable, Firefox Stable, Safari Stable, and Safari Technology Preview on 2026-07-18. Added a no-claim release-catalog manifest, schema, and validator. Wired the registry into the `PB-013` readiness handoff, task queue, documentation indexes, repository map, benchmark-lab book, performance book, and repository validator.

Observations:

- the manifest records official release-catalog candidate versions only;
- every browser entry remains `benchmark_eligible: false`;
- no local executable path, executable hash, local profile, command line, settings, update state, raw artifacts, benchmark output, competitor result, ranking, or public claim exists;
- Safari stable metadata came from Apple Developer release-note catalog/search metadata and still needs local application version capture before benchmark use.

Decision:

Treat `PB13-EV-009` as partially strengthened by release-catalog candidate evidence only. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, project-buildout handoff, task queue, pre-build readiness registry, repository map, source bibliography, documentation indexes, and repository validator now include the competitor-version registry.

Next question:

Which fixed hardware and local installed-browser pin records should become the first benchmark-eligible competitor-version manifests?

## 2026-07-17 — Build readiness task queue

Question:

How should a future maintainer move from the current `PB-*` blocker list to executable work without inventing scope, weakening gates, or losing traceability?

Inputs:

- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- [Build Readiness Task Queue](project-buildout/17-build-readiness-task-queue.md);
- [Build readiness task queue registry](blueprint-v1/machine/build-readiness-task-queue.json);
- [Agent Execution and Autonomous Engineering](agent-execution/README.md);
- [Execution task schema](agent-execution/machine/execution-task.schema.json);
- [Pre-build readiness registry](blueprint-v1/machine/pre-build-readiness.json).

Method:

Added a proposed `TASK-*` queue that maps the current Servo/source-strategy, bootstrap reproduction, IPC, sandbox, benchmark, native UI, profile/session, and backup-ownership blockers to task-shaped handoff records. The queue records owners, independent reviewer scopes, requirements, risks, ADRs, allowed and prohibited paths, preconditions, acceptance criteria, negative tests, resource budgets, rollback evidence, and dependencies.

Observations:

- every queued task remains `proposed`, not approved or running;
- `TASK-000001` through `TASK-000008` cover the first continuation path from the operating board;
- the queue improves handoff from readiness records to task manifests, but it does not authorize execution, merge, release, source-strategy selection, or product claims;
- validation now requires the task queue to remain linked, ordered, dependency-consistent, and proposed-only.

Decision:

Treat the task queue as a documentation-control and handoff artifact. Keep broad implementation, source-strategy decisions, and public claims blocked until owner-reviewed task manifests and evidence exist.

Impact:

The documentation index, start-here guide, project-buildout handbook, operating board, repository map, pre-build readiness registry, Blueprint machine-companion summary, research log, and repository validator now include the build-readiness task queue.

Next question:

Which proposed task should be converted into the first owner-approved immutable task manifest?

## 2026-07-17 — Semantic resource attribution taxonomy

Question:

Which semantic owner taxonomy should Turing use before claiming memory, CPU, GPU, energy, wakeup, model, or 30-tab resource advantages over Chrome-class browsers?

Inputs:

- [Semantic Resource Attribution Taxonomy - July 2026](research/semantic-resource-attribution-taxonomy-2026-07.md);
- [Benchmark resource-attribution schema](blueprint-v1/machine/benchmark-resource-attribution.schema.json);
- [Semantic owner taxonomy](blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json);
- [`tools/validate_benchmark_resource_attribution.py`](../tools/validate_benchmark_resource_attribution.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Defined a checked taxonomy for semantic owners, required metrics, shared-resource charging policy, trace fields, collection-plan requirements, and UI/reporting disclosures. Wired the taxonomy into the no-claim benchmark manifest schema, sample manifest, smoke runner output, manifest validator, repository validator, and `PB-013` handoff documents.

Observations:

- the taxonomy ID is `TURING.BENCHMARK.RESOURCE_ATTRIBUTION.SEMANTIC_OWNERS.2026_07`;
- the checked owner classes cover browser UI/profile, documents/frames/site instances, JavaScript heap/code, DOM/style/layout/paint/accessibility, images/fonts/canvas/media, network/cache, storage, GPU, extensions, DevTools, agents, shared services, and unknown resources;
- the metrics include CPU time, queue wait, wakeups, private/resident/committed/shared/compressed/swap memory, GPU allocation, network bytes, disk I/O, energy estimate, model tokens, and provider cost estimate;
- `unknown` remains a first-class owner, and reports must distinguish physical totals from charged views.

Decision:

Treat `PB13-EV-011` as partial taxonomy evidence only. Keep `PB-013` at `documented_no_runner`.

Impact:

The performance readiness packet, research program, benchmark-lab book, performance book, project-buildout handoff, ADR-0009 performance evidence, no-claim benchmark manifest, smoke runner, manifest validator, and repository validator now include the resource-attribution registry. No browser trace instrumentation, per-tab measurements, GPU accounting output, UI fixture, benchmark result, competitor comparison, or public performance claim exists.

Next question:

What trace-event schema and UI/report fixture should turn the taxonomy into browser-run evidence without hiding unknown or shared resource cost?

## 2026-07-17 — Benchmark OS and update-control manifest

Question:

Which current Windows OS, update, driver, firmware, power, display, thermal, clock, service, and artifact-control facts can seed `PB13-EV-002`, and what still prevents the host from being decision-grade benchmark evidence?

Inputs:

- [Benchmark OS and Update-Control Manifest - July 2026](research/benchmark-os-update-control-manifest-2026-07.md);
- [Benchmark OS-control schema](blueprint-v1/machine/benchmark-os-control.schema.json);
- [Current Windows high-end OS-control candidate](blueprint-v1/machine/benchmark-os-controls/current-windows-high-end.candidate.json);
- [`tools/validate_benchmark_os_controls.py`](../tools/validate_benchmark_os_controls.py);
- [Benchmark Hardware and OS Manifest - July 2026](research/benchmark-hardware-os-manifest-2026-07.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Captured current-host facts from Windows Update policy registry keys, Windows Update UX settings, Windows Insider registry keys, Windows current-version registry keys, selected update-related services, CIM OS/GPU/BIOS/baseboard queries, `powercfg`, timezone state, and `w32tm /query /status`. Stored the result in a checked OS-control manifest, wired its validator into repository validation, and linked the no-claim benchmark manifest and smoke runner output to the current OS-control ID.

Observations:

- the host is Windows 11 Pro Insider Preview `10.0.26220`, display version `25H2`, UBR `8491`, on the Beta/External Insider channel;
- `DisableWindowsUpdateAccess=1`, `DisableOSUpgrade=1`, and `NoAutoUpdate=1` were observed, but target release version, quality update, driver exclusion, and preview-build approval policies are not benchmark-grade;
- `bits` and `usosvc` were running, `wuauserv` was stopped/manual, and `WaaSMedicSvc` returned a permission-denied note while reporting stopped/manual;
- Ultimate Performance is active with processor min/max AC at 100 percent, but the display is still 165 Hz and thermal state is unmeasured;
- `w32tm /query /status` failed because the time service was not started;
- the manifest deliberately excludes product IDs, SIDs, digital product IDs, and other owner/machine secrets.

Decision:

Treat `PB13-EV-002` as partially strengthened by checked current-host OS-control evidence. Keep `PB-013` at `documented_no_runner`.

Impact:

The pre-build readiness registry, performance readiness packet, research program, benchmark-lab book, performance book, documentation indexes, repository map, pre-build checklist, operating board, project-buildout handoff, benchmark manifest validator, smoke runner self-test, and repository validator now include the OS-control manifest. No clean image, approved update freeze, driver freeze, browser-run benchmark result, competitor comparison, or public performance claim exists.

Next question:

Should the current Tier H host be cleaned and approved, or should benchmark lab work move to a separate Tier H host plus Tier M and Tier L reference machines?

## 2026-07-17 — Benchmark hardware and OS manifest

Question:

Which current Windows host facts can seed the `PB-013` hardware registry, and what remains before the host can support decision-grade Chrome-class performance evidence?

Inputs:

- [Benchmark Hardware and OS Manifest - July 2026](research/benchmark-hardware-os-manifest-2026-07.md);
- [Benchmark hardware schema](blueprint-v1/machine/benchmark-hardware.schema.json);
- [Current Windows high-end candidate manifest](blueprint-v1/machine/benchmark-hardware/current-windows-high-end.candidate.json);
- [No-claim benchmark manifest sample](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [`tools/validate_benchmark_hardware.py`](../tools/validate_benchmark_hardware.py);
- [`tools/validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py);
- [`tools/run_benchmark_smoke.py`](../tools/run_benchmark_smoke.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [Chrome-Class Performance Runbook - July 2026](research/chrome-class-performance-runbook-2026-07.md).

Method:

Captured current-host facts from Windows CIM, Windows registry version keys, and `powercfg /getactivescheme`, then stored them in a checked benchmark hardware and OS manifest. Added the validator to the repository-wide validation path, wired the no-claim benchmark manifest sample to the current hardware registry entry, and made the smoke runner emit that hardware ID in its artifact package summary.

Observations:

- the available host is a high-end Windows desktop with AMD Ryzen 9 5950X, 64 GiB installed memory class, AMD Radeon RX 7900 XTX, Windows 11 Pro Insider Preview build 26220, and Ultimate Performance power scheme;
- the display is currently observed at 165 Hz, which is not normalized for MotionMark-class cross-browser comparison;
- the OS is not a clean lab image and update, driver, firmware, display, thermal, and artifact-storage controls are not frozen;
- the host is a Tier H candidate, not a Tier M denominator;
- the no-claim sample and smoke runner now carry the Tier H hardware ID for traceability, but they still do not launch a browser, measure performance, or create a result denominator.

Decision:

Treat `PB13-EV-001` and `PB13-EV-002` as partially strengthened by checked Tier H candidate hardware/OS evidence. Keep `PB-013` at `documented_no_runner`.

Impact:

The pre-build readiness registry, performance readiness packet, Chrome-class runbook, research program, benchmark-lab book, performance book, documentation indexes, repository map, pre-build checklist, operating board, project-buildout handoff, and repository validator now include the hardware manifest. Benchmark manifest validation also cross-checks the default no-claim sample against the hardware registry. No browser benchmark, competitor comparison, or public performance claim exists.

Next question:

Which Tier M and Tier L machines should be captured next, and should the current high-end host be cleaned and approved or replaced?

## 2026-07-17 — Chrome-class performance runbook and no-claim metadata

Question:

Which current primary sources, competitor controls, and claim-expiry rules should govern Turing's Chrome-class and extreme-performance measurement path before any runner or result exists?

Inputs:

- [Chrome-Class Performance Runbook - July 2026](research/chrome-class-performance-runbook-2026-07.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [Benchmark manifest schema](blueprint-v1/machine/benchmark-manifest.schema.json);
- [No-claim benchmark manifest sample](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [`tools/validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py);
- BrowserBench Speedometer, JetStream, and MotionMark sources;
- Chromium Telemetry, Chrome UX Report, Web Vitals, Chrome DevTools, WebPageTest agent, and Chrome Releases sources.

Method:

Checked current primary benchmark and Chrome measurement sources, then converted them into a four-level runbook covering harness smoke, local browser pipeline, competitor diagnostic comparison, and public claim candidate evidence. Added explicit optional `claim` metadata to the benchmark manifest schema and no-claim sample, with validator enforcement for the default sample.

Observations:

- BrowserBench suites are useful diagnostics but cannot establish broad product leadership alone;
- Chrome-class comparison requires exact browser versions, channels, release metadata, command lines, profiles, security settings, caches, lifecycle settings, hardware, OS image, raw artifacts, and denominator accounting;
- Web Vitals and CrUX inform user-experience metrics, but CrUX is Chrome field data for eligible public destinations and is not a Turing lab result;
- claim text needs owner, reviewer, scope, unsupported behavior, expiration, and rerun triggers before it can appear publicly.

Decision:

Treat the runbook as stronger `PB13-EV-009` and `PB13-EV-010` evidence. Keep `PB-013` at `documented_no_runner` because fixed hardware, expanded corpus, browser launch, runner-generated raw artifacts, actual competitor runs, and owner-reviewed claim bundles do not exist.

Impact:

The research index, documentation index, repository map, performance book, benchmark-lab book, research program, pre-build checklist, build-readiness board, pre-build readiness registry, benchmark schema, sample manifest, and benchmark manifest validator now distinguish no-claim harness evidence from actual Chrome-class performance evidence.

Next question:

Which Tier M Windows hardware and OS image manifest should become the first Level 1 local browser pipeline target?

## 2026-07-17 — ADR-0009 public-claim and support-impact draft

Question:

What public-claim, support-language, requirement, risk, and registry impact would each `ADR-0009` source-strategy option require before owner review?

Inputs:

- [ADR-0009 Decision Draft and Public-Claim Impact](project-buildout/16-adr-0009-decision-draft.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [Start here](start-here.md);
- [Definition of done](blueprint-v1/20-definition-of-done.md).

Method:

Converted the existing source-strategy options into a non-decision template that names allowed claims, unsupported behavior, required document and registry updates, residual risks, and support-language baselines for each outcome.

Observations:

- no `ADR-0009` option is selected;
- Turing still cannot claim Servo adoption, Servo-derived release code, Chrome-class compatibility, production-safe browsing, security posture, memory leadership, speed leadership, or support commitments;
- each option requires different changes to the charter, requirements, risks, detailed engineering books, machine registries, support statements, dependency/provenance records, and work packages;
- final public wording depends on an owner-selected option and cannot be completed by an implementation agent alone.

Decision:

Move `ADR9-EV-017` from missing to partial. Keep `ADR9-EV-018` blocked and keep `PB-002` blocked.

Impact:

The buildout handbook, documentation index, repository map, start-here page, research program, operating board, evidence matrix, and readiness registries now include the decision draft as public-claim/support-impact evidence. No source strategy, public claim, support statement, or release path changed.

Next question:

Which owner-selected `ADR-0009` outcome, if any, should be accepted, rejected, superseded, or time-boxed?

## 2026-07-17 — Servo security and maintenance implications

Question:

What security/sandbox implications and upstream-maintenance signals exist before `ADR-0009` can accept, reject, or supersede a Servo relationship?

Inputs:

- [Servo Security and Maintenance Implications - July 2026](research/servo-security-maintenance-implications-2026-07.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [Security policy](security.md);
- [Security engineering book](security-engine/README.md).

Method:

Inspected Servo sandbox, multiprocess, event-loop, process-manager, option, feature, release, security-policy, CODEOWNERS, Dependabot, and workflow surfaces from the clean external checkout at `C:\ts\servo`, plus current `gh repo view` and release-list metadata for `servo/servo`.

Observations:

- Servo defaults are single-process and unsandboxed unless multiprocess/sandbox options are configured;
- the inspected Windows content-process sandbox path is unsupported, and the Windows multiprocess path spawns an unsandboxed child process;
- macOS/Linux-like `gaol` profiles exist but have no Turing effective-policy evidence or negative sandbox tests;
- event-loop routing, public/private resource/storage threads, and selected origin checks exist as security-relevant implementation concepts but need identity-preservation tests;
- script initial state carries many authority-bearing senders that need an owner-reviewed capability map;
- upstream `servo/servo` is public, not archived, security-policy-enabled, recently pushed/updated, and has release, CODEOWNERS, Dependabot, workflow, nightly, attestation, and crates.io publishing signals;
- those upstream signals do not satisfy Turing's own support, security-response, signing, update, or backup-owner obligations.

Decision:

Move `ADR9-EV-015` and `ADR9-EV-016` from missing to partial. Keep `PB-002` blocked. Treat the report as evidence preparation only, not security approval or an upstream maintenance commitment.

Impact:

The source-strategy packet, evidence matrix, machine registry, build-readiness board, research indexes, repository map, security policy, security book, research program, and pre-build checklist now separate observed Servo security/maintenance surfaces from owner-reviewed Turing acceptance. No source strategy, release-code authorization, security claim, or support statement changed.

Next question:

What exact public-claim, requirement, risk, support-language, and registry diff would each `ADR-0009` option require before an owner can review a decision draft?

## 2026-07-17 — Servo performance baseline preparation

Question:

What fixed-host, artifact, command-surface, fixture, and run-record evidence exists before `ADR-0009` can use Servo performance or memory data?

Inputs:

- [Servo Performance Baseline Preparation - July 2026](research/servo-performance-baseline-2026-07.md);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json).

Method:

Inspected the clean external Servo checkout at `C:\ts\servo`, the current debug `servoshell.exe` artifact identity, host hardware and OS facts from Windows CIM, Servo performance command surfaces, page-load harness files, TP5-style manifest state, and benchmark-adjacent fixture directories. No browser benchmark was executed.

Observations:

- the external checkout remained clean at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- the named Windows reference host and debug Servo artifact are now recorded for performance-prep traceability;
- Servo exposes page-load, Dromaeo, Speedometer, jQuery, and macOS power-measurement surfaces, but the page-load path is not a Turing fixed-hardware no-claim runner;
- Servo's current performance path can involve external downloads, WARC infrastructure, Python package installation, and Perfherder submission, so it must be adapted or replaced before Turing can use it as decision-grade evidence;
- no raw timing, memory, frame pacing, process, lifecycle, energy, competitor, or BrowserBench result exists.

Decision:

Move `ADR9-EV-014` from missing to partial. Keep `PB-002` blocked and keep `PB-013` at no-claim readiness status. Treat the new report as runbook and evidence-prep material only.

Impact:

The `ADR-0009` packet, evidence matrix, machine registry, build-readiness board, research indexes, repository map, performance book, benchmark-lab book, and pre-build checklist now distinguish performance preparation from performance measurement. No source strategy, dependency approval, component approval, compatibility claim, performance claim, or release-code authorization changed.

Next question:

Which browser-launch no-claim runner should execute the selected Servo source baseline against a Turing-owned local corpus and emit raw traces, memory snapshots, process topology, lifecycle state, failure denominator, and artifact hashes?

## 2026-07-17 — ADR-0009 machine evidence registry

Question:

How can the blocked `PB-002` source-strategy work stay coherent across many Servo evidence reports without relying only on prose tables?

Inputs:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](blueprint-v1/machine/adr-0009-evidence.json);
- [`tools/validate_blueprint.py`](../tools/validate_blueprint.py).

Method:

Added a machine-readable `ADR9-EV-001` through `ADR9-EV-018` registry and JSON schema for the `ADR-0009` source-strategy decision. The registry records decision area, status, owner scopes, existing evidence, missing outputs, blocked dependencies, and next action for each evidence item. Added `tools/validate_adr_0009_evidence.py` and wired it into `tools/validate_blueprint.py` so the IDs, owner scopes, existing evidence paths, matrix synchronization, unresolved-output fields, claim boundaries, and `PB-002` blocked status are checked.

Observations at registry creation time:

- `ADR9-EV-001` through `ADR9-EV-010` have partial evidence but no owner-reviewed decision-grade completion;
- `ADR9-EV-011` through `ADR9-EV-017` were missing at registry creation time;
- `ADR9-EV-018` remains blocked by the unresolved evidence set;
- no Servo source strategy, source baseline, dependency approval, component approval, compatibility claim, performance claim, or release-code authorization exists.

Decision:

Treat the registry as the executable status companion for the prose matrix. Any future evidence-status move must update the registry and matrix together. `PB-002` remains blocked until `ADR-0009` evidence is owner-reviewed and the source-strategy decision is accepted, rejected, or superseded.

Impact:

Continuing agents now have a machine-checked queue for the first broad-build blocker. The registry improves handoff coherence but does not move Turing closer to a release-path Servo dependency by itself.

Next question:

Which `ADR9-EV-001` source-baseline option should be prepared for owner selection, and what exact provenance/equivalence policy would make later evidence reusable?

## 2026-07-17 — Benchmark smoke runner artifact package

Question:

Which runner command should capture the static-server self-test artifact, own a first artifact-package shape, and label unsupported browser behavior without hiding failures?

Inputs:

- [`tools/run_benchmark_smoke.py`](../tools/run_benchmark_smoke.py);
- [`tools/serve_benchmark_profile.py`](../tools/serve_benchmark_profile.py);
- [no-claim benchmark manifest sample](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added `tools/run_benchmark_smoke.py` with a `--self-test` mode that invokes the static-server self-test, writes `profile-self-test.json`, `runner-summary.json`, and `artifact-index.json` into a temporary artifact package, verifies file hashes, and emits a no-claim JSON summary. The command also accepts `--output-dir` for a persisted package during manual runner development. Wired the smoke runner into `validate_blueprint.py`.

Observations:

- the repository can now prove a minimal runner-owned artifact package shape without launching a browser;
- the artifact package records the static-server self-test, runner summary, artifact index, file byte counts, SHA-256 hashes, and unsupported behavior;
- no browser process, Turing page load, competitor page load, timing sample, memory sample, energy sample, accessibility sample, compatibility result, benchmark result, or performance claim exists.

Decision:

Treat `PB13-EV-005` as partial, not ready. The no-claim smoke runner is a command-contract seed only. `PB-013` remains `documented_no_runner` until fixed hardware, expanded corpus, runner-managed server artifacts, browser-launch runner behavior, runner-generated raw benchmark output, traces, non-sample artifact packages, competitor runbooks, and claim-expiry records exist.

Impact:

Future benchmark-runner work has a concrete artifact-package handoff and validation hook. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, compatibility, accessibility, battery, memory, regression, or production claims.

Next question:

Which browser-launch runner interface should add timeout, cancellation, cache reset, viewport, failure capture, and unsupported-case recording while preserving this no-claim artifact package?

## 2026-07-17 — Benchmark static-server self-test command

Question:

What is the smallest repository-owned static-server command that can serve the no-claim network profile, record its bound port and DNS override behavior, and still avoid benchmark or browser claims?

Inputs:

- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- [`tools/serve_benchmark_profile.py`](../tools/serve_benchmark_profile.py);
- [`tools/validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added `tools/serve_benchmark_profile.py` with a `--self-test` mode that validates the profile, starts an ephemeral loopback HTTP/1.1 static server, requests each configured route with a `turing.invalid:{port}` Host header, verifies status, content type, `Cache-Control: no-store`, bytes, and SHA-256, then emits a no-claim JSON artifact. The command also has a `--serve` mode that prints a startup artifact and serves the same profile for manual runner development. Wired the self-test into `validate_blueprint.py` and updated the network profile status to `self_test_only_no_benchmark_result`.

Observations:

- both seeded corpus cases can be served through the profile over `127.0.0.1` with a runner-assigned ephemeral port;
- the DNS behavior is recorded as Host-header self-test behavior only and does not modify the operating-system resolver;
- no browser run, benchmark result, latency result, cache result, TLS result, external DNS result, performance result, or competitor comparison exists.

Decision:

Treat `PB13-EV-004` as partially evidenced by the network-profile schema, no-claim profile, route-to-corpus mapping, validator, and static-server self-test command. Keep `PB-013` at `documented_no_runner` until fixed hardware, an expanded reviewed corpus, runner-managed server artifacts, runner-generated output, and non-sample raw-artifact validation exist.

Impact:

The benchmark lane can now prove the profile is executable without creating performance claims. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, compatibility, TLS, HTTP/2, HTTP/3, network-stack, or production claims.

Next question:

Which runner command should capture this self-test artifact, own server start/stop lifecycle, attach raw artifacts, and label unsupported browser behavior without hiding failures?

## 2026-07-17 — Benchmark local network-profile contract

Question:

What can make the `PB-013` local-server and network-profile requirement concrete before a server command, benchmark runner, fixed hardware, or performance result exists?

Inputs:

- [Benchmark network profile schema](blueprint-v1/machine/benchmark-network-profile.schema.json);
- [no-claim local static network profile](blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- [no-claim sample benchmark manifest](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [`tools/validate_benchmark_network_profile.py`](../tools/validate_benchmark_network_profile.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added a network-profile schema and a no-claim profile for serving the seeded corpus from the then-future loopback HTTP/1.1 static server path. The profile records `turing.invalid` DNS override requirements, route-to-corpus mapping, cold cache state, no-store response headers, disabled external network, disabled authentication, loopback transport, and explicit unsupported cases. Added a validator that checks loopback-only serving, route coverage against the corpus manifest, corpus entry-path agreement, DNS policy, cache headers, disabled HTTP/2/HTTP/3/TLS/authentication flags, unsupported-case declarations, and no benchmark-run claims. Wired the validator into `validate_blueprint.py`.

Observations:

- the repository had a concrete local serving contract for the then-current two no-claim corpus cases;
- the no-claim sample benchmark manifest points to `TURING.NETWORK.NOCLAIM_LOCAL_STATIC.2026_07`;
- at this earlier stage, the repository still lacked a server process, DNS override execution, TLS certificate profile, HTTP/2 or HTTP/3 profile, proxy profile, authentication mock, latency/loss/bandwidth shaping, browser run, or benchmark result.

Decision:

Treat `PB13-EV-004` as partially evidenced by the network-profile schema, no-claim local static profile, route-to-corpus mapping, and validator. Keep `PB-013` at `documented_no_runner` until runner-managed server evidence, runner-generated output, and non-sample artifact package exist.

Impact:

The benchmark lane now has an enforceable network-profile contract before implementation. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, compatibility, TLS, network-stack, or production claims.

Next question:

What is the smallest repository-owned static-server command that can serve this profile, record its bound port and DNS override behavior, and produce a no-claim runner smoke artifact?

## 2026-07-17 — Benchmark corpus seed and validator

Question:

What can make the `PB-013` offline-corpus requirement concrete before a fixed hardware lab, local server, benchmark runner, or performance result exists?

Inputs:

- [Benchmark corpus schema](blueprint-v1/machine/benchmark-corpus.schema.json);
- [no-claim smoke corpus manifest](blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json);
- generated static-document fixture under `benchmarks/corpus/no-claim-smoke/static-document/`;
- generated app-like fixture under `benchmarks/corpus/no-claim-smoke/app-like/`;
- [`tools/validate_benchmark_corpus.py`](../tools/validate_benchmark_corpus.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added the initial two local generated HTML fixtures and a machine-readable corpus manifest that records case IDs, categories, entry paths, `turing.invalid` origins, SHA-256 hashes, byte counts, generated-content license notes, expected M0 unsupported behavior, and no-claim status. Added a validator that checks unique case IDs, required categories, local fixture paths, fixture byte counts, SHA-256 hashes, LF line endings, no external network URL references, and no measurement-claim flags. Wired the validator into `validate_blueprint.py`.

Observations:

- the repository gained the initial concrete two-case corpus seed for the first no-claim runner smoke contract;
- the seed covers one static-document case and one app-like JavaScript interaction case;
- fixture bytes and hashes are checked, so local corpus drift fails validation;
- no local server, DNS/TLS profile, browser run, trace, sample statistics, competitor baseline, or performance claim exists.

Decision:

Treat `PB13-EV-003` as partially evidenced by the schema, no-claim corpus manifest, the initial generated local fixtures, and corpus validator. Keep `PB-013` at `documented_no_runner` until a reviewed representative corpus, fixed hardware, runner-generated results, and artifact package exist.

Impact:

Benchmark readiness now has enforceable corpus identity before the runner exists. The seed is not representative enough for compatibility, low-memory, fastest, Chrome-class, daily-driver, or production claims.

Next question:

Which local server, cache, DNS/TLS, and network profile should serve the no-claim corpus cases for the first runner smoke task?

## 2026-07-17 — Benchmark manifest sample and validator

Question:

What evidence can make the `PB-013` raw-result schema requirement concrete before a benchmark runner, fixed hardware, or corpus exists?

Inputs:

- [Benchmark manifest schema](blueprint-v1/machine/benchmark-manifest.schema.json);
- [no-claim sample manifest](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json);
- [raw-artifact index fixture](blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.raw-artifacts.json);
- [`tools/validate_benchmark_manifests.py`](../tools/validate_benchmark_manifests.py);
- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md).

Method:

Added a sample manifest that exercises the current benchmark-manifest fields without claiming a benchmark result. Added a raw-artifact index fixture and a validator command that checks required fields, rejects unsupported fields, compares lifecycle state counts to tabs, validates SHA-256 format, and verifies the checked raw-artifact hash for the default fixture. Wired the validator into `validate_blueprint.py` so CI and local repository validation enforce the fixture.

Observations:

- the manifest schema now has an executable no-claim fixture;
- the raw-artifact hash path is checked against a committed file, so fixture drift fails validation;
- the sample deliberately records unsupported M0 web-rendering behavior and the note "harness smoke evidence only";
- no hardware, corpus, runner-generated raw result, trace, statistics, competitor baseline, or performance claim was created.

Decision:

Treat `PB13-EV-006` as partially evidenced by the sample manifest, raw-artifact index, direct validator command, and repository validation hook. Keep `PB-013` at `documented_no_runner` until runner-generated results and non-sample artifact packages exist.

Impact:

The benchmark evidence lane is more concrete and harder to drift. It still cannot support Chrome-class, fastest, lower-memory, daily-driver, or production claims.

Next question:

Which Tier M host and first two local corpus cases should generate the first real no-claim runner output using this manifest contract?

## 2026-07-17 — Performance benchmark readiness packet

Question:

What must exist before Turing can treat performance measurement as build-ready, compare against Chrome-class browsers, or support an extreme-performance claim?

Inputs:

- [Performance Benchmark Readiness Packet - July 2026](research/performance-benchmark-readiness-packet-2026-07.md);
- [Performance, Memory, Energy, and the 30-Tab Contract](blueprint-v1/09-performance-memory.md);
- [Fixed-Hardware Benchmark Laboratory](benchmark-lab/README.md);
- [Browser Performance Engineering](performance/README.md);
- [benchmark manifest schema](blueprint-v1/machine/benchmark-manifest.schema.json);
- official BrowserBench and Microsoft Windows Performance Toolkit pages checked on 2026-07-17.

Method:

Reviewed current performance and benchmark documentation, machine readiness state for `PB-013`, the existing benchmark manifest schema, BrowserBench's current benchmark entry points, and Microsoft WPR/WPA documentation. Converted the broad "fixed hardware, offline corpus, raw result schema" blocker into a `PB13-EV-*` evidence matrix. No benchmark was run and no performance result was created.

Observations:

- the performance Blueprint, benchmark-lab book, and benchmark manifest schema already define measurement discipline, but they do not provide a fixed host, corpus, runner, raw artifact store, or competitor baseline;
- BrowserBench currently exposes Speedometer 3.1, JetStream 3.0, and MotionMark from the generic MotionMark page, which means every benchmark run must pin the exact suite URL and version;
- Windows WPR/WPA are suitable first Windows trace-capture inputs, but they do not solve cross-platform tracing or product claim governance by themselves;
- `PB-013` needed more precise missing evidence: fixed hardware inventory, OS image/update control, offline corpus, local server/network profile, runner command, raw samples, trace package, 30-tab manifests, competitor runbooks, and claim-expiry policy.

Decision:

- add the performance benchmark readiness packet;
- add it to the documentation index, research index, performance book, benchmark-lab book, repository map, project-buildout handoff, build-readiness board, and `pre-build-readiness.json`;
- update benchmark source references to include JetStream 3.0, the current MotionMark entry point, and Windows WPR/WPA documentation;
- keep `PB-013` at `documented_no_runner`.

Impact:

The project now has a concrete performance-readiness queue aligned with the Chrome-class and extreme-performance destination. No benchmark runner exists yet, no competitor comparison exists, and no speed, memory, energy, Chrome-class, daily-driver, accessibility, security, or production claim changed.

Next question:

Which Tier M reference host, OS image, first two local corpus cases, result fixture, and WPR/WPA trace artifact layout should seed the first no-claim benchmark runner smoke test?

## 2026-07-17 — Documentation orientation and audit-status refresh

Question:

Which top-level orientation documents still described earlier documentation snapshots as current state, and what should a maintainer read before continuing build-prep work?

Inputs:

- [Start Here](start-here.md);
- [Documentation index](README.md);
- [Research index](research/README.md);
- [Blueprint index](blueprint-v1/README.md);
- [Documentation Expansion Audit - July 2026](research/documentation-expansion-audit-2026-07.md);
- [Performance, Security, Developer, and Missing-Systems Expansion Audit - July 2026](research/performance-security-developer-expansion-audit-2026-07.md);
- current [Pre-build Readiness Checklist](project-buildout/11-pre-build-readiness-checklist.md), [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md), and `pre-build-readiness.json`.

Method:

Scanned orientation and audit documents for stale book counts, old expansion queues, readiness language, and missing handoff links. Updated current-state documents to point maintainers to the readiness board and `ADR-0009` packet before implementation. Preserved older research reports as historical snapshots instead of rewriting their original findings.

Observations:

- `start-here.md` still described the repository as having nineteen detailed books and did not put the readiness board in the primary reading order;
- the first documentation expansion audit still described later networking, storage, media, platform, accessibility, release, extension, web-governance, and benchmark books as a future queue even though those books now exist;
- the second expansion audit described the nineteen-book state as current, while the current documentation index lists twenty-seven detailed books;
- the authoritative build-start controls are now the pre-build checklist, build-readiness board, machine readiness registry, and `ADR-0009` source-strategy packet.

Decision:

- update current orientation to say the repository has twenty-seven detailed engineering, product, operating, and competitive books;
- add the pre-build checklist and build-readiness board to the primary reading order;
- add an explicit current build-readiness section stating that only contained M0 implementation is authorized;
- mark the earlier expansion audits as historical snapshots and route current continuation through the readiness controls;
- keep all implementation, requirement, risk, work-package, source-policy, and support statuses unchanged.

Impact:

Documentation handoff is clearer for a maintainer or agent resuming work. No implementation status changed, no Chrome-class or performance claim was promoted, and broad implementation remains blocked by the readiness gates.

Next question:

Which current readiness item should be converted into the next evidence packet: the native UI reference-shell comparison, packaged sandbox probes, fixed-hardware benchmark laboratory, or profile/session schema work?

## 2026-07-17 — Servo build-script and proc-macro side-effect audit

Question:

Which Servo registry, git, and path build scripts and proc macros need side-effect review before `ADR-0009` can trust any candidate component boundary?

Inputs:

- [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](research/servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- default Cargo metadata with `1069` packages and all-features metadata with `1120` packages;
- local registry, Stylo git, and Servo path source roots referenced by Cargo metadata.

Method:

Parsed Cargo metadata outside Turing, classified build-script and proc-macro packages by source kind, compared default and all-features metadata, and ran static marker scans over locally available build-script files and proc-macro source roots. Marker classes covered process execution, filesystem writes and `OUT_DIR`, URL/download/fetch strings, environment and Cargo cfg variables, compiler/linker/tool names, time/git inputs, and native-copy/package strings. No Servo source, metadata file, generated output, build log, proc-macro expansion, registry archive, or native artifact was copied into Turing.

Observations:

- default metadata exposed `157` build-script packages, `70` proc-macro packages, and `25` native-link packages;
- all-features metadata exposed `167` build-script packages, `71` proc-macro packages, and `26` native-link packages;
- default build-script packages were `144` registry, `9` path, and `4` git packages;
- default proc-macro packages were `62` registry, `6` path, and `2` git packages;
- all-features metadata added `10` build-script packages, `prost-derive`, and `libdbus-sys` as a native-link package;
- build-script marker triage found `3492` environment/cfg markers, `816` compiler/linker markers, `631` native-copy/package markers, `410` filesystem/write markers, `267` URL/download/fetch markers, `116` process markers, and `18` time/git markers;
- proc-macro source roots covered `744` Rust files and `5331698` bytes, with registry proc macros dominating marker volume.

Inference:

The `ADR9-EV-008` blocker is now a concrete review queue instead of a broad "registry/git build-script" gap. The evidence is still static triage only. Turing still needs owner-selected baseline/profile/component boundary, accepted side-effect policy, dynamic tracing, proc-macro expansion review, generated-output provenance, clean-target regeneration, independent replay, and owner approval.

Changes:

- add the [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](research/servo-build-script-proc-macro-side-effect-audit-2026-07.md);
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, generated/native/unsafe/FFI classification, build-script/generated-output audit, repository map, project-buildout index, and this log;
- keep `PB-002` blocked and keep `ADR9-EV-008` partial.

Security, privacy, provenance, and release impact:

No build script, proc macro, generated output, native package, dependency, or source baseline was approved. The report improves release safety by requiring deny-by-default network policy, environment allowlists, output-directory bounds, compiler/linker/native-copy tracing, proc-macro expansion review, and owner approval before build-time code can be trusted.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. Build-time code and proc-macro review remain prerequisites for selecting a component boundary, not evidence that any web-platform feature works.

Performance and resource impact:

No performance claim changed. Marker counts and proc-macro source size are build/review-cost inputs, not runtime memory, startup, interaction, energy, or Chrome-class evidence.

Licensing and operational impact:

No license status changed. Build-script outputs, proc-macro expansions, generated files, native-copy behavior, registry crates, Stylo git packages, and path packages still need source-to-output provenance, notices, advisory handling, and package-manifest linkage.

Next question:

Which owner-selected Servo baseline, feature profile, target, build profile, and candidate component boundary should dynamic side-effect tracing and proc-macro expansion review use?

## 2026-07-17 — Servo native package decision prep

Question:

What native source-build, binary-package exception, deterministic-download verification, package-minimization, notice, and manifest decisions remain before `ADR-0009` can select any Servo relationship that reaches Servo's Windows bootstrap or media package surface?

Inputs:

- [Servo Native Package Decision Prep - July 2026](research/servo-native-package-decision-prep-2026-07.md);
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](research/servo-native-bootstrap-provenance-audit-2026-07.md);
- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- `servo/servo-build-deps` release metadata for tag `msvc-deps`;
- local native asset hashes and signature checks under `C:\ts\servo-native-artifacts-msvc-deps`;
- bounded extracted dependency, license-root, plugin-list, and debug-output counts under `C:\ts\servo`.

Method:

Captured bounded local facts without importing Servo source, native packages, generated output, build logs, downloaded archives, or MSI files into Turing. Rechecked `servo-build-deps` release metadata through GitHub CLI, summarized local asset hashes and Authenticode posture, counted extracted package roots and signature states, parsed GStreamer plugin-list and Windows copy-candidate counts from source files, and converted the prior native provenance audit into source-build, binary-package exception, deterministic-download, and package-manifest decision queues.

Observations:

- the external checkout is still a shallow build-baseline snapshot and is `2` commits behind `origin/main`;
- `servo-build-deps` release metadata for the three relevant assets still exposed `digest: null`;
- local hashes exist for `moztools-4.0.zip` and the two GStreamer MSVC `1.22.8` MSI assets, but the GStreamer MSIs were not Authenticode-signed;
- extracted dependencies contained `4630` files under `gstreamer`, `14824` files under `moztools`, and two smaller extracted-tree GStreamer MSI artifacts;
- extracted `.dll`, `.exe`, and `.msi` signature checks found `981` unsigned files and one valid signed `vswhere.exe`;
- GStreamer packaging source names `86` Windows GStreamer copy candidates before transitive dependency and package availability checks;
- debug output contained `146` DLLs, `208` EXEs, and `263` PDBs, proving a final package manifest cannot be implicit.

Inference:

The native package blocker is now split into explicit package-family decisions. `ADR9-EV-005` needs source-build recipes or binary-package exception records, package-minimization decisions, legal/advisory/notice review, final manifests, and owner approvals. `ADR9-EV-006` needs accepted hash/signature/mirror policy, implementation, and independent replay evidence.

Changes:

- add the [Servo Native Package Decision Prep - July 2026](research/servo-native-package-decision-prep-2026-07.md);
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, native bootstrap audit, repository map, project-buildout index, and this log;
- keep `PB-002` blocked and keep `ADR9-EV-005` and `ADR9-EV-006` partial.

Security, privacy, provenance, and release impact:

No native package was approved. The decision-prep report improves release safety by requiring fail-closed download verification, source-build or binary-package exception records, signature/hash/mirror policy, native advisory review, and final package manifests before any Servo-native surface can affect release code.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. Media and platform package decisions remain prerequisites for later compatibility and accessibility testing, not evidence that those tests pass.

Performance and resource impact:

No performance claim changed. File counts, copied package candidates, and debug-output size are release-footprint inputs, not runtime speed, memory, energy, or Chrome-class evidence.

Licensing and operational impact:

No license status changed. GStreamer, moztools, MSYS2-derived tools, codec libraries, crypto libraries, ANGLE outputs, platform redistributables, notices, source-offer obligations, package minimization, and SBOM component records remain owner-review items.

Next question:

Which owner-selected Servo baseline and feature profile should the native package manifest, source-build recipes, binary-package exception records, deterministic-download implementation, and independent replay use?

## 2026-07-17 — Servo license advisory and SBOM decision prep

Question:

What Turing-specific license, advisory, duplicate-version, native-notice, and SBOM decisions remain before `ADR-0009` can select any Servo relationship?

Inputs:

- [Servo License Advisory and SBOM Decision Prep - July 2026](research/servo-license-advisory-decision-prep-2026-07.md);
- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- Servo `Cargo.lock`, `deny.toml`, `about.toml`, default and all-features Cargo metadata, and rerun `cargo-deny` logs outside the Turing repository;
- bounded native GStreamer license-directory counts from the extracted Windows dependency tree.

Method:

Reran bounded evidence extraction against the external checkout and local metadata. Parsed Cargo metadata for package, source, license-expression, missing-license, git-source, and duplicate-version counts. Read Servo's `deny.toml` advisory comments and license allow-list. Checked the rerun `cargo-deny` log summaries and hashes. Counted the native GStreamer license directory without copying native files, logs, metadata, generated output, or Servo source into Turing.

Observations:

- the external checkout is still a shallow build-baseline snapshot and is `2` commits behind `origin/main`;
- the default metadata has `1069` packages, `48` unique license expressions, `0` packages missing both `license` and `license_file`, and `58` duplicate package names;
- the all-features metadata has `1120` packages, `50` unique license expressions, `0` packages missing both `license` and `license_file`, and `69` duplicate package names;
- the rerun `cargo-deny` logs exited clean under Servo policy for default and all-features metadata, but Servo's policy ignores `12` RustSec advisories;
- the observed GStreamer license directory has `69` package directories, `155` files, and `1141093` bytes of license material;
- no complete Turing SBOM was generated and no Turing SBOM toolchain was selected.

Inference:

The license/advisory gap is no longer unshaped. It is now a specific queue: select baseline and feature profile, select SBOM tooling, generate a complete SBOM, normalize license expressions, decide notices/source-offer obligations, decide duplicate-version policy, accept or reject advisory exceptions, and review native license/notice/source-build obligations.

Changes:

- add the [Servo License Advisory and SBOM Decision Prep - July 2026](research/servo-license-advisory-decision-prep-2026-07.md);
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, dependency inventory, supply-chain scan, repository map, project-buildout index, and this log;
- keep `PB-002` blocked, keep `ADR9-EV-003` partial, and move `ADR9-EV-004` from missing to partial.

Security, privacy, provenance, and release impact:

No dependency, advisory exception, native package, generated output, or source baseline was approved. The report reduces release risk by making unaccepted RustSec ignores, duplicate versions, native license material, and SBOM gaps explicit before any implementation relies on Servo.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. The evidence is supply-chain and legal-readiness input only.

Performance and resource impact:

No performance claim changed. Duplicate-version and native-package counts are resource-risk inputs, not runtime measurements.

Licensing and operational impact:

No license status changed. Legal approval, accepted license list, third-party notices, source-offer handling, codec and patent review, native package notices, generated-output provenance, advisory exceptions, and SBOM generation remain required.

Next question:

Which owner-selected Servo baseline and feature profile should the SBOM, license matrix, advisory exception records, duplicate-version policy, and native package decision prep use?

## 2026-07-17 — Servo build replay protocol draft

Question:

What exact runbook should an owner review before attempting the independent clean-target Servo build replay required by `ADR9-EV-002`?

Inputs:

- [Servo Build Reproduction Evidence and Gap Report - July 2026](research/servo-independent-build-reproduction-2026-07.md);
- current `ADR9-EV-002` evidence matrix row;
- same-host Visual Studio, LLVM, Python, Rust, `uv`, log, artifact, target, and cache observations.

Method:

Extended the existing `ADR9-EV-002` report instead of creating a competing document. Added explicit protocol tiers, required variables, path/deletion guard, host/toolchain capture commands, source checkout and identity checks, bootstrap/build log capture, evidence-bundle requirements, and success criteria. No command was executed and no Servo source, generated output, native binary, registry archive, downloaded package, build log, or build artifact was copied into Turing.

Observations:

- the previous report had enough evidence for same-host handoff but only a minimal command sketch;
- `ADR9-EV-002` needs an owner-accepted protocol or script before the independent clean-target run can be evaluated consistently;
- the protocol must reject Turing-internal paths, avoid blind `vswhere -latest` selection, record cache modes, capture failures, and distinguish same-host replay from decision-grade independent replay.

Inference:

The build-reproduction gap is now narrower: the missing work is no longer "what should the replay capture" but owner acceptance and an actual independent clean-target run using the documented protocol.

Changes:

- expand the build reproduction report with a replay-protocol draft;
- update the ADR-0009 packet, evidence matrix, readiness registry, research index, documentation index, build-readiness board, pre-build checklist, Servo source inventory, and this log to name the protocol draft;
- keep `PB-002` blocked and `ADR9-EV-002` partial.

Security, privacy, provenance, and release impact:

No source approval changed. The protocol improves deletion safety and evidence capture by requiring path resolution, external workspace checks, target/cache mode disclosure, and failure logs before any independent replay can be treated as evidence.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. The protocol only builds Servo; it does not run WPT, Test262, accessibility tests, a local corpus, or browser UI workflows.

Performance and resource impact:

No performance claim changed. The protocol records build and cache footprint evidence only; browser runtime measurements remain separate `ADR9-EV-014` work.

Next question:

Can release-operations and quality owners accept this replay protocol, then run it from a clean target on an independent Windows host or clean VM and preserve the required success/failure evidence bundle?

## 2026-07-17 — Servo build reproduction evidence and gap report

Question:

Can the successful external Servo Windows bootstrap and development build be handed off with enough environment, log, artifact, cache, and failure detail for `ADR9-EV-002`, and what still blocks independent build reproduction?

Inputs:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`;
- local build logs under `C:\ts`;
- local `servoshell.exe` under `C:\ts\servo\target\debug`;
- Visual Studio 2022, LLVM, Python, Rust, `uv`, target, Cargo registry, and Cargo git cache observations from the reference Windows host.

Method:

Inspected Git identity, tracked-file status, log sizes and hashes, selected build result lines, artifact size/hash, normal shell tool availability, Visual Studio developer prompt compiler availability, host hardware/OS, and target/cache footprints. No Servo source file, generated output, native binary, registry archive, downloaded package, build log, or build artifact was copied into Turing.

Observations:

- the build checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- `C:\ts\servo-build-dev-vsdevcmd-llvm.out.log` recorded `Succeeded in 0:09:21` and `BUILD_EXIT=0`;
- Cargo reported `Finished dev profile [unoptimized + debuginfo] target(s) in 9m 14s`;
- `servoshell.exe` was `298702336` bytes with SHA-256 `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B`;
- the successful environment used CPython `3.11.9`, Servo Rust `1.95.0-x86_64-pc-windows-msvc`, Visual Studio Professional 2022 Developer Command Prompt `17.14.21`, MSVC `14.44.35207`, compiler/linker version `19.44.35221` / `14.44.35221.0`, and `LLD 22.1.8`;
- normal PowerShell still lacks `cl`, `link`, and `lld-link`;
- `C:\ts\servo\target` contained `38370` files and `35941861226` bytes, so the existing target cannot stand in for clean-target reproduction.

Inference:

The old "build logs outside repo" note is now too vague. Same-host build evidence is captured enough for handoff, but `ADR9-EV-002` is still partial because decision-grade reproduction requires an owner-reviewed replay script, target/cache isolation policy, clean-target replay on an independent Windows host or VM, and success/failure log bundles.

Changes:

- add the [Servo Build Reproduction Evidence and Gap Report - July 2026](research/servo-independent-build-reproduction-2026-07.md);
- link it from the documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, and this log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo source, dependency, native artifact, generated output, build log, or provenance attestation entered the repository.

Security, privacy, provenance, and release impact:

No source approval changed. The report strengthens provenance and release handoff by recording log and artifact hashes, but it also preserves the unresolved risks around a shallow build checkout, warm target directory, shared Cargo caches, native bootstrap downloads, and missing independent replay.

Compatibility and accessibility impact:

No compatibility or accessibility claim changed. The report did not run WPT, Test262, accessibility tests, a local corpus, or UI/input workflows.

Performance and resource impact:

No performance claim changed. The build duration, artifact size, and target/cache footprint are build-operational observations only; they do not measure browser startup, memory, energy, layout, rendering, or interaction performance.

Documentation and registry impact:

- `PB-002` has sharper build-reproduction evidence but remains blocked;
- `ADR9-EV-002` remains partial;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, research log, and the new build reproduction report.

Next question:

Can the same Servo commit be rebuilt from a clean target on an independent Windows host or clean VM using an owner-reviewed replay script, with target/cache isolation, success/failure logs, and no hidden dependency on warm local state?

## 2026-07-17 — Servo source-baseline equivalence policy prep

Question:

What source-content, release-archive, and crates.io package equivalence evidence exists for the Servo source candidates, and what policy decisions remain before `ADR-0009` can select or reject a source baseline?

Sources and versions:

- independent bare Servo clone at `C:\ts\servo-independent-source-verify-20260717.git`;
- Servo release tag `v0.3.0` at `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`;
- vendored release source archive `C:\ts\servo-upstream-source-provenance-20260717\servo-v0.3.0-src-vendored.tar.gz`;
- cached crates.io package `servo-0.4.0.crate`;
- crates.io package VCS commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873`.

Method and environment:

Compared Git tree path sets with Python `tarfile` path sets for the vendored source archive and cached `.crate` package. Read only bounded metadata such as `GIT_REVISION` and `.cargo_vcs_info.json`. No Servo source files, release archive, crate archive, generated output, native binary, or build log was copied into Turing.

Observations:

- the vendored release archive records `GIT_REVISION` as `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, matching `v0.3.0`;
- the `v0.3.0` Git tree has `191174` files;
- the vendored release archive has `252589` files and `2089732373` file bytes;
- `191078` vendored archive files match release Git paths;
- `61511` vendored archive files are not in the release Git tree, led by `61510` under `vendor/` plus `GIT_REVISION`;
- `96` release Git files are missing from the vendored archive, mostly under `etc/`;
- crates.io `servo 0.4.0` records VCS commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873` and `path_in_vcs` `components/servo`;
- the crate contains all `30` files from `components/servo` at that commit plus four Cargo package metadata files.

Inference:

The vendored release archive is a derived source package, not the release Git tree. The crates.io package is a component package, not the whole Servo repository. `ADR-0009` cannot reuse evidence across Git trees, vendored archives, and crates.io packages without an owner-accepted equivalence policy.

Decision:

- add the [Servo Source Baseline Equivalence Policy Prep - July 2026](research/servo-source-baseline-equivalence-policy-2026-07.md);
- link it from the documentation index, research index, repository map, build-readiness board, pre-build checklist, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, independent source verification report, source/archive provenance audit, and this log;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- update `ADR9-EV-001` missing output from raw equivalence discovery to owner-selected source baseline, signed-tag or equivalent provenance decision, owner-accepted equivalence policy, selected-baseline blob/legal review, and rerun plan.

Security/privacy impact:

No runtime authority changed. The report prevents source-surface confusion that could otherwise let vendored dependencies or normalized crate packages bypass security and provenance review.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. If an accepted baseline differs from the current build commit, future compatibility, accessibility, and local corpus evidence must be tied to that selected baseline.

Performance/memory/energy impact:

No performance claim changed. The source-surface differences mean performance evidence must not be reused across Git tree, release archive, and crates.io package surfaces without explicit scoping.

Licensing/operational impact:

No license or redistribution status changed. The report identifies vendored dependencies, omitted Git files, and normalized Cargo package metadata as legal/source-offer and operations review inputs.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has sharper equivalence evidence but remains blocked;
- `ADR9-EV-001` remains partial until baseline selection, accepted provenance/equivalence policy, selected-baseline blob/legal review, and rerun policy are complete;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, independent source verification report, source/archive provenance audit, research log, and the new equivalence policy prep report.

Unresolved questions:

Which source baseline model should an owner select or reject, and what provenance, blob-content, legal, source-offer, and rerun rules are acceptable for that model?

Next evidence required:

Choose or reject a source-baseline model, accept or reject a signed-tag/equivalent provenance policy, perform selected-baseline blob/legal/source-offer review, and scope or rerun build/dependency/generated/native/compatibility/performance evidence for the selected baseline.

## 2026-07-17 — Servo independent source verification

Question:

Can Turing independently verify Servo's current `main`, the successful external build baseline, and the latest GitHub release source objects from a non-shallow Git fetch, and what remains before `ADR-0009` can select a source baseline?

Sources and versions:

- independent bare partial clone at `C:\ts\servo-independent-source-verify-20260717.git`;
- Servo remote `https://github.com/servo/servo.git`;
- current Servo `main` `622600e045c2e5ea688a9b19b8671b6f43112817`;
- successful external build baseline `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- Servo release tag and branch `v0.3.0` / `release/v0.3` at `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`.

Method and environment:

Created a fresh bare, non-shallow, `blob:none` partial clone outside Turing. Inspected ref identity, object identity, tree identity, tree file counts, ancestry counts, merge bases, connectivity, tag verification posture, and local commit-signature posture. No Servo source files, release archives, crate archives, generated output, native binaries, or build logs were copied into Turing.

Observations:

- the independent clone is bare, non-shallow, and partial with `blob:none`;
- `git fsck --connectivity-only` exited `0` and reported `82` dangling commits plus `153` dangling trees;
- current `main` resolved to `622600e045c2e5ea688a9b19b8671b6f43112817`, tree `9d71530fe4d36dd9c94a2a411d75f219fde0dfc9`, with `193033` tree files;
- the successful build baseline resolved to `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, with `193033` tree files;
- non-shallow ancestry showed the build baseline is exactly two commits behind current `main`;
- `v0.3.0` and `release/v0.3` resolved to `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`, tree `c41b1defccd9ed47a5ac2a8ad40929bc34de80a0`, with `191174` tree files;
- non-shallow ancestry for `v0.3.0...main` returned `1 838`, so the release branch is not a simple ancestor of current `main`;
- `git tag -v v0.3.0` failed because the ref is a lightweight commit tag, not a tag object;
- local `git verify-commit` found signatures on the two GitHub-merged commits but could not check them without the relevant public key; the release commit produced no local signature detail.

Inference:

Independent non-shallow Git object and ancestry verification is now captured for `ADR9-EV-001`. The remaining source-identity work is no longer "can we fetch the object graph independently"; it is owner-selected baseline policy, signed-tag or equivalent provenance policy, blob-content/release-archive/crates.io equivalence, and rerun scoping for whichever baseline is selected.

Decision:

- add the [Servo Independent Source Verification - July 2026](research/servo-independent-source-verification-2026-07.md);
- link it from the documentation index, research index, repository map, build-readiness board, pre-build checklist, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, and this log;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- update `ADR9-EV-001` missing output from independent non-shallow source verification to owner-selected baseline, provenance policy, content/archive/package equivalence, and rerun policy.

Security/privacy impact:

No runtime authority changed. The report improves source-trust evidence while making clear that local GPG verification is not a configured Turing trust root and that source-identity evidence is not security approval.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The source-baseline choice still determines which future WPT, local corpus, accessibility, and platform-surface evidence must be rerun.

Performance/memory/energy impact:

No performance claim changed. The report reinforces that current `main`, the build baseline, and release branch cannot share performance evidence without explicit scoping.

Licensing/operational impact:

No license or redistribution status changed. The report does not inspect full source blob content, release-archive equivalence, crates.io package contents, notices, source-offer obligations, or SBOM posture.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has sharper independent Git evidence but remains blocked;
- `ADR9-EV-001` remains partial until baseline selection, equivalent provenance policy, content/archive/package equivalence, and rerun policy are complete;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, upstream source provenance report, research log, and the new independent source verification report.

Unresolved questions:

Which source baseline model should `ADR-0009` evaluate first, and what does Turing accept as equivalent provenance when a release is represented by a lightweight tag, a GitHub source archive, and a crates.io package surface that are not the same source object?

Next evidence required:

Select or reject a source-baseline model, define signed-tag or equivalent provenance policy, define blob-content/release-archive/crates.io package equivalence checks, and rerun build/dependency/generated/native/compatibility/performance evidence if the selected baseline differs from the current external build baseline.

## 2026-07-17 — Servo upstream source provenance report

Question:

Which upstream Servo source identities correspond to the successful external Windows build baseline, current upstream `main`, the latest GitHub release, and the latest crates.io package, and what remains before `ADR-0009` can select a source baseline?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- successful external build baseline `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- refreshed Servo `origin/main` `622600e045c2e5ea688a9b19b8671b6f43112817`;
- Servo GitHub release `v0.3.0`, published 2026-06-25T15:09:42Z;
- downloaded `servo-v0.3.0-src-vendored.tar.gz` under `C:\ts\servo-upstream-source-provenance-20260717`;
- crates.io `servo 0.4.0`.

Method and environment:

Fetched Servo tags and `origin`, inspected local and remote object IDs, queried GitHub release and commit verification metadata through GitHub CLI, queried crates.io metadata through Cargo and the crates.io API, downloaded the `v0.3.0` vendored source archive outside Turing, verified SHA-256 hashes, and performed a bounded archive readability check. No Servo source, release archive, crate archive, generated output, native binary, or build log was copied into Turing.

Observations:

- the successful external build baseline remains `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`;
- refreshed `origin/main` is `622600e045c2e5ea688a9b19b8671b6f43112817`, two commits ahead of the build baseline;
- the external build checkout is a shallow partial clone, so it is not full-history provenance evidence;
- GitHub commit verification reported the build baseline and current `origin/main` commits as valid;
- `v0.3.0` and `release/v0.3` point to `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`;
- `v0.3.0` is a lightweight tag and its commit was reported unsigned;
- the downloaded `servo-v0.3.0-src-vendored.tar.gz` was `364697035` bytes and matched GitHub's SHA-256 digest `C75EFFBDC0AB6F86B318E28D139EB056268224E072A684492B49409C5221C871`;
- crates.io `servo 0.4.0` was published 2026-07-16, is not yanked, and the local cached `.crate` matched checksum `01A05FFCE7829E67E41C5CB4E10849924CBD781D0EA0D6332D81AFE8476D8A89`.

Inference:

The successful build baseline, current upstream `main`, latest GitHub release source, and latest crates.io package are distinct source surfaces. None is automatically the Turing source baseline. The old "upstream release/archive comparison" gap is now narrowed, but source identity remains unresolved until an owner selects a baseline model and accepts a provenance policy.

Decision:

- add the [Servo Upstream Source Provenance - July 2026](research/servo-upstream-source-provenance-2026-07.md);
- link it from the research index, documentation index, repository map, build-readiness board, pre-build checklist, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, source inventory, source/archive audit, source bibliography, and this log;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- replace current operating gaps that said "upstream release/archive comparison" with owner-selected source baseline, equivalent provenance policy, and independent non-shallow source verification.

Security/privacy impact:

No runtime authority changed. The report clarifies that GitHub commit verification, GitHub asset digests, and crates.io checksums are source-identity inputs, not security approval. It also records that the current build checkout is shallow, which prevents overclaiming full-history provenance.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The source-baseline choice will determine which future WPT, local corpus, accessibility, and platform-surface evidence must be rerun.

Performance/memory/energy impact:

No performance claim changed. Because current `origin/main`, `v0.3.0`, and `servo 0.4.0` differ from the built baseline, any selected baseline other than the current build commit requires fresh fixed-hardware performance and memory evidence.

Licensing/operational impact:

No license or redistribution status changed. The release source archive and crates.io package checksums are evidence for later legal, source-offer, notice, advisory, SBOM, and reproducible-release review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has sharper upstream source evidence but remains blocked;
- `ADR9-EV-001` remains partial until baseline selection, equivalent provenance policy, and independent non-shallow verification are complete;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, ADR-0009 evidence matrix, readiness registry, Servo source inventory, dependency/provenance inventory, supply-chain scan, source/archive provenance audit, source bibliography, research log, and the new upstream source provenance report.

Unresolved questions:

Which source baseline model should `ADR-0009` evaluate first: the already built main-branch commit, refreshed current `origin/main`, the `v0.3.0` release source archive, the crates.io `servo 0.4.0` package surface, or no Servo source baseline?

Next evidence required:

Select or reject a source-baseline model, define signed-tag or equivalent provenance policy, perform an independent non-shallow source verification run, and rerun build/dependency/generated/native/compatibility/performance evidence if the selected baseline differs from the current external build baseline.

## 2026-07-17 — ADR-0009 evidence traceability matrix

Question:

How should the remaining Servo/source-strategy evidence be ordered and traced so a maintainer can continue `PB-002` without losing the relationship between evidence reports, owner scopes, missing outputs, and `ADR-0009` acceptance checks?

Sources and versions:

- [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [`pre-build-readiness.json`](blueprint-v1/machine/pre-build-readiness.json);
- current Servo research reports indexed in [Research Index](research/README.md);
- [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md).

Method and environment:

Reviewed the current readiness registry, ADR packet, operating board, research index, documentation policy, dependency policy, release-operations policy, ADR list, and research program. No external source, generated output, dependency, native artifact, build log, or browser-engine code was imported.

Observations:

- `PB-002` had multiple evidence reports but no single ordered matrix showing which `ADR-0009` evidence items were captured, partial, missing, owner-review-required, or blocked;
- the remaining evidence spans source identity, independent build reproduction, Cargo SBOM/license/advisory posture, native package source-build or binary-package decisions, deterministic download verification, generated-output determinism, build-script/proc-macro side effects, unsafe/FFI review, component boundaries, JavaScript-runtime conflict, compatibility, performance, security, maintenance, public claims, and ADR owner review;
- the machine readiness registry remains the status source of truth, while the ADR packet remains the narrative source of truth.

Inference:

A traceability matrix reduces handoff risk without promoting any Servo option. It makes the remaining work auditable and prevents future continuation from treating local identity evidence as dependency approval, performance evidence, compatibility evidence, or a source-strategy decision.

Decision:

- add the [ADR-0009 Evidence Traceability Matrix](project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- link it from the documentation index, research index, project-buildout index, repository map, pre-build checklist, build-readiness board, ADR-0009 packet, and readiness registry;
- keep `PB-002` blocked and keep proposed `ADR-0009` proposed;
- keep Turing's dependency, unsafe-code, native-code, generated-code, and provenance ledgers unchanged because no Servo source or dependency entered the repository.

Security/privacy impact:

No authority or runtime security behavior changed. The matrix makes security-sensitive follow-up work explicit, especially native package review, deterministic download verification, unsafe review, FFI contracts, sandbox implications, and update/release provenance.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The matrix records local compatibility corpus, WPT/Test262 evidence, unsupported API accounting, and accessibility-sensitive component boundaries as missing before `ADR-0009`.

Performance/memory/energy impact:

No performance claim changed. The matrix records fixed-hardware startup, memory, interaction, frame pacing, energy, and process-disclosure evidence as missing before any speed, low-memory, energy, or Chrome-class inference.

Licensing/operational impact:

No license status changed. The matrix records license, notice, patent, source-offer, advisory, native source-build, binary-package exception, SBOM, maintenance, and release-manifest work as required before a Servo relationship can be accepted.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has clearer continuation evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, readiness registry, research log, and the new evidence matrix.

Unresolved questions:

Which evidence item should the owner prioritize next: upstream source/archive comparison, independent build reproduction, accepted license/advisory/SBOM decisions, native source-build decisions, clean generated-output reproduction, or component-boundary analysis?

Next evidence required:

Use the matrix order to complete `ADR9-EV-001` and `ADR9-EV-002` first, then proceed through dependency/legal/native, generated/build-script, unsafe/FFI, component-boundary, compatibility, performance, security, maintenance, and ADR owner-review evidence.

## 2026-07-17 — Servo native bootstrap provenance and source-build audit

Question:

Which native packages and toolchain inputs does Servo's Windows bootstrap path download or install, what identity and signature evidence exists for those inputs on the reference host, and what source-build or binary-package decisions remain before `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- Servo Windows bootstrap sources under `C:\ts\servo\python\servo`;
- `servo/servo-build-deps` release tag `msvc-deps`;
- downloaded upstream bootstrap assets under `C:\ts\servo-native-artifacts-msvc-deps`;
- extracted bootstrap dependency tree under `C:\ts\servo\target\dependencies`;
- external debug build output under `C:\ts\servo\target\debug`.

Method and environment:

Inspected Servo bootstrap scripts, release metadata, local asset hashes, Authenticode signatures, extracted dependency tree counts, license-like file counts, plugin-list inputs, and debug output footprint outside the Turing repository. No Servo source, generated output, build log, native binary, downloaded archive, MSI file, or package metadata was copied into Turing.

Observations:

- Servo Windows bootstrap downloads `moztools-4.0.zip` and GStreamer MSVC `1.22.8` runtime/development MSIs from `servo/servo-build-deps` release tag `msvc-deps`;
- GitHub release metadata for the relevant assets exposed `digest: null` on 2026-07-17;
- the original upstream GStreamer runtime MSI was `127258624` bytes with SHA-256 `37F9973FE5C720CE1F1602E7E599336384B9FF3E4878817987DD6B77265F17BB` and Authenticode status `NotSigned`;
- the original upstream GStreamer development MSI was `225861632` bytes with SHA-256 `2D0CF6E89CF88D94E670CD81087C002408161D1C8843C00D3F27D33CE254C523` and Authenticode status `NotSigned`;
- the original upstream `moztools-4.0.zip` was `143306382` bytes with SHA-256 `CCEB354767EF3DAD8813E63CB95ED081814225BF5FA15BFA083AA8B31A339153`;
- the two small GStreamer `.msi` files under `target\dependencies` are extracted-tree artifacts, not the original upstream downloads;
- Authenticode checks over extracted `.dll`, `.exe`, and `.msi` files found `981` unsigned files and one valid signed `vswhere.exe`;
- external debug output under `target\debug` contained `617` `.dll`, `.exe`, and `.pdb` files totaling `5223312616` bytes.

Inference:

The old "native binary provenance" gap is now too broad. Local native bootstrap identity evidence exists for the observed upstream assets and extracted dependency tree, but Turing still lacks source-build recipes or binary-package exceptions, legal/advisory/notice decisions, deterministic download verification, package minimization, final release manifests, SBOM policy, and independent-host reproduction.

Decision:

- add the [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](research/servo-native-bootstrap-provenance-audit-2026-07.md);
- correct older GStreamer MSI wording so extracted-tree MSI artifacts are not confused with original upstream downloads;
- link the audit from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, source/archive provenance audit, pre-build checklist, build-readiness board, project-buildout index, repository map, source bibliography, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo source, dependency, native artifact, generated output, or provenance attestation entered the repository.

Security/privacy impact:

The audit strengthens bootstrap artifact traceability and highlights unsigned native execution surfaces, but no runtime authority, sandbox, dependency, source code, or security claim changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Local corpus, WPT, Web IDL, accessibility, platform, media, and embedding evidence remain required.

Performance/memory/energy impact:

No performance claim changed. The native bootstrap dependency size and debug-output footprint are now explicit build, binary-size, packaging, symbol-handling, and measurement review inputs.

Licensing/operational impact:

No license status changed. GStreamer, moztools, `servo-build-deps`, MSYS2-derived tools, native DLLs, EXEs, PDBs, codec libraries, crypto libraries, notices, source-offer obligations, and redistribution still require Turing-specific legal, advisory, source-build, binary-package exception, and package-manifest review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, source/archive provenance audit, source bibliography, readiness registry, research log, and the new native bootstrap audit.

Unresolved questions:

Which native bootstrap packages can Turing rebuild from source? Which require explicit binary-package exceptions? Which codec, patent, source-offer, notice, advisory, sandbox, update, and package-minimization decisions would be required for each candidate Servo relationship?

Next evidence required:

Run native source-build or binary-package exception review, legal/advisory/notice review, deterministic bootstrap download verification design, independent-host bootstrap reproduction, final release package manifest/SBOM planning, upstream release/archive comparison, clean generated-output regeneration, component-boundary analysis, local corpus experiments, and fixed-hardware performance baseline for `ADR-0009`.

## 2026-07-17 — Servo source and archive provenance audit

Question:

Which local source identities, source archives, Cargo registry cache entries, Stylo git-source records, and native/bootstrap artifact summaries exist for the clean external Servo checkout, and what remains before `ADR-0009` can decide a source strategy?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- Stylo git source `https://github.com/servo/stylo` at `d3de91cbac7bba38e159239b3c0a360783fce2ee`;
- local Cargo registry caches under `C:\Users\bcw19\.cargo\registry`;
- Servo Windows bootstrap dependencies under `C:\ts\servo\target\dependencies`;
- local source archives under `C:\ts`.

Method and environment:

Ran Git identity, tracked-file manifest, archive hash, Cargo metadata, Cargo lockfile checksum, registry cache, Stylo checkout, and bounded native/bootstrap artifact checks outside the Turing repository. No Servo source, Stylo source, registry archive, generated output, metadata file, build log, native binary, or bootstrap artifact was copied into Turing.

Observations:

- the clean Servo checkout remained at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, tree `daa2bc0e189e1981fb021501065fc3466159b00d`, with `193033` tracked files and `git fsck --connectivity-only` exit `0`;
- the Servo tracked-file manifest digest was `54E852C7337C1913B72A057D5E1E354B0201D8945D14B19F36471B8E9EF72DE7`;
- the local Servo archive `C:\ts\servo-source-4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe-20260717.tar` was `931993600` bytes with SHA-256 `205530091A7E36977BBF7417F5D48D91D122137B9450985897E54C9A5D00841D`;
- the Stylo checkout was pinned to `d3de91cbac7bba38e159239b3c0a360783fce2ee`, with local archive SHA-256 `323900D70CCF149C61F187A10F47D899A977772E3CE5D7BA82FD83B0DA5D1375`;
- default and all-features registry `.crate` archives were all present, matched Servo `Cargo.lock` checksums, and had unpacked source directories;
- the Windows bootstrap dependency tree contained `19456` files and `1582709414` bytes, including `537` DLLs, `443` EXEs, `309` PDBs, and `2` extracted-tree GStreamer MSI artifacts.

Inference:

The old "source/archive digests" gap is now too broad. Local Servo, Stylo, registry-cache, and native bootstrap identity evidence exists, but it is not adoption evidence. The remaining gate is upstream release/archive comparison, independent source verification, native source-build or binary-package exceptions, legal/advisory decisions, clean generated-output regeneration, build-script/proc-macro/native review, component-boundary analysis, local compatibility and performance evidence, and owner review.

Decision:

- add the [Servo Source and Archive Provenance Audit - July 2026](research/servo-source-archive-provenance-audit-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, pre-build checklist, build-readiness board, project-buildout index, repository map, source bibliography, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo source, dependency, native artifact, generated output, or provenance attestation entered the repository.

Security/privacy impact:

The audit strengthens source and bootstrap artifact traceability, but no runtime authority, sandbox, dependency, source code, or security claim changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Local corpus, WPT, Web IDL, accessibility, platform, and embedding evidence remain required.

Performance/memory/energy impact:

No performance claim changed. The archive sizes, registry cache size, and native bootstrap footprint are now explicit build, binary-size, packaging, and measurement review inputs.

Licensing/operational impact:

No license status changed. Servo, Stylo, registry crates, generated outputs, GStreamer, moztools, native DLLs, EXEs, PDBs, and source-offer obligations still require Turing-specific legal, notice, advisory, source-build, and redistribution review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, source bibliography, readiness registry, research log, and the new provenance audit.

Unresolved questions:

Do the local Servo and Stylo archives match a selected upstream release/tag/source package? Which native bootstrap artifacts can be rebuilt from source, redistributed, minimized, sandboxed, updated, and covered by notices? Which source provenance records would be required if a selective component boundary is proposed?

Next evidence required:

Run upstream release/archive comparison, independent-source fetch verification, source-offer and notice review, native source-build policy review, clean generated-output regeneration, registry/git build-script review, component-boundary analysis, local corpus experiments, and fixed-hardware performance baseline for `ADR-0009`.

## 2026-07-17 — Servo build-script and generated-output audit

Question:

What build-script side effects and generated outputs does the clean external Servo Windows development build expose, and what remains before Turing can trust generated outputs or build-time behavior for `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- generated outputs under `C:\ts\servo\target\debug\build`;
- first-party Servo workspace `build.rs` files;
- local Cargo timing artifact `C:\ts\servo\target\cargo-timings\cargo-timing-20260717T184252676Z-d205ee0048504b27.html`.

Method and environment:

Inspected Cargo `out` directories, first-party build scripts, generator inputs, and build-script `output` logs. Hashed key generated-output directories and generator inputs. Ran one incremental no-op Servo rebuild from Visual Studio 2022 Developer Command Prompt with LLVM on `PATH`. No Servo source, generated output, metadata, build log, native binary, or timing artifact was copied into Turing.

Observations:

- the Windows debug build contained `103` Cargo `out` directories, `3955` files, and `1106039671` bytes under `target\debug\build`;
- largest output directories came from `mozjs_sys`, `mozangle`, `harfbuzz-sys`, `aws-lc-sys`, `fontsan`, `servo-script-bindings`, `glslopt`, `zstd-sys`, `libsqlite3-sys`, and `stylo`;
- first-party generated outputs included `1631` files from `servo-script-bindings`, `546` copied files from `servo-script`, `539` copied files from `servo-script-webgpu`, a generated DevTools build ID, Windows servoshell resource output, and Stylo CSS property output;
- key generator inputs included `556` Web IDL files, Python codegen, a vendored WebIDL parser, PLY, `uv.lock`, `.python-version`, `rust-toolchain.toml`, and Stylo `css-properties.json`;
- one incremental no-op rebuild exited `0`, reported `Succeeded in 0:00:03`, and kept inspected first-party generated-output directory digests unchanged;
- first-party build scripts depend on Python or `uv`, `SOURCE_DATE_EPOCH`, `OUT_DIR`, git state, target cfg, platform SDK/resource tools, `OHOS_SDK_NATIVE`, nested Cargo, and DLL/resource copying behavior;
- build-script `output` logs across all build scripts contained `41890` lines, `11685` `rerun-if-env-changed` markers, `11013` `rerun-if-changed` markers, and many warnings, dominated by registry/native-facing packages.

Inference:

Generated-output and first-party build-script evidence is now concrete enough for the ADR packet, but it is not enough for adoption. Turing still needs clean-target regeneration, independent-host comparison, accepted build-script/proc-macro side-effect policy, dynamic tracing, generated-output source/license provenance, and policy for environment-sensitive build inputs before any candidate component can enter release code.

Decision:

- add the [Servo Build-Script and Generated-Output Audit - July 2026](research/servo-build-script-generated-output-audit-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, pre-build checklist, build-readiness board, project-buildout index, repository map, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo dependency, generated output, native code, or provenance attestation entered the repository.

Security/privacy impact:

The audit identifies build-time process execution, environment-variable sensitivity, generated binding output, native build output, and DLL/resource copying surfaces that must be reviewed before adoption. No Turing runtime authority or source code changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Web IDL, WebGPU, WebGL, DOM, CSS, DevTools, and platform-generated outputs remain evidence targets for local corpus and conformance work.

Performance/memory/energy impact:

No performance claim changed. The output size and large registry/native build outputs are now explicit binary-size, build-time, memory-footprint, and packaging review targets.

Licensing/operational impact:

No license status changed. Generated outputs, generated headers, WebIDL inputs, Stylo outputs, registry/native outputs, DLLs, and toolchain-derived files still need source-to-output provenance, license, notice, and source-offer review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, generated/native/unsafe/FFI classification, readiness registry, research log, and the new audit report.

Unresolved questions:

Can the same generated outputs be reproduced from a clean target directory and on an independent host? Which registry and git build scripts execute tools, touch native packages, read environment variables, or generate files relevant to any candidate component boundary? Which generated outputs carry license or source-offer obligations?

Next evidence required:

Run clean generated-output regeneration with diff proof, independent-host comparison, accepted build-script/proc-macro side-effect policy, dynamic tracing, generated-output source/license provenance review, FFI ABI contract review, component-boundary analysis, local corpus experiments, and fixed-hardware performance baseline for `ADR-0009`.

## 2026-07-17 — Servo generated native unsafe and FFI classification

Question:

Where do generated-code, build-script, proc-macro, native-link, FFI, and unsafe-code surfaces concentrate in the clean external Servo checkout before Turing can decide `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- local default Cargo metadata file `C:\ts\servo-metadata-default.json`;
- first-party Servo `build.rs` files under `components`, `ports`, and `tests`.

Method and environment:

Ran `rg` source-shape queries for unsafe, `SAFETY:`, FFI/export/link, generated-code, Web IDL, and native-source markers while excluding `target/` and `.venv/`. Parsed Cargo metadata with Node for build-script, proc-macro, and native-link package counts. Inspected the nine first-party Servo workspace `build.rs` files. No Servo source, generated output, metadata file, or native artifact was copied into Turing.

Observations:

- unsafe queries found `2280` unsafe mentions across `241` Rust files, including `1629` unsafe-block matches, `224` unsafe functions, `104` unsafe impls, and `157` `SAFETY:` comments;
- unsafe usage concentrates in `components/script`, `components/script_bindings`, `components/webgl`, `ffi/capi`, `components/fonts`, `ports/servoshell`, `components/media`, and `components/layout`;
- FFI/export/link markers appeared `217` times across `40` Rust files, led by script runtime/bindings, `ffi/capi`, servoshell platform paths, fonts, allocator, and media;
- default metadata contained `157` packages with build scripts, `70` proc-macro packages, and `25` native-link packages;
- the nine first-party build scripts generate or copy Web IDL/script/WebGPU bindings, emit DevTools build IDs, infer production cfgs, inspect OpenHarmony SDK metadata, compile platform C/resources, and run nested `cargo cinstall` for C API tests.

Inference:

The classification turns a broad generated/unsafe/FFI concern into concrete review queues. Servo-derived or selective-component paths would need block-level unsafe inventory, generated-output provenance, build-script side-effect audit, proc-macro review, FFI ABI contracts, native source/binary provenance, and sanitizer/fuzz/Miri/C API evidence before source adoption could be considered.

Decision:

- add the [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](research/servo-generated-native-unsafe-classification-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, pre-build checklist, build-readiness board, project-buildout index, repository map, readiness registry, and research log;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo dependency, native code, unsafe code, generated output, or provenance attestation entered the repository.

Security/privacy impact:

The pass identifies unsafe, FFI, generated-code, build-time execution, and native-link review targets. No Turing runtime authority, dependency, source code, or release claim changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. Script bindings, WebGL, WebGPU, C API, platform shell, fonts, media, and accessibility-adjacent generated code remain evidence targets for later local corpus and conformance work.

Performance/memory/energy impact:

No performance claim changed. The unsafe and native-link clusters are now explicit performance, memory, binary-size, and driver/media review targets before any adoption discussion.

Licensing/operational impact:

No license status changed. Proc macros, build scripts, generated outputs, native-link packages, C API headers/tests, Stylo-derived outputs, and downloaded native binaries still need Turing-specific provenance, license, source-offer, and source-build review.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, dependency ledger, unsafe-code ledger, native-code ledger, generated-code ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, project-buildout index, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, supply-chain scan, readiness registry, research log, and the new classification report.

Unresolved questions:

Which candidate component boundary, if any, can avoid SpiderMonkey, Stylo, generated script bindings, WebGL/native driver exposure, media/native binary packages, and C API lifetime contracts? Which unsafe blocks and generated outputs are reachable in that boundary, and what sanitizer, fuzzing, Miri, C API, and conformance evidence would be required?

Next evidence required:

Run block-level unsafe review, generated-output provenance and regeneration checks, build-script side-effect audit, proc-macro expansion review, FFI ABI contract review, native source/binary provenance review, component-boundary analysis, and then local corpus/performance experiments for `ADR-0009`.

## 2026-07-17 — Servo supply-chain policy scan

Question:

Does the clean external Servo checkout pass its own advisory, license, ban, and source policy checks, and what supply-chain evidence remains before Turing can decide `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- `cargo-deny 0.19.0`;
- Servo `deny.toml`, `about.toml`, `Cargo.lock`, and the default/all-features Cargo metadata files.

Method and environment:

Ran `cargo deny check all --show-stats` against both default and all-features metadata using Servo's own `deny.toml`. Inspected `Cargo.lock` checksum posture and the unpacked Windows bootstrap dependencies under `C:\ts\servo\target\dependencies`. No Servo source, Cargo metadata, or native artifact was copied into Turing.

Observations:

- default and all-features `cargo-deny` scans both exited `0` under Servo's policy;
- default metadata had `0` advisory, license, source, or ban errors, with `11` unnecessary duplicate-skip warnings;
- all-features metadata had `0` errors and `0` warnings across advisories, bans, licenses, and sources;
- Servo's `deny.toml` ignores `12` RustSec advisories and permits a large duplicate-version skip list;
- `Cargo.lock` contains `1034` registry entries with checksums, `11` Stylo git entries pinned by revision but without Cargo checksums, and `75` path entries;
- Windows bootstrap unpacked `19456` files under `target\dependencies`, including `537` DLLs, `443` EXEs, `309` PDBs, and `2` extracted-tree GStreamer MSI artifacts;
- the extracted-tree GStreamer MSI artifacts were hashed and recorded in the scan report; follow-up native bootstrap audit records the original upstream MSI asset hashes.

Inference:

Passing Servo's own policy is useful evidence, but it is not Turing acceptance. Turing still needs its own advisory decisions, license/legal review, upstream source/archive comparison, native source-build or binary-package exceptions, generated-code review, unsafe/FFI inventory, and component-boundary analysis.

Decision:

- add the [Servo Supply-Chain Policy Scan — July 2026](research/servo-supply-chain-policy-scan-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, Servo source inventory, pre-build checklist, build-readiness board, and readiness registry;
- keep `PB-002` blocked and keep Turing's security ledgers unchanged because no Servo dependency entered the repository.

Security/privacy impact:

The scan identifies ignored advisories, native binaries, source-policy exceptions, and checksum gaps that must be reviewed before adoption. No Turing runtime authority, dependency, or source code changed.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The native media, platform, input, WebDriver, and accessibility-related dependency surfaces remain evidence targets.

Performance/memory/energy impact:

No performance claim changed. The native dependency footprint and duplicate-version exceptions are now explicit performance and packaging review targets.

Licensing/operational impact:

Servo's `cargo-deny` license check passed under Servo policy, but Turing-specific license text, notice, source-offer, patent, native binary, and distribution review remain required.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, dependency ledger, provenance ledger, native-code ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, dependency/provenance inventory, readiness registry, research log, and the new supply-chain policy scan.

Unresolved questions:

Which of Servo's ignored advisories and duplicate exceptions would Turing accept, reject, patch, or avoid? Can the Windows native bootstrap surface be rebuilt from source, minimized, sandboxed, licensed, and kept current at the level required for a browser release?

Next evidence required:

Run Turing-specific legal/advisory/native provenance reviews, compare upstream source/archive artifacts against the local digest evidence, classify build scripts/proc macros/generated code/unsafe/FFI, then evaluate component boundaries and local corpus/performance evidence for `ADR-0009`.

## 2026-07-17 — Servo dependency and provenance metadata pass

Question:

What dependency and provenance shape does the clean external Servo build expose before Turing can decide `ADR-0009`?

Sources and versions:

- clean external Servo checkout at `C:\ts\servo`;
- Servo remote `https://github.com/servo/servo.git`;
- Servo commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, committed 2026-07-17T15:50:14Z;
- local metadata artifacts `C:\ts\servo-metadata-default.json`, `C:\ts\servo-metadata-all-features.json`, and `C:\ts\servo-tree-features-depth1.txt`.

Method and environment:

Ran `cargo metadata --locked --format-version 1`, `cargo metadata --locked --format-version 1 --all-features`, and `cargo tree --locked -e features --depth 1 -p servo` from the external checkout. The all-features metadata command downloaded additional optional crates into the user Cargo cache. No Servo source or generated metadata was copied into Turing.

Observations:

- default metadata contained `1069` packages: `75` Servo path packages, `983` registry packages, and `11` git packages;
- all-features metadata contained `1120` packages: `75` Servo path packages, `1034` registry packages, and `11` git packages;
- default metadata exposed `157` packages with build scripts, `70` proc-macro packages, `25` native-link packages, `58` package names with multiple versions, and no package missing both `license` and `license_file` metadata;
- the git packages all came from `https://github.com/servo/stylo` at revision `d3de91cbac7bba38e159239b3c0a360783fce2ee`;
- high-impact clusters include MozJS/SpiderMonkey and default `js_jit`, Stylo, WebRender/WebGPU/ANGLE, GStreamer/media, rustls/aws-lc/ring, SQLite, platform UI/input/accessibility crates, DevTools, and WebDriver.

Inference:

Servo adoption or selective reuse would be a significant source, dependency, license, native, generated-code, unsafe, and maintenance program. The dependency metadata makes a whole-workspace adoption path more visibly expensive and reinforces the need to evaluate component boundaries before any release-code relationship.

Decision:

- add the [Servo Dependency and Provenance Inventory — July 2026](research/servo-dependency-provenance-inventory-2026-07.md);
- link it from the documentation and research indexes;
- update the ADR-0009 packet, pre-build checklist, build-readiness board, and readiness registry;
- keep `PB-002` blocked and preserve the rule that no Servo-derived release code enters Turing before `ADR-0009`.

Security/privacy impact:

No new Turing dependency or source code was added. The inventory identifies native-link, build-script, proc-macro, JavaScript-runtime, crypto/TLS, media, storage, DevTools, and platform review targets that must be classified before adoption.

Compatibility/accessibility impact:

No compatibility or accessibility claim changed. The report identifies Servo dependencies and feature clusters that later local WPT, corpus, UI/input, and accessibility tests must account for.

Performance/memory/energy impact:

No performance claim changed. Dependency scale, duplicate versions, JIT defaults, GPU/media stacks, and native libraries are now explicit performance and footprint review targets.

Licensing/operational impact:

Cargo metadata had no package missing both `license` and `license_file`, but this is not legal clearance. Full license text, notices, patent review, advisory scan, upstream source/archive comparison, build-script classifications, generated-code review, and maintenance ownership remain required.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` has additional evidence but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, dependency ledger, provenance ledger, or support claim changed;
- affected documents: documentation index, research index, repository map, pre-build checklist, build-readiness board, ADR-0009 packet, Servo source inventory, readiness registry, research log, and the new dependency/provenance inventory.

Unresolved questions:

Which Servo component boundaries, if any, can be studied without importing SpiderMonkey/MozJS semantics, Stylo ownership, native build complexity, or unsupported supply-chain obligations into Turing? What are the exact advisory, license, upstream source/archive comparison, generated-code, unsafe, native, WPT, corpus, and benchmark results for the candidate boundary?

Next evidence required:

Run a full SBOM/license/advisory/source-provenance pass for the exact Servo checkout and feature profile, classify build scripts/proc macros/native links/generated code/unsafe/FFI, then perform component-boundary, local corpus, fixed-hardware benchmark, and maintenance-model analysis for `ADR-0009`.

## 2026-07-17 — Build readiness operating board and Servo source inventory

Question:

What does a maintainer or agent need to continue pre-build documentation and research without confusing contained M0 work for broad implementation readiness?

Sources and versions:

- current Turing documentation, readiness, backlog, and research registries at this change;
- Servo home page, repository README, docs.rs crate page, LTS policy, WPT pass-rate page, and recent Servo project updates retrieved 2026-07-17;
- local isolated Windows preflight observations from `C:\Users\bcw19\AppData\Local\Temp\turing-adr-0009-servo-evidence\servo`;
- clean short-path Servo bootstrap and build observations from `C:\ts\servo`.

Method and environment:

Documentation and source-strategy handoff audit plus external preflights only. The pass did not import Servo source into Turing, run WPT, run benchmarks, or change implementation status. The second external preflight installed `uv`, bootstrapped Servo, and built Servo outside this repository.

Observations:

- the repository had strong canonical policy but lacked a single human continuation board that ordered `PB-*`, `WP-*`, `RQ-*`, and `ADR-*` records;
- `PB-002` remained the first blocked broad-web-engine item;
- Servo public sources show active embedding releases and a published crate surface, but also best-effort LTS language, no Servo 1.0 definition, and JavaScript-runtime coupling that conflicts with Turing's accepted Turing-owned runtime goal unless superseded by ADR.
- the external Servo workspace matched the observed public `main` commit, but `git ls-files` returned no tracked files, `git status` counted `193074` entries, and `git fsck` reported dangling objects, so the checkout was invalid for build evidence;
- during the first preflight, the host had Visual Studio Professional 2022 with queried VC tools, ATL, and Windows 11 SDK components, but `uv` was missing and `cl`/`link` were not on the normal PowerShell `PATH`;
- Servo pins Python `3.11` and Rust `1.95.0`, so the source-strategy experiment needs isolated tooling rather than Turing's M0 toolchain alone.
- a clean short-path checkout at `C:\ts\servo` later pointed at `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, counted `193033` tracked files, and had no tracked-file changes after bootstrap and build;
- installing `uv 0.11.29`, using Servo's CPython `3.11.9` and Rust `1.95.0` environment, entering the Visual Studio 2022 Developer Command Prompt, and adding `C:\Program Files\LLVM\bin` for `lld-link.exe` allowed `.\mach.ps1 bootstrap` and `.\mach.ps1 build --dev -j 8` to complete;
- the Servo build produced `C:\ts\servo\target\debug\servoshell.exe`, but that build artifact does not authorize Servo-derived Turing code or any compatibility, performance, security, accessibility, or support claim.

Inference:

Handoff clarity and a dated Servo inventory reduce the risk that future work jumps from "contained M0 allowed" to broad browser implementation, or from "Servo is useful to study" to unreviewed Servo-derived release code.

Decision:

- add the [Build Readiness Operating Board](project-buildout/13-build-readiness-operating-board.md);
- add the [Servo Source Strategy Inventory — July 2026](research/servo-source-strategy-inventory-2026-07.md);
- add the [ADR-0009 Source Strategy Decision Packet](project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- add root `.gitattributes` for Rust and tooling line-ending stability on Windows checkouts;
- link both from the relevant indexes;
- add Servo source-strategy evidence to `PB-002` while keeping it blocked;
- record the first Windows preflight blockers and the second short-path bootstrap/build evidence in the Servo inventory, ADR-0009 packet, and build-readiness board.

Security/privacy impact:

No source or dependency was imported. The new inventory reinforces provenance, clean-room, JavaScript-runtime, sandbox, support, and public-claim gates before any Servo relationship can affect release code.

Compatibility/accessibility impact:

The inventory points to WPT and accessibility evidence that must be reproduced before compatibility or accessibility conclusions are accepted. No support matrix changes.

Performance/memory/energy impact:

Servo performance and layout observations remain external evidence leads. Turing still requires fixed-hardware, equal-workload, equal-security measurement before any performance claim.

Licensing/operational impact:

No license status changes. The next ADR packet must include license, LTS, support, maintenance, and patch-ownership evidence.

Affected requirements, risks, ADRs, work packages, and documents:

- `PB-002` now has dated evidence and an operating decision packet but remains blocked;
- proposed `ADR-0009` remains proposed;
- no requirement, risk, work-package status, source-policy ledger, or support claim changed;
- affected files and docs: `.gitattributes`, documentation index, research index, repository map, source bibliography, pre-build checklist, project-buildout index, research log, readiness registry, and the new board, inventory, and decision-packet documents.

Unresolved questions:

What exact Servo dependency graph, component boundary, SpiderMonkey implication, WPT/local-corpus result, benchmark baseline, maintenance model, and provenance record should be compared, and which components if any can be studied without conflicting with Turing-owned engine and JavaScript commitments?

Next evidence required:

Create the `ADR-0009` research branch, use the clean short-path build evidence, extract API, dependency, and source-policy inventories, analyze runtime and maintenance implications, and run a small local corpus through the planned comparison harness without copying Servo source into Turing.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## 2026-07-17 — Native UI architecture and pre-build readiness

Added the Native UI Runtime book, Slint/Vizia/Floem/GPUI evaluation, React design-lab boundary, page-surface integration plan, UI framework and budget registries, PB-001 through PB-020 readiness control, proposed ADR-0013 through ADR-0016, RQ-55 through RQ-58, repository-wide cross-references, and validation requirements. No UI framework, dependency, reference platform, performance claim, support claim, or implementation status was accepted.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## 2026-07-17 — Agent execution and production readiness

Added task-scoped agent authority, run and evidence provenance, independent-verification rules, stable-scope and platform contracts, release channels, SLO catalog, production gates, update trust roles, service dependencies, vulnerability SLA framework, secure-development crosswalk, signing separation, and human release authority. Turing remains not ready for production or stable release.

<!-- WP-002-KERNEL-IPC-2026-07 -->
## 2026-07-17 — WP-002 kernel identity, capability, and bounded IPC reference

Question:

How can Turing turn its process-role and IPC architecture into an executable policy reference without prematurely selecting an operating-system transport or serialization dependency?

Method and environment:

Added a dependency-free Rust implementation and a standard-library-only deterministic generator on the pinned M0 workspace. The schema, generated Rust, generated process-capability documentation, unit tests, shell integration, workspace validators, and CI are reviewed together.

Decision:

- make `schemas/ipc/control-plane.json` the M0 source for role, capability, launch, message, route, scope, size, and queue policy;
- generate committed Rust and process-capability documentation and reject drift;
- use restart-safe process ID/epoch pairs;
- enforce capability attenuation, deny-by-default routes, exact sequence state, channel endpoint binding, and bounded queues;
- keep `WP-002`, `REQ-SEC-003`, and `REQ-PERF-004` at M0 reference status rather than claiming transport, sandbox, or production completion.

Security/privacy impact:

The reference rejects stale identity, capability escalation, unauthorized routes, missing capabilities, endpoint reuse, sequence errors, and resource overcommit. It introduces no external runtime or native dependency and no unsafe code. It does not yet authenticate real peers or decode hostile wire bytes.

Performance/memory/energy impact:

Count and byte budgets now have executable backpressure behavior. Values remain unvalidated M0 defaults pending fixed-hardware transport workloads.

Affected requirements, risks, ADRs, work packages, and documents:

- `WP-002` is `m0_reference_in_progress`;
- `REQ-SEC-003` and `REQ-PERF-004` gain traceable M0 implementation evidence but remain unverified;
- source, generated-code ledger, workspace map, pre-build readiness, CI, root/docs/research indexes, architecture/security/performance/testing/roadmap/backlog/definition-of-done prose, and the dated report are synchronized.

Next evidence required:

Canonical fuzzable wire encoding, authenticated per-platform transports, handle/shared-memory leases, cancellation and close state machines, compromised-process negative traffic, sandbox integration, fixed-hardware measurements, and independent security review.

<!-- WP-002-AUDIT-HARDENING-2026-07 -->
## 2026-07-17 — WP-002 channel and queue audit hardening

A final non-approving audit found that the first envelope could implicitly claim an unused channel ID and that generic queue accounting recomputed `EncodedSize` during dequeue. The reference now requires process-broker registration before a channel can carry messages, rejects unknown and duplicate channel use, and stores the byte charge captured at admission. Negative tests and all affected architecture, security, performance, testing, task, and evidence records were synchronized. The change remains an M0 reference and does not add an operating-system transport or production-security claim.

## 2026-07-17 — Servo component boundary and JavaScript conflict evidence

Question:

Which Servo package boundaries and JavaScript-runtime conflicts shape `ADR-0009` before any source-strategy decision?

Sources and versions:

- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- Turing `ADR-0004`, engine, JavaScript, security, project-buildout, and `ADR-0009` evidence records.

Method and environment:

- ran read-only `git`, `cargo metadata`, `rg`, and local summary scripts from the Windows reference host;
- computed package closures for selected Servo roots with dev-only dependency edges excluded;
- counted heuristic unsafe, FFI/export/link, MozJS/SpiderMonkey, Web IDL/binding, WebRender/GPU, and GStreamer/media markers.

Observations:

- `servoshell`, `servo`, `servo-layout`, `servo-script`, `servo-script-bindings`, `servo-net`, `servo-storage`, and `servo-media-gstreamer` closures remain large enough that no obvious package name is a small approved component boundary;
- `servo` defaults include `js_jit`, while `--no-default-features` still reaches `mozjs`, `mozjs_sys`, Stylo, and WebRender;
- `servo-layout` directly reaches `servo-script`, `servo-script-traits`, Stylo packages, and `webrender_api`;
- `servo-script` and `servo-script-bindings` concentrate MozJS/SpiderMonkey, Web IDL, unsafe, and FFI-sensitive markers.

Inference:

`ADR9-EV-011` and `ADR9-EV-012` can move from missing to partial, but no component boundary, JavaScript runtime relationship, dependency, compatibility result, performance result, or source-strategy option is approved.

Affected records:

- `docs/research/servo-component-boundary-analysis-2026-07.md`;
- `docs/blueprint-v1/machine/adr-0009-evidence.json`;
- `docs/blueprint-v1/machine/pre-build-readiness.json`;
- `docs/project-buildout/13-build-readiness-operating-board.md`;
- `docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`;
- `docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`;
- `docs/README.md`;
- `docs/research/README.md`;
- `docs/repository-map.md`.

Next evidence required:

Owner-selected source baseline and feature profile, target-specific dependency closures, in/out component lists, replacement contracts, accepted JavaScript conflict decision, local compatibility corpus, fixed-hardware performance baseline, security/sandbox implications, maintenance model, and final `ADR-0009` review.

## 2026-07-17 — Servo WPT and compatibility denominator evidence

Question:

What WPT/Test262 denominator and local corpus evidence is required before `ADR-0009` can use compatibility results?

Sources and versions:

- external Servo checkout at `C:\ts\servo`, commit `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`, with `193033` tracked files and no tracked-file changes;
- Servo WPT configuration, include rules, metadata manifests, host aliases, Python testing commands, and WPT-hosted Test262 data.

Method and environment:

- inspected `tests/wpt/` layout, `config.ini`, `include.ini`, `hosts`, `aliases`, `MANIFEST.json` files, metadata `.ini` files, WPT focus directories, and Test262 vendoring;
- used read-only `Get-ChildItem`, `rg`, and Python summary scripts;
- did not run WPT, Test262, local corpus, Servo, or comparison browsers.

Observations:

- Servo's upstream WPT source tree contains `160978` files under `tests/wpt/tests`;
- Servo's upstream WPT metadata root contains `18777` `.ini` files and a `39462596` byte `MANIFEST.json`;
- `include.ini` starts with `skip: true`, then has `116` opt-in entries and `74` skip entries;
- upstream metadata contains `154382` expected markers and `145965` fail markers, with separate WebGL and WebGPU expectation surfaces;
- WPT-hosted Test262 data is vendored from `tc39/test262` at `b66872a92487694396fb082343e08dd7cca5ddf4` and includes `53441` `.js` tests under `third_party/test262/test`.

Inference:

`ADR9-EV-013` can move from missing to partial because WPT/Test262 denominator and corpus-planning evidence now exists. No compatibility result exists, and WPT-hosted Test262 evidence does not satisfy Turing's `ADR-0004` runtime harness requirement.

Affected records:

- `docs/research/servo-local-compatibility-corpus-2026-07.md`;
- `docs/blueprint-v1/machine/adr-0009-evidence.json`;
- `docs/blueprint-v1/machine/pre-build-readiness.json`;
- `docs/project-buildout/11-pre-build-readiness-checklist.md`;
- `docs/project-buildout/13-build-readiness-operating-board.md`;
- `docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`;
- `docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`;
- `docs/README.md`;
- `docs/research/README.md`;
- `docs/repository-map.md`;
- `docs/blueprint-v1/22-research-program.md`.

Next evidence required:

Local compatibility corpus HTTPS harness, browser-run logs against the external Servo build, focused WPT subset runs for the selected `ADR-0009` option, disabled/expected/timeout/crash/unsupported-API accounting, flakiness policy, and a separate Turing Test262 harness plan for `ADR-0004`.

## 2026-07-16 — Performance, security, developer, and missing-systems research expansion

Question:

Which browser-scale domains still lacked implementation-grade research contracts after the first eight detailed books?

Sources and versions:

- Turing main at the 95-document engineering-library baseline;
- official WHATWG, W3C, RFC, TC39, WPT, platform, accessibility, reproducible-build, update-security, benchmark, and primary security sources retrieved 2026-07-16;
- existing Turing requirements, risks, work packages, benchmark schema, process capability registry, and prototype.

Method and environment:

Repository-wide architecture and documentation audit followed by deterministic generation of eleven new books, sixteen advanced performance/security/developer chapters, a dated audit, navigation, research questions, bibliography, and validator topology. No implementation, benchmark, conformance run, independent audit, or supported-feature evidence was produced.

Observations:

- network, storage, media/document, platform, accessibility, release, extension/enterprise/sync, web-platform governance, benchmark, quality, and everyday product areas required independent owners and evidence contracts;
- performance leadership requires locality, allocation, virtual-memory, IPC, startup, PGO, tail-latency, causal-trace, energy, pressure, and recovery work;
- security leadership requires native/JIT compartments, side-channel policy, capability provenance, privileged developer/extension/agent controls, trusted UI, phishing defense, update response, and independent assurance;
- developer leadership requires deterministic replay, safe local-workspace integration, automatic reduction, generated SDKs, and cross-domain causal explanations.

Decision:

- add eleven detailed books and 81 chapters;
- add sixteen advanced chapters to performance, security, and developer experience;
- publish the [expansion audit](research/performance-security-developer-expansion-audit-2026-07.md);
- add RQ-26 through RQ-40 and corresponding experiment families;
- strengthen the repository validator to require 204 Markdown documents and nineteen book indexes.

Security/privacy impact:

The research strengthens least authority, partitioning, brokered devices and sockets, native/JIT containment, update integrity, trusted UI, phishing defenses, redaction, private reporting, and explicit unsafe early-release warnings. It changes no current security claim.

Compatibility/accessibility impact:

The expansion adds open-web feature governance, full-denominator conformance, platform accessibility bridges, assistive-technology latency, browser UI workflows, and cross-browser protocol studies. It changes no support matrix.

Performance/memory/energy impact:

The expansion defines measurement and experiments for data locality, allocators, pages, IPC, scheduling, startup, PGO/LTO, GPU, 30 tabs, energy, thermal behavior, background work, and recovery. All proposed advantages remain unmeasured hypotheses.

Affected requirements, risks, ADRs, work packages, and documents:

- requirement count remains 46; risk count remains 40; work-package count remains 18;
- no ADR or status changes;
- all nineteen detailed book indexes, the documentation and Blueprint indexes, repository map, research index/log/program, bibliography, definition of done, policies, and validator are synchronized.

Next evidence required:

Run the fixed-hardware baseline, then execute the representation, process, sandbox, networking, storage, replay, accessibility, release, and product experiments defined by RQ-26 through RQ-40.

## 2026-07-16 — Detailed browser engineering research library

Question:

Where was the initial Blueprint too compressed to guide implementation research, and which detailed subsystem books were required before architecture experiments and code could proceed without inventing undocumented assumptions?

Sources and versions:

- complete Turing Blueprint and repository policies at merge commit `70f151f74a6e199415c7125169230ae1231fb561`;
- official Chromium, WebKit, Gecko, Servo, Ladybird, Rust, platform sandbox, W3C/WHATWG, WPT, BrowserBench, WebDriver BiDi, MCP, and browser-product sources retrieved 2026-07-16;
- W3C Web Platform Design Principles Group Note dated 2026-02-24;
- current MCP specification version identified as 2025-11-25 at retrieval;
- current official product/project pages recorded in the new competitive studies.

Method and environment:

Repository-wide documentation audit. The audit tested whether each major area had enough detail to define identities, inputs, outputs, ownership, lifetimes, invalidation, failure, security, accessibility, limits, observability, experiments, and acceptance evidence. No implementation, fixed-hardware benchmark, or independent security review was performed.

Observations:

- the 22 Blueprint chapters covered the correct browser-scale surface but several combined too many independently reviewable subsystems;
- implementation research needed deeper contracts for rendering, runtime, security, developer protocols, APIs, performance, agents, and comparative adoption;
- the existing documentation governance could support nested engineering books if indexes, repository mapping, research status, and validation were updated together;
- networking, storage, media, PDF, printing, native platform adapters, accessibility bridges, extensions, enterprise/sync, and release operations remain future detailed-book candidates.

Inference:

Keeping the Blueprint as the normative overview while adding indexed detailed books gives the project enough depth for experiments without prematurely freezing implementation. A large body of prose is useful only if status, ownership, evidence, and change discipline remain explicit.

Decision:

- add a [browser engine engineering book](engine/README.md);
- add a [JavaScript runtime engineering book](javascript/README.md);
- add a [browser security engineering book](security-engine/README.md);
- add a [developer experience and DevTools book](developer-experience/README.md);
- add an [API design book](api-design/README.md);
- add a [performance engineering book](performance/README.md);
- add an [AI and agent engineering book](ai/README.md);
- add [competitive browser and engine studies](competitive/README.md);
- publish the [documentation expansion audit](research/documentation-expansion-audit-2026-07.md);
- add RQ-18 through RQ-25 to the research program;
- document the repository-owner, documentation-only direct-main exception requested for the single-owner research phase;
- strengthen repository validation so the complete detailed-book topology is required.

Alternatives rejected:

- expanding only the existing Blueprint chapters, because they would become difficult to navigate and own;
- creating disconnected essays without canonical relationships, because they would drift;
- changing requirements, risks, ADRs, or work-package status based only on desk research;
- treating competitor architecture descriptions or vendor benchmarks as measured Turing evidence.

Security/privacy impact:

The new security and AI books deepen containment, platform sandbox evidence, unsafe/native governance, trusted UI, update response, semantic redaction, tool/MCP boundaries, and adversarial evaluation. They do not change the existing warning that Turing is not safe for hostile or sensitive browsing.

Compatibility/accessibility impact:

The engine, runtime, DevTools, API, competitive, and AI books reinforce standards-first development, full WPT/Test262 accounting, explicit unsupported behavior, semantic accessibility, platform assistive technology, keyboard workflows, and cross-browser automation.

Performance/memory/energy impact:

The performance and subsystem books establish representation budgets, critical-path graphs, semantic resource attribution, adaptive parallelism, cache and pressure policy, tail-latency rules, energy/startup/recovery measurement, and benchmark governance. These remain hypotheses until experiments run.

Licensing/operational impact:

The MPL-2.0 direction is unchanged. External implementations remain research and differential references. Primary sources are linked; no external source code was copied. The expansion increases maintenance load and requires future owners to refresh changing product/project information.

Affected requirements, risks, ADRs, work packages, and documents:

- no requirement, risk, ADR, or work-package status changed;
- root `README.md`;
- `AGENTS.md`;
- `docs/README.md`;
- `docs/start-here.md`;
- `docs/repository-map.md`;
- `docs/research/README.md`;
- `docs/blueprint-v1/README.md`;
- `docs/blueprint-v1/16-governance-contributing.md`;
- `docs/blueprint-v1/18-source-bibliography.md`;
- `docs/blueprint-v1/22-research-program.md`;
- `tools/validate_blueprint.py`;
- all new documents under the eight detailed book directories;
- the dated documentation audit.

Unresolved questions:

See RQ-18 through RQ-25 and each new book's evidence and risk sections. The most immediate empirical gap is the fixed-hardware cross-engine baseline.

Next evidence required:

Execute issue #14, then build the smallest engine-artifact, process-topology, platform-sandbox, protocol, runtime-tiering, and scheduling prototypes needed to falsify the proposed designs.

## 2026-07-16 — Browser engine landscape and excellence strategy

Question:

Which documented lessons from Chromium, WebKit, Gecko, Servo, and Ladybird should guide a top-tier independent engine for developers and everyday users?

Sources and versions:

- official engine architecture and source documentation retrieved 2026-07-16;
- WebDriver BiDi Editor's Draft dated 2026-07-15;
- W3C Web Platform Design Principles Group Note dated 2026-02-24;
- Interop 2026 material published 2026-02-12;
- current WPT and BrowserBench documentation.

Method and environment:

Architecture and standards comparison only. No comparative fixed-hardware performance run was performed, so the report does not rank engines by unmeasured speed, memory, energy, security, or compatibility.

Observations:

- production engines converge on multiprocess isolation, specialized services, staged rendering, and tiered JavaScript execution;
- Chromium provides the broadest developer-protocol and compatibility reference;
- WebKit and Gecko provide additional process, broker, platform, runtime, and observability lessons;
- Servo and Ladybird are the closest independent-engine research peers;
- stable APIs, adaptive parallelism, semantic resource ownership, and standards-aligned tests are major opportunities for differentiation.

Inference:

Turing should pursue a measured synthesis rather than clone one architecture. “Number one” must be a reproducible multi-dimensional scorecard covering compatibility, latency, memory, energy, security, accessibility, stability, developer APIs, and open-source health.

Decision:

- add a permanent [research index](research/README.md);
- publish the [browser engine landscape and Turing excellence strategy](research/browser-engine-landscape-2026-07.md);
- add formal research questions for competitive architecture measurement and developer-protocol design;
- keep all recommendations exploratory until falsifiable experiments and existing decision gates are satisfied.

Security/privacy impact:

The study reinforces site isolation, capability-separated processes, brokered privileged access, authenticated developer attachment, bounded protocols, trusted UI, and data minimization.

Compatibility/accessibility impact:

The study reinforces WPT, Test262, WebDriver BiDi, Interop tracking, explicit unsupported behavior, accessibility semantics, and manual assistive-technology validation.

Performance/memory/energy impact:

The study prioritizes end-to-end user latency, adaptive parallelism, immutable/versioned artifacts, semantic resource accounting, fixed-hardware baselines, tail latency, 30-tab disclosure, and energy measurement.

Licensing/operational impact:

The MPL-2.0 decision is unchanged. The study adds open benchmark data, public protocol schemas, reproducible results, and contributor-health metrics as leadership criteria.

Affected records:

- root `README.md`;
- `docs/README.md`;
- `docs/repository-map.md`;
- `docs/blueprint-v1/README.md`;
- `docs/blueprint-v1/22-research-program.md`;
- this research log;
- the two documents under `docs/research/`.

Unresolved questions:

See the study's experiment queue and unresolved-question section.

Next evidence required:

A fixed-hardware, versioned, reproducible reference-engine baseline using equivalent workloads, security settings, process disclosure, and compatibility accounting.

## 2026-07-16 — Professional buildout gap audit

A repository-wide review found that the remaining gap was the project control plane rather than another disconnected subsystem survey. The change adds professional phase, ownership, decision, traceability, repository, build, coding, API/configuration, cross-cutting review, release, legal, data, product, documentation, sustainability, Servo, Plug-in, and embedding baselines. It changes no implementation, requirement, risk, or support status.

<!-- MARKET-STRATEGY-2026-07 -->
## 2026-07-16 — Project-browser market gap

Added the Market Strategy and Differentiation book, dated browser-market study, `OP-001` through `OP-014` registry, opportunity-promotion template, cross-document product hypotheses, and validator coverage. No opportunity became an accepted requirement, implementation claim, risk status, or support promise.

<!-- MARKET-RQ-ID-CORRECTION-2026-07 -->
## 2026-07-16 — Research-question identifier correction

Renumbered market-differentiation studies from the conflicting `RQ-45`–`RQ-50` range to `RQ-49`–`RQ-54`, preserving `RQ-45`–`RQ-48` for the professional-buildout program. Added a repository validator that requires globally unique, contiguous research-question headings. No research conclusion, requirement, risk, work package, implementation status, or support claim changed.

## 2026-07-16 — Market strategy consistency and validator hardening

After the market-strategy merge, a repository-wide audit corrected canonical table placement, added explicit product ownership, normalized release-review scope naming, and extended validation to `OP-*` IDs, reviewer-to-owner resolution, and market index invariants. No opportunity was promoted and no implementation or support status changed.

## 2026-07-15 — Canonical documentation system

Decision:

- place canonical prose under `docs/`;
- retain root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md` only for discovery and repository control;
- place the complete Blueprint under `docs/blueprint-v1/`;
- keep machine-readable requirements, risks, backlog, process capabilities, benchmark manifests, and agent-action schemas beside the Blueprint;
- require same-change documentation for code, configuration, dependencies, interfaces, features, risks, and repository structure;
- add static link, location, registry, index-coverage, and diff-based documentation validation;
- remove temporary transfer and self-modifying bootstrap machinery from the durable repository structure.

Rationale:

A browser project has too many cross-cutting security, compatibility, performance, accessibility, and operational obligations for documentation to be optional or scattered. Centralizing canonical prose and requiring impact review reduces silent drift while preserving standard GitHub discovery files.

Affected records:

- root `AGENTS.md`;
- `docs/documentation-policy.md`;
- `docs/repository-map.md`;
- `docs/contributing.md`;
- GitHub issue and pull-request templates;
- repository validation workflow and tools.

Residual risk:

Automation can verify location, links, registries, and minimum same-change behavior, but it cannot prove that prose is semantically complete. Human and agent review must still apply the full impact matrix.

## Entry template

```text
## YYYY-MM-DD — Topic

Question:
Sources and versions:
Method and environment:
Observations:
Inference:
Decision:
Alternatives rejected:
Security/privacy impact:
Compatibility/accessibility impact:
Performance/memory/energy impact:
Licensing/operational impact:
Affected requirements, risks, ADRs, work packages, and documents:
Unresolved questions:
Next evidence required:
```
## 2026-07-19 - Fresh-host toolchain reproduction closure preparation

Question:

What exact replay and review evidence can close `PB-008`/`PB-009` without treating a current-host rerun or a checked template as independent reproduction?

Inputs:

- [Build Information Readiness Ledger](research/build-information-readiness-ledger-2026-07.md);
- [Fresh Host Reproduction Inventory](research/fresh-host-reproduction-inventory-2026-07.md);
- [Fresh-Host Toolchain Reproduction Closure Preparation](research/fresh-host-toolchain-reproduction-closure-preparation-2026-07.md);
- the checked fresh-host registries, schemas, templates, validators, and `TASK-000002` route.

Method:

Consolidated evidence classes for reference hosts, same-host reruns, clean-VM equivalents, and independent fresh hosts. Defined pre-run facts, the bootstrap/doctor/check/`xtask` replay sequence, retained command-log/hash requirements, cache and target-directory controls, source-tree cleanliness proof, failure denominator, cleanup/rollback record, and owner-review axes.

Decision:

Keep `PB-008` and `PB-009` partial. This is a no-claim replay and review contract only; it does not execute `TASK-000002`, produce independent toolchain or fresh-host evidence, approve a clean-VM waiver, promote either gate, or support broad implementation, release, production, performance, compatibility, security, accessibility, or Chrome-class claims.

Next question:

Which owner-approved `TASK-000002` execution environment will produce the first retained run record and readiness review?
## 2026-07-19 - IPC transport and authority closure preparation

Question:

What evidence order separates `TASK-000011` M0 policy review, wire-format selection, and later real-transport proof without expanding IPC authority or claims?

Inputs:

- [IPC Capability Boundary Inventory](research/ipc-capability-boundary-inventory-2026-07.md);
- [WP-002 kernel identity, capability, and bounded IPC reference](research/wp-002-kernel-ipc-2026-07.md);
- [TASK-000011 WP-002 Review Handoff](research/task-000011-wp002-review-handoff-2026-07.md);
- [IPC Wire-Encoding Decision Preparation](research/ipc-wire-encoding-decision-prep-2026-07.md);
- the specified `TASK-000003` and `TASK-000011` manifests, schemas, templates, validators, and non-accepting evidence capture.

Method:

Separated the M0 policy-reference review, wire decision, and transport execution scopes. Added a no-claim sequence for exact-commit independent review, explicit encoding disposition, control-envelope freeze, per-platform authenticated transport experiments, hostile/negative coverage, lifecycle/resource accounting, and owner-reviewed readiness. Added rejection rules for using a template, in-process test, generated output, or passing validator as production IPC evidence.

Decision:

Keep `PB-011` partial. The new route improves execution traceability only; it does not accept `TASK-000011`, select a wire codec or generator, authorize a platform transport, approve `TASK-000003`, promote IPC readiness, or support renderer-security, agent-security, process-isolation, site-isolation, production IPC, or Chrome-class claims.

Next question:

Which owner-approved reviewer will produce the first independent `TASK-000011` evidence bundle on the exact commit?
## 2026-07-19 - Sandbox probe execution and containment closure preparation

Question:

What execution and review order can convert the `WP-003` probe contract into platform containment evidence without counting stubs or policy names as sandbox proof?

Inputs:

- [Sandbox Probe Inventory](research/sandbox-probe-inventory-2026-07.md);
- [WP-003 Sandbox Probe Contract](research/wp-003-sandbox-probe-plan-2026-07.md);
- [Sandbox Platform-Evidence Decision Preparation](research/sandbox-platform-evidence-decision-prep-2026-07.md);
- the specified `TASK-000004` manifest, probe catalog, evidence schema, package/readiness-review templates, security policy, and platform containment book.

Method:

Separated role/authority freeze, host-safe fixture preparation, unsandboxed controls, real constrained-role launch, expected-deny operations, compromised-client/lifecycle cases, per-platform effective-policy capture, full-denominator artifact retention, and owner-reviewed readiness. Added explicit rejection rules for application-level stubs, policy names without effective state, substituted helper processes, unsupported primitives treated as pass, success-only logs, and templates treated as containment evidence.

Decision:

Keep `PB-012` partial. The new route improves execution traceability only; it does not execute `TASK-000004`, prove platform containment, satisfy `SEC-GATE-1` or `SEC-GATE-6`, promote sandbox readiness, or support renderer-security, site-isolation, hostile-browsing, production-safety, or Chrome-class claims.

Next question:

Which owner-approved platform and real process role will produce the first reviewed sandbox probe package with an unsandboxed control?
## 2026-07-19 - Benchmark evidence and claim closure preparation

Question:

What transition separates benchmark infrastructure self-tests, browser-run diagnostics, competitor comparisons, and public Chrome-class or extreme-performance claims?

Inputs:

- [Performance Benchmark Readiness Packet](research/performance-benchmark-readiness-packet-2026-07.md);
- [Chrome-Class Performance Runbook](research/chrome-class-performance-runbook-2026-07.md);
- [Benchmark Engine Baseline Harness Readiness Map](research/benchmark-engine-baseline-harness-readiness-map-2026-07.md);
- [Benchmark Statistics Analysis Contract](research/benchmark-statistics-analysis-contract-2026-07.md);
- benchmark manifests, browser-pin capture contracts, competitor inventories, runner self-tests, and the specified `TASK-000005` manifest.

Method:

Separated L0 contract/self-test evidence, L1 local browser-run diagnostics, L2 equal-workload competitor diagnostics, and L3 owner-reviewed public-claim candidates. Defined identity/control capture, runner and browser-run transitions, raw artifact and failure-denominator requirements, competitor pinning, statistical treatment, claim wording, expiry, rerun triggers, and rejection rules for silent reduction or unequal security/lifecycle settings.

Decision:

Keep `PB-013` partial and `TASK-000005` proposed-only. The new route improves evidence and claim traceability only; it does not run a browser, approve hardware, produce a competitor result, accept statistics, promote benchmark readiness, or support faster, lower-memory, lower-energy, Chrome-class, compatibility, production, or daily-driver claims.

Next question:

Which owner-approved fixed host and no-real-profile browser-run configuration will produce the first reviewed L1 diagnostic package?
## 2026-07-19 - Native UI and accessibility closure preparation

Question:

What evidence order can connect toolkit selection, page-surface composition, component fixtures, input/IME, and assistive technology without expanding toolkit authority?

Inputs:

- [Toolkit-Neutral UI Adapter Contract Inventory](research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md);
- [Native UI Framework Bake-Off Inventory](research/native-ui-framework-bakeoff-inventory-2026-07.md);
- [Native UI Component Fixture Inventory](research/native-ui-component-fixture-inventory-2026-07.md);
- [Page Surface Composition Inventory](research/page-surface-composition-inventory-2026-07.md);
- [Window Input Accessibility Spike Inventory](research/window-input-accessibility-spike-inventory-2026-07.md);
- UI-runtime/accessibility machine registries, readiness-review templates, and specified `TASK-000006` manifest.

Method:

Connected toolkit-neutral contracts, equivalent adapter runs, authority-separation tests, page-surface identity and fault evidence, component fixtures, reference-platform workflows, manual assistive-technology review, performance/recovery traces, and cross-lane owner review. Added rejection rules for toolkit-owned authority, substituted renderers, semantic models treated as platform accessibility proof, stale surface identity, and one-toolkit or one-platform leadership claims.

Decision:

Keep `PB-003`, `PB-004`, `PB-005`, `PB-014`, and `PB-015` partial and `TASK-000006` proposed-only. The new route improves execution traceability only; it does not select a toolkit, accept an ADR, satisfy `UI-GATE-7`/`UI-GATE-10`, promote accessibility or trusted-chrome readiness, or support release-path UI, performance, Chrome-class, production, or implementation claims.

Next question:

Which owner-approved toolkit-neutral adapter slice and reference platform will produce the first reviewed native UI/accessibility evidence package?
# 2026-07-19 - Profile/session execution and data-safety closure preparation

Question:

What evidence must replace the checked profile/session planning templates before `PB-016` or `TASK-000007` can be treated as executable or data-safety evidence?

Inputs:

- [Profile Session Format Inventory](research/profile-session-format-inventory-2026-07.md);
- [Profile and Session Data-Lifecycle Decision Preparation](research/profile-session-data-lifecycle-decision-prep-2026-07.md);
- [profile-session-format-inventory.json](storage/machine/profile-session-format-inventory.json);
- checked no-claim schema-package and readiness-review templates;
- `TASK-000007` and the `PB-016` continuation/readiness records.

Method:

Added a no-claim closure route that sequences synthetic-fixture schema execution, forward/resume/rollback/downgrade migration, disk-full/power-loss/partial-write/corruption/crash fault injection, privacy and origin/private-session isolation, recovery and protected-work accounting, and named owner/independent review. Added rejection rules for real profiles, secrets, success-only evidence, silent downgrade/deletion, missing denominators, and template-only readiness.

Decision:

Keep `PB-016` partial and `TASK-000007` specified/proposed-only. The new report improves the handoff from planning templates to an evidence packet but does not approve profile implementation, real-profile migration, sync, credential storage, private-session readiness, protected-work readiness, data-loss safety, user-data handling, a production profile format, or release-path behavior.

Impact:

The profile/session lane now has one explicit execution and review sequence tied to the state-class decisions, machine ledger, crosswalk, continuation pack, and documentation audit. The next acceptable artifact is a retained synthetic-fixture execution packet with redacted logs, hashes, fault coverage, migration transitions, recovery accounting, cleanup evidence, and named review.

Next question:

Which synthetic profile/session schema package and fault boundary should be implemented first under a separately reviewed immutable task manifest?
# 2026-07-19 - Profile/session closure route synchronization

Question:

Did the profile/session execution and data-safety closure route reach every canonical human-facing handoff that describes `PB-016` and `TASK-000007`?

Method:

Audited the task queue, pre-build checklist, build-readiness start guide, documentation-readiness evidence matrix, storage book, product-experience book, research index, continuation pack, operating board, machine crosswalk, build-information ledger, and documentation-readiness audit. Added the closure-preparation report to stale template-only routes and made the required evidence sequence consistent: synthetic fixtures, executable schema harness, migration/fault/recovery accounting, privacy isolation, and named owner review.

Decision:

The route is now synchronized without changing `PB-016` from `partial` or `TASK-000007` from proposed/specified-only. No profile implementation, real-profile migration, sync, credential storage, data-loss safety, user-data handling readiness, production profile format, or release-path claim was made.

Validation:

Focused profile/session, audit, Blueprint-link, and diff checks passed. The full PowerShell aggregate check passed with 387 Markdown files and 5,179 relative links; only existing CRLF normalization warnings were emitted.

Next question:

Which owner-reviewed dependency lane should produce the first real evidence packet after a reviewed immutable task manifest is approved?
# 2026-07-19 - Closure-preparation route index synchronization

Question:

Do the dated closure-preparation reports have one coherent stop/resume route across the root docs entrypoint, operating board, task queue, evidence matrix, continuation pack, research index, crosswalk, and machine ledgers?

Method:

Compared all seven active closure-preparation reports for `PB-002`, `PB-008`/`PB-009`, `PB-011`, `PB-012`, `PB-013`, native UI/accessibility, and `PB-016` against their canonical references. Added a shared route index to the operating board, proposed task queue, evidence matrix, and root documentation entrypoint, and repaired missing lane-specific references in the continuation pack and stop/resume prose.

Decision:

Keep every lane no-claim and below owner-reviewed readiness. The route index is documentation organization and evidence sequencing only; it does not approve a task, source, toolkit, transport, sandbox policy, benchmark claim, profile format, production path, or broad build.

Impact:

Maintainers can now start from one cross-lane closure route and reach the matching report before shaping a reviewed immutable task manifest. The canonical percentage remains unchanged because route completeness does not equal owner-reviewed evidence or decision closure.

Next question:

Which first closure packet will receive the required named owner and independent review record without weakening the no-claim boundaries?
# 2026-07-19 - Operational closure-preparation contracts

Question:

Can the package/update, incident-response, backup-ownership, and `PB-020` closure lanes use the same evidence-order and review discipline as the engineering lanes?

Method:

Added no-claim execution/review preparation reports for `PB-017`/`TASK-000009`, `PB-018`/`TASK-000010`, and `PB-019`/`PB-020`/`TASK-000008`. Each report defines synthetic or fake-key fixtures, ordered evidence, fault and failure accounting, privacy/access controls, rejection rules, named owner and independent review, and explicit unsupported authority boundaries. Synchronized the reports through the research index, root docs index, route crosswalk, build-information ledger, documentation audit, repository map, task queue, operating board, evidence matrix, and continuation pack.

Decision:

Keep `PB-017` and `PB-018` partial, `PB-019` blocked, and `PB-020` unresolved. The reports improve documentation completeness and stop/resume continuity but do not approve an updater, signing hierarchy, incident authority, disclosure, qualified backups, two-person control, release path, production authority, or broad build.

Impact:

All ten active closure routes now have a common no-claim handoff shape before a task can become a reviewed immutable execution manifest. The documentation percentage remains a gate measure: route completeness does not equal owner-reviewed evidence or readiness closure.

Next question:

Which operational evidence packet can be reviewed first without using production keys, live incident data, placeholder owners, or unbounded authority?
# 2026-07-19 - Operational closure routes added to primary entrypoints

Question:

Can a maintainer starting from `Start Here`, the progress snapshot, or the owner-decision board reach the same package/update, incident-response, and backup-ownership closure packet as the machine registries and research index?

Method:

Audited the root README, `docs/start-here.md`, the progress snapshot, and the owner-decision closure board after adding the three operational closure-preparation reports. Added each report to the primary human handoff surfaces and preserved the existing no-claim status and owner-decision boundaries.

Decision:

The operational lanes are now discoverable from the primary entrypoints, but `PB-017`/`PB-018` remain partial, `PB-019` remains blocked, and `PB-020` remains unresolved. Entry-point completeness does not establish execution evidence, authority, or full-build readiness.

Impact:

A stopping or continuing maintainer can follow the same route from root orientation through the owner board, task queue, closure report, evidence matrix, machine crosswalk, and validation commands without relying on chat history.

Next question:

Which owner-approved evidence packet should be admitted into the closure board first, with all names, hashes, review records, and exception expiry fields populated?
# 2026-07-19 - Progress and readiness-claim consistency audit

Question:

Do the repository's documented percentages, gate distributions, and broad-build statements still match the authoritative documentation-readiness and build-information registries after the closure-route expansion?

Method:

Searched the root README, documentation index and policy, start page, progress snapshot, owner-decision board, research index, repository map, Blueprint research program, implementation audit, capability traceability map, and current readiness reports for percentage, broad-build, all-information-ready, and documentation-completion claims. No contradictory percentage or authorization claim was found. Added the three operational closure routes to the completion-audit blocker table so the prose audit points directly to the same package/update, incident-response, and backup-ownership evidence contracts as the machine records.

Decision:

Retain **90% contained-M0 documentation organization** and **0% full-build closure**. The percentages remain machine-audited gate measures, not document-count estimates. No readiness or owner decision was promoted.

Next question:

Which owner-reviewed decision record can change a machine-audited criterion without weakening the broad-build claim boundary?

# 2026-07-19 - PB-020 closure and owner-decision preparation

Question:

Does the checked closure-review template have a usable final handoff without being mistaken for an approval record?

Method:

Reviewed the closure schema and no-claim template, implementation kickoff inventory, dependency graph, owner-decision board, documentation audit, and current continuation surfaces. Added a human-readable closure-preparation route that defines evidence collection order, decision-record fields, immutable task-authority checks, named owner and independent review, exception handling, rejection rules, and the promotion boundary. Linked it from all relevant discovery, tracking, and repository-index documents.

Decision:

Keep `PB-020` partial and preserve **90% contained-M0 documentation organization** and **0% full-build closure**. The new route improves stop/resume continuity and does not authorize tasks, close gates, or establish all-information-ready-for-building.

Next question:

Which named owner-reviewed gate record, with retained evidence and independent review, is ready to replace a no-claim template?

# 2026-07-19 - PB-020 closure handoff entrypoint synchronization

Question:

Do the one-screen and first-entry documents point to the same final closure-preparation route as the indexes and machine audit?

Method:

Added the PB-020 closure and owner-decision preparation report to the progress snapshot, Start Here, root README, and machine documentation-audit evidence references. Re-ran the documentation-readiness validator and relative-link validation.

Decision:

The closure route is now reachable from every primary stop/resume entrypoint. The audit remains 9 of 10 criteria ready for contained M0 and 0 of 10 ready for the full goal; no owner decision or readiness state changed.

Next question:

Which unresolved lane can produce the next real, independently reviewed evidence packet without expanding authority or weakening claim boundaries?

# 2026-07-19 - ADR-0009 closure-route synchronization

Question:

Can a maintainer reach the source-strategy evidence-order handoff from every primary `PB-002` continuation surface?

Method:

Compared the ADR-0009 closure-preparation report, source packet, evidence matrix, decision draft, evidence registry, operating board, continuation pack, and owner-decision board. Added the closure-preparation route to the ordered `PB-002` continuation step, both source-strategy readiness tables, and the owner-decision action row.

Decision:

The source-strategy documentation route is now coherent and still explicitly no-claim. `PB-002` remains blocked because the evidence registry is partial/blocked and no owner-reviewed decision exists.

Next question:

Which `ADR9-EV-*` item can be converted from preparation to independently reproduced evidence under an approved, immutable task manifest?

# 2026-07-19 - Fresh-host closure-route synchronization

Question:

Can a maintainer reach the same pinned-toolchain and fresh-host evidence-order contract from the ordered operating path, progress snapshot, and owner-decision board?

Method:

Compared the fresh-host reproduction inventory, run-record and readiness-review templates, closure-preparation report, task queue, operating board, progress snapshot, and owner-decision board. Added the closure route to the ordered `PB-008`/`PB-009` step, the progress dashboard, and the owner-decision action row.

Decision:

The lane is now coherently routed without changing its status. `PB-008` and `PB-009` remain partial, `TASK-000002` remains proposed-only, and no fresh-host, reproducibility, release-confidence, or broad-build claim is supported.

Next question:

Which evidence lane can be executed only after a reviewed immutable task manifest is available?

# 2026-07-19 - Cross-lane closure index and IPC/sandbox route synchronization

Question:

Does the documentation readiness matrix and owner board expose both the final PB-020 reconciliation route and the security-lane evidence order?

Method:

Compared the operating-board route index, task-queue route index, documentation-readiness evidence matrix, owner-decision board, IPC closure report, sandbox closure report, and primary stop/resume pages. Added the final PB-020 route to the cross-lane indexes and linked the IPC and sandbox closure reports from their owner-decision actions.

Decision:

The closure indexes now cover all ten evidence lanes plus final PB-020 reconciliation. IPC and sandbox remain partial; templates and validators do not establish transport, containment, renderer-security, site-isolation, or production claims.

Next question:

Which security-lane evidence packet can be admitted only after task authority, source identity, and independent review are present?

# 2026-07-19 - Benchmark and extreme-performance route synchronization

Question:

Can the Chrome-competitor performance objective be followed from the progress dashboard and task/owner decisions to one claim-gated evidence contract?

Method:

Compared the Chrome-class performance lane map, benchmark evidence and claim closure preparation, statistics-analysis contract, benchmark readiness and claim-bundle templates, task queue, progress snapshot, and owner-decision board. Added the closure route to the `PB-013` owner action, `TASK-000005` handoff, and performance research dashboard.

Decision:

The performance route is now coherent and remains explicitly no-claim. `PB-013` is still documented without a browser runner, `TASK-000005` remains proposed-only, and no speed, memory, energy, competitor, Chrome-class, or daily-driver claim is supported.

Next question:

What reviewed L1 browser-run evidence packet must exist before any competitor comparison is even considered?

# 2026-07-19 - Native UI and accessibility route synchronization

Question:

Can a maintainer reach the native-shell, page-surface, IME, and assistive-technology evidence order from the task, owner, and progress records?

Method:

Compared the native UI/accessibility closure report, native readiness-review template, component/page-surface/window-input inventories, `TASK-000006`, the progress snapshot, and the owner-decision board. Added the closure route to the native owner action, task handoff, and native research dashboard.

Decision:

The native-shell route is now coherent and remains no-claim. `PB-003`, `PB-004`, `PB-005`, `PB-014`, and `PB-015` remain partial; `TASK-000006` remains proposed-only; no toolkit, trusted-chrome, page-surface, accessibility, screen-reader, or release-path UI claim is supported.

Next question:

Which native workflow evidence can be reviewed without selecting a release toolkit or granting toolkit-owned authority?

# 2026-07-19 - Profile and session data-safety route synchronization

Question:

Can a maintainer reach the profile/session migration and data-loss evidence order from the task, owner, and progress records before real user data is involved?

Method:

Compared the profile/session format inventory, lifecycle decision preparation, execution/data-safety closure report, schema-package and readiness-review templates, `TASK-000007`, the progress snapshot, and owner-decision board. Added the closure route to the `PB-016` owner action and profile/session research dashboard.

Decision:

The profile/session route is now coherent and remains no-claim. `PB-016` remains partial, `TASK-000007` remains proposed-only, and no real-profile migration, sync, credential, private-session, protected-work, data-loss, or production-format claim is supported.

Next question:

Which synthetic-fixture migration packet can demonstrate fault and recovery behavior without accessing real user data?

# 2026-07-19 - Package/update release-safety route synchronization

Question:

Can a maintainer reach the package identity, fake-key, rollback, migration, and release-safety evidence order from the owner and progress records?

Method:

Compared the package/update lab inventory, trust decision preparation, execution/release-safety closure report, package and readiness-review templates, `TASK-000009`, the progress snapshot, and owner-decision board. Added the closure route to the `PB-017` owner action and package/update research dashboard.

Decision:

The package/update route is now coherent and remains no-claim. `PB-017` remains partial, `TASK-000009` remains proposed-only, and no package format, updater, signing, stable-channel, rollback-safety, supported-security, release, or production claim is supported.

Next question:

Which fake-key local lab packet can demonstrate metadata and staged-install failure handling without approaching production release authority?

# 2026-07-19 - Owner-decision board scope synchronization

Question:

Does the human owner-decision closure board preserve the same canonical gate scopes as the machine synchronization matrix?

Method:

Compared the owner-decision closure board, synchronization matrix, closure-review template, pre-build readiness, and both owner-decision validators. The check found that the board combined `PB-019` backup ownership and `PB-020` build-readiness closure even though the machine matrix treats them as separate scopes.

Decision:

Split the board into distinct `PB-019` and `PB-020` rows and added a validator check requiring exactly 11 board decision-lane scopes to match the machine matrix. Backup ownership and build-readiness closure remain unresolved and no-claim.

Next question:

Which owner-reviewed evidence packet can close one of the separate scopes without conflating backup coverage with readiness promotion?

# 2026-07-19 - Research packet ownership metadata audit

Question:

Can a maintainer identify the status and responsible role for every durable research packet without inferring ownership from a linked gate?

Method:

Scanned all 103 indexed durable research Markdown files for explicit `Status` and `Owner` metadata, then compared the missing entries with each packet's gate, scope, and existing governance language.

Decision:

Added role-based owner metadata to the nine previously incomplete packets and the final closure-record example found during validation. Strengthened `validate_research_index.py` so future durable research files cannot enter the index without both fields. This improves handoff metadata only and does not promote any gate or research claim.

Next question:

Which remaining research packets require a dated evidence-refresh trigger beyond their owner and status metadata?

# 2026-07-19 - JavaScript JIT requirement routing audit

Question:

Can accepted baseline-JIT and hardened no-JIT requirements be followed from the requirements registry into design, work-package, milestone, dependency, and evidence planning without implying implementation?

Method:

Compared `REQ-JS-004` and `REQ-JS-005` across the requirements registry, professional traceability, Blueprint 06, the JavaScript engineering book, M6 implementation plan, work-package playbooks, backlog, execution graph, task sequence, and Chrome-class traceability map. The audit found that the M6 prose existed but no canonical work package or design references routed the two requirements.

Decision:

Added planned `WP-019` for baseline JIT and hardened JavaScript execution, synchronized the backlog, dependency graph, roadmap, M6 sequence, playbook, and traceability records, and preserved explicit no-claim status. `WP-019` remains non-executable until its interpreter/GC, W^X, differential, no-JIT, security, and owner-review gates are satisfied.

Next question:

Which accepted requirement family next lacks a dedicated work-package or verification route after the JavaScript runtime correction?

# 2026-07-19 - Accepted requirement to work-package coverage audit

Question:

Does every accepted requirement have a canonical work-package owner and design route before implementation planning is considered complete?

Method:

Compared all 46 accepted requirements with the work-package backlog, execution graph, implementation plan, professional traceability, and Chrome-class capability map. The audit found six unmapped requirements: web-content accessibility bridging, WebAssembly, CORS/CSP policy, supported-version and emergency-patch capacity, ephemeral private sessions, and history/bookmarks/downloads/settings surfaces.

Decision:

Attached five requirements to their existing domain packages, added design references, and created planned `WP-020` for everyday product surfaces and browser workflows. Synchronized the roadmap, implementation plan, dependency graph, task sequence, traceability records, and capability map. All 46 requirements now have work-package coverage; no implementation, acceptance, compatibility, security, accessibility, product, or performance claim was promoted.

Next question:

Which accepted requirements still lack non-empty verification or evidence plans after their ownership routes are present?

# 2026-07-19 - Work-package playbook completeness control

Question:

Can a maintainer rely on every canonical work package having an executable documentation shape before task manifests are considered?

Method:

Audited all 20 backlog packages against `16-work-package-playbooks.md` for a package section, acceptance criteria, negative tests, handoff, and unsupported-scope statement. Separately checked that the union of package requirement mappings covers all 46 accepted requirements without unknown IDs.

Decision:

The current playbooks satisfy those conditions. Strengthened `validate_implementation_plan.py` to enforce them on every future change. This validates documentation structure and requirement routing only; it does not approve a package, task, implementation, or readiness gate.

Next question:

Which evidence class still has no package-specific collection route beyond generic acceptance prose?

# 2026-07-19 - Professional requirement design-route audit

Question:

Can every accepted requirement be traced from the stable registry to canonical design sources before implementation begins?

Method:

Compared all 46 requirements in `professional-traceability.json` with the owning Blueprint and detailed engineering books. Thirty-six requirements had empty design arrays despite existing canonical design material.

Decision:

Added existing canonical design sources for all 46 requirements. Implementation, source adoption, tests, reviews, and evidence remain empty unless separately supported. Strengthened `validate_blueprint.py` so future changes cannot omit design routes or point at missing files.

Next question:

Which requirement-specific verification or evidence route should be formalized first after design routing is complete?

# 2026-07-19 - Requirement verification matrix audit

Question:

Does every accepted requirement have a concrete verification and evidence-collection route before implementation work is approved?

Method:

Compared all 46 accepted requirements, 20 work packages, the implementation evidence catalog, professional traceability registry, detailed engineering books, and existing no-claim readiness lanes. Forty-four requirements had no explicit planned test or evidence route; the two existing reference-test records were not production evidence.

Decision:

Added the no-claim Requirement Verification Matrix with 11 domain lanes. Each lane records requirement coverage, work-package ownership, existing source documents, evidence classes, test layers, negative and failure cases, required artifacts, and a next-proof condition. Added validator enforcement for exact 46-requirement coverage, valid work packages/evidence classes, and existing source paths. This creates a verification plan without populating actual tests, reviews, or evidence in professional traceability.

Next question:

Which owner-approved evidence lane should be selected first after the unresolved source-strategy, fresh-host, IPC, sandbox, native-shell, and ownership gates are closed?

# 2026-07-19 - Requirement verification navigation sync

Question:

Can a maintainer reach the planned verification layer from both the requirements handbook and the documentation-readiness evidence matrix without relying on chat history?

Method:

Reconciled the new requirement verification matrix, professional traceability registry, requirements registry, work-package backlog, implementation evidence catalog, project-buildout handbook, documentation-readiness matrix, documentation index, and repository navigation.

Decision:

Added explicit inbound routes from the requirements/evidence handbook, documentation-readiness matrix, and stop/resume documentation index. The synchronization clarifies that planned verification is distinct from actual source, tests, reviews, and evidence and does not change the 90% contained-M0 or 0% full-build measurements.

Next question:

Which planned verification lane should receive the first owner-approved task manifest after the remaining source-strategy and readiness gates are resolved?

# 2026-07-19 - Semantic maturity-language audit

Question:

Do canonical entry points distinguish the validation-backed M0 foundation from browser implementation, supported capability, production readiness, and Chrome-class claims?

Method:

Scanned the root README, documentation index, project-buildout handbook, Blueprint chapters, readiness records, research packets, and validator policy markers for maturity terms such as implemented, verified, supported, complete, production-ready, compatible, faster, and Chrome-class. Compared each positive statement with its surrounding scope and claim boundary.

Decision:

Reworded the root README heading from `Implemented foundation` to `Contained M0 foundation currently present and validation-backed` and added the requirement verification matrix to the root canonical-status route. No unsupported product, security, compatibility, performance, accessibility, release, or production claim was found or promoted.

Next question:

Which remaining human-facing status statement should be reviewed after the next evidence lane changes its maturity state?

# 2026-07-19 - Servo upstream freshness refresh

Question:

Has upstream Servo moved since the dated `ADR-0009` provenance and maintenance evidence, and does that change any Turing source-strategy conclusion?

Method:

Read the official `servo/servo` GitHub repository, `main` branch, latest-release API, and crates.io package metadata on 2026-07-19. Compared the refreshed observations with the 2026-07-17 provenance, security/maintenance, and ADR-0009 packet records. No upstream checkout, source archive, build, dependency extraction, or artifact was copied into Turing.

Decision:

Recorded that upstream `main` now points to `736ad1bda08c1af419aadc903e82938f8610a65d` and that the repository was pushed/updated on 2026-07-19. The latest release remains immutable `v0.3.0` and the latest crates.io package remains `servo 0.4.0`. The prior build comparison is explicitly historical; no build, compatibility, security, performance, license, maintenance, or source-baseline conclusion transfers to the newer `main` commit, and `PB-002` remains blocked.

Next question:

Will an owner select the historical build baseline, refresh and rebuild upstream `main`, select the release/archive/package surface, or reject Servo as a release-code source?

# 2026-07-19 - Current-host toolchain wrapper diagnostic

Question:

Does the documented Windows doctor entry point execute against the pinned contained-M0 toolchain without changing the fresh-host claim boundary?

Method:

Ran `tools/doctor.ps1 --ci` from the current checkout with `CARGO_TARGET_DIR` set to `%TEMP%\turing-current-host-doctor`. The command reported Rust/Cargo `1.97.1`, rustfmt and Clippy `1.97.1`, Python `3.12.10`, Git `2.52.0.windows.1`, and `doctor: ready for contained M0 development`.

Decision:

The Windows doctor wrapper is executable in this checkout and uses an external target directory as documented. This is same-host diagnostic evidence only: no independent host was provisioned, no fresh-host run record or retained log bundle was created, and `PB-008`, `PB-009`, `PB-020`, and `TASK-000002` remain unchanged. The result does not support a clean-host, reproducibility, release-confidence, production, broad-implementation, or Chrome-class claim.

Next question:

When will the owner provide the named independent reviewer and fresh reference host or explicitly scoped clean VM required to execute `TASK-000002`?

# 2026-07-19 - Memory representation and tab lifecycle research handoff

Question:

Can the deferred memory/object-representation and tab-lifecycle questions be made executable as a source-backed experiment route without turning compactness or lifecycle vocabulary into a performance claim?

Method:

Checked the Rust type-layout and allocation documentation and Chromium's public tab-discard/lifecycle documentation and source on 2026-07-19. Reconciled those observations with `RQ-01`, `RQ-03`, `RQ-35`, `REQ-PERF-002`, `REQ-PERF-003`, the performance engineering book, the benchmark closure route, resource attribution, security identity rules, and the research-question coverage registry.

Decision:

Added a deferred no-claim research packet defining representation families, legal corpus and 5/15/30/100-tab workloads, memory categories, lifecycle/recovery/accessibility measures, safety and authority constraints, required artifacts, statistical treatment, and rejection rules. The packet explicitly rejects relying on unspecified default Rust layout, a single memory number, silent tab discard, hidden failures, or reduced security/accessibility/recovery workloads. No representation, allocator, process model, lifecycle policy, benchmark result, performance claim, or readiness gate changed.

Next question:

After source-strategy, toolchain/fresh-host, IPC, sandbox, and benchmark authority prerequisites are resolved, which owner-approved experiment manifest and synthetic fixture package will execute this lane?

# 2026-07-19 - Process topology and isolation-adjusted memory research handoff

Question:

Can the process-topology question be made executable without confusing lower process count or lower memory with security-equivalent performance?

Method:

Checked the official Chromium process-model/site-isolation, process-model, and RenderingNG documentation plus Firefox process-model, process-role, and accessibility architecture documentation on 2026-07-19. Reconciled those observations with `RQ-02`, `RQ-20`, `RQ-36`, `PB-011`, `PB-012`, `PB-013`, the IPC and sandbox closure routes, the benchmark 30-tab contract, and the existing memory/lifecycle research packet.

Decision:

Added an active no-claim process-topology research packet defining site-instance identity, candidate sharing models, helper roles, security-equivalence constraints, 8/16/32 GiB and 5/15/30/100-tab workloads, process/resource/IPC/accessibility/recovery measures, required artifacts, and rejection rules. It explicitly prevents site-isolation relaxation, omitted helper processes, hidden failures, or lower process count from becoming an optimization claim. No topology, IPC, sandbox, benchmark, security, performance, or readiness decision changed.

Next question:

After task authority, real transport, sandbox-policy, and benchmark prerequisites are resolved, which owner-approved topology manifest and synthetic process/lifecycle fixture package will execute this route?

# 2026-07-19 - Completion-audit research-lane synchronization

Question:

Does the central documentation-readiness completion audit include the newly added performance and process-topology research packets, rather than leaving them discoverable only through the general research index?

Method:

Compared the research index, completion-audit machine source list, completion-audit validator requirements, research-lane evidence references, and the human completion-audit narrative after adding the memory/lifecycle and process-topology packets.

Decision:

Added both packets to the checked completion-audit source set and `DOC-READY-RESEARCH_LANES` evidence references, added them to the validator's required source records, and updated the human audit to name them as active performance/security research inputs. The audit remains `9/10` ready for contained M0 and `0%` full-build closure; this synchronization does not answer a research question, approve a task, or promote a gate.

Next question:

Which remaining active research route should receive the next source-backed packet without duplicating an existing closure preparation or bypassing task authority?

# 2026-07-19 - Nova native build-entry criteria

Question:

Can the supplied Nova visual/layout source become an unambiguous future native-build input without allowing React, JSX, page content, or visual previews to own trusted browser behavior?

Method:

Compared the Nova source manifest and surface-contract map with the UI runtime book, token authoring workflow, component-fixture inventory, page-surface contract, native UI closure preparation, trusted UI rules, and current `PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `PB-020` boundaries.

Decision:

Added a no-claim Nova Native Build Entry Criteria packet defining source identity, visual-versus-behavioral authority, semantic token and surface extraction, typed state/command mapping, native fixture requirements, page-surface identity, build-entry gates, review artifacts, and rejection rules. Linked it from the UI runtime book, research indexes, progress snapshot, repository map, and chronology. Nova remains the primary visual/layout reference, React remains design-lab-only, and no toolkit, native adapter, UI gate, page-surface, accessibility, performance, or implementation decision changed.

Next question:

When the native UI predecessors and task authority are accepted, which owner-approved extraction manifest and toolkit-neutral fixture package will be used to start the Nova handoff?
# 2026-07-19 - Research packet continuity contract

Question:

Can every durable research packet preserve enough local context for a new maintainer or agent to resume it without relying on chat history or a narrow index row?

Method:

Audited all 127 durable Markdown packets after the existing research-index validator confirmed indexing, status, and owner metadata. The audit used flexible vocabulary rather than requiring identical headings: question or scope, evidence or method, disposition or next step, and an explicit no-claim or unsupported boundary.

Decision:

Strengthened `tools/validate_research_index.py` to enforce those four continuity fields for every durable packet, added the missing market-research question to `browser-market-gap-2026-07.md`, and documented the contract in the research index and documentation-readiness evidence matrix. This improves resumability and catches structurally incomplete packets without promoting any research result, readiness gate, implementation task, performance claim, or product claim.

Next question:

Which owner-controlled evidence lane should replace its no-claim preparation records with retained executable evidence after task authority and independent review are available?
