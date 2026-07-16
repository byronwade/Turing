# Servo Study

Status: comparative research baseline  
Owner: competitive independent-engine research  
Purpose: Study Rust-first modular engine architecture, embeddability, and safe concurrency while preserving independent Turing decisions.

## Relationship to the Turing program

This study directly informs RQ-01, RQ-04, RQ-05, RQ-06, RQ-13, and RQ-16.

## Project relevance

Servo is the closest established Rust-first engine research peer. Its public goals, repository, governance, components, standards work, and embedding direction provide evidence about Rust browser architecture, parallel style/layout research, graphics, WPT, and maintaining an engine outside a dominant browser vendor.

Current project status, supported features, and architecture must be retrieved at the time of each decision; Turing does not assume historical Servo papers equal current implementation.

## Rust and modularity lessons

Servo demonstrates that parsers, DOM-like structures, style, layout, script, graphics, networking, and embedding can be organized in Rust with explicit component boundaries. Turing should study APIs, unsafe/native boundaries, dependency management, build ergonomics, and contributor onboarding.

The goal is to learn which Rust design patterns scale, not reuse Servo as Turing's release engine.

## Parallelism lessons

Servo's research heritage motivates experiments in parallel style and layout. Turing should not assume parallel is always faster: task granularity, cache locality, memory bandwidth, synchronization, hardware tier, energy, and deterministic debugging matter. A serial correctness oracle and adaptive controller remain required.

Independent subtrees and immutable/versioned artifacts are promising hypotheses.

## Embedding and product lessons

A modular engine can support embeddings, test shells, and multiple product surfaces. Turing's priority remains a general-purpose browser, so embedding APIs cannot weaken browser security, site isolation, updates, accessibility, or developer tooling. A future embedder surface requires separate support and threat decisions.

## Open-source lessons

Servo offers lessons in foundation/community governance, issue labeling, roadmap communication, contribution boundaries, WPT work, build reproducibility, and sustaining specialist subsystems. Turing should measure contributor throughput and ownership rather than assume an open repository automatically creates maintainership.

## Patterns not to copy blindly

Research architecture, feature coverage, product maturity, platform support, and security operations may differ materially from Turing's Chrome-class target. Historical emphasis on parallelism should not become a requirement without current end-to-end evidence. Turing's agent, protocol, and product requirements also differ.

## Experiments

Run compact data-structure, adaptive parallelism, GPU abstraction, embedding boundary, WPT harness, and build/contributor studies. Results must identify exact Servo revision and unsupported workload surface.

## Non-negotiable invariants

- Servo remains an external research reference and differential target.
- Rust-first similarity does not substitute for independent evidence.
- Parallelism is adopted only when end-to-end latency, memory, and energy improve.
- Embedding cannot weaken browser security or support commitments.

## Required evidence

- Pinned Servo revision, official project documentation, and license/provenance record.
- Equivalent runnable corpus with failures and unsupported cases retained.
- Turing-native prototypes for adopted patterns.
- Build, dependency, unsafe, contributor, and platform analysis.

## Known risks and unresolved questions

- Turing can overfit to a fellow research engine rather than production requirements.
- Runnable Servo subsets may not support equivalent workloads.
- Shared Rust ecosystem dependencies can create correlated supply-chain risk.

## Primary sources

- Servo project — https://servo.org/about/
- Web Platform Tests — https://web-platform-tests.org/
- The Rustonomicon — https://doc.rust-lang.org/nomicon/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
