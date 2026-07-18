# Servo License Advisory and SBOM Decision Prep - July 2026

Status: dated decision-prep evidence for `ADR9-EV-003` and `ADR9-EV-004`; no legal, dependency, advisory, native-package, SBOM, or source approval
Owner: security, provenance, legal-review, release operations, architecture, and documentation owners
Retrieval date: 2026-07-17
Confidence: medium for Cargo metadata and Servo-policy `cargo-deny` observations; low for Turing redistribution, native-package, and legal conclusions until owner review completes

## Question

What Turing-specific license, advisory, duplicate-version, native-notice, and SBOM decisions remain before `ADR-0009` can select any Servo relationship?

This report prepares decisions. It does not approve Servo, Stylo, WebRender, SpiderMonkey, GStreamer, moztools, `servo-build-deps`, registry crates, native packages, generated outputs, or license exceptions for Turing release code.

## Scope

Included:

- the external Servo checkout at `C:\ts\servo`;
- Cargo metadata files generated outside this repository;
- Servo's own `deny.toml`, `about.toml`, and `Cargo.lock`;
- rerun `cargo-deny` logs generated outside this repository;
- bounded native-license surface counts from the extracted Windows GStreamer package.

Excluded:

- legal advice or license acceptance;
- source-offer, patent, codec, trademark, export-control, or commercial-use approval;
- a complete SBOM;
- source-content review of every package or generated output;
- native source-build recipe review;
- copying Servo source, native binaries, generated output, logs, or registry archives into Turing.

## Evidence Inputs

| Input | Observation |
|---|---|
| Servo remote | `https://github.com/servo/servo.git` |
| External checkout head | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| External checkout tree | `daa2bc0e189e1981fb021501065fc3466159b00d` |
| Checkout state | `## main...origin/main [behind 2]`; shallow repository; `193033` tracked files |
| Default metadata | `C:\ts\servo-metadata-default.json`, SHA-256 `01314363C1E5F7375B5C0024D8C698C8C46EA1F6858CA945CE5560F17F5B3F11` |
| All-features metadata | `C:\ts\servo-metadata-all-features.json`, SHA-256 `7E9DB6EFD7BFBB370B57EE72DEF52E8C3D025FF4C602F461444530591C37CB3F` |
| `Cargo.lock` | `C:\ts\servo\Cargo.lock`, SHA-256 `327FDD559E87B0D18A4B24B201D9254E06C56D59C38388EDD37236F25BA47E22` |
| `deny.toml` | `C:\ts\servo\deny.toml`, SHA-256 `034CA60C05E2CCF9D22FD1BC617338BB5A094546AF711E3DA64B0B671AD04FE5` |
| `about.toml` | `C:\ts\servo\about.toml`, SHA-256 `8DDB21BB7A14081C4016BFDB2C9EF48DDB0A09B16B8B3CE1B0C897B7D790EDAE` |
| Default `cargo-deny` rerun log | `C:\ts\servo-cargo-deny-default-rerun-20260717.log`, SHA-256 `753BB2724E68295ED22369AC744EAAEB28688C83569FBA74C8D30BA9DDAB8570` |
| All-features `cargo-deny` rerun log | `C:\ts\servo-cargo-deny-all-features-rerun-20260717.log`, SHA-256 `CCFA9C0A4EC11FA7605F58BAA73FE0385AE814AC86B9A79D42392D09FE67A26C` |

The checkout being behind `origin/main` means this is a dated build-baseline snapshot. Any owner-selected baseline different from `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` needs a rerun.

## Turing Policy Baseline

Turing's current M0 dependency posture is intentionally narrow. The machine dependency registry records no external runtime or build dependency beyond the Rust toolchain for the current workspace.

Blueprint 03 requires every proposed dependency to identify its exact function, source and version, maintainers, license and patent posture, transitive count, build scripts, proc macros, native links, generated code, network or filesystem behavior, advisories, update path, fuzz or boundary evidence, target platforms, deterministic-build impact, replacement cost, and accepted owner.

Servo's policy is therefore useful input, but it is not Turing policy.

## Servo Policy Observations

Servo's `deny.toml` allows these license identifiers under Servo policy:

`Apache-2.0 WITH LLVM-exception`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `BSL-1.0`, `CC0-1.0`, `CDLA-Permissive-2.0`, `ISC`, `MIT`, `MPL-2.0`, `OFL-1.1`, `Ubuntu-font-1.0`, `Unicode-3.0`, and `Zlib`.

Servo also has a per-crate exception allowing `NCSA` for `libfuzzer-sys`.

Servo's bans policy sets `multiple-versions = "deny"`, `external-default-features = "allow"`, `wildcards = "allow"`, and `workspace-default-features = "allow"`. Duplicate-version skips exist, and the default rerun log still reports `11` unnecessary duplicate-skip warnings.

## Cargo-Deny Rerun Results

The reruns used Servo's own metadata and policy. They exited `0`; that is evidence that the inspected snapshot passed Servo policy, not Turing policy.

| Profile | Advisory result | Ban result | License result | Source result |
|---|---|---|---|---|
| Default metadata | `0` errors, `0` warnings, `24` notes | `0` errors, `11` warnings, `124` notes | `0` errors, `0` warnings, `987` notes | `0` errors, `0` warnings, `11` notes |
| All-features metadata | `0` errors, `0` warnings, `24` notes | `0` errors, `0` warnings, `138` notes | `0` errors, `0` warnings, `1036` notes | `0` errors, `0` warnings, `11` notes |

The default warnings were unnecessary duplicate-skip entries for `jni`, `rand_chacha`, `bit-set`, `naga`, `wgpu-core`, `wgpu-core-deps-apple`, `wgpu-core-deps-emscripten`, `wgpu-core-deps-windows-linux-android`, `wgpu-hal`, `wgpu-naga-bridge`, and `wgpu-types`.

## Cargo Metadata License Shape

| Profile | Packages | Registry | Git | Path | Unique license expressions | Missing both `license` and `license_file` | Duplicate package names |
|---|---:|---:|---:|---:|---:|---:|---:|
| Default metadata | `1069` | `983` | `11` | `75` | `48` | `0` | `58` |
| All-features metadata | `1120` | `1034` | `11` | `75` | `50` | `0` | `69` |

Top all-features license expressions:

| Expression | Count |
|---|---:|
| `MIT OR Apache-2.0` | `425` |
| `MIT` | `213` |
| `Apache-2.0 OR MIT` | `113` |
| `MPL-2.0` | `99` |
| `MIT/Apache-2.0` | `53` |
| `Unicode-3.0` | `44` |
| `Apache-2.0` | `37` |
| `BSD-3-Clause` | `19` |
| `Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT` | `16` |
| `Zlib OR Apache-2.0 OR MIT` | `14` |

All `11` git packages came from `git+https://github.com/servo/stylo?rev=d3de91cbac7bba38e159239b3c0a360783fce2ee#d3de91cbac7bba38e159239b3c0a360783fce2ee`. Most were `MPL-2.0`; `servo_arc` and `stylo_malloc_size_of` were `MIT OR Apache-2.0`.

## License Decision Queue

The following items need Turing owner/legal review before any affected code, package, generated output, or native artifact can enter a release path:

- permissive-looking expressions such as `MIT`, `Apache-2.0`, `BSD-*`, `ISC`, `Zlib`, `BSL-1.0`, `CC0-1.0`, and `Unicode-3.0` still need exact package mapping, notices, source mapping, and accepted license text;
- `MPL-2.0` appears in `99` all-features packages and includes Stylo and Servo clusters, so any reuse needs file-level obligations, modification policy, source-offer handling, and clean-room boundaries;
- font and data licenses, including `OFL-1.1`, `Ubuntu-font-1.0`, `CDLA-Permissive-2.0`, and `Unicode-3.0`, need notice, bundling, modification, and redistribution review;
- `NCSA` is allowed only as a Servo exception for `libfuzzer-sys`; Turing needs its own exception decision if the crate is reachable in a selected profile;
- `Unlicense`, `0BSD`, `MIT-0`, complex `AND` expressions, and slash-separated expressions need normalized SPDX policy handling rather than string-only acceptance;
- expressions with copyleft alternatives, such as `Apache-2.0 OR GPL-2.0-only` and `MIT OR Apache-2.0 OR LGPL-2.1-or-later`, require an explicit selected-license path; their presence is not by itself approval or rejection;
- generated outputs need source-to-output license mapping before they are copied, regenerated, vendored, or distributed by Turing;
- native packages need separate legal and notice review because Cargo metadata does not cover the extracted Windows dependency tree.

## Advisory Decision Queue

Servo ignores `12` RustSec advisories in `deny.toml`. Turing cannot inherit those ignores automatically.

| Advisory | Servo policy note | Turing decision required |
|---|---|---|
| `RUSTSEC-2024-0436` | `paste` is no longer maintained | replace, avoid, patch, or time-bound exception |
| `RUSTSEC-2025-0075` | `unic-char-range` is unmaintained | replace, avoid, patch, or time-bound exception |
| `RUSTSEC-2025-0080` | `unic-common` is unmaintained | replace, avoid, patch, or time-bound exception |
| `RUSTSEC-2025-0081` | `unic-char-property` is unmaintained | replace, avoid, patch, or time-bound exception |
| `RUSTSEC-2025-0098` | `unic-ucd-version` is unmaintained | replace, avoid, patch, or time-bound exception |
| `RUSTSEC-2025-0100` | `unic-ucd-ident` is unmaintained | replace, avoid, patch, or time-bound exception |
| `RUSTSEC-2023-0071` | `rsa` Marvin Attack side channel; Servo waits for a stable upstream patch | determine reachability, threat model, patch plan, or rejection |
| `RUSTSEC-2025-0141` | `bincode` is unmaintained and pinned in Servo | pin justification, replacement plan, or rejection |
| `RUSTSEC-2026-0192` | `ttf-parser` is unmaintained; dependency of `usvg`, `rustybuzz`, and `fontdb` | font/text stack replacement or time-bound exception |
| `RUSTSEC-2026-0194` | `quick-xml` duplicate-attribute check can be quadratic; Servo waits for `winit`/`sctk` upgrade | XML input threat model, patch, avoid, or time-bound exception |
| `RUSTSEC-2026-0195` | `quick-xml` namespace allocation can exhaust memory; Servo waits for `winit`/`sctk` upgrade | XML input threat model, patch, avoid, or time-bound exception |
| `RUSTSEC-2026-0206` | `rustybuzz` is unmaintained; Servo notes dependency through `resvg` | text/font stack replacement, package avoidance, or exception |

Every accepted exception must be time-bounded, owner-approved, tied to a selected feature profile and component boundary, and recorded in the machine registry that owns dependency/advisory exceptions.

## Duplicate-Version and Feature Decision Queue

All-features metadata had `69` package names with multiple versions; default metadata had `58`. The all-features top duplicate groups included `itertools`, `hashbrown`, `rand`, `skrifa`, `read-fonts`, `getrandom`, `rand_core`, and `redox_syscall`.

This matters because duplicate versions can expand attack surface, binary size, update burden, license notice volume, and patch ambiguity. A Turing decision needs:

- selected feature profile and component boundary before duplicate counts are final;
- exact duplicate allow/deny policy;
- accepted skip list with owner and expiry;
- replacement or consolidation plan for high-impact duplicate families;
- proof that duplicate handling is reflected in SBOM, advisory, packaging, and update tooling.

## Native License and Notice Surface

Cargo metadata does not cover Servo's native bootstrap surface. The observed Windows GStreamer license directory under `C:\ts\servo\target\dependencies\gstreamer\1.0\msvc_x86_64\share\licenses` contained `69` package directories, `155` files, and `1141093` bytes of license material.

Sample directories included `bzip2`, `cairo`, `dav1d`, `expat`, `ffmpeg`, `flac`, `fontconfig`, `freetype`, `fribidi`, `gdk-pixbuf`, `glib`, `glib-networking`, `gst-plugins-bad-1.0`, `gst-plugins-base-1.0`, `gstreamer-1.0`, `harfbuzz`, `lame`, `libass`, `libdca`, `libdv`, `libjpeg-turbo`, `librsvg`, `librtmp`, and `libsoup`.

This native surface needs source-build recipes or explicit binary-package exceptions, codec and patent review, package minimization, final notices, source-offer handling, update provenance, sandbox impact review, and release-package manifests. The [Servo Native Bootstrap Provenance Audit - July 2026](servo-native-bootstrap-provenance-audit-2026-07.md) remains the owning provenance report for native packages.

## SBOM Gap

No complete Turing SBOM was generated in this pass. Installed Cargo tooling exposed `cargo-deny`, but this pass did not have `cargo cyclonedx`, `cargo about`, `cargo license`, or `cargo auditable` available as accepted Turing tools.

`ADR9-EV-003` still needs:

- owner-selected SBOM format and toolchain;
- exact selected Servo baseline and feature profile;
- Cargo, git, path, generated-output, and native-package inclusion rules;
- stable package identifiers and source URLs;
- advisory snapshot timestamp policy;
- yanked-package and duplicate-version handling;
- generated-output and native-binary provenance fields;
- validation that SBOM generation is reproducible on the selected reference host.

## What This Proves

- The inspected Servo build-baseline snapshot passes Servo's own `cargo-deny` policy for the two inspected metadata profiles.
- Servo's Cargo metadata exposes no package missing both `license` and `license_file`.
- The license and advisory surface is large enough that Turing needs explicit policy decisions before source adoption or redistribution.
- The native Windows bootstrap surface is outside Cargo metadata and requires separate package/legal/notice/source-build review.
- The reserved `ADR9-EV-003` and `ADR9-EV-004` evidence slots now have a concrete decision queue.

## What This Does Not Prove

- legal approval;
- accepted license list;
- accepted advisory exceptions;
- complete SBOM;
- source-offer compliance;
- native package approval;
- codec or patent clearance;
- generated-output provenance;
- source or dependency approval;
- compatibility, performance, security, accessibility, daily-driver, or Chrome-class readiness.

## Gate Impact

`PB-002` remains blocked.

`ADR9-EV-003` remains partial. Existing evidence now includes this decision-prep report, but the selected SBOM tool, selected feature profile, generated SBOM, advisory timestamp policy, duplicate-version decisions, and owner approval remain missing.

`ADR9-EV-004` moves from missing to partial. Turing now has a license/advisory decision queue, but no legal approval, accepted license list, notices, source-offer plan, patent/codec decisions, native notice review, or accepted exception record.

## Affected Records

- [`docs/README.md`](../README.md)
- [`docs/research/README.md`](README.md)
- [`docs/repository-map.md`](../repository-map.md)
- [`docs/research-log.md`](../research-log.md)
- [`docs/project-buildout/11-pre-build-readiness-checklist.md`](../project-buildout/11-pre-build-readiness-checklist.md)
- [`docs/project-buildout/13-build-readiness-operating-board.md`](../project-buildout/13-build-readiness-operating-board.md)
- [`docs/project-buildout/14-adr-0009-source-strategy-decision-packet.md`](../project-buildout/14-adr-0009-source-strategy-decision-packet.md)
- [`docs/project-buildout/15-adr-0009-evidence-traceability-matrix.md`](../project-buildout/15-adr-0009-evidence-traceability-matrix.md)
- [`docs/blueprint-v1/machine/pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)

## Next Experiments

1. Select the exact Servo source baseline and feature profile for `ADR-0009`.
2. Select the Turing SBOM format, generator, advisory snapshot source, and generated-output/native-package inclusion rules.
3. Generate a trial SBOM outside the Turing source tree and compare it against Cargo metadata, `Cargo.lock`, Stylo git packages, generated outputs, and native dependency manifests.
4. Draft a Turing license acceptance and notice/source-offer matrix for the selected profile.
5. Draft advisory and duplicate-version exception records with owner, expiry, reachability, mitigation, and replacement plan.
6. Run native package legal/advisory/notice review with source-build or binary-package exception decisions.
