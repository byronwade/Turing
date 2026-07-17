# Security Embargo, Release, and Incident Boundaries

Status: operating baseline  
Owner: security, incident response, release, legal, and human release authority

Agents may assist with reproduction, root-cause analysis, regression tests, patch preparation, and evidence under restricted access. They may not:

- decide disclosure timing;
- publish an embargoed finding;
- contact affected parties without authorization;
- assign final severity alone;
- close the incident;
- sign or promote a release;
- rotate offline root keys;
- declare users safe.

Embargoed work uses dedicated restricted branches, minimal participants, audited access, separate provider policy, and no public CI logs. The incident commander and human release authority own escalation, communication, and final disposition.
