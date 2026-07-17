# Native UI Framework Evaluation — July 2026

Status: primary-source research and prototype recommendation; no framework adopted  
Owner: UI runtime, architecture, product, performance, accessibility, platform, security, build, and legal  
Research date: 2026-07-17

## Question

What is the easiest credible way to build Turing’s trusted browser shell with rapid design iteration, a small footprint, native performance, strong structure, accessibility, and no Electron, Tauri, system webview, or shipped React/JavaScript runtime?

## Conclusion

The best current working hypothesis is pure Rust product state and commands with a replaceable native UI adapter. Slint should be evaluated first because its normal model compiles declarative UI ahead of time, stores component elements and properties compactly, exposes stable 1.x APIs and live preview, and offers configurable native backends. It is not selected: licensing and browser-specific surface integration remain blocking.

Vizia should provide a stylesheet-oriented comparison. Floem or GPUI should provide the fine-grained/high-density comparison. Xilem, Makepad, and Freya are promising but currently carry maturity or evidence risk. egui is recommended for internal engineering tools rather than polished trusted chrome. A custom TSX-to-Rust compiler is deferred unless the adapter bake-off proves that existing toolkits cannot satisfy Turing.

## Why not Electron, Tauri, or ordinary React

Electron adds a Chromium and Node runtime. Tauri renders HTML through an operating-system webview using WRY and TAO. Both violate the trusted-shell independence rule. React Compiler performs build-time memoization for React applications; it does not emit native Rust controls or remove React’s runtime model. TypeScript permits implementation-specific JSX transforms, but turning that into a production native UI requires a complete language and tooling program.

## Slint observations

Upstream states that `.slint` files are normally compiled ahead of time and that Rust/C++ generators emit native code. It stores component elements, items, and properties in one memory region to reduce allocations. Slint provides stable 1.x APIs, a language server, live preview, editor integration, multiple renderers, a Winit backend, software rendering, and operating-system accessibility integration.

Risks:

- its licensing choices require written review against Turing’s MPL and distribution goals;
- WGPU texture/custom-platform integration exists but current low-level WGPU paths are feature-gated as unstable;
- FemtoVG has quality tradeoffs and Skia has a heavier footprint;
- browser page surfaces, cross-process accessibility, IME, native menus, capture, device loss, and crash recovery need direct evidence;
- an application-framework success case does not prove browser suitability.

## Comparison observations

### Vizia

A Rust declarative/reactive desktop framework with a styling workflow and permissive licensing. It is attractive for designers familiar with stylesheets. The principal unknowns are pre-1.0 stability, Skia/native build cost, ecosystem size, browser surface composition, and full accessibility/platform evidence.

### Floem

Uses fine-grained reactive signals, constructs the view tree once, provides virtual lists, multiple rendering paths, themes, animations, localization, and a layout inspector. Upstream explicitly says it is still maturing and may make breaking changes before v1.

### GPUI

The framework behind Zed provides a serious high-density application reference, GPU acceleration, commands, async tasks, and testing infrastructure. GPUI is pre-1.0 and tied closely to Zed’s development, so extraction, compatibility, licensing, platform, and maintenance ownership must be measured.

### Xilem and Vello

Xilem is an experimental Rust reactive UI architecture with a performance focus. Vello, used in its graphics stack, identifies itself as alpha and still lists important rendering and GPU-memory work. These are valuable architectural research inputs, not the lowest-risk initial dependency.

### Makepad

Provides a Rust-first GPU runtime, live-editable design language, Studio workflow, and broad targets. It requires stronger evidence for desktop accessibility, text/IME, native window behavior, browser-scale architecture, and stable maintenance.

### Freya

Offers React-like declarative Rust ergonomics with native Skia rendering and developer tools. It remains a watch candidate until API/release stability and native dependency cost are demonstrated.

### egui

Provides a very fast route to native Rust engineering tools and can render wherever textured triangles are available. Its immediate-mode and non-native product goals make it better suited to benchmark dashboards, inspectors, and laboratories than the final browser shell.

## Recommended design workflow

Maintain canonical JSON or schema-backed design tokens, component states, commands, icons, localization, and fixtures. Generate toolkit declarations and Rust constants from those sources. A separate React design lab may consume the same data for rapid visual exploration, but it cannot own product behavior or ship in Turing.

## Required reference-shell experiment

Build equivalent Slint, Vizia, and Floem/GPUI adapters over the same pure Rust model. Include 100 tabs, Spaces, address input, split page texture, side panel, settings, permission and agent prompts, resource manager, virtualization, keyboard, IME, accessibility, high contrast, reduced motion, renderer crash, and GPU loss.

Publish package size, startup, memory, allocations, input latency, frame pacing, accessibility latency, build/iteration time, dependency and unsafe surface, page-surface integration, license, update cadence, and replacement effort.

## Decision output

- ADR-0013: replaceable UI adapter and pure Rust state/command model;
- ADR-0014: selected initial UI toolkit;
- ADR-0015: React design-lab boundary;
- ADR-0016: page-surface/compositor ownership.

## Primary sources

- Slint repository and architecture — https://github.com/slint-ui/slint
- Slint Winit backend and renderers — https://docs.slint.dev/latest/docs/slint/guide/backends-and-renderers/backend_winit/
- Slint platform abstraction — https://docs.slint.dev/latest/docs/rust/slint/platform/
- Slint accessibility roles — https://docs.slint.dev/latest/docs/rust/slint/language/enum.AccessibleRole
- Slint WGPU texture integration — https://docs.slint.dev/latest/docs/rust/slint/platform/femtovg_renderer/struct.FemtoVGWGPURenderer
- Vizia repository — https://github.com/vizia/vizia
- Floem repository — https://github.com/lapce/floem
- GPUI documentation — https://github.com/zed-industries/zed/tree/main/crates/gpui
- Xilem — https://xilem.dev/
- Vello — https://github.com/linebender/vello
- Makepad — https://github.com/makepad/makepad
- Freya — https://freyaui.dev/
- egui — https://github.com/emilk/egui
- Tauri architecture — https://v2.tauri.app/concept/architecture/
- React Compiler — https://react.dev/blog/2025/10/07/react-compiler-1
- TypeScript JSX — https://www.typescriptlang.org/docs/handbook/jsx
