# Incident Response And Emergency Patch Decision Preparation - July 2026

Status: no-claim source-backed decision preparation
Owner: security, incident response, release operations, support, legal-community, and documentation-research
Related gate: `PB-018`
Retrieval date: 2026-07-19
Tested configuration: documentation and research only; no private intake, vulnerability, signing key, or production system was used

## Question

What incident-response, severity, disclosure, patch, and recovery properties must Turing document and rehearse before `PB-018` can move beyond planning evidence?

## Decision status

No response team, severity SLA, disclosure authority, supported-version policy, patch channel, signing process, or incident command structure is approved by this report. It turns external guidance into decision criteria and makes the future rehearsal's evidence and authority boundaries explicit.

`PB-018` remains `partial`. The checked incident-patch inventory and no-claim rehearsal/readiness templates define a future exercise, but they do not prove executed tabletop output, emergency patch capacity, supported security versions, disclosure authority, signing authority, incident closure authority, or production-safe browsing.

## Source-backed observations

### NIST treats response as a risk-management capability

NIST's [incident-response program page](https://csrc.nist.gov/Projects/incident-response) identifies SP 800-61 Revision 3 as the current incident-response publication and describes preparation, detection, response, and recovery as activities integrated with cybersecurity risk management. The [SP 800-61r3 publication](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf) includes containment, eradication, recovery, communications, and improvement considerations.

Implications for Turing:

- incident handling must be a maintained capability with preparation, detection, analysis, containment, eradication, recovery, and lessons-learned records;
- a patch is one possible response action, not the definition of response success;
- each incident class needs pre-defined containment and evidence-preservation choices because disabling a browser capability can affect user safety, availability, and forensic visibility;
- the rehearsal must record both the decision and the authority that made it, not only elapsed time.

NIST guidance does not select Turing's staffing, disclosure date, supported-version window, or emergency update mechanism.

### CVSS communicates severity, not the whole release decision

The [FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document) separates Base, Threat, Environmental, and Supplemental metrics. FIRST's [consumer implementation guide](https://www.first.org/cvss/v4.0/implementation-guide) explains that Base scores provide a common baseline and that Threat and Environmental metrics add deployment-specific context.

Implications for Turing:

- triage records must preserve the vector, score, scorer, version, and timestamp;
- exploitability, active exploitation, reachable browser principals, affected process boundaries, default configuration, user interaction, and installed feature set must be assessed separately from the base score;
- patch priority, temporary mitigation, channel exposure, disclosure timing, and minimum secure version require an explicit risk decision beyond a numeric CVSS label;
- disagreement or missing information must remain visible instead of being silently converted to a severity tier.

CVSS is a measurement input. It is not authorization for disclosure, patch release, signing, stable promotion, or incident closure.

### Coordinated disclosure is a coordination process

CISA's [information-sharing and coordinated vulnerability disclosure page](https://www.cisa.gov/topic/cybersecurity-information-sharing) describes coordinated vulnerability disclosure as coordination of remediation and public disclosure between a reporter and affected vendor(s).

Implications for Turing:

- private intake must protect report access and preserve only the minimum necessary exploit detail;
- the response record must identify affected versions, dependencies, platforms, and downstream parties before public communication;
- disclosure timing, reporter communication, credit, advisory content, and exceptions for active exploitation require human authority and a documented rationale;
- public documentation must not expose exploit-enabling details before the approved coordination point.

CISA's coordination model does not grant Turing authority, define legal obligations in every jurisdiction, or replace counsel and owner review.

## Required authority separation

The future process must keep these decisions separate:

1. **intake**: who may receive and access the report;
2. **triage**: who may reproduce, classify impact, and identify affected assets;
3. **containment**: who may disable or restrict a feature and under what signed, bounded policy;
4. **patch**: who may approve code, regression tests, backports, and release candidates;
5. **signing**: who may authorize package and update metadata signatures;
6. **promotion**: who may move an artifact through a channel or set a minimum secure version;
7. **disclosure**: who may coordinate with reporters, affected parties, and the public;
8. **closure**: who may accept residual risk, postmortem actions, and evidence retention.

An agent may collect bounded diagnostics or execute an approved rehearsal step, but must not decide severity, disclosure timing, signing, stable promotion, or incident closure.

## Evidence contract for the future rehearsal

The exercise must retain, with private access control and redaction review:

- an intake timestamp, reporter identity handling, access list, acknowledgement, and chain of custody;
- reproduction inputs, affected build/source identity, platform matrix, reachable trust boundaries, and failure denominator;
- severity vector and environmental risk analysis, known exploitation state, user-impact assessment, and uncertainty log;
- containment options considered, selected action, authority, expiry, rollback, and user-visible effect;
- patch branch identity, review records, regression test, backport decision, dependency impact, and build/provenance identity;
- fake-key or otherwise non-production signing/update dry-run records, staged rollout, minimum secure version, revocation, and recovery outcomes;
- communication and disclosure decisions, reporter coordination, advisory draft, credit, legal review, and sanitized public artifact;
- postmortem, systemic remediation, owner assignment, due dates, and verification of completed follow-up.

Template fields, timestamps, and logs must not contain credentials, private-session contents, profile data, unreduced exploit payloads, production signing material, or unnecessary personal information.

## Incident-class decision matrix

| Incident class | First decision questions | Evidence that must not be skipped |
| --- | --- | --- |
| active exploitation | What is reachable now, and what can be contained without destroying evidence? | exploitation confidence, affected versions, containment authority, communication and patch path |
| update or signing compromise | Which trust roots, metadata, artifacts, or builders are affected? | key/role scope, revocation, clean rebuild, minimum secure version, recovery path |
| dependency vulnerability | Which direct and transitive components and supported platforms are exposed? | dependency identity, advisory source, fixed version, compatibility, rebuild and backport evidence |
| data loss or corruption | Which user state may be damaged, and can recovery be proven without overwriting it? | preservation, backup/journal path, migration/repair result, user communication |
| privacy leak | What data crossed the boundary and who received it? | data inventory, access review, containment, notification and retention decisions |
| sandbox regression | Which principal gained authority and which hostile inputs can reach it? | policy diff, exploitability, platform scope, containment, negative test and patch evidence |
| malicious extension/provider | Which capability grant or provider boundary was abused? | affected grants, revocation, user/admin controls, evidence preservation and cleanup |
| service outage | What fails closed, what remains locally usable, and how is recovery verified? | dependency scope, degraded mode, retry bounds, communication, restoration and postmortem |

The matrix is a rehearsal contract, not evidence that any incident class is currently handled.

## Timing and support decisions

Turing must choose and publish response targets only after it has named supported platforms, owners, backups, build capacity, signing separation, communication channels, and rollback or recovery limits. A target without demonstrated capacity is not an SLA. A fast patch that cannot be verified, migrated, signed, or recovered is not a successful response.

The readiness review must therefore compare target times with observed tabletop times, identify unavailable roles, record waivers and expiry, and state which channels and versions are unsupported. Stable support cannot be inferred from a working development build or a green repository check.

## Next proof

`PB-018` needs a private fake-vulnerability tabletop and emergency patch dry run beyond the checked templates. The exercise should use synthetic artifacts and non-production keys, cover every incident class above, test protected patch and embargoed-CI handling, exercise regression/backport/signing/update/revocation paths, and end with an owner-reviewed readiness record. It must not publish exploitable details or promote production authority.

## Claim boundary

This report does not approve an incident-response program, staffing model, severity SLA, disclosure process, signing hierarchy, patch channel, stable support policy, production security, emergency patch capacity, incident closure authority, or production-safe browsing. It does not contain a vulnerability or authorize a real incident exercise.

## References

- [NIST incident response project](https://csrc.nist.gov/Projects/incident-response)
- [NIST SP 800-61 Revision 3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)
- [FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document)
- [FIRST CVSS consumer implementation guide](https://www.first.org/cvss/v4.0/implementation-guide)
- [CISA information sharing and coordinated vulnerability disclosure](https://www.cisa.gov/topic/cybersecurity-information-sharing)
