# Benchmark Competitor Runbook Examples - July 2026

Status: no-claim sample records for `PB-013`; no browser run, competitor result, or performance claim
Owner: performance measurement, benchmark operations, quality, security, and release operations
Research date: 2026-07-19

## Purpose

The [Chrome-Class Performance Runbook](chrome-class-performance-runbook-2026-07.md) defines the evidence levels and controls for Chrome-class and extreme-performance work. This page supplies two illustrative, sample-only competitor records so a future runner and reviewer have a concrete shape for Chrome Stable and Firefox Stable without confusing an executable inventory, release-catalog observation, or browser-pin diagnostic with benchmark evidence.

The values below are intentionally fictitious. They are not current browser versions, measurements, executable hashes, or statements about Chrome or Firefox behavior. Replace every sample value with runner-captured evidence before using the record.

## Required record shape

Every competitor record must bind browser identity to the exact workload and lab state:

| Field group | Required fields | Why it matters |
|---|---|---|
| Identity | `browser_id`, product, channel, version, platform, architecture, release-date source, executable path/hash | A release catalog does not prove which binary ran. |
| Profile and policy | temporary profile root, profile hash, extension/account/sync state, feature flags, user-agent policy, sandbox/site-isolation/JIT state | Defaults and security posture can materially change behavior. |
| Lab controls | hardware tier, OS image/update state, driver, power mode, thermal state, display/refresh rate, network profile, cache state | Cross-run environmental differences invalidate causal comparison. |
| Workload | corpus/fixture hash, route map, suite/version, viewport/DPR, tab scenario, action script, cold/warm/repeat policy | A score without an exact workload cannot be reproduced. |
| Collection | timestamps, runner revision, command line, trace package, raw samples, memory/CPU/GPU/energy artifacts, screenshot/video when applicable | A summary is not a raw evidence package. |
| Outcome | status, failure class, timeout/crash/unsupported flags, denominator inclusion, metric values, uncertainty, artifact digests | Failed and unsupported cases must remain visible. |
| Review | owner, independent reviewer, review date, claim scope, expiry, rerun triggers, prohibited claims | Evidence does not become a public claim automatically. |

## Sample-only Chrome Stable record

```yaml
record_status: sample_only_no_claim
browser_id: chrome-stable-sample
product: Chrome
channel: Stable
version: SAMPLE-VERSION-DO-NOT-USE
platform: windows-x64
architecture: x86_64
release_date_source: SAMPLE-OFFICIAL-RELEASE-CATALOG-URL
executable_path: SAMPLE-RUNNER-OWNED-PATH
executable_sha256: SAMPLE-HASH-REPLACE-BEFORE-USE
profile:
  root: runner-owned-temp-profile
  sha256: SAMPLE-PROFILE-HASH
  extensions: none
  account_sync: disabled
  feature_flags: captured-by-runner
  user_agent_policy: captured-by-runner
  sandbox_site_isolation_jit: captured-by-runner
lab:
  hardware_tier: SAMPLE-TIER-M
  os_image_id: SAMPLE-CLEAN-IMAGE
  update_state: captured-before-and-after
  driver_set: SAMPLE-DRIVER-SET
  power_thermal_state: captured-and-stable
  display_refresh_hz: SAMPLE-REFRESH
  network_profile: no-claim-local-static
  cache_state: cold-and-warm-defined
workload:
  corpus_id: SAMPLE-CORPUS-ID
  corpus_sha256: SAMPLE-CORPUS-HASH
  suite: Speedometer-3.1-or-local-corpus
  suite_revision: SAMPLE-SUITE-REVISION
  viewport_dpr: SAMPLE-VIEWPORT-DPR
  tab_scenario: 30-tab-mixed-or-all-live
  action_script: SAMPLE-ACTION-SCRIPT-HASH
  repetitions: SAMPLE-COUNT
  warmup_policy: SAMPLE-WARMUP-POLICY
collection:
  runner_revision: SAMPLE-RUNNER-COMMIT
  command_line: captured-by-runner
  start_utc: SAMPLE-TIMESTAMP
  end_utc: SAMPLE-TIMESTAMP
  trace_package: SAMPLE-TRACE-PACKAGE-ID
  raw_samples: SAMPLE-RAW-SAMPLE-PACKAGE-ID
  resource_artifacts: SAMPLE-RESOURCE-PACKAGE-ID
outcome:
  status: sample_not_run
  failure_class: not_applicable
  denominator: retained-if-run
  metrics: not_collected
review:
  owner: null
  independent_reviewer: null
  claim_scope: none
  expires_at: null
  rerun_triggers: browser-update-suite-change-hardware-or-os-change
```

## Sample-only Firefox Stable record

The Firefox record uses the same fields. Do not compare records merely because both are labeled `Stable`; exact version, platform, settings, workload, and collection state must match the comparison bundle.

```yaml
record_status: sample_only_no_claim
browser_id: firefox-stable-sample
product: Firefox
channel: Stable
version: SAMPLE-VERSION-DO-NOT-USE
platform: windows-x64
architecture: x86_64
release_date_source: SAMPLE-OFFICIAL-RELEASE-CATALOG-URL
executable_path: SAMPLE-RUNNER-OWNED-PATH
executable_sha256: SAMPLE-HASH-REPLACE-BEFORE-USE
profile:
  root: runner-owned-temp-profile
  sha256: SAMPLE-PROFILE-HASH
  extensions: none
  account_sync: disabled
  feature_flags: captured-by-runner
  user_agent_policy: captured-by-runner
  sandbox_site_isolation_jit: captured-by-runner
lab:
  hardware_tier: SAMPLE-TIER-M
  os_image_id: SAMPLE-CLEAN-IMAGE
  update_state: captured-before-and-after
  driver_set: SAMPLE-DRIVER-SET
  power_thermal_state: captured-and-stable
  display_refresh_hz: SAMPLE-REFRESH
  network_profile: no-claim-local-static
  cache_state: cold-and-warm-defined
workload:
  corpus_id: SAMPLE-CORPUS-ID
  corpus_sha256: SAMPLE-CORPUS-HASH
  suite: local-corpus-or-supported-browserbench-suite
  suite_revision: SAMPLE-SUITE-REVISION
  viewport_dpr: SAMPLE-VIEWPORT-DPR
  tab_scenario: 30-tab-mixed-or-all-live
  action_script: SAMPLE-ACTION-SCRIPT-HASH
  repetitions: SAMPLE-COUNT
  warmup_policy: SAMPLE-WARMUP-POLICY
collection:
  runner_revision: SAMPLE-RUNNER-COMMIT
  command_line: captured-by-runner
  start_utc: SAMPLE-TIMESTAMP
  end_utc: SAMPLE-TIMESTAMP
  trace_package: SAMPLE-TRACE-PACKAGE-ID
  raw_samples: SAMPLE-RAW-SAMPLE-PACKAGE-ID
  resource_artifacts: SAMPLE-RESOURCE-PACKAGE-ID
outcome:
  status: sample_not_run
  failure_class: not_applicable
  denominator: retained-if-run
  metrics: not_collected
review:
  owner: null
  independent_reviewer: null
  claim_scope: none
  expires_at: null
  rerun_triggers: browser-update-suite-change-hardware-or-os-change
```

## Failure and comparison rules

- A missing browser pin, mismatched suite revision, different viewport or refresh rate, uncontrolled cache, changed security setting, or missing artifact digest makes the comparison incomplete; it is not a reason to silently omit the run.
- A crash, timeout, unsupported API, invalid subtest, or missing duration remains in the denominator with its failure class and raw evidence reference.
- A release-catalog version, local executable inventory, or browser-pin diagnostic can populate identity fields, but none is a benchmark result.
- Synthetic sample values never populate a claim bundle. A future claim bundle must reference runner-generated raw artifacts and owner-reviewed statistics.
- These examples do not authorize downloading, launching, or benchmarking a browser, accessing a real user profile, attaching an account, changing security settings, or publishing a comparison.

## Review handoff

Before Level 1 or higher work, the owner must approve the runner-owned temporary-profile policy, hardware/OS controls, corpus and server fixtures, competitor pin capture, trace/artifact package, failure denominator, and statistics plan. An independent reviewer must verify that the records describe what ran and what failed. The [Benchmark Evidence and Claim Closure Preparation](benchmark-evidence-and-claim-closure-preparation-2026-07.md) remains the authoritative transition from sample shape to evidence and claim review.

## Claim boundary

This page is sample-only documentation. It does not establish Chrome or Firefox versions, browser behavior, benchmark output, speed, memory, energy, compatibility, security, Chrome-class performance, extreme-performance leadership, or production readiness.
