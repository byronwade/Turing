# Pre-build Readiness Gap Audit — July 2026

Status: repository-wide readiness audit; broad implementation is not authorized  
Owner: program, architecture, security, product, UI runtime, platform, build, quality, and documentation  
Audit date: 2026-07-17

## Conclusion

Turing has enough documentation to begin contained M0/M1 architecture spikes, but not enough accepted evidence to begin broad parallel application implementation. The largest previously under-specified area was the trusted browser-shell runtime. This change adds that architecture and converts remaining pre-build unknowns into `PB-001` through `PB-020`.

## P0 before the native shell implementation expands

1. Accept or explicitly time-box the toolkit-neutral UI model and command boundary.
2. Select one reference desktop platform.
3. Complete the three-adapter UI framework bake-off.
4. Prove page-surface composition, input routing, accessibility composition, crash recovery, and GPU device loss.
5. Complete the UI framework license and provenance decision.
6. Accept the Cargo workspace and crate dependency graph.
7. Pin the Rust, native, SDK, linker, Python, Node/tooling, and test-suite environment.
8. Provide bootstrap and doctor commands on a fresh reference machine.
9. Create dependency, unsafe, native, and provenance ledgers.
10. Create design tokens, component inventory, command registry, and fixtures.

## P0 before web-engine implementation expands

- resolve ADR-0009 for the Servo/source relationship;
- generate canonical process capability and IPC schemas;
- implement packaged sandbox probes;
- establish the reference hardware, offline corpus, benchmark runner, WPT/Test262 acquisition, and result storage;
- define profile, Space, session, storage, and migration versioning boundaries;
- keep the page renderer, shell, GPU, network, storage, Plug-in, DevTools, and agent boundaries independently testable.

## Required before a developer preview, not before every prototype

Signed packages, updater rollback, crash symbols, private incident workflows, patch rehearsal, broad platform matrices, telemetry policy, support lifecycle, independent review, and backup maintainers remain preview or later gates. Research prototypes may proceed without pretending these operations exist.

## Other gaps checked

The audit reviewed product requirements, market strategy, engine, JavaScript, networking, storage, media, platform, accessibility, security, performance, DevTools, AI, Plug-ins, embedding, testing, release operations, legal/provenance, ownership, traceability, and documentation governance. No additional top-level subsystem book is required before M1. Remaining work is evidence and executable infrastructure rather than another broad prose category.

## New control

The machine-readable [pre-build readiness registry](../blueprint-v1/machine/pre-build-readiness.json) is the source of truth. A readiness item cannot be marked ready from a design document alone when it calls for source, tests, measurements, legal review, platform evidence, or independent reproduction.

## Kickoff rule

`PB-GATE-0` does not block focused research code. It blocks declaring the repository ready for broad implementation staffing or allowing multiple subsystems to hard-code unresolved interfaces.
