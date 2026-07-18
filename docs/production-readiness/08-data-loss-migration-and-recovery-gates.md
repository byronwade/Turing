# Data-loss, Migration, and Recovery Gates

Status: release-gate framework  
Owner: storage, product, release, quality, and support

Profile, Space, session, snapshot, history, bookmark, credential-reference, Plug-in, policy, and settings formats are versioned. Every migration is transactional, crash-tested, disk-full-tested, reversible where feasible, and covered by backup/recovery guidance.

The checked [Profile Session Format Inventory](../research/profile-session-format-inventory-2026-07.md) and checked no-claim [schema-package template](../storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json) are planning evidence only. They do not satisfy this gate until executable schemas beyond the template, corrupt/downgrade/fault tests, migration rehearsal, data-loss review, real-profile fixture policy, and owner approval exist.

Stable release requires defined behavior for interrupted updates, downgrade, corrupt records, clock changes, device loss, partial sync, conflict resolution, and previous-version recovery.

A known data-loss path is a release blocker. Consequential browser or agent actions are never replayed merely to reconstruct UI state.
