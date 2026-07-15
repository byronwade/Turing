# Turing Browser

> **Status:** architecture, research, and executable policy bootstrap. This repository is not yet a usable or security-reviewed browser and does not claim Chrome parity.

Turing is a working codename for an independent, Rust-first browser and web-engine program. The long-term target is broad modern-web compatibility, a restrained native-feeling UI, developer-first tooling, measurable efficiency under large tab sets, and optional AI assistance that cannot inherit ambient browser authority.

## Start here

1. [Program orientation](START_HERE.md)
2. [Blueprint v1 index](blueprint-v1/README.md)
3. [Product requirements](blueprint-v1/21-product-requirements.md)
4. [Capability parity definition](blueprint-v1/02-capability-parity.md)
5. [Language and dependency strategy](blueprint-v1/03-language-and-dependency-strategy.md)
6. [System architecture](blueprint-v1/04-system-architecture.md)
7. [Security and sandbox model](blueprint-v1/08-security-and-sandbox.md)
8. [Performance and 30-tab methodology](blueprint-v1/09-performance-memory.md)
9. [AI and agent authority model](blueprint-v1/10-ai-agent-platform.md)
10. [Roadmap, work breakdown, and risk register](blueprint-v1/14-roadmap-work-breakdown.md)

## Independence boundary

Turing will not embed or fork Chromium, WebKit, Gecko, Electron, CEF, or an operating-system web view as its release rendering engine. It intends to own browser behavior: HTML/DOM integration, CSS and layout, display-list construction, navigation, process orchestration, permissions, storage partitioning, DevTools, UI, and agent policy.

Independent does **not** mean rewriting cryptography, Unicode data, text shaping, compression, image/media codecs, GPU drivers, or operating-system sandbox mechanisms. Those foundational capabilities should use audited components through narrow, capability-limited interfaces. Reinventing them would increase security and interoperability risk without making the browser engine meaningfully more independent.

## Architecture direction

The planned process model separates browser/UI authority from site-isolated renderers, networking, storage, GPU/composition, hostile decoders, extensions, and AI workers. Messages are typed and bounded. Privileged resources are brokered. A renderer or model is assumed compromiseable and receives no ambient credential, filesystem, cross-origin, or unrestricted network authority.

The [Rust prototype](prototype/) is intentionally not a rendering engine. It encodes several non-negotiable invariants in dependency-free code: explicit process roles, bounded messages, legal tab lifecycle transitions, ordered rendering stages, scoped network requests, origin/profile/document-bound agent grants, confirmation gates, and auditable policy reason codes.

## Performance claims

The goal is to materially reduce **browser-owned** memory under a published 30-tab workload while maintaining equivalent site isolation and preserving user state. Every comparison must disclose the page corpus, browser versions, process count, isolation policy, frozen/discarded tabs, background activity, restoration correctness, latency, and measurement API. Silently discarding most tabs or weakening isolation is not reported as a free memory win.

## AI claims

AI is optional. Models observe policy-filtered semantic state and propose structured actions. A deterministic browser policy layer checks origin, profile, grant lifetime, document epoch, action class, data sensitivity, confirmation state, and egress immediately before execution. Models do not receive raw credential stores or direct privileged tools.

## Repository map

- `blueprint-v1/` — charter, requirements, architecture, engine/runtime plans, security, AI, UX, performance, testing, release operations, roadmap, governance, risk register, ADR index, sources, and initial backlog.
- `blueprint-v1/machine/` — machine-readable requirements, risks, process capabilities, benchmark manifest, and agent-action schema.
- `prototype/` — dependency-free Rust policy and state-machine bootstrap.
- `tools/validate_blueprint.py` — structural validation for requirements, risks, links, schemas, and source invariants.
- `.github/` — issue/PR templates and validation workflow.

## Validation

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml
```

## License and product status

Original bootstrap source is offered under MPL-2.0. Turing is a codename and requires trademark review before product branding. Codec, DRM, platform distribution, and third-party integration rights remain explicit external dependencies. Do not use the current prototype with real credentials, sensitive profiles, or untrusted browsing data.
