# Graphics, Energy, Startup, and Recovery Performance

Status: research and design baseline  
Owner: graphics and platform performance  
Purpose: Define sustained visual performance and system-level costs beyond page script benchmarks.

## Relationship to the Turing program

This document deepens startup, frame, energy, and recovery requirements from [Blueprint 09](../blueprint-v1/09-performance-memory.md).

## Graphics pipeline

Measure display-list construction, retained chunk reuse, damage, layerization, tile generation, raster queueing, uploads, GPU submission, composition, presentation, overdraw, surface memory, and device synchronization. Frame pacing distributions and input-to-present matter more than raw frames per second.

Software and GPU paths share semantic traces so acceleration does not hide correctness differences.

## GPU budgets and device loss

Textures, buffers, pipelines, glyph/image caches, video surfaces, canvas, WebGL/WebGPU, and browser chrome have owners and budgets. The compositor adapts resolution, tile priority, cache retention, and promotion without silently lowering semantic output. Device loss triggers bounded reconstruction or software fallback.

Driver workarounds are versioned, public where safe, and measured.

## Energy model

Energy work includes CPU package time, GPU active time, wakeups, timer frequency, network radio activity, disk I/O, memory pressure/swap, display refresh, video decode, and local AI accelerator use. Tests cover idle, background tabs, scrolling, animation, video, WebGL/WebGPU, downloads, calls, DevTools, and agents.

The browser responds to OS low-power and thermal states and avoids periodic wakeups without deadlines.

## Startup phases

Startup is decomposed into executable load/link, runtime initialization, security setup, profile metadata, browser window, UI first paint, address-field readiness, process pool, session enumeration, active-tab restoration, background restoration, update checks, extensions, and agent/model initialization.

Only the minimum path blocks address input. Large histories, bookmarks, extensions, and restored tabs load lazily with correctness and recovery.

## Process launch and warm state

Process creation, sandbox setup, code loading, shared immutable data, fonts, GPU initialization, and IPC handshakes are measured by role and platform. Prelaunch or warm pools are allowed only with explicit memory/energy budgets and no weaker security identity.

A warm process cannot inherit stale profile, origin, capability, or document state.

## Crash and recovery

Renderer, GPU, network, storage, DevTools, extension, agent, and browser crashes have detection, restart, state restoration, user feedback, and repeated-crash containment. Recovery metrics include time, lost state, network refetch, storage integrity, and whether the same trigger loops.

Session journals use incremental crash-safe writes and lazy restoration.

## Platform variation

macOS, Windows, Linux, display server, GPU vendor/driver, refresh rate, scaling, font stack, power policy, storage, and memory compression produce different bottlenecks. Results are platform-specific before cross-platform conclusions are drawn.

## Non-negotiable invariants

- Graphics results include frame pacing, memory, correctness, and device-loss behavior.
- Every GPU resource has an owner and budget.
- Idle features do not keep CPUs, GPUs, or model accelerators active without work.
- Address-field readiness is not blocked by avoidable restoration or network work.
- Warm pools preserve clean principal and capability identity.
- Recovery reports state loss and repeated-failure behavior.

## Required evidence

- MotionMark-family diagnostics plus real-page scrolling, animation, canvas, video, and GPU workloads.
- GPU allocation, layer churn, damage, overdraw, device-loss, and fallback traces.
- OS energy/wakeup/thermal measurements across Tier L/M/H.
- Cold/warm startup phase traces and binary/page-cache controls.
- Process launch and sandbox initialization measurements by platform.
- Crash/recovery loops, session journal fault injection, and state-loss reports.

## Known risks and unresolved questions

- GPU benchmarks can overfit simple scene patterns.
- Warm pools improve latency while retaining significant idle memory.
- Energy APIs vary by platform and carry uncertainty.
- Fallback paths can lag compatibility or accessibility.

## Primary sources

- MotionMark — https://browserbench.org/MotionMark/
- WebGPU — https://www.w3.org/TR/webgpu/
- wgpu project — https://github.com/gfx-rs/wgpu
- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
