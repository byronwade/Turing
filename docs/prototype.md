# Turing Architecture Prototype

The `prototype/` directory contains a dependency-free Rust executable that models—not implements—the first browser invariants. It is intentionally small enough to audit in one focused review.

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

```bash
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

The package uses only the Rust standard library. A stable Rust toolchain compatible with Edition 2021 is sufficient.

## Change requirements

Every prototype change must update this document and the affected Blueprint chapters. Changes to process roles, IPC, request identity, tab lifecycle, rendering stages, or agent policy also require review of the threat model, architecture decisions, requirements, risks, and machine registries.

The prototype must remain honest about its scope. A passing executable is architecture evidence, not browser-readiness evidence.

## Next implementation steps

1. Split the types into a workspace of kernel, IPC, lifecycle, network-context, trace, and agent-policy crates.
2. Generate protocol types from bounded schemas.
3. Add platform sandbox probe child processes.
4. Add a deterministic 30-tab pressure simulator and benchmark-manifest output.
5. Begin HTML tokenizer and DOM-arena work behind separate fuzzable crates.

The roadmap and work-package dependencies remain canonical in [Blueprint v1](blueprint-v1/14-roadmap-work-breakdown.md) and the [initial backlog](blueprint-v1/19-initial-backlog.md).
