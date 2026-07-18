# Servo Performance Baseline Preparation - July 2026

Status: first-pass performance-baseline preparation; no performance, memory, energy, or speed claim
Owner: performance, benchmark operations, release operations, quality, documentation, and architecture
Related gate: `PB-002`, `PB-013`, `ADR-0009`, `ADR9-EV-014`
Date: 2026-07-17

## Question

What fixed-host, artifact, and runner-surface evidence exists around the external Servo build, and what remains before `ADR-0009` can use Servo performance or memory data in a source-strategy decision?

This report does not claim that Servo, Turing, or any source-strategy option is fast, low-memory, low-energy, Chrome-class, or suitable for performance comparison. It records the current host and artifact identity, the Servo performance command surfaces found in the external checkout, and the missing run record required before any performance inference is allowed.

## Sources and Environment

Primary local evidence came from the external Servo checkout at `C:\ts\servo`, outside this repository.

| Item | Value |
|---|---|
| Servo commit inspected | `4a0b2b1a218606c99fa1d45f6c78ed7d316c1bbe` |
| Tracked-file status | `0` changed paths |
| Reference host | `BYRON-HOME` |
| OS | Windows 11 Pro Insider Preview `10.0.26220`, build `26220` |
| CPU | AMD Ryzen 9 5950X, 16 cores, 32 logical processors |
| RAM | `68625825792` bytes from `Win32_ComputerSystem.TotalPhysicalMemory` |
| GPU | AMD Radeon RX 7900 XTX, driver `32.0.22029.1019` |
| GPU adapter RAM field | `4293918720` bytes from `Win32_VideoController.AdapterRAM`; raw CIM value only |
| Built shell evidence | `C:\ts\servo\target\debug\servoshell.exe`, `298702336` bytes, SHA-256 `B6625766D9952B01E1F178D61FEB2C342D37084B9AE813C16AB20211FAC69C2B`, modified `2026-07-17T18:17:34.7581979Z` |
| Turing repository role | documentation and registry update only |
| Commands | read-only `git`, `Get-CimInstance`, `Get-FileHash`, `Get-ChildItem`, `rg`, and file inspection |

The host is a useful named reference host. It is not yet a fixed-hardware benchmark laboratory because the report did not capture an owner-approved power plan, OS image, firmware and BIOS configuration, display refresh, thermal controls, driver freeze, Windows update policy, background-service policy, storage state, or replacement policy.

## Method

The analysis inspected:

1. the clean external Servo checkout and debug `servoshell.exe` identity;
2. Servo performance command entries in `python/servo/testing_commands.py`;
3. Servo page-load performance scripts and documentation under `etc/ci/performance/`;
4. Servo test fixture directories under `tests/blink_perf_tests`, `tests/dromaeo`, `tests/jquery`, and `tests/power`;
5. the Turing performance Blueprint, performance engineering book, benchmark-lab book, and `PB-013` performance benchmark readiness packet.

No Servo browser performance test was run. No Turing benchmark runner launched a browser. No raw timing, memory, frame pacing, process, energy, or trace samples were collected. No competitor browser was measured.

## Current Servo Performance Surface

Servo exposes several performance or benchmark-adjacent command paths.

| Surface | Observation | Turing implication |
|---|---|---|
| `mach test-perf` | Runs the page-load performance harness under `etc/ci/performance/` and writes JSON output under `etc/ci/performance/output/` | Useful upstream run surface, but not a Turing fixed-hardware run record |
| Page-load runner | `runner.py` loads a manifest, can output JSON or CSV, defaults to Servo or Gecko engine modes, and targets release `servoshell` for Servo runs | Needs adaptation because the current local build evidence is a debug `servoshell.exe`, and release/profile flags must be explicit |
| TP5-style manifest | `page_load_test/test.manifest` contained local `http://localhost/page_load_test/tp5n/...` page entries | Useful local-page shape, but corpus legality, representativeness, hashes, and disabled-case denominator remain unresolved |
| `test_all.sh` | Uses a reduced manifest rather than the full `tp5n/20160509.manifest` because some cases can time out | Any future run must publish the disabled and timeout denominator |
| Servo README warning | The Servo performance docs state that the test differs from Gecko Talos TP5 and cannot support Servo versus Gecko speed conclusions | Turing must preserve this no-comparison boundary |
| `test-dromaeo`, `test-speedometer`, `test-jquery` | Servo command layer includes these runner entry points | Synthetic suites are diagnostics only until compatibility, unsupported cases, suite versioning, and run artifacts are captured |
| `tests/power` | Power measurement scripts exist, but the README describes macOS PowerMetrics usage | Not sufficient for the Windows reference host energy baseline |

The page-load harness has a valuable structure for subtest repetition and result files, but it is not a decision-grade Turing benchmark pipeline. It does not by itself capture the full host manifest, ETW/WPR or equivalent traces, process topology, site-isolation state, memory categories, GPU allocation, power and thermal state, raw artifact hashes, competitor settings, or claim expiry.

## Fixture Inventory

The inspected checkout had the following benchmark-adjacent fixture surfaces:

| Path | Files | Bytes | Notes |
|---|---:|---:|---|
| `tests/blink_perf_tests` | 647 | 50730475 | Vendored Blink performance tests; provenance, license, and relevance need review before Turing use |
| `tests/dromaeo` | 1 | 3047 | Dromaeo runner support surface only |
| `tests/jquery` | 3 | 10332 | jQuery benchmark support surface only |
| `tests/power` | 2 | 7938 | macOS PowerMetrics-oriented power scripts |
| `etc/ci/performance/page_load_test/tp5n` | 1 | 4801 | Manifest file present in this checkout; TP5 page corpus itself was not present under this directory |

The Servo `test_perf.sh` path can download TP5N material, clone or update WARC test infrastructure, create a Python virtual environment, install packages, and submit to Perfherder when configured. That behavior is incompatible with Turing's no-claim fixed-hardware gate until inputs are vendored, mirrored, hash-pinned, or replaced by a reviewed local corpus and the network, dependency, credential, and artifact behavior is explicitly controlled.

## Required Source-Strategy Run Record

`ADR9-EV-014` needs a source-strategy performance run record that is stricter than the current Servo harness.

| Area | Required fields |
|---|---|
| Source and artifact | selected `ADR-0009` source baseline, binary path, binary hash, build profile, feature flags, JIT state, debug symbols, and package/native dependency state |
| Host | machine ID, OS image, patch level, CPU, cores, RAM, GPU, driver, display, storage, firmware, power plan, thermal state, update freeze, and background-service policy |
| Corpus | Turing-owned local corpus manifest, fixture hashes, legal/provenance notes, route map, disabled cases, unsupported cases, timeout policy, and comparison denominator |
| Network | loopback/static-server profile, DNS behavior, cache headers, TLS or non-TLS disclosure, protocol versions, proxy/authentication state, shaping policy, and server artifact hashes |
| Browser state | profile reset, cache state, viewport, device scale, extensions/plugins, agent state, accessibility state, devtools state, sandbox and site-isolation settings |
| Process and lifecycle | process count, process roles, site instance or origin mapping, active/background/frozen/discarded/BFCache states, page-protection reasons, crash/recovery behavior |
| Measures | cold and warm startup, navigation stages, input latency, frame pacing, CPU time, wakeups, private working set, resident memory, committed memory, shared memory, compressed/swap state, GPU allocation, disk/cache bytes, and energy/power data |
| Raw artifacts | manifest JSON, raw samples, ETW/WPR or equivalent traces, logs, screenshots or visual hashes, memory snapshots, process tree, GPU data, power data, failure records, and SHA-256 artifact index |
| Statistics | repetitions, warmup policy, outlier policy, median, p95/p99 where applicable, confidence or variance, failure denominator, flakiness policy, and rerun trigger |
| Claims | exact no-claim or claim label, unsupported conclusions, expiration date, owner approval, and equal-security/equal-workload disclosure for any comparison |

## Turing Harness Relationship

The existing `PB-013` no-claim harness material remains the right foundation for Turing's pipeline, but it is not enough for `ADR9-EV-014` yet.

Current Turing-side evidence provides:

- benchmark manifest schema and sample shape;
- checked Tier H current-host benchmark hardware candidate;
- checked current-host OS-control candidate;
- no-claim corpus schema and expanded generated local fixtures;
- no-claim local static network profile and validator;
- checked resource-attribution schema and semantic owner taxonomy;
- static-server self-test and hardware/OS-control/resource-attribution-linked no-claim smoke runner artifact package;
- claim discipline in the performance Blueprint, performance engineering book, and benchmark-lab book;
- Chrome-class competitor comparison and claim-expiry runbook;
- explicit no-claim metadata in the benchmark manifest schema and sample.

Missing Turing-side evidence includes:

- Tier L and Tier M fixed hardware inventories, owner-approved Tier H clean-image or replacement decision, approved update/driver/firmware/display/thermal/time/network/artifact-storage controls, and clean OS image manifests;
- a representative local performance corpus;
- a browser-launch runner with sample control, cache/profile control, timeout and failure capture;
- runner-generated raw artifacts from Servo, Turing prototypes, or competitors;
- ETW/WPR or equivalent traces;
- browser-emitted memory and GPU accounting snapshots using the checked semantic owner taxonomy;
- process and site-isolation disclosure;
- energy or power data;
- pinned competitor version manifests and actual equal-workload comparison runs;
- owner-reviewed claim bundles generated from real results.

## Inference

The evidence moves `ADR9-EV-014` from missing to partial. The project now has a named reference host, a hashed debug Servo artifact, a mapped Servo performance command surface, fixture inventory, and a concrete run-record checklist. It still lacks every measurement artifact required for a performance, memory, energy, or comparison conclusion.

## Unsupported Conclusions

This report does not show:

- Servo startup time;
- Servo page-load time;
- Servo memory use;
- Servo energy use;
- Servo frame pacing or input latency;
- Turing performance, memory, or energy behavior;
- Chrome, Edge, Firefox, Safari, WebKit, Gecko, Ladybird, or BrowserBench comparison results;
- that Servo's TP5-style page-load harness is acceptable for Turing claims;
- that the Windows host is an approved fixed-hardware lab machine;
- that the debug `servoshell.exe` artifact represents a release or optimized build.

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
- [Performance engineering book](../performance/README.md);
- [Benchmark laboratory book](../benchmark-lab/README.md).

It does not change source code, dependency approvals, security ledgers, benchmark schemas, benchmark fixtures, public claims, or the blocked status of `PB-002`.
