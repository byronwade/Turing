# Model, Prompt, Environment, and Run Provenance

Status: operating baseline  
Owner: agent operations, build, security, and audit

Every material agent run records:

- task ID and immutable task manifest digest;
- model/provider and agent/tool versions;
- system and repository instruction digests;
- source commit and branch;
- environment image and toolchain digests;
- filesystem and network grants;
- credentials issued by identifier, never secret value;
- commands and tool calls;
- generated diff and artifact digests;
- tests and evidence produced;
- failures, retries, overrides, and escalations;
- human and independent-agent review decisions;
- final disposition.

Prompt text containing embargoed or sensitive material follows the same retention and access policy as the underlying finding. Provider retention and training behavior must be known before sending restricted content.

The agent run manifest is part of source provenance, not an informal chat log.
