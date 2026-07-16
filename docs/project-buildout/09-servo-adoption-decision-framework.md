# Servo Adoption Decision Framework

Status: detailed research and professional operating baseline  
Owner: engine, architecture, embedding, security, and provenance owners  
Last researched: 2026-07-16

## Purpose

Resolve the conflict between the accepted independent-engine boundary and the desire to use Servo as a baseline through evidence rather than ideology or schedule pressure.

## Governing principles

- Preserve provenance before code experiments.
- Compare total security, compatibility, performance, maintenance, embedding, and governance cost.
- Prefer upstream contribution when shared work remains generally useful.
- Any complete existing engine in the release path requires a superseding ADR and public disclosure.
- Keep the Turing embedding contract independent of internal engine choice.

## Required contract

- Evaluate five options: clean implementation informed by Servo; selective Servo components; upstream-first shared architecture; Servo-derived engine; explicit charter change to a Servo browser.
- Inventory component APIs, unsafe/native surface, process assumptions, WPT status, embedding stability, governance, license, cadence, and LTS/security response.
- Prototype representative parsing, style/layout/paint, offscreen, interactive, and headless paths under equivalent tests.
- Measure startup, interaction, memory, energy, process integration, diagnostics, patch/merge burden, and replacement cost.
- Define which Turing differentiators remain owned: kernel, capabilities, process model, resource attribution, Plug-ins, embedding, DevTools, AI policy, and UI.

## Professional workflow

1. Publish dated Servo inventory.
2. Select representative boundaries.
3. Build prototypes and conformance harnesses.
4. Review security, legal, upstream, and staffing.
5. Write ADR-0009.
6. Update charter, requirements, roadmap, and claims if accepted.

## Evidence and exit gates

- PBO-GATE-15: no Servo-derived release code before ADR-0009.
- Every option has reproducible evidence and maintenance cost.
- No option weakens sandbox or hides unsupported behavior.
- Upstream and patch ownership are explicit.

## Risks and failure modes

- Selective reuse can cost more than a coherent fork.
- A fork can diverge beyond staffing capacity.
- Upstream APIs may conflict with Turing's process model.
- Misleading independence claims would damage trust.

## Primary sources

- Servo — https://servo.org/
- Servo repository — https://github.com/servo/servo
- Servo library release — https://servo.org/blog/2026/04/13/servo-0.1.0-release/
- MPL 2.0 — https://www.mozilla.org/en-US/MPL/2.0/

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.
