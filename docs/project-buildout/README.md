# Professional Project Buildout and Operating Handbook

Status: detailed research and professional operating baseline  
Owner: program architecture and engineering operations  
Last researched: 2026-07-16

This handbook is the control plane for turning Turing's research into a multi-year, multi-maintainer implementation. It defines who decides, how work becomes accepted, how evidence is traced, how the repository is structured, how contributors reproduce the environment, and how the product is released and maintained.

## Reading order

1. [01 Program Lifecycle And Phase Gates](01-program-lifecycle-and-phase-gates.md)
2. [02 Ownership Codeowners And Maintainer Ladder](02-ownership-codeowners-and-maintainer-ladder.md)
3. [03 Rfc Adr And Design Review Process](03-rfc-adr-and-design-review-process.md)
4. [04 Requirements Traceability And Evidence](04-requirements-traceability-and-evidence.md)
5. [05 Repository Build Toolchain And Coding Standards](05-repository-build-toolchain-and-coding-standards.md)
6. [06 Api Schema Configuration And Version Governance](06-api-schema-configuration-and-version-governance.md)
7. [07 Cross Cutting Security Performance Accessibility Privacy](07-cross-cutting-security-performance-accessibility-privacy.md)
8. [08 Release Incident Legal Data And Support](08-release-incident-legal-data-and-support.md)
9. [09 Servo Adoption Decision Framework](09-servo-adoption-decision-framework.md)
10. [10 Product Localization Documentation And Sustainability](10-product-localization-documentation-and-sustainability.md)

## Machine-readable companions

- [Ownership](../blueprint-v1/machine/professional-owners.json)
- [Requirements traceability](../blueprint-v1/machine/professional-traceability.json)
- [Phase gates](../blueprint-v1/machine/professional-phase-gates.json)
- [Review rules](../blueprint-v1/machine/professional-review-rules.json)
- [Exceptions](../blueprint-v1/machine/professional-exceptions.json)

## Non-negotiable rule

A phase or release is incomplete while an applicable control lacks linked evidence, a time-bounded approved exception, or an explicit declaration that it is outside supported scope.

<!-- MARKET-STRATEGY-2026-07 -->
## Market opportunity control

The [market strategy book](../market-strategy/README.md) feeds this handbook through `OP-*` proposals. An opportunity cannot enter accepted scope until ownership, review class, requirements, risks, work packages, traceability, evidence, and phase gates agree.
