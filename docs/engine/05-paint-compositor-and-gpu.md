# Paint, Compositor, Raster, and GPU Architecture

Status: research baseline; GPU backend and process contract are undecided  
Owner: graphics  
Purpose: Define a retained, bounded graphics pipeline that keeps scrolling and compositor animations responsive while treating display commands, shaders, images, and drivers as hostile boundaries.

## Relationship to the Turing program

The process privilege model is owned by [Blueprint 04](../blueprint-v1/04-system-architecture.md) and the [security book](../security-engine/README.md).

## Paint properties and display items

Layout fragments produce paint properties and immutable display items. Transform, clip, effect, scroll, and stacking state use stable property-tree nodes. Display items carry explicit bounds, resource references, blend/filter state, hit-test metadata, and origin cleanliness.

Paint chunks group items with compatible property state and stable client identities. A retained list reuses unchanged chunks across epochs; the damage system remains conservative. Missing paint is a correctness failure, while extra paint is a performance cost.

## Layerization and compositor graph

Layerization is a budgeted decision based on scrolling, transforms, animations, video, canvas, filters, isolation, raster scale, and damage—not a direct mirror of DOM elements. Promotion and demotion reasons are traceable.

Compositor surfaces represent process and cross-origin boundaries. Embedded surfaces are referenced by unforgeable tokens and validated geometry. A renderer cannot read another surface’s pixels or GPU resources through compositor metadata.

## Raster architecture

The reference rasterizer is software and deterministic enough for reduced tests. Production raster may use GPU compute/graphics or platform APIs. Raster tasks are tiled, prioritized by visibility and predicted use, cancelable, and charged to a semantic owner.

Tile size, raster scale, color space, antialiasing, image decode size, and cache policy are explicit. Large filters, shadows, paths, glyph runs, and images are decomposed or rejected before unbounded allocation.

## GPU process boundary

The GPU service receives validated, bounded commands and resource descriptors. It owns native devices, queues, swap chains, shader compilation, and device-loss recovery. Renderers receive only task-specific handles.

Command decoding validates counts, offsets, formats, dimensions, usage flags, synchronization, ownership, and lifetime. The process has restricted filesystem, network, and device access beyond the graphics interfaces required by platform policy.

## Frame scheduling

The scheduler coordinates browser chrome, page input, main-thread rendering, compositor work, raster, presentation, and refresh feedback. It targets stable frame pacing rather than maximum average throughput.

Compositor-only scrolling and animations can proceed from committed property and hit-test state. Main-thread dependencies are surfaced. The scheduler adapts to 60–144 Hz displays, variable refresh, occlusion, low-power mode, thermal pressure, and remote/display changes.

## Recovery and fallbacks

Device loss, driver reset, surface loss, memory pressure, and shader failure are expected events. The browser can recreate GPU state, restart the GPU process, fall back to software, and preserve tab/session state.

Fallback differences are documented in traces and test manifests. Security or correctness checks are never disabled to recover performance.

## Non-negotiable invariants

- Renderers never submit unchecked native GPU handles or arbitrary driver commands.
- Display lists and resources are bounded before allocation or execution.
- Cross-origin/process surfaces cannot be sampled without an explicitly authorized path.
- Device loss and GPU process crash do not terminate the browser or corrupt profile state.
- Compositor fast paths use committed, epoch-checked state and cannot forge user activation.

## Required evidence

- Software-reference and GPU-output comparisons with declared tolerance and color metadata.
- Display-list and shader/command fuzzing in isolated processes.
- High-refresh frame-time distributions, input-to-present traces, tile-cache behavior, and GPU memory attribution.
- Device-loss, GPU-crash, low-memory, resize, display-change, and fallback tests.
- Direct Metal/D3D12/Vulkan versus pinned abstraction experiments from RQ-05.

## Known risks and unresolved questions

- A cross-platform abstraction may hide driver capabilities or add startup and memory cost.
- Direct backends multiply maintenance and security review.
- Layer promotion can trade smoothness for excessive memory and battery use.
- Platform text and color pipelines can make pixel equality an invalid oracle.

## Primary sources

- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- WebGPU — https://www.w3.org/TR/webgpu/
- wgpu project — https://github.com/gfx-rs/wgpu
- MotionMark — https://browserbench.org/MotionMark1.3/
- WebKit documentation — https://docs.webkit.org/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
