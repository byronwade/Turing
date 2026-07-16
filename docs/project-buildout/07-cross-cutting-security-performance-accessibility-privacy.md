# Security, Performance, Accessibility, and Privacy Review

Status: detailed research and professional operating baseline  
Owner: security, performance, accessibility, privacy, and architecture owners  
Last researched: 2026-07-16

## Purpose

Prevent teams from optimizing one dimension by externalizing risk to another through a risk-scaled but mandatory cross-cutting review.

## Governing principles

- Review real authority and data flows, not only intended UI.
- Performance evidence uses release-equivalent security and accessibility.
- Accessibility is semantic architecture.
- Privacy starts with minimization and local processing.
- Residual risk has an owner, expiry, affected release, and user consequence.

## Required contract

- Classify changes by trust boundary, hostile input, data sensitivity, critical path, compatibility, accessibility, operations, and reversibility.
- Require threat-model delta, abuse cases, privacy data map, accessibility impact, resource budget, and recovery plan for high-risk work.
- Review CPU, memory, GPU, network, disk, energy, model, and wakeup cost by principal and lifecycle.
- Review keyboard, screen reader, voice, switch, magnification, contrast, motion, localization, and cognitive load.
- Record exceptions in a time-bounded registry with compensating controls and release disclosure.

## Professional workflow

1. Complete impact classification.
2. Select required reviewers.
3. Review design before expensive implementation.
4. Produce negative and failure evidence.
5. Close reviewer conditions.
6. Revalidate high-risk assumptions in release-equivalent builds.

## Evidence and exit gates

- PBO-GATE-11: no release-critical review is conditional or expired.
- Security and accessibility remain enabled in performance results.
- Privacy inventory matches implementation and provider disclosures.
- Every exception has owner, expiry, and remediation.

## Risks and failure modes

- Checklist review can miss emergent interactions.
- Performance pressure can weaken configurations.
- Privacy labels can omit derived data.
- Late accessibility review forces redesign.

## Primary sources

- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- NIST Privacy Framework — https://www.nist.gov/privacy-framework
- NIST Secure Software Development Framework — https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA specification — https://slsa.dev/spec/v1.2/
- Semantic Versioning — https://semver.org/
- JSON Schema 2020-12 — https://json-schema.org/draft/2020-12

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.
