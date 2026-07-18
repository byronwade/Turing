# Turing Architecture Prototype

The `prototype/` directory contains a dependency-free Rust executable that models—not implements—the first browser invariants. It remains a separate research reference inside the root Cargo workspace and is intentionally small enough to audit in one focused review.

## Demonstrated invariants

- explicit process roles and deny-by-default capabilities;
- bounded typed message envelopes;
- legal tab lifecycle transitions and protection reasons;
- ordered rendering invalidation;
- network requests carrying profile, origin, top-level site, document epoch, destination, and credential mode;
- deterministic AI-agent authorization by principal grant, profile, origin, action class, expiry, quota, document epoch, and confirmation.

## Explicit non-capabilities

The prototype does not:

- parse HTML;
- build a DOM;
- apply CSS;
- lay out or paint content;
- execute JavaScript or WebAssembly;
- open network connections;
- create native windows;
- implement a platform sandbox;
- claim web compatibility or production security.

Its purpose is to turn architecture statements into testable types before large subsystems are written.

## Build and run

The preferred complete repository check is:

```bash
sh tools/check.sh
```

On Windows PowerShell, use the equivalent wrapper:

```powershell
.\tools\check.ps1
```

The prototype may also be checked directly through the locked root workspace:

```bash
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

Contributor and agent handoffs that touch the prototype still run the complete local gate set from [`docs/contributing.md`](contributing.md), including documentation validation, implementation-plan validation, ADR-0009 evidence validation, diff whitespace checks, and `xtask check`.

The package uses only the Rust standard library, retains Edition 2021, and declares Rust 1.97 as its minimum within the repository-pinned Rust 1.97.1 toolchain. It does not depend on the new production-oriented crates.

## Relationship to the M0 workspace

The root workspace now contains typed identity, IPC, kernel, UI-model, build-identity, shell-laboratory, and repository-tool packages. Those crates are the contained M0 implementation foundation. This prototype remains an independent oracle for earlier architectural invariants; it is not silently converted into the production browser.

The reference model intentionally defines roles, action classes, lifecycle states, protection reasons, and credential modes beyond those used by its executable smoke path. Such catalog items use targeted `#[expect(dead_code)]` annotations with reasons; the production-oriented crates do not receive broad dead-code exemptions.

## Change requirements

Every prototype change must update this document and the affected Blueprint chapters. Changes to process roles, IPC, request identity, tab lifecycle, rendering stages, or agent policy also require review of the threat model, architecture decisions, requirements, risks, and machine registries.

The prototype must remain honest about its scope. A passing executable is architecture evidence, not browser-readiness evidence.

## Next implementation steps

1. Expand the accepted `turing-types`, `turing-ipc`, and `turing-kernel` boundaries through bounded, independently reviewed tasks.
2. Generate protocol types from bounded schemas after the wire-format decision.
3. Add platform sandbox probe child processes.
4. Add a deterministic 30-tab pressure simulator and benchmark-manifest output.
5. Begin HTML tokenizer and DOM-arena work behind separate fuzzable crates after source-strategy review.

The roadmap and work-package dependencies remain canonical in [Blueprint v1](blueprint-v1/14-roadmap-work-breakdown.md) and the [initial backlog](blueprint-v1/19-initial-backlog.md).
