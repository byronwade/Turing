# 04 — M0–M1: Foundation, Shell, Process, Sandbox, and Resource Laboratory

Status: implementation game plan; completion depends on evidence, not prose  
Owner: program, architecture, security, platform, UI runtime, accessibility, performance, and release operations

## 1. Objective

M0 and M1 establish the trusted foundation on which every later web feature depends. The outcome is not a browser. It is a native, crash-resilient process laboratory with trustworthy identities, bounded IPC, effective sandbox evidence, accessible shell primitives, resource accounting, deterministic traces, and signed research packaging.

## 2. M0 completion sequence

### M0-A — repository and evidence foundation

Complete WP-001 and keep it continuously green:

- pinned toolchain and clean bootstrap;
- root workspace and dependency-direction validation;
- requirements, risks, ADRs, work packages, tasks, evidence, and ownership records;
- dependency, unsafe, native, generated-code, and provenance ledgers;
- repository CI, same-change documentation checks, and clean-tree checks;
- task and agent-run schemas;
- reproducible research artifact conventions.

### M0-B — kernel identities and IPC reference

Complete bounded WP-002 tasks in this order:

1. typed non-zero IDs and restart epochs;
2. generated roles, capabilities, routes, message kinds, and bounds;
3. capability attenuation and process-launch policy oracle;
4. broker-created channels and endpoint binding;
5. exact sequence and operation identities;
6. bounded queues and explicit backpressure;
7. canonical wire-format decision and parser/encoder;
8. timeout, cancellation, terminal response, close, reconnect, and crash state machines;
9. shared-memory lease and handle-transfer contracts;
10. malformed/compromised-sender fuzz and negative harness;
11. per-platform authenticated transport spikes;
12. independent security review and measured queue/transport budgets.

The reference policy remains separable from each OS transport.

### M0-C — decisions and laboratories

In parallel:

- resolve ADR-0009 before production engine source work;
- build the native UI comparison harness without selecting a toolkit prematurely;
- establish reference hardware and controlled corpus definitions;
- prototype profile/session schema formats;
- draft update trust and package identity;
- prepare safe sandbox fixtures and evidence validation.

## 3. M1 work packages

### WP-003 — cross-platform renderer sandbox probes

Stage order:

1. common catalog, evidence schema, redaction, fixture, and unsandboxed control;
2. Linux namespace, `no_new_privs`, seccomp, Landlock, descriptor, environment, working-directory, resource-limit, and broker-disconnect laboratory;
3. Windows token/AppContainer or selected model, job, mitigation, handle inheritance, image loading, network, registry, and broker laboratory;
4. macOS App Sandbox, entitlements, Hardened Runtime, code-signing, XPC/broker, security-scoped grant, helper, and denied-operation laboratory;
5. reproducible independent review on every claimed platform.

A denied operation passes only when evidence identifies an effective OS or authenticated broker enforcement source. Unsupported operations, host ACL failures, and application stubs never count.

### WP-004 — native accessible browser-shell spike

Implement behind toolkit-neutral Rust contracts:

1. window and application lifecycle;
2. profile and Space placeholders;
3. tab strip, address field, command routing, menus, dialogs, and settings shell;
4. typed surface host for synthetic renderer frames;
5. keyboard, focus, pointer, touch where supported, IME, clipboard, drag-and-drop;
6. native accessibility tree and actions;
7. renderer-hang and crash behavior;
8. GPU/device-loss and software fallback behavior;
9. Slint, Vizia, and Floem/GPUI equivalent implementations;
10. measured framework comparison and ADR selection;
11. component tokens, fixtures, inspector, and visual/accessibility regression harness.

Trusted prompts and security indicators cannot be supplied by page content or Plug-ins.

### WP-005 — tab lifecycle, resource attribution, and 30-tab simulator

Implement after the shell contract is usable:

- Active, Background, Frozen, Serialized, Discarded, and Restoring states;
- transition guards, protection reasons, user overrides, and state-loss disclosure;
- synthetic process, DOM, JS, image, media, network, storage, GPU, Plug-in, and agent resource owners;
- physical and attributed memory accounting;
- CPU, wakeup, disk, network, GPU, and model cost attribution;
- 30-tab all-live and mixed-state scenarios;
- pressure injection and recovery;
- revival latency, restored-state quality, and lost-state accounting;
- Resource Truth Center prototype;
- trace export and deterministic replay of lifecycle decisions.

## 4. M1 integration laboratory

The integrated laboratory contains:

- one native shell process;
- browser-kernel policy process or test harness;
- renderer-class synthetic child processes;
- mock network, storage, GPU, and decoder services;
- authenticated bounded control channels;
- platform sandbox configuration and probe execution;
- surface presentation and crash replacement;
- session journal and clean recovery;
- resource and trace viewer;
- signed research package and rollback simulation.

## 5. Required negative scenarios

- renderer hang during navigation and input;
- renderer crash while a permission prompt is visible;
- stale process, channel, view, surface, and document identities;
- malformed, oversized, duplicated, reordered, and unauthorized IPC;
- queue saturation and cancellation races;
- inherited handle, environment, and working-directory leaks;
- denied file, socket, process, debugger, credential, clipboard, device, and platform IPC access;
- GPU device loss and compositor restart;
- disk full during session journal update;
- corrupted session checkpoint;
- upgrade then rollback of a research package;
- 30-tab pressure with protected unsaved work;
- accessibility focus during renderer and shell recovery.

## 6. M1 exit evidence

M1 exits only when:

- every claimed platform has independently reproduced effective sandbox evidence;
- shell remains responsive during synthetic renderer hangs and process pressure;
- trusted UI cannot be spoofed by page surfaces;
- keyboard, screen-reader, IME, high-contrast, and reduced-motion critical flows pass on the reference platform;
- process, tab, Space, and shared resource attribution reconcile;
- lifecycle actions expose state-loss and recovery behavior;
- signed research package install, upgrade, rollback, and profile recovery tests pass;
- all interfaces needed by M2 are versioned and documented;
- no preview or hostile-web safety claim is made.

## 7. Explicit non-goals

M1 does not implement HTML, CSS, JavaScript, Fetch, persistent web storage, media playback, Plug-in compatibility, or general browsing. Synthetic page surfaces are test fixtures, not a hidden existing engine.
