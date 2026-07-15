# Repository Map

Status: canonical repository-structure reference
Update rule: required for every file or directory addition, deletion, rename, or ownership change

## Durable structure

```text
.
├── AGENTS.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── config.yml
│   │   └── engineering.yml
│   ├── pull_request_template.md
│   └── workflows/
│       └── repository-validation.yml
├── docs/
│   ├── README.md
│   ├── contributing.md
│   ├── documentation-policy.md
│   ├── prototype.md
│   ├── repository-map.md
│   ├── research-log.md
│   ├── security.md
│   ├── start-here.md
│   └── blueprint-v1/
│       ├── README.md
│       ├── 01-charter-and-principles.md
│       ├── 02-capability-parity.md
│       ├── 03-language-and-dependency-strategy.md
│       ├── 04-system-architecture.md
│       ├── 05-web-engine.md
│       ├── 06-javascript-runtime.md
│       ├── 07-network-storage-media.md
│       ├── 08-security-and-sandbox.md
│       ├── 09-performance-memory.md
│       ├── 10-ai-agent-platform.md
│       ├── 11-product-ui-devtools.md
│       ├── 12-testing-compatibility.md
│       ├── 13-build-release-operations.md
│       ├── 14-roadmap-work-breakdown.md
│       ├── 15-risk-register.md
│       ├── 16-governance-contributing.md
│       ├── 17-architecture-decisions.md
│       ├── 18-source-bibliography.md
│       ├── 19-initial-backlog.md
│       ├── 20-definition-of-done.md
│       ├── 21-product-requirements.md
│       ├── 22-research-program.md
│       └── machine/
│           ├── agent-action.schema.json
│           ├── backlog.json
│           ├── benchmark-manifest.schema.json
│           ├── process-capabilities.json
│           ├── requirements.json
│           └── risks.json
├── prototype/
│   ├── Cargo.toml
│   └── src/
│       ├── agent.rs
│       ├── main.rs
│       ├── network.rs
│       ├── process.rs
│       ├── render.rs
│       └── tabs.rs
└── tools/
    ├── check_documentation_change.py
    └── validate_blueprint.py
```

## Ownership and purpose

### Root control and discovery files

- `AGENTS.md` defines mandatory behavior for human and software agents across the repository.
- `README.md` is the concise public entry point.
- `CONTRIBUTING.md` and `SECURITY.md` are short GitHub-discovery pointers to canonical documents under `docs/`.
- `LICENSE` states the original-source licensing policy.

Root Markdown must remain limited to these deliberate exceptions. Product and engineering prose belongs under `docs/`.

### `.github/`

This directory contains GitHub-specific workflow and contribution interfaces:

- `ISSUE_TEMPLATE/config.yml` directs security reports away from public issues.
- `ISSUE_TEMPLATE/engineering.yml` requires evidence, impact, and documentation analysis.
- `pull_request_template.md` requires requirements, risks, tests, and documentation impact.
- `workflows/repository-validation.yml` validates documentation, registries, Rust formatting, tests, and the executable prototype, and retains the validator output as a short-lived diagnostic artifact for every run.

Workflow files are operational configuration, not the canonical description of policy. The corresponding policy remains under `docs/`.

### `docs/`

This is the canonical documentation root.

- `README.md` is the complete documentation index.
- `start-here.md` states scope, maturity, definitions, and reading order.
- `documentation-policy.md` defines same-change documentation and impact review.
- `repository-map.md` is this file.
- `contributing.md` and `security.md` are canonical operating policies.
- `prototype.md` describes the executable model in `prototype/`.
- `research-log.md` records material research and governance changes.
- `blueprint-v1/` contains the complete architecture and execution baseline.
- `blueprint-v1/machine/` contains machine-readable evidence paired with the prose.

### `prototype/`

A dependency-free Rust executable that models selected architecture invariants. It is not a browser engine. Its canonical description is `docs/prototype.md`.

As implementation begins, new crates must have explicit subsystem ownership, privilege level, inputs, outputs, memory budgets, failure behavior, test strategy, and corresponding documentation before being added.

### `tools/`

Repository-local validation scripts with no third-party Python dependency:

- `validate_blueprint.py` validates the static repository and documentation graph.
- `check_documentation_change.py` validates minimum documentation impact across a Git diff.

## Placement rules

- New prose: `docs/<topic>.md` or the relevant indexed subdirectory.
- New machine-readable documentation support: the owning document’s `machine/` directory.
- New source: a clearly owned subsystem directory, documented before or with creation.
- New tests: colocated with the subsystem or under a documented shared test hierarchy.
- New benchmarks: under a future documented benchmark hierarchy with fixed manifests.
- Generated files: only when their source, generator, and regeneration command are documented.
- Temporary transfer chunks, bootstrap scripts, debug dumps, local traces, credentials, and editor artifacts must not remain in the durable tree.

## Change procedure

For every structural change:

1. update the tree above;
2. update the ownership and purpose section;
3. update `docs/README.md` when documentation topology changes;
4. update root navigation when entry points change;
5. update validation required paths and legacy-path checks;
6. update build, workflow, packaging, and ownership configuration;
7. remove obsolete references;
8. run repository validation.
