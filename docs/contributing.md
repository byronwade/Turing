# Contributing to Turing

Turing is an independent browser and web-engine research program. Contributions must preserve the distinction between an ambitious target and currently verified behavior.

## Before writing code

Read:

- [Start here](start-here.md)
- [Documentation policy](documentation-policy.md)
- [Blueprint v1](blueprint-v1/README.md)
- the relevant [detailed engineering book](README.md#detailed-engineering-books)
- [Threat model](blueprint-v1/08-security-and-sandbox.md)
- [Security engineering book](security-engine/README.md) for hostile-input or trust-boundary work
- [Architecture decisions](blueprint-v1/17-architecture-decisions.md)
- root [`AGENTS.md`](../AGENTS.md)

Significant changes should begin as an issue or design note describing requirements, alternatives, security boundaries, compatibility, accessibility, tests, performance, memory, operational impact, and documentation impact.

Do not add Chromium, Blink, V8, WebKit, JavaScriptCore, Gecko, SpiderMonkey, Electron, CEF, a system web view, or remote rendering to a release path. Do not implement custom cryptography. Foundational dependencies require the review in the language and dependency strategy.

## Documentation requirement

Every change must update every affected canonical document and detailed engineering companion in the same commit or pull request. This includes code, configuration, workflows, dependencies, features, interfaces, risks, requirements, ADRs, benchmarks, schemas, repository structure, and removals.

At minimum:

- update `repository-map.md` for every file or directory addition, deletion, or rename;
- update `README.md` and affected book indexes for documentation topology changes;
- update the owning Blueprint chapter and detailed book together when their truth changes;
- update prose and machine-readable registries together;
- update all relative links and commands;
- state unsupported behavior and residual risks;
- explain why other documentation is unaffected.

See the [documentation policy](documentation-policy.md).

## Local checks

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

The initial prototype has no third-party Rust dependencies.

## Pull requests

A pull request must state:

- problem and user/developer impact;
- requirement, risk, issue, work-package, or ADR identifiers affected;
- behavior, data-flow, lifecycle, and architecture changes;
- security, privacy, accessibility, compatibility, performance, memory, energy, platform, and agent impact;
- tests, conformance results, fuzzing, sanitizers, and benchmarks;
- dependency, license, unsafe-code, generated-code, protocol, schema, or profile-format changes;
- Blueprint and detailed-book documentation updated and documents reviewed but unchanged;
- unsupported cases, residual risks, rollback, and follow-up work.

A visual demo without negative tests, lifecycle behavior, failure handling, recovery, resource accounting, and explicit unsupported cases is not complete.

## Security-sensitive changes

Changes to parsers, unsafe code, native libraries, process roles, IPC, sandboxing, site isolation, network or storage policy, permissions, credentials, internal pages, updates, extensions, DevTools, remote automation, AI observations or actions, logging, crash reporting, telemetry, or release infrastructure require security review.

Use private reporting for suspected vulnerabilities; see the [security policy](security.md).

## Rust standards

- Use stable Rust unless a pinned exception is approved in an ADR.
- Represent profile, origin, site, frame, document epoch, process role, capability, and grant with typed values at security boundaries.
- Bound untrusted sizes, nesting, recursion, queues, channels, caches, and task counts.
- Avoid panics in untrusted-input and recoverable runtime paths.
- Every `unsafe` block requires a `SAFETY:` explanation and appropriate Miri, sanitizer, fuzz, or targeted test evidence.
- Do not use global mutable state for identity, policy, lifecycle, or resource accounting.
- Add the smallest useful regression test for every defect.
- Test cancellation, timeout, exhaustion, crash, restart, and stale-epoch behavior where applicable.

## Standards and provenance

Use primary standards and tests from the [source bibliography](blueprint-v1/18-source-bibliography.md). Established engines may be used for differential testing and research, but their source must not be copied without explicit provenance and license review.

Contributors are responsible for the originality and licensing of AI-assisted code. Model output is not proof that code is safe, correct, original, or unencumbered.

## Dependencies

A dependency proposal must document:

- exact purpose and why standard library or existing code is insufficient;
- privilege level and untrusted-input exposure;
- memory, CPU, startup, binary-size, and build-time cost;
- maintenance health, release cadence, security history, and ownership;
- license and distribution obligations;
- feature flags and transitive dependencies;
- replacement or removal plan;
- fuzzing, sanitizer, and platform coverage where relevant.

## Licensing

By contributing, you certify that you have the right to submit the contribution under the project's MPL-2.0 policy. Developer Certificate of Origin enforcement is planned before broad external contribution intake.

## Conduct

Technical criticism should be specific, evidence-based, and respectful. Security reports, accessibility feedback, and beginner contributions require careful handling. Schedule, publicity, visual polish, or benchmark pressure is not a reason to merge unsafe, inaccessible, misleading, or undocumented work.

## Expanded research library

Before work in networking, storage, media/documents, platform integration, accessibility, release operations, extensions/enterprise/sync, web-platform behavior, benchmarks, quality assurance, or everyday product workflows, read the corresponding index linked from [the documentation index](README.md#detailed-engineering-books). Research proposals include exact sources, experiments, evidence, risks, unsupported behavior, and the owning Blueprint relationship.

## Professional change workflow

Significant work identifies owner and backup status, requirement/traceability impact, RFC/ADR class, required cross-cutting reviewers, configuration, Plug-in/embedding, dependency/provenance, migration, evidence, rollback, release/support, and any expiring exception.
