# Servo Security and Maintenance Implications - July 2026

Status: first-pass security and maintenance implications; no security approval, sandbox approval, maintenance commitment, or source-strategy decision
Owner: security, architecture, program, release operations, documentation, and source-strategy owners
Related gate: `PB-002`, `ADR-0009`, `ADR9-EV-015`, `ADR9-EV-016`
Date: 2026-07-19 metadata refresh; original evidence capture 2026-07-17

## Question

What security/sandbox implications and upstream-maintenance signals are visible in the inspected Servo checkout and current upstream metadata, and what remains before any Servo relationship can enter a Turing release path?

This report does not approve Servo source, dependencies, sandboxing, release infrastructure, security response, LTS posture, upstream relationship, or maintenance burden for Turing. It records evidence that must be converted into owner-reviewed security and program decisions before `ADR-0009` can be accepted, rejected, or superseded.

## Sources and Environment

Primary local evidence came from the external Servo checkout at `C:\ts\servo`, outside this repository.

| Item | Value |
|---|---|
| Servo commit inspected | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Tracked-file status | `0` changed paths |
| Repository metadata command | `gh repo view servo/servo --json ...`, run 2026-07-17 |
| GitHub repository | `servo/servo`, public, not archived, default branch `main` |
| GitHub repository activity | `pushedAt` `2026-07-17T22:08:58Z`, `updatedAt` `2026-07-17T22:15:14Z` |
| GitHub latest release metadata | `v0.3.0`, published `2026-06-25T15:09:42Z` |
| Additional release-list observations | `v0.1.2 (LTS)` published `2026-07-06T12:13:24Z`; `v0.1.1 (LTS)` and `v0.1.0 (LTS)` also listed |
| Security policy | GitHub security policy enabled; local `SECURITY.md` points to GitHub security reports |
| License | MPL-2.0 from GitHub metadata |
| Repository controls observed | `22` workflow files, `25` CODEOWNERS rules, `19` Dependabot groups |
| Turing repository role | documentation and registry update only |
| Commands | read-only `git`, `gh`, `Get-Content`, `Get-ChildItem`, `rg`, and file inspection |

## Method

The analysis inspected:

1. Servo sandbox and multiprocess code under `components/constellation/`, `components/config/`, `components/servo/`, and `ports/servoshell/`;
2. event-loop, process-manager, origin-check, profile/resource-thread, and storage-thread surfaces;
3. feature and dependency surfaces for MozJS/SpiderMonkey, WebRender, WebGL, WebGPU, GStreamer, Bluetooth, `gaol`, and release packaging;
4. upstream security policy, CODEOWNERS, Dependabot, release, platform build, bencher, and nightly-upload workflows;
5. the current Turing security Blueprint, security-engine book, source-strategy packet, and prior Servo provenance/native/component reports.

No Servo sandbox test, compromised-renderer test, WPT security run, fuzz run, negative filesystem/socket/device test, release drill, upstream merge drill, or security-response exercise was executed.

## 2026-07-19 upstream metadata refresh

A read-only refresh of the official GitHub repository, `main` branch, latest release, and crates.io package metadata found that the repository was pushed and updated at `2026-07-19T20:13:05Z` and `2026-07-19T20:13:09Z`, respectively; `main` now points to `736ad1bda08c1af419aadc903e82938f8610a65d`; the latest published release remains immutable `v0.3.0` on `release/v0.3`; and the latest crates.io package remains `servo 0.4.0`. These are freshness observations only. No new checkout, build, sandbox, dependency, compatibility, performance, security, or maintenance evidence was produced.

## Security and Sandbox Observations

Servo has security-relevant separation concepts, but the inspected state is not equivalent to Turing's required security model.

| Area | Observation | Turing implication |
|---|---|---|
| Default process options | `Opts::default()` sets `multiprocess: false` and `sandbox: false` | A default Servo shell run is not evidence for Turing's multiprocess or sandbox requirements |
| User-facing sandbox option | `servoshell` exposes `--sandbox` as "Run in a sandbox if multiprocess" | Sandbox posture depends on explicit configuration and platform support |
| Windows sandbox support | The Windows-target `content_process_sandbox_profile()` logs unsupported sandboxed multiprocess and exits; the Windows content-process `create_sandbox()` path panics when sandboxing is requested | The current Windows reference host has no Servo sandbox approval path for Turing release use |
| Windows multiprocess spawn | The Windows/Android/OpenHarmony/ARM/RISC-V spawn path starts an unsandboxed child process | Multiprocess alone does not satisfy Turing's compromised-renderer containment requirements |
| macOS/Linux sandbox profile | Servo defines `gaol`-based profiles for macOS and non-Windows/non-mobile Unix-like targets with file-read allowances for fonts/resources and system information | Useful reference material, but still requires platform-specific effective-policy evidence and negative tests |
| Sandboxed process management | The process manager can track `Sandboxed(u32)` but notes wait handling is not implemented for sandboxed processes | Lifecycle and cleanup behavior need review before any release-path boundary claim |
| Event-loop reuse | New pipelines reuse event loops by registered domain except sandboxed-origin contexts, and `about:blank`/`about:srcdoc` share creator event loops | This is not yet a Turing site-isolation decision; origin/site/profile and browsing-context-group behavior need focused tests |
| Origin checks | Broadcast channel, storage event, and service-worker paths check message origin against the pipeline origin in the constellation | Positive identity-preservation signal, but not a full cross-origin or cross-profile isolation proof |
| Public/private separation | Event-loop setup chooses public or private resource/storage threads based on `is_private` | Profile separation exists as an implementation concept, but it still needs storage, cookie, cache, service-worker, DevTools, crash, and process-boundary tests |
| Content-process authority | Initial script state receives senders for resource/storage threads, DevTools, font service, paint, memory/time profilers, optional Bluetooth, WebGL/WebXR, privileged URLs, and user contents | A Turing authority map must classify every sender, capability, lifetime, and policy check before accepting any component boundary |
| Certificate controls | `ignore_certificate_errors` exists in core options; WebDriver `acceptInsecureCerts` defaults to false | Turing must forbid accidental weakening of certificate policy and record any test-only exceptions |

The most important current security implication is direct: the inspected Windows path does not provide a usable sandboxed-content-process model. Any `ADR-0009` option that depends on Servo release code on Windows must either reject that dependency, design a Turing-owned Windows sandbox around it, or accept a time-bounded non-release experiment with explicit unsafe-use labeling.

## Native, Media, GPU, Runtime, and Update Risk Surfaces

Prior reports already mapped dependency, generated-code, native-package, unsafe, FFI, component-boundary, and JavaScript-runtime risk surfaces. The security implication for `ADR9-EV-015` is that those surfaces must be reviewed as authority and exploit-chain inputs, not only as build or legal inputs.

| Surface | Current evidence | Required decision before release-path use |
|---|---|---|
| MozJS/SpiderMonkey and `js_jit` | Servo default features include `js_jit`; `servoshell` defaults include `js_jit` | Decide whether this supersedes `ADR-0004`, is excluded, or remains only a comparator |
| WebRender/WebGL/WebGPU | WebRender is in workspace dependencies; `servoshell` defaults include `webgpu`; optional WebGPU feature crosses script, paint, constellation, and traits | GPU process, driver, shader, buffer, capture, and crash containment review |
| GStreamer/media | Workspace includes many `gstreamer*` crates and optional media-gstreamer feature; Windows bootstrap pulls GStreamer packages in prior native audits | Codec/native package source-build or binary exception, sandbox, license, patent, crash, and media permission review |
| Native Bluetooth | Optional `native-bluetooth` reaches platform device APIs | Device permission, broker, profile, prompt, and revocation model |
| `gaol` sandbox library | Present as a workspace dependency and used for supported sandbox paths | Platform capability mapping, active-maintenance review, and negative sandbox tests |
| Release workflow and artifacts | Upstream has scheduled/manual release workflow, production builds, source archive upload, artifact attestations, crates.io publishing path, and nightly upload script | Turing cannot inherit this as an update system; update trust, signing, rollback, emergency patching, and support windows remain Turing-owned |

## Maintenance and Upstream Signals

The upstream project has active maintenance signals, but those signals are not Turing support guarantees.

| Signal | Observation | Turing implication |
|---|---|---|
| Repository state | `servo/servo` is public, not archived, and the 2026-07-19 refresh observed push/update metadata at `2026-07-19T20:13:05Z` / `2026-07-19T20:13:09Z` | Active upstream signal only; not a contractual dependency guarantee |
| Release cadence | Recent release list includes `v0.3.0` and LTS-labeled `v0.1.x` releases in 2026 | Useful for monitoring, but Turing needs exact patch/backport expectations |
| Security reporting | GitHub security policy is enabled and local `SECURITY.md` points to GitHub security reports | Good upstream channel signal; not a Turing vulnerability SLA |
| CODEOWNERS | `25` path rules cover script, layout, compositing, fonts, servoshell, canvas, WebGPU, WebDriver, XPath, DevTools, CI, and crown | Review ownership exists upstream; Turing still needs its own named owners and backup owners |
| Dependabot | Daily Cargo configuration with grouped updates, Stylo ignores, and wgpu patch-only automation | Active dependency maintenance signal; Turing needs its own advisory and exception decisions |
| Workflows | `22` workflow files cover major platforms, WPT, releases, docs, lint, Docker, try labels, and other operations | Strong CI surface, but Turing must decide which evidence is reusable and what remains independently verified |
| Release workflow | Scheduled/manual release flow builds production artifacts for major platforms, uploads vendored source, attests artifacts, and can publish crates | Release capability exists upstream; Turing cannot outsource its release authority, signing, support statement, or emergency response |
| Project coordination | README points to GitHub issues, Servo Zulip, and video calls advertised in the Servo Project repo | Collaboration channels exist; Turing still needs contribution etiquette, patch-ownership, escalation, and fallback policy |

## Required Owner Decisions

`ADR9-EV-015` remains incomplete until Turing owners produce, review, and accept:

- process authority maps for each `ADR-0009` option, including content, network, storage, GPU, media, DevTools, WebDriver, extension, agent, updater, and embedder boundaries;
- Windows, macOS, and Linux sandbox deltas, including effective policies and negative tests for file, socket, process, registry, device, debug, shared-memory, profile, credential, and IPC access;
- origin, site, profile, private-mode, browsing-context-group, service-worker, storage, cache, cookie, and DevTools identity-preservation tests;
- native/media/GPU/runtime/update risk review covering MozJS, JIT, WebRender, WebGL, WebGPU, GStreamer, Bluetooth, FFI, generated code, native packages, and update artifacts;
- fuzzing, sanitizer, crash, memory-corruption, and compromised-process evidence for any accepted component boundary;
- explicit unsupported behavior and residual risk for every platform and maturity level.

`ADR9-EV-016` remains incomplete until Turing owners produce, review, and accept:

- patch ownership for clean-reference, selective-component, upstream-first, Servo-derived, and charter-change options;
- upstream cadence and tracking policy, including selected source baseline, branch/release choice, merge window, and stale-evidence trigger;
- LTS and security-response expectations, including what Turing expects from upstream versus what Turing must self-maintain;
- merge burden estimate for source, generated output, dependencies, native packages, WPT metadata, SpiderMonkey/Stylo/WebRender/GStreamer, and platform build changes;
- breakage handling and rollback plan;
- named primary owner, backup owner, reviewer, release owner, security owner, and legal/community owner for any accepted relationship.

## Inference

The evidence moves `ADR9-EV-015` and `ADR9-EV-016` from missing to partial. Turing now has concrete source evidence for the Windows sandbox gap, process/event-loop/security-relevant sender surfaces, native/media/GPU/runtime/update review areas, and upstream maintenance signals. It still has no owner-approved security model, no platform sandbox proof, no accepted maintenance contract, no source-strategy recommendation, and no release-code authorization.

## Unsupported Conclusions

This report does not show:

- Servo is safe for hostile browsing;
- Servo's Windows content process is sandboxed;
- Servo's macOS or Linux sandbox profiles satisfy Turing release gates;
- Servo's process model preserves all Turing origin, site, profile, storage, DevTools, extension, or agent boundaries;
- Servo native, media, GPU, JIT, WebDriver, Bluetooth, or update surfaces are acceptable for Turing release code;
- Servo's upstream security policy, LTS labels, workflows, CODEOWNERS, or Dependabot configuration satisfy Turing's support obligations;
- Turing has staffing or owner capacity for any Servo relationship;
- any `ADR-0009` option is accepted.

## Documentation and Registry Impact

This report affects:

- [ADR-0009 Source Strategy Decision Packet](../project-buildout/14-adr-0009-source-strategy-decision-packet.md);
- [ADR-0009 Evidence Traceability Matrix](../project-buildout/15-adr-0009-evidence-traceability-matrix.md);
- [`adr-0009-evidence.json`](../blueprint-v1/machine/adr-0009-evidence.json);
- [`pre-build-readiness.json`](../blueprint-v1/machine/pre-build-readiness.json);
- [Build Readiness Operating Board](../project-buildout/13-build-readiness-operating-board.md);
- [Pre-build readiness checklist](../project-buildout/11-pre-build-readiness-checklist.md);
- [Research index](README.md);
- [Documentation index](../README.md);
- [Repository map](../repository-map.md);
- [Research log](../research-log.md);
- [Research program](../blueprint-v1/22-research-program.md);
- [Security policy](../security.md);
- [Security engineering book](../security-engine/README.md).

It does not change source code, dependency approvals, security ledgers, release gates, support statements, public claims, or the blocked status of `PB-002`.
