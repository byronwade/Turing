# 15 — Risk Register

Status values: `open`, `mitigating`, `accepted`, `blocked`, `retired`.  
Impact: `critical`, `high`, `medium`, `low`. Likelihood is an engineering estimate that must be revised from evidence.

Risk owners are roles until named maintainers exist. Acceptance of a critical or high residual risk requires a dated decision record and cannot be implied by inactivity.

## R-001 — Program scale exceeds available capacity

- Impact: critical; likelihood: high; status: open; owner: program lead.
- Failure: implementation expands across engine, runtime, security, platform, media, DevTools, AI, and operations faster than maintainers can make any path safe or compatible.
- Mitigation: gate-based milestones, strict supported subset, subsystem ownership, freeze feature growth when security/compatibility maintenance consumes capacity, publish staffing gaps.
- Trigger: release-critical backlog grows for two milestones, security patch target missed, or no owner for a supported subsystem.

## R-002 — “From scratch” becomes unsafe reinvention

- Impact: critical; likelihood: medium; owner: architecture/security.
- Failure: custom crypto, TLS, Unicode, font, codec, database, or sandbox primitives create avoidable vulnerabilities and incompatibility.
- Mitigation: independent engine definition permits audited foundations; dependency ADRs; prohibit custom cryptography; fuzz and isolate native boundaries.
- Trigger: proposal duplicates a security-critical mature primitive without measured strategic benefit.

## R-003 — Hidden dependency on an existing browser engine

- Impact: high; likelihood: medium; owner: architecture.
- Failure: platform views, remote rendering, or engine libraries enter as “temporary” paths and become permanent, invalidating the project goal.
- Mitigation: prohibited-dependency policy, binary/source scans, architecture reviews, explicit experiment branches only.
- Trigger: shipped build links or invokes an existing web engine for page behavior.

## R-004 — Renderer escape or insufficient sandbox

- Impact: critical; likelihood: high in early phases; owner: security/platform.
- Failure: compromised renderer gains local files, sockets, processes, credentials, devices, or kernel IPC.
- Mitigation: OS-native deny-by-default sandbox, brokers, negative tests, minimal handles, independent review, no arbitrary-web safety claim before gates.
- Trigger: prohibited-operation test succeeds or sandbox profile is weakened for compatibility.

## R-005 — Site isolation is incomplete

- Impact: critical; likelihood: high; owner: kernel/security.
- Failure: hostile site receives another site’s DOM, response, storage, process memory, accessibility subtree, or compositor resource.
- Mitigation: typed site-instance/browsing-context model, process assignment tests, swaps on navigation/redirect, no pressure-based cross-site coalescing.
- Trigger: cross-site frames share unreviewed renderer state or process reuse bypasses policy.

## R-006 — IPC confused-deputy vulnerabilities

- Impact: critical; likelihood: high; owner: kernel/security.
- Failure: a renderer forges identity/origin/epoch or sends malformed state that a broker treats as authoritative.
- Mitigation: kernel-issued context, receiver revalidation, bounded schemas, capability handles, fuzzing, compromised-renderer harness.
- Trigger: privileged operation depends on unverified renderer-supplied security fields.

## R-007 — Memory-unsafe native dependency compromise

- Impact: critical; likelihood: high; owner: dependency/security.
- Failure: codec, font, image, PDF, GPU, database, or platform library bug leads to code execution.
- Mitigation: narrow sandboxed utility processes, version/advisory policy, fuzzing, caps, immutable outputs, rapid update path.
- Trigger: native parser moves into kernel/renderer without isolation or upstream critical advisory remains unresolved.

## R-008 — Rust unsafe surface grows without control

- Impact: high; likelihood: medium; owner: language/security.
- Failure: GC/JIT/FFI/GPU/shared-memory unsafe code accumulates undocumented invariants and recreates C++-class risk.
- Mitigation: unsafe ledger, mandatory `SAFETY` rationale, designated reviewers, Miri/sanitizers/fuzzing, safe wrappers, metrics per release.
- Trigger: unsafe additions lack owner/test or inventory trend exceeds approved budget.

## R-009 — JavaScript conformance stalls

- Impact: high; likelihood: high; owner: JS runtime.
- Failure: long-tail semantics, modules, proxies, weak references, regex, Intl, and host bindings prevent useful web compatibility.
- Mitigation: interpreter-first Test262 map, generated bindings, feature slices, upstream tests, no premature optimizing JIT.
- Trigger: Test262/WPT progress plateaus while runtime complexity rises.

## R-010 — JIT creates exploitable unsoundness

- Impact: critical; likelihood: high; owner: compiler/security.
- Failure: incorrect speculation, guards, stack maps, deoptimization, code permissions, or cache validation enables memory corruption.
- Mitigation: interpreter oracle, randomized tiering, W^X, CFI/PAC/CET where available, JIT fuzzing, no-JIT mode, delayed optimizer.
- Trigger: tier differential, sanitizer, or generated-code validation failure.

## R-011 — Garbage collector lifetime defects

- Impact: critical; likelihood: high; owner: runtime.
- Failure: missing roots/barriers, wrapper cycles, weak handling, finalization, or concurrent races cause UAF, leaks, or semantic errors.
- Mitigation: exact stop-the-world baseline, stress collection, barrier verifier, heap graph checks, stable handles, concurrency deferred.
- Trigger: nondeterministic liveness, detached-document growth, or stress-only crash.

## R-012 — CSS/layout breadth takes longer than expected

- Impact: high; likelihood: high; owner: layout.
- Failure: flex/grid/tables/inline/bidi/fragmentation/writing modes and incremental invalidation create years of compatibility debt.
- Mitigation: formatting-context interfaces, reference fragments, reduced tests, WPT prioritization, correctness before parallelism.
- Trigger: feature work produces regressions faster than test coverage or full recomputation diverges from incremental results.

## R-013 — Text and internationalization are incorrect

- Impact: high; likelihood: high; owner: text/i18n.
- Failure: shaping, fallback, bidi, line breaking, IME, vertical writing, emoji, locale and time-zone behavior fail outside English demos.
- Mitigation: audited data/libraries, multilingual corpus, platform input/accessibility testing, dedicated ownership.
- Trigger: locale/script coverage omitted from milestone gates or text geometry differs unpredictably across paths.

## R-014 — GPU/compositor attack surface or instability

- Impact: critical; likelihood: high; owner: graphics/security.
- Failure: malformed display/GPU commands, driver bugs, device loss, unbounded resources, or layer churn cause exploit, crash, or poor performance.
- Mitigation: GPU process, strict validation/budgets, CPU reference backend, device-loss recovery, fuzzing, driver deny/workaround registry.
- Trigger: renderer can submit unchecked native handles/shaders or GPU reset kills the browser.

## R-015 — Web compatibility blocked by missing proprietary capabilities

- Impact: high; likelihood: high; owner: product/legal.
- Failure: DRM, codecs, vendor services, approved-browser lists, extension store, sync, safe browsing, or accounts prevent literal Chrome parity.
- Mitigation: explicit external-dependency matrix, licensing research, alternative services, no fake claims, prioritize open standards.
- Trigger: a parity claim omits a proprietary blocker or implementation attempts unauthorized bypass.

## R-016 — Codec patent and licensing exposure

- Impact: high; likelihood: medium; owner: legal/media.
- Failure: distributing H.264/AAC/HEVC or related technology creates royalty, patent, territory, or store-policy obligations.
- Mitigation: legal review, platform-codec strategy, per-platform matrix, optional components, notices, budget.
- Trigger: release package includes a codec without documented rights and jurisdictions.

## R-017 — DRM licensing unavailable

- Impact: high; likelihood: high; owner: business/media.
- Failure: major streaming sites remain unsupported because content-decryption modules require vendor approval and compliance.
- Mitigation: disclose gap, architect secure CDM boundary, do not block open-web milestones, pursue licensing only when operational maturity exists.
- Trigger: product messaging promises protected playback before agreement and certification.

## R-018 — Performance optimization compromises correctness/security

- Impact: critical; likelihood: medium; owner: performance/security.
- Failure: benchmarks disable isolation, mitigations, lifecycle protections, accessibility, or behavior.
- Mitigation: benchmark manifest, default-equivalent comparisons, experimental labeling, security/perf joint review.
- Trigger: improvement cannot reproduce with release settings or changes security/process state undisclosed.

## R-019 — 30-tab memory goal becomes misleading

- Impact: high; likelihood: high; owner: performance/product.
- Failure: memory appears low only because tabs are discarded, sites coalesced unsafely, caches omitted, or activity suppressed.
- Mitigation: mixed and all-live scenarios, per-tab lifecycle/process/isolation disclosure, revival latency/state-loss reporting.
- Trigger: headline memory number lacks manifest or competitor is tested under different lifecycle policy.

## R-020 — Memory accounting is inaccurate

- Impact: medium; likelihood: high; owner: performance/platform.
- Failure: shared pages, GPU allocations, allocator reserve, compressed memory, swap, or external buffers are double-counted or omitted.
- Mitigation: platform-specific definitions, physical versus charged views, allocator/GC/GPU telemetry reconciliation, uncertainty labels.
- Trigger: semantic totals do not reconcile within published tolerance to process/system measurements.

## R-021 — Tab suspension loses user work

- Impact: critical; likelihood: medium; owner: lifecycle/product.
- Failure: freeze/serialize/discard destroys unsaved edits, uploads, calls, device sessions, or app state.
- Mitigation: protection reasons, conservative eligibility, explicit lifecycle API tests, crash-safe checkpoint design, user keep-active control.
- Trigger: any reproducible silent work loss from normal pressure policy.

## R-022 — Network/security-policy incompatibility

- Impact: critical; likelihood: high; owner: network/security.
- Failure: Fetch/CORS/CSP/cookies/cache/TLS/redirect differences break sites or expose data.
- Mitigation: hermetic servers, WPT, one URL/origin implementation, request context issued outside renderer, differential traces.
- Trigger: security decision made inconsistently across renderer/network/kernel or cross-origin test fails.

## R-023 — Storage corruption or migration data loss

- Impact: critical; likelihood: medium; owner: storage/release.
- Failure: profile upgrades, power loss, disk full, rollback, or schema bugs destroy history, credentials metadata, offline data, or settings.
- Mitigation: transactional migrations, journals, independent stores, backups/recovery tools, fault injection, downgrade block.
- Trigger: migration lacks interruption tests or prior version opens newer schema unsafely.

## R-024 — Update/signing compromise

- Impact: critical; likelihood: medium; owner: release/security.
- Failure: attacker ships code through stolen keys, builder compromise, mirror tamper, replay, or rollback.
- Mitigation: protected pipeline, hermetic/reproducible builds, hardware/threshold keys, signed metadata, expiry, minimum secure version, provenance, incident plan.
- Trigger: release secrets available to PR builds, unsigned mutable artifact, or metadata verification bypass.

## R-025 — Security response cannot meet browser timelines

- Impact: critical; likelihood: high for small team; owner: program/security.
- Failure: known exploitable flaws remain unpatched because supported platforms and subsystems exceed response capacity.
- Mitigation: no stable claim before staffing, narrow platform matrix, automated builds/updates, upstream monitoring, emergency no-JIT/feature-disable options.
- Trigger: critical fix target missed or release pipeline cannot produce all supported updates promptly.

## R-026 — Supply-chain compromise

- Impact: critical; likelihood: medium; owner: release/dependency.
- Failure: malicious crate, build script, compiler, binary blob, CI action, or source archive enters artifacts.
- Mitigation: pinned sources/hashes, minimal dependencies, isolated builders, no release-network access, SBOM/provenance, action pinning, review of build code.
- Trigger: unpinned executable dependency or unexplained binary delta.

## R-027 — Browser UI enables spoofing

- Impact: critical; likelihood: medium; owner: product/security.
- Failure: pages imitate or obscure origin, permission, certificate, credential, fullscreen, capture, download, or agent confirmation UI.
- Mitigation: trusted non-overlay chrome, origin binding, delayed/position-safe prompts, accessibility parity, spoofing studies.
- Trigger: user test cannot distinguish page prompt from browser prompt or critical state disappears in compact/fullscreen modes.

## R-028 — Accessibility is deferred

- Impact: high; likelihood: high; owner: accessibility/product/engine.
- Failure: browser UI or engine semantics become structurally inaccessible and expensive to retrofit; agent snapshots also degrade.
- Mitigation: accessibility tree in core pipeline, native bridges early, manual assistive-tech matrix, release-blocking critical flows.
- Trigger: milestone ships new UI/engine control without semantics and keyboard path.

## R-029 — Agent prompt injection causes unauthorized action

- Impact: critical; likelihood: high; owner: AI/security.
- Failure: page/document/tool text convinces model to exfiltrate data, change accounts, publish, buy, delete, grant permission, or run code.
- Mitigation: no secret exposure, source labels, deterministic grants/risk classes, epoch checks, confirmation, adversarial suite, visible stop/audit.
- Trigger: page/model text changes policy result or high-risk action executes without valid confirmation.

## R-030 — Agent privacy/provider leakage

- Impact: critical; likelihood: medium; owner: AI/privacy.
- Failure: remote providers receive page text, files, prompts, credentials, or enterprise data unexpectedly or retain/train on it contrary to expectation.
- Mitigation: provider manifests, preview/indicator, redaction, origin/file grants, local-only policy, no silent fallback, audit and budgets.
- Trigger: transmitted field absent from declared provider data flow or local task invokes remote endpoint.

## R-031 — Local AI destroys memory/energy advantage

- Impact: high; likelihood: high; owner: AI/performance.
- Failure: model weights, KV cache, accelerator use, and background loops consume more RAM/energy than the browser saves.
- Mitigation: on-demand load/unload, quantized model options, separate budgets and process, remote/local choices, agent-disabled baseline.
- Trigger: dormant feature retains significant model resources or 30-tab headline includes/excludes AI inconsistently.

## R-032 — DevTools/automation becomes a privilege backdoor

- Impact: critical; likelihood: medium; owner: DevTools/security.
- Failure: unauthenticated remote debugging, generic eval, internal protocol, or automation profile accesses normal user data or bypasses prompts.
- Mitigation: disabled-by-default remote endpoint, authentication, loopback, visible attachment, isolated profiles, versioned task-specific protocol.
- Trigger: remote listener exposed broadly or automation bypass attaches to signed-in profile without explicit launch consent.

## R-033 — Extension ecosystem recreates security and memory problems

- Impact: high; likelihood: high; owner: extensions/security/performance.
- Failure: broad host access, native messaging, persistent background work, unsafe updates, or unbounded rules undermine privacy/performance.
- Mitigation: MV3-like event model, optional host grants, isolated host, quotas, signing/update provenance, resource manager, private opt-in.
- Trigger: extension gets ambient all-profile authority or cannot be attributed/throttled.

## R-034 — Cross-platform parity fragments architecture

- Impact: high; likelihood: high; owner: platform/architecture.
- Failure: macOS, Windows, and Linux adapters diverge in input, accessibility, sandbox, graphics, packaging, and update semantics until bugs are platform-specific and unmaintainable.
- Mitigation: platform-neutral contracts, conformance traces, smallest supported platform set, explicit capability differences, shared reference backends.
- Trigger: core security/product decision moves into one adapter without cross-platform contract.

## R-035 — Licensing or contributor provenance failure

- Impact: high; likelihood: medium; owner: legal/governance.
- Failure: copied engine code, incompatible license, missing attribution/source offer, patents, or contributor ownership prevents distribution.
- Mitigation: MPL-2.0 policy, DCO/CLA decision, source provenance review, automated license checks, third-party ledger, clean-room notes where needed.
- Trigger: code origin cannot be established or dependency terms conflict with distribution.

## R-036 — Benchmarks are not reproducible

- Impact: medium; likelihood: high; owner: performance/quality.
- Failure: environment drift, live-site changes, thermal state, cache differences, missing raw data, or cherry-picked runs invalidate claims.
- Mitigation: fixed hardware, offline corpus, manifests, raw samples, statistical policy, current competitor versions, failure inclusion.
- Trigger: reported result lacks commit/config/corpus/raw samples or cannot reproduce within noise bounds.

## R-037 — Scope drift toward services before engine foundation

- Impact: medium; likelihood: high; owner: product/program.
- Failure: sync, accounts, cloud AI, store, telemetry, or monetization consumes effort while parser/runtime/security remain immature.
- Mitigation: milestone gates, separate service proposals, engine/security capacity floor, explicit opportunity cost.
- Trigger: service work enters critical path before its browser prerequisites pass.

## R-038 — Project claims damage trust

- Impact: high; likelihood: medium; owner: program/product.
- Failure: “better than Chrome,” “secure,” or “complete” language outruns evidence, causing unsafe use and credibility loss.
- Mitigation: claim maturity labels, versioned comparison reports, prominent unsupported/risk sections, external review.
- Trigger: public wording lacks test link or omits material compatibility/security limitation.

## R-039 — Contributor burnout and bus factor

- Impact: high; likelihood: high; owner: governance.
- Failure: critical subsystem depends on one person, review stalls, or emergency work becomes unsustainable.
- Mitigation: documented ownership, code tours, mentoring, rotation, automation, realistic support matrix, funding plan.
- Trigger: sole owner unavailable or repeated release/security work exceeds sustainable load.

## R-040 — Legal/privacy obligations are underestimated

- Impact: high; likelihood: medium; owner: legal/privacy.
- Failure: telemetry, sync, AI providers, crash data, minors, international transfer, export controls, accessibility, consumer protection, or enterprise commitments create unplanned obligations.
- Mitigation: privacy-by-design, minimal collection, jurisdictional counsel before services/stable distribution, data inventory and deletion/retention controls.
- Trigger: personal data leaves device or paid/general distribution begins without reviewed policy.

## Review cadence

- Critical risks: reviewed at every security/release meeting and milestone gate.
- High risks: reviewed monthly and on relevant architecture changes.
- Medium/low risks: reviewed each milestone.
- Any triggered risk creates or updates a GitHub issue with owner, evidence, mitigation, target gate, and residual risk.

Risk counts are not a quality metric. Closing a risk requires evidence that the condition no longer applies; moving it to “accepted” requires explicit residual-impact disclosure.
