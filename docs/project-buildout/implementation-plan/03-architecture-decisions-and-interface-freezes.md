# 03 — Architecture Decisions and Interface Freeze Points

Status: canonical decision schedule; proposed decisions remain unaccepted until their ADRs are approved  
Owner: architecture and subsystem owners

## 1. Why freeze points exist

Turing cannot freeze all APIs before evidence exists, but it also cannot let every subsystem change shape indefinitely. A freeze point means a versioned contract is stable enough for dependent work. It does not mean the contract can never change. Breaking changes require an explicit migration, compatibility window, and downstream impact review.

## 2. Decision classes

- **Charter decision:** changes what Turing is, such as using an existing browser engine.
- **Trust-boundary decision:** changes process, sandbox, credential, update, or agent authority.
- **Public-contract decision:** changes the embedding ABI, Plug-in API, DevTools protocol, profile format, or stable product behavior.
- **Foundation dependency decision:** adopts a library, toolkit, compiler backend, database, graphics layer, or native service.
- **Implementation decision:** selects an internal representation behind an already accepted boundary.
- **Experiment decision:** authorizes a bounded prototype without promoting it to production direction.

Charter, trust-boundary, public-contract, and high-privilege dependency decisions require ADRs.

## 3. Required decisions by phase

### Before production WP-006 through WP-009

- ADR-0009: Servo relationship and source strategy.
- Exact provenance and license boundary for any reused source or generated data.
- Initial engine crate boundaries and hostile-input ownership.

### Before framework-specific WP-004 production code

- ADR-0013: toolkit-neutral shell model and replaceable adapter.
- ADR-0014: initial native UI toolkit.
- ADR-0015: React design-lab boundary.
- ADR-0016: swapchain, page-surface, and compositor ownership.
- Dependency, licensing, accessibility, platform, and replacement review.

### Before public embedding or Plug-in implementation

- ADR-0010: stable C ABI and generated SDKs.
- ADR-0011: capability-based Turing Plug-ins.
- Package, version, signing, lifecycle, resource, and revocation contracts.

### Before broad autonomous implementation

- ADR-0017: task-scoped autonomous engineering.
- Protected branch, independent review, and run/evidence storage enforcement.

### Before stable scope or public updating

- ADR-0018: stable-v1 scope and support contract.
- ADR-0019: update trust separation.
- ADR-0020: human release and signing authority.

## 4. Interface freeze schedule

### IF-000 — Repository and identity baseline, M0

Freeze for dependent M0 work:

- stable requirement, risk, ADR, WP, task, process-role, capability, and message identifiers;
- root workspace membership rules;
- documentation and evidence locations;
- maturity/status vocabulary;
- task lifecycle and review states.

Breaking changes require repository-wide migration and validator updates.

### IF-001 — Kernel/process/control-plane research contract, late M0

Freeze version 0 research interfaces for:

- `ProcessIdentity` and restart epochs;
- process roles and launch authority;
- capability attenuation;
- bounded control envelope metadata;
- channel identity and sequence rules;
- generated schema ownership;
- broker registration semantics;
- trace identity fields.

The operating-system transport and wire codec may remain experimental, but must implement this contract or formally supersede it.

### IF-002 — Native shell and page-surface contract, M1

Freeze versioned contracts for:

- window, profile, Space, tab, view, surface, input, focus, and accessibility identities;
- UI snapshots and typed commands;
- page-frame delivery, damage, scale, color, synchronization, and device-loss events;
- renderer crash and surface replacement;
- accessibility subtree composition;
- platform adapter responsibilities.

### IF-003 — Static engine semantic contract, M2

Freeze versioned internal interfaces for:

- decoded input and source locations;
- tokenizer/tree-builder events;
- DOM handles, node lifetime, mutation epochs, and tree ownership;
- stylesheet and selector representation;
- computed-style identity and invalidation;
- fragments, display lists, hit-test data, and accessibility semantics;
- deterministic reference raster input.

### IF-004 — JavaScript/DOM binding contract, M3

Freeze:

- runtime value and object handles;
- realm, agent, job, task, and microtask identity;
- root and tracing interfaces;
- DOM wrapper identity and lifetime;
- Web IDL generated binding boundary;
- exception, cancellation, and OOM behavior;
- interpreter/JIT equivalence contract.

### IF-005 — Navigation and service contract, M4

Freeze:

- browsing-context group, site instance, frame, document epoch, navigation, history, and commit identities;
- request context, origin/site/partition, cookie, cache, and credential dimensions;
- storage keys, quotas, transactions, migration, and service-worker identities;
- download and brokered file-handle contracts;
- profile, Space, session, snapshot, and migration schema versioning.

### IF-006 — Developer, Plug-in, embedding, and agent protocols, M5–M6

Freeze experimental versioned surfaces for:

- DevTools domains and event ordering;
- WebDriver BiDi extensions;
- embedding lifecycle and C ABI handles;
- Plug-in manifests, capabilities, resource budgets, and events;
- agent observations, grants, actions, confirmations, audit, and revocation;
- protocol compatibility and deprecation windows.

### IF-007 — Package, update, and support contract, M5–M8

Freeze per release channel:

- artifact identity and layout;
- profile-format compatibility range;
- update metadata roles and expiry;
- rollback and minimum-secure-version behavior;
- crash/symbol/provenance formats;
- supported platforms and support duration;
- stable SLO and conformance thresholds.

## 5. Freeze evidence

An interface freezes only when:

- owner and backup or explicit unowned status are recorded;
- schema or API is versioned;
- valid, invalid, old-version, unknown-field, bounds, cancellation, and failure tests exist;
- threat and privacy review is complete for its authority;
- performance overhead is measured where it sits on a critical path;
- accessibility semantics are defined where user-facing;
- migration and rollback are defined;
- downstream consumers have a conformance test or generated client;
- the ADR or design review records known limitations.

## 6. Change after freeze

A breaking change requires:

1. change proposal and impact graph;
2. compatibility or migration strategy;
3. updated schemas and generated code;
4. old/new differential tests;
5. security and data-loss analysis;
6. release-channel and profile-version implications;
7. downstream owner acknowledgment;
8. deprecation period or explicit research-only reset.

An agent cannot silently break a frozen contract because a local refactor is easier.
