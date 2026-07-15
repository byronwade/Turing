from __future__ import annotations

import json
import re
import shutil
import textwrap
from pathlib import Path

from data import ADRS, BIBLIOGRAPHY, DOCS, GLOSSARY, REQUIREMENTS, RISKS

ROOT = Path.cwd()
UPDATED = "2026-07-15"


def clean_repository() -> None:
    for item in ROOT.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    normalized = textwrap.dedent(content).strip() + "\n"
    target.write_text(normalized, encoding="utf-8")


def bullets(raw: str) -> str:
    return "\n".join(f"- {part.strip()}" for part in raw.split("|") if part.strip())


def requirement_table() -> str:
    rows = ["| ID | Area | Requirement | Evidence gate | Phase |", "|---|---|---|---|---|"]
    for index, (area, statement, metric, phase) in enumerate(REQUIREMENTS, 1):
        rows.append(f"| BR-{index:03d} | {area} | {statement} | {metric} | {phase} |")
    return "\n".join(rows)


def risk_table() -> str:
    rows = ["| ID | Severity | Likelihood | Risk | Mitigation | Trigger | Owner |", "|---|---|---|---|---|---|---|"]
    for index, row in enumerate(RISKS, 1):
        severity, likelihood, risk, mitigation, trigger, owner = row
        rows.append(f"| R-{index:03d} | {severity} | {likelihood} | {risk} | {mitigation} | {trigger} | {owner} |")
    return "\n".join(rows)


def bibliography() -> str:
    lines = []
    for title, url, use in BIBLIOGRAPHY:
        lines.append(f"- [{title}]({url}) — {use} Accessed {UPDATED}.")
    return "\n".join(lines)


def language_matrix() -> str:
    return """
| Language | Best use | Strengths | Constraints | Decision |
|---|---|---|---|---|
| Rust | Engine, brokers, network policy, storage policy, IPC, agent policy | Memory safety without a tracing runtime, explicit ownership, strong enums, useful concurrency model, mature tooling | Compile-time complexity, smaller browser ecosystem, FFI still required | Primary language |
| C++ | Narrow integration with unavoidable native graphics, media, or OS components | Ecosystem reach, ABI access, mature profilers | Memory-unsafety and complex ownership increase exploit risk | Exception only, isolated behind reviewed FFI |
| C | Stable ABI shims and tiny platform boundaries | Universal interoperability and simple ABI | No ownership model; easy bounds and lifetime defects | Minimal shims only |
| Zig | Build experiments, utilities, and controlled systems prototypes | Explicit allocation, cross-compilation, simple interop | Younger ecosystem and weaker safety guarantees than Rust for hostile parser code | Experimental, not trusted-core default |
| Swift / Objective-C | macOS UI and platform adapters | Native framework access and platform conventions | Platform-specific runtime and limited cross-platform reuse | Thin macOS adapter |
| C# / C++ WinRT | Windows UI and platform adapters | Native Windows integration and strong productivity | Platform-specific deployment and runtime tradeoffs | Thin Windows adapter after prototype evidence |
| Kotlin / Java | Future Android shell and platform services | Android ecosystem and tooling | Managed-runtime overhead and platform scope | Mobile adapter only, outside desktop critical path |
| TypeScript | Documentation tooling, generated protocol clients, optional UI prototypes | Fast iteration and ecosystem | GC and web-runtime dependency conflict with trusted browser core goals | Tooling only |
""".strip()


def capability_matrix() -> str:
    rows = [
        ("HTML, DOM, navigation", "Independent implementation", "WPT plus real-site corpus", "Core target"),
        ("CSS, layout, painting", "Independent implementation", "WPT and reference rendering", "Core target"),
        ("JavaScript and WebAssembly", "Independent runtime or separately governed in-project runtime", "Test262 and spec tests", "Critical research track"),
        ("HTTP, Fetch, security policy", "Independent browser integration over audited protocol and crypto foundations", "Interop and negative-security suites", "Core target"),
        ("Unicode and text shaping", "Adopt mature data and shaping libraries behind narrow interfaces", "International text corpus", "Foundation dependency"),
        ("Images and compression", "Adopt reviewed codecs where safe and licensed", "Corpus, fuzzing, visual tests", "Foundation dependency"),
        ("Audio, video, WebRTC", "Browser semantics owned; codecs modular", "Web media tests and interop", "Legal and platform gates"),
        ("DRM / protected media", "External content-decryption integration only", "Provider certification", "Not guaranteed; commercial gate"),
        ("WebGL / WebGPU", "Independent validation and integration over native GPU APIs", "Conformance and driver matrix", "High-risk target"),
        ("Extensions", "New least-privilege model; constrained compatibility adapters later", "Permission and compatibility suites", "Late phase"),
        ("DevTools", "Versioned in-project protocol and UI", "Protocol compatibility and workflow tests", "Developer-first target"),
        ("Profiles, sync, passwords", "Local features first; sync uses separately threat-modeled service", "Recovery, crypto, and privacy tests", "Product target"),
        ("Enterprise policy", "Declarative policy layer after stable product semantics", "Policy corpus", "Late phase"),
        ("AI assistance", "Separate untrusted process and deterministic capability mediator", "Injection and authorization red teams", "Differentiating target"),
    ]
    out = ["| Surface | Independence boundary | Evidence | Status classification |", "|---|---|---|---|"]
    out.extend(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows)
    return "\n".join(out)


def roadmap() -> str:
    return """
| Phase | Indicative horizon | Deliverable | Exit gate |
|---|---:|---|---|
| P0 — Program foundation | 0–3 months | Repository, architecture, threat model, test harnesses, benchmark disclosure format, contributor workflow | Documentation and skeleton validation; no parity claims |
| P1 — Secure shell | 3–9 months | Native window, URL loading, process launcher, bounded IPC, sandbox experiments, text-only document inspection | Each process can be terminated independently; policy tests fail closed |
| P2 — Static web engine | 9–18 months | HTML parser, DOM, CSS cascade, basic block/inline layout, text shaping, paint, image loading | Published WPT slice and visual corpus thresholds |
| P3 — Interactive engine | 18–36 months | Events, forms, editing, incremental layout, interpreter, GC, fetch, storage, basic DevTools and agent observation | Representative interactive sites work without disabling isolation |
| P4 — Hardened developer preview | 3–5 years | Workers, service workers, richer CSS, site isolation, robust storage, GPU process, automation protocol, agent action policy | Continuous fuzzing, sandbox verification, recovery and accessibility gates |
| P5 — Alpha product | 5–8 years with a specialist team | Broad APIs, media, WebGL/WebGPU, extensions, polished UI, updater, multi-platform support | Public scorecards and sustained security operations |
| P6 — Broad parity program | 8–12+ years and substantial staffing | Long-tail compatibility, enterprise, ecosystem and external integrations | Capability-by-capability evidence; proprietary gates remain separate |

The horizons are planning ranges, not delivery promises. A solo project can produce meaningful research and a useful constrained browser much earlier; broad Chrome-class compatibility and security operations are organization-scale work.
""".strip()


def work_breakdown() -> str:
    tracks = [
        ("Program", "Requirements, ADRs, issue taxonomy, scorecards", "All work is test-linked and risk-owned"),
        ("Core", "Types, state machines, scheduler, resource accounting", "Deterministic model and property tests"),
        ("HTML / DOM", "Parser, tree, events, editing, navigation", "WPT module thresholds"),
        ("CSS / Layout", "Cascade, formatting contexts, incremental invalidation", "Visual and layout conformance"),
        ("Runtime", "Interpreter, bytecode, GC, event loop, Wasm, optional JIT", "Test262, stress, W^X verification"),
        ("Rendering", "Paint, display lists, raster, compositor, animation", "Pixel, jank, and GPU fault tests"),
        ("Network", "Fetch, protocols, TLS integration, policy, partitioning", "Interop and negative-security tests"),
        ("Storage", "Origin stores, cache, profile DBs, migration, secrets", "Crash consistency and forensic privacy"),
        ("Platform", "Windows, macOS, Linux adapters and packaging", "Shared behavioral matrix"),
        ("Security", "Sandbox, capabilities, fuzzing, exploit-chain testing, updates", "Release-blocking invariants"),
        ("AI", "Observation, planning, authorization, action ledger, model routing", "Prompt-injection and authority tests"),
        ("Product", "UI system, tabs, profiles, settings, history, downloads", "Journey, accessibility, and latency gates"),
        ("Developer", "Inspector, console, tracing, automation, documentation", "Versioned protocol and workflow tests"),
        ("Operations", "CI, release, SBOM, signing, incident response", "Reproducible artifact verification"),
    ]
    rows = ["| Track | Deliverables | Definition of done |", "|---|---|---|"]
    rows.extend(f"| {a} | {b} | {c} |" for a, b, c in tracks)
    return "\n".join(rows)


def extras(slug: str) -> str:
    if slug == "00-charter.md":
        return """
## Operating principles

1. Correctness and containment outrank benchmark screenshots.
2. Engine independence means no Chromium, Gecko, or WebKit engine embedding; it does not justify custom cryptography, Unicode, codec, or sandbox primitives.
3. Compatibility is a measured matrix, not a slogan.
4. Memory comparisons disclose lifecycle and isolation state.
5. AI is optional and never receives ambient user authority.
6. Risk, licensing, accessibility, and external dependencies remain visible.

## Explicit non-goals for the bootstrap

The bootstrap does not claim a production browser, a secure sandbox on any platform, passing web compatibility, a competitive JavaScript runtime, DRM availability, or measured performance superiority. It creates the contracts needed to investigate those outcomes honestly.
"""
    if slug == "01-product-requirements.md":
        return "## Stable requirement inventory\n\n" + requirement_table()
    if slug == "02-capability-parity.md":
        return "## Initial capability classification\n\n" + capability_matrix() + "\n\nEvery row must later split into versioned sub-capabilities with supported, partial, experimental, blocked, and unsupported states."
    if slug == "03-language-research.md":
        return "## Comparative decision matrix\n\n" + language_matrix() + "\n\n## Selection rule\n\nA language exception requires a benchmark or platform-access need, a threat-boundary description, an ownership plan, and an exit strategy. No language choice compensates for weak process isolation or missing conformance tests."
    if slug == "05-process-model.md":
        return """
## Initial role graph

```text
UI ──intent──> Browser broker ──capability──> Renderer(s)
                      ├──> Network service
                      ├──> Storage service
                      ├──> GPU/compositor service
                      ├──> Utility/decoder services
                      └──> Agent policy service ──filtered context──> Model worker
```

Renderers never receive profile secrets, unrestricted filesystem access, or raw network sockets. The broker does not parse arbitrary web formats. Privileged services treat renderer messages as hostile.
"""
    if slug == "06-ipc.md":
        return """
## Envelope invariants

Every envelope carries protocol version, source role, destination role, message class, request identifier, deadline, payload length, and capability reference. Receivers validate role pairing before payload decoding. Queues are bounded by messages and bytes. Cancellation is idempotent. Shared memory is immutable or single-writer by construction and cannot carry authority by itself.
"""
    if slug == "10-javascript-runtime.md":
        return """
## Staged runtime plan

1. Parse and interpret a deliberately small ECMAScript slice.
2. Build exact object, realm, job-queue, exception, and host-binding semantics.
3. Add a precise tracing collector with incremental work budgets.
4. Close Test262 clusters before adding optimization.
5. Add bytecode specialization and inline caches with deoptimization metadata.
6. Consider baseline and optimizing JIT tiers only after sandbox, W^X, code-signing, and exploit-response designs exist.

Embedding an existing browser engine is out of scope. Reusing a separately governed general-purpose runtime would require a new ADR because host integration and security patch cadence become architectural dependencies.
"""
    if slug == "21-tab-memory.md":
        return """
## Lifecycle state machine

| State | Live renderer | JavaScript | Media / network | Restore source | User signal |
|---|---|---|---|---|---|
| Active | Yes | Running | Normal | Memory | Selected tab |
| Background | Usually | Budgeted | Policy-limited | Memory | None |
| Frozen | Retained or pooled | Paused | Only explicit exemptions | Memory plus journal | Visible frozen indicator in diagnostics |
| Discarded | No | No | No | Navigation state or validated snapshot | Reload marker and reason |
| Restoring | Allocating | Starts after state validation | Reconnected by policy | Snapshot and network | Progress state |

No tab with active capture, unsaved form state lacking a journal, audible media, WebRTC, a user-approved background task, or an in-progress sensitive agent action is discarded automatically. Pressure policy is deterministic and inspectable.
"""
    if slug == "23-benchmarking.md":
        return """
## Mandatory disclosure record

Every comparison records browser and build identifiers, operating system, kernel, firmware, CPU, memory, storage, GPU, power mode, display state, page corpus hashes, network shaping, profile state, extensions, process isolation, lifecycle decisions, warm-up, run count, outlier rule, measurement API, raw samples, summary statistic, and confidence interval. Browser-owned and page-content cost are separated where attribution allows. A result that cannot disclose discarded tabs is invalid.
"""
    if slug == "25-threat-model.md":
        return """
## Primary assets and attackers

Assets include credentials, cookies, local files selected by the user, history, private profile state, payment and communication intent, code-signing keys, update channels, agent context, and cross-origin confidentiality. Attackers include malicious sites, compromised dependencies, hostile media, malicious extensions, local malware, compromised model providers, prompt-injecting content, and insiders with release access.

The controlling exploit chain is: hostile bytes → parser or runtime defect → renderer control → IPC abuse → broker or service confusion → sandbox escape or secret access → persistence through profile or update state. Test planning must break each edge independently.
"""
    if slug == "28-ai-architecture.md":
        return """
## Trust-preserving action flow

```text
Page/UI state → policy-filtered observation → untrusted model plan
           → structured proposal → deterministic authorization
           → user confirmation when required → narrow executor
           → postcondition check → append-only redacted ledger
```

The model never receives raw credential stores, unrestricted history, arbitrary files, browser-process memory, or direct network credentials. Tool adapters are separately permissioned. Core navigation remains fully usable with the entire AI subsystem disabled.
"""
    if slug == "29-agent-permissions.md":
        return """
## Authorization tuple

A grant is valid only for `(profile, top-level origin, frame origin, document version, action class, target descriptor, data classification, expiry, nonce, confirmation state)`. The executor re-observes target state immediately before mutation. Navigation, DOM replacement, origin change, expiry, profile switch, permission revocation, or consumed nonce invalidates the grant.
"""
    if slug == "30-prompt-injection.md":
        return """
## Non-model controls

- Page text, accessibility labels, documents, tool output, extensions, and retrieved content are data, not authority.
- The policy engine rejects cross-origin disclosure and privilege escalation even when the model insists.
- Sensitive values are represented by handles and never copied into model context unless a specific disclosure grant exists.
- Proposed actions include provenance and a human-readable preview.
- Red-team pages attempt hidden instructions, CSS concealment, role impersonation, tool-result injection, stale-state attacks, and multi-step laundering.
"""
    if slug == "38-roadmap.md":
        return "## Phase program\n\n" + roadmap()
    if slug == "39-work-breakdown.md":
        return "## Program tracks\n\n" + work_breakdown()
    if slug == "40-risk-register.md":
        return "## Active risks\n\n" + risk_table() + "\n\nRisk closure requires evidence that the trigger can no longer occur or that residual risk was explicitly accepted."
    if slug == "41-cost-team.md":
        return """
## Feasibility bands

| Band | Typical shape | Planning implication |
|---|---|---|
| Solo research | One engineer, a few reference devices, hosted CI, narrow prototypes | Can validate architecture and build a constrained browser; cannot provide continuous broad-platform security response alone |
| Focused engine team | Roughly 8–20 specialists across rendering, runtime, security, networking, platform, testing, and product | Can pursue a credible developer preview if scope is disciplined |
| Broad parity organization | Dozens to more than one hundred engineers plus security response, release, accessibility, legal, infrastructure, and partner functions | Required for sustained long-tail compatibility and multiple stable platforms |

Budget numbers depend heavily on geography, compensation, device labs, fuzzing, signing, model use, and external licensing. Any funding plan must publish assumptions rather than copy a single headline estimate.
"""
    if slug == "45-research-bibliography.md":
        return "## Primary source register\n\n" + bibliography() + "\n\nReferences describe standards and comparison points; they do not imply code reuse or endorsement. Architecture decisions cite exact sections as implementation work begins."
    if slug == "46-glossary.md":
        return "## Terms\n\n" + "\n".join(f"- **{term}:** {definition}" for term, definition in GLOSSARY.items())
    if slug == "47-open-questions.md":
        return """
## Prioritized experiments

| Question | Experiment | Decision trigger |
|---|---|---|
| Independent JavaScript runtime versus separately governed runtime | Implement interpreter and host-binding slice; compare conformance velocity, memory, and hardening burden | ADR before P3 expansion |
| Retained display list versus scene graph | Prototype scrolling, animation, and damage workloads | P2 renderer architecture freeze |
| GPU abstraction | Compare direct native adapters with a reviewed portability layer under device-loss and validation tests | Before WebGL/WebGPU implementation |
| Renderer process economics | Simulate same-site pools under 30-tab corpora without changing isolation | P4 memory policy |
| DOM snapshot representation for agents | Red-team accessibility tree, semantic DOM, and task-specific views | Before agent writes |
| Extension compatibility | Threat-model a constrained adapter against a clean capability model | P5 scope review |
| Cross-platform UI toolkit | Prototype startup, accessibility, native input, and memory on each desktop OS | Before production shell selection |
"""
    if slug == "48-decision-log.md":
        rows = ["| ADR | Decision | Status |", "|---|---|---|"]
        for filename, title, status, *_ in ADRS:
            rows.append(f"| [{filename}](../adr/{filename}) | {title} | {status} |")
        return "## Architecture decisions\n\n" + "\n".join(rows)
    return ""


def render_doc(index: int, entry: tuple[str, str, str, str, str, str]) -> str:
    slug, title, decision, core, gate, risk = entry
    doc_id = f"DOC-{index:02d}"
    return f"""
---
id: {doc_id}
status: working-specification
updated: {UPDATED}
owners: [program]
---

# {title}

[Documentation index](README.md) · [Program charter](00-charter.md) · [Risk register](40-risk-register.md) · [Decision log](48-decision-log.md)

## Decision

{decision}

## Scope

{bullets(core)}

This document defines the intended architecture and evidence contract. It is not proof that the capability exists. Implementation status must be reported separately from target behavior, and external licensing or platform approval must never be presented as an engineering certainty.

## Engineering rules

- Inputs from web content, files, extensions, models, tools, IPC peers, and network services are untrusted unless a narrower trust statement is documented.
- Resource ownership, cancellation, deadlines, quotas, and failure behavior are explicit at every process boundary.
- Correctness work begins with standards and minimized tests; optimization begins with traces from reproducible workloads.
- Security, privacy, accessibility, internationalization, and recovery are design dimensions, not release polish.
- New complexity requires a measurable user or compatibility outcome and an owner for long-term maintenance.

## Architecture and data flow

The subsystem exposes typed interfaces rather than sharing mutable global state. Privileged operations flow through a broker or policy service. Persistent changes use transactional or journaled boundaries. Diagnostics carry identifiers and structured reasons while avoiding page content and secrets by default. Cross-process state is versioned so stale replies and agent proposals can be rejected.

## Performance accounting

The implementation records CPU time, allocation, retained memory, queue delay, I/O, wakeups, and presentation latency attributable to browser-owned work. Improvements are evaluated against correctness, isolation, and restoration behavior. A lower number achieved by skipping work, silently discarding state, changing the page corpus, or weakening isolation is not accepted as an optimization.

## Validation gate

- {gate}
- Unit and property tests cover local invariants.
- Integration tests cover cancellation, crash, restart, malformed input, and resource pressure.
- Conformance or reference tests are linked where a standard defines behavior.
- Results include build identifiers, environment, raw artifacts, and known limitations.

## Security and privacy review

The review records assets, attacker control, process role, capabilities, persistent data, external providers, logs, and deletion behavior. Any new native or unsafe boundary needs a focused threat model and fuzz target. Any model-visible field needs purpose, sensitivity, retention, and egress rules.

## Principal failure mode

{risk}

The subsystem must fail closed for authority decisions and fail recoverably for ordinary compatibility or performance defects. User-visible recovery state is preferable to silent corruption or hidden privilege expansion.

## Non-goals

This specification does not authorize embedding an existing browser engine, writing custom cryptography, claiming unsupported proprietary integrations, removing process isolation for benchmark results, or allowing a model to bypass deterministic policy.

## Open research

Implementation issues should record competing designs, smallest useful prototype, measurement plan, decision date, and ADR requirement. Unresolved questions remain visible in [Open research questions](47-open-questions.md).

## Acceptance checklist

- [ ] Interfaces and trust boundaries are documented.
- [ ] Stable requirements and tests are linked.
- [ ] Performance budgets and measurement disclosures are defined.
- [ ] Security, privacy, accessibility, and recovery reviews are complete.
- [ ] Known gaps and external dependencies are public.

{extras(slug)}
"""


def docs_index() -> str:
    groups = {
        "Program": range(0, 4),
        "Engine architecture": range(4, 18),
        "Product and performance": range(18, 24),
        "Security and privacy": range(24, 28),
        "AI": range(28, 33),
        "Quality and operations": range(33, 45),
        "Reference": range(45, 49),
    }
    lines = ["# Turing documentation", "", "These documents define targets, gates, and risks. They do not claim that the browser is production-ready.", ""]
    for group, indexes in groups.items():
        lines.append(f"## {group}")
        lines.append("")
        for i in indexes:
            slug, title, *_ = DOCS[i]
            lines.append(f"- [{title}]({slug})")
        lines.append("")
    return "\n".join(lines)


def root_files() -> None:
    write("README.md", f"""
# Turing Browser

> **Status:** architecture and bootstrap research only. This repository is not yet a usable or security-reviewed browser and makes no Chrome-parity claim.

Turing is a working codename for an independent, Rust-first browser and web-engine program. The long-term target is broad modern-web capability, developer-first tooling, restrained native-feeling UI, evidence-backed performance, and optional AI assistance that cannot inherit ambient browser authority.

## The boundary

Turing will not embed or fork Chromium, Gecko, or WebKit. It will own browser behavior: parsing, DOM, style, layout, paint integration, navigation policy, process orchestration, UI, DevTools protocol, and agent authorization. It will still use audited foundations for cryptography, Unicode data, text shaping, compression, image/media codecs, and operating-system sandboxing. Reimplementing those primitives would increase risk without making the engine independent.

## Start here

- [Program charter](docs/00-charter.md)
- [Product requirements](docs/01-product-requirements.md)
- [Capability parity matrix](docs/02-capability-parity.md)
- [Language research](docs/03-language-research.md)
- [Architecture overview](docs/04-architecture-overview.md)
- [Security model](docs/24-security-model.md)
- [AI architecture](docs/28-ai-architecture.md)
- [Roadmap](docs/38-roadmap.md)
- [Risk register](docs/40-risk-register.md)
- [Complete documentation index](docs/README.md)

## Bootstrap code

The dependency-free Rust workspace encodes a few foundational invariants: process roles, tab lifecycle transitions, origin- and document-bound agent grants, bounded IPC, ordered rendering stages, and a minimal shell. It is intentionally not a rendering engine implementation.

```bash
python3 scripts/validate_repository.py
cargo fmt --all -- --check
cargo test --workspace
cargo run -p turing-shell
```

## Performance claims

The target is at least 35% lower browser-owned memory than a declared comparison baseline in a reproducible 30-tab workload while retaining equivalent isolation. Every report must disclose the page corpus, process assignment, frozen/discarded tabs, restoration correctness, latency, and measurement APIs. Turing will not call tab discard or weakened isolation a free memory win.

## AI claims

AI is optional. Models run outside trusted browser processes, observe policy-filtered state, propose structured actions, and receive no direct credentials or unrestricted tools. A deterministic policy engine validates profile, origins, document version, action class, expiry, confirmation, taint, and egress immediately before execution.

## License

Original bootstrap source is offered under MPL-2.0. The codename and architecture require further legal, trademark, codec, and distribution review before a product release.
""")
    write("LICENSE", """
Mozilla Public License Version 2.0

SPDX-License-Identifier: MPL-2.0

This project is licensed under the Mozilla Public License, version 2.0. The canonical, controlling license text is published by Mozilla at:
https://www.mozilla.org/MPL/2.0/

Source files may also carry the standard notice: "This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0."
""")
    write("CONTRIBUTING.md", """
# Contributing

Read the charter, requirements, security model, dependency policy, and relevant ADR before changing architecture. Open an issue with the capability, threat boundary, smallest testable slice, standards references, performance budget, and expected evidence. Keep pull requests narrow. New dependencies, unsafe code, IPC messages, persistent formats, permissions, model-visible data, or platform privileges require explicit review.

Required local checks are `python3 scripts/validate_repository.py`, `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`, and `cargo test --workspace`. Compatibility changes include a minimized conformance or regression test. Performance changes include raw measurements and disclosure metadata. Security fixes should not be disclosed publicly before coordination under SECURITY.md.

Contributions are accepted under MPL-2.0 and must include a Developer Certificate of Origin sign-off (`Signed-off-by:`) until a different contributor agreement is adopted. Be precise about what is implemented, experimental, blocked, or merely planned.
""")
    write("SECURITY.md", """
# Security policy

The bootstrap is research software and is not safe for ordinary browsing. Do not use it with real credentials, sensitive profiles, or untrusted sites.

Report suspected vulnerabilities privately through GitHub's private vulnerability reporting for this repository when enabled. Otherwise contact the repository owner without opening a public issue. Include affected commit, platform, process role, reproduction, impact, and whether exploit details are already public. Do not include real user data.

The project aims to acknowledge reports within seven days, establish severity and coordination within fourteen days, and publish fixes and advisories when users can act. These are targets, not a staffed service-level guarantee. Security-sensitive releases require threat-model review, fuzzing evidence, sandbox verification, signed provenance, and rollback planning.
""")
    write("GOVERNANCE.md", """
# Governance

The repository owner is the bootstrap maintainer and final decision maker until a multi-maintainer charter is adopted. Decisions affecting trust boundaries, language policy, engine independence, storage formats, update trust, agent authority, licensing, or compatibility commitments require an ADR. Ordinary implementation choices remain in pull requests.

Maintainers must distinguish research targets from shipped capability, publish conflicts of interest, avoid private feature promises, and keep risk owners current. A future steering group should include engine, security, accessibility, performance, release, and user-representation perspectives. No single commercial model or external integration may redefine browser security policy without public review.
""")
    write("CODE_OF_CONDUCT.md", """
# Code of conduct

Participate professionally. Harassment, threats, discrimination, doxxing, sexualized conduct, deliberate disruption, and retaliation are not accepted. Technical criticism must address evidence and design rather than personal attributes. Security disclosures and private user data must remain confidential during coordination.

Report conduct concerns privately to the repository owner. Enforcement may include a warning, temporary restriction, removal from project spaces, or referral to the hosting platform. This compact bootstrap policy should be replaced by a fully reviewed community code before broad contributor recruitment.
""")
    write("Cargo.toml", """
[workspace]
members = [
  "crates/turing-core",
  "crates/turing-ipc",
  "crates/turing-render",
  "crates/turing-shell",
]
resolver = "2"

[workspace.package]
edition = "2024"
license = "MPL-2.0"
rust-version = "1.85"
version = "0.0.1"

[workspace.lints.rust]
unsafe_code = "forbid"

[workspace.lints.clippy]
all = "warn"
pedantic = "warn"
""")
    write("rust-toolchain.toml", """
[toolchain]
channel = "stable"
components = ["clippy", "rustfmt"]
profile = "minimal"
""")
    write("deny.toml", """
[advisories]
yanked = "deny"

[bans]
multiple-versions = "warn"
wildcards = "deny"

[licenses]
confidence-threshold = 0.93
allow = ["MPL-2.0", "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unicode-3.0"]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
""")
    write(".gitignore", """
/target/
Cargo.lock
*.profraw
*.trace
.DS_Store
.vscode/
.idea/
__pycache__/
""")
    write(".editorconfig", """
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{yml,yaml,json,toml}]
indent_size = 2
""")


def github_files() -> None:
    write(".github/CODEOWNERS", "* @byronwade\n")
    write(".github/pull_request_template.md", """
## Change

Describe the capability, user impact, and why this is the smallest coherent change.

## Evidence

- [ ] Tests or conformance cases
- [ ] Security and privacy review
- [ ] Performance data and disclosure record when relevant
- [ ] Accessibility and internationalization review when relevant
- [ ] Documentation and ADR links

## Risk

List new privileges, unsafe/FFI code, dependencies, persistent data, IPC, model context, external services, known gaps, and rollback plan.
""")
    write(".github/ISSUE_TEMPLATE/bug.yml", """
name: Bug report
description: Reproducible defect in implemented bootstrap behavior
title: "bug: "
body:
  - type: markdown
    attributes:
      value: Do not report security vulnerabilities publicly. This repository is research software.
  - type: input
    id: commit
    attributes:
      label: Commit and platform
    validations:
      required: true
  - type: textarea
    id: repro
    attributes:
      label: Minimal reproduction and expected behavior
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Logs, traces, tests, and data-handling notes
""")
    write(".github/ISSUE_TEMPLATE/feature.yml", """
name: Capability proposal
description: Propose a measurable browser capability or research experiment
title: "proposal: "
body:
  - type: textarea
    id: outcome
    attributes:
      label: User or compatibility outcome
    validations:
      required: true
  - type: textarea
    id: boundary
    attributes:
      label: Trust boundary, standards basis, and non-goals
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Smallest prototype, tests, metrics, and decision gate
    validations:
      required: true
""")
    write(".github/ISSUE_TEMPLATE/security.yml", """
name: Security design review
description: Public design review without vulnerability details
title: "security-design: "
body:
  - type: markdown
    attributes:
      value: Suspected vulnerabilities must use private reporting, not this form.
  - type: textarea
    id: assets
    attributes:
      label: Assets, attackers, entry points, and trust boundaries
    validations:
      required: true
  - type: textarea
    id: authority
    attributes:
      label: New privileges, data, IPC, FFI, model, or external-service access
    validations:
      required: true
  - type: textarea
    id: tests
    attributes:
      label: Abuse cases, fuzzing, sandbox, and rollback evidence
    validations:
      required: true
""")
    write(".github/workflows/ci.yml", """
name: CI
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt, clippy
      - run: python3 scripts/validate_repository.py
      - run: cargo fmt --all -- --check
      - run: cargo clippy --workspace --all-targets -- -D warnings
      - run: cargo test --workspace
""")
    write(".github/workflows/docs.yml", """
name: Documentation integrity
on:
  pull_request:
    paths:
      - "**/*.md"
      - "scripts/validate_repository.py"
      - "schemas/**"
permissions:
  contents: read
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python3 scripts/validate_repository.py
""")
    write(".github/workflows/security.yml", """
name: Security baseline
on:
  pull_request:
  schedule:
    - cron: "17 7 * * 1"
permissions:
  contents: read
jobs:
  policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: EmbarkStudios/cargo-deny-action@v2
      - run: cargo test --workspace
      - run: test "$(grep -R --include='*.rs' -n 'unsafe' crates | wc -l)" -eq 0
""")


def script_files() -> None:
    write("scripts/validate_repository.py", r'''
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILES = 89
errors: list[str] = []
files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
if len(files) != EXPECTED_FILES:
    errors.append(f"expected {EXPECTED_FILES} files, found {len(files)}")

for path in files:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"non-UTF-8 file: {path.relative_to(ROOT)}")
        continue
    if not text.endswith("\n"):
        errors.append(f"missing final newline: {path.relative_to(ROOT)}")
    for number, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            errors.append(f"trailing whitespace: {path.relative_to(ROOT)}:{number}")
        if "\t" in line:
            errors.append(f"tab character: {path.relative_to(ROOT)}:{number}")

for path in ROOT.rglob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

for path in ROOT.rglob("*.toml"):
    try:
        tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid TOML {path.relative_to(ROOT)}: {exc}")

link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for target in link_re.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"broken link {target!r} in {path.relative_to(ROOT)}")

all_markdown = "\n".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.md"))
if len(set(re.findall(r"BR-\d{3}", all_markdown))) != 46:
    errors.append("stable requirement inventory is not exactly 46 IDs")
if len(set(re.findall(r"R-\d{3}", all_markdown))) != 35:
    errors.append("risk inventory is not exactly 35 IDs")
if len(list((ROOT / "adr").glob("[0-9][0-9][0-9][0-9]-*.md"))) != 6:
    errors.append("ADR inventory is not exactly six decisions")
if "not yet a usable or security-reviewed browser" not in (ROOT / "README.md").read_text(encoding="utf-8"):
    errors.append("README safety status is missing")
for path in (ROOT / "crates").rglob("*.rs"):
    if re.search(r"\bunsafe\b", path.read_text(encoding="utf-8")):
        errors.append(f"unsafe Rust is forbidden in bootstrap: {path.relative_to(ROOT)}")

if errors:
    print("repository validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print(f"validated {len(files)} files, 46 requirements, 35 risks, and 6 ADRs")
''')
    write("scripts/benchmark_stub.py", r'''
from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser(description="Record a disclosed Turing benchmark sample; this tool does not run the benchmark.")
parser.add_argument("--browser", required=True)
parser.add_argument("--build", required=True)
parser.add_argument("--scenario", required=True)
parser.add_argument("--metric", required=True)
parser.add_argument("--value", required=True, type=float)
parser.add_argument("--unit", required=True)
parser.add_argument("--page-corpus", required=True)
parser.add_argument("--isolation", required=True)
parser.add_argument("--lifecycle", required=True)
parser.add_argument("--measurement-api", required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
record = {
    "schema_version": 1,
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "browser": args.browser,
    "build": args.build,
    "scenario": args.scenario,
    "metric": args.metric,
    "value": args.value,
    "unit": args.unit,
    "environment": {"platform": platform.platform(), "python": platform.python_version()},
    "disclosure": {
        "page_corpus": args.page_corpus,
        "isolation_mode": args.isolation,
        "tab_lifecycle": args.lifecycle,
        "measurement_api": args.measurement_api,
    },
    "claim_status": "unreviewed-sample",
}
args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(args.output)
''')


def schema_files() -> None:
    write("schemas/agent-action.schema.json", json.dumps({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://turing.invalid/schemas/agent-action.schema.json",
        "title": "Turing agent action proposal",
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "profile_id", "top_origin", "frame_origin", "document_version", "action_class", "target", "expires_at", "nonce", "confirmation"],
        "properties": {
            "version": {"const": 1},
            "profile_id": {"type": "string", "minLength": 1},
            "top_origin": {"type": "string", "minLength": 1},
            "frame_origin": {"type": "string", "minLength": 1},
            "document_version": {"type": "integer", "minimum": 0},
            "action_class": {"enum": ["observe", "navigate", "input", "submit", "download", "permission", "communicate", "purchase", "delete"]},
            "target": {"type": "object"},
            "data_labels": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "expires_at": {"type": "string", "format": "date-time"},
            "nonce": {"type": "string", "minLength": 16},
            "confirmation": {"enum": ["not-required", "required", "confirmed", "denied"]},
        },
    }, indent=2))
    write("schemas/benchmark-result.schema.json", json.dumps({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://turing.invalid/schemas/benchmark-result.schema.json",
        "title": "Turing benchmark result",
        "type": "object",
        "additionalProperties": True,
        "required": ["schema_version", "recorded_at", "browser", "build", "scenario", "metric", "value", "unit", "environment", "disclosure", "claim_status"],
        "properties": {
            "schema_version": {"const": 1},
            "value": {"type": "number"},
            "disclosure": {"type": "object", "required": ["page_corpus", "isolation_mode", "tab_lifecycle", "measurement_api"]},
            "claim_status": {"enum": ["unreviewed-sample", "reviewed", "retracted"]},
        },
    }, indent=2))
    write("schemas/process-capability.schema.json", json.dumps({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://turing.invalid/schemas/process-capability.schema.json",
        "title": "Turing process capability manifest",
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "role", "sandbox_profile", "capabilities", "forbidden"],
        "properties": {
            "version": {"const": 1},
            "role": {"enum": ["ui", "browser", "renderer", "network", "storage", "gpu", "utility", "agent"]},
            "sandbox_profile": {"type": "string", "minLength": 1},
            "capabilities": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "forbidden": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        },
    }, indent=2))


def adr_files() -> None:
    write("adr/README.md", """
# Architecture decision records

ADRs are immutable after acceptance except for status and links to a superseding ADR. Significant changes to engine independence, trusted languages, process boundaries, IPC authority, persistent formats, agent permissions, release trust, or licensing require an ADR.

See the [decision log](../docs/48-decision-log.md).
""")
    for filename, title, status, context, decision, consequences in ADRS:
        write(f"adr/{filename}", f"""
# {title}

- Status: {status}
- Date: {UPDATED}
- Owners: program

## Context

{context}

## Decision

{decision}

## Consequences

{consequences}

## Validation

The decision remains accepted only while implementation and tests preserve its stated boundary. A contradictory change must link a superseding ADR, migration plan, and risk review.

## Related documents

- [Architecture overview](../docs/04-architecture-overview.md)
- [Security model](../docs/24-security-model.md)
- [Risk register](../docs/40-risk-register.md)
""")


def rust_files() -> None:
    manifest = lambda name, extra="": f'''[package]\nname = "{name}"\nversion.workspace = true\nedition.workspace = true\nlicense.workspace = true\nrust-version.workspace = true\n\n[lints]\nworkspace = true\n{extra}'''
    write("crates/turing-core/Cargo.toml", manifest("turing-core"))
    write("crates/turing-core/src/lib.rs", r'''
#![forbid(unsafe_code)]

use std::fmt;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProcessRole { Ui, Browser, Renderer, Network, Storage, Gpu, Utility, Agent }

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum TabState { Active, Background, Frozen, Discarded, Restoring, Closed }

#[derive(Debug, Eq, PartialEq)]
pub enum TransitionError { Illegal { from: TabState, to: TabState } }

#[derive(Debug)]
pub struct TabLifecycle { state: TabState, document_version: u64 }

impl TabLifecycle {
    #[must_use]
    pub const fn new() -> Self { Self { state: TabState::Active, document_version: 0 } }
    #[must_use]
    pub const fn state(&self) -> TabState { self.state }
    #[must_use]
    pub const fn document_version(&self) -> u64 { self.document_version }
    pub fn navigate(&mut self) { self.document_version = self.document_version.saturating_add(1); }
    pub fn transition(&mut self, to: TabState) -> Result<(), TransitionError> {
        use TabState::{Active, Background, Closed, Discarded, Frozen, Restoring};
        let legal = matches!((self.state, to),
            (Active, Background | Closed) |
            (Background, Active | Frozen | Discarded | Closed) |
            (Frozen, Active | Background | Discarded | Closed) |
            (Discarded, Restoring | Closed) |
            (Restoring, Active | Background | Discarded | Closed));
        if legal { self.state = to; Ok(()) } else { Err(TransitionError::Illegal { from: self.state, to }) }
    }
}

impl Default for TabLifecycle { fn default() -> Self { Self::new() } }

#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct Origin(String);

impl Origin {
    pub fn parse(value: impl Into<String>) -> Result<Self, OriginError> {
        let value = value.into();
        let valid = (value.starts_with("https://") || value.starts_with("http://"))
            && !value.chars().any(char::is_whitespace) && value.len() > 8;
        valid.then_some(Self(value)).ok_or(OriginError)
    }
    #[must_use]
    pub fn as_str(&self) -> &str { &self.0 }
}

#[derive(Debug, Eq, PartialEq)]
pub struct OriginError;
impl fmt::Display for OriginError { fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { f.write_str("invalid bootstrap origin") } }

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AgentAction { Observe, Navigate, Input, Submit, Download, Permission, Communicate, Purchase, Delete }

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AgentGrant {
    pub profile_id: String,
    pub origin: Origin,
    pub document_version: u64,
    pub action: AgentAction,
    pub expires_at_ms: u64,
    pub confirmed: bool,
}

#[derive(Clone, Debug)]
pub struct ActionContext<'a> {
    pub profile_id: &'a str,
    pub origin: &'a Origin,
    pub document_version: u64,
    pub action: AgentAction,
    pub now_ms: u64,
    pub sensitive: bool,
}

impl AgentGrant {
    #[must_use]
    pub fn authorizes(&self, context: &ActionContext<'_>) -> bool {
        self.profile_id == context.profile_id
            && &self.origin == context.origin
            && self.document_version == context.document_version
            && self.action == context.action
            && context.now_ms <= self.expires_at_ms
            && (!context.sensitive || self.confirmed)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn lifecycle_rejects_direct_restore_from_active() {
        let mut tab = TabLifecycle::new();
        assert!(tab.transition(TabState::Restoring).is_err());
    }
    #[test]
    fn stale_agent_grant_fails_closed() {
        let origin = Origin::parse("https://example.test").expect("origin");
        let grant = AgentGrant { profile_id: "p1".into(), origin: origin.clone(), document_version: 4, action: AgentAction::Submit, expires_at_ms: 100, confirmed: true };
        let context = ActionContext { profile_id: "p1", origin: &origin, document_version: 5, action: AgentAction::Submit, now_ms: 50, sensitive: true };
        assert!(!grant.authorizes(&context));
    }
}
''')
    write("crates/turing-ipc/Cargo.toml", manifest("turing-ipc", "\n[dependencies]\nturing-core = { path = \"../turing-core\" }\n"))
    write("crates/turing-ipc/src/lib.rs", r'''
#![forbid(unsafe_code)]

use std::collections::VecDeque;
use turing_core::ProcessRole;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Capability { RenderDocument, FetchForOrigin, ReadOriginStorage, WriteOriginStorage, SubmitGpuCommands, ProposeAgentAction }

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Envelope<T> {
    pub protocol_version: u16,
    pub source: ProcessRole,
    pub destination: ProcessRole,
    pub request_id: u64,
    pub deadline_ms: u64,
    pub capability: Capability,
    pub payload: T,
}

#[derive(Debug, Eq, PartialEq)]
pub enum QueueError { Full, Oversized }

#[derive(Debug)]
pub struct BoundedQueue<T> {
    messages: VecDeque<(usize, T)>,
    max_messages: usize,
    max_bytes: usize,
    bytes: usize,
}

impl<T> BoundedQueue<T> {
    #[must_use]
    pub fn new(max_messages: usize, max_bytes: usize) -> Self { Self { messages: VecDeque::new(), max_messages, max_bytes, bytes: 0 } }
    pub fn push(&mut self, encoded_bytes: usize, value: T) -> Result<(), QueueError> {
        if encoded_bytes > self.max_bytes { return Err(QueueError::Oversized); }
        if self.messages.len() >= self.max_messages || self.bytes.saturating_add(encoded_bytes) > self.max_bytes { return Err(QueueError::Full); }
        self.messages.push_back((encoded_bytes, value));
        self.bytes += encoded_bytes;
        Ok(())
    }
    pub fn pop(&mut self) -> Option<T> {
        self.messages.pop_front().map(|(size, value)| { self.bytes -= size; value })
    }
    #[must_use]
    pub const fn retained_bytes(&self) -> usize { self.bytes }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn queue_enforces_both_bounds() {
        let mut queue = BoundedQueue::new(1, 8);
        assert_eq!(queue.push(8, 1), Ok(()));
        assert_eq!(queue.push(1, 2), Err(QueueError::Full));
        assert_eq!(queue.pop(), Some(1));
        assert_eq!(queue.retained_bytes(), 0);
    }
}
''')
    write("crates/turing-render/Cargo.toml", manifest("turing-render"))
    write("crates/turing-render/src/lib.rs", r'''
#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub enum Stage { Parse, Style, Layout, Paint, Raster, Composite, Present }

#[derive(Debug, Default)]
pub struct FramePipeline { completed: Vec<Stage> }

#[derive(Debug, Eq, PartialEq)]
pub enum PipelineError { OutOfOrder { expected: Stage, received: Stage }, AlreadyComplete }

impl FramePipeline {
    #[must_use]
    pub fn new() -> Self { Self::default() }
    pub fn complete(&mut self, stage: Stage) -> Result<(), PipelineError> {
        const ORDER: [Stage; 7] = [Stage::Parse, Stage::Style, Stage::Layout, Stage::Paint, Stage::Raster, Stage::Composite, Stage::Present];
        let Some(expected) = ORDER.get(self.completed.len()).copied() else { return Err(PipelineError::AlreadyComplete); };
        if stage != expected { return Err(PipelineError::OutOfOrder { expected, received: stage }); }
        self.completed.push(stage);
        Ok(())
    }
    #[must_use]
    pub fn is_presented(&self) -> bool { self.completed.last() == Some(&Stage::Present) }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn paint_cannot_precede_layout() {
        let mut pipeline = FramePipeline::new();
        assert!(pipeline.complete(Stage::Paint).is_err());
    }
}
''')
    write("crates/turing-shell/Cargo.toml", manifest("turing-shell", "\n[dependencies]\nturing-core = { path = \"../turing-core\" }\nturing-ipc = { path = \"../turing-ipc\" }\nturing-render = { path = \"../turing-render\" }\n"))
    write("crates/turing-shell/src/main.rs", r'''
#![forbid(unsafe_code)]

use turing_core::{TabLifecycle, TabState};
use turing_ipc::BoundedQueue;
use turing_render::{FramePipeline, Stage};

fn main() {
    let mut tab = TabLifecycle::new();
    tab.transition(TabState::Background).expect("legal lifecycle transition");
    let mut queue = BoundedQueue::new(16, 64 * 1024);
    queue.push(5, "hello").expect("bounded bootstrap message");
    let mut frame = FramePipeline::new();
    for stage in [Stage::Parse, Stage::Style, Stage::Layout, Stage::Paint, Stage::Raster, Stage::Composite, Stage::Present] {
        frame.complete(stage).expect("ordered frame stage");
    }
    println!("Turing bootstrap: tab={:?}, queued={}, presented={}", tab.state(), queue.retained_bytes(), frame.is_presented());
}
''')


def main() -> None:
    clean_repository()
    root_files()
    github_files()
    script_files()
    schema_files()
    write("docs/README.md", docs_index())
    for index, entry in enumerate(DOCS):
        write(f"docs/{entry[0]}", render_doc(index, entry))
    adr_files()
    rust_files()
    files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    if len(files) != 89:
        raise SystemExit(f"generator produced {len(files)} files, expected 89")
    print("generated 89-file Turing browser program")


if __name__ == "__main__":
    main()
