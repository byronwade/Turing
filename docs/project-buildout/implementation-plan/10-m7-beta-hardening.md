# 10 — M7: Beta Hardening

Status: implementation game plan; beta requires explicit risk acceptance
Owner: release board, security, compatibility, quality, accessibility, operations, and all supported subsystem owners

## 1. Objective

M7 moves Turing from architecture proof and developer preview toward a serious daily-use candidate for informed, non-sensitive volunteers. The focus is sustained evidence: compatibility breadth, crash and data-loss reduction, security containment, update reliability, accessibility, operational staffing, and measured performance.

## 2. Entry gates

- developer preview update/rollback path is reliable;
- supported beta platform candidates are named;
- critical process classes have effective sandbox evidence;
- site-isolation model is implemented for the supported navigation subset;
- profile formats and migrations are versioned;
- fuzzing, crash triage, symbols, and private vulnerability intake are operational;
- compatibility and performance labs run continuously;
- beta disclosure, support boundary, telemetry choices, and volunteer consent are drafted.

## 3. Compatibility campaign

- broaden current HTML, CSS, JavaScript, WebAssembly, Fetch, network, storage, media, device, accessibility, and internationalization subsets;
- track WPT and Test262 using full denominators and stable revisions;
- maintain top-site/application corpora with legal and privacy review;
- classify failures by missing feature, incorrect behavior, interoperability difference, security policy, platform dependency, or proprietary service;
- require owners and expiry for compatibility interventions;
- reject hidden site-specific semantics that cannot be documented and removed;
- publish regressions and denominator changes with each beta.

## 4. Performance and reliability campaign

- fixed-hardware startup, interaction, frame pacing, memory, network, storage, energy, thermal, and recovery suites;
- 10/30/100-tab lifecycle scenarios where supported;
- long-duration leak and wakeup tests;
- crash-free session, browser-process, renderer-process, GPU, network, storage, Plug-in, and agent metrics;
- queue, cache, allocator, GC, JIT, layout, paint, IPC, and binary-layout profiling;
- profile-guided and link-time optimization only with reproducible before/after evidence;
- pressure, suspend/resume, display/GPU changes, low disk, low memory, offline, and clock-change chaos testing;
- explicit error budgets and automatic rollback or promotion pause.

## 5. Security hardening

- independent threat-model and architecture review;
- sustained coverage-guided fuzzing and sanitizer/verification lanes;
- compromised-renderer, decoder, Plug-in, DevTools, and agent tests;
- platform sandbox and mitigation verification in release-equivalent packages;
- site-isolation and cross-profile negative suites;
- update/signing, credential, permission, download, phishing, trusted-UI, and telemetry review;
- unsafe/native/JIT inventory audit;
- dependency/advisory response drills;
- bug-bounty readiness and safe-harbor review if staffing permits;
- no unresolved critical or known actively exploited release issue.

## 6. Accessibility and usability

- VoiceOver, Narrator, NVDA, Orca/AT-SPI, keyboard, switch, zoom, contrast, forced-color, reduced-motion, and IME matrix for supported platforms;
- qualified human testing, not automation alone;
- task completion for onboarding, navigation, permissions, downloads, settings, recovery, update, DevTools, Plug-ins, and agent controls;
- screen-reader latency and event-coalescing budgets;
- accessible crash/recovery and split/workspace behavior;
- usability studies under 30-tab pressure and interrupted work;
- blocking severity and waiver rules.

## 7. Operations and support

- staged beta rollout and pause controls;
- private incident channel and on-call rotation;
- vulnerability acknowledgment, triage, patch, and release targets;
- supported-version matrix and emergency minimum version;
- crash/symbol service, optional telemetry, update service, reputation strategy, Plug-in revocation, sync/AI service boundaries where offered;
- service outage and offline behavior;
- support intake, severity, escalation, and known-issue publication;
- disaster recovery for signing, update metadata, accounts, domains, and infrastructure;
- cost and capacity review.

## 8. Exit criteria

Beta exits only when:

- independent security review critical findings are resolved;
- sustained fuzzing has no unresolved release-critical crash class;
- selected conformance thresholds are met and published;
- update, rollback, migration, crash recovery, and incident response are rehearsed;
- accessibility and platform matrices pass for supported scope;
- numeric SLOs and error budgets are active;
- support, update, and vulnerability response have qualified owners and backups;
- beta risk disclosure is approved by release owners;
- remaining gaps are compatible with the finite M8 stable-scope proposal.
