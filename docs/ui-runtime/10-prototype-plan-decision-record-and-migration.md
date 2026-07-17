# Prototype Plan, Decision Record, and Migration

Status: executable research plan  
Owner: UI runtime, program, architecture, platform, performance, accessibility, security, and legal

## Phase A — toolkit-neutral model

Build `turing-ui-model`, `turing-ui-contracts`, fixture services, component-state catalog, command registry, design tokens, and the page-surface protocol without a production toolkit dependency.

## Phase B — three adapters

Implement the reference shell in Slint, Vizia, and Floem or GPUI. Use the same state, commands, fixtures, assets, benchmark harness, platform tasks, and failure tests.

## Phase C — browser-specific spike

Compose simulated renderer textures, route input and IME, combine accessibility, survive renderer and GPU failures, restore state, run 100 tabs, and package the result on the reference platform.

## Phase D — decision

Publish raw results and draft:

- ADR-0013 for the replaceable UI adapter and pure Rust state model;
- ADR-0014 for the selected initial toolkit;
- ADR-0015 for the React design-lab boundary;
- ADR-0016 for page-surface and compositor ownership.

Only ADR-0013 may be accepted before the framework bake-off if its contracts are independently reviewed. The others require experiment evidence.

## Phase E — migration readiness

Keep fixtures and adapter conformance tests independent. Record toolkit-specific state as non-durable. Maintain a feature inventory and migration estimate each milestone. A framework replacement must not change profile, Space, session, command, Plug-in, embedding, or agent data formats.

## Stop conditions

Stop or simplify if framework adaptation consumes more effort than the shell itself, page-surface composition requires unstable private APIs without an ownership plan, accessibility cannot meet release gates, license obligations conflict with distribution, or binary/memory costs erase the product advantage.
