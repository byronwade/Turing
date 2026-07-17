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
│   ├── turing-kernel/
│   ├── turing-types/
│   └── turing-ui-model/
├── docs/
│   ├── README.md
│   ├── blueprint-v1/
│   │   └── machine/
│   │       ├── implementation-execution-graph.json
│   │       ├── implementation-milestone-gates.json
│   │       ├── implementation-interface-freezes.json
│   │       ├── implementation-evidence-catalog.json
│   │       └── implementation-task-sequence.json
│   ├── research/
│   ├── project-buildout/
│   │   └── implementation-plan/
│   │       ├── README.md
│   │       └── 01–17 execution chapters
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
    ├── validate_blueprint.py
    ├── validate_build_foundation.py
    ├── check_documentation_change.py
    └── xtask/
```

The detailed documentation topology is indexed by [`docs/README.md`](README.md). It is intentionally not duplicated line-for-line here.

## Root workspace

`Cargo.toml` is the canonical Rust workspace definition. `Cargo.lock` is committed. `rust-toolchain.toml` pins the M0 compiler and required components.

Workspace membership must match [`workspace-components.json`](blueprint-v1/machine/workspace-components.json). Every component record declares package/path, owner, privilege, hostile-input exposure, public/internal status, unsafe policy, targets, internal dependencies, and failure boundary.

`tools/validate_build_foundation.py` rejects missing components, dependency cycles, toolchain drift, unledgered unsafe/native syntax, or prohibited M0 external runtime dependencies.

## `apps/`

Application binaries live here.

`turing-shell` is currently a command-line M0 laboratory. It validates toolkit-neutral shell contracts but has no native UI, web engine, networking, storage, Plug-in, or AI capability.

Future applications require an accepted purpose, owner, maturity label, support boundary, task/WP mapping, and package/update implications.

## `crates/`

Production-oriented Rust libraries live here. Crates are split by authority, ownership, replacement, and failure boundary rather than convenience.

Current crates:

- `turing-types`: shared identities;
- `turing-build-info`: build and maturity identity;
- `turing-ipc`: bounded control-envelope foundation;
- `turing-kernel`: process roles and capabilities;
- `turing-ui-model`: toolkit-neutral shell state and commands.

A toolkit, platform, GPU, network, storage, or runtime dependency may not enter these crates merely to accelerate a demo.

## `prototype/`

The dependency-free architecture prototype remains a research executable. It is a reference model, not the production browser implementation.

## `docs/project-buildout/implementation-plan/`

This nested handbook is the canonical implementation game plan. It contains:

- M0 through M9 phase sequencing;
- the WP-001 through WP-018 critical path;
- agent startup, stop, review, rollback, and handoff rules;
- decision gates and interface freezes;
- subsystem milestone plans;
- cross-cutting evidence requirements;
- staffing, capacity, replan, replacement, and abandonment rules;
- work-package and delivery checklists.

It is linked from the root README, documentation index, project-buildout handbook, roadmap, backlog, pre-build checklist, and `AGENTS.md`.

## Implementation machine records

The five `implementation-*.json` files under `docs/blueprint-v1/machine/` provide machine-readable dependency, milestone, interface, evidence, and planned-wave records. They do not promote task or production status. The accepted backlog remains authoritative for WP dependencies, and only a reviewed ready `TASK-*` authorizes implementation.

## `security/`

Machine-readable source and supply-chain ledgers live here.

- `dependencies.json`: exact external runtime, build, and toolchain dependencies;
- `unsafe-code.json`: every approved unsafe island;
- `native-code.json`: FFI, native libraries, platform SDKs, build scripts, and dynamic code;
- `generated-code.json`: schemas, generators, commands, ownership, and deterministic-output policy;
- `provenance.json`: original-source license, contribution, source, and build attestations.

These files are not prose. Governing explanation remains under `docs/`.

## `tools/`

Repository-owned tools live here.

- `bootstrap.sh`: non-installing M0 environment entry point;
- `doctor.sh`: read-only environment diagnostics;
- `check.sh`: complete local check;
- `xtask`: cross-platform Rust implementation of bootstrap, doctor, and check;
- `validate_blueprint.py`: documentation and program-record validation;
- `validate_build_foundation.py`: executable workspace, toolchain, ledger, and source-policy validation;
- `check_documentation_change.py`: pull-request same-change documentation enforcement.

Tools must fail visibly, avoid hidden network access, preserve source-tree cleanliness, and document generated output.

## Documentation

All durable prose belongs under `docs/`. Root Markdown is limited to repository discovery and agent-control files.

A new document must have an owner, status, unsupported behavior, evidence expectations, and an inbound link. Machine-readable companions use JSON under the owning machine directory.

## Build output and temporary material

Build output, caches, transfer payloads, generated publication scripts, secrets, and local editor state are not durable source.

CI and wrapper commands set `CARGO_TARGET_DIR` outside the repository. Validation rejects known generated or temporary paths.

## Change procedure

For any structural change:

1. update this map;
2. update `Cargo.toml` and `workspace-components.json` when workspace membership changes;
3. update CODEOWNERS and professional ownership;
4. update dependency, unsafe, native, generated, and provenance ledgers;
5. update affected Blueprint, detailed book, implementation plan, roadmap, and readiness records;
6. update validation deliberately;
7. run `sh tools/check.sh`;
8. attach evidence, unsupported behavior, rollback, and downstream handoff to review.
