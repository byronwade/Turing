# Goals, Invariants, and Trust Boundary

Status: research baseline  
Owner: UI runtime, architecture, security, product, and platform

## Objective

Deliver polished browser chrome with low startup, memory, binary, energy, and maintenance cost while preserving native accessibility, text input, platform behavior, crash containment, and a rapid design workflow.

## Trusted-state rule

The shell renders trusted state; it does not own the truth. Canonical state lives in typed Rust models owned by the browser kernel and product services. The UI receives bounded snapshots and emits commands. It never receives raw credentials, unrestricted file handles, arbitrary sockets, renderer pointers, or generic privileged IPC.

## Process and failure boundary

The shell must remain usable when page renderers, GPU work, media decoders, Plug-ins, DevTools, or agents crash. The initial spike may run the UI model and platform adapter together for speed of experimentation, but the architecture must retain an explicit boundary so the UI can be isolated or restarted without losing the session journal.

## Working hypothesis

- Pure Rust owns state, commands, policy, persistence, tracing, and recovery.
- A native compiled toolkit owns presentation and local widget behavior only.
- Slint is the first candidate because it ahead-of-time compiles declarative UI, has stable 1.x APIs, live preview, configurable renderers, and compact component storage.
- Vizia is the stylesheet-oriented comparison.
- Floem or GPUI is the fine-grained/high-density performance comparison.
- Xilem, Makepad, Freya, and egui remain monitored or specialized alternatives.
- A custom Turing UI compiler is deferred unless measured toolkit limitations justify its lifetime cost.
- React is allowed only in a separate design lab consuming shared tokens and fixtures.

## Rejection conditions

Reject a candidate if it requires a webview or ambient JavaScript runtime, cannot compose a browser page surface safely, cannot expose native accessibility and IME behavior, prevents crash recovery, has unacceptable licensing, forces multiple heavy renderers, cannot be bounded or instrumented, or cannot be replaced behind a Turing-owned adapter.
