# Technology and Dependency Decision Research - July 2026

Status: deferred `RQ-41` source-backed decision route; no technology, language, framework, dependency, security, performance, license, provenance, or release claim
Owner: architecture, dependency, security, build, release, legal-community, and maintenance owners
Research date: 2026-07-19
Related questions: `RQ-41`, `RQ-44`, `RQ-46`, `ADR-0009`, `PB-002`, `PB-008`, `PB-009`, `PB-020`

## Question

Which languages, frameworks, and foundational dependencies minimize total security, performance, build, license, and maintenance cost for an independent browser while preserving replaceability, reproducibility, and a small trusted computing base?

This packet is a decision route, not a recommendation. It does not select Rust, a UI framework, a browser engine, a JavaScript runtime, a graphics abstraction, a codec stack, a storage engine, or any Servo component.

## Why the choice is not a package list

A browser foundation is a coupled set of language rules, unsafe boundaries, compiler and linker behavior, build scripts, generated output, native packages, licenses, advisories, platform adapters, and long-lived maintenance obligations. A dependency can be technically functional and still be unacceptable because its source cannot be reproduced, its license obligations are unresolved, its native build path is opaque, its security response is inadequate, or its replacement cost freezes an internal interface.

The decision unit is therefore:

`candidate foundation + exact versions and features + target platforms + build profile + native/runtime dependencies + generated outputs + source/provenance records + owner approval`

No conclusion may be drawn from a language name, a crate count, a passing local build, a popularity measure, or a benchmark in isolation.

## Source-backed observations

### Rust safety is conditional on explicit proof obligations

The Rust Reference distinguishes safe operations from `unsafe` operations and makes clear that `unsafe` marks obligations the compiler cannot verify. Raw-pointer access, unsafe calls and traits, unsafe extern declarations, and unsafe attributes require a contract that remains sound for safe callers. The Reference also warns that the listed undefined behavior categories are not an exhaustive formal model.

For Turing, a Rust baseline can reduce some classes of memory-safety risk, but it cannot turn FFI, platform handles, custom allocators, JIT memory, GPU resources, codecs, or build scripts into trusted code automatically. Every candidate must carry an unsafe and foreign-boundary inventory with safety invariants, owners, tests, and release relevance.

### Cargo resolves dependencies, but resolution is not provenance

The Cargo Reference defines manifests, workspaces, dependency specifications, source replacement, dependency resolution, features, profiles, build scripts, registries, and lockfile-related behavior as separate parts of the build model. A lockfile records a resolution for a configuration; it does not by itself prove that the source, registry, mirror, archive, generated output, build script, or native artifact used in a build is the intended one.

Source replacement and vendoring can change where packages are obtained while preserving package identity rules, but the project still needs an explicit source policy, checksums or equivalent content identity, mirror controls, freshness/revocation handling, and an independently replayable build record.

Build scripts are part of the dependency boundary. They may discover or generate files and can affect the build through environment, filesystem, compiler, linker, and native-tool interactions. Their outputs and side effects must be recorded rather than treated as invisible implementation detail.

### SPDX identifiers improve exchange but do not decide legal acceptability

SPDX provides standardized license and exception identifiers, license expressions, list-version metadata, source information, and SBOM concepts. Those fields improve machine-readable identification and exchange. They do not constitute legal advice, prove that a notice or source-offer obligation is satisfied, resolve patent or codec questions, or authorize distribution.

The project must preserve the exact observed license text and provenance alongside any SPDX expression, identify the list version used, and route interpretation and exceptions to the legal-community and release owners.

### Maintenance is a security and performance input

Dependency review must include advisories, release cadence, maintainer and ownership continuity, issue and patch latency, unsafe/FFI/native surface, build cost, binary and memory effects, platform coverage, replacement seams, and compatibility behavior. A small dependency with an opaque native build or no viable replacement can impose more long-term risk than a larger reviewed dependency with a stable boundary.

These are evaluation criteria, not evidence that any current candidate satisfies them.

## Candidate foundation classes

The first comparison must keep these classes separate:

1. Rust-first native implementation with reviewed specialist libraries and narrow platform FFI.
2. Rust implementation with selective, independently reviewed engine or subsystem components.
3. Mixed-language implementation where a specialist runtime or codec is isolated behind a typed, versioned boundary.
4. Existing browser-engine or framework adoption, including the source/provenance, license, maintenance, and independent-engine constraints in `AGENTS.md` and `ADR-0009`.
5. A proposed foundation rejected before prototype because its source, build, authority, license, replacement, or maintenance evidence fails the gate.

These classes are not ranked. A candidate must be compared at the component-boundary level; “all Rust” and “use the existing engine” are not sufficiently precise alternatives.

## Required evidence record

For every candidate foundation and selected feature profile, retain:

- exact source revision, package identifiers, registry or archive source, checksums, signatures where available, and retrieval dates;
- compiler, linker, SDK, target, host, shell, Cargo, registry, mirror, cache, and feature-profile versions;
- complete dependency graph, duplicate-version explanation, optional-feature closure, native package list, generated-output list, and SBOM;
- license and exception expressions, exact notices, source-offer obligations, patent/codec flags, and legal-community decision fields;
- unsafe, FFI, ABI, build-script, proc-macro, code-generation, dynamic-loading, and native-copy inventories;
- build-script and tool side effects for filesystem, process, network, environment, time, compiler, linker, and platform discovery actions;
- clean-host and independent replay results, retained logs, artifact hashes, source-tree state, cache/target policy, and failure classification;
- startup, compile, link, binary size, resident memory, peak memory, incremental rebuild, test, fuzz, sanitizer, and diagnostic measurements on fixed configurations;
- security advisories, response history, maintenance ownership, update policy, end-of-life risk, replacement path, and exception expiry;
- component boundary, authority, process, thread, allocator, panic, cancellation, and resource-accounting contracts;
- conformance, accessibility, compatibility, and platform support evidence where the dependency can affect user-visible behavior;
- named owner, independent reviewer, decision status, limitations, revisit trigger, and synchronized ADR, requirement, risk, backlog, and release records.

## Decision matrix

| Dimension | Required comparison | Rejection condition |
|---|---|---|
| Memory and safety | unsafe/FFI surface, invariants, sanitizer/fuzz evidence, process boundary, resource ownership | Safety depends on undocumented caller discipline or an unbounded native surface |
| Reproducibility | exact source, lock/resolution, vendoring or mirror policy, generated outputs, clean-host replay | A local build succeeds but source, toolchain, native downloads, or outputs cannot be replayed |
| Security | advisories, patch path, sandbox interaction, privilege, dynamic loading, build-time authority | Unreviewed code execution, network, credential, or platform authority is required in a privileged path |
| Performance | compile/link, startup, binary, memory, latency, frame pacing, energy, and workload-specific effects | A microbenchmark or language-level claim substitutes for end-to-end measurements |
| Compatibility | standards, platform, text, accessibility, codec, and API behavior | Compatibility cost is hidden in an unsupported or unmeasured native dependency |
| Legal and distribution | SPDX expression, exact text, notices, source offers, patents, codecs, and exceptions | License identity is known but distribution obligations or legal interpretation are unresolved |
| Maintenance | owner continuity, release cadence, issue/patch response, upgrade cost, replacement seam | No responsible upgrade path, stale security response, or unbounded fork burden |
| Replaceability | opaque stable boundary, schema/ABI, migration path, and independent test oracle | The dependency leaks internal types, global state, or authority into the browser kernel |

## Measurement protocol

Run each candidate under the same pinned host and target matrix, with separate debug, release, and instrumented profiles. Record cold and incremental build time, compiler and linker peak memory, artifact size, startup, input-to-present latency where applicable, resident and charged memory, CPU, energy, test and fuzz throughput, and failure/recovery behavior. Attribute costs to the dependency, generated output, native package, and integration boundary rather than reporting only whole-repository totals.

Use representative browser workloads and negative cases: malformed inputs, cancellation, tool failure, cache poisoning, source mismatch, unavailable native dependency, stale generated output, advisory discovery, license mismatch, platform absence, process restart, and resource exhaustion. Preserve raw logs and hashes. A passing self-test or dependency scanner is a control check, not a foundation decision.

## Rejection and promotion rules

Reject a candidate for release-path consideration when any of the following remains unresolved:

- source identity, license interpretation, source-offer, patent, or native-package provenance;
- unsafe, FFI, build-script, proc-macro, dynamic-loading, or platform authority without an owner and evidence;
- reproducible clean-host build or generated-output provenance;
- security advisory response, upgrade, replacement, or support boundary;
- component identity, thread/lifetime, panic, cancellation, allocator, or resource-accounting contract;
- compatibility, accessibility, performance, or energy denominator needed for the claimed role.

Promote only after the candidate-specific evidence record is complete, the independent reviewer has checked it, the owner has accepted or explicitly rejected the candidate, and all affected ADRs, requirements, risks, work packages, registries, and support boundaries are synchronized. A deferred route may inform future work but cannot authorize a dependency or implementation.

## Current status and claim boundary

`RQ-41` remains deferred outside the current pre-build crosswalk. This packet closes an organization and evidence-route gap only. It does not select Rust, Cargo, a framework, a dependency, a source strategy, a license, a runtime, a graphics stack, a codec, a storage engine, or a release foundation. It does not change `PB-002`, `PB-008`, `PB-009`, `PB-020`, `ADR-0009`, or the 90% contained-M0 / 0% full-build closure metrics.

## Next question

Which owner-approved candidate foundation and exact feature profile should receive the first independent source, dependency, unsafe/FFI, clean-host, legal, maintenance, and replacement review, and what evidence will cause it to be rejected rather than rationalized?

## Sources

- [Rust Reference: unsafety](https://doc.rust-lang.org/reference/unsafety.html)
- [Rust Reference: `unsafe` keyword](https://doc.rust-lang.org/stable/reference/unsafe-keyword.html)
- [Rust Reference: behavior considered undefined](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html)
- [Cargo Reference](https://doc.rust-lang.org/cargo/reference/)
- [Cargo source replacement](https://doc.rust-lang.org/cargo/reference/source-replacement.html)
- [Cargo build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html)
- [SPDX 3.0.1 specification](https://spdx.dev/wp-content/uploads/sites/31/2024/12/SPDX-3.0.1-1.pdf)
- [SPDX overview and license list](https://spdx.dev/learn/overview/)
