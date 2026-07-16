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
│   │   ├── documentation-expansion-audit-2026-07.md
│   │   └── performance-security-developer-expansion-audit-2026-07.md
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
│   │   ├── 07-speculation-timers-and-side-channels.md
│   │   ├── 08-native-parser-and-codec-isolation.md
│   │   ├── 09-heap-sandboxes-pointer-tables-and-jit-compartments.md
│   │   ├── 10-capability-provenance-attenuation-and-revocation.md
│   │   ├── 11-developer-extension-automation-and-agent-attack-surfaces.md
│   │   ├── 12-anti-phishing-reputation-and-trusted-ui.md
│   │   └── README.md
│   ├── developer-experience/
│   │   ├── 01-protocol-architecture-and-versioning.md
│   │   ├── 02-devtools-workflows-and-ui.md
│   │   ├── 03-observability-tracing-and-replay.md
│   │   ├── 04-automation-headless-and-reproducibility.md
│   │   ├── 05-debugging-memory-performance-and-security.md
│   │   ├── 06-deterministic-replay-virtual-time-and-state-capture.md
│   │   ├── 07-source-maps-live-editing-and-local-development.md
│   │   ├── 08-diagnostic-bundles-and-automatic-reduction.md
│   │   ├── 09-generated-sdks-plugins-and-compatibility-adapters.md
│   │   ├── 10-integrated-accessibility-security-network-and-storage-debugging.md
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
│   │   ├── 06-data-locality-cpu-caches-and-numa.md
│   │   ├── 07-allocators-virtual-memory-and-page-reclamation.md
│   │   ├── 08-ipc-shared-memory-serialization-and-batching.md
│   │   ├── 09-pgo-lto-binary-layout-and-startup.md
│   │   ├── 10-causal-profiling-and-regression-diagnosis.md
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
│   ├── networking/
│   │   ├── 01-identities-and-request-context.md
│   │   ├── 02-network-service-and-brokers.md
│   │   ├── 03-dns-proxies-and-connection-racing.md
│   │   ├── 04-tls-certificates-and-client-auth.md
│   │   ├── 05-http1-http2-http3-and-quic.md
│   │   ├── 06-fetch-redirects-cors-and-security-policy.md
│   │   ├── 07-cache-preload-speculation-and-service-workers.md
│   │   ├── 08-cookies-partitioning-and-tracking-resistance.md
│   │   ├── 09-streaming-websocket-webtransport-and-downloads.md
│   │   ├── 10-observability-testing-and-resource-budgets.md
│   │   └── README.md
│   ├── storage/
│   │   ├── 01-storage-keys-buckets-and-partitioning.md
│   │   ├── 02-quota-eviction-and-pressure.md
│   │   ├── 03-indexeddb-transactions-and-durability.md
│   │   ├── 04-cache-storage-service-workers-and-background-work.md
│   │   ├── 05-cookies-sessions-and-private-data.md
│   │   ├── 06-profile-history-bookmarks-settings-and-journals.md
│   │   ├── 07-migrations-corruption-disk-full-and-power-loss.md
│   │   ├── 08-encryption-credentials-clearing-and-export.md
│   │   ├── 09-observability-repair-and-testing.md
│   │   └── README.md
│   ├── media-documents/
│   │   ├── 01-decoder-processes-and-input-limits.md
│   │   ├── 02-images-fonts-color-and-animation.md
│   │   ├── 03-audio-video-clocks-buffering-and-seeking.md
│   │   ├── 04-webrtc-capture-and-devices.md
│   │   ├── 05-codecs-hardware-acceleration-and-licensing.md
│   │   ├── 06-drm-and-content-decryption-boundaries.md
│   │   ├── 07-pdf-viewer-and-document-security.md
│   │   ├── 08-printing-pagination-accessibility-and-quality.md
│   │   └── README.md
│   ├── platform/
│   │   ├── 01-browser-chrome-scene-graph-and-trusted-surfaces.md
│   │   ├── 02-windows-surfaces-displays-and-lifecycle.md
│   │   ├── 03-input-ime-clipboard-and-drag-drop.md
│   │   ├── 04-macos-integration.md
│   │   ├── 05-windows-integration.md
│   │   ├── 06-linux-integration.md
│   │   ├── 07-credentials-notifications-and-external-protocols.md
│   │   ├── 08-packaging-startup-power-and-support-matrix.md
│   │   └── README.md
│   ├── accessibility/
│   │   ├── 01-engine-semantics-and-tree-generation.md
│   │   ├── 02-names-relations-text-ranges-and-editing.md
│   │   ├── 03-cross-process-and-cross-origin-composition.md
│   │   ├── 04-platform-accessibility-bridges.md
│   │   ├── 05-browser-ui-devtools-automation-and-agents.md
│   │   ├── 06-latency-event-coalescing-and-resource-use.md
│   │   ├── 07-testing-assistive-technology-matrices-and-release-gates.md
│   │   └── README.md
│   ├── release-operations/
│   │   ├── 01-build-identity-and-hermetic-toolchains.md
│   │   ├── 02-reproducible-builds-provenance-and-sbom.md
│   │   ├── 03-signing-keys-and-package-attestation.md
│   │   ├── 04-platform-packaging-and-installers.md
│   │   ├── 05-update-metadata-rollout-and-rollback.md
│   │   ├── 06-profile-migrations-and-downgrade-protection.md
│   │   ├── 07-crash-reporting-symbols-and-redaction.md
│   │   ├── 08-vulnerability-response-and-supported-lifecycle.md
│   │   └── README.md
│   ├── extensions-enterprise/
│   │   ├── 01-extension-processes-worlds-and-isolation.md
│   │   ├── 02-permissions-host-grants-and-user-control.md
│   │   ├── 03-event-driven-background-work-and-quotas.md
│   │   ├── 04-declarative-network-rules-and-native-messaging.md
│   │   ├── 05-extension-updates-devtools-and-agents.md
│   │   ├── 06-enterprise-policy-precedence-and-audit.md
│   │   ├── 07-accounts-sync-encryption-conflicts-and-quotas.md
│   │   └── README.md
│   ├── web-platform/
│   │   ├── 01-user-needs-and-design-principles.md
│   │   ├── 02-feature-lifecycle-and-standards-participation.md
│   │   ├── 03-tests-interop-and-dependency-graphs.md
│   │   ├── 04-privacy-security-accessibility-and-abuse-review.md
│   │   ├── 05-experiments-deprecation-and-compatibility-interventions.md
│   │   ├── 06-governance-evidence-and-public-dashboard.md
│   │   └── README.md
│   ├── benchmark-lab/
│   │   ├── 01-hardware-os-power-and-thermal-control.md
│   │   ├── 02-corpus-servers-and-network-control.md
│   │   ├── 03-startup-navigation-and-input-latency.md
│   │   ├── 04-frame-pacing-raster-composite-and-gpu.md
│   │   ├── 05-memory-process-topology-and-thirty-tabs.md
│   │   ├── 06-energy-accessibility-developer-agent-and-recovery.md
│   │   ├── 07-statistics-artifacts-regressions-and-claims.md
│   │   └── README.md
│   ├── quality-assurance/
│   │   ├── 01-conformance-suites-and-reduced-tests.md
│   │   ├── 02-fuzzing-property-model-and-formal-methods.md
│   │   ├── 03-differential-testing-and-oracles.md
│   │   ├── 04-fault-injection-chaos-and-long-duration.md
│   │   ├── 05-security-assurance-and-independent-review.md
│   │   ├── 06-flakes-release-evidence-and-go-no-go.md
│   │   └── README.md
│   ├── product-experience/
│   │   ├── 01-tabs-groups-workspaces-and-command-field.md
│   │   ├── 02-onboarding-migration-profiles-and-private-sessions.md
│   │   ├── 03-permissions-credentials-agents-and-trusted-ux.md
│   │   ├── 04-resource-manager-lifecycle-and-recovery.md
│   │   ├── 05-settings-updates-support-usability-and-accessibility.md
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

- `engine/` owns pipeline artifacts, html/dom, css, invalidation, layout, paint, gpu, text, media, input, accessibility, memory, and observability.
- `javascript/` owns front end, bytecode, interpreter, values, objects, inline caches, gc, jit, web idl, event loop, webassembly, testing, and performance.
- `security-engine/` owns threat model, isolation, sandbox brokers, native/jit hardening, side channels, trusted ui, updates, and assurance.
- `developer-experience/` owns protocols, workflows, causal tracing, replay, automation, sdks, reduction, and integrated diagnosis.
- `api-design/` owns identity, authority, bounds, async work, streaming, cancellation, schemas, errors, compatibility, sdks, authentication, and redaction.
- `performance/` owns critical paths, locality, allocation, virtual memory, ipc, scheduling, graphics, energy, startup, pgo, profiling, and regression governance.
- `ai/` owns trust boundaries, observations, redaction, actions, grants, confirmation, audit, memory, planning, providers, local models, mcp/tools, and evaluation.
- `competitive/` owns chromium, webkit, gecko, servo, ladybird, browser-product lessons, valid comparison, and adoption rules.
- `networking/` owns request identity, the network service, dns, proxies, tls, http, fetch policy, caches, cookies, streaming transports, downloads, diagnostics, testing, and resource budgets.
- `storage/` owns storage keys, quotas, indexeddb, cache storage, service workers, cookies, profile stores, migrations, corruption, encryption boundaries, clearing, repair, and recovery.
- `media-documents/` owns sandboxed decoders, images, fonts, audio/video, webrtc, capture, codecs, hardware acceleration, drm, pdf, printing, accessibility, licensing, testing, and energy.
- `platform/` owns browser chrome, windows, surfaces, input, ime, clipboard, drag-and-drop, macos, windows, linux, credentials, notifications, external protocols, packaging, startup, power, and support evidence.
- `accessibility/` owns engine semantics, accessible names, text ranges, cross-process trees, platform bridges, browser ui, devtools, automation, agents, latency, testing, and release gates.
- `release-operations/` owns build identity, hermetic toolchains, reproducibility, provenance, sboms, signing, packaging, updates, rollout, rollback, migrations, crash reporting, incident response, and support lifecycle.
- `extensions-enterprise/` owns extension processes, worlds, grants, event execution, rules, native messaging, updates, devtools and agents, enterprise policy, accounts, encrypted sync, conflicts, schemas, and quotas.
- `web-platform/` owns user needs, standards participation, feature lifecycle, dependency graphs, tests, interoperability, privacy/security/accessibility review, experiments, deprecation, compatibility interventions, and evidence dashboards.
- `benchmark-lab/` owns hardware tiers, os images, corpora, servers, startup, navigation, input, frame pacing, memory, process topology, 30 tabs, energy, accessibility, developer, agent, recovery, statistics, artifacts, and claims.
- `quality-assurance/` owns conformance suites, reduced tests, fuzzing, property/model/formal methods, differential testing, fault injection, chaos, longevity, security assurance, independent review, flakes, and release evidence.
- `product-experience/` owns tabs, groups, workspaces, command field, onboarding, migration, profiles, private sessions, permissions, credentials, agents, resource manager, lifecycle, recovery, settings, updates, support, usability, and accessibility.

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
