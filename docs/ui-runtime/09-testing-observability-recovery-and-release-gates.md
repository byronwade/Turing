# Testing, Observability, Recovery, and Release Gates

Status: quality and release plan  
Owner: UI runtime, quality, accessibility, security, performance, and release operations

## Test layers

- pure Rust state and command unit tests;
- generated sequence/property tests for windows, tabs, Spaces, panels, prompts, focus, and recovery;
- adapter contract tests shared by every toolkit candidate;
- component fixtures and semantic snapshots;
- keyboard, focus, accessibility, IME, clipboard, drag/drop, localization, RTL, theme, and density tests;
- screenshot and geometry baselines where semantics are insufficient;
- page-surface, damage, resize, scaling, occlusion, capture, and device-loss tests;
- renderer/UI/GPU crash, restart, memory pressure, OOM, disk-full, and session-recovery tests;
- fixed-hardware startup, update, memory, binary, energy, and 100-tab tests;
- package and clean-system platform tests.

## Native UI inspector

Development builds expose component source, toolkit node, Turing component ID, layout boxes, token/style provenance, bindings, invalidation reason, paint commands, accessibility nodes, input routing, command emission, memory ownership, and update duration. The inspector cannot invoke arbitrary browser-kernel methods.

## Release gates

- **UI-GATE-7:** page surface composition passes resize, scale, crash, occlusion, capture, and device-loss tests.
- **UI-GATE-8:** selected framework passes license, provenance, dependency, unsafe, update, and replacement review.
- **UI-GATE-9:** shell startup, memory, binary, input, frame, energy, and hidden-window budgets pass on the reference platform.
- **UI-GATE-10:** core shell, security prompts, agent stop/confirmation, recovery, and resource workflows pass keyboard and assistive-technology matrices.
- **UI-GATE-11:** normal packages contain no webview, React/JavaScript runtime, runtime UI interpreter, or unused renderer backend.
- **UI-GATE-12:** toolkit upgrade and rollback procedures reproduce from clean source and preserve session/profile compatibility.

## Claim rule

No framework is described as selected, fastest, smallest, native-quality, or accessible until the corresponding gate has current evidence.
