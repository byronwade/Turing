# Service and Offline Architecture Research - July 2026

Status: deferred `RQ-65` research packet; no service, self-hosting, availability, privacy, or production claim
Owner: architecture, product, platform, security, privacy, storage, networking, release operations, support, and legal-community
Question: Which optional services materially improve safety or continuity, and how should the browser degrade, export, self-host, or shut down without lock-in?

This packet consolidates the [Service Dependencies and Offline Behavior](../production-readiness/10-service-dependencies-and-offline-behavior.md) contract with profile/session, networking, update, privacy, agent, support, and incident routes. It does not select a service provider, require a cloud dependency, establish availability, or authorize production deployment.

## Service classification

Every proposed service must be classified before it can enter a product or release path:

| Class | Examples | Required browser behavior when unavailable |
|---|---|---|
| `local-essential` | navigation, local profile access, security policy, core rendering, user export | Continue locally or enter an explicit safe failure; never silently lose accepted user state |
| `local-optional` | caches, local diagnostics, indexing, optional local models | Disable or rebuild within bounded resource and privacy policy |
| `remote-optional` | sync, account, remote agent provider, update metadata, crash upload, optional intelligence | Browsing and local profile use continue where the support contract says they do; show explicit unavailable state and preserve retry/export paths |
| `remote-required-for-declared-feature` | a feature whose contract explicitly requires a service | Scope the feature as unavailable, preserve user data, explain the limitation, and prevent hidden fallback authority |
| `external-authority` | OS credential vault, OS update/signing service, platform accessibility, network/DNS/identity dependency | Preserve the platform boundary, record unavailable or degraded behavior, and never treat a missing response as approval |

The same service can have different classes for different workflows. A service inventory must therefore record the caller, data class, principal, origin/profile scope, network requirement, authority granted, and failure behavior rather than labeling the service globally as “optional.”

## Required service record

Each service row must identify:

- purpose, user-visible benefit, workflow dependency, owner, provider, version/API, region and platform scope, and replacement or shutdown path;
- data classes sent, received, derived, retained, exported, deleted, encrypted, or disclosed, including credentials, profile state, page content, URLs, telemetry, model prompts, and crash artifacts;
- authentication, authorization, capability grant, origin/profile/site scope, rate limits, abuse controls, quota, cost, and privacy/retention controls;
- availability assumptions, timeout/cancellation, retry/backoff, offline behavior, degraded mode, stale-data policy, recovery, export, self-hosting, migration, and user-visible error state;
- incident, vulnerability, update, legal/community, support, and end-of-life responsibilities, including data return and verifiable deletion;
- deterministic negative tests for outage, partition, timeout, malformed response, stale response, replay, quota, credential-vault lock, provider compromise, provider shutdown, and partial local state.

No service response, model output, remote page content, provider status, or stale cache may expand browser authority. Page and provider input remain untrusted, and service unavailability is not permission to bypass a local security or privacy boundary.

## Offline and continuity contract

The owner decision must define, per workflow:

1. what remains functional without network access;
2. what local state is authoritative and what state is cache or derived data;
3. how stale, conflicting, partial, or unavailable remote state is represented;
4. how users export data in an open, documented, redacted, and integrity-preserving format;
5. whether a self-hosted or alternate endpoint is supported, experimental, or explicitly out of scope;
6. how credentials, private sessions, agent grants, update metadata, and security indicators behave offline;
7. how shutdown, provider migration, account deletion, service retirement, and data deletion are performed without lock-in;
8. which offline limitations change the public support contract, SLO denominator, incident response, or release gate.

An outage must not silently disable local browsing, profile access, security indicators, protected work, required accessibility, or user export. Conversely, local fallback must not silently use stale credentials, stale security policy, unauthorized agent grants, or unverified update metadata.

## Evidence sequence

1. Inventory services, dependencies, principals, data classes, and authority boundaries.
2. Define local-essential behavior and explicit degraded modes for supported workflows.
3. Build synthetic fixtures for outage, partition, timeout, stale/replay, malformed response, provider compromise, quota, migration, export, deletion, and shutdown paths.
4. Exercise privacy, credential, profile/session, agent, update, accessibility, and support effects with redacted artifacts and no production secrets or user data.
5. Measure user-visible recovery, data-integrity, resource, latency, and retry behavior against the SLO and incident contracts.
6. Review service replacement, self-hosting, export, legal, support, cost, and end-of-life decisions with named owners and independent review.
7. Synchronize the service registry, product requirements, risks, support boundary, privacy records, update/incident records, and `PB-020` closure evidence.

The next acceptable artifact is an owner-reviewed service and offline decision packet with workflow matrices, failure evidence, data-handling review, export/shutdown plan, and exact support wording. A service inventory, successful local fallback, provider documentation, or passing repository check is preparation only.

## Current disposition

`RQ-65` remains deferred. This packet clarifies the service/offline evidence route without selecting a provider, making a self-hosting promise, changing active/deferred counts, authorizing broad implementation, or changing the `90%` contained-M0 / `0%` full-build measures.

## Source records

- [Service Dependencies and Offline Behavior](../production-readiness/10-service-dependencies-and-offline-behavior.md)
- [Profile/Session Execution and Data-Safety Closure Preparation](profile-session-execution-and-data-safety-closure-preparation-2026-07.md)
- [Human Release, Legal, and Incident Capacity Research](human-release-legal-and-incident-capacity-research-2026-07.md)
- [Product SLOs and Error Budgets Research](product-slos-and-error-budgets-research-2026-07.md)
