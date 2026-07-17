# 13 — Cross-Cutting Verification and Evidence

Status: normative evidence matrix for implementation work  
Owner: quality, security, performance, accessibility, compatibility, release, and documentation

## 1. Rule

A subsystem is not complete because its happy-path test passes. Every accepted task and work package must produce the applicable evidence below. A category may be marked not applicable only with an explanation and reviewer agreement.

## 2. Evidence classes

### EV-SPEC — specification and requirements

- exact normative source and revision;
- supported and unsupported subset;
- requirement, risk, ADR, and WP mapping;
- behavior for invalid, unknown, future-version, and platform-specific inputs;
- contradiction or ambiguity record.

### EV-UNIT — focused correctness

- deterministic unit tests;
- boundary values and integer/size overflow;
- invalid states and transitions;
- property/model tests where state space is meaningful;
- regression cases for every fixed defect.

### EV-CONFORMANCE — standards and protocol behavior

- WPT, Test262, WebDriver BiDi, protocol, ABI, or platform suite revision;
- complete denominator and skip reasons;
- raw results and reduced failures;
- differential results against multiple references where useful;
- no hidden compatibility exceptions.

### EV-SECURITY — authority and hostile input

- updated threat model and protected assets;
- trust boundary, identity source, capability, and broker analysis;
- malformed, stale, duplicate, reordered, oversized, unauthorized, confused-deputy, and resource-exhaustion tests;
- sandbox/mitigation evidence from release-equivalent artifacts;
- fuzzing, sanitizers, Miri/model checks, or formal models as applicable;
- secret/redaction review;
- independent review and residual risk.

### EV-PRIVACY — data flow

- collected, observed, stored, transmitted, and derived data classes;
- purpose, consent, retention, deletion, export, partitioning, and recipient;
- URL, identifier, credential, page content, model prompt, and diagnostic handling;
- private-session and enterprise-policy behavior;
- outage and service-shutdown behavior.

### EV-PERF — performance, memory, and energy

- hardware, OS, toolchain, build profile, process topology, security settings, and workload;
- warm/cold/cache/lifecycle state;
- p50/p95/p99 or appropriate statistics and sample count;
- physical and attributed memory reconciliation;
- CPU, GPU, disk, network, wakeup, energy, and thermal data where applicable;
- before/after raw samples and regression threshold;
- no benchmark-only code path.

### EV-A11Y — accessibility and usability

- semantic roles, names, descriptions, states, relations, actions, ranges, and live events;
- keyboard and focus behavior;
- screen reader, switch, zoom, contrast, forced-color, reduced-motion, and IME coverage;
- platform assistive-technology matrix;
- automated checks plus qualified human evaluation;
- latency and failure-state behavior.

### EV-RELIABILITY — failure and recovery

- cancellation, timeout, crash, hang, restart, partial write, disk full, OOM, device loss, network loss, clock change, suspend/resume, and power-loss cases where applicable;
- transactional or idempotent behavior;
- retry rules and unsafe replay prevention;
- user-visible recovery and data-loss statement;
- long-duration leak and stability tests.

### EV-COMPAT — versions and migration

- schema/API/protocol version;
- old/new compatibility matrix;
- unknown-field and future-version behavior;
- migration, downgrade, rollback, and deprecation;
- generated clients/conformance tests;
- profile and persisted-data implications.

### EV-OPERATIONS — build, package, update, and support

- reproducible build inputs and provenance;
- SBOM, notices, symbols, artifact digest, and signatures;
- install/update/rollback evidence;
- observability, alert, runbook, owner, and escalation;
- supported-version and end-of-life effects;
- service dependency and offline behavior.

### EV-DOCS — documentation and status integrity

- affected Blueprint chapters and detailed books;
- requirements, risks, ADRs, WPs, tasks, owners, and traceability;
- repository map and indexes;
- unsupported behavior and residual risk;
- commands, examples, and generated artifacts verified;
- no stale or contradictory claim.

## 3. Evidence bundle structure

Every task bundle contains:

```text
manifest.json
summary.md
requirements.json
commands.json
results/
logs/
benchmarks/
conformance/
security/
accessibility/
artifacts/
review.json
rollback.md
```

Sensitive evidence uses the private security process and is referenced by opaque identifier in public records.

## 4. Independent verification lanes

- **Implementation lane:** author tests and source.
- **Conformance lane:** suite and reduced-case reproduction.
- **Security lane:** hostile-input, sandbox, fuzz, and threat-path review.
- **Performance lane:** fixed-hardware runner and statistical review.
- **Accessibility lane:** platform AT and human task review.
- **Release lane:** package, provenance, install, update, rollback, and migration.

A single agent or person may contribute to several lanes, but security-sensitive and stable-release acceptance requires reviewer independence defined by policy.

## 5. Evidence retention

- source tests and schemas are permanent;
- raw benchmark and conformance artifacts follow versioned retention policy;
- release and signing evidence is retained for the support lifetime plus the legal/incident period;
- private vulnerability evidence follows restricted access and disclosure policy;
- generated summaries link exact immutable artifacts;
- expired or superseded evidence remains traceable and cannot silently support a current claim.

## 6. Failure classification

Every failure is classified as:

- implementation defect;
- specification ambiguity;
- unsupported feature;
- test defect;
- platform limitation;
- dependency defect;
- performance regression;
- security/privacy issue;
- accessibility issue;
- flaky/unstable environment;
- accepted expiring exception.

Quarantining a test requires an owner, reason, expiry, and blocking/non-blocking effect. A quarantine is not a pass.

## 7. Claim rule

A claim may be no broader than its evidence. “Fast,” “secure,” “compatible,” “accessible,” “private,” “low memory,” “stable,” and “Chrome-class” require named scope, environment, comparison method, denominator, date, and limitations.
