# Turing Platform Architecture

Status: owner-directed target architecture; implementation and release adoption remain gated
Owner: architecture, engine, UI runtime, platform, security, performance, accessibility, and developer experience
Last reviewed: 2026-07-22

This document is the canonical architecture contract for evolving Turing into the foundation of Nova. It turns the application-runtime direction into explicit ownership, boundaries, APIs, and migration rules. It does not claim that the runtime, SDK, desktop shell, Servo integration, or any product surface is complete.

## Product shape

Turing is a platform with several products built on the same contracts:

1. **Browser engine platform:** an independent web engine and brokered browser services.
2. **JSX application runtime:** a Turing-owned component and composition runtime that can be authored from JSX-shaped source and compiled to a native, typed runtime representation.
3. **Browser SDK:** versioned Rust APIs, an opaque C ABI, and generated SDKs for embedding and tooling.
4. **Desktop runtime:** windows, surfaces, input, accessibility, lifecycle, packaging, and resource accounting for applications beyond the browser.
5. **Developer platform:** DevTools, traces, profiling, inspection, replay, automation, and diagnostics.
6. **Nova foundation:** shared design tokens, themes, component contracts, workspace primitives, and application lifecycle across future Nova products.

The browser is the first Turing application. It is not a special second UI system.

## Rendering rule

There is one Turing-owned visual composition pipeline for application UI:

```text
JSX or native component authoring
    -> validated component IR
    -> retained component tree and state snapshot
    -> layout, semantics, hit regions, and animation timeline
    -> shared scene/display representation
    -> selected platform compositor and accessibility adapter
```

Browser chrome, tabs, toolbars, sidebars, settings, dialogs, downloads, history, DevTools, context menus, workspaces, and future desktop surfaces all use this pipeline. App-specific renderers are prohibited.

The JSX source is an authoring and visual source of truth, not an authority source. The release runtime must not embed the external npm React package, React DOM, Node, a system webview, or a runtime browser DOM/CSS parser. The intended implementation is a Turing-owned compiler/runtime that produces bounded native component IR and routes behavior through typed Rust state and commands. A future implementation may execute a compatible JSX/React API surface, but compatibility is not permission to import the external implementation.

Operating-system integrations required for security, text input, window management, or accessibility remain adapters at the boundary. They do not create a second application renderer or own browser authority.

## Ownership boundary

| Area | Turing owns | Engine/Servo boundary | Evidence required before promotion |
|---|---|---|---|
| Component runtime | component IR, lifecycle, state synchronization, layout, motion, themes, tokens, variants, hit testing, semantic output | none | runtime contract, deterministic fixtures, accessibility and performance evidence |
| Browser UI | windows, tabs, workspaces, command palette, settings, downloads, history, DevTools surfaces | typed page-surface handles only | UI ADRs, page-surface proof, security and accessibility gates |
| Web content | browser policy, process identity, broker authority, product integration | HTML, CSS, DOM, layout, rendering, scripting, networking, standards behavior according to the accepted engine strategy | ADR-0009, engine conformance, process/sandbox/IPC evidence |
| Browser services | navigation, history, permissions, storage, credentials, network policy, GPU scheduling, tracing, profiling | engine-facing adapters and broker protocols | service contracts, identity/epoch tests, transport and recovery evidence |
| Platform shell | native window, input, IME, clipboard, display, accessibility, packaging | OS APIs through replaceable adapters | platform matrix, manual accessibility workflows, fault and resource evidence |

The requested statement that Servo owns networking is a proposal, not an accepted repository decision. ADR-0009 still governs the source strategy. Until it is accepted, Turing must describe the engine/network ownership split as unresolved and must not import Servo-derived release code.

## Crate and module boundary

The current workspace is a valid M0 decomposition and should be evolved in place:

```text
turing-types
    -> turing-ipc -> turing-kernel
    -> turing-ui-model -> future turing-runtime contracts

turing-html -> turing-css -> turing-layout -> turing-raster/turing-paint
       \\-> turing-dom -> turing-input
turing-gc -> turing-js -> turing-webidl
all engine stages -> turing-engine -> browser/embedding adapters
```

Current audit disposition:

- `turing-ui-model` is the correct owner for the first toolkit-neutral state/command contract. It is not a dead abstraction.
- `turing-chrome` is a reference renderer and Nova visual regression path. It duplicates the future component runtime only at the presentation layer and must be retired or converted after runtime parity evidence exists; deleting it now would remove the current Nova geometry and hit-test reference.
- `turing-browser` is a laboratory presenter with the workspace's only external runtime dependencies, `winit` and `softbuffer`. It is not a product shell and remains useful for visual and compositor experiments.
- `prototype` is a dependency-free invariant executable wired into validation. It is research-only by design, not dead code.
- No current crate is proven obsolete. Removing any of the four research/reference components above would reduce evidence or collapse an authority boundary without a replacement.

Future runtime code must be a Turing-owned module/crate with no dependency on `turing-engine` page semantics. It may consume shared geometry, paint, accessibility, tracing, and platform contracts through narrow interfaces. Do not add a second virtual DOM, page DOM, or toolkit-owned state graph.

## Browser Engine API

The public API is organized by capability and identity rather than by internal structs:

| API family | Core objects | Required invariants |
|---|---|---|
| Windows and surfaces | `WindowId`, `SurfaceId`, `DisplayId` | lifecycle, device generation, resize, scale, occlusion, recovery |
| Tabs and navigation | `TabId`, `NavigationId`, `DocumentEpoch` | origin, profile, frame, epoch, cancellation, commit authority |
| History and workspaces | `HistoryEntryId`, `WorkspaceId`, `SpaceId` | explicit profile scope, transactional updates, recovery |
| Permissions and storage | `PermissionRequestId`, partition keys, storage handles | deny by default, broker ownership, redaction, quota, migration |
| Network and GPU | request contexts, page-surface handles, device generations | policy-issued identity, bounded resources, device-loss recovery |
| Accessibility and UI | semantic snapshots, component IDs, typed commands | one state source, focus/IME correctness, platform adapter replacement |
| Performance and tracing | span IDs, resource-owner IDs, profile snapshots | causality, bounded payloads, redaction, reproducible artifacts |
| DevTools and automation | target IDs, protocol sessions, subscriptions | authentication, backpressure, cancellation, no ambient kernel methods |
| Component and desktop runtime | app IDs, component IDs, runtime leases | capability grants, lifecycle, replacement, versioned IR |

Every API operation declares caller, callee, principal, identity scope, authority, limits, lifetime, deadline, cancellation, retryability, redaction, and compatibility policy. Public embedding uses opaque stable handles and generated schemas; Rust layout is never an ABI.

## Nova design system contract

Nova supplies the shared visual vocabulary:

- semantic colors and themes;
- typography and text-fit rules;
- spacing, density, radii, and responsive constraints;
- motion and reduced-motion variants;
- component variants and interaction states;
- iconography and accessibility naming inputs.

The pinned JSX source and design manifest remain the visual source of truth. Each runtime component must have a stable ID, source-region reference, state/command map, semantic output, fixture matrix, and measured cost. Visual similarity never grants navigation, permission, credential, profile, agent, Plug-in, update, process, IPC, or persistence authority.

## Developer platform

The runtime must expose the same causality model to developers that the browser uses internally. The planned DevTools surface includes page DOM/layout, JSX component tree, Rust state and commands, network and storage, GPU scene/display data, animation timelines, accessibility trees, memory ownership, CPU scheduling, and trace spans. Inspection is read-only by default; mutations require a typed, authenticated, target-scoped protocol.

The first implementation milestone is not a large DevTools UI. It is a stable trace and snapshot vocabulary that can be consumed by a CLI, the browser UI, and future Nova applications without duplicate instrumentation.

## Performance rules

The runtime is optimized around measurable budgets, not framework branding:

- bounded retained trees and event queues;
- stable IDs and structural sharing for unchanged subtrees;
- dirty-region and dependency-aware layout/paint invalidation;
- explicit frame deadlines and cancellation;
- resource accounting by application, surface, component, and process;
- startup and steady-state traces with allocations and wakeups;
- reduced-motion and background scheduling policies;
- deterministic reference output for regression comparison.

No startup, memory, CPU, GPU, battery, responsiveness, or compatibility advantage is claimed until the benchmark lane records hardware, OS, workload, process topology, live/discarded state, sample count, statistics, and artifacts.

## Customization model

Customization is dependency injection at contract boundaries, not mutation of engine internals. Applications may replace tabs, sidebars, themes, layouts, toolbars, command palettes, DevTools, workspaces, animations, icons, and window chrome through versioned component registries and capability-scoped commands. A replacement cannot widen authority, bypass identity checks, access secrets, or create an unbounded resource owner.

## Migration sequence

1. **Contained M0:** freeze this ownership contract, keep `turing-ui-model` and `turing-chrome` as reference surfaces, and add no second renderer.
2. **Runtime contract task:** define the component IR, state/command protocol, semantic tree, invalidation model, animation clock, and trace vocabulary as an approved task with negative tests.
3. **Native runtime proof:** implement a small runtime slice against the current Nova fixture set and compare it with the existing reference renderer across states, accessibility, fault, and performance axes.
4. **Browser composition:** compose chrome and typed page surfaces through the shared scene/compositor contract after `ADR-0013`, `ADR-0014`, `ADR-0016`, and the applicable UI gates are accepted.
5. **SDK and desktop expansion:** freeze versioned capabilities, generate SDKs, add a second application, and prove replacement, lifecycle, packaging, and recovery before calling the runtime a platform.

No step authorizes broad implementation or release claims without an immutable `TASK-*` manifest, independent review, and the relevant evidence bundle.

## AI implementation guidance

An implementation agent must:

- read this contract and the relevant Blueprint/detailed books before changing runtime or engine code;
- keep page content, JSX source, model output, and toolkit events untrusted;
- use typed IDs, snapshots, commands, deadlines, cancellation, and bounded queues;
- add negative tests for stale epochs, authority escalation, malformed component IR, resource exhaustion, cancellation, and renderer/process failure;
- update the Nova source map, design tokens, accessibility fixtures, performance budgets, registries, and roadmap in the same change;
- avoid importing external React/Node/webview code or creating a parallel renderer;
- report prototype, partial, gated, and release status separately.

## Known limitations

The component runtime is not implemented as a release platform. The current engine is a partial research engine, `turing-browser` is local-file laboratory software, the native toolkit and page-surface compositor are unselected, the Servo/source strategy is unresolved, and the browser services/SDK/desktop runtime listed above are contracts and research targets rather than supported APIs.
