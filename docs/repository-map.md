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
│   ├── research/
│   │   ├── README.md
│   │   ├── browser-engine-landscape-2026-07.md
│   │   └── documentation-expansion-audit-2026-07.md
│   ├── engine/
│   │   ├── 01-pipeline-and-artifacts.md
│   │   ├── 02-html-parser-and-dom.md
│   │   ├── 03-css-cascade-and-invalidation.md
│   │   ├── 04-layout-and-fragmentation.md
│   │   ├── 05-paint-compositor-and-gpu.md
│   │   ├── 06-text-fonts-and-i18n.md
│   │   ├── 07-images-media-svg-and-canvas.md
│   │   ├── 08-input-editing-accessibility.md
│   │   ├── 09-memory-data-structures-and-observability.md
│   │   └── README.md
│   ├── javascript/
│   │   ├── 01-front-end-bytecode-interpreter.md
│   │   ├── 02-values-objects-shapes-and-inline-caches.md
│   │   ├── 03-garbage-collection-and-host-lifetimes.md
│   │   ├── 04-jit-tiering-ir-and-deoptimization.md
│   │   ├── 05-webassembly-webidl-and-event-loop.md
│   │   ├── 06-runtime-security-testing-and-performance.md
│   │   └── README.md
│   ├── security-engine/
│   │   ├── 01-threat-model-and-process-isolation.md
│   │   ├── 02-sandbox-brokers-and-platform-containment.md
│   │   ├── 03-memory-safety-jit-and-exploit-hardening.md
│   │   ├── 04-web-security-privacy-and-trusted-ui.md
│   │   ├── 05-update-supply-chain-and-vulnerability-response.md
│   │   ├── 06-security-verification-and-release-gates.md
│   │   └── README.md
│   ├── developer-experience/
│   │   ├── 01-protocol-architecture-and-versioning.md
│   │   ├── 02-devtools-workflows-and-ui.md
│   │   ├── 03-observability-tracing-and-replay.md
│   │   ├── 04-automation-headless-and-reproducibility.md
│   │   ├── 05-debugging-memory-performance-and-security.md
│   │   └── README.md
│   ├── api-design/
│   │   ├── 01-design-principles.md
│   │   ├── 02-async-streaming-and-cancellation.md
│   │   ├── 03-schemas-errors-versioning-and-compatibility.md
│   │   ├── 04-sdk-generation-authentication-and-redaction.md
│   │   └── README.md
│   ├── performance/
│   │   ├── 01-performance-model-and-critical-path.md
│   │   ├── 02-memory-allocation-and-cache-policy.md
│   │   ├── 03-scheduler-parallelism-and-latency.md
│   │   ├── 04-graphics-energy-startup-and-recovery.md
│   │   ├── 05-benchmarks-statistics-and-regression-governance.md
│   │   └── README.md
│   ├── ai/
│   │   ├── 01-agent-architecture-and-trust-boundaries.md
│   │   ├── 02-semantic-observations-and-redaction.md
│   │   ├── 03-actions-grants-confirmation-and-audit.md
│   │   ├── 04-memory-planning-multi-agent-and-lifecycle.md
│   │   ├── 05-providers-local-models-mcp-and-tools.md
│   │   ├── 06-evaluation-safety-performance-and-usability.md
│   │   └── README.md
│   ├── competitive/
│   │   ├── 01-chromium-blink-v8.md
│   │   ├── 02-webkit-javascriptcore.md
│   │   ├── 03-gecko-spidermonkey.md
│   │   ├── 04-servo.md
│   │   ├── 05-ladybird.md
│   │   ├── 06-browser-products.md
│   │   ├── 07-comparison-scorecard-and-adoption-rules.md
│   │   └── README.md
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
- `workflows/repository-validation.yml` validates documentation, registries, Rust formatting, tests, and the executable prototype, and retains validator output as a short-lived diagnostic artifact.

Workflow files are operational configuration, not the canonical description of policy.

### `docs/`

This is the canonical documentation root.

- `README.md` is the complete documentation index.
- `start-here.md` states scope, maturity, definitions, and reading order.
- `documentation-policy.md` defines same-change documentation and impact review.
- `repository-map.md` is this file.
- `contributing.md` and `security.md` are canonical operating policies.
- `prototype.md` describes the executable model in `prototype/`.
- `research-log.md` records material research and governance changes.
- `research/` contains dated evidence reports and audits. Research recommendations remain exploratory until accepted through owning Blueprint records.
- `blueprint-v1/` contains the normative architecture and execution baseline.
- `blueprint-v1/machine/` contains machine-readable evidence paired with the prose.

### Detailed engineering books

The following directories expand Blueprint chapters without replacing their normative ownership:

- `engine/` owns detailed rendering-engine research and contracts.
- `javascript/` owns detailed ECMAScript, GC, JIT, Web IDL, and WebAssembly research.
- `security-engine/` owns detailed process, sandbox, hardening, update, and assurance research.
- `developer-experience/` owns DevTools, protocol workflows, observability, automation, and diagnosis research.
- `api-design/` owns common interface, schema, versioning, cancellation, SDK, authentication, and redaction rules.
- `performance/` owns critical-path, memory, scheduler, graphics, energy, startup, recovery, and measurement research.
- `ai/` owns agent trust, observations, actions, memory, providers, MCP/tools, and evaluation research.
- `competitive/` owns per-engine, browser-product, comparison, and adoption studies.

Each directory has a `README.md` index. Child documents must link back to the relevant Blueprint owner and cannot silently change requirements, risks, ADRs, or support statements.

### `prototype/`

A dependency-free Rust executable that models selected architecture invariants. It is not a browser engine. Its canonical description is `docs/prototype.md`.

As implementation begins, new crates must have explicit subsystem ownership, privilege level, inputs, outputs, memory budgets, failure behavior, test strategy, and corresponding documentation before being added.

### `tools/`

Repository-local validation scripts with no third-party Python dependency:

- `validate_blueprint.py` validates the static repository, detailed-book topology, documentation graph, registries, and source hygiene. It permits exactly two trailing spaces only when used as an intentional Markdown hard break and rejects other trailing spaces or tabs.
- `check_documentation_change.py` validates minimum documentation impact across a Git diff.

## Placement rules

- New canonical policy or architecture prose: `docs/<topic>.md` or the relevant indexed subdirectory.
- New detailed subsystem design: the relevant engineering book, linked from its book index and mapped to a Blueprint owner.
- New dated research evidence: `docs/research/<topic>-<date>.md`, linked from `docs/research/README.md` and recorded in `docs/research-log.md`.
- New machine-readable documentation support: the owning document's `machine/` directory.
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
5. update validation required paths and legacy-path checks when integrity requirements change;
6. update build, workflow, packaging, and ownership configuration;
7. remove obsolete references;
8. run repository validation.
