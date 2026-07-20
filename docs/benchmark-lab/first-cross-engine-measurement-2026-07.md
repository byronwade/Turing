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

## Corpus extension (same day)

Three further fixtures joined the corpus, each stressing a different engine
path, all inside the implemented subset: `blocks-150.html` (150 stacked
margined blocks), `selectors-120.html` (120 class rules over 120 elements),
and `text-30x120.html` (30 paragraphs of 120 words, exercising word-level
line breaking). Same method: five cold Turing processes per fixture
(medians of `load` + `display_list`), Chrome DevTools traces of the same
files (two for `blocks-150`, one each for the others — a stated
under-sampling to grow before any stronger wording is used).

| Fixture | Turing comparable span | Chrome comparable span | Ratio |
| --- | --- | --- | --- |
| bench-fixture | 155 µs | ~1,003 µs | ~6.5x |
| blocks-150 | ~1,095 µs | ~3,976–5,694 µs | ~3.6–5.2x |
| selectors-120 | ~1,218 µs | ~6,164 µs | ~5.1x |
| text-30x120 | ~1,599 µs | ~3,552 µs | ~2.2x |

The licensed sentence widens to: on this four-fixture corpus, on this
machine, Turing's cold comparable span ran roughly **2x to 6x faster** than
Chrome's equivalent main-thread events, with the narrowest margin on
text-heavy content — where Chrome's text machinery is most optimised and
Turing allocates one fragment box per placed word. That narrowing is the
most useful datum in the table: it says where optimisation attention goes
if the corpus keeps growing this direction. Every scope limit from the
single-fixture section applies unchanged.

## Growing this into the real lane

Each step is already specified by this book: a corpus beyond one fixture
(02), thermal and power control (01), startup and input latency (03), frame
pacing (04), the statistics protocol and claim gates (07). The marginal
value of this record is that the harness now exists end to end: fixture in
the corpus, a cold-load probe in the engine, a trace-extraction recipe, and
a results format whose scope limits are part of the result.
