# Servo Upstream Refresh and Source-Strategy Delta - July 2026

Status: dated upstream observation and `ADR-0009` handoff; no source-strategy decision
Owner: architecture, engine, JavaScript, security, supply-chain, release operations, quality, and documentation owners
Related gates: `PB-002`, `ADR-0009`, `ADR9-EV-001`, `ADR9-EV-002`, `ADR9-EV-012`, `ADR9-EV-016`
Retrieved: 2026-07-19

## Question

What has changed or become clearer in the official Servo and Servo `mozjs` surfaces since the existing source-strategy packets were written, and how should a maintainer use those observations without treating upstream activity as Turing approval?

This packet is a freshness and routing update. It does not select Servo, approve a source baseline, approve a dependency, transfer compatibility or security behavior, or authorize source import or release code.

## Sources and authority

The primary sources are the official upstream repositories and their live public documentation:

- [Servo repository](https://github.com/servo/servo), including its README, tracked top-level structure, license, security policy, build files, and supported-platform statement;
- [Servo pull requests](https://github.com/servo/servo/pulls), used only as a current activity and maintenance signal;
- [Servo `mozjs` repository](https://github.com/servo/mozjs), including its README and release metadata.

The pages are live branch and project views, not immutable evidence. A future decision packet must record the exact commit, tag, archive, package, retrieval timestamp, and hashes used for any reproducible conclusion. Existing local checkout and build records remain the stronger source for the already captured commit-specific observations.

## Observations

### Servo repository and build surface

The official Servo repository describes Servo as a prototype web browser engine written in Rust and lists 64-bit macOS, Linux, Windows, OpenHarmony, and Android development targets. Its top-level surface includes `components`, `ports/servoshell`, `ffi/capi`, `python`, `tests`, build metadata, a security policy, and a `mach` bootstrap/build entry point. The README gives platform-specific bootstrap requirements and includes Windows SDK, MSVC, C++ ATL, `uv`, `rustup`, and `mach` steps.

These observations strengthen the existing source-strategy inventory in two ways:

1. Servo is a substantial upstream engine and embedding surface, not a small dependency that can be approved by checking one Cargo manifest.
2. A source-strategy comparison must include the repository's build orchestration, native/bootstrap inputs, C API and embedding surface, test corpus, release/security process, and platform-specific toolchain—not only Rust source files.

The repository's public description still calls the project a prototype. That is an upstream maturity statement, not a Turing maturity decision and not evidence that Turing can use Servo safely or compatibly.

### Upstream activity is not release assurance

The official pull-request view shows ongoing work across IndexedDB, script bindings, layout, accessibility, media, WebGPU, WebDriver BiDi, and dependency/build surfaces. This is evidence of active engineering, not evidence of a stable API, fixed feature set, security response commitment, or compatible Turing release boundary.

The practical source-strategy implication is that an upstream-first option needs an explicit moving-baseline policy. A live branch or active pull-request stream cannot be the implicit dependency version. The decision record must name a baseline, update window, revalidation triggers, branch/patch ownership, and what happens when upstream changes invalidate generated output, security assumptions, compatibility results, or performance evidence.

### JavaScript runtime remains a hard boundary

The official `mozjs` repository describes Servo's SpiderMonkey bindings and documents a vendored/upstream SpiderMonkey relationship, generated or imported source workflows, and pre-built archive behavior. Its current README identifies a SpiderMonkey tracking branch/version, but that live value must be captured by commit and release metadata before it can be used in a Turing decision.

### Exact live repository capture - 2026-07-19

A read-only GitHub API capture recorded the following identities without changing either repository:

| Repository | Live observation | Interpretation boundary |
| --- | --- | --- |
| `servo/servo` | Public, non-archived, default branch `main`; head `736ad1bda08c1af419aadc903e82938f8610a65d`; latest release `v0.3.0` published 2026-06-25 at tag commit `fb6c9d511f67a311f5883ec859aa0c5dd88d19c3`; API license metadata `MPL-2.0` | The moving head and release tag are different source identities. Neither is selected for Turing, and neither proves reproducibility, compatibility, security, performance, or release suitability. |
| `servo/mozjs` | Public, non-archived, default branch `main`; head `f5cbf8aa6076064fd658a1e9fb16147c2347affb`; API metadata returned null SPDX license and security-policy URL fields | Null API metadata is unresolved metadata, not proof that licensing or security documentation is absent. `mozjs` must be pinned and reviewed independently from Servo. |

The machine [`ADR-0009 source-observation manifest`](../blueprint-v1/machine/adr-0009-source-observation-manifest.json) now retains these observations as no-claim source inputs. The capture is time-bounded: future refreshes must repeat the API queries, retain retrieval timestamps, compare selected refs and hashes, inspect repository license/security files, and record changed release/head relationships before downstream evidence is reused.

This reinforces `ADR9-EV-012`: a Servo-derived option cannot be evaluated as a rendering-only choice. It must explicitly decide whether the JavaScript runtime is:

- excluded and replaced by the Turing-owned runtime direction;
- retained only as an external comparator or research input;
- accepted behind a named, reviewed boundary; or
- allowed to supersede the current runtime ADR and dependent requirements.

Each outcome changes Web IDL bindings, garbage collection and wrapper lifetime, realm and origin identity, debugger/DevTools behavior, JIT and native-code review, Test262 attribution, licensing/provenance, and maintenance obligations. None of those decisions is made by this refresh.

## Decision impact by evidence item

| Evidence item | Fresh observation | Required Turing follow-up | Current maturity |
|---|---|---|---|
| `ADR9-EV-001` source identity | Live API capture distinguishes Servo head `736ad1b...` from release tag `v0.3.0` at `fb6c9d...`; `mozjs` has independent head `f5cbf8a...` | Freeze one candidate commit/tag/archive/package for each accepted input, record hashes and retrieval metadata, then apply the accepted equivalence policy | Partial |
| `ADR9-EV-002` reference build | Official build instructions span platform toolchains and `mach` bootstrap/build behavior | Reproduce the selected baseline from a clean target on an independent host or approved clean VM, retaining bootstrap, dependency, cache, target, and failure logs | Partial |
| `ADR9-EV-012` runtime conflict | `mozjs` is a distinct binding and vendored SpiderMonkey surface with independent head identity and unresolved API license/security metadata | Produce option-specific runtime, provenance, security, Web IDL, identity, debugger, and Test262 decisions | Partial |
| `ADR9-EV-016` maintenance | Active upstream changes span engine, runtime, media, accessibility, tooling, and dependencies | Name update cadence, patch ownership, stale-evidence triggers, security-response split, merge burden, rollback, primary owner, backup owner, and reviewer | Partial |

## Required evidence preservation

For any future refresh or decision packet, preserve:

- exact upstream repository URLs and API/page locators;
- retrieval date and timezone;
- selected commit/tag/release/archive/package and SHA-256 values;
- the source tree, feature profile, target platforms, and generated-output policy;
- all build/bootstrap commands and external download/package inputs;
- upstream branch, release, security, and dependency signals as observations with expiry dates;
- contradictory or unavailable evidence, including live-page volatility;
- the exact Turing claim, support, security, compatibility, performance, and ownership records affected.

Do not use commit counts, pull-request counts, release labels, README adjectives, repository stars, or active maintenance alone as evidence of security, compatibility, performance, stability, production readiness, or source-strategy fit.

## Next proof

The next proof remains owner-controlled and is not a broad build:

1. select or reject a source-baseline model and runtime relationship;
2. freeze the exact candidate inputs and rerun the required provenance/equivalence checks;
3. execute the independent clean-host reproduction and capture the full failure denominator;
4. convert the option-specific runtime and maintenance analysis into a real owner-reviewed `ADR-0009` decision record.

Until then, `PB-002` and `ADR9-EV-018` remain blocked. The current status is evidence tracking only.

## Unsupported conclusions

This refresh does not show that:

- Servo or `mozjs` is safe for hostile browsing or suitable for Turing release code;
- upstream activity creates a Turing maintenance, security, compatibility, performance, or support commitment;
- the official build instructions are a reproducible Turing toolchain;
- a live branch, release label, archive, Cargo package, or pre-built archive is equivalent to another source form;
- the JavaScript runtime relationship is resolved;
- any `ADR-0009` option, `PB-002`, or `PB-020` is accepted or ready.

## Canonical routing

This packet feeds the [ADR-0009 source-strategy closure preparation](adr-0009-source-strategy-closure-preparation-2026-07.md), [evidence traceability matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md), [source-strategy decision packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md), [decision draft](../project-buildout/16-adr-0009-decision-draft.md), and checked no-claim [decision-review template](../blueprint-v1/machine/adr-0009-decision-reviews/no-claim-decision-review-template.json). It does not supersede any of them.
