# Benchmark Corpus Expansion - July 2026

Status: `PB13-EV-003` no-claim corpus-shape evidence; no browser run, benchmark result, compatibility result, accessibility result, service-worker result, media result, or performance claim
Owner: performance measurement, benchmark operations, accessibility, internationalization, security, quality, and release operations
Research date: 2026-07-18
Confidence: high for generated local fixture and route coverage; low for benchmark readiness until the corpus is reviewed, representative, browser-run, and tied to raw artifacts

## Question

Can Turing expand the no-claim offline corpus beyond the two-case seed while preserving local-only provenance, checked hashes, route coverage, and no-claim boundaries?

## Inputs

- [Performance benchmark readiness packet](performance-benchmark-readiness-packet-2026-07.md)
- [Benchmark laboratory corpus, servers, and network-control chapter](../benchmark-lab/02-corpus-servers-and-network-control.md)
- [No-claim smoke corpus manifest](../blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json)
- [No-claim local static network profile](../blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json)
- [Benchmark corpus validator](../../tools/validate_benchmark_corpus.py)
- [Benchmark network profile validator](../../tools/validate_benchmark_network_profile.py)

## Method

Expanded the no-claim corpus manifest from two generated local fixtures to seven generated local fixtures. The manifest now requires category coverage for:

- `static_document`;
- `app_like`;
- `accessibility`;
- `international_text`;
- `hostile_markup`;
- `media_document`;
- `service_worker_contract`.

Added generated local HTML fixtures for accessibility/form semantics, international text and bidirectional content, bounded hostile-markup shape, media/document placeholders, and a service-worker contract placeholder. Each case records a stable case ID, category, entry path, `turing.invalid` top-level site, SHA-256 digest, byte count, generated-content license note, expected M0 unsupported behavior, disabled external network access, and disabled measurement claims.

The service-worker fixture checks only the local JavaScript API surface. It does not register a worker, open Cache Storage, intercept fetch, or produce compatibility evidence.

## Current Evidence

The following evidence now exists:

- the corpus schema and validator require all seven no-claim fixture categories;
- all generated fixture files are under `benchmarks/corpus/no-claim-smoke/`;
- fixture byte counts and SHA-256 hashes are checked by `tools/validate_benchmark_corpus.py`;
- fixture text is checked for LF line endings and blocked external URL references;
- the local static network profile maps every corpus case to a loopback route;
- `tools/validate_benchmark_network_profile.py`, `tools/serve_benchmark_profile.py --self-test`, and `tools/run_benchmark_server_profile.py --self-test` can check the expanded route set before any browser run exists.

This improves `PB13-EV-003` from a two-fixture seed to an expanded no-claim smoke corpus. It does not make the corpus reviewed, representative, benchmark-ready, compatibility-ready, accessibility-ready, or production-ready.

## Unsupported Conclusions

This record does not support:

- a representative web, app, accessibility, media, hostile-input, service-worker, or international corpus;
- WPT, Test262, BrowserBench, Web Vitals-style, accessibility, media, service-worker, or hostile-input conformance evidence;
- a browser launch, page load, page render, JavaScript result, worker registration, cache result, media decode result, accessibility tree result, trace, memory snapshot, power sample, competitor run, raw benchmark result, or compatibility result;
- any faster, lower-memory, lower-energy, Chrome-class, daily-driver, production, beta, stable, accessibility, security, compatibility, benchmark-ready, or performance claim.

## Remaining Proof For `PB13-EV-003`

`PB13-EV-003` remains partial until the benchmark program produces:

1. a reviewed corpus-selection policy with inclusion, exclusion, legal, privacy, disabled-case, and timeout rules;
2. a representative offline corpus with page, application, accessibility, media, hostile-input, service-worker, international, recovery, DevTools, and agent-workload cases;
3. route maps, hashes, generated-source or licensed-source provenance, and disabled-case denominators for every case;
4. browser-run evidence that records load, failure, unsupported behavior, artifacts, and cleanup for every case;
5. owner-reviewed corpus changes tied to benchmark-run manifests and raw artifact packages.

## Registry Impact

This report advances `PB13-EV-003` from a two-case no-claim seed to an expanded no-claim smoke corpus. It does not move `PB-013` out of `documented_no_runner`.

Synchronized records:

- `pre-build-readiness.json` now lists the added fixtures and this report as `PB-013` evidence while keeping the reviewed representative corpus as missing proof.
- `research-readiness-crosswalk.json` and `build-readiness-task-queue.json` now route the benchmark lane and `TASK-000005` through the expanded corpus evidence.
- The performance benchmark readiness packet, research index, repository map, benchmark laboratory, performance book, operating board, and documentation-readiness matrix now distinguish the expanded no-claim smoke corpus from the still-missing reviewed representative corpus.

## Next Actions

1. Convert the expanded no-claim seed into a reviewed corpus-selection policy.
2. Add browser-run fixture evidence only after the launch runner and artifact package controls exist.
3. Add active service-worker, cache-revalidation, media, accessibility-tree, hostile-input, and internationalization test cases only with explicit route, storage, privacy, timeout, and cleanup rules.
4. Keep every corpus artifact labeled no-claim until real benchmark-run evidence and owner review exist.
