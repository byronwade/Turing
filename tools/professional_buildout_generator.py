#!/usr/bin/env python3
"""Generate the professional Turing project-buildout documentation and controls."""
from __future__ import annotations

import ast
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-16"


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        raise RuntimeError(f"required file missing: {path}")
    return target.read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_once(path: str, marker: str, content: str) -> None:
    text = read(path)
    if marker not in text:
        write(path, text.rstrip() + "\n\n" + content.strip())


def insert_after(path: str, anchor: str, marker: str, content: str) -> None:
    text = read(path)
    if marker in text:
        return
    if anchor not in text:
        raise RuntimeError(f"anchor missing in {path}: {anchor[:80]}")
    write(path, text.replace(anchor, anchor + "\n" + content.strip(), 1))


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def chapter(title: str, owner: str, purpose: str, principles: list[str], rules: list[str], workflow: list[str], gates: list[str], risks: list[str], sources: list[tuple[str, str]]) -> str:
    return f"""# {title}

Status: detailed research and professional operating baseline  
Owner: {owner}  
Last researched: {DATE}

## Purpose

{purpose}

## Governing principles

{bullets(principles)}

## Required contract

{bullets(rules)}

## Professional workflow

{numbered(workflow)}

## Evidence and exit gates

{bullets(gates)}

## Risks and failure modes

{bullets(risks)}

## Primary sources

{bullets([f'{name} — {url}' for name, url in sources])}

## Status discipline

This document is a research and operating baseline, not an implementation or support claim. Any accepted change must update the owning Blueprint records, requirements, risks, ADRs, source, tests, evidence, and support statements in the same reviewed change.
"""


COMMON = [
    ("NIST Secure Software Development Framework", "https://csrc.nist.gov/pubs/sp/800/218/final"),
    ("SLSA specification", "https://slsa.dev/spec/v1.2/"),
    ("Semantic Versioning", "https://semver.org/"),
    ("JSON Schema 2020-12", "https://json-schema.org/draft/2020-12"),
]

PROJECT = {
"01-program-lifecycle-and-phase-gates.md": chapter(
    "Program Lifecycle and Phase Gates", "program, architecture, security, quality, and release owners",
    "Define an evidence-gated path from research through prototype, preview, beta, stable release, maintenance, and end-of-life. The existing M0–M9 roadmap remains the product sequence; this chapter makes entry, exit, stop, rollback, and claim rules explicit.",
    ["Maturity is earned from current evidence, not schedule, feature count, screenshots, or publicity.", "A later feature cannot bypass an earlier security, data-integrity, accessibility, or update boundary.", "Every phase has an owner, entry criteria, exit evidence, stop conditions, rollback path, and prohibited claims.", "Staffing and emergency-patch capacity are release evidence.", "A passed gate can be reopened when its assumptions are invalidated."],
    ["Maintain machine-readable status for M0 through M9.", "Every gate packet includes requirement status, risks, ADRs, conformance, fuzzing, security, accessibility, performance, reliability, operations, legal readiness, staffing, and unsupported behavior.", "Decisions are continue, continue with scope reduction, hold, rollback, or cancel.", "Waivers identify approver, scope, compensating controls, release disclosure, and automatic expiry.", "Security isolation, update verification, credential separation, and misleading maturity claims are non-waivable."],
    ["Confirm entry criteria and ownership.", "Execute the implementation and evidence plan.", "Run subsystem and cross-cutting reviews.", "Assemble exact-commit evidence.", "Record go/no-go and dissent.", "Update status, public claims, roadmap, and next-phase plan atomically."],
    ["PBO-GATE-1: public maturity label matches machine status.", "PBO-GATE-2: all prerequisite trust boundaries pass before the next phase.", "Rollback or scope-reduction is exercised for irreversible changes.", "No release-critical requirement is complete without evidence."],
    ["Process can become performative if records are not derived from evidence.", "Single-maintainer approval creates blind spots.", "Waivers can become permanent through inertia.", "Overbroad phases can block indefinitely and need evidence-domain decomposition."], COMMON),
"02-ownership-codeowners-and-maintainer-ladder.md": chapter(
    "Ownership, CODEOWNERS, and Maintainer Ladder", "program and governance owners",
    "Convert conceptual roles into an executable ownership model for every subsystem, document, schema, test suite, benchmark, release artifact, service, and incident path.",
    ["Ownership is responsibility for maintenance, incidents, deprecation, and outcomes—not exclusive control.", "CODEOWNERS routes review but does not prove competence.", "No supported subsystem has a bus factor of one.", "Unowned and provisional scopes remain visible.", "Access is least-privileged and reconciled with current responsibility."],
    ["Record primary, backup, architecture, security, accessibility, performance, release, and documentation reviewers.", "Define contributor, reviewer, subsystem maintainer, security maintainer, release maintainer, and program-owner levels.", "Document promotion, probation, recusal, inactivity, removal, succession, and emergency replacement.", "Use two-person control for stable signing, update trust, supported-version changes, and irreversible migrations.", "Review ownership and access quarterly and before every release phase."],
    ["Propose scope and evidence.", "Review coverage and conflicts.", "Update ownership registry, CODEOWNERS, escalation, and support matrix together.", "Reconcile GitHub, CI, signing, package, disclosure, and service access.", "Expire provisional assignments unless reaffirmed."],
    ["PBO-GATE-3: no beta/stable subsystem is ownerless or single-owner.", "Critical scopes have tested escalation and backup coverage.", "CODEOWNERS patterns match representative paths.", "Departed maintainers retain no privileged access."],
    ["A global wildcard can mask ownership gaps.", "Too-granular ownership creates review bottlenecks.", "Stale access survives social role changes.", "Titles without operational duties create false assurance."], [("GitHub CODEOWNERS", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"), ("GitHub rulesets", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets"), ("Developer Certificate of Origin", "https://developercertificate.org/")]),
"03-rfc-adr-and-design-review-process.md": chapter(
    "RFC, ADR, and Design-Review Process", "architecture and subsystem owners",
    "Create one discoverable decision pipeline for architecture, public APIs, data formats, dependencies, security boundaries, performance strategy, deprecation, and operations.",
    ["Use the smallest sufficient artifact, but durable choices need durable review.", "Alternatives, uncertainty, dissent, and rejected options remain visible.", "Accepted ADRs are immutable and changed through supersession.", "Experiments do not become architecture merely because a prototype works.", "Security and accessibility concerns require explicit risk ownership."],
    ["Classify work as routine, design note, RFC, ADR, security review, incident emergency, or compatibility intervention.", "Require RFCs for new subsystems, stable APIs, profile formats, Plug-in capabilities, embedding contracts, telemetry, sync, and major dependencies.", "Require ADRs for trust boundaries, languages, source strategy, long-lived formats, release trust, license model, and irreversible compatibility promises.", "Assign stable ID, state, owner, reviewers, comment period, implementation issue, and supersession chain.", "Keep proposal, experiment, accepted, implemented, verified, and supported states distinct."],
    ["Start from the indexed template.", "Classify decision and reviewers.", "Collect prototypes or research where empirical.", "Review every cross-cutting dimension.", "Record outcome and dissent.", "Link implementation.", "Verify assumptions after implementation."],
    ["PBO-GATE-4: no irreversible decision exists only in chat, commit, or code review.", "Required reviewers and alternatives are complete.", "Migration and rollback are linked.", "Decision status agrees across index, issues, code, and docs."],
    ["Excess process drives decisions into side channels.", "Consensus can delay urgent work.", "An ADR can overstate weak evidence.", "Retrospective records can rationalize instead of preserve facts."], [("Architecture Decision Records", "https://adr.github.io/"), ("Rust RFC process", "https://rust-lang.github.io/rfcs/"), ("IETF RFC 7282", "https://www.rfc-editor.org/rfc/rfc7282")]),
"04-requirements-traceability-and-evidence.md": chapter(
    "Requirements Traceability and Evidence", "quality, architecture, and documentation owners",
    "Define the authoritative chain from user need to requirement, design, source, tests, evidence, release gate, supported status, and current owner.",
    ["A requirement without verification is an intention.", "Evidence identifies exact commit, build, environment, configuration, and result.", "Negative, failure, recovery, security, and accessibility evidence are first-class.", "Unsupported, crash, timeout, and not-run outcomes remain visible.", "Traceability is generated from stable IDs, not an unaudited spreadsheet."],
    ["Link every requirement to owner, milestone, RFC/ADR, risks, source scopes, tests, conformance, fuzz targets, benchmarks, reviews, release gates, and evidence.", "Represent specified, implemented, verified, release-gated, and supported separately.", "Record platforms, configurations, freshness, expiry, and limitations.", "Validate references in both directions.", "Allow access-controlled references for embargoed security evidence without hiding debt."],
    ["Create or change requirement and owner.", "Add design and risk links.", "Register source and verification plan.", "Attach evidence as work completes.", "Run CI validation.", "Reconcile stale and waived evidence at milestones.", "Invalidate evidence when code or assumptions change."],
    ["PBO-GATE-5: every release-critical requirement has current evidence.", "No supported claim points only to prose.", "Evidence build IDs match released artifacts.", "No release requirement lacks owner or verification method."],
    ["Traceability can become enormous; generate views instead of duplicating records.", "A passing test can prove the wrong behavior.", "External suite revisions can invalidate interpretation.", "Embargoed evidence needs controlled visibility."], COMMON),
"05-repository-build-toolchain-and-coding-standards.md": chapter(
    "Repository, Build, Toolchain, and Coding Standards", "architecture, build, security, and language owners",
    "Define the final workspace, dependency direction, reproducible developer environment, and hostile-input coding rules before implementation sprawls across incompatible conventions.",
    ["Crates follow ownership, privilege, replacement, and failure boundaries.", "Privileged code is smaller and more stable than hostile-input code.", "Stable Rust is the default; C ABI and native/platform boundaries are explicit.", "Every untrusted size, count, depth, duration, queue, and allocation is bounded.", "Cancellation, timeout, crash, restart, and OOM are ordinary control paths."],
    ["Use a Cargo workspace organized into apps, crates, platform, schemas, tests, testdata, benchmarks, infra, security, and tools.", "Record each crate's owner, privilege, inputs, public status, unsafe allowance, platforms, resource budget, and failure boundary.", "Machine-check forbidden dependency edges and cycles.", "Pin Rust, C/C++, SDK, linker, Python, Node, generator, test-suite, and package-tool versions.", "Provide bootstrap and read-only doctor commands plus offline verified-source builds.", "Use typed IDs, checked arithmetic, bounded channels/collections, explicit lock ordering, structured errors, redacted structured logs, and SAFETY rationale for unsafe code.", "No general-purpose runtime or framework becomes browser-wide by convenience."],
    ["Approve workspace and component map.", "Create skeleton crates and ownership metadata.", "Add dependency graph and toolchain pinning.", "Exercise bootstrap on fresh macOS, Windows, and Linux hosts.", "Enforce format, lint, Miri/sanitizer/fuzz/property/model tests.", "Review topology each milestone."],
    ["PBO-GATE-6: every production crate has ownership and privilege metadata.", "PBO-GATE-7: fresh-host bootstrap is reproduced by someone other than its author.", "PBO-GATE-8: unsafe and concurrency inventories reconcile with source.", "Release compilation has no undeclared network access."],
    ["Too many crates increase compile and coordination cost.", "Too few create broad authority and coupling.", "Pinned tools can retain vulnerabilities.", "Safe Rust wrappers can hide unsound native contracts."], [("Cargo workspaces", "https://doc.rust-lang.org/cargo/reference/workspaces.html"), ("Rust 2024 edition", "https://doc.rust-lang.org/edition-guide/rust-2024/"), ("Rust API Guidelines", "https://rust-lang.github.io/api-guidelines/"), ("Reproducible Builds", "https://reproducible-builds.org/docs/")]),
"06-api-schema-configuration-and-version-governance.md": chapter(
    "API, Schema, Configuration, and Version Governance", "API/protocol, product, enterprise, and security owners",
    "Apply one governance model to IPC, shared memory, profile formats, DevTools, automation, agents, Plug-ins, embedding, settings, policies, commands, telemetry, traces, and error codes.",
    ["Schemas describe identity, authority, limits, cancellation, failure, and compatibility—not only field shapes.", "Stable identifiers are never reused.", "Unknown and downgrade input fails safely.", "Internal and public compatibility promises are distinct.", "Experiments expire and cannot silently become permanent."],
    ["Maintain catalog fields for owner, version, stability, producer, consumer, limits, data class, and support window.", "Define additive, breaking, experimental, deprecated, and security-removal changes.", "Require version negotiation, capability discovery, bounded messages, deadlines, cancellation, backpressure, and structured errors.", "Registry every setting, flag, enterprise policy, command-line switch, intervention, test hook, rollout, and emergency control.", "Define deterministic precedence across build, channel, enterprise, profile, site, session, process, and test.", "Ordinary settings cannot disable mandatory sandbox, site isolation, certificate, update, or confirmation controls."],
    ["Identify owner and consumers.", "Review malformed, compatibility, data, and downgrade behavior.", "Generate types, docs, fixtures, and conformance tests.", "Run old/new matrices.", "Ship diagnostics and migration.", "Remove expired flags and old paths."],
    ["PBO-GATE-9: every public/stable interface has a compatibility owner.", "PBO-GATE-10: release manifests enumerate all behavior-affecting configuration.", "Unknown fields and values fail safely.", "Effective policy is explainable from source to result."],
    ["Generic privileged APIs become escape hatches.", "Version negotiation can be downgraded.", "Flag combinations create untested products.", "Long support windows can block security changes."], COMMON),
"07-cross-cutting-security-performance-accessibility-privacy.md": chapter(
    "Security, Performance, Accessibility, and Privacy Review", "security, performance, accessibility, privacy, and architecture owners",
    "Prevent teams from optimizing one dimension by externalizing risk to another through a risk-scaled but mandatory cross-cutting review.",
    ["Review real authority and data flows, not only intended UI.", "Performance evidence uses release-equivalent security and accessibility.", "Accessibility is semantic architecture.", "Privacy starts with minimization and local processing.", "Residual risk has an owner, expiry, affected release, and user consequence."],
    ["Classify changes by trust boundary, hostile input, data sensitivity, critical path, compatibility, accessibility, operations, and reversibility.", "Require threat-model delta, abuse cases, privacy data map, accessibility impact, resource budget, and recovery plan for high-risk work.", "Review CPU, memory, GPU, network, disk, energy, model, and wakeup cost by principal and lifecycle.", "Review keyboard, screen reader, voice, switch, magnification, contrast, motion, localization, and cognitive load.", "Record exceptions in a time-bounded registry with compensating controls and release disclosure."],
    ["Complete impact classification.", "Select required reviewers.", "Review design before expensive implementation.", "Produce negative and failure evidence.", "Close reviewer conditions.", "Revalidate high-risk assumptions in release-equivalent builds."],
    ["PBO-GATE-11: no release-critical review is conditional or expired.", "Security and accessibility remain enabled in performance results.", "Privacy inventory matches implementation and provider disclosures.", "Every exception has owner, expiry, and remediation."],
    ["Checklist review can miss emergent interactions.", "Performance pressure can weaken configurations.", "Privacy labels can omit derived data.", "Late accessibility review forces redesign."], [("WCAG 2.2", "https://www.w3.org/TR/WCAG22/"), ("W3C Ethical Web Principles", "https://www.w3.org/TR/ethical-web-principles/"), ("NIST Privacy Framework", "https://www.nist.gov/privacy-framework"), *COMMON]),
"08-release-incident-legal-data-and-support.md": chapter(
    "Release, Incident, Legal, Data, and Support Operations", "release, security, legal, privacy, support, and platform owners",
    "Turn release principles into executable build, signing, update, rollback, migration, incident, data, legal, support, and end-of-life operations.",
    ["A supported release is an operational commitment.", "Users must recover from bad binaries, updates, profiles, dependencies, and services.", "Every distributed byte has known source and license.", "Every remote field has purpose, owner, retention, and deletion.", "Runbooks are exercised before incidents."],
    ["Maintain channel policy, platform matrix, security-patch target, support SLA, and EOL.", "Provide runbooks for exploitation, sandbox escape, signing compromise, dependency zero-day, credential leak, cross-profile leak, data loss, malicious Plug-in/provider, certificate failure, service outage, and rollback.", "Use reproducible unsigned builds, provenance, SBOM, notices, symbols, hardware-backed or threshold signing, staged rollout, rollback, and minimum secure versions.", "Maintain data inventory for profile, crash, update, telemetry, sync, Plug-ins, AI providers, diagnostics, and support bundles.", "Complete MPL/DCO-or-CLA, third-party, trademark, patent, media/codec/DRM, export, privacy, accessibility, app-store, and distribution review.", "Publish code of conduct, safe-harbor intent, moderation, and incident communication."],
    ["Build from protected commit and independent environments.", "Complete cross-cutting release evidence.", "Approve rollout and thresholds.", "Exercise rollback and migration.", "Run incidents with severity and command structure.", "Publish postmortem and systemic actions."],
    ["PBO-GATE-12: beta/stable has exercised emergency patch and communication paths.", "PBO-GATE-13: broad contribution and distribution wait for legal/provenance review.", "Every remote event is registered and tested for deletion.", "On-call, signing, domain, CI, and package recovery are tested."],
    ["Rollback can reintroduce known vulnerabilities.", "Crash data can contain secrets.", "Legal duties vary by jurisdiction.", "Runbooks and service ownership can stale."], [("NIST Incident Response SP 800-61 Rev. 3", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"), ("The Update Framework", "https://theupdateframework.io/"), ("Mozilla Public License 2.0", "https://www.mozilla.org/en-US/MPL/2.0/"), ("REUSE specification", "https://reuse.software/spec/")]),
"09-servo-adoption-decision-framework.md": chapter(
    "Servo Adoption Decision Framework", "engine, architecture, embedding, security, and provenance owners",
    "Resolve the conflict between the accepted independent-engine boundary and the desire to use Servo as a baseline through evidence rather than ideology or schedule pressure.",
    ["Preserve provenance before code experiments.", "Compare total security, compatibility, performance, maintenance, embedding, and governance cost.", "Prefer upstream contribution when shared work remains generally useful.", "Any complete existing engine in the release path requires a superseding ADR and public disclosure.", "Keep the Turing embedding contract independent of internal engine choice."],
    ["Evaluate five options: clean implementation informed by Servo; selective Servo components; upstream-first shared architecture; Servo-derived engine; explicit charter change to a Servo browser.", "Inventory component APIs, unsafe/native surface, process assumptions, WPT status, embedding stability, governance, license, cadence, and LTS/security response.", "Prototype representative parsing, style/layout/paint, offscreen, interactive, and headless paths under equivalent tests.", "Measure startup, interaction, memory, energy, process integration, diagnostics, patch/merge burden, and replacement cost.", "Define which Turing differentiators remain owned: kernel, capabilities, process model, resource attribution, Plug-ins, embedding, DevTools, AI policy, and UI."],
    ["Publish dated Servo inventory.", "Select representative boundaries.", "Build prototypes and conformance harnesses.", "Review security, legal, upstream, and staffing.", "Write ADR-0009.", "Update charter, requirements, roadmap, and claims if accepted."],
    ["PBO-GATE-15: no Servo-derived release code before ADR-0009.", "Every option has reproducible evidence and maintenance cost.", "No option weakens sandbox or hides unsupported behavior.", "Upstream and patch ownership are explicit."],
    ["Selective reuse can cost more than a coherent fork.", "A fork can diverge beyond staffing capacity.", "Upstream APIs may conflict with Turing's process model.", "Misleading independence claims would damage trust."], [("Servo", "https://servo.org/"), ("Servo repository", "https://github.com/servo/servo"), ("Servo library release", "https://servo.org/blog/2026/04/13/servo-0.1.0-release/"), ("MPL 2.0", "https://www.mozilla.org/en-US/MPL/2.0/")]),
"10-product-localization-documentation-and-sustainability.md": chapter(
    "Product, Localization, Documentation, and Sustainability", "product, accessibility, localization, documentation, community, and program owners",
    "Define the design system, trusted content, localization, documentation freshness, staffing, funding, infrastructure, succession, and safe scope reduction required to sustain the browser.",
    ["Trusted state is unmistakable and resistant to page imitation.", "Every component defines loading, empty, error, offline, crash, stale, and recovery states.", "Examples and commands are tested where practical.", "Supported scope cannot exceed patch, test, release, and communication capacity.", "Funding and material conflicts are disclosed."],
    ["Maintain design tokens, component catalog, command/shortcut registry, trusted-surface rules, semantic/focus behavior, performance budget, and spoofing analysis.", "Maintain localization IDs, translator context, plural/gender, locale fallback, bidi, pseudo-localization, and security-language review.", "Require document owner, status, last/next review, applicable versions, evidence dependencies, and supersession.", "Validate examples, links, anchors, IDs, sources, and stale claims.", "Model staffing, backup, on-call, audits, CI/fuzz hardware, signing, distribution, support, standards, legal, Plug-in services, and AI providers by phase.", "Reduce supported scope when capacity evidence fails; define maintenance, archive, and EOL modes."],
    ["Map product need to workflow and trusted-state review.", "Prototype all states.", "Run keyboard, assistive-technology, localization, and comprehension studies.", "Test docs/examples in CI.", "Review capacity quarterly.", "Update support or reduce scope when obligations exceed capacity."],
    ["PBO-GATE-14: release docs match the shipped build.", "PBO-GATE-16: stable has an owned design and localization pipeline.", "PBO-GATE-18: scope is reduced when sustained capacity fails.", "No critical service or account depends on one person."],
    ["Custom UI can lag native behavior.", "Localization can alter security meaning.", "Metadata can be rubber-stamped.", "Funding or burnout can interrupt security response."], [("WAI-ARIA Authoring Practices", "https://www.w3.org/WAI/ARIA/apg/"), ("Unicode CLDR", "https://cldr.unicode.org/"), ("Write the Docs: docs as code", "https://www.writethedocs.org/guide/docs-as-code/"), ("CHAOSS metrics", "https://chaoss.community/kb-metrics-and-metrics-models/")]),
}

PROJECT_INDEX = """# Professional Project Buildout and Operating Handbook

Status: detailed research and professional operating baseline  
Owner: program architecture and engineering operations  
Last researched: 2026-07-16

This handbook is the control plane for turning Turing's research into a multi-year, multi-maintainer implementation. It defines who decides, how work becomes accepted, how evidence is traced, how the repository is structured, how contributors reproduce the environment, and how the product is released and maintained.

## Reading order

""" + "\n".join(f"{i}. [{name.removesuffix('.md').replace('-', ' ').title()}]({name})" for i, name in enumerate(PROJECT, 1)) + """

## Machine-readable companions

- [Ownership](../blueprint-v1/machine/professional-owners.json)
- [Requirements traceability](../blueprint-v1/machine/professional-traceability.json)
- [Phase gates](../blueprint-v1/machine/professional-phase-gates.json)
- [Review rules](../blueprint-v1/machine/professional-review-rules.json)
- [Exceptions](../blueprint-v1/machine/professional-exceptions.json)

## Non-negotiable rule

A phase or release is incomplete while an applicable control lacks linked evidence, a time-bounded approved exception, or an explicit declaration that it is outside supported scope.
"""

TECH = """# Technology Stack and Engineering Toolchain

Status: candidate evaluation and operating baseline; no dependency approval  
Owner: architecture, build, security, and subsystem owners  
Last researched: 2026-07-16

## Decision model

“Best” means the lowest total cost across correctness, memory safety, latency, memory, energy, accessibility, interoperability, portability, licensing, build/release operations, maintainer health, and replacement—not popularity or one benchmark.

## Language map

| Layer | Preferred language | Rule |
|---|---|---|
| Browser kernel, IPC, engine, JS semantics, network/storage policy, resource model, Plug-in broker, DevTools protocol, agent authorization | Stable Rust, Rust 2024 edition | Default for Turing-owned runtime and hostile-input code |
| Universal public ABI | C | Opaque handles, explicit ownership, version negotiation; not the implementation default |
| GPU/codec/compiler/OS boundaries | C/C++ only when unavoidable | Narrow, reviewed, isolated, fuzzed, replaceable |
| Apple platform adapters | Swift/Objective-C | Thin adapter; no duplicate browser policy |
| Windows adapters | C++/WinRT or Rust windows bindings | Thin adapter with Turing semantic core |
| Android/JVM embedding | Kotlin/Java/JNI | Generated wrapper over stable contract |
| DevTools and constrained Plug-in UI | TypeScript | No privileged policy or ambient browser authority |
| Tests, analysis, benchmarks, release tooling, ergonomic SDK | Python | Not bundled as browser runtime |
| Portable multi-language Plug-ins | WebAssembly Components and WIT | Explicit imports, limits, interruption, no ambient WASI |
| C#, Go, Ruby and other SDKs | Generated bindings | Do not reimplement engine semantics |

## Framework and library candidates

- Text: Unicode/CLDR, HarfBuzz, FreeType, CoreText, DirectWrite behind Turing font/privacy/cache policy.
- Graphics: evaluate wgpu against direct Metal, D3D12, and Vulkan; retain deterministic software rendering; evaluate Vello for vector paths.
- Accessibility: evaluate AccessKit for custom chrome while validating VoiceOver, UI Automation, and AT-SPI directly.
- TLS/network foundations: evaluate rustls, low-level HTTP/2/3 and QUIC crates, and DNS primitives; Turing owns Fetch, CORS, cookies, cache, proxy, certificate UI, and partitioning.
- Storage: SQLite is the leading transactional-store candidate; use store-specific schemas and no general ORM in trusted stores.
- Compiler: Turing-owned interpreter/IR/GC; evaluate Cranelift for lowering and Wasmtime only for Plug-in components, never page JavaScript semantics.
- Async: do not standardize one ambient runtime across the browser. Use explicit schedulers; Tokio/Mio are candidates for isolated services and tooling.
- Testing: rustfmt, Clippy, Miri, sanitizers, Loom, proptest, cargo-fuzz/libFuzzer, cargo-nextest, WPT, Test262, fixed-hardware labs.
- Supply chain: lockfiles, cargo-deny, RustSec/cargo-audit, cargo-vet, SBOM, SLSA, in-toto/Sigstore, reproducible builds.
- Build: Cargo workspace plus a small Rust repository tool; CMake/Ninja for required native dependencies; evaluate sccache and lld/mold with evidence.

## Dependency gate

Every candidate needs exact version/source, owner, privilege, hostile-input exposure, unsafe/native inventory, transitive graph, license/patent review, fuzzing, platform matrix, update response, performance/build cost, Turing-owned adapter, and replacement plan. Mention here is not adoption.

## Primary sources

- Rust — https://www.rust-lang.org/
- Rust 2024 edition — https://doc.rust-lang.org/edition-guide/rust-2024/
- Servo — https://servo.org/
- WebAssembly Component Model — https://component-model.bytecodealliance.org/
- Wasmtime — https://wasmtime.dev/
- wgpu — https://wgpu.rs/
- AccessKit — https://github.com/AccessKit/accesskit
- HarfBuzz — https://harfbuzz.github.io/
- rustls — https://rustls.dev/
- SQLite — https://sqlite.org/
- Cranelift — https://cranelift.dev/
"""

PLUGIN_PORTFOLIO = ["Turing Assistant", "Developer Copilot", "Screenshot Studio", "Interaction Recorder", "Translation and Language Tools", "Reader and Research Mode", "Writing Assistant", "Dark/Contrast/Focus Modes", "Privacy Inspector", "Content Filter Lists", "Tab and Workspace Organizer", "Notes and Web Clipper", "Archive and Export", "JSON and Data Inspector", "API and Request Toolkit", "Accessibility Inspector", "Performance and Resource Profiler", "Framework and Source Inspector", "Shopping Comparison", "Meeting and Media Notes"]
PLUGINS = """# Turing Plug-in Platform

Status: architecture and product research; no Plug-in runtime or store exists  
Owner: Plug-in platform, security, product, ecosystem, and accessibility  
Last researched: 2026-07-16

Turing calls extensibility units **Plug-ins**. Every Plug-in—including first-party packages—is an untrusted, separately identified, revocable, resource-bounded principal.

## Native architecture

- Tier A: first-party maintained, separately updateable component with no kernel linkage or blanket privilege.
- Tier B: portable WebAssembly component using WIT imports, memory/fuel/epoch limits, cancellation, isolated storage, and no ambient WASI.
- Tier C: restricted WebExtensions compatibility adapter with a published API matrix; it does not define native Turing APIs.
- Tier D: visible developer-only local package in isolated profiles; never silently loaded by normal signed builds.
- Unrestricted third-party native code is prohibited by default. Native messaging is a separately installed, allowlisted broker.

## Manifest and package contract

A signed deterministic package declares publisher, package/version/API range, runtime tier, entry points, hashes, provenance, license, capabilities, origins, profiles/private mode, data classes, remote endpoints, user activation, confirmation class, resource budgets, background eligibility, UI/accessibility metadata, update/rollback, and support status. Signatures establish identity and integrity; they do not grant authority.

Plug-ins cannot access raw credentials, cookies, unrestricted sockets, arbitrary files, unrelated profiles, hidden cross-origin content, raw browser memory, generic IPC, trusted browser UI, or agent confirmation authority.

## Resource and lifecycle model

Account CPU, memory, GPU, wakeups, network, disk, storage, model tokens/cost, and logs. States include installed, disabled, idle, starting, active, suspended, terminating, crashed, quarantined, updating, and removed. Background work is event-driven, cancellable, bounded, suspendable, and visible in the resource manager.

## First-party portfolio research

""" + "\n".join(f"{i}. {name}" for i, name in enumerate(PLUGIN_PORTFOLIO, 1)) + """

This is a workflow cohort, not a claim of the exact global top twenty. Google does not publish a stable reproducible worldwide Chrome Web Store ranking. The portfolio learns from recurring demand and Google's 2025 favorite-extension editorial list without copying third-party code, branding, assets, or descriptions.

Start with lower-risk, locally useful packages: Screenshot Studio, Tab/Workspace Organizer, JSON/Data Inspector, Accessibility Inspector, Performance/Resource Profiler, Translation, read-only Turing Assistant, and Developer Copilot. Credentials, user scripts, network modification, media capture, shopping, remote AI, and consequential automation require later gates.

## Store, SDK, and governance

The store links listing to signed package, performs automated and risk-based manual review, shows capabilities/data/resource/accessibility/update history, supports appeal and transparency, and uses signed update metadata with minimum secure versions and narrow revocation. SDKs are generated from schemas and include project generator, manifest linter, capability simulator, test profile, package inspector, DevTools, compatibility report, and conformance suite.

## Primary sources

- Chrome Extensions — https://developer.chrome.com/docs/extensions/
- Chrome Manifest V3 — https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3
- Chrome extension security — https://developer.chrome.com/docs/extensions/mv3/security
- Google favorite extensions of 2025 — https://blog.google/products-and-platforms/products/chrome/our-favorite-chrome-extensions-of-2025/
- MDN WebExtensions — https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions
- WebAssembly Component Model — https://component-model.bytecodealliance.org/
"""

EMBEDDING = """# Embedding and Multi-language SDK

Status: public-contract research; no stable API or SDK exists  
Owner: embedding, API, platform, security, release, and SDK owners  
Last researched: 2026-07-16

Turing must be usable as a secure browser engine/platform without becoming a monolith. A host should create a safe profile and view in a few lines while advanced authority remains explicit.

## Contract layers

1. Canonical idiomatic Rust API: Engine, Profile, View, Surface, Navigation, EventStream, CapabilitySet, ResourceBudget, PluginHost, CancellationToken, and typed IDs.
2. Minimal stable C ABI: one version-negotiated function table, opaque generation-checked handles, pointer-plus-length inputs, explicit alloc/free, stable status/error handles, operation handles, and declared thread affinity.
3. Generated C++, Python, Node/TypeScript, Swift, Kotlin/Java, C#, Go, and WIT SDKs from one schema and conformance corpus.
4. Interactive, offscreen, headless, deterministic-test, automation, and server-render modes share navigation, security, storage, lifecycle, and policy machinery.

## Host and engine responsibilities

Turing owns web semantics, renderer/site isolation, IPC, navigation/origin policy, certificate core, network/storage partitioning, credential broker interfaces, Plug-in/agent authorization, crash containment, and diagnostics. The host owns signed packaging, verified engine delivery, OS entitlements, trusted application chrome, secure profile location, declared services, user disclosures, and incident support. Unsafe configurations fail startup rather than degrade silently.

## Lifecycle and surfaces

Engine, profile, view, navigation, surface, and async operation are explicit state machines. Long operations have deadline, cancellation, exactly one terminal result, bounded event streams, and stale-epoch rejection. Surfaces identify size, scale, color, damage, synchronization, device generation, presentation, and release. Input, IME, clipboard, drag/drop, and accessibility remain structured semantics—not pixels or raw page pointers.

## Versioning and packaging

Product, engine, Rust API, C ABI, protocol schemas, profile format, Plug-in API, and SDKs have separate versions and compatibility ranges. Artifacts include signatures, checksums, SBOM, provenance, symbols, notices, source references, supported platforms, and host conformance. Packages cannot download unverified engines during import/build.

## Minimal design target

```rust
let engine = Engine::builder().secure_defaults().build().await?;
let profile = engine.ephemeral_profile().await?;
let view = profile.create_view().await?;
view.navigate("https://example.com").await?;
```

This is a design target, not an existing API.

## Primary sources

- Rust API Guidelines — https://rust-lang.github.io/api-guidelines/
- Rust FFI guidance — https://doc.rust-lang.org/nomicon/ffi.html
- UniFFI — https://mozilla.github.io/uniffi-rs/
- WebAssembly Component Model/WIT — https://component-model.bytecodealliance.org/
- Servo embedding work — https://servo.org/
- Semantic Versioning — https://semver.org/
"""

TEMPLATES = """# Turing Engineering Templates

Status: mandatory starting structures  
Owner: architecture, quality, security, and documentation governance

Use the smallest applicable structure and delete instructional text. Every accepted artifact includes stable ID, owner, status, requirements, risks, unsupported behavior, evidence, and related records.

## RFC / design note

Metadata; summary; user need; goals/non-goals; proposed architecture; identities/authority/lifecycle; alternatives; security/privacy; accessibility/product; compatibility/standards; performance/resources; operations/licensing; implementation/rollout/rollback; evidence; open questions/dissent; decision.

## ADR

ID/status/date; context; decision; prohibited alternatives; consequences; evidence; migration; revisit trigger; supersession chain.

## API or embedding proposal

Audience/stability/version; minimum safe workflow; operations/types/identity/authority; ownership/threading/cancellation/backpressure/errors; security responsibilities; compatibility/deprecation; language bindings; conformance; performance.

## Dependency proposal

Exact source/version; owner; need/alternatives; privilege/hostile input; unsafe/native/transitive/build scripts; license/patent/provenance; security history/fuzzing; platform/performance/build cost; Turing adapter; replacement; decision/review date.

## Threat model and security review

Scope; assets; actors; trust assumptions; processes/data flow; attack surfaces; threats/abuse; mitigations; residual risk; verification; findings/severity/owners/dates; release implications.

## Performance or benchmark plan

Question/hypothesis; correctness/security/accessibility guardrails; critical path; metrics/budgets; fixed environment; workloads; repetitions/statistics; failure denominator; raw artifacts; regression/rollback.

## Migration, experiment, risk acceptance, deprecation, postmortem, and release readiness

Each records exact versions/builds, owner, preconditions, method, failure/recovery, evidence, user impact, rollback, expiry, communication, and changes required in requirements/risks/ADRs.

## Plug-in proposal

User job; publisher; execution tier; manifest/capabilities/origins/data; lifecycle/resource budgets; UI/accessibility; threat model; signing/update/revocation; store; conformance/support.
"""

RESEARCH = """# Professional Buildout Gap Audit — July 2026

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
"""

DOCS = {
    "docs/project-buildout/README.md": PROJECT_INDEX,
    **{f"docs/project-buildout/{name}": content for name, content in PROJECT.items()},
    "docs/technology-stack/README.md": TECH,
    "docs/plugins/README.md": PLUGINS,
    "docs/embedding/README.md": EMBEDDING,
    "docs/templates/README.md": TEMPLATES,
    "docs/research/professional-buildout-gap-audit-2026-07.md": RESEARCH,
}

BOOK_ROWS = """| [Technology Stack and Engineering Toolchain](technology-stack/README.md) | Language map, framework/library candidates, build/test/security tooling, and dependency lifecycle |
| [Turing Plug-in Platform](plugins/README.md) | Native Plug-ins, capabilities, Wasm/WIT, WebExtensions adapter, first-party portfolio, store, SDK, accessibility, and resources |
| [Embedding and Multi-language SDK](embedding/README.md) | Rust API, stable C ABI, generated SDKs, lifecycle, surfaces, host security, packaging, and conformance |
| [Professional Project Buildout and Operating Handbook](project-buildout/README.md) | Phase gates, ownership, review, traceability, repository, coding, schemas, cross-cutting review, operations, source strategy, product, and sustainability |"""

CODEOWNERS = """# Provisional single-owner research-phase routing. Multi-person backup and qualified domain ownership are required before preview/beta/stable.
* @byronwade
/docs/ @byronwade
/docs/engine/ @byronwade
/docs/javascript/ @byronwade
/docs/security-engine/ @byronwade
/docs/plugins/ @byronwade
/docs/embedding/ @byronwade
/docs/technology-stack/ @byronwade
/docs/project-buildout/ @byronwade
/prototype/ @byronwade
/tools/ @byronwade
/.github/ @byronwade
"""


def machine_records() -> None:
    machine = ROOT / "docs/blueprint-v1/machine"
    req = json.loads((machine / "requirements.json").read_text(encoding="utf-8"))["requirements"]
    scopes = ["program","architecture","security","engine","javascript","networking","storage","platform","media","accessibility","developer-experience","api-protocol","plugins","embedding","ai-agent","performance","quality","release-operations","privacy-data","legal-community","documentation-research"]
    owners = {"schema_version":1,"updated":DATE,"note":"Provisional single-owner research-phase assignments; backups required before preview.","owners":[{"scope":s,"status":"provisional","primary":"@byronwade","backup":None,"next_review":"2026-10-16"} for s in scopes]}
    category = {"A11Y":"accessibility","AI":"ai-agent","DEV":"developer-experience","ENG":"engine","JS":"javascript","NET":"networking","OPS":"release-operations","PERF":"performance","PROD":"program","SEC":"security","STO":"storage"}
    trace = {"schema_version":1,"updated":DATE,"requirements":[{"id":r["id"],"owner_scope":category[r["id"].split("-")[1]],"milestone":r["gate"],"specification_status":r["status"],"implementation_status":"not_started","verification_status":"none","design":[],"source":[],"tests":[],"reviews":[],"evidence":[],"note":"Populate without hiding absence as implementation begins."} for r in req]}
    phases = {"schema_version":1,"updated":DATE,"phases":[{"id":f"M{i}","status":"in_progress" if i==0 else "not_started","owner_scope":"program","evidence":[],"blockers":["Professional controls and multi-person ownership incomplete."] if i==0 else []} for i in range(10)]}
    reviews = {"schema_version":1,"rules":[
        {"id":"REV-ROUTINE","match":"low-risk internal behavior","artifacts":["tests","documentation impact"],"reviewers":["owner"],"minimum_approvals":1},
        {"id":"REV-SECURITY","match":"trust boundary, parser, IPC, permission, credential, update, Plug-in, DevTools, automation, or agent change","artifacts":["threat-model delta","negative tests","security review"],"reviewers":["owner","security"],"minimum_approvals":2},
        {"id":"REV-PUBLIC-API","match":"public API, ABI, schema, profile, policy, Plug-in, embedding, or compatibility change","artifacts":["RFC","compatibility tests","migration"],"reviewers":["owner","api-protocol","architecture"],"minimum_approvals":2},
        {"id":"REV-PERFORMANCE","match":"hot path, allocator, scheduler, memory layout, GPU, startup, or benchmark claim","artifacts":["performance plan","raw evidence","guardrails"],"reviewers":["owner","performance"],"minimum_approvals":2},
        {"id":"REV-RELEASE","match":"signing, update, release trust, supported-version, or irreversible migration","artifacts":["RFC","threat model","rollout/rollback","release readiness"],"reviewers":["owner","security","release","architecture"],"minimum_approvals":3}]}
    exceptions = {"schema_version":1,"updated":DATE,"exceptions":[]}
    for name, payload in {"professional-owners.json":owners,"professional-traceability.json":trace,"professional-phase-gates.json":phases,"professional-review-rules.json":reviews,"professional-exceptions.json":exceptions}.items():
        write(f"docs/blueprint-v1/machine/{name}", json.dumps(payload, indent=2))


def update_validator() -> None:
    path = "tools/validate_blueprint.py"
    text = read(path)
    start = text.index("DETAILED_BOOKS = ")
    end = text.index("\n\nREQUIRED_DOCS = [", start)
    books = ast.literal_eval(text[start + len("DETAILED_BOOKS = "):end])
    books.update({"technology-stack":["README.md"],"plugins":["README.md"],"embedding":["README.md"],"project-buildout":[*PROJECT.keys(),"README.md"]})
    text = text[:start] + "DETAILED_BOOKS = " + pprint.pformat(books, width=120, sort_dicts=False) + text[end:]
    anchor = '    MACHINE / "risks.json",'
    extra = anchor + '\n    MACHINE / "professional-owners.json",\n    MACHINE / "professional-traceability.json",\n    MACHINE / "professional-phase-gates.json",\n    MACHINE / "professional-review-rules.json",\n    MACHINE / "professional-exceptions.json",'
    if "professional-owners.json" not in text:
        text = text.replace(anchor, extra, 1)
    text = text.replace('"19 detailed engineering books, 46 requirements, 40 risks, "','"23 detailed engineering books, 46 requirements, 40 risks, "',1)
    text = text.replace('"18 work packages, 6 machine-readable registries"','"18 work packages, 11 machine-readable registries"',1)
    forbidden = '    ROOT / ".github" / "workflows" / "expand-bootstrap.yml",'
    if "professional-buildout-expand.yml" not in text:
        text = text.replace(forbidden, forbidden + '\n    ROOT / ".github" / "workflows" / "research-wave4-main-finalize.yml",\n    ROOT / ".github" / "workflows" / "professional-buildout-expand.yml",\n    ROOT / "tools" / "professional_buildout_generator.py",', 1)
    write(path, text)


def update_existing() -> None:
    insert_after("docs/README.md", "| [Everyday Product Experience Engineering](product-experience/README.md) | Tabs, groups, workspaces, command field, onboarding, migration, profiles, private sessions, permissions, credentials, agents, resource manager, lifecycle, recovery, settings, updates, support, usability, and accessibility. |", "project-buildout/README.md", BOOK_ROWS)
    insert_after("docs/README.md", "| [Performance, security, developer, and missing-systems expansion audit — July 2026](research/performance-security-developer-expansion-audit-2026-07.md) | Adds eleven books and advanced performance, security, and developer research; no implementation or support claim |", "professional-buildout-gap-audit-2026-07.md", "| [Professional buildout gap audit — July 2026](research/professional-buildout-gap-audit-2026-07.md) | Ownership, traceability, source strategy, technology, Plug-in, embedding, operations, legal, data, product, and sustainability controls |")
    insert_after("docs/blueprint-v1/README.md", "- [Everyday Product Experience Engineering](../product-experience/README.md)", "../project-buildout/README.md", "- [Technology Stack and Engineering Toolchain](../technology-stack/README.md)\n- [Turing Plug-in Platform](../plugins/README.md)\n- [Embedding and Multi-language SDK](../embedding/README.md)\n- [Professional Project Buildout and Operating Handbook](../project-buildout/README.md)")
    insert_after("docs/blueprint-v1/README.md", "- [Performance, security, developer, and missing-systems expansion audit — July 2026](../research/performance-security-developer-expansion-audit-2026-07.md)", "../research/professional-buildout-gap-audit-2026-07.md", "- [Professional buildout gap audit — July 2026](../research/professional-buildout-gap-audit-2026-07.md)")
    append_once("README.md", "## Professional buildout", "## Professional buildout\n\nThe [Professional Project Buildout and Operating Handbook](docs/project-buildout/README.md), [Technology Stack](docs/technology-stack/README.md), [Turing Plug-in Platform](docs/plugins/README.md), and [Embedding SDK](docs/embedding/README.md) define the proposed professional implementation control plane. They are research and operating baselines, not implementation or support claims.")
    append_once("AGENTS.md", "## Professional project-control requirements", "## Professional project-control requirements\n\nBefore production implementation, use the [project-buildout handbook](docs/project-buildout/README.md), machine ownership/traceability/review records, and [engineering templates](docs/templates/README.md). No Servo-derived release code lands before ADR-0009. No dependency is approved merely by appearing in research. Every Plug-in is a separate, revocable, resource-bounded principal. Public embedding uses an opaque stable ABI and generated SDKs, never Rust layout. Configuration, exceptions, evidence, and maturity are explicit and time-bounded.")
    append_once("docs/start-here.md", "## Professional implementation controls", "## Professional implementation controls\n\nRead the [project-buildout handbook](project-buildout/README.md), [technology stack](technology-stack/README.md), [Plug-in platform](plugins/README.md), [embedding SDK](embedding/README.md), and [templates](templates/README.md) before implementation work.")
    append_once("docs/documentation-policy.md", "## Professional control-plane records", "## Professional control-plane records\n\nChanges must inspect the professional ownership, traceability, phase, review, and exception registries under `blueprint-v1/machine/`, the project-buildout handbook, and the relevant technology, Plug-in, embedding, and template records. Research recommendations never silently change accepted implementation or support status.")
    append_once("docs/contributing.md", "## Professional change workflow", "## Professional change workflow\n\nSignificant work identifies owner and backup status, requirement/traceability impact, RFC/ADR class, required cross-cutting reviewers, configuration, Plug-in/embedding, dependency/provenance, migration, evidence, rollback, release/support, and any expiring exception.")
    append_once("docs/research/README.md", "## Professional buildout audit", "## Professional buildout audit\n\n- [Professional buildout gap audit — July 2026](professional-buildout-gap-audit-2026-07.md)\n- [Technology Stack](../technology-stack/README.md)\n- [Turing Plug-ins](../plugins/README.md)\n- [Embedding SDK](../embedding/README.md)\n- [Professional Project Buildout](../project-buildout/README.md)")
    append_once("docs/research-log.md", "Professional buildout gap audit", "## 2026-07-16 — Professional buildout gap audit\n\nA repository-wide review found that the remaining gap was the project control plane rather than another disconnected subsystem survey. The change adds professional phase, ownership, decision, traceability, repository, build, coding, API/configuration, cross-cutting review, release, legal, data, product, documentation, sustainability, Servo, Plug-in, and embedding baselines. It changes no implementation, requirement, risk, or support status.")
    append_once("docs/repository-map.md", "## Professional buildout additions", "## Professional buildout additions\n\n- `docs/project-buildout/`: professional lifecycle, ownership, review, traceability, engineering, operations, source-strategy, product, and sustainability controls.\n- `docs/technology-stack/`: language, framework, toolchain, and dependency research.\n- `docs/plugins/`: native Plug-in platform and compatibility research.\n- `docs/embedding/`: Rust/C/generated-SDK embedding contract.\n- `docs/templates/`: engineering artifact structures.\n- `docs/blueprint-v1/machine/professional-*.json`: ownership, traceability, phase, review, and exception companions.\n- `.github/CODEOWNERS`: provisional research-phase review routing.")
    append_once("docs/blueprint-v1/03-language-and-dependency-strategy.md", "## Detailed technology selection", "## Detailed technology selection\n\nThe [Technology Stack](../technology-stack/README.md) documents candidates and adoption gates. A named library is not approved without exact source/version, owner, license/provenance, unsafe/native and hostile-input review, fuzzing, platform/performance/build evidence, Turing-owned adapter, and replacement plan.")
    append_once("docs/blueprint-v1/14-roadmap-work-breakdown.md", "## Professional buildout prerequisite", "## Professional buildout prerequisite\n\nBefore substantial production implementation, resolve ADR-0009, accept the workspace/toolchain/interface contracts, activate ownership/traceability/review records, reproduce bootstrap on fresh hosts, and staff backup ownership. This refines M0 without changing WP-001 through WP-018 status.")
    append_once("docs/blueprint-v1/16-governance-contributing.md", "## Professional operating controls", "## Professional operating controls\n\n`.github/CODEOWNERS` and the professional machine records operationalize ownership, traceability, phase, review, and exceptions. Current assignments are provisional and do not satisfy preview/beta/stable multi-person gates.")
    append_once("docs/blueprint-v1/17-architecture-decisions.md", "## ADR-0009 — Servo relationship", "## Proposed decisions requiring review\n\n### ADR-0009 — Servo relationship and source strategy\n\nStatus: proposed. Compare clean implementation informed by Servo, selective components, upstream-first collaboration, Servo-derived engine, and explicit charter change. No Servo-derived release code before evidence and acceptance.\n\n### ADR-0010 — Stable C ABI and generated SDKs\n\nStatus: proposed. Canonical Rust API, minimal opaque C ABI, generated language SDKs, host responsibility matrix, and conformance suite.\n\n### ADR-0011 — Capability-based Turing Plug-ins\n\nStatus: proposed. Prefer WIT/WebAssembly components, isolate WebExtensions, and prohibit ambient authority/native code.\n\n### ADR-0012 — Machine-readable professional control plane\n\nStatus: proposed. Ownership, traceability, phase, review, and exception records become canonical Blueprint companions after a usability pilot.")
    append_once("docs/blueprint-v1/18-source-bibliography.md", "## Professional buildout sources", "## Professional buildout sources\n\n- NIST SSDF — https://csrc.nist.gov/pubs/sp/800/218/final\n- NIST Incident Response — https://csrc.nist.gov/pubs/sp/800/61/r3/final\n- SLSA — https://slsa.dev/spec/v1.2/\n- Reproducible Builds — https://reproducible-builds.org/\n- GitHub CODEOWNERS — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners\n- Semantic Versioning — https://semver.org/\n- JSON Schema — https://json-schema.org/draft/2020-12\n- Servo — https://servo.org/\n- WebAssembly Component Model — https://component-model.bytecodealliance.org/\n- Chrome Extensions — https://developer.chrome.com/docs/extensions/")
    append_once("docs/blueprint-v1/20-definition-of-done.md", "## Professional control-plane change", "## Framework or dependency adoption\n\nExact source/version, owner, alternatives, privilege, hostile input, unsafe/native, license/provenance, fuzzing, platforms, performance/build cost, update and replacement are reviewed. Research mention is not adoption.\n\n## Plug-in or embedding feature\n\nManifest/API, authority, identity, lifecycle, cancellation, resource, data, accessibility, compatibility, packaging, update, conformance, failure, and support are explicit.\n\n## Professional control-plane change\n\nOwnership, traceability, phase, decision class, review, evidence, exception, documentation, release, and capacity records agree.")
    append_once("docs/blueprint-v1/22-research-program.md", "## RQ-41 — Technology", "## RQ-41 — Technology and dependency set\n\nWhich languages, frameworks, and foundations minimize total security, performance, build, license, and maintenance cost?\n\n## RQ-42 — Native Plug-ins\n\nWhich capability/Wasm/WebExtensions architecture is safest and most useful?\n\n## RQ-43 — Embedding contract\n\nWhich Rust/C/generated-SDK contract remains simple without freezing internals?\n\n## RQ-44 — Servo relationship\n\nWhich clean, selective, upstream, derived, or charter-change option best serves Turing?\n\n## RQ-45 — Project controls\n\nWhich ownership, review, traceability, phase, and evidence controls reduce defects without blocking work?\n\n## RQ-46 — Reproducible environment\n\nWhich bootstrap, cache, linker, test runner, and host matrix is fast and maintainable?\n\n## RQ-47 — Traceability at browser scale\n\nCan requirement-to-evidence records remain accurate and useful?\n\n## RQ-48 — Capacity and sustainability\n\nWhat staffing, funding, infrastructure, and support capacity is required at each maturity?")
    append_once(".github/pull_request_template.md", "## Professional controls", "## Professional controls\n\n- Owner and backup status:\n- RFC/ADR/design-note class:\n- Traceability/phase impact:\n- Required cross-cutting reviews:\n- Configuration, Plug-in, embedding, dependency, migration, release, support, and expiring exception impact:")


def main() -> None:
    for path, content in DOCS.items():
        write(path, content)
    write(".github/CODEOWNERS", CODEOWNERS)
    machine_records()
    update_existing()
    update_validator()


if __name__ == "__main__":
    main()
