# Capacity and Sustainability Research - July 2026

Status: active `RQ-48` source-backed capacity and sustainability route; no staffing, funding, infrastructure, support, release, security, performance, or production claim
Owner: program, architecture, security, quality, performance, accessibility, release operations, legal-community, product, and support owners
Research date: 2026-07-19
Related questions: `RQ-25`, `RQ-31`, `RQ-45`, `RQ-47`, `RQ-48`, `RQ-60`, `RQ-62`, `RQ-66`
Related gates: `PB-002`, `PB-008`, `PB-009`, `PB-013`, `PB-018`, `PB-019`, `PB-020`

## Question

What staffing, funding, infrastructure, review capacity, and support capacity are required at each maturity for an independent browser to remain secure, compatible, accessible, performant, diagnosable, and maintainable?

This packet defines the evidence required to answer that question. It does not estimate the current team's capacity, name owners, approve a staffing plan, set product SLOs, or authorize a release.

## Why capacity is a product and safety boundary

Browser work does not end when the first window renders. Every supported platform and web capability creates continuing obligations for security response, dependency updates, standards and compatibility changes, accessibility regressions, crash and data-loss recovery, performance regression analysis, build infrastructure, release signing, user support, documentation freshness, and incident communication.

Capacity must therefore be evaluated against the support surface actually promised. A narrow, explicit support boundary with demonstrable coverage is stronger than a broad capability list that has no review, recovery, or incident owner.

## Source-backed observations

### Secure development requires an operating practice, not only code review

NIST SP 800-218 describes the Secure Software Development Framework as a set of practices that can be integrated into a development lifecycle to reduce vulnerabilities, address exploitation impact, and address root causes. For Turing, this means capacity must include secure design, dependency/provenance review, testing, vulnerability response, and evidence retention as recurring work, not one-time launch tasks.

### Error budgets connect reliability to change capacity

Google's SRE material defines service-level indicators and objectives, then uses an error budget to decide how much unreliability can be spent on change. It also describes freezing ordinary changes when the budget is exhausted, while continuing urgent security or corrective work. This is a useful control pattern for Turing, but it must be adapted to browser-specific dimensions: crash-free sessions, data integrity, security response, update recovery, compatibility, accessibility, startup/input latency, memory, energy, and diagnostic availability.

The observation does not establish numeric Turing SLOs. Numeric targets require owner approval, representative denominators, fixed measurement methods, and a support policy.

### Ownership must include the work around the code

The SRE material also distinguishes service ownership from an independent operations handoff and warns that automation maintained by a team with no long-term ownership can become stale or irrelevant. For a browser, the equivalent boundary includes build and release automation, benchmark infrastructure, corpus maintenance, crash triage, platform adapters, update metadata, incident rehearsal, documentation, and dependency refreshes.

No automation or AI-agent path may be treated as a substitute for named authority, independent review, or recovery capacity.

## Capacity dimensions

Evaluate each maturity and proposed support surface across:

- **Role coverage:** architecture, engine, JavaScript, networking, storage, security, sandbox, UI/runtime, accessibility, platform, graphics, media, performance, quality, build/release, incident response, legal/community, documentation, product, support, and agent operations.
- **Independence:** primary and backup owners, reviewer separation, two-person controls, recusal, escalation, and emergency replacement.
- **Time budget:** planned feature work, maintenance, dependency updates, compatibility work, accessibility review, incident response, documentation, and recurring evidence production.
- **Infrastructure:** clean hosts, CI, artifact storage, benchmark machines, test devices, assistive technology, crash collection, symbol storage, signing/release systems, and secure private intake.
- **Evidence throughput:** review latency, test/fuzz capacity, corpus refresh, benchmark repeatability, manual workflow coverage, and unresolved-risk aging.
- **Operational resilience:** incident coverage, on-call or equivalent response, rollback, migration repair, update recovery, disclosure, communication, and postmortem capacity.
- **Financial and legal sustainability:** compute, storage, devices, licenses, codec/patent review, security tooling, support commitments, and contingency budget.
- **Support boundary:** supported platforms, capabilities, update window, security response term, data recovery promise, accessibility scope, unsupported behavior, and end-of-life process.

## Maturity evidence contract

| Maturity | Minimum capacity evidence | Rejection condition |
|---|---|---|
| Research | Named question owner, bounded experiment, review path, reproducible environment, and evidence-retention budget | Research claims are made without a maintainer, denominator, or artifact owner |
| Contained M0 | Owner and reviewer for each approved work package, local reproducibility, no-claim task boundary, and controlled cleanup | M0 controls are mistaken for production staffing or broad implementation authority |
| Prototype / developer preview | Supported workflow list, platform and feature owner coverage, crash/security intake, update/recovery plan, and known-gap triage | A preview scope depends on primary-only coverage or cannot receive a security fix |
| Beta | Named primary and qualified backup coverage, executed incident rehearsal, release/update authority, compatibility/accessibility review cadence, and SLO/error-budget policy | Release scope exceeds demonstrated review, incident, support, or recovery capacity |
| Stable | Sustained owner coverage, independent security and release review, support term, vulnerability response, update rollback, data recovery, accessibility maintenance, and public unsupported matrix | Stable claims rely on templates, informal availability, or one-person authority |

## Required evidence record

For each proposed maturity and support scope, retain:

- role-to-subsystem ownership and qualified backup matrix with representative path coverage;
- time allocation and forecast for feature, maintenance, security, compatibility, accessibility, performance, release, support, and documentation work;
- infrastructure inventory with capacity, availability, retention, privacy, replacement, and cost assumptions;
- review queue measurements: age, severity, reviewer latency, blocked work, failed checks, and exception expiry;
- incident and vulnerability response records, including private intake, acknowledgement, containment, patch, backport, signing, update, disclosure, and postmortem capacity;
- dependency, platform, standards, accessibility, and benchmark refresh cadence with missed-refresh handling;
- SLI definitions, SLO candidates, denominators, exclusions, error-budget policy, and change-freeze or exception rules;
- support matrix with explicit unsupported behavior, update window, recovery boundaries, migration limits, and end-of-life procedure;
- funding and procurement assumptions for hardware, CI, storage, test devices, assistive technology, signing, legal review, and private operations;
- independent review, recusal, two-person-control, stale-access, succession, and emergency replacement evidence;
- named decision owner, independent reviewer, decision status, limitations, expiry, and synchronized requirement, risk, ADR, work-package, release, and support records.

## Browser-specific workload model

Capacity planning must model recurring work, not only implementation tickets. At minimum include:

1. Security triage for renderer, network, storage, GPU, decoder, extension, DevTools, agent, updater, dependency, and supply-chain findings.
2. Compatibility and standards updates across the supported web-platform denominator, including regression reduction and unsupported-feature documentation.
3. Native platform and accessibility maintenance across every supported OS, input method, screen reader, contrast mode, and graphics path.
4. Performance and resource regression work using fixed hardware, representative corpora, trace retention, and reproducible analysis.
5. Profile, session, migration, update, rollback, crash recovery, and data-integrity support.
6. Build, signing, release, incident, disclosure, documentation, support, and owner-backup operations.

If a proposed product scope cannot fund or staff these recurring obligations, reduce the scope or mark the capability unsupported. Do not compensate by weakening security, evidence, accessibility, recovery, or review gates.

## Measurement and review protocol

Measure capacity over a defined window and record planned versus actual work, review latency, unresolved-risk age, incidents, security response, dependency refreshes, test and fuzz throughput, benchmark availability, documentation drift, and owner coverage. Separate available hours from qualified hours; a person who is nominally assigned but unavailable, conflicted, untrained, or the only reviewer does not provide full coverage.

Use scenario exercises for security disclosure, dependency compromise, release rollback, data migration failure, platform breakage, accessibility regression, benchmark infrastructure loss, and owner unavailability. Preserve failed exercises and missing-capacity findings. A spreadsheet estimate, CI green state, or written intent is not execution evidence.

Review the capacity record at each maturity promotion and after major scope, platform, dependency, support, or threat-model changes. Expire assumptions rather than carrying them forward silently.

## Rejection and promotion rules

Reject a maturity or support claim when:

- a build-critical, security-critical, release-critical, accessibility-critical, or incident-critical path has no qualified backup or independent reviewer;
- support scope, security response term, update recovery, migration recovery, or unsupported behavior is not explicit;
- required infrastructure, hardware, assistive technology, private intake, signing separation, or artifact retention is unavailable or unbudgeted;
- SLOs or error budgets lack a denominator, measurement owner, response rule, or exception policy;
- planned capacity assumes uninterrupted single-owner availability or treats automation as authority;
- the evidence omits failed exercises, queue aging, documentation maintenance, dependency updates, or end-of-life work.

Promote only after the owner accepts the scope, the independent reviewer verifies the evidence, the required backups and authority controls exist, and synchronized records establish the new support boundary. Capacity evidence does not itself establish security, compatibility, performance, accessibility, production, or Chrome-class success.

## Current status and claim boundary

`RQ-48` is active in the readiness crosswalk. This packet closes a missing research-route and handoff-definition gap only. It does not name staff, approve funding, set SLOs, close `PB-019`, establish support capacity, authorize a release, or change the `90%` contained-M0 / `0%` full-build closure metrics.

## Next question

What finite first-build scope can the named owners and qualified backups actually maintain through security response, compatibility, accessibility, performance measurement, update recovery, and incident rehearsal, and what evidence will force scope reduction when capacity is exceeded?

## Sources

- [NIST SP 800-218: Secure Software Development Framework (SSDF) Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE: Production Services Best Practices](https://sre.google/sre-book/service-best-practices/)
- [Google SRE: Error Budget Policy](https://sre.google/workbook/error-budget-policy/)
- [Google SRE: Automation at Google](https://sre.google/sre-book/automation-at-google/)
