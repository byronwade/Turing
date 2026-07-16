# Security Policy

## Current status

Turing is an early research and architecture program. It is not currently a production-safe browser and must not be used for sensitive accounts, private data, financial activity, or arbitrary hostile browsing.

The project will not claim supported security versions until sandbox, site-isolation, update, release, vulnerability-response, fuzzing, and independent-review gates are operational.

## Reporting a vulnerability

Do not open a public issue for a suspected exploitable vulnerability, sandbox escape, cross-origin or cross-profile data leak, credential exposure, update or signing weakness, unsafe agent action, or private-data disclosure.

Use GitHub’s private security advisory/reporting flow for this repository when enabled. Until a dedicated encrypted address is published, contact the repository owner privately through a verified channel and include only the minimum reproduction detail needed to establish impact.

A useful report includes:

- affected commit, branch, build, platform, and configuration;
- prerequisite and attacker-controlled inputs;
- impact and assets reached;
- minimal reproduction or reduced test;
- whether the result crosses a process, sandbox, origin, site, profile, credential, update, DevTools, extension, or agent-policy boundary;
- crash stack or trace with secrets removed;
- suggested mitigation if known.

Do not test against other people, real accounts, production services without authorization, or data you do not own. Do not persist, exfiltrate, destroy, or publish secrets.

## Response targets

Formal response targets will be established before developer preview. During the research phase, maintainers will make a best effort to acknowledge reports, restrict access, reproduce, classify root cause, create regression tests, and coordinate disclosure.

No patch-time guarantee is implied yet. That absence is one reason the project is not production-safe.

## Scope priorities

Highest priority includes:

- renderer, decoder, GPU, extension, DevTools, agent, or utility process escape;
- cross-origin, cross-site, cross-profile, or private-session data access;
- arbitrary file, socket, device, process, credential, or browser-internal access;
- memory corruption in privileged or unsandboxed code;
- update, signing, build, dependency, CI, or release compromise;
- certificate, permission, origin, credential, download, or trusted-UI spoofing or bypass;
- DevTools, automation, extension, or agent authority bypass;
- secret leakage through logs, crashes, traces, telemetry, model observations, or provider payloads;
- high-risk agent action without a valid grant, current document epoch, and required confirmation;
- a documentation or release claim that materially conceals a known security limitation.

## AI and agent security

Page content, extension content, tool output, and model output are untrusted instructions. They never expand authority or approve consequential actions.

Agent observations and actions must remain scoped by principal, profile, origin, frame, current document epoch, action class, grant lifetime, quota, provider policy, and confirmation requirements. Secrets must be redacted before model or provider exposure unless a narrowly defined, user-approved protocol explicitly permits otherwise.

Prompt injection is treated as a confused-deputy and authority problem, not merely a model-quality problem.

## Disclosure

The intended policy is coordinated disclosure with credit where desired, a clear affected-version statement, patch and update guidance, regression coverage, and a root-cause-oriented postmortem when it benefits users without enabling active exploitation.

This policy will be expanded before public binary distribution.
