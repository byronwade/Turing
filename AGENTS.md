# AGENTS.md

This file governs every human or software agent working in this repository. Its scope is the entire repository unless a more specific `AGENTS.md` is added in a subdirectory.

## Mission

Turing is a research and engineering program for an independent browser and web engine. The long-term product target is a minimal, fast, secure, developer-first browser that can also serve everyday users and constrained AI agents.

The repository must distinguish clearly between:

- a researched or specified capability;
- a prototype or experiment;
- a partially implemented feature;
- a release-gated feature;
- a supported, production-safe capability.

Never describe a target as implemented, safe, compatible, faster, smaller, or complete without reproducible evidence.

## Required reading

Before changing anything, read:

1. [`docs/start-here.md`](docs/start-here.md)
2. [`docs/README.md`](docs/README.md)
3. [`docs/documentation-policy.md`](docs/documentation-policy.md)
4. [`docs/repository-map.md`](docs/repository-map.md)
5. the relevant Blueprint v1 chapters under [`docs/blueprint-v1/`](docs/blueprint-v1/README.md)
6. the relevant detailed engineering book linked from [`docs/README.md`](docs/README.md#detailed-engineering-books)
7. [`docs/security.md`](docs/security.md) and the [security engineering book](docs/security-engine/README.md) for trust-boundary or hostile-input work

## Core priorities

When priorities conflict, use this order:

1. security and correctness;
2. transparent compatibility and risk disclosure;
3. minimal resource use and predictable performance;
4. accessibility and user control;
5. developer ergonomics and visual refinement;
6. implementation convenience.

Minimalism means minimizing trusted code, ambient authority, duplicated state, hidden work, memory retention, dependencies, and user-visible complexity. It does not mean omitting required security, accessibility, compatibility, recovery, or diagnostics.

## Independent-engine boundary

Release paths must not depend on Chromium, Blink, V8, WebKit, JavaScriptCore, Gecko, SpiderMonkey, Electron, CEF, an operating-system web view, or remote rendering.

“From scratch” does not require unsafe reinvention. Use reviewed foundational libraries and platform primitives for cryptography, TLS, Unicode, font shaping, image/media codecs, compression, operating-system sandboxing, and similar specialist domains when the dependency review permits it.

Do not add custom cryptography.

## Documentation is part of every change

Canonical project documentation lives in `docs/`. The root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md`, plus GitHub templates under `.github/`, are deliberate discovery and workflow exceptions.

Every change must update every affected document in the same commit or pull request. Affected documentation includes prose, detailed engineering books, requirements, risks, ADRs, work packages, machine-readable registries, test plans, support statements, and repository navigation.

Do not touch unrelated documents merely to create churn. “Update all documentation” means update all documents whose truth, scope, status, links, ownership, assumptions, commands, interfaces, risks, or acceptance criteria changed.

### Mandatory documentation impact review

For every addition, modification, rename, or removal:

1. identify the user-visible, developer-visible, architectural, security, compatibility, performance, accessibility, operational, and AI-agent effects;
2. update the relevant canonical documents and detailed books;
3. update stable requirements, risks, ADRs, backlog entries, and machine registries when their meaning changes;
4. update `docs/repository-map.md` for any repository-structure change;
5. update `docs/README.md` and all inbound links for any documentation addition, rename, move, or deletion;
6. remove stale claims and obsolete instructions;
7. state unsupported behavior and residual risk;
8. run the repository validation commands.

A code-only feature change is incomplete. A documentation-only claim without evidence is also incomplete.

During the current single-owner research phase, documentation-only work may be committed directly to `main` only under the controlled exception in [`docs/blueprint-v1/16-governance-contributing.md`](docs/blueprint-v1/16-governance-contributing.md). The change must be atomic, main must not have moved, validation must pass, and implementation, accepted decisions, machine-registry status, security fixes, releases, and embargoed findings remain outside that exception.

### Documentation impact map

Use this as the minimum mapping, not a limit:

| Change area | Required documents to inspect |
|---|---|
| charter, scope, product claims | `01-charter-and-principles.md`, `02-capability-parity.md`, `21-product-requirements.md`, `docs/competitive/` |
| dependencies or language choices | `03-language-and-dependency-strategy.md`, `13-build-release-operations.md`, `18-source-bibliography.md` |
| process model, IPC, lifecycle, architecture | `04-system-architecture.md`, `08-security-and-sandbox.md`, `17-architecture-decisions.md`, `docs/security-engine/` |
| HTML, DOM, CSS, layout, paint, accessibility tree | `05-web-engine.md`, `11-product-ui-devtools.md`, `12-testing-compatibility.md`, `docs/engine/` |
| JavaScript, WebAssembly, GC, JIT, bindings | `06-javascript-runtime.md`, `08-security-and-sandbox.md`, `12-testing-compatibility.md`, `docs/javascript/` |
| network, storage, credentials, media, printing, PDF | `07-network-storage-media.md`, `08-security-and-sandbox.md`, `12-testing-compatibility.md` |
| performance, memory, startup, energy, tab lifecycle | `09-performance-memory.md`, `docs/performance/`, benchmark manifests, roadmap, and risks |
| AI observations, actions, providers, grants, audit | `10-ai-agent-platform.md`, `08-security-and-sandbox.md`, `docs/ai/`, agent-action schema, and risks |
| UI, accessibility, DevTools, automation | `11-product-ui-devtools.md`, `12-testing-compatibility.md`, `docs/developer-experience/`, `docs/api-design/`, product requirements |
| build, signing, updates, release, incident response | `13-build-release-operations.md`, `08-security-and-sandbox.md`, `docs/security.md`, `docs/security-engine/` |
| roadmap, milestone, backlog, or status | `14-roadmap-work-breakdown.md`, `19-initial-backlog.md`, `20-definition-of-done.md`, machine backlog |
| risk or architectural decision | `15-risk-register.md`, `17-architecture-decisions.md`, corresponding machine registry |
| repository layout, tools, CI, contributor workflow | `docs/repository-map.md`, `docs/documentation-policy.md`, `docs/contributing.md`, this file |

Blueprint paths in this table are relative to `docs/blueprint-v1/`.

## Research requirements

Research must be source-backed and reproducible.

- Prefer standards, specifications, official platform documentation, upstream source, test-suite documentation, peer-reviewed research, and vendor security material.
- Record the retrieval date, version, platform, and tested configuration when they affect the conclusion.
- Separate observations from inferences and proposals.
- Preserve contradictory evidence and unresolved questions.
- Do not copy implementation source from another engine without explicit provenance and license review.
- Record benchmark hardware, operating system, build profile, workload, process model, site-isolation state, tab state, sample count, and statistical method.
- Never compare memory or speed using undisclosed tab discarding, different workloads, different security settings, or unmatched builds.

Add durable findings to the relevant Blueprint chapter, detailed engineering book, bibliography, research program, requirements, risks, ADRs, or backlog. The chat, issue, or commit message is not the canonical record.

## Security and privacy rules

Treat all web, extension, automation, model, IPC, profile, file, network, media, and update input as untrusted unless a documented boundary proves otherwise.

- Use deny-by-default capabilities.
- Keep processes and principals least-privileged.
- Bound message sizes, recursion, queues, caches, tasks, and resource ownership.
- Preserve origin, site, profile, frame, process, and document-epoch identity across boundaries.
- Do not log secrets or place secrets in crash reports, traces, telemetry, model observations, or provider payloads.
- Page content and model output never expand authority.
- Consequential agent actions require deterministic authorization and visible confirmation where specified.
- Security-sensitive findings use the private process in `docs/security.md`, not public issues.
- Never weaken sandbox, site isolation, certificate validation, update verification, or permission policy to make a demo work.

## Engineering rules

- Prefer small, auditable components with explicit ownership and failure modes.
- Keep the browser kernel and privileged services smaller than renderer-facing code.
- Use stable Rust unless an approved ADR states otherwise.
- Every `unsafe` block requires a `SAFETY:` explanation and focused evidence.
- Avoid global mutable state for identity, policy, resource accounting, or lifecycle.
- Add regression tests with defect fixes.
- Add negative, timeout, cancellation, recovery, and resource-exhaustion tests where applicable.
- Keep headless, DevTools, automation, and agent paths on the same security and navigation machinery as interactive browsing.
- Do not merge placeholders that silently claim success, swallow failures, disable checks, or fabricate benchmark data.
- Generated files must identify their source and regeneration command. Edit the source of truth, not only the generated output.

## Repository changes

Before creating a file, determine whether an existing file should own the information. Avoid duplicate sources of truth.

When adding or removing a file or directory:

- update `docs/repository-map.md`;
- update relevant indexes and links;
- update validation allowlists or required-file lists deliberately;
- update CI, build, packaging, and ownership rules when applicable;
- remove obsolete references in the same change.

New prose documentation must be Markdown under `docs/` and must be linked from `docs/README.md` or from an indexed section beneath it. Machine-readable documentation support files may use JSON or schemas under the relevant `machine/` directory.

## Completion checklist

A task is complete only when all applicable items are true:

- implementation and documentation agree;
- affected Blueprint chapters, detailed books, requirements, risks, ADRs, backlog items, and registries agree;
- unsupported cases and residual risks are explicit;
- relevant tests and evidence exist;
- relative links resolve;
- repository navigation is current;
- no temporary bootstrap, transfer, debug, secret, or generated junk remains;
- the working tree contains only intentional changes;
- validation passes.

Run:

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

For pull-request documentation enforcement, CI also runs:

```bash
python3 tools/check_documentation_change.py <base-sha> <head-sha>
```

Do not bypass, weaken, or delete a failing validation rule without updating the governing documentation and explaining why the previous invariant is no longer correct.
