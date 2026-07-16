# Gecko and SpiderMonkey Study

Status: comparative research baseline  
Owner: competitive engine research  
Purpose: Study an independent standards engine, specialized process model, runtime, and extensive diagnostic culture.

## Relationship to the Turing program

This study informs process, runtime, observability, and standards strategy in the detailed engineering books.

## Documented strengths

Gecko and Firefox provide an independent implementation lineage, process specialization, site isolation and remote frames, SpiderMonkey, WebRender/graphics work, standards participation, memory reporting, performance documentation, accessibility, and remote protocols. They are a valuable counterweight to Chromium-shaped assumptions.

The study must distinguish Firefox product architecture, Gecko engine behavior, and platform-specific configuration.

## Independent-engine lessons

Multiple independent engines improve the web by exposing ambiguous specifications and avoiding single-implementation lock-in. Turing should use normative standards, WPT/Test262, multi-engine differential testing, and upstream reduced tests rather than optimize for one engine's quirks.

Compatibility triage should classify Turing defect, specification ambiguity, site bug, test bug, or proprietary dependency.

## Process and graphics lessons

Firefox's process documentation illustrates specialized content, socket, GPU, utility, extension, and other roles. Turing should study how process specialization affects isolation, launch cost, memory, recovery, and diagnostics. WebRender-related architecture is relevant to retained display data and GPU composition, but any adoption requires controlled Rust prototypes and current primary source review.

## SpiderMonkey lessons

SpiderMonkey provides a reference for bytecode/interpreter tiers, optimizing compilation, garbage collection, compartments/realms, WebAssembly, debugging, and memory diagnostics. Turing should compare register/stack/hybrid bytecode, GC spaces, baseline backend, and observability with its own constraints.

Runtime diagnostics and no-JIT/security configurations are product capabilities, not merely internal testing.

## Developer and observability lessons

Firefox's performance and remote-protocol documentation highlights profiling, memory reporting, process visibility, and automation. Turing should pursue a unified causal trace and semantic memory attribution that remains accessible through stable generated APIs.

Protocol compatibility should be measured by developer workflow, not domain count alone.

## Patterns not to copy blindly

Long-lived compatibility and platform code may carry historical complexity. Turing should avoid assuming every abstraction or process role is necessary. Firefox's product choices, telemetry, extension compatibility, and release operations also reflect Mozilla's organizational context.

## Experiments

Compare semantic memory reports, process topology, remote-frame composition, graphics/display representations, runtime diagnostics, developer workflows, and accessibility behavior. Use equivalent versions/configurations and do not infer causation from headline browser metrics.

## Non-negotiable invariants

- Gecko/Firefox is a standards and architecture reference, not a dependency.
- Multi-engine disagreements are resolved against standards and tests.
- Protocol and tooling comparisons use developer outcomes.
- Product and engine observations are not conflated.

## Required evidence

- Official process, runtime, performance, remote, and source documentation.
- Pinned Firefox/Gecko build and configuration in comparisons.
- Controlled Turing representation/process/protocol experiments.
- WPT/Test262 and accessibility comparison.

## Known risks and unresolved questions

- Historical documentation can lag current implementation.
- Firefox product configuration may obscure engine-level causes.
- Independent-engine similarity can lead to accidental design copying without measurement.

## Primary sources

- Firefox process model — https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html
- SpiderMonkey documentation — https://firefox-source-docs.mozilla.org/js/index.html
- Firefox Remote Protocol — https://firefox-source-docs.mozilla.org/remote/index.html

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
