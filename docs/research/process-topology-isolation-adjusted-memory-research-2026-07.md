# Process Topology and Isolation-Adjusted Memory Research - July 2026

Status: source-backed active research handoff; no process topology, site-isolation relaxation, sandbox policy, memory claim, or performance decision accepted
Owner: architecture, security, IPC, performance, memory, platform, quality, and release operations
Research date: 2026-07-20
Related questions: `RQ-02`, `RQ-20`, `RQ-36`
Related gates: `PB-011`, `PB-012`, `PB-013`

## Question

Which process assignment and site-isolation strategies produce the best user responsiveness and resource behavior while preserving security equivalence, bounded IPC, crash containment, accessibility continuity, recovery, and explainable ownership?

This packet turns the process-topology question into a controlled research route. It does not select a topology, weaken site isolation, authorize a shared renderer, or establish a performance or security claim.

## Source observations

The following primary sources were checked on 2026-07-20:

| Source | Observation | Turing consequence |
| --- | --- | --- |
| [Chromium Process Model and Site Isolation](https://chromium.googlesource.com/chromium/src/%2Bshow/main/docs/process_model_and_site_isolation.md) | Chromium defines web-site instances as groups of documents/workers that must share access, then chooses which instances share processes. Separate processes improve isolation and fault containment but add memory overhead; resource availability can influence the choice. | A process count is not a security or performance metric by itself. Turing must record the site-instance partition, the reason for every sharing decision, security invariants, and resource tradeoff. |
| [Chromium Process Models](https://chromium.googlesource.com/playground/chromium-org-site/%2B/master/developers/design-documents/process-models.md) | Chromium describes multiple renderer allocation models, including process-per-site-instance, process-per-site, process-per-tab, and single-process forms, with explicit tradeoffs between memory and failure isolation. | A fair experiment needs named topology variants and must treat lower process count as a tradeoff, not an optimization. Any variant that changes the security boundary must be rejected or labeled non-equivalent. |
| [Chromium RenderingNG architecture](https://developer.chrome.com/docs/chromium/renderingng-architecture) | Multiple processes provide performance and security isolation between sites and browser state and stability/security isolation from GPU hardware; under pressure, same-site sharing can change while cross-site frames remain separated. | Pressure adaptation must be measured as a policy transition with effective isolation and identity evidence, not inferred from memory reduction. |
| [Firefox Process Model](https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html) and [Gecko Processes](https://firefox-source-docs.mozilla.org/ipc/processes.html) | Firefox separates parent, content, GPU, decoder, network, utility, service-worker, extension, and other process roles; isolated content can be keyed by site and container/private context. | Specialized processes and identity dimensions belong in the denominator. A topology that omits helpers, workers, extensions, private contexts, or media is incomplete. |
| [Firefox accessibility architecture](https://firefox-source-docs.mozilla.org/accessible/Architecture.html) | Accessibility trees span processes, with remote content trees cached and composed by the parent/UI process. | Process changes must test accessibility tree identity, focus, events, actions, and stale remote nodes; an accessibility regression is not an acceptable hidden cost of lower memory. |

These observations describe external architecture and measurement inputs only. They do not prove that any external topology is correct for Turing and do not authorize copying implementation source.

## Security and authority boundary

The minimum invariant for every candidate is that untrusted content cannot obtain another site instance's DOM, script state, storage, response body, credentials, accessibility subtree, compositor resource, capability, or privileged IPC route. The experiment must make the following explicit:

- site, origin, browsing-context-group, agent-cluster, frame, profile/container, private-session, worker, service-worker, extension, media, GPU, and utility identities;
- process role, sandbox policy, peer authentication, channel binding, capability set, lifecycle epoch, and revocation state;
- which resources may be shared, which must be isolated, and which are copied or brokered;
- the exact reason a process is created, reused, split, merged, frozen, killed, or restarted;
- the recovery and user-visible effect of a renderer, helper, GPU, network, or broker failure.

Process coalescing is not a valid optimization when it crosses an incompatible security boundary, changes effective sandbox policy, makes revocation ambiguous, or hides a larger crash blast radius. A resource controller cannot silently relax site isolation to satisfy a memory target.

## Candidate topology matrix

Compare these named candidates, or document why a candidate is out of scope:

1. **Site-instance isolation:** one process assignment per security-equivalent site instance, with separate helper roles.
2. **Site-group sharing:** compatible instances of a site may share a process under explicit same-site and lifecycle rules.
3. **Connected-tab grouping:** tabs linked by the browser's browsing-context or application relationship share where security and failure policy permit.
4. **Adaptive pressure topology:** process assignments change under declared resource pressure only after preserving identity, sandbox, site isolation, pending work, accessibility, and recovery guarantees.
5. **Control variants:** a deliberately weaker or single-process model may be used only as a diagnostic control; it cannot be a release candidate or a security-equivalent comparison.

Each candidate must include browser/kernel, content, GPU, network, media/decoder, storage, extension, DevTools, agent, and crash-recovery roles. “Renderer count” alone is not a topology description.

## Workload and host matrix

Run on declared 8, 16, and 32 GiB memory tiers when the experiment is authorized, with 5, 15, 30, and 100 tabs covering:

- same-site tabs, cross-site tabs, cross-site iframes, COOP/COEP or equivalent isolation, workers, service workers, media, images/fonts, and storage;
- extensions, DevTools, accessibility clients, private/container contexts, downloads/uploads, unsaved work, active calls/audio, and agent tasks;
- foreground interaction, background throttling, sleep/resume, low-memory pressure, process launch bursts, renderer crash, GPU loss, network failure, IPC timeout, cancellation, and recovery;
- mixed lifecycle states: active, background, frozen, serialized, discarded, restored, crashed, and protected from discard.

Record exact hardware, OS/image, driver/firmware, power/thermal/network controls, build, toolchain, security configuration, profile/cache state, corpus, browser pin, and process-policy configuration. Keep a control workload with no topology adaptation.

## Measures

Retain per process, site instance, tab, and shared service:

- private, resident, committed, reserved, shared, compressed, swapped, GPU, charged, and attributable memory;
- process count and role, launch time, startup faulting, CPU time, scheduler queue wait, wakeups, IPC message/copy/queue bytes, and shared-resource attribution;
- input-to-present, navigation-stage, frame-pacing, IPC, process-launch, freeze/revival, recovery, and teardown p50/p95/p99 latency;
- crash/hang blast radius, affected tabs/sites, restart time, state preservation, origin/profile identity, permissions, credentials, uploads, media, DevTools, agents, and accessibility tree continuity;
- sandbox and capability policy before/after pressure transitions, peer/channel identity, stale-epoch rejection, and denied cross-site access attempts;
- every timeout, failed launch, process reuse refusal, unsupported combination, pressure transition, kill, retry, cleanup event, and missing artifact.

The denominator includes all attempted scenarios and all topology variants. A lower aggregate memory value is invalid if it is caused by missing tabs, discarded work, weaker security, reduced accessibility, different cache/profile state, or omitted helper processes.

## Required artifacts

Before the lane can influence an accepted architecture, performance budget, or release profile, retain:

1. A topology manifest with candidate policy, identity keys, sharing rules, process roles, sandbox/capability policy, transition reasons, and unsupported combinations.
2. A security-equivalence matrix proving which site, origin, frame, worker, profile, private-session, extension, media, GPU, accessibility, and agent boundaries remain intact for each candidate.
3. A runner-generated process/lifecycle/resource package with exact process tree, identity and epoch events, raw samples, traces, failures, and SHA-256 manifest.
4. Transport evidence for authenticated peer/channel binding, bounded queues, malformed/reordered/wrong-principal messages, timeout, cancellation, and stale-epoch rejection.
5. Packaged sandbox and expected-deny evidence for every platform/policy combination in scope.
6. Recovery and accessibility fixtures covering remote tree composition, focus, input/IME, crash/hang, GPU loss, process restart, and user-protected activity.
7. Statistical analysis that reports topology-specific uncertainty, tail latency, memory attribution, crash blast radius, and unsupported/failure denominators.
8. Owner and independent review that selects, rejects, or defers each candidate and synchronizes ADR, requirements, risks, work package, task, benchmark, security, accessibility, and support records.

## Rejection rules

Reject a result as topology or performance evidence when it:

- compares process counts without site-instance, helper-process, sandbox, or capability identity;
- disables or weakens site isolation, sandboxing, accessibility, user protection, or active page behavior to win memory;
- treats same-site sharing, process reuse, or pressure adaptation as equivalent without proving the boundary and revocation behavior;
- omits service workers, extensions, DevTools, media, GPU, private contexts, accessibility trees, agent tasks, or crash recovery;
- measures only one memory category or hides shared/charged/attributable memory;
- discards tabs, changes security flags, changes cache/profile state, or omits failures without disclosure;
- treats a simulator, documentation, process diagram, or benchmark self-test as a browser-run result;
- claims Chrome-class, faster, lower-memory, lower-energy, safer, more compatible, or production behavior from this packet.

## Current status and next proof

`RQ-02`, `RQ-20`, and `RQ-36` remain research questions. `PB-011`, `PB-012`, and `PB-013` remain partial, and `TASK-000003`, `TASK-000004`, and `TASK-000005` remain proposed-only. The next controlled proof is a reviewed topology manifest and synthetic process/lifecycle fixture package after task authority, real transport, sandbox policy, and benchmark prerequisites are resolved.

This packet improves the process/security/performance handoff only. It does not select a process model, relax site isolation, accept IPC or sandbox evidence, promote a readiness gate, or change the 90% contained-M0 documentation organization or 0% full-build closure measures.

## Canonical related records

- [Research-question coverage audit](research-question-coverage-audit-2026-07.md)
- [Browser engine landscape](browser-engine-landscape-2026-07.md)
- [IPC Transport and Authority Closure Preparation](ipc-transport-and-authority-closure-preparation-2026-07.md)
- [Sandbox Probe Execution and Containment Closure Preparation](sandbox-probe-execution-and-containment-closure-preparation-2026-07.md)
- [Memory Object Representation and Tab Lifecycle Research](memory-object-representation-and-tab-lifecycle-research-2026-07.md)
- [Performance engineering book](../performance/README.md)
- [Threat model and process isolation](../security-engine/01-threat-model-and-process-isolation.md)
- [Build-readiness progress snapshot](../project-buildout/22-build-readiness-progress-snapshot.md)
