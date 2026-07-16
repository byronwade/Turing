# Images, Media, SVG, and Canvas

Status: research baseline; codec and graphics feature matrix remains undecided  
Owner: media and graphics content  
Purpose: Define safe, bounded pipelines for images, vector graphics, canvas, audio, video, and protected media without pretending proprietary capabilities are automatically available.

## Relationship to the Turing program

Network/storage/media services remain owned by [Blueprint 07](../blueprint-v1/07-network-storage-media.md); this document concentrates on engine-facing contracts.

## Image pipeline

Image metadata is parsed before large allocation. Dimensions, color profiles, animation frame counts, durations, decoded-byte estimates, and target display size determine acceptance and decode strategy.

Decoding occurs in a restricted utility process. Output is immutable or read-only shared memory with explicit format, stride, dimensions, color space, alpha mode, generation, and owner. Large images use tiling, region decode, or safe downsampling when semantics permit.

## SVG architecture

SVG reuses DOM, CSS, text, layout, paint, filters, animation, hit testing, accessibility, and resource loading where semantics align. SVG-specific geometry, path, marker, mask, pattern, filter, and reference graphs remain explicit and bounded.

External references and embedded content follow origin, CSP, CORS, tainting, and lifecycle rules. Cyclic references, filter regions, and path complexity have deterministic limits and diagnostics.

## Canvas 2D

Canvas starts as a recorded command stream with a software reference backend. State stacks, paths, transforms, text, images, shadows, compositing, filters, and pixel readback have bounded representations.

The implementation may retain commands, raster tiles, or both based on measured workload. Origin cleanliness is tracked through every source. Readback synchronizes explicitly and is attributed in performance traces.

## Audio and video

Media is a graph of demux, decode, timing, buffering, audio output, video frame, subtitle, DRM boundary, and presentation components. Native codec libraries run in constrained processes. The browser owns HTML media semantics, resource selection, MSE/WebCodecs integration, track state, autoplay policy, permissions, lifecycle, and accessibility.

Buffering, frame queues, decoded surfaces, and hardware decoder sessions have budgets and backpressure. Background and hidden playback follow product policy without silently changing page-visible state.

## WebGL and WebGPU

WebGL/WebGPU are later, separately gated tracks. Their validators, shader translation, resource models, synchronization, error semantics, origin isolation, robustness, and GPU-process command boundary require dedicated fuzzing and conformance.

No graphics API receives raw host pointers, unrestricted native handles, or access to resources from another origin/profile. Device capability exposure is minimized and normalized where standards allow.

## Licensing and external gates

Codec patents, platform entitlements, protected-media modules, store policies, and vendor approval can block parity independently of engineering. Each shipped format has a platform/territory/license/source/security matrix.

Unsupported DRM or codec behavior is visible. Turing does not bypass access controls, misrepresent support, or make a general Chrome-parity claim while externally gated media remains absent.

## Non-negotiable invariants

- Metadata and size limits are validated before decoding or GPU allocation.
- Native decoders, font-like parsers, and shader translators run outside the browser kernel.
- Origin cleanliness and taint state survive every image/canvas/media transformation.
- Media queues implement backpressure and lifecycle cancellation.
- Proprietary feature gaps remain explicit product limitations.

## Required evidence

- Pinned image, SVG, canvas, media, WebGL/WebGPU, and accessibility conformance suites where applicable.
- Malformed corpus fuzzing for every enabled decoder/container and graphics command format.
- Peak decoded-memory, frame-queue, GPU-surface, startup, seek, and playback-energy measurements.
- Audio/video sync, device loss, suspend/resume, output change, crash, and recovery tests.
- License and provenance ledger for every distributed codec or binary component.

## Known risks and unresolved questions

- Hardware decoders and drivers expose platform-specific attack surfaces.
- Retained canvas commands can consume more memory than immediate raster for some workloads.
- SVG filters and paths can trigger extreme CPU/GPU work.
- DRM and patent constraints may prevent literal product parity.

## Primary sources

- SVG 2 — https://www.w3.org/TR/SVG2/
- WebGPU — https://www.w3.org/TR/webgpu/
- Web Platform Tests — https://web-platform-tests.org/
- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- WebKit documentation — https://docs.webkit.org/
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
