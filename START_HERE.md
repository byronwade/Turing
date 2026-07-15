# Turing Browser Program — Start Here

Turing is the working codename for an independent, Rust-first browser and web-engine program. The project is deliberately not a Chromium, WebKit, Gecko, Electron, or operating-system web-view wrapper. Its long-term target is broad modern-web compatibility, a materially lower memory footprint under large tab sets, developer-grade tooling, and an AI-agent surface designed as a security boundary rather than a hidden automation layer.

This repository is a program bootstrap, not a claim that a production-safe Chrome replacement already exists. A browser that can safely render arbitrary hostile web content is an operating-system-scale project. Every release must state exactly which standards, security controls, media formats, accessibility functions, extension APIs, enterprise controls, and platform integrations are implemented and independently tested.

## Canonical documentation

Read [`blueprint-v1/README.md`](blueprint-v1/README.md) first. It links the product charter, Chrome-equivalent capability inventory, language study, architecture, engine plans, threat model, memory strategy, AI authorization model, UI system, compatibility program, release operations, roadmap, and risk register.

The executable bootstrap is under [`prototype/`](prototype/). It encodes several non-negotiable invariants in dependency-free Rust: typed process roles, bounded messages, explicit tab lifecycle transitions, ordered rendering stages, scoped network authority, and deterministic AI-agent authorization.

## Non-negotiable definitions

**Independent engine** means Turing owns the DOM, CSS/style system, layout, display-list construction, browser process model, navigation lifecycle, JavaScript integration, permissions, storage partitioning, developer tooling, and agent protocol. It does not mean reimplementing cryptography, Unicode tables, font shaping, image codecs, or operating-system sandbox primitives without a security justification.

**Chrome-equivalent capability** is a tracked destination, never a marketing shortcut. It includes the web platform, accessibility, internationalization, media, printing, PDF, downloads, password and credential management, extensions, developer tools, automation, sync, updates, enterprise policy, crash recovery, security response, and distribution—not merely successful page rendering.

**Low memory** means measured private working set and resident memory on a published workload, with tab lifecycle, process count, site-isolation state, page types, background activity, and discard policy disclosed. Discarding 25 of 30 tabs is not presented as equivalent to keeping 30 hostile sites fully live.

**AI assistance** is capability-scoped. Models do not receive ambient access to cookies, credentials, cross-origin content, downloads, local files, clipboard, camera, microphone, payments, messages, or destructive actions. High-impact operations require deterministic policy checks and visible user confirmation.

## Current publication state

The default branch contains only the repository initialization. The complete program is introduced on `agent/bootstrap-browser-program` so the architecture and risk posture can be reviewed before becoming the default branch.
