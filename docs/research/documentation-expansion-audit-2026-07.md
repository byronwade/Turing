# Documentation Expansion Audit — July 2026

Status: completed audit and expansion record  
Owner: research and documentation governance  
Purpose: Record where the initial Blueprint was too compressed, what was expanded, and which evidence gaps remain.

## Relationship to the Turing program

This audit is indexed by [Turing Research](README.md), governed by the [documentation policy](../documentation-policy.md), and maps detailed books back to the [Blueprint](../blueprint-v1/README.md).

## Audit scope and method

The audit reviewed the complete Blueprint, repository operating policies, machine-readable registries, prototype documentation, existing engine-landscape study, and the cross-cutting documentation impact map. It asked whether an engineer could move from a high-level goal to a subsystem contract, experiment, threat model, performance metric, API rule, test oracle, and acceptance decision without inventing undocumented assumptions.

The review also compared the documentation topology with the capability surface of production browsers and current independent-engine efforts using official standards, architecture, test, benchmark, platform, and project sources retrieved in July 2026.

## Finding: the Blueprint was broad but too compressed for implementation

The 22 Blueprint chapters correctly covered product, engine, runtime, security, performance, AI, UI, testing, release, risks, and research. The largest gap was depth: a single web-engine or JavaScript chapter could not own every parser, representation, invalidation, compiler, GC, graphics, and diagnostic contract needed for implementation reviews.

Resolution: preserve the Blueprint as the normative overview and add eight indexed engineering books beneath it. Each book links back to its canonical owner and explicitly remains a research/design baseline until accepted evidence changes requirements or ADRs.

## Finding: engine stages needed explicit contracts

The engine chapter described the pipeline but did not provide enough detail for tokenizer state, DOM handles, cascade dependencies, invalidation graphs, formatting contexts, fragment identity, display-list retention, compositor scheduling, text behavior, media limits, editing, accessibility, object-size budgets, or semantic traces.

Resolution: add a ten-document browser-engine book covering pipeline artifacts; HTML/DOM; CSS/cascade/invalidation; layout/fragmentation; paint/compositor/GPU; text/fonts/i18n; images/media/SVG/canvas; input/editing/accessibility; and engine memory/observability.

## Finding: runtime implementation and verification needed separation

The JavaScript chapter established interpreter-first tiering but combined source, bytecode, values, objects, inline caches, GC, host lifetimes, JIT, deoptimization, Web IDL, modules, event loop, WebAssembly, security, tests, and performance into one document.

Resolution: add a seven-document runtime book with separate contracts for front end/interpreter, object model/caches, GC/DOM lifetimes, JIT/IR/deoptimization, web embedding/WebAssembly, and runtime evidence.

## Finding: security needed platform and operations depth

The threat model listed the correct layers but implementers still needed concrete broker rules, macOS/Windows/Linux evidence, unsafe/native governance, allocator/JIT/GPU hardening, privacy/trusted UI, update integrity, incident response, security evidence bundles, severity, waivers, and maturity gates.

Resolution: add a seven-document security-engineering book. It retains the explicit rule that Turing is not safe for hostile or sensitive browsing until platform containment, site isolation, update, response, fuzzing, and independent-review gates pass.

## Finding: developer leadership required a supported protocol product

The existing DevTools chapter described panels and protocol domains but did not fully define protocol layering, target identity, support windows, flow control, causal traces, safe replay, headless equivalence, automation profiles, developer workflow studies, or integrated memory/performance/security diagnosis.

Resolution: add a six-document developer-experience book and a separate five-document API-design book. WebDriver BiDi is the standards-facing layer; Turing-specific introspection remains schema-generated and independent from CDP, with a possible isolated compatibility adapter.

## Finding: performance rules needed an engineering operating system

The 30-tab contract was strong, but allocation budgets, cache policy, semantic ownership, critical-path graphs, adaptive scheduling, queue overload, GPU/energy/startup/recovery work, statistical methods, waiver rules, and public claim expiry needed their own documents.

Resolution: add a six-document performance book linking every headline metric to compatibility, security, process topology, lifecycle, raw samples, tail latency, energy, failure, and recovery.

## Finding: AI safety needed more than permissions

The agent Blueprint had a strong principal/grant foundation but needed implementation-level treatment of semantic snapshots, hidden/cross-origin content, redaction, planning state, working and long-term memory, multi-agent delegation, recovery, provider manifests, local model containment, MCP/tool authority, and combined safety/performance/usability evaluation.

Resolution: add a seven-document AI engineering book. MCP is treated as an untrusted tool/resource transport subordinate to browser grants, not a source of browser authority.

## Finding: competitive research needed durable separation

The initial landscape report synthesized engine lessons, but future work needed stable per-engine studies, browser-product studies, and rules for valid adoption. Product shells and engine architecture were at risk of being conflated.

Resolution: add an eight-document competitive book covering Chromium/Blink/V8, WebKit/JavaScriptCore, Gecko/SpiderMonkey, Servo, Ladybird, Brave/Arc/Zen/Orion/Safari product lessons, and a comparison/adoption scorecard.

## Cross-cutting result

The expansion adds explicit subsystem identities, invariants, evidence requirements, risks, primary sources, related documents, and change discipline. It does not alter the accepted independent-engine, Rust-first, multiprocess, capability-safe, documentation, requirement, risk, or work-package status by itself. No new implementation or benchmark result exists.

The repository validator is strengthened to require the complete engineering-library topology and audit. New documents are indexed from `docs/README.md`, each child is linked from a book index, the Blueprint points to the detailed books, and the repository map owns their locations.

## Remaining high-priority expansion gaps

At the time of this audit, the next audit cycle needed similarly detailed books for networking and Fetch/TLS/cache/cookies; storage/database/migration/recovery; media/PDF/printing/codecs; native platform adapters and browser chrome implementation; accessibility platform bridges and assistive-technology latency; build/release/package/update operations; extensions; enterprise policy/sync; standards feature-dependency graphs; and the fixed-hardware benchmark laboratory.

Those gaps were subsequently expanded by the [Performance, Security, Developer, and Missing-Systems Expansion Audit - July 2026](performance-security-developer-expansion-audit-2026-07.md). The current continuation status is governed by the [Pre-build Readiness Checklist](../project-buildout/11-pre-build-readiness-checklist.md) and [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md), not by this historical first-pass queue.

## Definition of completion for this audit

This audit is complete when all eight books and their chapters exist under `docs/`, every document has an inbound Markdown link, the repository map and top-level indexes describe the topology, the research log records the change, the bibliography includes the new primary-source classes, the research program lists the newly exposed questions, and repository validation passes on `main`.

Completion means a coherent research library exists. It does not mean the designs are implemented, benchmarked, independently reviewed, or frozen.

## Non-negotiable invariants

- The Blueprint remains the normative overview; detailed books do not silently change accepted decisions.
- Research recommendations are not implementation or performance claims.
- Every new document is indexed and included in repository integrity validation.
- Current requirements, risks, and work-package statuses remain unchanged unless their meaning changes.
- Remaining gaps are explicitly queued rather than hidden.

## Required evidence

- Repository-wide Markdown link and inbound-index validation.
- Required-file validation for all detailed book chapters.
- Updated repository map, documentation index, Blueprint index, research index, log, bibliography, and research program.
- No broken legacy paths, secret-like files, or unsupported documentation formats.
- GitHub Actions repository validation after direct-main publication.

## Known risks and unresolved questions

- Documentation breadth can outpace implementation capacity.
- Large research books can become stale without named subsystem owners and evidence refresh.
- Primary-source links and current product/project status can change.
- Detailed proposals can appear more settled than they are; status labels and decision discipline must remain visible.

## Primary sources

- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- WHATWG working mode — https://whatwg.org/working-mode
- Web Platform Tests — https://web-platform-tests.org/
- Speedometer — https://browserbench.org/Speedometer3.1/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
