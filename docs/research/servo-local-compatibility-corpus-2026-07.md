# Servo Local Compatibility Corpus and WPT/Test262 Evidence - July 2026

Status: first-pass compatibility evidence prep with checked no-claim corpus, route self-test, and HTTPS harness plan; no compatibility claim
Owner: quality, engine, JavaScript runtime, compatibility, documentation, and release operations
Related gate: `PB-002`, `ADR-0009`, `ADR9-EV-013`
Date: 2026-07-18

## Question

What compatibility evidence exists around the external Servo build, and what corpus/test-suite plan is required before `ADR-0009` can use Servo results to support a source-strategy decision?

This report does not claim that Servo, Turing, or any source-strategy option is compatible with the modern web. It does not approve Servo source, WPT metadata, Test262 files, or any browser-run result for Turing release claims. It records the test inventory and denominator requirements that must exist before compatibility evidence can influence `ADR-0009`.

## Sources and Environment

Primary local evidence came from the external Servo checkout at `C:\ts\servo`, outside this repository.

| Item | Value |
|---|---|
| Servo commit inspected | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Tracked files | `193033` |
| Tracked-file status | `0` changed paths |
| Built shell evidence | `servoshell.exe` exists from the previous short-path Windows development build |
| Turing repository role | documentation and registry update only |
| Commands | read-only `git`, `Get-ChildItem`, `rg`, Python manifest counters, and file inspection |

## Method

The analysis inspected:

1. Servo's WPT directory layout under `tests/wpt/`;
2. WPT configuration, include rules, host aliases, and runner command entry points;
3. WPT manifest and metadata files for upstream, Servo-specific, WebGL, and WebGPU suites;
4. focused WPT directory sizes for HTML, DOM, CSS, Fetch, storage, workers, WebDriver, WebGPU/WebGL, accessibility, JS, and WebAssembly;
5. Test262-related WPT integration and vendored Test262 metadata.

No WPT, Test262, local-corpus, or browser-run command was executed in this report. The previous Servo build proves a runnable development binary exists; it does not prove any compatibility result.

## Servo WPT Layout

Servo carries WPT sources, metadata, and additional suites under `tests/wpt/`.

| Path | Files | Directories | Bytes | Notes |
|---|---:|---:|---:|---|
| `tests/wpt/tests` | 160978 | 6683 | 499814577 | Upstream WPT test tree |
| `tests/wpt/meta` | 18778 | 1566 | 56771681 | Upstream WPT metadata and `MANIFEST.json` |
| `tests/wpt/mozilla/tests` | 1917 | 62 | 9362766 | Servo-specific Mozilla-origin suite path |
| `tests/wpt/mozilla/meta` | 329 | 37 | 344562 | Metadata for Mozilla-origin suite path |
| `tests/wpt/webgl/meta` | 321 | 58 | 922548 | WebGL metadata |
| `tests/wpt/webgpu/meta` | 33 | 5 | 26165729 | WebGPU metadata |

The WPT `config.ini` declares four manifest roots:

- upstream WPT: `tests = tests`, `metadata = meta`, `url-base = /`;
- Mozilla-origin tests: `tests = mozilla/tests`, `metadata = mozilla/meta`, `url_base = /_mozilla/`;
- WebGL: `tests = webgl/tests`, `metadata = webgl/meta`, `url_base = /_webgl/`;
- WebGPU: `tests = webgpu/tests`, `metadata = webgpu/meta`, `url_base = /_webgpu/`.

The `aliases` file maps `/`, `/_mozilla/`, `/_webgl/`, and `/_webgpu/` to the corresponding local test roots. The `hosts` file maps many `web-platform.test` and `not-web-platform.test` hostnames to `127.0.0.1`, including internationalized-domain variants. That host mapping is compatibility-relevant because origin, site, IDNA, mixed-content, cookie, CORS, CSP, and navigation tests depend on those names rather than plain `localhost`.

## WPT Include and Expectation Posture

The `include.ini` file begins with `skip: true`, then opts selected suites back in. It had:

| Include metric | Count |
|---|---:|
| Sections | 190 |
| `skip: false` entries | 116 |
| `skip: true` entries | 74 |

Top-level opt-ins include `_mozilla`, `_webgl`, `beacon`, `bluetooth`, `clipboard-apis`, `compression`, `console`, `content-security-policy`, `cookies`, `cors`, `css`, `custom-elements`, `dom`, `domparsing`, `domxpath`, `editing`, `encoding`, `eventsource`, `fetch`, `FileAPI`, `fullscreen`, `gamepad`, `geolocation`, `html`, `import-maps`, `IndexedDB`, `js`, `mimesniff`, `mixed-content`, `permissions`, `pointerevents`, `referrer-policy`, `resource-timing`, `sanitizer-api`, `secure-contexts`, `shadow-dom`, `svg`, `trusted-types`, `url`, `wasm`, `WebCryptoAPI`, `webdriver`, `webgl`, `webidl`, `websockets`, `webstorage`, `webxr`, `workers`, and `xhr`.

Scoped skips include WebDriver BiDi, COOP/COEP, service workers, streams as a root suite with selected subtrees enabled, several CSS modules, shared-array-buffer cases, CSS layout API, CSS view transitions, Web Animations root tests with interfaces enabled, WebVTT root tests with API enabled, WebXR DOM overlay, and several generated referrer-policy and navigation-timing cases.

This means "Servo has WPT" is not a compatibility denominator. Any `ADR-0009` result must publish the exact include rules, disabled rules, metadata expectations, selected test paths, and failure denominator.

## Manifest and Metadata Observations

`MANIFEST.json` files were present for upstream WPT, Mozilla-origin tests, WebGL, and WebGPU metadata roots.

| Metadata root | Manifest bytes | `.ini` files | Disabled markers | Expected markers | Crash markers | Fail markers |
|---|---:|---:|---:|---:|---:|---:|
| `tests/wpt/meta` | 39462596 | 18777 | 14 | 154382 | 160 | 145965 |
| `tests/wpt/mozilla/meta` | 304001 | 328 | 0 | 372 | 2 | 344 |
| `tests/wpt/webgl/meta` | 685301 | 320 | 38 | 5589 | 63 | 5445 |
| `tests/wpt/webgpu/meta` | 743679 | 32 | 0 | 58816 | 34 | 48337 |

The manifest item counts were small compared with the checked-out WPT source tree because the manifests reflect the active metadata/configuration state rather than every file under `tests/wpt/tests`.

| Metadata root | Testharness paths | Reftest paths | Crashtest paths | WDSpec paths | Test262 paths | Support paths |
|---|---:|---:|---:|---:|---:|---:|
| upstream WPT metadata | 263 | 41 | 43 | 2 | 2 | 299 |
| Mozilla metadata | 8 | 4 | 3 | 0 | 0 | 9 |
| WebGL metadata | 3 | 0 | 2 | 0 | 0 | 13 |
| WebGPU metadata | 1 | 1 | 0 | 0 | 0 | 4 |

The expectation counts prove that a future run must report both expected and unexpected outcomes. A pass count without the expected-failure and skipped-test denominator would be misleading.

## Focus-Area Inventory

The following WPT source-tree counts identify first focus areas for `ADR-0009`. These are file counts, not runnable-test counts and not pass/fail results.

| Focus area | Files |
|---|---:|
| `css` | 54344 |
| `html` | 14154 |
| `content-security-policy` | 1356 |
| `fetch` | 984 |
| `webdriver` | 943 |
| `wasm` | 830 |
| `dom` | 797 |
| `service-workers` | 794 |
| `workers` | 606 |
| `editing` | 379 |
| `encoding` | 340 |
| `interfaces` | 334 |
| `core-aam` | 289 |
| `websockets` | 266 |
| `IndexedDB` | 245 |
| `accname` | 183 |
| `cookies` | 171 |
| `accessibility` | 59 |
| `webidl` | 51 |
| `storage` | 42 |
| `js` | 32 |
| `html-aam` | 18 |
| `webgl` | 12 |
| `webgpu` | 4 |
| `ecmascript` | 3 |

`ADR-0009` should not rely on the largest directories alone. The minimum useful compatibility corpus must include security and lifecycle features that determine source-strategy risk: origin/site boundaries, COOP/COEP, CSP, Fetch/CORS, cookies/storage partitioning, navigation, workers/service workers, JS host bindings, Web IDL, layout, accessibility, WebDriver, WebGL/WebGPU, and media where a component option reaches those systems.

## Test262 Observations

The searched Servo command and docs surface did not expose a separate Servo-owned Test262 runner. Test262 appears through WPT infrastructure:

- `tests/wpt/tests/resources/test262/README.md` describes WPT's Test262 window-wrapper integration;
- `tests/wpt/tests/third_party/test262/vendored.toml` records source `https://github.com/tc39/test262` at revision `b66872a92487694396fb082343e08dd7cca5ddf4`;
- `tests/wpt/tests/third_party/test262` contained `53504` files and `86152755` bytes;
- `tests/wpt/tests/third_party/test262/test` contained `53441` `.js` test files;
- `tests/wpt/tests/third_party/test262/harness` contained `42` harness files;
- WPT's `ecmascript` directory contained only `3` files, and the WPT `js` directory contained `32` files.

For Turing, WPT-hosted Test262 integration is not a substitute for the `ADR-0004` requirement: Turing needs its own Test262 harness and published language-feature denominator for the Turing-owned runtime. For a Servo source-strategy decision, any SpiderMonkey-derived result must be labeled as such and cannot be treated as evidence for Turing's interpreter-first runtime.

## Servo Runner Entry Points

Servo's Python command layer exposes:

- `test-wpt` to run the regular web platform test suite;
- `test-wpt-failure` to invert a WPT run for failure expectations;
- `update-manifest` to regenerate `MANIFEST.json`;
- `update-wpt` to update WPT;
- `test-ohos-wpt` for a single WPT test on an OHOS device through WebDriver;
- additional commands for jQuery, Dromaeo, Speedometer, DevTools tests, unit tests, and script support tests.

The WPT runner path sets `HOST_FILE` to `tests/wpt/hosts`. The Turing `ADR-0009` replay plan must therefore capture host-file use, ports, TLS/cert setup, profile directory, process mode, feature flags, log output, selected test paths, include rules, metadata expectations, and exact binary hash.

## Tiny Local Corpus Plan

Before broad WPT runs, `ADR9-EV-013` needs a tiny local corpus that can run against Servo, future Turing prototypes, and comparison browsers without network nondeterminism.

| Corpus item | Purpose | Required result fields |
|---|---|---|
| Static HTML/CSS document | Parser, DOM, style, layout, paint, fonts, accessibility names | load status, DOM assertions, screenshot or semantic trace hash, accessibility snapshot, console errors |
| Dynamic DOM and events page | script execution, event loop, mutation, style/layout invalidation | DOM state, event order, task/microtask order, layout invalidation trace |
| Origin and storage page pair | site/origin, cookies, local/session storage, partitioning | origin identity, storage keys, cookie visibility, blocked cross-origin access |
| Fetch/CORS/CSP page | request policy, preflight, CSP, redirect, mixed-content behavior | request log, response status, blocked reasons, console/security events |
| Web IDL/JS host-binding page | wrappers, exceptions, brand checks, promises | assertion list, exception names, promise timing, wrapper identity |
| Form/editing/accessibility page | keyboard/editing, labels, roles, names, states | input events, selection state, accessibility tree |
| WebDriver/headless smoke | automation protocol and error behavior | command log, element resolution, navigation timing, failure reason |
| Crash/timeout resource | test harness failure denominator | timeout, crash, recovery, artifact hash |

Existing no-claim benchmark fixtures under `benchmarks/corpus/no-claim-smoke/` prove only local static-server shape. They are not compatibility tests and do not cover WPT host aliases, scripting semantics, origin/storage policy, accessibility assertions, or WebDriver.

## Checked No-Claim Local Corpus Fixtures

The machine-readable [ADR-0009 local compatibility corpus schema](../blueprint-v1/machine/servo-local-compatibility-corpus.schema.json), checked [no-claim tiny corpus manifest](../blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json), and [`validate_servo_local_compatibility_corpus.py`](../../tools/validate_servo_local_compatibility_corpus.py) now turn the tiny local corpus plan into a stable contract.

The checked manifest now points at generated local HTML fixtures under `benchmarks/compatibility/adr0009/no-claim-tiny/`, pins each fixture's byte count and SHA-256 digest, and requires local-only `turing.invalid` origins. The fixture set covers these local-only case categories:

- static document, style, layout, and accessibility smoke;
- dynamic DOM, events, and task ordering smoke;
- origin, site, cookie, and storage partition smoke;
- Fetch, CORS, CSP, redirect, and mixed-content smoke;
- Web IDL, wrapper identity, exceptions, and promises smoke;
- form, editing, focus, selection, and accessibility smoke;
- WebDriver and headless automation smoke;
- crash, timeout, and resource-denominator smoke.

Every case remains `not_executed`, forbids external network access, and forbids compatibility claims. The manifest and fixture root are useful because they fix the assertion groups, local `turing.invalid` origins, required artifacts, fixture paths, fixture hashes, WPT focus areas, Test262 attribution language, and failure denominator before any browser result exists. They do not provide local HTTPS execution, host-alias browser execution, browser-run raw logs, WPT output, Test262 output, Servo pass/fail counts, or a compatibility result.

## Checked No-Claim Route Self-Test

The dependency-free [`serve_servo_local_compatibility_corpus.py`](../../tools/serve_servo_local_compatibility_corpus.py) tool now provides a no-browser route self-test for the checked fixtures. `python3 -B tools/serve_servo_local_compatibility_corpus.py --self-test` validates the corpus manifest, starts a loopback HTTP/1.1 server on an ephemeral port, uses Host headers for the `turing.invalid` origins, serves every declared fixture route, checks response status, content type, byte count, SHA-256 hash, no-store cache header, shutdown, and closed-port behavior, and emits `ADR9.EV013.NOCLAIM_ROUTE_SELF_TEST.2026_07`.

This evidence proves only repository route plumbing for generated fixtures. It deliberately records `https_used=false`, `tls_certificate_provided=false`, `dns_os_modified=false`, `browser_launched=false`, `compatibility_result_generated=false`, `wpt_result_generated=false`, and `test262_result_generated=false`.

## Checked No-Claim HTTPS Harness Plan

The machine-readable [ADR-0009 local compatibility HTTPS harness schema](../blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json), checked [no-claim HTTPS host-alias harness plan](../blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json), and [`validate_servo_local_compatibility_https_harness.py`](../../tools/validate_servo_local_compatibility_https_harness.py) now define the required local HTTPS execution envelope for the checked corpus.

The plan is `plan_only_no_browser_run`. It requires a future ephemeral local test certificate or local CA outside source control, SNI and SAN coverage for every declared `turing.invalid` origin, isolated profile trust-store handling, host-to-loopback alias proof, before/after cleanup proof, browser-visible-origin evidence, per-origin route results, per-case pass/failure records, raw logs, certificate fingerprints, and failure-denominator accounting.

The plan deliberately forbids external DNS, persistent hosts-file modification, substituting Host headers for a browser run, committed private keys, Servo adoption claims, Turing compatibility claims, Chrome-class compatibility claims, WPT pass-rate claims, Test262 pass-rate claims, HTTPS execution claims, or release-code authorization. No HTTPS server, certificate, private key, trust-store change, host alias, browser launch, Servo run, WPT run, Test262 run, or compatibility result exists from this plan.

## Required Run Record

Every future compatibility run must record:

- source baseline, binary path, binary hash, build profile, feature flags, and `js_jit` or no-JIT state;
- OS, hardware, GPU, driver, display, power/thermal state, and sandbox/process mode;
- selected WPT include file, explicit test paths, metadata roots, manifest hashes, host-file hash, ports, TLS/cert state, and timeout policy;
- profile/cache state and cleanup policy;
- result counts for pass, fail, timeout, crash, error, skip, expected failure, unexpected pass, and subtest failures;
- disabled-test and unsupported-API map;
- raw logs and machine-readable result files with hashes;
- rerun/flakiness policy and sample count;
- exact statement of what the result can and cannot support.

## Inference

The evidence moves `ADR9-EV-013` from missing to partial. It shows that Servo has a large WPT tree, active include rules, extensive expected-result metadata, Test262 vendoring through WPT, runner entry points, and now a checked Turing-owned no-claim local compatibility corpus manifest, generated fixture files, HTTP route self-test, and HTTPS host-alias harness plan. It also shows why no compatibility claim is possible yet: the HTTPS harness plan has not been executed, no host-alias browser run exists, no local corpus was executed in Servo, no WPT focus-area run was captured, no disabled-test denominator was accepted, no unsupported-API map exists, and no result was compared against future Turing or competitor browsers.

## Unsupported Conclusions

This report does not show:

- Servo WPT pass rate;
- Servo Test262 pass rate;
- Turing compatibility;
- compatibility of any Servo component boundary;
- compatibility parity with Chrome, Firefox, Safari, WebKit, Gecko, or Ladybird;
- safety for arbitrary web browsing;
- that WPT-hosted Test262 evidence satisfies Turing's JavaScript-runtime plan;
- that any skipped or expected-failure metadata is acceptable for Turing.

## Documentation and Registry Impact

This report affects:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [`servo-local-compatibility-corpus.schema.json`](../blueprint-v1/machine/servo-local-compatibility-corpus.schema.json);
- [`servo-local-compatibility-https-harness.schema.json`](../blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json);
- [`no-claim-tiny-adr0009.corpus.json`](../blueprint-v1/machine/servo-local-compatibility-corpora/no-claim-tiny-adr0009.corpus.json);
- [`no-claim-https-host-alias.plan.json`](../blueprint-v1/machine/servo-local-compatibility-harnesses/no-claim-https-host-alias.plan.json);
- `benchmarks/compatibility/adr0009/no-claim-tiny/`;
- [`validate_servo_local_compatibility_corpus.py`](../../tools/validate_servo_local_compatibility_corpus.py);
- [`validate_servo_local_compatibility_https_harness.py`](../../tools/validate_servo_local_compatibility_https_harness.py);
- [`serve_servo_local_compatibility_corpus.py`](../../tools/serve_servo_local_compatibility_corpus.py);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Research index](README.md);
- [Documentation index](../README.md);
- [Research log](../research-log.md);
- [Research program](../blueprint-v1/22-research-program.md).

It does not change implementation status, support status, source approval, dependency approval, benchmark status, or public compatibility claims.

## Next Evidence Required

1. Execute the checked local HTTPS host-alias harness plan so the checked Turing-owned local compatibility corpus fixtures are served exactly as the manifest declares, beyond the checked HTTP Host-header route self-test and plan-only record.
2. Run the tiny local corpus against the external Servo build with raw logs, certificate fingerprints, host-alias cleanup proof, route artifacts, and hashes.
3. Run a focused WPT subset for `html`, `dom`, `css`, `fetch`, `cookies`, `storage`, `workers`, `webidl`, `js`, accessibility, WebDriver, WebGL/WebGPU as applicable to the selected `ADR-0009` option.
4. Produce disabled-test, expected-failure, timeout, crash, and unsupported-API accounting.
5. Produce a separate Turing Test262 harness plan for `ADR-0004`, then decide how Servo/SpiderMonkey results are labeled in `ADR-0009`.
6. Compare the same corpus against named browser versions only after the harness is stable and equivalent settings are documented.
