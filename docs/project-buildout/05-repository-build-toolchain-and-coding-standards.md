# Repository, Build, Toolchain, and Coding Standards

Status: detailed research and professional operating baseline  
Owner: architecture, build, security, and language owners  
Last researched: 2026-07-16

## Purpose

Define the final workspace, dependency direction, reproducible developer environment, and hostile-input coding rules before implementation sprawls across incompatible conventions.

## Governing principles

- Crates follow ownership, privilege, replacement, and failure boundaries.
- Privileged code is smaller and more stable than hostile-input code.
- Stable Rust is the default; C ABI and native/platform boundaries are explicit.
- Every untrusted size, count, depth, duration, queue, and allocation is bounded.
- Cancellation, timeout, crash, restart, and OOM are ordinary control paths.

## Required contract

- Use a Cargo workspace organized into apps, crates, platform, schemas, tests, testdata, benchmarks, infra, security, and tools.
- Record each crate's owner, privilege, inputs, public status, unsafe allowance, platforms, resource budget, and failure boundary.
- Machine-check forbidden dependency edges and cycles.
- Pin Rust, C/C++, SDK, linker, Python, Node, generator, test-suite, and package-tool versions.
- Provide bootstrap and read-only doctor commands plus offline verified-source builds.
- Use typed IDs, checked arithmetic, bounded channels/collections, explicit lock ordering, structured errors, redacted structured logs, and SAFETY rationale for unsafe code.
- No general-purpose runtime or framework becomes browser-wide by convenience.

## Professional workflow

1. Approve workspace and component map.
2. Create skeleton crates and ownership metadata.
3. Add dependency graph and toolchain pinning.
4. Exercise bootstrap on fresh macOS, Windows, and Linux hosts.
5. Enforce format, lint, Miri/sanitizer/fuzz/property/model tests.
6. Review topology each milestone.

## Evidence and exit gates

- PBO-GATE-6: every production crate has ownership and privilege metadata.
- PBO-GATE-7: fresh-host bootstrap is reproduced by someone other than its author.
- PBO-GATE-8: unsafe and concurrency inventories reconcile with source.
- Release compilation has no undeclared network access.

## Risks and failure modes

- Too many crates increase compile and coordination cost.
- Too few create broad authority and coupling.
- Pinned tools can retain vulnerabilities.
- Safe Rust wrappers can hide unsound native contracts.

## Primary sources

- Cargo workspaces — https://doc.rust-lang.org/cargo/reference/workspaces.html
- Rust 2024 edition — https://doc.rust-lang.org/edition-guide/rust-2024/
- Rust API Guidelines — https://rust-lang.github.io/api-guidelines/
- Reproducible Builds — https://reproducible-builds.org/docs/

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.
