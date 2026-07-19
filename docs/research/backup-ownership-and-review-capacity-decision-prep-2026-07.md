# Backup Ownership And Review Capacity Decision Preparation - July 2026

Status: no-claim source-backed decision preparation
Owner: program, security, release operations, support, legal-community, and subsystem owners
Related gate: `PB-019` and `PB-020`
Retrieval date: 2026-07-19
Tested configuration: documentation and repository-control research only; no owner appointment, access grant, signing ceremony, or protected-branch change was performed

## Question

What evidence must prove that Turing has qualified backup owners and independent review capacity for build-critical paths without treating `CODEOWNERS`, a title, a placeholder, or a branch rule as proof of competence or availability?

## Decision status

No backup owner is named or qualified by this report. No production, release, signing, disclosure, legal, incident-closure, or two-person authority is granted. The current `PB-019` status remains `blocked` because the machine inventory records `@byronwade` as the primary and a null backup across the covered scopes.

## Source-backed observations

### Governance requires explicit roles and accountability

The [NIST Cybersecurity Framework 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) Govern function calls for cybersecurity roles, responsibilities, and authorities to be established, communicated, understood, and enforced, with resources aligned to the risk strategy.

Implications for Turing:

- each build-critical scope needs a real role, decision boundary, named person or accountable team, backup, and escalation path;
- a backup must have the competence and access required for the specific path, not merely organizational membership or a general engineering title;
- availability, recusal, inactivity, removal, succession, and emergency replacement must be recorded because ownership that cannot act is not operational coverage;
- owner coverage is an evidence claim with a date and expiry, not a permanent repository attribute.

NIST provides governance outcomes, not Turing's staffing model or authority assignments.

### CODEOWNERS routes review but does not prove qualification

GitHub's [CODEOWNERS documentation](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) describes CODEOWNERS as a way to define individuals or teams responsible for repository paths and request their review. GitHub also notes that owners need repository write access and that code-owner approval can be required through repository settings.

Implications for Turing:

- CODEOWNERS is routing evidence and must be reconciled with the professional owner registry, review rules, escalation policy, and protected paths;
- a matching entry does not prove that the listed person is qualified, available, independent, or capable of emergency response;
- a team entry must resolve to current members, permissions, competence, and a backup route;
- path-pattern precedence, missing files, ownerless paths, and primary-only paths require explicit test results rather than assumptions.

### Branch protection is a control configuration, not a complete control assessment

GitHub's [protected-branch documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) describes requirements such as pull-request reviews, status checks, signed commits, restricted pushes, and limits on bypassing protections. The documentation also notes that administrators or roles with bypass permission may be outside default restrictions unless the repository applies the stricter setting.

Implications for Turing:

- retained evidence must capture the effective rule, matching branch/path scope, bypass actors, required review count, code-owner requirement, stale-review behavior, status-check source, and administrator exceptions;
- a green pull request is not independent review if the author can satisfy or bypass the required reviewer path;
- branch protection must be tested against the actual protected paths and emergency procedures, not inferred from the existence of a rule;
- a repository control cannot substitute for offline signing key separation or a human release authority ceremony.

The checked no-claim [ownership/control source manifest](../project-buildout/machine/ownership-control-source-manifest.json), [manifest schema](../project-buildout/machine/ownership-control-source-manifest.schema.json), and [`validate_ownership_control_sources.py`](../../tools/validate_ownership_control_sources.py) preserve these governance observations across eight evidence axes. They are source identity and control-input records only; they do not name a backup, prove qualification, capture effective repository settings, establish two-person control, or close `PB-019`/`PB-020`.

### Current GitHub control observation

On 2026-07-19, a read-only authenticated GitHub CLI audit of `byronwade/Turing` observed that `main` is the public repository's default branch, the branch-protection endpoint returned `404 Branch not protected`, the rulesets endpoint returned no rulesets, and automatic branch deletion after merge is disabled. The checked `.github/CODEOWNERS` file routes the wildcard and listed path classes to provisional `@byronwade` only. These observations are configuration evidence at the capture date, not owner qualification or proof of effective review independence. They confirm that repository enforcement and backup ownership remain open controls for `PB-019`; no authority or readiness claim follows from the audit.

## Required ownership evidence

For every build-critical scope, the future qualification record must contain:

1. named primary and backup identity, with no placeholders or title-only labels;
2. role level, subsystem competence, and representative path coverage;
3. recent review or implementation evidence sufficient to verify competence;
4. current availability, expected response window, timezone or on-call coverage, and contact route stored under appropriate privacy controls;
5. succession, recusal, inactivity, removal, and emergency replacement rules;
6. access scope, least-privilege review, stale-access review, and expiration or requalification date;
7. reconciliation against professional owners, review rules, CODEOWNERS, escalation policy, support, CI, package, service, and repository-access records;
8. independent reviewer identity and evidence that the reviewer is not relying only on the candidate's assertion;
9. residual risk where a scope remains primary-only, ownerless, or temporarily unavailable;
10. owner decision to accept the evidence or keep `PB-019` blocked.

## Two-person control boundaries

Two-person control must be explicit for actions where one compromised or unavailable person could create irreversible or high-impact outcomes:

- stable or emergency release signing;
- update trust-root, minimum-secure-version, revocation, or stable-channel changes;
- supported-version and security-lifecycle changes;
- security disclosure timing and public advisory approval;
- irreversible profile migration or destructive repair policy;
- release promotion, legal approval, and incident closure;
- changes to protected review, bypass, or authority configuration.

The evidence must name both roles, show independent authentication and review, record the action and timestamp, define unavailable-person handling, and prove that an agent or single owner cannot self-approve the action.

Two names in a document are not two-person control. A single team, shared credential, delegated bypass, or unreviewed emergency path does not satisfy this boundary.

## Reconciliation matrix

| Control surface | Evidence to compare | Failure that keeps `PB-019` blocked |
| --- | --- | --- |
| professional owner registry | scope, primary, backup, authority, expiry | null, placeholder, stale, or contradictory owner |
| CODEOWNERS | path patterns, team membership, write access, precedence | ownerless or primary-only protected path |
| review rules | required reviewer, independence, count, bypass | author can satisfy or bypass the required review |
| escalation policy | severity, timing, alternate route, authority | no reachable backup or no expiry-bound escalation |
| package, CI, and service controls | deployer, maintainer, break-glass access | privileged path has no qualified backup or stale access |
| signing and update controls | key ceremony, threshold, revocation, promotion | one-person or agent-controlled trust change |
| disclosure and incident controls | intake, severity, disclosure, closure | no independent authority or backup coverage |
| repository access | membership, tokens, apps, admin bypass, audit | stale privilege, ownerless path, or unreviewed bypass |

## Stop and recovery rules

If a primary becomes unavailable, the process must not silently promote a title-holder or agent. It must use the documented emergency replacement path, verify qualification and access, record scope and expiry, preserve a two-person requirement where applicable, and produce a later reconciliation record. If no qualified backup exists, the affected operation must remain explicitly blocked or move to a pre-approved bounded degraded mode.

Emergency replacement cannot retroactively prove prior coverage. A temporary waiver must name owner, reason, scope, compensating control, expiry, cleanup, and claim impact.

## Next proof

`PB-019` requires actual named qualification records beyond the checked no-claim template, followed by reconciliation against the owner, review, CODEOWNERS, escalation, access, package, CI, service, signing, disclosure, support, and incident records. An independent reviewer must replace the no-claim readiness-review template with evidence and explicitly accept or hold each scope. Until then, the current primary-only/null-backup state remains the authoritative blocker.

## Claim boundary

This report does not name backups, prove availability or competence, alter `CODEOWNERS`, change branch protection, grant authority, establish two-person control, or support broad-build, production, release, signing, disclosure, legal, incident-closure, or owner-coverage claims.

## References

- [NIST Cybersecurity Framework 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)
- [GitHub about CODEOWNERS](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub managing branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [GitHub branch protection REST API](https://docs.github.com/en/rest/branches/branch-protection)
