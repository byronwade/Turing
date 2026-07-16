# Developer Experience and DevTools Engineering Book

Status: detailed research and design baseline  
Owner: developer tools and automation  
Canonical overview: [Blueprint 11 — product UI, accessibility, and developer experience](../blueprint-v1/11-product-ui-devtools.md)

This book defines how Turing can become a leading browser for developers without making another browser's private protocol its internal architecture. Developer tooling is treated as a supported product surface with compatibility, latency, security, accessibility, and versioning obligations.

## Reading order

1. [Protocol architecture and versioning](01-protocol-architecture-and-versioning.md)
2. [DevTools workflows and UI](02-devtools-workflows-and-ui.md)
3. [Observability, tracing, and replay](03-observability-tracing-and-replay.md)
4. [Automation, headless mode, and reproducibility](04-automation-headless-and-reproducibility.md)
5. [Debugging memory, performance, and security](05-debugging-memory-performance-and-security.md)

## Product thesis

Developers should be able to answer not only what happened, but why. Turing's engine should expose causality for navigation, parser blocking, cascade, invalidation, layout, paint, raster, input, tasks, GC, JIT, network policy, storage, process assignment, sandbox, permissions, extensions, and agents. Tooling derives from stable engine schemas instead of scraping UI or invoking generic privileged methods.

Portable automation belongs in WebDriver BiDi. Turing-specific introspection belongs in a separate schema-generated protocol with explicit stable and experimental domains. A CDP adapter may support ecosystem migration, but CDP must not define Turing's internal object model or authority.

## Developer leadership criteria

- Common debugging tasks are faster and more reliable than in reference browsers under measured studies.
- Every event and command has target identity, document epoch, timing, limits, cancellation, and failure semantics.
- Traces can be captured, redacted, diffed, replayed where deterministic, and attached to issues safely.
- Headless mode uses the same engine, sandbox, network, storage, fonts, and lifecycle as interactive mode.
- Protocol clients are generated for Rust, TypeScript, and Python.
- Remote debugging is authenticated, visible, scoped, and disabled by default.
- Developer tools remain keyboard and screen-reader operable.
- Failures, unsupported domains, breaking changes, and support windows are published.

## Advanced research

6. [Deterministic Replay, Virtual Time, and State Capture](06-deterministic-replay-virtual-time-and-state-capture.md)
7. [Source Maps, Live Editing, and Local Development](07-source-maps-live-editing-and-local-development.md)
8. [Diagnostic Bundles and Automatic Reduction](08-diagnostic-bundles-and-automatic-reduction.md)
9. [Generated SDKs, Plugins, and Compatibility Adapters](09-generated-sdks-plugins-and-compatibility-adapters.md)
10. [Integrated Accessibility, Security, Network, and Storage Debugging](10-integrated-accessibility-security-network-and-storage-debugging.md)

## Related material

- [API design book](../api-design/README.md)
- [Performance engineering book](../performance/README.md)
- [Browser engine book](../engine/README.md)
- [JavaScript runtime book](../javascript/README.md)
- [Security engineering book](../security-engine/README.md)
