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
