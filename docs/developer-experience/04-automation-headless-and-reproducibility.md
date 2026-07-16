# Automation, Headless Mode, and Reproducibility

Status: research and design baseline  
Owner: automation and test infrastructure  
Purpose: Ensure automation uses the real browser architecture while remaining isolated, deterministic, and portable.

## Relationship to the Turing program

This document expands REQ-DEV-002 and REQ-DEV-003 and the headless section of [Blueprint 11](../blueprint-v1/11-product-ui-devtools.md).

## Same-engine rule

Headless mode uses the same parser, runtime, layout, paint, accessibility, process model, sandbox, network, storage, permissions, lifecycle, and GPU/software paths as interactive mode. Any difference is explicit in capability discovery and test results. A hidden lightweight renderer is prohibited.

Browser chrome may be absent, but trusted decisions are supplied by explicit automation policy rather than silently bypassed.

## Automation profiles

Automation launches isolated ephemeral profiles by default with dedicated storage, credential state, downloads, permissions, extensions, DevTools endpoints, and agent sessions. Attaching to a normal signed-in profile requires explicit local user action and visible state.

Profile directories include ownership/version markers and cannot be reused concurrently by incompatible builds.

## WebDriver BiDi

Portable control follows WebDriver BiDi targets, navigation, script, network, input, log, permissions, and session semantics as implemented. Turing extensions are namespaced and capability-negotiated. WPT webdriver tests and cross-browser fixtures define interoperability evidence.

Legacy or CDP adapters remain optional outer layers and do not bypass BiDi/Turing authorization.

## Deterministic controls

Test profiles can control virtual time, timezone, locale, random seeds, network, DNS, certificates, device metrics, color scheme, reduced motion, CPU, memory pressure, permissions, file handles, process failure, GPU reset, storage faults, and model/provider behavior. Each control is unavailable to ordinary web content and stable interactive profiles.

A result records every enabled control so deterministic test behavior is not presented as normal product behavior.

## Input and stabilization

Automation uses structured input and element actions with target identity, visibility, interactability, user-activation semantics, and current document epoch. Coordinate input is available where needed but does not substitute for semantic targeting.

Waits use lifecycle, DOM/role, network, animation, rendering, or application conditions with deadlines and cancellation. Generic “sleep until it probably works” is discouraged and diagnosed.

## Artifacts and reproducibility

Tests can emit screenshots with metadata, DOM/fragment/paint/accessibility snapshots, console/network logs, traces, video where authorized, crash artifacts, and environment manifests. Artifacts are deterministic enough for review or clearly identify platform-dependent fields.

One command can create a pinned local server, isolated profile, browser build, protocol client, corpus revision, and test invocation.

## CI and scale

Automation workers have CPU, memory, disk, network, browser-process, trace, and artifact budgets. Parallelism respects host capacity and avoids shared profile or port races. Failures preserve the first useful diagnostic state without retaining secrets.

Flaky tests are measured and fixed, not converted into success by retries.

## Non-negotiable invariants

- Headless and interactive modes share the same engine and security machinery.
- Automation uses isolated profiles unless explicit local attachment is approved.
- Deterministic controls are unavailable to arbitrary web content.
- Semantic actions validate target identity, interactability, and document epoch.
- Every result records controls, environment, build, corpus, and unsupported differences.
- Retries do not transform a flaky failure into passing release evidence.

## Required evidence

- WebDriver BiDi WPT results and cross-browser portability tests.
- Interactive/headless semantic and rendering equivalence suites.
- Profile isolation, permission, credential, download, and remote-attachment tests.
- Deterministic replay and fault-injection fixtures.
- CI scaling, artifact, resource, and flake measurements.
- Developer setup-time study from clean checkout to first reproducible failure.

## Known risks and unresolved questions

- Headless-only shortcuts can create false test confidence.
- Powerful deterministic controls can become security bypasses if exposed.
- Platform font/GPU differences can make visual baselines fragile.
- Attaching automation to real profiles can expose sensitive state.

## Primary sources

- WebDriver BiDi — https://w3c.github.io/webdriver-bidi/
- Web Platform Tests — https://web-platform-tests.org/
- Chrome DevTools Protocol — https://chromedevtools.github.io/devtools-protocol/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
