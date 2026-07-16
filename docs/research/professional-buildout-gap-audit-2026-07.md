# Professional Buildout Gap Audit — July 2026

Status: completed repository and operating-model audit  
Owner: program architecture and documentation governance  
Research date: 2026-07-16

## Question

What remained undocumented after the subsystem research, and what is required to build Turing professionally from research through supported release?

## Finding

The existing library is broad across engine, JavaScript, security, performance, AI, DevTools, networking, storage, media, platform, accessibility, release, enterprise, web standards, benchmarking, quality, and product experience. The principal missing layer was not more disconnected browser theory. It was the control plane connecting those books to ownership, decisions, source, verification, release, and maintenance.

## Gaps closed

- evidence-gated phase lifecycle and public maturity rules;
- executable ownership, CODEOWNERS, backup coverage, maintainer ladder, and access reconciliation;
- RFC, ADR, dependency, threat, performance, migration, incident, Plug-in, and embedding review structures;
- requirement-to-source/test/review/evidence/release traceability;
- target workspace, dependency direction, pinned bootstrap, hostile-input coding, concurrency, unsafe, error, and logging rules;
- schema, API, ABI, setting, flag, policy, intervention, telemetry, and version governance;
- unified security, performance, accessibility, privacy, and exception review;
- release, signing, update, rollback, incident, support, legal, data, localization, documentation freshness, funding, capacity, succession, and end-of-life;
- explicit Servo source-strategy decision rather than an ambiguous “baseline” claim;
- native Turing Plug-ins, twenty-workflow first-party research cohort, store, SDK, resource model, and WebExtensions adapter;
- stable Rust/C/generated-SDK embedding contract and host responsibility model;
- machine-readable ownership, traceability, phase, review, and exception records.

## Source-strategy conclusion

Servo is the leading Rust-first modular and embeddable engine reference, but adopting or deriving from it conflicts with current ADR-0002 and REQ-ENG-007. Five options must be compared: clean implementation informed by Servo, selective components, upstream-first collaboration, Servo-derived engine, or explicit charter change. ADR-0009 remains proposed; no Servo-derived release code is authorized.

## Non-claims

This change does not implement or secure a browser, adopt a dependency, establish compatibility/performance leadership, create a Plug-in runtime/store, publish a stable SDK, close risks, complete work packages, or make Turing safe for arbitrary hostile browsing.

## Primary sources

- NIST SSDF — https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA — https://slsa.dev/spec/v1.2/
- NIST Incident Response — https://csrc.nist.gov/pubs/sp/800/61/r3/final
- Servo — https://servo.org/
- WebAssembly Component Model — https://component-model.bytecodealliance.org/
- GitHub CODEOWNERS — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Chrome Extensions — https://developer.chrome.com/docs/extensions/
