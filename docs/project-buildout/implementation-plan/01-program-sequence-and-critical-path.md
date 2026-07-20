# 01 — Program Sequence and Critical Path

Status: canonical implementation ordering
Owner: program and architecture

## 1. Planning model

Turing is delivered as a set of independently testable systems. Milestones describe product maturity. Work packages describe durable subsystem outcomes. `TASK-*` records describe the smallest units an agent may implement and submit for review.

Milestone dates are not promised before sustained throughput and staffing are measured. Dependency order is mandatory even when calendar work overlaps.

## 2. Critical dependency graph

The accepted work-package graph is:

```text
WP-001 Repository and evidence foundation
  ├── WP-002 Kernel identities, roles, capabilities, bounded IPC
  │     ├── WP-003 Cross-platform renderer sandbox probes
  │     ├── WP-004 Native accessible browser shell spike
  │     │     └── WP-005 Tab lifecycle, resource attribution, 30-tab simulator
  │     ├── WP-012 Navigation transactions and renderer assignment
  │     │     └── WP-013 Scoped HTTP/TLS/cache/cookies
  │     │           └── WP-014 Storage broker and service-worker foundation
  │     │                 ├── WP-017 Signed update, rollback, migration laboratory
  │     │                 └── WP-020 Everyday product surfaces and browser workflows
  │     └── WP-016 Agent reference implementation
  │
  ├── WP-006 HTML tokenizer and tree builder
  │     └── WP-007 DOM arena, mutations, epochs, events
  │           ├── WP-008 CSS parser, selectors, cascade, computed values
  │           │     └── WP-009 Block/text layout, display list, CPU raster
  │           │           ├── WP-015 DevTools, automation, trace viewer
  │           │           └── WP-018 Fixed-hardware laboratory
  │           ├── WP-011 Exact GC and Web IDL bindings
  │           ├── WP-012 Navigation transactions and renderer assignment
  │           └── WP-016 Agent reference implementation
  │
  └── WP-010 JavaScript parser, bytecode, interpreter, Test262
        └── WP-011 Exact GC and Web IDL bindings
              └── WP-019 Baseline JIT and hardened JavaScript execution

WP-015 additionally depends on WP-002.
WP-016 additionally depends on WP-015.
WP-017 additionally depends on WP-001 and WP-002.
WP-018 additionally depends on WP-005 and WP-013.
WP-019 additionally depends on WP-010 and WP-011.
WP-020 additionally depends on WP-004 and WP-012.
```

The machine source is [`backlog.json`](../../blueprint-v1/machine/backlog.json). This diagram must be updated in the same change whenever the machine graph changes.

## 3. Decision gates outside the work-package graph

Some work has a predecessor that is a decision rather than another work package:

- **Engine source gate:** ADR-0009 is accepted before production implementation of WP-006 through WP-009 or import of Servo-derived code. Research-only tokenizers or differential harnesses may proceed without committing the source strategy.
- **UI toolkit gate:** ADR-0013, ADR-0014, licensing review, and equivalent shell evidence precede framework-specific production code in WP-004.
- **Page-composition gate:** ADR-0016 precedes a production compositor/window ownership choice.
- **Native/unsafe gate:** every platform dependency, FFI surface, build script, and unsafe island receives a separate dependency and security review before landing.
- **Stable-scope gate:** ADR-0018 and `PRG-001` precede stable-release commitments.
- **Update-trust gate:** ADR-0019 precedes public update metadata and signing implementation.

## 4. Parallelization lanes

Parallel work is permitted only where inputs are stable enough to avoid speculative coupling.

### Lane A — security and process foundation

WP-002 → WP-003, with sandbox evidence feeding every later hostile-input process.

### Lane B — shell and product laboratory

WP-004 → WP-005. This lane may prototype while the web engine is absent, using synthetic views and renderer-hang fixtures.

### Lane C — static web engine

WP-006 → WP-007 → WP-008 → WP-009. It may proceed in parallel with the shell after ADR-0009, provided page/shell interfaces remain toolkit-neutral.

### Lane D — JavaScript runtime

WP-010 may proceed after WP-001. WP-011 waits for both WP-007 and WP-010 so GC roots, wrappers, and Web IDL are designed against real DOM and runtime contracts. WP-019 waits for WP-010 and WP-011 plus its M6 executable-memory, differential, and no-JIT review gates.

### Lane E — navigation and services

WP-012 → WP-013 → WP-014. This lane waits for kernel identity and DOM lifecycle contracts.

### Lane F — developer tooling and observability

Trace schema research starts early. WP-015 becomes implementation-ready after WP-002 and WP-009 establish process and rendering facts.

### Lane G — operations and measurement

Updater research and benchmark infrastructure start in M0. WP-017 and WP-018 become acceptance-bearing only after their graph dependencies exist.

### Lane H — agents and Plug-ins

Policy schemas and adversarial research can start early. Product-capable agent implementation waits for WP-002, WP-007, and WP-015.

### Lane I — everyday product experience

WP-020 waits for the shell, navigation, and storage/profile foundations from WP-004, WP-012, and WP-014. Its history, bookmarks, downloads, settings, permission, and recovery surfaces remain bounded to the declared profile and product scope.

## 5. Milestone ordering

- **M0:** repository, schemas, task controls, toolchain, provenance, initial kernel contracts, research harnesses.
- **M1:** native shell/process laboratory, sandbox evidence, lifecycle/resource simulator, signed research packages.
- **M2:** script-free static document engine and semantic developer traces.
- **M3:** interpreter-first JavaScript, exact GC, Web IDL, dynamic DOM.
- **M4:** navigation, network, storage, workers, multipage controlled applications.
- **M5:** coherent developer preview with broad layout, DevTools, updates, and accessibility baseline.
- **M6:** baseline JIT, media, Plug-ins, bounded agent preview.
- **M7:** beta hardening, compatibility breadth, independent review, sustained fuzzing.
- **M8:** finite stable release candidate with support and incident capacity.
- **M9:** continuous parity, standards evolution, enterprise breadth, and long-tail optimization.

## 6. Current start point

The accepted `main` baseline permits contained M0 tasks. Branch or pull-request work is not an input until it is independently reviewed and merged. A new agent always starts from accepted `main`, reads the current task registry, and refuses to infer completion from an unmerged branch.

## 7. No leapfrogging rule

A later milestone may prototype an interface, but it cannot claim supported behavior or merge a production dependency that assumes an earlier security, identity, persistence, or update boundary is complete. A visually impressive shell, renderer, agent, or Plug-in is not justification for bypassing the process, sandbox, data-loss, accessibility, or release gates.
