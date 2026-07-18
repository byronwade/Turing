# 12 — M9: Chrome-Class Parity and Continuous Maintenance

Status: continuous program plan; no fixed completion date
Owner: standards, compatibility, all subsystem owners, release operations, security, accessibility, and community governance

## 1. Objective

M9 is the continuing campaign to close long-tail compatibility, performance, enterprise, media, device, localization, accessibility, Plug-in, and developer-tool gaps while maintaining stable users and responding to an evolving web platform.

There is no honest point at which the browser is permanently “done.” Standards, sites, attacks, platforms, hardware, and user expectations continue to change.

## 2. Continuous standards program

- track WHATWG, W3C, TC39, WebAssembly, IETF, Khronos, Unicode, accessibility, and platform developments;
- participate in standards and interoperability work where implementation experience is relevant;
- continuously update WPT, Test262, WebDriver BiDi, and other conformance suites through controlled revision changes;
- publish feature status, denominator, interventions, deprecations, and experimental flags;
- implement features only with multi-implementer interest, user need, security/privacy/accessibility review, and removal strategy;
- upstream tests and specification fixes where appropriate;
- avoid proprietary behavior that fragments the open web.

## 3. Compatibility breadth

The long-tail campaign includes:

- advanced HTML, CSS, SVG, Canvas, WebGPU, WebAssembly, modules, workers, service workers, and device APIs;
- HTTP/2, HTTP/3, QUIC, proxies, enterprise certificates, authentication, and advanced cache behavior;
- internationalization, writing systems, fonts, input methods, printing, PDF, media, WebRTC, and accessibility breadth;
- complex editing, forms, contenteditable, selection, clipboard, drag-and-drop, and platform integration;
- enterprise policy, deployment, managed updates, and identity;
- extension/WebExtensions compatibility and Turing-native Plug-in ecosystem;
- embedding SDK maturity and host conformance;
- top-site/app compatibility with transparent interventions;
- proprietary codecs, DRM, reputation, sync, and platform-service negotiations where strategically justified.

## 4. Performance and efficiency program

- continuous fixed-hardware regression detection;
- startup, binary layout, PGO/LTO, page faults, and executable working-set optimization;
- allocator, virtual-memory, locality, cache, NUMA, heterogeneous-core, and IPC tuning;
- DOM/style/layout/display-list compactness and incremental invalidation;
- JS GC, baseline/optimizing JIT, WebAssembly, and deoptimization improvements;
- network, cache, storage, service-worker, media, and GPU scheduling;
- lifecycle policy, serialization, restoration, and semantic resource ownership;
- energy, thermal, background, and mobile-portability research;
- no optimization without correctness, security, accessibility, and full-workload evidence.

## 5. Security evolution

- exploit-mitigation research and defense-in-depth upgrades;
- new sandbox primitives and platform hardening;
- site-isolation and process-topology refinement;
- heap/JIT/native parser compartments;
- side-channel and timer policy;
- dependency, supply-chain, signing, and update hardening;
- phishing, malicious download, reputation, trusted-UI, Plug-in, DevTools, and agent defenses;
- bug bounty, coordinated disclosure, independent audits, and rapid stable updates;
- regular threat-model and incident-rehearsal refresh.

## 6. Product differentiation program

Market opportunities such as Spaces, Time Machine, Resource Truth, Research Canvas, identity routing, privacy receipts, encrypted collaboration, and continuity enter supported scope only after promotion through requirements, risks, work packages, user studies, security review, and operational ownership.

Features may be rejected, simplified, moved to Plug-ins, or removed when they:

- increase trusted complexity without durable user value;
- undermine privacy, accessibility, interoperability, or performance;
- cannot be maintained safely;
- duplicate a better standards-based solution;
- create service lock-in contrary to portability commitments.

## 7. Platform expansion

A new desktop or mobile platform requires:

- product and business justification;
- qualified primary and backup owners;
- native shell, accessibility, text/input, graphics, sandbox, package, update, crash, credential, device, power, and support evidence;
- hardware and OS test matrix;
- release and incident capacity;
- no reduction in existing platform security or support quality.

Mobile work begins only after desktop boundaries prove portable and staffing can support another security/update surface.

## 8. Governance and sustainability

- maintainers progress through documented review and authority levels;
- ownership, bus factor, funding, infrastructure, and succession are reviewed regularly;
- support scope contracts when capacity declines;
- deprecations include migration and user communication;
- services include export and shutdown plans;
- public roadmaps distinguish research, implementation, preview, beta, stable, deprecated, and unsupported status;
- project health includes contributor experience, review latency, security response, test quality, and documentation freshness.

## 9. Recurring quarterly review

Every quarter or release train reviews:

- requirement and risk status;
- standards and conformance movement;
- top compatibility regressions;
- security findings and patch performance;
- accessibility defects;
- crash and data-loss trends;
- startup, latency, memory, energy, and 30-tab results;
- update and migration success;
- service incidents and costs;
- Plug-in and agent abuse/evaluation results;
- owner capacity and unowned components;
- stale documentation, ADRs, flags, interventions, and exceptions;
- features to add, simplify, delay, move, or remove.

## 10. Success definition

Turing approaches Chrome-class status only when independent evidence shows strong, maintained results across compatibility, security, accessibility, reliability, performance, energy, developer tooling, ecosystem, updates, support, and open-source health. No single benchmark, feature count, or marketing claim establishes parity.
