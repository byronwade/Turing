# Ladybird Study

Status: comparative research baseline  
Owner: competitive independent-engine research  
Purpose: Study a visible greenfield browser and engine program without treating pre-release breadth as production evidence.

## Relationship to the Turing program

This study informs project execution, open-source health, and independent-engine research but does not alter the accepted architecture.

## Project relevance

Ladybird is a current greenfield independent browser/engine effort with openly inspectable source, architecture descriptions, development progress, and a from-scratch objective. It is relevant to project sequencing, subsystem ownership, contributor communication, compatibility breadth, and the practical difficulty of building a browser outside existing engines.

Its official project status must be respected; pre-alpha or development builds are not security, compatibility, or performance baselines for production claims.

## Execution lessons

Visible incremental milestones can sustain a large engineering program: parser, layout, runtime, graphics, networking, tooling, and platform work produce testable progress before full compatibility. Turing should likewise create independently useful artifacts and explicit unsupported maps.

However, visible page rendering must not outrun sandbox, site isolation, updates, accessibility, and incident-response documentation.

## Architecture lessons

Turing should study Ladybird's documented process separation, libraries, renderer architecture, JavaScript runtime, event loop, graphics, platform layers, and developer tooling at exact revisions. Similar greenfield goals do not imply its data structures, language choice, or sequencing are correct for a Rust-first capability-secure design.

## Open-source and communication lessons

Regular progress communication, sponsor/foundation models, issue/PR visibility, architecture accessibility, and contributor pathways can grow a community. Turing should pair progress with evidence: WPT/Test262 counts, risks, unsupported behavior, security maturity, and performance manifests.

Open development should not expose active vulnerability details before users are protected.

## Patterns not to copy blindly

Feature breadth, screenshots, demos, or commit velocity are not equivalent to Chrome-class compatibility, safe hostile browsing, accessibility, signed release operations, or sustainable patch response. Site-specific workarounds and implementation shortcuts must be reviewed against standards and long-term cost.

Turing has different language, memory, AI, and developer-protocol objectives.

## Experiments

Track milestone throughput, WPT/Test262 progression, issue ownership, process model, build complexity, supported sites, memory/process behavior when runnable, and contributor success. Do not publish benchmark rankings when feature coverage is materially unequal.

## Collaboration opportunities

Independent engines can cooperate through standards clarification, WPT/Test262 contributions, reduced interoperability cases, shared non-engine test infrastructure, security research, Rust/C++ library improvements where licenses permit, and open benchmark corpora. Collaboration must preserve provenance and Turing's independent implementation boundary.

## Non-negotiable invariants

- Ladybird's stated maturity and unsupported behavior are preserved in comparisons.
- Visual progress is not treated as production safety or parity.
- Turing decisions remain Rust-first and evidence-driven.
- Collaboration occurs through standards, tests, research, and reviewed foundations rather than embedding.

## Required evidence

- Pinned repository/project status and official architecture sources.
- Feature/support denominator and runnable workload disclosure.
- WPT/Test262 and process/security maturity tracking.
- Open-source governance and contributor metrics.

## Known risks and unresolved questions

- Competitive framing can discourage collaboration between independent engines.
- Unequal feature sets make performance comparison misleading.
- Rapidly evolving architecture can make a study stale quickly.

## Primary sources

- Ladybird project — https://ladybird.org/
- Web Platform Tests — https://web-platform-tests.org/
- WHATWG working mode — https://whatwg.org/working-mode

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
