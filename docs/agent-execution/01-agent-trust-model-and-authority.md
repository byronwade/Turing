# Agent Trust Model and Authority

Status: operating baseline  
Owner: security, program, architecture, and agent operations

## Threat model

A coding agent is a privileged software-supply-chain principal. Its prompt, repository context, terminal output, issues, pull requests, test fixtures, generated files, dependency documentation, and web content may contain malicious or misleading instructions.

## Authority classes

- **Research agent:** reads public material and drafts non-normative studies.
- **Implementation agent:** changes only paths and interfaces listed in an approved task.
- **Verification agent:** runs independent tests and reviews evidence but does not modify the implementation under review.
- **Security agent:** inspects threat boundaries and findings under separate access control.
- **Release-support agent:** prepares manifests and evidence but cannot sign or promote a release.
- **Human release authority:** owns final security, legal, support, signing, and promotion decisions.

## Deny-by-default rules

Agents receive only task-scoped repository paths, tools, network destinations, credentials, time, cost, and concurrency. Authority expires at task completion. A model response, webpage, issue, dependency README, or test fixture cannot expand authority.

## Separation of duties

The same agent run cannot be the sole author, verifier, security reviewer, and merger for a production-sensitive change. Multiple agents under identical prompts and permissions are not automatically independent.

## Stable controls

`AEX-001` through `AEX-020` in the capability matrix define the minimum authority and review constraints. Any exception is explicit, dated, approved, and expires.
