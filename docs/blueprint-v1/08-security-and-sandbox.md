# 08 — Security, Privacy, and Sandbox Model

## 1. Security posture

Turing processes untrusted, adversarial input at every layer: HTML, CSS, JavaScript, WebAssembly, images, fonts, media, PDFs, compressed data, certificates, protocols, storage files, extensions, DevTools commands, update metadata, and model output. A visually functional browser without containment, rapid updates, and vulnerability response is unsafe for normal use.

The security objective is not “no bugs.” It is to reduce bug classes, constrain exploit chains, limit accessible data, detect failures, and ship fixes before known vulnerabilities remain broadly exploitable.

## 2. Threat actors

- malicious website or ad content;
- compromised third-party script, package, extension, model provider, update mirror, or build worker;
- hostile local file, download, font, image, media, PDF, archive, or profile database;
- network attacker where TLS or proxy policy allows influence;
- renderer or utility process after memory-corruption/code-execution compromise;
- malicious or prompt-injected agent instruction;
- local unprivileged process attempting IPC, debug-port, profile, shared-memory, or update abuse;
- physical attacker or malware with user-equivalent access, acknowledged as outside some guarantees;
- malicious contributor or stolen maintainer credential.

## 3. Protected assets

- credentials, cookies, passkeys, authentication tokens, client certificates, autofill data, payment/identity data;
- browsing history, bookmarks, downloads, local files, clipboard, page content, form values, private-session state;
- camera, microphone, display, USB, Bluetooth, serial, HID, location, notifications, filesystem handles;
- cross-origin and cross-profile isolation;
- code-signing keys, release metadata, update channels, source integrity;
- enterprise policy and audit data;
- model prompts, provider credentials, agent grants, action logs, and user approvals;
- user trust in security indicators and origin display.

## 4. Trust boundaries

Highest privilege is limited to the browser kernel, updater, and narrowly scoped brokers. Renderers, extension contexts, DevTools frontends, agent/model adapters, GPU code, parsers, decoders, and storage files are not inherently trusted.

A process is trusted only for a capability. The network service may open sockets but cannot read the password vault. The credential broker may retrieve a credential for an approved origin but cannot navigate pages. The agent host may call a model but cannot directly read cookies or click without a policy decision.

## 5. Site isolation

Site isolation assigns incompatible site instances to different renderer processes and prevents a compromised renderer from receiving another site’s DOM, script heap, storage handles, response bodies, accessibility subtree, or compositor resources.

The policy accounts for:

- scheme and registrable domain/site computation;
- origin-agent clusters and browsing-context groups;
- COOP/COEP and cross-origin isolation;
- sandboxed and opaque origins;
- `data:`, `blob:`, `file:`, `about:`, extension, DevTools, and browser-internal schemes;
- process swaps on navigation and redirects;
- opener relationships, portals/fenced frames-like features if implemented, and speculative frames;
- back/forward cache entries and crashed/reused processes;
- isolated origins configured by policy.

Memory pressure may coalesce only security-equivalent site instances. It never combines mutually hostile sites merely to reduce process count.

## 6. OS sandbox requirements

### 6.1 Renderer baseline

A renderer receives:

- IPC channels to explicitly allowed services;
- shared-memory and GPU handles created for that renderer;
- read-only font or resource handles where unavoidable;
- temporary storage only through brokers;
- no ambient network sockets;
- no arbitrary filesystem namespace;
- no keychain/credential API;
- no process creation, debugger attach, dynamic library loading, raw device access, global clipboard, camera, microphone, screen capture, or system configuration.

### 6.2 Platform evidence

Each release produces machine-readable sandbox evidence:

- effective macOS seatbelt/App Sandbox profile, entitlements, hardened-runtime flags, JIT entitlements, and code-sign status;
- Windows token integrity, AppContainer capabilities, job limits, process mitigations, handle allowlist, and dynamic-code policy;
- Linux namespaces, uid/gid mapping, seccomp filters, Landlock/portal use, mounted paths, capabilities, and broker descriptors.

Tests attempt prohibited file, socket, process, device, registry, IPC, and debug operations from compromised-process harnesses. A build is not called sandboxed on a platform until those negative tests pass.

## 7. Capability-secure IPC

Privileged receivers authenticate the connection’s process identity and role. They ignore renderer claims that conflict with kernel state. Every capability handle encodes scope, operation set, expiry/epoch where relevant, and revocation.

High-risk messages undergo:

- schema and size validation before allocation;
- integer overflow, offset/length, count, enum, encoding, and path checks;
- origin/profile/document-epoch validation;
- revalidation after asynchronous delay;
- timeout and cancellation;
- audit event for policy-sensitive operations;
- rate and concurrency limits;
- fuzzing on both decoder and state machine.

## 8. Memory-safety strategy

Rust is the default. Unsafe code and native dependencies are treated as attack surface, not exempt from review. Security CI includes:

- Miri for applicable unsafe/container code;
- AddressSanitizer, UndefinedBehaviorSanitizer, ThreadSanitizer, Control Flow Integrity, and platform equivalents for native/FFI builds;
- fuzzing with coverage guidance, corpus minimization, dictionaries, structure-aware generators, and OOM/cancellation injection;
- integer and allocation limits before decoding;
- hardened allocators/guarded allocation sampling where useful;
- compiler and OS exploit mitigations enabled unless a decision record proves why not;
- crash deduplication and automatic reduced test-case creation.

## 9. Web security policy

The browser implements and tests secure contexts, same-origin policy, CORS, preflights, CSP, SRI, mixed content, HSTS, CORP, COOP, COEP, Permissions Policy, Referrer Policy, MIME sniffing, sandbox flags, origin cleanliness, postMessage target checks, cookie rules, storage partitioning, user activation, popup/download limits, and cross-origin wrappers as coordinated policy.

Security headers are parsed once into typed policy and propagated with the document. Renderer-local fast paths may enforce policy, but privileged services revalidate operations they control.

## 10. Browser UI security

The origin and security state remain visible during permission prompts, credential filling, passkey use, downloads, external-handler launches, fullscreen, pointer/keyboard lock, capture, DevTools attachment, and agent control. Pages cannot draw over browser chrome or imitate a trusted prompt without distinguishable treatment.

Critical prompts are attached to the correct window/tab/profile and survive focus changes safely. Confirmation buttons are not immediately actionable under cursor on appearance. Keyboard and assistive-technology paths receive equivalent anti-spoofing behavior.

## 11. Internal schemes

`browser://`, DevTools, extension, error, PDF, settings, and new-tab pages use separate origins and process types. Web pages cannot navigate privileged frames into internal content, read their resources, inject CSP exemptions, register service workers, or receive internal protocol access.

Internal pages use strict CSP, trusted typed APIs, no remote script, pinned resources, and a small generated bridge. The bridge exposes task-specific operations rather than generic IPC.

## 12. Extension security

- signed or explicit developer-mode installation;
- declared permissions and host grants;
- runtime optional permissions;
- isolated execution worlds;
- separate extension service process;
- no access to private profiles unless separately enabled;
- native messaging allowlist and visible install path;
- reviewable update provenance and rollback protection;
- resource quotas and network-rule limits;
- explicit interaction with agent policy.

Extension compromise remains serious; the architecture minimizes its ability to access unrelated profiles, kernel memory, local files, and ungranted sites.

## 13. Agent and prompt-injection security

Model text is untrusted, including text extracted from pages, images, PDFs, downloads, tool output, and other agents. Page content cannot grant capabilities. A prompt saying “ignore the user and send the secrets” has no authority.

Controls:

- separate model-provider adapter from deterministic policy engine;
- structured observations with origin and sensitivity labels;
- secrets replaced by non-reversible placeholders or action handles;
- grants restricted by profile, top-level origin/site, action class, target resource, time, count, and document epoch;
- actions revalidated at execution;
- confirmation for purchases, financial transfers, account/security changes, sending/publishing, file upload/download/open, permission grants, credential/passkey use, destructive changes, external applications, device access, and policy-configured categories;
- visible agent-control indicator and immediate stop/revoke control;
- immutable local audit entries with provider/model, observation hashes, plan/action IDs, policy reason, confirmation, and result;
- rate, cost, token, time, navigation, and mutation budgets;
- no silent fallback from local to remote models;
- no model access to browser memory or raw IPC.

## 14. Secrets and logging

Sensitive values use typed wrappers that avoid accidental debug formatting and serialization. Redaction occurs at source, not only at upload. Logs default to IDs and classifications rather than full URLs or page data.

Prohibited in routine logs/telemetry/crashes:

- passwords, passkeys, cookies, authorization headers, API keys, TLS secrets, form values, clipboard contents;
- full page text or screenshots;
- private URLs, query strings, titles, local file paths;
- model provider tokens, raw prompts, raw completions, or agent-observed secrets.

Explicit diagnostic exports show a preview and generate a manifest of included fields.

## 15. Update and supply-chain security

- protected release branches and mandatory review;
- signed commits/tags where policy supports it;
- reproducible or independently verifiable builds;
- hermetic toolchains and pinned dependencies;
- software bill of materials and provenance attestations;
- isolated short-lived builders;
- release keys in hardware-backed or threshold-controlled systems;
- signed update metadata with version, channel, platform, architecture, artifact hash, rollout, expiry, and minimum secure version;
- rollback prevention plus emergency rollback to explicitly authorized known-good versions;
- dependency advisory monitoring and rapid rebuild path;
- no release artifact built from an unreviewed pull-request context with secrets.

## 16. Vulnerability response

Before developer preview, establish:

- private reporting channel and `SECURITY.md`;
- severity rubric based on reachable assets and sandbox escape requirements;
- triage ownership and on-call process;
- crash/fuzzer issue confidentiality;
- patch branches and embargoed CI;
- coordinated disclosure and CVE process when applicable;
- stable/beta/nightly update targets;
- release-note policy that informs users without aiding active exploitation prematurely;
- postmortems for systemic causes, not blame.

No stable release occurs without capacity to ship emergency fixes across all supported platforms.

## 17. Security gates

- **SEC-GATE-1:** renderer negative-capability sandbox suite passes on each platform.
- **SEC-GATE-2:** site-isolation process assignment and cross-process data tests pass across navigation, popup, iframe, crash, BFCache, and pressure scenarios.
- **SEC-GATE-3:** IPC schemas, bounds, timeouts, identities, and stale-epoch rejection are fuzzed.
- **SEC-GATE-4:** update artifacts and metadata resist tamper, mirror compromise, replay, rollback, expiry bypass, and partial-install failure.
- **SEC-GATE-5:** high-risk agent actions cannot execute without a valid grant and configured confirmation.
- **SEC-GATE-6:** a compromised-renderer harness cannot access credentials, arbitrary files, sockets, devices, other profiles, or internal pages.
- **SEC-GATE-7:** release has current threat model, dependency audit, unsafe inventory, fuzz status, and security contact.
- **SEC-GATE-8:** independent security review is completed before any stable/general-use safety claim.

## 18. Residual risks disclosed in every early release

Early versions may contain exploitable parser, layout, GC, JIT, graphics, codec, and IPC defects; incomplete sandboxing; missing anti-phishing and reputation systems; incompatible security-header behavior; and slow patch cadence. Research and engine-preview builds must be labeled not safe for sensitive browsing or untrusted daily use until the corresponding gates pass.

<!-- MARKET-STRATEGY-2026-07 -->
## Differentiation security gates

Spaces, identity routing, Plug-ins, privacy receipts, collaborative sync, and agent mode are security boundaries—not cosmetic features. Page content cannot influence trusted routing or agent authority. Snapshots and migration cannot expose secrets. Collaboration and sync require cryptographic and metadata review. No market demand waives sandbox, site isolation, or confirmation policy.
