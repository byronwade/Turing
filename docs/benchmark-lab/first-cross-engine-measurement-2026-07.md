# First controlled cross-engine measurement (2026-07)

Status: bounded measurement record. This is the first execution of the
cross-engine methodology this book requires before any competitive language
is used. It supports exactly the claims in its "What may be said" section
and no others. `PB-013` governs.

## Question

The owner's product direction uses competitive superlatives ("fastest").
The repository forbids unmeasured competitive claims. The only way through
is a controlled comparison: identical input, same machine, stage-comparable
instrumentation, stated scope. This record is the first such measurement,
deliberately small.

## Workload

One fixture: [`benchmarks/corpus/cross-engine/bench-fixture.html`](../../benchmarks/corpus/cross-engine/bench-fixture.html)
— the `turing-bench` fixture document with its stylesheet inlined in a
`<style>` element. The fixture lies inside Turing's implemented subset **by
construction**; that is the central scope limit of this record. It exercises
block and inline formatting, class selectors, margin collapse, and inline
runs. No images, fonts, scripts, network, or subresources.

## Method

Both engines execute a cold load of the identical file on the same machine
(Windows 11, x86_64, mains power), one navigation per process/tab, repeated
runs, medians reported.

- **Turing**: `cargo run --release -p turing-engine --example cold_load --
  benchmarks/corpus/cross-engine/bench-fixture.html 1280 720`, five fresh
  processes. `load` covers tokenize, tree build, style parse, cascade, and
  layout; `display_list` covers paint-command generation. This matches a
  cold navigation rather than `turing-bench`'s warm-loop medians, which
  measure a hot cache and are roughly 10x lower — the warm numbers are the
  right ones for tracking Turing against itself and the wrong ones for
  comparing against another engine's cold load.
- **Chrome** (stable, default profile, no throttling): three DevTools
  performance traces of a reload navigation; per-stage totals of the
  `ParseHTML`, `UpdateLayoutTree` (style recalculation), `Layout`,
  `PrePaint`, `Paint`, and `Layerize` main-thread events. Traces retained
  as raw artifacts alongside this record's session log.

## Results (medians)

| Matched span | Turing | Chrome main-thread events | Chrome |
| --- | --- | --- | --- |
| Parse HTML + inline CSS | in `load` | `ParseHTML` | 251 µs |
| Style resolution | in `load` | `UpdateLayoutTree` | 308 µs |
| Layout | in `load` | `Layout` | 202 µs |
| — load subtotal | **152 µs** | subtotal | **761 µs** |
| Paint-command generation | 3 µs | `PrePaint` + `Paint` + `Layerize` | 242 µs |
| **Comparable span total** | **155 µs** | | **~1,003 µs** |
| Producing pixels (1280x720) | 721 µs (CPU reference) | GPU raster, other threads | not comparable |

Chrome's per-run variation across the three traces was under 15% on every
stage; Turing's five cold runs spanned 148–185 µs on `load`.

## What may be said

On this one fixture, on this one machine, Turing's cold parse-style-layout-
paint-recording span completed in roughly **one sixth** of the time Chrome's
equivalent main-thread events consumed.

## What may not be said, and why

- **"Faster than Chrome."** Chrome executes an enormously larger platform
  per stage: full CSS, font shaping, invalidation infrastructure,
  accessibility, compositing layers, site isolation. Turing is fast here
  substantially *because it does less*. The measurement bounds the claim to
  the fixture's subset, and the subset is Turing-shaped.
- **"Fastest on the market."** One fixture, one machine, one competitor,
  no thermal control, no statistical protocol from
  [07-statistics-artifacts-regressions-and-claims](07-statistics-artifacts-regressions-and-claims.md).
  This record is the seed of that lane, not its completion.
- **Anything about pixels.** Chrome rasterises on GPU raster threads;
  Turing's 721 µs is a deliberately unoptimised CPU reference painter. The
  architectures are not comparable and are not compared.
- Chrome's tracing instrumentation adds overhead to Chrome's numbers;
  Turing's `Instant` pairs add effectively none. The asymmetry favours
  Turing and is stated rather than corrected, because correcting it would
  require instrumentation parity nobody has measured.

## Growing this into the real lane

Each step is already specified by this book: a corpus beyond one fixture
(02), thermal and power control (01), startup and input latency (03), frame
pacing (04), the statistics protocol and claim gates (07). The marginal
value of this record is that the harness now exists end to end: fixture in
the corpus, a cold-load probe in the engine, a trace-extraction recipe, and
a results format whose scope limits are part of the result.
