# Turing Architecture Prototype

This directory contains a dependency-free Rust executable that models—not implements—the first browser invariants. It is intentionally small enough to audit in one review.

It demonstrates:

- explicit process roles and deny-by-default capabilities;
- bounded typed message envelopes;
- legal tab lifecycle transitions and protection reasons;
- ordered rendering invalidation;
- network requests carrying profile, origin, top-level site, document epoch, destination, and credential mode;
- deterministic AI-agent authorization by principal grant, profile, origin, action class, expiry, quota, document epoch, and confirmation.

It does not parse HTML, render pages, execute JavaScript, open network connections, create windows, or claim production security. Its purpose is to turn architecture statements into testable types before large subsystems are written.

## Build

```bash
cargo test --manifest-path prototype/Cargo.toml
cargo run --manifest-path prototype/Cargo.toml
```

The package uses only the Rust standard library. A stable Rust toolchain compatible with Edition 2021 is sufficient.

## Next implementation steps

1. Split the types into a workspace of kernel, IPC, lifecycle, network-context, trace, and agent-policy crates.
2. Generate protocol types from bounded schemas.
3. Add platform sandbox probe child processes.
4. Add a deterministic 30-tab pressure simulator and benchmark manifest output.
5. Begin HTML tokenizer and DOM-arena work behind separate fuzzable crates.
