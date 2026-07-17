# 13 — Build, Release, Distribution, and Operations

## 1. Build-system goals

The build must be reproducible, reviewable, cacheable, cross-platform, and usable by contributors without proprietary infrastructure. Cargo is the Rust workspace driver. A thin repository tool orchestrates code generation, third-party builds, conformance suites, packaging, signing, and artifact manifests.

Build inputs are explicit:

- source commit and submodule/vendor revisions;
- Rust/compiler/linker/SDK/tool versions;
- target platform, architecture, minimum OS, feature set, channel, and optimization profile;
- generated-code schemas and generator versions;
- third-party source archives with hashes;
- environment variables that affect output;
- signing step separated from reproducible unsigned payload creation.

Network access is disabled during release compilation after dependencies are fetched into a verified source cache.

## 2. Repository layout target

```text
apps/                 browser shell, headless, tools
crates/               Rust components
platform/             macOS, Windows, Linux adapters
schemas/              IPC, DevTools, agent, trace, requirements
third_party/          manifests, patches, licenses; source strategy documented
tests/                component, integration, security, UI, compatibility
testdata/             generated/redistributable corpora
benchmarks/           definitions, runners, baselines
infra/                CI, builders, packaging, update metadata
security/             threat models, sandbox profiles, unsafe inventory
spec/                  design and behavior notes
docs/                  contributor and user documentation
tools/                 hermetic repository utilities
```

Large upstream conformance repositories and proprietary licensed modules are not committed casually; exact fetch and verification mechanisms are documented.

## 3. Build profiles

- `dev`: assertions, tracing, fast incremental compile, no safety claim.
- `test`: deterministic hooks, fault injection, virtual time, extra verification.
- `fuzz`: sanitizers/instrumentation, hardened limits, corpus interfaces.
- `profile`: near-release optimization plus rich symbols and tracing.
- `release`: full mitigation and optimization policy, stripped/split symbols, signed packaging.
- `hardened-no-jit`: JIT disabled, maximum feasible mitigations, used for comparison and emergency response.

A feature flag cannot silently disable site isolation, sandboxing, update verification, or high-risk agent confirmation in a normal signed profile.

## 4. Code generation

Schemas generate:

- IPC messages and role/capability tables;
- DevTools and agent protocol types/clients;
- Web IDL bindings;
- CSS property/value tables;
- HTML tokenizer tables where used;
- settings, policy, command, telemetry, trace, and requirement registries;
- localization keys and accessibility metadata checks.

Generated files include source hash and generator version. CI verifies regeneration produces no diff. Generators validate bounds and reject duplicate or unstable identifiers.

## 5. Dependency and third-party handling

A lockfile is mandatory. Third-party metadata records source, version, license, copyright, patches, features, build flags, advisory status, and owner. Native libraries build from source where feasible; system-library use is explicit per platform.

Automated gates check:

- approved license policy and notices;
- known advisories and yanked packages;
- duplicate versions and dependency growth;
- build scripts, proc macros, network access, native code, and binary artifacts;
- source checksum and provenance;
- minimum supported toolchain;
- patch divergence from upstream.

Updates arrive through reviewable pull requests with compatibility, fuzz, and performance evidence.

## 6. Continuous integration

### Pull request

- formatting, lint, compile, unit/component tests;
- docs links, stable IDs, JSON/YAML/TOML/schema validation;
- dependency/license/unsafe inventory diff;
- generated-code consistency;
- selected integration, WPT/Test262 shards, and fuzz seed corpus;
- package build smoke test where affordable.

### Merge queue

- all supported host platforms/architectures available in CI;
- sanitizer variants and process/sandbox integration;
- deterministic rendering and protocol tests;
- performance smoke thresholds;
- reproducibility comparison for unsigned artifacts.

### Nightly

- broad conformance shards;
- continuous fuzzing and corpus reduction;
- long-run stability, tab churn, memory leaks, sleep/wake, update simulation;
- fixed-hardware performance/energy/30-tab tests;
- dependency/advisory/license re-scan;
- installer/update smoke tests.

### Release candidate

- clean protected commit and signed tag;
- hermetic rebuild on independent workers;
- full security, compatibility, accessibility, performance, migration, rollback, and package matrix;
- SBOM, provenance, symbol, license, source, and support artifacts;
- manual platform smoke and security-indicator review;
- approval by release, security, platform, engine, and product owners.

## 7. Artifact model

For each platform/architecture/channel, publish:

- installer/package and portable form where supported;
- update payloads and signed metadata;
- exact version/commit/build ID;
- symbols or symbol-server index with controlled access for embargoed fixes;
- SBOM and provenance attestation;
- third-party notices and corresponding source offer where licenses require;
- checksums and signatures;
- compatibility, security-gate, performance, and known-issues report;
- reproducibility instructions and comparison result.

Artifacts are immutable. A bad release is superseded or revoked, not silently replaced under the same version.

## 8. Versioning and channels

Use semantic product versions plus monotonically increasing build IDs. Channels:

- `nightly`: frequent, diagnostics enabled, no compatibility/support promise;
- `preview`: milestone demos, explicit unsafe/incomplete warnings;
- `dev`: signed developer builds with automatic updates and documented subset;
- `beta`: broader validation and staged rollout;
- `stable`: support and emergency patch commitment;
- optional `esr/lts`: only after staffing and backport capacity exist.

Engine, DevTools protocol, agent protocol, profile schema, and extension API have separate compatibility versions.

## 9. Signing and key management

Release signing keys are hardware-backed or threshold-controlled, access-logged, and unavailable to pull-request builds. Platform-specific signing/notarization occurs after reproducible unsigned payload verification.

Key policy covers:

- roles for root/update targets/snapshot/timestamp-like metadata where adopted;
- offline root and delegated online keys;
- expiration and rotation;
- revocation and compromised-key incident plan;
- dual-control for stable releases;
- timestamping and notarization;
- separation of nightly and stable authority;
- audit of every signature.

## 10. Updater

The updater is a minimal component that:

1. fetches signed metadata over TLS but does not rely on TLS alone;
2. validates role, signature threshold, expiry, channel, platform, architecture, version, minimum secure version, rollout, and artifact hash;
3. downloads to a non-executable staging area;
4. verifies full payload before installation;
5. applies atomically or through versioned side-by-side directories;
6. retains a known-good rollback version within security policy;
7. validates post-install health;
8. rolls back on failure without accepting unauthorized downgrade;
9. records a privacy-preserving local event.

Updates cannot execute page-controlled paths, arguments, proxies, or files. Enterprise update control is separate from web content.

## 11. Packaging

### macOS

Universal or architecture-specific app bundles, hardened runtime, sandbox entitlements, notarization, Sparkle-like behavior only if its trust model is approved or a Turing updater, DMG/PKG strategy, default-browser registration, and code-sign verification tests.

### Windows

MSIX/MSI/EXE decision based on sandbox/update requirements, Authenticode, per-user versus per-machine install, services minimized, clean uninstall, protocol/default-app registration, and enterprise deployment.

### Linux

Distribution-neutral tarball plus selected Flatpak/AppImage/deb/rpm paths only as maintainable. Sandbox and update behavior differs by package; documentation states whether Turing or the distribution owns updates. Portal and desktop integration tests are required.

## 12. Profile migrations

Profile schema changes are versioned, transactional, resumable, and rollback-aware. Before migration:

- verify free disk and backup/journal capability;
- retain previous binaries and schema compatibility path where feasible;
- migrate stores independently;
- never expose private-session state;
- test large, old, corrupt, interrupted, and partially synced profiles;
- provide export/recovery tools before destructive format changes.

Downgrade behavior is explicit. Older versions must not open a newer profile and corrupt it.

## 13. Crash handling and symbols

Crash capture records process role, build ID, thread stacks, fault metadata, and bounded diagnostics without routine page content or secrets. Dumps are stored locally under policy; upload requires consent/enterprise configuration.

Symbols are generated deterministically, indexed by build ID, and retained according to support policy. Security-sensitive crashes can be routed privately. Automatic issue creation uses deduplicated fingerprints and access control.

## 14. Observability

Operational metrics are separated:

- local product diagnostics: detailed and user-inspectable;
- opt-in aggregate telemetry: small, documented schemas;
- security/update health: minimum data required to protect users;
- benchmark lab: controlled test profiles, not user telemetry;
- agent provider usage: local accounting and provider-reported cost, never hidden product analytics.

Every remote event schema declares fields, purpose, retention, sampling, aggregation, and sensitive-data review. Collection endpoints cannot remotely command the browser.

## 15. Incident response

Incident classes include active exploitation, update/signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension/provider, and service outage.

Runbooks define:

- incident commander and technical leads;
- evidence preservation and secret rotation;
- affected versions/platforms/configurations;
- emergency feature disable through signed policy only where architected;
- patch and release workflow;
- revocation/minimum secure version;
- user/admin communication;
- coordination with upstreams and researchers;
- postmortem and systemic remediation.

Remote kill switches are narrowly scoped, signed, auditable, expiry-bound, and unable to execute arbitrary code.

## 16. Support policy

Before stable, publish:

- supported OS versions and architectures;
- update cadence and maximum security-fix target;
- profile compatibility and backup expectations;
- supported web/extension/enterprise/agent subset;
- telemetry defaults;
- vulnerability reporting and disclosure;
- end-of-life process;
- known proprietary gaps such as DRM/codecs/services.

Dropping an OS or architecture requires advance notice and cannot leave users on an insecure auto-updating channel without clear warning.

## 17. Release gates

- **REL-GATE-1:** clean protected commit builds hermetically and unsigned payloads reproduce within documented limits.
- **REL-GATE-2:** artifacts, update metadata, SBOM, provenance, notices, symbols, and source references share one build identity.
- **REL-GATE-3:** update/rollback/migration pass power-loss, disk-full, corrupt-download, replay, rollback, and revoked-key tests.
- **REL-GATE-4:** platform packages are signed, sandboxed, uninstallable, and tested on supported clean systems.
- **REL-GATE-5:** security, compatibility, performance, accessibility, and known-risk reports are published.
- **REL-GATE-6:** emergency patch and communication path is staffed before beta/stable.

<!-- MARKET-STRATEGY-2026-07 -->
## Product-state portability and support

Migration, export, snapshots, synchronization, and collaboration introduce versioned interchange formats, schema migrations, compatibility windows, backup/recovery, support, and incident obligations. No cloud or account service may become required for local export or normal browsing without an explicit decision.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Production release control plane

Stable release requires the machine `PRG-*` gates, numeric `SLO-*` objectives, accepted platform and scope records, source/build provenance, update trust roles, vulnerability operations, service/offline behavior, support commitments, legal approval, and human release authorization. An agent may assemble evidence but cannot approve or sign stable release.
