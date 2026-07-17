# Slint Adapter, Component Model, and Exit Strategy

Status: candidate-specific research; Slint is not adopted  
Owner: UI runtime, build, performance, accessibility, security, and legal

## Why evaluate Slint first

Slint compiles `.slint` declarations ahead of time into Rust or C++ code, supports stable 1.x APIs, live preview and editor tooling, configurable Winit/rendering backends, operating-system accessibility integration, and compact component storage. These properties align with Turing’s small native shell goals.

## Adapter constraints

The Slint layer may contain component declarations, visual bindings, design tokens, local animation, accessibility metadata, and conversion to typed Turing commands. It may not contain browser policy, profile authority, credential logic, persistence, agent authorization, unrestricted network/file access, or direct renderer process access.

## Feature policy

- Disable default features and compile only the selected backend and renderer.
- Do not ship `slint_interpreter` or runtime `.slint` loading in normal release builds.
- Prefer precompiled components and deterministic assets.
- Evaluate Winit with FemtoVG, WGPU-backed FemtoVG, and software fallback; do not include Skia without measured justification.
- Treat low-level WGPU APIs marked unstable as a decision risk, not a stable contract.
- Validate every accessibility role and platform bridge with real assistive technology.

## Licensing gate

Slint’s GPLv3, royalty-free, and paid options require legal review against Turing’s MPL-2.0 source, redistribution model, attribution expectations, commercial embedding goals, package channels, and contribution strategy. No production dependency is approved before a written license decision.

## Exit strategy

Turing owns state, commands, surface contracts, design tokens, fixtures, traces, and accessibility expectations. Slint-specific code lives in one adapter subtree. A second reference adapter must remain buildable during the decision phase so replacement cost is measured rather than assumed.
