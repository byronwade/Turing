# Human Release, Legal, and Incident Capacity Research - July 2026

Status: deferred `RQ-66` research packet; no staffing, legal, release, support, or production claim
Owner: program, security, release operations, incident response, legal-community, support, quality, and documentation-research
Question: What staffing, separation of duties, legal approval, signing ceremony, support term, on-call, and incident-rehearsal evidence is necessary before beta and stable?

This packet connects the existing incident-response, ownership, update, secure-development, SLO, and production-readiness routes. It is a decision and evidence plan, not a staffing plan, legal opinion, release authorization, or proof of operational capacity.

## Source-backed observations

NIST SP 800-61 Rev. 3 frames incident response as part of cybersecurity risk management and emphasizes preparation, detection, response, recovery, and improvement. A Turing incident process therefore needs maintained preparation and rehearsal evidence, not only a document describing who might respond. [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)

GitHub's protected-branch guidance shows that review requirements, status checks, code-owner review, signed commits, linear history, merge queues, and restrictions on bypassing or pushing are separate controls that can be configured for a branch. Repository settings are evidence inputs, not proof that Turing has independent security, legal, release, or incident capacity. [GitHub: About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

Legal and community review cannot be inferred from a license file, source manifest, dependency scanner, or public repository status. Counsel or an explicitly qualified legal reviewer must decide the applicable license, notice, patent, export, trademark, privacy, disclosure, employment, and jurisdiction questions; the record must preserve scope and limitations without presenting it as legal advice.

## Authority separation

The owner-reviewed operating model must keep these roles separate where the risk requires it:

| Role | May decide or perform | Must not silently inherit |
|---|---|---|
| Product/support owner | supported scope, user impact, support term, deprecation and communication policy | security severity, signing, legal approval, or incident closure |
| Security/incident lead | triage, containment recommendation, evidence custody, response coordination | unilateral public disclosure, signing, release promotion, or residual-risk acceptance |
| Engineering/release owner | patch implementation, regression evidence, package preparation, rollback rehearsal | self-approval, signing ceremony, legal clearance, or stable promotion |
| Signing/update authority | approve authorized artifact and metadata transition under policy | source selection, vulnerability severity, support commitment, or incident closure |
| Legal/community reviewer | scoped legal, notice, disclosure, trademark, and community advice | technical readiness, security severity, or release promotion |
| Independent reviewer | challenge evidence, conflicts, exceptions, and claim boundaries | approving their own work or bypassing required owners |
| Backup owner | execute an explicitly delegated role during a recorded absence or conflict | becoming an unnamed substitute for missing qualification or two-person control |

The exact people, backups, access, qualifications, recusal rules, emergency replacement, and two-person controls must come from the ownership registries and a real owner-reviewed record. Role names or email aliases are not evidence of capacity.

## Capacity evidence contract

Before beta or stable consideration, the record must identify:

- supported platforms, versions, channels, product scope, and support term;
- named primary and backup roles for program, security, release, signing, incident, legal/community, support, quality, supply chain, documentation, platform, engine, accessibility, and privacy;
- qualifications, subsystem competence, availability, time-zone/on-call coverage, succession, recusal, inactivity, removal, emergency replacement, and access review;
- protected paths, review rules, CODEOWNERS or equivalent controls, two-person actions, admin/bypass policy, and evidence that the latest change was independently reviewed;
- severity, response, escalation, communication, disclosure, patch, backport, signing, rollout, rollback, minimum-secure-version, and closure authority;
- rehearsal schedule, scenario classes, timing measurements, failure accounting, retained artifacts, postmortem actions, and follow-up verification;
- legal review scope, jurisdiction, unresolved advice, notice and source-offer obligations, patent/codec and trademark boundaries, privacy/disclosure constraints, and expiry or re-review triggers;
- SLO/error-budget linkage, service dependencies, update trust, incident obligations, and the support decision taken when a gate or budget is missed.

Every record must name the owner, independent reviewer, evidence paths and hashes, decision, rationale, limitations, exceptions, expiry, rollback, and synchronized changes to readiness, task, requirement, risk, ownership, support, release, and security records.

## Rehearsal and decision sequence

1. Freeze the proposed beta/stable scope and support boundary.
2. Reconcile primary and backup ownership, access, review, recusal, and two-person control before granting authority.
3. Run private tabletop scenarios for active exploitation, compromised signing, bad update, data-loss or migration failure, renderer or sandbox escape, major compatibility regression, and service outage.
4. Exercise patch, backport, regression, fake-key/update, rollback, communication, disclosure, and recovery paths with production secrets and user data excluded.
5. Obtain independent technical, security, quality, support, and legal/community review for the exact evidence packet.
6. Record the human decision to proceed, hold, restrict, or roll back, then synchronize the relevant `PB-*`, `TASK-*`, requirements, risks, SLOs, ownership, update, incident, and release records.

Failure of a role, backup, escalation, legal review, signing ceremony, support commitment, or rehearsal is a readiness result and must not be hidden by substituting a template, automation, or agent output.

## Current disposition

`RQ-66` remains deferred. The packet makes the cross-lane human-capacity evidence route explicit without naming owners, granting authority, selecting a support term, approving legal posture, changing active/deferred counts, authorizing broad implementation, or changing the `90%` contained-M0 / `0%` full-build measures.

## Retrieval record

- Retrieved 2026-07-19.
- NIST SP 800-61 Rev. 3: https://csrc.nist.gov/pubs/sp/800/61/r3/final
- GitHub protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
