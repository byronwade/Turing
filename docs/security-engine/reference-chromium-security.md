# Chromium as a security reference

Status: authoritative external security reference. Owner: browser security
architecture. Added 2026-07-20 by owner direction.

/ Reference: [`chromium/chromium`](https://github.com/chromium/chromium) /

Chromium is the most battle-tested browser security codebase in existence:
two decades of adversarial exposure, a public bug-bounty history, a mature
sandbox and site-isolation architecture, and an unusually well-documented
security-process culture. This project treats it as a **primary reference
for threat modeling, exploit-class enumeration, mitigation design, and
vulnerability-response practice.**

## The boundary this reference does not cross

`AGENTS.md` is unambiguous: release paths must not depend on Chromium,
Blink, V8, or any of their components, and "from scratch" is a hard
constraint. **This reference is for learning, not for lifting.** Concretely:

- **Permitted:** reading Chromium's design documents, security notes, threat
  models, `//docs/security/` guidance, public vulnerability write-ups, the
  "Rule of 2", the security-severity guidelines, and its sandbox/IPC/site-
  isolation architecture — and letting those *inform* Turing's own,
  independently written design and threat model.
- **Prohibited:** copying Chromium source into Turing; depending on any
  Chromium/Blink/V8 component in a release path; reproducing GPL/BSD-covered
  code without the license review `docs/blueprint-v1/03` requires; or citing
  "Chromium does X" as sufficient justification for a decision without an
  independent rationale that stands on its own.

A design that can only be justified by "Chromium does it this way" has not
been justified. Chromium is where we learn which attacks exist and which
mitigations have survived contact with real adversaries; the decision to
adopt a mitigation is still made against Turing's own threat model, recorded
in this book with its own reasoning.

## How to use it, per subsystem

| Turing security chapter | What Chromium teaches |
| --- | --- |
| [01 threat model / process isolation](01-threat-model-and-process-isolation.md) | Site Isolation, the renderer-is-untrusted assumption, `//docs/security/` threat models |
| [02 sandbox / brokers](02-sandbox-brokers-and-platform-containment.md) | The platform sandbox designs (seccomp-bpf, Windows AppContainer, macOS Seatbelt), broker patterns |
| [03 memory safety / JIT hardening](03-memory-safety-jit-and-exploit-hardening.md) | The Rule of 2, V8 sandbox / pointer compression, JIT mitigation history, MiraclePtr/BackupRefPtr |
| [04 web security / trusted UI](04-web-security-privacy-and-trusted-ui.md) | Same-origin/CORS/CSP enforcement points, the trusted-chrome spoofing history, permission-prompt design |
| [05 update / supply chain / response](05-update-supply-chain-and-vulnerability-response.md) | The security-severity guidelines, disclosure timelines, the release-to-patch pipeline |
| [07 speculation / side channels](07-speculation-timers-and-side-channels.md) | Spectre mitigations, cross-origin isolation (COOP/COEP), timer coarsening |
| [08 parser / codec isolation](08-native-parser-and-codec-isolation.md) | Why codecs and parsers are the highest-value isolation targets; the codec-CVE history |

## Operating rule for agents and contributors

When designing or reviewing any trust-boundary or hostile-input change,
**consult the corresponding Chromium security material as a checklist of
attacks and mitigations to have considered** — then design Turing's answer
independently and record it here. If a Chromium mitigation is deliberately
*not* adopted, say so and say why, because a known mitigation silently
omitted is the failure mode this reference exists to prevent.

Chromium's severity guidelines are also the recommended calibration for this
project's own severity language until Turing publishes its own: a bug that
Chromium would rate Critical (renderer RCE to sandbox escape, universal
cross-site scripting) is Critical here.
