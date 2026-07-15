# Research Log

This log records material research-program and documentation-governance changes. Detailed technical conclusions belong in the owning Blueprint chapter, requirement, risk, ADR, benchmark, or backlog entry.

## 2026-07-15 — Canonical documentation system

Decision:

- place canonical prose under `docs/`;
- retain root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md` only for discovery and repository control;
- place the complete Blueprint under `docs/blueprint-v1/`;
- keep machine-readable requirements, risks, backlog, process capabilities, benchmark manifests, and agent-action schemas beside the Blueprint;
- require same-change documentation for code, configuration, dependencies, interfaces, features, risks, and repository structure;
- add static link, location, registry, index-coverage, and diff-based documentation validation;
- remove temporary transfer and self-modifying bootstrap machinery from the durable repository structure.

Rationale:

A browser project has too many cross-cutting security, compatibility, performance, accessibility, and operational obligations for documentation to be optional or scattered. Centralizing canonical prose and requiring impact review reduces silent drift while preserving standard GitHub discovery files.

Affected records:

- root `AGENTS.md`;
- `docs/documentation-policy.md`;
- `docs/repository-map.md`;
- `docs/contributing.md`;
- GitHub issue and pull-request templates;
- repository validation workflow and tools.

Residual risk:

Automation can verify location, links, registries, and minimum same-change behavior, but it cannot prove that prose is semantically complete. Human and agent review must still apply the full impact matrix.

## Entry template

```text
## YYYY-MM-DD — Topic

Question:
Sources and versions:
Method and environment:
Observations:
Inference:
Decision:
Alternatives rejected:
Security/privacy impact:
Compatibility/accessibility impact:
Performance/memory/energy impact:
Licensing/operational impact:
Affected requirements, risks, ADRs, work packages, and documents:
Unresolved questions:
Next evidence required:
```
