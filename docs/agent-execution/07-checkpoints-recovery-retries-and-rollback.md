# Checkpoints, Recovery, Retries, and Rollback

Status: operating baseline  
Owner: quality, repository operations, and subsystem owners

Long tasks use explicit checkpoints after specification resolution, interface acceptance, implementation, test completion, and evidence collection.

Retries must be bounded and preserve the original failure. An agent cannot loop until a flaky test happens to pass and then discard the failed runs.

Rollback requirements include:

- reversible repository changes;
- migration downgrade or recovery path;
- feature flag or channel containment where applicable;
- compatibility and profile-format impact;
- artifact and update rollback;
- documentation and registry reversal;
- evidence that rollback itself is safe.

If an agent loses context, tool state, credentials, or environment integrity, it stops and hands off rather than reconstructing authority from memory.
