# Documentation Coherence Audit Findings - July 2026

Status: checked coherence-audit findings record; open items require owner or book-owner decisions
Owner: documentation-research, architecture, security, AI, product, and Plug-in platform owners
Audit date: 2026-07-20
Updated: 2026-07-20

## Question

Which documentation defects exist that the 79 `tools/validate_*.py` checks structurally cannot detect, and which of them are factual corrections versus scope decisions an agent must not make alone?

## Method

A thirty-domain adversarial audit was run across `docs/`. Each domain produced candidate findings; every candidate was then passed to an independent reviewer instructed to refute it, with instructions to default to refuted when uncertain. Twenty-eight candidates were produced and eleven were refuted, leaving seventeen. Ten of the seventeen were duplicate reports of a single stale count.

The validators cannot catch this defect class because every finding involves prose bound to a stale or wrong value while the identifiers, links, and schemas all remain valid. Existence, schema-shape, and link-target checks pass over all of them.

## Corrected in this pass

These were verified directly against the machine registries before editing.

| Defect | Records involved | Correction |
|---|---|---|
| Charter section 4 bound `REQ-ENG-002`, `REQ-A11Y-001`, `REQ-AI-001`, and `REQ-OPS-001` to subject matter the registry assigns to other IDs | `01-charter-and-principles.md`, `requirements.json` | Bound each statement to its correct registry ID and added the previously unlisted `REQ-ENG-003` through `REQ-ENG-006`, `REQ-A11Y-002`, `REQ-AI-003`, `REQ-AI-004`, `REQ-SEC-004` |
| Component-fixture inventory described as 15 surfaces with 9 core shell | `start-here.md`, `11-pre-build-readiness-checklist.md` | Corrected to 16 surfaces with 10 core shell, matching `component-fixture-inventory.json` and the owning research packet |
| Active research packets reported as `7/7` | `22-build-readiness-progress-snapshot.md` | Corrected to `8/8` |
| `PB-013` shown as partial in two rows | `20-build-continuation-readiness-pack.md` | Corrected to `documented_no_runner`, matching `pre-build-readiness.json` |
| Source-queue digest `617B0BE3...` presented as an acceptance gate | `TASK-000001-owner-review.md` | Corrected to the canonical-JSON digest `6F6C7542...` used by all ten manifests and the validator; documented the computation method and marked the old value unusable |
| Profile/session source manifest described as nine axes | `storage/README.md` | Corrected to ten axes, matching the manifest and its validator |
| Work-package graph omitted `WP-020` and `WP-015`'s `WP-002` dependency | `implementation-plan/01-program-sequence-and-critical-path.md` | Added `WP-020` and completed the additional-dependency footnotes for `WP-015`, `WP-017`, and `WP-020` |
| Five playbooks listed fewer requirements than the backlog they call authoritative | `implementation-plan/16-work-package-playbooks.md` | Restored `REQ-A11Y-002` to `WP-009`, `REQ-JS-006` to `WP-019`, `REQ-NET-004` to `WP-013`, `REQ-PROD-002` to `WP-014`, and `REQ-OPS-002` to `WP-017` |
| Market-strategy chapter defined a tab-lifecycle state set that dropped `Throttled` and added `Restoring` and `Terminated` | `market-strategy/06-resource-truth-and-lifecycle-control.md` | Aligned to the normative seven-state model and removed the competing definition |
| `RQ-42` (native Plug-ins, capability tiers, Wasm, WebExtensions) routed only to a book without that material | `research-question-coverage.json` | Added `docs/plugins/README.md`, which owns the Tier A-D capability model, WIT-based Wasm components, and WebExtensions adapter |

A sixth playbook, `WP-016`, initially appeared to drop three `REQ-AI-*` requirements. It does not; it uses the range notation `REQ-AI-001` through `REQ-AI-005`. That candidate was a detection artifact and no edit was made.

## Open findings requiring an owner or book-owner decision

These are documentation-scope questions, not factual errors. An agent should not resolve them unilaterally.

| Finding | Records | Decision required |
|---|---|---|
| The extensibility principal is named and modelled differently in two books: `extensions-enterprise` treats extensions as the first-class principal, while `plugins` defines Plug-ins as the first-class principal with Tier A-D and treats WebExtensions as a restricted Tier C adapter. The books do not cross-reference each other. | `extensions-enterprise/README.md`, `plugins/README.md`, `ADR-0011` | Now briefed in the [Extensibility Principal Ownership Briefing](extensibility-principal-ownership-briefing-2026-07.md). The divergence is downstream of `ADR-0011`, which is **proposed**: the Plug-in principal and tier model are that ADR's proposal written as settled vocabulary, while the normative Blueprint Capability Parity §8 still frames the target as a WebExtensions compatibility layer. The briefing recommends marking the Plug-in model `ADR-0011`-dependent rather than restructuring five chapters, which would decide the ADR by editorial action. Owner ruling still required. |

## Resolved since the audit

| Finding | Resolution |
|---|---|
| The AI book overview presented the `RQ-10` comparison (semantic snapshots versus screenshot-first control) as settled rationale while `RQ-10` is open and deferred. | Restated as the current working hypothesis, with `RQ-10` named as open and the absence of measured accessibility, latency, token-cost, or task-success advantage made explicit. |
| Security-engine chapters 10, 11, and 12 carried chapter 07's Spectre, RLBox, and LLVM CFI sources, none of which bear on their topics. | Replaced with topic-specific primary sources, each individually fetched and verified on 2026-07-20. Chapter 10 now cites Hardy's confused deputy, Capsicum, the seL4 reference manual, Macaroons, and Zircon handles. Chapter 11 cites Barth et al. on extension vulnerabilities, Chrome native messaging, WebDriver Level 2, WebDriver BiDi, Greshake et al. on indirect prompt injection, and NIST AI 100-2e2025. Chapter 12 cites UTS #39, RFC 5894, Safe Browsing v5, Porter Felt et al. on connection security indicators, Jackson et al. on picture-in-picture attacks, and Ye et al. on trusted paths. |
| `extensions-enterprise` chapter 06 (enterprise policy precedence and audit) was backed by WebExtensions, JWE, and HKDF references. | Replaced with the Chromium policy-template formats, Microsoft ADMX policy structure and its Enabled/Disabled/Not Configured precedence model, Apple device-management payloads, and NIST SP 800-92 for the audit half. |
| All seven `extensions-enterprise` chapters shared one four-item source list in which JWE and HKDF applied only to the sync chapter. | Every chapter now carries topic-specific verified sources: chapter 01 the Chromium process model, Chrome and MDN content scripts, Gecko Xray vision, and Barth et al.; chapter 02 the WebExtensions CG specification, Chrome permission declaration and activeTab, the MDN permissions API, and Picazo-Sanchez et al. on least privilege; chapter 03 the Service Workers spec, the Chrome extension service-worker lifecycle, MDN background scripts, `chrome.alarms`, and `chrome.storage`; chapter 04 Chrome and MDN `declarativeNetRequest`, Chrome and MDN native messaging, and native manifests; chapter 05 Mozilla signing and distribution, Chrome self-hosted distribution, Web Store review, DevTools extension surfaces, and WebDriver BiDi; chapter 07 Web Crypto, RFC 7516, RFC 5869, CRDTs, and `chrome.storage` sync quotas. RFC 7516 and RFC 5869 are now carried only by chapter 07. |
| **Dead external link.** All seven chapters and the book README cited `https://wicg.github.io/webextensions/`, which returns HTTP 404. The WebExtensions Community Group specification moved to `https://w3c.github.io/webextensions/specification/`. | Repaired in all eight files. No validator covers this class: the repository's link checks resolve internal repository paths, not external URLs, so an external specification can move or die silently. |

One candidate source was rejected during verification: Miller's *Robust Composition* thesis at `erights.org` was unreachable at verification time, so it was not cited despite being on-topic. Sources are cited only when a fetch confirmed identity and topic.

## Second pass: entry documents

The first audit swept the `docs/*/` book directories but never the entry points themselves. That was a real coverage gap: the root `README.md`, `AGENTS.md`, and the `docs/` root files are the first documents a new or returning maintainer reads, so a wrong fact there misleads maximally.

A second audit over eleven entry documents produced six candidates, of which four survived refutation. `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/start-here.md`, `docs/security.md`, and `docs/contributing.md` returned clean.

| Defect | Severity | Correction |
|---|---|---|
| `docs/prototype.md` described the `turing-types`, `turing-ipc`, and `turing-kernel` boundaries as **accepted**. `TASK-000011` is `review_pending`, `IF-001` is `partial` and still requires accepted `WP-002` tasks, a wire codec, a transport binding, a negative harness, and security review, and the root README states the manifest is "not accepted". | High | Removed the word and named both blocking records inline. |
| `docs/README.md` and `docs/research/README.md` labelled `RQ-35` deferred. `research-question-coverage.json` lists it in `active_question_ids`, and the crosswalk binds it to the benchmark and extreme-performance lane with `RQ-16`, `RQ-23`, `RQ-34`, and `RQ-37`. The two sets are disjoint, so it cannot be both. | Medium | Corrected in both indexes and in the owning research packet, which made the same claim. |
| `docs/repository-map.md` described the fresh-host toolchain manifest as nine evidence axes; the manifest and validator both define ten, after `reproducibility_levels` was added without updating the map. | Medium | Corrected to ten. |
| `docs/repository-map.md` described the profile/session manifest as nine evidence axes; both define ten, after `storage_backend_and_process_model` was added. | Low | Corrected to ten. |

The `prototype.md` case is the most instructive finding in either pass. "Accepted" is this program's load-bearing maturity term — the root README uses it precisely to draw the line — so a positive status overclaim in an entry document is more damaging than any missing-evidence statement. It is also the exact inverse of the no-claim discipline: the discipline guards statements about what is *not* proven, and nothing was guarding a statement that something *was*.

Two candidates were refuted: the README's expanded name for `OP-007` elaborates the registry rather than contradicting it, and the documentation policy's list of eight book directories carries no exhaustivity marker.

## Source-list convention: repo-wide measurement

The audit raised whether shared source lists are a defect. A mechanical sweep of every `## Primary sources` block in `docs/` was run on 2026-07-20 to answer this with data rather than impression.

Result: 85 distinct source lists exist; 17 of them are shared by more than one chapter, covering 106 chapters across 17 books.

Sharing is not itself the defect. In most books the shared list is a set of book-wide foundational specifications that genuinely applies to every chapter:

- `networking` shares Fetch, URL, WebTransport, TLS 1.3, QUIC, HTTP semantics, HTTP/2, and HTTP/3 across all eleven chapters, and every one of those chapters sits on those specifications;
- `accessibility` shares WCAG 2.2, WAI-ARIA, accname, and the three platform accessibility APIs across eight chapters;
- `storage` shares the Storage spec, IndexedDB, Service Workers, Clear-Site-Data, and SQLite across nine chapters;
- `release-operations`, `quality-assurance`, `web-platform`, `platform`, `media-documents`, `benchmark-lab`, `product-experience`, `developer-experience`, and `performance` follow the same pattern.

The defect is topic mismatch, not reuse. Security-engine chapters 07, 08, and 09 share Spectre, RLBox, and LLVM CFI and are correctly matched: chapter 07 scopes speculation and side channels, chapter 08 scopes native parser and codec isolation, which is precisely RLBox's subject, and chapter 09 scopes heap sandboxes and JIT compartments, where control-flow integrity applies. That same list was inherited by chapters 10, 11, and 12, whose topics are unrelated, and only those three were defective.

The one genuine mismatch found was `extensions-enterprise`, where RFC 7516 (JWE) and RFC 5869 (HKDF) applied only to the accounts and sync chapter but were carried by all seven. That has since been resolved: every chapter now carries topic-specific verified sources, and RFC 7516 and RFC 5869 are carried only by chapter 07.

The working conclusion is that a book-level foundational source list is an accepted convention in this repository, and that per-chapter sources are required only where a chapter's topic diverges from the book's shared foundation. This is a documentation-convention observation, not an approved policy; a book owner may still require per-chapter sourcing.

## Open finding: CI enforces a fraction of the documented gate

Measured on 2026-07-20, from `tools/xtask/src/main.rs` and `.github/workflows/`:

| | Count |
|---|---|
| `tools/validate_*.py` on disk | 79 |
| Run by `xtask check`, the documented handoff gate | 36 |
| Run by CI workflows | 7 |
| **In `xtask check` but never run by CI** | **29** |

No workflow invokes `cargo run -p xtask -- check`. CI runs `xtask doctor --ci`, which checks toolchain versions and the presence of required files but executes no validator, then seven named validators, then `cargo fmt`, `clippy`, `test`, the shell self-test, the prototype, the documentation-change check, and a clean-tree check.

The consequence is that a change breaking any of 29 validators merges green. The set includes `validate_documentation_readiness_completion_audit.py`, which computes the readiness percentage this whole document depends on; `validate_research_index.py`; `validate_owner_decision_synchronization.py`; `validate_specified_task_manifests.py`; `validate_readiness_review_templates.py`; every source-manifest validator; and both validators added on 2026-07-20.

This may be deliberate. Some of those checks are slow, and CI already runs the Cargo steps that `xtask check` would duplicate. But nothing in the repository records it as deliberate, and the evidence in the code points the other way: `validate_blueprint.py` contains `check_xtask_aggregate_check`, which reconciles a named subset of validators between `main.rs` and the workflow. Something was intended to keep the two in step; it currently keeps seven of thirty-six in step.

The practical risk is that the documented gate and the enforced gate have quietly diverged. [Start Here](../start-here.md) instructs maintainers to run the aggregate check before handing off work, and the evidence matrix lists all 79 focused validators. A contributor who follows that guidance is held to a much higher standard than a contributor who relies on CI.

**Recommendation, not a change.** Either invoke `xtask check` from `repository-validation.yml` and drop the duplicated Cargo steps, or record explicitly which validators are merge-gating and which are local-only, and why. The first is simpler and matches the apparent intent.

This was not changed unilaterally. Altering which checks block a merge changes the repository's enforcement boundary, which is an owner decision rather than a defect with one right answer in a registry.

## New coverage: external-link liveness

The dead WebExtensions URL exposed a gap with no owner. The repository's link checks resolve internal repository paths; nothing has ever verified that a cited external specification still exists. A specification can move or be withdrawn and every validator will keep passing.

[`tools/check_external_links.py`](../../tools/check_external_links.py) closes that gap. It extracts external URLs from `docs/`, probes each one, and fails only on a confirmed `404` or `410`. Access conditions — timeouts, bot-blocking `403`s, rate-limiting `429`s — are reported but never fail the run, because they are not evidence that a source is gone. URLs written inside inline code or fenced blocks are skipped, since that is how this repository records a URL that has died rather than cites it as live.

It is deliberately **not** part of `xtask check`. It requires network access and depends on third-party availability, so it must not gate the offline validation path. `xtask` lists its validators explicitly, so adding this file does not alter the aggregate check.

A repo-wide run on 2026-07-20 found **10 confirmed-dead URLs** and 43 unconfirmed results, the latter almost all `www.w3.org` returning `403` to automated clients.

An earlier entry in this document claimed the same run found zero dead URLs. That claim was wrong, and the way it was wrong is worth recording: the tool prints confirmed-dead URLs to `stderr` and unconfirmed ones to `stdout`, and the run was inspected through a pipe that surfaced only the tail of `stdout`. The tool had reported the failures correctly and exited non-zero; the reader did not see them. A checker is only as good as the reading of its output.

All ten were pre-existing citations, not ones added on 2026-07-20. Eight were genuinely dead and are now repaired; two were defects in the checker itself.

| Dead URL | Citations | Resolution |
|---|---|---|
| `learn.microsoft.com/.../apps/design/accessibility/` | 18, across `accessibility/`, `platform/`, and research | The bare directory 404s; replaced with `.../accessibility/accessibility-overview`, verified to cover UI Automation, assistive technology, and screen-reader support |
| `learn.microsoft.com/.../win32/procthread/process-mitigation-policy` | 4 | Replaced with `.../win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy` |
| `llvm.org/docs/ControlFlowIntegrity.html` | 3, in `security-engine/07`-`09` | Moved to `clang.llvm.org/docs/ControlFlowIntegrity.html`. Notably this was a source the 2026-07-20 pass *kept* as correctly matched to its chapters, without checking that it still resolved |
| `docs.webkit.org/Testing/WebPlatformTests.html` | 2 | Moved to `docs.webkit.org/Infrastructure/WPTTests.html` |
| two `chromium.googlesource.com/catapult/+/c5f59e09.../telemetry` links | 2 | The pinned commit no longer resolves; repointed to `+/HEAD` |
| `chromium.googlesource.com/chromium/src/%2B/720dadbc.../tab_lifecycle_unit.h` | 1 | Two faults: a `%2B` encoding error where `+` was meant, and an unresolvable pinned commit. Repointed to `+/HEAD` |
| `chromium.googlesource.com/chromium/src/+/show/HEAD/...TaskSchedulingInBlink.md` | 1 | Malformed `+/show/HEAD/` path segment; corrected to `+/HEAD/` |

Two were the checker's own false positives, and both produced tool fixes:

- `crates.io/crates/servo` returns 404 to a plain GET because crates.io serves a single-page app; `crates.io/api/v1/crates/servo` returns 200. `crates.io` is now treated as a bot-blocking host.
- `developer.apple.com/.../xpc_connection_set_peer_platform_identity_requirement(_:_:)` was never dead. The URL contains parentheses, and the bare-URL regex stopped at the first `)`, truncating a valid link into a 404. The extractor now parses Markdown link targets with one level of balanced parentheses before falling back to bare-URL matching.

A repo-wide run after these repairs reports **534 URLs, 0 dead, 40 unconfirmed**.

Repointing a pinned commit to `HEAD` is a deliberate trade. A pinned URL is better provenance, but a pinned URL that 404s is no evidence at all. Where a pin no longer resolves, `HEAD` at least identifies the file; restoring true pinning would require finding a commit that still exists and re-verifying the content matches what the citing text claims.

## Refuted candidates

Eleven candidates did not survive refutation and were not acted on. The notable ones: the `product-experience` book's use of "owns" is domain-scope language rather than a normativity claim; `technology-stack` naming SQLite a leading candidate sits under an explicit candidate-evaluation heading and does not rank backends against the storage lane; security-engine chapters 07-12 sit under a separate "Advanced research" heading rather than inside the six-chapter reading order, so the reading-path incoherence claim did not hold; and the `ADR-0009` packet date labels are a local/UTC rendering artifact rather than a traceability contradiction.

## Current disposition and next proof

All 79 validators and the aggregate check pass after the corrections. The corrections improve internal accuracy only.

The next proof for the open findings is a book-owner ruling on extensibility ownership and on source-backing expectations for the `extensions-enterprise` and advanced security-engine lanes.

## Claim boundary

This record documents internal documentation accuracy only. It does not promote any readiness gate, approve a task, close a research question, or support broad M1, Chrome-class, performance, compatibility, security, accessibility, production, release, or all-information-ready-for-building claims.
