# Benchmark Server Lifecycle Self-Test - July 2026

Status: `PB13-EV-004` no-claim server lifecycle evidence; no browser run, benchmark result, latency result, cache result, TLS result, DNS result, or performance claim
Owner: performance measurement, benchmark operations, quality, security, privacy, and release operations
Research date: 2026-07-18
Confidence: high for runner-managed lifecycle self-test coverage; low for benchmark-run network readiness until browser-run server evidence and richer network profiles exist

## Question

Can Turing produce a checked runner-managed server startup, route-check, shutdown, and artifact-hash package before browser benchmark execution exists?

## Inputs

- [Performance benchmark readiness packet](performance-benchmark-readiness-packet-2026-07.md)
- [Benchmark laboratory corpus, servers, and network-control chapter](../benchmark-lab/02-corpus-servers-and-network-control.md)
- [No-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json)
- [Benchmark network profile validator](../../tools/validate_benchmark_network_profile.py)
- [Benchmark profile server](../../tools/serve_benchmark_profile.py)
- [Benchmark server lifecycle self-test](../../tools/run_benchmark_server_profile.py)

## Method

Added `tools/run_benchmark_server_profile.py --self-test` as a runner-owned lifecycle wrapper around the checked no-claim network profile server. The tool loads the validated network profile, starts the local HTTP/1.1 loopback server on an ephemeral port, checks each configured route with the `turing.invalid` Host header, shuts the server down, verifies the port no longer accepts the test connection, and writes a hashed artifact package.

The artifact package contains:

- `server-startup.json`;
- `route-checks.json`;
- `server-shutdown.json`;
- `runner-summary.json`;
- `artifact-index.json`.

The runner emits `NOCLAIM.NETWORK_PROFILE_SERVER_RUN.2026_07` with `server_started=true`, `server_shutdown=true`, `browser_launched=false`, `benchmark_result_generated=false`, `external_network_used=false`, and `dns_os_modified=false`.

## Current Evidence

The following evidence now exists:

- the no-claim local static network profile validates with route-to-corpus coverage, loopback-only serving, Host-header DNS behavior, no-store cache headers, and disabled external network access;
- `serve_benchmark_profile.py --self-test` still provides the static-server route self-test;
- `run_benchmark_server_profile.py --self-test` provides checked runner-managed server lifecycle self-test evidence with startup, route checks, shutdown, artifact hashes, and no-claim finalization;
- `PB-013`, the benchmark research lane, and `TASK-000005` point to the server lifecycle self-test as planning evidence.

This closes the previous no-claim lifecycle gap where `PB13-EV-004` had a static server self-test and smoke-runner package but no checked runner-managed server-start/stop artifact package.

## Unsupported Conclusions

This record does not support:

- a browser-run server artifact;
- DNS resolver modification proof outside the self-test Host header;
- TLS, HTTP/2, HTTP/3, proxy, authentication, cache-revalidation, service-worker, latency, loss, or bandwidth-shaping evidence;
- a browser launch, page load, benchmark sample, trace, memory snapshot, power sample, competitor run, or raw benchmark result;
- any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, beta, stable, accessibility, security, compatibility, benchmark-ready, or performance claim.

## Remaining Proof For `PB13-EV-004`

`PB13-EV-004` remains partial until the benchmark runner produces:

1. browser-run server evidence tied to a real run manifest;
2. DNS execution proof or an equivalent reviewed host-mapping mechanism outside the self-test Host header;
3. TLS certificate profile and HTTP/2, HTTP/3 or QUIC profile decisions;
4. proxy, authentication, cache-revalidation, service-worker, and network-shaping profiles where required by the reviewed corpus;
5. server logs, route maps, startup/shutdown records, cleanup records, artifact hashes, and failure records retained in a real benchmark artifact package.

## Registry Impact

This report advances `PB13-EV-004` from static-server self-test evidence to checked runner-managed server lifecycle self-test evidence. It does not move `PB-013` out of `documented_no_runner`.

Synchronized records:

- `pre-build-readiness.json` now lists the server lifecycle runner as `PB-013` evidence while keeping browser-run server evidence and richer network profiles as missing proof.
- `research-readiness-crosswalk.json` and `build-readiness-task-queue.json` now route the benchmark lane and `TASK-000005` through the checked server lifecycle self-test.
- The performance benchmark readiness packet, research index, repository map, benchmark laboratory, performance book, operating board, and documentation-readiness matrix now link the server lifecycle self-test.

## Next Actions

1. Add benchmark-run server artifacts to the eventual browser benchmark runner output.
2. Decide the reviewed DNS-host-mapping mechanism for benchmark runs.
3. Add TLS, HTTP/2, HTTP/3 or QUIC, proxy, authentication, cache-revalidation, and network-shaping profile contracts where the expanded corpus requires them.
4. Keep every server lifecycle artifact labeled no-claim until real benchmark-run evidence and owner review exist.
