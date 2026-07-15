# 18 — Primary Source Bibliography

This program uses standards, official platform documentation, upstream test suites, and peer-reviewed or primary technical material as sources of truth. Existing browser implementations may be studied for interoperability and research, subject to license/provenance rules, but they are not copied into Turing or treated as normative when they conflict with standards.

Links below are starting points. Each implemented feature records the exact standard revision/test commit used by the corresponding milestone.

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
- Rustonomicon — https://doc.rust-lang.org/nomicon/
- Miri — https://github.com/rust-lang/miri
- Rust fuzzing book — https://rust-fuzz.github.io/book/
- Cargo supply-chain and package metadata — https://doc.rust-lang.org/cargo/
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

## Browser security research inputs

Primary research should be added as individual annotated references tied to a design decision. Relevant domains include site isolation, sandbox architecture, capability systems, memory-safe browser components, browser fuzzing, JIT hardening, CFI, pointer authentication, allocator hardening, renderer exploit chains, origin isolation, storage partitioning, and update security.

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

The implementation’s behavior notes should quote minimally and describe algorithms in original language. Test imports preserve upstream licenses and revision metadata.
