## Summary

Describe the change, why it belongs in Turing, and whether it is research, specification, prototype, partial implementation, release-gated work, or supported behavior.

## Requirements, risks, decisions, and work packages

- Requirements:
- Risks:
- ADRs/design notes:
- Work packages/milestones:
- Research questions/experiments:

## Behavior and architecture

Describe user-visible and developer-visible behavior, process roles, data flow, lifecycle, privilege boundaries, schemas, protocols, migrations, and failure behavior.

## Evidence

- Tests:
- Negative/recovery tests:
- Conformance:
- Fuzzing/sanitizers:
- Performance, memory, startup, and energy:
- Accessibility/platform validation:
- Reproduction environment:
- Research sources/versions and confidence:

## Security and privacy

Describe trust-boundary, sandbox, site-isolation, origin/site/profile, credential, update, logging, crash-reporting, extension, DevTools, automation, provider/tool, and agent implications. Write `none` only after considering each relevant category.

## Compatibility and unsupported behavior

State standards behavior, platform differences, media/printing/PDF implications, migrations, known gaps, residual risks, and rollback behavior.

## Dependencies and unsafe code

List dependency, license, generated-code, native-code, schema, toolchain, model/tool/provider, or `unsafe` changes.

## Documentation impact

- Owning Blueprint chapters updated:
- Detailed engineering books updated:
- Canonical policy/research documents updated:
- Documents reviewed but unchanged, with reason:
- Requirements/risks/ADRs/backlog/registries updated:
- `docs/repository-map.md` updated for additions, removals, or renames:
- `docs/README.md`, affected book indexes, and inbound links updated for documentation topology changes:
- Stale claims and obsolete paths removed:

A non-documentation change without affected canonical documentation is incomplete. A research document does not change accepted architecture until the owning records are updated.

## Validation

```bash
python3 tools/validate_blueprint.py
cargo fmt --manifest-path prototype/Cargo.toml -- --check
cargo test --manifest-path prototype/Cargo.toml --all-targets
cargo run --manifest-path prototype/Cargo.toml --quiet
```

## Release impact

State the maturity label and release gates affected. A visual demo, detailed design, or competitive study is not production-readiness evidence.

## Professional controls

- Owner and backup status:
- RFC/ADR/design-note class:
- Traceability/phase impact:
- Required cross-cutting reviews:
- Configuration, Plug-in, embedding, dependency, migration, release, support, and expiring exception impact:

<!-- MARKET-STRATEGY-2026-07 -->
## Market strategy and opportunity impact

- Affected `OP-*` records:
- Target user/job and evidence:
- Promotion state: research only / requirement proposal / accepted scope:
- Switching, migration, recovery, resource, AI-authority, accessibility, and lock-in effects:
- Competing behavior and non-copying/provenance review:

<!-- NATIVE-UI-ARCHITECTURE-2026-07 -->
## Native UI impact

- [ ] No native UI impact.
- [ ] Updated toolkit-neutral state/commands, adapter, platform, surface, component, token, accessibility, or UI budget documentation.
- [ ] Confirmed no webview or runtime React/JavaScript dependency entered trusted chrome.
- [ ] Attached relevant adapter conformance, accessibility, failure, binary, memory, latency, or page-surface evidence.

<!-- AGENT-PRODUCTION-READINESS-2026-07 -->
## Agent and production controls

- [ ] Agent-generated work links an approved task manifest, run provenance, independent review, evidence bundle, and rollback where applicable.
- [ ] This change does not give an implementation agent self-approval, signing, disclosure, or stable-promotion authority.
- [ ] Production scope, platform, SLO, release, update, service, support, legal, or signing changes update `docs/production-readiness/` and machine gates.
