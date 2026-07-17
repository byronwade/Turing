# Repository Map

Status: canonical repository-structure reference  
Update rule: required for every file or directory addition, deletion, rename, or ownership change

## Durable top-level structure

```text
.
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── rustfmt.toml
├── clippy.toml
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── .github/
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
│       └── repository-validation.yml
├── apps/
│   └── turing-shell/
├── crates/
│   ├── turing-build-info/
│   ├── turing-ipc/
│   │   └── src/
│   │       ├── generated.rs
│   │       ├── envelope.rs
│   │       ├── queue.rs
│   │       └── sequence.rs
│   ├── turing-kernel/
│   ├── turing-types/
│   └── turing-ui-model/
├── schemas/
│   └── ipc/
│       └── control-plane.json
├── docs/
│   ├── README.md
│   ├── blueprint-v1/
│   ├── research/
│   ├── project-buildout/
│   ├── agent-execution/
│   ├── production-readiness/
│   ├── ui-runtime/
│   └── subsystem engineering books
├── prototype/
├── security/
│   ├── dependencies.json
│   ├── unsafe-code.json
│   ├── native-code.json
│   ├── generated-code.json
│   └── provenance.json
└── tools/
    ├── bootstrap.sh
    ├── doctor.sh
    ├── check.sh
    ├── generate_ipc.py
    ├── validate_blueprint.py
    ├── validate_build_foundation.py
    ├── check_documentation_change.py
    └── xtask/
```

The detailed documentation topology is indexed by [`docs/README.md`](README.md). It is intentionally not duplicated line-for-line here.

## Root workspace

`Cargo.toml` is the canonical Rust workspace definition. `Cargo.lock` is committed. `rust-toolchain.toml` pins the M0 compiler and required components.

Workspace membership must match [`workspace-components.json`](blueprint-v1/machine/workspace-components.json). Every component record declares:

- package and path;
- owner;
- privilege;
- hostile-input exposure;
- public or internal status;
- unsafe policy;
- supported development targets;
- internal dependencies;
- failure boundary.

`tools/validate_build_foundation.py` rejects missing components, dependency cycles, manifest/registry drift, toolchain drift, generated IPC drift, unledgered unsafe/native syntax, or M0 external runtime dependencies.

## `apps/`

Application binaries live here.

`turing-shell` is currently a command-line M0 integration laboratory. It exercises toolkit-neutral shell state plus the generated process/capability/IPC policy reference. It has no native UI, web engine, operating-system IPC transport, networking, storage, Plug-in, or AI capability.

Future application directories require an accepted purpose, owner, maturity label, support boundary, and package/update implications.

## `crates/`

Production-oriented Rust libraries live here. Crates are split by authority, ownership, replacement, and failure boundary rather than convenience.

Current crates:

- `turing-types`: shared non-zero identities, including restart-safe process identities;
- `turing-build-info`: build and maturity identity;
- `turing-ipc`: generated role/message contracts, bounded envelopes, exact sequence state, and bounded queues;
- `turing-kernel`: process registration, role launch policy, capability attenuation, route authorization, and channel binding;
- `turing-ui-model`: toolkit-neutral shell state and commands.

A toolkit, platform, GPU, network, storage, serializer, or runtime dependency may not enter these crates merely to accelerate a demo.

## `schemas/`

Canonical machine-readable interface definitions live here when they generate source or cross-language contracts.

`schemas/ipc/control-plane.json` owns the M0 control-plane protocol version, stable process-role and capability IDs, default capability sets, launch authority, message IDs, role-pair routes, document-scope rules, encoded-size limits, and queue budgets.

The schema is untrusted input to the generator. `tools/generate_ipc.py` validates it before producing committed Rust and documentation outputs. Schema changes require review of compatibility, authority, resource limits, generated diffs, tests, and migration implications.

## Generated IPC output

`tools/generate_ipc.py` deterministically generates:

- `crates/turing-ipc/src/generated.rs`;
- `docs/blueprint-v1/machine/process-capabilities.json`.

Run:

```bash
python3 -B tools/generate_ipc.py
python3 -B tools/generate_ipc.py --check
```

Generated output must not be edited directly. The source, generator, command, outputs, owner, and review boundary are registered as `GEN-IPC-001` in [`security/generated-code.json`](../security/generated-code.json).

## `prototype/`

The dependency-free architecture prototype remains a research executable. It is a reference model, not the production browser implementation.

## `security/`

Machine-readable source and supply-chain ledgers live here.

- `dependencies.json`: exact external runtime, build, and toolchain dependencies;
- `unsafe-code.json`: every approved unsafe island;
- `native-code.json`: FFI, native libraries, platform SDKs, build scripts, and dynamic code;
- `generated-code.json`: schemas, generators, commands, ownership, deterministic-output checks, and review boundaries;
- `provenance.json`: original-source license, contribution, source, and build attestations.

These files are not prose. Governing explanation remains under `docs/`.

## `tools/`

Repository-owned tools live here.

- `bootstrap.sh`: non-installing M0 environment entry point;
- `doctor.sh`: read-only environment diagnostics;
- `check.sh`: complete local check;
- `xtask`: cross-platform Rust implementation of bootstrap, doctor, and check;
- `generate_ipc.py`: deterministic control-plane schema validator and generator;
- `validate_blueprint.py`: documentation and program-record validation;
- `validate_build_foundation.py`: executable workspace, toolchain, generated-code, ledger, and source-policy validation;
- `check_documentation_change.py`: pull-request same-change documentation enforcement.

Tools must fail visibly, avoid hidden network access, preserve source-tree cleanliness, and document any generated output.

## Documentation

All durable prose belongs under `docs/`. Root Markdown is limited to repository discovery and agent-control files.

A new document must have an owner, status, unsupported behavior, evidence expectations, and an inbound link. Machine-readable companions use JSON under the owning `machine/` directory.

## Build output and temporary material

Build output, caches, transfer payloads, generated publication scripts, secrets, and local editor state are not durable source.

CI and wrapper commands set `CARGO_TARGET_DIR` outside the repository. The repository validator rejects known generated or temporary paths.

## Change procedure

For any structural change:

1. update this map;
2. update `Cargo.toml` and `workspace-components.json` when workspace membership or dependency direction changes;
3. update CODEOWNERS and professional ownership;
4. update dependency, unsafe, native, generated, and provenance ledgers;
5. update affected Blueprint, book, roadmap, traceability, and readiness records;
6. update validation and deterministic generation checks;
7. run `sh tools/check.sh`;
8. attach evidence, unsupported behavior, and rollback implications to the review.
