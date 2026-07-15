# 16 — Governance, Contribution, and Engineering Process

## 1. Governance objective

Turing needs enough process to protect architecture, security, compatibility, and contributors without turning a research program into paperwork. Decisions are written because a browser’s behavior is too interconnected to live in one maintainer’s memory.

## 2. Roles

Initial roles may be held by the same person, but responsibilities remain distinct:

- **Program lead:** scope, milestones, release label, staffing, public claims.
- **Architecture owner:** cross-component contracts, dependency boundaries, ADR process.
- **Security owner:** threat model, sandbox, vulnerability response, supply chain, release gates.
- **Engine owners:** DOM/HTML, CSS/layout, graphics/text/accessibility.
- **Runtime owner:** JavaScript, GC, JIT, WebAssembly, bindings.
- **Network/storage owner:** URL/Fetch/protocols/cookies/cache/databases/service workers.
- **Platform owners:** macOS, Windows, Linux UI/sandbox/packaging.
- **DevTools/automation owner.**
- **AI/agent safety owner.**
- **Quality/performance owner.**
- **Release/operations owner.**
- **Accessibility owner.**

A supported subsystem has a primary and backup owner before stable release.

## 3. Decision classes

### Routine implementation

Changes that preserve approved interfaces and behavior proceed through normal pull-request review.

### Design note

A meaningful component behavior or data-model change uses a design note with problem, requirements, alternatives, security/performance/accessibility impact, test plan, and rollout.

### Architecture Decision Record

An ADR is required for:

- process/trust boundaries;
- programming language or major runtime choice;
- dependency category/foundation change;
- profile/storage format and compatibility contract;
- site-isolation/sandbox policy;
- JavaScript GC/JIT architecture;
- protocol versioning;
- update/signing/release trust;
- telemetry, sync, account, or remote AI data flow;
- license/governance model;
- irreversible compatibility commitment.

ADRs are immutable after acceptance; a superseding ADR explains the change.

### Security review

Any new parser, native library, IPC method, permission, device API, internal scheme, extension capability, DevTools privilege, agent observation/action, updater behavior, or secret flow requires security review.

## 4. Pull-request requirements

A pull request states:

- problem and user/developer impact;
- requirements and issues addressed;
- architecture/behavior changes;
- security, privacy, accessibility, compatibility, performance, memory, and platform impact;
- tests and benchmark results;
- dependency/unsafe/generated-code changes;
- unsupported behavior and follow-up;
- screenshots/traces only when they add evidence and are redacted.

Large changes are split by reviewable boundaries but not in ways that temporarily disable mandatory security checks on protected branches.

## 5. Review policy

- one qualified approval for routine low-risk code;
- code-owner approval for subsystem changes;
- security approval for trust-boundary changes;
- accessibility approval for critical product/semantic workflows;
- performance evidence for hot-path or memory-layout changes;
- two-person approval for release/signing/update policy;
- author cannot be sole approver of a protected release.

Review focuses on invariants and tests, not formatting already enforced by tools.

## 6. Commit and branch policy

- `main` is protected and expected to remain buildable;
- work lands through pull requests and merge queue;
- branches use descriptive prefixes such as `engine/`, `security/`, `agent/`, `platform/`, `docs/`;
- generated files are updated in the same change as source schemas;
- commits should be bisectable; security embargo branches use restricted access;
- force-push policy is allowed on personal branches but not protected release refs;
- releases use signed annotated tags from protected commits.

## 7. Issue taxonomy

Labels or fields cover:

- component and platform;
- type: bug, feature, conformance, security, performance, accessibility, docs, operations;
- severity/priority;
- milestone/gate;
- good-first/requires-design/blocked/external;
- reproducibility and affected versions;
- risk ID and requirement IDs.

Security vulnerabilities are not filed publicly before coordinated disclosure.

## 8. Definition of done

A change is done when:

- behavior and unsupported cases are documented;
- stable requirements are updated;
- tests include negative/error/lifecycle behavior;
- relevant WPT/Test262 or reduced test exists;
- fuzz target/corpus is updated for new parsers/state machines;
- security/privacy/accessibility impacts are addressed;
- performance/memory baseline is recorded for hot paths;
- logs/traces are redacted and bounded;
- dependencies/licenses/notices are updated;
- platform behavior is implemented or explicitly gated;
- no ownerless follow-up is required for the claimed milestone.

A demo is not definition of done.

## 9. Coding standards

### Rust

- stable Rust by default; nightly requires a pinned toolchain and ADR/design note if shipped;
- warnings denied in protected CI with documented platform exceptions;
- formatting and Clippy policy automated;
- avoid panics across trust boundaries and in recoverable input paths;
- errors are typed and retain context without secrets;
- integer conversions and allocation sizes are checked;
- channels/collections/recursion are bounded for untrusted input;
- `unsafe` follows the inventory and `SAFETY` policy;
- no global mutable state for profile/document/security identity;
- capability/identity types use newtypes, not strings or raw integers;
- tests live near algorithms; integration/security tests live under dedicated suites.

### Protocols and schemas

- stable numeric/string identifiers are never reused;
- unknown variants fail safely;
- sizes and nesting limits are schema-defined;
- compatibility and downgrade behavior are tested;
- code generation is deterministic;
- security fields are not optional merely for convenience.

### Documentation

- claims link to evidence;
- normative requirements use stable IDs;
- diagrams have text alternatives;
- examples avoid secrets and unsafe copy/paste defaults;
- current support tables include date/version;
- obsolete decisions are marked superseded, not silently rewritten.

## 10. Testing expectations by change

- parser/decoder: unit, corpus, fuzz, limits, malformed input;
- state machine: model/property tests and invalid transitions;
- IPC/broker: compromised-sender negative tests;
- UI: semantics, keyboard, focus, high contrast, reduced motion, platform test;
- rendering: semantic trace plus pixel/geometry where relevant;
- JS/GC/JIT: Test262, tier differential, stress, sanitizer/fuzz;
- network/storage: hermetic protocol, cross-origin/partition, fault/corruption;
- performance: before/after raw samples and trace for hot-path claims;
- agent: grant/epoch/risk/confirmation/adversarial cases;
- update/release: tamper, rollback, interruption, reproducibility.

## 11. Security reporting

`SECURITY.md` will state supported versions, private contact, encrypted channel, expected acknowledgment, disclosure approach, safe-harbor intent, and scope. Reports receive confidential tracking. Public issues that appear exploitable are moved to the private process without unnecessary reproduction details.

Researchers are not asked to test real users, exfiltrate data, persist, or disrupt services.

## 12. Contributor provenance and licensing

Original Turing code is MPL-2.0 unless a file states otherwise. Contributors certify they have the right to submit code through the project’s chosen DCO or CLA policy; the initial recommendation is Developer Certificate of Origin for an open research project, revisited before commercial relicensing is contemplated.

Copied code from Chromium, WebKit, Gecko, Servo, other engines, proprietary SDKs, tutorials, generated AI output, or third parties must not enter without provenance and license review. “Rewritten” code that closely follows a protected implementation may still create concerns; use standards, papers, clean-room notes, and independent tests.

AI-assisted contributions remain the contributor’s responsibility. The contributor must review correctness, security, originality, license implications, and tests; prompts or model output are not evidence of provenance.

## 13. Code of conduct and community safety

Adopt a standard code of conduct with clear reporting and enforcement. Technical disagreement is resolved through evidence and written alternatives. Security disclosures, accessibility feedback, and beginner questions receive respectful handling. Maintainers avoid public pressure to merge unsafe features for schedule or publicity.

## 14. Release governance

A release board records go/no-go against the maturity label. Required sign-off expands by channel:

- research/nightly: subsystem owner and CI evidence;
- developer preview: program, security, release, and affected platform owners;
- beta: plus engine/runtime/network/accessibility/quality owners and independent security status;
- stable: full board, support/incident capacity, published evidence and residual risks.

Any owner may block for a release-critical security, data-loss, update, accessibility, or misleading-claim issue. Overrides require a written risk acceptance by the program and security leads and cannot relabel an unsafe build stable.

## 15. Deprecation and compatibility

Public protocol, extension, policy, profile, and automation behavior has versioning and deprecation windows. Security fixes may require faster removal, documented with migration paths where feasible. Experimental APIs are namespaced or gated and carry no compatibility promise.

## 16. Project health metrics

Track without gaming:

- requirements/gates passed;
- conformance pass/fail/crash/timeout denominator;
- security findings by root cause and patch time;
- fuzzing coverage/time and unresolved crashes;
- regression age and flake rate;
- benchmark trends with raw evidence;
- accessibility matrix;
- dependency/unsafe surface;
- supported-subsystem bus factor;
- review and contributor retention;
- release/update success and rollback;
- user-reported data loss, spoofing, unauthorized agent action, and crashes.

Lines of code, number of features, closed issues, or benchmark wins are not standalone success metrics.
