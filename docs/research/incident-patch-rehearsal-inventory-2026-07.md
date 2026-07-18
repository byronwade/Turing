# Incident Patch Rehearsal Inventory - July 2026

Status: no-claim planning inventory and checked no-claim incident patch rehearsal template
Owner: security, incident-response, release operations, support, legal-community, and documentation-research
Related gate: `PB-018` Security incident and patch rehearsal
Updated: 2026-07-18

## Question

Can `PB-018` move from security and release prose into checked planning evidence and a checked no-claim incident patch rehearsal template without implying that incident-response readiness, emergency patch capacity, supported security versions, disclosure authority, stable promotion authority, signing authority, incident closure authority, or production-safe browsing exists?

## Short Answer

Yes, for planning only. The new [`incident-patch-rehearsal.json`](../security-engine/machine/incident-patch-rehearsal.json) registry, [`incident-patch-rehearsal-record.schema.json`](../security-engine/machine/incident-patch-rehearsal-record.schema.json), checked no-claim [`incident patch rehearsal template`](../security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json), and [`validate_incident_patch_rehearsal.py`](../../tools/validate_incident_patch_rehearsal.py) validator make the incident-response and emergency patch rehearsal terms concrete enough to continue security, support, legal, and release work. They define required private-intake steps, emergency-patch steps, incident classes, role boundaries, timing/escalation/secret-rotation expectations, fixture policy, rejection rules, unsupported authority boundaries, and future fake-vulnerability tabletop handoff fields.

This is not an incident-response program, executed rehearsal record, patch-capacity proof, supported-security statement, release authority grant, disclosure authorization, signing authorization, or production-safety claim.

## Inputs

- [Security policy](../security.md)
- [Security Verification and Release Gates](../security-engine/06-security-verification-and-release-gates.md)
- [Vulnerability Response and Supported Lifecycle](../release-operations/08-vulnerability-response-and-supported-lifecycle.md)
- [Update, Supply Chain, and Vulnerability Response](../security-engine/05-update-supply-chain-and-vulnerability-response.md)
- [Blueprint 08](../blueprint-v1/08-security-and-sandbox.md)
- [Blueprint 13](../blueprint-v1/13-build-release-operations.md)
- [`incident-patch-rehearsal.schema.json`](../security-engine/machine/incident-patch-rehearsal.schema.json)
- [`incident-patch-rehearsal.json`](../security-engine/machine/incident-patch-rehearsal.json)
- [`incident-patch-rehearsal-record.schema.json`](../security-engine/machine/incident-patch-rehearsal-record.schema.json)
- [`no-claim-incident-patch-rehearsal-template.json`](../security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json)
- [`validate_incident_patch_rehearsal.py`](../../tools/validate_incident_patch_rehearsal.py)

## Inventory Scope

The checked inventory covers private intake:

- report access control, acknowledgement, reproduction, severity, asset analysis, affected-version statement, embargo handling, and sanitized evidence preservation.

It covers emergency patch rehearsal:

- protected patch branch, embargoed CI, regression test, backport decision, signing and update dry run, staged rollout, minimum secure version, revocation, release notes, user and admin communication, CVE and credit handling, coordinated disclosure, and postmortem remediation.

It covers incident classes:

- active exploitation, update or signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension or provider, and service outage.

It covers role boundaries:

- owner, reviewer, release, security, legal, support, and on-call responsibilities, plus timing targets, escalation path, secret rotation, backup coverage, and unavailable agent, disclosure, stable promotion, signing, and incident closure authority.

The checked no-claim incident patch rehearsal template adds the handoff shape for a future fake-vulnerability private tabletop and emergency patch dry run. It records required source records, lifecycle stages, fixture-policy controls, rejection rules, unsupported boundaries, and validation commands, but every rehearsal status flag remains false until an actual private exercise replaces the template-only fields with reviewed evidence.

## Decision

`PB-018` can move from `not_started` to `partial` because the inventory, checked no-claim incident patch rehearsal template, and validator now exist. The status must not move beyond `partial` until a private-intake tabletop beyond the checked no-claim incident patch rehearsal template, emergency patch dry run, regression and backport evidence, signing/update dry-run evidence, staged rollout and revocation evidence, coordinated disclosure rehearsal, postmortem evidence, incident-class workflow exercise, role-matrix review, timing/escalation/secret-rotation drill, backup-owner coverage, and owner approval exist.

## Unsupported Boundaries

The inventory explicitly keeps these outside the proof:

- no production-safe browsing claim;
- no supported security versions claim;
- no incident-response readiness claim;
- no emergency patch capacity claim;
- no disclosure authority claim;
- no stable promotion authority claim;
- no signing authority claim;
- no incident closure authority claim;
- no implementation claim.

## Next Proof Required

To advance beyond partial planning evidence and beyond the checked no-claim incident patch rehearsal template, `PB-018` needs:

1. private-intake tabletop records beyond the checked no-claim incident patch rehearsal template with access-control, acknowledgement, reproduction, severity, asset-analysis, affected-version, embargo, and sanitized-evidence outputs;
2. emergency patch rehearsal records beyond the checked no-claim incident patch rehearsal template for protected patch branch, embargoed CI, regression, backport, signing/update dry run, staged rollout, minimum secure version, revocation, release notes, user/admin communication, CVE/credit handling, coordinated disclosure, and postmortem remediation;
3. incident-class tabletop coverage for active exploitation, update/signing compromise, dependency vulnerability, data loss, privacy leak, sandbox regression, malicious extension/provider, and service outage;
4. role-matrix review naming owner, reviewer, release, security, legal, support, and on-call responsibilities;
5. timing-target, escalation-path, backup-owner, and secret-rotation evidence;
6. confirmation that agents cannot decide severity, disclosure timing, incident closure, stable promotion, or signing;
7. security, legal-community, support, release-operations, and owner review.

## Affected Records

- [`incident-patch-rehearsal-record.schema.json`](../security-engine/machine/incident-patch-rehearsal-record.schema.json)
- [`no-claim-incident-patch-rehearsal-template.json`](../security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json)
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json)
- [`build-readiness-task-queue.json`](../blueprint-v1/machine/build-readiness-task-queue.json)
- [`research-readiness-crosswalk.json`](../blueprint-v1/machine/research-readiness-crosswalk.json)
- [`security.md`](../security.md)
- [`Security Verification and Release Gates`](../security-engine/06-security-verification-and-release-gates.md)
- [`Vulnerability Response and Supported Lifecycle`](../release-operations/08-vulnerability-response-and-supported-lifecycle.md)

## Validation

Run:

```bash
python3 -B tools/validate_incident_patch_rehearsal.py
python3 -B tools/validate_blueprint.py
```

The aggregate Windows wrapper also runs the blueprint validator:

```powershell
.\tools\check.ps1
```
