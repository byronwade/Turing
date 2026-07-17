# 12 — Testing, Compatibility, Fuzzing, and Quality Gates

## 1. Test pyramid

A browser cannot be validated by screenshots and manual browsing. Turing uses layered evidence:

1. pure algorithm and data-structure unit tests;
2. parser/runtime/style/layout component tests;
3. process, IPC, sandbox, storage, update, and recovery integration tests;
4. Web Platform Tests and Test262 conformance;
5. rendering, accessibility, input, printing, media, and DevTools end-to-end suites;
6. fuzzing, property tests, mutation tests, sanitizers, model checking, and fault injection;
7. performance, memory, energy, and stability laboratories;
8. adversarial security and agent evaluations;
9. manual accessibility, usability, platform, and release validation;
10. independent review before stable claims.

Every defect adds the smallest useful regression test at the lowest applicable layer, plus a higher-level test when the bug crossed a trust boundary or user workflow.

## 2. Standards conformance

### 2.1 Web Platform Tests

Turing imports pinned Web Platform Tests revisions and records:

- commit and local patches;
- enabled directories and metadata;
- pass, fail, timeout, crash, leak, not-run, and harness-error counts;
- expected failures with linked issues and owners;
- platform/configuration differences;
- test flakiness and repeatability;
- comparison to prior Turing revision.

Unsupported tests remain visible. A smaller denominator cannot be used to inflate pass rate.

### 2.2 Test262

Test262 runs against interpreter and each JIT tier. Results separate language features, built-ins, modules, internationalization, annex behavior, implementation-defined behavior, and harness limitations. Tier differential failures are release-blocking even if one tier matches another engine by accident.

### 2.3 Other primary suites

As features appear, use standards-owned or broadly recognized suites for WebAssembly, CSS, WebGL/WebGPU, WebDriver BiDi, accessibility APIs, URL/encoding, Unicode, HTTP, TLS integrations, and platform-specific behavior. The source bibliography records exact upstreams.

## 3. Turing reduced tests

Turing maintains compact internal formats for:

- HTML parser token/tree traces;
- DOM mutation and event sequences;
- selector/cascade/computed-style expectations;
- layout fragment trees and intrinsic-size cases;
- paint/property/display-list traces;
- pixel references with color-space metadata;
- hit-test, selection, caret, and scroll behavior;
- accessibility-tree snapshots and action results;
- JavaScript bytecode/runtime/GC/JIT differential cases;
- navigation/process assignment/security policy traces;
- storage transaction and recovery scenarios;
- agent observation/policy/action traces.

Textual semantic traces are preferred where pixels are not the relevant truth. Reference updates require review explaining why behavior changed.

## 4. Differential testing

Differential tests compare Turing with multiple established engines to identify likely defects. They do not define correctness when engines disagree. The workflow:

1. generate or mutate a case;
2. execute under equivalent configuration in Turing and at least two reference engines where practical;
3. normalize nondeterministic output;
4. classify agreement/disagreement;
5. consult the normative standard and tests;
6. reduce the case;
7. add a Turing regression and, where appropriate, upstream test.

Differential targets include DOM serialization, style values, layout geometry, pixels, event order, JS results, errors, accessibility, network policy, and storage behavior.

## 5. Fuzzing program

Continuous fuzz targets include:

- URL, host, IDNA, MIME, header, cookie, CSP, CORS, and content-disposition parsing;
- HTML/XML/CSS/selectors/values/fonts/images/SVG/PDF/media/container formats;
- DOM mutation/event/editing/selection/structured clone;
- layout formatting contexts and fragmentation;
- display-list/GPU command validation and shader translation;
- JavaScript lexer/parser/bytecode/interpreter/GC/JIT/deoptimization/regexp;
- WebAssembly decoder/validator/compiler/traps;
- IPC encoders/decoders and privileged state machines;
- storage schemas, migrations, transaction logs, corruption repair;
- update metadata/package application;
- extension manifests/messages/rules;
- DevTools and agent protocol schemas;
- semantic snapshot reduction and prompt-injection policy.

Fuzzers run with dictionaries, grammar/structure-aware producers, crossover, resource limits, sanitizer variants, randomized scheduling, OOM injection, and corpus minimization. Crashes are deduplicated by root cause, not stack hash alone.

## 6. Property and model tests

Properties include:

- parse/serialize/parse stability where semantics allow;
- no origin/profile/epoch widening through IPC round trips;
- lifecycle transitions follow the allowed graph;
- bounded queues never exceed configured capacity;
- cache/storage clear removes all matching partition keys and no others;
- navigation commit is atomic;
- style/layout incremental result equals full recomputation;
- interpreter/JIT tiers produce equivalent observable behavior;
- GC preserves reachable objects and removes unreachable objects under stress;
- update selects only authorized versions and artifacts;
- agent grant narrowing never expands authority;
- confirmed action effect matches the presented action class and target.

State machines for navigation, service workers, storage transactions, updates, permissions, and agent confirmation use model-based generated sequences.

## 7. Security testing

- compromised-renderer harness calls every broker method with forged IDs, origins, epochs, sizes, handles, and orderings;
- sandbox negative tests attempt prohibited files, sockets, devices, processes, debugging, shared memory, registry/config, keychain, and platform IPC;
- site-isolation tests cover redirects, popups, opener changes, nested frames, opaque origins, history, BFCache, crashes, pressure, and process reuse;
- web security tests cover SOP, CORS, CSP, CORP/COOP/COEP, mixed content, SRI, MIME, sandbox, user activation, permissions, credentials, downloads, and internal schemes;
- update tests cover tamper, replay, rollback, expiry, mirror compromise, partial write, disk full, power loss, revoked keys, and emergency rollback;
- secret scanners inspect logs, traces, crashes, telemetry, agent payloads, and diagnostic exports;
- dependency, provenance, SBOM, unsafe-code, and binary-hardening checks are release gates.

Red-team exercises and independent audits occur before general-use claims, with findings tracked to closure or explicit accepted risk.

## 8. Agent adversarial suite

Scenarios include:

- direct instructions to ignore user policy;
- indirect instructions in comments, emails, documents, images, PDFs, metadata, hidden content, and tool output;
- fake security/confirmation UI;
- page swap between observation and action;
- cross-origin iframe exfiltration;
- malicious extension or service-worker interference;
- credential, cookie, token, clipboard, local-file, source-code, and personal-data requests;
- purchase, transfer, publish, send, delete, permission, passkey, extension-install, and external-app actions;
- multi-agent delegation and collusion;
- resource exhaustion, infinite planning, repeated confirmations, and cancellation races;
- provider timeout, malformed tool call, hallucinated target, and stale reference.

The suite scores unauthorized action rate as the primary safety metric. Task completion does not offset a policy violation.

## 9. Accessibility testing

Automated checks validate semantic roles, names, states, focus, relationships, keyboard paths, contrast, zoom, forced colors, reduced motion, and accessibility-tree diffs. Manual matrices include supported screen readers and platform assistive technologies.

Web-engine accessibility tests cover HTML/ARIA/SVG/forms/tables/live regions/dialogs/shadow DOM/canvas fallback/text ranges. Browser UI tests cover address bar, tabs, profiles, permissions, downloads, DevTools, agent confirmations, resource manager, and crash recovery.

## 10. Rendering tests

Pixel tests specify viewport, scale factor, color space, font set, antialiasing mode, GPU/software backend, locale, and animation clock. Where platform text rasterization differs, use geometry/fragment/paint semantics plus bounded pixel masks instead of broad exemptions.

Animations and asynchronous resources use virtual time/test hooks in isolated test builds. Reference images are reviewed with semantic trace changes.

## 11. Network and storage test infrastructure

A hermetic local test environment provides HTTP/1.1, HTTP/2, HTTP/3, TLS variants, proxy, authentication, redirects, slow/partial/chunked responses, WebSocket, service-worker, DNS mapping, certificate errors, cache controls, and connection failures.

Storage tests inject power loss, disk full, permission denial, corruption, old schemas, concurrent transactions, clock changes, quota pressure, and process crashes. Test profiles never share real user directories.

## 12. Fault injection

Non-stable builds can inject:

- allocation failure by subsystem/size/count;
- renderer, network, storage, GPU, media, extension, DevTools, and agent process termination;
- IPC delay, reorder where protocol permits, drop, duplication, malformed payload, and disconnect;
- network offline, latency, loss, bandwidth, DNS, TLS, proxy, and portal conditions;
- disk full, read-only, slow I/O, corruption, and migration interruption;
- GPU reset/device lost and surface resize races;
- clock/time-zone changes and sleep/resume;
- memory pressure and OS working-set trimming;
- model timeout, malformed response, provider switch, token exhaustion, and cancellation.

Fault hooks are inaccessible to arbitrary web content and disabled in signed stable builds.

## 13. Performance regression testing

Performance CI has tiers:

- fast micro/component checks on pull requests;
- deterministic page benchmarks and memory leak loops on protected merge queues;
- fixed-hardware startup/interaction/30-tab/energy labs on scheduled builds;
- release-candidate comparison against prior Turing and named competitor versions.

Regressions store raw traces and semantic attribution. Noisy metrics use control charts or confidence intervals. A waiver records impact, owner, expiry, and follow-up issue.

## 14. Stability and longevity

Long-duration tests cover:

- repeated navigation and tab churn;
- days of background service-worker/timer activity;
- media playback and device connect/disconnect;
- DevTools attach/detach and trace capture;
- sleep/wake, network changes, display/GPU changes;
- profile migration across versions;
- update and rollback;
- agent sessions, cancellation, provider errors, and audit growth.

Crash-free session rate alone is not enough; hangs, data loss, repeated renderer crashes, excessive resource use, and silent feature failure are tracked.

## 15. CI matrix

Pull requests run formatting, lint, unit/component tests, documentation/link/schema validation, dependency and license policy, unsafe inventory changes, and selected fuzz seeds on supported host platforms.

Protected merge/release builds add sanitizers, full conformance shards, sandbox negative tests, deterministic integration suites, reproducible build comparison, SBOM/provenance, signing dry run, and package smoke tests.

Nightly jobs run fuzzing, broad WPT/Test262, performance, compatibility, long-run stability, and corpus minimization.

## 16. Flake policy

A flaky test is a bug. It is quarantined only with:

- owner and linked issue;
- observed failure rate and configurations;
- retained logs/traces/artifacts;
- expiry date;
- no masking of security, data-loss, sandbox, update, or agent-policy failures.

Retries may measure flakiness but do not convert a failing release gate into a pass.

## 17. Milestone exit report

Each milestone report includes:

- requirement status;
- test inventory and pass/fail/skip/crash/timeout counts;
- unsupported behavior;
- security gates and residual risk;
- fuzzing duration/coverage/crashes;
- performance and memory against baseline;
- accessibility matrix;
- platform/package status;
- known data-loss or recovery defects;
- dependency/unsafe/SBOM changes;
- go/no-go decision and signed owners.

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI framework conformance

Candidate adapters run one toolkit-neutral suite covering state sequences, commands, components, keyboard/focus, accessibility, IME, clipboard, drag/drop, localization, themes, page surfaces, crash/device loss, recovery, binary, memory, latency, frame pacing, and energy. Results include exact framework source, backend, renderer, features, license, platform, and raw artifacts.

<!-- WP-002-KERNEL-IPC-2026-07 -->
## Generated control-plane verification

CI now checks that the canonical IPC schema is valid and that committed Rust and process-capability documentation regenerate byte-for-byte. Unit and integration tests cover identity epochs, message limits, document scope, sequence gaps and duplicates, queue backpressure, launch denial, capability escalation, stale identities, denied routes, attenuated capabilities, channel endpoint binding, and shell-level authorization.

The next verification stage requires a fuzzable wire codec, malformed and unauthorized traffic corpus, peer-authentication tests, platform handle-transfer tests, compromised-process harness, transport crash/reconnect tests, and independent security review. Passing the M0 Rust tests does not imply sandbox or production IPC compatibility.
