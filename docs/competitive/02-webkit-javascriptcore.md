# WebKit and JavaScriptCore Study

Status: comparative research baseline  
Owner: competitive engine research  
Purpose: Study compact multiprocess integration, platform behavior, and a mature tiered runtime.

## Relationship to the Turing program

This study informs RQ-04, RQ-05, RQ-06, RQ-09, and RQ-16 without changing existing decisions.

## Documented strengths

WebKit's documentation describes WebKit2 multiprocess separation, UI and web processes, network and GPU roles, platform abstraction, site isolation work, testing infrastructure, and JavaScriptCore. Safari/WebKit integration provides a reference for native platform services, power behavior, input, media, accessibility, and distribution.

WebKit is not treated as inherently smaller or faster without equivalent measurement.

## Process and broker lessons

A browser UI process can remain distinct from page execution while brokering navigation, permissions, platform services, and process lifecycle. Turing should use narrow process roles and explicit remote-frame/proxy state. Site isolation, not simply “multiprocess”, is the relevant security requirement.

Platform integration should live behind adapters so native strengths do not leak inconsistent web semantics across systems.

## Rendering and platform lessons

WebKit shows the importance of coordinating engine behavior with native text, input, media, accessibility, graphics, energy, and application lifecycle. Turing should evaluate native versus shared text/raster paths and direct versus abstracted GPU backends by platform.

A compact process topology is useful only if reachable assets and cross-site isolation remain equivalent.

## JavaScriptCore lessons

JavaScriptCore provides a mature reference for interpreter, baseline and optimizing tiers, object representations, garbage collection, WebAssembly, debugging, and platform JIT constraints. Turing should study tier responsibilities and verification patterns while maintaining its own ECMAScript frontend, semantics, object model, GC, bindings, and policy.

Apple platform code-signing and JIT constraints must be designed early, not handled after a compiler exists.

## Testing lessons

WebKit's WPT workflows reinforce pinned revisions, import/export/upstream contribution, expected-result metadata, and platform-specific accounting. Turing should keep unsupported results visible and contribute reduced standards tests upstream.

Platform fidelity cannot excuse divergence from normative web behavior.

## Patterns not to copy blindly

Tight coupling to one vendor's platform services is incompatible with Turing's desktop cross-platform target. System frameworks, process counts, JIT entitlements, energy behavior, and native controls differ across macOS, Windows, and Linux. Turing should not generalize Safari results to WebKit architecture or other platforms.

## Experiments

Measure text stack options, native control policy, startup/process launch, energy/video, site-isolation memory, JIT backend constraints, and accessibility latency across platforms. Compare direct platform adapters with shared abstractions using equivalent features.

## Non-negotiable invariants

- Platform integration cannot silently change web-visible semantics.
- Compact process topology is not accepted at the cost of site isolation.
- JavaScriptCore is a runtime research reference, not embedded code.
- Safari product claims are not generalized to every WebKit build or platform.

## Required evidence

- Official WebKit architecture/testing/source documentation.
- Per-platform Turing prototypes and equivalent measurements.
- WPT/Test262 coverage and platform-difference reports.
- JIT signing, sandbox, accessibility, and energy evidence.

## Known risks and unresolved questions

- Apple-specific success can bias architecture toward unavailable APIs elsewhere.
- Native text/media behavior can create cross-platform inconsistency.
- Site-isolation maturity and platform support can change over time.

## Primary sources

- WebKit documentation — https://docs.webkit.org/
- WebKit2 architecture — https://docs.webkit.org/Deep%20Dive/Architecture/WebKit2.html
- WebKit site isolation — https://docs.webkit.org/Deep%20Dive/SiteIsolation.html
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html
- Apple Hardened Runtime — https://developer.apple.com/documentation/security/hardened-runtime

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
