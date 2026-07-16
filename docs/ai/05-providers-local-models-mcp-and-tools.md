# Providers, Local Models, MCP, and Tools

Status: research and design baseline  
Owner: model and tool integration  
Purpose: Integrate external intelligence and tools while preserving browser authority, privacy, and resource control.

## Relationship to the Turing program

This document expands the provider and tool portions of [Blueprint 10](../blueprint-v1/10-ai-agent-platform.md). API transport rules are in the [API design book](../api-design/README.md).

## Provider manifest

Every provider/model declares local or remote execution, endpoint/region, model/version, authentication, data fields sent, retention/training configuration, tool format, context/output limits, streaming/cancellation, cost, fallback, safety controls, availability, and audit behavior. A provider is selected by explicit user/profile/enterprise policy.

No silent local-to-remote or provider-to-provider fallback occurs.

## Remote providers

The browser redacts and serializes only the approved observation manifest. Transport uses authenticated secure channels, timeouts, cancellation, rate/cost limits, and no browser credentials beyond provider authentication. Responses are bounded and parsed as untrusted structured data.

Remote activity has persistent visible status and per-session cost/data accounting.

## Local models

Weights are signed or hash-verified, versioned, stored outside profile secrets, and loaded into a restricted process. The model process cannot map browser memory, open arbitrary files/network, access credentials/devices, or invoke tools except through the gateway. RAM, VRAM, accelerator, CPU, energy, and unload latency are measured.

Size classes and hardware compatibility are explicit. A dormant feature does not retain gigabytes or keep the accelerator awake.

## MCP integration

MCP can be used as an external tool/resource transport, not as browser authority. Each MCP server is an untrusted principal with identity, origin/install source, allowed transport, selected tools/resources, schemas, data destinations, rate limits, and revocation. Tool descriptions and results are untrusted content.

The browser gateway translates approved tool calls through existing grants. An MCP server cannot request cookies, credentials, arbitrary tabs/files, confirmations, or kernel methods merely because its schema names them.

## Tool design

Tools are task-specific, typed, bounded, cancellable, idempotence-aware, and return structured effects. Tools identify data they receive and external side effects. Files use selected handles; repositories use explicit workspace grants; code execution uses isolated developer tooling; payments/security/device operations follow high-risk policy.

Generic shell, arbitrary HTTP with browser credentials, unrestricted filesystem, raw browser IPC, and hidden UI automation are prohibited defaults.

## Tool and provider lifecycle

Connections authenticate, negotiate capability, expire, revoke, and close on session/profile policy. Tool updates require provenance and permission review. Server or provider failure cannot leave a grant active indefinitely or duplicate effects. Results are source-labeled and audited.

Enterprise policy can disable external tools, require allowlists, local-only models, specific regions, no retention, or separate profiles.

## Supply chain and ecosystem

Model files, native runtimes, GPU libraries, provider SDKs, MCP servers, and tool packages expand supply-chain and native attack surface. Turing should prefer protocol boundaries over linking provider SDKs into privileged processes. Dependencies have owners, versions, licenses, advisories, integrity, and replacement plans.

## Non-negotiable invariants

- Provider selection and data flow are explicit; no silent fallback occurs.
- Local model processes have no ambient browser, file, network, credential, or device authority.
- MCP servers and tool output are untrusted principals/data.
- Tool capabilities remain subordinate to browser grants and action policy.
- Generic shell, filesystem, credentialed network, and kernel interfaces are not default tools.
- Provider/tool/model resource and supply-chain costs are separately visible.

## Required evidence

- Provider payload manifests, redaction, cancellation, timeout, cost, and fallback tests.
- Local model sandbox negative tests and RAM/VRAM/energy/unload measurements.
- MCP malformed schema, malicious description/result, over-broad request, transport, and revocation tests.
- Tool side-effect, idempotency, selected-file, repository, code-execution, and audit tests.
- Dependency/provenance/license/advisory review for runtimes, weights, and packages.
- User studies for provider/data-destination comprehension.

## Known risks and unresolved questions

- Third-party provider policies and models can change independently.
- MCP/tool ecosystems may normalize excessive permissions.
- Local inference can destroy the browser's memory and energy advantage.
- Native model runtimes and GPU libraries add memory-unsafe attack surface.

## Primary sources

- Model Context Protocol specification — https://modelcontextprotocol.io/specification/2025-11-25
- Model Context Protocol architecture — https://modelcontextprotocol.io/docs/learn/architecture
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
