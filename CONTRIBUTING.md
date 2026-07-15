# Contributing to Turing

Turing is an independent browser and web-engine research program. Contributions must preserve the distinction between an ambitious long-term target and currently verified behavior.

## Before writing code

Read [`START_HERE.md`](START_HERE.md), the [Blueprint v1 index](blueprint-v1/README.md), the [threat model](blueprint-v1/08-security-and-sandbox.md), and the [architecture decisions](blueprint-v1/17-architecture-decisions.md). Significant changes should begin as an issue or design note describing requirements, alternatives, security boundaries, compatibility, tests, and performance implications.

Do not add Chromium, Blink, V8, WebKit, JavaScriptCore, Gecko, SpiderMonkey, Electron, CEF, a system web view, or a remote-rendering fallback to a release path. Do not implement custom cryptography. Foundational dependencies require the review described in the language/dependency strategy.

## Local checks

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
```

The initial prototype has no third-party Rust dependencies.

## Pull requests

A pull request should state:

- problem and user/developer impact;
- requirement, risk, issue, or ADR identifiers affected;
- behavior and architecture changes;
- security, privacy, accessibility, compatibility, performance, memory, platform, and agent impact;
- tests, conformance results, fuzzing, and benchmarks;
- dependency, license, unsafe-code, generated-code, protocol, or profile-format changes;
- unsupported cases and follow-up work.

A demo without negative tests, lifecycle behavior, failure handling, and explicit unsupported cases is not complete.

## Security-sensitive changes

Changes to parsers, unsafe code, native libraries, process roles, IPC, sandboxing, site isolation, network/storage policy, permissions, credentials, internal pages, updates, extensions, DevTools, remote automation, AI observations/actions, logging, or telemetry require security review.

Use private reporting for suspected vulnerabilities; see [`SECURITY.md`](SECURITY.md).

## Rust standards

- Use stable Rust unless a pinned exception is approved.
- Represent profile, origin, site, frame, document epoch, process role, capability, and grant with typed values rather than strings at security boundaries.
- Bound untrusted sizes, nesting, recursion, queues, channels, caches, and task counts.
- Avoid panics in untrusted-input and recoverable runtime paths.
- Every `unsafe` block requires a `SAFETY:` explanation and appropriate Miri, sanitizer, fuzz, or targeted test coverage.
- Do not use global mutable state for identity or policy.
- Add the smallest useful regression test for every defect.

## Standards and provenance

Use primary standards and tests from the [source bibliography](blueprint-v1/18-source-bibliography.md). Established engines may be used for differential testing and research, but their source must not be copied without explicit provenance and license review.

Contributors are responsible for the originality and licensing of AI-assisted code. Model output is not proof that code is safe or unencumbered.

## Licensing

By contributing, you certify that you have the right to submit the contribution under the project’s MPL-2.0 policy. The project intends to use Developer Certificate of Origin sign-off before accepting broad external contributions; the exact bot/enforcement mechanism will be added with the governance setup.

## Conduct

Technical criticism should be specific, evidence-based, and respectful. Security reports, accessibility feedback, and beginner contributions receive careful handling. Schedule or publicity is not a reason to merge an unsafe or misleading change.
