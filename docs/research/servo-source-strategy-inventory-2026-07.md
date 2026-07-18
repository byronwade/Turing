# Servo Source Strategy Inventory — July 2026

Status: dated research inventory for `RQ-44`, `PB-002`, and proposed `ADR-0009`; no source-strategy decision
Owner: architecture, engine, security, provenance, release operations, and embedding owners
Retrieval date: 2026-07-17
Confidence: medium for public project posture; low for adoption cost until local prototypes run

## Question

Which Servo relationship should Turing evaluate before web-engine implementation expands: clean implementation informed by Servo, selective Servo components, upstream-first collaboration, Servo-derived engine, or explicit charter change?

This inventory does not approve Servo-derived release code. It prepares the evidence packet required by [`09-servo-adoption-decision-framework.md`](../project-buildout/09-servo-adoption-decision-framework.md), `PB-002`, `RQ-44`, and proposed `ADR-0009`.

## Sources and versions

- Servo home page, retrieved 2026-07-17: https://servo.org/
- Servo repository README, retrieved 2026-07-17: https://github.com/servo/servo
- Successful external build baseline, observed 2026-07-17: `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`
- Servo repository `origin/main`, refreshed 2026-07-17: `622600e045c2e5ea688a9b19b8671b6f43112817`
- Servo GitHub release metadata, observed 2026-07-17: `v0.3.0`, published 2026-06-25T15:09:42Z, target `release/v0.3`
- Servo `v0.3.0` vendored source archive, downloaded and hashed 2026-07-17: SHA-256 `C75EFFBDC0AB6F86B318E28D139EB056268224E072A684492B49409C5221C871`
- Servo independent bare partial clone, observed 2026-07-17: `C:\ts\servo-independent-source-verify-20260717.git`, non-shallow, `blob:none`
- Servo source-baseline equivalence comparison, observed 2026-07-17: `v0.3.0` Git tree has `191174` files; vendored release archive has `252589` files; crates.io `servo 0.4.0` maps to `components/servo` at commit `e8dbc1dfbf6f58621346a5f61ab7a17d01387873`
- Servo same-host build reproduction capture, observed 2026-07-17: build log hashes, `servoshell.exe` SHA-256 `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B`, target/cache footprint, and replay-protocol draft recorded from `C:\ts`
- Servo license/advisory/SBOM decision prep, observed 2026-07-17: Cargo license-expression counts, Servo-policy `cargo-deny` rerun hashes, ignored advisory queue, duplicate-version counts, native GStreamer license-surface counts, and SBOM gap record from `C:\ts`
- Servo native package decision prep, observed 2026-07-17: `servo-build-deps` asset metadata, native asset hashes/signatures, extracted dependency-tree counts, GStreamer copy-candidate counts, deterministic-download policy proposal, and package-family decision matrix from `C:\ts`
- Servo build-script/proc-macro side-effect audit, observed 2026-07-17: default and all-features build-script/proc-macro counts, source-kind distribution, high-marker build-script and proc-macro queues, and side-effect policy gaps from `C:\ts`
- Servo crate documentation, observed as `servo 0.4.0`, dated 2026-07-16: https://docs.rs/servo/latest/servo/
- Servo crate metadata from `cargo search`, `cargo info`, and crates.io API, observed 2026-07-17: `servo = "0.4.0"`, `MPL-2.0`, Rust `1.88.0`, checksum `01a05ffce7829e67e41c5cb4e10849924cbd781d0ea0d6332d81afe8476d8a89`
- Servo crates.io/LTS announcement, posted 2026-04-13: https://servo.org/blog/2026/04/13/servo-0.1.0-release/
- Servo LTS book page, retrieved 2026-07-17: https://book.servo.org/embedding/lts-release.html
- Servo May update for `0.3.0`, posted 2026-06-30: https://servo.org/blog/2026/06/30/may-in-servo/
- Servo browser-building post, posted 2024-09-11: https://servo.org/blog/2024/09/11/building-browser/
- Linux Foundation Europe Servo announcement, posted 2023-09-07: https://linuxfoundation.eu/newsroom/servo-web-rendering-engine-joins-linux-foundation-europe
- Servo WPT pass-rate page, retrieved 2026-07-17: https://servo.org/wpt/

## Observations

Servo currently presents itself as a Rust web rendering engine for embedding web technologies in desktop, mobile, and embedded applications. Its public site emphasizes a WebView API, WebGL/WebGPU support, modularity, parallelism, cross-platform support, and open governance under Linux Foundation Europe.

The GitHub README describes Servo as a prototype web browser engine and lists active development targets including macOS, Linux, Windows, OpenHarmony, and Android. The README also shows that building Servo uses Servo-specific `mach` tooling and platform dependency bootstrap steps rather than a small Cargo-only workspace.

Servo's release posture is active and changing. The April 2026 announcement introduced the first `servo` crate release and said the project had not yet defined Servo 1.0. The LTS page says LTS releases are best effort, security-fix oriented, and do not provide specific guarantees. On 2026-07-17, docs.rs and Cargo metadata showed `servo 0.4.0`, while GitHub's latest release metadata returned `v0.3.0` and the latest Servo blog update found during this pass discussed `0.3.0` from the May update. Turing should therefore pin exact source revisions and crate versions instead of relying on a blog headline.

Servo's embedding API is material enough to study. The docs.rs crate page exposes `Servo`, `WebView`, embedder controls, preferences, protocol handling, WebDriver senders, site-data management, permission prompts, file pickers, notifications, navigation requests, input-method requests, and web-resource interception. Cargo metadata shows default features including `baked-in-resources`, `clipboard`, and `js_jit`, with optional areas such as Bluetooth, gamepad, GStreamer media, Vello, WebGPU, WebXR, tracing, and JavaScript diagnostic features. These APIs and feature flags are useful comparison points for Turing's own embedding, UI, permission, DevTools, and profile boundaries.

Servo's current architecture is not a clean match for Turing's accepted independence goals. The May 2026 update states Servo's JavaScript runtime uses SpiderMonkey and that security fixes were incorporated through a SpiderMonkey update. A complete Servo-derived release path would therefore conflict with Turing's accepted Turing-owned JavaScript semantics unless `ADR-0004`, `ADR-0002`, and `REQ-ENG-007` are explicitly superseded.

Servo is a valuable performance and architecture reference, but not performance proof for Turing. Its public updates describe layout, thread-pool, text-shaping, DOM attribute, accessibility, DevTools, and `about:memory` work. Turing still needs fixed-hardware, equal-workload, equal-security, process-disclosed measurement before adopting any pattern as a performance claim.

## Local preflight observations

An isolated Windows preflight on 2026-07-17 used an external workspace at `C:\Users\bcw19\AppData\Local\Temp\turing-adr-0009-servo-evidence\servo`. The workspace pointed at `https://github.com/servo/servo.git` and `27f61918dff58b8479d7608ab831d42cd0d5a2dc`, matching the then-observed public `main` commit, but the checkout could not be trusted:

- `git ls-files` returned `0`;
- `git status --porcelain` counted `193074` entries;
- `git ls-files --error-unmatch README.md` failed even though `README.md` existed on disk;
- `git fsck --connectivity-only` reported many dangling objects;
- the working tree contained about `207903` files, which is file presence rather than source integrity.

The preflight therefore did not support dependency, compatibility, performance, or source-adoption conclusions.

The host had useful prerequisites: Windows 11 Pro Insider Preview build `26220`, AMD Ryzen 9 5950X, about 64 GiB RAM, AMD Radeon RX 7900 XTX, `git 2.52.0.windows.1`, `gh 2.93.0`, `cargo 1.97.1`, `rustc 1.97.1`, `python3 3.12.10`, and `winget v1.29.250`. Visual Studio Professional 2022 `17.14.36717.8` was installed and `vswhere` found the queried VC tools, C++ ATL, and Windows 11 SDK components.

The first preflight's missing and mismatched prerequisites were material:

- `uv` was not on `PATH`, but Servo's `mach.ps1` invokes `uv run --frozen`;
- `cl` and `link` were not on the normal PowerShell `PATH`, so the next attempt needed Developer PowerShell, `vcvars`, or an equivalent scripted compiler environment;
- Servo's `.python-version` is `3.11`, while the host default `python3` is `3.12.10`;
- Servo's `rust-toolchain.toml` pins Rust `1.95.0`, while Turing M0 currently uses Rust `1.97.1`;
- direct `python3 mach --help` is not the documented path and reported a Windows case-sensitive-path failure in this invalid workspace.

A second isolated Windows preflight on 2026-07-17 used `C:\ts\servo` to avoid the long-path and invalid-index behavior. The checkout pointed at `https://github.com/servo/servo.git` and `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe`; `git ls-files` counted `193033` tracked files, and `git status --porcelain` counted `0` tracked-file changes after bootstrap and build. Ignored generated files included the virtualenv, Python caches, downloaded dependencies, and `target/` outputs.

The repaired host path installed `uv 0.11.29` through `winget`, used CPython `3.11.9`, and used Servo's Rust `1.95.0-x86_64-pc-windows-msvc` override. `.\mach.ps1 bootstrap` completed with exit `0`, installed or verified CMake, LLVM, Ninja, WiX, `crown`, `moztools-4.0`, and GStreamer MSVC packages. `.\mach.ps1 build --dev -j 8` ran from the Visual Studio 2022 Developer Command Prompt with MSVC `14.44.35207`; `C:\Program Files\LLVM\bin` had to be added to `PATH` so `lld-link.exe` resolved. The build completed with `BUILD_EXIT=0`, stdout reported `Succeeded in 0:09:21`, Cargo reported `Finished dev profile [unoptimized + debuginfo] target(s) in 9m 14s`, and `C:\ts\servo\target\debug\servoshell.exe` was produced.

This proves a reproducible local Servo bootstrap and development build on the reference host, but it still does not support Turing source adoption. Follow-up reports now provide dependency/provenance, supply-chain, license/advisory/SBOM, generated/native/unsafe/FFI, source/archive, native-package, first-pass component-boundary, JavaScript-conflict, WPT/Test262 denominator, a checked no-claim local compatibility corpus manifest, fixtures, HTTP route self-test, and HTTPS host-alias harness plan, performance-baseline-preparation, security/maintenance implication, and public-claim/support-impact evidence. The missing `ADR-0009` evidence remains owner-selected baseline and provenance policy, owner-reviewed component boundaries, owner-reviewed JavaScript-runtime conflict decisions, local compatibility HTTPS harness execution, WPT or corpus browser-run results, runner-generated fixed-hardware performance/memory data, owner-reviewed security/sandbox implications, owner-approved maintenance/upstream model, owner-applied public-claim/document/registry diffs, and explicit owner review.

A follow-up [Servo Dependency and Provenance Inventory — July 2026](servo-dependency-provenance-inventory-2026-07.md) extracted Cargo metadata from the clean checkout. It found `1069` packages in default metadata, including `75` Servo path packages, `983` registry packages, and `11` git packages from `servo/stylo`; it also identified build-script, proc-macro, native-link, duplicate-version, MozJS, Stylo, WebRender/WebGPU, media, crypto/TLS, storage, platform, DevTools, and WebDriver review targets. That report narrows the dependency/provenance work but does not approve any Servo dependency or move `PB-002`.

The [Servo Supply-Chain Policy Scan — July 2026](servo-supply-chain-policy-scan-2026-07.md) then ran Servo's own `cargo-deny` policy against default and all-features metadata. Both scans exited `0`, but Servo's policy includes ignored RustSec advisories and duplicate-version exceptions, and Windows bootstrap unpacked a large native dependency surface under `target\dependencies`. This is useful source-strategy evidence, not a Turing approval.

The [Servo License Advisory and SBOM Decision Prep - July 2026](servo-license-advisory-decision-prep-2026-07.md) narrows `ADR9-EV-003` and `ADR9-EV-004`. It records Cargo license-expression counts, `0` packages missing both `license` and `license_file`, `12` Servo-ignored RustSec advisories, default and all-features duplicate-version counts, a native GStreamer license-surface count, and the lack of a generated Turing SBOM. It moves license/advisory work from unshaped gap to decision queue, but does not grant legal approval or accept exceptions.

The [Servo Native Package Decision Prep - July 2026](servo-native-package-decision-prep-2026-07.md) narrows `ADR9-EV-005` and `ADR9-EV-006`. It records native package families, local upstream asset hashes, GStreamer and moztools extracted-tree surfaces, GStreamer copy candidates, debug-output package shape, and a deterministic-download verification proposal. It moves native package work from broad blocker to source-build/binary-exception and download-verification decision queues, but does not approve any native package.

The [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md) adds a first-pass review of source-shape and metadata surfaces for the same checkout. It found `2280` unsafe mentions, `1629` unsafe-block matches, `217` FFI/export/link markers, `157` default-metadata build-script packages, `70` proc-macro packages, and `25` native-link packages, with high concentrations in script, script bindings, WebGL, C API, fonts, media, layout, and servoshell platform code. That report narrows the generated/native/unsafe/FFI work but does not approve any unsafe block, generated output, native library, or FFI contract.

The [Servo Unsafe and FFI Contract Review - July 2026](servo-unsafe-ffi-contract-review-2026-07.md) narrows `ADR9-EV-009` and `ADR9-EV-010`. It records the top unsafe-block, unsafe-function, unsafe-impl, and FFI marker files; inventories `52` C API exports across builder, options, preferences, rendering context, servo, and webview modules; and identifies JavaScript rooting/tracing plus WebGL/driver boundary review classes. It does not approve any unsafe block, C API, ABI contract, SpiderMonkey integration, WebGL integration, component boundary, or release code.

The [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md) then hashed key generated-output directories and generator inputs, audited first-party build-script side effects, and ran one no-op incremental Servo rebuild. The inspected first-party generated-output digests stayed stable across that rebuild, but the report does not prove clean-target determinism, independent-host reproducibility, source-to-output licensing, or registry/git build-script safety.

The [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md) narrows `ADR9-EV-008`. It records `157` default build-script packages, `70` default proc-macro packages, `167` all-features build-script packages, `71` all-features proc-macro packages, registry-dominated marker volume, high-pressure build scripts, and proc-macro source scale. It does not accept a side-effect policy, prove behavior dynamically, approve proc-macro expansions, or make any build-time code acceptable for Turing release code.

The [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md) records local Servo and Stylo source archive digests, tracked-file manifest digests, Cargo registry cache checksum verification, and a bounded Windows bootstrap artifact summary. The [Servo Upstream Source Provenance - July 2026](servo-upstream-source-provenance-2026-07.md) compares the successful build baseline, refreshed upstream `origin/main`, latest GitHub release tag, vendored release source archive, and crates.io package checksum. The [Servo Independent Source Verification - July 2026](servo-independent-source-verification-2026-07.md) verifies the main, build-baseline, and release source objects from a separate non-shallow Git object graph. The [Servo Source Baseline Equivalence Policy Prep - July 2026](servo-source-baseline-equivalence-policy-2026-07.md) then shows the vendored release archive is a derived package with a large `vendor/` tree and that crates.io `servo 0.4.0` maps only to `components/servo`. The [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md) records Windows bootstrap download behavior, original upstream `servo-build-deps` asset hashes, extracted artifact hashes, signature posture, and packaging-footprint evidence. The [Servo Build Reproduction Evidence and Gap Report - July 2026](servo-independent-build-reproduction-2026-07.md) records the same-host environment, build log hashes, artifact hash, replay protocol draft, and target/cache footprint. Together they narrow the source/archive, upstream source, independent Git, equivalence, native identity, and build-reproduction gaps but do not provide owner-selected baseline approval, legal approval, owner-accepted replay protocol, independent clean-target build replay, native source-build or binary-package exceptions, or a source-strategy decision.

## Decision options to evaluate

| Option | Possible benefit | Primary conflict or cost | Evidence required before ADR-0009 |
|---|---|---|---|
| Clean implementation informed by Servo | Preserves Turing independence and avoids inherited architecture | Slowest path and highest staffing burden | Standards notes, differential tests, no source copying, architecture comparison |
| Selective Servo components | Reuses focused Rust browser work where boundaries fit | Provenance, dependency graph, unsafe/native, SpiderMonkey or other transitive coupling | Component API inventory, license review, replacement plan, security/fuzz evidence |
| Upstream-first collaboration | Shares work useful to both projects | May not satisfy Turing-specific process, agent, UI, and resource contracts | Upstream issue map, contribution plan, divergence and review cost |
| Servo-derived engine | Fastest path to visible rendering experiments | Conflicts with independent engine and Turing-owned JS requirements | Superseding ADRs, public claim changes, full dependency/security/support review |
| Explicit Servo browser charter change | Honest if Turing becomes a Servo product | Changes mission, requirements, roadmap, market position, and support story | Owner decision, requirements rewrite, risk acceptance, user-facing disclosure |

## Minimum ADR-0009 evidence packet

Before `PB-002` can move out of blocked status, produce:

1. Exact Servo repository commit, crate versions, build command, host OS, toolchain, and dependency snapshot.
2. License, provenance, generated-code, unsafe/native, build-script, and transitive dependency inventory.
3. WPT focus-area snapshot from Servo's public WPT data plus locally reproducible subset results.
4. Embedding API inventory for windows, WebViews, navigation, permissions, prompts, files, site data, DevTools, WebDriver, input, accessibility, and offscreen rendering.
5. Process, sandbox, network, storage, GPU, media, extension, DevTools, and updater authority map.
6. JavaScript runtime boundary analysis, including SpiderMonkey implications for `ADR-0004`.
7. Fixed-hardware startup, memory, interaction, frame pacing, energy, crash, and recovery baseline against the same local corpus Turing will use for other engines.
8. Patch ownership, upstream cadence, security response, LTS guarantees, and breakage-handling plan.
9. A clean-room rule that separates standards notes, independent tests, and source-derived implementation details.
10. A recommendation that names unsupported behavior, residual risk, and the documents or machine registries that would change.

## Current inference

Servo should remain a high-priority research and differential target. It should not enter Turing release code until `ADR-0009` is accepted and every affected requirement, risk, source-policy record, roadmap entry, support statement, and public claim is updated.

The near-term path is to build a Servo decision packet, not a Servo dependency. The packet can proceed in parallel with Turing-owned M0 kernel, IPC, UI-model, sandbox, benchmark, and documentation work as long as no release path depends on Servo-derived code.

## Contradictory or unresolved evidence

- Servo has active releases and an embedding API, but the project still states that Servo 1.0 is not defined.
- The docs.rs crate version can move ahead of the most recent monthly blog post, so the decision packet must use exact crate and commit identifiers.
- Best-effort Servo LTS is useful for embedders but does not satisfy Turing's stable-browser support obligations.
- Servo's SpiderMonkey use may make some components unsuitable for Turing's accepted independent JavaScript runtime goal even if other Rust components are useful.
- Public WPT pass-rate pages require a reproducible data extraction step before Turing can cite numeric compatibility conclusions.

## Next experiment

Create a local `ADR-0009` research branch that follows the [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md): use the clean short-path Servo build evidence, build reproduction protocol draft, dependency/provenance metadata, supply-chain policy scan, license/advisory/SBOM decision prep, generated/native/unsafe/FFI classification, unsafe/FFI contract review, build-script/generated-output audit, build-script/proc-macro side-effect audit, source/archive provenance audit, upstream source provenance report, independent source verification report, source-baseline equivalence policy prep, native bootstrap provenance audit, native package decision prep, component-boundary/JavaScript-conflict analysis, local compatibility denominator, checked no-claim local compatibility corpus manifest, fixtures, HTTP route self-test, and HTTPS host-alias harness plan, performance-baseline preparation, security/maintenance implications, and public-claim/support-impact draft; complete owner-selected source-baseline policy, owner-accepted equivalence policy, selected-baseline blob/legal review, owner-accepted replay protocol, independent clean-target build replay, accepted license/advisory/SBOM decisions, source-build recipes or binary-package exception records, block-level unsafe review using the unsafe/FFI triage plan, clean generated-output regeneration, accepted build-script/proc-macro side-effect policy, dynamic tracing, accepted FFI ABI contracts, component inventories, SpiderMonkey implications, tiny local compatibility HTTPS harness execution and corpus browser runs through Servo and Turing's future harness format, runner-generated performance data, owner-reviewed security/sandbox implications, owner-approved maintenance model, and owner-applied public-claim/document/registry diffs. No Servo source should be copied into this repository during that experiment.

## Affected records

This inventory adds evidence for `PB-002` but does not change its blocked status. It informs:

- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [Servo adoption framework](../project-buildout/09-servo-adoption-decision-framework.md)
- [Servo Dependency and Provenance Inventory - July 2026](servo-dependency-provenance-inventory-2026-07.md)
- [Servo Supply-Chain Policy Scan - July 2026](servo-supply-chain-policy-scan-2026-07.md)
- [Servo Generated, Native, Unsafe, and FFI Classification - July 2026](servo-generated-native-unsafe-classification-2026-07.md)
- [Servo Unsafe and FFI Contract Review - July 2026](servo-unsafe-ffi-contract-review-2026-07.md)
- [Servo Build-Script and Generated-Output Audit - July 2026](servo-build-script-generated-output-audit-2026-07.md)
- [Servo Build-Script and Proc-Macro Side-Effect Audit - July 2026](servo-build-script-proc-macro-side-effect-audit-2026-07.md)
- [Servo Source and Archive Provenance Audit - July 2026](servo-source-archive-provenance-audit-2026-07.md)
- [Servo Upstream Source Provenance - July 2026](servo-upstream-source-provenance-2026-07.md)
- [Servo Independent Source Verification - July 2026](servo-independent-source-verification-2026-07.md)
- [Servo Source Baseline Equivalence Policy Prep - July 2026](servo-source-baseline-equivalence-policy-2026-07.md)
- [Servo Native Bootstrap Provenance and Source-Build Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md)
- [Servo Build Reproduction Evidence and Gap Report - July 2026](servo-independent-build-reproduction-2026-07.md)
- [Servo License Advisory and SBOM Decision Prep - July 2026](servo-license-advisory-decision-prep-2026-07.md)
- [Servo Native Package Decision Prep - July 2026](servo-native-package-decision-prep-2026-07.md)
- [Servo Local Compatibility Corpus and WPT/Test262 Evidence - July 2026](servo-local-compatibility-corpus-2026-07.md)
- [ADR-0009 local compatibility corpus manifest](../blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json)
- [ADR-0009 HTTPS host-alias harness plan](../blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json)
- [Servo Performance Baseline Preparation - July 2026](servo-performance-baseline-2026-07.md)
- [Servo Security and Maintenance Implications - July 2026](servo-security-maintenance-implications-2026-07.md)
- [ADR-0009 Decision Draft and Public-Claim Impact](../project-buildout/16-adr-0009-decision-draft.md)
- [Architecture decisions](../blueprint-v1/17-architecture-decisions.md)
- [Research program](../blueprint-v1/22-research-program.md)
- [Competitive Servo study](../competitive/04-servo.md)
- [Technology stack](../technology-stack/README.md)
- [Source bibliography](../blueprint-v1/18-source-bibliography.md)
