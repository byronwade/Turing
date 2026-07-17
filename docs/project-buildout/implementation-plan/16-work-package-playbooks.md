# 16 — WP-001 Through WP-018 Execution Playbooks

Status: canonical work-package implementation guide  
Owner: program and named subsystem owners

The machine dependency graph in [`backlog.json`](../../blueprint-v1/machine/backlog.json) is authoritative. Each work package is completed through multiple bounded `TASK-*` records. The sections below define the minimum task families and evidence; they are not single-agent assignments.

## Common work-package contract

Every WP has:

- stable purpose and requirements;
- accepted dependencies and entry gates;
- versioned outputs and owners;
- positive, negative, failure, recovery, resource, and compatibility tests;
- security, privacy, performance, accessibility, operational, and documentation evidence;
- explicit unsupported behavior;
- downstream handoff and rollback;
- independent review before acceptance.

## WP-001 — Repository validation and evidence foundation

**Milestone:** M0. **Dependencies:** none. **Requirements:** `REQ-ENG-007`, `REQ-OPS-001`.

**Deliver:** root workspace, pinned toolchain, bootstrap/doctor/check, documentation and schema validation, CI, source hygiene, task/evidence schemas, ownership, traceability, dependency/native/unsafe/generated/provenance ledgers, artifact conventions.

**Task families:** workspace skeleton; toolchain pinning; dependency DAG; documentation validator; same-change enforcement; agent task/run/evidence controls; reproducibility; CI diagnostics; ownership and exception records.

**Acceptance:** clean fresh-host reproduction; all validators pass; no hidden network/build behavior; every durable source path is owned and mapped; failures are visible; generated files are deterministic.

**Negative tests:** missing docs/registry; dependency cycle; unledgered unsafe/native/build script; stale generated file; secret-like file; committed build output; broken links; unauthorized status promotion.

**Handoff:** stable repository contracts for every later WP. **Not supported:** browser functionality or production release.

## WP-002 — Kernel identities, process roles, capabilities, and bounded IPC

**Milestone:** M1. **Dependencies:** WP-001. **Requirements:** `REQ-SEC-003`, `REQ-PERF-004`.

**Deliver:** typed identities/epochs; generated roles/capabilities/messages/routes; process policy oracle; brokered channel registration; canonical wire codec; bounded queues; exact sequencing; cancellation/timeout/close state machines; handle/shared-memory contracts; authenticated platform transports; compromised-sender harness.

**Task families:** ID types; schema generator; envelope; queue; process registry; channel lifecycle; wire codec; fuzzing; Unix/Windows/macOS transport spikes; shared memory; tracing; performance budgets.

**Acceptance:** stale/forged/oversized/unauthorized/reordered inputs fail closed; no capability escalation; transport identity binds to broker record; parser/codec fuzzing passes; platform and queue costs measured; independent security review.

**Negative tests:** zero/reused IDs; stale epochs; duplicate endpoints; sequence gaps; queue overcommit; unknown versions; malformed lengths; handle forgery; peer mismatch; disconnect races.

**Handoff:** IF-001 for WP-003, WP-004, WP-012, WP-013, WP-014, WP-015, WP-016, WP-017. **Not supported:** site isolation or sandbox merely because policy exists.

## WP-003 — Cross-platform renderer sandbox probes

**Milestone:** M1. **Dependencies:** WP-002. **Requirement:** `REQ-SEC-001`.

**Deliver:** safe probe catalog, redacted evidence schema, unsandboxed controls, Linux/Windows/macOS launchers and policies, forbidden-operation probes, effective-enforcement classification, packaged-binary evidence, regression CI.

**Task families:** common harness; fixtures; evidence validator; Linux namespaces/seccomp/Landlock; Windows token/AppContainer/job/mitigations; macOS App Sandbox/Hardened Runtime/entitlements/XPC; broker disconnect; release package verification.

**Acceptance:** all claimed prohibited operations fail through OS or authenticated broker enforcement; positive controls prove the probes work; granted handles/capabilities are enumerated; evidence is reproducible and private-data-free; independent security review reproduces results.

**Negative tests:** unsupported-as-pass; host ACL mistaken for sandbox; inherited descriptors/handles; environment/working-directory leaks; process/debugger/cross-memory access; ambient sockets/files/devices/credentials/clipboard/IPC; policy drift.

**Handoff:** effective sandbox baseline for every hostile process. **Not supported:** platforms without passing evidence.

## WP-004 — Native accessible browser-shell spike

**Milestone:** M1. **Dependencies:** WP-002. **Requirements:** `REQ-PROD-001`, `REQ-PROD-003`, `REQ-A11Y-001`.

**Deliver:** toolkit-neutral state/commands; equivalent framework prototypes; selected reference platform/toolkit ADRs; native windows; tabs/address/commands/settings; surface host; input/IME/clipboard/drag-drop; native accessibility; trusted prompts; crash/GPU recovery; design tokens and component fixtures.

**Task families:** state model; command router; platform window; component system; Slint/Vizia/Floem-or-GPUI comparison; page texture; accessibility bridge; IME; visual/a11y testkit; framework decision and migration plan.

**Acceptance:** shell stays responsive under renderer hang; trusted UI cannot be spoofed; keyboard and AT critical flows pass; page-surface/device-loss recovery works; measured package/startup/memory/input costs; toolkit remains behind replaceable boundary.

**Negative tests:** stale view/surface; renderer-drawn prompt; focus trap; IME cancellation; clipboard leakage; hidden-window wakeups; GPU reset; toolkit crash; high-contrast/reduced-motion failures.

**Handoff:** IF-002 to WP-005 and page engine. **Not supported:** general browsing or framework lock-in without ADR.

## WP-005 — Tab lifecycle, resource attribution, and 30-tab simulator

**Milestone:** M1. **Dependencies:** WP-002, WP-004. **Requirements:** `REQ-PROD-005`, `REQ-PERF-001`, `REQ-PERF-002`, `REQ-PERF-003`.

**Deliver:** lifecycle state machine; protection reasons; process/tab/Space attribution; pressure coordinator; synthetic workload; all-live/mixed-state 30-tab runs; resource viewer; trace/replay; restoration-quality measurement.

**Task families:** state model; accounting schema; synthetic resources; pressure injection; freeze/serialize/discard/restore; user controls; Resource Truth prototype; benchmark exporter.

**Acceptance:** invalid transitions fail; unsaved/call/audio/upload/DevTools/agent protections work; memory reconciles; no hidden discard; revival latency and lost state are reported; shell remains responsive; fixed-hardware baseline is reproducible.

**Negative tests:** pressure race; protected-tab discard; stale restoration; process crash; corrupt serialized state; accounting double charge; shared-resource ambiguity; user override conflict.

**Handoff:** lifecycle/resource contracts to M5/M6 and WP-018. **Not supported:** claims against Chrome without equivalent workloads.

## WP-006 — HTML tokenizer and tree builder

**Milestone:** M2. **Dependencies:** WP-001 plus ADR-0009 decision gate. **Requirement:** `REQ-ENG-001`.

**Deliver:** encoding stream, tokenizer, character references, tree construction, source traces, limits, conformance harness, structured fuzzer, reducer.

**Task families:** decoder; tokenizer states; entity data generation; token types; insertion modes; active formatting; templates; streaming; cancellation/OOM; html5lib/WPT adapter; fuzzing.

**Acceptance:** declared parser corpus passes; invalid/truncated/deep/oversized inputs are bounded; differential failures are reduced; no ambient authority; deterministic token/tree traces.

**Negative tests:** split code units; malformed encodings; entity edge cases; deep nesting; attribute explosion; EOF in every state; cancellation and OOM.

**Handoff:** parser events and documents to WP-007. **Not supported:** scripts or network loading.

## WP-007 — DOM arena, mutation epochs, and events

**Milestone:** M2. **Dependencies:** WP-006. **Requirement:** `REQ-ENG-002`.

**Deliver:** generational handles; node/tree/attribute/text operations; document ownership; mutation epochs; traversal/ranges/selection; event skeleton; form state; accessibility semantic source; wrapper hooks; model tests; memory accounting.

**Task families:** arena; node model; tree validation; mutations; traversal; events; ranges; document lifecycle; forms; AX source; JS binding hooks.

**Acceptance:** arbitrary valid mutation sequences preserve invariants; stale handles fail; teardown releases ownership; epochs invalidate async work; cross-document adoption is explicit; memory is attributed.

**Negative tests:** cycles; double parent; stale handle; mutation during traversal; detached document; event reentrancy; deep tree; OOM; navigation teardown.

**Handoff:** DOM contracts to WP-008, WP-011, WP-012, WP-016. **Not supported:** complete Web IDL or custom elements until scheduled.

## WP-008 — CSS parser, selectors, cascade, and computed values

**Milestone:** M2. **Dependencies:** WP-007. **Requirement:** `REQ-ENG-003`.

**Deliver:** tokenizer/parser; property metadata; selector matching; specificity; origins/layers/inheritance; custom properties; computed values; style invalidation reference; diagnostics; conformance/fuzzing.

**Task families:** tokens; rules/declarations; generated properties; selectors; cascade; variables; computed representation; media queries; invalidation; inspector.

**Acceptance:** declared WPT subset passes; unknown syntax recovers per spec; selector complexity is bounded; full restyle and incremental results agree; cascade reasons are traceable.

**Negative tests:** malformed escapes; nested functions; selector explosion; variable cycles; invalid at-rules; style mutation races; memory pressure.

**Handoff:** stable style input to WP-009. **Not supported:** unimplemented properties through compatibility guesses.

## WP-009 — Block/text layout, display list, and CPU reference raster

**Milestone:** M2. **Dependencies:** WP-008. **Requirements:** `REQ-ENG-004`, `REQ-ENG-005`, `REQ-ENG-006`.

**Deliver:** fragments; sizing; block/inline/replaced layout; Unicode/bidi/shaping adapter; scroll/hit-test/selection; stacking; display list; CPU raster; GPU handoff; AX bounds; traces; differential/pixel tests.

**Task families:** geometry; formatting contexts; intrinsic sizing; line layout; fonts; bidi; fragments; paint properties; display items; raster; hit testing; scrolling; accessibility.

**Acceptance:** full/incremental equivalence; deterministic reference output; international text cases pass for declared subset; pathological complexity is capped; semantic/pixel/geometry tests and traces exist.

**Negative tests:** huge dimensions; deep fragmentation; font failure; bidi extremes; invalid image metrics; stale fragments; GPU loss; zoom/scale changes.

**Handoff:** rendering facts to WP-015 and WP-018. **Not supported:** broad modern layout until added with tests.

## WP-010 — JavaScript parser, bytecode, interpreter, and Test262 harness

**Milestone:** M3. **Dependencies:** WP-001. **Requirement:** `REQ-JS-001`.

**Deliver:** lexer/parser; early errors; bytecode/verifier; interpreter; values/objects/functions/modules subset; realms/intrinsics; exceptions; Test262 runner; differential and fuzz harnesses.

**Task families:** syntax; AST/bytecode; runtime values; objects; environments; functions; classes; modules; promises/async foundations; host hooks; debugger hooks.

**Acceptance:** published feature map meets threshold; invalid bytecode rejected; interpreter is deterministic under reference mode; limits/OOM/cancellation work; differential discrepancies are reduced.

**Negative tests:** parser ambiguity; stack/recursion; integer/length overflow; prototype cycles; exceptions through host boundary; module cycles; microtask explosion.

**Handoff:** runtime contract to WP-011. **Not supported:** JIT or full language until mapped.

## WP-011 — Exact tracing GC and Web IDL bindings

**Milestone:** M3. **Dependencies:** WP-007, WP-010. **Requirements:** `REQ-JS-002`, `REQ-JS-003`.

**Deliver:** exact heap; roots/handles; trace metadata; stop-the-world collector; weak/finalization plan; stress verifier; external memory; IDL parser/generator; wrappers; realm/exposure/security hooks.

**Task families:** heap; allocator; roots; trace; sweep; weak refs; stress mode; wrapper identity; conversions; overloads; exceptions; generated binding tests.

**Acceptance:** repeated navigation/realm teardown has no known root/wrapper leaks; stress mode passes; OOM is recoverable within declared behavior; generated code is deterministic; IDL tests and GC models pass.

**Negative tests:** missing root; stale wrapper; resurrection; finalizer reentrancy; external-memory undercount; cross-realm identity; navigation during callback.

**Handoff:** dynamic DOM/runtime foundation to M4 and JIT. **Not supported:** concurrent/generational GC unless reference-equivalent.

## WP-012 — Navigation transactions, site instances, and renderer swaps

**Milestone:** M4. **Dependencies:** WP-002, WP-007. **Requirement:** `REQ-SEC-002`.

**Deliver:** URL/origin/site; browsing contexts/groups; site instances; navigation intents; renderer assignment; redirects; provisional docs; atomic commits; frames; history; process swaps; initial BFCache; traces.

**Task families:** identity types; origin/site algorithms; transaction state machine; assignment oracle; redirect/commit; history; frames; BFCache; crash/cancel; differential navigation tests.

**Acceptance:** renderer cannot self-commit origin; stale commits fail; cross-site swaps follow policy; history/recovery is deterministic; security state updates atomically; site-isolation tests pass for supported scope.

**Negative tests:** redirect origin change; download disposition; stale user activation; renderer restart; commit race; frame detach; history corruption.

**Handoff:** request/commit context to WP-013 and service integration. **Not supported:** all site-isolation edge cases until tested.

## WP-013 — Scoped HTTP/TLS, cache, cookies, and hermetic server

**Milestone:** M4. **Dependencies:** WP-002, WP-012. **Requirements:** `REQ-NET-001`, `REQ-NET-002`, `REQ-NET-003`.

**Deliver:** request context; DNS/proxy interfaces; socket-owning network service; TLS/cert adapter; HTTP/1.1; Fetch/CORS/security subset; cookies; partitioned cache; downloads; hermetic servers; diagnostics.

**Task families:** URL/request; DNS/proxy; transport; TLS; HTTP parser; decompression; redirects; Fetch filters; CORS/security; cookies; cache; download; DevTools.

**Acceptance:** no renderer socket authority; certificate errors fail safely; request context cannot be forged; partition/cookie/cache tests pass; protocol failures are bounded; secrets are redacted; fixed-hardware costs measured.

**Negative tests:** smuggling/framing; slowloris; truncation; decompression bomb; cert/clock failure; redirect loop; cookie limits; cache corruption; cancellation/retry.

**Handoff:** network service to WP-014 and WP-018. **Not supported:** HTTP/2/3 until separate evidence.

## WP-014 — Storage broker, quota, migrations, and service-worker foundation

**Milestone:** M4. **Dependencies:** WP-002, WP-013. **Requirements:** `REQ-STO-001`, `REQ-STO-002`, `REQ-STO-003`.

**Deliver:** storage keys; local/session storage; IndexedDB subset; Cache Storage; quotas; eviction; origin-private handles; service-worker lifecycle; clear/export/repair; private-session behavior; transactional migrations.

**Task families:** key schema; metadata DB; transaction engine; quota; IDB; cache storage; file handles; service workers; migrations; corruption; clearing; DevTools.

**Acceptance:** cross-profile/origin isolation; disk-full/power-loss/crash tests; migration rollback; quota consistency; corrupt origin quarantine; no renderer paths; user clearing/export works.

**Negative tests:** interrupted commit; corrupted pages/indexes; versionchange races; eviction during transaction; clock change; private-session exit; service-worker update conflict.

**Handoff:** persistence to WP-017 and stable product data. **Not supported:** durability guarantees broader than measured platforms/filesystems.

## WP-015 — Versioned DevTools, automation protocol, and trace viewer

**Milestone:** M2+ integration, productized by M5. **Dependencies:** WP-002, WP-009. **Requirements:** `REQ-DEV-001`, `REQ-DEV-002`, `REQ-DEV-003`.

**Deliver:** target discovery; versioned protocol; Elements/Styles/Layout/AX; Console/Sources; Network/Storage/Security; Performance/Memory; trace viewer; headless; WebDriver BiDi; replay/reduction; SDK generation.

**Task families:** schema; target/auth; events; domains; frontend; headless; virtual time; record/replay; diagnostics; client generation; conformance.

**Acceptance:** protocol reflects engine truth; messages bounded/cancellable; remote attachment authenticated; secrets redacted; clients/conformance tests pass; keyboard/AT frontend paths work; replay divergence visible.

**Negative tests:** stale target/document; unauthorized remote attach; event flood; malformed client; partial trace; secret bundle; headless policy bypass.

**Handoff:** developer/agent observation surface to WP-016 and product preview. **Not supported:** Chrome DevTools Protocol equivalence unless explicitly mapped.

## WP-016 — Capability-safe agent reference implementation

**Milestone:** M6. **Dependencies:** WP-002, WP-007, WP-015. **Requirements:** `REQ-AI-001` through `REQ-AI-005`.

**Deliver:** agent principal; semantic observations; redaction; grants; typed actions; risk classes; deterministic policy; confirmations; isolated task profiles; provider adapters; audit; stop/revoke; adversarial evaluation.

**Task families:** observation schema; grant store; action protocol; policy engine; confirmation UI; provider interface; local model budgets; audit; evaluation; recovery.

**Acceptance:** page/model output cannot expand authority; secrets never enter observations; stale actions fail; Class 3/4 actions cannot bypass confirmation; audit is complete; stop/revoke is immediate; prompt-injection benchmark results disclosed.

**Negative tests:** indirect prompt injection; context poisoning; secret request; cross-origin observation; stale document; replay; confirmation spoofing; provider outage; token/memory exhaustion.

**Handoff:** bounded agent preview. **Not supported:** unrestricted autonomous browsing or consequential stable actions.

## WP-017 — Signed update, rollback, and profile migration laboratory

**Milestone:** M5. **Dependencies:** WP-001, WP-002, WP-014. **Requirements:** `REQ-SEC-004`, `REQ-SEC-005`, `REQ-OPS-001`.

**Deliver:** artifact identity; reproducible package; SBOM/provenance; TUF-style or accepted update metadata; channel delegation; signing separation; staged rollout; rollback; minimum version; profile migration/downgrade; disaster recovery.

**Task families:** package layout; build manifest; signing lab; metadata roles; updater; installer; rollback; migration; key rotation/revocation; compromise drills; release evidence.

**Acceptance:** tamper/replay/freeze/rollback/mix-and-match defenses; interrupted install recovery; known-good rollback; profile transaction and downgrade protection; no agent signing authority; rehearsed key compromise.

**Negative tests:** expired metadata; corrupt artifact; disk full; power loss; clock skew; revoked key; partial mirror; malicious downgrade; incompatible profile.

**Handoff:** developer/beta/stable release channels. **Not supported:** production signing until human ceremony and gates.

## WP-018 — Fixed-hardware compatibility, performance, memory, and energy laboratory

**Milestone:** M5. **Dependencies:** WP-005, WP-009, WP-013. **Requirements:** `REQ-PERF-001`, `REQ-PERF-002`, `REQ-PERF-003`.

**Deliver:** tiered hardware; pinned OS images; offline corpus; local DNS/TLS/HTTP; startup/input/frame/memory/network/storage/energy scenarios; 30-tab workloads; statistics; raw artifacts; regression gating; public claim format.

**Task families:** hardware inventory; image/config capture; corpus; runner; process/lifecycle disclosure; memory reconciliation; power/thermal capture; statistics; dashboards; claim expiry.

**Acceptance:** repeated reproducible results; equivalent security/process/workload settings; raw samples and confidence intervals; no hidden discard; regressions block appropriately; benchmark-specific code rejected.

**Negative tests:** thermal drift; background noise; cache mismatch; lifecycle mismatch; missing process; clock/power measurement failure; cherry-picked samples.

**Handoff:** evidence for every optimization, beta SLO, and product claim. **Not supported:** leadership claims outside measured scope.
