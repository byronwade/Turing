# Data-loss, Migration, and Recovery Gates

Status: release-gate framework  
Owner: storage, product, release, quality, and support

Profile, Space, session, snapshot, history, bookmark, credential-reference, Plug-in, policy, and settings formats are versioned. Every migration is transactional, crash-tested, disk-full-tested, reversible where feasible, and covered by backup/recovery guidance.

Stable release requires defined behavior for interrupted updates, downgrade, corrupt records, clock changes, device loss, partial sync, conflict resolution, and previous-version recovery.

A known data-loss path is a release blocker. Consequential browser or agent actions are never replayed merely to reconstruct UI state.
