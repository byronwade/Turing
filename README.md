# Turing Browser

Turing is the working codename for an independent, Rust-first browser and web-engine research program.

The long-term target is a minimal, fast, secure, developer-first browser that can also serve everyday users and capability-scoped AI agents. The engine is intended to be independent: release paths must not embed Chromium, WebKit, Gecko, Electron, CEF, an operating-system web view, or remote rendering.

This repository is not yet a production browser and is not safe for sensitive or arbitrary hostile browsing. It currently contains the architecture, security model, compatibility inventory, performance contract, AI authorization model, roadmap, risk register, machine-readable requirements, active engine research, detailed engineering books, and a small executable Rust model of foundational invariants.

## Start here

- [Project orientation](docs/start-here.md)
- [Documentation index](docs/README.md)
- [Detailed engineering books](docs/README.md#detailed-engineering-books)
- [Active research](docs/research/README.md)
- [Blueprint v1](docs/blueprint-v1/README.md)
- [Documentation policy](docs/documentation-policy.md)
- [Repository map](docs/repository-map.md)
- [Security policy](docs/security.md)
- [Contributing](docs/contributing.md)
- [Agent instructions](AGENTS.md)

## Project priorities

1. Security and correctness.
2. Honest compatibility and risk disclosure.
3. Minimal memory, CPU, energy, dependency, and trusted-code cost.
4. Accessibility and user control.
5. Developer-grade tooling and a restrained native interface.
6. AI capabilities that never receive ambient browser authority.

## Current executable scope

The `prototype/` package is a dependency-free Rust model of process roles, bounded IPC, tab lifecycle transitions, rendering invalidation order, scoped request identity, and deterministic agent authorization. It does not parse HTML, render pages, execute JavaScript, open network connections, or create windows.

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

All durable prose documentation belongs under `docs/`. Every code, configuration, dependency, interface, feature, risk, or repository-structure change must update every affected document in the same change.
