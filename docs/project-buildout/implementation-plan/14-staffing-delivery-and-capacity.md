# 14 — Staffing, Delivery, and Capacity Model

Status: program planning baseline; named qualified backups are still required before preview  
Owner: program and subsystem owners

## 1. Principle

A browser can be prototyped by a small team, but a stable general-purpose browser is an ongoing security, compatibility, accessibility, platform, and release operation. Scope must match sustained maintenance capacity, not only implementation speed.

## 2. Required ownership domains

At stable scale, Turing needs primary and backup ownership for:

- browser kernel, process model, IPC, lifecycle, and recovery;
- platform sandboxing and security architecture;
- HTML/DOM/events/editing;
- CSS/style/layout/text;
- paint/raster/compositor/GPU;
- JavaScript parser/interpreter/JIT/GC/WebAssembly/Web IDL;
- networking/TLS/HTTP/Fetch/cache/cookies;
- storage/databases/service workers/migrations;
- media/images/fonts/PDF/printing/devices;
- native shell/platform integration/accessibility/localization;
- DevTools/automation/headless/protocols;
- Plug-ins/enterprise/accounts/sync;
- AI/agent policy/providers/evaluation;
- compatibility/WPT/Test262/fuzzing/quality;
- performance/memory/energy/benchmark laboratory;
- build/release/signing/update/provenance;
- crash/telemetry/services/privacy operations;
- vulnerability response/incident/on-call;
- documentation/governance/community/support/legal coordination.

One person may own multiple early research domains, but stable support cannot rely on one unavailable individual for all critical paths.

## 3. Maintainer ladder

- **Contributor:** bounded source/docs changes under review.
- **Component reviewer:** reviews correctness and tests for one component.
- **Subsystem maintainer:** owns architecture, roadmap, incidents, and releases for a subsystem.
- **Security/accessibility/performance specialist:** provides independent cross-cutting review.
- **Release operator:** executes packages, signing, rollout, rollback, and evidence.
- **Release authority:** approves supported release scope and promotion.

Authority is granted by demonstrated evidence and reviewed responsibility, not commit count alone.

## 4. Capacity accounting

Each milestone plan records:

- available maintainers and reviewer hours;
- on-call and incident obligations;
- expected standards/compatibility churn;
- dependency and platform update burden;
- test and CI infrastructure cost;
- service and storage cost;
- hardware laboratory availability;
- legal/licensing work;
- documentation and support load;
- contingency for security emergencies.

Roadmap scope is reduced when maintenance demand exceeds capacity.

## 5. Delivery cadence

Use small, dependency-ordered trains:

- weekly or continuous M0/M1 research merges where evidence is complete;
- milestone integration branches only when interfaces require coordinated validation;
- nightly research artifacts after the package laboratory exists;
- preview/beta/stable trains only with channel-specific release gates;
- no date-driven merge of a failing security, data-loss, accessibility, or update gate.

## 6. Work-in-progress limits

Default limits until measured throughput exists:

- one active high-authority kernel/sandbox task per reviewer;
- one active interface-freeze proposal per affected subsystem;
- no more parallel platform implementations than can receive native review;
- no broad feature campaign while critical CI, fuzzing, update, or incident debt is unresolved;
- no new supported platform without primary and backup owners.

A long queue of partially integrated features is treated as risk, not progress.

## 7. Build-versus-adopt decisions

Every major component compares:

- Turing-owned implementation;
- audited foundational library;
- platform service;
- isolated helper process;
- generated adapter;
- deferred or unsupported capability.

The decision accounts for semantics, security, performance, binary size, memory, accessibility, license, provenance, update cadence, maintenance, replacement, and staffing. “From scratch” never requires custom cryptography or unaudited specialist code.

## 8. Infrastructure plan

Required program infrastructure grows by phase:

- M0: source hosting, CI, artifact retention, dependency/provenance checks;
- M1: platform runners, sandbox machines, reference hardware, signed research packages;
- M2–M4: WPT/Test262 farms, fuzzing, corpora, hermetic protocol servers;
- M5: crash symbols, update service, preview distribution, compatibility dashboards;
- M6–M7: media/device labs, Plug-in store test service, AI evaluation infrastructure;
- M8: production signing, staged update, on-call, support, status, disaster recovery;
- M9: expanded hardware/platform matrix and sustained standards infrastructure.

## 9. Funding and sustainability

Before stable release, document:

- hosting, CI, bandwidth, signing, hardware, service, audit, legal, and support costs;
- funding source and continuity;
- infrastructure account ownership and recovery;
- service shutdown/export plans;
- conflict-of-interest and sponsor influence rules;
- how user privacy and open-web commitments survive funding changes.

## 10. Scope-reduction order

When capacity is insufficient, reduce in this order before weakening security or quality:

1. postpone new market opportunities;
2. reduce supported platforms;
3. reduce Plug-in/API breadth;
4. defer proprietary media/DRM/services;
5. narrow stable web-platform scope transparently;
6. pause stable release and remain preview/research;
7. never remove required sandboxing, update verification, accessibility, recovery, or incident disclosure to preserve schedule.
