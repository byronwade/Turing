# Native UI and Accessibility Workflow Examples - July 2026

Status: no-claim sample workflow records for `PB-003`, `PB-005`, `PB-014`, and `PB-015`; no toolkit, page-surface, accessibility, or UI-gate claim
Owner: UI runtime, accessibility, platform, product, security, quality, performance, and release operations
Research date: 2026-07-19

## Purpose

The [Native UI and Accessibility Closure Preparation](native-ui-and-accessibility-closure-preparation-2026-07.md) defines the cross-lane evidence order for trusted chrome, page-surface composition, input/IME, component fixtures, and assistive technology. This page gives a sample workflow record showing how one address-field and page-surface interaction should bind authority, identity, accessibility semantics, fault behavior, and measurements.

All values are fictitious. They are not evidence that a toolkit, page surface, accessibility bridge, screen reader, or platform workflow exists or works.

## Sample workflow record

```yaml
record_status: sample_only_no_claim
workflow_id: UI-SAMPLE-ADDRESS-FIELD-PAGE-SURFACE-0001
task_id: TASK-000006
source_commit: SAMPLE-COMMIT-REPLACE-BEFORE-USE
platform: windows-x64
os_build: SAMPLE-OS-BUILD
toolkit_adapter: toolkit-neutral-reference-adapter-sample
page_surface_path: brokered-surface-handle-sample
hardware_tier: SAMPLE-TIER-M
profile: fake-profile-only
fixture_root: runner-owned-temporary-root
security_state: no-account-no-real-credentials-no-public-data
```

## Workflow stages

| Stage | Required observation | Required evidence | Sample result |
|---|---|---|---|
| Window creation | Trusted shell receives a bounded window identity and epoch | Source/target identity, epoch, adapter event, authority decision | `sample_not_run` |
| Command-field focus | Keyboard focus moves to the command field without page content minting a command | Focus owner, document/page identity, command validation, stale-event result | `sample_not_run` |
| Text input and IME | Plain text, dead key, composition, commit, cancellation, and invalid sequence are distinguished | Input event trace, composition state, locale/keyboard layout, cancellation outcome | `sample_not_run` |
| Navigation proposal | Field submits a typed navigation intent to the browser authority | Command schema, origin/profile context, confirmation/rejection, no direct toolkit navigation | `sample_not_run` |
| Page-surface attach | A page texture/surface is attached only with document, origin/site/frame, process, and device generations | Handle lease, identity tuple, resize/scale/damage metadata, broker decision | `sample_not_run` |
| Accessibility tree update | Chrome and page subtrees expose stable names, roles, states, focus, and relationships | Platform tree snapshot, semantic diff, event order, live-region behavior | `sample_not_run` |
| Screen-reader interaction | The declared platform assistive technology announces focus, role, value, state, and error | Manual transcript, AT version/configuration, action/result timestamps | `sample_not_run` |
| Fault injection | Renderer hang, stale surface, GPU loss, and adapter failure produce bounded recovery UI | Fault trigger, identity preservation, fallback, user-visible result, cleanup | `sample_not_run` |
| Measurement | Input-to-focus, input-to-announcement, tree-update, surface-present, and recovery latency are captured | p50/p95/p99 traces, resource artifacts, failure denominator | `sample_not_run` |

## Authority and identity checks

The workflow must demonstrate, with negative cases, that:

- page content, renderer output, accessibility events, extensions, DevTools, or agent input cannot invoke browser navigation directly;
- a stale document, frame, process, device, or surface generation cannot update trusted chrome or a page subtree;
- an accessibility event cannot grant credentials, permissions, persistence, profile access, agent authority, or privileged surface handles;
- toolkit callbacks produce only validated typed commands or declared rendering data;
- renderer crash, GPU loss, timeout, cancellation, and adapter failure do not silently retain authority or misroute focus;
- software fallback preserves identity and authority boundaries rather than bypassing them.

## Platform accessibility record

The real packet must name the platform API and assistive technology actually used. A sample matrix is:

| Platform | Accessibility API | Assistive technology | Required retained artifact |
|---|---|---|---|
| Windows | UI Automation | Narrator and/or NVDA | Tree snapshot, action transcript, focus/live-region result, version/configuration |
| macOS | AXAPI | VoiceOver | Tree snapshot, action transcript, focus/live-region result, version/configuration |
| Linux | AT-SPI | Orca | Tree snapshot, action transcript, focus/live-region result, version/configuration |

Rows not executed are `not_run` or `unsupported`, never passes. Results from one platform or assistive technology cannot be generalized to the others.

## Rejection rules

Reject the sample packet as readiness evidence when it uses a mock tree instead of a platform tree, automated accessibility checks instead of manual assistive-technology review, a toolkit-owned navigation path, an unbound page surface, a stale identity, an omitted IME case, a swallowed fault, a missing latency denominator, or a placeholder reviewer. Screenshots and a passing validator do not establish accessibility or trusted-chrome readiness.

The next acceptable artifact is a reviewed immutable `TASK-000006` package for one adapter, one platform, and the declared workflow. It must replace sample fields with rendered fixtures, platform tree snapshots, manual transcripts, negative authority tests, fault traces, measurements, and named review.

## Claim boundary

This page is sample-only documentation. It does not select a toolkit, establish trusted chrome, prove page-surface composition, accessibility, screen-reader coverage, IME correctness, UI-GATE-7, UI-GATE-10, performance, Chrome-class parity, or release-path readiness.
