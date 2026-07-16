# 07 — Network, Storage, Media, and Platform Services

## 1. Network service principles

The network service is a privileged broker with less semantic trust than the kernel. It may own sockets and caches, but it does not decide a renderer’s origin, profile, user activation, permission, or navigation authority.

Every request carries an immutable context issued or validated by the kernel:

- profile and private-session identity;
- requesting process/frame/document epoch;
- requesting origin and top-level site;
- network partition key;
- destination and request mode;
- credentials mode;
- redirect mode and navigation/download classification;
- referrer policy and client hints policy;
- service-worker controller identity;
- user activation or agent grant reference when relevant;
- priority, deadline, byte budget, and cancellation token.

Renderers provide request intent and body streams. The service computes cookies, authorization eligibility, proxy route, cache key, CORS/preflight behavior, referrer, security headers, and connection reuse.

## 2. Protocol roadmap

### Network N0

- URL parsing through Turing-owned standard behavior;
- DNS abstraction, direct connections, HTTP/1.1, TLS, certificate verification, redirects, decompression, basic cache, cookies, and Fetch subset;
- proxy configuration and offline/error behavior;
- deterministic test server and packet/transaction trace format.

### Network N1

- HTTP/2, connection pooling, prioritization, authentication, range requests, resumable downloads, cache revalidation, CSP/CORS/CORP/COOP/COEP, HSTS, SRI, mixed-content policy, service-worker interception, and partitioning.

### Network N2

- HTTP/3/QUIC, Alt-Svc, WebSocket, server-sent events, WebTransport track, private-network access policy, certificate revocation strategy, enterprise roots/proxies, captive portals, and platform network changes.

Protocol libraries may be used, but Turing owns browser semantics, context propagation, partitioning, security policy, logging redaction, and resource accounting.

## 3. URL and origin handling

A single reviewed implementation defines URL parsing/serialization, special schemes, file/blob/data/about handling, percent encoding, host parsing, IDNA integration, default ports, origin computation, site computation, opaque origins, and trustworthy-origin decisions. No subsystem parses security-relevant URLs with general-purpose string or path utilities.

`file:` access is disabled or highly restricted in early builds. Local-file navigation never grants broad directory access. Blob URLs are scoped to their environment and revoked on lifecycle changes as specified.

## 4. TLS and certificates

Turing uses audited TLS and cryptographic implementations. It never creates custom ciphers, signature schemes, random-number generators, or certificate validation.

The certificate layer supports:

- platform or bundled root strategy documented per platform;
- hostname, validity, key usage, algorithm, chain, and policy validation;
- HSTS and secure-context integration;
- user/enterprise roots where supported;
- client certificates through a privileged chooser and keychain broker;
- certificate error pages that do not permit silent agent bypass;
- pinning only for Turing-owned update/service endpoints where operationally justified;
- rapid distrust and minimum-version updates independent from major releases.

Secret keys remain in OS-backed stores or hardware modules and are referenced by handles.

## 5. HTTP cache and connection reuse

Cache keys include profile, partition key, URL, method, relevant request headers, Vary behavior, credentials context, and response policy. Cache metadata is treated as untrusted serialized input. Bodies are content-addressed where useful, integrity-checked, quota-bound, and evicted by policy.

Connection coalescing is allowed only when certificate, origin, proxy, privacy, and network-partition constraints match. Preconnect and speculative fetch are budgeted and disabled or reduced under data-saver, battery, background, private, and agent policies.

## 6. Cookies and state

The cookie store implements domain/path matching, secure/http-only/same-site rules, prefixes, expiration, partitioning, size/count limits, public-suffix checks, and clear-site-data semantics. Renderers never enumerate HttpOnly values. DevTools access is local, explicit, profile-scoped, and audited.

Third-party state policy is configurable and versioned. Privacy mitigations are not inserted as undocumented compatibility changes; each has a spec/behavior note, telemetry-free test plan, and user/enterprise controls where appropriate.

## 7. Storage architecture

### 7.1 Logical stores

- session storage: browsing-context-group scoped and primarily memory-resident;
- local storage: small synchronous API presented over a mirrored/transactional service model with strict quotas;
- IndexedDB: transactional structured data, indexes, cursors, version changes, and structured clone;
- Cache Storage: request/response objects with body streams and quota accounting;
- service-worker registrations and scripts;
- origin-private file storage through logical handles;
- cookie and permission databases;
- history, bookmarks, downloads, credentials metadata, settings, extensions, and session journals as separate stores.

### 7.2 Isolation keys

All web storage is keyed by profile and origin, with top-level-site or other partition dimensions where policy requires. Opaque origins receive ephemeral or denied storage according to API semantics. Private sessions use separate ephemeral roots and keys.

### 7.3 Quota and eviction

Quota is enforced before allocation and after actual disk growth. The quota manager understands per-origin, per-site, per-profile, and global limits; persistent grants; recency; user importance; active service workers; and data-loss risk. Eviction is transactional and emits diagnostics. User-created downloads and explicit file handles are not silently treated as evictable web cache.

### 7.4 Durability and corruption

Databases use checksums, journaling/WAL where appropriate, schema versions, transactional migrations, interrupted-write tests, and backup/repair policy. A corrupt origin store is quarantined without deleting unrelated profile data. Browser startup does not block indefinitely on large repair work.

## 8. Service workers and offline behavior

Service-worker execution uses dedicated worker processes or renderer-class sandboxes with origin/site assignment. Registration, update, activation, fetch interception, lifecycle, cache access, push, background sync, and notification capabilities are separately permissioned and scheduled.

Workers do not stay resident indefinitely. The service persists versioned state, wakes workers for bounded events, and terminates idle instances. Resource usage is attributed to the responsible origin and visible in diagnostics.

Agent requests are not invisibly intercepted with broader credentials than the current policy permits. Agent-originated navigations and fetches carry explicit initiator metadata through service-worker dispatch.

## 9. Downloads and local files

The download broker owns destination selection, filename sanitization, temporary files, resume metadata, quarantine/mark-of-the-web integration, content-disposition handling, danger classification hooks, and opening/revealing files. A renderer receives status, not arbitrary write handles.

Rules:

- path separators, reserved names, Unicode confusion, trailing characters, extensions, and collisions are normalized safely;
- automatic downloads are origin- and gesture-limited;
- agents cannot choose hidden paths or auto-open dangerous files;
- completed files are not executed by Turing;
- opening external handlers requires user-visible intent and policy;
- private-session download behavior is explicit and does not claim files vanish when the user saved them.

## 10. Credentials, autofill, and passkeys

Credential secrets are accessed through a privileged credential broker and OS keychain. Page renderers receive fill operations or opaque handles, not a database dump. Fill policy binds credentials to canonical origins and form context. Password-field values are excluded from accessibility-agent snapshots, logs, crash reports, and remote diagnostics.

Passkeys/WebAuthn use platform authenticators and CTAP integrations through a broker. User presence/verification prompts cannot be satisfied by a model. Cross-origin iframe and related-origin behavior follow explicit policy and tests.

Payment and identity APIs are later tracks requiring separate threat models.

## 11. Image, font, PDF, and archive utilities

Parsers and decoders for images, fonts, PDFs, compressed archives, and document previews run in narrow sandboxes with:

- input/output byte caps;
- dimension, object-count, recursion, frame, duration, and CPU budgets;
- no network access unless explicitly required by a reviewed protocol;
- no arbitrary filesystem access;
- immutable shared-memory output where possible;
- cancellation and kill-on-timeout;
- fuzzing with upstream and Turing corpora.

PDF is treated as a subproduct: parser, renderer, forms, links, search, selection, accessibility, printing, downloads, scripts policy, and embedded attachments. Early versions may use a separately sandboxed audited PDF library, disclosed as a dependency.

## 12. Media pipeline

A media pipeline contains demux, decode, audio processing, video frames, synchronization, controls, captions, tracks, encrypted-media boundary, capture, and hardware acceleration. Turing owns HTML media semantics and security policy but may use OS codecs or audited codec libraries.

Media requirements:

- codec support matrix per platform and license;
- sandboxed demux/decode;
- protected-content paths isolated from page pixels and agents;
- autoplay and background policy;
- visible camera/microphone/screen-capture indicators;
- device labels withheld before permission;
- audio focus and media session integration;
- GPU/CPU frame accounting and zero-copy paths only with validated ownership;
- robust recovery from decoder and device failures.

DRM cannot be promised without licensed content-decryption modules and distribution agreements. The gap remains explicit.

## 13. Printing

Printing is mediated by a print service. The renderer produces paginated, validated print content; native dialogs and spooler access remain outside the renderer. Print preview, CSS paged media, headers/footers, backgrounds, scaling, paper sizes, accessibility, PDF output, and enterprise policy are tested independently. Agents cannot print without a visible confirmation policy.

## 14. Platform integration

### macOS

- App Sandbox/seatbelt profiles, hardened runtime, code signing/notarization, Keychain, Accessibility, CoreText, Metal, AVFoundation, print panels, notifications, and default-browser registration.

### Windows

- AppContainer or equivalent sandbox tokens, job objects, mitigations, UI Automation, DirectWrite, D3D12, Media Foundation, Credential Manager, SmartScreen/mark-of-the-web integration, printing, signing, and default-app registration.

### Linux

- namespaces, seccomp-bpf, Landlock where available, portals, Wayland with X11 compatibility policy, AT-SPI, fontconfig/FreeType, Vulkan/OpenGL strategy, PipeWire, Secret Service, distribution packaging, and update-policy variants.

Platform capability differences are documented. A weaker sandbox on one platform is not hidden behind a generic “sandboxed” badge.

## 15. Privacy and telemetry

Local diagnostics are rich. Remote telemetry is minimal, off by default in research/developer phases, schema-documented, and separated from page content. Collection categories have retention, purpose, sampling, and deletion rules. URLs, titles, search terms, page text, cookies, headers, credentials, file paths, form values, prompt content, and model outputs are excluded unless a separate explicit diagnostic flow states exactly what will be sent.

No advertising identifier, cross-product tracking SDK, or hidden analytics dependency is accepted.

<!-- MARKET-STRATEGY-2026-07 -->
## Market-driven service research

Identity routing, open migration/export, Time Machine, selective sync, collaboration, and privacy receipts create new network/storage obligations. Research must cover partitioning, credentials, journals, encryption, metadata leakage, conflict resolution, clearing, downgrade, and recovery before product acceptance.
