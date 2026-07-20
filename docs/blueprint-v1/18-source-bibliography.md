# 18 — Primary Source Bibliography

This program uses standards, official platform documentation, upstream test suites, and peer-reviewed or primary technical material as sources of truth. Existing browser implementations may be studied for interoperability and research, subject to license/provenance rules, but they are not copied into Turing or treated as normative when they conflict with standards.

Links below are starting points. Each implemented feature records the exact standard revision/test commit used by the corresponding milestone. Dated comparative studies additionally record retrieval date, product version, platform, and current project status where those can change.

## Web platform

- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- WHATWG DOM Standard — https://dom.spec.whatwg.org/
- WHATWG Fetch Standard — https://fetch.spec.whatwg.org/
- WHATWG URL Standard — https://url.spec.whatwg.org/
- WHATWG Encoding Standard — https://encoding.spec.whatwg.org/
- WHATWG Streams Standard — https://streams.spec.whatwg.org/
- WHATWG Web IDL Standard — https://webidl.spec.whatwg.org/
- WHATWG MIME Sniffing — https://mimesniff.spec.whatwg.org/
- WHATWG Infra Standard — https://infra.spec.whatwg.org/
- CSS Working Group drafts — https://drafts.csswg.org/
- SVG 2 — https://www.w3.org/TR/SVG2/
- WAI-ARIA — https://www.w3.org/TR/wai-aria/
- Accessible Name and Description Computation — https://www.w3.org/TR/accname-1.2/
- Permissions — https://www.w3.org/TR/permissions/
- Permissions Policy — https://www.w3.org/TR/permissions-policy-1/
- Content Security Policy — https://www.w3.org/TR/CSP3/
- Referrer Policy — https://www.w3.org/TR/referrer-policy/
- Subresource Integrity — https://www.w3.org/TR/SRI/
- Secure Contexts — https://www.w3.org/TR/secure-contexts/
- Web Authentication — https://www.w3.org/TR/webauthn-3/
- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- WebGPU — https://www.w3.org/TR/webgpu/
- WebAssembly specifications — https://webassembly.github.io/spec/

## Web principles and standards process

- WHATWG working mode — https://whatwg.org/working-mode
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/

These principles guide user needs, interoperability, safety, privacy, accessibility, feature detection, trusted UI, and transparent failure. They do not replace individual normative specifications.

## JavaScript

- ECMA-262 ECMAScript Language Specification — https://tc39.es/ecma262/
- ECMA-402 Internationalization API — https://tc39.es/ecma402/
- TC39 proposals — https://github.com/tc39/proposals
- Test262 — https://github.com/tc39/test262

## Conformance and interoperability

- Web Platform Tests — https://web-platform-tests.org/
- WPT source — https://github.com/web-platform-tests/wpt
- Interop project — https://wpt.fyi/interop
- WebDriver tests within WPT — https://github.com/web-platform-tests/wpt/tree/master/webdriver
- ARIA Authoring Practices — https://www.w3.org/WAI/ARIA/apg/

The 2026-07-19 [Servo local compatibility corpus and WPT/Test262 evidence report](../research/servo-local-compatibility-corpus-2026-07.md) records the retrieval date and inspected Servo checkout. It found Test262 pinned to an exact commit while Servo's WPT configuration still names a moving `master` branch. Any future WPT result must pin the exact commit, local patch set, manifest-generation inputs, and denominator before it can support `ADR-0009`; this entry is a source-control requirement, not a compatibility result.

## Browser architecture and runtime references

These sources support comparative research and falsifiable hypotheses. They do not define Turing behavior and do not authorize source copying.

### Chromium, Blink, and V8

- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- Chromium LayoutNG — https://developer.chrome.com/docs/chromium/layoutng
- Chromium process model and site isolation — https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md
- Chromium tab discarding and reloading — https://chromium.googlesource.com/playground/chromium-org-site/%2B/refs/heads/main/chromium-os/chromiumos-design-docs/tab-discarding-and-reloading.md
- Chromium tab lifecycle source — https://chromium.googlesource.com/chromium/src/%2B/720dadbc215c229ce100bc408edb3aee03b0697e8/chrome/browser/resource_coordinator/tab_lifecycle_unit.h
- Chromium sandbox — https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md
- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/
- V8 Sparkplug baseline compiler — https://v8.dev/blog/sparkplug
- V8 Maglev compiler — https://v8.dev/blog/maglev
- Chromium source license — https://chromium.googlesource.com/chromium/src/+/main/LICENSE

### WebKit and JavaScriptCore

- WebKit documentation — https://docs.webkit.org/
- WebKit2 multiprocess architecture — https://docs.webkit.org/Deep%20Dive/Architecture/WebKit2.html
- WebKit site isolation — https://docs.webkit.org/Deep%20Dive/SiteIsolation.html
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html
- WebKit WPT integration — https://docs.webkit.org/Testing/WebPlatformTests.html
- WebKit licensing — https://webkit.org/licensing-webkit/

### Gecko and SpiderMonkey

- Firefox process model — https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html
- Firefox process roles — https://firefox-source-docs.mozilla.org/ipc/processes.html
- Firefox accessibility architecture — https://firefox-source-docs.mozilla.org/accessible/Architecture.html
- SpiderMonkey overview — https://firefox-source-docs.mozilla.org/js/index.html
- Firefox performance documentation — https://firefox-source-docs.mozilla.org/performance/index.html
- Firefox Remote Protocol — https://firefox-source-docs.mozilla.org/remote/index.html
- Firefox source license — https://github.com/mozilla-firefox/firefox/blob/main/LICENSE

### Independent engines

- Servo project goals and governance — https://servo.org/about/
- Servo repository — https://github.com/servo/servo
- Servo GitHub releases — https://github.com/servo/servo/releases
- Servo crates.io package — https://crates.io/crates/servo
- Servo Stylo repository — https://github.com/servo/stylo
- Servo build dependency release repository — https://github.com/servo/servo-build-deps
- Servo `msvc-deps` release — https://github.com/servo/servo-build-deps/releases/tag/msvc-deps
- Servo project updates — https://servo.org/blog/
- Servo crate documentation — https://docs.rs/servo/latest/servo/
- Servo LTS release policy — https://book.servo.org/embedding/lts-release.html
- Servo WPT pass rates — https://servo.org/wpt/
- Servo license — https://github.com/servo/servo/blob/main/LICENSE
- Ladybird project — https://ladybird.org/
- Ladybird repository and architecture overview — https://github.com/LadybirdBrowser/ladybird
- Ladybird license — https://github.com/LadybirdBrowser/ladybird/blob/master/LICENSE

## Browser benchmarks

- BrowserBench index — https://browserbench.org/
- Speedometer 3.1 — https://browserbench.org/Speedometer3.1/
- JetStream 3.0 — https://browserbench.org/JetStream3.0/
- MotionMark current benchmark — https://browserbench.org/MotionMark/
- JetStream 3 announcement — https://blog.google/chromium/jetstream-3-a-modern-benchmark-for-high-performance-compute-intensive-web-applications/
- Chrome Speedometer 3.1 and JetStream 3 performance announcement — https://blog.google/chromium/a-double-victory-for-web-speed-chrome-breaks-records-again-on-speedometer-31-and-jetstream-3/
- Chromium competitive-benchmark regression policy — https://chromium.googlesource.com/chromium/src/+/main/docs/benchmark_performance_regressions.md
- Web Platform Tests documentation — https://web-platform-tests.org/
- Chrome Releases — https://chromereleases.googleblog.com/
- Microsoft Edge Stable release notes — https://learn.microsoft.com/en-us/deployedge/microsoft-edge-relnote-stable-channel
- Firefox release notes — https://www.firefox.com/en-US/releases/
- Safari release notes — https://developer.apple.com/documentation/safari-release-notes/
- Safari resources and Technology Preview — https://developer.apple.com/safari/resources/

BrowserBench suites are diagnostics. Product claims also require compatibility coverage, real interaction workloads, memory, energy, process/isolation disclosure, failure accounting, and fixed hardware.

## Developer protocols, agents, and tools

- WebDriver BiDi Editor's Draft — https://w3c.github.io/webdriver-bidi/
- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/
- Firefox Remote Protocol — https://firefox-source-docs.mozilla.org/remote/index.html
- Model Context Protocol specification, version 2025-11-25 at retrieval — https://modelcontextprotocol.io/specification/2025-11-25
- Model Context Protocol architecture — https://modelcontextprotocol.io/docs/learn/architecture

MCP is evaluated as an external tool/resource transport subordinate to Turing grants and policy, not as a browser authority model.

## Browser product references

Product references support dated UX, privacy, workflow, distribution, and governance studies. Their marketing or benchmark claims are not accepted as independent evidence.

- Brave — https://brave.com/
- Brave Shields — https://brave.com/shields/
- Arc — https://arc.net/
- Arc feature documentation — https://resources.arc.net/hc/en-us/categories/16435255982103-Features
- Zen Browser — https://zen-browser.app/
- Zen Browser source — https://github.com/zen-browser/desktop
- Orion Browser — https://orionbrowser.com/
- Safari — https://www.apple.com/safari/

## Networking

- HTTP Semantics, RFC 9110 — https://www.rfc-editor.org/rfc/rfc9110
- HTTP/1.1, RFC 9112 — https://www.rfc-editor.org/rfc/rfc9112
- HTTP/2, RFC 9113 — https://www.rfc-editor.org/rfc/rfc9113
- HTTP/3, RFC 9114 — https://www.rfc-editor.org/rfc/rfc9114
- QUIC Transport, RFC 9000 — https://www.rfc-editor.org/rfc/rfc9000
- TLS 1.3, RFC 8446 — https://www.rfc-editor.org/rfc/rfc8446
- Cookies, RFC 6265 and current HTTPbis work — https://httpwg.org/specs/
- WebSocket, RFC 6455 — https://www.rfc-editor.org/rfc/rfc6455
- Public Suffix List — https://publicsuffix.org/

## Unicode, text, locale, and fonts

- Unicode Standard — https://www.unicode.org/standard/standard.html
- Unicode Standard Annexes — https://www.unicode.org/reports/
- Unicode Bidirectional Algorithm — https://www.unicode.org/reports/tr9/
- Common Locale Data Repository — https://cldr.unicode.org/
- International Components for Unicode — https://icu.unicode.org/
- HarfBuzz — https://harfbuzz.github.io/
- FreeType — https://freetype.org/
- OpenType specification — https://learn.microsoft.com/en-us/typography/opentype/spec/

## Graphics and GPU

- Vulkan specification — https://registry.khronos.org/vulkan/
- Metal documentation — https://developer.apple.com/metal/
- Direct3D 12 documentation — https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-graphics
- WebGL specifications — https://www.khronos.org/webgl/
- Khronos Conformance Tests — https://github.com/KhronosGroup/VK-GL-CTS
- wgpu project, if evaluated as an abstraction — https://github.com/gfx-rs/wgpu

## Operating-system security and platform APIs

### macOS

- Apple Platform Security — https://support.apple.com/guide/security/welcome/web
- App Sandbox — https://developer.apple.com/documentation/security/app-sandbox
- Hardened Runtime — https://developer.apple.com/documentation/security/hardened-runtime
- Accessibility — https://developer.apple.com/documentation/appkit/accessibility
- Code signing and notarization — https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution

### Windows

- Windows application security — https://learn.microsoft.com/en-us/windows/security/
- Microsoft C++ (MSVC) Build Tools installation and servicing — https://learn.microsoft.com/en-us/cpp/overview/acquire-msvc?view=msvc-160
- AppContainer isolation — https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation
- Process mitigation policies — https://learn.microsoft.com/en-us/windows/win32/procthread/process-mitigation-policy
- UI Automation — https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/ui-automation-overview
- Code signing — https://learn.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing-reqs

### Linux

- Linux namespaces — https://man7.org/linux/man-pages/man7/namespaces.7.html
- seccomp — https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html
- Landlock — https://www.kernel.org/doc/html/latest/userspace-api/landlock.html
- Flatpak sandbox and portals — https://docs.flatpak.org/
- Wayland — https://wayland.freedesktop.org/
- AT-SPI — https://gitlab.gnome.org/GNOME/at-spi2-core
- PipeWire — https://pipewire.org/

## Rust and compiler infrastructure

- Rust language documentation — https://doc.rust-lang.org/
- Rust Reference type layout — https://doc.rust-lang.org/stable/reference/type-layout.html
- Rust allocation APIs and `Layout` — https://doc.rust-lang.org/stable/alloc/alloc/
- Rustonomicon — https://doc.rust-lang.org/nomicon/
- Rustup toolchain concepts — https://rust-lang.github.io/rustup/concepts/toolchains.html
- Miri — https://github.com/rust-lang/miri
- Rust fuzzing book — https://rust-fuzz.github.io/book/
- Cargo supply-chain and package metadata — https://doc.rust-lang.org/cargo/
- Cargo build command and `--locked`/`--offline` semantics — https://doc.rust-lang.org/cargo/commands/cargo-build.html
- Cargo registry index and checksums — https://doc.rust-lang.org/cargo/reference/registry-index.html
- Cargo-deny supply-chain checks — https://embarkstudios.github.io/cargo-deny/
- Git archive command — https://git-scm.com/docs/git-archive
- RustSec advisory database — https://rustsec.org/advisories/
- Cranelift — https://cranelift.dev/
- WebAssembly Binary Toolkit — https://github.com/WebAssembly/wabt
- LLVM sanitizers — https://clang.llvm.org/docs/index.html
- libFuzzer — https://llvm.org/docs/LibFuzzer.html
- AFL++ — https://aflplus.plus/

## Cryptography and secure update foundations

- Rustls project — https://github.com/rustls/rustls
- BoringSSL project, if evaluated behind a platform boundary — https://boringssl.googlesource.com/boringssl/
- The Update Framework — https://theupdateframework.io/
- in-toto — https://in-toto.io/
- SLSA — https://slsa.dev/
- SPDX — https://spdx.dev/
- CycloneDX — https://cyclonedx.org/
- Sigstore — https://www.sigstore.dev/

Use of any listed project is not automatic approval. It remains subject to the dependency, license, threat-model, fuzzing, and replacement policy.

## Databases, compression, media, and document formats

- SQLite — https://sqlite.org/
- zlib — https://zlib.net/
- Brotli — https://github.com/google/brotli
- Zstandard — https://facebook.github.io/zstd/
- PNG — https://www.w3.org/TR/png-3/
- JPEG — https://jpeg.org/
- AV1 — https://aomedia.org/av1-features/
- WebM — https://www.webmproject.org/
- PDF Association technical resources — https://pdfa.org/resource/
- ISO specifications may require licensed access; exact normative editions must be recorded by implementers.

## Accessibility testing references

- Web Content Accessibility Guidelines — https://www.w3.org/TR/WCAG22/
- Accessibility Object Model work — https://wicg.github.io/aom/
- Apple accessibility testing documentation — https://developer.apple.com/accessibility/
- Microsoft accessibility testing — https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-testing
- GNOME accessibility — https://developer.gnome.org/documentation/guidelines/accessibility.html

## Networking, storage, media, platform, operations, and verification sources

### Networking and transport

- DNS concepts — RFC 1034 and RFC 1035: https://www.rfc-editor.org/rfc/rfc1034 and https://www.rfc-editor.org/rfc/rfc1035
- Happy Eyeballs v2 — RFC 8305: https://www.rfc-editor.org/rfc/rfc8305
- HTTP Semantics and HTTP/1.1/2/3 — RFC 9110, 9112, 9113, 9114
- QUIC — RFC 9000: https://www.rfc-editor.org/rfc/rfc9000
- TLS 1.3 — RFC 8446: https://www.rfc-editor.org/rfc/rfc8446
- Fetch, URL, Streams, WebSocket, WebTransport, CSP, CORS-related WPT, and Public Suffix List upstreams

### Storage and reliability

- Storage Standard: https://storage.spec.whatwg.org/
- Indexed Database API: https://w3c.github.io/IndexedDB/
- Service Workers: https://w3c.github.io/ServiceWorker/
- Google SRE Book, Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
- Google SRE Book, Embracing Risk: https://sre.google/sre-book/embracing-risk/
- Google SRE Workbook, Implementing SLOs: https://sre.google/workbook/implementing-slos/
- Clear Site Data: https://w3c.github.io/webappsec-clear-site-data/
- SQLite: https://sqlite.org/

### Media, documents, and devices

- Media Source Extensions: https://w3c.github.io/media-source/
- WebCodecs: https://www.w3.org/TR/webcodecs/
- WebRTC: https://w3c.github.io/webrtc-pc/
- Encrypted Media Extensions: https://www.w3.org/TR/encrypted-media/
- GStreamer project and source releases: https://gstreamer.freedesktop.org/
- PNG, AV1, WebM, OpenType, PDF Association, and platform printing documentation

### Platform and accessibility

- Apple AppKit, Platform Security, accessibility, sandbox, signing, and notarization documentation
- Microsoft Windows application, graphics, UI Automation, AppContainer, mitigation, packaging, and signing documentation
- Wayland, XDG portals, PipeWire, Linux namespaces, seccomp, Landlock, and AT-SPI documentation
- WAI-ARIA, Accessible Name and Description Computation, WCAG, and ARIA Authoring Practices

### Build, release, and update trust

- Reproducible Builds: https://reproducible-builds.org/
- SLSA: https://slsa.dev/
- in-toto: https://in-toto.io/
- The Update Framework: https://theupdateframework.io/
- Sigstore: https://www.sigstore.dev/
- Git tag and signed-tag semantics: https://git-scm.com/docs/git-tag
- Git tag signature verification: https://git-scm.com/docs/git-verify-tag
- GitHub commit and tag signature verification: https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
- SPDX and CycloneDX
- Windows Package Manager and winget package manifests: https://learn.microsoft.com/en-us/windows/package-manager/
- MSYS2 package and source records: https://www.msys2.org/

### Performance, security, and developer evidence

- Perfetto: https://perfetto.dev/
- Perfetto track events: https://perfetto.dev/docs/instrumentation/track-events
- Chromium trace-event best practices: https://chromium.googlesource.com/chromium/src/+/main/docs/trace_events.md
- Chromium tracing architecture: https://chromium.googlesource.com/chromium/src/+/HEAD/base/tracing/README.md
- rr deterministic debugging: https://rr-project.org/
- Firefox debugging with rr: https://firefox-source-docs.mozilla.org/contributing/debugging/debugging_firefox_with_rr.html
- Windows Performance Toolkit and Event Tracing for Windows
- Apple Instruments and signposts
- Linux perf and platform power/energy interfaces
- Spectre paper: https://spectreattack.com/spectre.pdf
- RLBox paper: https://www.usenix.org/conference/usenixsecurity20/presentation/narayan
- LLVM CFI and sanitizer documentation
- WebDriver BiDi, Chrome DevTools Protocol, Firefox Remote Protocol, and WebKit Inspector documentation

All sources require exact revision, retrieval date, license/provenance, tested platform, and local patch recording before they support implementation or product claims.

## Browser security research inputs

Primary research should be added as individual annotated references tied to a design decision. Relevant domains include site isolation, sandbox architecture, capability systems, memory-safe browser components, browser fuzzing, JIT hardening, CFI, pointer authentication, allocator hardening, renderer exploit chains, origin isolation, storage partitioning, update security, provider/tool isolation, and trusted UI.

Do not cite a secondary blog when an original paper, standard, advisory, platform document, or source repository is available.

## Source recording template

For each design or implementation source record:

```yaml
id: SRC-0001
title: Exact title
publisher: Standards body, project, vendor, or authors
url: Canonical URL
revision: Commit, edition, draft date, or retrieval date
used_by:
  - REQ-...
  - ADR-...
notes: What behavior or decision it supports
license_or_access: Applicable terms
```

The implementation's behavior notes should quote minimally and describe algorithms in original language. Test imports preserve upstream licenses and revision metadata.

## Professional buildout sources

- NIST SSDF — https://csrc.nist.gov/pubs/sp/800/218/final
- NIST Incident Response — https://csrc.nist.gov/pubs/sp/800/61/r3/final
- SLSA — https://slsa.dev/spec/v1.2/
- Reproducible Builds — https://reproducible-builds.org/
- GitHub CODEOWNERS — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Semantic Versioning — https://semver.org/
- JSON Schema — https://json-schema.org/draft/2020-12
- Servo — https://servo.org/
- WebAssembly Component Model — https://component-model.bytecodealliance.org/
- Chrome Extensions — https://developer.chrome.com/docs/extensions/

<!-- MARKET-STRATEGY-2026-07 -->
## Market and product evidence — retrieved 2026-07-16

- StatCounter desktop browser share: https://gs.statcounter.com/browser-market-share/desktop
- Chrome tab groups and AI: https://support.google.com/chrome/answer/2391819 and https://blog.google/products-and-platforms/products/chrome/chrome-reimagined-with-ai/
- Edge Workspaces and performance: https://support.microsoft.com/en-us/edge/getting-started-with-microsoft-edge-workspaces and https://support.microsoft.com/en-us/edge/learn-about-performance-features-in-microsoft-edge
- Firefox sidebar, split view, and containers: https://support.mozilla.org/en-US/kb/use-sidebar-access-tools-and-vertical-tabs , https://support.mozilla.org/en-US/kb/split-view-firefox , https://support.mozilla.org/en-US/kb/containers
- Vivaldi Workspaces and Sync: https://vivaldi.com/features/workspaces/ and https://help.vivaldi.com/desktop/tools/sync/
- Opera One R3: https://blogs.opera.com/news/2026/01/opera-one-r3-new-browser-update/
- Brave Leo and agentic safety: https://brave.com/leo/ and https://brave.com/blog/ai-browsing/
- Safari iCloud continuity and Profiles: https://support.apple.com/guide/icloud/what-you-can-do-with-icloud-and-safari-mm9b8da4f328/icloud and https://support.apple.com/en-euro/105100
- Arc Profiles, Split View, and sharing: https://resources.arc.net/hc/en-us/articles/19227964556183-Profiles-Separate-Work-Personal-Browsing , https://resources.arc.net/hc/en-us/articles/19335393146775-Split-View-View-Multiple-Tabs-at-Once , https://resources.arc.net/hc/en-us/articles/19228534606743-Share-Spaces-Folders-Splits-with-Anyone
- Mozilla Connect and Zen demand signals are listed in the dated market report.
- Agent security research: WASP https://arxiv.org/abs/2504.18575 , ceLLMate https://arxiv.org/abs/2512.12594 , context manipulation https://arxiv.org/abs/2506.17318 , MUZZLE https://arxiv.org/abs/2602.09222 .

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI framework and authoring sources

- Slint repository and architecture — https://github.com/slint-ui/slint
- Slint Winit backend — https://docs.slint.dev/latest/docs/slint/guide/backends-and-renderers/backend_winit/
- Slint platform abstraction — https://docs.slint.dev/latest/docs/rust/slint/platform/
- Slint accessibility roles — https://docs.slint.dev/latest/docs/rust/slint/language/enum.AccessibleRole
- Vizia — https://github.com/vizia/vizia
- Floem — https://github.com/lapce/floem
- GPUI — https://github.com/zed-industries/zed/tree/main/crates/gpui
- Xilem — https://xilem.dev/
- Makepad — https://github.com/makepad/makepad
- Freya — https://freyaui.dev/
- egui — https://github.com/emilk/egui
- Tauri architecture — https://v2.tauri.app/concept/architecture/
- React Compiler — https://react.dev/blog/2025/10/07/react-compiler-1
- TypeScript JSX — https://www.typescriptlang.org/docs/handbook/jsx

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent execution, secure development, and production release

- NIST SP 800-218 SSDF 1.1 — https://csrc.nist.gov/pubs/sp/800/218/final
- NIST SP 800-218A — https://csrc.nist.gov/pubs/sp/800/218/a/final
- NIST SSDF publications and 1.2 draft status — https://csrc.nist.gov/projects/ssdf/publications
- SLSA 1.2 — https://slsa.dev/spec/v1.2/
- The Update Framework — https://theupdateframework.github.io/specification/latest/
- GitHub protected branches — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub CODEOWNERS — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- W3C accessibility evaluation tools — https://www.w3.org/WAI/test-evaluate/tools/selecting/
- WebDriver BiDi — https://www.w3.org/TR/webdriver-bidi/
