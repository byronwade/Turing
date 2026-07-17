# Framework Landscape and Selection Method

Status: comparative research  
Owner: UI runtime, performance, accessibility, build, security, and legal

## Candidate roles

| Candidate | Proposed role | Principal strengths | Principal uncertainty |
|---|---|---|---|
| Slint | Initial production candidate | Ahead-of-time compilation, compact component storage, stable 1.x API, live preview, native backends, accessibility hooks | Licensing, browser texture composition, some low-level WGPU interfaces unstable, full desktop edge cases |
| Vizia | Styling-oriented comparison | Pure Rust, declarative/reactive model, CSS-like styling, hot reload, permissive license | Pre-1.0 maturity, Skia/native cost, smaller ecosystem |
| Floem | Fine-grained comparison | One-time view-tree construction, signals, virtual lists, flexible renderers, inspector | Project states it is still maturing; API and renderer stability |
| GPUI | High-density performance reference | Proven in Zed, GPU acceleration, command and async architecture | Pre-1.0, frequent changes, broad Zed coupling and licensing review |
| Xilem | Architecture watch | Serious performance focus, retained widget foundations, AccessKit integration | Experimental/pre-alpha status and renderer maturity |
| Makepad | GPU/live-design watch | Rust-first, shader UI, live-editable design language, direct rendering control | Accessibility, native behavior, browser-scale evidence, API maturity |
| Freya | React-like Rust watch | Declarative native Rust, Skia, developer tooling | Active architectural change and native dependency cost |
| egui | Internal tools | Fastest path for inspectors and laboratories, portable pure Rust | Immediate-mode cost and non-native product feel for trusted chrome |
| Restricted TSX compiler | Future escape path | Familiar authoring and zero JS runtime if fully compiled | Building a language, compiler, debugger, tooling, semantics, and long-term compatibility |

## Selection experiment

Implement the same reference shell in Slint, Vizia, and one of Floem or GPUI. The shell contains one window, 100 synthetic tabs, vertical and horizontal modes, a Space selector, address field, split page placeholder, side panel, settings, permission prompt, agent confirmation, resource panel, virtualized history, keyboard navigation, native accessibility, IME, high contrast, reduced motion, renderer-hang simulation, and GPU-device-loss simulation.

## Required measurements

- stripped binary and packaged application contribution;
- cold and warm startup to interactive address field;
- idle and 10/30/100-tab physical memory;
- allocations and p50/p95/p99 update latency for activation, close, reorder, typing, and resource changes;
- resize, scrolling, split-pane, and animation frame pacing;
- text shaping, selection, clipboard, international input, and IME correctness;
- accessibility-tree update latency and platform assistive-technology behavior;
- page-surface composition and damage synchronization;
- UI crash, GPU loss, renderer crash, and state restoration;
- clean build, incremental build, preview/hot-reload time, native dependencies, unsafe surface, license, update cadence, and replacement cost.

## Decision rule

No framework wins from an empty-window microbenchmark. The selected candidate must pass complete product workflows on the reference platform and retain a credible path to Windows, macOS, and Linux. ADR-0014 records the decision only after raw evidence and legal review are public.
