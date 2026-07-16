# Media, Documents, and Printing Engineering Book

Status: detailed research and design baseline  
Owner: media, document, codec, and printing engineering  
Canonical overview: [Blueprint owner](../blueprint-v1/07-network-storage-media.md)

This book expands the Blueprint into subsystem contracts, falsifiable experiments, evidence gates, performance and security budgets, accessibility obligations, operational requirements, and explicit unsupported cases. It does not claim that the described systems are implemented, safe, compatible, or faster than another browser.

## Thesis

Media and document formats combine hostile parsing, large allocations, hardware drivers, privacy-sensitive devices, licensing constraints, and long-lived playback state. They require process isolation, strict limits, capability mediation, and explicit distribution matrices.

## Reading order

1. [Decoder Processes and Input Limits](01-decoder-processes-and-input-limits.md)
2. [Images, Fonts, Color, and Animation](02-images-fonts-color-and-animation.md)
3. [Audio/Video Clocks, Buffering, and Seeking](03-audio-video-clocks-buffering-and-seeking.md)
4. [WebRTC, Capture, and Devices](04-webrtc-capture-and-devices.md)
5. [Codecs, Hardware Acceleration, and Licensing](05-codecs-hardware-acceleration-and-licensing.md)
6. [DRM and Content-Decryption Boundaries](06-drm-and-content-decryption-boundaries.md)
7. [PDF Viewer and Document Security](07-pdf-viewer-and-document-security.md)
8. [Printing, Pagination, Accessibility, and Quality](08-printing-pagination-accessibility-and-quality.md)

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

- https://www.w3.org/TR/webcodecs/
- https://w3c.github.io/media-source/
- https://w3c.github.io/webrtc-pc/
- https://www.w3.org/TR/encrypted-media/
- https://www.w3.org/TR/png-3/
- https://aomedia.org/av1-features/
- https://pdfa.org/resource/

## Related program material

- [Documentation index](../README.md)
- [Research index](../research/README.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Testing and compatibility](../blueprint-v1/12-testing-compatibility.md)
- [Security model](../blueprint-v1/08-security-and-sandbox.md)
- [Performance contract](../blueprint-v1/09-performance-memory.md)

## Status discipline

The book is a research baseline. Accepted architecture requires an ADR or owning Blueprint change with reproducible evidence. Current and early Turing builds remain unsafe for sensitive or hostile browsing.
