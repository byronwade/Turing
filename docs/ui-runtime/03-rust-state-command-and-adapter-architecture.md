# Rust State, Command, and Adapter Architecture

Status: architecture proposal  
Owner: UI runtime, product, architecture, API, and security

## Layering

```text
browser kernel and product services
        ↓ typed snapshots / events
Turing UI model and command contracts
        ↓ toolkit-neutral adapter
selected native UI toolkit
        ↓ platform and renderer adapters
window system / GPU / accessibility
```

## Crate boundaries

- `turing-ui-model`: pure Rust window, Space, profile, tab, panel, permission, download, resource, agent, Plug-in, settings, and recovery state.
- `turing-ui-contracts`: typed IDs, snapshots, commands, events, errors, deadlines, and cancellation.
- `turing-ui-components`: toolkit-neutral component behavior and fixture definitions where practical.
- `turing-ui-slint` or equivalent: declarative presentation and binding adapter only.
- `turing-ui-platform`: native windows, menus, clipboard, drag/drop, IME, notifications, appearance, and platform capabilities.
- `turing-ui-surfaces`: page, DevTools, media, and offscreen surface composition.
- `turing-ui-assets`: design tokens, icons, localization, and deterministic asset compilation.
- `turing-ui-testkit`: fixtures, fake services, accessibility assertions, screenshots, fault injection, and trace verification.

## Command rule

Toolkits never invoke browser services directly. A button emits a typed command such as `CloseTab { tab_id, expected_epoch }`. The receiving Rust service validates identity, lifecycle, profile, unsaved-work protection, policy, and current epoch before acting.

## State rule

The toolkit receives immutable or versioned snapshots and fine-grained updates. Toolkit-native state is limited to ephemeral visual concerns such as hover, press, local selection, animation progress, and text composition. Durable product state never exists only inside toolkit objects.

## Concurrency rule

The UI thread owns platform event-loop objects. Background services communicate through bounded queues with coalescing, priorities, cancellation, and stale-version rejection. Blocking file, network, model, database, or renderer work is prohibited on the UI thread.

## Replacement rule

No public API exposes Slint, Vizia, GPUI, Winit, Skia, or toolkit object layouts. The adapter may be removed without changing product state formats, commands, trace schemas, embedding contracts, or security decisions.
