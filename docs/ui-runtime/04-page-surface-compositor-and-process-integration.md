# Page Surface, Compositor, and Process Integration

Status: highest-risk implementation research  
Owner: UI runtime, compositor, GPU, platform, accessibility, and security

## Why this is the decisive spike

Ordinary application widgets do not prove browser suitability. Turing must place independently rendered page content inside trusted chrome while preserving damage, synchronization, input routing, accessibility, scaling, color, device loss, process failure, and security boundaries.

## Surface contract

A page surface carries a typed view ID, document epoch, device generation, logical and physical size, scale factor, color space, alpha mode, damage region, synchronization primitive, frame sequence, presentation deadline, and release acknowledgement.

The current M0 model implements only the renderer-neutral metadata subset as
`turing_ui_model::PageSurfaceDescriptor`. It is bounded, validates one surface
per view in a `ShellSnapshot`, and rejects invalid scale, size, and physical
allocation metadata. It is not a brokered handle and does not prove that Servo
frames can be composed into trusted chrome.

The UI never receives a renderer process pointer. The GPU or compositor service publishes a brokered surface handle. Stale document, view, or device generations are rejected.

## Composition alternatives

1. Turing owns the window swapchain and composites toolkit chrome plus page textures.
2. The toolkit owns the window surface and exposes a stable external-texture/custom-render hook.
3. Platform child surfaces are used only where unavoidable and tested for clipping, focus, accessibility, capture, transforms, and security.

The preferred result is one compositor path with deterministic software fallback. Any toolkit-specific GPU integration must remain behind `turing-ui-surfaces`.

## Input and accessibility

Hit testing decides whether an event targets trusted chrome or a page surface before dispatch. Pointer capture, drag/drop, gestures, scrolling, keyboard focus, IME, clipboard, and accessibility focus preserve typed target identity. The browser accessibility tree composes chrome and web subtrees without exposing hidden cross-origin data.

## Failure behavior

Renderer crash replaces only the page surface with recovery UI. GPU device loss rebuilds toolkit and page resources without discarding the session model. Toolkit failure must not corrupt profile state or automatically replay consequential actions.

## Current no-claim inventory

The checked [Page Surface Composition Inventory](../research/page-surface-composition-inventory-2026-07.md) records `PB-005` planning evidence for surface contract fields, composition alternatives, workflow tests, failure cases, security identity boundaries, evidence blockers, and unsupported claims. It does not prove renderer-produced page texture composition, typed page-surface handles, brokered surface handles, deterministic software fallback, `ADR-0016`, `UI-GATE-7`, compositor ownership, toolkit selection, page-surface approval, or release-path UI approval.

## Exit gate

`UI-GATE-7` passes only when the selected toolkit can present the page placeholder and simulated renderer frames across resize, scale, occlusion, capture, crash, and device-loss tests with bounded latency and no trust-boundary bypass.
