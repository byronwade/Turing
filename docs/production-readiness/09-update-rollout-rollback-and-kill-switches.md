# Update Rollout, Rollback, and Kill Switches

Status: architecture requirement; implementation not selected  
Owner: release, security, operations, and platform

The update design evaluates TUF or an equivalently rigorous model with separate root, targets, snapshot, and timestamp roles; threshold signatures; offline root protection; expiry; consistent snapshots; rollback and freeze resistance; delegation; rotation; and compromise recovery.

Rollout is staged by channel and cohort with health gates, pause, rollback, minimum secure version, emergency revocation, and signed configuration boundaries.

A kill switch cannot become ambient remote code or a hidden compatibility override. It is narrowly scoped, signed, auditable, expiring, and incapable of weakening fundamental certificate, sandbox, origin, or update verification.
