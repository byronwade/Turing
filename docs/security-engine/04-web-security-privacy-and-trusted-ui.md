# Web Security, Privacy, and Trusted UI

Status: research and design baseline  
Owner: web security and browser UX  
Purpose: Keep origin policy, permissions, privacy, credentials, and user decisions coherent across engine and product surfaces.

## Relationship to the Turing program

This document expands the web policy and trusted-UI sections of [Blueprint 08](../blueprint-v1/08-security-and-sandbox.md) and the product behavior in [Blueprint 11](../blueprint-v1/11-product-ui-devtools.md).

## Unified web security policy

Same-origin policy, CORS, Fetch modes, CSP, SRI, mixed content, HSTS, CORP, COOP, COEP, sandboxing, permissions policy, referrer policy, MIME sniffing, user activation, origin cleanliness, postMessage, cookie rules, storage partitioning, downloads, and cross-origin wrappers are one coordinated system.

Policy is parsed into typed state with source provenance and document identity. Fast renderer checks are permitted, but privileged network, storage, credential, permission, and device services revalidate the operations they control.

## Origin and identity

Every web-visible resource carries URL, origin, site, profile, top-level site/partition, frame, document epoch, credentials mode, and policy context as appropriate. Opaque origins and internal schemes use unforgeable identities. Displayed origins are derived from committed navigation state, not page text.

Internationalized domains, confusables, certificate errors, redirects, downloads, external handlers, fullscreen, capture, and passkeys receive dedicated spoofing review.

## Credentials and sensitive data

Passwords, passkey private material, cookies, authorization headers, tokens, payment data, keychain contents, and hidden autofill values remain inside dedicated brokers. Renderers and models request an operation bound to an approved origin; they do not receive general credential databases.

Credential UI identifies the profile, origin, selected account, and effect. Logs, crashes, traces, automation output, and agent observations redact values at source.

## Permission system

Permissions bind origin, top-level context, profile, device/resource class, expiry, session, and user decision. Prompts occur only from trusted browser UI and cannot be page-styled or overlaid. Persistent decisions are inspectable and revocable. Active camera, microphone, display, location, device, fullscreen, pointer lock, download, extension, DevTools, and agent states remain visible.

Prompt timing, placement, focus, keyboard, and accessibility behavior are designed against clickjacking and habituation.

## Privacy architecture

Turing minimizes collected, retained, shared, and transmitted data. Storage, caches, network state, service workers, and identifiers are partitioned where standards and product policy require. Private sessions are ephemeral by construction and do not silently use normal-profile state.

Telemetry is opt-in or otherwise explicitly governed, data-minimized, locally aggregated where possible, documented by field, and never a hidden requirement for browser function. Remote AI transmission is separately indicated and configured.

## Trusted browser UI

The address field, origin state, certificate warnings, permissions, credentials, dangerous downloads, external protocols, extension installation, DevTools attachment, agent control/confirmation, update state, and crash recovery are rendered by protected browser UI. Web content cannot position above them, copy their privileged style without distinction, or receive their input events.

Critical state remains available under compact layouts, full screen, zoom, high contrast, screen readers, voice control, and keyboard-only operation.

## Internal pages and extensions

Settings, new tab, errors, PDF, DevTools, extensions, and browser pages use dedicated origins and process roles with strict CSP, pinned resources, no remote script, and small task-specific bridges. Web pages cannot navigate privileged frames, install service workers in internal origins, or obtain internal protocol access.

Extensions receive declared and optional host permissions, isolated worlds, event-driven/background budgets, signed or explicit developer installation, update provenance, and profile separation.

## Non-negotiable invariants

- Origin/profile/document identity is explicit and preserved across every policy boundary.
- Privileged services revalidate security-sensitive operations rather than trusting renderer checks.
- Credentials and secrets are brokered operations, not data handed to pages, tools, or models.
- Trusted UI cannot be covered, page-styled, or activated by page/model automation.
- Permission and privacy decisions are visible, revocable, accessible, and scoped.
- Internal schemes and extension privileges cannot leak into ordinary web origins.

## Required evidence

- WPT web-security suites plus Turing reduced policy traces.
- Phishing, IDN, origin-display, fullscreen, permission, credential, and trusted-UI usability studies.
- Cross-profile/private-session storage, cache, service-worker, and credential tests.
- Secret scanners for logs, crashes, traces, telemetry, protocols, and agent/provider payloads.
- Accessibility testing of every critical warning and confirmation.
- Extension and internal-page compromised-context harnesses.

## Known risks and unresolved questions

- Inconsistent policy implementations across network, renderer, storage, and UI can create bypasses.
- Prompt fatigue can turn nominal user consent into ineffective protection.
- Compatibility pressure may tempt broad cookie, storage, or mixed-content exceptions.
- Internal pages and extensions can recreate privileged web-app attack surfaces.

## Primary sources

- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- WHATWG DOM Standard — https://dom.spec.whatwg.org/
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/
- W3C Ethical Web Principles — https://www.w3.org/TR/ethical-web-principles/
- WAI-ARIA — https://www.w3.org/TR/wai-aria/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
