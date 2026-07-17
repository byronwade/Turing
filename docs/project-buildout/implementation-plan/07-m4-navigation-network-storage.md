# 07 — M4: Navigation, Network, Storage, and Multipage Applications

Status: implementation game plan  
Owner: kernel, navigation, networking, storage, security, privacy, quality, and developer tooling

## 1. Objective

M4 connects the renderer, browser kernel, network service, and storage service into controlled multipage applications. It introduces real requests, redirects, commits, history, frames, cookies, cache, persistent origin storage, workers, downloads, permissions foundations, and crash-aware migrations without granting renderers ambient sockets or filesystem access.

## 2. Entry gates

- WP-002 provides accepted identity, route, channel, cancellation, and broker contracts appropriate for real transports.
- WP-003 demonstrates effective renderer restrictions on the selected reference platform.
- WP-007 provides document/frame lifetime and mutation epochs.
- M3 host hooks are versioned for script/module/network integration.
- Profile, Space, origin, site, network-partition, storage-partition, and private-session identities are specified.
- TLS, certificate, database, compression, and URL foundation candidates receive dependency and license review.
- Hermetic DNS, TLS, HTTP, proxy, clock, and fault-injection test infrastructure exists.

## 3. WP-012 — navigation transactions and renderer assignment

Task sequence:

1. URL parsing/serialization and origin/site algorithms;
2. browsing-context, frame, browsing-context-group, site-instance, history-entry, navigation, and document-epoch types;
3. navigation intent from UI or renderer;
4. kernel validation of initiator, user activation, sandbox flags, target, profile, and policy;
5. site-instance and renderer assignment oracle;
6. provisional document and response classification;
7. redirect revalidation;
8. atomic commit and old-document teardown;
9. same-document navigation;
10. history traversal and initial BFCache eligibility;
11. frame creation, detach, and process swap;
12. download and external-protocol disposition;
13. crash, cancellation, timeout, and stale-commit handling;
14. semantic navigation traces and differential tests.

A renderer cannot choose its effective origin, site instance, profile, or committed URL.

## 4. WP-013 — scoped HTTP, TLS, cache, cookies, and hermetic server

### Request context

Every request includes kernel-issued:

- profile/private-session identity;
- top-level site and requesting origin;
- network partition key;
- destination, mode, credentials, redirect, referrer, integrity, priority, and user-activation metadata;
- frame/document/process identity;
- service-worker or preload initiator where applicable;
- cancellation, deadline, budget, and trace identity.

### Implementation order

1. DNS and proxy interface using hermetic test services;
2. socket ownership exclusively in the network service;
3. TLS 1.3 and certificate verification adapter using reviewed libraries/platform roots;
4. HTTP/1.1 parser, framing, limits, decompression isolation, and connection reuse;
5. redirects and authentication challenge skeleton;
6. Fetch request/response filtering;
7. CORS, mixed content, CSP/CORP/COOP/COEP subset tied to implemented standards;
8. cookie parsing, SameSite, Secure, HttpOnly, partitioning, prefixes, limits, and attachment policy;
9. cache key, freshness, validation, eviction, partitioning, and corruption behavior;
10. downloads through brokered destinations;
11. offline/fault/slowloris/truncation/certificate/clock/proxy test matrix;
12. network DevTools and privacy-safe diagnostics.

HTTP/2 and HTTP/3 are later capabilities, not shortcuts around a correct request-policy core.

## 5. WP-014 — storage broker, quota, migrations, and service workers

### Storage identity

Every store is keyed by profile/private session, origin, top-level partition where required, bucket, and storage type. Renderers receive logical handles, never database paths.

### Implementation order

- local and session storage reference semantics;
- transactional metadata and profile schema versioning;
- quota accounting and reservation;
- IndexedDB subset with versionchange and transaction durability;
- Cache Storage;
- origin-private file interface through brokered handles;
- service-worker registration, lifecycle, script update, event dispatch, and storage foundation;
- clear-site-data and user-visible clearing;
- eviction and storage pressure;
- interrupted migration, corruption quarantine, repair, and export;
- private-session ephemeral keys and cleanup without claiming physical erasure;
- storage DevTools and evidence bundles.

## 6. Credentials, permissions, files, and clipboard

M4 establishes broker contracts, not final UX breadth:

- credentials remain in OS-protected services or encrypted stores and are not exported to renderers or agents;
- permission decisions are kernel-owned, profile/origin scoped, revocable, and visible;
- file access uses user-selected, scoped handles with lifetime and revocation;
- clipboard access follows user activation, platform, permission, and trusted-UI rules;
- downloads are quarantined/marked where the platform supports it;
- renderer requests carry current document epoch and fail after navigation.

## 7. Workers and structured clone

Add only after main-realm and service contracts are stable:

- dedicated workers with explicit process/realm ownership;
- shared workers when cross-document identity and lifetime are defined;
- structured clone types and transfer ownership;
- message-port bounds, close, cancellation, and backpressure;
- worker network/storage contexts derived from kernel authority;
- crash and parent-destruction behavior;
- no ambient persistence or socket access.

## 8. Failure and recovery matrix

Test:

- DNS, proxy, TLS, HTTP, decompression, network-process, and cache failures;
- navigation cancellation at every phase;
- redirect loops and origin/site changes;
- stale commit after renderer restart;
- storage-process crash during each transaction phase;
- disk full before, during, and after commit;
- power loss/interrupted migration;
- database corruption per origin and global metadata;
- quota races and eviction during active use;
- service-worker crash/update conflict;
- download interruption and unsafe retry;
- profile deletion, private-session exit, and clock change.

## 9. Verification

- URL, Fetch, CORS, cookies, cache, navigation, storage, workers, and service-worker WPT subsets with disclosed denominators;
- hermetic protocol tests and captured raw traces;
- parser and structured-clone fuzzing;
- cross-origin, cross-site, cross-profile, private-session, and partition negative tests;
- compromised-renderer attempts to open sockets/files or forge context;
- migration/property/chaos tests;
- fixed-hardware connection, request, cache, storage, commit, and recovery measurements;
- network/storage DevTools correctness and redaction review;
- accessibility and user-understanding tests for permissions, downloads, errors, and recovery.

## 10. Exit criteria

- implemented APIs satisfy their chosen standards thresholds;
- cross-origin and cross-profile isolation tests pass;
- renderer cannot obtain ambient socket, path, credential, or storage-file authority;
- storage migrations and crash recovery preserve declared data guarantees;
- supported controlled-application corpus works with documented gaps;
- M5 receives stable navigation, request, storage, permission, and diagnostic contracts;
- general daily browsing and sensitive use remain unsupported.
