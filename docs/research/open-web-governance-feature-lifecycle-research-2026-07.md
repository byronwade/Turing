# Open-Web Governance and Feature-Lifecycle Research - July 2026

Status: no-claim deferred research packet
Owner: web-platform standards and interoperability
Research question: `RQ-33`
Related active route: `PB-002` / `TASK-000001` source strategy
Last reviewed: 2026-07-19

## Question

Which feature-lifecycle and open-web governance process should Turing use before selecting a web-platform feature for implementation or compatibility support, while preserving user needs, interoperability, privacy, security, accessibility, maintainability, and a credible multi-implementer path?

`RQ-33` remains outside the active pre-build crosswalk. This packet expands its future route; it does not create a task, select a feature, approve a standards source, or promote `PB-002` or `PB-020`.

## Relationship to current work

The checked [web-platform source manifest](../web-platform/machine/web-platform-source-manifest.json) separates the seven active PB-002 source-strategy questions from `RQ-33` deferred context. The manifest is a source inventory, not a feature decision. The active source-strategy lane must resolve source provenance, legal and maintenance boundaries, and engine strategy before any feature-specific compatibility work can become implementation-authorized.

## Evidence-backed observations

The following observations are recorded from official sources retrieved or checked on 2026-07-19:

1. WHATWG's working mode describes living standards as continuously maintained and provides commit-based snapshots for historical reference. A Turing evidence packet therefore needs the exact source identity used, rather than an unqualified product name or a moving URL.
2. The W3C Web Platform Design Principles put user needs first, require care when adding capabilities, prioritize compatibility when changing or removing behavior, and call for consideration of security, privacy, accessibility, internationalization, and different platforms and devices.
3. WPT, Test262, protocol suites, and interoperability dashboards are evidence inputs, not a complete support claim by themselves. Results require a pinned revision, harness and environment, selected scope, complete denominator, retained artifacts, and explicit expected failures and exclusions.
4. A feature can be technically implementable without being appropriate for Turing support. User value, multi-implementer interest, abuse review, accessibility, privacy, maintenance, and rollback or deprecation consequences are separate decision inputs.

These are research observations and process constraints. They do not establish that Turing currently implements or conforms to any web-platform feature.

## Feature promotion packet

Before `RQ-33` can move from deferred context into an active implementation lane, a feature packet must contain all of the following:

1. **User need:** named user or developer problem, affected workflows, alternatives considered, and evidence that the feature is not only an implementation convenience.
2. **Scope and identity:** feature name, exact normative sources and revisions, dependencies, API or language surface, origin and principal effects, and an explicit unsupported boundary.
3. **Interoperability:** relevant implementer and ecosystem context, WPT/Test262/protocol mappings, selected test scope, denominator rules, known differences, and a plan for multi-implementation validation.
4. **Security and privacy:** assets, trust boundaries, abuse cases, fingerprinting and data-flow consequences, permission and user-activation requirements, compromised-component behavior, and residual risk.
5. **Accessibility and internationalization:** semantic exposure, keyboard and assistive-technology behavior, localization, text direction, input methods, zoom, contrast, reduced motion, and platform differences.
6. **Lifecycle:** origin-trial or experiment boundary where applicable, feature detection, rollout, deprecation, removal, compatibility intervention, rollback, and user communication.
7. **Implementation economics:** privileged code, dependencies, maintenance owner, resource budgets, failure and recovery behavior, test cost, and release-support burden.
8. **Decision record:** alternatives, dissent, owner, independent reviewer, acceptance criteria, evidence locations and hashes, requirements, risks, ADRs, backlog, work package, and crosswalk changes to update atomically.

## Required evidence order

The packet must be assembled in this order so later claims cannot hide an earlier gap:

1. Freeze the feature question, user need, source identity, and scope.
2. Build the dependency graph from normative algorithms and host integrations to tests and implementation boundaries.
3. Map tests and fixtures, including pass, fail, timeout, crash, harness-error, leak, excluded, and not-run outcomes.
4. Run security, privacy, accessibility, internationalization, abuse, and resource-exhaustion review before feature selection.
5. Compare at least the intended semantic behavior, unsupported cases, and known multi-implementer differences.
6. Define experiment, rollout, rollback, deprecation, and support language before implementation work is proposed.
7. Obtain owner and independent review, then synchronize the canonical requirements, risks, ADR, backlog, work package, readiness, and research records.

## Promotion and rejection rules

`RQ-33` may be promoted only when the packet has a named owner, independent reviewer, pinned sources, executable evidence scope, complete denominator policy, security/privacy/accessibility review, explicit unsupported behavior, and synchronized decision records. A report, source manifest, passing validator, browser screenshot, single-engine result, or moving standards URL is insufficient.

Reject or hold the packet when any of the following applies:

- the user need is absent or is only an implementation convenience;
- the feature depends on a moving source without a revision or retrieval identity;
- compatibility evidence omits failures, exclusions, harness errors, or not-run cases;
- privacy, security, accessibility, internationalization, or abuse consequences are unreviewed;
- the feature expands trusted authority, origin access, fingerprinting surface, or resource budgets without an accepted policy;
- the support boundary relies on user-agent deception, hidden intervention, or proprietary behavior presented as standards parity;
- lifecycle, rollback, deprecation, maintenance, or ownership is unspecified;
- a proposed task or release claim would be inferred from research presence alone.

## Current disposition

`RQ-33` stays `deferred_outside_current_prebuild_crosswalk`. Its owner route is the web-platform standards owner and its revisit trigger remains: before a web-platform feature is selected for implementation or compatibility support. The next proof is a real feature-specific packet, not another generic source list.

## Sources and local controls

Official sources checked on 2026-07-19:

- [WHATWG working mode](https://whatwg.org/working-mode)
- [W3C Web Platform Design Principles](https://www.w3.org/TR/design-principles/)
- [W3C Privacy Principles](https://www.w3.org/TR/privacy-principles/)
- [Web Platform Tests](https://web-platform-tests.org/)
- [Interop project](https://wpt.fyi/interop)

Local controls:

- [Open Web Platform Governance Engineering Book](../web-platform/README.md)
- [Web-platform source manifest](../web-platform/machine/web-platform-source-manifest.json)
- [Web-platform source and conformance evidence](web-platform-source-and-conformance-evidence-2026-07.md)
- [Research-question coverage audit](research-question-coverage-audit-2026-07.md)
- [Research-readiness crosswalk](../blueprint-v1/machine/research-readiness-crosswalk.json)

## Claim boundary

This packet does not establish feature selection, implementation, compatibility, standards conformance, security, privacy, accessibility, performance, production readiness, or Chrome-class behavior. It does not change the active crosswalk, task queue, readiness registry, requirements, risks, ADRs, or support language.
