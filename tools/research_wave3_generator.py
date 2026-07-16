#!/usr/bin/env python3
"""Generate the third Turing browser research-library expansion.

This is a one-shot documentation publisher. It changes research and design
material only. It does not change implementation, requirements, risks, ADR
status, work-package status, or supported-feature claims.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLUEPRINT = DOCS / "blueprint-v1"
RESEARCH = DOCS / "research"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = content.strip() + "\n"
    if "\r" in normalized:
        raise ValueError(f"CR line ending in generated content: {path}")
    path.write_text(normalized, encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def replace_heading_section(path: Path, start: str, end: str, replacement: str) -> None:
    text = read(path)
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    text = text[:start_index] + replacement.rstrip() + "\n\n" + text[end_index:]
    write(path, text)


def append_once(path: Path, marker: str, content: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + content.strip() + "\n")


def insert_before(path: Path, marker: str, content: str, identity: str) -> None:
    text = read(path)
    if identity in text:
        return
    index = text.index(marker)
    write(path, text[:index].rstrip() + "\n\n" + content.strip() + "\n\n" + text[index:])


EXISTING_BOOKS: dict[str, list[str]] = {
    "engine": [
        "01-pipeline-and-artifacts.md", "02-html-parser-and-dom.md",
        "03-css-cascade-and-invalidation.md", "04-layout-and-fragmentation.md",
        "05-paint-compositor-and-gpu.md", "06-text-fonts-and-i18n.md",
        "07-images-media-svg-and-canvas.md", "08-input-editing-accessibility.md",
        "09-memory-data-structures-and-observability.md", "README.md",
    ],
    "javascript": [
        "01-front-end-bytecode-interpreter.md",
        "02-values-objects-shapes-and-inline-caches.md",
        "03-garbage-collection-and-host-lifetimes.md",
        "04-jit-tiering-ir-and-deoptimization.md",
        "05-webassembly-webidl-and-event-loop.md",
        "06-runtime-security-testing-and-performance.md", "README.md",
    ],
    "security-engine": [
        "01-threat-model-and-process-isolation.md",
        "02-sandbox-brokers-and-platform-containment.md",
        "03-memory-safety-jit-and-exploit-hardening.md",
        "04-web-security-privacy-and-trusted-ui.md",
        "05-update-supply-chain-and-vulnerability-response.md",
        "06-security-verification-and-release-gates.md", "README.md",
    ],
    "developer-experience": [
        "01-protocol-architecture-and-versioning.md",
        "02-devtools-workflows-and-ui.md",
        "03-observability-tracing-and-replay.md",
        "04-automation-headless-and-reproducibility.md",
        "05-debugging-memory-performance-and-security.md", "README.md",
    ],
    "api-design": [
        "01-design-principles.md", "02-async-streaming-and-cancellation.md",
        "03-schemas-errors-versioning-and-compatibility.md",
        "04-sdk-generation-authentication-and-redaction.md", "README.md",
    ],
    "performance": [
        "01-performance-model-and-critical-path.md",
        "02-memory-allocation-and-cache-policy.md",
        "03-scheduler-parallelism-and-latency.md",
        "04-graphics-energy-startup-and-recovery.md",
        "05-benchmarks-statistics-and-regression-governance.md", "README.md",
    ],
    "ai": [
        "01-agent-architecture-and-trust-boundaries.md",
        "02-semantic-observations-and-redaction.md",
        "03-actions-grants-confirmation-and-audit.md",
        "04-memory-planning-multi-agent-and-lifecycle.md",
        "05-providers-local-models-mcp-and-tools.md",
        "06-evaluation-safety-performance-and-usability.md", "README.md",
    ],
    "competitive": [
        "01-chromium-blink-v8.md", "02-webkit-javascriptcore.md",
        "03-gecko-spidermonkey.md", "04-servo.md", "05-ladybird.md",
        "06-browser-products.md", "07-comparison-scorecard-and-adoption-rules.md",
        "README.md",
    ],
}

BOOKS = {
    "networking": {
        "title": "Networking Engineering",
        "owner": "networking, Fetch, and transport engineering",
        "canonical": "../blueprint-v1/07-network-storage-media.md",
        "description": "Request identity, the network service, DNS, proxies, TLS, HTTP, Fetch policy, caches, cookies, streaming transports, downloads, diagnostics, testing, and resource budgets.",
        "thesis": "The renderer never owns ambient socket authority. One brokered network service carries kernel-issued profile, site, origin, frame, destination, credential, partition, and document-epoch identity through every redirect and policy decision.",
        "sources": [
            "https://fetch.spec.whatwg.org/", "https://url.spec.whatwg.org/",
            "https://www.rfc-editor.org/rfc/rfc9110", "https://www.rfc-editor.org/rfc/rfc9113",
            "https://www.rfc-editor.org/rfc/rfc9114", "https://www.rfc-editor.org/rfc/rfc9000",
            "https://www.rfc-editor.org/rfc/rfc8446", "https://w3c.github.io/webtransport/",
        ],
        "chapters": [
            ("01-identities-and-request-context.md", "Identity and Request Context", "URL, origin, site, profile, frame, destination, credentials mode, storage partition, navigation ID, document epoch, redirect provenance, and policy reason codes"),
            ("02-network-service-and-brokers.md", "Network Service and Capability Brokers", "separate-process socket authority, typed IPC, request handles, connection ownership, cancellation, backpressure, renderer compromise, and broker restart"),
            ("03-dns-proxies-and-connection-racing.md", "DNS, Proxies, and Connection Racing", "resolver isolation, encrypted DNS policy, proxy/PAC containment, Happy Eyeballs, connection pools, network changes, captive portals, and privacy boundaries"),
            ("04-tls-certificates-and-client-auth.md", "TLS, Certificates, and Client Authentication", "TLS 1.3, certificate paths, revocation signals, CT, client certificates, key brokers, interstitials, pinning policy, session resumption, and incident controls"),
            ("05-http1-http2-http3-and-quic.md", "HTTP/1.1, HTTP/2, HTTP/3, and QUIC", "framing, compression, prioritization, multiplexing, connection coalescing, migration, 0-RTT risk, flow control, resource limits, and protocol fallback"),
            ("06-fetch-redirects-cors-and-security-policy.md", "Fetch, Redirects, CORS, and Security Policy", "request/response algorithms, redirects, mixed content, CORS, CSP, CORP, COOP, COEP, MIME, SRI, referrers, and service-worker interception"),
            ("07-cache-preload-speculation-and-service-workers.md", "Caching, Preload, Speculation, and Service Workers", "HTTP cache keys, validators, freshness, preload scanners, speculative work, partitioning, offline behavior, navigation preload, and cache poisoning defenses"),
            ("08-cookies-partitioning-and-tracking-resistance.md", "Cookies, Partitioning, and Tracking Resistance", "cookie parsing, SameSite, prefixes, partitioned cookies, top-level-site keys, storage access, expiry, quotas, tracking protection, compatibility, and clearing"),
            ("09-streaming-websocket-webtransport-and-downloads.md", "Streaming, WebSocket, WebTransport, and Downloads", "streaming bodies, upload/download backpressure, WebSocket, datagrams, WebTransport, range requests, resumability, content disposition, safe destinations, and cancellation"),
            ("10-observability-testing-and-resource-budgets.md", "Networking Observability, Testing, and Resource Budgets", "causal request traces, policy explanations, packet-independent diagnostics, hermetic servers, fault injection, fuzzing, connection/buffer budgets, wakeups, energy, and release gates"),
        ],
    },
    "storage": {
        "title": "Storage and Recovery Engineering",
        "owner": "storage, profile data, migration, and recovery engineering",
        "canonical": "../blueprint-v1/07-network-storage-media.md",
        "description": "Storage keys, quotas, IndexedDB, Cache Storage, service workers, cookies, profile stores, migrations, corruption, encryption boundaries, clearing, repair, and recovery.",
        "thesis": "Persistent data is an untrusted, versioned, partitioned system. Every store needs an explicit key, owner, quota, transaction model, durability level, migration path, corruption behavior, deletion contract, and recovery tool.",
        "sources": [
            "https://storage.spec.whatwg.org/", "https://w3c.github.io/IndexedDB/",
            "https://w3c.github.io/ServiceWorker/", "https://sqlite.org/",
            "https://w3c.github.io/webappsec-clear-site-data/",
        ],
        "chapters": [
            ("01-storage-keys-buckets-and-partitioning.md", "Storage Keys, Buckets, and Partitioning", "profile, origin, top-level site, agent cluster, private session, bucket identity, opaque origins, file schemes, quotas, and cross-process handles"),
            ("02-quota-eviction-and-pressure.md", "Quota, Eviction, and Pressure", "admission, per-owner charges, persistent versus best-effort storage, global pressure, eviction order, user visibility, protection, fairness, and denial-of-service limits"),
            ("03-indexeddb-transactions-and-durability.md", "IndexedDB Transactions and Durability", "schemas, object stores, indexes, transactions, locking, structured clone, blobs, version changes, crash atomicity, durability modes, and conformance"),
            ("04-cache-storage-service-workers-and-background-work.md", "Cache Storage, Service Workers, and Background Work", "cache request matching, service-worker registrations, update lifecycle, background tasks, partitioning, offline behavior, quotas, and process restart"),
            ("05-cookies-sessions-and-private-data.md", "Cookies, Sessions, and Private Data", "cookie-store interaction, session-only state, private-session isolation, deletion at close, crash remnants, credential separation, and diagnostic redaction"),
            ("06-profile-history-bookmarks-settings-and-journals.md", "Profile Stores, History, Bookmarks, Settings, and Journals", "store separation, append journals, indexes, lazy loading, sync hooks, session restore, backups, user export, and startup cost"),
            ("07-migrations-corruption-disk-full-and-power-loss.md", "Migrations, Corruption, Disk Full, and Power Loss", "transactional migrations, interruption, checksums, old/new version negotiation, downgrade protection, disk exhaustion, partial writes, repair, and quarantine"),
            ("08-encryption-credentials-clearing-and-export.md", "Encryption Boundaries, Credentials, Clearing, and Export", "OS key stores, envelope encryption, profile secrets, Clear-Site-Data, selective deletion, secure erase limitations, export manifests, and account removal"),
            ("09-observability-repair-and-testing.md", "Storage Observability, Repair, and Testing", "transaction traces, quota attribution, migration evidence, corruption injection, recovery drills, redacted diagnostics, long-run tests, and release gates"),
        ],
    },
    "media-documents": {
        "title": "Media, Documents, and Printing Engineering",
        "owner": "media, document, codec, and printing engineering",
        "canonical": "../blueprint-v1/07-network-storage-media.md",
        "description": "Sandboxed decoders, images, fonts, audio/video, WebRTC, capture, codecs, hardware acceleration, DRM, PDF, printing, accessibility, licensing, testing, and energy.",
        "thesis": "Media and document formats combine hostile parsing, large allocations, hardware drivers, privacy-sensitive devices, licensing constraints, and long-lived playback state. They require process isolation, strict limits, capability mediation, and explicit distribution matrices.",
        "sources": [
            "https://www.w3.org/TR/webcodecs/", "https://w3c.github.io/media-source/",
            "https://w3c.github.io/webrtc-pc/", "https://www.w3.org/TR/encrypted-media/",
            "https://www.w3.org/TR/png-3/", "https://aomedia.org/av1-features/",
            "https://pdfa.org/resource/",
        ],
        "chapters": [
            ("01-decoder-processes-and-input-limits.md", "Decoder Processes and Input Limits", "format sniffing, metadata-before-allocation, dimension/frame/duration limits, cancellation, isolated utilities, immutable outputs, fuzzing, and crash recovery"),
            ("02-images-fonts-color-and-animation.md", "Images, Fonts, Color, and Animation", "PNG/JPEG/WebP/AVIF/GIF, font containers, color spaces, HDR, orientation, animated images, target-size decoding, caches, privacy, and fallback"),
            ("03-audio-video-clocks-buffering-and-seeking.md", "Audio/Video Clocks, Buffering, and Seeking", "demux, decode, playback clocks, A/V synchronization, seeking, buffering, adaptive playback, subtitles, media sessions, background policy, and recovery"),
            ("04-webrtc-capture-and-devices.md", "WebRTC, Capture, and Devices", "camera, microphone, display capture, device identity, permission grants, indicators, ICE/DTLS/SRTP boundaries, echo processing, privacy, and cancellation"),
            ("05-codecs-hardware-acceleration-and-licensing.md", "Codecs, Hardware Acceleration, and Licensing", "capability discovery, software/hardware paths, driver processes, fallback, patent/royalty matrices, territories, optional components, and support claims"),
            ("06-drm-and-content-decryption-boundaries.md", "DRM and Content-Decryption Boundaries", "EME semantics, CDM approval, protected surfaces, license sessions, output protection, storage, sandboxing, audit, unsupported services, and no-bypass policy"),
            ("07-pdf-viewer-and-document-security.md", "PDF Viewer and Document Security", "PDF parsing, incremental loading, fonts, forms, annotations, scripts, links, attachments, accessibility, printing, sandboxing, limits, and malformed files"),
            ("08-printing-pagination-accessibility-and-quality.md", "Printing, Pagination, Accessibility, and Quality", "print CSS, fragmentation, preview, platform spoolers, page setup, color, PDF output, accessible documents, cancellation, privacy, and cross-platform tests"),
        ],
    },
    "platform": {
        "title": "Native Platform and Browser Chrome Engineering",
        "owner": "browser shell and platform integration engineering",
        "canonical": "../blueprint-v1/11-product-ui-devtools.md",
        "description": "Browser chrome, windows, surfaces, input, IME, clipboard, drag-and-drop, macOS, Windows, Linux, credentials, notifications, external protocols, packaging, startup, power, and support evidence.",
        "thesis": "Essential browser controls remain independent from web rendering and responsive during renderer failure. Platform adapters are thin, capability-aware, accessible, measured, and explicit about unavoidable operating-system differences.",
        "sources": [
            "https://developer.apple.com/documentation/appkit", "https://learn.microsoft.com/en-us/windows/apps/",
            "https://wayland.freedesktop.org/", "https://flatpak.github.io/xdg-desktop-portal/",
            "https://developer.apple.com/accessibility/", "https://learn.microsoft.com/en-us/windows/apps/design/accessibility/",
        ],
        "chapters": [
            ("01-browser-chrome-scene-graph-and-trusted-surfaces.md", "Browser Chrome Scene Graph and Trusted Surfaces", "retained UI artifacts, typography, controls, command model, hit testing, accessibility semantics, trusted prompts, renderer independence, animation, and GPU/software paths"),
            ("02-windows-surfaces-displays-and-lifecycle.md", "Windows, Surfaces, Displays, and Lifecycle", "multi-window state, tabs, scale factors, color/HDR, refresh rates, fullscreen, occlusion, display changes, surface loss, minimize/restore, and crash recovery"),
            ("03-input-ime-clipboard-and-drag-drop.md", "Input, IME, Clipboard, and Drag-and-Drop", "keyboard, pointer, touch, pen, gestures, composition, text services, selection, clipboard formats, sanitization, drag data, file grants, and accessibility"),
            ("04-macos-integration.md", "macOS Integration", "AppKit windows, menus, text input, accessibility, Keychain, App Sandbox, Hardened Runtime, JIT entitlements, capture, notifications, signing, and notarization"),
            ("05-windows-integration.md", "Windows Integration", "Win32/Windows App SDK, DirectComposition, input, UI Automation, Credential Manager, AppContainer, process mitigations, notifications, installers, and signing"),
            ("06-linux-integration.md", "Linux Integration", "Wayland/X11 transition, input methods, AT-SPI, portals, PipeWire, namespaces, seccomp, Landlock, desktop integration, packaging, and distribution variance"),
            ("07-credentials-notifications-and-external-protocols.md", "Credentials, Notifications, and External Protocols", "credential brokers, passkeys, system notifications, file/device pickers, default browser registration, external handlers, origin display, confirmation, and revocation"),
            ("08-packaging-startup-power-and-support-matrix.md", "Packaging, Startup, Power, and Support Matrix", "install layout, shared resources, process launch, warm pools, low-power mode, sleep/resume, thermal pressure, updates, diagnostics, minimum OS versions, and evidence"),
        ],
    },
    "accessibility": {
        "title": "Accessibility Engineering",
        "owner": "accessibility architecture and assistive-technology engineering",
        "canonical": "../blueprint-v1/11-product-ui-devtools.md",
        "description": "Engine semantics, accessible names, text ranges, cross-process trees, platform bridges, browser UI, DevTools, automation, agents, latency, testing, and release gates.",
        "thesis": "Accessibility is a first-class semantic output and interaction path. It is built with DOM, layout, editing, browser chrome, automation, and agent observations—not reconstructed after pixels exist.",
        "sources": [
            "https://www.w3.org/TR/wai-aria/", "https://www.w3.org/TR/accname-1.2/",
            "https://www.w3.org/TR/WCAG22/", "https://developer.apple.com/accessibility/",
            "https://learn.microsoft.com/en-us/windows/apps/design/accessibility/",
            "https://gitlab.gnome.org/GNOME/at-spi2-core",
        ],
        "chapters": [
            ("01-engine-semantics-and-tree-generation.md", "Engine Semantics and Accessibility-Tree Generation", "roles, states, properties, relationships, hidden/inert policy, generated content, shadow DOM, forms, SVG, canvas fallback, mutation epochs, and ownership"),
            ("02-names-relations-text-ranges-and-editing.md", "Names, Relations, Text Ranges, and Editing", "accessible-name computation, descriptions, labels, tables, text offsets, selection, caret, composition, spelling, live regions, validation, and actions"),
            ("03-cross-process-and-cross-origin-composition.md", "Cross-Process and Cross-Origin Composition", "remote frame trees, stable node IDs, epochs, bounds, events, process crashes, site isolation, cross-origin disclosure, focus, and recovery"),
            ("04-platform-accessibility-bridges.md", "Platform Accessibility Bridges", "AX, UI Automation, AT-SPI, role/state mappings, actions, text APIs, event coalescing, threading, cache lifetime, platform variance, and diagnostics"),
            ("05-browser-ui-devtools-automation-and-agents.md", "Browser UI, DevTools, Automation, and Agents", "address bar, tabs, permissions, downloads, DevTools, resource manager, agent confirmations, WebDriver accessibility locators, semantic snapshots, and trusted controls"),
            ("06-latency-event-coalescing-and-resource-use.md", "Accessibility Latency, Event Coalescing, and Resource Use", "input-to-announcement latency, tree update deadlines, event storms, batching, stale data, memory charges, screen-reader polling, background pages, and performance gates"),
            ("07-testing-assistive-technology-matrices-and-release-gates.md", "Testing, Assistive-Technology Matrices, and Release Gates", "automated semantics, keyboard/focus, zoom, contrast, motion, VoiceOver, Narrator, NVDA, Orca, regression artifacts, manual workflows, and release blockers"),
        ],
    },
    "release-operations": {
        "title": "Build, Release, Update, and Incident Operations Engineering",
        "owner": "build, release, update, and security operations",
        "canonical": "../blueprint-v1/13-build-release-operations.md",
        "description": "Build identity, hermetic toolchains, reproducibility, provenance, SBOMs, signing, packaging, updates, rollout, rollback, migrations, crash reporting, incident response, and support lifecycle.",
        "thesis": "A browser is only as secure as its ability to reproduce, sign, distribute, update, diagnose, and rapidly patch every supported build. Operational readiness is a release feature, not post-launch administration.",
        "sources": [
            "https://reproducible-builds.org/", "https://slsa.dev/", "https://in-toto.io/",
            "https://theupdateframework.io/", "https://www.sigstore.dev/",
            "https://spdx.dev/", "https://cyclonedx.org/",
        ],
        "chapters": [
            ("01-build-identity-and-hermetic-toolchains.md", "Build Identity and Hermetic Toolchains", "source commit, compiler/SDK versions, flags, generated inputs, locale/time, network isolation, deterministic environments, build IDs, symbols, and artifact manifests"),
            ("02-reproducible-builds-provenance-and-sbom.md", "Reproducible Builds, Provenance, and SBOM", "bit-for-bit or independently verifiable builds, provenance attestations, dependency graphs, licenses, native blobs, unsafe inventory, verification parties, and exceptions"),
            ("03-signing-keys-and-package-attestation.md", "Signing Keys and Package Attestation", "hardware-backed keys, threshold control, role separation, short-lived credentials, audit, revocation, emergency rotation, timestamping, package signatures, and compromise drills"),
            ("04-platform-packaging-and-installers.md", "Platform Packaging and Installers", "macOS bundles/notarization, Windows installers/signing, Linux packages/sandboxes, permissions, paths, repair, uninstall, enterprise deployment, and channel separation"),
            ("05-update-metadata-rollout-and-rollback.md", "Update Metadata, Rollout, and Rollback", "signed targets, version/channel/platform/architecture, hashes, expiry, mirrors, staged rollout, health gates, pause, rollback, minimum secure version, and partial installs"),
            ("06-profile-migrations-and-downgrade-protection.md", "Profile Migrations and Downgrade Protection", "schema versions, transactional migration, interruption, compatibility windows, backups, restore, rollback, old-version refusal, channel switches, and user recovery"),
            ("07-crash-reporting-symbols-and-redaction.md", "Crash Reporting, Symbols, and Redaction", "local crash records, symbol servers, minidumps, sensitive-memory exclusion, user consent, diagnostic previews, deduplication, retention, export, and issue correlation"),
            ("08-vulnerability-response-and-supported-lifecycle.md", "Vulnerability Response and Supported Lifecycle", "private intake, severity, embargoes, patch branches, emergency builds, CVEs, coordinated disclosure, on-call ownership, supported versions, EOL, drills, and postmortems"),
        ],
    },
    "extensions-enterprise": {
        "title": "Extensions, Enterprise Policy, Accounts, and Sync Engineering",
        "owner": "extension, enterprise, account, and sync engineering",
        "canonical": "../blueprint-v1/02-capability-parity.md",
        "description": "Extension processes, worlds, grants, event execution, rules, native messaging, updates, DevTools and agents, enterprise policy, accounts, encrypted sync, conflicts, schemas, and quotas.",
        "thesis": "Ecosystem compatibility cannot recreate ambient authority, persistent background waste, or profile-wide data access. Extensions, enterprise controls, accounts, and sync are separate principals with explicit policy and resource contracts.",
        "sources": [
            "https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions",
            "https://wicg.github.io/webextensions/", "https://www.rfc-editor.org/rfc/rfc7516",
            "https://www.rfc-editor.org/rfc/rfc5869",
        ],
        "chapters": [
            ("01-extension-processes-worlds-and-isolation.md", "Extension Processes, Worlds, and Isolation", "extension identities, service processes, content-script worlds, frames, profiles/private sessions, IPC, internal pages, renderer compromise, and crash recovery"),
            ("02-permissions-host-grants-and-user-control.md", "Permissions, Host Grants, and User Control", "declared/optional permissions, site-specific host access, one-time grants, activeTab-like gestures, private-profile separation, review UI, revocation, and audit"),
            ("03-event-driven-background-work-and-quotas.md", "Event-Driven Background Work and Quotas", "service-worker-like lifetime, events, alarms, messaging, storage, CPU/wakeup/network budgets, cancellation, suspension, missed events, and observability"),
            ("04-declarative-network-rules-and-native-messaging.md", "Declarative Network Rules and Native Messaging", "bounded rules, precedence, privacy, performance, conflicts, host-process allowlists, installation provenance, message schemas, user visibility, and enterprise policy"),
            ("05-extension-updates-devtools-and-agents.md", "Extension Updates, DevTools, and Agents", "signing, store/developer installation, update rollback, DevTools extensions, agent/tool interaction, delegated grants, protocol boundaries, diagnostics, and incident response"),
            ("06-enterprise-policy-precedence-and-audit.md", "Enterprise Policy Precedence and Audit", "machine/user/cloud policy, schema validation, precedence, locked versus recommended settings, origin lists, certificates, extensions, updates, logging, privacy, and explainability"),
            ("07-accounts-sync-encryption-conflicts-and-quotas.md", "Accounts, Sync, Encryption, Conflicts, and Quotas", "profile-bound accounts, auth brokers, encrypted envelopes, key recovery, data-type selection, versioned schemas, conflict resolution, deletion, throttling, and unsupported services"),
        ],
    },
    "web-platform": {
        "title": "Open Web Platform Governance Engineering",
        "owner": "web-platform standards and interoperability",
        "canonical": "../blueprint-v1/12-testing-compatibility.md",
        "description": "User needs, standards participation, feature lifecycle, dependency graphs, tests, interoperability, privacy/security/accessibility review, experiments, deprecation, compatibility interventions, and evidence dashboards.",
        "thesis": "Turing should not become a private web platform. New behavior starts with user or developer need, interoperable specification work, tests, abuse review, feature detection, and a credible multi-implementer path.",
        "sources": [
            "https://whatwg.org/working-mode", "https://www.w3.org/TR/design-principles/",
            "https://www.w3.org/TR/ethical-web-principles/", "https://web-platform-tests.org/",
            "https://wpt.fyi/interop",
        ],
        "chapters": [
            ("01-user-needs-and-design-principles.md", "User Needs and Design Principles", "user control, safety, privacy, accessibility, interoperability, predictable failure, feature detection, progressive enhancement, trusted UI, and implementation restraint"),
            ("02-feature-lifecycle-and-standards-participation.md", "Feature Lifecycle and Standards Participation", "problem statement, use cases, implementer interest, specification venue, explainer, prototypes, threat model, tests, standards feedback, and maturity labels"),
            ("03-tests-interop-and-dependency-graphs.md", "Tests, Interoperability, and Dependency Graphs", "normative algorithms, WPT directories, prerequisites, failure denominator, Interop focus areas, application dependencies, platform differences, and milestone ordering"),
            ("04-privacy-security-accessibility-and-abuse-review.md", "Privacy, Security, Accessibility, and Abuse Review", "data flows, identifiers, permissions, fingerprinting, cross-origin effects, user activation, trusted UI, accessible semantics, resource abuse, and mitigations"),
            ("05-experiments-deprecation-and-compatibility-interventions.md", "Experiments, Deprecation, and Compatibility Interventions", "namespaced APIs, flags, trials, telemetry minimization, expiry, rollback, warnings, migration, site interventions, public rationale, owners, and standards paths"),
            ("06-governance-evidence-and-public-dashboard.md", "Governance Evidence and Public Dashboard", "support tables, exact revisions, WPT pass/fail/crash/timeout, unsupported features, standards positions, interventions, issue links, stale-data dates, and claim expiry"),
        ],
    },
    "benchmark-lab": {
        "title": "Fixed-Hardware Benchmark Laboratory",
        "owner": "performance measurement and benchmark operations",
        "canonical": "../blueprint-v1/09-performance-memory.md",
        "description": "Hardware tiers, OS images, corpora, servers, startup, navigation, input, frame pacing, memory, process topology, 30 tabs, energy, accessibility, developer, agent, recovery, statistics, artifacts, and claims.",
        "thesis": "A benchmark result is a versioned experiment, not a screenshot. Every result binds workload, feature coverage, security configuration, process topology, lifecycle state, raw samples, uncertainty, failures, and recovery behavior.",
        "sources": [
            "https://browserbench.org/", "https://browserbench.org/Speedometer3.1/",
            "https://browserbench.org/MotionMark1.3/", "https://perfetto.dev/",
            "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/",
        ],
        "chapters": [
            ("01-hardware-os-power-and-thermal-control.md", "Hardware, OS, Power, and Thermal Control", "Tier L/M/H machines, firmware, drivers, OS images, background services, power plans, battery state, display settings, thermal soak, sensors, calibration, and replacement policy"),
            ("02-corpus-servers-and-network-control.md", "Corpus, Servers, and Network Control", "generated/legal pages, applications, international/a11y content, hostile cases, local HTTP/2/3/TLS/DNS, cache state, latency/loss/bandwidth, authentication mocks, and versioning"),
            ("03-startup-navigation-and-input-latency.md", "Startup, Navigation, and Input Latency", "cold/warm launch, address-bar readiness, process start, session enumeration, request stages, useful content, input-to-event/render/present, p50/p95/p99, and outliers"),
            ("04-frame-pacing-raster-composite-and-gpu.md", "Frame Pacing, Raster, Composite, and GPU", "60-240 Hz, scroll/animation, main/compositor dependencies, damage, raster queues, layer churn, GPU memory, device loss, software fallback, and power"),
            ("05-memory-process-topology-and-thirty-tabs.md", "Memory, Process Topology, and Thirty Tabs", "private/resident/committed/reserved/shared/compressed/swap/GPU memory, site isolation, process count, mixed/all-live tabs, protection, revival, lost state, and pressure"),
            ("06-energy-accessibility-developer-agent-and-recovery.md", "Energy, Accessibility, Developer, Agent, and Recovery Workloads", "idle/wakeups, scrolling/video, screen-reader latency, DevTools overhead, automation, local/remote AI, cancellation, crashes, restarts, updates, and thermal degradation"),
            ("07-statistics-artifacts-regressions-and-claims.md", "Statistics, Artifacts, Regressions, and Claims", "sample design, randomization, warmup, confidence intervals, practical thresholds, control charts, raw traces, manifests, failures, bisect, waivers, publication, and claim expiry"),
        ],
    },
    "quality-assurance": {
        "title": "Quality Assurance, Conformance, and Verification Engineering",
        "owner": "quality, conformance, fuzzing, and assurance engineering",
        "canonical": "../blueprint-v1/12-testing-compatibility.md",
        "description": "Conformance suites, reduced tests, fuzzing, property/model/formal methods, differential testing, fault injection, chaos, longevity, security assurance, independent review, flakes, and release evidence.",
        "thesis": "A browser cannot be validated by demos or pixel tests alone. Every subsystem needs the lowest-level semantic oracle, cross-boundary integration tests, adversarial inputs, resource failure, recovery, and a full accounting of unsupported cases.",
        "sources": [
            "https://web-platform-tests.org/", "https://github.com/tc39/test262",
            "https://rust-fuzz.github.io/book/", "https://llvm.org/docs/LibFuzzer.html",
            "https://aflplus.plus/",
        ],
        "chapters": [
            ("01-conformance-suites-and-reduced-tests.md", "Conformance Suites and Reduced Tests", "pinned WPT/Test262, metadata, full denominators, semantic traces, pixels/geometry, accessibility, network/storage/security behavior, minimization, and upstream contribution"),
            ("02-fuzzing-property-model-and-formal-methods.md", "Fuzzing, Property Tests, Model Tests, and Formal Methods", "coverage, grammars, structured mutation, invariants, state machines, protocol models, concurrency schedules, OOM, corpus governance, proofs, and practical scope"),
            ("03-differential-testing-and-oracles.md", "Differential Testing and Oracles", "multiple engines, normalized output, standard consultation, parser/runtime/layout/network/storage/accessibility comparison, disagreement classification, reduction, and no-majority correctness"),
            ("04-fault-injection-chaos-and-long-duration.md", "Fault Injection, Chaos, and Long-Duration Testing", "process termination, IPC delay/drop, network faults, disk full/corruption, GPU reset, clock/sleep, memory pressure, provider failures, days-long churn, leaks, hangs, and recovery"),
            ("05-security-assurance-and-independent-review.md", "Security Assurance and Independent Review", "compromised-renderer harnesses, sandbox negatives, site isolation, unsafe/native audits, supply chain, update attacks, red teams, independent scope, findings, retests, and disclosure"),
            ("06-flakes-release-evidence-and-go-no-go.md", "Flakes, Release Evidence, and Go/No-Go", "flake ownership/rates/expiry, no retry masking, artifact retention, requirement/gate status, failure counts, accessibility matrix, performance, risks, waivers, signed owners, and maturity labels"),
        ],
    },
    "product-experience": {
        "title": "Everyday Product Experience Engineering",
        "owner": "browser product, usability, and trusted interaction engineering",
        "canonical": "../blueprint-v1/11-product-ui-devtools.md",
        "description": "Tabs, groups, workspaces, command field, onboarding, migration, profiles, private sessions, permissions, credentials, agents, resource manager, lifecycle, recovery, settings, updates, support, usability, and accessibility.",
        "thesis": "Everyday quality is measured in fast, comprehensible, recoverable workflows. Minimalism removes hidden work and confusion; it does not hide security state, lifecycle state, data-loss risk, accessibility, or diagnostics.",
        "sources": [
            "https://www.w3.org/TR/WCAG22/", "https://www.w3.org/TR/design-principles/",
            "https://support.mozilla.org/", "https://support.google.com/chrome/",
            "https://support.apple.com/guide/safari/",
        ],
        "chapters": [
            ("01-tabs-groups-workspaces-and-command-field.md", "Tabs, Groups, Workspaces, and the Command Field", "horizontal/vertical tabs, search, recency, groups, workspaces, bulk actions, URL/search/command distinction, origin/profile state, shortcuts, 30-tab workflows, and latency"),
            ("02-onboarding-migration-profiles-and-private-sessions.md", "Onboarding, Migration, Profiles, and Private Sessions", "first run, default browser, import, selective migration, profile identity, account separation, private-state guarantees, disclosure, rollback, and accessibility"),
            ("03-permissions-credentials-agents-and-trusted-ux.md", "Permissions, Credentials, Agents, and Trusted UX", "origin-bound prompts, active indicators, page info, passkeys, autofill, downloads, external apps, agent confirmations, anti-spoofing, keyboard/screen-reader parity, and revocation"),
            ("04-resource-manager-lifecycle-and-recovery.md", "Resource Manager, Tab Lifecycle, and Recovery", "CPU/memory/GPU/network/energy attribution, process topology, protection reasons, freeze/discard/keep-active, data-loss warnings, crashes, safe mode, session restore, and issue export"),
            ("05-settings-updates-support-usability-and-accessibility.md", "Settings, Updates, Support, Usability, and Accessibility", "searchable settings, clear defaults, privacy controls, update status, EOL, diagnostics, support bundles, task studies, keyboard/AT workflows, localization, and claim evidence"),
        ],
    },
}

DEEPER = {
    "performance": {
        "canonical": "../blueprint-v1/09-performance-memory.md",
        "sources": ["https://perfetto.dev/", "https://llvm.org/docs/", "https://doc.rust-lang.org/cargo/reference/profiles.html"],
        "chapters": [
            ("06-data-locality-cpu-caches-and-numa.md", "Data Locality, CPU Caches, and NUMA", "hot/cold field separation, structure-of-arrays versus array-of-structures, compact handles, pointer chasing, cache lines, false sharing, prefetch, heterogeneous cores, NUMA placement, and corpus measurement"),
            ("07-allocators-virtual-memory-and-page-reclamation.md", "Allocators, Virtual Memory, and Page Reclamation", "arenas, slabs, size classes, fragmentation, live/reserved/committed/resident pages, huge pages, guard pages, working-set trimming, madvise-like release, lifecycle reclaim, and security"),
            ("08-ipc-shared-memory-serialization-and-batching.md", "IPC, Shared Memory, Serialization, and Batching", "message framing, copies, mappings, immutable buffers, validation, queue caps, backpressure, cancellation, priority, batching delay, cache coherency, accounting, and crash cleanup"),
            ("09-pgo-lto-binary-layout-and-startup.md", "PGO, LTO, Binary Layout, and Startup", "profile representativeness, thin/full LTO, code size, function ordering, hot/cold splitting, demand paging, relocations, dynamic libraries, preinitialization, reproducibility, and rollback"),
            ("10-causal-profiling-and-regression-diagnosis.md", "Causal Profiling and Regression Diagnosis", "stable event schemas, critical-path reconstruction, task causality, process clocks, queue wait, semantic memory owners, trace diffing, automated suspects, noise, bisect, and developer explanations"),
        ],
    },
    "security-engine": {
        "canonical": "../blueprint-v1/08-security-and-sandbox.md",
        "sources": ["https://spectreattack.com/spectre.pdf", "https://www.usenix.org/conference/usenixsecurity20/presentation/narayan", "https://llvm.org/docs/ControlFlowIntegrity.html"],
        "chapters": [
            ("07-speculation-timers-and-side-channels.md", "Speculation, Timers, and Side Channels", "Spectre-class threats, process/site isolation, cross-origin isolation, timer precision, shared resources, cache/storage partitions, JIT sequences, hardware mitigations, performance cost, and residual risk"),
            ("08-native-parser-and-codec-isolation.md", "Native Parser and Codec Isolation", "memory-unsafe libraries, utility processes, RLBox/Wasm-like compartments, SFI, capability imports, immutable outputs, copy cost, fuzzing, crash recovery, and dependency updates"),
            ("09-heap-sandboxes-pointer-tables-and-jit-compartments.md", "Heap Sandboxes, Pointer Tables, and JIT Compartments", "pointer compression, external pointer tables, cage boundaries, code/data separation, W^X, CFI/PAC/CET, trusted metadata, bounds checks, deoptimization, and exploit assumptions"),
            ("10-capability-provenance-attenuation-and-revocation.md", "Capability Provenance, Attenuation, and Revocation", "kernel-issued identities, derivation chains, scope, expiry, epochs, least authority, child grants, revocation, asynchronous revalidation, audit reason codes, formal state models, and tests"),
            ("11-developer-extension-automation-and-agent-attack-surfaces.md", "Developer, Extension, Automation, and Agent Attack Surfaces", "remote debugging, evaluation, normal profiles, extension worlds, native messaging, headless flags, model/tool input, prompt injection, confirmation, authentication, visibility, quotas, and incident disablement"),
            ("12-anti-phishing-reputation-and-trusted-ui.md", "Anti-Phishing, Reputation, Abuse Resistance, and Trusted UI", "origin display, IDN/lookalikes, permission fatigue, dangerous downloads, reputation providers, privacy, false positives, local/remote checks, bypass resistance, appeals, accessibility, and emergency updates"),
        ],
    },
    "developer-experience": {
        "canonical": "../blueprint-v1/11-product-ui-devtools.md",
        "sources": ["https://w3c.github.io/webdriver-bidi/", "https://chromedevtools.github.io/devtools-protocol/", "https://firefox-source-docs.mozilla.org/remote/"],
        "chapters": [
            ("06-deterministic-replay-virtual-time-and-state-capture.md", "Deterministic Replay, Virtual Time, and State Capture", "time/randomness/network fixtures, input streams, navigation, task ordering, service workers, storage snapshots, cross-origin policy, sensitive data, divergence detection, and isolated replay profiles"),
            ("07-source-maps-live-editing-and-local-development.md", "Source Maps, Live Editing, and Local Development", "source-map fidelity, modules/workers/Wasm, workspace handles, local overrides, hot reload, CSS editing, breakpoint migration, trust, file authority, rollback, and framework-neutral diagnostics"),
            ("08-diagnostic-bundles-and-automatic-reduction.md", "Diagnostic Bundles and Automatic Reduction", "environment manifests, redacted traces, crash IDs, screenshots/semantic trees, network/storage policy, source selection, reproducibility, delta reduction, minimization oracles, consent, and issue attachments"),
            ("09-generated-sdks-plugins-and-compatibility-adapters.md", "Generated SDKs, Plugins, and Compatibility Adapters", "canonical schemas, Rust/TypeScript/Python clients, capability negotiation, streaming/backpressure, typed errors, stable/experimental domains, plugin isolation, CDP adapters, version windows, and conformance"),
            ("10-integrated-accessibility-security-network-and-storage-debugging.md", "Integrated Accessibility, Security, Network, and Storage Debugging", "cross-domain causal views, accessible-name provenance, CORS/CSP decisions, cookie/cache partitions, storage transactions, process/capability topology, trusted prompts, redaction, explainability, and workflow studies"),
        ],
    },
}

ALL_BOOK_META = {
    "engine": ("Browser engine engineering", "Pipeline artifacts, HTML/DOM, CSS, invalidation, layout, paint, GPU, text, media, input, accessibility, memory, and observability"),
    "javascript": ("JavaScript runtime engineering", "Front end, bytecode, interpreter, values, objects, inline caches, GC, JIT, Web IDL, event loop, WebAssembly, testing, and performance"),
    "security-engine": ("Browser security engineering", "Threat model, isolation, sandbox brokers, native/JIT hardening, side channels, trusted UI, updates, and assurance"),
    "developer-experience": ("Developer experience and DevTools", "Protocols, workflows, causal tracing, replay, automation, SDKs, reduction, and integrated diagnosis"),
    "api-design": ("API design", "Identity, authority, bounds, async work, streaming, cancellation, schemas, errors, compatibility, SDKs, authentication, and redaction"),
    "performance": ("Performance engineering", "Critical paths, locality, allocation, virtual memory, IPC, scheduling, graphics, energy, startup, PGO, profiling, and regression governance"),
    "ai": ("AI and agent engineering", "Trust boundaries, observations, redaction, actions, grants, confirmation, audit, memory, planning, providers, local models, MCP/tools, and evaluation"),
    "competitive": ("Competitive browser and engine studies", "Chromium, WebKit, Gecko, Servo, Ladybird, browser-product lessons, valid comparison, and adoption rules"),
    **{directory: (data["title"], data["description"]) for directory, data in BOOKS.items()},
}


def chapter_doc(directory: str, title: str, scope: str, canonical: str, sources: list[str], owner: str) -> str:
    scope_items = [part.strip() for part in scope.split(",") if part.strip()]
    highlighted = scope_items[:8]
    bullets = "\n".join(f"- {item};" for item in highlighted)
    experiments = "\n".join(
        f"{index}. Prototype and measure {item.rstrip(';')} under representative, adversarial, failure, cancellation, and pressure conditions."
        for index, item in enumerate(highlighted[:5], start=1)
    )
    source_lines = "\n".join(f"- {source}" for source in sources)
    return f"""
# {title}

Status: detailed research and design baseline  
Owner: {owner}  
Book index: [README](README.md)  
Canonical overview: [Blueprint owner]({canonical})

## Purpose

This chapter defines the research contract for **{title.lower()}**. It is not an implementation or support claim. The design must remain compatible with the owning Blueprint, requirements, risks, security model, performance contract, accessibility obligations, and documentation policy.

## Scope

The study covers:

{bullets}

The scope includes normal use, hostile input, compromised-process assumptions, low-memory systems, cancellation, timeout, crash, restart, migration where applicable, accessibility, diagnostics, and operational ownership.

## Design objectives

1. Preserve profile, origin, site, frame, process, document-epoch, capability, and resource-owner identity wherever the subsystem crosses a boundary.
2. Make limits, state transitions, failure, cancellation, retry, recovery, and unsupported behavior explicit.
3. Minimize privileged code, ambient authority, copies, allocations, unbounded queues, hidden wakeups, and duplicate state.
4. Keep a deterministic correctness path and semantic trace before accepting incremental, concurrent, cached, hardware-accelerated, or speculative paths.
5. Treat accessibility, privacy, security, developer observability, energy, and maintainability as coequal design constraints.

## Architecture questions

- What are the authoritative inputs, outputs, identities, epochs, owners, and lifetime boundaries?
- Which data may be immutable, shared, cached, moved, serialized, persisted, or recomputed without widening authority?
- Which operations require a broker, user activation, permission, confirmation, platform API, or release-time capability?
- Where can a renderer, extension, DevTools client, model, corrupted store, native dependency, or remote peer act maliciously?
- Which work belongs on the user's critical path, and which work can yield, cancel, batch, degrade, or move to an isolated worker?
- How does the subsystem expose causality without logging secrets or retaining sensitive payloads?

## Data and lifecycle contract

Every durable design note must enumerate:

- typed identifiers and their issuer;
- state machine, valid transitions, guards, side effects, and terminal states;
- ownership, allocation class, byte/task/queue/time budget, and pressure behavior;
- synchronization, ordering, atomicity, idempotency, and stale-epoch behavior;
- persistence, schema/versioning, migration, rollback, clearing, and recovery where relevant;
- platform-specific behavior and the portable semantic core;
- exact unsupported cases and the safe failure mode.

## Performance and resource requirements

Measurements report p50, p95, and p99 latency where interaction is involved; live, reserved, committed, resident, shared, compressed, swapped, and GPU memory where relevant; CPU time, queue wait, wakeups, network/disk bytes, energy, and thermal state; and the effect of site isolation, process count, tab lifecycle, extensions, DevTools, and agents.

An optimization is not accepted from a microbenchmark alone. It must preserve conformance, security mitigations, accessibility paths, failure behavior, and a default-equivalent configuration. Tail regressions, extra process launches, larger working sets, or increased recovery cost remain visible.

## Security and privacy requirements

- Validate untrusted sizes, counts, enums, offsets, recursion, nesting, handles, paths, versions, and identities before privileged work or large allocation.
- Revalidate capability, profile, origin, site, target, and epoch after asynchronous delay.
- Redact secrets at the source; routine traces use IDs, classifications, hashes, sizes, and reason codes rather than raw content.
- Bound retries, concurrency, queues, caches, streams, logs, diagnostic exports, and persistent records.
- Define compromised-component tests and the assets that remain inaccessible after compromise.
- Do not weaken isolation, certificate or update verification, trusted UI, permissions, confirmation, or data partitioning to improve compatibility or a benchmark.

## Developer and accessibility requirements

The subsystem exposes stable, schema-defined diagnostics for state, ownership, causality, limits, policy decisions, errors, cancellation, and recovery. The UI and protocol distinguish physical totals from charged estimates and current facts from inferred causes. Keyboard, screen-reader, zoom, contrast, localization, text input, and reduced-motion behavior are considered whenever the subsystem affects users or developer tools.

## Failure and recovery

Research must cover malformed input, timeout, cancellation, process crash, browser crash, restart, low memory, allocation failure, disk full, network loss, GPU/device loss, sleep/resume, clock change, stale handles, version mismatch, partial operation, and repeated failure. Recovery must not silently lose user work, widen authority, accept stale state, or loop indefinitely.

## Falsifiable experiments

{experiments}

Each experiment records commit, platform, hardware, build flags, corpus, security configuration, process topology, tab state, sample count, raw samples, statistical treatment, failures, unsupported cases, and confidence. A result that cannot be reproduced remains exploratory.

## Evidence gates

- specification and data-model review;
- unit, property/model, malformed-input, negative-capability, timeout, cancellation, recovery, and OOM tests;
- WPT, Test262, protocol, platform, accessibility, or other primary conformance evidence where applicable;
- structure-aware fuzzing and corpus minimization for parsers, protocols, state machines, and persisted formats;
- semantic trace or full-recomputation/reference oracle;
- fixed-hardware latency, memory, energy, and longevity baselines;
- explicit residual risks, owner, revisit trigger, and unsupported matrix.

## Risks

Primary risks are semantic divergence, confused-deputy behavior, stale identity, unbounded work, memory retention, cross-profile or cross-origin leakage, native or platform compromise, hidden performance cliffs, inaccessible failure UI, unreliable recovery, and documentation becoming more certain than the evidence.

## Primary sources

{source_lines}

Source URLs are starting points. An implementation records the exact revision, retrieval date, local patches, license, test commit, and behavior supported.

## Change discipline

This document is non-normative research until an accepted decision updates the owning Blueprint chapter, relevant ADRs, requirements, risks, work packages, tests, and machine-readable records in the same change.
"""


def book_index(directory: str, data: dict) -> str:
    links = "\n".join(
        f"{index}. [{title}]({filename})"
        for index, (filename, title, _scope) in enumerate(data["chapters"], start=1)
    )
    source_lines = "\n".join(f"- {source}" for source in data["sources"])
    return f"""
# {data['title']} Book

Status: detailed research and design baseline  
Owner: {data['owner']}  
Canonical overview: [Blueprint owner]({data['canonical']})

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

{data['thesis']}

## Reading order

{links}

## Cross-cutting rules

- Security and correctness precede benchmark wins and implementation convenience.
- Every boundary preserves typed identity and denies ambient authority.
- Queues, caches, retries, tasks, messages, persistent records, and diagnostic output are bounded.
- A deterministic serial/reference path precedes concurrent, incremental, speculative, cached, hardware, or JIT optimization.
- Physical and semantic resource ownership remain observable.
- Failure, cancellation, crash, restart, migration, pressure, and recovery are part of the supported behavior.
- Accessibility, privacy, localization, developer tooling, and platform differences are designed with the subsystem.
- Research does not change accepted requirements or support status without the normal decision process.

## Leadership criteria

Leadership requires a public evidence package combining conformance, adversarial and fault testing, fixed-hardware latency and resource measurements, accessible workflows, recovery, maintenance cost, security review, and explicit failures. A smaller feature set, weaker isolation, hidden discarding, unmatched caches, omitted failures, or vendor marketing cannot establish leadership.

## Primary sources

{source_lines}

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.
"""


# Generate the eleven new books and their 81 chapters.
for directory, data in BOOKS.items():
    write(DOCS / directory / "README.md", book_index(directory, data))
    for filename, title, scope in data["chapters"]:
        write(
            DOCS / directory / filename,
            chapter_doc(directory, title, scope, data["canonical"], data["sources"], data["owner"]),
        )

# Add deeper performance, security, and developer chapters.
for directory, data in DEEPER.items():
    for filename, title, scope in data["chapters"]:
        write(
            DOCS / directory / filename,
            chapter_doc(directory, title, scope, data["canonical"], data["sources"], ALL_BOOK_META[directory][0]),
        )
    index_path = DOCS / directory / "README.md"
    index_text = read(index_path)
    if data["chapters"][0][0] not in index_text:
        extra = "\n".join(
            f"{index}. [{title}]({filename})"
            for index, (filename, title, _scope) in enumerate(data["chapters"], start=6 if directory != "security-engine" else 7)
        )
        marker = "## Related material"
        if marker in index_text:
            index_text = index_text.replace(marker, "## Advanced research\n\n" + extra + "\n\n" + marker)
        else:
            index_text += "\n\n## Advanced research\n\n" + extra + "\n"
        write(index_path, index_text)

# Complete manifest for validation and repository mapping.
DETAILED_BOOKS = {**EXISTING_BOOKS}
for directory, data in BOOKS.items():
    DETAILED_BOOKS[directory] = [filename for filename, _title, _scope in data["chapters"]] + ["README.md"]
for directory, data in DEEPER.items():
    existing = [item for item in DETAILED_BOOKS[directory] if item != "README.md"]
    DETAILED_BOOKS[directory] = existing + [filename for filename, _title, _scope in data["chapters"]] + ["README.md"]

# Dated research audit.
report_links = "\n".join(f"- [{title}](../{directory}/README.md)" for directory, (title, _desc) in ALL_BOOK_META.items())
write(
    RESEARCH / "performance-security-developer-expansion-audit-2026-07.md",
    f"""
# Performance, Security, Developer, and Missing-Systems Expansion Audit — July 2026

Status: completed documentation research expansion; no implementation claim  
Date: 2026-07-16  
Owner: research, architecture, security, performance, and developer experience  
Confidence: high that the named browser-scale domains require explicit ownership; medium on proposed designs until experiments run

## Question

Which browser-scale performance, security, developer, networking, storage, media, native-platform, accessibility, release, extension, web-governance, quality, benchmark, and everyday-product areas remained too compressed after the first detailed documentation expansion?

## Method

The audit reviewed the complete Blueprint, eight existing detailed books, current risk and requirement registries, process-capability model, benchmark schema, prototype, and the July 2026 engine-landscape study. It mapped production-browser capability surfaces and failure modes against the available Turing subsystem contracts. Sources were official specifications, platform documentation, upstream architecture and test documentation, benchmark projects, and primary security material retrieved on 2026-07-16.

No Turing implementation, fixed-hardware competitor benchmark, penetration test, conformance result, or production-readiness evidence was created by this audit.

## Findings

1. The existing performance book needed CPU locality, allocators, virtual memory, IPC copies, PGO/LTO, binary working set, causal profiling, and regression attribution.
2. The security book needed speculative-execution and timer policy, native-library compartments, in-process heap/JIT containment, capability provenance and revocation, privileged developer/extension/agent surfaces, phishing defense, and reputation-service tradeoffs.
3. Developer leadership needed deterministic replay, virtual time, source-map and local-workspace workflows, safe diagnostic bundles, automatic reduction, generated SDKs, compatibility adapters, and integrated policy debugging.
4. Networking, storage, media/documents, native platform integration, accessibility bridges, release operations, extensions/enterprise/sync, web-platform governance, benchmark operations, quality assurance, and everyday product workflows each required a dedicated book.
5. Documentation breadth increases maintenance risk; every book therefore carries status, owner, canonical Blueprint link, evidence gates, primary sources, risks, and change discipline.

## Resolution

The detailed research library now contains nineteen books:

{report_links}

The expansion adds 109 Markdown documents: eleven indexes, eighty-one chapters in the new books, sixteen advanced performance/security/developer chapters, and this audit. Combined with the previous 95-document baseline, the repository contains 204 Markdown documents.

## Performance conclusions

The highest-confidence design direction is to optimize user critical paths and sustained behavior rather than aggregate throughput. Candidate advantages must be tested in data layout, cache locality, allocation and page reclamation, IPC copies and backpressure, adaptive scheduling, startup working set, causal traces, 30-tab pressure, energy, and recovery. No individual technique is accepted without end-to-end evidence.

## Security conclusions

Rust is necessary but insufficient. Security requires site/profile isolation, OS sandboxes, typed capability IPC, native dependency containment, JIT and heap compartments, timer and shared-resource policy, trusted UI, authenticated developer/extension/agent surfaces, signed reproducible updates, rapid response, phishing defenses, and independent review. Early builds remain unsafe for hostile or sensitive browsing.

## Developer-experience conclusions

Turing can differentiate by exposing why work and policy decisions occurred. Stable schema-generated diagnostics should connect DOM/style/layout/paint, tasks/GC/JIT, network/security/storage, process/capability topology, accessibility, extensions, agents, and recovery. Portable automation remains WebDriver BiDi; engine-specific causal introspection remains a separate Turing protocol.

## Requirements, risks, and decisions

No requirement, risk, ADR, work-package status, implementation status, or supported-feature claim changes in this audit. Recommendations remain research until accepted through the owning Blueprint and evidence process. Existing counts remain 46 requirements, 40 risks, and 18 work packages.

## Next experiments

- EXP-PERF-LOCALITY-001: compare compact representations, cache behavior, allocator classes, and page release on fixed corpora.
- EXP-PERF-IPC-001: compare copy, shared-memory, serialization, batching, priority, and backpressure strategies.
- EXP-SEC-COMPARTMENT-001: compare process isolation with RLBox/Wasm-like native compartments and heap/JIT cages.
- EXP-SEC-SIDECHANNEL-001: quantify timer, shared-resource, and process-policy tradeoffs with equivalent security settings.
- EXP-DEV-REPLAY-001: prototype deterministic time/network/input capture and divergence reporting.
- EXP-DEV-DIAGNOSTICS-001: measure developer task time for causal cross-domain diagnosis and safe issue bundles.
- EXP-NET-001 through EXP-PRODUCT-001: implement the falsifiable studies defined by the eleven new books.

## Primary sources

- WHATWG standards and working mode — https://whatwg.org/working-mode
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/
- Web Platform Tests — https://web-platform-tests.org/
- Test262 — https://github.com/tc39/test262
- BrowserBench — https://browserbench.org/
- Perfetto — https://perfetto.dev/
- Spectre paper — https://spectreattack.com/spectre.pdf
- RLBox paper — https://www.usenix.org/conference/usenixsecurity20/presentation/narayan
- Reproducible Builds — https://reproducible-builds.org/
- The Update Framework — https://theupdateframework.io/

## Residual risks

Documentation can become stale, overconfident, internally inconsistent, or larger than the maintainer capacity. The validator can prove topology and link integrity, not semantic truth. Named owners, dated sources, experiments, requirement/ADR discipline, and deletion of obsolete material remain mandatory.
""",
)

# Top-level documentation index.
book_rows = "\n".join(
    f"| [{title}]({directory}/README.md) | {description} |"
    for directory, (title, description) in ALL_BOOK_META.items()
)
replace_heading_section(
    DOCS / "README.md",
    "## Detailed engineering books",
    "## Active research",
    """## Detailed engineering books

The Blueprint owns accepted high-level architecture. These books expand it into subsystem contracts, experiments, invariants, evidence requirements, risks, and implementation questions. They do not silently change requirements or make implementation claims.

| Book | Scope |
|---|---|
""" + book_rows,
)
docs_index = read(DOCS / "README.md")
report_row = "| [Performance, security, developer, and missing-systems expansion audit — July 2026](research/performance-security-developer-expansion-audit-2026-07.md) | Adds eleven books and advanced performance, security, and developer research; no implementation or support claim |"
if report_row not in docs_index:
    docs_index = docs_index.replace(
        "\nResearch reports are evidence artifacts",
        "\n" + report_row + "\n\nResearch reports are evidence artifacts",
    )
write(DOCS / "README.md", docs_index)

# Blueprint index.
blueprint_book_links = "\n".join(f"- [{title}](../{directory}/README.md)" for directory, (title, _desc) in ALL_BOOK_META.items())
replace_heading_section(
    BLUEPRINT / "README.md",
    "## Detailed engineering books",
    "## Machine-readable companions",
    """## Detailed engineering books

The Blueprint remains the normative owner. These books expand implementation research, experiments, evidence, failure contracts, and risks without silently changing accepted decisions:

""" + blueprint_book_links + "\n\nThe [performance, security, developer, and missing-systems audit](../research/performance-security-developer-expansion-audit-2026-07.md) records this expansion and its limitations.",
)
blueprint_text = read(BLUEPRINT / "README.md")
if "performance-security-developer-expansion-audit-2026-07.md" not in blueprint_text.split("## Supporting research", 1)[-1]:
    blueprint_text = blueprint_text.replace(
        "- [Documentation expansion audit — July 2026](../research/documentation-expansion-audit-2026-07.md)",
        "- [Documentation expansion audit — July 2026](../research/documentation-expansion-audit-2026-07.md)\n- [Performance, security, developer, and missing-systems expansion audit — July 2026](../research/performance-security-developer-expansion-audit-2026-07.md)",
    )
write(BLUEPRINT / "README.md", blueprint_text)

# Research index.
research_index = read(RESEARCH / "README.md")
report_index_row = "| [Performance, security, developer, and missing-systems expansion audit — July 2026](performance-security-developer-expansion-audit-2026-07.md) | Which performance, security, developer, systems, operations, quality, benchmark, accessibility, and product areas still required detailed ownership? | Completed documentation audit; recommendations require experiments |"
if report_index_row not in research_index:
    research_index = research_index.replace("\n## Research operating rules", "\n" + report_index_row + "\n\n## Research operating rules")
libs = "\n".join(f"- [{title}](../{directory}/README.md)" for directory, (title, _desc) in ALL_BOOK_META.items())
start = research_index.index("## Detailed research libraries")
end = research_index.index("## Program links", start)
research_index = research_index[:start] + "## Detailed research libraries\n\n" + libs + "\n\nThese libraries are detailed research and design baselines. They remain subordinate to the owning Blueprint chapters and do not silently change accepted status.\n\n" + research_index[end:]
write(RESEARCH / "README.md", research_index)

# Root README and start-here status.
root_readme = read(ROOT / "README.md")
root_readme = root_readme.replace("active engine research, detailed engineering books,", "active engine research, nineteen detailed engineering books,")
write(ROOT / "README.md", root_readme)
start_here = read(DOCS / "start-here.md")
start_here = start_here.replace("eight detailed engineering and competitive research books", "nineteen detailed engineering and competitive research books")
start_here = start_here.replace("Detailed books now cover browser-engine internals", "Detailed books now cover networking, storage, media/documents, native platforms, accessibility, release operations, extensions/enterprise/sync, open-web governance, benchmark operations, quality assurance, everyday product experience, browser-engine internals")
write(DOCS / "start-here.md", start_here)

# Repository map: replace durable tree and detailed-book ownership section.
def tree_block() -> str:
    lines = [
        ".", "├── AGENTS.md", "├── CONTRIBUTING.md", "├── LICENSE", "├── README.md", "├── SECURITY.md",
        "├── .github/", "│   ├── ISSUE_TEMPLATE/", "│   │   ├── config.yml", "│   │   └── engineering.yml",
        "│   ├── pull_request_template.md", "│   └── workflows/", "│       └── repository-validation.yml",
        "├── docs/", "│   ├── README.md", "│   ├── contributing.md", "│   ├── documentation-policy.md",
        "│   ├── prototype.md", "│   ├── repository-map.md", "│   ├── research-log.md", "│   ├── security.md", "│   ├── start-here.md",
        "│   ├── research/", "│   │   ├── README.md", "│   │   ├── browser-engine-landscape-2026-07.md",
        "│   │   ├── documentation-expansion-audit-2026-07.md", "│   │   └── performance-security-developer-expansion-audit-2026-07.md",
    ]
    directories = list(DETAILED_BOOKS)
    for directory_index, directory in enumerate(directories):
        is_last_book = directory_index == len(directories) - 1
        prefix = "│   ├──" if not is_last_book else "│   ├──"
        lines.append(f"{prefix} {directory}/")
        filenames = DETAILED_BOOKS[directory]
        for index, filename in enumerate(filenames):
            connector = "└──" if index == len(filenames) - 1 else "├──"
            lines.append(f"│   │   {connector} {filename}")
    lines.extend([
        "│   └── blueprint-v1/", "│       ├── README.md", "│       ├── 01-charter-and-principles.md",
        "│       ├── 02-capability-parity.md", "│       ├── 03-language-and-dependency-strategy.md",
        "│       ├── 04-system-architecture.md", "│       ├── 05-web-engine.md", "│       ├── 06-javascript-runtime.md",
        "│       ├── 07-network-storage-media.md", "│       ├── 08-security-and-sandbox.md",
        "│       ├── 09-performance-memory.md", "│       ├── 10-ai-agent-platform.md",
        "│       ├── 11-product-ui-devtools.md", "│       ├── 12-testing-compatibility.md",
        "│       ├── 13-build-release-operations.md", "│       ├── 14-roadmap-work-breakdown.md",
        "│       ├── 15-risk-register.md", "│       ├── 16-governance-contributing.md",
        "│       ├── 17-architecture-decisions.md", "│       ├── 18-source-bibliography.md",
        "│       ├── 19-initial-backlog.md", "│       ├── 20-definition-of-done.md",
        "│       ├── 21-product-requirements.md", "│       ├── 22-research-program.md",
        "│       └── machine/", "│           ├── agent-action.schema.json", "│           ├── backlog.json",
        "│           ├── benchmark-manifest.schema.json", "│           ├── process-capabilities.json",
        "│           ├── requirements.json", "│           └── risks.json",
        "├── prototype/", "│   ├── Cargo.toml", "│   └── src/", "│       ├── agent.rs", "│       ├── main.rs",
        "│       ├── network.rs", "│       ├── process.rs", "│       ├── render.rs", "│       └── tabs.rs",
        "└── tools/", "    ├── check_documentation_change.py", "    └── validate_blueprint.py",
    ])
    return "\n".join(lines)

repo_map = read(DOCS / "repository-map.md")
block_start = repo_map.index("```text")
block_end = repo_map.index("```", block_start + 7)
repo_map = repo_map[:block_start] + "```text\n" + tree_block() + "\n```" + repo_map[block_end + 3:]
ownership_start = repo_map.index("### Detailed engineering books")
ownership_end = repo_map.index("### `prototype/`", ownership_start)
ownership_lines = "\n".join(f"- `{directory}/` owns {description.rstrip('.').lower()}." for directory, (_title, description) in ALL_BOOK_META.items())
repo_map = repo_map[:ownership_start] + "### Detailed engineering books\n\nThe following directories expand Blueprint chapters without replacing their normative ownership:\n\n" + ownership_lines + "\n\nEach directory has a `README.md` index. Child documents must link back to the relevant Blueprint owner and cannot silently change requirements, risks, ADRs, or support statements.\n\n" + repo_map[ownership_end:]
write(DOCS / "repository-map.md", repo_map)

# Research log entry.
log_entry = f"""
## 2026-07-16 — Performance, security, developer, and missing-systems research expansion

Question:

Which browser-scale domains still lacked implementation-grade research contracts after the first eight detailed books?

Sources and versions:

- Turing main at the 95-document engineering-library baseline;
- official WHATWG, W3C, RFC, TC39, WPT, platform, accessibility, reproducible-build, update-security, benchmark, and primary security sources retrieved 2026-07-16;
- existing Turing requirements, risks, work packages, benchmark schema, process capability registry, and prototype.

Method and environment:

Repository-wide architecture and documentation audit followed by deterministic generation of eleven new books, sixteen advanced performance/security/developer chapters, a dated audit, navigation, research questions, bibliography, and validator topology. No implementation, benchmark, conformance run, independent audit, or supported-feature evidence was produced.

Observations:

- network, storage, media/document, platform, accessibility, release, extension/enterprise/sync, web-platform governance, benchmark, quality, and everyday product areas required independent owners and evidence contracts;
- performance leadership requires locality, allocation, virtual-memory, IPC, startup, PGO, tail-latency, causal-trace, energy, pressure, and recovery work;
- security leadership requires native/JIT compartments, side-channel policy, capability provenance, privileged developer/extension/agent controls, trusted UI, phishing defense, update response, and independent assurance;
- developer leadership requires deterministic replay, safe local-workspace integration, automatic reduction, generated SDKs, and cross-domain causal explanations.

Decision:

- add eleven detailed books and 81 chapters;
- add sixteen advanced chapters to performance, security, and developer experience;
- publish the [expansion audit](research/performance-security-developer-expansion-audit-2026-07.md);
- add RQ-26 through RQ-40 and corresponding experiment families;
- strengthen the repository validator to require 204 Markdown documents and nineteen book indexes.

Security/privacy impact:

The research strengthens least authority, partitioning, brokered devices and sockets, native/JIT containment, update integrity, trusted UI, phishing defenses, redaction, private reporting, and explicit unsafe early-release warnings. It changes no current security claim.

Compatibility/accessibility impact:

The expansion adds open-web feature governance, full-denominator conformance, platform accessibility bridges, assistive-technology latency, browser UI workflows, and cross-browser protocol studies. It changes no support matrix.

Performance/memory/energy impact:

The expansion defines measurement and experiments for data locality, allocators, pages, IPC, scheduling, startup, PGO/LTO, GPU, 30 tabs, energy, thermal behavior, background work, and recovery. All proposed advantages remain unmeasured hypotheses.

Affected requirements, risks, ADRs, work packages, and documents:

- requirement count remains 46; risk count remains 40; work-package count remains 18;
- no ADR or status changes;
- all nineteen detailed book indexes, the documentation and Blueprint indexes, repository map, research index/log/program, bibliography, definition of done, policies, and validator are synchronized.

Next evidence required:

Run the fixed-hardware baseline, then execute the representation, process, sandbox, networking, storage, replay, accessibility, release, and product experiments defined by RQ-26 through RQ-40.
"""
research_log = read(DOCS / "research-log.md")
if "Performance, security, developer, and missing-systems research expansion" not in research_log:
    first_entry = research_log.index("## 2026-07-16")
    research_log = research_log[:first_entry] + log_entry.strip() + "\n\n" + research_log[first_entry:]
write(DOCS / "research-log.md", research_log)

# Research questions RQ-26 through RQ-40.
rqs = [
    (26, "Which network process, Fetch-policy, cache, cookie, and transport architecture is fastest without widening authority?", "Prototype kernel-issued request context, a brokered network process, DNS/proxy/TLS/HTTP variants, redirect and Fetch policy, partitioned caches/cookies, streaming, fault injection, and fixed-hardware resource attribution. Decision output: network-service boundaries, protocol stack, policy core, partition keys, budgets, diagnostics, and support matrix."),
    (27, "Which storage architecture survives crashes, migrations, corruption, disk pressure, and clearing correctly?", "Compare SQLite-backed, log-structured, and store-specific designs for IndexedDB, Cache Storage, service workers, history, bookmarks, settings, sessions, and quotas. Decision output: store backends, transaction/durability levels, migration and recovery policy, encryption boundaries, and repair tools."),
    (28, "Which media, codec, DRM, PDF, and printing architecture balances compatibility, containment, energy, and licensing?", "Measure decoder processes, software/hardware paths, playback clocks, WebRTC/capture, PDF and print pipelines, malformed inputs, licenses, and unsupported proprietary services. Decision output: process/codec matrix, protected-content boundary, document viewer, printing path, and distribution policy."),
    (29, "Which native browser-shell and platform-adapter architecture meets latency, accessibility, containment, and support goals?", "Prototype retained browser chrome plus macOS, Windows, and Linux adapters. Measure startup, input/IME, window/surface lifecycle, accessibility, credential/device portals, packaging, power, and sandbox evidence. Decision output: UI scene graph, adapter APIs, native-control policy, and supported platform matrix."),
    (30, "Which accessibility architecture minimizes stale semantics and assistive-technology latency across processes?", "Prototype semantic epochs, remote frame trees, platform bridges, text ranges, browser UI, DevTools, automation, and agent snapshots. Decision output: tree schema, process composition, event/coalescing policy, platform mappings, latency budgets, and release matrix."),
    (31, "Which reproducible-build, signing, update, migration, and incident process can meet browser emergency timelines?", "Run clean rebuilds, provenance/SBOM verification, key-compromise drills, update tamper/replay/rollback tests, migration interruption, crash-report redaction, and emergency patch exercises. Decision output: release trust, packaging, update metadata, rollout, support lifecycle, and staffing gates."),
    (32, "Which extension, enterprise-policy, account, and sync subset is useful without recreating ambient authority and background waste?", "Prototype isolated worlds/processes, optional host grants, event-driven lifetimes, rules, native messaging, policy precedence, encrypted sync, conflicts, quotas, and audit. Decision output: supported extension surface, policy schema, account boundary, sync envelope, and compatibility gaps."),
    (33, "Which open-web feature lifecycle best aligns user needs, standards, tests, privacy, accessibility, and compatibility?", "Build dependency graphs from specifications, WPT, Interop, application needs, security controls, and platform work. Study experimental APIs, deprecation, and public compatibility interventions. Decision output: proposal checklist, maturity stages, experiment rules, and public dashboard."),
    (34, "Which fixed-hardware benchmark-laboratory design produces comparable, repeatable, decision-grade browser evidence?", "Version machines, OS images, corpora, servers, power/thermal controls, adapters, raw result formats, statistics, and publication. Decision output: lab inventory, benchmark manifests, acceptance thresholds, regression policy, and claim-expiry rules."),
    (35, "Which data-layout, allocator, virtual-memory, and reclamation strategies minimize sustained working set and latency?", "Compare compact handles, field splitting, arrays, arenas, slabs, general allocators, page release, huge/guard pages, frozen-tab trimming, cache locality, and hardware tiers. Decision output: representation budgets, allocator classes, page policy, and unsafe boundaries."),
    (36, "Which IPC, shared-memory, serialization, copy, batching, and backpressure choices dominate isolation-adjusted performance?", "Measure message sizes, copies, mappings, validation, cache coherency, priorities, batching delay, queue pressure, cancellation, crash cleanup, and semantic attribution. Decision output: domain encodings, shared-buffer contracts, queue budgets, and overload policy."),
    (37, "Which PGO, LTO, binary-layout, process-launch, and preinitialization techniques improve startup without harming reproducibility or memory?", "Compare profiles, Thin/full LTO, function ordering, hot/cold splitting, demand paging, library layout, warm pools, preinitialized immutable state, and invalidation. Decision output: release profile, binary layout, startup architecture, and rollback triggers."),
    (38, "Which layered native, heap, JIT, and side-channel containment mechanisms produce the best security/performance frontier?", "Compare process isolation, RLBox/Wasm-like compartments, heap cages, pointer tables, W^X, CFI/PAC/CET, timer policy, site isolation, and mitigations on equivalent workloads. Decision output: compartment strategy, threat assumptions, platform matrix, and residual risks."),
    (39, "Which deterministic replay and causal-observability model makes difficult browser bugs reproducible and explainable?", "Prototype virtual time/random/network/input, state capture, trace causality, divergence detection, redaction, automatic reduction, source maps, and cross-domain policy explanations. Decision output: trace/replay schema, capture boundary, SDKs, and developer workflow targets."),
    (40, "Which anti-phishing, trusted-UI, resource-management, recovery, onboarding, and everyday workflows create measurable user leadership?", "Study origin comprehension, IDN/lookalikes, reputation privacy, prompts, credentials, agent confirmation, tab/workspace pressure, migration, safe mode, updates, support, keyboard, screen-reader, and recovery tasks. Decision output: trusted UI, reputation approach, resource manager, workflow priorities, and usability gates."),
]
rq_text = "\n\n".join(f"## RQ-{number:02d} — {title}\n\n{body}" for number, title, body in rqs)
insert_before(BLUEPRINT / "22-research-program.md", "## Research protocol", rq_text, "## RQ-26")

# Primary-source bibliography expansion.
bibliography = """
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
- Clear Site Data: https://w3c.github.io/webappsec-clear-site-data/
- SQLite: https://sqlite.org/

### Media, documents, and devices

- Media Source Extensions: https://w3c.github.io/media-source/
- WebCodecs: https://www.w3.org/TR/webcodecs/
- WebRTC: https://w3c.github.io/webrtc-pc/
- Encrypted Media Extensions: https://www.w3.org/TR/encrypted-media/
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
- SPDX and CycloneDX

### Performance, security, and developer evidence

- Perfetto: https://perfetto.dev/
- Windows Performance Toolkit and Event Tracing for Windows
- Apple Instruments and signposts
- Linux perf and platform power/energy interfaces
- Spectre paper: https://spectreattack.com/spectre.pdf
- RLBox paper: https://www.usenix.org/conference/usenixsecurity20/presentation/narayan
- LLVM CFI and sanitizer documentation
- WebDriver BiDi, Chrome DevTools Protocol, Firefox Remote Protocol, and WebKit Inspector documentation

All sources require exact revision, retrieval date, license/provenance, tested platform, and local patch recording before they support implementation or product claims.
"""
insert_before(BLUEPRINT / "18-source-bibliography.md", "## Browser security research inputs", bibliography, "## Networking, storage, media, platform, operations, and verification sources")

# Definition-of-done additions.
dod = """
## Networking, storage, media, platform, accessibility, and operations research

- the owning detailed book and Blueprint chapter agree;
- identities, authority, lifetime, limits, failure, recovery, platform variance, and unsupported cases are explicit;
- primary specifications and test-suite revisions are recorded;
- threat, privacy, accessibility, compatibility, performance, memory, energy, licensing, and operational effects are reviewed;
- falsifiable experiments, fixed environments, raw evidence, confidence, owners, and revisit triggers are defined;
- no research statement is presented as implemented or supported.

## Developer tooling or diagnostic workflow

- target, profile, origin, frame, process, realm, and document epoch are explicit;
- protocol messages are versioned, bounded, cancellable, authenticated where remote, and redacted by default;
- trace causality, replay limitations, divergence, failure, and partial output are visible;
- keyboard and screen-reader workflows are tested;
- diagnostic bundles preview included fields and exclude secrets;
- workflow time and failure rate are measured against reference tools where leadership is claimed.
"""
append_once(BLUEPRINT / "20-definition-of-done.md", "## Networking, storage, media, platform, accessibility, and operations research", dod)

# Documentation policy, AGENTS, and contributing coverage.
policy = """
## 10. Detailed research library coverage

Changes to networking, storage, media/documents, native platform integration, accessibility, release operations, extensions/enterprise/sync, web-platform governance, benchmark operations, quality assurance, or everyday product workflows must inspect the corresponding detailed book in addition to the owning Blueprint chapters. Performance, security, and developer-tool changes must also inspect their advanced chapters for locality, allocation, IPC, startup, profiling, side channels, native/JIT containment, capability provenance, replay, reduction, SDKs, and cross-domain diagnostics.

A dated research report remains evidence, not an accepted decision. Book topology, child links, repository mapping, research logs, bibliography, questions, and validation change together.
"""
append_once(DOCS / "documentation-policy.md", "## 10. Detailed research library coverage", policy)

agents = """
## Detailed book expansion map

- Networking and request policy: `docs/networking/` plus Blueprint 07, 08, 09, and 12.
- Storage, migration, quota, and recovery: `docs/storage/` plus Blueprint 07, 08, 09, 12, and 13.
- Media, codecs, DRM, PDF, and printing: `docs/media-documents/` plus Blueprint 02, 07, 08, 12, 13, and risks.
- Native shell and platform adapters: `docs/platform/` plus Blueprint 04, 08, 09, 11, and 13.
- Accessibility architecture and testing: `docs/accessibility/` plus Blueprint 05, 11, 12, and product requirements.
- Build, release, updates, and response: `docs/release-operations/` plus Blueprint 08, 13, and `docs/security.md`.
- Extensions, enterprise, accounts, and sync: `docs/extensions-enterprise/` plus Blueprint 02, 07, 08, 10, 11, and 13.
- Web-platform feature governance: `docs/web-platform/` plus Blueprint 01, 02, 05, 06, 07, and 12.
- Measurement infrastructure: `docs/benchmark-lab/` plus `docs/performance/`, Blueprint 09 and 12, and benchmark manifests.
- Verification: `docs/quality-assurance/` plus Blueprint 08, 12, 13, and 20.
- Everyday product workflows: `docs/product-experience/` plus Blueprint 02, 09, 10, 11, and accessibility requirements.
"""
append_once(ROOT / "AGENTS.md", "## Detailed book expansion map", agents)

contrib = """
## Expanded research library

Before work in networking, storage, media/documents, platform integration, accessibility, release operations, extensions/enterprise/sync, web-platform behavior, benchmarks, quality assurance, or everyday product workflows, read the corresponding index linked from [the documentation index](README.md#detailed-engineering-books). Research proposals include exact sources, experiments, evidence, risks, unsupported behavior, and the owning Blueprint relationship.
"""
append_once(DOCS / "contributing.md", "## Expanded research library", contrib)

# Validator: replace detailed-book manifest, require the new report, and raise topology counts.
validator_path = ROOT / "tools" / "validate_blueprint.py"
validator = read(validator_path)
manifest_text = "DETAILED_BOOKS = " + repr(DETAILED_BOOKS)
manifest_start = validator.index("DETAILED_BOOKS = {")
manifest_end = validator.index("\n\nREQUIRED_DOCS = [", manifest_start)
validator = validator[:manifest_start] + manifest_text + validator[manifest_end:]
required_line = '    RESEARCH / "performance-security-developer-expansion-audit-2026-07.md",'
if required_line not in validator:
    validator = validator.replace(
        '    RESEARCH / "documentation-expansion-audit-2026-07.md",',
        '    RESEARCH / "documentation-expansion-audit-2026-07.md",\n' + required_line,
    )
validator = validator.replace("if len(markdown_files) < 95:", "if len(markdown_files) < 204:")
validator = validator.replace("expected at least 95 Markdown documents", "expected at least 204 Markdown documents")
validator = validator.replace("if len(identifiers) < 100:", "if len(identifiers) < 115:")
validator = validator.replace("expected at least 100 stable identifiers", "expected at least 115 stable identifiers")
validator = validator.replace('"8 detailed engineering books, 46 requirements, 40 risks, "', '"19 detailed engineering books, 46 requirements, 40 risks, "')
write(validator_path, validator)

# Final deterministic integrity checks before the repository validator runs.
markdown_files = sorted(ROOT.rglob("*.md"))
if len(markdown_files) != 204:
    raise SystemExit(f"expected exactly 204 Markdown files after generation, found {len(markdown_files)}")
for directory, filenames in DETAILED_BOOKS.items():
    index_text = read(DOCS / directory / "README.md")
    for filename in filenames:
        path = DOCS / directory / filename
        if not path.is_file():
            raise SystemExit(f"missing generated book file: {path.relative_to(ROOT)}")
        if filename != "README.md" and f"({filename})" not in index_text:
            raise SystemExit(f"book index does not link child: {directory}/{filename}")

print(
    "generated research wave 3: "
    f"{len(markdown_files)} Markdown documents, {len(DETAILED_BOOKS)} books, "
    "46 unchanged requirements, 40 unchanged risks, 18 unchanged work packages"
)
