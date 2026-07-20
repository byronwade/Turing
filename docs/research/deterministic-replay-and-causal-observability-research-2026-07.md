# Deterministic Replay and Causal Observability Research - July 2026

Status: no-claim deferred research packet
Owner: quality, developer-experience, engine, security, privacy, performance, and operations owners
Research question: `RQ-39`
Related future routes: `WP-015`, `WP-018`, `PB-013`, `PB-020`
Research date: 2026-07-19

## Question

Which deterministic replay and causal-observability model makes difficult browser bugs reproducible and explainable without retaining secrets, weakening isolation, or turning diagnostics into a second authority path?

`RQ-39` remains deferred outside the active pre-build crosswalk. This packet expands its future route; it does not authorize a replay runtime, select a trace format, establish browser behavior, or promote any readiness gate.

## Evidence-backed observations

The following observations were checked against official primary project documentation on 2026-07-19:

1. Mozilla's `rr` project records an execution once and replays the recording deterministically, including reverse execution. Its model is valuable for low-level debugging, but its documented platform and execution assumptions cannot be treated as a portable browser product contract.
2. Firefox's official debugging guidance shows that a browser replay record can span multiple processes and that process identity is necessary to select the correct execution during replay. Turing therefore needs process, profile, origin, document, and restart-epoch identity in every cross-process causal record.
3. Chromium's trace-event guidance recommends static event names, explicit categories, documented ownership, typed arguments, and asynchronous tracks that can span threads or processes. It also calls out privacy filtering and warns against misleading events emitted while a thread is idle.
4. Chromium's Perfetto integration describes typed trace events as a more compact, efficient, stable, and privacy-filterable trace encoding. This is an observation about an upstream diagnostic system, not a recommendation to adopt Chromium or Perfetto.
5. Fuzzing and differential testing can find or reduce inputs, but they do not by themselves explain a causal chain. Replay, trace causality, reduction, conformance oracles, and independent review are separate evidence classes.

These observations support a layered research model: deterministic input/state replay for portable browser semantics; optional execution replay for selected debugging environments; and causal traces that explain ownership, ordering, policy, resource, and recovery decisions without becoming a privileged control channel.

## Model alternatives

| Model | Strength | Boundary or cost | Turing research disposition |
| --- | --- | --- | --- |
| Input and nondeterminism replay | Portable across platforms; retains browser-visible events, virtual time, random seeds, network responses, and selected state | Does not reproduce every scheduler or native-driver effect; requires explicit external-input capture | Required baseline for browser-level correctness and developer workflows |
| Deterministic execution replay | Can inspect difficult races and reverse through a recorded execution | Platform, architecture, system-call, device, binary, and performance constraints; recordings can contain highly sensitive data | Research option for bounded developer/debug environments, never an assumed release dependency |
| Semantic state snapshots plus event log | Supports targeted replay, reduction, redaction, and cross-version analysis | Snapshot completeness and schema evolution can hide omitted state or alter behavior | Required companion to input replay for engine and browser-state debugging |
| Causal trace without replay | Low overhead and useful for production-safe diagnostics | Correlation is not causation; missing events and clock skew can mislead | Required observability layer, with explicit uncertainty and completeness fields |
| Full browser recording | Broad forensic context | High storage, privacy, security, and retention burden; may capture credentials or page secrets | Reject as a default; consider only for explicit opt-in, bounded, redacted research capture |

No model is accepted by this comparison. The choice must be made per use case, platform, trust boundary, retention period, and claim.

## Proposed evidence contract

Every replay or trace artifact should bind:

- source revision, binary identity, build profile, feature flags, symbol/source-map identity, and dependency profile;
- host OS, architecture, display/GPU state where relevant, process topology, sandbox/site-isolation mode, profile class, and extension/agent state;
- browser session, profile, origin, top-level site, frame, document epoch, process epoch, tab, task, and capability identities;
- virtual clock, random seeds, network responses, storage inputs, device/input events, permission decisions, update state, and other nondeterminism that is intentionally captured;
- event schema version, category, static name, timestamp/clock domain, causal parent or track, sequence, producer, resource owner, policy result, and uncertainty/completeness status;
- redaction class, secret-handling decision, retention/expiry, encryption/access-control metadata, artifact hash, and deletion result;
- replay mode, expected oracle, outcome, divergence point, first differing event/state, failure denominator, reduction history, and reviewer disposition.

The schema must distinguish facts directly recorded from inferred causes. It must reject stale profile, origin, document, process, capability, and epoch identities rather than replaying them against a different authority context.

## Causal integrity rules

1. A trace event cannot grant capability, bypass policy, alter a navigation, or substitute for an authenticated command.
2. Cross-thread and cross-process causality uses explicit track/message/sequence identity; wall-clock proximity is insufficient.
3. Missing, filtered, dropped, redacted, sampled, or reordered events are represented as evidence limitations, not silently omitted.
4. Trace collection must be bounded by bytes, duration, event rate, nesting, queue depth, and retention policy, with defined overload behavior.
5. Sensitive page content, credentials, tokens, private URLs, clipboard data, and model/provider payloads are redacted at capture boundaries. Hashes and classifications must not be reversible secrets.
6. Replay runs in a non-authoritative diagnostic context. It cannot access live credentials, issue real network side effects, mutate the user profile, or send consequential agent actions.
7. A replay result is valid only when the binary, source, environment, input package, security configuration, and expected oracle are identified; a successful replay does not prove production behavior.

## Required experiments

1. Build a deterministic virtual-time/input harness for a small browser-state corpus covering navigation cancellation, tab lifecycle, IPC ordering, storage faults, permission changes, renderer restart, and accessibility focus.
2. Inject controlled nondeterminism, record the selected inputs, and measure replay success, divergence location, trace size, CPU/memory overhead, redaction cost, and reduction quality.
3. Compare input/state replay with an execution-replay prototype on at least one supported host and document unsupported platform, architecture, GPU, driver, and system-call cases.
4. Generate cross-process traces with explicit process/document/sequence identity and test delayed, duplicated, dropped, reordered, stale, and malicious events.
5. Run the same reduced failure through a correctness oracle, security negative tests, accessibility checks, and performance/resource attribution so diagnosis does not hide a regression.
6. Exercise retention, export, access, deletion, crash, disk-full, encryption-key loss, and profile-clearing behavior with synthetic secrets and no real user data.

## Evidence gates

Before `RQ-39` can support an implementation task or release-facing diagnostic claim, retain:

- a versioned schema and ownership/authority review;
- deterministic corpus, input-package, oracle, and reduction manifests;
- replay and trace artifacts with complete failure, divergence, drop, redaction, and unsupported denominators;
- negative tests proving diagnostics cannot expand authority or cross profile/origin/process boundaries;
- malformed-input, queue-pressure, timeout, cancellation, crash, restart, migration, low-memory, and disk-full tests;
- privacy/security review of capture, export, retention, encryption, access, and deletion;
- accessibility and developer-workflow evaluation for trace inspection and error recovery;
- fixed-host overhead measurements and comparison with a no-trace control;
- independent review, owner, revisit/expiry rule, and synchronized requirement, risk, work-package, task, and support records.

## Promotion and rejection rules

Promote only when the exact replay/trace scope, platform, trust boundary, retention policy, source/binary identity, oracle, and unsupported cases are explicit. Hold or reject when:

- “deterministic” means only that a screenshot looked similar;
- a trace infers causality from timestamps without identity and ordering evidence;
- a replay can contact real services, use live credentials, mutate user data, or emit consequential actions;
- redaction, dropped events, sampling, or missing process state are hidden in a success result;
- a low-overhead trace is used to claim complete diagnosis or a replay is used to claim browser correctness;
- execution replay is presented as portable across platforms without a tested support matrix;
- a fuzz finding or differential disagreement is treated as fixed without a retained reduced input, oracle result, and regression test.

## Current disposition

`RQ-39` remains `deferred_outside_current_prebuild_crosswalk`. Its owner route is quality, developer experience, engine, security, privacy, performance, and operations. Revisit it before deterministic replay, causal traces, or differential diagnostic evidence becomes an implementation task, a release support promise, or a public debugging claim.

## Sources

- [rr: lightweight recording and deterministic debugging](https://rr-project.org/)
- [Firefox debugging with rr](https://firefox-source-docs.mozilla.org/contributing/debugging/debugging_firefox_with_rr.html)
- [Chromium trace-event best practices](https://chromium.googlesource.com/chromium/src/+/main/docs/trace_events.md)
- [Chromium tracing architecture and Perfetto](https://chromium.googlesource.com/chromium/src/+/HEAD/base/tracing/README.md)
- [Perfetto track events](https://perfetto.dev/docs/instrumentation/track-events)
- [LLVM LibFuzzer](https://llvm.org/docs/LibFuzzer.html)

## Claim boundary

This packet does not establish deterministic replay, causal diagnosis, browser correctness, compatibility, security, privacy, accessibility, performance, production readiness, or Chrome-class behavior. It does not select `rr`, Perfetto, a trace format, a replay runtime, or a release diagnostic contract.
