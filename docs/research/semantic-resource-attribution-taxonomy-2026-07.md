# Semantic Resource Attribution Taxonomy - July 2026

Status: `PB-013` resource-attribution evidence draft; no instrumentation, benchmark result, or performance claim
Owner: performance measurement, memory architecture, benchmark operations, developer experience, product experience, and release operations
Research date: 2026-07-17
Confidence: high for taxonomy coverage against current Turing documents; medium for source alignment; low for implementation readiness until browser traces, platform counters, shared-resource charging, UI reporting, and raw artifacts exist

## Question

Which semantic owner taxonomy should Turing use before claiming memory, CPU, GPU, energy, wakeup, model, or 30-tab resource advantages over Chrome-class browsers?

## Inputs

Machine-readable records:

- [Benchmark resource-attribution schema](../blueprint-v1/machine/benchmark-resource-attribution.schema.json)
- [Semantic owner taxonomy](../blueprint-v1/machine/benchmark-resource-attribution/semantic-owners.v1.json)
- [Benchmark resource-attribution validator](../../tools/validate_benchmark_resource_attribution.py)
- [Benchmark manifest schema](../blueprint-v1/machine/benchmark-manifest.schema.json)
- [No-claim benchmark manifest sample](../blueprint-v1/machine/benchmark-manifests/no-claim-runner-smoke.sample.json)
- [Benchmark manifest validator](../../tools/validate_benchmark_manifests.py)
- [Benchmark smoke runner](../../tools/run_benchmark_smoke.py)
- [Performance Benchmark Readiness Packet - July 2026](performance-benchmark-readiness-packet-2026-07.md)

Internal design inputs:

- [Blueprint 09 - Performance, Memory, Energy, and the 30-Tab Contract](../blueprint-v1/09-performance-memory.md)
- [Memory, Allocation, and Cache Policy](../performance/02-memory-allocation-and-cache-policy.md)
- [Observability, Tracing, and Replay](../developer-experience/03-observability-tracing-and-replay.md)
- [Resource Manager, Lifecycle, and Recovery](../product-experience/04-resource-manager-lifecycle-and-recovery.md)

External primary sources checked on 2026-07-17:

- Chromium [MemoryInfra](https://chromium.googlesource.com/chromium/src/+/master/docs/memory-infra/)
- Chromium [adding MemoryInfra tracing to a component](https://www.chromium.org/developers/how-tos/trace-event-profiling-tool/memory/howto-adding-memory-infra-tracing-to-a-component/)
- Perfetto [tracing documentation](https://perfetto.dev/docs/)
- Perfetto [memory counters and events](https://perfetto.dev/docs/data-sources/memory-counters)
- Perfetto [GPU tracing](https://perfetto.dev/docs/data-sources/gpu)
- Chrome DevTools [Performance monitor](https://developer.chrome.com/docs/devtools/performance-monitor)
- Microsoft Learn [Introduction to Windows Performance Recorder](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr)

These sources define measurement patterns and constraints. They do not prove that Turing emits compatible traces, has memory attribution, or can compare resource use against any browser.

## Taxonomy

The registry defines these semantic owner classes:

1. `browser-ui-profile`
2. `document-frame-site-instance`
3. `javascript-heap-code-metadata`
4. `dom-style-layout-paint-accessibility`
5. `images-fonts-canvas-media`
6. `network-buffers-cache`
7. `storage-transactions-mappings`
8. `gpu-textures-buffers-pipelines`
9. `extension`
10. `devtools`
11. `agent-model`
12. `shared-service`
13. `unknown`

The taxonomy deliberately keeps `unknown` as a first-class owner. A report that hides unknown memory, CPU, GPU, energy, or wakeup cost cannot support an extreme-performance claim.

## Metrics

The first taxonomy includes:

- CPU: `cpu_time_ns`, `queue_wait_ns`, `wakeups`;
- memory: `private_working_set_bytes`, `resident_bytes`, `committed_bytes`, `shared_bytes`, `compressed_bytes`, `swap_bytes`;
- GPU: `gpu_allocated_bytes`;
- I/O: `network_bytes`, `disk_io_bytes`;
- energy: `energy_estimate_joules`;
- agent cost: `model_tokens`, `provider_cost_estimate`.

The metrics distinguish physical totals from charged views. Shared resources must appear once in physical totals and separately in charged owner views under a documented proportional or first-owner policy.

## Required Trace Contract

A browser trace that claims resource attribution must carry at least:

- monotonic timestamp;
- process, thread, and task identity;
- profile, site, frame, and document epoch;
- owner class;
- resource metric;
- value;
- confidence.

This mirrors the project-wide rule that performance claims must preserve profile, site, frame, process, document-epoch, lifecycle, and resource-owner identity across boundaries.

## Interpretation

This taxonomy partially advances `PB13-EV-011` because it names owner classes, metrics, shared-resource rules, trace fields, and reporting rules in a checked registry. It does not complete `PB13-EV-011`, because no Turing browser emits these events, no benchmark runner collects platform counters by semantic owner, no shared GPU accounting exists, and no UI/report fixture demonstrates the physical-versus-charged views.

The no-claim benchmark manifest sample and smoke runner now carry `TURING.BENCHMARK.RESOURCE_ATTRIBUTION.SEMANTIC_OWNERS.2026_07` for traceability. That link is useful for runner development. It is not instrumentation and does not create memory, CPU, GPU, energy, or wakeup results.

## Unsupported Conclusions

This record does not show:

- any measured Turing memory, CPU, GPU, energy, wakeup, or model cost;
- any per-tab or per-process resource attribution;
- any platform trace reconciled to the owner model;
- any shared-resource charging implementation;
- any GPU accounting implementation;
- any user or developer resource UI;
- any Chrome, Edge, Firefox, Safari, Servo, Ladybird, or Turing comparison;
- any lower-memory, lower-energy, fastest, Chrome-class, or extreme-performance claim.

## Remaining Gaps

The taxonomy cannot support decision-grade resource claims until these are added:

- trace event schema carrying `owner_class` and stable principal IDs;
- per-process and per-tab memory collection;
- shared-resource charging implementation and validation;
- GPU allocation accounting and fallback disclosure;
- CPU, wakeup, I/O, and energy attribution by owner;
- unknown-bucket reduction threshold and waiver policy;
- user/developer report fixture showing physical and charged views;
- runner-generated raw artifacts using this `resource_attribution_id`;
- independent review before any memory, energy, or performance claim.

## Readiness Impact

`PB-013` remains `documented_no_runner`. `PB13-EV-011` moves from missing to partial taxonomy evidence. The fixed-hardware lab still lacks real instrumentation, browser-run artifacts, traces, and report fixtures.

## Next Actions

1. Add a trace-event schema for resource-owner samples and counters.
2. Define unknown-bucket thresholds that block performance claims.
3. Add runner output fields for `resource_attribution_id` and raw owner-counter artifacts.
4. Create a static report fixture that shows physical memory, charged memory, shared memory, GPU memory, wakeups, energy estimates, and unknown resources by owner.
5. Validate the taxonomy against the first browser-launch runner output once a browser runner exists.
