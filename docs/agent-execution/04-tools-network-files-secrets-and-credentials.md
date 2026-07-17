# Tools, Network, Files, Secrets, and Credentials

Status: operating baseline  
Owner: security, build, infrastructure, and agent operations

## Default environment

Agent execution uses an ephemeral workspace, read-only task manifest, scoped filesystem access, bounded CPU/memory/disk/time, command logging, and deny-by-default outbound network.

## Network

Allow only exact dependency, standards, test-suite, or repository destinations required by the task. Record every fetched object by URL, digest, retrieval time, and license/provenance context. No arbitrary exfiltration endpoint is permitted.

## Files

Protect against symlink traversal, path confusion, generated-file replacement, repository escape, hidden files, binary payloads, and build-script side effects. Agents modify only declared paths.

## Secrets

Agents never receive offline update roots, production signing keys, unrestricted cloud credentials, user data, or production browser profiles. Short-lived credentials are task-scoped, auditable, non-exportable where possible, and revoked after use.

## Build scripts and dependencies

New build scripts, procedural macros, native tool invocations, package hooks, or networked generators require dependency and supply-chain review before execution in privileged CI.
