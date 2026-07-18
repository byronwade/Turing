# Servo Component Boundary and JavaScript Conflict Analysis - July 2026

Status: first-pass decision prep; no component approval
Owner: architecture, engine, JavaScript runtime, security, provenance, and quality
Related gate: `PB-002`, `ADR-0009`, `ADR9-EV-011`, `ADR9-EV-012`
Date: 2026-07-17

## Question

Can any Servo component boundary be considered independently before `ADR-0009`, and how does each source-strategy option interact with Turing's accepted Turing-owned JavaScript-runtime decision?

This report does not approve Servo, Stylo, WebRender, SpiderMonkey, GStreamer, Servo C API code, or any transitive dependency for Turing release code. It does not copy Servo source into this repository. It turns the previous broad "component-boundary analysis" and "JavaScript-runtime implications" gaps into a concrete evidence queue.

## Sources and Environment

Primary local evidence came from the external Servo checkout at `C:\ts\servo`, outside this repository.

| Item | Value |
|---|---|
| Servo commit inspected | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Tracked files | `193033` |
| Tracked-file status | `0` changed paths |
| Turing repository | documentation and registry update only |
| Commands | `git`, `cargo metadata`, `rg`, and read-only Python/Powershell summary scripts |
| Cargo metadata caveat | closure calculations exclude dev-only edges but still reflect Cargo workspace feature resolution, the active platform, build dependencies, proc macros, and native-link packages |

The successful external Servo build, dependency inventory, supply-chain scan, generated/native/unsafe/FFI classification, build-script/generated-output audit, build-script/proc-macro side-effect audit, source/archive provenance audit, upstream source provenance report, independent source verification report, source-baseline equivalence prep, native bootstrap audit, native package prep, and build reproduction report remain the prior evidence base.

## Method

The analysis used four evidence passes:

1. Confirmed the external checkout identity and cleanliness with `git -C C:\ts\servo rev-parse HEAD`, `git status --porcelain`, and `git ls-files`.
2. Ran `cargo metadata --format-version 1` for default, no-default-feature, and all-feature Servo profiles.
3. Computed package closures for selected Servo workspace roots with dev-only edges excluded.
4. Counted targeted markers in subsystem Rust sources for unsafe, FFI/export/link, MozJS/SpiderMonkey, Web IDL/binding, WebRender/GPU, and GStreamer/media surfaces.

The marker counts are heuristic. They identify review pressure and likely coupling; they are not a block-level unsafe inventory, ABI review, generated-output provenance review, compatibility result, or performance result.

## Package Closure Observations

Closure totals below are from the active metadata profile with dev-only edges removed. Build scripts, proc macros, native links, registry packages, and git dependencies remain part of the decision pressure because they affect reproducibility, provenance, generated output, and review scope.

| Root package | Total packages | Servo path | Registry | Git | Build scripts | Proc macros | Native links | Reachability notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `servoshell` | 1004 | 63 | 930 | 11 | 140 | 68 | 25 | Full shell path reaches MozJS/SpiderMonkey, Stylo, WebRender/GPU, DevTools/WebDriver, WebGPU/WebGL |
| `servo` | 842 | 61 | 770 | 11 | 125 | 58 | 23 | Core embedding package reaches MozJS/SpiderMonkey, Stylo, WebRender/GPU, DevTools/WebDriver, WebGPU/WebGL |
| `servo-capi` | 843 | 62 | 770 | 11 | 125 | 58 | 23 | C API follows nearly the same closure as `servo` and adds ABI/lifetime/panic review pressure |
| `servo-layout` | 766 | 46 | 709 | 11 | 115 | 55 | 19 | Layout reaches `servo-script`, Stylo, and WebRender API surfaces |
| `servo-paint` | 561 | 34 | 516 | 11 | 80 | 47 | 8 | Paint reaches Stylo traits, WebRender, WebGPU/WebGL, and surface management |
| `servo-script` | 764 | 45 | 708 | 11 | 115 | 55 | 19 | Script reaches MozJS, Web IDL/bindings, Stylo, WebRender API, crypto, compression, network policy, and storage-adjacent crates |
| `servo-script-bindings` | 499 | 16 | 472 | 11 | 83 | 46 | 12 | Bindings reach MozJS, Stylo, generated-code inputs, build-time codegen, and native-link packages |
| `servo-net` | 579 | 19 | 549 | 11 | 88 | 46 | 14 | Network is not a small policy-only component; closure reaches fonts, paint API, DevTools traits, and large build/proc-macro surfaces |
| `servo-storage` | 503 | 16 | 476 | 11 | 74 | 44 | 9 | Storage is smaller than shell/script but still reaches shared traits, profile/base policy, SQLite, and build/proc-macro surface |
| `servo-media` | 381 | 12 | 358 | 11 | 57 | 32 | 7 | Media core is still tied to shared Servo traits and registry/git dependency surface |
| `servo-media-gstreamer` | 422 | 16 | 395 | 11 | 71 | 34 | 7 | GStreamer path adds native package, license, codec, and binary/source-build decisions |
| `servo-webgpu` | 512 | 15 | 486 | 11 | 79 | 45 | 7 | WebGPU path reaches GPU validation and WebRender-adjacent review scope |
| `servo-webgl` | 481 | 18 | 452 | 11 | 73 | 42 | 8 | WebGL path reaches GPU/native and script-facing API review scope |
| `servo-devtools` | 580 | 20 | 549 | 11 | 89 | 46 | 14 | DevTools reaches network and browser-state protocol surfaces |
| `servo-webdriver-server` | 456 | 11 | 434 | 11 | 69 | 42 | 7 | WebDriver path is not enough evidence for Turing's protocol, auth, replay, or automation boundary |

The closure shape argues against treating "take just one Servo component" as a simple implementation shortcut. The candidate boundary first needs a selected source baseline, feature profile, target platform, explicit in/out component list, build-script policy, native-package policy, unsafe/FFI review, generated-output provenance, and replacement plan.

## Feature-Profile Contrast

The core `servo` package was also measured across feature profiles:

| Metadata profile | Total packages | Servo path | Registry | Git | MozJS | WebRender | Stylo | GStreamer |
|---|---:|---:|---:|---:|---|---|---|---|
| default | 842 | 61 | 770 | 11 | yes | yes | yes | no |
| `--no-default-features` | 805 | 57 | 737 | 11 | yes | yes | yes | no |
| `--all-features` | 923 | 65 | 847 | 11 | yes | yes | yes | yes |

Direct manifest evidence shows `components/servo/Cargo.toml` has default features `baked-in-resources`, `bundled_freetype`, `clipboard`, and `js_jit`; the `js_jit` feature enables `script/js_jit`. Disabling default features reduces the package count but does not remove MozJS/SpiderMonkey, Web IDL bindings, Stylo, or WebRender from the measured core closure. Therefore a no-default-feature Servo profile is not equivalent to Turing's interpreter-first, Turing-owned JavaScript runtime.

## Direct Dependency Observations

The direct manifests show several high-pressure boundaries:

- `servo-layout` directly depends on `servo-script`, `servo-script-traits`, `stylo`, `stylo_atoms`, `stylo_traits`, and `webrender_api`.
- `servo-script` directly depends on `mozjs`, `servo-script-bindings`, `stylo`, `stylo_dom`, `stylo_malloc_size_of`, `stylo_traits`, `servo-layout-api`, `servo-net-traits`, and `webrender_api`.
- `servo-script-bindings` declares `links = "script_bindings_crate"` and has build dependencies on `phf_codegen`, `phf_shared`, and `serde_json`.
- `servo-paint` directly depends on `servo-webgl`, `servo-webgpu`, `webrender`, `webrender_api`, `surfman`, `gleam`, and `stylo_traits`.
- `servo-net` directly depends on DevTools traits, font packages, `servo-paint-api`, Fetch/network libraries, TLS libraries, compression, image/SVG-related packages, and Turing-relevant policy surfaces such as cookies, CSP, CORS, cache behavior, and partitioning.
- `servo-storage` directly depends on SQLite through `rusqlite`, query-generation packages, shared profile/base/url/storage traits, and temporary-file behavior.
- `servo-media-gstreamer` directly depends on GStreamer crates, GStreamer sys crates, media traits, render backends, and platform-specific render packages.

These observations do not prove that separation is impossible. They prove that separation has not been demonstrated and that any option scorecard must measure the actual component cut rather than the package name alone.

## Subsystem Marker Counts

The following source marker counts are heuristic and are meant to steer review scope.

| Area | Rust files | Bytes | `unsafe` markers | FFI/export/link markers | MozJS/SpiderMonkey markers | Web IDL/binding markers | WebRender/GPU markers | GStreamer/media markers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `components/script` | 866 | 11160464 | 960 | 77 | 8449 | 11289 | 3259 | 2236 |
| `components/script_bindings` | 38 | 322882 | 418 | 31 | 729 | 195 | 1 | 3 |
| `components/layout` | 62 | 1843547 | 39 | 0 | 44 | 8 | 209 | 33 |
| `components/paint` | 14 | 225250 | 0 | 0 | 27 | 6 | 259 | 7 |
| `components/net` | 42 | 829401 | 8 | 0 | 22 | 5 | 29 | 16 |
| `components/storage` | 20 | 254355 | 1 | 0 | 21 | 0 | 0 | 1 |
| `components/media` | 95 | 605419 | 48 | 10 | 24 | 3 | 21 | 1893 |
| `components/devtools` and WebDriver server | 56 | 592429 | 0 | 0 | 103 | 10 | 0 | 6 |
| `ffi/capi` | 7 | 74830 | 172 | 56 | 4 | 0 | 1 | 0 |

The script and binding areas concentrate the highest JavaScript, Web IDL, unsafe, and FFI-sensitive pressure. The C API is small by file count but dense in ABI-sensitive markers. Media has separate native and license pressure. Layout and paint carry direct style/GPU coupling even before compatibility or performance evidence is considered.

## Source-Strategy Option Impact

### Clean implementation informed by Servo

This option currently fits Turing's accepted independence and JavaScript-runtime decisions best, provided the project treats Servo as public research input rather than source material. It still needs clean-room guidance for implementation notes, test derivation, bug-reduction techniques, and contributor provenance. It also needs a public statement that the resulting Turing code is not Servo-derived release code.

### Selective Servo components

This option remains unapproved and incomplete. The measured closures show that obvious package names do not form small, isolated boundaries. A selective option must define the exact selected component, source baseline, feature profile, target platforms, in/out APIs, replacement boundaries, generated-output policy, native/package policy, unsafe/FFI review, and maintenance owner.

The most sensitive candidates are:

- `servo-script` and `servo-script-bindings`, because they conflict directly with Turing-owned JavaScript semantics, Web IDL generation, GC/wrapper lifetime, JIT/no-JIT policy, debugger, and Test262 strategy.
- `servo-layout`, because it directly reaches `servo-script` and Stylo, so it is not just a layout algorithm package.
- `servo-paint`, WebRender, WebGL, and WebGPU, because the GPU validation, process, native, and security boundaries would need to align with Turing's process model.
- `servo-media-gstreamer`, because the native package, codec, license, source-build, and containment work is still unresolved.
- `servo-net` and `servo-storage`, because Turing owns profile, site, origin, partitioning, credentials, cache, cookie, quota, migration, and privacy semantics even if protocol/storage libraries are reused behind policy.

### Upstream-first collaboration

This option can be useful without a release-code dependency if the project contributes tests, reduced cases, documentation, or bug reports upstream. It does not solve Turing's implementation burden unless a later ADR accepts a component relationship with evidence. Collaboration must not become a backdoor source import or implicit maintenance commitment.

### Servo-derived engine

This option conflicts with the current independent-engine architecture unless `ADR-0002`, `ADR-0004`, requirements, roadmap, risks, support language, and public claims are explicitly superseded. It would require a new charter-level decision, not a normal dependency approval.

### Explicit Servo browser charter change

This option replaces the current product promise. It would make Turing a Servo browser rather than an independent engine program. The documentation impact would include the charter, requirements, risks, roadmap, competitive claims, technology stack, release operations, support statements, and all public positioning.

## JavaScript Runtime Conflict Analysis

Turing has accepted `ADR-0004`: Turing owns JavaScript semantics, object model, GC, Web IDL integration, debugger, tiering policy, no-JIT mode, and Test262 strategy. The Servo evidence conflicts with that baseline in several ways:

1. `servo` default features include `js_jit`, and the feature maps to `script/js_jit`.
2. The `--no-default-features` metadata profile still reaches `mozjs` and `mozjs_sys`.
3. `servo-script` directly depends on `mozjs`, `servo-script-bindings`, Stylo packages, layout API, network traits, and WebRender API.
4. `servo-script-bindings` is generated and native-link sensitive, and it reaches MozJS and Stylo.
5. Script and binding directories contain dense MozJS/SpiderMonkey, Web IDL, unsafe, and FFI markers.
6. The C API introduces a separate ABI contract and panic/lifetime/threading review even if it appears smaller by package count.

Disabling JIT is therefore not enough to align Servo with Turing's runtime plan. It may reduce one class of executable-code risk, but it does not make SpiderMonkey semantics, GC, wrappers, generated bindings, debugger behavior, or Test262 accountability Turing-owned.

For each source-strategy option, the JavaScript decision must answer:

- whether SpiderMonkey is prohibited, accepted as an external dependency, or used only as a comparator;
- whether Turing's interpreter remains the semantic oracle;
- how Web IDL definitions, generated bindings, and host-object lifetimes are owned;
- how DOM wrapper identity and cross-origin wrappers are validated;
- how no-JIT mode is implemented and tested;
- how debugger/profiler behavior maps to Turing's DevTools protocol;
- how Test262 results are attributed without hiding the underlying runtime;
- whether accepting Servo script code would supersede `ADR-0004`.

## Replacement and Isolation Plans Required

Before any selective option can be scored, owners need at least these replacement plans:

| Surface | Required plan |
|---|---|
| MozJS/SpiderMonkey | Replace with Turing runtime, explicitly prohibit, or supersede `ADR-0004`; define Web IDL and GC bridge consequences |
| `servo-script` and `servo-script-bindings` | Define whether they are excluded, adapted only for research, or accepted with a new runtime decision |
| Stylo | Decide if CSS selector/style machinery can be isolated without importing DOM/runtime assumptions |
| WebRender/WebGPU/WebGL | Define GPU process authority, command validation, device-loss, tracing, memory, and native package boundaries |
| GStreamer/media | Define source-build or binary-package exception policy, codec/patent review, sandbox process, and package minimization |
| Network/storage | Preserve Turing-owned origin/site/profile/partition/quota/credential semantics before considering lower-level protocol or database code |
| Servo C API | Define stable ABI, ownership, panic, lifetime, threading, and header/source provenance rules |
| Build scripts and proc macros | Apply the accepted side-effect policy and dynamic tracing to the selected baseline/profile |

## Inference

The evidence moves `ADR9-EV-011` and `ADR9-EV-012` from missing to partial. It does not move them to captured or owner-reviewed.

The strongest current inference is negative: no measured Servo package boundary is ready to be treated as a small, approved, release-path dependency. The component and runtime questions are now concrete enough to drive owner review, but they remain unresolved.

## Unsupported Conclusions

This report does not show:

- a selected source baseline;
- an accepted Servo relationship;
- a dependency approval;
- an approved component boundary;
- an accepted SpiderMonkey, Stylo, WebRender, or GStreamer dependency;
- a no-JIT-compatible Turing runtime integration;
- a block-level unsafe review;
- a generated-output provenance decision;
- a local compatibility result;
- a fixed-hardware performance result;
- a maintenance or security-response model;
- permission to import Servo source into Turing.

## Documentation and Registry Impact

This report affects:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Research index](README.md);
- [Documentation index](../README.md);
- [Research log](../research-log.md).

It does not change implementation status, support status, risk acceptance, or any source/dependency ledger.

## Next Evidence Required

1. Select the candidate `ADR-0009` baseline and feature profile before reusing closure measurements.
2. Produce per-option dependency closures with normal/build/dev separation, platform/target separation, and selected-component in/out lists.
3. Convert the replacement table into owner-reviewed acceptance or rejection criteria.
4. Complete a Web IDL, GC, wrapper, debugger, no-JIT, and Test262 conflict decision for each source-strategy option.
5. Run dynamic build-script and proc-macro tracing for the selected baseline/profile.
6. Start block-level unsafe and FFI review only for a selected boundary.
7. Pair this analysis with local compatibility, performance, security/sandbox, maintenance, and public-claim impact reports before drafting `ADR-0009`.
