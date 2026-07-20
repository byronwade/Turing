# Performance Baselines

Raw per-stage timings for the rendering pipeline, produced by `turing-bench`.

```
cargo run --release -p turing-bench
```

## What these numbers are for

`PB-013` forbids any performance claim that is not backed by measurement. This
file is where the measurement lives, so that a claim can point at something.

They are for tracking this engine against its own past. **No comparison against
another engine is stated or implied.** There is no comparison data — producing a
Turing number next to a Chrome number without a controlled methodology, matched
hardware, and matched input would be a fabricated comparison, which is exactly
what `PB-013` exists to prevent.

## What these numbers are not

Wall-clock timings on one developer machine. They move with CPU frequency
scaling, background load, and allocator state. A few percent between runs is
noise. They are deliberately **not** wired into any validator: a noisy
measurement used as a gate produces flaky failures and teaches people to ignore
it.

The fixture is a small hand-written document, not a captured real page. A real
page would exercise constructs this engine refuses by design, so the run would
be timing error paths. The fixture should grow as the engine does — **when it
changes, these baselines reset and earlier numbers stop being comparable.**
Record that in `docs/research-log.md` when it happens.

## Method

Borrowed from criterion, not the crate — the workspace takes no external
dependencies. Per stage: 20 warm-up iterations discarded, then 100 recorded.
Results are order statistics rather than a mean, because a mean is dragged
around by a single scheduling hiccup. `std::hint::black_box` guards each stage's
output so the optimiser cannot delete work whose result is unused.

Minimum is the most stable figure across runs, being the iteration least
contaminated by unrelated load. A maximum far above the median usually indicates
an allocation or a vector growth step rather than measurement noise.

## Baselines

Recorded 2026-07-20. Release build.

| Stage | Min | Median | Max |
| --- | --- | --- | --- |
| tokenize | 6.9 µs | 7.1 µs | 7.6 µs |
| tree-build | 2.5 µs | 2.6 µs | 2.8 µs |
| parse-css | 4.5 µs | 4.7 µs | 4.9 µs |
| cascade | 3.4 µs | 3.5 µs | 3.9 µs |
| layout | 5.2 µs | 6.4 µs | 21.9 µs |

Environment: Windows 11, `x86_64-pc-windows-msvc`, release profile. Absolute
figures are not portable across machines; the shape of the distribution and the
relative cost of the stages are the parts worth reading.

Two observations, recorded without acting on them yet:

- Tokenizing costs more than tree construction and layout individually. It is
  the stage that touches every input byte, so this is expected rather than
  anomalous, but it is where optimisation effort would pay first.
- Layout's maximum sits well above its median while every other stage is tight.
  That asymmetry is consistent with allocation during box-tree construction. It
  is a hypothesis, not a finding — confirming it needs allocation profiling that
  does not exist yet.

## Footprint

The other half of the mandate, and the part measurable without ambiguity today.

| Measure | Value |
| --- | --- |
| External dependencies (whole workspace) | 0 |
| `turing-shell` release binary | 177,152 bytes (173 KiB) |

Dependency count is exact and verifiable: `Cargo.lock` contains only
workspace-local packages. Binary size is from the release profile as currently
configured, with no size-oriented flags (`opt-level = "z"`, LTO, panic=abort)
applied — those are available and untried, so this figure is an upper bound
rather than a tuned result.

Neither figure supports a claim about a finished browser. The shell does not yet
contain a renderer, networking, or a JavaScript heap wired to the DOM. What can
honestly be said today is that the engine crates carry no third-party code.
