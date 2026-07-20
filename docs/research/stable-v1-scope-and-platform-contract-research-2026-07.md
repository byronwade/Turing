# Stable v1 Scope and Platform Contract Research - July 2026

Status: deferred `RQ-61` research packet; no stable scope, platform, or support claim
Owner: product, program, platform, architecture, security, accessibility, performance, release, support, and legal-community
Question: What finite capability and support boundary provides meaningful daily use while remaining maintainable by the actual team?

This packet consolidates the [Stable v1 Scope and Non-scope](../production-readiness/01-stable-v1-scope-and-non-scope.md), [Supported Platform and Hardware Matrix](../production-readiness/02-supported-platform-and-hardware-matrix.md), and checked no-claim [Reference Platform Support Scorecard](reference-platform-support-scorecard-2026-07.md). It does not select a platform, define stable capabilities, or authorize product implementation.

## Contract principles

- Stable v1 is a finite, versioned support contract, not a claim to implement everything Chrome supports.
- A capability is supported only when its user workflow, security boundary, accessibility path, compatibility denominator, recovery behavior, performance/resource behavior, ownership, and support response are evidenced.
- A platform row is supported only when installation, signing, sandboxing, updates, rollback, text and IME, accessibility, graphics/software fallback, power lifecycle, crash recovery, diagnostics, and support procedures pass the same declared release-equivalent bar.
- An excluded, experimental, not-evaluated, or unsupported item must be discoverable and must not be implied by user-agent branding, feature presence, successful compilation, or a partial workflow.
- Mobile, proprietary DRM without agreement, vendor account services, broad enterprise management, unrestricted third-party native Plug-ins, consequential agent actions, and unverified hardware/device APIs remain explicit candidates for exclusion until separate evidence and owner decisions exist.

## Scope record

The owner-reviewed stable-scope record must identify:

- supported browser workflows and their complete success/failure/unsupported denominators;
- web-platform capability classes, standards/revision sources, compatibility policy, proprietary gaps, and feature-promotion or deprecation rules;
- profile, Space, session, snapshot, migration, credential, private-session, and recovery formats;
- Plug-in, embedding, DevTools, automation, and agent authority surfaces, including prohibited actions;
- platforms, OS versions, architectures, hardware tiers, GPU/software fallback, display/input/IME, accessibility technologies, languages, package/distribution routes, and end-of-support dates;
- SLOs, memory/energy budgets, security and update policy, incident/support term, on-call capacity, legal/community review, named owners/backups, and customer-visible limitations.

Every row needs a status from `supported`, `experimental`, `planned`, `not_evaluated`, `unsupported`, or `excluded`, plus owner, evidence references, review date, expiry or revisit trigger, and safe user-visible behavior. “Not evaluated” is not “supported,” and “unsupported” is not a reason to omit the attempted case from a compatibility or workflow denominator.

## Platform decision sequence

The reference platform decision should proceed in this order:

1. Propose Windows, macOS, or Linux scope with exact OS/image, architecture, hardware, compositor/windowing environment, support term, and owner.
2. Reproduce the pinned toolchain and build on an independent fresh host or approved clean-VM equivalent.
3. Exercise native window/lifecycle, input/IME, accessibility and assistive technology, page-surface, graphics/device-loss, sandbox, package/update, crash/recovery, and diagnostics workflows.
4. Capture versions, configuration, source/build identity, raw logs, traces, tree snapshots or screenshots where appropriate, failures, timeouts, unsupported rows, and cleanup.
5. Run fixed-hardware latency, memory, energy, and stability measurements using the benchmark and resource-attribution contracts.
6. Reconcile profile/migration, package/update, incident, backup ownership, support, legal, and release authority before calling the row supported.
7. Record one owner-reviewed decision that synchronizes the stable-scope registry, platform scorecard, Blueprint, requirements, risks, ADRs, backlog, task scope, and public support language.

## Promotion and rejection rules

Stable scope must not be promoted when any required workflow has no denominator, when a platform is represented only by CI or a target triple, when accessibility is inferred from a semantic tree or automated checker alone, when a security or recovery boundary is untested, or when support/incident capacity is assumed rather than rehearsed. A narrow scope with explicit exclusions is preferable to an unmaintainable compatibility promise, but the choice remains an owner decision.

The next acceptable artifact is an owner-reviewed scope and platform decision packet with raw evidence, unsupported rows, claim wording, support term, rollback or deprecation path, and synchronized registry changes. A scorecard, source manifest, compilation result, or passing repository check is preparation only.

## Current disposition

`RQ-61` remains deferred and `PB-006` remains `not_selected`. This packet consolidates the decision route without selecting a platform or stable capability set, changing active/deferred counts, authorizing broad implementation, or changing the `90%` contained-M0 / `0%` full-build measures.

## Source records

- [Stable v1 Scope and Non-scope](../production-readiness/01-stable-v1-scope-and-non-scope.md)
- [Supported Platform and Hardware Matrix](../production-readiness/02-supported-platform-and-hardware-matrix.md)
- [Reference Platform Support Scorecard](reference-platform-support-scorecard-2026-07.md)
- [Native UI and Accessibility Closure Preparation](native-ui-and-accessibility-closure-preparation-2026-07.md)
- [Fresh-Host Toolchain Reproduction Closure Preparation](fresh-host-toolchain-reproduction-closure-preparation-2026-07.md)
